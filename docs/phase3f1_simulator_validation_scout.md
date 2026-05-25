# Phase 3F.1 - Simple Thin-Film Simulator-Validation Scout

## Decision

- Status: `phase3f1_no_candidate_ready_keep_phase3f_open`
- Selected next candidate: `none`
- Phase 3F.2 intake allowed: `false`
- Residual modeling performed: `false`
- Phase 4 candidate: `false`
- Recommended next phase: `Phase 3F.1 - continue bounded scout with stricter simple-stack leads`

This scout is contract-first and does not download source files, build a TMM
adapter, choose model variants, or inspect residuals.

## Search Summary

- Candidate count: `10`
- Hard-gate pass count: `0`
- Candidate limit: `10`

## Candidate Gate Table

| Candidate | Label | Gate Pass? | Main Missing Flags |
| --- | --- | --- | --- |
| filmoptics_inverse_solutions_2022 | `promising_but_blocked` | no | machine_readable_material_constants, substrate_backside_coherence_specified, leakage_safe_no_fit_split, source_hash_ready |
| self_consistent_sio2_ta2o5_2016 | `promising_but_blocked` | no | machine_readable_material_constants, machine_readable_measured_holdout, leakage_safe_no_fit_split, source_hash_ready |
| self_consistent_peald_al2o3_2025 | `promising_but_blocked` | no | machine_readable_material_constants, machine_readable_measured_holdout, leakage_safe_no_fit_split, source_hash_ready |
| refractiveindex_info_dataset_2024 | `constants_only_fixture` | no | machine_readable_measured_holdout, geometry_specified, stack_thickness_specified, substrate_backside_coherence_specified, ... |
| ekhi_radiative_properties_2026 | `measured_only_fixture` | no | machine_readable_material_constants, geometry_specified, stack_thickness_specified, substrate_backside_coherence_specified, ... |
| fused_quartz_transmission_ellipsometry_2026 | `bulk_substrate_sanity_fixture` | no | stack_thickness_specified, substrate_backside_coherence_specified, leakage_safe_no_fit_split, tmm_suitable |
| ksemaw_sample_workdirs_2023 | `software_or_simulation_fixture` | no | machine_readable_material_constants, machine_readable_measured_holdout, geometry_specified, stack_thickness_specified, ... |
| tmmax_material_database_2026 | `software_or_simulation_fixture` | no | machine_readable_measured_holdout, geometry_specified, stack_thickness_specified, substrate_backside_coherence_specified, ... |
| solpoc_multilayer_stack_2026 | `software_or_simulation_fixture` | no | machine_readable_material_constants, machine_readable_measured_holdout, geometry_specified, stack_thickness_specified, ... |
| multilayer_app_validation_examples_2026 | `software_or_simulation_fixture` | no | machine_readable_measured_holdout, substrate_backside_coherence_specified, leakage_safe_no_fit_split, tmm_suitable, ... |

## Stop Rule

- Residual stop active: `true`
- Reason: Phase 3F.1 is scouting/gating only; residuals require a later Phase 3F.2 source-file intake and frozen no-fit adapter.
