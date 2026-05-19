# Phase 3E.2A - Wang W/WO3 Non-ENZ Baseline Intake

## Decision

- Status: `non_enz_baseline_source_data_snapshotted_semantics_partial`
- Claim label: `candidate_non_enz_tmm_baseline_source_data_semantics_partial`
- Claim ceiling: `non_enz_planar_tmm_baseline_candidate`
- Non-ENZ baseline intake ready: `True`
- Phase 4 ENZ ready: `False`
- Can feed serious core: `False`
- Can promote calibrated evidence: `False`
- Download integrity: `selected_downloaded_md5_match`
- Recommended next phase: `Phase 3E.2B - Wang Fig. 2f semantics and no-fit baseline plan`

The package has public source-data spreadsheets, direct W/WO3 n,k tables, and a W/WO3 thickness-series reflectance workbook. It is not ENZ evidence, and Fig. 2f reflectance semantics are not clean enough for a no-fit validation residual yet.

## Source

- Title: `Towards Full-colour Tunability of Inorganic Electrochromic Devices Using Ultracompact Fabry-Perot Nanocavities`
- DOI: `10.6084/m9.figshare.11154791.v1`
- Figshare URL: `https://figshare.com/articles/dataset/Towards_Full-colour_Tunability_of_Inorganic_Electrochromic_Devices_Using_Ultracompact_Fabry-Perot_Nanocavities/11154791`
- Public: `True`
- License: `CC0`
- File count in source package: `30`

## Selected Files

| File | Bytes | MD5 Match |
| --- | ---: | --- |
| `Fig2f-R.xlsx` | `68675` | `true` |
| `FigS1-W.xlsx` | `91218` | `true` |
| `FigS1-WO3.xlsx` | `49191` | `true` |
| `FigS2-nk.xlsx` | `29292` | `true` |

## Constants

| Sheet | Rows | Wavelength Range | n Range | k Range |
| --- | ---: | --- | --- | --- |
| `WO3` | `318` | `[349.99, 856.06]` | `[2.09341, 2.54897]` | `[0.0, 0.07015]` |
| `W` | `316` | `[349.93, 850.97]` | `[2.61453, 4.52814]` | `[2.97504, 3.54254]` |

## Fig. 2f Reflectance Workbook

- Semantics status: `offset_plot_traces_not_plain_absolute_reflectance`
- Thicknesses: `[152, 163, 185, 200, 215, 233, 250]`
- Expected thicknesses match: `True`
- Wavelength range: `[350, 780]` nm
- Wavelength axis descending: `True`
- Measured/simulated assignment: `unlabeled_in_workbook`
- Contains nonphysical plot values: `True`

## Blockers

- W/WO3 Fabry-Perot is a non-ENZ planar TMM baseline, not ENZ calibrated evidence.
- Fig2f-R.xlsx contains vertically offset/nonphysical plotted traces rather than plain 0-100 reflectance columns.
- Fig2f-R.xlsx pairs are not labeled as measured versus simulated inside the workbook.
- Absolute reflectance normalization and holdout-not-used-for-fit status are not proven by the selected spreadsheets alone.
- Ellipsometry source workbook angle labels should be reconciled with article/supplement method wording before formal modeling.

## Next Actions

- Inspect the article figure/caption and any supplementary text to recover the Fig. 2f vertical-offset convention.
- Identify which column in each Fig2f-R.xlsx pair is measured and which is simulated before computing residuals.
- If offsets and measured columns can be source-backed, build a no-fit TMM baseline using FigS2-nk.xlsx constants only.
- Keep Saha TiN/AZO as the ENZ backup; do not let Wang count as the first ENZ Phase 4 evidence.
