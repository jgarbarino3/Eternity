# Phase 3E.3 - Saha OPJU Origin Viewer Export

Date: 2026-05-23

## Status

The Saha TiN/AZO OPJU export blocker is cleared for the two key Fig. 2 source
tables. This does not promote Saha to calibrated evidence. It only moves the
candidate from `opju_export_blocked` to `source_tables_exported_ready_for_audit`.

## Export Route

- Source package: Springer Nature Figshare `23734116`.
- Source OPJU files:
  - `lab_data/raw/public_saha_tin_azo_2023/Source data for Fig 2b.opju`
  - `lab_data/raw/public_saha_tin_azo_2023/Source data for Fig 2cd.opju`
- Tool: official Windows Origin Viewer 9.9.5.
- Environment: temporary AirGPU Windows VM.
- Viewer action: `File -> Export Data to CSV...`.
- Transfer route: CSVs uploaded from the VM to `tmpfiles.org` and downloaded
  back to the Mac.

## Exported Artifacts

| Artifact | Path | SHA-256 | Rows |
| --- | --- | --- | --- |
| Fig. 2b reflectance worksheet export | `lab_data/raw/public_saha_tin_azo_2023/origin_viewer_exports/saha_fig2b_origin_viewer_export.csv` | `b8134a6ff368a2c8707453ca80dae862b27608bffbb1b9ad4bdb163a8cf2d0b2` | 178 |
| Fig. 2c/d permittivity worksheet export | `lab_data/raw/public_saha_tin_azo_2023/origin_viewer_exports/saha_fig2cd_origin_viewer_export.csv` | `436a6db455883ae66cc6f3880e563c0287c6f04842eb231150567737cc1caaa8` | 184 |

## Initial Shape Check

`saha_fig2b_origin_viewer_export.csv` preserves worksheet labels for:

- `Wavelength`
- `Simulated Rp`
- `Measured Rp`
- `Measured Rs`
- `Simulated Rs`

The worksheet comments preserve `50 deg` for all four reflectance channels. The
numeric wavelength rows span 260-2000 nm.

`saha_fig2cd_origin_viewer_export.csv` preserves worksheet labels for:

- `TiN real part of permittivity`
- `AZO real part of permittivity`
- `TiN imaginary part of permittivity`
- `AZO imaginary part of permittivity`

The worksheet comments preserve `Film thickness 130 nm` for TiN and `Film
thickness 250 nm` for AZO. The numeric wavelength rows span 300-2100 nm, with
AZO columns ending before the TiN long-wavelength tail.

## Claim Boundary

Phase-close claim label ceiling: `source_tables_exported_ready_for_audit`.

Do not promote Saha until a follow-up audit confirms:

- measured Fig. 2b columns are truly measured absolute or otherwise usable
  reflectance, not normalized/arbitrary plot values;
- simulated Fig. 2b columns are excluded from any holdout metric;
- 50 degree geometry and s/p polarization semantics match the paper methods;
- Si substrate and stack order are fully specified for the TMM model;
- no reflectance-side fitting, scale offset, roughness tuning, or thickness
  tuning is needed after seeing the measured holdout;
- the paper/source data do not show leakage from Fig. 2b reflectance into the
  Fig. 2c/d permittivity/thickness model.

## Next Phase

Recommended next phase: `Phase 3E.3A - Saha exported-table audit and candidate
gate`.

Planning effort: GPT-5.5 `high`; implementation effort: `medium` for a
report-only audit, `high` if building the TMM candidate adapter.

Follow-up status: Phase 3E.3A is now complete in
`docs/phase3e3a_saha_exported_table_audit.md`. It canonicalized the exported
tables and stopped before TMM residual modeling because substrate optical
constants, substrate/backside treatment, and full source-model leakage
boundaries are not frozen by the source tables.

Second follow-up status: Phase 3E.3B is now complete in
`docs/phase3e3b_saha_stack_model_gate.md`. It confirmed that the missing frozen
stack contract cannot be source-backed from the paper, Supplementary
Information, Figshare metadata, or exported tables. No TMM residuals were run.
