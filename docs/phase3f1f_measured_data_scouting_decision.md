# Phase 3F.1F - Measured-Data Scouting Decision Or Pause

Date: 2026-05-26

## Decision

Phase 3F.1F pauses measured-data scouting for now.

This is not a success-by-lowering-the-bar decision. It records that the current
public measured-data search envelope has been exhausted far enough to stop
looping on broad discovery. Phase 3F.2 intake remains closed, measured residual
modeling remains forbidden, and Phase 4 remains gated until a future candidate
clears every hard source-backed flag before modeling.

## Evidence Basis

| Phase | Scope | Result | Gate consequence |
| --- | --- | --- | --- |
| Phase 3F.1 | 10 simple/thin-film-adjacent public leads | 0 hard-gate passes | No Phase 3F.2 intake |
| Phase 3F.1B | 16 pasted GPT-5.5 Pro leads | 0 hard-gate passes | No Phase 3F.2 intake |
| Phase 3F.1C | Top-three source-file audit | 0 hard-gate passes | No measured-data candidate |
| Phase 3F.1D | 8 targeted benchmark/source-data or software-fixture leads | 0 measured-data hard-gate passes | Code-regression lane only |
| Phase 3F.1E | 3 deterministic `structural_color_FROCs` parity cases | All code-regression cases passed below `2e-16` | Machinery coverage only, not measured validation |

## Pause Conditions

Measured-data scouting should resume only if at least one of these conditions is
true:

- The user supplies a new source-data package, lead list, or paper/dataset that
  was not already covered by Phase 3F.1 through Phase 3F.1D.
- The next search is intentionally narrower than the exhausted envelope, for
  example a known teaching/benchmark coating package with source-backed optical
  constants and measured spectra.
- A current-source refresh reveals newly published machine-readable measured
  R/T, ellipsometry, or source-code packages that were not public during the
  Phase 3F.1 searches.

Any resumed measured-data lane must still prove public access, source-qualified
constants or model, independent measured holdout, machine-readable files,
geometry, stack/thickness, substrate/backside/coherence handling, leakage-safe
split, TMM suitability, and source/hash readiness before Phase 3F.2 can open.

## Stop Rules Preserved

- Do not run measured residuals on Saha, St Andrews, TiON, Wang, FROC, ultrathin
  Au, or any other candidate without a frozen source-backed model contract.
- Do not use residual shape, fitted thickness, fitted constants, or guessed
  substrate/backside assumptions to rescue a candidate.
- Do not promote Phase 3F.1E beyond `non_promoting_code_regression_fixture`.
- Do not open Phase 4 until a future candidate clears every required gate.

## Next Phase Recommendation

Recommended next phase: `Phase 3G - Research Memory / Executive Research
Assistant measured-data intake queue`.

Planning effort: GPT-5.5 `high`.
Implementation effort: `medium`.

Rationale: the measured-data search has produced useful failure memory and a
small TMM code-regression fixture, but no measured validation candidate. The
best immediate value is now to turn those gates, rejection memories, and phase
rules into a stronger assistant-facing intake workflow so future leads can be
triaged quickly without repeating exhausted searches or weakening the evidence
bar.

