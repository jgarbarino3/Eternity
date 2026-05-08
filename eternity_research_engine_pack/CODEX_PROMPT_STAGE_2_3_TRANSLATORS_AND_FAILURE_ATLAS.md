# Codex Prompt — Stage 2/3: Paper Translator, Failure Atlas, Hypothesis Queue, Contradiction Detector

Use this prompt only after Stage 0/1 research memory exists and tests pass.

## Context

Eternity now has a local research-memory system with typed records, deterministic IDs, SQLite storage, local note ingestion, search, digest output, and Codex task drafting. Stage 2/3 should make it scientifically useful for ultrafast ENZ research by adding structured paper-to-action translation, lab failure-mode memory, hypothesis queues, and contradiction scans.

## Goal

Turn research memory from a searchable note archive into a decision engine that produces reviewable:

- paper/action cards,
- method-transfer cards,
- lab failure-mode records,
- negative-result records,
- hypothesis records,
- contradiction/tension records,
- advisor-safe summaries,
- stronger Codex task drafts.

This stage still should not call external networks by default and should not depend on an LLM. It may include LLM-ready prompt templates, but any LLM extraction output must be explicitly marked `needs_human_review`.

## Hard constraints

- No autonomous scientific claims.
- No automatic evidence upgrade to validated status.
- No external ingest yet unless explicitly configured in a later stage.
- No lab/instrument control.
- No hidden state; all generated artifacts must be stored and reviewable.
- Existing Stage 0/1 tests and current V0 experiment runner must still pass.

## Implement these record types

Extend `records.py` with strict Pydantic models. Preserve the common base fields.

### PaperActionRecord

Fields:

```python
paper_title: str
paper_authors: list[str] = []
year: int | None = None
doi: str | None = None
arxiv_id: str | None = None
paper_url: str | None = None
main_claims: list[str]
methods: list[str]
parameters: dict[str, str] = {}
measurements: list[str]
what_eternity_can_reproduce: list[str]
what_eternity_can_adapt: list[str]
what_is_irrelevant: list[str]
suggested_simulation_tasks: list[str]
suggested_lab_tests: list[str]
suggested_codex_tasks: list[str]
caveats: list[str]
relevance_score: float | None = None
```

Evidence state defaults to `candidate_claim`.

### MethodTransferRecord

Fields:

```python
method_name: str
original_field: str
transfer_target: str
why_it_might_help: list[str]
first_synthetic_test: str | None
lab_feasibility: str | None
required_inputs: list[str]
risks_or_misfits: list[str]
suggested_codex_task: str | None
```

Evidence state defaults to `lead`.

### FailureModeRecord

Fields:

```python
symptom: str
known_observations: list[str]
likely_causes: list[str]
ruled_out_or_weakened: list[str]
diagnostic_tests: list[str]
related_runs_or_samples: list[str]
advisor_safe_wording: str | None
```

Evidence state defaults to `lab_observed` if source type is `lab_note`, otherwise `candidate_claim`.

### NegativeResultRecord

Fields:

```python
negative_result: str
why_it_matters: str
what_it_rules_out_or_weakens: list[str]
future_reuse: list[str]
related_records: list[str]
```

Evidence state defaults to `rejected_or_failed` or `lab_observed` depending on context.

### HypothesisRecord

Fields:

```python
hypothesis_id: str | None
hypothesis_statement: str
why_plausible: list[str]
what_would_support_it: list[str]
what_would_weaken_it: list[str]
next_simulation: str | None
next_lab_test: str | None
current_confidence: Literal["low", "medium", "high"] = "low"
validation_status: Literal["untested", "synthetic_only", "lab_partial", "validated", "weakened", "rejected"] = "untested"
```

Default evidence state: `validation_candidate`.

### ContradictionRecord

Fields:

```python
record_a: str
record_b: str
tension_summary: str
why_it_matters: str
possible_resolution: str | None
recommended_follow_up: str | None
severity: Literal["low", "medium", "high"] = "low"
```

Default evidence state: `lead` or `candidate_claim`.

## Add commands

```bash
eternity memory add-paper-action PAPER_NOTE_PATH [options]
eternity memory add-method-transfer NOTE_PATH [options]
eternity memory add-failure-mode NOTE_PATH [options]
eternity memory add-negative-result NOTE_PATH [options]
eternity memory add-hypothesis NOTE_PATH [options]
eternity memory hypothesis-list [--project-area AREA]
eternity memory failure-search QUERY [--project-area AREA]
eternity memory contradiction-scan [--project-area AREA] [--limit N]
eternity memory advisor-summary [--project-area AREA]
eternity memory make-codex-task RECORD_ID --task-kind simulation|analysis|plotting|ingestion|validation
```

Implementation can be template-based: parse Markdown sections by headings if present. For example, if a note contains `## Main claims`, parse bullet lists into `main_claims`. If a section is missing, leave the list empty and add a warning.

## Add template files

```text
research/templates/paper_action_template.md
research/templates/method_transfer_template.md
research/templates/failure_mode_template.md
research/templates/negative_result_template.md
research/templates/hypothesis_template.md
```

Each template should include fields users can fill manually. Do not require LLM extraction.

## Research taste scoring

Create or extend:

```text
config/research_taste.yaml
```

Suggested weights:

```yaml
weights:
  phase_sensitive_measurement: 3.0
  enz_material_response: 3.0
  broadband_ultrafast_pulses: 2.5
  reproducible_parameters: 2.0
  dispersion_vs_nonlinearity_relevance: 3.0
  frog_zscan_pumpprobe_relevance: 3.0
  simulation_module_potential: 2.0
  paper_storyline_value: 1.5
  source_trust: 2.0
negative_weights:
  no_parameters: -2.0
  pure_buzzword_match: -2.0
  wrong_regime_without_transfer_path: -1.5
  no_phase_information: -1.0
```

Implement a deterministic scoring function that can score paper/action records from tags and fields. It does not need to be perfect. It must explain the score.

Output:

```text
score: 8.5 / 10
positive factors:
- phase-sensitive measurement
- ENZ material response
- simulation module potential
negative factors:
- different material stack
```

## Contradiction/tension detection

Implement conservative contradiction scans.

Inputs:

- records in same project area,
- overlapping tags,
- evidence states,
- keywords like `failed`, `ruled out`, `supports`, `weakens`, `GDD`, `broadening`, `nonlinear`, `linear dispersion`.

Output should be a `ContradictionRecord` only when there is a plausible tension.

Example:

```markdown
## Possible tension
Earlier records describe TiN/FROG effects as simple broadening. Later records say scalar GDD-only replacement failed for B7 Run1.

## Why this matters
A broadening-only narrative may overstate the explanation and understate higher-order phase/spectral filtering/retrieval artifact possibilities.

## Safer resolution wording
TiN modifies temporal structure; in several cases the modification is not well described by uniform broadening or scalar GDD alone.

## Follow-up
Matched no-sample/TiN/neutral-mirror control at multiple pulse energies with consistent retrieval settings.
```

Do not write “contradiction proven” unless records explicitly conflict.

## Advisor-safe summary

Implement:

```bash
eternity memory advisor-summary --project-area tin_frog
```

Output sections:

```markdown
# Advisor-safe summary — <project_area>

## Known
## Likely
## Possible
## Unknown
## Weak claims to avoid
## Best next validation step
## One-sentence safe wording
```

The summary must avoid novelty claims. It should promote cautious wording like “consistent with” or “suggests” instead of “proves”.

## Enhanced Codex task generation

`make-codex-task` should tailor tasks by kind.

For simulation tasks, include:

- physical question,
- model level,
- assumptions,
- expected plots,
- validation caveats,
- success criteria,
- “do not touch lab acquisition code”.

For analysis/plotting tasks, include:

- expected input artifact paths,
- output directory,
- deterministic plotting requirements,
- report requirements.

For validation tasks, include:

- calibration/holdout warning,
- metrics,
- evidence labels.

## Tests

Add tests for:

- template parsing,
- paper/action scoring,
- failure-mode creation,
- hypothesis creation,
- contradiction scan creates conservative tension records,
- advisor summary sections exist,
- Codex task generation includes guardrails,
- all CLI commands smoke-test successfully.

## Acceptance checklist

```bash
uv run --no-editable pytest
uv run --no-editable ruff check .
uv run --no-editable eternity memory add-failure-mode research/templates/failure_mode_template.md --title "Example failure mode"
uv run --no-editable eternity memory contradiction-scan --project-area tin_frog
uv run --no-editable eternity memory advisor-summary --project-area tin_frog
```

## Final PR summary format

```markdown
## What changed
- Added paper/action, method-transfer, failure-mode, negative-result, hypothesis, and contradiction record types.
- Added template-based translators and CLI commands.
- Added research taste scoring, advisor-safe summaries, and enhanced Codex task generation.

## Scientific guardrails
- Generated records are review artifacts unless explicitly validated by serious-core workflows.
- Contradiction detector flags possible tensions, not proven contradictions.
- Advisor summaries separate known, likely, possible, and unknown.

## Validation
- `uv run --no-editable pytest`
- `uv run --no-editable ruff check .`
```
