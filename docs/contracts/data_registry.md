# Data Registry Contract

The lab-data registry is the canonical map from ids to immutable raw artifacts,
samples, stacks, media, measurements, material models, data splits, calibration
plans, and validation plans.

Real or literature data must not enter through loose paths. Every raw artifact
requires a SHA-256 digest, source label, byte size, and immutable path.
