# Phase 3A.1 Pro Checkpoint

Date: 2026-05-16

## Why This Checkpoint Exists

Phase 3A produced a measured-reflectance comparison, but the residuals have
already been inspected. Any threshold chosen now would be post hoc for that run.

The remaining decisions are scientific, not mechanical:

- whether thesis/exported `Intensity` columns are absolute reflectance;
- what source evidence is required for normalization;
- what wavelength window and residual metrics are defensible for a future
  predeclared run;
- what gates must pass before `calibrated_linear_evidence`.

## Paste-Ready Prompt

```text
Review Eternity Phase 3A.1 for TiN/SiO2 thesis reflectance validation. The
existing candidate run has already produced residuals, so thresholds must not be
reverse-engineered from that result. Decide whether thesis/exported Intensity
columns can be treated as absolute reflectance, what source evidence is required
for that decision, what wavelength window and residual metrics are defensible
for a future predeclared validation run, and what gate states must remain
blocked before calibrated_linear_evidence.
```
