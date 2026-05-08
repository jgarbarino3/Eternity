# Source, Agent, and Science Policy for Eternity Research Engine

## Mission

The research engine helps Eternity remember, connect, critique, and prioritize. It does not validate scientific claims by itself.

## Source policy

### Source trust levels

| Source type | Default evidence state | Notes |
|---|---|---|
| peer-reviewed paper | candidate_claim | Useful, but transfer to Eternity must be checked. |
| preprint | lead or candidate_claim | Useful but lower confidence. |
| instrument manual | background or candidate_claim | High for operation/specs, not for research interpretation. |
| lab note | lab_observed | Observation is preserved; interpretation may be wrong. |
| simulation artifact | simulation_unvalidated | Unless serious-core validation says otherwise. |
| conference talk | lead | Often incomplete; preserve as lead. |
| newsletter | lead | Useful monitoring, not evidence. |
| Twitter/X/social | lead | Lowest-trust; never evidence by itself. |
| agent summary | background | Never evidence; must point back to source records. |
| Codex task | lead | Implementation proposal, not evidence. |

## Copyright and API policy

- Store descriptive metadata freely when allowed.
- Store local notes, user-written summaries, and permitted text.
- Do not mirror or serve PDFs unless license/permission allows.
- Prefer links to abstract pages and source identifiers.
- Respect source API terms and rate limits.
- Cache repeated API calls.
- Keep recurring ingest disabled by default.
- Never commit API keys or private tokens.

## Scientific policy

No memory output may claim:

- novelty,
- validation,
- mechanism proof,
- material-model correctness,
- nonlinear response isolation,
- paper-ready conclusion,

unless supported by serious-core validation artifacts and human expert review.

### Allowed language

Use:

- “suggests,”
- “consistent with,”
- “candidate explanation,”
- “possible transfer,”
- “needs validation,”
- “weakens this interpretation,”
- “not explained by this baseline.”

Avoid:

- “proves,”
- “discovers,”
- “validated,”
- “novel,”
- “the mechanism is,”
- “paper-ready,”

unless validation gates have been passed.

## Agent permission policy

### Level 0 — Manual local use

Allowed:

- local note ingestion,
- search,
- show,
- export,
- digest,
- Codex task drafts.

### Level 1 — Scheduled local ingest

Allowed only after source config is reviewed:

- RSS/arXiv/Semantic Scholar/OpenAlex dry-run,
- low-volume metadata fetch,
- digest creation.

Still not allowed:

- unbounded crawling,
- social auto-scroll,
- private inbox scraping without explicit request,
- writing scientific conclusions.

### Level 2 — Graph/semantic memory

Allowed:

- index local records,
- retrieve related records,
- suggest connections.

Not allowed:

- source-of-truth replacement,
- evidence-state upgrades,
- uncited claims.

### Level 3 — Cloud agent read-only mode

Hermes/OpenClaw or similar may call only allowlisted commands:

```bash
eternity memory home
eternity memory search <query>
eternity memory show <record_id>
eternity memory digest --weekly
```

### Level 4 — Draft-only task generation

Allowed:

```bash
eternity memory task-from-record <record_id> --draft-only
```

Not allowed:

- automatically opening PRs,
- automatically editing repo files,
- automatically running lab systems,
- automatically classifying claims as validated.

### Never allowed in this roadmap

- autonomous lab/instrument control,
- bypassing safety interlocks,
- arbitrary shell execution from a messaging app,
- broad filesystem access without sandboxing,
- unreviewed third-party skills/plugins,
- autonomous novelty or publication claims.

## Data governance

Store memory data in predictable paths:

```text
data/research_memory/
results/research_memory/
```

Do not commit private lab notes by default. Add `.gitignore` rules if needed:

```gitignore
data/research_memory/
results/research_memory/
```

Commit only schemas, docs, templates, examples, and tests unless the user explicitly wants curated records in git.

## Human review gates

Human review is required before:

- using a memory record as an advisor-meeting claim,
- turning a hypothesis into lab time,
- treating a simulation task as evidence,
- adding a new source adapter with credentials,
- enabling recurring ingest,
- granting a cloud agent write permissions,
- connecting anything to lab instruments.

## Failure preservation

Negative results should be stored, not hidden. A failed model or failed Codex task can be highly valuable if it prevents repeated work or narrows interpretation.

Required negative-result fields:

- what failed,
- context,
- why it matters,
- what it weakens or rules out,
- what would be needed to revisit it,
- related records.
