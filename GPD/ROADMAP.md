# Eternity GPD Roadmap Mirror

This file mirrors the repo roadmap for GPD planning. If this file disagrees
with `CURRENT_REALISTIC_ROADMAP.md`, `GOALS.md`, or `docs/PROJECT_ATLAS.md`,
the repo docs win.

## Phase 1: TiN/TiON + Thesis Reflectance Grounding

Status: completed for first grounding pass; extended by Phase 3A

Decisive outputs:

- Immutable raw snapshots under `lab_data/raw/tin_tion_v1/` and
  `lab_data/raw/thesis_reflectance/`.
- Registry entries for raw artifacts, samples, stacks, measurements, material
  models, and calibration/holdout-style splits.
- Loaders for TiN/TiON epsilon tables and thesis reflectance spectra.
- A tabulated-epsilon TMM example that emits `calibration_only_no_holdout`.
- Roadmap, atlas, and contract docs updated with the TiON R/T provenance
  blocker.

## Phase 3A: TiN/SiO2 Thesis Reflectance Reconciliation

Status: validation candidate implemented; corrected by Phase 3A.2 and followed
by Phase 3A.1

Decisive outputs:

- Immutable raw snapshots under `lab_data/raw/thesis_phase3a/` for
  `30_20_10` reflectance, p/s intensity, Psi/Delta, derived e1/e2, and SiO2
  Sellmeier epsilon.
- Registry mapping from thesis `d_10nm` to `3L2/Quartz` with the incident-order
  stack `air / 20 nm TiN / 10 nm SiO2 / 30 nm TiN / quartz`.
- Separate `30_20_10` exports demoted to an unresolved candidate bundle until
  source evidence links the filenames to a sample and stack.
- Registry-backed multilayer TMM example
  `experiments/examples/linear_tin_sio2_d10nm_validation_candidate.yaml`.
- Validation candidate run `results/runs/run_f35a15cef565fb15`, capped at
  `weak_within_dataset_holdout`, with calibrated promotion blocked by
  `thresholds_predeclared` and `normalization_gate`.

## Phase 3A.2: Stack Mapping Correction

Status: active

Decisive outputs:

- Thesis/appendix evidence checked for 3L2, d=10 nm, 60 degree TE/S-polarized
  reflectance, and `30_20_10` filename linkage.
- `d_10nm` remains source-backed as 3L2/Quartz.
- `30_20_10` files no longer feed the validation candidate.

## Phase 3A.3: Thesis Figure/Data Provenance Reconciliation

Status: active

Decisive outputs:

- `d_10nm_initial` and `d_10nm_12V` align with thesis Figure 4.1 and the local
  `10 nm SiO2 Reflectance.png` figure.
- Current normalization basis is `relative_intensity_only`, not absolute
  calibrated reflectance.
- `30_20_10` remains excluded from the validation candidate, though AFRL 6E
  notebook evidence supports it as a 30/10/20 quartz model bundle.

## Phase 3A.4: Absolute Reflectance Decision And Threshold Policy Prep

Status: active

Decisive outputs:

- `docs/phase3a4_absolute_reflectance_decision.md` records the fail-closed
  decision: `relative_intensity_only`.
- Local thesis text, figures, byte-identical raw-table hashes, CompleteEASE
  manual passages, and nearby Woollam/CompleteEASE artifacts support measured
  reflectance provenance but not calibrated absolute `%R` for the exported
  `Intensity` columns.
- Existing residuals remain historical only; future thresholds must be
  source-backed, approved, and recorded before a future run.

Next source-retrieval target:

- Find a CompleteEASE/Woollam export, recipe, project file, debug bundle, lab
  note, or newly exported table that ties the exact dynamic traces to absolute
  reflectance calibration.

## Phase 3A.5: Source-Backed Export/Provenance Retrieval

Status: completed/blocked

Goal:

- Recover the missing source link needed to upgrade from relative-only
  diagnostics to absolute-reflectance policy, or decide to stop searching and
  require a new measurement/export.

Result:

- Decision `blocked_needs_new_export`.
- Related RC2/CompleteEASE, thesis, SDSU slide/report, and scanned lab-notebook
  provenance was found, including reflectivity/reflection-intensity artifacts,
  but no exact source-backed proof that the thesis `d_10nm` `Intensity` exports
  are calibrated absolute `%R`.
- Operational normalization remains `relative_intensity_only`.

## Phase 3A.6: CompleteEASE Re-export / Measurement Packet

Status: active/packet-ready

Goal:

- Write the exact source-evidence request for a clean future Phase 3A run:
  sample ID, stack, angle, polarization, calibration state, channel name, units,
  export settings, source file, and predeclared threshold-policy boundary.

Plan:

- `docs/superpowers/plans/2026-05-16-phase3a6-completeease-reexport-measurement-packet.md`

Artifacts:

- `docs/phase3a6_completeease_reexport_packet.md`
- `docs/phase3a6_acceptance_policy.yaml`

## Phase 3A.7: CompleteEASE Source Recovery + 3L2 Provenance Lock

Status: completed/blocked

Goal:

- Recover and rank local CompleteEASE/Woollam source candidates without copying
  large binary `.SE`, `.SEsnap`, or `.iSE` files into the repo.

Artifacts:

- `src/eternity/phase3a7.py`
- `docs/phase3a7_completeease_source_recovery.md`
- `docs/phase3a7_completeease_source_recovery.json`

Result:

- Decision `related_source_candidates_found` with `absolute_reflectance_blocked`.
- Thesis-backed `3L2/Quartz` stack and 60-degree S-polarized RC2 context are
  strengthened.
- Local CompleteEASE/Woollam candidates include quartz cap-test and 10 nm SiO2
  dynamic snapshots, including DoD SAFE zip-contained `.SEsnap` members.
- No readable metadata proves calibrated absolute `%R`; Phase 3A remains capped
  below calibrated evidence.

## Phase 3A.8: Source Candidate Triage + Relative-Only Diagnostic Decision

Status: completed/blocked

Goal:

- Deduplicate and classify Phase 3A.7 source candidates, then decide whether
  the current lane should keep searching or pivot to relative-only diagnostics.

Artifacts:

- `src/eternity/phase3a8.py`
- `docs/phase3a8_source_candidate_triage.md`
- `docs/phase3a8_source_candidate_triage.json`
- `docs/phase3a8_relative_only_diagnostic_policy.yaml`

Result:

- Decision `pivot_to_relative_only_diagnostic` with
  `absolute_reflectance_blocked`.
- Quartz 10 nm dynamic snapshots are the top manual-follow-up candidates.
- Si 100 candidates are separated as controls/wrong-substrate context for
  `3L2/Quartz`.
- Relative-only diagnostics may compare spectral shape, dip position, trend
  direction, and figure provenance only; they cannot feed serious-core evidence.

## Phase 3A.9: Relative-Only Diagnostic Run Packet

Status: completed/diagnostic

Goal:

- Preserve the useful relative-shape information from the existing Phase 3A run
  while keeping claim promotion blocked.

Artifacts:

- `src/eternity/phase3a9.py`
- `docs/phase3a9_relative_only_diagnostic_packet.md`
- `docs/phase3a9_relative_only_diagnostic_packet.json`
- `docs/phase3a9_relative_only_diagnostic_table.csv`

Result:

- Decision `relative_only_diagnostic_packet_ready`.
- Min-max shape correlation is about 0.986 over 400-900 nm.
- Prediction and measurement dips both occur at 400 nm in the inspected window.
- Both normalized traces trend upward over 400-900 nm.
- The packet is descriptive context only and cannot feed serious-core evidence.

## Phase 3A.10: Manual Source Follow-Up vs Phase 3B Return Decision

Status: completed/decision

Goal:

- Decide whether to spend the next slice on manual CompleteEASE source
  follow-up or return to parked Phase 3B TiON evidence gathering.

Artifacts:

- `src/eternity/phase3a10.py`
- `docs/phase3a10_branch_decision.md`
- `docs/phase3a10_branch_decision.json`

Result:

- Decision `limited_manual_source_followup_first`.
- Inspect only the top three quartz dynamic `.SEsnap` candidates unless new
  evidence appears.
- Success requires exact `3L2/Quartz` identity plus channel name, units,
  calibration state, angle, and polarization.
- If the pass fails, use Phase 3A.6 for a clean export/new measurement or
  return to Phase 3B.
- Phase 3B is still not calibrated-ready because TiON raw R/T is missing.

## Phase 3A.11: Bounded Manual Source Follow-Up Packet

Status: completed/packet-ready

Goal:

- Turn the Phase 3A.10 branch choice into an exact manual review packet for the
  top three quartz dynamic source candidates.

Artifacts:

- `src/eternity/phase3a11.py`
- `docs/phase3a11_manual_source_followup_packet.md`
- `docs/phase3a11_manual_source_followup_packet.json`

Result:

- The packet lists the three source candidates, snippets to inspect first,
  exact proof gates, stop rules, and manual-log fields.
- It does not do a new broad search and does not copy large binary source
  files into the repo.
- It cannot feed serious-core evidence or promote the existing run.

## Phase 3A.12: Manual Source Review Result Or Clean Export Pivot

Status: completed/exhausted

Goal:

- Inspect the three bounded Phase 3A.11 candidates once and decide whether
  Phase 3A source follow-up is still worth pursuing.

Artifacts:

- `src/eternity/phase3a12.py`
- `docs/phase3a12_manual_source_review_input.json`
- `docs/phase3a12_manual_source_review_result.md`
- `docs/phase3a12_manual_source_review_result.json`

Result:

- Decision `manual_source_followup_exhausted`.
- The candidates pass only the 60-degree context gate.
- Exact `3L2/Quartz`, 30/10/20 stack, S/TE reflectance channel, absolute
  reflectance calibration, and `d_10nm` source-lineage gates remain failed or
  unresolved.
- Pivot to Phase 3B evidence reality check or use Phase 3A.6 only if a clean
  export/new measurement appears.

## Phase 3C: Public TiN Dataset Validation Lane

Status: active / intake-ready

Goal:

- Use the St Andrews 2025 public TiN dataset as a cleaner validation lane after
  Phase 3A source exhaustion.
- Keep the lane fail-closed until exact R/T-to-ellipsometry pairing,
  no-fit-leakage status, and threshold policy are explicit.

Artifacts:

- `lab_data/raw/public_st_andrews_tin_2025/TiN-data_Pure.zip`
- `lab_data/raw/public_st_andrews_tin_2025/Das_2025_JoPP_TiN.pdf`
- `docs/phase3c_public_tin_dataset_intake.md`
- `docs/phase3c_public_tin_dataset_intake.json`

Current result:

- Public dataset includes ellipsometry permittivity tables, raw Woollam files,
  `RT.xlsx` R/T data, and XRD.
- The linked paper maps Figure 4 to 50 nm TiN on glass, normal-incidence
  unpolarized R/T over 400-1000 nm.
- `RT.xlsx` reflectance reaches `0.20377` at `542.06 nm`, matching the paper's
  approximate 20% reflectance minimum near 540 nm.

Next:

- Phase 3C.1 should decide which ellipsometry table predicts `RT.xlsx`, then
  predeclare validation metrics before any residual-gated run.

## Phase 3A.1: Normalization And Threshold Gate Hardening

Status: active

Decisive outputs:

- Machine-readable policy `docs/phase3a1_threshold_policy.yaml` with
  normalization `relative_intensity_only` and threshold status
  `blocked_pending_pro_checkpoint`.
- Audit command `eternity phase3a1-audit` that separates existing-run promotion
  from future-run policy readiness.
- Pro checkpoint packet for source-backed normalization and future threshold
  decisions.

Stop/rethink conditions:

- Existing Phase 3A residuals are used to choose thresholds.
- A policy created after residual inspection is allowed to promote the existing
  run.
- Normalization is marked absolute without source-backed evidence.

Global stop/rethink conditions:

- Any TiN/TiON run is labeled `calibrated_linear_evidence` without an
  independent holdout.
- Holdout thresholds are chosen after looking at holdout residuals.
- FROG labels are treated as sample mapping evidence without a provenance
  record.
- The Phase 3A residuals are reused to tune layer thickness, optical constants,
  wavelength window, or normalization before a frozen policy is recorded.
- Thesis intensity exports are treated as absolute reflectance without a
  source-backed normalization decision.

## Phase 2: Independent Linear Holdout

Status: partially reopened by Phase 3A, still blocked for calibrated promotion

Needs one of:

- recovered sample-matched TiON_48/TiON_49 R/T spectra;
- newly measured R/T spectra with geometry and normalization notes;
- raw ellipsometry psi/delta or another independent optical holdout.
- for TiN/SiO2 Phase 3A, a source-backed normalization decision plus
  predeclared residual thresholds before pass/fail interpretation.

## Phase 3: Calibrated Linear Evidence Candidate

Status: gated

Allowed only after the model is frozen, the split is predeclared, residual
thresholds are approved, and validation gates pass.
