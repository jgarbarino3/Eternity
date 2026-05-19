# Eternity Agent Rules

Eternity is a long-term personal research project for building toward an AI researcher for ultrafast ENZ optics. Treat scientific rigor as part of the product.

## Working Style

- Keep the serious physics core separate from speculative researcher-playground ideas.
- Prefer reproducible scripts, schemas, tests, and recorded artifacts over notebook-only results.
- Every scientific result should state model level, assumptions, synthetic vs measured inputs, warnings, validity envelope, and follow-up needed.
- Do not present simulation output as evidence of new physics without validation against baselines, literature, and eventually lab data.

## Post-Implementation Next-Step Rule

- After every non-trivial implementation or verification pass, recommend the next best phase from the newest implementation state, `CURRENT_REALISTIC_ROADMAP.md`, `GOALS.md`, open blockers, and any tasks explicitly skipped while waiting on information.
- Always give the recommendation a stable phase ID, such as `Phase 3`, `Phase 3A`, or `Phase 3A.1`. Reuse the existing ID from `docs/phase_index.md` when one exists; create a new suffix only when the work is genuinely a new branch or slice.
- Be direct about what is real, what is missing, what is blocked, and whether the next phase has enough information to be fully completed. Do not let deferred tasks disappear just because the current pass finished.
- State whether a planning phase is needed before implementation. Recommend reasoning effort for the assumed current model family, currently GPT-5.5, using `low`, `medium`, `high`, or `xhigh`; if planning and implementation need different effort, say both.
- Prefer quality over cost. Treat cost/usage as a tie-breaker, but do not shy away from `xhigh` for complex, ambiguous, or high-stakes planning and review. A strong default for difficult phases is often `xhigh` planning followed by `high` implementation. Avoid `xhigh` only when `medium` or `high` is clearly enough for the uncertainty and risk.
- Recommend helpful MCPs, plugins, skills, or safe local tools for the next phase. Distinguish available tools from candidates. If no obvious available tool fits, search current sources for safe installable tools or commands before recommending one.
- When benchmark values, model capabilities, pricing, or tool availability are unclear, stale, or partially legible in a local artifact, refresh from the live/current source before making the recommendation.
- Use `docs/agent_next_step_policy.md`, `docs/phase_index.md`, and `docs/agent_reasoning_effort_reference.md` as the local reference. If the user changes model families in the future, update those docs and this rule's model assumption.

## Project Atlas Maintenance Rule

- When changing Eternity strategy, major goals, evidence-promotion rules, claim-status policy, roadmap staging, Research Memory/Radar direction, or Hypothesis Harness direction, update `docs/PROJECT_ATLAS.md` and the interactive atlas in `docs/project_atlas/` in the same work.
- If the atlas is deployed, redeploy the Netlify site after atlas changes and report the live URL.
- Keep the simple roadmap, reverse mind maps, authority map, evidence ladder, and conflict board aligned with the newest repo state.

## GPD Usage Cadence Rule

GPD is a planning mirror and claim-boundary checker, not the default execution engine and not the scientific source of truth.

- Use GPD for phase planning, phase transitions, claim-status decisions, validation/promotion decisions, blocker inventory, and final scientific review.
- Use repo-local docs, scripts, tests, generated artifacts, and direct inspection for ordinary implementation, report generation, CLI plumbing, artifact inspection, atlas/docs updates, and routine verification.
- If GPD blocks on its own runtime/schema state, continue with direct repo verification when the repo evidence is sufficient, and report the GPD limitation plainly.
- Do not run a full GPD ritual just because work is research-adjacent. Bring it in when it materially reduces scientific overclaim risk or clarifies a phase decision.
- Treat `GPD/PROJECT.md`, `GPD/ROADMAP.md`, `GPD/STATE.md`, and `GPD/state.json` as mirrors that should be updated when phase state changes, but prefer the authoritative sources listed there when they disagree.

## Hard Data Availability Rule

As of 2026-05-19, the project does not have CompleteEASE access, a CompleteEASE contact, raw sample-matched TiON_48/TiON_49 R/T spectra, or permission to contact the St Andrews authors.

- Treat unavailable CompleteEASE re-exports, unavailable TiON raw R/T, and St Andrews author contact as hard constraints, not active next steps.
- Do not recommend Phase 3A clean CompleteEASE re-export, TiON raw R/T acquisition, or St Andrews author contact again unless the user supplies new information.
- Local TiON_48/TiON_49 epsilon tables may support `calibration_only_no_holdout` examples only.
- The next meaningful validation-data path after local evidence exhaustion is a literature/public-data search for a dataset with both optical constants and independent R/T or ellipsometry holdout evidence.

## Git Push Cadence Rule

- Prefer pushing coherent, verified chunks to GitHub as work progresses.
- Do not push mid-change when the worktree is still unstable, verification has not been run, or nearby files are likely to be edited again immediately.
- When holding back a push, say why and name the next verification or cleanup step that would make the branch push-ready.
- Never bundle unrelated user changes into a commit just to push. Stage only the files that belong to the finished chunk.

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
