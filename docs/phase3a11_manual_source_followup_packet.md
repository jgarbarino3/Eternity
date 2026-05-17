# Phase 3A.11 Bounded Manual Source Follow-Up Packet

## Decision

- Status: `manual_review_packet_ready`
- Selected branch: `limited_manual_source_followup_first`
- Candidate count: `3`
- Stop after candidate count: `3`
- Can feed serious core: `False`
- Can promote calibrated evidence: `False`
- Claim-status ceiling before manual proof: `weak_within_dataset_holdout`

## Scope

- Search mode: `no_new_broad_search`

Allowed work:
- open or inspect only the listed source candidates
- record exact source-backed evidence lines or external screenshots if needed
- classify each candidate against the proof gates

Forbidden work:
- adding unregistered large binary source files to the repo
- assuming intensity is absolute reflectance without source proof
- tuning thresholds from run_f35a15cef565fb15
- promoting any existing run to calibrated_linear_evidence

## Proof Gates

- `exact_3l2_quartz_identity`
- `stack_30nm_tin_10nm_sio2_20nm_tin`
- `s_polarized_or_te_reflectance_channel`
- `sixty_degree_incidence`
- `absolute_reflectance_units_or_calibration_state`
- `export_or_source_lineage_to_d10nm_text_trace`

## Candidates

### phase3a11_candidate_1

- Review status: `pending_manual_review`
- SHA-256: `b14020a0b37291da7bb2e6f4729686bcca54a87b5d61d94346449d6495e09dfb`
- Path: `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-iHiV4KrT7ctHmyRx.zip::DoD SAFE-iHiV4KrT7ctHmyRx/20230524 - quartz - 10nm SiO2 - cap - pulsed 0-12Vdc - 0.01Hz - 50pct duty cycle.SEsnap`
- Inner iSE entries: 200230524 - Quartz -10nm SiO2 - Puck 4 - 16V pulsed zero offset - square wave - offset to 0 to 8V 0.01 mHz.iSE
- Current assessment: `absolute_reflectance_proof_found=False`, `exact_source_identity_proven=False`

Evidence snippets to inspect first:
- `'C:\CompleteEASE\StateFileOpen\200230524 - Quartz -10nm SiO2 - Puck 4 - 16V pulsed zero offset - square wave - offset to 0 to 8V 0.01 mHz.iSE'`
- `'20230524 - quartz - 10nm SiO2 - cap - pulsed 0-8Vdc - 0.01Hz - 50pct duty cycle'`
- `2100.0 15160.0`
- `'C:\CompleteEASE\StateFileOpen\200230524 - Quartz -10nm SiO2 - Puck 4 - 16V pulsed zero offset - square wave - offset to 0 to 8V 0.01 mHz.iSE'`
- `20230524 - quartz - 10nm SiO2 - cap - pulsed 0-8Vdc - 0.01Hz - 50pct duty cycle`
- `5.0 F 0.0 20.0 F '# Back Reflections' F F 0.0 0.0 100000.0 F 100.0`

Manual review questions:
- Does the source file explicitly identify the sample as 3L2/Quartz or the thesis d_10nm stack?
- Does it state or encode the layer order 30 nm TiN / 10 nm SiO2 / 20 nm TiN on quartz?
- Does it identify the channel as S-polarized/TE reflectance rather than generic intensity?
- Does it preserve the 60 degree incidence geometry used by thesis Figure 4.1?
- Does it prove the exported values are calibrated absolute reflectance or percent reflectance?
- Can the source lineage be tied to the existing d_10nm_initial or d_10nm_12V text trace?

### phase3a11_candidate_2

- Review status: `pending_manual_review`
- SHA-256: `f7a54e3f1c67005da251fa4538c50bae4d2f1b2e4a9c72246a7e1302162990c5`
- Path: `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-iHiV4KrT7ctHmyRx.zip::DoD SAFE-iHiV4KrT7ctHmyRx/20230524 - quartz - 10nm SiO2 - cap - pulsed 0-8Vdc - 0.01Hz - 50pct duty cycle.SEsnap`
- Inner iSE entries: 200230524 - Quartz -10nm SiO2 - Puck 4 - 8V pulsed zero offset - 0.05msec - square wave - offset to 0 to 8V 0.01Hz.iSE
- Current assessment: `absolute_reflectance_proof_found=False`, `exact_source_identity_proven=False`

Evidence snippets to inspect first:
- `'C:\CompleteEASE\StateFileOpen\200230524 - Quartz -10nm SiO2 - Puck 4 - 8V pulsed zero offset - 0.05msec - square wave - offset to 0 to 8V 0.01Hz.iSE'`
- `'20230524 - data collected with random freq - 8V - rand offset - bump probe - then 16V zero offset pulsed'`
- `'C:\CompleteEASE\StateFileOpen\200230524 - Quartz -10nm SiO2 - Puck 4 - 8V pulsed zero offset - 0.05msec - square wave - offset to 0 to 8V 0.01Hz.iSE'`
- `20230524 - data collected with random freq - 8V - rand offset - bump probe - then 16V zero offset pulsed`
- `5.0 F 0.0 20.0 F '# Back Reflections' F F 0.0 0.0 100000.0 F 100.0`
- `100.0 F 0.0 100.0 F '% 1st Reflection' F F 0.0 0.0 100000.0 F 100.0`

Manual review questions:
- Does the source file explicitly identify the sample as 3L2/Quartz or the thesis d_10nm stack?
- Does it state or encode the layer order 30 nm TiN / 10 nm SiO2 / 20 nm TiN on quartz?
- Does it identify the channel as S-polarized/TE reflectance rather than generic intensity?
- Does it preserve the 60 degree incidence geometry used by thesis Figure 4.1?
- Does it prove the exported values are calibrated absolute reflectance or percent reflectance?
- Can the source lineage be tied to the existing d_10nm_initial or d_10nm_12V text trace?

### phase3a11_candidate_3

- Review status: `pending_manual_review`
- SHA-256: `2c63ad6f9d86290249818ef41c9ff6e3ef20ab53e6911fbf495c962a6a6b751d`
- Path: `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-iHiV4KrT7ctHmyRx.zip::DoD SAFE-iHiV4KrT7ctHmyRx/20230525 - probes removed - 890 nm peaks still present.SEsnap`
- Inner iSE entries: 20230524 - Puck 4 - check of reflectivity at 890 nm -- is it from probes - data while removing probes.iSE
- Current assessment: `absolute_reflectance_proof_found=False`, `exact_source_identity_proven=False`

Evidence snippets to inspect first:
- `'C:\CompleteEASE\StateFileOpen\20230524 - Puck 4 - check of reflectivity at 890 nm -- is it from probes - data while removing probes.iSE'`
- `'20230524 - quartz - 10nm SiO2 - cap - pulsed 0-12Vdc - 0.01Hz - 50pct duty cycle'`
- `'C:\CompleteEASE\StateFileOpen\20230524 - Puck 4 - check of reflectivity at 890 nm -- is it from probes - data while removing probes.iSE'`
- `20230524 - quartz - 10nm SiO2 - cap - pulsed 0-12Vdc - 0.01Hz - 50pct duty cycle`
- `5.0 F 0.0 20.0 F '# Back Reflections' F F 0.0 0.0 100000.0 F 100.0`
- `100.0 F 0.0 100.0 F '% 1st Reflection' F F 0.0 0.0 100000.0 F 100.0`

Manual review questions:
- Does the source file explicitly identify the sample as 3L2/Quartz or the thesis d_10nm stack?
- Does it state or encode the layer order 30 nm TiN / 10 nm SiO2 / 20 nm TiN on quartz?
- Does it identify the channel as S-polarized/TE reflectance rather than generic intensity?
- Does it preserve the 60 degree incidence geometry used by thesis Figure 4.1?
- Does it prove the exported values are calibrated absolute reflectance or percent reflectance?
- Can the source lineage be tied to the existing d_10nm_initial or d_10nm_12V text trace?

## Outcome Rules

- All gates pass: prepare a future Phase 3A.12 absolute-reflectance policy packet; do not retroactively promote existing inspected residuals
- Any gate unresolved: keep Phase 3A relative-only and use Phase 3A.6 clean export/new measurement packet or return to Phase 3B evidence gathering
- All candidates unresolved: mark manual source follow-up exhausted

Recommended manual log fields: `reviewer`, `review_date`, `candidate_id`, `tool_used`, `evidence_location`, `evidence_quote_or_note`, `passed_gates`, `failed_or_unresolved_gates`, `decision`.
