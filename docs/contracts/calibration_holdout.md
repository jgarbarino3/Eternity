# Calibration And Holdout Contract

Calibration and holdout splits are explicit records, not conventions.

A split must be created and hashed before fitting. Fitting code may receive only
calibration views. Holdout measurements and holdout y-values must not appear in
fit inputs or AI researcher-playground prompts before the model is frozen.

Validation must fail if any holdout measurement or index hash appears in
`fit_result.used_data`.

The TiN/TiON optical-constants snapshots are calibration-side inputs by default:
they may define or load a frozen material model, but they do not provide an
independent holdout by themselves. If no sample-matched R/T or raw
ellipsometry holdout is registered, the strongest permitted status is
`calibration_only_no_holdout`.

Thesis initial/12V reflectance pairs may be organized as an audit split, but
they are not automatically calibrated evidence. The split must record what is
forbidden for fitting, and downstream validation must still check geometry,
normalization, stack assumptions, residuals, and leakage.

Phase 3A may compare a frozen TiN/SiO2 multilayer prediction against
`thesis_d_10nm` initial reflectance. Without predeclared residual thresholds and
normalization approval, the strongest allowed status is
`weak_within_dataset_holdout`.

Phase 3A.1 records normalization and threshold policy separately from the run
that already produced residuals. A policy created after residual inspection may
audit that existing run, but it must not make that existing run calibrated
evidence. Promotion requires a source-backed normalization decision and
threshold policy recorded before the future run being judged.

Phase 3A.4 keeps the current normalization basis at `relative_intensity_only`.
The thesis `d_10nm` exports may remain holdout candidates for future planning,
but they cannot become calibrated holdout evidence unless absolute reflectance
normalization is source-backed before a new run and the thresholds are
predeclared before residual inspection.
