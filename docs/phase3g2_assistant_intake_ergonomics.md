# Phase 3G.2 - Assistant Intake Ergonomics And Research-Memory Record Promotion

## Decision

- Status: `phase3g2_assistant_ergonomics_ready`
- Record drafts: `4`
- Phase 3F.2 intake allowed: `false`
- Residual modeling allowed now: `false`
- Phase 4 candidate ready now: `false`
- Recommended next phase: `Phase 3G.3 - new-lead intake dry run and queue maintenance`

Phase 3G.2 makes the assistant intake queue easier to use. It writes
compact status cards and review-gated research-memory draft records from
the Phase 3G.1 queue. It does not change any hard gate, open Phase 3F.2,
or authorize measured residual modeling.

## Promotion Policy

- Record drafts are validation evidence: `false`
- Default review state: `needs_human_review`
- Default evidence state: `literature_supported`

## Generated Draft Records

- `phase3g1_queue_saha_tin_azo_2023_exported_tables`: saha_tin_azo_2023_exported_tables is queued as weak_within_dataset_holdout; hard-gate pass is false. Warnings: queue_record_not_validation_evidence, no_measured_residual_modeling_from_queue_record.
- `phase3g1_queue_st_andrews_tin_2025_public_tin`: st_andrews_tin_2025_public_tin is queued as weak_within_dataset_holdout; hard-gate pass is false. Warnings: queue_record_not_validation_evidence, no_measured_residual_modeling_from_queue_record.
- `phase3g1_queue_structural_color_froc_2023_code_parity`: structural_color_froc_2023_code_parity is queued as reject; hard-gate pass is false. Warnings: queue_record_not_validation_evidence, no_measured_residual_modeling_from_queue_record.
- `phase3g1_queue_ultrathin_au_absorber_2020`: ultrathin_au_absorber_2020 is queued as weak_within_dataset_holdout; hard-gate pass is false. Warnings: queue_record_not_validation_evidence, no_measured_residual_modeling_from_queue_record.

## Status Cards

# Phase 3G.2 Status Cards

## Queue

- Status: `phase3g2_assistant_ergonomics_ready`
- Phase 3F.2 intake allowed: `false`
- Residual modeling allowed now: `false`
- Hard-gate passes: `0` / `5`
- Next phase: `Phase 3G.3 - new-lead intake dry run and queue maintenance`

## Lead Cards

### future_clean_teaching_stack_template

- Label: `reject`
- Gate pass: `false`
- Missing count: `10`
- Top missing flags: public_access, source_qualified_constants_or_model, independent_measured_holdout, machine_readable_files, +6_more
- Claim ceiling: `reject`
- Next action: Replace placeholder fields with source-backed evidence before considering Phase 3F.2.

### saha_tin_azo_2023_exported_tables

- Label: `weak_within_dataset_holdout`
- Gate pass: `false`
- Missing count: `2`
- Top missing flags: substrate_backside_coherence_clear, leakage_safe_no_fit_split
- Claim ceiling: `weak_within_dataset_holdout`
- Next action: Keep parked unless source-backed silicon/backside/coherence and leakage proof appears.

### ultrathin_au_absorber_2020

- Label: `weak_within_dataset_holdout`
- Gate pass: `false`
- Missing count: `1`
- Top missing flags: leakage_safe_no_fit_split
- Claim ceiling: `weak_within_dataset_holdout`
- Next action: Revisit only if an independent no-fit material split is found.

### st_andrews_tin_2025_public_tin

- Label: `weak_within_dataset_holdout`
- Gate pass: `false`
- Missing count: `2`
- Top missing flags: substrate_backside_coherence_clear, leakage_safe_no_fit_split
- Claim ceiling: `weak_within_dataset_holdout`
- Next action: Do not continue toward Phase 4 without exact roughness/back-reflection or acquisition-parity evidence.

### structural_color_froc_2023_code_parity

- Label: `reject`
- Gate pass: `false`
- Missing count: `2`
- Top missing flags: independent_measured_holdout, leakage_safe_no_fit_split
- Claim ceiling: `reject`
- Next action: Keep as code-regression coverage, not measured validation.

## Warnings

- `queue_record_not_validation_evidence`
- `no_measured_residual_modeling_from_queue_record`
