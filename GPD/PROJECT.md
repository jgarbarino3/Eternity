# Eternity GPD Alignment

This is a thin Get Physics Done alignment layer for the Eternity repo. It
mirrors the current Serious Core direction so GPD workflows can help plan and
verify future phases without becoming the scientific source of truth.

Updated: 2026-05-19. Current mirrored focus is Phase 3C.6 source-model parity
implementation or lane park decision: the public archive and paper are
snapshotted, `RT.xlsx` has canonical R/T CSV snapshots, the threshold-locked
clean run failed all five reflectance metrics, Phase 3C.4 triaged the failure
as a non-near-miss dominated by blue-edge residuals, and Phase 3C.5 recorded
source-model parity gaps in the raw Woollam `.mod/.SE` files. The clean-run
stack still lacks the source Float Glass Cauchy substrate, roughness metadata,
and back-reflection settings. Calibrated promotion remains blocked; the next
useful step is deciding whether to implement bounded parity code or park the
St Andrews lane as diagnostic-only.

Authoritative sources remain:

- `GOALS.md`
- `CURRENT_REALISTIC_ROADMAP.md`
- `docs/PROJECT_ATLAS.md`
- `docs/contracts/`
- `src/eternity/claim_status.py`

Current research objective:

```text
Build a calibrated ENZ linear digital twin by grounding TiN/TiON optical
constants and thesis reflectance spectra in immutable registry artifacts,
then require independent holdout evidence before any calibrated claim.
```

Claim boundary:

```text
Optical constants plus deterministic TMM output can support
calibration_only_no_holdout. Only a frozen model plus independent measured
holdout residuals can support calibrated_linear_evidence.
```
