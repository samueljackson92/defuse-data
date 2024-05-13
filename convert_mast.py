import argparse
from pathlib import Path

from convert import add_camera_parameters, combine_channels, convert_to_hdf, load_signals, remove_channels, standardise_names, write_zarr

defuse_signals = [
    'ama/n=odd_amplitude',
    'ama/n=2_frequency',
    'amc/plasma_current',
    'asm/out_nn_rating',
    'esm/surface_area',
    'efm/bvac_rmag',
    'efm/triang_lower',
    'efm/triang_upper',
    'efm/plasma_currx',
    'efm/elongation',
    'efm/li',
    'efm/q_95',
    'efm/magnetic_axis_r',
    'efm/geom_axis_rc',
    'efm/plasma_volume',
    'efm/plasma_energy',
    'efm/current_centrd_z',
    'efm/magnetic_axis_z',
    'efm/minor_radius',
    'efm/lcfsr_c',
    'efm/lcfsz_c',
    'esm/v_loop_dynamic',
    'esm/v_loop_static',
    'xdc/ip_t_ipref',
    'xsx/hcam_l_1',
    'xsx/hcam_l_10',
    'xsx/hcam_l_11',
    'xsx/hcam_l_12',
    'xsx/hcam_l_13',
    'xsx/hcam_l_14',
    'xsx/hcam_l_15',
    'xsx/hcam_l_16',
    'xsx/hcam_l_17',
    'xsx/hcam_l_18',
    'xsx/hcam_l_2',
    'xsx/hcam_l_3',
    'xsx/hcam_l_4',
    'xsx/hcam_l_5',
    'xsx/hcam_l_6',
    'xsx/hcam_l_7',
    'xsx/hcam_l_8',
    'xsx/hcam_l_9',
    'xsx/hcam_u_1',
    'xsx/hcam_u_10',
    'xsx/hcam_u_11',
    'xsx/hcam_u_12',
    'xsx/hcam_u_13',
    'xsx/hcam_u_14',
    'xsx/hcam_u_15',
    'xsx/hcam_u_16',
    'xsx/hcam_u_17',
    'xsx/hcam_u_18',
    'xsx/hcam_u_2',
    'xsx/hcam_u_3',
    'xsx/hcam_u_4',
    'xsx/hcam_u_5',
    'xsx/hcam_u_6',
    'xsx/hcam_u_7',
    'xsx/hcam_u_8',
    'xsx/hcam_u_9',
    'xsx/tcam_1',
    'xsx/tcam_10',
    'xsx/tcam_11',
    'xsx/tcam_12',
    'xsx/tcam_13',
    'xsx/tcam_14',
    'xsx/tcam_15',
    'xsx/tcam_16',
    'xsx/tcam_17',
    'xsx/tcam_18',
    'xsx/tcam_2',
    'xsx/tcam_3',
    'xsx/tcam_4',
    'xsx/tcam_5',
    'xsx/tcam_6',
    'xsx/tcam_7',
    'xsx/tcam_8',
    'xsx/tcam_9',
]

tcam_channels = [
    'xsx/tcam_1',
    'xsx/tcam_2',
    'xsx/tcam_3',
    'xsx/tcam_4',
    'xsx/tcam_5',
    'xsx/tcam_6',
    'xsx/tcam_7',
    'xsx/tcam_8',
    'xsx/tcam_9',
    'xsx/tcam_10',
    'xsx/tcam_11',
    'xsx/tcam_12',
    'xsx/tcam_13',
    'xsx/tcam_14',
    'xsx/tcam_15',
    'xsx/tcam_16',
    'xsx/tcam_17',
    'xsx/tcam_18',
]

hcam_l_channels = [
    'xsx/hcam_l_1',
    'xsx/hcam_l_2',
    'xsx/hcam_l_3',
    'xsx/hcam_l_4',
    'xsx/hcam_l_5',
    'xsx/hcam_l_6',
    'xsx/hcam_l_7',
    'xsx/hcam_l_8',
    'xsx/hcam_l_9',
    'xsx/hcam_l_10',
    'xsx/hcam_l_11',
    'xsx/hcam_l_12',
    'xsx/hcam_l_13',
    'xsx/hcam_l_14',
    'xsx/hcam_l_15',
    'xsx/hcam_l_16',
    'xsx/hcam_l_17',
    'xsx/hcam_l_18',
]

hcam_u_channels = [
    'xsx/hcam_u_1',
    'xsx/hcam_u_2',
    'xsx/hcam_u_3',
    'xsx/hcam_u_4',
    'xsx/hcam_u_5',
    'xsx/hcam_u_6',
    'xsx/hcam_u_7',
    'xsx/hcam_u_8',
    'xsx/hcam_u_9',
    'xsx/hcam_u_10',
    'xsx/hcam_u_11',
    'xsx/hcam_u_12',
    'xsx/hcam_u_13',
    'xsx/hcam_u_14',
    'xsx/hcam_u_15',
    'xsx/hcam_u_16',
    'xsx/hcam_u_17',
    'xsx/hcam_u_18',
]




def main(path: str):
    path = Path(path).expanduser()

    # Load signals
    datasets = load_signals(path, defuse_signals)
    datasets = {name: standardise_names(ds) for name, ds in datasets.items()}

    # Rescale plasma current
    datasets['amc/plasma_current']['data'] * 1000
    datasets['amc/plasma_current'].attrs['units'] = 'A'
    # Rescale ipref 
    datasets['xdc/ip_t_ipref']['data'] * 1000 * 1000
    datasets['xdc/ip_t_ipref'].attrs['units'] = 'A'

    # Combine hcam/tcam channels
    datasets['xsx/tcam'] = combine_channels(datasets, tcam_channels)
    datasets['xsx/hcam_l'] = combine_channels(datasets, hcam_l_channels)
    datasets['xsx/hcam_u'] = combine_channels(datasets, hcam_u_channels)

    remove_channels(datasets, tcam_channels)
    remove_channels(datasets, hcam_l_channels)
    remove_channels(datasets, hcam_u_channels)

    # Add parameters for hcam/tcam
    add_camera_parameters(datasets, 'xsx/tcam', 'xsx_camera_l.csv')
    add_camera_parameters(datasets, 'xsx/hcam_l', 'xsx_camera_u.csv')
    add_camera_parameters(datasets, 'xsx/hcam_u', 'xsx_camera_t.csv')

    # Write files
    file_name = Path(path.name)
    write_zarr(datasets, file_name)
    convert_to_hdf(file_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    main(args.path)