# Claim Status Contract

Every Eternity run must emit `claim_status.json` and render the same status in
`report.md`.

Allowed statuses:

- `synthetic_software_fixture`
- `literature_reproduction_fixture`
- `calibration_only_no_holdout`
- `weak_within_dataset_holdout`
- `calibrated_linear_evidence`
- `failed_validation`

Only `calibrated_linear_evidence` may feed serious-core scientific conclusions.
All other statuses may be used for software testing, reproduction, planning, or
researcher-playground critique only.

TiN/TiON optical constants alone map to `calibration_only_no_holdout` when they
are local lab-derived tables and to `literature_reproduction_fixture` when the
goal is only reproducing a published table. Missing or ambiguous R/T provenance
must not be hidden inside a positive status; it belongs in a provenance-gap or
R/T audit artifact.

Thesis reflectance spectra may become holdout candidates only after sample,
stack, geometry, normalization, and split boundaries are explicit. Until then,
they are measured inputs and provenance anchors, not validated serious-core
conclusions.

Phase 3A TiN/SiO2 runs may use `weak_within_dataset_holdout` for a prepared
comparison against thesis d=10 nm initial reflectance. That status cannot feed
serious-core conclusions and must report blocked normalization/threshold gates
when they are unresolved.

Phase 3A.1 audits those blocked gates. It may report a future policy as ready,
but it cannot upgrade an already-inspected run unless the policy explicitly
applied before that run and all gate artifacts pass.

Phase 3A.4 records the fail-closed absolute-reflectance decision. Thesis text
and figures support measured reflectance provenance for `d_10nm` / `3L2`, but
exported `Intensity` columns remain `relative_intensity_only` until a
source-backed export, recipe, project file, lab note, or approved policy proves
absolute reflectance normalization before a future residual-gated run.

Phase 3A.7 source recovery may report `related_source_candidates_found` and
`stack_mapping_confirmed`, but these are provenance findings only. They do not
permit `calibrated_linear_evidence` while absolute normalization and
predeclared thresholds remain blocked.

Phase 3A.8 source triage may report `pivot_to_relative_only_diagnostic`.
Relative-only diagnostics may compare spectral shape, dip position, trend
direction, and figure provenance, but they must not feed serious-core evidence,
claim absolute reflectance, tune thresholds retroactively, or promote above
`weak_within_dataset_holdout`.

Phase 3A.9 diagnostic packets may report relative-shape metrics and trend/dip
descriptors for an already-inspected run. These metrics are descriptive only:
they are not pass/fail thresholds, they do not repair normalization, and they
must not upgrade the run's claim status.
