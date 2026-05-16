# Research State

## Project Reference

See: GPD/PROJECT.md (updated 2026-05-16)

**Machine-readable scoping contract:** `GPD/state.json` field `project_contract`

**Core research question:** Can Eternity build a calibrated ENZ linear digital twin from source-qualified TiN/TiON optical constants and measured holdout spectra without overclaiming?
**Current focus:** Phase 3A TiN/SiO2 thesis reflectance reconciliation

## Current Position

**Current Phase:** 3A
**Current Phase Name:** TiN/SiO2 Thesis Reflectance Reconciliation
**Total Phases:** 3
**Current Plan:** none
**Total Plans in Phase:** none
**Status:** Executing
**Last Activity:** 2026-05-16
**Last Activity Description:** Implemented a fail-closed TiN/SiO2 3L2/d_10nm validation candidate and kept claim promotion blocked by normalization and threshold gates.

**Progress:** [███████░░░] 70%

## Active Calculations

- `results/runs/run_74411c01c8a4b74e`: Phase 3A frozen TiN/SiO2 multilayer TMM candidate, 400-900 nm, 60 deg TE/S geometry.

## Intermediate Results

- Phase 3A candidate emitted `weak_within_dataset_holdout`, not `calibrated_linear_evidence`.
- Validation summary for `run_74411c01c8a4b74e`: 501 points over 400-900 nm; mean absolute residual about 0.280, RMSE about 0.281, max absolute residual about 0.305.
- Blocking gates remain `thresholds_predeclared` and `normalization_gate`; serious-core ingestion stays false.

## Open Questions

- What exact substrate and ellipsometry acquisition geometry apply to TiON_48 and TiON_49?
- Can the thesis/exported `Intensity` columns be justified as absolute or consistently normalized reflectance for Phase 3A?
- What predeclared residual thresholds and wavelength window are defensible before any calibrated-evidence promotion?

## Performance Metrics

| Label | Duration | Tasks | Files |
| ----- | -------- | ----- | ----- |
| -     | -        | -     | -     |

## Accumulated Context

### Decisions

- [Phase 1]: GPD is a planning mirror, not the source of scientific authority. — Eternity claim status remains governed by repo docs, contracts, and src/eternity/claim_status.py.
- [Phase 1]: TiN/TiON optical constants can support calibration_only_no_holdout only. — No independent TiON R/T or ellipsometry holdout provenance is registered yet.
- [Phase 3A]: Map `30_20_10` exports to thesis `d_10nm` / `3L2/Quartz` unless contradicted. — Registry notes preserve the provenance caveat and stack mapping.
- [Phase 3A]: Phase 3A validation candidates are capped at `weak_within_dataset_holdout`. — Normalization certainty and predeclared thresholds are still missing, and residuals have now been inspected only under that capped status.

### Active Approximations

None yet.

**Convention Lock:**

No conventions locked yet.

### Propagated Uncertainties

None yet.

### Pending Todos

- Recover or measure sample-matched TiON_48/TiON_49 R/T spectra with geometry notes.
- Record Pro/user-approved Phase 3A residual thresholds before any future residual-gated pass/fail run.
- Resolve whether thesis/exported intensity spectra are absolute reflectance or only comparable normalized traces.

### Blockers/Concerns

- TiON_48/TiON_49 raw R/T spectra are not registered.
- FROG labels are not authoritatively mapped to TiON_48/TiON_49.
- Phase 3A `thresholds_predeclared` gate is blocked.
- Phase 3A `normalization_gate` is blocked.

## Session Continuity

**Last session:** none
**Stopped at:** none
**Resume file:** none
**Last result ID:** none
**Hostname:** none
**Platform:** none
