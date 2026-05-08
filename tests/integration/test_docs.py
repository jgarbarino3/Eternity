from pathlib import Path


def test_docs_reference_v0_commands_and_pro_checkpoints() -> None:
    readme = Path("README.md").read_text()
    agents = Path("AGENTS.md").read_text()
    roadmap = Path("CURRENT_REALISTIC_ROADMAP.md").read_text()

    assert "eternity validate experiments/examples/linear_ito_toy.yaml" in readme
    assert "eternity run experiments/examples/linear_ito_toy.yaml" in readme
    assert "eternity validate-registry lab_data/registry.yaml" in readme
    assert "eternity hash-artifact lab_data/raw/synthetic_v0/transmission_fixture.csv" in readme
    assert "Pro checkpoint recommended" in agents
    assert "Pro Model Checkpoints" in roadmap
