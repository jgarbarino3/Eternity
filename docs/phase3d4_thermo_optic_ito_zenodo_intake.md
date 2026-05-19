# Phase 3D.4 - Thermo-Optic ITO Zenodo Source-Data Intake

Date: 2026-05-19

## Candidate

- Dataset: Wu et al., "Thermo-optic epsilon-near-zero effects"
- Dataset DOI: `10.5281/zenodo.10148545`
- Paper DOI: `10.1038/s41467-024-45054-z`
- Zenodo API: `https://zenodo.org/api/records/10148545`
- Package: `Zenodo_Data.zip`
- License: `cc-by-4.0`

The package was downloaded locally. The ZIP is small enough to inspect directly,
but it is still kept out of git as raw source data.

## Snapshot

- Local archive:
  `lab_data/raw/public_thermo_optic_ito_2024/Zenodo_Data.zip`
- Archive size: `20337405` bytes
- Supplied MD5: `aeeb8ee5508416df612004f6f7343218`
- Local MD5: `aeeb8ee5508416df612004f6f7343218`
- Local SHA-256:
  `14facee0809006c2d6ceb988c7183256fc4558f473d697fc20b61f76b96c0faf`
- Archive entries: `347`
- Total uncompressed size: `27990803` bytes

## Contents

File-type summary:

| Type | Count | Notes |
| --- | ---: | --- |
| `.txt` | 160 | Mostly extracted optical constants and supporting metadata. |
| `.SE` | 155 | Binary Woollam-style ellipsometry files; not inspected as table text. |
| `.m` | 14 | MATLAB figure scripts. |
| `.mat` | 4 | Figure data arrays. |
| `.tif` | 4 | SEM cross-section images. |
| `.xlsx` | 2 | Vacuum comparison and Hall-effect data. |

The strongest data lane is the extracted optical-constant tables. Each inspected
thermal-tuning text file starts:

```text
Opt. Const. of ITO parameterized vs. nm
Wavelength (nm),e1,e2
```

The main thermal-tuning families contain 23 files each for `1300`, `1550`,
`2000`, and `inf` sample labels. The first three are ENZ-like; `inf` is a
non-ENZ/reference lane. Each parsed table has `1041` rows over `210-2500 nm`.

Approximate zero-crossing ranges from the package tables:

| Family | Files | Wavelength range | ENZ range |
| --- | ---: | --- | --- |
| `1300` | 23 | 210-2500 nm | 1272.003721-1276.333369 nm |
| `1550` | 23 | 210-2500 nm | 1545.103808-1550.973807 nm |
| `2000` | 23 | 210-2500 nm | 1900.643878-1913.527255 nm |
| `inf` | 23 | 210-2500 nm | no zero crossing found |

The package also contains:

- `ENZ_thermal_data.mat`, with 102 MATLAB variables including many `ENZ_*`
  arrays shaped `(1041, 3)` and `ENZ_Plot_*` zero-crossing summary arrays.
- `ENZ_thermal_baseline.mat`, with baseline `ENZ_1300_bl`, `ENZ_1550_bl`,
  `ENZ_2000_bl`, and `ENZ_inf_bl` arrays.
- `Hall Effect Stat.xlsx`, with mobility/resistivity data for O-band, C-band,
  2-um-band, and non-ENZ samples.
- SEM cross-section images and metadata for the same sample families.
- A cycle note stating that ENZ wavelength-difference compensation was applied
  because of non-uniformity between measurement points.

## Acceptance Gate

This package is strong for public material-model provenance, but not for the
current calibrated-linear validation gate.

Passes:

- Public repository package.
- Machine-readable epsilon tables.
- Multiple temperature/sample families.
- Supporting Hall and SEM context.
- Figure-generation code and MAT arrays.

Fails or remains unavailable for `calibrated_linear_evidence`:

- No independent measured static R/T holdout was found.
- The `.txt` files are parameterized optical constants, not a separate
  measured R/T lane.
- The `.SE` files are binary in this environment; paired `.txt` tables are the
  accessible source-qualified material outputs.
- MATLAB scripts calculate reflectance/transmittance-like quantities from
  epsilon-derived `n,k`, but no measured R/T table was found.
- The included scripts reference helper functions such as `GetReflection`,
  `GetTransmittance`, `epsilon2nk`, and `epsilon2alphadB`; no definitions for
  those helpers were found in the included `.m` files during this pass.

## Decision

Decision: `source_package_snapshotted_calibration_fixture_no_holdout`.

Claim ceiling: `calibration_only_no_holdout`.

Serious-core promotion:

- Can feed `calibrated_linear_evidence`: `false`.
- Can enter Phase 4: `false`.
- Can be used as a public real-material constants fixture: `true`.
- Can support future thermo-optic/nonlinear readiness work: `true`, with a
  separate plan and claim gate.

## Next Step

Move to the next known public candidate. This package is worth keeping as a
well-curated real ITO/ENZ material-memory fixture, but it should not be promoted
unless a separate independent measured optical holdout is found.
