# Phase 3G.1 No-Overclaim Status

- Status: `phase3g1_intake_queue_ready_no_candidate`
- Phase 3F.2 intake allowed: `false`
- Residual modeling allowed now: `false`
- Phase 4 candidate ready now: `false`
- Queue lead count: `5`
- Hard-gate pass count: `0`

## Top Blockers

- `leakage_safe_no_fit_split`: 5 lead(s). material model and measured holdout can be separated without residual-driven tuning
- `substrate_backside_coherence_clear`: 3 lead(s). source-backed substrate/backside/coherence treatment or irrelevant backside
- `independent_measured_holdout`: 2 lead(s). independent measured R/T, A, or ellipsometry holdout
- `geometry_backed`: 1 lead(s). source-backed wavelength axis, angle, polarization, side, and units
- `machine_readable_files`: 1 lead(s). machine-readable files for constants and measured data
- `planar_linear_tmm_suitable`: 1 lead(s). measurement is appropriate for planar linear TMM
- `public_access`: 1 lead(s). public data access without private credentials or author contact
- `source_hash_ready`: 1 lead(s). source files can be hashed or have checksums before intake
- `source_qualified_constants_or_model`: 1 lead(s). source-qualified n,k, epsilon, or model constants
- `stack_thickness_backed`: 1 lead(s). source-backed stack order, material identity, and thicknesses

## Stop Rules

- A queue lead is not validation evidence.
- Phase 3F.2 can open only after every hard gate is pass.
- Measured residual modeling remains forbidden in Phase 3G.1.
- No claim label may be promoted from code parity, constants-only data, or leakage-risk holdouts.
