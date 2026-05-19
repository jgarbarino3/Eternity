# Eternity Phase Index

Date: 2026-05-19

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
| Phase 3A.9 | Completed/diagnostic | Relative-only diagnostic run packet | Reports non-promoting spectral-shape, dip-position, trend-direction, and figure-provenance diagnostics for `run_f35a15cef565fb15`; the packet is useful context but cannot feed serious-core evidence. |
| Phase 3A.10 | Completed/decision | Manual source follow-up vs Phase 3B return | Chooses one bounded manual follow-up pass on the top three quartz dynamic `.SEsnap` candidates before falling back to Phase 3A.6 clean export/new measurement or Phase 3B TiON evidence gathering. |
| Phase 3A.11 | Completed/packet-ready | Bounded manual source follow-up packet | Converts the Phase 3A.10 branch choice into a three-candidate review packet with exact proof gates, stop rules, and non-promotion boundaries. |
| Phase 3A.12 | Completed/exhausted | Manual source review result or clean export pivot | Inspected the three bounded candidates and found related provenance but no exact `3L2/Quartz`, 30/10/20 stack, absolute `%R`, or `d_10nm` source-lineage proof. Phase 3A should not continue without new user-supplied source evidence or a clean export/measurement. |
| Phase 3B | Blocked/parked | TiON optical constants and plot-level reflectance provenance | TiON_48/TiON_49 have epsilon tables and grower guidance; no repo-local raw R/T or digitizable plot candidates are available. Calibration-only examples are allowed, but calibrated promotion is blocked. |
| Phase 3B.1 | Completed/local-exhausted | TiON evidence reality check / digitized plot intake | Inventory found TiON_48/TiON_49 epsilon tables, two material models, and TiON_48/TiON_49 calibration-only examples, but zero R/T measurements and zero repo plot candidates. Decision: `local_validation_data_exhausted_literature_or_external_data_needed`. |
| Phase 3C | Completed/intake-ready | Public TiN dataset validation lane | St Andrews 2025 public TiN dataset has paper-backed 50 nm TiN-on-glass normal-incidence unpolarized R/T plus ellipsometry tables. Snapshot and intake report are ready. |
| Phase 3C.1 | Completed/fail-closed candidate | St Andrews TiN pairing + validation candidate | Extracted `RT.xlsx` into canonical R/T CSV snapshots, registered `50nm-MTiN-50c` as the candidate frozen epsilon input, added the St Andrews sample/stack/material/split records, and created a normal-incidence validation candidate capped at `weak_within_dataset_holdout`. |
| Phase 3C.2 | Completed/future-only policy | St Andrews candidate run audit + threshold policy decision | Audited `run_42fe0ad6dd295019`, preserved residuals as historical context, and wrote a pending future-only threshold policy with `applies_to_existing_run: false`. |
| Phase 3C.3 | Completed/failed-validation | St Andrews threshold lock + clean run decision | Locked conservative reflectance thresholds before `run_f6ea582618328f44`; the clean run failed all five metrics and cannot move to Phase 4 as-is. |
| Phase 3C.4 | Completed/triaged | St Andrews failure triage | Triage packet found a non-near-miss dominated by blue-edge residuals; no alternate epsilon table, simple thickness sweep, or fixed substrate-index sweep repairs the locked-threshold failure. |
| Phase 3C.5 | Completed/parity gaps recorded | St Andrews source-model parity diagnostic | Raw Woollam `.mod/.SE` inspection found source-model gaps: Float Glass Cauchy substrate, film-thickness/roughness metadata, and back-reflection settings are not represented in the current clean-run stack. No model revision or promotion is justified yet. |
| Phase 3C.6 | Completed/decision implemented | Source-model parity implementation or lane park decision | Resolved by Phase 3C.6A: bounded parity code was implemented and the lane remains non-promoting. |
| Phase 3C.6A | Completed/parked | Bounded St Andrews source-model parity implementation | Tested source Cauchy substrate, inferred source thickness, approximate roughness EMA, and approximate backside reflection. All variants failed locked thresholds; exact roughness/back-reflection parity remains underdetermined, so St Andrews is parked before Phase 4. |
| Phase 3D | Active/intake in progress | Literature/public validation dataset search | Public search identified Exeter/Bohn ITO ENZ as the first package to inspect and Saha TiN/AZO as backup. Broad search should pause while Exeter/Bohn is ingested. |
| Phase 3D.1 | Completed/intake-ready | Exeter/Bohn ITO package intake | Downloaded and snapshotted `OpenData.zip` from DOI `10.24378/exe.3004`, verified archive hash/test, and found table/code candidates for ellipsometry-derived ITO epsilon plus TIR-normalized reflection. |
| Phase 3D.1A | Completed/promising-no-promotion | Exeter/Bohn calibration-holdout split audit | Figure 1 provides source-qualified ellipsometry epsilon; Figure 2 provides the cleanest static pre-pump reflection candidate via TIR-normalized `R0`, but the split still needs no-fit extraction/locking before any residual claim. |
| Phase 3D.1B | Completed/split-locked | Exeter/Bohn no-fit static R0 extraction and split lock | Extracted Figure 1 optical constants, Figure 2 TIR reference, and Figure 2 pre-pump `R0` into canonical CSV artifacts; registered the Figure 1 epsilon model; and wrote a split-lock YAML that forbids residual-driven tuning. |
| Phase 3D.1C | Completed/non-promoting diagnostic | Exeter/Bohn package-constant no-fit model reconstruction | Reconstructed the package static Figure 2 model with locked constants. Shape agreement is strong in the plotted window, but absolute residuals are nontrivial, thresholds were not predeclared before residual inspection, and the result remains capped at `weak_within_dataset_holdout`. |
| Phase 3D.2 | Completed/export-blocked | Saha TiN/AZO source-data intake | Snapshotted the public Figshare package, verified all 12 OPJU file MD5s, and confirmed Fig. 2b measured/simulated reflectance labels plus Fig. 2c/d TiN/AZO permittivity labels. No table-ready CSV exists yet because the worksheet data remain inside Origin `.opju` containers. |
| Phase 3D.2A | Recommended/blocker | Saha OPJU worksheet export or open-format alternate | Export Fig. 2b and Fig. 2c/d worksheets to CSV using Origin/Origin Viewer on Windows, LabPlot GUI import/export, or an open-format mirror. Without table export, Saha must stay non-promoting. |
| Phase 4 | Gated | First calibrated linear evidence attempt | Requires frozen model, independent holdout, residual/uncertainty gates, split integrity, and claim-status promotion checks. |

## Active Recommendation

Current phase: **Phase 3D.2A - Saha OPJU worksheet export or open-format alternate**.

Reason: Phase 3D search found a concrete first-ingest package. Phase 3D.1
downloaded and verified Exeter/Bohn ITO `OpenData.zip`; Phase 3D.1A found a
promising but non-promoting split: Figure 1 source-qualified ellipsometry
epsilon and Figure 2 TIR-normalized pre-pump static reflection. Phase 3D.1B
extracted the canonical Figure 1 epsilon, TIR reference, and static `R0`
surface, then locked the split before residuals. Phase 3D.1C reconstructed the
package no-fit static model and found strong shape agreement but nontrivial
absolute residuals, with promotion still forbidden. Phase 3D.2 then inspected
the Saha TiN/AZO backup package: the source exists and is hash-verified, but the
critical Fig. 2 worksheets are proprietary Origin `.opju` containers. The next
meaningful step is export/open-format recovery, not residual modeling.

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
- Enough to report that the current relative-only packet has strong min-max
  shape correlation, matched 400 nm dip location, and shared increasing trend
  over 400-900 nm.
- Enough to choose a bounded manual source follow-up before returning to Phase
  3B, because there are three concrete quartz dynamic candidates and Phase 3B
  still lacks raw TiON R/T.
- Enough to package the manual review scope, source candidates, proof gates,
  and stop rules for Phase 3A.11.
- Enough to conclude the bounded Phase 3A manual source follow-up is exhausted:
  all three candidates pass only the 60-degree context gate and fail or leave
  unresolved the identity, stack, channel, absolute-normalization, and source
  lineage gates.
- Enough to start Phase 3C: the St Andrews dataset archive and linked paper are
  snapshotted under `lab_data/raw/public_st_andrews_tin_2025/`, the archive hash
  is registered, and the `RT.xlsx` reflectance minimum in the paper window
  matches the linked paper's Figure 4 description.
- Enough to complete Phase 3C.1 as a fail-closed validation candidate:
  `RT.xlsx` has canonical reflectance/transmittance CSV snapshots, the selected
  `50nm-MTiN-50c` epsilon table is registered, and the example forbids R/T
  holdout artifacts from fitting.
- Enough to complete Phase 3C.2 as a future-only policy/audit phase:
  `run_42fe0ad6dd295019` is explicitly non-promotable, the policy has
  `applies_to_existing_run: false`, and a next clean run is required before any
  threshold-gated judgment.
- Enough to complete Phase 3C.3 as a clean negative threshold decision:
  the St Andrews reflectance normalization gate is accepted for this public
  dataset, but the clean run failed all five predeclared metrics and remains
  unable to feed the serious core.
- Enough to complete Phase 3C.4 as a diagnostic failure triage: the failure is
  not a near miss, the 400-450 nm residuals dominate, no alternate St Andrews
  epsilon table passes the locked thresholds, and simple thickness/substrate
  changes do not fix the dip or shape.
- Enough to complete Phase 3C.5 as a no-promotion source-model parity packet:
  the selected raw Woollam source model exposes Float Glass Cauchy substrate,
  film-thickness/roughness metadata, and back-reflection settings that differ
  from the current clean-run stack.
- Enough to complete Phase 3C.6A as a bounded no-promotion implementation:
  source-derived parity variants were implemented and all failed the locked
  thresholds, while roughness/back-reflection remain approximate and
  underdetermined.
- Enough to complete Phase 3B.1 as local evidence exhaustion: TiON_48/TiON_49
  epsilon tables and calibration-only examples are available, but no TiON raw
  R/T measurements or repo-local digitizable plot candidates exist.
- Enough to complete Phase 3D.1 as Exeter/Bohn package intake: the ORE/Figshare
  package was snapshotted, hash-verified, and found to contain notebooks, CSVs,
  code, and Figure 1 optical data.
- Enough to complete Phase 3D.1A as a split audit: Figure 1 has
  ellipsometry-derived epsilon and Figure 2 has a table route to
  TIR-normalized pre-pump static reflection, but the lane remains
  non-promoting until no-fit extraction and split locking are done.
- Enough to complete Phase 3D.1B as extraction/split lock: canonical Figure 1
  epsilon, Figure 2 TIR reference, and Figure 2 static `R0` artifacts now exist,
  the Figure 1 epsilon model is registered, and holdout-driven fitting is
  explicitly forbidden by `docs/phase3d1b_exeter_bohn_split_lock.yaml`.
- Enough to complete Phase 3D.1C as a non-promoting no-fit diagnostic: the
  package static model was reconstructed with locked constants, and the plotted
  window has 324 points, RMSE `0.03417097064799868`, and shape correlation
  `0.9808096173689084`.
- Enough to complete Phase 3D.2 as Saha source-data intake: all 12 public OPJU
  files were downloaded from Figshare and matched supplied MD5 digests; Fig. 2b
  labels identify measured `Rp`/`Rs` at 50 degrees; Fig. 2c/d labels identify
  TiN/AZO permittivity and 130 nm / 250 nm thickness comments.
- Not enough to use `30_20_10` files as thesis `d_10nm` validation evidence.
- Not enough to claim absolute reflectance normalization.
- Not enough to complete calibrated Phase 3A promotion without a new export,
  recovered project/recipe/lab note, or source-backed absolute normalization.
- Not enough to promote `run_f35a15cef565fb15` or any Phase 3A run to
  `calibrated_linear_evidence`.
- Not enough to set pass/fail thresholds for already-inspected residuals.
- Not enough to run Phase 3C as calibrated evidence yet: the pairing is only
  `candidate_supported_reflectance_only`, transmittance scaling/noise remains
  auxiliary, and the threshold-locked clean run failed.
- Not enough to use Phase 3C.2 residuals as threshold evidence. They were
  inspected before policy approval and are historical context only.
- Not enough to move to Phase 4 promotion review without explaining or fixing
  the Phase 3C.3 failure.
- Not enough to choose a replacement St Andrews material model from the
  holdout-derived sweeps without leakage; source-model parity must come first.
- Not enough to continue St Andrews toward Phase 4: Phase 3C.6A failed the
  bounded parity test and exact source-model parity remains unavailable.
- Not enough to continue local validation without new data: CompleteEASE
  re-export, TiON raw R/T, and St Andrews author contact are unavailable under
  the user's stated constraints.
- Not enough to promote Exeter/Bohn: Phase 3D.1C residuals are now inspected
  without predeclared numeric pass/fail thresholds, and the holdout is still
  within the source package's nonlinear experiment lane.
- Not enough to run Saha residuals or promote Saha: Fig. 2b and Fig. 2c/d are
  still inside `.opju` files, and only the embedded worksheet previews/labels
  have been inspected. Preview images are audit aids, not calibrated data.

Recommended next phase under the current GPT-5.5 assumption:

- **Phase 3D.2A - Saha OPJU worksheet export or open-format alternate**.
  Planning: GPT-5.5 `medium`, because the scientific split is straightforward
  but the data-export route is tooling-sensitive.
  Implementation: `medium` for documented CSV export; `high` only if attempting
  custom `.opju` parsing or GUI automation.

Helpful tools:

- GPD planning/checking/verifier workflows for phase design and scientific claim boundaries.
- Local `unzip`, `strings`, `pdftotext`, `shasum`, registry validation, and pytest commands.
- Origin/Origin Viewer on Windows, or LabPlot GUI import/export, for OPJU-to-CSV
  extraction if the user can provide access.
- The `eternity phase3c6-parity` CLI for repeatable St Andrews stop-state context.
- The `eternity phase3a7-recovery` CLI for repeatable read-only source scans when comparing source-provenance rules.
- Consensus MCP or current literature search for candidate datasets and
  published validation context.
- Local registry validation, pytest, `pdftotext`, `tabula`/spreadsheet tooling,
  and artifact hashing if a public dataset is selected for intake.
- Plot digitization only if a specific public figure is chosen and is explicitly
  labeled as `digitized_from_plot`; do not treat it as calibrated validation
  without an approved policy.
