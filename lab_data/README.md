# Lab Data

V0 uses synthetic data. V1 real-data grounding stores small local text snapshots
immutably under `lab_data/raw/...` and references them by registry id plus
SHA-256 hash.

Current curated snapshot groups:

- `raw/synthetic_v0/`: repo-owned synthetic fixture.
- `raw/tin_tion_v1/`: TiN/TiON tabulated optical constants.
- `raw/thesis_reflectance/`: thesis wavelength/intensity reflectance spectra.
- `raw/thesis_phase3a/`: Phase 3A `30_20_10` auxiliary exports and SiO2
  Sellmeier-derived epsilon table.

These artifacts are inputs and provenance anchors. They do not by themselves
promote any run to `calibrated_linear_evidence`.
