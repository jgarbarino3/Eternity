# Eternity Current Realistic Roadmap

Date: 2026-05-19

## Framing

Eternity is a long-term personal research/build project, not a short-term product sprint.

The goal is to see how far one person plus current and future AI systems can go toward building an AI researcher for ultrafast ENZ optics over the next few years. The project should be useful, scientifically grounded, and fun. It does not need to become a fully autonomous scientist immediately. The right standard is compounding progress.

The long-term destination is:

> An AI researcher that can read literature and lab memory, form hypotheses, design theoretical ENZ/ultrafast optics experiments, run simulations, compare against real lab data, critique its own conclusions, propose next experiments, and eventually help draft research notes or papers.

The realistic starting point is:

> Build the experimental world that a future AI researcher can think and act inside.

That world is the ENZ digital twin: simulation infrastructure, lab data, material models, validation records, uncertainty tracking, and reproducible experiment runs.

## Why Start With The Digital Twin

The digital twin is still the best start, but not because the AI researcher idea is being dismissed.

It is the best start because it is the most direct path to making the AI researcher meaningful.

If the project starts with autonomous agents first, the result will probably be a smart-sounding chatbot with weak contact with physical reality. If the project starts with the digital twin, every later AI upgrade can plug into a real substrate:

- Data it can inspect.
- Simulators it can run.
- Results it can compare.
- Assumptions it must state.
- Validity envelopes it must respect.
- Failed hypotheses it can remember.
- Experimental artifacts it can learn to avoid.

The digital twin is the body, lab bench, notebook, and reality-check layer for the future AI researcher.

## Two-Track Strategy

Because this is a long-term personal project, Eternity should not be overly conservative. It should have a serious physics core and a more experimental AI researcher playground.

### Track A: Serious Core

This is the validated ENZ digital twin.

Principles:

- Slow and careful.
- Test-driven where possible.
- Physically explicit.
- Reproducible.
- Versioned.
- Skeptical about claims.
- Grounded in real lab data and known literature.

This track owns:

- Experiment specs.
- Lab-data registry.
- Material models.
- Transfer-matrix simulation.
- FDTD adapters.
- Fitting and calibration.
- Run provenance.
- Reports.
- Validity envelopes.
- Regression tests.

### Track B: Researcher Playground

This is where we explore the AI researcher idea early.

Principles:

- Fun and speculative.
- Allowed to be wrong.
- Clearly labeled as exploratory.
- Never allowed to overwrite or contaminate validated core results.
- Useful for learning what future AI workflows might look like.

This track can include:

- Hypothesis generation.
- Literature-question answering.
- Proposed simulation sweeps.
- Research-note drafting.
- Critique agents.
- Mechanism comparison.
- Paper-outline generation.
- Weird search strategies.
- Multi-agent debate.

The rule is simple: the playground may suggest; the serious core verifies.

## First Real Loop

The first important milestone is not a complete simulator. It is a complete research loop:

```text
question
  -> experiment spec
  -> simulation
  -> result
  -> critique
  -> proposed next experiment
```

This is the seed of the autonomous researcher.

At first, the loop can use toy data and a simple linear simulator. Later, each piece becomes more real:

- Toy material -> fitted Drude/Drude-Lorentz material.
- Synthetic pulse -> measured laser spectrum/FROG/autocorrelation data.
- Linear TMM -> nonlinear ENZ dynamics and FDTD validation.
- Human-written question -> AI-generated hypothesis.
- Simple report -> research notebook entry with uncertainty and literature context.

## V0: First Vertical Slice

Build a minimal but real ENZ thin-film experiment runner.

V0 should include:

- Python package foundation.
- One YAML experiment spec.
- One lab-data registry.
- One material model.
- One transfer-matrix simulator.
- One deterministic run command.
- One generated Markdown report.
- Tests proving deterministic behavior and basic energy bookkeeping.

The first V0 experiment can use:

- Synthetic ITO/AZO material parameters.
- Synthetic Gaussian or chirped Gaussian pulse.
- Simple thin-film stack.
- Transmission/reflection output.
- Plots of epsilon, n/k, transmission, and reflection.

The point is to make the entire system shape real, even before the physics is deep.

## V1: Real Inputs

After V0 works, add real data one path at a time.

Priority order:

1. Ellipsometry import.
2. Linear transmission/reflection import.
3. Measured laser spectrum import.
4. Pulse duration/chirp metadata.
5. Sample thickness and uncertainty.
6. Incidence angle and polarization metadata.

V1 goal:

> Given one measured sample and one measured optical setup, predict linear transmission/reflection and compare against measurement.

This is the first serious digital-twin checkpoint.

### Active V1 Phase 3: TiN/TiON + Thesis Reflectance Grounding

The immediate core move is not yet a calibrated claim. It is to make the
available real data safe for the Serious Core:

- Snapshot the 50 nm TiN optical constants, TiON_48/TiON_49 40 nm epsilon
  tables, and thesis reflectance spectra under `lab_data/raw/...`.
- Register every artifact with SHA-256, byte size, source notes, sample/stack
  refs, and claim-status boundaries.
- Load tabulated epsilon as a frozen linear material model for deterministic
  TMM grounding runs.
- Preserve thesis initial/12V reflectance spectra as measured provenance and
  possible holdout candidates.
- Emit explicit R/T provenance audits and gaps when TiON sample-matched
  reflection/transmission data is missing.

Allowed status for optical-constants-only TiN/TiON runs:

```text
calibration_only_no_holdout
```

Forbidden language until an independent holdout exists:

```text
calibrated TiN/TiON evidence
validated nonlinear ENZ response
sample-matched R/T agreement
```

#### Phase 3A: TiN/SiO2 Thesis Reflectance Reconciliation

Active core move:

- Reconcile the thesis/paper TiN/SiO2 measured spectra with the sample labels
  and stack records already in the registry.
- Add the `30_20_10` reflectance, Psi/Delta, p/s intensity, and e1/e2 exports
  as candidate raw artifacts, but do not treat them as thesis `d_10nm`
  validation evidence until the filename-to-thesis mapping is source-confirmed.
- Decide the measurement geometry, polarization, normalization, and holdout
  split policy before any residual thresholds are set.
- Keep TiON_48/TiON_49 in a parked Phase 3B path unless raw R/T or
  source-tabulated reflectance appears.

Implemented Phase 3A should emit a fail-closed validation candidate using the
`thesis_d_10nm` / `3L2` stack:

- frozen TiN and SiO2 epsilon tables;
- incident-order stack `air / 20 nm TiN / 10 nm SiO2 / 30 nm TiN / quartz`;
- TE/S-polarized, 60-degree comparison against the d=10 nm initial spectrum;
- `30_20_10` reflectance, p/s intensity, Psi/Delta, and e1/e2 exports as a
  separate unresolved candidate bundle, not auxiliary evidence for the
  `d_10nm` holdout.

Phase 3A may emit `weak_within_dataset_holdout`, but it cannot claim
`calibrated_linear_evidence` while normalization and residual-threshold gates
remain blocked.

#### Phase 3A.1: Normalization And Threshold Gate Hardening

Active follow-up:

- Keep the already-inspected Phase 3A residuals as historical context only.
- Record the normalization decision as a machine-readable gate policy with the
  current state `relative_intensity_only`.
- Record that no residual thresholds are approved for the existing run.
- Provide an audit command that reports whether the current run can be promoted
  and why it remains blocked.

Phase 3A.1 is not a calibration phase. It may prepare future gate policy, but
it must not convert `run_f35a15cef565fb15` into
`calibrated_linear_evidence`.

#### Phase 3A.2: Stack Mapping Correction

Active correction:

- Keep thesis `d_10nm` mapped to `3L2/Quartz` because the thesis Table 4.1 and
  Figure 4.1 support the 30 nm TiN / 10 nm SiO2 / 20 nm TiN stack.
- Demote separate `30_20_10` Coding/txt exports to
  `phase3a_30_20_10_candidate` because the thesis/appendix do not prove those
  filenames are the plotted `d_10nm` spectra.
- Keep calibrated promotion blocked by normalization and threshold gates.

#### Phase 3A.3: Thesis Figure/Data Provenance Reconciliation

Active provenance closure:

- Align `d_10nm_initial.txt` and `d_10nm_12V.txt` with thesis Figure 4.1 and
  the local `10 nm SiO2 Reflectance.png` plot.
- Record that the values are plotted as reflectance but exported as
  `Intensity`, so the current normalization basis is `relative_intensity_only`,
  not absolute calibrated reflectance.
- Keep `30_20_10` as a separate candidate bundle. AFRL 6E notebook evidence
  supports a 30 nm TiN / 10 nm SiO2 / 20 nm TiN quartz model, but not identity
  with the thesis Figure 4.1 export.
- Keep calibrated promotion blocked by normalization and threshold gates.

#### Phase 3A.4: Absolute Reflectance Decision And Threshold Policy Prep

Active decision:

- Treat the thesis `d_10nm` exports as `relative_intensity_only` after checking
  thesis text, local figures, byte-identical raw tables, local CompleteEASE
  manual passages, and nearby Woollam/CompleteEASE artifacts.
- Preserve the stronger Phase 3A.3 provenance result: `d_10nm` is source-backed
  to thesis Figure 4.1 and sample `3L2/Quartz`, with 60-degree S-polarized RC2
  reflectance context.
- Do not treat the exported `Intensity` columns as absolute `%R` until a
  source-backed export/recipe/project/lab-note record proves that calibration.
- Keep `run_f35a15cef565fb15` historical only. No pass/fail thresholds may be
  chosen from already-inspected residuals, and no current Phase 3A run may
  promote to `calibrated_linear_evidence`.
- Prepare future policy only: absolute-normalization evidence, wavelength
  window, residual metrics, numeric thresholds, approver, and date must all be
  recorded before a future residual-gated run.

#### Phase 3A.5: Source-Backed Export/Provenance Retrieval

Decision: `blocked_needs_new_export`.

The bounded local/SDSU/Google Drive search found strong RC2/CompleteEASE,
thesis, SDSU slide, AFRL report, and scanned lab-notebook provenance, including
related reflectivity/reflection-intensity files and the `3L2/Quartz` sample
narrative. It still did not find a source-backed export, recipe, project, debug
bundle, or lab-note statement proving that the exact `d_10nm_initial.txt` and
`d_10nm_12V.txt` `Intensity` columns are calibrated absolute `%R`.

The Phase 3A normalization basis therefore stays `relative_intensity_only`.
`run_f35a15cef565fb15` remains historical and capped below calibrated evidence.

Next best core move:

- `Phase 3A.6 - CompleteEASE re-export / measurement packet`: write the exact
  source-evidence request needed for a clean future run, or define a
  Pro/user-approved relative-only diagnostic policy that cannot promote to
  `calibrated_linear_evidence`.

#### Phase 3A.6: CompleteEASE Re-export / Measurement Packet

Implementation artifacts:

- `docs/phase3a6_completeease_reexport_packet.md`
- `docs/phase3a6_acceptance_policy.yaml`
- `docs/superpowers/plans/2026-05-16-phase3a6-completeease-reexport-measurement-packet.md`

Planning file:
`docs/superpowers/plans/2026-05-16-phase3a6-completeease-reexport-measurement-packet.md`.

Purpose:

- Turn the Phase 3A.5 blocked result into a precise evidence request for the
  original CompleteEASE/Woollam project, a fresh re-export, an export recipe,
  or a new measurement note.
- Require sample identity, stack, angle, polarization, channel name, units,
  calibration/baseline state, source file identity, hash, and future-only
  threshold boundaries before any absolute-reflectance run.
- Keep all existing inspected runs below `calibrated_linear_evidence`.

Not enough information exists yet to complete calibrated Phase 3A promotion.
Enough information exists to use the source-evidence packet and prevent another
ambiguous export from entering the serious core.

#### Phase 3A.7: CompleteEASE Source Recovery + 3L2 Provenance Lock

Decision: `related_source_candidates_found`, with `absolute_reflectance_blocked`.

Implementation artifacts:

- `src/eternity/phase3a7.py`
- `docs/phase3a7_completeease_source_recovery.md`
- `docs/phase3a7_completeease_source_recovery.json`

Phase 3A.7 adds a read-only recovery scanner for local CompleteEASE/Woollam
`.SE`, `.SEsnap`, and `.iSE` files, including matching members inside DoD SAFE
zip containers. It records hashes, archive/member paths, `_FitLog` snippets,
and candidate scores without copying large binary source files into the repo.

Result:

- Thesis-backed `3L2/Quartz` mapping is stronger: 30 nm TiN / 10 nm SiO2 /
  20 nm TiN on quartz, S-polarized RC2 in-situ reflectance/reflective intensity
  at 60 degrees, Figure 4.1.
- The strongest recovered local candidates are related CompleteEASE/Woollam
  source snapshots for quartz cap-test and 10 nm SiO2 pulsed/dynamic runs.
- No readable source metadata proves that the exported `Intensity` columns are
  calibrated absolute `%R`. Generic CompleteEASE strings such as `% 1st
  Reflection` or `Absolute MSE` are not normalization proof.
- `run_f35a15cef565fb15` remains historical, capped at
  `weak_within_dataset_holdout`, and blocked by normalization and
  predeclared-threshold gates.

Enough information exists to continue relative-intensity diagnostics and source
triage. Not enough information exists to approve absolute normalization,
thresholds, or `calibrated_linear_evidence`.

#### Phase 3A.8: Source Candidate Triage + Relative-Only Diagnostic Decision

Decision: `pivot_to_relative_only_diagnostic`, with `absolute_reflectance_blocked`.

Implementation artifacts:

- `src/eternity/phase3a8.py`
- `docs/phase3a8_source_candidate_triage.md`
- `docs/phase3a8_source_candidate_triage.json`
- `docs/phase3a8_relative_only_diagnostic_policy.yaml`

Phase 3A.8 consumes the Phase 3A.7 recovery manifest without rescanning local
source files. It deduplicates source candidates by SHA-256, separates the
quartz 10 nm dynamic/manual-follow-up candidates from Si-control candidates,
and records the relative-only lane explicitly.

Result:

- The highest manual-follow-up candidates are the DoD SAFE zip-contained quartz
  10 nm SiO2 pulsed/dynamic `.SEsnap` files.
- Related quartz cap-test files remain provenance context, not exact source
  identity records.
- Si 100 files are classified as controls or wrong-substrate candidates for the
  thesis `3L2/Quartz` path.
- Future Phase 3A diagnostics may compare spectral shape, dip position, trend
  direction, and figure provenance only.
- Serious-core ingestion, calibrated-linear-evidence promotion, absolute
  reflectance claims, and retroactive threshold tuning remain forbidden.

Enough information exists to run relative-only diagnostics honestly. Not enough
information exists to approve absolute normalization, thresholds, or
`calibrated_linear_evidence`.

#### Phase 3A.9: Relative-Only Diagnostic Run Packet

Decision: `relative_only_diagnostic_packet_ready`, with serious-core ingestion
and calibrated promotion still forbidden.

Implementation artifacts:

- `src/eternity/phase3a9.py`
- `docs/phase3a9_relative_only_diagnostic_packet.md`
- `docs/phase3a9_relative_only_diagnostic_packet.json`
- `docs/phase3a9_relative_only_diagnostic_table.csv`

Phase 3A.9 consumes the existing Phase 3A validation-candidate run and the
Phase 3A.8 relative-only policy. It reports normalized shape, dip-position, and
trend-direction diagnostics without treating them as thresholds or calibrated
validation.

Result for `run_f35a15cef565fb15`:

- Window: 400-900 nm, 501 points.
- Min-max shape correlation: about 0.986.
- Prediction and measurement dips both occur at 400 nm in the inspected window.
- Both normalized spectra trend upward over the inspected window.
- Historical absolute residual context remains visible, but it is not used for
  threshold setting or promotion.

Enough information exists to say the relative spectral shape is worth keeping
as a diagnostic clue. Not enough information exists to claim absolute
reflectance agreement, pass/fail validation, or `calibrated_linear_evidence`.

#### Phase 3A.10: Manual Source Follow-Up vs Phase 3B Return Decision

Decision: `limited_manual_source_followup_first`.

Implementation artifacts:

- `src/eternity/phase3a10.py`
- `docs/phase3a10_branch_decision.md`
- `docs/phase3a10_branch_decision.json`

Phase 3A.10 consumes the Phase 3A.8 source triage, Phase 3A.9 diagnostic
packet, and registry state. It chooses the next branch without doing another
open-ended source search.

Result:

- Do one bounded manual follow-up pass on the three highest-priority quartz
  dynamic `.SEsnap` candidates.
- Stop after those three candidates unless the user adds new evidence.
- Success requires source-backed channel name, units, calibration state, angle,
  polarization, and exact `3L2/Quartz` identity.
- If the manual pass fails, keep Phase 3A relative-only and either use the
  Phase 3A.6 clean export/new measurement packet or return to Phase 3B TiON
  evidence gathering.
- Phase 3B remains parked for calibrated evidence because TiON_48/TiON_49 have
  optical constants registered but no raw sample-matched R/T.

Enough information exists to run the bounded manual follow-up. Not enough
information exists to promote calibrated evidence or to unpark TiON as a
calibrated-evidence route.

#### Phase 3A.11: Bounded Manual Source Follow-Up Packet

Status: packet-ready / non-promoting.

Implementation artifacts:

- `src/eternity/phase3a11.py`
- `docs/phase3a11_manual_source_followup_packet.md`
- `docs/phase3a11_manual_source_followup_packet.json`

Phase 3A.11 converts the Phase 3A.10 branch choice into an exact review packet:
inspect only the three listed quartz dynamic `.SEsnap` candidates, classify
them against the proof gates, and stop unless source-backed evidence proves
exact `3L2/Quartz` identity, stack, S/TE reflectance channel, 60-degree
geometry, absolute reflectance units/calibration state, and lineage to the
`d_10nm` text trace.

Result:

- The manual review scope is bounded and reproducible.
- The current default remains `relative_intensity_only`.
- The packet cannot feed serious-core evidence and cannot promote any existing
  run to `calibrated_linear_evidence`.
- If any proof gate remains unresolved after the three candidates, use the
  Phase 3A.6 clean export/new measurement packet or return to Phase 3B TiON
  evidence gathering.

#### Phase 3A.12: Manual Source Review Result Or Clean Export Pivot

Status: completed / exhausted.

Implementation artifacts:

- `src/eternity/phase3a12.py`
- `docs/phase3a12_manual_source_review_input.json`
- `docs/phase3a12_manual_source_review_result.md`
- `docs/phase3a12_manual_source_review_result.json`

Phase 3A.12 inspected the three bounded Phase 3A.11 `.SEsnap` candidates by
hash, inner archive members, `_FitLog` metadata, and targeted proof-term
search. All three candidates strengthen related quartz / 10 nm SiO2 /
60-degree CompleteEASE provenance, but none prove exact `3L2/Quartz` identity,
the `30 nm TiN / 10 nm SiO2 / 20 nm TiN` stack, absolute reflectance units or
calibration state, or lineage to the `d_10nm` text exports.

Result:

- Decision `manual_source_followup_exhausted`.
- Phase 3A remains `relative_intensity_only` with ceiling
  `weak_within_dataset_holdout`.
- Continuing Phase 3A source searching is not recommended unless the user adds
  new source evidence. CompleteEASE re-export is now a hard unavailable path
  under the user's stated constraints.
- The Phase 3B evidence reality check is now complete: TiON calibrated evidence
  remains blocked until new local data or an external public/literature dataset
  supplies an independent holdout.

#### Phase 3C: Public TiN Dataset Validation Lane

Status: completed / intake-ready.

Implementation artifacts:

- `lab_data/raw/public_st_andrews_tin_2025/TiN-data_Pure.zip`
- `lab_data/raw/public_st_andrews_tin_2025/Das_2025_JoPP_TiN.pdf`
- `docs/phase3c_public_tin_dataset_intake.md`
- `docs/phase3c_public_tin_dataset_intake.json`

Phase 3C pivots away from the exhausted thesis-source path into a public,
paper-backed TiN dataset from the University of St Andrews:

- Dataset DOI: `10.17630/42a1d567-9e02-4916-8709-e2b4911c715c`
- Paper DOI: `10.1088/2515-7647/adcddc`
- Public data include extracted ellipsometry permittivity tables, raw Woollam
  `.SE/.mod` files, `RT.xlsx` reflectance/transmittance data, and XRD.

This path looks meaningfully better than continuing Phase 3A because the linked
paper states Figure 4 is unpolarized normal-incidence reflectance/transmittance
for 50 nm TiN films on glass over `400-1000 nm`. The `RT.xlsx` reflectance
minimum in that window is `0.20377` at `542.06 nm`, matching the paper text that
reflectance reaches about `20%` near `540 nm`.

Result:

- Decision `public_dataset_intake_ready`.
- This can support a new validation candidate after pairing and leakage policy
  are explicit.
- It still cannot emit `calibrated_linear_evidence` until the exact
  `RT.xlsx`-to-ellipsometry-table pairing, no-fit-leakage status, residual
  metrics, and thresholds are predeclared before residual inspection.

Recommended next:

- `Phase 3C.1 - St Andrews TiN Pairing + Validation Candidate`: interpret the
  public archive, extract canonical R/T and epsilon member snapshots, register a
  fail-closed validation candidate, and keep calibrated promotion blocked.

#### Phase 3C.1: St Andrews TiN Pairing + Validation Candidate

Status: completed / fail-closed validation candidate ready.

Implementation artifacts:

- `docs/phase3c1_standrews_tin_pairing.md`
- `docs/phase3c1_standrews_tin_pairing.json`
- `lab_data/raw/public_st_andrews_tin_2025/standrews_tin_50nm_reflectance.csv`
- `lab_data/raw/public_st_andrews_tin_2025/standrews_tin_50nm_transmittance.csv`
- `lab_data/raw/public_st_andrews_tin_2025/standrews_tin_50nm_50c_epsilon.txt`
- `experiments/examples/linear_standrews_tin_50nm_validation_candidate.yaml`

Phase 3C.1 turns the public St Andrews archive into a usable, fail-closed
validation lane:

- `RT.xlsx` was converted into deterministic unsmoothed reflectance and
  transmittance CSV snapshots.
- `TiN-data_Pure/Ellipsometry/50nm-MTiN-50c.txt` was copied as the candidate
  frozen epsilon input for `public_standrews_tin_50nm_50c`.
- The registry now contains the St Andrews sample, air / 50 nm TiN / glass
  stack, tabulated-epsilon material model, R/T measurements, and a
  no-fit-leakage validation split.
- The validation candidate uses normal-incidence TMM over `400-1000 nm`, with
  reflectance as the first holdout and transmittance as auxiliary diagnostic.

Result:

- Decision `candidate_supported_reflectance_only`.
- The paper-backed reflectance minimum and `RT.xlsx` agree: about `20%`
  reflectance near `540 nm`, extracted as `0.20377` at `542.06 nm`.
- Pairing is good enough to run a validation candidate, but not enough for
  `calibrated_linear_evidence`.
- Transmittance scaling/noise remains auxiliary until audited.
- Thresholds remain `blocked_not_predeclared`, so the claim ceiling is
  `weak_within_dataset_holdout`.

Recommended next:

- `Phase 3C.2 - St Andrews Candidate Run Audit + Threshold Policy Decision`:
  inspect the generated fail-closed run, decide whether more source pairing
  evidence is needed, and use a Pro/GPD checkpoint before approving any future
  thresholds or calibrated-evidence policy. Planning should use GPT-5.5 `xhigh`
  if thresholds/promotion are on the table; implementation can use `medium` for
  report-only work or `high` if claim gates/contracts change.

#### Phase 3C.2: St Andrews Candidate Run Audit + Future-Only Threshold Policy

Status: completed / future-only policy prepared.

Implementation artifacts:

- `docs/phase3c2_standrews_run_audit.md`
- `docs/phase3c2_standrews_run_audit.json`
- `docs/phase3c2_future_threshold_policy.yaml`

Phase 3C.2 audits the already-inspected St Andrews candidate run and prepares a
future threshold-policy packet without promoting the run:

- `run_42fe0ad6dd295019` remains `weak_within_dataset_holdout` with
  `can_feed_serious_core: false`.
- The existing run is not promotable because residuals were inspected before
  threshold approval.
- The policy status is `pending_pro_or_user_lock_before_clean_run`.
- The policy explicitly sets `applies_to_existing_run: false` and
  `requires_clean_run_after_policy_lock: true`.
- The required future metrics are MAE, RMSE, max absolute residual, dip
  wavelength offset, and min-max shape correlation over `400-1000 nm`.

Result:

- Decision `candidate_run_audited_future_policy_prepared`.
- Historical residual context is preserved, but forbidden for threshold tuning:
  MAE about `0.0847`, RMSE about `0.178`, max absolute residual about `0.698`,
  dip offset about `-142 nm`, and min-max shape correlation about `-0.111`.
- Current blockers remain threshold predeclaration and normalization/promotion
  approval. No calibrated evidence exists yet.

Recommended next:

- `Phase 3C.3 - St Andrews Threshold Lock + Clean Run Decision`: lock the
  future-only threshold policy, run a new clean St Andrews spec, and decide
  whether the candidate can move toward Phase 4 review or should be parked as a
  failed/diagnostic lane.

#### Phase 3C.3: St Andrews Threshold Lock + Clean Run Decision

Status: completed / clean run failed thresholds.

Implementation artifacts:

- `docs/phase3c3_standrews_threshold_policy.yaml`
- `experiments/examples/linear_standrews_tin_50nm_threshold_locked_clean_run.yaml`
- `docs/phase3c3_clean_run_evaluation.md`
- `docs/phase3c3_clean_run_evaluation.json`
- `results/runs/run_f6ea582618328f44` (ignored run artifact, regenerated by CLI)

Phase 3C.3 locks a conservative reflectance-only policy before a new clean run:

- Window: `400-1000 nm`.
- Primary metric channel: St Andrews `RT.xlsx` reflectance only.
- Auxiliary channel: transmittance remains diagnostic only.
- Thresholds: MAE `<= 0.04`, RMSE `<= 0.06`, max absolute residual `<= 0.15`,
  absolute dip offset `<= 40 nm`, min-max shape correlation `>= 0.90`.
- The historical `run_42fe0ad6dd295019` is explicitly excluded from the policy.
- The St Andrews reflectance normalization gate is accepted as absolute fraction
  for this public dataset because the paper labels Figure 4 as reflectance /
  transmittance spectra and `RT.xlsx` matches the paper's reported reflectance
  minimum near `540 nm`.

Result:

- Decision `clean_run_failed_thresholds`.
- Clean run `run_f6ea582618328f44` remains unable to feed the serious core.
- All five locked metrics failed: MAE about `0.0847`, RMSE about `0.178`, max
  absolute residual about `0.698`, dip offset about `-142 nm`, and min-max
  shape correlation about `-0.111`.
- This is a meaningful negative result: the current St Andrews 50 C epsilon
  table / `RT.xlsx` pairing is not Phase 4-ready without deeper source or model
  reconciliation.

Completed follow-up:

- `Phase 3C.4 - St Andrews Failure Triage` inspected whether the failure is
  driven by material-table mismatch, roughness/substrate assumptions,
  ellipsometry-table pairing, or model limitations.

#### Phase 3C.4: St Andrews Failure Triage

Status: completed / triaged, no promotion.

Implementation artifacts:

- `src/eternity/phase3c4.py`
- `docs/phase3c4_standrews_failure_triage.md`
- `docs/phase3c4_standrews_failure_triage.json`
- `docs/phase3c4_diagnostic_sweeps.csv`

Phase 3C.4 converts the failed threshold-locked run into a reproducible
failure packet. It keeps the same no-promotion boundary while checking
residual localization, alternate St Andrews epsilon tables, selected-table
thickness sensitivity, substrate-index sensitivity, and an affine shape check.

Result:

- Decision `failure_triaged_no_promotion`.
- The failure is not a near miss: all locked metrics still fail.
- The dominant residual is at the blue edge: `400-450 nm` has MAE about
  `0.574` and bias about `-0.574`.
- No candidate St Andrews epsilon table passes the locked thresholds.
- Simple thickness or fixed substrate-index changes do not move the predicted
  dip to the measured `542.06 nm` dip or restore the required shape
  correlation.
- The leading failure mode is now source-model or material-pairing mismatch,
  with roughness/source-ellipsometry model parity and `RT.xlsx` annealing
  ambiguity as the next clean questions.

Completed next:

- `Phase 3C.5 - St Andrews Source-Model Parity Diagnostic`: inspected the raw
  Woollam `.mod/.SE` source-model assumptions for the selected 50 nm / 50 C
  file and recorded parity gaps without changing thresholds, tuning a
  replacement model, or promoting the lane.

#### Phase 3C.5: St Andrews Source-Model Parity Diagnostic

Status: completed / parity gaps recorded, no promotion.

Implementation artifacts:

- `src/eternity/phase3c5.py`
- `docs/phase3c5_standrews_source_model_parity.md`
- `docs/phase3c5_standrews_source_model_parity.json`

Phase 3C.5 inspects the source-model assumptions that are readable from the
selected St Andrews Woollam `.mod/.SE` files before any code-backed model
revision. It is a no-promotion parity packet, not a model-fitting pass.

Result:

- Decision `source_model_parity_gaps_recorded`.
- The selected source members are `50nm-MTiN-50c.mod` and
  `50nm-MTiN-50c.SE` paired with the already selected
  `50nm-MTiN-50c.txt` epsilon table.
- The source model exposes a Float Glass Cauchy substrate, a raw film
  thickness-like value of `417.36509145893865` (possibly `41.7365 nm` if the
  raw unit is Angstrom), a raw roughness-like value of `114.62616711097938`,
  and back-reflection settings.
- The clean run uses a simpler flat TiN-on-fixed-glass stack and does not model
  the source Cauchy substrate, roughness metadata, or back-reflection settings.
- These gaps explain why a source-model parity implementation may be useful,
  but they do not identify a validated replacement model and do not make the
  St Andrews lane Phase 4-ready.

Completed next:

- `Phase 3C.6A - Bounded St Andrews Source-Model Parity Implementation`:
  implemented source-derived Cauchy substrate, inferred source thickness,
  approximate roughness EMA, and approximate backside-reflection variants
  without fitting to the holdout, loosening thresholds, or promoting the lane.

#### Phase 3C.6A: Bounded St Andrews Source-Model Parity Implementation

Status: completed / parity variants failed, roughness and back-reflection
remain underdetermined.

Implementation artifacts:

- `src/eternity/phase3c6.py`
- `tests/unit/test_phase3c6.py`
- `docs/phase3c6_source_model_parity_decision.md`
- `docs/phase3c6_source_model_parity_decision.json`
- `docs/phase3c6_parity_variants.csv`

Phase 3C.6A turns the readable Phase 3C.5 source-model gaps into bounded
simulations. It implements only what can be justified from the public packet:
Float Glass Cauchy substrate, a plausible Angstrom interpretation of the raw
film/roughness length fields, a 50/50 air-TiN Bruggeman roughness estimate, and
an approximate incoherent glass-air backside estimate. It does not reproduce
CompleteEASE exactly.

Result:

- Decision `parity_variants_failed_roughness_back_reflection_underdetermined`.
- All bounded variants fail the locked Phase 3C.3 thresholds.
- The best RMSE variant is source Cauchy glass with nominal 50 nm thickness
  (`RMSE ~= 0.177976`), still failing all five metrics.
- Roughness and back-reflection parity are recorded as approximate and
  unresolved; exact CompleteEASE acquisition reduction and substrate thickness
  remain unavailable from the public packet.
- The St Andrews lane remains non-promoting, cannot feed the serious core, and
  is not Phase 4-ready.

Recommended next:

- `Phase 3B.1 - TiON Evidence Reality Check / Digitized Plot Intake`: complete
  a local TiON evidence inventory before any new validation-data search. Use
  local plot/table inspection, registry validation, plot digitizer only if
  usable plot files exist, and GPD only as a claim-boundary/phase-check mirror.
- `Phase 3C.6B` should be opened only if new St Andrews source evidence appears
  that resolves the exact roughness/back-reflection implementation or
  CompleteEASE acquisition geometry. Without that evidence, do not continue
  iterating St Andrews parity variants.

#### Phase 3B.1: TiON Evidence Reality Check / Digitized Plot Intake

Artifacts:

- `docs/phase3b1_tion_evidence_reality_check.md`
- `docs/phase3b1_tion_evidence_reality_check.json`
- `experiments/examples/linear_tion_49_tabulated.yaml`

Phase 3B.1 re-inventories the local TiON lane under the hard constraints the
user confirmed: no CompleteEASE access, no CompleteEASE contact, no TiON raw
R/T, and no St Andrews author contact.

Result:

- Decision `local_validation_data_exhausted_literature_or_external_data_needed`.
- TiON_48/TiON_49 epsilon tables and material models are registered.
- TiON_48 and TiON_49 calibration-only examples are available and capped at
  `calibration_only_no_holdout`.
- No TiON R/T measurements are registered.
- No repo-local TiON plot candidates were found for explicit
  `digitized_from_plot` intake.
- Phase 4 remains blocked because there is no independent holdout.

Recommended next:

- `Phase 3D - Literature/Public Validation Dataset Search`: search current
  literature and public repositories for a dataset with source-qualified optical
  constants plus independent R/T or ellipsometry holdout. Planning: GPT-5.5
  `high`; implementation: `medium` for search/report intake, `high` if a new
  dataset loader or material-provider path is added.
- Do not reopen Phase 3A CompleteEASE re-export, TiON raw R/T acquisition, or
  St Andrews author contact unless the user supplies new data or access.

## Near-Term Reach With Current Tools

With the V0 skeleton in place, the project can go meaningfully further before
waiting for future model releases.

Realistic current-tool milestones:

1. **Real linear ENZ digital twin**
   - Ingest ellipsometry or exported `n,k` data.
   - Fit Drude and Drude-Lorentz parameters.
   - Simulate real ITO/AZO thin films.
   - Compare predicted and measured transmission/reflection.
   - Produce reproducible reports with warnings and validity envelopes.

2. **First calibration loop**
   - Take one sample.
   - Fit material parameters from one dataset.
   - Predict another dataset.
   - Show where the model works and where it fails.
   - Track uncertainty and model limits.

3. **Pump-probe / nonlinear prototype**
   - Add simple time-dependent Drude parameters.
   - Add fluence and delay as experiment dimensions.
   - Fit relaxation times from synthetic or real pump-probe traces.
   - Compare mechanisms such as plasma-frequency modulation vs damping
     modulation.

4. **Researcher playground**
   - Let an AI read a result manifest.
   - Ask it to explain what happened.
   - Ask it to propose next simulations.
   - Ask it to identify missing physics and possible artifacts.
   - Keep it separate from validated claims.

5. **Literature and lab memory**
   - Build a local paper library around ENZ, ITO, AZO, hot electrons, temporal
     refraction, pump-probe methods, and FDTD.
   - Extract model equations, parameter ranges, and experimental conditions.
   - Connect papers to simulations and results.

6. **Higher-fidelity validation**
   - Add Meep/FDTD for selected simple cases.
   - Compare TMM vs FDTD in limits where both should agree.
   - Use FDTD when it adds scientific value, not as the foundation for
     everything.

The honest limit is that current tools should not be trusted as a fully
autonomous scientist. The useful target is a research copilot with a real
physics substrate.

The most exciting next scientific checkpoint is:

> Eternity takes one identified ENZ film dataset, currently the local TiN/TiON
> family if sample provenance is strong enough, loads or fits a constrained
> linear material model, predicts an independent measured spectrum, compares
> against holdout data, and writes a report saying exactly where it agrees and
> fails.

## V2: First Researcher Behavior

Once V0 or early V1 exists, add a small AI researcher command or notebook.

It should not claim discovery. It should do bounded reasoning:

- Read one result manifest.
- Summarize what was simulated.
- State assumptions.
- State what was not modeled.
- Compare against baseline.
- Suggest three follow-up simulations.
- Write a cautious research note.

This keeps the AI researcher dream visible from the beginning while preserving scientific discipline.

## V3: Nonlinear ENZ Dynamics

After the linear setup is validated, begin adding nonlinear material response.

Start with simple, explicit models:

- Fluence-dependent Drude parameters.
- Time-dependent plasma frequency.
- Time-dependent damping/scattering rate.
- Simple relaxation time.
- Electron-temperature-inspired response.

Then move toward richer models:

- Two-temperature-style dynamics.
- Effective mass changes.
- Nonparabolic band corrections.
- Hot-electron scattering mechanisms.
- Pump-probe delay dependence.

Every nonlinear feature must include:

- Literature provenance.
- Parameter source.
- Validity envelope.
- Baseline comparison.
- Failure modes.
- Tests against known or synthetic limits.

## V4: Higher-Fidelity Simulation

Add Meep or another FDTD backend only after the project has a clean lower-fidelity baseline.

FDTD should be used for:

- Boundary-condition-sensitive effects.
- Angle-dependent behavior.
- Subwavelength field enhancement.
- Pump-probe geometry tests.
- Multilayer or metasurface expansion.

It should not replace the simple models. It should sit above them and be forced to agree with them in limits where the simple models are valid.

## V5: Mechanism-Separating Researcher

This is where the AI researcher starts becoming more interesting.

The system should compare mechanisms, not just sweep parameters.

Example:

- Mechanism A: spectral shift from bulk temporal refraction.
- Mechanism B: spectral shift from time-dependent boundary conditions.
- Mechanism C: apparent shift from detector/spectral-window artifact.

The AI researcher should propose simulations or lab experiments that distinguish these mechanisms.

This is the first version that feels like a research collaborator rather than a plotting assistant.

## V6: Long-Term Autonomous Researcher Direction

Over the 2.5-year horizon, the AI researcher can gradually gain more autonomy:

- Read new papers and add them to lab memory.
- Extract model equations and parameter ranges.
- Generate experiment specs.
- Run cheap models.
- Queue expensive simulations.
- Compare simulation levels.
- Identify disagreement between literature, simple theory, high-fidelity simulation, and lab data.
- Propose next experiments.
- Draft research notes.
- Maintain a failed-hypothesis archive.
- Build a case for possible novelty.

Even at this stage, human review remains central. The AI can accelerate search and synthesis, but the project should keep scientific claims gated by validation.

## Later Model-Customization Track

Down the line, Eternity may benefit from model customization tools such as
Unsloth Studio or Thinking Machines Lab's Tinker-style managed fine-tuning. They
should not be used to train the physics simulator itself. Their likely value is
training or adapting smaller specialist models around Eternity's accumulated
research process.

Possible later uses:

- A local experiment-spec drafting model trained on accepted Eternity specs.
- A result-critique model trained to flag missing assumptions, bad units,
  unsupported claims, and validity-envelope violations.
- A literature triage model trained on promoted vs rejected ENZ papers.
- A report-drafting assistant that follows Eternity's cautious reporting style.
- A mechanism-comparison assistant that proposes alternative explanations from
  structured result manifests.

Use this track only after the project has enough high-quality internal data:

- Accepted and rejected experiment specs.
- Result manifests with human critiques.
- Literature notes with quality labels.
- Failed-hypothesis records.
- Reports that clearly separate evidence from speculation.

Unsloth Studio is likely most useful for local no-code or low-code fine-tuning
and side-by-side model comparison. Thinking Machines credits would be most useful
for managed post-training or reinforcement-style fine-tuning if Tinker access is
available and the project has a clean training/evaluation dataset.

This track should stay downstream of the serious core:

```text
validated registry -> curated training examples -> fine-tuned helper model ->
held-out evaluation -> optional use in researcher playground
```

Do not fine-tune on raw papers, raw lab data, or unreviewed AI outputs and then
trust the result. For Eternity, customization should teach process discipline,
not invent physics authority.

## What Success Could Look Like By The End Of The PhD Window

An ambitious but realistic 2.5-year outcome:

- A working ENZ digital-twin codebase.
- Several real lab datasets ingested.
- Material parameters fit for specific samples.
- Linear and nonlinear simulations with provenance.
- Meep/FDTD validation for selected cases.
- A lab-memory system with papers, notes, datasets, and failed ideas.
- An AI researcher prototype that proposes mechanism-separating simulations.
- Optional fine-tuned helper models for spec drafting, result critique,
  literature triage, or report style.
- Reproducible research reports that could support thesis work or paper ideation.
- A clear record of where the model succeeded, failed, and suggested useful experiments.

The win is not necessarily "AI independently discovers new physics."

The win is:

> We built a system that makes AI meaningfully participate in ultrafast ENZ research instead of merely talking about it.

## Immediate Next Step

Choose `Phase 3D.1C - Exeter/Bohn package-constant no-fit model reconstruction`.

Recommended decision scope:

```text
1. Use the Phase 3D.1B split lock and canonical artifacts as immutable inputs:
   Figure 1 epsilon, Figure 2 TIR reference, and Figure 2 static `R0`.
2. Reconstruct the package static Figure 2 model path with locked material,
   thickness, incident-index, angle-offset, and normalization choices.
3. Keep Phase 3A, Phase 3B, and Phase 3C parked unless new evidence appears;
   do not loop on unavailable CompleteEASE, TiON raw R/T, or St Andrews author
   contact paths.
```

First implementation target:

```text
Create a Phase 3D.1C no-fit reconstruction packet. Do not tune material
parameters, thickness, incident index, angle offset, vertical scale, wavelength
axis, or thresholds after inspecting Figure 2 residuals.
```

First output:

```text
docs/phase3d1c_exeter_bohn_no_fit_reconstruction.md
docs/phase3d1c_exeter_bohn_no_fit_reconstruction.json
```

The decision packet should include:

- Which package constants and nuisance values were used without tuning.
- Which solver path reconstructs the package static reflection calculation.
- Residual metrics against the locked static `R0` surface.
- Whether the result is `weak_within_dataset_holdout`, `failed_validation`, or
  a Phase 4 candidate needing final promotion review.
- Whether the Saha TiN/AZO backup should be inspected next if Exeter/Bohn fails.

That is the next brick on the direct path toward the AI researcher.

#### Phase 3D.1: Exeter/Bohn ITO Package Intake

Artifacts:

- `docs/phase3d1_exeter_bohn_ito_package_intake.md`
- `docs/phase3d1_exeter_bohn_ito_package_intake.json`
- `lab_data/raw/public_exeter_bohn_ito_2021/OpenData.zip`

Result:

- Downloaded and hash-verified the public Exeter/Bohn ITO ENZ package from DOI
  `10.24378/exe.3004`.
- The package is a real data/code archive with Figure 1 optical constants,
  notebooks, CSVs, Mathematica code, EPS/SVG figures, and TIR/reflection
  experiment tables.
- This intake did not promote any claim; it only made Phase 3D.1A possible.

#### Phase 3D.1A: Exeter/Bohn Calibration-Holdout Split Audit

Artifacts:

- `docs/phase3d1a_exeter_bohn_split_audit.md`
- `docs/phase3d1a_exeter_bohn_split_audit.json`

Decision:

- Status: `split_audit_promising_no_fit_reconstruction_needed`.
- Current claim ceiling: `weak_within_dataset_holdout`.
- Can feed serious core: `false`.
- Can promote calibrated evidence: `false`.
- Phase 4 ready: `false`.

Findings:

- Figure 1 provides source-qualified ellipsometry-derived ITO epsilon over
  `1046.10498`-`1684.096069` nm.
- Figure 2 provides the best static holdout candidate: TIR-normalized pre-pump
  reflection reconstructed as `R0 = mean(power_norm for delay <= -0.4 ps)`.
- Figure 2 has 65,286 experiment rows, all diagonal in
  `wavelength_1 == wavelength_2`, with 8,866 pre-pump rows.
- Figure 3/4 remain auxiliary because their first-use split is less clean.
- The package is promising but cannot be promoted yet because the notebook
  already compares experiment to static model and uses hard-coded Drude/geometry
  constants that must be locked before residual inspection.

Recommended next:

- `Phase 3D.1B - Exeter/Bohn no-fit static R0 extraction and split lock`.
- Extract Figure 1 optical constants and Figure 2 TIR/pre-pump `R0` into
  canonical artifacts.
- Lock a calibration/holdout split that forbids Figure 2 reflection rows from
  fitting.
- Run only package-constant/no-fit reconstruction before emitting residuals.

#### Phase 3D.1B: Exeter/Bohn No-Fit Static R0 Extraction and Split Lock

Artifacts:

- `docs/phase3d1b_exeter_bohn_static_r0_extraction.md`
- `docs/phase3d1b_exeter_bohn_static_r0_extraction.json`
- `docs/phase3d1b_exeter_bohn_split_lock.yaml`
- `lab_data/raw/public_exeter_bohn_ito_2021/exeter_bohn_ito_fig1_epsilon.csv`
- `lab_data/raw/public_exeter_bohn_ito_2021/exeter_bohn_fig2_tir_reference.csv`
- `lab_data/raw/public_exeter_bohn_ito_2021/exeter_bohn_fig2_static_r0.csv`

Decision:

- Status: `static_r0_extracted_split_locked_no_residuals`.
- Current claim ceiling: `weak_within_dataset_holdout`.
- Can feed serious core: `false`.
- Can promote calibrated evidence: `false`.
- Phase 4 ready: `false`.

Findings:

- Figure 1 epsilon is now a canonical 187-row CSV over
  `1046.10498`-`1684.096069` nm, with ENZ crossing at `1233.996861` nm.
- Figure 2 TIR normalization is now a 31-row locked reference.
- Figure 2 static pre-pump `R0` is now an 806-row surface over 31 wavelengths
  and 26 prism angles, with 11 pre-pump rows averaged per grid point.
- The registry records the Figure 1 epsilon artifact, sample, stack mirror,
  measurement, and tabulated material model; the 2D `R0` surface remains governed
  by the split-lock YAML rather than being misregistered as a 1D spectrum.
- No residuals were run and no claim was promoted.

Recommended next:

- `Phase 3D.1C - Exeter/Bohn package-constant no-fit model reconstruction`.
- Use only the locked Phase 3D.1B artifacts and package constants/nuisance
  values.
- Compare to the locked `R0` surface only after the model path is frozen.
- Emit a residual report and conservative claim-status decision.

### Pivot If Phase 3D Fails

If the strongest public packages cannot honestly support a calibrated-linear
evidence attempt, keep the evidence bar intact and pivot the near-term milestone
to the executive research assistant / public-dataset gate:

```text
public dataset gate -> candidate registry -> failed-validation memory ->
conservative fixtures -> executive research assistant workflows
```

This pivot is recorded in
`docs/pivots/executive_research_assistant_fallback.md`.

The executive assistant lane should stay inside Eternity rather than splitting
into a separate project by default. It becomes the user-facing right-hand layer
for planning, summaries, prompts, reports, dataset triage, phase tracking, and
evidence-aware next actions, while Serious Core keeps ownership of scientific
claim validation.

## Pro Model Checkpoints

Eternity should periodically ask for outside input from 5.5 Pro, or whatever the
current best Pro reasoning model is, when the project enters hard or unknown
territory. This is not for routine implementation. It is for checkpoint gates
where better abstract reasoning could materially change the path.

Use this process before:

- Unknown physics or material-modeling choices.
- Major architecture decisions that will be hard to reverse.
- Surprising simulation results.
- Possible novelty claims.
- Failed validation loops where the reason is unclear.
- Phase transitions such as V0 to V1, linear to nonlinear, or local simulator to
  FDTD.

When a checkpoint is warranted, the assistant should say:

```text
Pro checkpoint recommended
```

Then it should explain why in 2-4 bullets and provide a compact prompt the user
can paste into the current Pro model.
