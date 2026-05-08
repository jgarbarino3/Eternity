# Run Artifact Contract

V1 runs must include the V0 artifacts plus:

- `input_manifest.json`
- `registry_snapshot.json`
- `registry_snapshot.sha256`
- `raw_artifacts.json`
- `data_splits.json`
- `material_model.json`
- `fit_plan.json`
- `fit_result.json`
- `fit_diagnostics.json`
- `prediction_table.csv`
- `comparison_table.csv`
- `holdout_residuals.csv`
- `validation_gates/*.json`
- `claim_status.json`
- `assumptions.json`
- `validity_envelope.json`
- `artifact_hashes.json`
- `environment.json`

The manifest must record artifact hashes, semantic artifact kinds, and whether
each artifact comes from calibration, holdout, or neither.
