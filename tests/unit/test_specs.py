from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from eternity.specs import ExperimentSpec, QuantitySpec


def test_toy_spec_is_valid() -> None:
    data = yaml.safe_load(Path("experiments/examples/linear_ito_toy.yaml").read_text())

    spec = ExperimentSpec.model_validate(data)

    assert spec.schema_version == "0.1"
    assert spec.experiment_id == "linear_ito_toy_001"
    assert spec.sample.thickness.unit == "nm"


def test_quantity_spec_rejects_missing_unit() -> None:
    with pytest.raises(ValidationError):
        QuantitySpec.model_validate({"value": 1550})


def test_quantity_spec_parses_common_units() -> None:
    assert QuantitySpec(value=1550, unit="nm").to("m").magnitude == pytest.approx(1.55e-6)
    assert QuantitySpec(value=30, unit="deg").to("rad").magnitude == pytest.approx(0.5235987756)
    assert QuantitySpec(value=0.01, unit="mJ/cm^2").to("J/m^2").magnitude == pytest.approx(0.1)
