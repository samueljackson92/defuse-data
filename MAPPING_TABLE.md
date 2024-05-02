## Mapping Table DEFUSE - MAST

| DEFUSE Name | DEFUSE Units | MAST Name | MAST Units | HDF Name | Description |
| --- | --- | --- | --- | --- | --- |
| AREA | m**2 | EFM_PLASMA_AREA | m**2 | esm/surface_area | Plasma surface area. |
| BZERO | T | EFM_BVAC_RMAG | T | efm/bvac_rmag | Vacuum toroidal B field at the magnetic axis. |
| DELTA_BOTTOM | a.u. | EFM_TRIANG_LOWER | nounits | efm/triang_lower | Lower Plasma Triangularity |
| DELTA_TOP | a.u. | EFM_TRIANG_UPPER | nounits | efm/triang_upper | Upper Plasma Triangularity |
| ECEcore |  | - |  | - | Not available |
| IPLA | A | AMC_PLASMA CURRENT | kA | amc/plasma_current | Plasma current |
| I_P | A | EFM_PLASMA_CURR(X) | A | efm/plasma_currx | Plasma current from the equillibrium |
| Iref | A | XDC_IP_T_IPREF | MA | xdc/ip_t_ipref | Reference plasma current |
| KAPPA | a.u. | EFM_ELONGATION | nounits | efm/elongation | Elongation of LCFS; (Zmax-Zmin)/(Rmax-Rmin); f(B) |
| LI | a.u. | EFM_LI | nounits | efm/li | Plasma internal inductance. With units of vol avg (Bp^2) / surf avg (Bp)^2; f(B) |
| ML |  | AMA/N=ODD AMPLITUDE, AMA/N=2_FREQUENCY, ASM/OUT/NN_RATING | Tesla, Hz, Arb | ama/n=odd_amplitude, ama/n=2_frequency, asm/out_nn_rating | Not a straight mapping! |
| Q95 | a.u. | EFM_Q_95 | nounits | efm/q_95 | Safety factor at normalized 95% magnetic flux |
| RMAG | m | EFM_MAGNETIC_AXIS_R | m | efm/magnetic_axis_r | R coordinate of magnetic axis |
| R_geom | m | EFM_GEOM_AXIS_R(C) | m | efm/geom_axis_rc | R of geometric axis of plasma; f(B) |
| SXRcore |  | - |  | - | Not available  |
| Termination |  | - |  | - | Not available |
| VOL | m3 | EFM_PLASMA_VOLUME | m**3 | efm/plasma_volume | Plasma Volume |
| Vloop | V | ESM_V_LOOP_DYNAMIC, ESM_V_LOOP_STATIC | V | esm/v_loop_dynamic, esm/v_loop_static | Plasma surface VLoop calculated allowing for the movement of the LCFS; ie. in the observers frame of reference Plasma surface calculated without allowing for the movement of LCFS ie. in the frame of reference of the plasma boundary.  |
| Wtot | J | EFM_PLASMA_ENERGY | J | efm/plasma_energy | plasma thermal energy (J) |
| ZCC | m | EFM_CURRENT_CENTRD_Z | m | efm/current_centrd_z | Z coordinate of current centroid |
| ZMAG | m | EFM_MAGNETIC_AXIS_Z | m | efm/magnetic_axis_z | Z co-ordinate of magnetic axis; f(B) |
| Zc_v |  | - |  | - | Only need ZMAG |
| a_minor | m | EFM_MINOR_RADIUS | m | efm/minor_radius | Minor radius of the plasma |
