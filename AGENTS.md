# Eternity Agent Rules

Eternity is a long-term personal research project for building toward an AI researcher for ultrafast ENZ optics. Treat scientific rigor as part of the product.

## Working Style

- Keep the serious physics core separate from speculative researcher-playground ideas.
- Prefer reproducible scripts, schemas, tests, and recorded artifacts over notebook-only results.
- Every scientific result should state model level, assumptions, synthetic vs measured inputs, warnings, validity envelope, and follow-up needed.
- Do not present simulation output as evidence of new physics without validation against baselines, literature, and eventually lab data.

## Pro Model Checkpoint Rule

Use checkpoint gates for hard, abstract, or unknown-territory work. When a checkpoint is warranted, say exactly:

> Pro checkpoint recommended

Then explain why in 2-4 bullets and give a compact prompt the user can paste into 5.5 Pro or whatever the current best Pro reasoning model is.

Trigger a checkpoint before:

- Unknown physics/modeling choices.
- Major architecture decisions that will be hard to reverse.
- Surprising simulation results.
- Possible novelty claims.
- Failed validation loops where the reason is unclear.
- Phase transitions such as V0 to V1, linear to nonlinear, or local simulator to FDTD.

Do not interrupt routine implementation for Pro input.

