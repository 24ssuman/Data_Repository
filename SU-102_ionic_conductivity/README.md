# SU-102 Li+/PC Simulation Samples

This directory provides sample LAMMPS workflows for Li+/PC simulations in the SU-102 framework.

Two simulation workflows are included:

* **NEMD simulation:** color-charge nonequilibrium molecular dynamics (CCD-NEMD) for calculating ionic conductivity.
* **Solvation free-energy calculation:** Finite Difference Thermodynamic Integration (FDTI) for calculating the solvation free energy of a selected Li+ ion.

The scripts are provided as templates. Scheduler settings, software modules, LAMMPS executables, run lengths, and sampling parameters should be adapted to the target computing environment.

---

# Initial Structures

The `initial_structure/` directory contains 120 equilibrated configurations used in this project:

```text
initial_001.data
initial_002.data
...
initial_120.data
```

The NEMD simulations use `initial_001.data` through `initial_100.data`.

The solvation free-energy calculations use `initial_001.data` through `initial_060.data`.

---

## Atom-Type Naming Convention

The atom labels used in the force-field files differ from the oxygen notation used in the main text.

For the SU-102 framework, the atom labels in `para.in` and the LAMMPS data files correspond to the notation in the main text as follows:

* `O_2` corresponds to $O_2$.
* `O_3` and `O_3H` correspond to $O_1$.

Here, `O_3H` denotes the protonated form of the corresponding framework oxygen.

For propylene carbonate, the atom labels used in `pot_file.param` and `pc.mol` correspond to the notation in the main text as follows:

* `O_2` corresponds to $O_1^{\mathrm{PC}}$.
* `OS` corresponds to $O_2^{\mathrm{PC}}$.

These force-field atom labels should therefore not be confused with the oxygen-site notation used in the main text.

---

# Part I: NEMD Simulation

The `NEMD_simulation/` directory provides a sample setup for color-charge nonequilibrium molecular dynamics (CCD-NEMD) simulations of Li+/PC in SU-102.

A uniform color field is applied along the crystallographic `c` direction, corresponding to the Cartesian `z` direction of the simulation cell. Li+ ions are assigned a color charge of `+1`, while an equal and opposite color charge is distributed over the negatively charged SU-102 framework. PC molecules have zero color charge and therefore do not couple directly to the applied field.

Only the transverse `x` and `y` kinetic degrees of freedom are thermostatted during the NEMD simulation.

## Directory Contents

```text
NEMD_simulation/
├── parameter/
│   ├── li.mol
│   ├── li.param
│   ├── para.in
│   ├── pc.mol
│   └── pot_file.param
└── start.lmps
```

# Files

## start.lmps

Main LAMMPS input script for the CCD-NEMD simulation.

The workflow in this input file is:

* Read the equilibrated initial structure.
* Apply the force-field parameters.
* Assign color charges to Li+ and the SU-102 framework.
* Apply the external color field along the `c` direction.
* Thermostat the transverse `x` and `y` kinetic degrees of freedom.
* Run the NEMD production simulation.
* Write the trajectory, thermodynamic information, and final structure.

The electric-field strength and random velocity seed are defined as variables near the beginning of the input file and can be changed for different simulations.

## Initial structures

The first 100 equilibrated structures, `initial_001.data` through `initial_100.data`, are used for the NEMD calculations.

For each simulation, copy the desired structure into the calculation directory and rename it:

```text
initial_structure.data
```

All 72 Li+ ions remain atom type 8 for the NEMD simulations. Atom type 17 is not used in this workflow.

## parameter/

This folder contains the force-field and molecule-template files required by the NEMD input.

### para.in

SU-102 framework force-field parameters for atom types 1–7.

### pot_file.param

Propylene carbonate force-field parameters for atom types 9–16.

### pc.mol

Molecule template for propylene carbonate.

### li.mol

Molecule/atom template for Li+.

### li.param

Li+ mass and Lennard-Jones parameters for atom type 8.


## Running the NEMD Simulation

Prepare one directory for each initial structure and field strength. Copy the required parameter files, `start.lmps`, run script, and equilibrated structure into the calculation directory.

## NEMD Outputs

The main output files are:

### trajectory.lammpstrj

LAMMPS trajectory containing atomic positions and velocities.

### thermo.dat

Thermodynamic and simulation-cell information.

### final_structure.restart

Final LAMMPS restart file.

### final_structure.data

Final LAMMPS data file.

---

# Part II: Solvation Free-Energy Calculation

The `solvation_free_energy_calculation/` directory provides a sample FEP/TI workflow for calculating the solvation free energy of one selected Li+ ion in SU-102.

The calculation consists of two steps:

1. **vdW step:** the soft-core Lennard-Jones interaction of the selected Li+ ion is controlled by the coupling parameter `lambda`, while its charge is set to zero.
2. **Charge step:** the electrostatic charge of the selected Li+ ion is restored as a function of `lambda`, while its Lennard-Jones interaction remains fully coupled.

The Li+ ion selected for the solvation free-energy calculation must be assigned a unique atom type, **atom type 17**, so that its interactions can be modified independently from the other Li+ ions.

Atom type 17 is only a bookkeeping label and represents the same Li+ species as atom type 8.

## Directory Contents

```text
solvation_free_energy_calculation/
├── vdw_step/
│   └── blnk_files/
│       ├── parameter/
│       │   ├── li.param
│       │   ├── para.in
│       │   └── pot_file.param
│       └── start.lmp
├── charge_step/
│   └── blnk_files/
│       ├── parameter/
│       │   ├── li.param
│       │   ├── para.in
│       │   └── pot_file.param
│       └── start.lmp
└── initial_structure.data
```

# Files

## start.lmp

Main LAMMPS input script for an individual lambda window.

For the vdW step, the selected Li+ ion has zero charge and its soft-core Lennard-Jones interaction is varied according to `lambda` (`0.0` to `1.0` in increments of `0.1`).

For the charge step, the Lennard-Jones interaction is fully coupled and the charge of the selected Li+ ion is scaled according to `lambda` (`0.0` to `1.0` in increments of `0.2`).

The solvation free-energy calculations require a LAMMPS executable built with the FEP package.

## Initial structure

The first 60 equilibrated structures, `initial_001.data` through `initial_060.data`, are used for the FDTI calculations. The supplied `initial_structure.data` provides one representative structure prepared in the format required for the solvation free-energy calculation.

The Li+ ion whose solvation free energy is being calculated must be assigned **atom type 17**. The original equilibrated structures contain 16 atom types and 72 $\mathrm{Li}^+$ ions of atom type 8.

To prepare an initial structure for the solvation free-energy calculation:

* Change the header from `16 atom types` to `17 atom types`.
* Select the $\mathrm{Li}^+$ ion whose solvation free energy will be calculated.
* Change only its atom type from 8 to 17 in the `Atoms # full` section.
* Leave all other properties of the selected $\mathrm{Li}^+$ unchanged.
* Update the `Masses` and `PairIJ Coeffs` sections to include atom type 17, following the format provided in `initial_structure.data`.
* Verify that exactly one $\mathrm{Li}^+$ ion is atom type 17 and the remaining 71 $\mathrm{Li}^+$ ions are atom type 8.

`initial_structure.data` can be used directly as the sample initial configuration for the supplied FEP/TI input files, where lithium 3189 is selected as the one whose solvation energy is being calculated.


## parameter/

This folder contains the force-field parameters required by the FEP/TI calculations.

### para.in

SU-102 framework force-field parameters.

### pot_file.param

Propylene carbonate force-field parameters.

### li.param

Li+ parameters, including the definitions for the normal Li+ atom type and the selected type-17 Li+ ion.

# Running the Solvation Free-Energy Calculation

For each initial configuration, first prepare the structure by assigning the Li$^+$ ion of interest to atom type 17.

Copy the prepared structure to:

```text
blnk_files/initial_structure.data
```

The `blnk_files` directory serves as a template and does not contain a specific assigned $\lambda$ value. For each desired $\lambda$, the run script creates a copy of `blnk_files` in a separate $\lambda$-named directory and replaces the lambda placeholders in the input and submission files with the corresponding value.


# Solvation Free-Energy Outputs

Each lambda window produces the following main output files:

### fdti.dat

Free-energy perturbation/TI data used for integration over lambda.

### energy.dat

Energy components recorded during the simulation.

### thermo.dat

Thermodynamic and simulation-cell information.

### trajectory.lammpstrj

LAMMPS trajectory for the corresponding lambda window.

### Restart and final structure files

Files containing the final state of the individual lambda-window simulation.

The vdW and charge contributions are analyzed and integrated separately and then combined to obtain the total solvation free energy.
