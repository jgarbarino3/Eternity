# Phase 3F.1B - 5.5 Pro Lead Gate

## Decision

- Status: `phase3f1_no_candidate_ready_keep_phase3f_open`
- Selected next candidate: `none`
- Phase 3F.2 intake allowed: `false`
- Residual modeling performed: `false`
- Phase 4 candidate: `false`
- Recommended next phase: `Phase 3F.1C - continue strict simple-stack source search or intake a newly supplied clean lead`

This scout is contract-first and does not download source files, build a TMM
adapter, choose model variants, or inspect residuals.

## Search Summary

- Candidate count: `16`
- Hard-gate pass count: `0`
- Candidate limit: `16`

## Candidate Gate Table

| Candidate | Label | Gate Pass? | Main Missing Flags |
| --- | --- | --- | --- |
| tin_mkid_optical_stack_2022 | `weak_within_dataset_holdout` | no | machine_readable_material_constants, stack_thickness_specified, leakage_safe_no_fit_split, source_hash_ready |
| fano_ultrathin_coatings_froc_2021 | `simulator_validation_fallback` | no | machine_readable_material_constants, geometry_specified, stack_thickness_specified, leakage_safe_no_fit_split |
| structural_color_froc_2023 | `simulator_validation_fallback` | no | machine_readable_material_constants, leakage_safe_no_fit_split |
| ultrathin_gold_absorber_2020 | `simulator_validation_fallback` | no | machine_readable_material_constants, substrate_backside_coherence_specified, leakage_safe_no_fit_split |
| sb2s3_tamm_cavity_2023 | `simulator_validation_fallback` | no | machine_readable_material_constants, leakage_safe_no_fit_split |
| transparent_electrode_umtf_2020 | `simulator_validation_fallback` | no | machine_readable_measured_holdout, substrate_backside_coherence_specified, leakage_safe_no_fit_split |
| pfpe_pvdf_thin_films_2021 | `simulator_validation_fallback` | no | machine_readable_material_constants, machine_readable_measured_holdout, substrate_backside_coherence_specified, leakage_safe_no_fit_split |
| filmoptics_inverse_solutions_2022_pro | `calibration_only_no_holdout` | no | machine_readable_measured_holdout, substrate_backside_coherence_specified, leakage_safe_no_fit_split |
| azo_infrared_emissivity_regulator_2023 | `literature_reproduction_fixture` | no | machine_readable_material_constants, substrate_backside_coherence_specified, leakage_safe_no_fit_split, tmm_suitable |
| shg_time_varying_interface_2024 | `literature_reproduction_fixture` | no | machine_readable_material_constants, machine_readable_measured_holdout, geometry_specified, stack_thickness_specified, ... |
| enz_time_gate_scattering_media_2026 | `literature_reproduction_fixture` | no | machine_readable_material_constants, machine_readable_measured_holdout, geometry_specified, stack_thickness_specified, ... |
| double_slit_time_diffraction_2023 | `literature_reproduction_fixture` | no | machine_readable_material_constants, machine_readable_measured_holdout, geometry_specified, stack_thickness_specified, ... |
| time_refraction_enz_2020 | `rejected_request_only` | no | public_access, machine_readable_material_constants, machine_readable_measured_holdout, geometry_specified, ... |
| saturable_time_varying_mirror_2022 | `rejected_request_only` | no | public_access, machine_readable_material_constants, machine_readable_measured_holdout, geometry_specified, ... |
| ito_ring_resonator_enz_2023 | `blocked_source_data_lead` | no | machine_readable_material_constants, machine_readable_measured_holdout, geometry_specified, stack_thickness_specified, ... |
| annealing_free_ito_2023 | `blocked_source_data_lead` | no | machine_readable_material_constants, machine_readable_measured_holdout, stack_thickness_specified, substrate_backside_coherence_specified, ... |

## Stop Rule

- Residual stop active: `true`
- Reason: Phase 3F.1B is scouting/gating only; residuals require a later Phase 3F.2 source-file intake and frozen no-fit adapter.
