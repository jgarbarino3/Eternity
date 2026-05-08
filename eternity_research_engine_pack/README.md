# Eternity Research Engine Roadmap Pack

This pack is designed to be handed to Codex as implementation guidance for adding a personal/research-memory engine to the Eternity repo without compromising Eternity's serious scientific core.

## Recommended usage

Start with this order:

1. `CODEX_PROMPT_STAGE_0_1_RESEARCH_MEMORY_FOUNDATION.md`
2. `CODEX_PROMPT_STAGE_2_3_TRANSLATORS_AND_FAILURE_ATLAS.md`
3. `CODEX_PROMPT_STAGE_4_PLUS_EXTERNAL_INGEST_GRAPH_AND_AGENT.md`

Use `ETERNITY_RESEARCH_ENGINE_ROADMAP.md` as the strategic source of truth. Use `RESEARCH_MEMORY_SCHEMA_SPEC.md` and `SOURCE_AGENT_AND_SCIENCE_POLICY.md` as constraints Codex must obey. `EXAMPLE_RECORDS_AND_OUTPUTS.md` gives concrete target outputs.

## High-level recommendation

The Twitter idea is good, but the Eternity implementation should not begin as an always-on cloud agent that reads everything and writes conclusions. Eternity should begin with a typed, local, provenance-backed research-memory layer that can later be indexed by Cognee and optionally orchestrated by Hermes/OpenClaw.

The initial value should come from five queues:

1. must-read this week,
2. possible experiment ideas,
3. possible Codex tasks,
4. contradictions / weak claims,
5. surprising outside-field connections.

The serious core remains responsible for validated material models, simulations, calibration, holdout, provenance, reports, uncertainty, and scientific conclusions. The research engine is a researcher-playground layer: it can propose, connect, critique, and draft tasks, but it must not promote an idea into validated evidence.

## Current repo assumptions used by this roadmap

As of this roadmap, Eternity is assumed to be a private repo at `jgarbarino3/Eternity`, default branch `main`. V0 is a reproducible synthetic thin-film experiment runner, not an autonomous scientist. It uses Python 3.11-3.12, Pydantic, Pint, NumPy, Matplotlib, PyYAML, TMM, Typer, Pytest, and Ruff. The CLI currently exposes `eternity validate` and `eternity run`, and runs create deterministic artifacts under `results/runs/<run_id>/`.

If the repo has changed by the time Codex receives this pack, Codex should inspect the newest repo files and adapt paths/names while preserving the scientific guardrails.
