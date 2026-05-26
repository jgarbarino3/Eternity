# Phase 3F - Simulator-Validation Fallback On Simpler Public Thin-Film Data

Date: 2026-05-25

## Purpose

Validate the local linear TMM machinery on a deliberately simpler public
planar thin-film dataset before another ENZ evidence attempt.

This phase is not an ENZ claim phase. It is a simulator-validation fallback:
use a boring, source-backed optical stack to test whether the code, reporting,
registry, and no-fit comparison workflow behave correctly when the scientific
contract is easier than the current ENZ packages.

## Trigger

Phase 3E.5 showed that Saha can support a no-claim sensitivity fixture, but not
a frozen no-fit validation candidate. The missing Saha pieces remain:

- source-backed silicon optical constants;
- substrate thickness, backside, wedge, and coherence treatment;
- interface roughness or native-oxide assumptions;
- a clean calibration-vs-holdout split;
- proof that the measured Fig. 2b curve was not effectively used to tune the
  source simulation or model.

## Candidate Acceptance Gate

A Phase 3F candidate should have:

- machine-readable optical constants, `n,k`, or epsilon;
- measured reflectance, transmittance, or ellipsometry in machine-readable
  form;
- explicit wavelength axis, units, angle, polarization, and normalization;
- explicit stack order and layer thicknesses;
- source-backed substrate material and backside/coherence treatment, or a
  geometry where backside effects are provably irrelevant;
- no need to fit, tune, or choose model variants from the measured holdout;
- source-page and file hashes recorded before residual inspection.

## Stop Rules

Stop before residual modeling if any of these are missing:

- measured-data normalization;
- geometry;
- stack details;
- substrate/backside/coherence treatment;
- leakage-safe split between material model construction and holdout data.

## Allowed Output

Phase 3F may produce:

- an intake card;
- canonical CSV artifacts;
- a frozen no-fit TMM adapter;
- a predeclared residual policy;
- a simulator-validation report.

It may not produce:

- ENZ calibrated evidence;
- a promoted material claim;
- a residual-tuned model;
- a Phase 4 candidate unless a future ENZ dataset independently clears the
  calibrated-linear evidence gate.

## Suggested Effort And Tools

- Planning: GPT-5.5 `high`.
- Implementation: `medium` for intake/report work, `high` if a candidate clears
  the full contract and needs a frozen adapter.
- Tools: Browse.sh or Plasmate for read-only source scouting, local hashing and
  table inspection for artifacts, GPD only for claim-boundary review.

## Phase 3F.1 Result

The first bounded scout pass is recorded in
`docs/phase3f1_simulator_validation_scout.md` and
`docs/phase3f_simulator_validation_candidate_registry.yaml`.

Result: 10 public simple/thin-film-adjacent leads were gated, 0 cleared every
hard flag, no Phase 3F.2 intake opened, no TMM adapter started, and no residual
modeling was run. Phase 3F remains open under the same stop rules.

## Phase 3F.1B Result

The pasted GPT-5.5 Pro lead list is recorded in
`docs/phase3f1b_pro_lead_candidate_registry.yaml`, with generated reports at
`docs/phase3f1b_pro_lead_gate.md` and
`docs/phase3f1b_pro_lead_gate.json`.

Result: 16 candidate cards were gated, 0 cleared every hard flag, no Phase
3F.2 intake opened, no TMM adapter started, and no residual modeling was run.
The best non-ENZ simulator fallbacks are useful future source-file audit
targets, but they are not intake-ready validation candidates yet.

## Phase 3F.1C Result

The top-three source-file audit is recorded in
`docs/phase3f1c_source_file_audit.md` and
`docs/phase3f1c_source_file_audit.json`.

Result: the three best practical fallback packages from Phase 3F.1B were
downloaded, hash-verified, and inspected. `structural_color_froc_2023` is
blocked because its Source Data workbook is chromaticity/comparison coordinate
data rather than measured spectral R/T holdout, and its optimization output is
not present in the public archive. `fano_ultrathin_coatings_froc_2021` is
blocked because measured figure data are Origin OPJ containers rather than open
machine-readable tables. `ultrathin_gold_absorber_2020` has rich raw FTIR R/T
tables, but is blocked because material constants/model parameters are fitted
from the same optical measurements and the processing code is request-only.

No candidate cleared every hard flag, no Phase 3F.2 intake opened, no TMM
adapter started, and no residual modeling was run.
