# Phase 3E.3B - Saha Frozen-Stack Model Provenance And No-Fit Adapter Gate

## Decision

- Status: `frozen_stack_contract_not_source_backed_tmm_blocked`
- Claim-status ceiling: `weak_within_dataset_holdout`
- Current claim label: `source_tables_audited_stack_contract_blocked`
- Adapter contract frozen: `false`
- Full no-fit TMM validation allowed: `false`
- Residual modeling performed: `false`
- Stop rule triggered: `true`
- Recommended next phase: `Phase 3E.4 - renewed ENZ public-data search through stack-contract gate`

Stop before TMM residual modeling: silicon optical constants, substrate/backside/coherence handling, and source-model leakage boundaries are not source-backed tightly enough to freeze a no-fit adapter without guessing.

## Stack-Contract Items

- `canonical_measured_reflectance`: `pass`
  - Phase 3E.3A produced a measured-only Fig. 2b Rp/Rs canonical CSV with source labels preserved.
- `canonical_material_epsilon`: `pass`
  - Phase 3E.3A produced separate TiN and AZO epsilon canonical CSVs from the Fig. 2c/d source table.
- `stack_order_and_thickness`: `pass_for_source_semantics`
  - Paper/source evidence supports air/AZO/TiN/silicon with 250 nm AZO and 130 nm TiN.
- `incidence_and_polarization`: `pass`
  - Fig. 2b source labels preserve 50 degree p/s reflectance channels.
- `silicon_substrate_material`: `partial`
  - The source identifies silicon as the substrate, but does not publish the silicon optical-constant table or model used for Fig. 2b.
- `silicon_optical_constants`: `blocked`
  - Any choice of Palik/Green/Aspnes/crystalline-Si constants would be an external predeclared assumption, not a source-backed Saha Fig. 2 contract.
- `substrate_backside_and_coherence`: `blocked`
  - The source does not freeze substrate thickness, backside condition, wedge/roughness, or coherent versus incoherent backside handling.
- `interface_roughness_or_native_oxide`: `not_source_backed`
  - No source-backed interfacial roughness, native oxide, or EMA layer contract was found for a no-fit adapter.
- `source_model_leakage_boundary`: `partial_not_promotion_clean`
  - Measured and source-simulated Fig. 2b curves are separable, but the article/source package includes author simulations and does not publish a full model-settings file or a promotion-clean calibration/holdout split.

## Source Evidence

- Article: https://www.nature.com/articles/s41467-023-41377-5
- Supplementary information: https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-023-41377-5/MediaObjects/41467_2023_41377_MOESM1_ESM.pdf
- Figshare API: https://api.figshare.com/v2/articles/23734116

Source-backed support:

- The article/Fig. 2 source context supports a 250 nm AZO layer on 130 nm TiN on silicon, with Fig. 2b measured and simulated 50 degree s/p reflectance spectra.
- Figshare describes Fig. 2b as simulated Rp/Rs and experimentally measured reflectance versus wavelength, and Fig. 2c/d as TiN/AZO permittivity tables with film thickness comments.
- The supplementary information says TiN films were measured by VASE at 50 and 70 degrees and modeled with a Drude-Lorentz form.
- The supplementary information says AZO was grown on TiN layers on silicon, and also discusses AZO on silicon/fused-silica comparison samples.

Missing for a frozen no-fit TMM contract:

- No source table or methods text found here freezes silicon optical constants.
- No source table or methods text found here specifies silicon substrate thickness, backside polish/roughness/wedge, or coherent/incoherent backside treatment.
- No complete source TMM settings file is published with the Fig. 2b source-simulated curves.

## Forbidden Next

- Do not run Saha TMM residuals from a convenience silicon optical-constant table.
- Do not tune substrate constants, backside handling, roughness, scale, or offsets.
- Do not use source-simulated Fig. 2b curves as an independent holdout.
- Do not promote Saha above weak-within-dataset holdout without a future predeclared source-backed stack contract and uncertainty policy.
