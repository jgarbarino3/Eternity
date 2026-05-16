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

Status: active, fail-closed validation candidate implemented

Decisive outputs:

- Immutable raw snapshots under `lab_data/raw/thesis_phase3a/` for
  `30_20_10` reflectance, p/s intensity, Psi/Delta, derived e1/e2, and SiO2
  Sellmeier epsilon.
- Registry mapping from `30_20_10` to thesis `d_10nm` / `3L2/Quartz` with the
  incident-order stack `air / 20 nm TiN / 10 nm SiO2 / 30 nm TiN / quartz`.
- Registry-backed multilayer TMM example
  `experiments/examples/linear_tin_sio2_d10nm_validation_candidate.yaml`.
- Validation candidate run `results/runs/run_74411c01c8a4b74e`, capped at
  `weak_within_dataset_holdout`, with calibrated promotion blocked by
  `thresholds_predeclared` and `normalization_gate`.

Stop/rethink conditions:

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
