# Force-Field Files

`coefficients` contains the bonded MOF-808 parameters. `PAIR_COEFFICIENTS` contains the MOF and H2O–MOF Lennard-Jones parameters for the hydrated system. The MOF diagonal values are retained, while H2O–MOF values use Lorentz–Berthelot mixing with the MB-pol O and H site parameters specified in the file comments. Each entry names the `lj/cut` sub-style so the file can be included by the MBX `hybrid/overlay` input.

`PAIR_COEFFICIENTS_EMPTY_MOF` is the empty-framework alternative. It contains the same MOF-only coefficients for atom types 1–11 and deliberately omits every type 12/13 H2O–MOF entry. Since the input files include `PAIR_COEFFICIENTS` by basename, use this file as `PAIR_COEFFICIENTS` when staging an empty-MOF run.

MB-pol water many-body interactions are supplied by the MBX `h2o` mapping in `inputs/in.mof_water`.
