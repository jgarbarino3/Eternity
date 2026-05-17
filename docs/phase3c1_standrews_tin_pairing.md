# Phase 3C.1 - St Andrews TiN Pairing

Date: 2026-05-17

## Decision

- Pairing status: `candidate_supported_reflectance_only`
- Selected sample: `public_standrews_tin_50nm_50c`
- Selected epsilon member: `TiN-data_Pure/Ellipsometry/50nm-MTiN-50c.txt`
- Holdout member: `TiN-data_Pure/RT.xlsx`
- Claim ceiling: `weak_within_dataset_holdout`
- Can feed serious core: `false`

## Evidence

- The paper identifies Figure 4 as 50 nm TiN on glass at normal incidence.
- The paper describes a reflectance minimum of about 20% near 540 nm.
- The extracted `RT.xlsx` reflectance minimum in 400-1000 nm is `0.20377` at `542.06 nm`.
- The selected 50 C epsilon table has ENZ crossings `[664.334]` and passivity `pass`.

## Caveats

- `RT.xlsx` does not independently label the annealing condition. Transmittance remains auxiliary: its 400-1000 nm range is `0.02035` to `0.71769` and requires scaling/noise review before it becomes a clean absolute channel.
- Thresholds are not predeclared, so calibrated promotion is blocked.

## Generated Raw-Member Snapshots

- `lab_data/raw/public_st_andrews_tin_2025/standrews_tin_50nm_reflectance.csv`
- `lab_data/raw/public_st_andrews_tin_2025/standrews_tin_50nm_transmittance.csv`
- `lab_data/raw/public_st_andrews_tin_2025/standrews_tin_50nm_50c_epsilon.txt`
