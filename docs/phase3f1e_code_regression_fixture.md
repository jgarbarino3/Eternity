# Phase 3F.1E - Non-Promoting TMM Code-Regression Fixture Contract

Date: 2026-05-26

## Decision

- Status: `phase3f1e_code_regression_fixture_ready`
- Case count: `3`
- Pass count: `3`
- All cases passed: `true`
- Max reflection absolute delta: `1.6653345369377348e-16`
- Max transmission absolute delta: `1.3877787807814457e-16`
- Phase 3F.2 intake allowed: `false`
- Residual modeling allowed: `false`
- Recommended next phase: `Phase 3F.1F - decide whether code-regression coverage is enough for now or continue public measured-data scouting`

This is a non-promoting code-regression fixture. It compares deterministic
transfer-matrix convention outputs only. It does not compare to measured
spectra, fit parameters, validate a public dataset, or change any claim
label.

## Pinned Source

- Source root: `lab_data/raw/phase3f1c_structural_color_froc_2023/structural_color_FROCs_7c0998d/structural_color_FROCs-7c0998d720c387f1efbffe6d1417593ba2f845b1`
- GitHub revision: `7c0998d720c387f1efbffe6d1417593ba2f845b1`
- Archive SHA-256: `9d595ac110fc203b500780c97393a070c876fc81c5b75e7c20f0e1abf7949d92`
- Archive hash matches expected: `true`
- `TMM_numba.py` SHA-256: `881948db767e986cd3ffb38914d561a1d96ee06d3e9d07c6df57f83f63326aef`

## Claim Boundary

- Label: `non_promoting_code_regression_fixture`
- Experimental validation: `false`
- Measured residual modeling performed: `false`
- Phase 4 candidate: `false`

## Parity Table

| Case | Polarization | Wavelength (nm) | R Delta | T Delta | Pass? |
| --- | --- | ---: | ---: | ---: | --- |
| `lossless_te_single_layer` | `s` | 550.000 | 6.939e-18 | 0.000e+00 | yes |
| `lossy_tm_double_layer_angle` | `p` | 650.000 | 9.714e-17 | 1.110e-16 | yes |
| `source_table_ge_sio2_tio2_tm` | `p` | 550.000 | 1.665e-16 | 1.388e-16 | yes |

## Method Note

TMM_numba.py is loaded with numba.jit stubbed as an identity decorator so the public source formula runs without local NumPy/Numba binary compatibility requirements.
