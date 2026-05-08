# Pro Checkpoint Prompt for Eternity Research Engine

Pro checkpoint recommended

## Why this is a checkpoint

This integration is a major architecture decision for Eternity. It changes Eternity from a pure reproducible simulation/report runner into a broader research-memory and agent-facing system. If done wrong, it can create a persuasive but scientifically unsafe layer that blurs source notes, hypotheses, simulations, and validated evidence.

## Decision needing deeper reasoning

Decide the long-term boundary between:

1. local typed records as the source of truth,
2. graph/semantic memory such as Cognee as an index,
3. cloud agents such as Hermes/OpenClaw as orchestration/front end,
4. Eternity serious-core validation workflows.

The key question is how much automation to allow at each stage without weakening provenance, review, validation, and security.

## Context needed

- Latest Eternity repo tree and current tests.
- Existing artifact layout under `results/runs/<run_id>/`.
- Planned V1 registry/calibration/holdout data contracts.
- Whether research-memory records should be committed to git or kept local/private.
- Which external sources are actually needed first: arXiv, Semantic Scholar, OpenAlex, RSS, newsletters, local manuals, lab notes.
- Whether the user wants Hermes/OpenClaw now or only after local workflows are proven.
- Privacy/security constraints for lab notes, emails, Twitter/X, manuals, and cloud agents.

## Paste-ready prompt for a Pro reasoning model

```text
You are advising the Eternity project, a long-term AI-assisted ultrafast ENZ optics research platform. Current V0 is a deterministic synthetic linear thin-film/TMM runner with explicit schemas, units, provenance, reports, and tests. The user wants to add a personal research engine inspired by cloud agents + memory systems + recurring ingest + digest/search skills.

Evaluate the proposed architecture:

- local typed research-memory records as source of truth,
- SQLite/JSON artifacts and hashes for provenance,
- paper-to-action translator,
- lab failure atlas,
- hypothesis queue,
- contradiction detector,
- weekly digest/home queues,
- optional external ingest later,
- optional Cognee graph memory as index only,
- optional Hermes/OpenClaw as read-only/draft-only orchestrator.

Please critique this architecture for scientific validity, software architecture, security, future extensibility, and integration with the existing Eternity serious core. Identify the biggest irreversible decisions, hidden risks, simpler alternatives, and validation gates. Recommend a staged implementation plan and explicit "do not implement yet" boundaries. Keep the answer specific to ultrafast ENZ optics workflows: FROG, Z-scan, pump-probe, TiN/ITO/AZO thin films, material-model provenance, calibration/holdout, simulation artifacts, and lab failure memory.
```
