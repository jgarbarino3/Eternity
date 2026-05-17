# Phase 3C - Public TiN Dataset Intake

Date: 2026-05-17

## Decision

Status: `public_dataset_intake_ready`

This is the first public dataset found so far that looks genuinely useful for a
validation lane instead of another provenance-only loop. It should be treated as
Phase 3C, separate from the exhausted Phase 3A thesis path and the parked Phase
3B TiON path.

The dataset is:

- Title: Low-temperature fabrication of plasmonic titanium nitride thin films by
  electron beam evaporation (dataset)
- Dataset DOI: `10.17630/42a1d567-9e02-4916-8709-e2b4911c715c`
- Dataset URL: `https://research-portal.st-andrews.ac.uk/en/datasets/low-temperature-fabrication-of-plasmonic-titanium-nitride-thin-fi/`
- Linked paper DOI: `10.1088/2515-7647/adcddc`
- Dataset license: CC BY
- Paper: Das et al., Journal of Physics: Photonics 7, 025032 (2025)

## Safe Intake

The browser-downloaded archive was checked before repo snapshotting.

- Local source: `/Users/joegarbarino/Downloads/TiN-data_Pure.zip`
- Repo snapshot: `lab_data/raw/public_st_andrews_tin_2025/TiN-data_Pure.zip`
- SHA-256: `e3a6eaf3baf86c926a1234302a888c2a6678a1c8949a33e2898fdb8c75efdc00`
- Bytes: `899515`
- File type: zip archive
- Archive members inspected with `unzip -l`; no executable payloads were run.

The linked open-access paper was also snapshotted as provenance:

- Repo snapshot: `lab_data/raw/public_st_andrews_tin_2025/Das_2025_JoPP_TiN.pdf`
- SHA-256: `6f3a0e86debce7de92148fe84431e645fdf590ca1f5d1466664541cd8544ac55`
- Bytes: `2321499`

## Contents Found

The archive contains 33 files:

- 11 extracted ellipsometry permittivity tables under `Ellipsometry/*.txt`.
- Woollam/CompleteEASE-style raw `.SE` and `.mod` files under
  `Ellipsometry/raw file/`.
- `RT.xlsx`, with wavelength/transmittance and wavelength/reflectance columns.
- `XRD_2DT2T_ex2_exported.xy`.

The ellipsometry tables cover approximately `245.874-1689.242 nm`. The RT
spreadsheet covers approximately `340-1030 nm`, while the paper states the
reflectance/transmittance spectra were recorded over `400-1000 nm`.

## Paper-Backed Mapping

The linked paper states that all TiN films were deposited on AmScope microscope
glass slides. It describes ellipsometry with a J.A. Woollam M-2000 and
CompleteEASE modeling. It says reflectance and transmittance spectra were
recorded from `400 nm` to `1000 nm` using an Ocean Optics USB-4000 CCD
spectrometer and a white LED.

Most important for validation, the paper states that Figure 4 displays
unpolarized transmittance and reflectance spectra for `50 nm` TiN films measured
at normal incidence on glass. The text says the reflectance minimum is about
`20%` near `540 nm`. The downloaded `RT.xlsx` reflectance column has a minimum
inside the paper window at:

- `542.06 nm`
- value `0.20377`

That strongly supports interpreting the reflectance column as a fractional
absolute-like reflectance trace, at least for Figure 4, but it is not yet a
complete validation contract because the spreadsheet does not explicitly label
which ellipsometry table is the exact paired material model.

## Current Claim Boundary

This dataset is promising enough to continue. It is not yet
`calibrated_linear_evidence`.

Current permitted status:

- `public_dataset_grounding`
- `validation_candidate_ready_after_mapping`

Current forbidden status:

- `calibrated_linear_evidence`

Remaining blockers before calibrated evidence:

- Identify the exact ellipsometry table that pairs with `RT.xlsx`.
- Confirm whether `RT.xlsx` is Figure 4 for the 50 nm TiN film annealed at
  `50 C`, another 50 nm condition, or a combined/exported trace.
- Decide whether the measured R/T data are independent of the material-model
  fit or part of the same characterization package.
- Predeclare wavelength window, residual metrics, and pass/fail thresholds
  before inspecting any new model residuals.
- Add a loader or extraction path for `RT.xlsx` and selected ellipsometry tables.

## Recommended Next Phase

Next: **Phase 3C.1 - St Andrews TiN Pairing + Validation Candidate Plan**

Planning effort: GPT-5.5 `high`

Implementation effort: GPT-5.5 `high` if adding loaders and a validation
candidate; `medium` if only writing the mapping packet.

Planning is recommended before implementation because the key scientific choice
is not code mechanics. The real question is which ellipsometry table is allowed
to predict which R/T trace without leakage.

Helpful tools:

- Local shell, `unzip`, `pdftotext`, `shasum`, and spreadsheet parsing.
- GPD planner/checker/verifier for the mapping and no-fit-leakage policy.
- Consensus MCP only if we need literature support for acceptable R/T
  validation metrics or TiN optical-model practice.
