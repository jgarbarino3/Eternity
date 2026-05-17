# Research State

## Project Reference

See: GPD/PROJECT.md (updated 2026-05-17)

**Machine-readable scoping contract:** `GPD/state.json` field `project_contract`

**Core research question:** Can Eternity build a calibrated ENZ linear digital twin from source-qualified TiN/TiON optical constants and measured holdout spectra without overclaiming?
**Current focus:** Phase 3C.1 St Andrews TiN pairing and fail-closed validation candidate

## Current Position

**Current Phase:** 3C.1
**Current Phase Name:** St Andrews TiN Pairing + Validation Candidate
**Total Phases:** 3
**Current Plan:** docs/phase3c1_standrews_tin_pairing.md
**Total Plans in Phase:** 2
**Status:** Completed/fail-closed candidate ready
**Last Activity:** 2026-05-17
**Last Activity Description:** Extracted St Andrews `RT.xlsx` into canonical R/T snapshots, registered the candidate 50 C epsilon input, and added a fail-closed TiN-on-glass validation candidate capped at weak_within_dataset_holdout.

**Progress:** [█████████░] 90%

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
- Phase 3A.7 found related local CompleteEASE/Woollam `.SE/.SEsnap/.iSE`
  candidates, including DoD SAFE zip-contained quartz cap and 10 nm SiO2
  dynamic snapshots; stack mapping is strengthened, but absolute `%R` proof is
  still blocked.
- Phase 3A.8 deduplicated recovered candidates by SHA-256, prioritized quartz
  10 nm dynamic snapshots for manual follow-up, separated Si controls, and
  recorded `pivot_to_relative_only_diagnostic`.
- Phase 3A.9 reported relative-only diagnostics for `run_f35a15cef565fb15`:
  min-max shape correlation about 0.986, matched 400 nm dip position, and
  shared increasing trend over 400-900 nm. Serious-core ingestion remains
  false.
- Phase 3A.10 chose `limited_manual_source_followup_first`: inspect the top
  three quartz dynamic `.SEsnap` candidates only, then fall back to Phase 3A.6
  clean export/new measurement or Phase 3B if exact source/calibration proof is
  not found.
- Phase 3A.11 wrote `docs/phase3a11_manual_source_followup_packet.md` and
  `.json`: the packet lists proof gates, snippets to inspect first, and stop
  rules for the three candidates. It remains non-promoting.
- Phase 3A.12 wrote `docs/phase3a12_manual_source_review_result.md` and
  `.json`: all three candidates are related provenance only. They pass the
  60-degree context gate but fail or leave unresolved the identity, stack,
  channel, absolute-normalization, and source-lineage gates.
- Phase 3C wrote `docs/phase3c_public_tin_dataset_intake.md` and `.json`:
  St Andrews `TiN-data_Pure.zip` and the linked Das et al. paper are
  snapshotted. `RT.xlsx` has a reflectance minimum of `0.20377` at `542.06 nm`
  in the paper's 400-1000 nm window, matching the paper's Figure 4 description
  of about 20% reflectance near 540 nm.
- Phase 3C.1 wrote `docs/phase3c1_standrews_tin_pairing.md` and `.json`:
  `RT.xlsx` is extracted into canonical reflectance/transmittance CSV
  snapshots, `50nm-MTiN-50c` is the candidate epsilon table, and
  `experiments/examples/linear_standrews_tin_50nm_validation_candidate.yaml`
  runs as a fail-closed normal-incidence validation candidate.

## Open Questions

- What exact substrate and ellipsometry acquisition geometry apply to TiON_48 and TiON_49?
- Can the thesis/exported `Intensity` columns be justified as absolute reflectance for Phase 3A?
- What predeclared residual thresholds and wavelength window are defensible before any calibrated-evidence promotion?
- Can a Woollam project file, plotting script, or lab note map the `30_20_10` exports to a sample and stack?
- Is the Phase 3C.1 `candidate_supported_reflectance_only` pairing sufficient
  for future threshold policy, or should more source/paper metadata be reviewed?

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
- [Phase 3A.7]: Related CompleteEASE/Woollam source candidates do not equal
  absolute reflectance proof. — Keep normalization `relative_intensity_only`
  unless source metadata explicitly proves channel name, units, calibration
  state, angle, polarization, and exact sample identity.
- [Phase 3A.8]: Source-candidate triage pivots to relative-only diagnostics. —
  Spectral shape, dip position, trend direction, and figure provenance may be
  compared, but serious-core evidence and calibrated promotion remain forbidden.
- [Phase 3A.9]: Relative-only diagnostics are descriptive, not validating. —
  Shape/dip/trend agreement is useful context, but cannot become a pass/fail
  gate or calibrated-evidence promotion for the already-inspected run.
- [Phase 3A.10]: Bounded manual source follow-up comes before Phase 3B return.
  — The follow-up has concrete targets and Phase 3B still lacks raw TiON R/T.
- [Phase 3A.11]: Manual source follow-up is packetized, not proven. — The
  packet guides review but does not prove absolute reflectance or source
  identity.
- [Phase 3A.12]: Phase 3A source follow-up is exhausted. — Do not continue
  open-ended searching without new evidence, a clean export, or a new
  measurement.
- [Phase 3C]: St Andrews public TiN is the next best validation lane. — It has
  paper-backed R/T and ellipsometry in one public dataset, but still needs exact
  pairing, leakage policy, and predeclared thresholds before calibrated
  promotion.
- [Phase 3C.1]: St Andrews TiN can run as a fail-closed validation candidate.
  — Reflectance supports the 50 nm / 50 C candidate pairing well enough for a
  capped run, but not for calibrated promotion; R/T holdouts remain forbidden
  for fitting and thresholds are blocked.
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
- Phase 3B.1: perform a TiON evidence reality check / digitized plot intake, or
  use Phase 3A.6 only if a clean CompleteEASE export/new measurement appears.
- Phase 3A.6 packet remains available if a fresh CompleteEASE re-export or new
  measurement is needed.
- Bring back Pro/user guidance for Phase 3A.1 absolute-normalization and future threshold policy.
- Find source evidence for the `30_20_10` filename-to-sample mapping, or leave it parked as unresolved provenance.
- Phase 3C.2: audit the St Andrews fail-closed run and use Pro/GPD review
  before any future threshold approval or calibrated-evidence promotion policy.

### Blockers/Concerns

- TiON_48/TiON_49 raw R/T spectra are not registered.
- FROG labels are not authoritatively mapped to TiON_48/TiON_49.
- Phase 3A `thresholds_predeclared` gate is blocked.
- Phase 3A `normalization_gate` is blocked.
- `30_20_10` filename-to-thesis provenance is unresolved.
- Absolute reflectance calibration for thesis `Intensity` exports remains
  unresolved and currently blocked after Phase 3A.8 source triage, even with
  related CompleteEASE/Woollam source candidates.
- Phase 3C.1 pairing is `candidate_supported_reflectance_only`, not calibrated
  evidence; transmittance scaling/noise remains auxiliary and thresholds are
  not predeclared.

## Session Continuity

**Last session:** none
**Stopped at:** none
**Resume file:** none
**Last result ID:** none
**Hostname:** none
**Platform:** none
