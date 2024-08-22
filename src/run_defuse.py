import os
import argparse
import subprocess
import logging
import s3fs
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

    dest_file = Path(dest_file)

    if dest_file.exists():
        dest_file.unlink()

    sources = ["amc", "efm", "esm", "xdc", "xsx"]

    for key in sources:
        file_name = f"{url}/{key}"
        endpoint_url = "https://s3.echo.stfc.ac.uk/"
        fs = s3fs.S3FileSystem(anon=True, endpoint_url=endpoint_url)
        try:
            dataset = xr.load_dataset(fs.get_mapper(file_name), engine='zarr')
        except Exception as e:
            logging.error(f'Cannot load data {file_name}')
            raise e

        dataset = drop_attrs(dataset)

        if key == "amc":
            dataset["plasma_current"] = dataset["plasma_current"] * 1000

        if key == "xdc":
            dataset["ip_t_ipref"] = dataset["ip_t_ipref"] * 1000 * 1000

        dataset.to_netcdf(dest_file, group=key, mode="a")


def run_defuse(shot_id: int):
    logging.info("Running defuse")
    script_command = f"\"setup_DEFUSE_paths;Run_DEFUSE_batch_default('MAST', {shot_id}, access_mode='server', save_mode='hdf5');exit;\""
    command = ["matlab", "-nodisplay", "-nosplash", "-nodesktop", "-r", script_command]
    command = ' '.join(command)
    logging.info(command)
    result = subprocess.run(command, cwd="./defuse", shell=True, capture_output=True, text=True)
    logging.info(result.stdout)


def cleanup(input_file: str):
    input_file = Path(input_file)
    if input_file.exists():
        input_file.unlink()


def predict_defuse(shot_id: int, url: str, output_folder: str):
    input_file = Path(output_folder) / f"{shot_id}.nc"
    logging.info(url, '--->', input_file)

    try:
        download_data(url, input_file)
        run_defuse(shot_id)
    except Exception as e:
        logging.error(f'Exception: {e}')
    finally:
        cleanup(input_file)

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
    shot_df = shot_df.sort_values('shot_id', ascending=False)
    
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
