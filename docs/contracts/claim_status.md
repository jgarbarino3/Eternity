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
