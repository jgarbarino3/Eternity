# Eternity Goals

Date: 2026-05-07

## Active Codex Goal

Build Eternity into an automated AI researcher for ultrafast ENZ optics.
Long-term, it should ingest documents and web sources, plan investigations, run
structured multi-step research, preserve evidence trails, synthesize cited
findings, and improve its research workflow over time.

Short-term implementation choices should connect back to that direction while
treating the first major milestone as a lab twin.

## First Major Milestone

Turn the current synthetic V0 runner into a first calibrated linear evidence
milestone:

> Given one explicitly identified sample/stack, use calibration-only optical
> data to produce or load a physically constrained material model, freeze that
> model, predict an independent linear transmission/reflection or ellipsometry
> holdout measurement under recorded geometry, and produce a report whose claim
> status is machine-gated by provenance, split integrity, physics sanity,
> numerical reproducibility, and residual/uncertainty checks.

Evidence labels must stay explicit:

- `synthetic_software_fixture`
- `literature_reproduction_fixture`
- `calibration_only_no_holdout`
- `weak_within_dataset_holdout`
- `calibrated_linear_evidence`
- `failed_validation`

Only `calibrated_linear_evidence` can feed serious-core conclusions.

## Current State

The repo currently has a working V0 skeleton and an active V1 real-data
grounding phase:

- `uv run --no-editable pytest` passes.
- `uv run --no-editable eternity validate experiments/examples/linear_ito_toy.yaml`
  validates the example spec.
- `uv run --no-editable eternity run experiments/examples/linear_ito_toy.yaml`
  writes deterministic artifacts under `results/runs/run_47d4e2d9baa7f574/`.
- TiN/TiON optical-constants snapshots and thesis reflectance spectra are being
  registered as immutable `lab_data/raw/...` artifacts with SHA-256 hashes.
- `experiments/examples/linear_tion_48_tabulated.yaml` is the first tabulated
  TiON grounding run. Its strongest permitted status is
  `calibration_only_no_holdout`.
- The active named phase is `Phase 3A - TiN/SiO2 thesis reflectance
  reconciliation`: map the thesis/paper measured spectra and `30_20_10`
  reflectance/Psi/Delta/e1e2 exports to exact samples, geometry,
  normalization, and a holdout policy, then emit a fail-closed validation
  candidate whose ceiling is `weak_within_dataset_holdout`.
- The active follow-up is `Phase 3A.1 - normalization and threshold gate
  hardening`: preserve the already-inspected residuals as historical context,
  keep the current run blocked, and prepare source-backed policy for future
  predeclared validation.
- The active correction is `Phase 3A.2 - stack mapping correction`: preserve
  the thesis-supported `d_10nm` / `3L2/Quartz` mapping, but remove the separate
  `30_20_10` files from the validation candidate until their provenance is
  proven.
- The active provenance closure is `Phase 3A.3 - thesis figure/data provenance
  reconciliation`: align `d_10nm` text exports with thesis Figure 4.1 while
  recording normalization as `relative_intensity_only`.
- The completed retrieval phase is `Phase 3A.5 - source-backed export /
  provenance retrieval`: a bounded local/SDSU/Google Drive search found related
  RC2/CompleteEASE, thesis, SDSU slide/report, and scanned lab-notebook
  provenance, but no exact export/project/recipe/lab-note proof that the
  `d_10nm` `Intensity` columns are calibrated absolute `%R`.
- The active packet phase is `Phase 3A.6 - CompleteEASE re-export /
  measurement packet`: use the exact source-evidence request and future-only
  policy boundary before any future absolute-reflectance validation run.
- The active recovery phase is `Phase 3A.7 - CompleteEASE source recovery +
  3L2 provenance lock`: a read-only scanner now records local `.SE`, `.SEsnap`,
  `.iSE`, and DoD SAFE zip-contained candidates. It strengthens source
  provenance but keeps absolute reflectance blocked.
- The active triage result is `Phase 3A.8 - Source candidate triage +
  relative-only diagnostic decision`: it deduplicates recovered candidates,
  prioritizes quartz 10 nm dynamic files for manual follow-up, classifies Si
  control files separately, and pivots Phase 3A to relative-only diagnostics
  unless a source-backed absolute export or new measurement appears.
- The active diagnostic result is `Phase 3A.9 - Relative-only diagnostic run
  packet`: it reports spectral shape, dip position, trend direction, and
  figure-provenance diagnostics for the existing run while keeping serious-core
  and calibrated-evidence promotion forbidden.
- The active branch decision is `Phase 3A.10 - Manual source follow-up vs
  Phase 3B return`: do one bounded manual follow-up pass on the top three
  quartz dynamic `.SEsnap` candidates, then fall back to Phase 3A.6 or Phase 3B
  if exact source/calibration proof is not found.
- The active packet result is `Phase 3A.11 - Bounded manual source follow-up
  packet`: the three-candidate review scope, proof gates, stop rules, and
  forbidden uses are now written as repo artifacts.

This is a synthetic thin-film experiment runner, not yet a calibrated lab twin.
The active step is to keep source-qualified TiN/TiON optical constants, thesis
reflectance spectra, material models, and provenance gaps inside the registry
without promoting them to calibrated evidence.

Current blocker:

- TiON_48/TiON_49 raw R/T spectra and authoritative FROG-label mapping are not
  registered. Until that is fixed, TiON runs cannot emit
  `calibrated_linear_evidence`.
- TiON grower guidance and attached plots are useful provenance, but they are
  not raw sample-matched R/T tables unless explicitly digitized and labeled as
  plot-derived evidence.
- Phase 3A normalization certainty and predeclared residual thresholds are not
  yet resolved, so no Phase 3A run may promote to `calibrated_linear_evidence`.
- Phase 3A.1 does not have enough information to pass normalization or threshold
  gates. It can only audit and harden those gates until Pro/user-approved policy
  is recorded before a future run.
- Phase 3A.2 does not have enough information to use `30_20_10` as thesis
  `d_10nm` evidence. A Woollam project file, plotting script, lab note, or other
  source link is still needed.
- Phase 3A.3 does not have enough information to claim absolute reflectance.
  The thesis/figure evidence is enough for provenance, not calibration.
- Phase 3A.4 keeps that result fail-closed after checking the local thesis,
  figures, copied data hashes, CompleteEASE manual evidence, and nearby
  Woollam/CompleteEASE artifacts. A new export, project/recipe record, lab note,
  or Pro/user-approved relative-only policy is still needed before any future
  calibrated-evidence attempt.
- Phase 3A.5 has now searched the likely local source locations, the desktop
  SDSU Google Drive folder, targeted Google Drive thesis/defense hits, and the
  scanned lab notebook. It keeps the status at `blocked_needs_new_export`. The
  current data are still useful for provenance and relative-intensity
  diagnostics, but not for calibrated promotion.
- Phase 3A.6 has enough information to request or perform a clean re-export /
  measurement intake. It does not yet have enough information to approve
  absolute normalization, write numeric thresholds, or promote any existing run.
- Phase 3A.7 has enough information to confirm the thesis-backed `3L2/Quartz`
  stack and to rank related local CompleteEASE/Woollam source candidates. It
  still does not have enough information to treat exported `Intensity` columns
  as calibrated absolute `%R`.
- Phase 3A.8 has enough information to compare spectral shape, dip position,
  trend direction, and figure provenance as relative-only diagnostics. It does
  not have enough information to feed the serious core or promote any Phase 3A
  run above `weak_within_dataset_holdout`.
- Phase 3A.9 has enough information to preserve the current relative-shape
  agreement as a useful diagnostic clue. It does not have enough information to
  convert that clue into absolute reflectance validation or calibrated evidence.
- Phase 3A.10 has enough information to choose bounded manual source follow-up
  before returning to Phase 3B. It does not have enough information to unpark
  TiON as calibrated evidence, because raw sample-matched R/T is still missing.
- Phase 3A.11 has enough information to guide the manual review of the three
  candidate source files. It does not itself prove absolute reflectance,
  exact source identity, or calibrated-evidence readiness.

## Goal Usage In Codex

Codex goals are thread-scoped objective state, not normal repo files and not a
visible standalone `codex goals` CLI command in the current local CLI build.
Use a prompt like this at the start of a new Eternity thread:

```text
Set this thread goal: Build Eternity into an automated AI researcher for
ultrafast ENZ optics. Long-term, it should ingest documents and web sources,
plan investigations, run structured multi-step research, preserve evidence
trails, synthesize cited findings, and improve its research workflow over time.
In this thread, connect short-term implementation choices back to that long-term
direction while treating the first major milestone as a lab twin.
```

Then make the turn prompt concrete:

```text
Start by reading the repo and advancing the first lab-twin milestone. Do not
make nonlinear or novelty claims from synthetic runs.
```

## Operating Rules

- Keep the serious physics core separate from speculative researcher-playground
  ideas.
- The playground may suggest; the serious core verifies.
- Every scientific result must state model level, assumptions, synthetic vs
  measured inputs, warnings, validity envelope, and follow-up needed.
- Passing tests or producing plots is not evidence of new physics.
- Before moving from V0 to V1, linear to nonlinear, or local simulator to FDTD,
  use the Pro checkpoint gate described in `AGENTS.md`.
