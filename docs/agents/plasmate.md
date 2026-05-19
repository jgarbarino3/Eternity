# Plasmate MCP Usage

Date: 2026-05-19

Plasmate is available as an optional MCP surface for Eternity read-only web
inspection. Use it more often alongside Browse.sh when literature sweeps or
public-data triage benefit from quick page text extraction or lightweight
persistent browser sessions.

## Intended Eternity Uses

- Extract readable text from candidate paper, repository, dataset, supplement,
  and source-data pages.
- Quickly inspect public pages before deciding whether a heavier Browse.sh,
  download, or repo-local ingestion step is worth doing.
- Cross-check whether public-data claims in papers point to actual downloadable
  artifacts.
- Seed Research Memory/Radar records, candidate cards, and follow-up tasks.

## Boundaries

- Plasmate output is discovery evidence, not serious-core validation evidence.
- Do not promote a dataset or claim from Plasmate text alone.
- Prefer downloaded files, checksums, machine-readable tables, repo scripts, and
  explicit source citations for validation artifacts.
- Do not use Plasmate for authenticated, payment, form-submission, or
  rate-sensitive scraping workflows without a separate human review gate.

## Verified Smoke

The `extract_text` tool successfully extracted readable text from
`https://example.com` in this repo session.
