The molecular models of NU-1500-Cr in the format of MBX interface with LAMMPS.

Files description:

unsaturated_framework: NU-1500-Cr framework with unsaturated Cr sites. Only partial Cr sites are saturated by chlorides.

saturated_framework: NU-1500-Cr framework with all Cr sites saturated with water molecules or chlorides. This configuration is considered as the "empty" framework in this study. See J. Am. Chem. Soc. 2019, 141, 2900−2905 and the crystallography data in its Supporting Information.

saturated_framework_+512w: NU-1500-Cr framework with all Cr sites saturated with water molecules or chlorides, with additional 512 water molecules loaded via Packmol (i.e. in total 16 + 512 = 528 water molecules).

lmp_npt_mbpol: the LAMMPS input file for running isothermal-isobaric ensemble MD simulations with MB-pol.

lmp_nve_mbpol: the LAMMPS input file for running microcanonical ensemble MD simulations with MB-pol.

CONFIG.01: the DLPOLY2 input file for the initial configuration of the NU-1500-Cr loaded with 512 additional water molecules.

FINAL_CONFIG.01: the DLPOLY2 output file for the last configuration of NU-1500-Cr loaded with 512 additional water molecules after randomization and full 1 ns NPT run.

Remark:

It should be noted that DLPOLY_2 and LAMMPS have different conventions of the same functional forms. As a result, the force field parameters documented in the Supporting Information are converted to align LAMMPS convention in LAMMPS input files.
