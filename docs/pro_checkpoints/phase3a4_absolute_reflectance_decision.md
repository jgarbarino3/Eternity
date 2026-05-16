# Phase 3A.4 Pro Checkpoint

Date: 2026-05-16

## Why This Checkpoint Exists

Phase 3A.4 resolves the local evidence search fail-closed: thesis text and
figures support measured reflectance provenance, but the raw exported column is
still labeled `Intensity`. A calibrated-evidence threshold policy would be
scientific judgment, not a mechanical coding choice.

Use this checkpoint before:

- treating the `d_10nm` export as absolute reflectance;
- choosing wavelength windows or residual thresholds;
- allowing any future Phase 3A run to promote above
  `weak_within_dataset_holdout`.

## Paste-Ready Prompt

```text
Review Eternity Phase 3A.4: thesis d_10nm/3L2 reflectance validation has text
exports labeled Intensity, thesis plots labeled Reflectance, and no hard proof
yet that the exported values are calibrated absolute reflectance. Decide whether
this supports absolute reflectance, relative-only shape validation, or requires
new measurement/export evidence before calibrated_linear_evidence. If future
thresholds are allowed, specify wavelength window, metrics, and evidence gates
without using already-inspected residuals to tune thresholds.
```
