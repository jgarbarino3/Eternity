# Eternity Feasibility Audit

Date: 2026-05-07

## Bottom Line

The Eternity vision is scientifically plausible only if the durable core is the calibrated ENZ optics environment, not the AI researcher. Current AI coding and research assistants can accelerate literature review, data ingestion, simulation plumbing, reproducible reports, parameter sweeps, code generation, test writing, and hypothesis bookkeeping. They cannot yet be trusted to autonomously discover new ultrafast ENZ physics, validate that it is novel, diagnose subtle lab artifacts, or write publishable claims without expert human review and independent experimental confirmation.

The right near-term goal is not "AI scientist writes papers." It is "validated lab memory plus reproducible simulation runs plus skepticism-enforcing reports." If that works, future models can sit on top of it. If it does not work, stronger models will only produce more convincing false positives.

## What Current Assistants Can Realistically Do

### 1. Build the research infrastructure

This is the highest-confidence use case.

Assistants can help create:

- YAML experiment specifications.
- CSV/HDF5/Parquet loaders for laser spectra, ellipsometry, pump-probe traces, and detector calibration.
- Drude and Drude-Lorentz fitting code.
- Transfer-matrix simulations.
- Plotting/report pipelines.
- Result manifests with input hashes, simulator version, git commit, parameters, plots, warnings, and validation status.
- Regression tests for numerical determinism, units, energy bookkeeping, low-loss limits, and fit reproducibility.

This is normal software engineering plus scientific computing. AI assistants are already useful here because failure can be caught with tests, plots, unit checks, and human inspection.

### 2. Keep a useful lab memory

Assistants are good at organizing documents, extracting structured metadata, summarizing papers, generating comparison tables, and linking results to source files. This can be valuable if every extracted claim has provenance and if the system stores machine-readable data rather than screenshots of plots.

Good use:

- "Find every sample with ellipsometry near 1300-1700 nm."
- "List all measurements taken at 45 degrees TM polarization."
- "Show papers that model ITO ENZ response with two-temperature hot-electron dynamics."
- "Compare our fitted plasma frequency and damping against the literature, with citations."

Bad use:

- "Tell me whether this effect is novel" without source verification and expert review.

### 3. Generate bounded hypotheses and experiment specs

Current assistants can propose hypotheses if they are forced into a narrow experimental grammar:

- State the mechanism.
- State which model predicts it.
- State the baseline that should make it disappear.
- State the observable.
- State what result would falsify it.
- State which calibration data are used and which holdout data are untouched.

This is useful even when the idea is not novel. It turns vague research thinking into runnable comparisons.

### 4. Automate first-pass simulations and sweeps

Assistants can run or script cheap sweeps across:

- Wavelength.
- Film thickness.
- incidence angle.
- polarization.
- chirp.
- fluence.
- Drude parameters.
- relaxation times.

They can also produce result dashboards and flag disagreement regions between analytic models, FDTD runs, and data. This is practical if the simulator exposes a strict result contract and logs failures rather than letting the assistant improvise.

### 5. Draft research notes

Assistants can draft internal notes, figure captions, reproducibility checklists, and paper skeletons. This should happen after the data and simulation record exist. The assistant should not invent citations, smooth over caveats, or turn weak model agreement into a discovery claim.

## What Current Assistants Cannot Reliably Do

### 1. They cannot certify new physics

An LLM can make a mechanism sound plausible. That is not evidence. For ENZ ultrafast optics, apparent novelty can come from:

- Wrong material parameters.
- Unmodeled chirp.
- pump-probe timing offsets.
- detector response.
- finite bandwidth artifacts.
- sample heating.
- damage or permanent sample change.
- roughness and interface effects.
- incorrect angle/polarization assumptions.
- numerical dispersion or boundary artifacts.
- overfitting a flexible material model.

The system can suggest "this disagreement is interesting." It cannot decide "this is new physics" without expert and experimental validation.

### 2. They cannot replace physical judgment in ENZ modeling

Generic solvers and LLM-generated code are dangerous when the material response is the hard part. Meep supports many material classes, including dispersive and nonlinear media, but ultrafast ENZ dynamics may require custom time-dependent Drude/hot-electron equations that do not map cleanly to a generic Kerr or Pockels term. A transfer-matrix model can be exactly the right baseline for linear thin films, but wrong for pump-driven time-varying media. A GNLSE-style propagation model is useful for some pulse evolution questions, but it is not automatically appropriate for subwavelength ENZ boundary-sensitive thin-film physics.

### 3. They cannot be trusted as citation or novelty judges

Recent work keeps showing that LLMs can hallucinate, overgeneralize, or miss limitations. That matters more in science than in normal writing because a subtly inflated claim can become a false discovery. Even web-enabled systems need citation verification against DOI, title, authors, year, and quoted claim.

### 4. They cannot run an autonomous lab loop safely

Even if the agent can write code, call tools, and plan experiments, it needs hard gates:

- No experiment is "validated" until a predefined acceptance test passes.
- No paper claim can cite a source that was not fetched and verified.
- No holdout data can be used during calibration.
- No surrogate result can be treated as discovery outside its training domain.
- No simulation result can omit model assumptions and known invalid regimes.

Without those gates, an autonomous research loop will optimize for plausible narratives.

## Main False-Discovery Risks

### 1. Model bias mistaken for physics

Digital-twin literature treats model bias as a central problem: discrepancies between the computational model and the real system can make calibrated predictions overconfident and unreliable. In Eternity, model bias is not a side issue. It is the main failure mode.

Examples:

- Fitting ellipsometry with an under-parameterized Drude model, then calling the residual "nonlocal response."
- Matching one pump-probe trace with a flexible hot-electron relaxation model, then extrapolating to other fluences.
- Treating a 1D model as valid for an angled TM experiment where interface fields dominate.

### 2. Leakage between calibration and validation

If the assistant sees all data while proposing the model, "prediction" becomes retrospective fitting. Keep explicit calibration and holdout splits. The system should know which data are forbidden for fitting.

### 3. Literature overclaiming

LLMs tend to compress nuance. A paper saying "consistent with hot-electron relaxation under these conditions" can become "ENZ nonlinearities are governed by hot electrons." That conversion is scientifically costly. The lab memory should store exact claim scope and source context.

### 4. Numerical artifacts

FDTD and pulse simulations can create fake effects through grid resolution, time step, PML settings, source normalization, interpolation, windowing, or Fourier transform choices. Every interesting result needs convergence checks and baseline comparisons.

### 5. Surrogate extrapolation

Surrogates are useful only inside a known training envelope. Outside that envelope they should return "out of domain," not a confident spectrum.

### 6. Human automation bias

The system will produce attractive plots and fluent explanations. That creates pressure to believe it. The UI and reports should emphasize failure modes first: assumptions, data provenance, residuals, uncertainty, and falsification tests.

## Narrow Milestones That Create Real Value Now

### Milestone 0: Source-backed lab memory

Build a local registry with strict provenance:

- Papers and notes.
- DOI/arXiv/PubMed metadata.
- exact claim extraction with page/section/source link.
- sample IDs and measurement IDs.
- raw data paths and hashes.
- plots regenerated from raw data where possible.

Deliverable: a queryable notebook where every claim points back to a source or dataset.

### Milestone 1: Linear ENZ thin-film digital twin

Implement the V0 from the roadmap:

- Drude/Drude-Lorentz material models.
- transfer matrix reflection/transmission.
- ellipsometry fitting.
- measured laser spectrum ingestion.
- predicted vs measured spectra.
- uncertainty and residual plots.
- reproducible Markdown report.

Success criterion: predict held-out low-fluence transmission/reflection for one actual sample better than a naive baseline, with documented failure cases.

### Milestone 2: Validation harness before complex physics

Before adding hot-electron dynamics, build the harness that will catch wrong claims:

- calibration/holdout split support.
- convergence tests.
- energy accounting.
- unit tests for wavelength/frequency/angular conversions.
- result manifests with input hashes.
- "known invalid" warnings in every report.

Success criterion: the system can reject its own bad runs.

### Milestone 3: Minimal hot-electron model

Add a two-temperature or reduced relaxation model only after the linear twin works.

Target one measured pump-probe dataset. Fit only a small parameter set. Compare against:

- no-pump linear baseline.
- instantaneous Kerr-only baseline if appropriate.
- plasma-frequency modulation.
- damping/scattering-rate modulation.

Success criterion: the model predicts a held-out delay, fluence, chirp, or angle setting within uncertainty.

### Milestone 4: Mechanism-separating experiment planner

Only after the above, let the AI propose experiments. Constrain it to pick experiments that distinguish mechanisms:

- What do mechanism A and B predict differently?
- Which observable separates them most?
- What existing data already answers the question?
- What is the cheapest next simulation?
- What real measurement would falsify the favored mechanism?

Success criterion: a human researcher accepts at least one proposed experiment as genuinely useful, even if it disproves the AI's preferred hypothesis.

### Milestone 5: Paper-assist mode, not paper-autonomy

Generate paper outlines and notes only from validated result manifests. The assistant can draft, but publication claims require:

- source-verified citations.
- exact data provenance.
- uncertainty and residual reporting.
- negative results.
- human signoff on novelty.

## Practical Architecture Recommendations

1. Make the AI researcher replaceable.
   The stable interfaces should be experiment specs, result manifests, lab memory, and validation reports. The model can change later.

2. Build an "anti-hype" result contract.
   Every result should include model layer, assumptions, calibrated domain, convergence status, fit residuals, known missing physics, and required follow-up.

3. Treat simple models as mandatory baselines.
   A transfer-matrix or Drude baseline is not primitive work. It is the guardrail that stops ordinary dispersion, absorption, and interference from being labeled as discovery.

4. Store raw data and regenerated plots.
   If a plot cannot be reproduced from stored data and code, it should be treated as weak evidence.

5. Enforce citation verification.
   Each citation should have DOI/arXiv/PubMed URL, title, authors, year, and the exact claim it supports. Do not let the assistant cite from memory in paper mode.

6. Prefer small, falsifiable prompts.
   Bad prompt: "Find new ENZ physics."
   Good prompt: "Given these two fitted models and this holdout delay scan, propose one simulation that best distinguishes plasma-frequency modulation from damping modulation."

7. Use multi-agent workflows only as reviewers, not authorities.
   Parallel agents can check code, citations, units, assumptions, and plots. Agreement between agents is not proof.

8. Do not fine-tune early.
   Retrieval plus structured data and tools will likely beat fine-tuning until the project has enough clean examples of correct lab-specific reasoning.

## Near-Term Build Recommendation

The next build should be `enz-digital-twin`, not `ai-researcher`.

Recommended first implementation:

- `experiments/*.yaml` for specs.
- `lab_data/registry.yaml` for samples, lasers, measurements, and paths.
- `src/eternity/materials.py` for Drude and Drude-Lorentz models.
- `src/eternity/tmm.py` for linear transfer matrix.
- `src/eternity/pulses.py` for Gaussian, chirped Gaussian, and measured-spectrum pulses.
- `src/eternity/fitting.py` for ellipsometry/material fitting.
- `src/eternity/results.py` for run manifests.
- `reports/` for generated Markdown and plots.
- `tests/` for reproducibility, units, and physics sanity checks.

The first impressive demo should be boring in the right way: load one real sample, fit its linear response, predict a held-out spectrum, produce a report that says exactly what it trusts and exactly what it does not.

## Sources

- OpenAI Responses API and tools: https://developers.openai.com/api/docs/guides/migrate-to-responses
- OpenAI Agents SDK tools: https://openai.github.io/openai-agents-js/guides/tools/
- Google Research AI co-scientist overview: https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/
- The AI Scientist v1: https://arxiv.org/abs/2408.06292
- The AI Scientist v2: https://arxiv.org/abs/2504.08066
- Why LLMs Aren't Scientists Yet: https://arxiv.org/abs/2601.03315
- Detecting hallucinations in LLMs using semantic entropy: https://www.nature.com/articles/s41586-024-07421-0
- Larger and more instructable LLMs become less reliable: https://www.nature.com/articles/s41586-024-07930-y
- Generalization bias in LLM summarization of scientific research: https://arxiv.org/abs/2504.00025
- Ten simple rules for using LLMs in science: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1011767
- Meep documentation: https://meep.readthedocs.io/
- Meep material modeling: https://meep.readthedocs.io/en/latest/Materials/
- GNLSE Python documentation: https://gnlse.readthedocs.io/en/latest/gnlse_intro.html
- Alam, De Leon, Boyd, large optical nonlinearity of ITO near ENZ: https://www.science.org/doi/10.1126/science.aae0330
- PubMed record for 2025 hot-electron ENZ dynamics paper: https://pubmed.ncbi.nlm.nih.gov/40397738/
- Time-dependent ultrafast quadratic nonlinearity in ENZ platform: https://pubmed.ncbi.nlm.nih.gov/38483127/
- Model bias in Bayesian calibration of digital twins: https://arxiv.org/abs/2312.00664
