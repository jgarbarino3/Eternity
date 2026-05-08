# Codex Prompt — Stage 4+: External Ingest, Cognee Graph Memory, Hermes/OpenClaw Orchestration

Use this prompt only after Stage 0/1 and Stage 2/3 are merged and stable.

## Context

Eternity now has a local research-memory system with typed records, deterministic IDs, provenance, local note ingestion, search, digests, paper/action translation, lab failure atlas, hypothesis queue, contradiction scans, advisor-safe summaries, and Codex task drafting.

Stage 4+ carefully adds automation and better retrieval. This must be done without turning the system into an uncontrolled agent or untrusted evidence generator.

## Goal

Add, in separate PRs if possible:

1. weekly/home digest outputs,
2. external academic/RSS source adapters,
3. optional graph/semantic memory backend such as Cognee,
4. optional cloud-agent read-only orchestration through Hermes/OpenClaw.

## Hard constraints

- All recurring jobs off by default.
- All network ingest must be source-configured, rate-limited, cached, and logged.
- No PDF hoarding unless license/permission permits.
- Twitter/X or social content is low-trust `lead` only.
- Cognee/graph/vector memory is an index, not the source of truth.
- Hermes/OpenClaw can only run approved read-only commands at first.
- No lab/instrument control.
- No autonomous novelty claims.
- No validated scientific conclusions from external ingest.

## PR A — Weekly digest and home screen

Implement:

```bash
eternity memory home
eternity memory digest --weekly
```

Output five queues:

1. Must-read / must-review this week
2. Possible experiment ideas
3. Possible Codex tasks
4. Contradictions / weak claims
5. Surprising connections

Write artifacts to:

```text
results/research_memory/digests/<date>_<digest_id>/digest.md
results/research_memory/digests/<date>_<digest_id>/manifest.json
```

Digest manifest should include:

- digest ID,
- date,
- included record IDs,
- criteria used,
- warnings,
- evidence-state distribution.

## PR B — External source config and adapters

Create:

```text
config/research_sources.example.yaml
src/eternity/research_memory/adapters/
  __init__.py
  http_cache.py
  rss_client.py
  arxiv_client.py
  semantic_scholar_client.py
  openalex_client.py
```

Add CLI:

```bash
eternity memory ingest-feeds --config config/research_sources.yaml --dry-run
eternity memory ingest-feeds --config config/research_sources.yaml
```

Example config:

```yaml
sources:
  - id: arxiv_optics_daily
    type: arxiv_query
    enabled: false
    query: 'cat:physics.optics AND (ENZ OR epsilon-near-zero OR TiN OR ITO OR AZO)'
    max_results: 25
    project_areas: [literature_radar]
    tags: [arxiv, optics, enz]
    default_evidence_state: lead

  - id: semantic_scholar_enz_frog
    type: semantic_scholar_search
    enabled: false
    query: 'epsilon near zero ultrafast FROG pulse phase TiN ITO'
    max_results: 20
    project_areas: [tin_frog]
    tags: [semantic_scholar, enz, frog]
    default_evidence_state: lead

  - id: lab_newsletters_manual_export
    type: local_folder
    enabled: false
    path: data/external_notes/newsletters
    project_areas: [tool_watch]
    tags: [newsletter]
    default_evidence_state: lead
```

### External ingest rules

For every fetched item:

- store raw metadata snapshot,
- compute hash,
- deduplicate by DOI/arXiv ID/URL/content hash,
- create `SourceRecord` or `PaperActionRecord` with `review_state: needs_human_review`,
- do not mark as validated,
- include API/source and retrieval timestamp,
- include rate-limit and cache metadata.

### arXiv rules

- Respect arXiv API rate limits.
- Use caching.
- Prefer metadata and abstract pages.
- Do not store and serve PDFs unless the license permits it.

### Semantic Scholar/OpenAlex rules

- Use API keys only through environment variables/config ignored by git.
- Never commit secrets.
- Keep query volume low.
- Store only needed metadata fields.

## PR C — Optional graph/semantic memory backend

Add interface:

```python
class MemoryIndexBackend(Protocol):
    name: str
    def index_records(self, records: Sequence[ResearchRecord]) -> IndexReport: ...
    def search(self, query: str, limit: int = 10) -> list[SearchResult]: ...
    def related(self, record_id: str, limit: int = 10) -> list[SearchResult]: ...
```

Keep default backend:

```text
LocalLexicalBackend
```

Add optional backend:

```text
CogneeBackend
```

Cognee requirements:

- dependency must be optional, e.g. `research-graph` extra or documented manual install,
- backend disabled unless configured,
- all indexed content comes from local structured records,
- never use Cognee output as source evidence,
- search results must point back to record IDs and source provenance,
- tests should mock Cognee if dependency is absent.

CLI:

```bash
eternity memory index --backend local
eternity memory index --backend cognee
eternity memory related RECORD_ID --backend local
eternity memory related RECORD_ID --backend cognee
```

## PR D — Optional Hermes/OpenClaw orchestration

Do this only after local workflows are stable.

The agent should be a thin interface to approved commands, not the scientific engine.

Approved read-only commands:

```bash
eternity memory home
eternity memory search <query>
eternity memory show <record_id>
eternity memory digest --weekly
```

Approved draft-only command:

```bash
eternity memory task-from-record <record_id> --draft-only
```

Not approved:

- arbitrary shell execution,
- repo writes,
- lab control,
- instrument control,
- secret access,
- uncontrolled source ingestion,
- unreviewed plugin/skill installation,
- automatic PR creation without human review,
- “validate this scientific claim” as an agent conclusion.

Create docs:

```text
docs/agents/research_engine_agent_policy.md
docs/agents/openclaw_or_hermes_readonly_setup.md
```

The docs should include a permissions matrix:

| Capability | Stage | Allowed? |
|---|---:|---|
| search memory | 7A | yes |
| show records | 7A | yes |
| weekly digest | 7A | yes |
| draft Codex task | 7B | yes, draft only |
| ingest configured feeds | 7C | maybe, dry-run first |
| write memory record | 7C | no without human approval |
| run simulations | 7D | no until explicit gate |
| control lab instruments | never in this roadmap | no |

## Tests

For external ingest:

- mock HTTP responses,
- test cache and rate-limit behavior,
- test deduplication,
- test source trust defaults,
- test dry-run does not write records,
- test secrets are not printed.

For graph backend:

- test local backend always works,
- test Cognee backend gracefully skips/errors when dependency missing,
- test graph results map back to record IDs.

For agent docs/policy:

- no code execution required unless a safe wrapper is implemented,
- tests for command allowlist if implemented.

## Acceptance checklist

```bash
uv run --no-editable pytest
uv run --no-editable ruff check .
uv run --no-editable eternity memory ingest-feeds --config config/research_sources.example.yaml --dry-run
uv run --no-editable eternity memory home
uv run --no-editable eternity memory digest --weekly
```

## Final PR summary format

```markdown
## What changed
- Added weekly/home digest queues.
- Added disabled-by-default external source adapters with dry-run, caching, deduplication, and source trust labels.
- Added optional memory index backend interface and optional Cognee adapter.
- Added read-only agent orchestration policy docs.

## Scientific/security guardrails
- External ingest creates leads/candidate records only.
- Cognee is an index, not source of truth.
- Agent orchestration is read-only/draft-only by default.
- No lab control, no autonomous validation, no novelty claims.

## Validation
- `uv run --no-editable pytest`
- `uv run --no-editable ruff check .`
```
