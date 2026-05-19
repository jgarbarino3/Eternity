# Browserbase Browse Setup

Date: 2026-05-19

`browse` is installed as an optional browser-automation and Browse.sh skill
surface for Eternity agents. It is useful for repeatable read-only web tasks,
especially literature search and site-specific browser workflows. It is not a
serious-core validation dependency.

## Installed Surface

- Global CLI: `browse@0.7.2`
- Global agent skill: `~/.agents/skills/browse`
- Eternity-local Browse.sh skill:
  `.agents/skills/search-papers/SKILL.md`
- Skill lock:
  `skills-lock.json`

The Eternity-local skill is the Browserbase Browse.sh arXiv skill:

```text
arxiv.org/search-papers-zv05w6
```

It documents a read-only arXiv Atom API workflow, including query syntax,
pagination, date filtering, field-search limits, and rate-limit guidance.

## Intended Eternity Uses

- Literature/radar scouting for arXiv preprints.
- Resolving known arXiv IDs into structured metadata before creating a paper
  card or radar digest item.
- Repeatable browser smoke checks for web surfaces or public data portals when
  a Browse.sh skill exists and the workflow is read-only.
- Discovery of candidate Browse.sh skills for future public-data portals before
  writing custom browser scripts.

## Boundaries

- Do not use Browse output as serious-core validation evidence by itself.
- Do not promote research-memory records automatically from Browse results.
- Do not scrape Google Scholar; keep Scholar manual alert/export only.
- Do not run authenticated, payment, booking, or form-submission workflows
  without a separate human review gate.
- Prefer public APIs, source archives, and repo-local scripts over browser UI
  automation whenever they provide equivalent evidence.
- Browserbase cloud commands require `BROWSERBASE_API_KEY`; local mode works
  without it.

## Verification Commands

```bash
browse --version
browse doctor
browse open https://example.com --local
browse snapshot
browse stop
```
Expected local status after setup:

```text
browse/0.7.2
Browse doctor: Status ok
```

## Useful Commands

```bash
browse skills find arxiv
browse skills add arxiv.org/search-papers-zv05w6
browse open https://example.com --local
browse snapshot
browse stop
```
