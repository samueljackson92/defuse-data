import intake
from pathlib import Path
import xarray as xr


def drop_attrs(dataset: xr.Dataset):
    dataset.attrs = {}
    for var in dataset.data_vars.values():
        var.attrs = {}
    for var in dataset.coords.values():
        var.attrs = {}
    return dataset


def main():
    dest_file = Path("30420.nc")

    url = "s3://mast/test/shots/30420.zarr"
    catalog = intake.open_catalog("https://mastapp.site/intake/catalog.yml")

    if dest_file.exists():
        dest_file.unlink()

    sources = ["amc", "efm", "esm", "xdc", "xsx"]

    for key in sources:
        dataset = catalog.level1.sources(url=f"{url}/{key}")
        dataset = dataset.to_dask()
        dataset = drop_attrs(dataset)

        if key == "amc":
            dataset["plasma_current"] = dataset["plasma_current"] * 1000

        if key == "xdc":
            dataset["ip_t_ipref"] = dataset["ip_t_ipref"] * 1000 * 1000

        dataset.to_netcdf(dest_file, group=key, mode="a")


if __name__ == "__main__":
    main()
