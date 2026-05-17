# Phase 3C.2 - St Andrews Candidate Run Audit

## Decision

- Status: `candidate_run_audited_future_policy_prepared`
- Can feed serious core: `False`
- Existing run promotable: `False`
- Next clean run required: `True`
- Claim-status ceiling: `weak_within_dataset_holdout`

## Historical Residual Context

- Points: `1785.0`
- Mean absolute residual: `0.0847482217267253`
- RMSE: `0.17824688884709078`
- Max absolute residual: `0.6976243466052916`
- Dip wavelength offset: `-141.92999999999995` nm
- Shape correlation: `-0.11145385096355263`

These values are recorded as historical context only. They must not
be used to tune pass/fail cutoffs for this already-inspected run.

## Future Policy

- Policy status: `pending_pro_or_user_lock_before_clean_run`
- Applies to existing run: `false`
- Primary channel: `reflectance`
- Auxiliary channel: `transmittance`, diagnostic only

## Boundary

Phase 3C.2 may prepare a future policy, but the existing St Andrews run remains historical because residuals were inspected first.
