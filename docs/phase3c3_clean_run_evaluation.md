# Phase 3C.3 - St Andrews Clean Run Evaluation

## Decision

- Status: `clean_run_failed_thresholds`
- Can feed serious core: `False`
- Claim-status decision: `failed_validation`
- Clean run ready for Phase 4 review: `False`

## Metrics

- Points: `1785`
- Wavelength window: `400.13`-`999.82` nm
- Dip offset: `-141.92999999999995` nm
- Shape correlation: `-0.11145385096355263`

| Metric | Value | Comparator | Threshold | Status |
| --- | --- | --- | --- | --- |
| `mean_absolute_error` | `0.084748221728215` | `less_equal` | `0.04` | `fail` |
| `root_mean_square_error` | `0.17824688885208068` | `less_equal` | `0.06` | `fail` |
| `max_absolute_residual` | `0.697624347` | `less_equal` | `0.15` | `fail` |
| `dip_wavelength_offset_nm` | `-141.92999999999995` | `abs_less_equal` | `40.0` | `fail` |
| `shape_correlation_minmax` | `-0.11145385096355263` | `greater_equal` | `0.9` | `fail` |

## Boundary

Phase 3C.3 may decide whether a clean run is ready for Phase 4 review, but it cannot feed the serious core or promote to calibrated_linear_evidence.
