# OpenClaw Research Radar Policy

OpenClaw can be useful as an orchestration layer for the weekly Eternity radar,
especially now that it can use OpenAI OAuth. It should remain a thin caller
around the repo-native CLI and Codex web-search digest workflow.

## Allowed v1 Commands

```bash
uv run --no-editable eternity memory radar validate-config config/research_radar.example.yaml
uv run --no-editable eternity memory radar scan --config config/research_radar.example.yaml --dry-run
uv run --no-editable eternity memory radar digest --run-dir <run-dir>
uv run --no-editable eternity memory search research_memory/examples "<query>"
uv run --no-editable eternity memory show <record-id> --dir research_memory/examples --json
```

## Not Allowed In v1

- Automatic `radar promote`.
- Repo edits or pull requests from a radar item.
- Evidence-state upgrades.
- Serious-core conclusions.
- Lab, instrument, browser-login, inbox, or private-document access.
- Google Scholar scraping.

## Weekly Codex Web-Search Prompt

Use this as the scheduled Codex/OpenClaw task prompt:

```text
Run the Eternity weekly research radar for /Users/joegarbarino/Desktop/Eternity.

1. Use `uv run --no-editable eternity memory radar validate-config config/research_radar.example.yaml`.
2. Use Codex web search for the recurring queries in `config/research_radar.example.yaml`, prioritizing arXiv, OpenReview, ACL Anthology, Hugging Face Papers, Papers with Code, Nature Machine Intelligence, Nature Communications, Science Advances, ACS Photonics, Optica/OSA, AIP/APL Photonics/APL Machine Learning, and npj Computational Materials.
3. Do not use an OpenAI/model API key. Use rules/templates only.
4. Classify leads A-E and by the configured themes.
5. Write a Markdown digest under `results/research_memory/radar/` and update `results/research_memory/radar/latest.md`.
6. The digest must include: Why this matters for Eternity, Possible experiment, Possible code module, Risk / limitation, and Should we act now for all A and strong B items.
7. State that the digest is a review queue, not validated evidence.
8. End by asking whether selected A items should be manually promoted into research-memory records or Codex task drafts.

Do not promote records, edit code, open PRs, or claim scientific validation.
```
