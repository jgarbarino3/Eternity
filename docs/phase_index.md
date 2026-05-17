# Eternity Phase Index

Date: 2026-05-17

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
| Phase 3A.5 | Completed/blocked | Source-backed export/provenance retrieval | Bounded local/SDSU/Google Drive search found related RC2/CompleteEASE, thesis, SDSU slide/report, and scanned lab-notebook provenance, but no exact source-backed proof that `d_10nm` `Intensity` exports are calibrated absolute `%R`; decision is `blocked_needs_new_export`. |
| Phase 3A.6 | Active/packet-ready | CompleteEASE re-export / measurement packet | Packet and acceptance policy are ready for a clean future re-export, new measurement, or source-file intake. Artifacts: `docs/phase3a6_completeease_reexport_packet.md`, `docs/phase3a6_acceptance_policy.yaml`, and `docs/superpowers/plans/2026-05-16-phase3a6-completeease-reexport-measurement-packet.md`. |
| Phase 3A.7 | Completed/blocked | CompleteEASE source recovery + 3L2 provenance lock | Read-only scanner and report found related local CompleteEASE/Woollam `.SEsnap/.SE/.iSE` candidates, including DoD SAFE zip-contained 10 nm quartz cap and cap-test snapshots. Stack/geometry provenance is strengthened; absolute `%R` proof is still blocked. |
| Phase 3A.8 | Completed/blocked | Source candidate triage + relative-only diagnostic decision | Deduplicated Phase 3A.7 candidates by SHA-256, separated quartz dynamic/manual follow-up candidates from Si controls, and pivoted to `relative_only_diagnostic` while keeping serious-core and calibrated-evidence promotion forbidden. |
| Phase 3B | Blocked/parked | TiON optical constants and plot-level reflectance provenance | TiON_48/TiON_49 have epsilon tables and grower guidance; attached plots provide reflectance evidence only at image/digitization level unless raw R/T appears. |
| Phase 4 | Gated | First calibrated linear evidence attempt | Requires frozen model, independent holdout, residual/uncertainty gates, split integrity, and claim-status promotion checks. |

## Active Recommendation

Current phase: **Phase 3A.8 - Source candidate triage + relative-only diagnostic decision**.

Reason: the TiN/SiO2 thesis path has local measured spectra and additional same-sample-looking ellipsometry exports, while TiON_48/TiON_49 currently remain optical-constant plus plot-level provenance without raw sample-matched R/T.

Information sufficiency:

- Enough to keep the thesis `d_10nm` validation candidate source-backed at the
  stack-mapping and figure-provenance level.
- Enough to audit and harden the current gate policy.
- Enough to decide that local retrieval did not prove absolute `%R`.
- Enough to use the exact re-export/measurement packet for future source
  recovery or measurement intake.
- Enough to rank local CompleteEASE/Woollam source candidates and keep their
  hashes/member paths in a small repo report.
- Enough to preserve Phase 3A residuals as historical context.
- Enough to classify and preserve the present normalization basis as
  `relative_intensity_only`.
- Enough to pivot Phase 3A into relative-only diagnostics for spectral shape,
  dip position, trend direction, and figure provenance.
- Not enough to use `30_20_10` files as thesis `d_10nm` validation evidence.
- Not enough to claim absolute reflectance normalization.
- Not enough to complete calibrated Phase 3A promotion without a new export,
  recovered project/recipe/lab note, or source-backed absolute normalization.
- Not enough to promote `run_f35a15cef565fb15` or any Phase 3A run to
  `calibrated_linear_evidence`.
- Not enough to set pass/fail thresholds for already-inspected residuals.

Recommended next phase under the current GPT-5.5 assumption:

- **Phase 3A.9 - Relative-Only Diagnostic Run Packet.** Planning: `high`
  because it must keep the relative-only lane useful without overclaiming.
  Implementation: `medium` if it only adds diagnostics/reporting, `high` if
  claim-gate logic changes. Use `xhigh` before any threshold or calibrated
  evidence policy.

Helpful tools:

- GPD planning/checking/verifier workflows for phase design and scientific claim boundaries.
- Local `pdftotext`, `shasum`, registry validation, and pytest commands.
- The `eternity phase3a7-recovery` CLI for repeatable read-only source scans.
- Consensus MCP for literature context on reflectance validation policy if the
  next phase needs published threshold/normalization precedent.
- Plot digitization only if TiON plot-level reflectance needs to become an explicitly labeled `digitized_from_plot` artifact later.
