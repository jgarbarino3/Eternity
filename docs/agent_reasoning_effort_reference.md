# GPT-5.5 Reasoning Effort Reference

Date: 2026-05-16

Source inspected once for this repo: `AI Model & API Providers Analysis _ Artificial Analysis.pdf` in the Eternity root. It is a printed Artificial Analysis web page captured on 2026-05-16 with GPT-5.5 effort variants selected. Extraction used `pdfinfo`, `pdftotext`, and rendered page images.

Use this as a practical local policy aid, not as a live benchmark feed. Some charts in the PDF are horizontally clipped, so unclear values were refreshed from the live Artificial Analysis model pages on 2026-05-16. If a future decision depends on current benchmark values, refresh from live sources again.

Live source pages checked for unclear values:

- `https://artificialanalysis.ai/models/gpt-5-5`
- `https://artificialanalysis.ai/models/gpt-5-5-high`
- `https://artificialanalysis.ai/models/gpt-5-5-medium`
- `https://artificialanalysis.ai/models/gpt-5-5-low`

## Visible GPT-5.5 Signals

| Signal | xhigh | high | medium | low | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| Artificial Analysis Intelligence Index | 60 | 59 | 57 | 51 | PDF plus live model pages. |
| Output speed, tokens/s | 65.3 | 63.0 | 60.0 | 60.8 | Live model pages; values drift slightly from the printed PDF snapshot. |
| Cost to run Intelligence Index, USD | 3,357.00 | 2,159.38 | 1,199.14 | 500.67 | Embedded live page data; not the same as API token price. |
| Tokens used for Intelligence Index | 75M total | 45M total | 22M total | 7.0M total | Live model pages. The PDF visibly splits xhigh as about 68M answer + 7.5M reasoning and high as about 39M answer + 5.9M reasoning. |
| API price components, USD / 1M tokens | cache 0.5, input 5, output 30 | cache 0.5, input 5, output 30 | cache 0.5, input 5, output 30 | cache 0.5, input 5, output 30 | Live model pages; blended 3:1 input-output price is 11.25 USD / 1M tokens for all four. |
| Artificial Analysis Coding Agent Index | not shown | not shown | Codex 60; Cursor CLI 58 | not shown | Coding-agent chart compares agent products, not just raw model effort. |

## Visible Evaluation Breakdown

The breakdown charts compare GPT-5.5 effort variants directly. Values below are percentages from visible bar labels.

| Evaluation | xhigh | high | medium | low |
| --- | ---: | ---: | ---: | ---: |
| GDPval-AA | 63 | 63 | 58 | 47 |
| Terminal-Bench Hard | 61 | 60 | 58 | 52 |
| tau2-Bench Telecom | 94 | 93 | 92 | 84 |
| AA-LCR | 74 | 73 | 72 | 72 |
| AA-Omniscience Accuracy | 57 | 56 | 56 | 54 |
| AA-Omniscience Non-Hallucination Rate | 14 | 14 | 14 | 14 |
| Humanity's Last Exam | 44 | 43 | 41 | 31 |
| GPQA Diamond | 94 | 93 | 93 | 91 |
| SciCode | 56 | 56 | 53 | 52 |
| IFBench | 76 | 72 | 71 | 64 |
| CritPt | 27 | 25 | 19 | 8 |
| MMMU-Pro | 81 | 81 | 80 | 79 |

## Eternity Recommendation Policy

Use GPT-5.5 `medium` by default for ordinary coding, docs, and verification when the plan is already clear.

Use GPT-5.5 `high` for most serious Eternity implementation work: schema changes, registry/data provenance, physics-contract edits, validation triage, roadmap updates, and anything that must preserve scientific claim boundaries.

Use GPT-5.5 `xhigh` confidently for hard planning and reasoning checkpoints: moving from synthetic to measured evidence, deciding pass/fail gates, interpreting surprising physics results, choosing model families, reviewing claim promotion, or planning multi-stage work with many unknowns. A particularly good split for complex work is `xhigh` planning followed by `high` implementation.

Use GPT-5.5 `low` only when the task is narrow, reversible, and mostly mechanical.

Quality is the primary objective. Cost and usage are secondary. The right recommendation should spend `xhigh` when it materially improves planning or review, while still avoiding it for narrow mechanical work where `medium` or `high` is clearly enough.
