import pytest
import xarray as xr
import convert as t
from pathlib import Path


@pytest.fixture()
def shot_file():
    return Path("~/data/tiny/30420.zarr").expanduser()


def test_load_signals(shot_file):
    loader = t.LoadSignals(shot_file, ["amc/plasma_current"])
    datasets = loader.run()
    assert isinstance(datasets, dict)
    assert isinstance(datasets["amc/plasma_current"], xr.Dataset)


def test_standardise_names(shot_file):
    loader = t.LoadSignals(shot_file, ["xdc/ip_t_ipref"])
    datasets = loader.run()

    standardizer = t.StandardiseNames()
    for name, dataset in datasets.items():
        datasets[name] = standardizer.run(dataset)

    dims = list(datasets["xdc/ip_t_ipref"].dims.keys())
    assert dims == ["time"]


def test_combine_channels(shot_file):
    hcam_u_channels = [
        "xsx/hcam_u_1",
        "xsx/hcam_u_2",
        "xsx/hcam_u_3",
    ]

    loader = t.LoadSignals(shot_file, hcam_u_channels)
    datasets = loader.run()

    standardizer = t.StandardiseNames()
    for name, dataset in datasets.items():
        datasets[name] = standardizer.run(dataset)

    combiner = t.CombineChannels(hcam_u_channels)
    dataset = combiner.run(datasets)

    dims = list(dataset.dims.keys())
    assert dims == ["channel", "time"]
    assert dataset.attrs["name"] == "/XSX/HCAM/U"


def test_crop_dataset(shot_file):
    signals = [
        "efm/lcfsr_c",
    ]
    loader = t.LoadSignals(shot_file, signals)
    datasets = loader.run()

    cropper = t.CropFilledDataset()
    dataset = cropper.run(datasets[signals[0]])

    assert dataset.data.shape == (
        53,
        147,
    )


def test_apply_camera_parameters(shot_file):
    tcam_channels = [
        "xsx/tcam_1",
        "xsx/tcam_2",
        "xsx/tcam_3",
        "xsx/tcam_4",
        "xsx/tcam_5",
        "xsx/tcam_6",
        "xsx/tcam_7",
        "xsx/tcam_8",
        "xsx/tcam_9",
        "xsx/tcam_10",
        "xsx/tcam_11",
        "xsx/tcam_12",
        "xsx/tcam_13",
        "xsx/tcam_14",
        "xsx/tcam_15",
        "xsx/tcam_16",
        "xsx/tcam_17",
        "xsx/tcam_18",
    ]

    loader = t.LoadSignals(shot_file, tcam_channels)
    datasets = loader.run()

    combiner = t.CombineChannels(tcam_channels)
    dataset = combiner.run(datasets)

    add_params = t.AddCameraParameters("xsx_camera_l.csv")
    dataset = add_params.run(dataset)

    assert "r1" in dataset
    assert "r2" in dataset
    assert "z1" in dataset
    assert "z2" in dataset


def test_xsx_camera_transformer(shot_file):
    tcam_channels = [
        "xsx/tcam_1",
        "xsx/tcam_2",
        "xsx/tcam_3",
        "xsx/tcam_4",
        "xsx/tcam_5",
        "xsx/tcam_6",
        "xsx/tcam_7",
        "xsx/tcam_8",
        "xsx/tcam_9",
        "xsx/tcam_10",
        "xsx/tcam_11",
        "xsx/tcam_12",
        "xsx/tcam_13",
        "xsx/tcam_14",
        "xsx/tcam_15",
        "xsx/tcam_16",
        "xsx/tcam_17",
        "xsx/tcam_18",
    ]

    loader = t.LoadSignals(shot_file, tcam_channels)
    transform = t.XSXCameraTransform(loader, "xsx_camera_t.csv")
    dataset = transform.run()

    assert "r1" in dataset
    assert "r2" in dataset
    assert "z1" in dataset
    assert "z2" in dataset

    assert dataset["r1"].shape == (18,)
