# Phase 3E.3A - Saha Exported-Table Audit And Candidate Gate

## Decision

- Status: `canonical_tables_ready_tmm_adapter_blocked`
- Claim-status ceiling: `weak_within_dataset_holdout`
- Current claim label: `source_tables_audited_not_tmm_ready`
- Canonical tables ready: `true`
- Full no-fit TMM validation allowed: `false`
- Stop rule triggered: `true`
- Recommended next phase: `Phase 3E.3B - Saha frozen-stack model provenance and no-fit adapter gate`

Stop before TMM residual modeling because substrate optical constants, substrate/backside treatment, and full source-model leakage boundaries are not frozen by the source tables.

## Canonical Artifacts

- `fig2b_measured_reflectance`: `lab_data/raw/public_saha_tin_azo_2023/saha_fig2b_measured_reflectance_canonical.csv`
  - Role: `holdout_candidate_measured_reflectance_source_labeled`
  - SHA-256: `1a9d799fa66b157bb629b28aa6052a7696e8c246abbf5e7e514eaae37c2a2455`
- `fig2b_source_simulated_reflectance`: `lab_data/raw/public_saha_tin_azo_2023/saha_fig2b_source_simulated_reflectance_canonical.csv`
  - Role: `source_simulated_reference_for_audit_not_holdout`
  - SHA-256: `436e0197e2efed80197f067ef19de12716f61aaa3aa9ebec6f3b778490f45dc8`
- `fig2cd_tin_epsilon`: `lab_data/raw/public_saha_tin_azo_2023/saha_fig2cd_tin_epsilon_canonical.csv`
  - Role: `calibration_material_input_candidate_tin`
  - SHA-256: `8542dc38f6a31c9a825d0fff0f23e7f8b76c9b069b55f37a080924a8552f1cfe`
- `fig2cd_azo_epsilon`: `lab_data/raw/public_saha_tin_azo_2023/saha_fig2cd_azo_epsilon_canonical.csv`
  - Role: `calibration_material_input_candidate_azo`
  - SHA-256: `56750fe9a771d79228d417bbbabeb3d833b094dbd39f68993a27e21f2e0aa75f`

## Fig. 2b Reflectance Audit

- Numeric rows: `175`
- Wavelength range: `260.0`-`2000.0` nm
- Wavelength step: `10.0` nm
- Measured Rp fraction range: `0.000542849`-`0.661244`
- Measured Rs fraction range: `0.0974151`-`0.844539`
- Unit-interval check: `pass`
- Measured/source-simulated split: `explicit_source_labels`

## Fig. 2c/d Permittivity Audit

- TiN numeric rows: `181`
- TiN wavelength range: `300.0`-`2100.0` nm
- TiN ENZ crossings: `[484.054679]` nm
- AZO numeric rows: `171`
- AZO wavelength range: `300.0`-`2000.0` nm
- AZO ENZ crossings: `[1364.223257]` nm

## Gates

- `split_gate`: `pass`
  - Origin Viewer export preserves explicit measured Rp/Rs and source-simulated Rp/Rs labels. Canonical artifacts keep those families in separate CSV files.
- `geometry_gate`: `pass_for_source_semantics`
  - Source comments and paper text agree on 50 degree s/p reflectance from the air/AZO/TiN/silicon stack.
- `normalization_gate`: `conditional_pass_for_weak_holdout_only`
  - Figshare and paper call Fig. 2b reflectance, not normalized modulation; all measured values are unit-interval fractions. The source does not provide a separate instrument calibration record, so this is not calibrated-linear evidence.
- `leakage_gate`: `partial_not_promotion_clean`
  - The source backs VASE/Drude-Lorentz material fitting, and no source text found here says Fig. 2b measured reflectance was used to fit the Fig. 2c/d epsilon tables. However, the same article contains the source simulated Fig. 2b curves, TMM calculations, and device design, so independence is only weak-within-dataset.
- `stack_model_gate`: `blocked`
  - A reproducible no-fit TMM adapter still needs a frozen silicon substrate optical-constant source and substrate/backside handling. Those are not specified by the exported Fig. 2 source tables.

## Source Evidence

- Article: https://www.nature.com/articles/s41467-023-41377-5
- Supplementary information: https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-023-41377-5/MediaObjects/41467_2023_41377_MOESM1_ESM.pdf
- Figshare API: https://api.figshare.com/v2/articles/23734116
- Figshare metadata: Fig. 2b has simulated and experimentally measured reflectance tables; Fig. 2c/d has TiN/AZO permittivity tables with thickness comments.

## Forbidden Next

- Do not use source-simulated Fig. 2b curves as a holdout measurement.
- Do not tune TiN/AZO epsilon, thickness, roughness, substrate constants, scale, or offsets to Fig. 2b residuals.
- Do not run or report a TMM residual until a frozen substrate/backside model contract is recorded.
- Do not promote Saha beyond weak-within-dataset holdout without a future predeclared residual and uncertainty policy.
