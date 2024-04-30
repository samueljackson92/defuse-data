# MAST/DEFUSE Mappings

This repo contains information for the mapping between DEFUSE and MAST.

 - [MAPPING_TABLE.md](MAPPING_TABLE.md) provides the mappings between signal names from MAST and what they are called in DEFUSE
 - [ssx_spec.pdf](ssx_spec.pdf) is the specification from the soft x-rays cameras. The CSV files were derived from this PDF.
 - [convert.py](convert.py) is a file to convert the Zarr files to a HDF file
 - Camera data
    - [xsx_camera_l.csv](xsx_camera_l.csv) is the lower camera from the MAST soft x-rays
    - [xsx_camera_u.csv](xsx_camera_u.csv) is the upper camera from the MAST soft x-rays
    - [xsx_camera_t.csv](xsx_camera_t.csv) is the tangential camera from the MAST soft x-rays