# Wang 2020 W/WO3 Fabry-Perot Source-Data Snapshot

Date: 2026-05-19

Source: Figshare dataset DOI `10.6084/m9.figshare.11154791`, supporting
Wang et al., *Nature Communications* 2020, DOI
`10.1038/s41467-019-14194-y`.

This is a non-ENZ planar Fabry-Perot baseline candidate, not ENZ calibrated
evidence. The selected files are kept because they provide a small public
source-data package for testing TMM validation plumbing:

- `FigS1-W.xlsx`: W ellipsometry-like source-data sheets.
- `FigS1-WO3.xlsx`: WO3 ellipsometry-like source-data sheets.
- `FigS2-nk.xlsx`: direct W and WO3 `n,k` tables.
- `Fig2f-R.xlsx`: W/WO3 thickness-series reflectance-like plotted traces.
- `figshare_article_11154791.json`: Figshare API metadata snapshot.

Important blocker: `Fig2f-R.xlsx` contains vertically offset/nonphysical plot
values and does not label the paired columns as measured versus simulated in the
workbook. Do not compute validation residuals from this file until the offset
and column semantics are source-backed.
