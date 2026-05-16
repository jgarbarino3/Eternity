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

Real-data grounding runs that load tabulated optical constants should also
emit:

- `source_provenance.json`
- `sample_stack.json`
- `rt_provenance_audit.json`
- `provenance_gaps.json`

When no independent holdout is registered, `comparison_table.csv` and
`holdout_residuals.csv` may be emitted as empty prepared tables, and
`claim_status.json` must remain `calibration_only_no_holdout`.

Phase 3A validation-candidate runs should additionally emit
`validation_summary.json` and gate files for stack mapping, no-fit leakage,
threshold predeclaration, normalization, and claim-status ceiling. Blocked
threshold or normalization gates must prevent `calibrated_linear_evidence`.

Phase 3A.1 audit artifacts, when written, must include a JSON payload and a
Markdown summary. They must distinguish existing-run promotion from future-run
policy readiness and must keep historical residuals out of threshold selection.
