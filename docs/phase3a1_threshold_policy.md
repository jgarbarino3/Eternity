# Phase 3A.1 Threshold Policy

Date: 2026-05-16

## Decision

Current state: **blocked pending Pro/user approval**.

The residuals from `run_f35a15cef565fb15` have already been inspected. They may
be reported as historical context, but they must not be used to select a pass or
fail threshold for that same run.

## Required Before Future Promotion

A future threshold policy must be recorded before the future residual-gated run
and must include:

- source-backed normalization basis;
- wavelength window;
- residual metrics and numeric thresholds;
- approver and approval date;
- explicit statement that the policy applies only to future runs unless it was
  created before the run being judged.

## Current Historical Context

The current Phase 3A candidate over 400-900 nm produced:

- 501 comparison points;
- mean absolute residual about 0.280;
- RMSE about 0.281;
- max absolute residual about 0.305.

These values are intentionally not encoded as pass/fail thresholds.
