# Phase 3A.10 Branch Decision

## Decision

- Selected branch: `limited_manual_source_followup_first`
- Can feed serious core: `False`
- Can promote calibrated evidence: `False`
- Normalization basis: `relative_intensity_only`
- Claim-status ceiling: `weak_within_dataset_holdout`
- Pro checkpoint before thresholds: `True`

## Manual Source Follow-Up

- Status: `bounded_followup_recommended`
- Candidate count: `3`
- Stop after: the listed top-three candidates unless the user adds new evidence
- Success condition: Find source-backed channel name, units, calibration state, angle, polarization, and exact 3L2/Quartz identity.
- Failure action: Keep Phase 3A relative-only and use Phase 3A.6 clean export/new measurement packet or return to Phase 3B.

| Priority | Score | SHA-256 | Path |
| ---: | ---: | --- | --- |
| 86 | 40 | `b14020a0b37291da7bb2e6f4729686bcca54a87b5d61d94346449d6495e09dfb` | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-iHiV4KrT7ctHmyRx.zip::DoD SAFE-iHiV4KrT7ctHmyRx/20230524 - quartz - 10nm SiO2 - cap - pulsed 0-12Vdc - 0.01Hz - 50pct duty cycle.SEsnap` |
| 86 | 40 | `f7a54e3f1c67005da251fa4538c50bae4d2f1b2e4a9c72246a7e1302162990c5` | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-iHiV4KrT7ctHmyRx.zip::DoD SAFE-iHiV4KrT7ctHmyRx/20230524 - quartz - 10nm SiO2 - cap - pulsed 0-8Vdc - 0.01Hz - 50pct duty cycle.SEsnap` |
| 86 | 40 | `2c63ad6f9d86290249818ef41c9ff6e3ef20ab53e6911fbf495c962a6a6b751d` | `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-iHiV4KrT7ctHmyRx.zip::DoD SAFE-iHiV4KrT7ctHmyRx/20230525 - probes removed - 890 nm peaks still present.SEsnap` |

## Phase 3B Return

- Status: `parked_not_calibrated`
- TiON optical constants registered: `tion_48_0p8pa_epsilon`, `tion_49_1p0pa_epsilon`
- TiON raw R/T measurements registered: `none`
- Ready for calibrated evidence: `False`

First actions:
- Keep TiON_48/TiON_49 as optical-constants-only material models.
- Register raw sample-matched R/T if it appears.
- If using grower plots, digitize them explicitly as plot-derived evidence.
- Do not use TiON optical constants alone as calibrated evidence.

## Branch Order

1. bounded manual source follow-up on the top quartz dynamic candidates
2. Phase 3A.6 clean export or new measurement if absolute reflectance is required
3. Phase 3B TiON evidence gathering if no Phase 3A source proof appears

Forbidden uses: `serious_core_evidence`, `calibrated_linear_evidence`, `absolute_reflectance_claim`, `retroactive_threshold_tuning`.
