# Phase 3G.1 - Measured-Data Intake Queue And Assistant Brief

## Decision

- Status: `phase3g1_intake_queue_ready_no_candidate`
- Selected next lead: `none`
- Phase 3F.2 intake allowed: `false`
- Residual modeling allowed now: `false`
- Phase 4 candidate ready now: `false`
- Recommended next phase: `Phase 3G.2 - assistant intake ergonomics and research-memory record promotion`

Phase 3G.1 is an assistant-facing queue. It ranks leads and preserves
missing evidence, but it does not download files, fit parameters, inspect
measured residuals, or promote claim status.

## Prior Failure Memory

- Phase 3F.1F memory available: `true`
- Prior measured-data leads recorded: `37`
- Phase 3F.2 allowed by prior memory: `false`

## Searchable Failure Memory

- `research_memory/examples/failure_memory/phase3f_public_measured_data_scouts.yaml`
- `research_memory/examples/failure_memory/saha_stack_contract_block.yaml`
- `research_memory/examples/failure_memory/st_andrews_tin_fail_closed.yaml`
- `research_memory/examples/failure_memory/wang_wo3_reproduction_fixture.yaml`
- `research_memory/examples/failure_memory/tion_local_data_exhausted.yaml`

## Queue Summary

- Lead count: `5`
- Hard-gate pass count: `0`

## Lead Gate Table

| Lead | Label | Gate Pass? | Missing / Risk Flags | Next Action |
| --- | --- | --- | --- | --- |
| future_clean_teaching_stack_template | `reject` | no | public_access, source_qualified_constants_or_model, independent_measured_holdout, machine_readable_files, geometry_backed, ... | Replace placeholder fields with source-backed evidence before considering Phase 3F.2. |
| saha_tin_azo_2023_exported_tables | `weak_within_dataset_holdout` | no | substrate_backside_coherence_clear, leakage_safe_no_fit_split | Keep parked unless source-backed silicon/backside/coherence and leakage proof appears. |
| ultrathin_au_absorber_2020 | `weak_within_dataset_holdout` | no | leakage_safe_no_fit_split | Revisit only if an independent no-fit material split is found. |
| st_andrews_tin_2025_public_tin | `weak_within_dataset_holdout` | no | substrate_backside_coherence_clear, leakage_safe_no_fit_split | Do not continue toward Phase 4 without exact roughness/back-reflection or acquisition-parity evidence. |
| structural_color_froc_2023_code_parity | `reject` | no | independent_measured_holdout, leakage_safe_no_fit_split | Keep as code-regression coverage, not measured validation. |

## Assistant Workflows

- Primary CLI: `eternity phase3g1-intake-queue`
- Command `summarize_current_blockers`: `eternity phase3g1-summarize-blockers`
- Command `rank_next_public_data_leads`: `eternity phase3g1-rank-leads`
- Command `generate_pro_prompt`: `eternity phase3g1-pro-prompt`
- Command `make_no_overclaim_status_report`: `eternity phase3g1-no-overclaim-report`
- Command `compare_new_dataset_against_gate`: `eternity phase3g1-compare-lead --lead-card <lead.yaml>`
- summarize_current_blockers: No-overclaim status plus top missing hard gates.
- rank_next_public_data_leads: Sorted lead table by priority rank and missing hard-gate count.
- generate_pro_prompt: A compact 5.5 Pro prompt asking for source-backed missing evidence only.
- make_no_overclaim_status_report: Markdown report with claim ceiling, stop rules, and next action.
- compare_new_dataset_against_gate: Add a lead card to the queue YAML and rerun the same command.

## 5.5 Pro Prompt

```text
You are reviewing candidate public thin-film measured-data leads for Eternity.
Do not relax the evidence bar. Find only source-backed evidence for missing hard gates.
Current selected lead: none.
Required gates: public access; source-qualified constants/model; independent measured holdout; machine-readable files; geometry; stack/thickness; substrate/backside/coherence; leakage-safe no-fit split; planar linear TMM suitability; source/hash readiness.
Return a table with pass/unknown/fail for each gate, exact source files, and a conservative claim ceiling. Do not propose residual modeling unless every hard gate is source-backed before fitting.
```

## Stop Rules

- A queue lead is not validation evidence.
- Phase 3F.2 can open only after every hard gate is pass.
- Measured residual modeling remains forbidden in Phase 3G.1.
- No claim label may be promoted from code parity, constants-only data, or leakage-risk holdouts.
