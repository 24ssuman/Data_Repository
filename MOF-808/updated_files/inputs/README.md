# Input Files

`in.mof_water` is the hydrated MOF-808 example. Its active water model is MB-pol evaluated through MBX:

- atom types 12/13 are mapped as O/H/H for the MBX `h2o` monomer;
- water bond and angle coefficients are zero because MBX supplies the monomer energy;
- the existing MOF LJ coefficients remain active through `lj/cut` in the hybrid pair style;
- H2O–MOF LJ terms use Lorentz–Berthelot mixing with O-O `(sigma, epsilon) = (3.26393 A, 0.26948 kcal/mol)` and H-H `(2.68354 A, 3.7e-10 kcal/mol)` site parameters;
- the timestep is 0.5 fs for flexible MB-pol water, with SHAKE restricted to the MOF framework;

`in.empty_mof` is the empty-framework example. For this input, use `force_field/PAIR_COEFFICIENTS_EMPTY_MOF` as the staged `PAIR_COEFFICIENTS` include file so that no type 12/13 H2O–MOF terms are loaded.

`in.mof_water` uses `force_field/PAIR_COEFFICIENTS`, which includes the MOF coefficients and the requested H2O–MOF mixed terms. The input files themselves are unchanged; select the appropriate coefficient include file when staging a run. `mbx.json` contains the shared MBX settings for this cell.
