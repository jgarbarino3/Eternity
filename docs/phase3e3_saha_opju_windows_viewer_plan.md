# Phase 3E.3 - Saha OPJU Windows Viewer Plan

Date: 2026-05-19

## Status

Saha TiN/AZO remains the best ENZ backup candidate, but it is blocked on
source-table extraction from Origin `.opju` files.

Current classification:

- Candidate: Saha et al. 2023 TiN/AZO, Nature Communications.
- Public package: Springer Nature Figshare `23734116`.
- Key files: `Source data for Fig 2cd.opju` and `Source data for Fig 2b.opju`.
- Current blocker: no reliable native macOS OPJU-to-CSV extraction route.
- Claim status: not calibrated evidence; keep parked until true worksheet
  extraction succeeds.

## Agreed Next Practical Route

While the user looks for a Windows PC or Windows VM:

1. Run a bounded Mac smoke test for direct OPJU parsing.
   Expected result: fail or no usable worksheet tables.
2. Try official Windows Origin Viewer 9.9.5 on a borrowed Windows machine.
3. In Origin Viewer, open each Saha OPJU file.
4. Try to save as `.opj`.
5. Try to export active worksheets as CSV.
6. Bring any OPJ/CSV exports back to the Mac.
7. Parse and audit exported files in Eternity.

Do not use generic online converters for the evidence gate.
Do not treat plot digitization or chart-trace recovery as source-table data.

## Success Criteria

Saha can move from `opju_export_blocked` to inspectable only if exports preserve
real worksheet tables and enough labels/comments to identify:

- TiN and AZO epsilon/permittivity tables from Fig. 2c/d.
- Film thickness metadata, ideally comments/notes rather than paper-only memory.
- Fig. 2b measured reflectance columns separated from simulated Rp/Rs columns.
- Angle and polarization labels, especially 50 degrees and s/p.
- Whether any holdout leakage is visible or still unresolved.

## Stop Rule

Park Saha again if:

- direct Mac parsers fail,
- Windows Origin Viewer cannot export OPJ/CSV,
- only chart traces/images are recoverable,
- metadata labels/comments are not preserved well enough,
- or no Windows Viewer/Origin route becomes available.

The honest next state in that case is:

`candidate_status = opju_export_blocked_requires_windows_origin_viewer_or_origin`
