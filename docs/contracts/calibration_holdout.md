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

Phase 3A.12 exhausted the bounded manual source follow-up. Its result keeps the
Phase 3A thesis spectra useful only as relative-intensity diagnostics unless a
new clean export, measurement, or source-backed absolute-reflectance record is
added later.

Phase 3C.2 may audit the St Andrews `RT.xlsx` reflectance holdout and draft a
future threshold policy. Because the current St Andrews residuals were already
inspected before threshold approval, that policy must set
`applies_to_existing_run: false`; calibrated promotion requires a later clean
run after the policy is locked.

Phase 3C.3 may lock thresholds for a later St Andrews clean run and may treat
the reflectance channel as an absolute fraction when the public paper/RT.xlsx
normalization evidence is recorded. Transmittance remains auxiliary. A clean
run that fails any locked metric is `failed_validation` for this lane, not a
reason to loosen thresholds after inspection.

Phase 3D.1A identifies Exeter/Bohn Figure 1 ellipsometry-derived epsilon and
Figure 2 TIR-normalized pre-pump reflection as a promising split candidate, but
not as calibrated evidence. Phase 3D.1B must canonically extract the Figure 1
calibration input and Figure 2 `R0` holdout, lock package constants/nuisance
values before residuals, and forbid any tuning of material, thickness, angle,
scaling, wavelength, or thresholds after inspecting the Figure 2 reflection
surface.

Phase 3D.1B completed that extraction and wrote
`docs/phase3d1b_exeter_bohn_split_lock.yaml`. Phase 3D.1C may only use the
locked artifacts and predeclared package constants/nuisance values for no-fit
model reconstruction. Figure 2 `R0` values remain forbidden for material,
thickness, incident-index, angle-offset, vertical-scale, wavelength-axis, or
threshold tuning. Any Phase 3D.1C residual report remains capped at
`weak_within_dataset_holdout` unless a later promotion review proves full
independence, uncertainty handling, and claim-status criteria.

Phase 3D.1C inspected residuals and therefore cannot become a calibrated
promotion run after the fact. Its output is a non-promoting reconstruction
diagnostic. Any future Exeter/Bohn promotion attempt would require a separate
predeclared gate that is not tuned to these inspected residuals; the immediate
next public-data step is not loosening the Exeter threshold story.

Phase 3D.2 snapshotted the Saha TiN/AZO Figshare source-data package and
confirmed the target Fig. 2b and Fig. 2c/d Origin worksheet labels, but it did
not extract table-ready numerical data. Embedded OPJU worksheet previews may be
used only as audit evidence for file contents. They must not be digitized into a
calibrated holdout unless a separate policy explicitly labels the result as
plot-derived and caps its claim status below `calibrated_linear_evidence`.

Phase 3D.2A tested the local OPJU export path and found it blocked: LabPlot
installed on macOS but did not expose a batch OPJU-to-CSV route, and offscreen
opening did not produce tables. Saha can be reopened only with a real table
export or open-format mirror.

Phase 3D.3 snapshotted the Exeter spatiotemporal ITO package for DOI
`10.24378/exe.3644`. The archive contains public table-ready ITO epsilon and
open measurement CSV/ASC files, but the inspected measurement lane is pumped
time-resolved transmission/frequency-shift data. It is capped at
`literature_reproduction_fixture` for now and must not be promoted to
`calibrated_linear_evidence` without a separate static linear holdout and a
predeclared gate.
