# Phase 3A.12 Manual Source Review Result

## Decision

- Status: `manual_source_followup_exhausted`
- Source proof found: `False`
- Can feed serious core: `False`
- Can promote calibrated evidence: `False`
- Normalization basis: `relative_intensity_only`
- Claim-status ceiling: `weak_within_dataset_holdout`
- Continue Phase 3A manual source follow-up: `False`
- Recommended next phase: `Phase 3B - TiON evidence gathering or Phase 3A.6 clean export`

## Bottom Line

The three bounded source candidates strengthen related provenance but do not prove exact 3L2/Quartz source identity, the 30/10/20 stack, absolute reflectance calibration, or lineage to the d_10nm text trace.

## Candidate Results

### phase3a11_candidate_1

- Decision: `related_but_not_source_identity`
- SHA-256: `b14020a0b37291da7bb2e6f4729686bcca54a87b5d61d94346449d6495e09dfb`
- Path: `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-iHiV4KrT7ctHmyRx.zip::DoD SAFE-iHiV4KrT7ctHmyRx/20230524 - quartz - 10nm SiO2 - cap - pulsed 0-12Vdc - 0.01Hz - 50pct duty cycle.SEsnap`
- Passed gates: `sixty_degree_incidence`
- Failed or unresolved gates: `absolute_reflectance_units_or_calibration_state`, `exact_3l2_quartz_identity`, `export_or_source_lineage_to_d10nm_text_trace`, `s_polarized_or_te_reflectance_channel`, `stack_30nm_tin_10nm_sio2_20nm_tin`

Positive evidence:
- FitLog line 4 references C:\CompleteEASE\StateFileOpen\200230524 - Quartz -10nm SiO2 - Puck 4 - 16V pulsed zero offset - square wave - offset to 0 to 8V 0.01 mHz.iSE
- FitLog line 31 labels the model snapshot as 20230524 - quartz - 10nm SiO2 - cap - pulsed 0-8Vdc - 0.01Hz - 50pct duty cycle
- FitLog line 155 states Standard Ellipsometric
- FitLog line 216 records 60.0 degrees

Negative evidence:
- No FitLog hits for 3L2, d_10, 30_20_10, 30 nm, 30nm, absolute reflect, %R, % R, calibrated reflect, s-polar, or TE reflect.
- The readable source metadata does not prove exact 3L2/Quartz identity, the 30/10/20 stack, absolute reflectance units, or lineage to d_10nm text exports.

### phase3a11_candidate_2

- Decision: `related_but_not_source_identity`
- SHA-256: `f7a54e3f1c67005da251fa4538c50bae4d2f1b2e4a9c72246a7e1302162990c5`
- Path: `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-iHiV4KrT7ctHmyRx.zip::DoD SAFE-iHiV4KrT7ctHmyRx/20230524 - quartz - 10nm SiO2 - cap - pulsed 0-8Vdc - 0.01Hz - 50pct duty cycle.SEsnap`
- Passed gates: `sixty_degree_incidence`
- Failed or unresolved gates: `absolute_reflectance_units_or_calibration_state`, `exact_3l2_quartz_identity`, `export_or_source_lineage_to_d10nm_text_trace`, `s_polarized_or_te_reflectance_channel`, `stack_30nm_tin_10nm_sio2_20nm_tin`

Positive evidence:
- FitLog line 4 references C:\CompleteEASE\StateFileOpen\200230524 - Quartz -10nm SiO2 - Puck 4 - 8V pulsed zero offset - 0.05msec - square wave - offset to 0 to 8V 0.01Hz.iSE
- FitLog line 31 labels the model snapshot as 20230524 - data collected with random freq - 8V - rand offset - bump probe - then 16V zero offset pulsed
- FitLog line 155 states Standard Ellipsometric
- FitLog line 216 records 60.0 degrees

Negative evidence:
- No FitLog hits for 3L2, d_10, 30_20_10, 30 nm, 30nm, absolute reflect, %R, % R, calibrated reflect, s-polar, or TE reflect.
- The readable source metadata does not prove exact 3L2/Quartz identity, the 30/10/20 stack, absolute reflectance units, or lineage to d_10nm text exports.

### phase3a11_candidate_3

- Decision: `related_but_not_source_identity`
- SHA-256: `2c63ad6f9d86290249818ef41c9ff6e3ef20ab53e6911fbf495c962a6a6b751d`
- Path: `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-iHiV4KrT7ctHmyRx.zip::DoD SAFE-iHiV4KrT7ctHmyRx/20230525 - probes removed - 890 nm peaks still present.SEsnap`
- Passed gates: `sixty_degree_incidence`
- Failed or unresolved gates: `absolute_reflectance_units_or_calibration_state`, `exact_3l2_quartz_identity`, `export_or_source_lineage_to_d10nm_text_trace`, `s_polarized_or_te_reflectance_channel`, `stack_30nm_tin_10nm_sio2_20nm_tin`

Positive evidence:
- FitLog line 4 references C:\CompleteEASE\StateFileOpen\20230524 - Puck 4 - check of reflectivity at 890 nm -- is it from probes - data while removing probes.iSE
- FitLog line 31 labels the model snapshot as 20230524 - quartz - 10nm SiO2 - cap - pulsed 0-12Vdc - 0.01Hz - 50pct duty cycle
- FitLog line 155 states Standard Ellipsometric
- FitLog line 216 records 60.0 degrees

Negative evidence:
- No FitLog hits for 3L2, d_10, 30_20_10, 30 nm, 30nm, absolute reflect, %R, % R, calibrated reflect, s-polar, or TE reflect.
- The readable source metadata does not prove exact 3L2/Quartz identity, the 30/10/20 stack, absolute reflectance units, or lineage to d_10nm text exports.

## Allowed Next Actions

- Use Phase 3A.6 to request a clean CompleteEASE export or new measurement.
- Return to Phase 3B only if raw sample-matched TiON R/T appears.
- Use TiON plots only if explicitly digitized as plot-derived evidence.
- Keep Phase 3A relative-only until source-backed absolute data exists.

## Forbidden Next Actions

- continue open-ended Phase 3A source searching without new user-supplied evidence
- treat thesis Intensity columns as absolute reflectance
- promote run_f35a15cef565fb15
- feed Phase 3A relative-only diagnostics into the serious core
