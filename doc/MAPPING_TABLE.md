## Mapping Table DEFUSE - MAST

| DEFUSE Name | DEFUSE Units | MAST Name | MAST Units | MASTU Name | MASTU Units | HDF Name | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AREA | m**2 | EFM_PLASMA_AREA | m**2 | EPQ_OUTPUT_GLOBALPARAMETERS_POLOIDALAREA, EPM_OUTPUT_GLOBALPARAMETERS_POLOIDALAREA |  | esm/surface_area | Plasma surface area. |
| BZERO | T | EFM_BVAC_RMAG | T | EPQ_OUTPUT_GLOBALPARAMETERS_BVACRMAG, EPM_OUTPUT_GLOBALPARAMETERS_BVACRMAG |  | efm/bvac_rmag | Vacuum toroidal B field at the magnetic axis. |
| DELTA_BOTTOM | a.u. | EFM_TRIANG_LOWER | nounits | EPQ/OUTPUT/FLUXFUNCTIONPROFILES/LOWERTRIANGULARITY, EPM/OUTPUT/FLUXFUNCTIONPROFILES/LOWERTRIANGULARITY |  | efm/triang_lower | Lower Plasma Triangularity |
| DELTA_TOP | a.u. | EFM_TRIANG_UPPER | nounits | EPQ_OUTPUT_GLOBALPARAMETERS_UPPERTRIANGULARITY, EPM_OUTPUT_GLOBALPARAMETERS_UPPERTRIANGULARITY |  | efm/triang_upper | Upper Plasma Triangularity |
| ECEcore |  | - |  |  |  | - | Not available |
| IPLA | A | AMC_PLASMA CURRENT | kA | IP |  | amc/plasma_current | Plasma current |
| I_P | A | EFM_PLASMA_CURR(X) | A | EPM/OUTPUT/GLOBALPARAMETERS/PLASMACURRENT |  | efm/plasma_currx | Plasma current from the equillibrium |
| Iref | A | XDC_IP_T_IPREF | MA | XDC/PLASMA/T/IP_REF | kA | xdc/ip_t_ipref | Reference plasma current |
| KAPPA | a.u. | EFM_ELONGATION | nounits | /epm/lcfs/elongation |  | efm/elongation | Elongation of LCFS; (Zmax-Zmin)/(Rmax-Rmin); f(B) |
| LI | a.u. | EFM_LI | nounits | /epm/li |  | efm/li | Plasma internal inductance. With units of vol avg (Bp^2) / surf avg (Bp)^2; f(B) |
| ML | - | AMA/N=ODD AMPLITUDE, AMA/N=2_FREQUENCY, ASM/OUT/NN_RATING | Tesla, Hz, Arb | - |  | ama/n=odd_amplitude, ama/n=2_frequency, asm/out_nn_rating | Not a straight mapping! |
| Q95 | a.u. | EFM_Q_95 | nounits | /epm/q95 |  | efm/q_95 | Safety factor at normalized 95% magnetic flux |
| RMAG | m | EFM_MAGNETIC_AXIS_R | m | EPQ/OUTPUT/GLOBALPARAMETERS/MAGNETICAXIS/R
RMAG |  | efm/magnetic_axis_r | R coordinate of magnetic axis |
| R_geom | m | EFM_GEOM_AXIS_R(C) | m | /epm/lcfs/geomaxis/r |  | efm/geom_axis_rc | R of geometric axis of plasma; f(B) |
| SXRcore |  | - |  |  |  | - | Not available  |
| Termination |  | - |  |  |  | - | Not available |
| VOL | m3 | EFM_PLASMA_VOLUME | m**3 | EPQ/OUTPUT/RADIALPROFILES/PLASMAVOLUME |  | efm/plasma_volume | Plasma Volume |
| Vloop | V | ESM_V_LOOP_DYNAMIC, ESM_V_LOOP_STATIC | V | AMB/LOOPV/LV_C_A07? or maybe XDC/PLASMA/T/VLOOP_REF |  | esm/v_loop_dynamic, esm/v_loop_static | Plasma surface VLoop calculated allowing for the movement of the LCFS; ie. in the observers frame of reference. Plasma surface calculated without allowing for the movement of LCFS ie. in the frame of reference of the plasma boundary.  |
| Wtot | J | EFM_PLASMA_ENERGY | J | EPQ/OUTPUT/GLOBALPARAMETERS/PLASMAENERGY |  | efm/plasma_energy | plasma thermal energy (J) |
| ZCC | m | EFM_CURRENT_CENTRD_Z | m | EPQ/INPUT/CONSTRAINTS/MAGNETICPROBES/ZCENTRE |  | efm/current_centrd_z | Z coordinate of current centroid |
| ZMAG | m | EFM_MAGNETIC_AXIS_Z | m | EPQ/OUTPUT/GLOBALPARAMETERS/MAGNETICAXIS/Z
ZMAG |  | efm/magnetic_axis_z | Z co-ordinate of magnetic axis; f(B) |
| Zc_v |  | - |  |  |  | - | Only need ZMAG |
| a_minor | m | EFM_MINOR_RADIUS | m | EPQ/OUTPUT/SEPARATRIXGEOMETRY/MINORRADIUS, EPM/OUTPUT/SEPARATRIXGEOMETRY/MINORRADIUS |  | efm/minor_radius | Minor radius of the plasma |
| r_LCFS | m | EFM_LCFS(R)_(C) | m | EPQ/OUTPUT/SEPARATRIXGEOMETRY/RBOUNDARY, EPM/OUTPUT/SEPARATRIXGEOMETRY/RBOUNDARY |  | efm/lcfsr_c | r-coords of separatrix |
| z_LCFS | m | EFM_LCFS(Z)_(C) | m | EPQ/OUTPUT/SEPARATRIXGEOMETRY/ZBOUNDARY, EPM/OUTPUT/SEPARATRIXGEOMETRY/ZBOUNDARY |  | efm/lcfsz_c | z-coords of separatrix |
|  |  | XSX/TCAM/<n> | V | None! |  | xsx/tcam_<n> | Soft X-ray camera: tangential camera |
|  |  | XSX/HCAM/U/<n> | V | ASX/HCAM/U/CH<n> |  | xsx/hcam_u_<n> | Soft X-ray camera: upper horizontal |
|  |  | XSX/HCAM/L/<n> | V | ASX/HCAM/L/CH<n> |  | xsx/hcam_l_<n> | Soft X-ray camera: lower horizontal |


