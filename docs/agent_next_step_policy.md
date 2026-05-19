# Agent Next-Step Policy

Date: 2026-05-16

This is the repo-local rule for keeping Eternity moving after each implementation pass. `AGENTS.md` is authoritative; this file gives the reusable checklist.

## Required Closeout

After every non-trivial implementation or verification pass, include a compact next-step recommendation based on:

- a stable phase ID from `docs/phase_index.md`;
- the newest implementation result and verification outcome;
- `CURRENT_REALISTIC_ROADMAP.md`, `GOALS.md`, and current project contracts;
- blockers, provenance gaps, failed checks, skipped tasks, and deferred work;
- whether the next phase can be fully completed with the information currently available.

The recommendation should be honest and operational. If the next phase is possible only as a planning, audit, or data-search phase, say that instead of implying the full science claim can be finished.

## Phase ID Discipline

Every next-step recommendation must start from a named phase value. Use this pattern:

- `Phase N`: roadmap-level phase.
- `Phase N[A-Z]`: substantial branch inside that phase.
- `Phase N[A-Z].M`: narrow implementation, audit, or verification slice inside that branch.

Do not invent a fresh number when an existing phase covers the work. Update `docs/phase_index.md` whenever a new phase ID becomes active, blocked, completed, or superseded. Keep skipped tasks visible under the phase that owns them.

## Reasoning Effort Recommendation

Assume GPT-5.5 until the user asks to update the model reference. Recommend one of:

- `low`: routine status, small docs edits, simple mechanical changes, or executing an already-tested command.
- `medium`: ordinary implementation with low ambiguity, local refactors with tests, straightforward artifact registration, or follow-up verification.
- `high`: non-trivial implementation, schema or contract changes, evidence-boundary decisions, data provenance audits, test-failure triage, or roadmap-affecting work.
- `xhigh`: hard-to-reverse architecture, unknown physics/modeling choices, evidence promotion, novelty claims, phase transitions, or Pro-checkpoint style review.

Quality comes first. Cost and usage matter only as a tie-breaker. Do not recommend `xhigh` just because it exists, but also do not steer away from it for complex work. For difficult roadmap phases, model-choice decisions, claim-boundary reviews, or multi-step science planning, `xhigh` planning followed by `high` implementation is often the right pattern.

If planning and implementation need different effort, state both. Example: "Planning: GPT-5.5 xhigh; implementation: GPT-5.5 high unless the provenance audit resolves into a narrow mechanical data-ingestion pass."

## Tool Recommendation

Every next-step recommendation should name useful support:

- MCPs or plugins already available in the current environment;
- repo-local skills or GPD workflows that match the phase;
- local commands or scripts that are safe and useful;
- candidate external tools only when they fill a clear gap.

If no available MCP, plugin, skill, or local command obviously fits, search current sources for safe installable tools or commands before recommending one. Keep candidate installs separate from available tools, and do not install new tools unless the user asked for implementation or approved the install.

For model benchmark values, pricing, API capabilities, or tool availability, treat local PDFs and old notes as snapshots. If a value is unclear, clipped, stale, or important for the recommendation, refresh from the live/current source before relying on it.

## GPD Cadence

Use GPD deliberately, not automatically.

- Reach for GPD when the next step is a phase decision, claim-status review,
  validation/promotion gate, blocker inventory, or final scientific review.
- Skip GPD for routine code edits, CLI/report plumbing, local artifact
  inspection, atlas updates, and ordinary test/lint/build verification unless a
  claim-boundary risk is present.
- If a GPD workflow is blocked by GPD runtime/schema state, do not treat that as
  a blocker on direct repo work when the repo evidence is sufficient. Continue
  with direct verification and report the GPD limitation.
- Keep `GPD/` files synchronized after phase-state changes, but treat them as
  mirrors of the authoritative roadmap, contracts, generated artifacts, and
  claim-status code.

## Deferred Task Tracking

When information is missing, leave a visible handle for it:

- name the missing artifact, measurement, source, or decision;
- state why it blocks the stronger claim or next phase;
- say what can still be done while waiting;
- preserve it in the relevant roadmap, contract, registry, atlas, GPD, or TODO artifact when the work changes project state.
