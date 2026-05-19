# Eternity GPD Alignment

This is a thin Get Physics Done alignment layer for the Eternity repo. It
mirrors the current Serious Core direction so GPD workflows can help plan and
verify future phases without becoming the scientific source of truth.

Updated: 2026-05-19. Current mirrored focus is Phase 3D literature/public
validation dataset search: Phase 3B.1 completed the local TiON evidence reality
check after Phase 3C.6A parked St Andrews before Phase 4. TiON_48/TiON_49 have
registered epsilon tables, material models, and calibration-only examples, but
no repo-local raw R/T measurements or digitizable plot candidates were found.
The user has confirmed no CompleteEASE access/contact, no TiON raw R/T, and no
St Andrews author-contact path. Calibrated promotion remains blocked; the next
useful step is exhausting current literature/public repositories for a dataset
with source-qualified optical constants plus independent R/T or ellipsometry
holdout evidence.

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
