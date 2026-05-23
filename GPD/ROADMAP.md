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

Status: completed / intake-ready

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

- Phase 3C.1 should turn the intake into a fail-closed validation candidate.

## Phase 3C.1: St Andrews TiN Pairing + Fail-Closed Validation Candidate

Status: completed / fail-closed candidate ready

Goal:

- Convert the public archive into small member-derived snapshots that can enter
  the registry without using hidden zip/Excel members as loose paths.
- Pair `RT.xlsx` to the candidate 50 nm TiN epsilon input only as far as the
  evidence supports.
- Keep serious-core and calibrated-evidence promotion blocked.

Artifacts:

- `docs/phase3c1_standrews_tin_pairing.md`
- `docs/phase3c1_standrews_tin_pairing.json`
- `lab_data/raw/public_st_andrews_tin_2025/standrews_tin_50nm_reflectance.csv`
- `lab_data/raw/public_st_andrews_tin_2025/standrews_tin_50nm_transmittance.csv`
- `lab_data/raw/public_st_andrews_tin_2025/standrews_tin_50nm_50c_epsilon.txt`
- `experiments/examples/linear_standrews_tin_50nm_validation_candidate.yaml`

Current result:

- Pairing status is `candidate_supported_reflectance_only`.
- Reflectance agrees with the paper-level Figure 4 description: minimum
  `0.20377` at `542.06 nm` in the 400-1000 nm window.
- The selected epsilon table has ENZ at about `664.334 nm` and passes the
  simple passivity check.
- Transmittance remains auxiliary until scaling/noise is audited.
- Claim ceiling remains `weak_within_dataset_holdout`.

Completed follow-up:

- Phase 3C.2 audits the generated fail-closed run and prepares a future-only
  threshold policy.

## Phase 3C.2: St Andrews Candidate Run Audit + Future-Only Threshold Policy

Status: completed / future-only policy prepared

Goal:

- Preserve the inspected St Andrews residuals as historical context only.
- Prepare a threshold-policy packet that cannot apply to the existing run.
- Require a clean future run after any Pro/user threshold lock.

Artifacts:

- `docs/phase3c2_standrews_run_audit.md`
- `docs/phase3c2_standrews_run_audit.json`
- `docs/phase3c2_future_threshold_policy.yaml`

Current result:

- Decision `candidate_run_audited_future_policy_prepared`.
- Existing run promotable: `false`.
- Next clean run required: `true`.
- Future policy status: `pending_pro_or_user_lock_before_clean_run`.
- Historical residuals must not tune thresholds.

Next:

- Phase 3C.3 locks thresholds before a new clean run and records whether the
  public St Andrews lane is Phase 4-ready.

## Phase 3C.3: St Andrews Threshold Lock + Clean Run Decision

Status: completed / failed validation

Goal:

- Lock conservative reflectance-only thresholds before a clean run.
- Accept St Andrews reflectance normalization for the public dataset only under
  the locked policy.
- Decide whether the clean run is ready for Phase 4 review.

Artifacts:

- `docs/phase3c3_standrews_threshold_policy.yaml`
- `experiments/examples/linear_standrews_tin_50nm_threshold_locked_clean_run.yaml`
- `docs/phase3c3_clean_run_evaluation.md`
- `docs/phase3c3_clean_run_evaluation.json`

Result:

- Decision `clean_run_failed_thresholds`.
- Clean run `run_f6ea582618328f44` failed MAE, RMSE, max absolute residual,
  dip-offset, and min-max shape-correlation gates.
- Serious-core ingestion remains false; this lane is not Phase 4-ready as-is.

Completed follow-up:

- Phase 3C.4 triaged the failure before any model revision or parking decision.

## Phase 3C.4: St Andrews Failure Triage

Status: completed / triaged, no promotion

Goal:

- Explain the Phase 3C.3 threshold failure without loosening thresholds or
  selecting a replacement model from the holdout.
- Rank likely causes: material-table mismatch, source-model mismatch,
  roughness/substrate assumptions, pairing ambiguity, and model limitations.

Artifacts:

- `src/eternity/phase3c4.py`
- `docs/phase3c4_standrews_failure_triage.md`
- `docs/phase3c4_standrews_failure_triage.json`
- `docs/phase3c4_diagnostic_sweeps.csv`

Result:

- Decision `failure_triaged_no_promotion`.
- The failure is not a near miss; all locked metrics still fail.
- The dominant residual is at `400-450 nm`, where prediction is far below the
  measured reflectance.
- No candidate St Andrews epsilon table passes the locked thresholds.
- Simple selected-table thickness and substrate-index sweeps do not fix the dip
  offset or shape correlation.
- Leading next question: source-model parity for the raw Woollam glass,
  roughness, film-thickness, and back-reflection assumptions.

Completed next:

- Phase 3C.5 inspected St Andrews source-model parity before any material
  pairing/model revision or lane parking decision.

## Phase 3C.5: St Andrews Source-Model Parity Diagnostic

Status: completed / parity gaps recorded, no promotion

Goal:

- Inspect the selected St Andrews raw Woollam `.mod/.SE` source-model
  assumptions without tuning a replacement model against the holdout.
- Record whether the clean-run stack omits source assumptions that could
  plausibly explain the Phase 3C.3 failure.

Artifacts:

- `src/eternity/phase3c5.py`
- `docs/phase3c5_standrews_source_model_parity.md`
- `docs/phase3c5_standrews_source_model_parity.json`

Result:

- Decision `source_model_parity_gaps_recorded`.
- The selected source model exposes Float Glass Cauchy substrate assumptions,
  film-thickness/roughness metadata, and back-reflection settings.
- The current clean run uses a simpler flat TiN-on-fixed-glass stack and does
  not represent those source-model assumptions.
- The gaps justify a Phase 3C.6 decision, but not a silent replacement model,
  threshold change, serious-core feed, or Phase 4 promotion.

Completed next:

- Phase 3C.6A implemented bounded source-model parity variants and parked the
  current St Andrews lane before Phase 4.

## Phase 3C.6A: Bounded St Andrews Source-Model Parity Implementation

Status: completed / parked, no promotion

Goal:

- Implement only source-model parity pieces justified by the public St Andrews
  packet: Float Glass Cauchy substrate, plausible source thickness, approximate
  roughness, and an approximate backside-reflection estimate.
- Decide whether those bounded variants resolve the Phase 3C.3 failure well
  enough to continue toward Phase 4, without fitting to the holdout or changing
  thresholds.

Artifacts:

- `src/eternity/phase3c6.py`
- `tests/unit/test_phase3c6.py`
- `docs/phase3c6_source_model_parity_decision.md`
- `docs/phase3c6_source_model_parity_decision.json`
- `docs/phase3c6_parity_variants.csv`

Result:

- Decision `parity_variants_failed_roughness_back_reflection_underdetermined`.
- Source Cauchy substrate and inferred source thickness are implemented for a
  bounded test.
- Roughness and backside reflection remain approximate: 50/50 air-TiN
  Bruggeman EMA and thick-glass incoherent backside estimate, not exact
  CompleteEASE parity.
- All bounded variants fail the locked Phase 3C.3 thresholds; best RMSE is the
  Cauchy substrate with nominal 50 nm thickness, still failing all five metrics.
- The St Andrews lane is not Phase 4-ready and cannot feed serious-core
  evidence.

Next:

- Phase 3B.1 should complete the local TiON evidence inventory before any
  external validation-data search.
- Open Phase 3C.6B only if new St Andrews source evidence resolves exact
  roughness/back-reflection or CompleteEASE acquisition parity.

## Phase 3B.1: TiON Evidence Reality Check / Digitized Plot Intake

Status: completed / local evidence exhausted, no promotion

Goal:

- Inventory TiON_48/TiON_49 local evidence under hard constraints: no
  CompleteEASE access/contact, no TiON raw R/T, and no St Andrews author
  contact.
- Decide whether plot-derived evidence can be registered explicitly as
  `digitized_from_plot`.
- Keep calibrated promotion blocked without an independent holdout.

Artifacts:

- `src/eternity/phase3b1.py`
- `tests/unit/test_phase3b1.py`
- `docs/phase3b1_tion_evidence_reality_check.md`
- `docs/phase3b1_tion_evidence_reality_check.json`
- `experiments/examples/linear_tion_49_tabulated.yaml`

Result:

- Decision `local_validation_data_exhausted_literature_or_external_data_needed`.
- TiON_48/TiON_49 epsilon measurements and material models are registered.
- TiON_48/TiON_49 calibration-only examples are available and capped at
  `calibration_only_no_holdout`.
- No TiON R/T measurements and no repo-local plot candidates are available.

Next:

- Phase 3E.1 has built the public-dataset gate and executive research assistant
  scaffold while preserving the `calibrated_linear_evidence` bar.
- Phase 3E.2A-3E.2D has completed Wang W/WO3 as a non-ENZ literature
  reproduction fixture only. Its `FigS2-nk.xlsx` constants are machine-readable,
  and `Fig2f-R.xlsx` now has a bounded de-offseted CSV/residual artifact, but
  the measured/simulated columns remain inferred rather than workbook-labeled.
  No validation claim or ENZ Phase 4 promotion is allowed.
- Phase 3E.3A has completed the Saha exported-table audit: canonical measured
  reflectance, source-simulated reflectance, TiN epsilon, and AZO epsilon CSVs
  exist, but no residual model may run yet.
- Phase 3E.3B has completed the Saha frozen-stack model gate: stack order,
  thickness, 50 degree s/p geometry, and canonical material tables are
  source-backed, but silicon constants, substrate/backside/coherence handling,
  and interface/oxide assumptions are not source-backed enough for no-fit TMM.
- Phase 3E.4 has completed a first renewed public-data search snapshot: seven
  live-source leads were inspected, the ACS/intracavity lane was corrected to a
  non-promoting Zenodo MATLAB fixture, the registry now tracks 15 candidates,
  and zero Phase 4 candidates opened.
- Continue `Phase 3E.4 - renewed ENZ public-data search through
  stack-contract gate`.
- Reopen unavailable CompleteEASE, TiON raw R/T, St Andrews author contact, or
  new literature-package paths only if the user supplies new access or data.

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

- a current literature/public dataset with source-qualified optical constants
  plus independent R/T or ellipsometry holdout;
- newly supplied local R/T or ellipsometry holdout with geometry and
  normalization notes;
- for TiN/SiO2 Phase 3A, a source-backed normalization decision plus
  predeclared residual thresholds before pass/fail interpretation.

Unavailable under current constraints:

- CompleteEASE re-export;
- TiON_48/TiON_49 raw R/T acquisition from the user;
- St Andrews author contact.

## Phase 3: Calibrated Linear Evidence Candidate

Status: gated

Allowed only after the model is frozen, the split is predeclared, residual
thresholds are approved, and validation gates pass.
