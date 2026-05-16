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
- **Doing**: Phase 3A.4 absolute-reflectance decision and threshold-policy prep
  after the TiN/SiO2 thesis reflectance candidate:
  source-qualified TiN/TiON optical
  constants, thesis reflectance snapshots, sample/stack IDs,
  registry-backed tabulated models, R/T provenance audits, and atlas/GPD
  alignment.
- **Next**: Phase 3A.5 source-backed export/provenance retrieval, then
  Pro/user-approved thresholds before any future calibrated-evidence promotion
  attempt.
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
  -> IN PROGRESS: Phase 3A.4 absolute-reflectance decision
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
CompleteEASE, hash, and nearby Woollam-artifact checks. Phase 3A.2 keeps thesis
`d_10nm` source-backed but keeps the separate `30_20_10` files out of the
validation candidate. Phase 3A.1 now keeps the already-inspected residuals as
historical context only and blocks promotion until a future predeclared policy
exists.
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
