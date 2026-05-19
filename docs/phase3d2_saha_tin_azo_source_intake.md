# Phase 3D.2 - Saha TiN/AZO Source-Data Intake

## Decision

- Status: `source_package_snapshotted_origin_export_blocked`
- Can feed serious core: `False`
- Can promote calibrated evidence: `False`
- Phase 4 ready: `False`
- Claim-status ceiling: `candidate_unclassified_until_table_export`
- Download integrity: `all_downloaded_md5_match`
- Recommended next phase: `Phase 3D.2A - Saha OPJU worksheet export or open-format alternate`

## Source

- Title: `Engineering the Temporal Dynamics 
of All-Optical Switching with Fast and Slow Materials`
- DOI: `10.6084/m9.figshare.23734116.v1`
- Figshare URL: `https://springernature.figshare.com/articles/dataset/Engineering_the_Temporal_Dynamics_of_All-Optical_Switching_with_Fast_and_Slow_Materials/23734116`
- Public: `True`
- License: `CC BY 4.0`
- File count: `12`

## Target Files

- Fig. 2b file: `Source data for Fig 2b.opju`
- Fig. 2b labels: `['Wavelength', 'Simulated Rp', '50 deg', 'Measured Rp', '50 deg', 'Wavelength', 'Measured Rs', '50 deg', 'Wavelength', 'Simulated Rs', '50 deg']`
- Fig. 2c/d file: `Source data for Fig 2cd.opju`
- Fig. 2c/d labels: `["'&Wavelength", 'Film thickness 130 nm', 'TiN real part of permittivity', "'&Wavelength", 'Film thickness 250 nm', 'AZO real part of permittivity', 'Wavelength', '$#TiN imaginary part of permittivity', 'Wavelength', '$#AZO imaginary part of permittivity']`

## Interpretation

The public Figshare package contains the expected Fig. 2b reflectance and Fig. 2c/d permittivity Origin files, and their embedded labels match the intended calibration/holdout lanes. The current local environment cannot export the proprietary OPJU worksheet tables to CSV, so no residual run or promotion decision is allowed yet.

## Extraction Options

- Export the two OPJU worksheets to CSV with Origin or free Origin Viewer on Windows.
- Try LabPlot GUI import/export if installed on a compatible macOS system.
- Find a publisher-provided open-format mirror for Fig. 2b and Fig. 2c/d.
- If only plot/image digitization is possible, downgrade to literature_reproduction_fixture.
