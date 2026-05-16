# Research State

## Project Reference

See: GPD/PROJECT.md (updated 2026-05-16)

**Machine-readable scoping contract:** `GPD/state.json` field `project_contract`

**Core research question:** Can Eternity build a calibrated ENZ linear digital twin from source-qualified TiN/TiON optical constants and measured holdout spectra without overclaiming?
**Current focus:** Phase 3A.6 CompleteEASE re-export / measurement packet planning plus Phase 3A.1 gates

## Current Position

**Current Phase:** 3A.6
**Current Phase Name:** CompleteEASE Re-export / Measurement Packet
**Total Phases:** 3
**Current Plan:** docs/superpowers/plans/2026-05-16-phase3a6-completeease-reexport-measurement-packet.md
**Total Plans in Phase:** 1
**Status:** Executing
**Last Activity:** 2026-05-16
**Last Activity Description:** Planned the source-evidence packet required before any future absolute-reflectance Phase 3A run.

**Progress:** [████████░░] 80%

## Active Calculations

- `results/runs/run_f35a15cef565fb15`: Phase 3A frozen TiN/SiO2 multilayer TMM candidate, 400-900 nm, 60 deg TE/S geometry.

## Intermediate Results

- Phase 3A candidate emitted `weak_within_dataset_holdout`, not `calibrated_linear_evidence`.
- Validation summary for `run_f35a15cef565fb15`: 501 points over 400-900 nm; mean absolute residual about 0.280, RMSE about 0.281, max absolute residual about 0.305.
- Blocking gates remain `thresholds_predeclared` and `normalization_gate`; serious-core ingestion stays false.
- Phase 3A.1 policy records normalization as `relative_intensity_only` and thresholds as `blocked_pending_pro_checkpoint`.
- Phase 3A.3 found strong figure-provenance alignment for `d_10nm` and no absolute reflectance calibration proof.
- Phase 3A.4 preserved `relative_intensity_only` after local evidence/manual checks and prepared future-only threshold policy guidance.
- Phase 3A.5 found related RC2/CompleteEASE, thesis, SDSU slide/report, and
  scanned lab-notebook provenance, but no exact source-backed absolute `%R`
  proof; decision is `blocked_needs_new_export`.

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
- [Phase 3A.4]: Keep `d_10nm` exports at `relative_intensity_only` until a
  source-backed export, recipe, project file, lab note, or approved policy
  proves absolute normalization before a future residual-gated run.
- [Phase 3A.5]: Local retrieval did not find exact source-backed absolute `%R`
  evidence for `d_10nm`. — Continue with relative-intensity diagnostics unless
  a new export/project/recipe/lab note is recovered.
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
- Retrieve source-backed export/recipe/project/lab-note evidence if thesis
  exported intensity spectra are to be treated as absolute reflectance.
- Phase 3A.5: decide whether a real CompleteEASE/Woollam project/export/debug
  bundle can be recovered, or pivot to a new measurement/export. Current local
  search result: `blocked_needs_new_export`.
- Phase 3A.6: prepare a CompleteEASE re-export / measurement packet with
  required sample ID, angle, polarization, calibration state, channel name, and
  units.
- Bring back Pro/user guidance for Phase 3A.1 absolute-normalization and future threshold policy.
- Find source evidence for the `30_20_10` filename-to-sample mapping, or leave it parked as unresolved provenance.

### Blockers/Concerns

- TiON_48/TiON_49 raw R/T spectra are not registered.
- FROG labels are not authoritatively mapped to TiON_48/TiON_49.
- Phase 3A `thresholds_predeclared` gate is blocked.
- Phase 3A `normalization_gate` is blocked.
- `30_20_10` filename-to-thesis provenance is unresolved.
- Absolute reflectance calibration for thesis `Intensity` exports remains
  unresolved and currently blocked by the Phase 3A.5 retrieval decision, even
  after SDSU Google Drive, thesis/defense, and scanned lab-notebook checks.

## Session Continuity

**Last session:** none
**Stopped at:** none
**Resume file:** none
**Last result ID:** none
**Hostname:** none
**Platform:** none
