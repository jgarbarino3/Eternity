# Phase 3A.9 Relative-Only Diagnostic Run Packet

## Decision

- Status: `relative_only_diagnostic_packet_ready`
- Normalization basis: `relative_intensity_only`
- Can feed serious core: `False`
- Can promote calibrated evidence: `False`
- Claim-status ceiling: `weak_within_dataset_holdout`
- Existing run promotion: `forbidden`

## Relative Diagnostics

- Wavelength window: `400.0` to `900.0` nm
- Points: `501`
- Min-max shape correlation: `0.9861424344926918`
- Mean absolute relative-shape delta: `0.0961868323899881`
- Max absolute relative-shape delta: `0.18075756860177566`
- Prediction dip: `400.0` nm
- Measurement dip: `400.0` nm
- Dip offset: `0.0` nm
- Prediction trend: `increasing`
- Measurement trend: `increasing`
- Trend agreement: `True`

## Boundary

These diagnostics compare relative spectral shape only. They are not absolute-reflectance validation, pass/fail thresholds, or calibrated evidence.

Allowed diagnostics: `spectral_shape`, `dip_position`, `trend_direction`, `figure_provenance`.

Forbidden uses: `serious_core_evidence`, `calibrated_linear_evidence`, `absolute_reflectance_claim`, `retroactive_threshold_tuning`.
