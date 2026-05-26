# Research State

## Project Reference

See: GPD/PROJECT.md (updated 2026-05-19)

**Machine-readable scoping contract:** `GPD/state.json` field `project_contract`

**Core research question:** Can Eternity build a calibrated ENZ linear digital twin from source-qualified TiN/TiON optical constants and measured holdout spectra without overclaiming?
**Current focus:** Phase 3G Research Memory / Executive Research Assistant measured-data intake queue

## Current Position

**Current Phase:** 3G
**Current Phase Name:** Research Memory / Executive Research Assistant Measured-Data Intake Queue
**Total Phases:** 3
**Current Plan:** docs/phase3f1f_measured_data_scouting_decision.md
**Total Plans in Phase:** 15
**Status:** Active / Phase 3F.1F measured-data scouting paused
**Last Activity:** 2026-05-26
**Last Activity Description:** Completed Phase 3F.1F by pausing measured-data scouting after Phase 3F.1 through Phase 3F.1D produced 0 measured-data hard-gate passes across 37 leads and Phase 3F.1E supplied only non-promoting code-regression coverage. Phase 3F.2 intake, measured residual modeling, and Phase 4 remain closed. Next remembered work is Phase 3G: build the Research Memory / Executive Research Assistant measured-data intake queue.

**Progress:** [██████████] 99%

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
- Phase 3C.2 wrote `docs/phase3c2_standrews_run_audit.md`, `.json`, and
  `docs/phase3c2_future_threshold_policy.yaml`: `run_42fe0ad6dd295019`
  remains non-promotable, `applies_to_existing_run` is false, and the next
  calibrated-evidence attempt would require thresholds locked before a new
  clean run.
- Phase 3C.3 wrote `docs/phase3c3_standrews_threshold_policy.yaml`,
  `experiments/examples/linear_standrews_tin_50nm_threshold_locked_clean_run.yaml`,
  and `docs/phase3c3_clean_run_evaluation.md` / `.json`: clean run
  `run_f6ea582618328f44` failed all five predeclared metrics and is not ready
  for Phase 4 review.
- Phase 3C.4 wrote `docs/phase3c4_standrews_failure_triage.md`, `.json`, and
  `docs/phase3c4_diagnostic_sweeps.csv`: failure is not a near miss, blue-edge
  residuals dominate, no alternate St Andrews epsilon table passes the locked
  thresholds, and simple thickness/substrate-index sweeps do not repair the
  shape or dip.
- Phase 3C.5 wrote `docs/phase3c5_standrews_source_model_parity.md` and
  `.json`: raw Woollam `.mod/.SE` inspection found Float Glass Cauchy
  substrate assumptions, film-thickness/roughness metadata, and
  back-reflection settings missing from the current clean-run stack. The lane
  remains non-promoting and not Phase 4-ready.
- Phase 3C.6A wrote `docs/phase3c6_source_model_parity_decision.md`,
  `.json`, and `docs/phase3c6_parity_variants.csv`: bounded source Cauchy
  substrate, inferred source thickness, approximate roughness EMA, and
  approximate backside-reflection variants all failed the locked thresholds.
  Exact roughness/back-reflection parity remains underdetermined, so St Andrews
  is parked before Phase 4.
- Phase 3B.1 wrote `docs/phase3b1_tion_evidence_reality_check.md` and
  `.json`: TiON_48/TiON_49 epsilon tables, material models, and
  calibration-only examples are available, but the registry has no TiON R/T
  measurements and the repo scan found no usable plot candidates. Decision is
  `local_validation_data_exhausted_literature_or_external_data_needed`.
- Phase 3E.1 wrote `docs/phase3e1_public_dataset_gate_assistant_scaffold.md`,
  `.json`, `docs/phase3e1_claim_status_summary.json`, and the candidate
  registry. The current registry evaluates 15 candidates and opens 0 Phase 4
  candidates.
- Phase 3E.2A wrote `docs/phase3e2a_wang_wo3_baseline_intake.md` and
  `.json`: selected Wang W/WO3 Figshare spreadsheets are public and
  MD5-verified. `FigS2-nk.xlsx` provides direct W/WO3 `n,k` tables, but
  `Fig2f-R.xlsx` contains offset/unlabeled plotted traces, so Wang remains only
  a non-ENZ planar TMM baseline candidate.
- Phase 3E.2B-3E.2D wrote Wang semantics, de-offseted fixture, and handoff
  artifacts. The source paper/SI back the figure-level measured/simulated
  semantics and model inputs, but the workbook lacks explicit measured/simulated
  labels, so Wang is locked as `literature_reproduction_fixture`, not validation.
- Phase 3E.3A wrote `docs/phase3e3a_saha_exported_table_audit.md` and
  `.json`, plus four canonical Saha CSVs under
  `lab_data/raw/public_saha_tin_azo_2023/`. The measured/source-simulated
  split and 50-degree s/p semantics are source-backed, but the TMM adapter is
  blocked before residuals because the source tables do not freeze silicon
  substrate optical constants, substrate/backside handling, or full leakage
  boundaries.
- Phase 3E.3B wrote `docs/phase3e3b_saha_stack_model_gate.md` and `.json`.
  It found the Saha stack order, thickness, 50-degree s/p geometry, and
  canonical material tables source-backed, but failed the frozen-stack gate
  because silicon optical constants, substrate/backside/coherence handling, and
  interface/oxide assumptions are not source-backed tightly enough for a no-fit
  TMM residual run.
- Phase 3E.4 wrote `docs/phase3e4_renewed_public_data_search.md` and `.json`,
  updated the public candidate registry to 15 candidates, and regenerated the
  Phase 3E.1 gate scaffold. It inspected ACS/intracavity Zenodo, Linkoping
  ITO/PEDOT, ITO/glass/SiO2, space-time ITO, natural-ENZ compendium, LBSO, and
  ENZ metal-oxide reflector leads. Zero Phase 4 candidates opened.
- Phase 3E.5 wrote `docs/phase3e5_saha_sensitivity_fixture.md`, `.json`, and
  `docs/phase3e5_saha_sensitivity_curves.csv`. Twelve external
  silicon/interface/backside variants were compared as diagnostics only. The
  spread is small under the tested assumptions, but Saha remains
  non-promoting because the author substrate/backside/source-model contract is
  not recovered and residual-driven variant selection would leak.
- Phase 3F.1 wrote `docs/phase3f1_simulator_validation_scout.md`, `.json`,
  `docs/phase3f_simulator_validation_candidate_registry.yaml`, and the
  `phase3f1-simulator-validation-scout` CLI. Ten public simple/thin-film-
  adjacent candidate cards were gated; zero cleared every hard flag, no Phase
  3F.2 intake opened, no TMM adapter started, and no residual modeling was run.
- Phase 3F.1B wrote `docs/phase3f1b_pro_lead_candidate_registry.yaml`,
  `docs/phase3f1b_pro_lead_gate.md`, and `.json`. Sixteen pasted GPT-5.5 Pro
  leads were gated; zero cleared every hard flag, no Phase 3F.2 intake opened,
  no TMM adapter started, and no residual modeling was run.
- Phase 3F.1C wrote `docs/phase3f1c_source_file_audit.md` and `.json`. The
  top-three practical fallback packages were downloaded, hash-verified, and
  inspected. Structural color FROC lacks an open measured spectral holdout
  package, FROC 2021 measured data are Origin OPJ containers, and ultrathin Au
  is leakage-blocked by same-measurement fitting plus request-only processing
  code. Zero cleared every hard flag, no Phase 3F.2 intake opened, no TMM
  adapter started, and no residual modeling was run.
- Phase 3F.1D wrote `docs/phase3f1d_benchmark_fixture_candidate_registry.yaml`,
  `docs/phase3f1d_benchmark_fixture_gate.md`, and `.json`. Eight targeted
  benchmark/source-data or software-fixture leads were gated. Zero measured-data
  candidates cleared every hard flag. The selected next lane is
  `structural_color_froc_2023_code_parity_fixture` as a non-promoting
  code-regression fixture; ultrathin Au remains only a secondary parser fixture.
- Phase 3F.1E wrote `src/eternity/phase3f1e.py`,
  `tests/unit/test_phase3f1e.py`,
  `docs/phase3f1e_code_regression_fixture.md`, and `.json`. The pinned
  `structural_color_FROCs` archive hash matched, and 3 deterministic parity
  cases passed with max R/T deltas below `2e-16`. This is code-regression
  coverage only, not measured validation.

## Open Questions

- Should Phase 3F pause measured-data scouting now that code-regression coverage
  exists, or should it open one more narrower public measured-data search?
- Which stricter simple public planar thin-film dataset can later provide
  source-qualified optical constants plus independent R/T or ellipsometry
  holdout without author contact, so Phase 3F.2 can eventually open?
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
- [Phase 3C.2]: St Andrews residuals are historical context only. — A future
  threshold policy now exists, but it has `applies_to_existing_run: false` and
  cannot promote `run_42fe0ad6dd295019`.
- [Phase 3C.3]: St Andrews threshold-locked clean run failed. — The public
  dataset reflectance normalization is acceptable for this policy, but the
  current 50 C epsilon / RT.xlsx pairing fails all five metrics and is not
  Phase 4-ready.
- [Phase 3C.4]: St Andrews failure triage points to source-model parity. — The
  failure is not a near miss; blue-edge residuals dominate, alternate tables do
  not pass, and simple thickness/substrate sweeps do not repair the shape.
- [Phase 3C.5]: St Andrews source-model parity gaps are real but
  non-promoting. — The raw Woollam source model includes Float Glass Cauchy
  substrate, film-thickness/roughness metadata, and back-reflection settings
  absent from the clean run, but those gaps do not validate a replacement model
  or calibrated promotion.
- [Phase 3C.6A]: Bounded St Andrews source-model parity does not rescue the
  lane. — Source-derived variants still fail locked thresholds; roughness and
  back-reflection remain approximate, so stop before Phase 4 unless new source
  evidence appears.
- [Phase 3B.1]: Local TiON validation evidence is exhausted. — TiON_48/TiON_49
  epsilon tables and calibration-only examples are available, but no raw R/T
  measurements or repo-local plot candidates exist; the next validation-data
  path is literature/public search.
- [Phase 3E.3A]: Saha is source-table-ready but TMM-blocked. — Canonical
  measured reflectance and material epsilon artifacts now exist, but no residual
  model may run until a frozen substrate/backside model contract is recorded
  before looking at residuals.
- [Phase 3E.3B]: Saha remains canonical source-table memory only. — The
  source package does not freeze silicon optical constants,
  substrate/backside/coherence handling, or interface/oxide assumptions, so no
  no-fit TMM adapter or residual report may run from guessed settings.
- [Phase 3E.4]: Renewed public-data search keeps Phase 4 closed. — The newest
  inspected leads are useful fixtures or blocked cards, but none clears the
  measured holdout, stack/substrate/backside, and leakage gates required before
  residual inspection.
- [Phase 3E.5]: Saha sensitivity is non-promoting. — The tested
  silicon/interface/backside variants produce small spread, but every variant
  is an external assumption, the source-simulated Fig. 2b curves are
  author-curve context, and no residual-driven selection is allowed.
- [Phase 3F.1]: The first simulator-validation scout found no intake-ready
  simple stack. — Ten public simple/thin-film-adjacent leads were useful
  failure memory, but zero cleared the full material/holdout/geometry/stack/
  substrate/backside/leakage/hash gate, so Phase 3F.2 remains closed.
- [Phase 3F.1B]: The 5.5 Pro lead list found no intake-ready candidate either.
  — Sixteen pasted leads yielded useful fallback/rejection memory, but zero
  cleared the full hard gate, so Phase 3F.2 remains closed.
- [Phase 3F.1C]: The top-three source-file audit found no intake-ready
  candidate either. — Structural color FROC, FROC 2021, and ultrathin Au each
  failed at least one hard gate, so Phase 3F.2 remains closed.
- [Phase 3F.1D]: The targeted benchmark/source-data follow-up found no
  measured-data candidate either. — Eight leads yielded zero hard-gate passes,
  so the only active next lane is a non-promoting code-regression fixture
  against `structural_color_FROCs`.
- [Phase 3F.1E]: The selected code-regression fixture passed. — Three
  deterministic TMM parity cases matched the current backend below `2e-16`, but
  this is not measured validation and does not open Phase 3F.2.
- [Phase 3F.1F]: Measured-data scouting is paused for now. — The current broad
  search envelope produced 0 measured-data hard-gate passes across 37 leads, so
  the next useful lane is Phase 3G assistant-facing intake, not another broad
  search.
- [Phase 3A]: Phase 3A validation candidates are capped at `weak_within_dataset_holdout`. — Normalization certainty and predeclared thresholds are still missing, and residuals have now been inspected only under that capped status.
- [Phase 3A.1]: Existing residuals are historical context only. — Threshold policy must apply to a future run unless it was recorded before the run being judged.

### Active Approximations

- Phase 3C.6A roughness uses a 50/50 air-TiN Bruggeman EMA layer for bounded
  testing only.
- Phase 3C.6A back-reflection uses a thick lossless incoherent glass-air
  backside estimate for bounded testing only.

**Convention Lock:**

No conventions locked yet.

### Propagated Uncertainties

None yet.

### Pending Todos

- Phase 3G: build a Research Memory / Executive Research Assistant measured-data
  intake queue that preserves the Phase 3E/3F gates, rejection memory, and
  pause/resume rules for future source-backed leads.
- Record Pro/user-approved Phase 3A residual thresholds before any future residual-gated pass/fail run.
- Retrieve source-backed export/recipe/project/lab-note evidence if thesis
  exported intensity spectra are to be treated as absolute reflectance.
- Phase 3A.6 packet remains archived as the acceptance template if new source
  evidence or a future measurement appears; CompleteEASE re-export is not
  available under current constraints.
- Bring back Pro/user guidance for Phase 3A.1 absolute-normalization and future threshold policy.
- Find source evidence for the `30_20_10` filename-to-sample mapping, or leave it parked as unresolved provenance.
- Later, run a sandboxed `google-research/era` fit trial only for scorable
  code-generation loops such as parser experiments, fixture regressions, or
  bounded model-variant sweeps. Do not adopt ERA as an Eternity backend or
  evidence/claim authority without that trial.

### Blockers/Concerns

- CompleteEASE access/contact, TiON_48/TiON_49 raw R/T, and St Andrews author
  contact are unavailable under the user's stated constraints.
- TiON_48/TiON_49 raw R/T spectra are not registered.
- FROG labels are not authoritatively mapped to TiON_48/TiON_49.
- Phase 3A `thresholds_predeclared` gate is blocked.
- Phase 3A `normalization_gate` is blocked.
- `30_20_10` filename-to-thesis provenance is unresolved.
- Absolute reflectance calibration for thesis `Intensity` exports remains
  unresolved and currently blocked after Phase 3A.8 source triage, even with
  related CompleteEASE/Woollam source candidates.
- Phase 3C.6A keeps St Andrews non-promoting; do not proceed to Phase 4, change
  thresholds, contact authors, or choose more source-model variants without new
  evidence for exact roughness/back-reflection or CompleteEASE acquisition
  parity.

## Session Continuity

**Last session:** none
**Stopped at:** none
**Resume file:** none
**Last result ID:** none
**Hostname:** none
**Platform:** none
