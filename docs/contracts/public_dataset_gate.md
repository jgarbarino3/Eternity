# Public Dataset Gate Contract

Phase 3E.1 adds a conservative gate for public/literature datasets before any
future Phase 4 calibrated-linear attempt.

The gate is intentionally stricter than "this paper looks useful." It asks
whether a candidate has public, machine-readable, source-qualified calibration
data and an independent measured optical holdout that can be modeled by the
linear planar thin-film solver without hidden fitting leakage.

## Required Phase 4 Flags

A candidate may enter Phase 4 only when every flag is true:

- `data_are_public`
- `no_author_contact_required`
- `identified_sample_stack`
- `source_qualified_material_model`
- `independent_measured_holdout`
- `machine_readable_numerical_data`
- `absolute_calibration_documented`
- `geometry_specified`
- `calibration_holdout_split_predeclared`
- `holdout_not_known_used_for_fit`
- `tmm_appropriate`
- `no_existing_nonpromoting_validation`

Failing any flag blocks Phase 4. The candidate may still be useful as a
calibration-only fixture, literature-reproduction fixture, failed-validation
memory, or public-data search lead.

## Registry

The current registry lives at:

```text
docs/phase3e1_dataset_candidate_registry.yaml
```

Each candidate card records:

- candidate id, title, material family, and source type;
- DOI/source refs and public links;
- exact files to inspect first when known;
- evidence flags;
- proposed claim label;
- decision, blockers, notes, and next file.

## CLI

Run:

```bash
PYTHONPATH=src uv run python -m eternity.cli phase3e1-scaffold --output-dir docs
```

Expected outputs:

```text
docs/phase3e1_public_dataset_gate_assistant_scaffold.json
docs/phase3e1_public_dataset_gate_assistant_scaffold.md
docs/phase3e1_claim_status_summary.json
```

## Assistant Boundary

The executive research assistant may use this gate to create candidate cards,
rejection cards, search plans, project briefs, and next-action reports. It may
not promote scientific claims, lower evidence standards, or treat Browse.sh /
Plasmate text extraction as validation evidence by itself.
