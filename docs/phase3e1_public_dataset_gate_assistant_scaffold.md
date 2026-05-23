# Phase 3E.1 - Public Dataset Gate And Executive Research Assistant Scaffold

## Decision

- Status: `phase3e1_scaffold_ready_no_phase4_candidate`
- Can open Phase 4 now: `false`
- Can feed Serious Core now: `false`
- Claim standard changed: `false`
- Recommended next phase: `Phase 3E.4 - renewed ENZ public-data search through stack-contract gate`

## Candidate Gate Summary

- Candidates evaluated: `15`
- Phase 4 candidates: `0`

| Candidate | Label | Phase 4? | Main Blockers |
| --- | --- | --- | --- |
| exeter_bohn_ito_2021 | `weak_within_dataset_holdout` | no | no_existing_nonpromoting_validation |
| saha_tin_azo_2023 | `weak_within_dataset_holdout` | no | absolute_calibration_documented, calibration_holdout_split_predeclared, holdout_not_known_used_for_fit |
| acs_intracavity_ito_2025 | `literature_reproduction_fixture` | no | independent_measured_holdout, absolute_calibration_documented, calibration_holdout_split_predeclared, holdout_not_known_used_for_fit, ... |
| linkoping_ito_pedot_2026 | `literature_reproduction_fixture` | no | source_qualified_material_model, independent_measured_holdout, absolute_calibration_documented, calibration_holdout_split_predeclared, ... |
| ito_glass_sio2_optical_properties_2025 | `calibration_only_no_holdout` | no | independent_measured_holdout, absolute_calibration_documented, geometry_specified, calibration_holdout_split_predeclared, ... |
| spacetime_synthetic_motion_ito_2025 | `literature_reproduction_fixture` | no | source_qualified_material_model, independent_measured_holdout, absolute_calibration_documented, calibration_holdout_split_predeclared, ... |
| natural_enz_compendium_2025 | `calibration_only_no_holdout` | no | identified_sample_stack, independent_measured_holdout, absolute_calibration_documented, geometry_specified, ... |
| acs_lbsno_ferrell_berreman_2026 | `blocked_source_data_lead` | no | identified_sample_stack, source_qualified_material_model, independent_measured_holdout, machine_readable_numerical_data, ... |
| enz_metal_oxide_reflectors_2024 | `blocked_source_data_lead` | no | identified_sample_stack, source_qualified_material_model, independent_measured_holdout, machine_readable_numerical_data, ... |
| exeter_spatiotemporal_ito_2021 | `literature_reproduction_fixture` | no | independent_measured_holdout, absolute_calibration_documented, calibration_holdout_split_predeclared, holdout_not_known_used_for_fit, ... |
| thermo_optic_ito_2024 | `calibration_only_no_holdout` | no | independent_measured_holdout, absolute_calibration_documented, calibration_holdout_split_predeclared, holdout_not_known_used_for_fit, ... |
| wang_wo3_fp_2020_non_enz_baseline | `literature_reproduction_fixture` | no | independent_measured_holdout, absolute_calibration_documented, calibration_holdout_split_predeclared, holdout_not_known_used_for_fit, ... |
| cdo_dielectric_function_2020 | `calibration_only_no_holdout` | no | independent_measured_holdout, absolute_calibration_documented, calibration_holdout_split_predeclared, holdout_not_known_used_for_fit |
| al_doped_zno_ald_energies_2021 | `weak_within_dataset_holdout` | no | machine_readable_numerical_data, absolute_calibration_documented, calibration_holdout_split_predeclared, holdout_not_known_used_for_fit |
| request_only_tin_microbolometer | `rejected_candidate` | no | data_are_public, no_author_contact_required, machine_readable_numerical_data |

## Assistant Contract

Allowed outputs:

- candidate cards and rejection cards
- dataset-gate reports and claim-label summaries
- phase-state briefs and next-action recommendations
- literature-search prompts and Browse/Plasmate scouting plans
- failed-validation memory summaries

Forbidden outputs:

- promoting a candidate without all gate flags passing
- treating Browse/Plasmate text extraction as validation evidence
- lowering calibrated_linear_evidence standards to proceed
- recommending unavailable CompleteEASE, TiON raw R/T, or author-contact paths
- opening Phase 4 from plot-only, PDF-only, constants-only, or request-only data

## Interpretation

Phase 3E.1 turns the blocked Phase 3D public-data search into durable machinery. The assistant may now organize candidates and search results aggressively, but the gate still refuses Phase 4 unless every required public-data flag passes.
