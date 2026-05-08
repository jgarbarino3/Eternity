# Codex Prompt — Stage 0/1: Research Memory Foundation for Eternity

You are working in the private GitHub repo `jgarbarino3/Eternity`.

## Context

Eternity is a long-term AI-assisted ultrafast ENZ optics research project. Current V0 is a reproducible synthetic thin-film experiment runner, not an autonomous scientist. It already has a Python package under `src/eternity`, Pydantic experiment schemas, Pint units, TMM simulation, deterministic run IDs, Typer CLI commands `eternity validate` and `eternity run`, artifact output under `results/runs/<run_id>/`, and tests.

Your task is to add the first local research-memory layer. This is a researcher-playground layer. It must not alter existing simulation behavior or present memory outputs as validated scientific conclusions.

Create a new branch such as:

```bash
git checkout -b codex/research-memory-v0
```

## Goal

Implement a local, deterministic, provenance-backed research-memory system that can ingest local notes, store typed records, search them, show them, export them, produce simple digests, and draft Codex tasks.

The first version must be useful without cloud agents, LLM calls, Cognee, Hermes, OpenClaw, Twitter scraping, or external network access.

## Hard constraints

- Do not break the existing `eternity validate` and `eternity run` commands.
- Do not modify current experiment schemas unless absolutely necessary.
- Do not add autonomous network calls.
- Do not add cloud-agent integrations.
- Do not add lab or instrument control.
- Do not claim anything is scientifically validated.
- All generated memory artifacts must include provenance and evidence status.
- Identical normalized records should have deterministic IDs.
- Tests must pass with `uv run --no-editable pytest`.
- Ruff should pass with the repo's current lint settings.

## Implementation plan

### 1. Add package structure

Create:

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
```

Add tests:

```text
tests/research_memory/
  test_records.py
  test_ids.py
  test_store.py
  test_ingest.py
  test_search.py
  test_digest.py
  test_cli_memory.py
```

Add docs/examples:

```text
docs/roadmaps/research_engine.md
docs/policies/research_memory_policy.md
docs/schemas/research_memory_schema.md
config/research_taste.yaml
research/examples/notes/tin_frog_failure_mode_example.md
research/examples/notes/ptychography_method_transfer_example.md
```

### 2. Add record schemas

Use Pydantic v2. Keep schemas strict: `ConfigDict(extra="forbid")`.

Create enums:

```python
SourceType = Literal[
    "peer_reviewed_paper",
    "preprint",
    "instrument_manual",
    "lab_note",
    "simulation_artifact",
    "conference_talk",
    "newsletter",
    "twitter_lead",
    "agent_summary",
    "codex_task",
    "other",
]

EvidenceState = Literal[
    "lead",
    "background",
    "candidate_claim",
    "lab_observed",
    "simulation_unvalidated",
    "validation_candidate",
    "validated_with_holdout",
    "rejected_or_failed",
    "deprecated",
]

ReviewState = Literal[
    "needs_human_review",
    "reviewed",
    "approved_for_codex",
    "approved_for_lab_planning",
    "archived",
]
```

Important rule: this Stage 0/1 implementation should allow users to create records with `validated_with_holdout` only if they explicitly provide a field such as `validation_artifact_ref`. Otherwise reject or downgrade it. The research-memory CLI should not create `validated_with_holdout` records by default.

Common base fields:

```python
class ResearchRecord(BaseModel):
    schema_version: Literal["0.1"] = "0.1"
    record_type: str
    record_id: str | None = None
    title: str
    summary: str
    body: str = ""
    source_type: SourceType
    evidence_state: EvidenceState = "lead"
    review_state: ReviewState = "needs_human_review"
    project_areas: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    related_record_ids: list[str] = Field(default_factory=list)
    raw_artifact_hash: str | None = None
    source_locator: str | None = None
    created_at: datetime
    updated_at: datetime
    assumptions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
```

Specialized records may include:

- `SourceRecord`
- `PaperNoteRecord`
- `MethodTransferRecord`
- `LabObservationRecord`
- `FailureModeRecord`
- `HypothesisRecord`
- `ContradictionRecord`
- `CodexTaskRecord`
- `DigestRecord`

Do not over-engineer every field in Stage 0/1. Prioritize a robust base record, one or two useful specialized models, and clear extension points.

### 3. Deterministic IDs

Use existing Eternity canonical hashing utilities if available. Otherwise implement local canonical JSON hashing compatible with existing style.

Desired ID format:

```text
rm_<record_type_slug>_<hash12>
```

Normalize before hashing:

- exclude `record_id`,
- sort dictionary keys,
- sort tags/project areas if semantically unordered,
- use ISO timestamps only if they are part of identity; for note ingestion, avoid using current time in identity hash.

Tests:

- same input yields same record ID,
- changed title/body/source hash changes ID,
- record ID is stable across runs.

### 4. Local storage

Use Python standard-library SQLite.

Default database path:

```text
data/research_memory/research_memory.sqlite
```

Create table:

```sql
records(
  record_id TEXT PRIMARY KEY,
  record_type TEXT NOT NULL,
  title TEXT NOT NULL,
  summary TEXT NOT NULL,
  body TEXT NOT NULL,
  source_type TEXT NOT NULL,
  evidence_state TEXT NOT NULL,
  review_state TEXT NOT NULL,
  tags_json TEXT NOT NULL,
  project_areas_json TEXT NOT NULL,
  related_record_ids_json TEXT NOT NULL,
  raw_artifact_hash TEXT,
  source_locator TEXT,
  payload_json TEXT NOT NULL,
  content_hash TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
)
```

Optionally create indexes on `record_type`, `source_type`, `evidence_state`, `review_state`, and `content_hash`.

Do not require SQLite FTS5. Implement simple deterministic lexical scoring in Python so tests are portable.

### 5. Ingestion

Support local Markdown/text ingestion.

Command:

```bash
eternity memory ingest-note PATH \
  --source-type lab_note \
  --title "TiN FROG B7 Run1 scalar GDD failure" \
  --summary "Scalar GDD-only model failed to reproduce post-TiN temporal structure." \
  --tag tin --tag frog --tag gdd \
  --project-area tin_frog
```

Behavior:

- read the file,
- compute SHA-256 of raw bytes,
- copy raw file to `data/research_memory/raw/<sha256>.<suffix>` or store a metadata pointer if copying is disabled,
- create a `ResearchRecord` or `LabObservationRecord`,
- set `raw_artifact_hash`, `source_locator`, `tags`, `project_areas`, and timestamps,
- store in SQLite,
- print the record ID.

Support `--no-copy-raw` for files the user does not want copied.

### 6. CLI commands

Extend current Typer CLI by adding a `memory` sub-app without breaking existing commands.

Commands:

```bash
eternity memory init
eternity memory ingest-note PATH [options]
eternity memory list [--limit 20] [--tag TAG] [--project-area AREA]
eternity memory search QUERY [--limit 10]
eternity memory show RECORD_ID
teternity memory export --format jsonl
eternity memory digest [--since YYYY-MM-DD] [--project-area AREA]
eternity memory task-from-record RECORD_ID [--output PATH]
```

Fix the typo above during implementation: the command is `eternity`, not `teternity`.

Output rules:

- `search` should show record ID, title, source type, evidence state, review state, tags, and a short snippet.
- `show` should show full payload as pretty JSON or Markdown. Use a `--json` flag if useful.
- `digest` writes a Markdown digest to `results/research_memory/digests/<date>_<digest_id>/digest.md` and prints the path.
- `task-from-record` writes a Codex-ready Markdown task to `results/research_memory/codex_tasks/<record_id>_<task_id>.md`.

### 7. Search/scoring

Implement simple lexical search:

- tokenize lowercased query and record text,
- score matches in title > summary > tags > body,
- stable tie-break by `record_id`,
- return deterministic order.

No embeddings yet.

### 8. Digest

Stage 0/1 digest can be simple and deterministic.

Sections:

```markdown
# Eternity Research Memory Digest — <date>

## Must-read / must-review
## Possible Codex tasks
## Possible experiment ideas
## Weak claims / needs validation
## Surprising connections
## Recent records
```

Since no LLM is used, classify based on record types/tags/evidence states. The output is allowed to be basic but must be useful and honest.

### 9. Codex task generator

Generate a Markdown task that includes:

- Goal
- Context
- Source record
- Inputs
- Expected outputs
- Success criteria
- Safety/scientific guardrails
- Do not do

Default guardrails:

```text
Do not touch lab acquisition code.
Do not make novelty claims.
Do not treat synthetic outputs as validation.
Do not change serious-core schemas unless explicitly required.
Keep outputs deterministic and tested.
```

### 10. Example notes

Add two example notes:

1. `tin_frog_failure_mode_example.md`

Content should preserve a failure/negative result style:

```text
Symptom: FROG retrieval after TiN reflection shows changed temporal structure and possible satellite suppression. A scalar GDD-only replacement does not reproduce at least one run's structure.
Known observations: TiN/FROG runs show phase-sensitive changes; scalar GDD may be partial in some cases but insufficient in others.
Possible explanations: higher-order spectral phase, ENZ linear dispersion, nonlinear response, alignment/spectral filtering, retrieval artifact.
Needed test: matched no-sample / TiN reflection / neutral mirror control across pulse energies with consistent retrieval settings.
Evidence state: lab_observed, not validated.
```

2. `ptychography_method_transfer_example.md`

Content should be a method-transfer radar card:

```text
Method: ptychographic temporal reconstruction.
Original field: ultrafast/attosecond pulse metrology and phase retrieval.
Possible transfer: compare robustness against FROG retrieval for broadband ENZ-centered pulses with higher-order phase distortions.
First Codex task: implement a synthetic toy comparison only; no lab pipeline changes.
Evidence state: lead.
```

### 11. Tests

Add tests for:

- record schema rejects extra fields,
- invalid evidence/source states fail,
- deterministic ID generation,
- raw file hash stability,
- duplicate ingest does not create duplicate content unintentionally,
- lexical search ordering,
- digest artifact generation,
- CLI smoke tests with Typer runner or subprocess,
- existing V0 commands still import and work.

### 12. Acceptance checklist

Before finishing:

```bash
uv run --no-editable pytest
uv run --no-editable ruff check .
uv run --no-editable eternity validate experiments/examples/linear_ito_toy.yaml
uv run --no-editable eternity run experiments/examples/linear_ito_toy.yaml
uv run --no-editable eternity memory init
uv run --no-editable eternity memory ingest-note research/examples/notes/tin_frog_failure_mode_example.md --source-type lab_note --title "TiN/FROG failure mode example" --summary "Example failure-mode note for TiN/FROG scalar-GDD insufficiency." --tag tin --tag frog --tag gdd --project-area tin_frog
uv run --no-editable eternity memory search "scalar GDD TiN FROG"
uv run --no-editable eternity memory digest --project-area tin_frog
```

Commit only after tests pass.

## Final PR summary format

Use this summary:

```markdown
## What changed
- Added local research-memory package with typed records, deterministic IDs, SQLite store, local note ingestion, search, digest, and Codex task drafting.
- Added docs/policies/schema examples for the research engine.
- Added tests for records, IDs, ingest, search, digest, and CLI.

## Scientific guardrails
- Research-memory outputs are candidate/review artifacts, not validated evidence.
- No network ingestion, cloud agents, Cognee, Hermes, OpenClaw, or lab control in this stage.
- Validated scientific conclusions remain the responsibility of Eternity serious-core validation workflows.

## Validation
- `uv run --no-editable pytest`
- `uv run --no-editable ruff check .`
- `uv run --no-editable eternity validate experiments/examples/linear_ito_toy.yaml`
- `uv run --no-editable eternity run experiments/examples/linear_ito_toy.yaml`
```
