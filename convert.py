import zarr
import shutil
import pandas as pd
import h5py
import xarray as xr
import numpy as np
from pathlib import Path
import argparse
import typing as t
from abc import abstractmethod
from dataclasses import dataclass

TIME_AXES = ["t", "time1"]


class Task:

    def __call__(self, *args: t.Any, **kwds: t.Any) -> t.Any:
        return self.run(*args, **kwds)

    @abstractmethod
    def run(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        raise NotImplementedError()


class LoadSignals(Task):

    def __init__(self, shot_file: str, signals: list[str]) -> None:
        super().__init__()
        self.shot_file = shot_file
        self.channels = signals

    def run(self) -> dict[str, xr.Dataset]:
        datasets = {
            name: xr.open_dataset(self.shot_file, group=name) for name in self.channels
        }
        return datasets


class StandardiseNames(Task):

    def __init__(self) -> None:
        super().__init__()
        self.TIME_ALIASES = ["t", "time1"]

    def run(self, ds: xr.Dataset) -> xr.Dataset:
        for name in self.TIME_ALIASES:
            if name in ds:
                ds = ds.rename({name: "time"})
        return ds


class CombineChannels(Task):

    def __init__(self, channels: list[str]) -> None:
        super().__init__()
        self.channels = channels

    def run(self, datasets: dict[str, xr.Dataset]) -> xr.Dataset:
        channel_datasets = [datasets[channel] for channel in self.channels]
        name = channel_datasets[0].attrs["name"]
        ds = xr.combine_nested(
            channel_datasets, concat_dim="channel", combine_attrs="drop_conflicts"
        )
        name = "/".join(name.split("/")[:-1])
        ds.attrs["name"] = name
        return ds


class CropFilledDataset(Task):

    def run(self, dataset: xr.Dataset) -> xr.Dataset:
        fill_value = np.max(dataset.data)
        max_index = np.max(np.argmax(dataset.data.values, axis=1))
        dataset = dataset.sel(dim_0=dataset.dim_0[:max_index])
        dataset.data.values[dataset.data == fill_value] = np.nan
        return dataset


class AddCameraParameters(Task):

    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path

    def run(self, dataset: xr.Dataset) -> xr.Dataset:
        cam_data = pd.read_csv(self.path)
        cam_data.drop("name", inplace=True, axis=1)
        cam_data.drop("comment", inplace=True, axis=1)
        cam_data.index.name = "channel"
        cam_data = cam_data.to_xarray()
        dataset = xr.merge([dataset, cam_data], combine_attrs="drop_conflicts")
        return dataset


class XSXCameraTransform(Task):

    def __init__(self, loader: LoadSignals, params_file: str) -> None:
        super().__init__()
        self.loader = loader
        self.combiner = CombineChannels(loader.channels)
        self.add_params = AddCameraParameters(params_file)

    def run(self):
        datasets = self.loader.run()
        dataset = self.combiner(datasets)
        dataset = self.add_params(dataset)
        return dataset


class EFM_LCFSTransform(Task):

    def __init__(self, loader: LoadSignals) -> None:
        super().__init__()
        self.loader = loader
        self.cropper = CropFilledDataset()

    def run(self):
        datasets = self.loader()

        r = self.cropper(datasets["efm/lcfsr_c"])
        z = self.cropper(datasets["efm/lcfsr_c"])

        r = r.rename(dict(data="r"))
        z = z.rename(dict(data="z"))
        r = r.drop("error")
        z = z.drop("error")

        lcfs = xr.merge([r, z])
        lcfs = lcfs.rename_dims(dict(dim_0="coordinates"))

        return lcfs


def standardise_names(ds: xr.Dataset) -> xr.Dataset:
    for name in TIME_AXES:
        if name in ds:
            print(ds.attrs["name"])
            ds = ds.rename({name: "time"})
    return ds


def combine_channels(
    datasets: dict[str, xr.Dataset], channels: list[str]
) -> xr.Dataset:
    channel_datasets = [datasets[channel] for channel in channels]
    name = channel_datasets[0].attrs["name"]
    ds = xr.combine_nested(
        channel_datasets, concat_dim="channel", combine_attrs="drop_conflicts"
    )
    name = "/".join(name.split("/")[:-1])
    ds.attrs["name"] = name
    return ds


def load_signals(shot_file: str, channels: list[str]):
    return {name: xr.open_zarr(shot_file, group=name) for name in channels}


def remove_channels(datasets: dict[str, xr.Dataset], channels: list[str]):
    for channel in channels:
        datasets.pop(channel)


def convert_lcfs(datasets: dict[str, xr.Dataset]):
    crop_dataset(datasets, "efm/lcfsr_c")
    crop_dataset(datasets, "efm/lcfsz_c")
    r = datasets["efm/lcfsr_c"].rename(dict(data="r"))
    z = datasets["efm/lcfsz_c"].rename(dict(data="z"))
    r = r.drop("error")
    z = z.drop("error")
    lcfs = xr.merge([r, z])
    lcfs = lcfs.rename_dims(dict(dim_0="coordinates"))
    datasets["efm/lcfs"] = lcfs
    remove_channels(datasets, ["efm/lcfsr_c", "efm/lcfsz_c"])


def convert_to_hdf(path: str):
    path = Path(path)
    out_path = path.with_suffix(".h5")
    source = zarr.open_group(path, mode="r")
    dest = h5py.File(out_path, mode="w")
    zarr.copy_all(source, dest, without_attrs=True)


def crop_dataset(datasets: dict[str, xr.Dataset], channel: str):
    dataset = datasets[channel]
    fill_value = np.max(dataset.data)
    max_index = np.max(np.argmax(dataset.data.values, axis=1))
    dataset = dataset.sel(dim_0=dataset.dim_0[:max_index])
    dataset.data.values[dataset.data == fill_value] = np.nan
    datasets[channel] = dataset


def add_camera_parameters(datasets: dict[str, xr.Dataset], channel: str, path: str):
    cam_data = pd.read_csv(path)
    cam_data.drop("name", inplace=True, axis=1)
    cam_data.drop("comment", inplace=True, axis=1)
    cam_data.index.name = "channel"
    cam_data = cam_data.to_xarray()
    datasets[channel] = xr.merge(
        [datasets[channel], cam_data], combine_attrs="drop_conflicts"
    )


def write_zarr(datasets: dict[str, xr.Dataset], file_name: str):
    if file_name.exists():
        shutil.rmtree(file_name)

    for key, dataset in datasets.items():
        dataset.to_zarr(file_name, group=key, mode="w")

    zarr.consolidate_metadata(file_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    convert_to_hdf(args.path)
