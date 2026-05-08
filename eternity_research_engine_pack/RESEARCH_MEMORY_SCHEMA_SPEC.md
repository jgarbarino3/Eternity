# Research Memory Schema Spec

This spec defines the intended data model for Eternity's research-memory layer.

## Design principle

Every memory item is a reviewable record with provenance. Retrieval and graph systems index these records; they do not replace them.

```text
raw source -> raw hash/provenance -> typed record -> index/search -> digest/action -> human review -> serious-core validation
```

## Common fields

All records should include:

```yaml
schema_version: "0.1"
record_type: paper_action | method_transfer | lab_observation | failure_mode | negative_result | hypothesis | contradiction | codex_task | digest | source
record_id: rm_<type>_<hash12>
title: string
summary: string
body: string
source_type: peer_reviewed_paper | preprint | instrument_manual | lab_note | simulation_artifact | conference_talk | newsletter | twitter_lead | agent_summary | codex_task | other
evidence_state: lead | background | candidate_claim | lab_observed | simulation_unvalidated | validation_candidate | validated_with_holdout | rejected_or_failed | deprecated
review_state: needs_human_review | reviewed | approved_for_codex | approved_for_lab_planning | archived
project_areas: []
tags: []
related_record_ids: []
raw_artifact_hash: sha256 or null
source_locator: URL/path/DOI/arXiv ID/manual section/etc.
created_at: ISO timestamp
updated_at: ISO timestamp
assumptions: []
warnings: []
```

## Evidence-state meanings

### `lead`

Interesting but unverified. Use for Twitter/X, newsletters, new papers, method-transfer ideas, and candidate connections.

### `background`

Useful context but not a direct claim/action.

### `candidate_claim`

A claim extracted from a paper/manual/note that needs verification before use.

### `lab_observed`

Something observed in lab notes or data. This does not automatically mean the interpretation is correct.

### `simulation_unvalidated`

Synthetic or model output without calibration/holdout validation.

### `validation_candidate`

A hypothesis or proposed experiment/simulation ready for validation planning.

### `validated_with_holdout`

Reserved for serious-core validation workflows with calibration/holdout integrity. Research-memory commands should not create this by default.

### `rejected_or_failed`

Negative result, failed hypothesis, ruled-out model, or failed implementation.

### `deprecated`

Preserved for history but no longer recommended.

## Record types

### SourceRecord

Purpose: source metadata and provenance.

```yaml
record_type: source
source_kind: arxiv | semantic_scholar | openalex | local_file | manual | newsletter | social | other
canonical_id: DOI/arXiv/URL/path/etc.
retrieved_at: timestamp
raw_metadata_hash: sha256
license_notes: string
trust_notes: string
```

### PaperActionRecord

Purpose: paper-to-experiment/simulation/task translator.

```yaml
record_type: paper_action
paper_title: string
paper_authors: []
year: 2026
doi: null
arxiv_id: null
paper_url: null
main_claims: []
methods: []
parameters: {}
measurements: []
what_eternity_can_reproduce: []
what_eternity_can_adapt: []
what_is_irrelevant: []
suggested_simulation_tasks: []
suggested_lab_tests: []
suggested_codex_tasks: []
caveats: []
relevance_score: null
```

### MethodTransferRecord

Purpose: find methods from adjacent fields that could transfer into Eternity.

```yaml
record_type: method_transfer
method_name: ptychographic temporal reconstruction
original_field: attosecond / ultrafast pulse metrology
transfer_target: FROG robustness for broadband ENZ-centered pulses
why_it_might_help: []
first_synthetic_test: string
lab_feasibility: string
required_inputs: []
risks_or_misfits: []
suggested_codex_task: string
```

### LabObservationRecord

Purpose: preserve observed facts from lab notes.

```yaml
record_type: lab_observation
sample_ids: []
run_ids: []
instruments: []
observed_behavior: string
raw_data_refs: []
preprocessing_refs: []
interpretation_status: observed_not_explained | partially_explained | contested | obsolete
```

### FailureModeRecord

Purpose: searchable failure atlas.

```yaml
record_type: failure_mode
symptom: string
known_observations: []
likely_causes: []
ruled_out_or_weakened: []
diagnostic_tests: []
related_runs_or_samples: []
advisor_safe_wording: string
```

### NegativeResultRecord

Purpose: preserve what failed and why it matters.

```yaml
record_type: negative_result
negative_result: string
why_it_matters: string
what_it_rules_out_or_weakens: []
future_reuse: []
related_records: []
```

### HypothesisRecord

Purpose: ranked hypothesis queue.

```yaml
record_type: hypothesis
hypothesis_id: H-014
hypothesis_statement: string
why_plausible: []
what_would_support_it: []
what_would_weaken_it: []
next_simulation: string
next_lab_test: string
current_confidence: low | medium | high
validation_status: untested | synthetic_only | lab_partial | validated | weakened | rejected
```

### ContradictionRecord

Purpose: detect narrative conflicts or weak claims.

```yaml
record_type: contradiction
record_a: rm_...
record_b: rm_...
tension_summary: string
why_it_matters: string
possible_resolution: string
recommended_follow_up: string
severity: low | medium | high
```

### CodexTaskRecord

Purpose: convert research memory into implementation tasks.

```yaml
record_type: codex_task
goal: string
context: string
source_record_ids: []
inputs: []
expected_outputs: []
success_criteria: []
do_not: []
scientific_guardrails: []
```

### DigestRecord

Purpose: keep weekly/home-screen outputs auditable.

```yaml
record_type: digest
digest_kind: weekly | home | project_area | advisor_summary
included_record_ids: []
queues:
  must_read: []
  experiment_ideas: []
  codex_tasks: []
  weak_claims: []
  surprising_connections: []
warnings: []
```

## Research taste scoring

Scoring should be explicit and explainable. Suggested factors:

```yaml
positive:
  phase_sensitive_measurement: 3.0
  enz_material_response: 3.0
  broadband_ultrafast_pulses: 2.5
  reproducible_parameters: 2.0
  dispersion_vs_nonlinearity_relevance: 3.0
  frog_zscan_pumpprobe_relevance: 3.0
  simulation_module_potential: 2.0
  paper_storyline_value: 1.5
  source_trust: 2.0
negative:
  no_parameters: -2.0
  pure_buzzword_match: -2.0
  wrong_regime_without_transfer_path: -1.5
  no_phase_information: -1.0
```

The score is not truth. It is prioritization.

## Required warnings

Records should add warnings when appropriate:

- `unreviewed_llm_extraction`
- `social_source_low_trust`
- `paper_regime_mismatch`
- `no_reproducible_parameters`
- `simulation_not_validated`
- `lab_observation_not_interpretation`
- `possible_retrieval_artifact`
- `possible_alignment_artifact`
- `holdout_not_used`
- `copyright_or_license_unclear`

## Minimum provenance requirements

Every record must be able to answer:

1. Where did this come from?
2. When was it retrieved or written?
3. What raw artifact or source is it tied to?
4. What is its evidence state?
5. Who/what generated the extraction?
6. What assumptions or warnings are attached?
7. What should be done next before trusting it?
