# Phase 3C.5 - St Andrews Source-Model Parity Diagnostic

## Decision

- Status: `source_model_parity_gaps_recorded`
- Can feed serious core: `False`
- Can promote calibrated evidence: `False`
- Phase 4 ready: `False`
- Source-model revision ready: `False`
- Next phase: `Phase 3C.6 - source-model parity implementation or lane park decision`

## Source Members

- Selected epsilon table: `TiN-data_Pure/Ellipsometry/50nm-MTiN-50c.txt`
- Raw model member: `TiN-data_Pure/Ellipsometry/raw file/50nm-MTiN-50c.mod`
- Raw SE member: `TiN-data_Pure/Ellipsometry/raw file/50nm-MTiN-50c.SE`

## Readable Source-Model Assumptions

- Film thickness raw value: `417.36509145893865`
- Film thickness possible nm if raw value is Angstrom: `41.73650914589386`
- Roughness raw value: `114.62616711097938`
- Thickness non-uniformity percent: `0.0`
- Back reflections count: `5.0`
- First reflection percent: `100.0`
- Substrate model: `Float Glass - Air (Cauchy)`
- Cauchy A/B/C: `1.5052715793770524`, `-0.018660648237365515`, `-0.000833799619479561`
- Layer model label: `TIN 3 (Lorentz)`

## Parity Checks

- `film_thickness`: `mismatch_or_unit_unresolved`. The clean run uses the nominal registry thickness. The raw Woollam model exposes a different internal thickness-like value whose unit must be decoded before using it.
- `substrate_model`: `mismatch`. The clean run uses a fixed lossless glass index, while the source model uses a Float Glass Cauchy substrate.
- `roughness_model`: `missing_in_clean_run`. The source model exposes roughness metadata, but the clean run is a single flat TiN layer on glass.
- `back_reflection_settings`: `missing_or_not_modeled_in_clean_run`. The Woollam model includes back-reflection settings that are not represented in the current clean-run stack.

## Boundary

Phase 3C.5 records source-model parity gaps only. It must not use the holdout to tune a replacement model, change thresholds, feed the serious core, or promote calibrated_linear_evidence.
