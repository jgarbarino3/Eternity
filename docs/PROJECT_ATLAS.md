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
- **Doing**: registry, artifact hashes, validation gates, claim-status labels,
  research-memory/radar foundations, and the atlas itself.
- **Next**: real or literature linear data, calibration-only fitting, independent
  holdout comparison, residuals, uncertainty, and validity envelope.

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
  -> IN PROGRESS: registry-backed artifacts
  -> NEEDED: independent holdout measurement
  -> NEEDED: frozen material model
  -> NEEDED: residual and uncertainty report
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
