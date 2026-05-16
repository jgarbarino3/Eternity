# Phase 3A.1 Normalization Audit

Date: 2026-05-16

## Decision

Current state: **blocked**.

The thesis/exported columns are registered as `Intensity`, while the thesis
figure plots the same scale as `Reflectance`. Phase 3A.3 therefore records the
current basis as `relative_intensity_only`, not source-confirmed absolute
reflectance. These data are valid measured/provenance inputs for the Phase 3A
comparison, but they are not yet sufficient for `calibrated_linear_evidence`.

## Current Evidence

- `thesis_reflectance_d_10nm_initial_measurement` is mapped to
  `thesis_d_10nm` / `3L2/Quartz` by thesis Table 4.1 and Figure 4.1.
- The separate `30_20_10` Coding/txt exports are no longer treated as
  `d_10nm` auxiliary evidence; Phase 3A.2 keeps them in an unresolved candidate
  bundle.
- Thesis text in the registry identifies the three-layer reflectance geometry
  as S-polarized / TE at 60 degrees.
- Phase 3A.3 links the table scale to the local thesis Figure 4.1 PNG and
  CompleteEASE in-situ screenshot.
- The raw reflectance table was copied without smoothing or normalization
  changes.
- The Phase 3A run reports `normalization_gate: blocked` because the holdout
  export is labeled `Intensity/arb`.

## Gate Policy

The machine-readable policy is `docs/phase3a1_threshold_policy.yaml`.

Allowed normalization states:

- `unknown`: no source-backed decision.
- `relative_intensity_only`: useful for shape/provenance comparison only.
- `absolute_reflectance_confirmed`: may be used for future calibrated-evidence
  threshold policy if the source evidence is recorded before the future run.

No current Phase 3A run may pass the normalization gate until the policy records
`absolute_reflectance_confirmed` with source evidence.
