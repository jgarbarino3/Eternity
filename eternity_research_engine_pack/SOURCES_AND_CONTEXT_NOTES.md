# Sources and Context Notes

This file records the source context used when preparing the roadmap. Codex should still inspect the live repo before implementation.

## Current Eternity repo context checked

- Repository: `jgarbarino3/Eternity`
- Visibility: private
- Default branch: `main`
- README states V0 is a reproducible synthetic thin-film experiment runner, not an autonomous scientist.
- README commands include `uv sync`, `eternity validate experiments/examples/linear_ito_toy.yaml`, and `eternity run experiments/examples/linear_ito_toy.yaml`.
- `pyproject.toml` shows package `eternity` v0.1.0, Python `>=3.11,<3.13`, dependencies `matplotlib`, `numpy`, `pint`, `pydantic`, `pyyaml`, `tmm`, `typer`, and dev dependencies `pytest`, `ruff`.
- Current CLI has `validate` and `run` commands.
- Current runner writes deterministic run artifacts including resolved spec, provenance, metrics, warnings, manifest, plots, tables, and Markdown report.

## Tool landscape checked

- Cognee is currently described as an open-source memory control plane for agents that combines embeddings, graphs, and cognitive-science approaches; docs show loading content with `cognee.add(...)` and building a graph with `cognee.cognify(...)`.
- Hermes Agent is currently described as a self-improving agent from Nous Research with a learning loop, skills, persistent memory, and provider integrations.
- OpenClaw is currently described as a multi-channel gateway/personal AI assistant for agents, with Node 24 recommended in its quick start.
- arXiv official API docs describe the query API, Atom responses, `search_query`, `start`, and `max_results`; arXiv API terms state legacy APIs including OAI-PMH, RSS, and arXiv API should make no more than one request every three seconds and use a single connection.
- Semantic Scholar's API page describes Academic Graph, Recommendations, and Datasets APIs for papers, authors, citations, venues, embeddings, and recommendations.
- OpenAlex docs describe works search and filters including `publication_year`, DOI, title/abstract search, and related/citation queries.
