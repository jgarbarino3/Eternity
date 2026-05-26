# Phase 3F.1D - Targeted Benchmark Search And Fixture-Lane Decision

Date: 2026-05-26

## Decision

- Status: `phase3f1d_no_source_data_candidate_open_code_regression_fixture_lane`
- Selected Phase 3F.2 source-data candidate: `none`
- Hard-gate pass count: `0`
- Phase 3F.2 intake allowed: `false`
- TMM adapter started: `false`
- Residual modeling performed: `false`
- Phase 4 candidate: `false`
- Claim standard changed: `false`
- Recommended next phase: `Phase 3F.1E - non-promoting TMM code-regression fixture contract`

Phase 3F.1D did not find a public measured source-data candidate that can be
used as a frozen no-fit TMM validation target. The practical way forward is an
explicit non-promoting code-regression fixture lane, not a weakened evidence
bar.

## Fixture Lane Decision

- Selected fixture: `structural_color_froc_2023_code_parity_fixture`
- Scope: `non_promoting_code_regression_only`
- Secondary fixture: `ultrathin_gold_absorber_2020_measurement_parser_fixture`
- Independent Phase 3F.2 source-data candidate: `none`

Why Phase 3F.2 remains blocked:

- No candidate establishes all hard gates for public access, independent machine-readable constants, measured holdout, geometry, stack, substrate/backside/coherence, leakage-safe no-fit split, TMM suitability, and source-hash readiness.
- The strongest measured-data package remains leakage-blocked because optical constants/model pieces are fitted from the same measurement family.
- The strongest code package lacks measured spectral holdout and therefore can only test implementation parity.

Why `sbyrnes321/tmm` is not the oracle:

- Eternity already imports coh_tmm from sbyrnes321/tmm, so it is a dependency reference rather than an independent oracle.

Rules for Phase 3F.1E:

- No measured residuals, fitted parameters, or claim promotion in Phase 3F.1E.
- Pin source revision/hash before using external code as a fixture.
- Compare deterministic transfer-matrix outputs and conventions only.
- Report any match as machinery regression coverage, not experimental validation.

## Gate Table

| Candidate | Label | Gate Pass? | Main Missing Flags | Decision |
| --- | --- | --- | --- | --- |
| `transparent_electrode_umtf_2020` | `promising_but_blocked` | no | machine_readable_material_constants, substrate_backside_coherence_specified, leakage_safe_no_fit_split, source_hash_ready | `blocked_before_intake_by_unproven_split_and_backside_contract` |
| `pfpe_pvdf_mendeley_2021` | `simulator_validation_fallback` | no | stack_thickness_specified, substrate_backside_coherence_specified, leakage_safe_no_fit_split, source_hash_ready | `blocked_by_stack_backside_and_leakage_uncertainty` |
| `htem_db_thin_film_measurement_archive` | `measured_only_fixture` | no | machine_readable_material_constants, geometry_specified, stack_thickness_specified, substrate_backside_coherence_specified, ... | `database_discovery_surface_not_validation_candidate` |
| `precise_gaas_algaas_heterostructure_2023` | `calibration_only_no_holdout` | no | machine_readable_material_constants, machine_readable_measured_holdout, substrate_backside_coherence_specified, leakage_safe_no_fit_split, ... | `blocked_by_no_public_source_package_or_holdout_split` |
| `tmmax_software_benchmark_suite` | `software_or_simulation_fixture` | no | machine_readable_measured_holdout, source_hash_ready | `useful_as_software_fixture_not_measured_validation` |
| `sbyrnes_tmm_internal_dependency_reference` | `software_or_simulation_fixture` | no | machine_readable_measured_holdout, source_hash_ready | `rejected_as_independent_oracle_because_it_is_the_current_backend` |
| `structural_color_froc_2023_code_parity_fixture` | `software_or_simulation_fixture` | no | machine_readable_measured_holdout | `selected_for_non_promoting_phase3f1e_code_regression_fixture` |
| `ultrathin_gold_absorber_2020_measurement_parser_fixture` | `calibration_only_no_holdout` | no | machine_readable_material_constants, leakage_safe_no_fit_split | `useful_secondary_parser_fixture_but_not_no_fit_validation` |

## Source Refresh

Read-only source inspection and targeted search were used for the following
candidate surfaces. No new source package was ingested in this phase.

- https://www.nature.com/articles/s41467-020-17107-6
- https://data.mendeley.com/datasets/bwtzc9rzb9/2
- https://www.nrel.gov/research/software/htem-db-api-examples
- https://arxiv.org/abs/2301.07712
- https://github.com/bahremsd/tmmax
- https://github.com/sbyrnes321/tmm
- https://www.nature.com/articles/s41467-023-39602-2
- https://github.com/hincz-lab/structural_color_FROCs
- https://www.nature.com/articles/s41467-020-15762-3

## Stop Rule

Stop before measured residual modeling remains active. Any measured-data
residual at this point would require fitting, guessing, private/request-only
processing code, proprietary exports, or using one spectral family as both
calibration and holdout.

## Next Contract

Phase 3F.1E should build a small pinned fixture contract around the
`structural_color_FROCs` TMM code and material tables. The expected output is a
machine-checkable code-regression fixture proving that Eternity's wrapper and
conventions match an independent project implementation for selected simple
stacks. It is not experimental validation and must not alter claim labels.
