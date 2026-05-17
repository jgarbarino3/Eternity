# Eternity GPD Alignment

This is a thin Get Physics Done alignment layer for the Eternity repo. It
mirrors the current Serious Core direction so GPD workflows can help plan and
verify future phases without becoming the scientific source of truth.

Updated: 2026-05-17. Current mirrored focus is Phase 3C.3 St Andrews threshold
lock and clean-run decision: the public archive and paper are snapshotted,
`RT.xlsx` has canonical R/T CSV snapshots, the candidate `50nm-MTiN-50c`
epsilon table is registered, and a threshold-locked clean run now failed all
five reflectance metrics. Calibrated promotion remains blocked; the next useful
step is Phase 3C.4 failure triage rather than threshold loosening.

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
