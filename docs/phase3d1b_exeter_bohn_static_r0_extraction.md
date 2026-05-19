# Phase 3D.1B - Exeter/Bohn No-Fit Static R0 Extraction

## Decision

- Status: `static_r0_extracted_split_locked_no_residuals`
- Can feed serious core: `False`
- Can promote calibrated evidence: `False`
- Phase 4 ready: `False`
- Claim-status ceiling: `weak_within_dataset_holdout`
- Recommended next phase: `Phase 3D.1C - Exeter/Bohn package-constant no-fit model reconstruction`

## Canonical Artifacts

- `fig1_epsilon`: `lab_data/raw/public_exeter_bohn_ito_2021/exeter_bohn_ito_fig1_epsilon.csv`
  - SHA-256: `cf0c0e365334fe5257ac313d56f3e17a679624bbef81572a057ae173436f1489`
  - Source member: `Figure1/DATA_ellipsometer_fit.txt`
- `fig2_tir_reference`: `lab_data/raw/public_exeter_bohn_ito_2021/exeter_bohn_fig2_tir_reference.csv`
  - SHA-256: `a68892c9c66ddb8bb19b66aa27a59e4babefe698921b985a8c51003f29aff894`
  - Source member: `Figure2/DATA/DATA_Figure2a,b,c_calibration_probe_TIR.csv`
- `fig2_static_r0`: `lab_data/raw/public_exeter_bohn_ito_2021/exeter_bohn_fig2_static_r0.csv`
  - SHA-256: `e9a5109b4878373559cf367b020358c14fe187371babc1a087afee860eefa67a`
  - Source member: `Figure2/DATA/DATA_Figure2a,b,c_experiment.csv`

## Calibration Summary

- Rows: `187`
- Wavelength range: `1046.10498`-`1684.096069` nm
- Re(epsilon) range: `-2.842321`-`0.949581`
- Im(epsilon) range: `0.307948`-`1.254444`
- ENZ crossings: `[1233.996861]` nm
- Passivity check: `pass`

## Holdout Summary

- TIR reference rows: `31`
- Static R0 rows: `806`
- Wavelength range: `1150.0`-`1450.0` nm
- Prism-angle range: `38.35222290717139`-`54.93588374048224` deg
- R0 reflectance fraction range: `0.0033301334422230875`-`0.5116302643901643`
- Prepump rows per point: `[11]`

## Split Lock

- Calibration is Figure 1 epsilon.
- Holdout is Figure 2 TIR-normalized static pre-pump `R0`.
- Figure 2 reflection rows are forbidden for fitting.
- No residuals were run in this phase.

## Forbidden After Residuals

- material parameter refit
- thickness tuning
- incident-index tuning
- angle-offset tuning
- vertical scaling
- wavelength shifting
- threshold loosening
- using Figure 3/4 to rescue Figure 2
