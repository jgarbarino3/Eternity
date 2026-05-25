# Phase 3E.5 - Saha No-Claim Stack-Assumption Sensitivity Fixture

## Decision

- Status: `phase3e5_saha_sensitivity_fixture_ready`
- Claim label: `non_promoting_sensitivity_fixture`
- Claim-status ceiling: `literature_reproduction_fixture`
- Calibrated linear evidence allowed: `false`
- Phase 4 candidate: `false`
- Validation residual modeling performed: `false`
- Diagnostic comparisons performed: `true`
- Recommended next phase: `Phase 3F - simulator-validation fallback on simpler public thin-film data`

This fixture asks how much the Saha Fig. 2b predicted reflectance moves under
explicitly non-source-backed silicon, interface, and backside assumptions.
It is not validation and it does not select a correct variant.

## Assumption Space

- Variants: `12`
- Stack: `air / 250 nm AZO / 130 nm TiN / assumed silicon substrate`
- Wavelength window: `[300.0, 2000.0]` nm
- Points: `171`

## Variant Spread

| Polarization | Mean Spread | Median Spread | Max Spread | Max-Spread Wavelength |
| --- | ---: | ---: | ---: | ---: |
| rp | 0.000126306 | 6.65226e-06 | 0.00151909 | 450.000 |
| rs | 0.000242065 | 5.97517e-06 | 0.00346454 | 420.000 |

## Source-Simulated Versus Measured Context

- `rp` source-simulated RMSE versus measured: `0.0202558`
- `rs` source-simulated RMSE versus measured: `0.0300222`

These source-simulated curves are author-curve context, not an independent holdout.

## Lowest Diagnostic RMSE Rows

| Variant | Pol | RMSE vs Measured | RMSE vs Source-Simulated |
| --- | --- | ---: | ---: |
| `si_synthetic_blue_absorbing_dispersion__sio2_2nm_between_tin_and_si__semi_infinite_substrate` | `rp` | 0.0200632 | 0.0099263 |
| `si_synthetic_blue_absorbing_dispersion__none__semi_infinite_substrate` | `rp` | 0.0200639 | 0.00991877 |
| `si_synthetic_blue_absorbing_dispersion__sio2_2nm_between_tin_and_si__incoherent_air_backside_upper_bound` | `rp` | 0.0200669 | 0.00993226 |
| `si_synthetic_blue_absorbing_dispersion__none__incoherent_air_backside_upper_bound` | `rp` | 0.0200676 | 0.00992488 |
| `si_weak_absorbing_fixed_n3p7_k0p02__sio2_2nm_between_tin_and_si__semi_infinite_substrate` | `rp` | 0.0200949 | 0.00997766 |
| `si_weak_absorbing_fixed_n3p7_k0p02__none__semi_infinite_substrate` | `rp` | 0.0200959 | 0.00997412 |

These rows are descriptive only. A lower diagnostic RMSE is not a validation pass.

## Warnings

- Every silicon/backside/interface variant is an external sensitivity assumption, not a recovered Saha author model.
- The source-simulated Fig. 2b curves are not an independent holdout; comparisons to them are author-curve context only.
- The incoherent backside variant is an upper-bound diagnostic that ignores substrate bulk absorption and must not be treated as a measurement model.
- Do not promote Saha or tune variants from these diagnostic metrics.

## Remembered Next Work

- Phase: `Phase 3F`
- Title: Simulator-Validation Fallback On Simpler Public Thin-Film Data
- Reason: Public ENZ packages are proving useful as fixtures but unlikely to supply a fully frozen calibrated-linear validation contract.
- Acceptance target: Find a boring public planar thin-film dataset with machine-readable n/k or epsilon, measured R/T or ellipsometry, geometry, stack, and substrate details sufficient to validate the TMM machinery without making an ENZ evidence claim.
