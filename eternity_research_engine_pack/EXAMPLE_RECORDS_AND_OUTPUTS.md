# Example Records and Outputs

These examples show the kind of outputs the Eternity research engine should produce.

## Example 1 — Method transfer radar

```yaml
schema_version: "0.1"
record_type: method_transfer
record_id: rm_method_transfer_example
source_type: peer_reviewed_paper
evidence_state: lead
review_state: needs_human_review
title: Ptychographic temporal reconstruction as a possible FROG robustness check
summary: A ptychography-inspired redundancy idea may help test FROG retrieval robustness for broadband ENZ-centered pulses.
project_areas: [tin_frog, pulse_retrieval]
tags: [ptychography, frog, phase_retrieval, ultrafast]
method_name: Ptychographic temporal reconstruction
original_field: Attosecond / ultrafast pulse metrology
transfer_target: FROG retrieval robustness under ENZ-like higher-order phase distortions
why_it_might_help:
  - Adds an independent reconstruction philosophy for pulse retrieval.
  - Could stress-test standard SHG-FROG assumptions in synthetic cases.
  - May reveal failure modes when spectral phase is rapidly varying near ENZ.
first_synthetic_test: Implement a toy ptychographic-style iterative retrieval and compare against a standard synthetic SHG-FROG trace for known ENZ-like spectral phase.
lab_feasibility: No new hardware for first synthetic test; later requires careful comparison to existing FROG data.
required_inputs:
  - synthetic broadband pulse
  - known higher-order phase
  - simulated SHG-FROG trace
  - optional thin-film phase response
risks_or_misfits:
  - May not map cleanly to the actual FROG geometry.
  - Could become a distraction if not benchmarked against simple baselines.
suggested_codex_task: Build a synthetic-only notebook/module comparing FROG-style and ptychography-inspired reconstruction on ENZ-distorted pulses.
warnings:
  - lead_only
  - synthetic_first
  - no_lab_pipeline_changes
```

## Example 2 — Lab failure-mode memory

```yaml
schema_version: "0.1"
record_type: failure_mode
record_id: rm_failure_mode_example
source_type: lab_note
evidence_state: lab_observed
review_state: needs_human_review
title: TiN/FROG temporal reshaping not fully explained by scalar GDD-only model
summary: Some TiN/FROG observations appear inconsistent with a simple scalar quadratic-dispersion explanation.
project_areas: [tin_frog]
tags: [tin, frog, gdd, temporal_phase, satellite_suppression]
symptom: FROG retrieval after TiN reflection shows changed temporal structure and possible satellite/sidelobe changes.
known_observations:
  - No-sample and TiN-reflected retrieved pulses can differ substantially.
  - Scalar GDD-only replacement can be partial in some cases but insufficient in others.
  - The effect may involve temporal phase changes, not only intensity broadening.
likely_causes:
  - higher-order spectral phase from thin-film reflection
  - ENZ-related dispersive phase structure
  - spectral filtering or alignment artifact
  - FROG retrieval ambiguity/noise
  - possible nonlinear response, not isolated yet
ruled_out_or_weakened:
  - simple uniform broadening as the full explanation
  - scalar GDD-only as a universal explanation
diagnostic_tests:
  - matched no-sample / TiN reflection / neutral mirror control
  - multiple pulse energies with fixed retrieval settings
  - compare with thin-film transfer-matrix phase model
  - repeat with transmission geometry if available
related_runs_or_samples:
  - B7 Run1 as scalar-GDD insufficiency example
  - C20 Run2 as possible partial GDD-success example
advisor_safe_wording: TiN modifies the retrieved temporal structure; in several cases the modification is not well described by uniform broadening or scalar GDD alone.
warnings:
  - retrieval_artifact_possible
  - alignment_artifact_possible
  - nonlinear_not_isolated
```

## Example 3 — Hypothesis queue item

```yaml
schema_version: "0.1"
record_type: hypothesis
record_id: rm_hypothesis_H014_example
source_type: lab_note
evidence_state: validation_candidate
review_state: needs_human_review
title: H-014 TiN ENZ reflection phase may suppress temporal satellites
summary: TiN ENZ reflection may impose wavelength-dependent phase that changes few-cycle pulse temporal structure.
project_areas: [tin_frog]
tags: [tin, enz, frog, phase, thin_film]
hypothesis_id: H-014
hypothesis_statement: TiN ENZ reflection imposes a wavelength-dependent phase response that can suppress or reshape temporal satellites in broadband few-cycle pulses.
why_plausible:
  - ENZ thin-film reflection phase can vary rapidly near resonance.
  - FROG retrievals show temporal structure changes after TiN reflection.
  - Scalar GDD-only replacement is insufficient in at least some runs.
what_would_support_it:
  - reproducible phase reshaping across multiple matched runs
  - agreement with a thin-film transfer-matrix phase model using measured or calibrated epsilon
  - similar low-intensity effect consistent with linear dispersion
what_would_weaken_it:
  - same reshaping appears from a neutral mirror control
  - effect disappears after alignment/spectral support correction
  - retrieval changes strongly under alternate FROG constraints
next_simulation: Simulate broadband pulse reflection from TiN using measured/fit epsilon and compare temporal intensity/phase before and after reflection.
next_lab_test: Matched no-sample/TiN/neutral-mirror FROG at two or more pulse energies.
current_confidence: low
validation_status: untested
warnings:
  - possible_retrieval_artifact
  - possible_alignment_artifact
  - nonlinear_not_isolated
```

## Example 4 — Adversarial reviewer output

```markdown
# Adversarial review — TiN/FROG higher-order phase interpretation

## Candidate claim
TiN causes higher-order phase reshaping rather than simple pulse broadening.

## Supporting observations
- Scalar GDD replacement is insufficient in at least one noted run.
- Retrieved temporal phase changes are not obviously captured by uniform broadening.
- Satellite/sidelobe behavior may indicate phase-sensitive reshaping.

## Weak points
- FROG retrieval ambiguity/noise may exaggerate phase structure.
- No clean intensity-dependent separation yet.
- Reflection geometry may include spectral filtering or alignment artifacts.
- Neutral mirror control is needed.
- Thin-film phase model has not yet been calibrated against independent optical data.

## Best falsification test
Matched no-sample / neutral mirror / TiN reflection FROG at multiple pulse energies using the same spectral support and retrieval settings.

## Safer wording
The observations are consistent with phase-sensitive temporal reshaping after TiN reflection, but current evidence does not isolate whether the origin is linear thin-film dispersion, nonlinear response, alignment/spectral filtering, or retrieval artifact.
```

## Example 5 — Codex task draft

```markdown
# Codex Task — Synthetic thin-film phase test for TiN/FROG reshaping

## Goal
Implement a synthetic-only test of whether a plausible thin-film spectral phase response can reshape a broadband pulse without invoking nonlinear response.

## Context
Eternity has observed TiN/FROG temporal-structure changes. Some runs are not well reproduced by a scalar GDD-only model. Before using lab time or stronger language, test whether a linear thin-film phase response can plausibly create similar qualitative reshaping.

## Source records
- rm_failure_mode_example
- rm_hypothesis_H014_example

## Inputs
- synthetic broadband Gaussian or measured-like spectrum
- configurable spectral phase terms
- thin-film transfer-matrix reflection phase from a simple material model
- optional scalar GDD-only comparison

## Expected outputs
- plot: input spectrum and phase
- plot: reflected spectrum and phase
- plot: temporal intensity/phase before and after
- plot: scalar-GDD-only comparison
- Markdown report with assumptions, warnings, and validity envelope

## Success criteria
- deterministic run artifacts
- clear comparison between scalar GDD-only and wavelength-dependent thin-film phase
- no lab acquisition code touched
- no claim of validation

## Do not
- Do not claim TiN nonlinearity is proven.
- Do not fit to holdout data.
- Do not touch real lab data paths unless explicitly provided.
- Do not replace existing V0 commands.
```

## Example 6 — Weekly home-screen digest

```markdown
# Eternity Research Home — 2026-05-08

## 1. Must-read / must-review
1. Paper/action card on ENZ thin-film phase response near 545 nm — high simulation relevance, needs parameter extraction.
2. Instrument note on BBO bandwidth acceptance — relevant to FROG spectral support.

## 2. Possible experiment ideas
1. Matched no-sample / neutral mirror / TiN reflection FROG at two energies.
2. Transmission-control FROG if alignment and signal permit.

## 3. Possible Codex tasks
1. Synthetic thin-film phase reshaping test.
2. Scalar GDD versus higher-order phase comparison report.
3. Failure-atlas search command for Z-scan asymmetry.

## 4. Contradictions / weak claims
1. Avoid saying “TiN broadens the pulse” as the whole explanation. Safer: “TiN modifies temporal structure; scalar GDD alone is insufficient in some cases.”
2. Avoid saying “ENZ nonlinearity is isolated” until energy dependence and controls exist.

## 5. Surprising connections
1. Ptychographic redundancy may inspire a FROG retrieval robustness stress test.
2. Bayesian calibration may help Z-scan parameter extraction and uncertainty reporting.
```
