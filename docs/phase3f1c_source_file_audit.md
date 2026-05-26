# Phase 3F.1C - Top-Candidate Source-File Audit

Date: 2026-05-26

## Decision

- Status: `completed_source_file_audit_no_candidate_ready`
- Selected next candidate: `none`
- Hard-gate pass count: `0`
- Phase 3F.2 intake allowed: `false`
- TMM adapter started: `false`
- Residual modeling performed: `false`
- Phase 4 candidate: `false`
- Serious-core claim allowed: `false`
- Recommended next phase: `Phase 3F.1D - targeted benchmark/source-data search or explicit code-regression fixture lane`

This pass downloaded and inspected the top three practical non-ENZ fallback
leads from Phase 3F.1B. It remains a source-file audit only. No TMM adapter,
residual modeling, or evidence promotion was attempted.

## Source Packages

The downloaded source packages are stored locally under ignored
`lab_data/raw/phase3f1c_*` directories. They are intentionally not tracked in
git; this report records the source URLs, revisions, byte sizes, and hashes
needed to reacquire or verify them.

| Candidate | Package | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `structural_color_froc_2023` | Nature Source Data XLSX | 49854 | `5aae6bd74d386a6222a84c0e73535a110c0a4d69f6ab7bc13afc29d01edf9db9` |
| `structural_color_froc_2023` | GitHub archive at `7c0998d720c387f1efbffe6d1417593ba2f845b1` | 321170 | `9d595ac110fc203b500780c97393a070c876fc81c5b75e7c20f0e1abf7949d92` |
| `fano_ultrathin_coatings_froc_2021` | GitHub archive at `fb41dbd10b0a34645e5ee6611c4ab7faa15de9b8` | 2649293 | `f858c31647b806514fb805feafe9ec2a809448532e8d707e9fb6e7feb26e7edf` |
| `ultrathin_gold_absorber_2020` | Nature Source Data ZIP | 44262760 | `b765e13c6cc6c2dfc832ee643e134139fb61da9288c1640ad04c2a94cf5641d5` |

## Gate Table

| Candidate | Label After Audit | Gate Pass? | Main Blockers |
| --- | --- | --- | --- |
| `structural_color_froc_2023` | `simulator_validation_fallback_source_audit_blocked` | no | Source-data XLSX is chromaticity/comparison coordinates, not measured spectral R/T holdout; optimized stack artifact is absent; no leakage-safe no-fit split. |
| `fano_ultrathin_coatings_froc_2021` | `proprietary_figure_source_fixture` | no | Measured figure data are Origin OPJ containers; theory TXT files are not measured holdout; material/stack/leakage contract is not open-table-ready. |
| `ultrathin_gold_absorber_2020` | `source_data_rich_leakage_blocked` | no | Public raw FTIR R/T exists, but optical constants/Drude model are fitted from the same spectra and processing code is request-only; no leakage-safe no-fit split. |

## Candidate Notes

### `structural_color_froc_2023`

The Nature article says experimental and comparison data are provided in the
Source Data file and the simulation/optimization code is available on GitHub.
The downloaded Source Data workbook has only two sheets:

- `Fig3`: 49 nonempty rows and 3 columns. The inspected header is `Type, x, y`.
- `Fig5`: 178 nonempty rows and 20 columns. The inspected header is paired
  CIE `x, y` comparison data across multiple prior works and stack families.

That workbook is useful figure data, but it is not a machine-readable measured
spectral R/T holdout. The GitHub archive contains material tables such as
`WO3.csv`, `LiF.csv`, `Bi.csv`, `MoO3.csv`, `constants.csv`, `nGe.txt`, and
`kGe.txt`, plus a TMM notebook. The notebook also writes and later loads
`optimization_results.npy`; no `.npy` file is present in the downloaded archive.

Result: useful simulator/source-memory fallback, but blocked before Phase 3F.2.

### `fano_ultrathin_coatings_froc_2021`

The repository README states that the data types are `SVG`, `IPYNB`, `OPJ`, and
`TXT`, with `OPJ` requiring Origin. The local archive has figure source data in
Origin project files for Figures 2, 3, and 4. The open text files are
`theory-plots` oscillator outputs, not measured spectral holdout tables.

Result: useful literature and proprietary-container memory. It is not a public
open-table simulator-validation candidate without a separate OPJ export phase.

### `ultrathin_gold_absorber_2020`

This is the strongest source-data package among the three in the narrow sense:
the extracted ZIP has 174 files, including 57 `.dpt` spectra. The Fig. 3 and
Fig. 4 READMEs state that the `.dpt` files contain raw FTIR reflectivity or
transmittance, with first column wavenumber and second column measured R or T.

The blocker is leakage, not lack of data. The same public READMEs say the
processing scripts are available on request. `Plotter.m` estimates SiN optical
constants from the bare-SiN R/T data and outputs `SiN_data.mat`; another
`Plotter.m` processes metal-SiN R/T and outputs `measurements.mat`. The article
describes the final Drude/model comparison as fitted from the same bare-SiN and
metal-SiN optical measurements. The public ZIP contains no `.m` or `.mat` files.

Result: source-data-rich fixture or calibration-only reproduction target, but
not a leakage-safe no-fit simulator-validation candidate.

## Stop Rule

Stop before TMM residual modeling remains active. None of the audited top-three
candidates establishes all of:

- source-backed material constants independent of the holdout,
- machine-readable measured spectral holdout,
- source-backed geometry and stack,
- clear substrate/backside/coherence treatment,
- a clean no-fit leakage boundary.

Any residual model at this point would require fitting, guessing, proprietary
export work, or using the same spectral family as both calibration and holdout.
