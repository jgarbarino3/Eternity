# Calibration And Holdout Contract

Calibration and holdout splits are explicit records, not conventions.

A split must be created and hashed before fitting. Fitting code may receive only
calibration views. Holdout measurements and holdout y-values must not appear in
fit inputs or AI researcher-playground prompts before the model is frozen.

Validation must fail if any holdout measurement or index hash appears in
`fit_result.used_data`.
