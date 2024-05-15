import argparse
from pathlib import Path

from convert import add_camera_parameters, combine_channels, convert_to_hdf, load_signals, remove_channels, standardise_names, write_zarr

defuse_signals = [
    'ip',
    'epq/output_globalparameters_plasmacurrent',
    'epq/output_fluxfunctionprofiles_elongation',
    # 'epm/li',
    'epq/output_globalparameters_q95',
    # 'epm/lcfs_geomaxis_r',
    'epq/output_globalparameters_magneticaxis_r',
    'epq/output_radialprofiles_plasmavolume',
    'epq/output_globalparameters_plasmaenergy',
    'epq/input_constraints_magneticprobes_zcentre',
    'epq/output_globalparameters_magneticaxis_z',
    'epq/output_separatrixgeometry_minorradius',
    'epq/output_globalparameters_poloidalarea',
    'epq/output_globalparameters_bvacrmag',
    'epq/output_fluxfunctionprofiles_lowertriangularity',
    'xdc/plasma_t_ip_ref',
    # 'xdc/plasma_t_vloop_ref',
    'amb/loopv_lv_c_a07',
    'epq/output_separatrixgeometry_rboundary',
    'epq/output_separatrixgeometry_zboundary',
    'asx/hcam_l_ch01',
    'asx/hcam_l_ch02',
    'asx/hcam_l_ch03',
    'asx/hcam_l_ch04',
    'asx/hcam_l_ch05',
    'asx/hcam_l_ch06',
    'asx/hcam_l_ch07',
    'asx/hcam_l_ch08',
    'asx/hcam_l_ch09',
    'asx/hcam_l_ch10',
    'asx/hcam_l_ch11',
    'asx/hcam_l_ch12',
    'asx/hcam_l_ch13',
    'asx/hcam_l_ch14',
    'asx/hcam_u_ch01',
    'asx/hcam_u_ch02',
    'asx/hcam_u_ch03',
    'asx/hcam_u_ch04',
    'asx/hcam_u_ch05',
    'asx/hcam_u_ch06',
    'asx/hcam_u_ch07',
    'asx/hcam_u_ch08',
    'asx/hcam_u_ch09',
    'asx/hcam_u_ch10',
    'asx/hcam_u_ch11',
    'asx/hcam_u_ch12',
    'asx/hcam_u_ch13',
    'asx/hcam_u_ch14'
]

hcam_channels = [
    'asx/hcam_l_ch01',
    'asx/hcam_l_ch02',
    'asx/hcam_l_ch03',
    'asx/hcam_l_ch04',
    'asx/hcam_l_ch05',
    'asx/hcam_l_ch06',
    'asx/hcam_l_ch07',
    'asx/hcam_l_ch08',
    'asx/hcam_l_ch09',
    'asx/hcam_l_ch10',
    'asx/hcam_l_ch11',
    'asx/hcam_l_ch12',
    'asx/hcam_l_ch13',
    'asx/hcam_l_ch14',
    'asx/hcam_u_ch01',
    'asx/hcam_u_ch02',
    'asx/hcam_u_ch03',
    'asx/hcam_u_ch04',
    'asx/hcam_u_ch05',
    'asx/hcam_u_ch06',
    'asx/hcam_u_ch07',
    'asx/hcam_u_ch08',
    'asx/hcam_u_ch09',
    'asx/hcam_u_ch10',
    'asx/hcam_u_ch11',
    'asx/hcam_u_ch12',
    'asx/hcam_u_ch13',
    'asx/hcam_u_ch14',
]


def main(path: str):
    path = Path(path).expanduser()

    # Load signals
    datasets = load_signals(path, defuse_signals)
    datasets = {name: standardise_names(ds) for name, ds in datasets.items()}

    # Rescale plasma current
    datasets['ip']['data'] * 1000
    datasets['ip'].attrs['units'] = 'A'

    # Rescale ipref 
    datasets['xdc/plasma_t_ip_ref']['data'] * 1000
    datasets['xdc/plasma_t_ip_ref'].attrs['units'] = 'A'

    # # Combine hcam/tcam channels
    datasets['asx/hcam'] = combine_channels(datasets, hcam_channels)

    remove_channels(datasets, hcam_channels)

    # Add parameters for hcam/tcam
    add_camera_parameters(datasets, 'asx/hcam', 'mast-u_asx_calibration.csv')

    # Write files
    file_name = Path(path.name)
    write_zarr(datasets, file_name)
    convert_to_hdf(file_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    main(args.path)