# Eternity AI Research Direction Brief

**Project:** Eternity  
**Audience:** Joe + Codex / future repo agents  
**Snapshot date:** 2026-05-08  
**Status:** Strategic direction, not a frozen roadmap. This project is expected to evolve. New repo files, lab data, papers, tools, and better architectures should override this document when justified.

---

## 0. Core positioning

Eternity is not primarily trying to fine-tune an ultrafast-optics chatbot. The stronger and more realistic direction is to build a **physics-grounded scientific intelligence harness** around frontier and local models.

The base model may stay static. The *system* can still improve through:

- structured scientific memory,
- experiment/sample/material provenance,
- hypothesis cards,
- mechanism graphs,
- evaluators and falsifiers,
- simple physics tools,
- failed-hypothesis postmortems,
- context routing,
- claim-permission checks,
- and repeated comparison against synthetic and real data.

Fine-tuning may become useful later for narrow tasks such as metadata extraction, lab-note classification, schema conformance, or routine routing. It should not be treated as the main path to scientific intelligence.

---

## 1. Most original Eternity angle

> **Build a system that learns from failed ultrafast-optics hypotheses and improves its ability to choose falsifying experiments under provenance, uncertainty, and artifact constraints.**

This is the central research lane.

The generic world is already working on “AI scientist” systems, hypothesis generation, scientific agents, and multi-agent workflows. Eternity’s opportunity is narrower and deeper:

- ultrafast optics,
- ENZ/TiN thin films,
- FROG/Z-scan/ellipsometry/TMM workflows,
- real experimental ambiguity,
- material-model provenance,
- measurement artifacts,
- failed-hypothesis memory,
- and conservative claim auditing.

A generic AI scientist can say:

```text
Maybe ENZ nonlinearity caused the pulse reshaping.
```

Eternity should eventually say:

```text
That is one possible mechanism, but the current evidence does not permit that claim.
Top alternatives are higher-order linear spectral phase, FROG retrieval artifact,
bandwidth clipping, and sample/substrate effects.

The lowest-cost discriminating experiment is a fluence series at fixed center wavelength
plus retrieval-seed robustness analysis. If satellite timing is intensity-independent
but changes with wavelength detuning, higher-order linear phase strengthens and
nonlinear absorption weakens.
```

That is a qualitatively different system.

---

## 2. What is already being done elsewhere

The broad idea is not untouched. Many groups are already building scientific agents and hypothesis-generation systems. The gap is not “nobody is using AI for science.” The gap is a domain-specific, provenance-aware, artifact-aware, failure-learning AI harness for ultrafast ENZ experiments.

### 2.1 AI Scientist systems

**Sakana AI Scientist / AI Scientist-v2**  
AI Scientist-v2 is an end-to-end agentic system that formulates hypotheses, designs/runs experiments, analyzes/visualizes results, and authors manuscripts. It reports an AI-generated workshop paper accepted through peer review. The system focuses mainly on domains where experiments can be executed in code.

**Eternity takeaway:** do not copy the paper-writing layer first. Copy the discipline of full workflow traces, experiment execution, and evaluators. For Eternity, the core should be validation and claim control before manuscript generation.

Sources:
- https://arxiv.org/abs/2504.08066
- https://github.com/SakanaAI/AI-Scientist-v2
- https://sakana.ai/ai-scientist-nature/

### 2.2 Google AI co-scientist

Google’s AI co-scientist is a Gemini-based multi-agent system intended to generate novel hypotheses and research proposals from prior evidence and researcher goals, with strong emphasis on biomedical discovery.

**Eternity takeaway:** frontier labs are already attacking hypothesis generation. Eternity should differentiate by specializing in ultrafast measurement ambiguity, physical provenance, and falsifying experiment design.

Sources:
- https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/
- https://arxiv.org/abs/2502.18864

### 2.3 FutureHouse / Robin

Robin is a multi-agent scientific discovery system integrating literature search and data-analysis agents to generate hypotheses, propose experiments, interpret results, and update hypotheses in a lab-in-the-loop biomedical workflow.

**Eternity takeaway:** the valuable frontier is the iterative loop: background research → hypothesis → experiment/data analysis → updated hypothesis. Eternity should implement this loop in a physically constrained optics setting.

Sources:
- https://arxiv.org/abs/2505.13400
- https://www.futurehouse.org/research-announcements/demonstrating-end-to-end-scientific-discovery-with-robin-a-multi-agent-system

### 2.4 Scientific hypothesis-generation benchmarks

Several benchmarks now decompose scientific discovery into measurable subtasks.

- **ResearchBench** decomposes scientific discovery into inspiration retrieval, hypothesis composition, and hypothesis ranking across disciplines.
- **HypoBench** evaluates hypothesis-generation methods across practical utility, generalizability, and hypothesis discovery rate.
- **MOOSE-Chem** evaluates whether LLMs can rediscover chemistry hypotheses from background and inspirations.
- **SciMuse** combines literature knowledge graphs and LLMs to generate research ideas evaluated by research group leaders.

**Eternity takeaway:** hypothesis quality needs evals. Eternity should build ultrafast-optics-specific evals: mechanism-ranking accuracy, overclaim rate, artifact detection, falsifier quality, and experiment-selection quality.

Sources:
- https://arxiv.org/abs/2503.21248
- https://arxiv.org/abs/2504.11524
- https://arxiv.org/abs/2410.07076
- https://arxiv.org/abs/2405.17044
- https://github.com/artificial-scientist-lab/SciMuse

### 2.5 Agent learning without weight updates

Relevant agent-learning patterns already exist:

- **Reflexion:** agents improve by storing verbal reflections from feedback instead of updating weights.
- **Voyager:** an agent improves through an automatic curriculum, iterative prompting, environment feedback, and an executable skill library.
- **FunSearch:** an LLM generates candidate programs; an external evaluator scores them; evolutionary search promotes better candidates.
- **AlphaEvolve:** LLMs directly edit algorithms/code, with evaluators selecting better variants.
- **DSPy:** LM pipelines are written as modular programs and optimized against metrics, rather than relying only on handcrafted prompts.

**Eternity takeaway:** the harness can learn without fine-tuning by storing lessons, skills, tool outputs, and evaluation failures. The most promising patterns are evaluator-based search, skill libraries, and prompt/program optimization against domain metrics.

Sources:
- https://arxiv.org/abs/2303.11366
- https://arxiv.org/abs/2305.16291
- https://www.nature.com/articles/s41586-023-06924-6
- https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/
- https://arxiv.org/abs/2506.13131
- https://arxiv.org/abs/2310.03714
- https://dspy.ai/

### 2.6 Compound AI systems, memory, and context engineering

The Berkeley AI Research “compound AI systems” framing argues that many strong AI applications are systems composed of models, retrievers, tools, filters, solvers, and execution environments rather than single monolithic model calls.

Agent memory and context engineering are active areas. Current work treats memory as a write–manage–read loop, not just a vector database. Anthropic’s context-engineering guidance frames context as finite and emphasizes selecting the smallest high-signal context for the task.

**Eternity takeaway:** do not give the agent all memory every time. Give it controlled access through retrieval, auditing, status labels, and context routing.

Sources:
- https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://arxiv.org/html/2603.07670v1
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

### 2.7 Self-driving labs, materials agents, and photonics agents

Adjacent work exists in self-driving labs, materials discovery, and photonics design automation.

- A self-driving lab controlled a closed-loop ultrafast optical experiment to maximize metasurface emission directivity.
- PhIDO is a multi-agent framework for photonic integrated circuit design automation, converting natural-language PIC requests into layout mask files.
- Materials-science work is exploring LLM-generated hypotheses under goal-driven and constraint-guided workflows.
- Reviews of self-driving labs emphasize automated Design–Make–Test–Analyze loops and the need for data infrastructure, safety, and human oversight.

**Eternity takeaway:** autonomous optics and photonics agents exist, but much of the work is optimization/design/control. Eternity’s specific lane is measurement interpretation, mechanism discrimination, provenance, and failed-hypothesis learning for ultrafast ENZ experiments.

Sources:
- https://www.nature.com/articles/s41467-025-66916-0
- https://arxiv.org/abs/2508.14123
- https://pubs.aip.org/aip/aml/article/3/4/046113/3375781/AI-agents-for-photonic-integrated-circuit-design
- https://royalsocietypublishing.org/rsos/article/12/7/250646/235354/Autonomous-self-driving-laboratories-a-review-of
- https://aclanthology.org/2025.findings-naacl.420/

### 2.8 Model collapse / synthetic-data caution

Model collapse work shows that recursive training or learning from model-generated content without sufficient real-data grounding can degrade generative models. The Eternity analogue is memory poisoning: speculative AI outputs can be stored and later retrieved as if they were evidence.

**Eternity takeaway:** every memory item needs provenance and epistemic status. Speculation must not become evidence by being stored.

Sources:
- https://www.nature.com/articles/s41586-024-07566-y
- https://arxiv.org/abs/2404.01413

---

## 3. What is buildable today vs not yet

### 3.1 Buildable today

A limited but serious **Eternity Hypothesis Harness v0** is buildable now.

It can:

- store structured hypothesis cards,
- maintain a typed memory registry,
- retrieve only relevant project context,
- generate candidate mechanisms,
- critique overclaims,
- run simple TMM / phase-model / Z-scan / synthetic-data tools,
- score hypotheses against synthetic or real data,
- record failed hypotheses,
- write postmortem lessons,
- create reports with assumptions, evidence levels, and follow-up tests.

This does not require training a frontier model. It requires careful harness design, schemas, metrics, simple physics tools, and good provenance.

### 3.2 Not honestly buildable today as a solo project

A fully autonomous AI scientist that reliably invents new ultrafast physics, knows when it is wrong, safely designs/runs physical experiments, improves indefinitely, and produces validated discoveries without human review is not realistic today.

The long-term path should treat autonomy as staged:

```text
read-only lab memory
→ offline hypothesis/test suggestions
→ human-reviewed experiment plans
→ simulation-backed ranking
→ limited bounded automation
→ safety-gated closed-loop optimization
→ carefully constrained autonomy
```

---

## 4. System learning: what changes when Eternity improves?

Eternity should not define learning only as model-weight updates. In this project, learning can mean updates to:

- failed-hypothesis memory,
- mechanism graph edges,
- claim-permission rules,
- retrieval/context policy,
- evaluation cases,
- agent prompts or DSPy modules,
- reusable analysis scripts,
- experiment-prioritization rules,
- and human-reviewed scientific playbooks.

Example learning event:

```text
Mistake:
The agent inferred nonlinear ENZ dynamics from a single FROG trace.

Correction:
A single-intensity trace cannot isolate intensity-dependent physics.

Memory scar:
Do not infer nonlinear ENZ dynamics from pulse reshaping unless there is
fluence dependence, wavelength-detuning dependence, independent nonlinear
measurement, or another discriminating control.

Eval update:
Add a synthetic case where higher-order linear phase creates nonlinear-looking
pulse satellites.
```

This is the “wrong ideas leave useful scars” philosophy.

---

## 5. Core whiteboard questions

These are the questions Joe should keep thinking about. They are not solved in a plug-and-play way, especially not for ultrafast ENZ experiments.

### 5.1 What is a hypothesis as a data object?

A hypothesis should include:

- claim,
- mechanism,
- assumptions,
- predictions,
- falsifiers,
- alternative explanations,
- artifact risks,
- required evidence,
- test status,
- confidence,
- provenance,
- and next discriminating experiment.

Question:

```text
What schema makes a hypothesis testable instead of merely interesting?
```

### 5.2 How does a wrong idea leave a useful scar?

Question:

```text
When a hypothesis fails, what exactly should be written to memory so the system
avoids repeating the mistake without suppressing valid future variants?
```

A failed hypothesis should produce a future constraint, not just a summary.

### 5.3 What memory is allowed to influence conclusions?

Question:

```text
Which memory types can be used as evidence, and which can only be used as inspiration?
```

Suggested memory statuses:

```text
raw_observation
processed_result
simulation_result
hypothesis
failed_hypothesis
human_note
literature_claim
validated_claim
superseded_claim
artifact_warning
speculation
```

A speculation may inspire a future test. It should not support a scientific claim.

### 5.4 How do we rank hypotheses under sparse data?

Potential scoring terms:

```text
score = explanatory_power
      + consistency_with_data
      + consistency_with_material_model
      + falsifiability
      + simplicity
      + expected_testability
      - artifact_risk
      - parameter_degeneracy
      - unsupported_assumptions
      - experiment_cost
```

Question:

```text
Can Eternity rank mechanisms without overclaiming when the data are ambiguous?
```

### 5.5 How does Eternity choose the next experiment?

The agent should prefer discriminating tests, not vague “take more data.”

Question:

```text
What experiment best separates the top two mechanisms per unit cost, time, and risk?
```

Candidate score:

```text
experiment_score = mechanism_separation
                 + expected_information_gain
                 + feasibility
                 + safety
                 + cost_efficiency
                 - artifact_risk
                 - ambiguity_remaining
```

Example ENZ case:

```text
Mechanism A: higher-order linear phase.
Mechanism B: intensity-dependent nonlinear response.

Discriminating experiments:
- fluence series at fixed center wavelength,
- wavelength-detuning series at fixed fluence,
- input chirp scan,
- blank substrate control,
- repeat FROG retrieval with seed/noise robustness.
```

### 5.6 What is the minimal context needed?

Question:

```text
What is the smallest high-signal context needed for this task?
```

For a new FROG trace, likely context:

- sample card,
- experiment card,
- input pulse card,
- material model card,
- prior failed hypotheses for this sample or measurement type,
- active artifact warnings,
- current analysis tools,
- claim-permission rules.

### 5.7 When is the system allowed to make a claim?

Suggested claim levels:

```text
speculation
plausible_mechanism
weakly_supported
simulation_supported
single_measurement_supported
control_supported
validated_across_conditions
paper_claim_candidate
```

Question:

```text
What evidence is required to move a claim from one level to the next?
```

Example:

```text
“Pulse reshaping observed”
  → valid FROG measurement and preprocessing record.

“Scalar GDD insufficient”
  → baseline fit failure with residuals and uncertainty.

“Higher-order spectral phase plausible”
  → model reproduces trace features and survives holdout/noise checks.

“Nonlinear ENZ dynamics”
  → intensity dependence plus controls and alternative mechanisms weakened.

“Novel mechanism”
  → literature check, independent validation, controls, expert review.
```

### 5.8 How do we prove the agent improves?

Candidate metrics:

- mechanism-ranking accuracy,
- overclaim rate,
- missing-control detection,
- artifact-detection rate,
- falsifier quality,
- experiment-selection quality,
- retrieval relevance,
- repeated-failure rate,
- human usefulness score,
- cost per useful hypothesis.

Question:

```text
What is the ultrafast-optics equivalent of a benchmark score?
```

---

## 6. Proposed harness architecture

A good first architecture is not a single mega-agent. It is a controlled scientific loop.

```text
User / research question
        ↓
Orchestrator
        ↓
Context Router
  - decides what memory/tools are relevant
        ↓
Memory Auditor
  - retrieves context
  - checks provenance and epistemic status
  - blocks speculation from being treated as evidence
        ↓
Hypothesis Generator
  - proposes mechanism-specific hypotheses
        ↓
Skeptic / Artifact Agent
  - asks: what simpler mechanism or artifact explains this?
        ↓
Experiment Designer
  - proposes discriminating tests
        ↓
Simulation / Analysis Tool Runner
  - TMM, phase fitting, Z-scan fitting, synthetic benchmarks, unit checks
        ↓
Claim Auditor
  - checks whether the conclusion is allowed
        ↓
Memory Writer
  - stores hypothesis, result, failure, lesson, provenance
```

The source of truth should be:

```text
validated data
provenance
deterministic tool outputs
explicit uncertainty
human decisions
```

LLMs propose, critique, structure, and route. They do not become the source of scientific truth.

---

## 7. Memory design

Eternity should have access to memory, not automatic exposure to all memory.

Suggested layers:

```text
Raw archive:
  immutable raw files, scans, logs, traces, metadata, hashes.

Structured registry:
  samples, experiments, runs, artifacts, units, dates, provenance.

Semantic memory:
  validated mechanisms, material-model facts, known constraints.

Episodic memory:
  prior attempts, failed hypotheses, debugging stories, lab narratives.

Procedural memory:
  scripts, tools, analysis recipes, reusable prompts, playbook rules.

Working context:
  only the current task’s minimal relevant subset.
```

Memory entry fields should include at least:

```text
id
type
status
title
summary
source_refs
created_at
updated_at
related_samples
related_experiments
validity_scope
evidence_level
supersedes
superseded_by
human_review_status
risk_flags
```

---

## 8. First benchmark ideas

### 8.1 Do-not-overclaim ENZ benchmark

Synthetic scenarios:

```text
A. scalar GDD only
B. higher-order spectral phase
C. nonlinear absorption
D. intensity-dependent refractive index
E. bandwidth clipping
F. FROG retrieval instability
G. sample/substrate artifact
H. mixed mechanism with insufficient data
```

Agent must output:

```text
ranked mechanisms
simplest explanation
missing controls
predictions
falsifiers
next experiment
claim permission level
```

Metrics:

```text
mechanism-ranking accuracy
overclaim rate
artifact-awareness score
falsifier quality
missing-control detection
```

### 8.2 Best-next-experiment benchmark

Input:

```text
Current data allow mechanisms A and B.
Available experiments have cost, time, risk, and expected signal profiles.
```

Agent must choose the experiment that best separates A and B.

Metrics:

```text
expected information gain
mechanism separation
cost-normalized utility
safety/feasibility compliance
```

### 8.3 Failed-hypothesis memory benchmark

Run a sequence of related cases. Measure whether the agent:

```text
retrieves the relevant failed hypothesis,
avoids repeating the invalid claim,
keeps valid neighboring hypotheses alive,
updates confidence appropriately,
and writes a useful postmortem.
```

---

## 9. First implementation milestones

### Milestone 0: repo hygiene and schemas

- Add hypothesis-card schema.
- Add memory-card schema.
- Add claim-level enum.
- Add mechanism/artifact taxonomy.
- Add unit/provenance conventions.

### Milestone 1: synthetic hypothesis benchmark

- Create 10–20 toy ultrafast optics cases.
- Use simple synthetic observations.
- Define ground-truth mechanism labels.
- Define expected correct/incorrect reasoning patterns.
- Score agent outputs.

### Milestone 2: minimal harness loop

- Generate hypothesis cards.
- Critique hypothesis cards.
- Propose discriminating tests.
- Score against synthetic benchmark.
- Store failure lessons.

### Milestone 3: simple physics tools

- TMM baseline wrapper.
- Polynomial spectral phase/pulse propagation toy model.
- Scalar GDD vs TOD/FOD comparison.
- Z-scan fitting baseline.
- FROG retrieval robustness checklist or parser.

### Milestone 4: memory auditor

- Retrieve memory candidates.
- Filter by provenance, status, sample, experiment type, and validity scope.
- Prevent speculation from entering evidence tables.

### Milestone 5: research radar

- Scan papers/posts on scientific agents, memory, hypothesis benchmarks, self-driving labs, photonics agents, and ultrafast ML.
- Classify each item by actionability for Eternity.
- Write periodic Markdown digests or GitHub issues.

---

## 10. Codex implementation posture

Codex should treat this as a strategic brief, not a mandate to build everything at once.

For any implementation task:

1. Prefer small, testable modules.
2. Add schemas before complex agents.
3. Add evals before optimization.
4. Preserve provenance and units.
5. Keep synthetic outputs clearly labeled as synthetic.
6. Do not convert speculative agent text into validated claims.
7. Create deterministic artifacts where possible.
8. Write reports that include assumptions, warnings, and validity envelopes.
9. Use latest repo files and user instructions over this document if they conflict.
10. Leave extension points for future models and better AI tools.

Codex-specific references:

- Codex can read, edit, and run code, and can adapt to existing repo structure: https://developers.openai.com/codex
- Codex CLI can run locally from the terminal: https://developers.openai.com/codex/cli
- Codex can use `AGENTS.md` for repo-specific instructions: https://developers.openai.com/codex/guides/agents-md
- Codex skills can package repeatable workflows: https://developers.openai.com/codex/skills
- Codex subagents can be used for parallel/specialized code workflows when useful: https://developers.openai.com/codex/subagents

---

## 11. Research radar themes

The scanner should prioritize papers/posts under these themes:

```text
scientific_ai_agents
hypothesis_generation
scientific_hypothesis_benchmarks
agent_memory
context_engineering
failed_hypothesis_learning
claim_verification
compound_ai_systems
evaluator_based_search
self_driving_labs
bayesian_experiment_design
active_learning_for_experiments
materials_hypothesis_generation
photonics_agents
ultrafast_ml
frog_retrieval_ml
zscan_analysis_ml
enz_material_modeling
```

Each radar item should answer:

```text
What does this do?
What problem does it solve?
What is the evaluator or feedback signal?
What memory/state improves over time?
What could transfer to Eternity?
What is the smallest Eternity experiment inspired by it?
What are the risks or limitations?
Should we act now, save for later, or ignore?
```

---

## 12. Working thesis

The central bottleneck is not “can the model think?” but:

```text
Can Eternity structure scientific work so that every wrong idea creates a useful trace,
every claim knows its evidence level, and every next experiment is chosen to reduce
mechanism ambiguity rather than produce more pretty plots?
```

If yes, the system can become more scientifically useful over time even before any model weights are fine-tuned.

That is the whiteboard.
