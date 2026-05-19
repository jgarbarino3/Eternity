# Phase 3D.3 - Exeter Spatiotemporal ITO Source-Data Intake

Date: 2026-05-19

## Candidate

- Dataset: Bohn et al., "Spatiotemporal refraction of light in an
  epsilon-near-zero ITO layer: frequency shifting effects arising from
  interfaces"
- Dataset DOI: `10.24378/exe.3644`
- Public URL:
  `https://ore.exeter.ac.uk/articles/dataset/Spatiotemporal_refraction_of_light_in_an_epsilon-near-zero_ITO_layer_frequency_shifting_effects_arising_from_interfaces_dataset_/29783195`
- Figshare API article id: `29783195`
- Package: `OpenData.zip`
- File id: `56818877`
- License: `CC BY 4.0`

The package was downloaded locally but the large ZIP is not committed to the
repo. The source-data decision is recorded from file hashes, the archive
manifest, extracted previews, and package metadata.

## Snapshot

- Local archive:
  `lab_data/raw/public_exeter_spatiotemporal_ito_2021/OpenData.zip`
- Archive size: `261202936` bytes
- Supplied MD5: `03c4aac9c14cdbce244bf958ffb51dd6`
- Local MD5: `03c4aac9c14cdbce244bf958ffb51dd6`
- Local SHA-256:
  `43ffb47cdf0ca22f1b9a7c174cf2b10ea6386d704ed38bd98b744dd43a002f7c`
- Archive entries: `52`
- Total uncompressed size: `719120896` bytes

## Useful Contents

The archive contains table-ready ellipsometry-derived permittivity:

| File | Rows | Wavelength range | ENZ crossing | Notes |
| --- | ---: | --- | --- | --- |
| `OpenData/Ellipsometer/DATA/ito_115nm.txt` | 179 | 1073.067627-1684.096069 nm | 1221.388809 nm / 245.452108 THz | Columns are `nm`, `e1 Gen-Osc`, `e2 Gen-Osc`. |
| `OpenData/Ellipsometer/DATA/ito_407nm.txt` | 143 | 1194.928223-1684.096069 nm | 1417.195169 nm / 211.539289 THz | Columns are `nm`, `e1 Gen-Osc`, `e2 Gen-Osc`. |

The ellipsometer notebooks fit Drude models to those tables:

- 115 nm notebook fitted
  `[eps_inf, wp0, gamma0] =
  [3.810047680075314, 3030653329384417.5, 179586927494851.84]`.
- 407/417/560 nm thicker-sample lane fitted
  `[eps_inf, wp0, gamma0] =
  [3.452052772428599, 2502101375647594.5, 216678163849086.53]`.

The thicker-sample lane has a metadata warning: package filenames and modeling
notebooks refer to `407nm` / `417nm`, while the material-fitting notebook prints
`ITO thickness: 560`. That mismatch must be resolved before using the thicker
lane for any quantitative claim.

## Measurement Lane

The measurement archive is open-format but nonlinear/time-resolved:

- CSV files are chopped-probe transmission scans with columns:
  `average`, `theta`, `filter_angle`, `wavelength_1`, `wavelength_2`, `delay`,
  `power_s`, `power_r`, `power_r_probe`, `intensity`.
- Each inspected measurement CSV has `35428` rows.
- Angles span `0` to `80` degrees in `5` degree steps.
- Delays span about `-0.6` to `0.7` ps in `0.0025` ps steps.
- Intensities are `100`, `200`, `300`, and `400`.
- Measurement metadata explicitly says `Is this in transmission : True` and
  `Is this with a Prism : False`.
- The `Plot_experimental_data.ipynb` notebook normalizes spectra and computes
  frequency-shift and `I/I0` traces from pumped transmission data.
- The `Interpolate-Fit-GRIN_vs_Airy.ipynb` notebook uses Airy/TMM-inspired
  modeling and fitted temporal response logic for the nonlinear dynamics.

The package therefore contains source data and code for a real ENZ experiment,
but the inspected holdout lane is not an independent static absolute R/T
measurement suitable for the current calibrated-linear gate.

## Decision

Decision: `source_package_snapshotted_nonlinear_fixture_not_calibrated`.

Claim ceiling: `literature_reproduction_fixture`.

Serious-core promotion:

- Can feed `calibrated_linear_evidence`: `false`.
- Can enter Phase 4: `false`.
- Can be used as public source-data memory: `true`.
- Can be used as a nonlinear/reproduction fixture later: `true`, after a
  separate nonlinear-readiness plan.

Reasons:

- The material constants are table-ready and public.
- The measurement data are public and open-format.
- The measurement lane is pumped, time-resolved transmission/frequency-shift
  data, not a clean independent static calibrated-linear R/T holdout.
- The notebooks normalize spectra and fit nonlinear temporal dynamics, so this
  should not be forced into a frozen-linear residual gate.
- The thicker-sample thickness labels are internally inconsistent.

## Next Step

Move to the next public package before doing more modeling. Revisit this package
later as a nonlinear ENZ fixture or literature-reproduction benchmark, not as
the first calibrated-linear evidence attempt.
