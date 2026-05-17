# Data Registry Contract

The lab-data registry is the canonical map from ids to immutable raw artifacts,
samples, stacks, media, measurements, material models, data splits, calibration
plans, and validation plans.

Real or literature data must not enter through loose paths. Every raw artifact
requires a SHA-256 digest, source label, byte size, and immutable path.

For the TiN/TiON real-data grounding phase, every small raw text snapshot must
also preserve original filename, original local path when known, acquisition
date, source notes, access notes, and provenance refs. The registry is allowed
to point at publication PDFs as provenance references, but small text artifacts
used by loaders should be copied under `lab_data/raw/...` and treated as
immutable snapshots.

For Phase 3A TiN/SiO2 reconciliation, the `30_20_10` reflectance, p/s
intensity, Psi/Delta, derived e1/e2, and SiO2 Sellmeier-derived epsilon exports
are registered as immutable raw artifacts. Their registry records must state
whether each artifact is a frozen material input, holdout comparison target, or
auxiliary diagnostic, and whether it is forbidden for fitting.

Optical-constants artifacts may enter the Serious Core as calibration-side
material inputs. They do not become independent evidence for R/T prediction
unless a separate measured transmission, reflection, or ellipsometry holdout is
registered with geometry and split integrity.

For Phase 3C.1 St Andrews TiN, the original public zip and paper PDF remain
provenance containers. Loadable measurement/model inputs must be small
member-derived snapshots with their own SHA-256 digests, byte counts, source
member names, and registry ids. Hidden Excel-in-zip members must not be used as
direct loose measurement paths in experiment specs.
