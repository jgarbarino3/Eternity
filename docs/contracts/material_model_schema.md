# Material Model Schema Contract

Material models must declare sample id, model kind, equation convention,
parameters, uncertainty where available, fit provenance, validity envelope, and
source type.

Passive linear models must declare sign convention and passivity checks. ENZ
wavelength definitions must be explicit.

Tabulated TiN/TiON material models must declare whether they are loaded as a
frozen table or produced by a fit, the source measurement or raw artifact, the
interpolation rule, the extrapolation policy, the valid wavelength range, and
all ENZ crossings found from `Re(epsilon)=0`. Extrapolation is forbidden by
default for real-data grounding runs.

A frozen tabulated model can support `calibration_only_no_holdout` reports. It
cannot support `calibrated_linear_evidence` until it is frozen before an
independent measured holdout comparison and the holdout residual gates pass.

Phase 3A TiN/SiO2 validation candidates use frozen layer material tables for TiN
and SiO2. The measured `30_20_10` derived e1/e2 export is registered for audit
only and must not be silently substituted as a fitted material model.
