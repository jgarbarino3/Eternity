# Phase 3A.7 CompleteEASE Source Recovery

## Decision

- Source recovery status: `related_source_candidates_found`
- Exact source identity status: `not_found`
- Stack mapping: `stack_mapping_confirmed`
- Normalization basis: `relative_intensity_only`
- Absolute reflectance status: `absolute_reflectance_blocked`
- Can promote calibrated evidence: `False`
- Claim-status ceiling: `weak_within_dataset_holdout`

## Thesis-Backed Mapping

- Sample: `3L2/Quartz`
- Stack: 30 nm TiN / 10 nm SiO2 / 20 nm TiN on quartz
- Measurement: S-polarized RC2 in-situ reflectance/reflective intensity at 60 degrees
- Figure: Thesis Figure 4.1
- Boundary: Thesis text supports reflective-intensity/reflectance provenance, but not absolute calibrated %R for the exported Intensity columns.

## Supporting Files

| Role | Path | SHA-256 |
| --- | --- | --- |
| thesis_final_pdf | `/Users/joegarbarino/Desktop/Research Optics/Thesis/Checkpoints/Thesis Final Draft v13 May 17 committee.pdf` | `356a59062019805feb6c83471f20ff424f6d080b627603b01fda889dc572882f` |
| d_10nm_initial_export | `/Users/joegarbarino/Desktop/Research Optics/Thesis/Data/d_10nm_initial.txt` | `c093c27d277841140f7655da72372e9ffc90b2abf030c5e358cd0c01d2b3bc21` |
| d_10nm_12v_export | `/Users/joegarbarino/Desktop/Research Optics/Thesis/Data/d_10nm_12V.txt` | `0b4890786cbebe76d723447592ed67549a826e563a8d4a4c4970d33919be4819` |
| phase3a_30_20_10_p_s_intensity | `/Users/joegarbarino/Desktop/Research Optics/Coding/txt/30_20_10 p_s intensity.txt` | `c47f552a0b166775ecfb1bfe700e3911738f43056e17b53bb91508cd94a665d7` |
| phase3a_30_20_10_reflectance | `/Users/joegarbarino/Desktop/Research Optics/Coding/txt/30_20_10 reflectance.txt` | `f708bf4abd2efe49a131f423aabcccd4f669d0a16a9a9d16de44ead3100bb9a8` |

## Top CompleteEASE/Woollam Candidates

| Score | Reasons | Path |
| ---: | --- | --- |
| 50 | mentions_quartz, mentions_completeease, mentions_s_polarized_or_te, mentions_three_layer, mentions_tin, mentions_sio2, mentions_30nm, mentions_20nm | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-YuRhUUwxjvv8Zoh6.zip::DoD SAFE-YuRhUUwxjvv8Zoh6/20230519 - Puck 4 complete  - goal 75nm TiN - 30 nm SiO2 - 53nm TiN on quartz for 3 layer cap test.SEsnap` |
| 50 | mentions_quartz, mentions_completeease, mentions_s_polarized_or_te, mentions_three_layer, mentions_tin, mentions_sio2, mentions_30nm, mentions_20nm | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-YuRhUUwxjvv8Zoh6/20230519 - Puck 4 complete  - goal 75nm TiN - 30 nm SiO2 - 53nm TiN on quartz for 3 layer cap test.SEsnap` |
| 46 | mentions_quartz, mentions_completeease, mentions_s_polarized_or_te, mentions_three_layer, mentions_tin, mentions_sio2, mentions_20nm | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-YuRhUUwxjvv8Zoh6.zip::DoD SAFE-YuRhUUwxjvv8Zoh6/20230518 - Puck 4 complete - 20 nm SiO2 - 53nm TiN on quartz for 3 layer cap test.SEsnap` |
| 46 | mentions_quartz, mentions_completeease, mentions_s_polarized_or_te, mentions_three_layer, mentions_tin, mentions_sio2, mentions_20nm | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-YuRhUUwxjvv8Zoh6/20230518 - Puck 4 complete - 20 nm SiO2 - 53nm TiN on quartz for 3 layer cap test.SEsnap` |
| 46 | mentions_quartz, mentions_completeease, mentions_s_polarized_or_te, mentions_three_layer, mentions_tin, mentions_sio2, mentions_10nm_or_11nm | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-aCyVf5zQGhuzpg6f/RC-2.zip::20230523 - Puck 1 - ellipsometry - 10nm SiO2 -3 layer cap - Si 100 RT.SEsnap` |
| 44 | mentions_completeease, mentions_intensity, mentions_s_polarized_or_te, mentions_three_layer, mentions_tin, mentions_sio2, mentions_10nm_or_11nm | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-aCyVf5zQGhuzpg6f/RC-2.zip::20230519 - 3 layer cap - goal on masked 50nm TiN area - was 10nm SiO2 cap - Si 100 N type 2 in-reflection intensity.SEsnap` |
| 40 | mentions_completeease, mentions_s_polarized_or_te, mentions_three_layer, mentions_tin, mentions_sio2, mentions_10nm_or_11nm, mentions_20nm | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-YuRhUUwxjvv8Zoh6.zip::DoD SAFE-YuRhUUwxjvv8Zoh6/20230519 - Puck 2 complete  - goal 100nm TiN - 20 nm SiO2 - 53nm TiN on Si 100 for 3 layer cap test.SEsnap` |
| 40 | mentions_completeease, mentions_s_polarized_or_te, mentions_three_layer, mentions_tin, mentions_sio2, mentions_30nm, mentions_20nm | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-YuRhUUwxjvv8Zoh6.zip::DoD SAFE-YuRhUUwxjvv8Zoh6/20230519 - Puck 3 complete  - goal 100nm TiN - 30 nm SiO2 - 53nm TiN on Si 100 for 3 layer cap test.SEsnap` |
| 40 | mentions_completeease, mentions_s_polarized_or_te, mentions_three_layer, mentions_tin, mentions_sio2, mentions_10nm_or_11nm, mentions_20nm | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-YuRhUUwxjvv8Zoh6/20230519 - Puck 2 complete  - goal 100nm TiN - 20 nm SiO2 - 53nm TiN on Si 100 for 3 layer cap test.SEsnap` |
| 40 | mentions_completeease, mentions_s_polarized_or_te, mentions_three_layer, mentions_tin, mentions_sio2, mentions_30nm, mentions_20nm | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-YuRhUUwxjvv8Zoh6/20230519 - Puck 3 complete  - goal 100nm TiN - 30 nm SiO2 - 53nm TiN on Si 100 for 3 layer cap test.SEsnap` |
| 40 | mentions_completeease, mentions_intensity, mentions_s_polarized_or_te, mentions_three_layer, mentions_sio2, mentions_10nm_or_11nm | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-aCyVf5zQGhuzpg6f/RC-2.zip::20230519 - 3 layer cap - goal on entire stack of 10nm SiO2 cap - Si 100 N type 2 in-reflection intensity.SEsnap` |
| 40 | mentions_completeease, mentions_s_polarized_or_te, mentions_three_layer, mentions_tin, mentions_sio2, mentions_10nm_or_11nm, mentions_20nm | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-aCyVf5zQGhuzpg6f/RC-2.zip::20230523 - Puck 2 - ellipsometry - 20nm SiO2 -3 layer cap - Si 100 RT.SEsnap` |
| 40 | mentions_completeease, mentions_intensity, mentions_s_polarized_or_te, mentions_three_layer, mentions_sio2, mentions_20nm | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-aCyVf5zQGhuzpg6f/RC-2.zip::20230523 - Puck 4 - reflected intensity - 20nm SiO2 -3 layer cap - Si 100 RT.SEsnap` |
| 40 | mentions_quartz, mentions_completeease, mentions_s_polarized_or_te, mentions_tin, mentions_sio2, mentions_10nm_or_11nm | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-iHiV4KrT7ctHmyRx.zip::DoD SAFE-iHiV4KrT7ctHmyRx/20230524 - quartz - 10nm SiO2 - cap - pulsed 0-12Vdc - 0.01Hz - 50pct duty cycle.SEsnap` |
| 40 | mentions_quartz, mentions_completeease, mentions_s_polarized_or_te, mentions_tin, mentions_sio2, mentions_10nm_or_11nm | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-iHiV4KrT7ctHmyRx.zip::DoD SAFE-iHiV4KrT7ctHmyRx/20230524 - quartz - 10nm SiO2 - cap - pulsed 0-8Vdc - 0.01Hz - 50pct duty cycle.SEsnap` |

## Consequence

Phase 3A.7 strengthens the `3L2/Quartz` stack and geometry provenance,
and it finds related local source candidates. It does not find an exact
`3L2`, `30_20_10`, or source-export identity record for the thesis
`d_10nm` traces.

It keeps absolute reflectance blocked. The exported `Intensity` columns
may remain useful for relative diagnostics and figure provenance; they
cannot feed `calibrated_linear_evidence` without source-backed
absolute-normalization evidence and future predeclared thresholds.
