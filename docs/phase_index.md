# Eternity Phase Index

Date: 2026-05-16

This file gives stable phase IDs for next-step recommendations. `CURRENT_REALISTIC_ROADMAP.md` and `GOALS.md` remain the roadmap authorities; this index keeps the numbering consistent across Codex sessions.

## Numbering Rule

- `Phase N`: roadmap-level phase.
- `Phase N[A-Z]`: substantial branch inside that phase.
- `Phase N[A-Z].M`: narrow implementation, audit, or verification slice.

Do not renumber old phases unless the roadmap is explicitly reset. Add suffixes when the work splits.

## Current Phases

| Phase ID | Status | Name | Notes |
| --- | --- | --- | --- |
| Phase 1 | Completed | V0 synthetic vertical slice | Synthetic thin-film runner, contracts, deterministic example, reports, and tests. |
| Phase 2 | Completed/In progress | V1 registry and contract scaffolding | Claim-status labels, registry schemas, artifact provenance, material and measurement contracts. |
| Phase 3 | Active | Real-data grounding | Bring real optical constants and measured spectra into the Serious Core without promoting unsupported claims. |
| Phase 3A | Active | TiN/SiO2 thesis reflectance reconciliation | Reconcile thesis/paper TiN/SiO2 measured spectra, `30_20_10` reflectance/Psi/Delta/e1e2 exports, sample labels, angle, polarization, normalization, holdout policy, and fail-closed validation candidate. |
| Phase 3B | Blocked/parked | TiON optical constants and plot-level reflectance provenance | TiON_48/TiON_49 have epsilon tables and grower guidance; attached plots provide reflectance evidence only at image/digitization level unless raw R/T appears. |
| Phase 4 | Gated | First calibrated linear evidence attempt | Requires frozen model, independent holdout, residual/uncertainty gates, split integrity, and claim-status promotion checks. |

## Active Recommendation

Current phase: **Phase 3A - TiN/SiO2 thesis reflectance reconciliation**.

Reason: the TiN/SiO2 thesis path has local measured spectra and additional same-sample-looking ellipsometry exports, while TiON_48/TiON_49 currently remain optical-constant plus plot-level provenance without raw sample-matched R/T.

Information sufficiency:

- Enough for a planning and reconciliation pass.
- Enough to register additional candidate raw artifacts such as `30_20_10 reflectance.txt`, `30_20_10 psi delta.txt`, `30_20_10 p_s intensity.txt`, and `30_20_10 e1 e2.txt`.
- Not enough yet for `calibrated_linear_evidence` until normalization, threshold policy, and residual gates are resolved.

Recommended effort under the current GPT-5.5 assumption:

- Planning: `xhigh`.
- Implementation: `high`, unless the plan resolves into a narrow metadata-only registration pass, in which case `medium` may be enough.

Helpful tools:

- GPD planning/checking/verifier workflows for phase design and scientific claim boundaries.
- Local `pdftotext`, `shasum`, registry validation, and pytest commands.
- Plot digitization only if TiON plot-level reflectance needs to become an explicitly labeled `digitized_from_plot` artifact later.
