# Saha TiN/AZO 2023 Public Source-Data Snapshot

Phase 3D.2 downloaded the public Figshare source-data package for:

- `Engineering the Temporal Dynamics of All-Optical Switching with Fast and Slow Materials`
- Figshare DOI: `10.6084/m9.figshare.23734116`
- Paper DOI: `10.1038/s41467-023-41377-5`

The package contains Origin `.opju` source-data files. Fig. 2b and Fig. 2c/d
are the current target files because their embedded labels identify measured
reflectance and TiN/AZO permittivity columns. The files are public and hash
verified.

On 2026-05-23, the two key OPJU files were opened with official Windows Origin
Viewer 9.9.5 on a temporary Windows VM and exported with `File -> Export Data
to CSV...`. The exported worksheet CSVs are in `origin_viewer_exports/`:

- `saha_fig2b_origin_viewer_export.csv`
- `saha_fig2cd_origin_viewer_export.csv`

These are now source-table exports, not carved preview images. They still need a
scientific audit before any validation claim: confirm measured-vs-simulated
column semantics, geometry, normalization, and whether the Fig. 2b reflectance
comparison leaked into the permittivity/thickness model.

Phase 3E.3A audited those exports and wrote canonical split artifacts:

- `saha_fig2b_measured_reflectance_canonical.csv`
- `saha_fig2b_source_simulated_reflectance_canonical.csv`
- `saha_fig2cd_tin_epsilon_canonical.csv`
- `saha_fig2cd_azo_epsilon_canonical.csv`

The audit found that measured/source-simulated labels, 50 degree s/p semantics,
and TiN/AZO epsilon/thickness labels are clean enough for machine-readable
source-table use. It stopped before TMM residual modeling because the exported
source tables do not freeze a reproducible silicon substrate optical-constant
source, substrate/backside treatment, or full source-model leakage boundary.

Phase 3E.3B then checked whether the missing stack contract could be frozen
from the paper, Supplementary Information, Figshare metadata, and exported
source tables. It failed closed: stack order, thickness, and 50 degree s/p
semantics are source-backed, but silicon optical constants,
substrate/backside/coherence handling, and interface/oxide assumptions are not
source-backed enough for a no-fit TMM residual run.

Current status is `frozen_stack_contract_not_source_backed_tmm_blocked`, with a
`weak_within_dataset_holdout` ceiling for source-table memory only.

Embedded PNG worksheet previews were carved only for audit/visual inspection.
They are not calibrated numerical data and must not be promoted as a measured
holdout.
