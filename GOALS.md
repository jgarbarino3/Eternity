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
