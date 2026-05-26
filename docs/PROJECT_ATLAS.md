# Eternity Project Atlas

The Project Atlas is the durable map for understanding Eternity as one system
with three authority-separated lanes:

- **Serious Core**: calibrated ENZ digital twin, registry, material models,
  calibration/holdout, validation gates, reports, and claim status.
- **Research Memory / Radar**: paper cards, lab observations, failure modes,
  contradictions, weak-claim queues, digests, Codex task drafts, and optional
  Browse.sh/Plasmate-assisted read-only scouting.
- **Hypothesis Harness**: hypothesis cards, mechanism ranking, artifact
  skepticism, falsifiers, failed-hypothesis memory, and harness scores.

Open the interactive atlas locally:

```text
docs/project_atlas/index.html
```

The atlas is organizational and visual. It does not change claim-status logic,
research-memory schemas, or scientific validation behavior.

## Simple Roadmap

The first goal is:

```text
First calibrated linear ENZ digital twin checkpoint
```

That means: given one identified sample and optical setup, use
calibration-only optical data to fit or load a physically constrained material
model, freeze that model, predict an independent holdout measurement, and emit a
bounded claim status.

Current progress:

- **Done**: V0 synthetic runner and V1 contract scaffolding.
- **Done**: Phase 3C public TiN dataset intake after Phase 3A exhaustion:
  the St Andrews 2025 public TiN archive and linked paper are snapshotted, and
  the dataset includes ellipsometry tables plus `RT.xlsx` R/T data.
- **Done**: Phase 3C.1 St Andrews TiN pairing + validation candidate:
  canonical R/T CSV snapshots, the candidate `50nm-MTiN-50c` epsilon snapshot,
  registry records, and a fail-closed example now exist.
- **Done**: Phase 3C.2 St Andrews candidate run audit + future-only threshold
  policy. The existing St Andrews run is non-promotable and a clean future run
  is required after any threshold lock.
- **Done**: Phase 3C.3 St Andrews threshold lock + clean run decision. The
  clean run failed all five predeclared reflectance metrics and cannot move to
  Phase 4 as-is.
- **Done**: Phase 3C.4 St Andrews failure triage. The failure is not a near
  miss, blue-edge residuals dominate, no alternate St Andrews epsilon table
  passes the locked thresholds, and simple thickness/substrate sweeps do not
  repair the shape or dip.
- **Done**: Phase 3C.5 St Andrews source-model parity diagnostic. Raw Woollam
  `.mod/.SE` inspection found Float Glass Cauchy substrate,
  film-thickness/roughness metadata, and back-reflection settings missing from
  the clean-run stack.
- **Done**: Phase 3C.6A bounded St Andrews source-model parity implementation.
  Source Cauchy substrate, inferred source thickness, approximate roughness,
  and approximate backside variants all failed the locked thresholds; exact
  roughness/back-reflection parity remains underdetermined.
- **Done**: Phase 3B.1 TiON evidence reality check / digitized plot intake.
  TiON_48/TiON_49 epsilon tables, material models, and calibration-only
  examples are available; no raw R/T measurements or repo-local digitizable
  plot candidates were found.
- **Done**: Phase 3D.1B Exeter/Bohn no-fit static R0 extraction and split lock.
  Figure 1 epsilon, Figure 2 TIR reference, and Figure 2 static pre-pump `R0`
  are canonical artifacts now, and the split-lock YAML forbids residual-driven
  tuning.
- **Done**: Phase 3D.1C Exeter/Bohn package-constant no-fit model
  reconstruction. The static pattern reconstructs well in shape, but absolute
  residuals are nontrivial and the result remains non-promoting.
- **Done/source-exported**: Phase 3D.2/3E.3 Saha TiN/AZO source-data intake.
  Figshare source files are public and hash-verified; Fig. 2b and Fig. 2c/d
  now have Windows Origin Viewer CSV exports with measured/simulated
  reflectance labels, TiN/AZO permittivity labels, and thickness comments.
- **Done/TMM-blocked**: Phase 3E.3A Saha exported-table audit and candidate
  gate. Canonical measured reflectance, source-simulated reflectance, TiN
  epsilon, and AZO epsilon CSVs now exist, but TMM residual modeling is stopped
  until silicon substrate optics, substrate/backside treatment, and leakage
  boundaries are frozen before residual inspection.
- **Done/stack-contract-blocked**: Phase 3E.3B Saha frozen-stack model
  provenance and no-fit adapter gate. Stack order, thickness, and 50 degree
  s/p source semantics are backed, but silicon optical constants,
  substrate/backside/coherence handling, and interface/oxide assumptions are not
  source-backed enough to freeze a no-fit TMM adapter.
- **Done/blocked**: Phase 3D.2A Saha OPJU worksheet export audit. LabPlot was
  installed and probed, but no local OPJU-to-CSV path was found.
- **Done/non-promoting**: Phase 3D.3 Exeter spatiotemporal ITO source-data
  intake. The package is public, hash-verified, and open-format, with
  table-ready epsilon and pumped transmission/frequency-shift data, but no
  separable static absolute R/T holdout.
- **Done/calibration-only**: Phase 3D.4 thermo-optic ITO Zenodo intake. The
  package is public and table-rich, with many ITO epsilon tables and Hall/SEM
  support data, but no independent measured static R/T holdout.
- **Done/pivot-triggered**: Phase 3D.5 remaining public source-data lead
  triage. Phase 3D.5A corrected the ACS/intracavity Figshare-download path to
  SI PDF only; Phase 3E.4 later found the separate Zenodo MATLAB package and
  keeps that lane as a non-promoting source-code/data fixture. Remaining known
  leads are paper/plot/PDF-only, constants-only, fixture-only, or request-only;
  no immediate Phase 4 candidate remains.
- **Done**: Phase 3E.1 public dataset gate and executive research assistant
  scaffold. The registry evaluates 15 known candidates and opens 0 Phase 4
  candidates.
- **Done/non-ENZ baseline**: Phase 3E.2A-3E.2D Wang W/WO3 source-data fixture.
  Selected Figshare XLSX files are public and MD5-verified, with direct W/WO3
  `n,k` tables. Fig. 2f source semantics are now bounded into a de-offseted
  reproduction fixture, not a no-fit validation residual.
- **Done/search-snapshot-no-phase4-candidate**: Phase 3E.4 renewed ENZ
  public-data search through stack-contract gate. Seven live-source leads were
  inspected; zero opened Phase 4. Candidate intake now requires source-backed
  material constants, measured holdout, geometry, stack/substrate/backside
  handling, and leakage boundaries before residual inspection.
- **Done/non-promoting sensitivity fixture**: Phase 3E.5 Saha no-claim
  stack-assumption sensitivity fixture. Twelve external silicon/interface/
  backside variants show very small spread against the canonical Saha exported
  tables, but this is diagnostic only and does not recover the author model,
  select a variant, validate Saha, or open Phase 4.
- **Done/no-candidate-ready**: Phase 3F.1 simple thin-film
  simulator-validation scout. Ten public simple/thin-film-adjacent leads were
  gated; zero cleared every hard flag, no Phase 3F.2 intake opened, no TMM
  adapter started, and no residual modeling ran.
- **Done/pro-leads-no-candidate-ready**: Phase 3F.1B 5.5 Pro lead gate. The
  pasted 16-lead list was encoded into candidate cards and gated; zero cleared
  every hard flag, no Phase 3F.2 intake opened, and no residual modeling ran.
- **Done/source-file-audit-no-candidate-ready**: Phase 3F.1C top-candidate
  source-file audit. The top-three fallback packages were downloaded and
  hash-verified; structural color FROC lacks open measured spectral holdout,
  FROC 2021 leaves measured data in Origin OPJ containers, and ultrathin Au is
  leakage-blocked by same-measurement fitting plus request-only processing code.
- **Next**: Continue as Phase 3F.1D only if the target is narrowed to
  benchmark/source-data packages, or explicitly open a non-promoting
  code-regression fixture lane. Keep Phase 3F.2 closed until one boring public
  stack has source-backed material constants, measured R/T or ellipsometry,
  geometry, substrate/backside handling, leakage boundaries, and source/hash
  readiness.
- **Pivot active for current run**: Keep the evidence bar intact and promote
  the executive research assistant / public-dataset gate lane recorded in
  `docs/pivots/executive_research_assistant_fallback.md`.
- **Blocked/parked**: Phase 3B TiON_48/TiON_49 raw R/T remains missing; grower
  notes and plots are useful provenance but only plot-level reflectance unless
  raw tables or explicit digitized artifacts are registered.

Goal sequence:

```text
calibrated_linear_evidence
  -> research_memory_substrate
  -> hypothesis_harness
  -> nonlinear_ENZ_readiness
  -> paper_claim_candidate
```

Compact reverse mind map for the first goal. In the interactive atlas, this is
rendered as a left-to-right branching map: one goal card on the left and
completed, in-progress, needed, blocked, or gated branches to the right.

```text
calibrated_linear_evidence
  -> COMPLETE: V0 synthetic runner
  -> COMPLETE: claim-status contract
  -> IN PROGRESS: Phase 3 real-data grounding
  -> IN PROGRESS: Phase 3A TiN/SiO2 thesis reflectance reconciliation
  -> IN PROGRESS: Phase 3A.1 normalization/threshold gate hardening
  -> IN PROGRESS: Phase 3A.2 stack mapping correction
  -> IN PROGRESS: Phase 3A.3 figure/data provenance reconciliation
  -> COMPLETE: Phase 3A.4 absolute-reflectance decision
  -> BLOCKED: Phase 3A.5 export/provenance retrieval
  -> ARCHIVED/PACKET READY: Phase 3A.6 re-export or measurement packet
  -> COMPLETE/BLOCKED: Phase 3A.7 source recovery
  -> COMPLETE/BLOCKED: Phase 3A.8 source candidate triage
  -> COMPLETE/DIAGNOSTIC: Phase 3A.9 relative-only packet
  -> COMPLETE/DECISION: Phase 3A.10 branch decision
  -> PACKET READY: Phase 3A.11 manual source follow-up packet
  -> COMPLETE/EXHAUSTED: Phase 3A.12 manual source review
  -> COMPLETE: Phase 3C public TiN dataset intake
  -> COMPLETE: Phase 3C.1 St Andrews TiN pairing
  -> COMPLETE: Phase 3C.2 run audit / future-only policy
  -> COMPLETE/FAILED: Phase 3C.3 threshold lock / clean run decision
  -> COMPLETE/TRIAGED: Phase 3C.4 St Andrews failure triage
  -> COMPLETE/GAPS: Phase 3C.5 St Andrews source-model parity
  -> COMPLETE/PARKED: Phase 3C.6A bounded parity implementation
  -> COMPLETE/LOCAL EXHAUSTED: Phase 3B.1 TiON evidence reality check
  -> COMPLETE: Phase 3D.1 Exeter/Bohn package intake
  -> COMPLETE: Phase 3D.1A Exeter/Bohn split audit
  -> COMPLETE: Phase 3D.1B no-fit static R0 extraction
  -> COMPLETE/NON-PROMOTING: Phase 3D.1C no-fit model reconstruction
  -> COMPLETE/SOURCE-EXPORTED: Phase 3D.2 Saha TiN/AZO source-data intake
  -> COMPLETE/BLOCKED: Phase 3D.2A Saha OPJU worksheet export audit
  -> COMPLETE/NONLINEAR FIXTURE: Phase 3D.3 Exeter spatiotemporal ITO intake
  -> COMPLETE/CALIBRATION-ONLY: Phase 3D.4 thermo-optic ITO Zenodo intake
  -> COMPLETE/PIVOT-TRIGGERED: Phase 3D.5 remaining public lead triage
  -> COMPLETE/GATE: Phase 3E.1 public dataset gate / executive assistant scaffold
  -> COMPLETE/NON-ENZ BASELINE: Phase 3E.2A Wang W/WO3 source-data intake
  -> COMPLETE/FIXTURE: Phase 3E.2B-3E.2D Wang de-offseted reproduction handoff
  -> COMPLETE/TMM-BLOCKED: Phase 3E.3A Saha exported-table audit
  -> COMPLETE/STACK-BLOCKED: Phase 3E.3B Saha frozen-stack model provenance gate
  -> COMPLETE/0-PHASE-4: Phase 3E.4 renewed ENZ public-data search
  -> COMPLETE/SENSITIVITY: Phase 3E.5 Saha stack-assumption fixture
  -> COMPLETE/NO-CANDIDATE: Phase 3F.1 simulator-validation scout
  -> COMPLETE/NO-CANDIDATE: Phase 3F.1B 5.5 Pro lead gate
  -> COMPLETE/NO-CANDIDATE: Phase 3F.1C source-file audit
  -> NEXT: Phase 3F.1D benchmark search or code-regression fixture lane
  -> IN PROGRESS: frozen tabulated material model
  -> PARKED: Phase 3B TiON plot-level/R/T provenance
  -> NEEDED: independent holdout measurement
  -> NEEDED: residual and uncertainty report
```

Active conflict:

```text
Optical constants are available for TiN/TiON, but TiON_48/TiON_49
sample-matched R/T provenance is not registered. Grower notes and attached
plots support qualitative TiON trends but do not provide raw R/T tables. This
blocks calibrated TiON evidence while still allowing calibration_only_no_holdout
grounding runs. Phase 3A now follows the separate TiN/SiO2 measured-reflectance
path, capped below calibrated evidence until normalization and threshold gates
are resolved. Phase 3A.3 aligns `d_10nm` with thesis Figure 4.1 while Phase
3A.4 keeps normalization at relative-intensity-only after local thesis,
CompleteEASE, hash, and nearby Woollam-artifact checks. Phase 3A.5 searched
likely local source locations, the desktop SDSU Google Drive folder, targeted
Google Drive thesis/defense hits, SDSU slides/reports, and the scanned lab
notebook. It found related RC2/CompleteEASE and `3L2/Quartz` provenance but no
exact absolute-`%R` export proof, so the decision is `blocked_needs_new_export`.
Phase 3A.6 produced a packet and acceptance policy: the project has an archived
template for a clean source-backed intake if new access ever appears, but
CompleteEASE re-export is not an active path. Phase 3A.7 then recovered related
local CompleteEASE/Woollam source
candidates, including DoD SAFE zip-contained snapshots for quartz cap-test and
10 nm SiO2 pulsed/dynamic runs, but still found no source-backed calibrated
absolute-`%R` proof. Phase 3A.8 deduplicates those candidates, separates quartz
10 nm dynamic follow-up candidates from Si-control files, and pivots the
current lane to relative-only diagnostics that cannot feed serious-core
evidence. Phase 3A.9 then records those diagnostics for the existing run:
min-max spectral-shape correlation is high, prediction and measurement dips
coincide at the 400 nm edge of the inspected window, and both trends increase
over 400-900 nm. That is useful diagnostic context, not calibrated validation.
Phase 3A.10 chooses a bounded manual source follow-up on the top three quartz
dynamic candidates before returning to Phase 3B, because Phase 3B still lacks
raw sample-matched TiON R/T.
Phase 3A.11 records the exact three-candidate review packet, proof gates, and
stop rules without changing the relative-only claim boundary.
Phase 3A.12 exhausts that bounded manual source path: the reviewed candidates
are related provenance, not exact source/calibration proof.
Phase 3C opens a cleaner public-dataset lane: the St Andrews 2025 TiN dataset
contains ellipsometry permittivity tables and `RT.xlsx` R/T data, and the linked
paper maps Figure 4 to normal-incidence unpolarized spectra for 50 nm TiN on
glass. Phase 3C.1 extracts the `RT.xlsx` R/T snapshots, registers the
`50nm-MTiN-50c` epsilon table as the candidate frozen input, and adds a
fail-closed validation candidate. This is promising but still blocked from
calibrated promotion. Phase 3C.2 audits the existing run and preserves its
residuals as historical context only: the draft threshold policy is future-only,
`applies_to_existing_run` is false, and a clean run is required after any
threshold lock. Phase 3C.3 locks conservative reflectance thresholds before a
new clean run and accepts St Andrews reflectance normalization for this public
dataset, but the run fails all five metrics. The conflict has moved from
"can we lock thresholds?" to "is the failure caused by pairing/material-model
mismatch, missing roughness/substrate physics, or a fundamental model limit?"
Phase 3C.4 answers the first triage layer: the failure is not a near miss,
blue-edge residuals dominate, alternate epsilon tables do not pass, and simple
thickness/substrate-index sweeps do not repair the shape or dip. The next
discriminating move became source-model parity against the raw Woollam
`.mod/.SE` assumptions. Phase 3C.5 records that parity gap: the source model
uses Float Glass Cauchy substrate assumptions, film-thickness/roughness
metadata, and back-reflection settings missing from the clean-run stack.
Phase 3C.6A implements bounded source-derived variants, but all variants fail
the locked thresholds and roughness/back-reflection remain approximate rather
than exact CompleteEASE parity. St Andrews is parked before Phase 4 unless new
source evidence appears. Phase 3B.1 then exhausts the local TiON lane: the repo
has TiON_48/TiON_49 epsilon tables, material models, and calibration-only
examples, but no raw R/T measurements and no digitizable plot candidates. The
user has confirmed no CompleteEASE access/contact, no TiON raw R/T, and no
St Andrews author-contact path, so the next validation-data step is Phase 3D
literature/public dataset search rather than more local squeezing. Phase 3D.1
and Phase 3D.1A then selected Exeter/Bohn ITO as the first public package and
identified a promising Figure 1 epsilon / Figure 2 static `R0` split. Phase
3D.1B extracted those canonical artifacts and locked the split. Phase 3D.1C
reconstructed the package static model with strong shape agreement but
nontrivial absolute residuals and no predeclared residual thresholds, so
Exeter/Bohn remains useful weak memory rather than Phase 4-ready evidence.
Phase 3D.2 snapshotted the Saha TiN/AZO Figshare package and confirmed the
expected Fig. 2 labels. Phase 3D.2A tested the local open-source LabPlot route
and found no usable OPJU-to-CSV export path. Phase 3E.3 then used official
Windows Origin Viewer 9.9.5 to export the Fig. 2b and Fig. 2c/d source
worksheets to CSV, clearing the table-extraction blocker but not the leakage or
claim-status audit. Phase 3E.3A then split those exports into canonical measured
reflectance, source-simulated reflectance, TiN epsilon, and AZO epsilon tables;
it stopped before TMM because the source tables do not freeze substrate optical
constants, substrate/backside treatment, or full source-model leakage
boundaries. Phase 3E.3B then checked whether the missing contract could be
frozen from paper/SI/Figshare provenance and failed closed: silicon optical
constants, substrate backside/coherence handling, and interface/oxide assumptions
remain unbacked by the source package. Phase 3D.3 then inspected the Exeter
spatiotemporal ITO package: the source is public, hash-verified, and open-format
with table-ready epsilon, but the measurement lane is nonlinear pumped
transmission/frequency-shift data and the thicker-sample labels are internally
inconsistent. Phase 3D.4 inspected the thermo-optic ITO Zenodo package: it has
many public machine-readable epsilon tables, Hall data, SEM data, and figure
artifacts, but no independent measured static R/T holdout. Phase 3D.5 bounded
the remaining known public leads and found no immediate Phase 4 candidate.
Phase 3D.5A corrected only the ACS/intracavity Figshare-download path; Phase
3E.4 later found the separate Zenodo MATLAB package and corrected the global
registry to a non-promoting fixture. Saha is now CSV-exported and canonicalized
but stack-contract-blocked before TMM, AZO/ITO paper leads are not
table-package-ready, CdO/high-crystallinity ITO are constants-only, and
request-only papers remain rejected. Phase 3E.1 turned those outcomes into a
public-dataset gate and
executive research assistant scaffold. Phase 3E.2A added Wang W/WO3 as a
non-ENZ baseline candidate: the XLSX package has direct W/WO3 constants, but
Fig. 2f is offset/unlabeled plotted data. Phase 3E.2B-3E.2D completed the
honest Wang lane: source-backed offsets and inferred measured/simulated columns
support a bounded de-offseted reproduction fixture, while full no-fit validation
remains blocked by missing workbook labels and non-independent source-simulation
semantics. Phase 3E.4 inspected ACS/intracavity Zenodo, Linkoping ITO/PEDOT,
ITO/glass/SiO2, space-time ITO, natural-ENZ compendium, LBSO, and ENZ
metal-oxide reflector leads; all remain fixtures or blocked cards, not Phase 4
candidates. Phase 3E.5 then ran a no-claim Saha sensitivity fixture over 12
external silicon/interface/backside variants. The tested assumption spread is
small, but this is still not validation: the author substrate/backside/source
model is not recovered and residual-driven variant selection would leak.
Phase 3F.1 then ran a bounded simple thin-film simulator-validation scout:
10 public leads were recorded as candidate cards, but 0 cleared every hard
gate. Phase 3F.1B then encoded the pasted GPT-5.5 Pro list as 16 candidate
cards and again found 0 hard-gate passes. Phase 3F.1C then downloaded and
hash-verified the top-three practical fallback packages: structural color FROC,
FROC 2021, and ultrathin Au. The audit again found 0 hard-gate passes.
Structural color FROC has open code/constants but no open measured spectral
R/T holdout package, FROC 2021 measured data are Origin OPJ containers, and
ultrathin Au has public raw FTIR R/T but fails the leakage-safe no-fit split
because constants/model parameters are fit from the same optical measurements.
Phase 3F remains open as the next serious-core fallback; Phase 3F.2 intake
stays closed until a simpler public planar thin-film dataset has a complete
source-backed contract.
Phase 3A.2 keeps thesis `d_10nm` source-backed but
keeps the separate `30_20_10` files out of the validation candidate. Phase 3A.1
now keeps the already-inspected residuals as historical context only and blocks
promotion until a future predeclared policy exists.
```

## Core Rule

Claims do not inherit authority from upstream records. They are re-authorized
only by validation artifacts.

Research Memory/Radar may gather and organize context. The Hypothesis Harness
may propose, critique, rank, and falsify. Only the Serious Core may validate
bounded scientific claims through provenance, calibration/holdout integrity,
validation gates, reports, and `claim_status.json`.

## Visual Sections

The interactive atlas contains:

1. **Home / Where Am I?**: current anchor, active lanes, highest-authority
   evidence, speculative queues, and current conflicts.
2. **Simple Roadmap**: the first goal, goal sequence, current progress, and
   compact reverse mind maps.
3. **Authority Map**: what each lane may do, with Serious Core as the only
   validation authority.
4. **Storyboard**: `question -> context/memory -> hypothesis -> experiment or
   simulation -> result -> critique -> claim audit -> memory update -> next
   better question`.
5. **Evidence Promotion Conveyor**: `lead -> memory record -> hypothesis card
   -> validation candidate -> serious-core run -> claim_status.json -> memory
   update`.
6. **Reverse Goal Maps**: dependencies for calibrated linear evidence,
   failed-hypothesis memory, next discriminating experiment, paper-claim
   candidate, and nonlinear ENZ readiness.
7. **Multiple-Path Map**: competing routes to choosing the next useful
   experiment.
8. **Conflict Board**: unresolved tensions with forbidden overclaims and next
   discriminating tests.
9. **Evidence Ladder**: claim maturity from lead/speculation to paper-claim
   candidate.
10. **Roadmap Swimlanes**: parallel lanes for Serious Core, Research Memory,
   Hypothesis Harness, Literature Radar, and future nonlinear/FDTD work.
11. **Node Template**: required metadata for future atlas nodes.

## Evidence Promotion

Eternity should keep parallel paths visible, but not equally authoritative:

```text
Research Memory/Radar
  finds, stores, and organizes context
  (optionally with Browse.sh and Plasmate read-only scouting)
        |
        v
Hypothesis Harness
  converts context into rival hypotheses, falsifiers, artifact checks, and scars
        |
        v
Human Review Gate
  chooses what is worth validating
        |
        v
Serious Core
  runs calibrated simulations, comparisons, validation gates, and claim status
        |
        v
Memory Feedback
  records what survived, failed, weakened, or became a future constraint
```

## Node Metadata Standard

Every future atlas node should carry:

- status
- authority lane
- source refs
- claim level
- human review state
- linked artifacts
- allowed language
- forbidden language

This prevents speculative outputs from becoming visually adjacent to validated
artifacts in a way that makes them feel validated.
