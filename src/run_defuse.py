import os
import argparse
import subprocess
import logging
import intake
import pandas as pd
import xarray as xr
from dask.distributed import Client, as_completed
from dask_mpi import initialize
from pathlib import Path



def drop_attrs(dataset: xr.Dataset):
    dataset.attrs = {}
    for var in dataset.data_vars.values():
        var.attrs = {}
    for var in dataset.coords.values():
        var.attrs = {}
    return dataset


def download_data(url: str, dest_file: str):
    catalog = intake.open_catalog("https://mastapp.site/intake/catalog.yml")

    dest_file = Path(dest_file)

    if dest_file.exists():
        dest_file.unlink()

    sources = ["amc", "efm", "esm", "xdc", "xsx"]

    for key in sources:
        dataset = catalog.level1.sources(url=f"{url}/{key}")
        dataset = dataset.read()
        dataset = drop_attrs(dataset)

        if key == "amc":
            dataset["plasma_current"] = dataset["plasma_current"] * 1000

        if key == "xdc":
            dataset["ip_t_ipref"] = dataset["ip_t_ipref"] * 1000 * 1000

        dataset.to_netcdf(dest_file, group=key, mode="a")


def run_defuse(shot_id: int):
    print("Running defuse")
    script_command = f"\"setup_DEFUSE_paths;Run_DEFUSE_batch_default('MAST', {shot_id}, access_mode='server', save_mode='hdf5');exit;\""
    command = ["matlab", "-nodisplay", "-nosplash", "-nodesktop", "-r", script_command]
    command = ' '.join(command)
    print(command)
    result = subprocess.run(command, cwd="./defuse", shell=True, capture_output=True, text=True)
    print(result.stdout)


def cleanup(input_file: str):
    input_file = Path(input_file)
    if input_file.exists():
        input_file.unlink()


def predict_defuse(shot_id: int, url: str, output_folder: str):
    try:
        input_file = Path(output_folder) / f"{shot_id}.nc"
        print(url, '--->', input_file)
        download_data(url, input_file)
        run_defuse(shot_id)
        cleanup(input_file)
    except Exception as e:
        logging.error(f'Exception: {e}')
    return shot_id

def main():
    initialize()

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        prog="Run defuse",
    )

    parser.add_argument("shot_file")
    parser.add_argument("output_folder")
    args = parser.parse_args()


    shot_file = args.shot_file
    output_folder = Path(args.output_folder)

    shot_df = pd.read_csv(shot_file)
    
    client = Client()
    tasks = []

    for index, row in shot_df.iterrows():
        task = client.submit(predict_defuse, row.shot_id, row.url, output_folder)
        tasks.append(task)

    n = len(tasks)
    for i, task in enumerate(as_completed(tasks)):
        shot = task.result()
        logging.info(f"Done shot {shot}: {i+1}/{n} = {(i+1)/n*100:.2f}%")
    
    client.shutdown()

if __name__ == "__main__":
    main()
