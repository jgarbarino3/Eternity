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
