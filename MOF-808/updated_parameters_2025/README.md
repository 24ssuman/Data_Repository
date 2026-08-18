# MOF-808 MB-pol Files

This folder contains sample input files for molecular simulations of MOF-808 using [LAMMPS](https://github.com/lammps/lammps) interfaced with MBX. Two example systems are included: an empty MOF-808 framework and a hydrated MOF-808 framework containing 1040 H2O molecules. The hydrated sample uses MB-pol water through the MBX `h2o` monomer.

## File description

```text
updated/
├── README.md
├── force_field/
│   ├── README.md
│   ├── coefficients
│   ├── PAIR_COEFFICIENTS
│   └── PAIR_COEFFICIENTS_EMPTY_MOF
├── inputs/
│   ├── README.md
│   ├── mbx.json
│   ├── in.empty_mof
│   └── in.mof_water
└── structure/
    ├── README.md
    ├── mof808_empty.data
    └── mof808_1040wat.data
```

`structure/mof808_empty.data`: LAMMPS data file for the 1×1×1 empty MOF-808 framework containing 1248 atoms.

`structure/mof808_1040wat.data`: LAMMPS data file for the same 1×1×1 MOF-808 framework containing 1040 H2O molecules.

`inputs/in.empty_mof`: LAMMPS input file for MD simulations of the empty MOF-808 framework. The sample is configured for an NVT simulation, with alternative ensemble settings retained in the input file and available for modification as needed.

`inputs/in.mof_water`: LAMMPS input file for MD simulations of MOF-808 containing 1040 H2O molecules. MB-pol water is mapped to MBX with atom types 12/13 as O/H/H, uses a 0.5 fs timestep; the existing MOF force-field parameters and NVT default are retained.

`inputs/mbx.json`: MBX configuration file containing the settings required by the LAMMPS–MBX interface.

`force_field/coefficients`: bonded force-field parameters for the MOF-808 framework.

`force_field/PAIR_COEFFICIENTS`: nonbonded LJ coefficients for the MOF-808 framework and the hydrated system's H2O–MOF mixed terms. The `lj/cut` sub-style is written explicitly because the MB-pol sample uses the `hybrid/overlay` pair style. H2O–MOF terms use Lorentz–Berthelot mixing with O-O `(sigma, epsilon) = (3.26393 A, 0.26948 kcal/mol)` and H-H `(2.68354 A, 3.7e-10 kcal/mol)` site parameters.

`force_field/PAIR_COEFFICIENTS_EMPTY_MOF`: MOF-only nonbonded LJ coefficients for the empty framework. It contains only atom types 1–11 and no H2O–MOF terms. Both input files include the basename `PAIR_COEFFICIENTS`; stage this empty-MOF file under that basename for `in.empty_mof`, and stage the hydrated file under that basename for `in.mof_water`.

## Parameters

The MOF-808 force-field parameters and atomic charges used in these sample files are reported in:

Y. Pan, S. Saha, M. Burigana, V. Singh, O. M. Yaghi, and F. Paesani, **“Thermodynamics of alkali metal ion uptake from aqueous solution in MOF-808,”** *Chemical Science* **16**, 12129–12138 (2025). https://doi.org/10.1039/D5SC01596K

The files in `force_field/` collect the corresponding bonded and nonbonded parameters in the format required by LAMMPS.

The contents of the selected pair-coefficient include file should match the active pair style and atom types. Include H2O–MOF mixed parameters only for hydrated systems; use `PAIR_COEFFICIENTS_EMPTY_MOF` for the empty framework.

## Requirements

LAMMPS must be compiled with the packages required by the selected simulation settings and with the MBX interface enabled.

The supplied input files are intended as compact examples rather than production-ready simulation protocols. Optional settings for alternative ensembles and interaction models are retained in the input files and can be enabled or modified as needed.
