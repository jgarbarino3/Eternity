# Phase 3A.8 Source Candidate Triage

## Decision

- Final decision: `pivot_to_relative_only_diagnostic`
- Normalization basis: `relative_intensity_only`
- Absolute reflectance status: `absolute_reflectance_blocked`
- Can feed serious core: `False`
- Can promote calibrated evidence: `False`
- Claim-status ceiling: `weak_within_dataset_holdout`
- Historical run promotion: `forbidden`

## Relative-Only Lane

Allowed diagnostics: `spectral_shape`, `dip_position`, `trend_direction`, `figure_provenance`.

Forbidden uses: `serious_core_evidence`, `calibrated_linear_evidence`, `absolute_reflectance_claim`, `retroactive_threshold_tuning`.

## Candidate Buckets

### `manual_followup_priority`

| Priority | Score | SHA-256 | Rationale | Path |
| ---: | ---: | --- | --- | --- |
| 86 | 40 | `b14020a0b37291da7bb2e6f4729686bcca54a87b5d61d94346449d6495e09dfb` | matches quartz plus 10 nm/dynamic-source clues but not exact thesis identity | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-iHiV4KrT7ctHmyRx.zip::DoD SAFE-iHiV4KrT7ctHmyRx/20230524 - quartz - 10nm SiO2 - cap - pulsed 0-12Vdc - 0.01Hz - 50pct duty cycle.SEsnap` |
| 86 | 40 | `f7a54e3f1c67005da251fa4538c50bae4d2f1b2e4a9c72246a7e1302162990c5` | matches quartz plus 10 nm/dynamic-source clues but not exact thesis identity | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-iHiV4KrT7ctHmyRx.zip::DoD SAFE-iHiV4KrT7ctHmyRx/20230524 - quartz - 10nm SiO2 - cap - pulsed 0-8Vdc - 0.01Hz - 50pct duty cycle.SEsnap` |
| 86 | 40 | `2c63ad6f9d86290249818ef41c9ff6e3ef20ab53e6911fbf495c962a6a6b751d` | matches quartz plus 10 nm/dynamic-source clues but not exact thesis identity | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-iHiV4KrT7ctHmyRx.zip::DoD SAFE-iHiV4KrT7ctHmyRx/20230525 - probes removed - 890 nm peaks still present.SEsnap` |

### `related_but_not_source_identity`

| Priority | Score | SHA-256 | Rationale | Path |
| ---: | ---: | --- | --- | --- |
| 42 | 50 | `9c691779fd7235ec61ac545858e8258a55498a14497c1869ebb4bc4feb744212` | related CompleteEASE/Woollam cap-test provenance without exact thesis identity | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-YuRhUUwxjvv8Zoh6.zip::DoD SAFE-YuRhUUwxjvv8Zoh6/20230519 - Puck 4 complete  - goal 75nm TiN - 30 nm SiO2 - 53nm TiN on quartz for 3 layer cap test.SEsnap` |
| 42 | 46 | `3030a8650f9d8335f0a333857af85fbeca1ed9cbcf3db0fccab82962c0d975b2` | related CompleteEASE/Woollam cap-test provenance without exact thesis identity | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-YuRhUUwxjvv8Zoh6.zip::DoD SAFE-YuRhUUwxjvv8Zoh6/20230518 - Puck 4 complete - 20 nm SiO2 - 53nm TiN on quartz for 3 layer cap test.SEsnap` |
| 42 | 32 | `28da57b88b2e00b140aa64607424573c5003d4fee3fddf782336833f2143e963` | related CompleteEASE/Woollam cap-test provenance without exact thesis identity | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-GutD3WAH22Yxo9tX 2/20230517 - completed TiN RT growth - 50.3 nm actually on quartz..SEsnap` |
| 42 | 32 | `aecc47b1a55737d5c46886077ddc740d705c1667e80688e7ccc1631962929dd0` | related CompleteEASE/Woollam cap-test provenance without exact thesis identity | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-GutD3WAH22Yxo9tX 2/20230517 - quartz TiN growth - quartz modeled.SEsnap` |

### `wrong_substrate_or_control`

| Priority | Score | SHA-256 | Rationale | Path |
| ---: | ---: | --- | --- | --- |
| 38 | 46 | `f404042b9114cca6bf6521cf42589270ca384d4e7109af73b0af079434e4bf39` | file/member path names Si control/substrate context rather than 3L2/Quartz | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-aCyVf5zQGhuzpg6f/RC-2.zip::20230523 - Puck 1 - ellipsometry - 10nm SiO2 -3 layer cap - Si 100 RT.SEsnap` |
| 8 | 44 | `d28816d4984f1a1ca93c7edbe07d2b4684c9b056245e453d2c46c3f8d35ae884` | file/member path names Si control/substrate context rather than 3L2/Quartz | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-aCyVf5zQGhuzpg6f/RC-2.zip::20230519 - 3 layer cap - goal on masked 50nm TiN area - was 10nm SiO2 cap - Si 100 N type 2 in-reflection intensity.SEsnap` |
| 8 | 40 | `a87b27fa26619e9facc8e9b15608c3f9b4df1d4a8a9c68c4458508e5bbd45383` | file/member path names Si control/substrate context rather than 3L2/Quartz | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-YuRhUUwxjvv8Zoh6.zip::DoD SAFE-YuRhUUwxjvv8Zoh6/20230519 - Puck 2 complete  - goal 100nm TiN - 20 nm SiO2 - 53nm TiN on Si 100 for 3 layer cap test.SEsnap` |
| 8 | 40 | `d596ac024e2ec0bfa3a3357e1934b9c5999e6a045dac6bb82cc0491a457a3e24` | file/member path names Si control/substrate context rather than 3L2/Quartz | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-aCyVf5zQGhuzpg6f/RC-2.zip::20230519 - 3 layer cap - goal on entire stack of 10nm SiO2 cap - Si 100 N type 2 in-reflection intensity.SEsnap` |
| 8 | 40 | `1050fabc15ddde982530839c7f49696677df88332c65bae70dafb944599bf0df` | file/member path names Si control/substrate context rather than 3L2/Quartz | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-aCyVf5zQGhuzpg6f/RC-2.zip::20230523 - Puck 2 - ellipsometry - 20nm SiO2 -3 layer cap - Si 100 RT.SEsnap` |
| 8 | 36 | `6fa2aff53603014f297af80fabcdb1036ed8580e66a327b809ce5df498b62e81` | file/member path names Si control/substrate context rather than 3L2/Quartz | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-YuRhUUwxjvv8Zoh6.zip::DoD SAFE-YuRhUUwxjvv8Zoh6/20230518 - Puck 1 complete - 11 nm SiO2 - 53nm TiN on Si 100 for 3 layer cap test.SEsnap` |
| 8 | 36 | `5b55a3f218538170411d7529666a2e7a2ac00fc55890ef9b31e0ad6b0588a4db` | file/member path names Si control/substrate context rather than 3L2/Quartz | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-YuRhUUwxjvv8Zoh6.zip::DoD SAFE-YuRhUUwxjvv8Zoh6/20230518 - Puck 2 complete - 21 nm SiO2 - 56nm TiN on Si 100 for 3 layer cap test.SEsnap` |
| 8 | 36 | `ee3aa9f20795609c2f80807a6d3187c13589c88116dc2721985792d8b71566d3` | file/member path names Si control/substrate context rather than 3L2/Quartz | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-YuRhUUwxjvv8Zoh6.zip::DoD SAFE-YuRhUUwxjvv8Zoh6/20230519 - Puck 1 complete  - goal 100nm TiN - 11 nm SiO2 - 53nm TiN on Si 100 for 3 layer cap test.SEsnap` |

### `not_decisive_for_absolute_reflectance`

No candidates.

## Consequence

Phase 3A.8 keeps the strongest source candidates visible for manual
follow-up, but it does not treat any candidate as exact `3L2/Quartz`
source identity or calibrated absolute `%R` proof.

`run_f35a15cef565fb15` remains historical and non-promotable. Future
work may use the thesis traces for relative-only diagnostics, or use
the Phase 3A.6 packet for a clean export/new measurement.
