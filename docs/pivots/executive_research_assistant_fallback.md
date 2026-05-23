# Pivot Plan - Executive Research Assistant Fallback

Date: 2026-05-19

## Trigger

Use this pivot if Phase 3D and the strongest public packages, starting with
Exeter/Bohn ITO and Saha TiN/AZO, fail the calibration/holdout split audit or
cannot support an honest calibrated-linear evidence attempt.

Do not treat that as project failure, and do not lower the
`calibrated_linear_evidence` bar.

## Current Status

Phase 3D.5 triggered this pivot for the current implementation run.

The known public leads are not all of literature, but the leads already in hand
are exhausted enough that no immediate Phase 4 attempt is honest:

- Exeter/Bohn ITO is useful but non-promoting after no-fit reconstruction.
- Saha TiN/AZO is source-data-public and now CSV-canonicalized, but
  stack-contract-blocked: Phase 3E.3B found no source-backed silicon constants,
  substrate/backside/coherence handling, or interface/oxide assumptions for a
  no-fit residual run.
- Exeter spatiotemporal ITO is public and open-format, but nonlinear.
- Thermo-optic ITO is public and constants-rich, but has no independent
  measured static R/T holdout.
- Phase 3D.5A corrected the ACS/intracavity lead to public PDF/SI-only, with no
  raw tables or independent measured static R/T/A holdout.
- Remaining known leads are plots/PDF-only, constants-only, export-blocked, or
  request-only.

Reopen the calibrated-linear data hunt only with a new table-ready public
package that clears the stack-contract gate, a separate ACS/intracavity raw
source-data package, or new local sample-matched R/T.

## Pivot

Keep Eternity as one project, but promote the user-facing executive research
assistant lane to the near-term milestone:

- **Serious Core**: physics validation, claim gates, datasets, simulations,
  failed validations, and no-overclaim enforcement.
- **Research Memory**: papers, local lab notes, source-data packages, candidate
  cards, failed hypotheses, and provenance decisions.
- **Executive Research Assistant**: the user's right-hand workflow layer for
  planning, summaries, next actions, prompts, reports, dataset triage, phase
  tracking, and evidence-aware reminders.
- **Research Playground**: speculative ideas and mechanism brainstorming that
  cannot bypass Serious Core.

## Non-Dud Fallback Deliverable

If no public dataset can honestly pass, the fallback milestone is:

- A public-dataset acceptance gate.
- A dataset candidate registry with rejected and downgraded candidates.
- Conservative `calibration_only_no_holdout`, `literature_reproduction_fixture`,
  `failed_validation`, and `synthetic_software_fixture` examples.
- Report and prompt generation that stays tied to claim status.
- A practical assistant loop that answers what is known, what failed, what is
  blocked, and what to do next.

This is a success condition for the research-assistant substrate, even if the
first calibrated-linear evidence attempt has to wait for better data.

## Guardrail

The pivot is not permission to make weaker physics claims. It is a way to keep
the project useful while preserving the evidence standard that makes the
physics core trustworthy.
