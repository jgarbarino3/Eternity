from pathlib import Path

from eternity.registry import load_registry


def test_registry_loads_contract_fixture() -> None:
    registry = load_registry(Path("lab_data/registry.yaml"))

    assert registry.raw_artifacts["synthetic_v0_transmission"].source_type == "synthetic"
    assert registry.measurements["synthetic_v0_transmission_measurement"].kind == (
        "transmission_spectrum"
    )
    assert registry.splits["synthetic_v0_contract_split"].evidence_strength == "synthetic_fixture"
