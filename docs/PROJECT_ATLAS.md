# Eternity Project Atlas

The Project Atlas is the durable map for understanding Eternity as one system
with three authority-separated lanes:

- **Serious Core**: calibrated ENZ digital twin, registry, material models,
  calibration/holdout, validation gates, reports, and claim status.
- **Research Memory / Radar**: paper cards, lab observations, failure modes,
  contradictions, weak-claim queues, digests, and Codex task drafts.
- **Hypothesis Harness**: hypothesis cards, mechanism ranking, artifact
  skepticism, falsifiers, failed-hypothesis memory, and harness scores.

Open the interactive atlas locally:

```text
docs/project_atlas/index.html
```

The atlas is organizational and visual. It does not change claim-status logic,
research-memory schemas, or scientific validation behavior.

## Simple Roadmap

The first goal is:

```text
First calibrated linear ENZ digital twin checkpoint
```

That means: given one identified sample and optical setup, use
calibration-only optical data to fit or load a physically constrained material
model, freeze that model, predict an independent holdout measurement, and emit a
bounded claim status.

Current progress:

- **Done**: V0 synthetic runner and V1 contract scaffolding.
- **Done**: Phase 3C public TiN dataset intake after Phase 3A exhaustion:
  the St Andrews 2025 public TiN archive and linked paper are snapshotted, and
  the dataset includes ellipsometry tables plus `RT.xlsx` R/T data.
- **Doing**: Phase 3C.1 St Andrews TiN pairing + validation candidate:
  canonical R/T CSV snapshots, the candidate `50nm-MTiN-50c` epsilon snapshot,
  registry records, and a fail-closed example now exist.
- **Next**: Phase 3C.2 St Andrews candidate run audit + threshold policy
  decision. Pairing remains `candidate_supported_reflectance_only`,
  transmittance is auxiliary, and predeclared thresholds remain required before
  any calibrated-evidence promotion attempt.
- **Blocked/parked**: Phase 3B TiON_48/TiON_49 raw R/T remains missing; grower
  notes and plots are useful provenance but only plot-level reflectance unless
  raw tables or explicit digitized artifacts are registered.

Goal sequence:

```text
calibrated_linear_evidence
  -> research_memory_substrate
  -> hypothesis_harness
  -> nonlinear_ENZ_readiness
  -> paper_claim_candidate
```

Compact reverse mind map for the first goal. In the interactive atlas, this is
rendered as a left-to-right branching map: one goal card on the left and
completed, in-progress, needed, blocked, or gated branches to the right.

```text
calibrated_linear_evidence
  -> COMPLETE: V0 synthetic runner
  -> COMPLETE: claim-status contract
  -> IN PROGRESS: Phase 3 real-data grounding
  -> IN PROGRESS: Phase 3A TiN/SiO2 thesis reflectance reconciliation
  -> IN PROGRESS: Phase 3A.1 normalization/threshold gate hardening
  -> IN PROGRESS: Phase 3A.2 stack mapping correction
  -> IN PROGRESS: Phase 3A.3 figure/data provenance reconciliation
  -> COMPLETE: Phase 3A.4 absolute-reflectance decision
  -> BLOCKED: Phase 3A.5 export/provenance retrieval
  -> ACTIVE/PACKET READY: Phase 3A.6 re-export or measurement packet
  -> COMPLETE/BLOCKED: Phase 3A.7 source recovery
  -> COMPLETE/BLOCKED: Phase 3A.8 source candidate triage
  -> COMPLETE/DIAGNOSTIC: Phase 3A.9 relative-only packet
  -> COMPLETE/DECISION: Phase 3A.10 branch decision
  -> PACKET READY: Phase 3A.11 manual source follow-up packet
  -> COMPLETE/EXHAUSTED: Phase 3A.12 manual source review
  -> COMPLETE: Phase 3C public TiN dataset intake
  -> ACTIVE: Phase 3C.1 St Andrews TiN pairing
  -> NEXT: Phase 3C.2 run audit / threshold policy
  -> IN PROGRESS: frozen tabulated material model
  -> PARKED: Phase 3B TiON plot-level/R/T provenance
  -> NEEDED: independent holdout measurement
  -> NEEDED: residual and uncertainty report
```

Active conflict:

```text
Optical constants are available for TiN/TiON, but TiON_48/TiON_49
sample-matched R/T provenance is not registered. Grower notes and attached
plots support qualitative TiON trends but do not provide raw R/T tables. This
blocks calibrated TiON evidence while still allowing calibration_only_no_holdout
grounding runs. Phase 3A now follows the separate TiN/SiO2 measured-reflectance
path, capped below calibrated evidence until normalization and threshold gates
are resolved. Phase 3A.3 aligns `d_10nm` with thesis Figure 4.1 while Phase
3A.4 keeps normalization at relative-intensity-only after local thesis,
CompleteEASE, hash, and nearby Woollam-artifact checks. Phase 3A.5 searched
likely local source locations, the desktop SDSU Google Drive folder, targeted
Google Drive thesis/defense hits, SDSU slides/reports, and the scanned lab
notebook. It found related RC2/CompleteEASE and `3L2/Quartz` provenance but no
exact absolute-`%R` export proof, so the decision is `blocked_needs_new_export`.
Phase 3A.6 produced a packet and acceptance policy: the project can request or
perform a clean source-backed re-export rather than pretending the current data
are enough. Phase 3A.7 then recovered related local CompleteEASE/Woollam source
candidates, including DoD SAFE zip-contained snapshots for quartz cap-test and
10 nm SiO2 pulsed/dynamic runs, but still found no source-backed calibrated
absolute-`%R` proof. Phase 3A.8 deduplicates those candidates, separates quartz
10 nm dynamic follow-up candidates from Si-control files, and pivots the
current lane to relative-only diagnostics that cannot feed serious-core
evidence. Phase 3A.9 then records those diagnostics for the existing run:
min-max spectral-shape correlation is high, prediction and measurement dips
coincide at the 400 nm edge of the inspected window, and both trends increase
over 400-900 nm. That is useful diagnostic context, not calibrated validation.
Phase 3A.10 chooses a bounded manual source follow-up on the top three quartz
dynamic candidates before returning to Phase 3B, because Phase 3B still lacks
raw sample-matched TiON R/T.
Phase 3A.11 records the exact three-candidate review packet, proof gates, and
stop rules without changing the relative-only claim boundary.
Phase 3A.12 exhausts that bounded manual source path: the reviewed candidates
are related provenance, not exact source/calibration proof.
Phase 3C opens a cleaner public-dataset lane: the St Andrews 2025 TiN dataset
contains ellipsometry permittivity tables and `RT.xlsx` R/T data, and the linked
paper maps Figure 4 to normal-incidence unpolarized spectra for 50 nm TiN on
glass. Phase 3C.1 extracts the `RT.xlsx` R/T snapshots, registers the
`50nm-MTiN-50c` epsilon table as the candidate frozen input, and adds a
fail-closed validation candidate. This is promising but still blocked from
calibrated promotion until future thresholds are approved before residual
judgment and the transmittance/pairing caveats are resolved.
Phase 3A.2 keeps thesis `d_10nm` source-backed but
keeps the separate `30_20_10` files out of the validation candidate. Phase 3A.1
now keeps the already-inspected residuals as historical context only and blocks
promotion until a future predeclared policy exists.
```

## Core Rule

Claims do not inherit authority from upstream records. They are re-authorized
only by validation artifacts.

Research Memory/Radar may gather and organize context. The Hypothesis Harness
may propose, critique, rank, and falsify. Only the Serious Core may validate
bounded scientific claims through provenance, calibration/holdout integrity,
validation gates, reports, and `claim_status.json`.

## Visual Sections

The interactive atlas contains:

1. **Home / Where Am I?**: current anchor, active lanes, highest-authority
   evidence, speculative queues, and current conflicts.
2. **Simple Roadmap**: the first goal, goal sequence, current progress, and
   compact reverse mind maps.
3. **Authority Map**: what each lane may do, with Serious Core as the only
   validation authority.
4. **Storyboard**: `question -> context/memory -> hypothesis -> experiment or
   simulation -> result -> critique -> claim audit -> memory update -> next
   better question`.
5. **Evidence Promotion Conveyor**: `lead -> memory record -> hypothesis card
   -> validation candidate -> serious-core run -> claim_status.json -> memory
   update`.
6. **Reverse Goal Maps**: dependencies for calibrated linear evidence,
   failed-hypothesis memory, next discriminating experiment, paper-claim
   candidate, and nonlinear ENZ readiness.
7. **Multiple-Path Map**: competing routes to choosing the next useful
   experiment.
8. **Conflict Board**: unresolved tensions with forbidden overclaims and next
   discriminating tests.
9. **Evidence Ladder**: claim maturity from lead/speculation to paper-claim
   candidate.
10. **Roadmap Swimlanes**: parallel lanes for Serious Core, Research Memory,
   Hypothesis Harness, Literature Radar, and future nonlinear/FDTD work.
11. **Node Template**: required metadata for future atlas nodes.

## Evidence Promotion

Eternity should keep parallel paths visible, but not equally authoritative:

```text
Research Memory/Radar
  finds, stores, and organizes context
        |
        v
Hypothesis Harness
  converts context into rival hypotheses, falsifiers, artifact checks, and scars
        |
        v
Human Review Gate
  chooses what is worth validating
        |
        v
Serious Core
  runs calibrated simulations, comparisons, validation gates, and claim status
        |
        v
Memory Feedback
  records what survived, failed, weakened, or became a future constraint
```

## Node Metadata Standard

Every future atlas node should carry:

- status
- authority lane
- source refs
- claim level
- human review state
- linked artifacts
- allowed language
- forbidden language

This prevents speculative outputs from becoming visually adjacent to validated
artifacts in a way that makes them feel validated.
