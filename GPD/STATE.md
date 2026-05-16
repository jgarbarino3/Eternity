# Research State

## Project Reference

See: GPD/PROJECT.md (updated 2026-05-16)

**Machine-readable scoping contract:** `GPD/state.json` field `project_contract`

**Core research question:** Can Eternity build a calibrated ENZ linear digital twin from source-qualified TiN/TiON optical constants and measured holdout spectra without overclaiming?
**Current focus:** Phase 3A.3 thesis figure/data provenance plus Phase 3A.1 gates

## Current Position

**Current Phase:** 3A.3
**Current Phase Name:** Thesis Figure/Data Provenance Reconciliation
**Total Phases:** 3
**Current Plan:** none
**Total Plans in Phase:** none
**Status:** Executing
**Last Activity:** 2026-05-16
**Last Activity Description:** Reconciled thesis d_10nm text exports with Figure 4.1 provenance and kept normalization relative-intensity-only.

**Progress:** [████████░░] 80%

## Active Calculations

- `results/runs/run_f35a15cef565fb15`: Phase 3A frozen TiN/SiO2 multilayer TMM candidate, 400-900 nm, 60 deg TE/S geometry.

## Intermediate Results

- Phase 3A candidate emitted `weak_within_dataset_holdout`, not `calibrated_linear_evidence`.
- Validation summary for `run_f35a15cef565fb15`: 501 points over 400-900 nm; mean absolute residual about 0.280, RMSE about 0.281, max absolute residual about 0.305.
- Blocking gates remain `thresholds_predeclared` and `normalization_gate`; serious-core ingestion stays false.
- Phase 3A.1 policy records normalization as `relative_intensity_only` and thresholds as `blocked_pending_pro_checkpoint`.
- Phase 3A.3 found strong figure-provenance alignment for `d_10nm` and no absolute reflectance calibration proof.

## Open Questions

- What exact substrate and ellipsometry acquisition geometry apply to TiON_48 and TiON_49?
- Can the thesis/exported `Intensity` columns be justified as absolute reflectance for Phase 3A?
- What predeclared residual thresholds and wavelength window are defensible before any calibrated-evidence promotion?
- Can a Woollam project file, plotting script, or lab note map the `30_20_10` exports to a sample and stack?

## Performance Metrics

| Label | Duration | Tasks | Files |
| ----- | -------- | ----- | ----- |
| -     | -        | -     | -     |

## Accumulated Context

### Decisions

- [Phase 1]: GPD is a planning mirror, not the source of scientific authority. — Eternity claim status remains governed by repo docs, contracts, and src/eternity/claim_status.py.
- [Phase 1]: TiN/TiON optical constants can support calibration_only_no_holdout only. — No independent TiON R/T or ellipsometry holdout provenance is registered yet.
- [Phase 3A.2]: Keep thesis `d_10nm` mapped to `3L2/Quartz`, but do not map
  separate `30_20_10` exports to that sample without source evidence.
- [Phase 3A.3]: Treat `d_10nm` exports as thesis Figure 4.1 provenance with
  `relative_intensity_only` normalization, not absolute calibrated reflectance.
- [Phase 3A]: Phase 3A validation candidates are capped at `weak_within_dataset_holdout`. — Normalization certainty and predeclared thresholds are still missing, and residuals have now been inspected only under that capped status.
- [Phase 3A.1]: Existing residuals are historical context only. — Threshold policy must apply to a future run unless it was recorded before the run being judged.

### Active Approximations

None yet.

**Convention Lock:**

No conventions locked yet.

### Propagated Uncertainties

None yet.

### Pending Todos

- Recover or measure sample-matched TiON_48/TiON_49 R/T spectra with geometry notes.
- Record Pro/user-approved Phase 3A residual thresholds before any future residual-gated pass/fail run.
- Resolve whether thesis/exported intensity spectra are absolute reflectance.
- Bring back Pro/user guidance for Phase 3A.1 absolute-normalization and future threshold policy.
- Find source evidence for the `30_20_10` filename-to-sample mapping, or leave it parked as unresolved provenance.

### Blockers/Concerns

- TiON_48/TiON_49 raw R/T spectra are not registered.
- FROG labels are not authoritatively mapped to TiON_48/TiON_49.
- Phase 3A `thresholds_predeclared` gate is blocked.
- Phase 3A `normalization_gate` is blocked.
- `30_20_10` filename-to-thesis provenance is unresolved.
- Absolute reflectance calibration for thesis `Intensity` exports is unresolved.

## Session Continuity

**Last session:** none
**Stopped at:** none
**Resume file:** none
**Last result ID:** none
**Hostname:** none
**Platform:** none
