import zarr
import h5py
from pathlib import Path
import argparse

def main(path: str):
    path = Path(path)
    out_path = path.with_suffix('.h5')
    source = zarr.open_group(path, mode='r')
    dest = h5py.File(out_path, mode='w')
    zarr.copy_all(source, dest, without_attrs=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()

    main(args.path)