# Phase 3D.5 - Remaining Public Source-Data Lead Triage

Date: 2026-05-19

## Purpose

This phase bounds the already-known public validation leads after the concrete
package intakes for Exeter/Bohn, Saha, Exeter spatiotemporal ITO, and
thermo-optic ITO. It is not a fresh broad literature census. Its job is to
decide whether another known lead is ready for immediate package ingestion, or
whether the project should stop the current calibrated-linear push and pivot
without lowering the evidence bar.

## Inputs

Known leads came from the Phase 3D public-search work, the user's 5.5 Pro
response, and the earlier deep-research response.

Already executed before this triage:

- Phase 3D.1-3D.1C: Exeter/Bohn ITO package downloaded, split-audited, locked,
  and reconstructed as non-promoting `weak_within_dataset_holdout` memory.
- Phase 3D.2-3D.2A: Saha TiN/AZO source package downloaded and hash-verified,
  but local OPJU-to-CSV export is blocked.
- Phase 3D.3: Exeter spatiotemporal ITO package downloaded and inspected as a
  nonlinear/literature fixture, not a static calibrated-linear holdout.
- Phase 3D.4: thermo-optic ITO Zenodo package downloaded and inspected as a
  strong constants fixture, not an independent measured R/T holdout.

## Remaining Leads Checked

| Lead | Material | Current public access | Decision |
| --- | --- | --- | --- |
| Intracavity Epsilon-Near-Zero Dual-Range Frequency Switch | ITO | Direct Figshare-style `ndownloader` file `51010982` returns an HTTP 202 WAF challenge in this environment. Figshare API search did not expose a matching article record. DOI/ACS routes returned script-side 403. | Access-blocked source-data lead. Not immediate ingest-ready without manual/browser package access. |
| Swatowska et al. ALD AZO/ZnO | AZO/ZnO | Public article lead with clearly separated SE and T/R measurement lanes, but no open raw/source-data package was verified here. | Useful workflow lead; not calibrated ingest-ready unless raw numerical T/R and optical-constant tables are found. |
| Rasheed and Barille ITO on glass/PET | ITO | arXiv PDF route is reachable, but no companion raw repository or table package was verified. | Paper/PDF-only candidate until exact per-sample numerical data and split provenance are recovered. |
| Nolen et al. n-doped CdO dielectric function | In:CdO | Public SI/generator route exists for dielectric-function model parameters. | Real material-model fixture; no independent measured holdout verified. |
| Highly crystalline ITO / ENZ constants benchmark | ITO | Public paper/supplement trail from prior search, but no independent holdout verified. | Constants benchmark only unless a measured R/T or held-out ellipsometry table appears. |
| Request-only TiN/ITO/nanocavity papers | mixed ENZ | Data/code only on author request or no public table package found. | Reject for current milestone under no-author-contact rule. |

## Access Checks

Scripted checks in this environment found:

- `https://figshare.com/ndownloader/files/51010982`:
  HTTP `202`, `x-amzn-waf-action: challenge`.
- `https://api.figshare.com/v2/file/download/51010982`:
  HTTP `400`.
- Figshare API searches for the intracavity title and DOI:
  returned unrelated records, not a usable package manifest.
- `https://doi.org/10.1021/acsphotonics.4c01322`:
  script-side HTTP `403`.
- ACS supplementary PDF route for the same DOI:
  script-side HTTP `403`.
- `https://doi.org/10.3390/en14196271`:
  script-side HTTP `403`, while the public article remains a known literature
  lead from browser/deep-research inspection.
- `https://doi.org/10.48550/arXiv.1710.04814`:
  HTTP `200`; arXiv PDF route is reachable.
- `https://my.vanderbilt.edu/caldwellgroup/dielectric-functions/`:
  HTTP `200`; useful constants/model route, not a validation holdout.

## Decision

Decision: `known_public_leads_bounded_triage_no_immediate_phase4_candidate`.

Claim ceiling for this phase: `no_new_calibrated_claim`.

Serious-core promotion:

- Can feed `calibrated_linear_evidence`: `false`.
- Can enter Phase 4 now: `false`.
- Can support an immediate additional package intake: `false`, unless the user
  manually obtains the blocked ACS/intracavity source-data package or a real
  Saha OPJU table export appears.
- Can support the public-dataset gate / executive research assistant pivot:
  `true`.

## Interpretation

The current project path is not dead. The calibrated-linear evidence milestone
is dataset-limited. The strongest known public packages have now been handled
conservatively:

- Exeter/Bohn is useful but non-promoting after residual inspection.
- Saha remains promising but table-export blocked.
- Exeter spatiotemporal is nonlinear.
- Thermo-optic ITO is constants-rich but holdout-free.
- Remaining known leads are access-blocked, plots/PDF-only, constants-only, or
  request-only.

The correct next move is not to force a green validation. The correct next move
is to treat this as a successful gate failure and pivot the near-term milestone
to the dataset-acceptance and executive research-assistant substrate.

## Stop Rule

Stop the current Phase 3D implementation run here.

Reopen Phase 3D only if one of these appears:

- A real CSV/TXT/XLSX/HDF5/JSON export for Saha Fig. 2b and Fig. 2c/d.
- Manual/browser access to the ACS intracavity source-data package, with a
  package manifest proving raw or table-ready ellipsometry plus measured R/T/A.
- A new literature search finds a public package with same-sample optical
  constants and a separable measured static R/T or held-out ellipsometry lane.
- New local lab data provide sample-matched R/T with geometry, units,
  calibration, and sample identity.

## Recommended Next Phase

Recommended next phase: `Phase 3E.1 - Public Dataset Gate And Executive
Research Assistant Scaffold`.

Reasoning effort: high planning, medium implementation.

Helpful tools: repo-local scripts, GPD planner/verifier for phase framing,
local registry/schema tests, and live literature tools only when adding new
candidate cards.

