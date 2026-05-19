# Phase 3D.5A - ACS Intracavity PDF Correction

Date: 2026-05-19

## Purpose

Correct the Phase 3D.5 ACS/intracavity candidate classification after manual
browser downloads resolved what the direct `51010982` link provides.

## Local Files Inspected

- Main article PDF:
  `/Users/joegarbarino/Downloads/intracavity-epsilon-near-zero-dual-range-frequency-switch.pdf`
- Supporting Information PDF:
  `/Users/joegarbarino/Downloads/ph4c01322_si_001.pdf`

Hashes:

| File | MD5 | SHA-256 |
| --- | --- | --- |
| `intracavity-epsilon-near-zero-dual-range-frequency-switch.pdf` | `86e5085ae71210ac7819760155fff20a` | `8862ccd440e43b6c041190b13c174985de7bc817fe0d43ce0f84ee3045bc568d` |
| `ph4c01322_si_001.pdf` | `5bd17b23eaab2713772a717bb1416160` | `588d9257424994cf6a69128c5f88c82e20050206ba8be848ed69822f5847e7f6` |

## Correction

The direct `figshare.com/ndownloader/files/51010982` lead resolves, through the
manual browser path, to the ACS Supporting Information PDF rather than a
separate raw source-data package.

The public package currently available for this candidate is therefore:

- main article PDF;
- Supporting Information PDF.

No embedded data files were found in either PDF:

```text
pdfdetach -list ... -> 0 embedded files
```

## Useful Information Recovered

The PDFs strengthen provenance for a literature/model fixture:

- Structure: ITO / silica glass / ITO Fabry-Perot nanostructure.
- Silica thickness: `1.1 mm`.
- ITO layer thickness: `135 nm` on both sides.
- SI ellipsometry instrument: J.A. Woollam RC2, `210-2500 nm`.
- Measured ITO side thicknesses: `133.49 nm` and `135.46 nm`.
- Surface roughness: `7.14 +/- 0.148 nm` and `7.70 +/- 0.130 nm`.
- ENZ frequencies: `162.02 THz` and `156.85 THz`.
- SI Table S1 provides Drude parameters for both sides.
- SI Figure S4 shows T/R/A curves from transfer-matrix calculations for
  substrate thicknesses `1.1 mm`, `0.5 mm`, and `0.1 mm`.

## Acceptance Impact

This does not create a Phase 4 candidate.

Fails for `calibrated_linear_evidence`:

- No raw CSV/TXT/XLSX/HDF5/JSON source-data package was found.
- No machine-readable epsilon table was found.
- No independent measured static R/T/A holdout table was found.
- The visible T/R/A curves are calculated TMM outputs in the SI, not a separate
  measured holdout.
- Any use would require plot digitization or model reconstruction, both capped
  below calibrated evidence.

Updated candidate classification:

```text
public_pdf_si_only_no_raw_tables
```

Claim ceiling:

```text
literature_reproduction_fixture
```

## Decision

Decision: `acs_intracavity_pdf_only_no_phase4_candidate`.

The candidate is no longer an access-blocked unknown. It is a public PDF/SI-only
literature fixture unless a separate raw source-data package appears later.

## Next Step

Continue to `Phase 3E.1 - Public Dataset Gate And Executive Research Assistant
Scaffold`.
