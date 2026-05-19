# Phase 3E.2B - Wang Fig. 2f Semantics Audit

## Decision

- Status: `source_backed_offsets_inferred_columns_not_source_labeled`
- Full no-fit TMM validation allowed: `False`
- Bounded de-offset reproduction fixture allowed: `True`
- Claim-status ceiling: `literature_reproduction_fixture`
- Recommended next phase: `Phase 3E.2C - Wang bounded de-offseted reproduction fixture`

The source paper backs the measured/simulated figure semantics and the SI backs the model inputs, but Fig2f-R.xlsx has no chart XML, no series labels, and no workbook-level measured/simulated headers. A de-offseted reproduction fixture is honest; a clean no-fit validation residual is not.

## Source Evidence

- Article URL: https://www.nature.com/articles/s41467-019-14194-y
- Supplementary PDF URL: https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-019-14194-y/MediaObjects/41467_2019_14194_MOESM1_ESM.pdf
- Figshare URL: https://figshare.com/articles/dataset/Towards_Full-colour_Tunability_of_Inorganic_Electrochromic_Devices_Using_Ultracompact_Fabry-Perot_Nanocavities/11154791

The article backs Fig. 2f as measured solid traces and simulated dashed traces. The supplementary information backs ellipsometry-derived W/WO3 constants, normal-incidence characteristic-matrix calculations, and FDTD simulation inputs.

## Workbook Findings

- Chart XML present: `False`
- Drawing XML present: `False`
- Comments present: `False`
- Thicknesses: `[152, 163, 185, 200, 215, 233, 250]`
- Expected thicknesses match: `True`
- Offset rule status: `source_figure_encoded_not_workbook_labeled`

| Thickness nm | Columns | Offset added percent | De-offseted range percent | Assignment |
| --- | --- | ---: | --- | --- |
| 152 | B/C | 420 | 3.536 to 61.647 | first=inferred measured, second=inferred simulated |
| 163 | D/E | 350 | 3.341 to 62.327 | first=inferred measured, second=inferred simulated |
| 185 | F/G | 280 | 0.595 to 61.023 | first=inferred measured, second=inferred simulated |
| 200 | H/I | 210 | 1.342 to 55.931 | first=inferred measured, second=inferred simulated |
| 215 | J/K | 140 | 2.704 to 58.046 | first=inferred measured, second=inferred simulated |
| 233 | L/M | 70 | 3.680 to 58.200 | first=inferred measured, second=inferred simulated |
| 250 | N/O | 0 | 1.440 to 57.536 | first=inferred measured, second=inferred simulated |

## Guardrails

- Do not use Wang as ENZ evidence.
- Do not count de-offseting as experimental calibration.
- Do not promote inferred measured/simulated columns to source-labeled holdout columns.
- Use residuals only as source-data reproduction diagnostics.
