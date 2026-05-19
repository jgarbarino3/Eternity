# Phase 3D.1A - Exeter/Bohn Calibration-Holdout Split Audit

Date: 2026-05-19

## Decision

- Status: `split_audit_promising_no_fit_reconstruction_needed`
- Can feed serious core: `false`
- Can promote calibrated evidence: `false`
- Phase 4 ready: `false`
- Best candidate lane: `Figure2_static_prepump_reflection`
- Current claim ceiling: `weak_within_dataset_holdout`
- Recommended next phase: `Phase 3D.1B - Exeter/Bohn no-fit static R0 extraction and split lock`

## Audit Scope

This audit inspected the downloaded Exeter/Bohn ITO ENZ package:

- `lab_data/raw/public_exeter_bohn_ito_2021/OpenData.zip`
- Paper DOI: `10.1038/s41467-021-21332-y`
- Dataset DOI: `10.24378/exe.3004`

The goal was to decide whether the package has a usable calibration/holdout
split for a first calibrated-linear validation attempt, not to run residuals.

## Calibration-Side Evidence

The strongest calibration input is:

- `Figure1/DATA_ellipsometer_fit.txt`

The table contains 187 wavelength rows over `1046.10498`-`1684.096069` nm with
columns:

- `nm`
- `e1 Gen-Osc`
- `e2 Gen-Osc`
- `e1 Ref.`
- `e2 Ref.`

The Gen-Osc epsilon column has an interpolated zero crossing near
`1233.996861` nm. This is source-qualified optical-constant data from the
paper package and is the best candidate frozen material input.

The Figure 1 notebook reads this file as `wav`, `er_1`, `ei_1`, `crap_1`, and
`crap_2`, then fits a Drude model to `er_1 + 1j*ei_1`.

The Figure 2/3/4 notebooks use hard-coded Drude parameters:

- `eps_inf = 3.42725287`
- `wp0 = 2.8561e+15`
- `gamma0 = 2.2379e+14`
- `t_ITO = 60`
- `dth = 3.4*degree`
- `n = 1.43`

These constants may be source-code provenance, but they are not yet a locked
Eternity split. Phase 3D.1B must freeze exactly one calibration input before
checking any residuals: either the tabulated epsilon or the package Drude
parameters.

## Holdout-Side Evidence

The cleanest holdout candidate is Figure 2 static/pre-pump reflection:

- `Figure2/DATA/DATA_Figure2a,b,c_calibration_probe_TIR.csv`
- `Figure2/DATA/DATA_Figure2a,b,c_experiment.csv`

The Figure 2 notebook labels the calibration block as `Probe (TIR reflection)`
and plots the reference as `TIR Reference = 100% Reflection`.

The reconstruction formula in the notebook is:

```text
TIR reference = mean(power_s) / mean(power_r_probe)
power_norm = power_s / power_r_probe / f_1D_spline(wavelength_2)
R0 = mean(power_norm for delay <= -0.4 ps)
```

The Figure 2 experiment file has 65,286 rows, all with
`wavelength_1 == wavelength_2`, covering:

- raw `theta`: `35`-`60` degrees, 26 unique values
- `wavelength_1`/`wavelength_2`: `1150`-`1450` nm, 31 unique values
- `delay`: `-0.6` to `1.0` ps, 81 unique values
- `intensity`: `70`
- pre-pump rows with `delay <= -0.4`: `8866`

This is a real table path to a static reflection surface, not only a plotted
curve. It is therefore worth implementing a no-fit extraction in the next
phase.

## Lower-Priority Lanes

Figure 3 and Figure 4 use the same TIR-reference style, but they are less clean
for the first validation split:

- Figure 3 has a fixed `wavelength_1 = 1250` nm and no diagonal
  `wavelength_1 == wavelength_2` rows.
- Figure 4 has diagonal rows, but only 150 diagonal pre-pump rows per
  experiment table.
- Figure 3/4 notebooks include signal-offset handling in the experiment import
  path, so they should not be the first serious holdout unless Figure 2 fails.

Use Figure 3/4 later as auxiliary consistency checks, not as the Phase 3D.1B
primary split.

## Leakage Risks

The package is promising but not yet clean enough for calibrated evidence.

Known leakage/nuisance risks:

- The Figure 2 notebook already compares `Experiment` and `Static model`, so
  its visual agreement was part of the paper workflow.
- The notebook uses hard-coded `dth = 3.4*degree`, `n = 1.43`, and
  `t_ITO = 60`. These must not be re-fit or adjusted after residual inspection.
- The notebook model contains a small complex-index workaround comment in the
  Fresnel path: `not sure why the -1j*0.0001 is required, but it is necessary
  HERE`. That needs to be treated as package-reproduction code until reviewed.
- The static holdout is reconstructed from pre-pump rows inside a nonlinear
  pump-probe experiment, not from a separate standalone linear R/T file.
- Any vertical scaling, wavelength shifting, thickness tuning, angle-offset
  tuning, or Drude refitting against the Figure 2 reflection surface would
  invalidate a calibrated-linear claim.

## Allowed Next

Phase 3D.1B may:

- Extract `Figure1/DATA_ellipsometer_fit.txt` into a frozen material input.
- Extract Figure 2 TIR reference and pre-pump `R0` into canonical CSV/JSON
  artifacts.
- Create a `calibration_holdout_split` that forbids Figure 2 reflection rows
  from fitting.
- Reproduce the package's static model only with frozen package constants and
  no residual-driven tuning.
- Emit a residual report with a conservative claim label.

## Forbidden Next

Phase 3D.1B must not:

- Promote this dataset to `calibrated_linear_evidence` from this audit alone.
- Tune `eps_inf`, `wp0`, `gamma0`, `t_ITO`, `dth`, `n`, vertical scaling,
  wavelength shifts, or thresholds after seeing Figure 2 residuals.
- Use Figure 3/4 offsets or dynamic rows to rescue a failed Figure 2 static
  comparison.
- Proceed to Phase 4 without a locked split, reconstructed holdout table,
  no-fit model run, threshold policy, residual report, and claim-status review.

## Bottom Line

The Exeter/Bohn package is not a dud. It is the first public package in this
lane with enough table-level data to justify implementation. The honest next
move is a no-fit extraction and split lock, not more broad search and not a
promotion claim.
