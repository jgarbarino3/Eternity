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
