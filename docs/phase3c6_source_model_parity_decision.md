# Phase 3C.6A - Bounded St Andrews Source-Model Parity Implementation

## Decision

- Status: `parity_variants_failed_roughness_back_reflection_underdetermined`
- Can feed serious core: `False`
- Can promote calibrated evidence: `False`
- Phase 4 ready: `False`
- Continue to Phase 4: `False`
- Stop reason: Bounded source-derived variants still fail the locked thresholds, and roughness/back-reflection parity remains approximate rather than exact.
- Next phase: `Phase 3B.1 or Phase 3C.6B only with new source-model evidence`

## Source Length Inference

- Basis: `completeease_length_values_interpreted_as_angstrom_for_bounded_test`
- Confidence: `plausible_not_independently_verified`
- Film thickness used: `41.73650914589387` nm
- Roughness thickness used: `11.462616711097938` nm
- Reason: The raw fit limits around the thickness parameter are 200-1500, which is plausible as Angstrom for a nominal 50 nm film. This is sufficient for a bounded parity test, not exact source-model proof.

## Implemented Parity Pieces

- `cauchy_substrate`: `implemented_for_bounded_test`
- `source_thickness`: `implemented_with_angstrom_inference`
- `roughness`: `approximate_50_50_bruggeman_ema`
- `back_reflection`: `approximate_incoherent_backside_estimate`

## Resolution Status

- `cauchy_substrate`: `True`
- `source_thickness`: `True`
- `roughness`: `False`
- `back_reflection`: `False`

## Variant Results

| Variant | Metrics | Threshold status |
| --- | --- | --- |
| `clean_baseline_resimulated` | MAE `0.0847483`, RMSE `0.178247`, max residual `0.697624`, dip offset `-141.93` nm, shape corr `-0.111455` | `fail` |
| `source_cauchy_glass_nominal_thickness` | MAE `0.0845013`, RMSE `0.177976`, max residual `0.696487`, dip offset `-141.93` nm, shape corr `-0.103259` | `fail` |
| `source_cauchy_glass_source_thickness` | MAE `0.0984741`, RMSE `0.184667`, max residual `0.699227`, dip offset `-124.72` nm, shape corr `-0.075299` | `fail` |
| `source_cauchy_thickness_roughness_ema` | MAE `0.097356`, RMSE `0.186612`, max residual `0.709863`, dip offset `-141.93` nm, shape corr `-0.0909679` | `fail` |
| `source_cauchy_thickness_roughness_backside_estimate` | MAE `0.095636`, RMSE `0.18549`, max residual `0.707614`, dip offset `-141.93` nm, shape corr `-0.0932843` | `fail` |

## Boundary

Phase 3C.6A implements bounded source-derived parity diagnostics. It does not fit to RT.xlsx, change thresholds, select a replacement material model for promotion, feed the serious core, or make the St Andrews lane Phase 4-ready.
