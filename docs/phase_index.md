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
| Phase 3A.1 | Active | Normalization and threshold gate hardening | Audit the already-inspected Phase 3A run, keep current promotion blocked, and prepare machine-readable normalization/threshold policy for future predeclared runs. |
| Phase 3A.2 | Active | Stack mapping correction | Keep source-backed `d_10nm` -> `3L2/Quartz`, but demote separate `30_20_10` exports to an unresolved candidate bundle until filename-to-thesis provenance is found. |
| Phase 3A.3 | Active | Thesis figure/data provenance reconciliation | Align `d_10nm` text exports with thesis Figure 4.1, downgrade normalization to relative-intensity-only, and keep `30_20_10` separate unless export provenance is found. |
| Phase 3A.4 | Active | Absolute reflectance decision and threshold policy prep | Keep `d_10nm` at `relative_intensity_only` after local provenance/manual checks, and require source-backed absolute normalization plus future predeclared thresholds before promotion. |
| Phase 3A.5 | Next | Source-backed export/provenance retrieval | Look for CompleteEASE/Woollam project, recipe, export, debug bundle, lab note, or new export evidence tying exact dynamic traces to absolute reflectance calibration. |
| Phase 3B | Blocked/parked | TiON optical constants and plot-level reflectance provenance | TiON_48/TiON_49 have epsilon tables and grower guidance; attached plots provide reflectance evidence only at image/digitization level unless raw R/T appears. |
| Phase 4 | Gated | First calibrated linear evidence attempt | Requires frozen model, independent holdout, residual/uncertainty gates, split integrity, and claim-status promotion checks. |

## Active Recommendation

Current phase: **Phase 3A.4 - absolute reflectance decision and threshold policy prep**.

Reason: the TiN/SiO2 thesis path has local measured spectra and additional same-sample-looking ellipsometry exports, while TiON_48/TiON_49 currently remain optical-constant plus plot-level provenance without raw sample-matched R/T.

Information sufficiency:

- Enough to keep the thesis `d_10nm` validation candidate source-backed at the
  stack-mapping and figure-provenance level.
- Enough to audit and harden the current gate policy.
- Enough to preserve Phase 3A residuals as historical context.
- Enough to classify and preserve the present normalization basis as
  `relative_intensity_only`.
- Not enough to use `30_20_10` files as thesis `d_10nm` validation evidence.
- Not enough to claim absolute reflectance normalization.
- Not enough to promote `run_f35a15cef565fb15` or any Phase 3A run to
  `calibrated_linear_evidence`.
- Not enough to set pass/fail thresholds for already-inspected residuals.

Recommended effort under the current GPT-5.5 assumption:

- Planning: `medium` for the next source-retrieval pass; `xhigh` before any
  threshold or calibrated-evidence policy decision.
- Implementation: `medium` for local search/docs/registry updates; `high` if
  contract logic changes.

Helpful tools:

- GPD planning/checking/verifier workflows for phase design and scientific claim boundaries.
- Local `pdftotext`, `shasum`, registry validation, and pytest commands.
- Plot digitization only if TiON plot-level reflectance needs to become an explicitly labeled `digitized_from_plot` artifact later.
