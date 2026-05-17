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

Phase 3A.7 recovered related CompleteEASE/Woollam source candidates, including
DoD SAFE zip-contained snapshots. These candidates may guide future source
triage or re-export, but they do not relax the holdout rules unless they prove
channel name, units, calibration state, angle, polarization, and sample identity
before a new residual-gated run.

Phase 3A.8 triage turns those candidates into a relative-only diagnostic lane.
That lane can inform planning and provenance, but it is not a calibrated
holdout split. A future calibrated run still requires source-backed absolute
normalization or a new measurement plus predeclared thresholds before residual
inspection.

Phase 3A.9 packets may reuse the already-inspected comparison table to describe
relative-only behavior. Because the run and residuals are historical, those
descriptors must remain non-promoting context and cannot become holdout gates
for that same run.

Phase 3A.10 may choose a bounded manual source follow-up, but recovered source
metadata must still prove normalization before any future residual-gated run.
If that proof is not found, Phase 3A remains relative-only and Phase 3B remains
blocked until raw sample-matched TiON R/T is registered.

Phase 3A.11 may package exact candidates and proof gates for manual review.
That packet is not measurement evidence. Any positive finding must become a
separate source-backed decision artifact before thresholds, holdout gates, or
claim promotion are reconsidered.
