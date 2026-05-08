# Eternity Research Engine Roadmap

Generated for Eternity on 2026-05-08.

## Executive decision

Implement the idea, but do it in an Eternity-native way.

The generic Twitter workflow says: use a cloud-hosted agent, add memory, ingest sources, schedule jobs, generate digests, and improve retrieval. For Eternity, that is only partially right. The dangerous failure mode is building a beautiful agentic paper-hoarding machine that produces plausible but unvalidated scientific narratives. The better path is to make a research-memory substrate that turns papers, lab notes, manuals, and past analysis into reviewable records, candidate hypotheses, Codex tasks, and lab/simulation decisions.

The right first implementation is not Hermes/OpenClaw/Cognee as the center. The right first implementation is:

```text
local typed records + immutable raw artifacts + provenance + deterministic retrieval + review queues
```

Then:

```text
optional external ingest -> optional graph/semantic memory -> optional cloud agent orchestration
```

The key architectural rule:

```text
Research engine proposes. Eternity serious core validates.
```

## Why this is high value for Eternity

Eternity already has the beginning of a serious core: a deterministic experiment runner, explicit schemas, units, provenance, warnings, metrics, and reports. A research engine adds the missing front-end layer that can continuously convert outside information and lab memory into decisions.

The best immediate returns are:

1. Paper-to-experiment/simulation/Codex-task translation.
2. Lab failure-mode memory.
3. Contradiction detection across evolving interpretations.
4. Weekly relevance scoring for ENZ/FROG/Z-scan/pump-probe work.
5. Method-transfer radar from adjacent fields.

This is more valuable than a generic paper search bot because Eternity's bottleneck is not simply finding more papers. The bottleneck is preserving context, avoiding overclaiming, deciding what to simulate next, and turning fragmented observations into validated research progress.

## North star workflow

```text
New source appears
  ↓
Raw source is stored or referenced with hash/provenance
  ↓
Typed extraction creates reviewable research records
  ↓
Records are indexed for search and graph connections
  ↓
System proposes: relevant papers, failure modes, hypotheses, contradictions, Codex tasks
  ↓
Human reviews and chooses actions
  ↓
Codex implements simulation/analysis tasks
  ↓
Eternity serious core runs validated simulations/reports
  ↓
Validated outputs feed back into memory with evidence status
```

## Separation between Serious Core and Researcher Playground

### Serious Core

Owns:

- experiment specs,
- units,
- material models,
- raw lab data registry,
- calibration and holdout splits,
- simulations,
- validation reports,
- uncertainty and residual checks,
- evidence labels,
- deterministic artifacts,
- tests.

The serious core is allowed to say something is validated only when the validation machinery supports that claim.

### Researcher Playground

Owns:

- literature notes,
- method-transfer ideas,
- lab troubleshooting memory,
- hypotheses,
- contradiction scans,
- weekly digests,
- advisor-safe summaries,
- figure/storyline plans,
- Codex task drafts.

The playground may generate candidate claims but must label them as candidates. It cannot upgrade scientific confidence by sounding persuasive.

## Non-goals for the first implementation

Do not implement these first:

- autonomous Twitter scrolling,
- autonomous email/newsletter scraping,
- broad cloud agent deployment,
- real-time lab or instrument control,
- automatic novelty claims,
- paper-like conclusions from synthetic or unvalidated results,
- Cognee as the only database/source of truth,
- unreviewed LLM extraction that writes permanent claims,
- storage of copyrighted PDFs unless license/permission permits.

## Roadmap overview

### Stage 0 — Repo alignment and guardrails

Goal: add docs/config only, no behavior changes.

Deliverables:

- `docs/roadmaps/research_engine.md`
- `docs/policies/research_memory_policy.md`
- `docs/schemas/research_memory_schema.md`
- optional `config/research_taste.yaml`

Acceptance criteria:

- existing `eternity validate` and `eternity run` still work,
- no new network calls,
- no new agent permissions,
- docs explicitly state that research memory is not validated evidence.

### Stage 1 — Local research memory foundation

Goal: create a local, typed, provenance-backed memory store.

Implement:

- package: `src/eternity/research_memory/`
- Pydantic records for sources, claims, papers, methods, lab observations, failure modes, hypotheses, contradictions, Codex tasks, and digests.
- deterministic record IDs using canonical JSON hashing.
- local SQLite store using Python standard library.
- immutable raw artifact hashing/copying for local Markdown/text inputs.
- simple lexical search over title/summary/body/tags.
- CLI under `eternity memory ...`.

Commands:

```bash
eternity memory init
eternity memory ingest-note notes/tin_frog_b7_run1.md --source-type lab_note --tags tin frog phase --project-area tin_frog
eternity memory search "scalar GDD failed satellite suppression"
eternity memory show <record_id>
eternity memory list --tag frog --limit 20
eternity memory export --format jsonl
eternity memory task-from-record <record_id>
eternity memory digest --since 2026-05-01
```

Acceptance criteria:

- deterministic IDs for identical normalized record payloads,
- raw artifact hashes are recorded,
- search results include provenance and evidence status,
- tests cover schema validation, hashing, ingestion, search, exports,
- existing V0 tests still pass.

### Stage 2 — Paper-to-action translator

Goal: every important paper/manual/note can become a structured action card.

Implement record types and commands for:

- `PaperNoteRecord`
- `MethodTransferRecord`
- `ResearchActionRecord`
- `CodexTaskRecord`

Translator outputs must include:

- claim/method/parameters,
- what was measured,
- what Eternity can reproduce,
- what can be adapted,
- what is irrelevant,
- suggested simulation,
- suggested lab test,
- suggested Codex task,
- evidence caveats.

This stage can be template/rule driven first. Optional LLM extraction may be added later, but the output must still pass schema validation and must be marked `extraction_status: needs_human_review`.

### Stage 3 — Lab failure atlas and contradiction detector

Goal: preserve hard-won lab debugging memory and prevent narrative drift.

Implement:

- `FailureModeRecord`
- `NegativeResultRecord`
- `InterpretationRecord`
- `ContradictionRecord`
- `ValidationNeedRecord`

Core queries:

```bash
eternity memory failure-search "Z-scan asymmetric"
eternity memory contradiction-scan --project-area tin_frog
eternity memory advisor-summary --project-area tin_frog
```

The contradiction detector should be conservative. It should flag possible tensions, not claim logical contradictions unless the records clearly conflict.

Example tension:

```text
Earlier note: TiN mainly broadens the pulse.
Later note: scalar GDD-only model fails to reproduce B7 Run1 temporal structure.
Resolution wording: TiN modifies temporal structure; in several cases the modification is not well described by uniform broadening or scalar GDD alone.
```

### Stage 4 — Weekly digest and home-screen queues

Goal: produce useful recurring outputs without requiring a cloud agent.

Implement:

```bash
eternity memory digest --weekly
eternity memory home
```

The digest should produce Markdown artifacts under:

```text
results/research_memory/digests/<date>_<digest_id>/digest.md
```

Required queues:

1. must-read this week,
2. possible experiment ideas,
3. possible Codex tasks,
4. contradictions / weak claims,
5. surprising connections.

Ranking should use explicit research taste criteria:

- phase-sensitive measurement,
- ENZ material response,
- broadband ultrafast pulses,
- reproducible parameters,
- dispersion-vs-nonlinearity relevance,
- FROG/Z-scan/pump-probe relevance,
- simulation module potential,
- paper/conference storyline value,
- evidence quality,
- source trust.

### Stage 5 — External source adapters

Goal: carefully add automated ingestion.

Sources should be added in this order:

1. curated local Markdown/PDF-text notes,
2. arXiv queries/RSS,
3. Semantic Scholar/OpenAlex metadata search,
4. selected RSS feeds,
5. newsletter ingestion if user provides exported text,
6. Twitter/X only as low-trust social leads, not evidence.

Implement:

- `config/research_sources.yaml`,
- `eternity memory ingest-feeds --config config/research_sources.yaml`,
- HTTP caching,
- rate limiting,
- source trust labels,
- raw metadata snapshots,
- deduplication by DOI/arXiv ID/URL/content hash.

Rules:

- no PDF hoarding unless license/permission allows,
- no ToS circumvention,
- no infinite crawling,
- no source becomes scientific evidence without review,
- all recurring jobs must be off by default.

### Stage 6 — Optional Cognee graph/semantic memory adapter

Goal: improve retrieval and idea connections, not replace provenance.

Cognee can index validated research-memory records and produce graph/semantic retrieval. The source of truth remains Eternity's local structured records. Cognee is an adapter/backend, not the authority.

Implement interface:

```python
class MemoryIndexBackend(Protocol):
    def index_records(self, records: Sequence[ResearchRecord]) -> IndexReport: ...
    def search(self, query: str, limit: int = 10) -> list[SearchResult]: ...
    def related(self, record_id: str, limit: int = 10) -> list[SearchResult]: ...
```

Backends:

- `LocalLexicalBackend` — default, deterministic, no network.
- `CogneeBackend` — optional extra, disabled unless configured.

Cognee outputs must be treated as retrieval suggestions. They cannot create validated scientific claims.

### Stage 7 — Optional Hermes/OpenClaw agent orchestration

Goal: make the system easier to access from chat/mobile/cloud, not more scientifically authoritative.

The agent may run only approved read-only commands first:

```bash
eternity memory search ...
eternity memory home
eternity memory digest --weekly
eternity memory show <record_id>
```

Later it may draft, but not apply, Codex tasks:

```bash
eternity memory task-from-record <record_id> --draft-only
```

Agent must not:

- write scientific conclusions without human review,
- control lab instruments,
- access secrets broadly,
- ingest private data without explicit source configuration,
- run arbitrary shell commands,
- install unreviewed skills/plugins,
- open network surfaces without authentication and logging.

## Target file layout

```text
src/eternity/research_memory/
  __init__.py
  cli.py
  records.py
  ids.py
  store.py
  ingest.py
  search.py
  scoring.py
  digest.py
  tasks.py
  policies.py
  adapters/
    __init__.py
    local.py
    cognee_backend.py        # optional, later stage only
    arxiv_client.py          # optional, later stage only
    semantic_scholar.py      # optional, later stage only

config/
  research_taste.yaml
  research_sources.example.yaml

docs/
  roadmaps/research_engine.md
  policies/research_memory_policy.md
  schemas/research_memory_schema.md

research/examples/
  notes/tin_frog_failure_mode_example.md
  notes/ptychography_method_transfer_example.md
  records/paper_note_example.yaml

results/research_memory/
  digests/
  codex_tasks/

tests/research_memory/
  test_records.py
  test_store.py
  test_ingest.py
  test_search.py
  test_digest.py
  test_cli_memory.py
```

## Evidence-state taxonomy

Use these states consistently:

- `lead`: potentially interesting source or social/literature lead.
- `background`: useful context, not directly actionable.
- `candidate_claim`: extracted claim needing verification.
- `lab_observed`: observed in lab notes/data but not yet validated.
- `simulation_unvalidated`: produced by synthetic/toy/unvalidated simulation.
- `validation_candidate`: hypothesis with proposed validation test.
- `validated_with_holdout`: passed appropriate calibration/holdout validation.
- `rejected_or_failed`: negative result or disproven interpretation.
- `deprecated`: no longer recommended, preserved for history.

Only serious-core validation workflows should produce `validated_with_holdout`.

## Source-trust taxonomy

- `instrument_manual`: high for instrument operation, not necessarily for scientific interpretation.
- `peer_reviewed_paper`: high for reported claims, but still may not transfer to Eternity conditions.
- `preprint`: useful, lower confidence than peer-reviewed.
- `lab_note`: high relevance, variable reliability; must preserve context.
- `simulation_artifact`: depends on model validity envelope.
- `conference_talk`: useful lead, partial details.
- `newsletter`: useful lead/background.
- `twitter_lead`: low-trust lead only.
- `agent_summary`: never source evidence; points back to source records.
- `codex_task`: implementation proposal, not evidence.

## The most important design choice

Make memory records auditable artifacts. Do not make the graph/vector index the memory.

Bad architecture:

```text
source -> embeddings/graph -> chat answer
```

Better architecture:

```text
source -> raw artifact/provenance -> typed record -> index -> cited retrieval -> reviewable action
```

## When to stop and ask for deeper reasoning

Use a Pro checkpoint before:

- choosing the long-term memory backend,
- giving a cloud agent write permissions,
- turning literature extraction into scientific claims,
- connecting to lab instruments,
- switching from linear/TMM baseline to nonlinear modeling or FDTD/custom solvers,
- publishing/claiming novelty from engine outputs.
