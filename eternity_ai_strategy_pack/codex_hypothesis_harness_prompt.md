# Paste-Ready Codex Prompt: Build Eternity Hypothesis Harness v0

You are working in the Eternity repo, a long-term AI-assisted ultrafast ENZ optics research project. The goal is not to build a generic chatbot. The goal is to build a physics-grounded scientific harness that helps generate, test, critique, and remember hypotheses for ENZ/TiN ultrafast experiments under provenance, uncertainty, and artifact constraints.

Use the latest repo files and user instructions as the source of truth. This prompt is strategic context, not immutable law.

## Core idea

The most original Eternity angle is:

> Build a system that learns from failed ultrafast-optics hypotheses and improves its ability to choose falsifying experiments under provenance, uncertainty, and artifact constraints.

## v0 goal

Implement the smallest useful hypothesis harness:

1. A hypothesis-card schema.
2. A memory-card or failed-hypothesis schema.
3. A claim-level enum.
4. A mechanism/artifact taxonomy seed.
5. A synthetic benchmark with 5–10 toy cases.
6. A scoring script that can evaluate structured agent outputs.
7. A Markdown report generator summarizing hypotheses, evidence level, failure lessons, and next tests.

## Scientific rules

- Do not treat synthetic data as lab evidence.
- Do not treat model-generated speculation as evidence.
- Every hypothesis must include assumptions, predictions, falsifiers, alternatives, artifact risks, and proposed discriminating tests.
- Every conclusion must have a claim level.
- Every memory item must have provenance and epistemic status.
- Prefer simple physics baselines before complex models.
- Keep all units explicit.
- Keep artifacts deterministic when possible.

## Suggested first files

```text
eternity_ai/
  README.md
  schemas/
    hypothesis_card.schema.yaml
    memory_card.schema.yaml
    claim_levels.yaml
    mechanism_taxonomy.yaml
  evals/
    synthetic_cases.yaml
    score_hypothesis_cards.py
    README.md
  memory/
    failed_hypotheses.example.jsonl
    lessons.example.jsonl
  reports/
    report_template.md
    render_eval_report.py
  tools/
    toy_phase_model.py
    toy_zscan_baseline.py
```

## First synthetic cases

Create simple benchmark cases around:

- scalar GDD only,
- higher-order spectral phase,
- nonlinear absorption,
- intensity-dependent refractive index,
- bandwidth clipping,
- FROG retrieval instability,
- sample/substrate artifact,
- mixed mechanism with insufficient data.

Each case should include:

- observation text,
- available context,
- hidden ground-truth mechanism,
- expected correct answer features,
- overclaim patterns to penalize,
- missing controls,
- recommended next experiment.

## Metrics

Score at least:

- mechanism-ranking accuracy,
- overclaim penalty,
- artifact-awareness score,
- falsifier quality,
- missing-control detection,
- claim-level appropriateness,
- memory-scar usefulness.

## Implementation style

Start small. Do not implement a full autonomous agent yet. Build schemas, test cases, scoring, and deterministic report generation first. Leave clean extension points for future LLM calls, retrieval, DSPy optimization, and physics tools.
