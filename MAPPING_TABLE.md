## Mapping Table DEFUSE - MAST

| DEFUSE Name | MAST Name | HDF Name | Description |
| --- | --- | --- | --- |
| AREA | EFM_PLASMA_AREA | esm/surface_area | Plasma surface area. |
| BZERO | EFM_BVAC_RMAG | efm/bvac_rmag | Vacuum toroidal B field at the magnetic axis. |
| DELTA | EFM_TRIANG_LOWER, EFM_TRIANG_UPPER | efm/triang_lower, efm/triang_upper | Lower Plasma Triangularity. Upper Plasma Triangularity |
| ECEcore | - | - | Not available |
| IPLA | AMC_PLASMA CURRENT | amc/plasma_current | Plasma current |
| I_P | EFM_PLASMA_CURR(X) | efm/plasma_curr_x | Plasma current from the equillibrium |
| Iref | XDC_IP_T_IPREF | xdc/ip_t_ipref | Reference plasma current |
| KAPPA | EFM_ELONGATION | efm/elongation | Elongation of LCFS; (Zmax-Zmin)/(Rmax-Rmin); f(B) |
| LI | EFM_LI | efm/li | Plasma internal inductance. With units of vol avg (Bp^2) / surf avg (Bp)^2; f(B) |
| ML | AMA/N=ODD AMPLITUDE, AMA/N=FREQUENCY, ASM/OUT/NN_RATING | ama/n=odd_amplitude, ama/n=frequency, asm/out_nn_rating | Not a straight mapping! |
| Q95 | EFM_Q_95 | efm/q_95 | Safety factor at normalized 95% magnetic flux |
| RMAG | EFM_MAGNETIC_AXIS_R | efm/magnetic_axis_r | R coordinate of magnetic axis |
| R_geom | EFM_BVAC_RGEOM | efm/bvac_rgeom | Vaccuum toroidal B field at geometric axis |
| SXRcore | - | - | Not available  |
| Termination | - | - | Not available |
| VOL | EFM_PLASMA_VOLUME | efm/plasma_volume | Plasma Volume |
| Vloop | EFM_V_LOOP_DYNAMIC, EFM_V_LOOP_STATIC | efm/v_loop_dynamic, efm/v_loop_static | Plasma surface VLoop calculated allowing for the movement of the LCFS; ie. in the observers frame of reference. Plasma surface calculated without allowing for the movement of LCFS ie. in the frame of reference of the plasma boundary.  |
| Wtot | EFM_PLASMA_ENERGY | efm/plasma_energy | plasma thermal energy (J) |
| ZMAG | EFM_MAGNETIC_AXIS_Z | efm/magnetic_axis_z | Z co-ordinate of magnetic axis; f(B) |
| ZCC | EFM_CURRENT_CENTRD_Z | efm/current_centrd_z | Z coordinate of current centroid |
| Zc_v | - | - | Only need ZMAG |
| a_minor | EFM_MINOR_RADIUS | efm/minor_radius | Minor radius of the plasma |