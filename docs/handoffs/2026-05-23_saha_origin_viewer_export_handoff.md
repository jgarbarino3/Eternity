# Handoff - Saha Origin Viewer Export

Date: 2026-05-23

## What Just Happened

The Saha TiN/AZO OPJU conversion blocker was cleared for the two key Fig. 2
source-data files.

We used a temporary AirGPU Windows VM with official Windows Origin Viewer 9.9.5
to open:

- `lab_data/raw/public_saha_tin_azo_2023/Source data for Fig 2b.opju`
- `lab_data/raw/public_saha_tin_azo_2023/Source data for Fig 2cd.opju`

In Origin Viewer, each worksheet was exported with `File -> Export Data to
CSV...`. The CSVs were then transferred back to the Mac and placed in the repo.

The Windows cloud PC is no longer needed for these two files.

## New Data Artifacts

Exported CSVs:

- `lab_data/raw/public_saha_tin_azo_2023/origin_viewer_exports/saha_fig2b_origin_viewer_export.csv`
- `lab_data/raw/public_saha_tin_azo_2023/origin_viewer_exports/saha_fig2cd_origin_viewer_export.csv`

Hashes:

- Fig. 2b CSV: `b8134a6ff368a2c8707453ca80dae862b27608bffbb1b9ad4bdb163a8cf2d0b2`
- Fig. 2c/d CSV: `436a6db455883ae66cc6f3880e563c0287c6f04842eb231150567737cc1caaa8`

Initial shape checks:

- Fig. 2b export has 178 rows total and 175 numeric wavelength rows from
  260-2000 nm.
- Fig. 2b preserves labels for `Simulated Rp`, `Measured Rp`, `Measured Rs`,
  and `Simulated Rs`.
- Fig. 2b preserves `50 deg` comments for the reflectance channels.
- Fig. 2c/d export has 184 rows total and 181 numeric wavelength rows from
  300-2100 nm.
- Fig. 2c/d preserves labels for TiN/AZO real and imaginary permittivity.
- Fig. 2c/d preserves comments for `Film thickness 130 nm` and `Film thickness
  250 nm`.

## Repo Records Updated

- `docs/phase3e3_saha_opju_origin_viewer_export.md`
- `lab_data/raw/public_saha_tin_azo_2023/README.md`
- `lab_data/registry.yaml`
- `docs/phase_index.md`
- `docs/PROJECT_ATLAS.md`
- `docs/project_atlas/index.html`

The stale heartbeat automation `saha-opju-windows-pc-follow-up` was deleted
because Windows access is no longer the blocker.

## Claim Boundary

Current Saha status:

`source_tables_exported_ready_for_audit`

This is not calibrated evidence yet. Do not run a victory-lap TMM comparison or
promote the claim until the source semantics are audited.

Open audit questions:

- Are the Fig. 2b measured reflectance columns absolute reflectance or otherwise
  physically usable for a no-fit comparison?
- Are the simulated columns clearly separable and excluded from any holdout
  metric?
- Do the paper and source data fully specify stack order, Si substrate handling,
  incidence angle, and s/p polarization semantics?
- Were Fig. 2b reflectance data used to tune the Fig. 2c/d permittivity,
  thickness, roughness, scale, or other model parameters?
- Can a frozen no-fit model be declared before looking at residuals?

## Recommended Next Goal

Create a goal for:

`Phase 3E.3A - Saha exported-table audit and candidate gate`

Suggested objective:

Audit the exported Saha Fig. 2b and Fig. 2c/d CSV source tables, normalize them
into canonical machine-readable artifacts, verify source semantics against the
paper/Figshare metadata, and decide whether Saha can proceed to a frozen no-fit
TMM candidate attempt or must remain `weak_within_dataset_holdout`,
`literature_reproduction_fixture`, or another conservative label. Continue into
the TMM adapter only if the audit clears the split, geometry, normalization, and
leakage gates.

Suggested stop rule:

Stop before TMM residual modeling if measured reflectance normalization,
geometry, stack details, or leakage cannot be established without fitting or
guessing.

Suggested reasoning effort:

- Planning: GPT-5.5 `high`
- Implementation: `medium` for report-only audit
- Implementation: `high` if building the TMM candidate adapter after the audit

Helpful tools:

- local CSV/table inspection
- paper/Figshare metadata inspection
- GPD only for claim-boundary and promotion review
- Browse.sh/Plasmate only if source-page details need refreshing
