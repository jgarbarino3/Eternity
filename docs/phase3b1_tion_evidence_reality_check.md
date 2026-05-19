# Phase 3B.1 - TiON Evidence Reality Check / Digitized Plot Intake

## Decision

- Status: `local_validation_data_exhausted_literature_or_external_data_needed`
- Can feed serious core: `false`
- Can promote calibrated evidence: `false`
- Phase 4 ready: `false`
- Plot digitization ready: `false`
- Calibration-only modeling ready: `true`
- Validation ready: `false`
- Recommended next phase: `Phase 3D - literature/data search for validation datasets`

## Hard Constraints

- `completeease_available`: `false`
- `completeease_contact_available`: `false`
- `st_andrews_author_contact_available`: `false`
- `tion_raw_rt_available`: `false`
- Unavailable CompleteEASE/export paths are treated as hard blockers, not active tasks.
- Unavailable TiON raw R/T is treated as a hard validation blocker.
- St Andrews remains parked unless new source evidence appears externally.

## TiON Evidence Inventory

- Samples: `2`
- Raw TiON artifacts: `2`
- TiON epsilon measurements: `2`
- TiON R/T measurements: `0`
- TiON material models: `2`
- Repo plot candidates: `0`

### Material Models

- `tion_48_0p8pa_epsilon_model`: ENZ `[497.271]` nm, range `433.428676`-`1707.810202` nm, passivity `pass`
- `tion_49_1p0pa_epsilon_model`: ENZ `[546.387, 1213.844]` nm, range `412.7424238`-`1707.810202` nm, passivity `pass`

### Calibration-Only Examples

- `experiments/examples/linear_tion_48_tabulated.yaml`: `available`, `calibration_only_no_holdout`
- `experiments/examples/linear_tion_49_tabulated.yaml`: `available`, `calibration_only_no_holdout`

## Allowed Now

- Run calibration-only TiON_48/TiON_49 TMM examples from frozen epsilon tables.
- Use TiON optical constants for model exploration and mechanism planning.
- Register plot-derived evidence only if actual plot files with usable axes are supplied.
- Search literature/public repositories for a validation dataset with optical constants plus R/T.

## Forbidden Now

- Treat TiON optical constants alone as calibrated validation evidence.
- Treat unavailable raw R/T or unavailable CompleteEASE exports as active next tasks.
- Keep iterating St Andrews source-model parity without new external source evidence.
- Map FROG or pump-probe labels to TiON_48/TiON_49 without authoritative evidence.

## Stop Condition

Local repo evidence is exhausted for calibrated validation if no TiON R/T or digitizable plot candidates are present. The next meaningful validation step is a literature/public-data search for a new dataset.
