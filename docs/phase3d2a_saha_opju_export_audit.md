# Phase 3D.2A - Saha OPJU Worksheet Export Audit

## Decision

- Status: `local_opju_export_blocked`
- Can feed serious core: `false`
- Can promote calibrated evidence: `false`
- Phase 4 ready: `false`
- Claim-status ceiling: `opju_blocked_source_data_lead`
- Recommended next phase: `Phase 3D.3 - next public candidate source-data intake`

## What Was Tried

Phase 3D.2A tested whether the Saha Fig. 2b and Fig. 2c/d Origin `.opju`
worksheets could be exported locally instead of leaving the export path as a
hand-wavy TODO.

Local probes:

- Installed LabPlot 2.12.1 through Homebrew.
- Ran `/Applications/LabPlot.app/Contents/MacOS/labplot --help`.
- Inspected the LabPlot binary for Origin import/export strings.
- Tried opening `Source data for Fig 2cd.opju` with LabPlot in offscreen mode.

## Findings

- LabPlot installed, but its command-line surface only exposes file/project open
  behavior, not batch worksheet export.
- LabPlot's embedded Origin strings identify `OPJ` import support, not `OPJU`
  CSV export support.
- The offscreen `.opju` open attempt timed out in GUI/dialog behavior and
  produced no CSV or other table output.
- `JNisk/convert-opju` is a useful future route, but it requires Windows 11,
  Origin 2024b, and Origin's Python integration.
- Origin/Origin Viewer on Windows remains the most authoritative export path.

## Interpretation

Saha is not rejected scientifically. It is locally export-blocked. The public
package still has the right Fig. 2 labels and verified source files, but no
residual modeling or claim promotion can happen until the OPJU worksheets are
converted into auditable tables.

Do not digitize the embedded worksheet previews into calibrated evidence. If the
only available route is preview/image digitization, downgrade the candidate to a
plot-derived or literature-reproduction fixture.

## Next

Move to the next public candidate intake unless the user can provide a Windows
Origin/Origin Viewer export, an OPJU-capable GUI export, or an open-format mirror
for the Saha Fig. 2b and Fig. 2c/d worksheets.
