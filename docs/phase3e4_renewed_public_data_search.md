# Phase 3E.4 - Renewed ENZ Public-Data Search Through Stack-Contract Gate

## Decision

- Status: `phase3e4_search_snapshot_no_phase4_candidate`
- Can open Phase 4 now: `false`
- Can feed Serious Core now: `false`
- Claim standard changed: `false`
- Residual modeling performed: `false`
- TMM adapter started: `false`
- Recommended next phase: `Phase 3E.4 - continue renewed ENZ public-data search through the stack-contract gate`

Find a public ENZ/TCO/TiN/AZO thin-film dataset that clears material, measured holdout, geometry, stack/substrate/backside, and leakage gates before residual inspection.

## Search Summary

- Inspected leads: `7`
- Phase 4 candidates: `0`
- Corrected prior lead(s): `acs_intracavity_ito_2025_zenodo_data`

| Lead | Label | Phase 4? | Decision |
| --- | --- | --- | --- |
| acs_intracavity_ito_2025_zenodo_data | `literature_reproduction_fixture` | no | `zenodo_matlab_package_found_not_phase4_ready` |
| linkoping_ito_pedot_2026 | `literature_reproduction_fixture` | no | `table_ready_fixture_not_planar_phase4_candidate` |
| ito_glass_sio2_optical_properties_2025 | `calibration_only_no_holdout` | no | `constants_fixture_no_independent_holdout` |
| spacetime_synthetic_motion_ito_2025 | `literature_reproduction_fixture` | no | `nonlinear_source_data_fixture_no_static_holdout` |
| natural_enz_compendium_2025 | `calibration_only_no_holdout` | no | `constants_compendium_not_validation_dataset` |
| acs_lbsno_ferrell_berreman_2026 | `blocked_source_data_lead` | no | `public_si_pdf_only` |
| enz_metal_oxide_reflectors_2024 | `blocked_source_data_lead` | no | `public_si_pdf_only` |

## Stack-Contract Gate

- `source_backed_material_constants`: optical constants or model parameters are public and tied to the sample
- `independent_measured_holdout`: measured R/T/A or ellipsometry holdout is separable from calibration data
- `machine_readable_tables`: numerical data are tables, arrays, or scripts, not plots only
- `measurement_geometry`: angle, polarization, side, and units are source-backed
- `stack_order_and_thickness`: layer order, thicknesses, and sample identity are source-backed
- `substrate_optical_contract`: substrate optical constants/model are source-backed
- `backside_coherence_contract`: substrate backside, thickness, wedge/roughness, and coherence treatment are source-backed
- `leakage_boundary`: source model and measured holdout can be used without residual-driven tuning
- `planar_tmm_regime`: the measurement is physically suitable for the current linear planar TMM

## Inspected Lead Notes

### acs_intracavity_ito_2025_zenodo_data

- Title: Intracavity Epsilon-Near-Zero Dual-Range Frequency Switch
- Decision: `zenodo_matlab_package_found_not_phase4_ready`
- Claim label: `literature_reproduction_fixture`
- Reason: Useful source-code/data fixture, but not a clean independent static linear R/T/A holdout with frozen stack, substrate, backside, and leakage contracts.
- Sources:
  - https://zenodo.org/records/14236212
  - https://pubs.acs.org/doi/10.1021/acsphotonics.4c01322
- Inspection:
  - Zenodo exposes Zenodo_Data.zip with MD5 41d93af8f27d62a2474ee06fbc9b1ce8.
  - The ZIP has 31 MATLAB-oriented members, including article figure scripts, Data_ellipsometer_FP_2um.mat, Data_TMM_TRA_diff_thickness.mat, and Data_OSA_OSC.mat.
  - This corrects the older global registry wording that treated the ACS intracavity lane as only public PDF/SI.

### linkoping_ito_pedot_2026

- Title: Electrotunable coupling between an epsilon-near-zero thin film and conducting polymer nanoantennas
- Decision: `table_ready_fixture_not_planar_phase4_candidate`
- Claim label: `literature_reproduction_fixture`
- Reason: Good public source-data fixture for ENZ coupling and bare-film extinction, but the required material/holdout split and planar stack contract are not frozen.
- Sources:
  - https://zenodo.org/records/18412236
  - https://pubmed.ncbi.nlm.nih.gov/41671185/
- Inspection:
  - Zenodo exposes Figure 1/2/3/4 ZIPs; Figure 2 has measured and simulated angle/polarization-dependent extinction spectra for a 50 nm ITO film on glass.
  - The final device lane is nanorod/ITO hybrid coupling, not a plain planar thin-film validation target.

### ito_glass_sio2_optical_properties_2025

- Title: ITO, soda lime float glass and SiO2 buffer layer optical properties
- Decision: `constants_fixture_no_independent_holdout`
- Claim label: `calibration_only_no_holdout`
- Reason: Useful public optical-constants fixture; not a validation candidate.
- Sources:
  - https://zenodo.org/records/15055400
- Inspection:
  - Zenodo exposes ITO, soda-lime glass, and SiO2 optical dispersion files; ITO_20 Ohm_105 nm_e1e2.mat is a plain text e1/e2 table despite its extension.
  - No independent measured R/T/A holdout was found in the record metadata or files inspected.

### spacetime_synthetic_motion_ito_2025

- Title: Space-Time Optical Diffraction from Synthetic Motion
- Decision: `nonlinear_source_data_fixture_no_static_holdout`
- Claim label: `literature_reproduction_fixture`
- Reason: Public and table-ready, but it is a nonlinear diffraction package, not a static TMM holdout.
- Sources:
  - https://figshare.com/projects/Space-Time_Optical_Diffraction_from_Synthetic_Motion_-_Source_data/229662
  - https://www.nature.com/articles/s41467-025-60159-9
- Inspection:
  - Figshare project 229662 contains article 27925419 with XLSX, NPZ, and TXT source-data files for space-time diffraction measurements.
  - The inspected Fig. 2b workbook is diffraction efficiency versus pump-probe delay, and the NPZ/TXT files are nonlinear frequency-momentum data.

### natural_enz_compendium_2025

- Title: Compendium of Natural Epsilon-Near-Zero Materials
- Decision: `constants_compendium_not_validation_dataset`
- Claim label: `calibration_only_no_holdout`
- Reason: Good literature-memory fixture; not a sample-matched validation dataset.
- Sources:
  - https://acs.figshare.com/articles/dataset/Compendium_of_Natural_Epsilon-Near-Zero_Materials/29134854
  - https://pubs.acs.org/doi/10.1021/acsphotonics.5c00199
- Inspection:
  - The Figshare source file is an XLSX compendium of n, k, Re(epsilon), Im(epsilon), and quality metrics across spectral bands.
  - No sample-specific measured thin-film holdout or stack contract is present.

### acs_lbsno_ferrell_berreman_2026

- Title: Active Tuning of the Ferrell-Berreman Mode of La-Doped BaSnO3
- Decision: `public_si_pdf_only`
- Claim label: `blocked_source_data_lead`
- Reason: Interesting ENZ/TCO-like lead, but not table-package-ready.
- Sources:
  - https://acs.figshare.com/articles/journal_contribution/Active_Tuning_of_the_Ferrell-Berreman_Mode_of_La-Doped_BaSnO_sub_3_sub_/31618292
- Inspection:
  - Figshare exposes only the ACS supporting-information PDF for this lead.

### enz_metal_oxide_reflectors_2024

- Title: Epsilon-Near-Zero Metal Oxide-Based Spectrally Selective Reflectors
- Decision: `public_si_pdf_only`
- Claim label: `blocked_source_data_lead`
- Reason: Potentially relevant reflector paper, but no public numerical source package was found.
- Sources:
  - https://acs.figshare.com/articles/journal_contribution/Epsilon-Near-Zero_Metal_Oxide-Based_Spectrally_Selective_Reflectors/26097966
- Inspection:
  - Figshare exposes only the ACS supporting-information PDF for this lead.

## Stop Rule

- Triggered: `true`
- Reason: No inspected lead establishes the complete measured reflectance/geometry/stack/substrate/backside/leakage contract needed for no-fit TMM residual modeling.
