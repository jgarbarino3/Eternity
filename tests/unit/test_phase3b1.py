import json
from pathlib import Path

import yaml

from eternity.phase3b1 import build_phase3b1_packet, write_phase3b1_packet


def _write_registry(tmp_path: Path) -> Path:
    registry_path = tmp_path / "registry.yaml"
    registry_path.write_text(
        yaml.safe_dump(
            {
                "raw_artifacts": {
                    "tion_48_0p8pa_epsilon": {
                        "kind": "txt",
                        "path": "tion48.txt",
                        "source_type": "lab",
                        "source_notes": "TiON_48 optical constants; raw R/T not recovered.",
                        "sha256": "0" * 64,
                    },
                    "tion_49_1p0pa_epsilon": {
                        "kind": "txt",
                        "path": "tion49.txt",
                        "source_type": "lab",
                        "source_notes": "TiON_49 optical constants; raw R/T not recovered.",
                        "sha256": "1" * 64,
                    },
                },
                "samples": {
                    "tion_48_40nm_0p8pa": {
                        "material": "TiON",
                        "nominal_thickness": {"value": 40, "unit": "nm"},
                    },
                    "tion_49_40nm_1p0pa": {
                        "material": "TiON",
                        "nominal_thickness": {"value": 40, "unit": "nm"},
                    },
                },
                "measurements": {
                    "tion_48_0p8pa_epsilon_measurement": {
                        "kind": "epsilon_table",
                        "sample_ref": "tion_48_40nm_0p8pa",
                        "raw_artifact_ref": "tion_48_0p8pa_epsilon",
                        "stack_ref": "tion_48_stack",
                        "geometry_polarization": "unknown",
                    },
                    "tion_49_1p0pa_epsilon_measurement": {
                        "kind": "epsilon_table",
                        "sample_ref": "tion_49_40nm_1p0pa",
                        "raw_artifact_ref": "tion_49_1p0pa_epsilon",
                        "stack_ref": "tion_49_stack",
                        "geometry_polarization": "unknown",
                    },
                },
                "material_models": {
                    "tion_48_0p8pa_epsilon_model": {
                        "sample_ref": "tion_48_40nm_0p8pa",
                        "kind": "tabulated_epsilon",
                        "source_type": "lab",
                        "raw_artifact_ref": "tion_48_0p8pa_epsilon",
                        "enz_wavelengths_nm": [497.271],
                        "wavelength_min_nm": 433.4,
                        "wavelength_max_nm": 1707.8,
                        "passivity_check": "pass",
                        "limitations": ["No raw TiON R/T provenance registered yet."],
                    },
                    "tion_49_1p0pa_epsilon_model": {
                        "sample_ref": "tion_49_40nm_1p0pa",
                        "kind": "tabulated_epsilon",
                        "source_type": "lab",
                        "raw_artifact_ref": "tion_49_1p0pa_epsilon",
                        "enz_wavelengths_nm": [546.387, 1213.844],
                        "wavelength_min_nm": 412.7,
                        "wavelength_max_nm": 1707.8,
                        "passivity_check": "pass",
                        "limitations": ["No raw TiON R/T provenance registered yet."],
                    },
                },
            }
        ),
        encoding="utf-8",
    )
    return registry_path


def test_phase3b1_reports_local_validation_data_exhausted(tmp_path: Path) -> None:
    registry_path = _write_registry(tmp_path)

    packet = build_phase3b1_packet(registry_path, tmp_path)

    assert packet["phase_id"] == "Phase 3B.1"
    assert (
        packet["decision"]["status"]
        == "local_validation_data_exhausted_literature_or_external_data_needed"
    )
    assert packet["decision"]["calibration_only_modeling_ready"] is True
    assert packet["decision"]["plot_digitization_ready"] is False
    assert packet["decision"]["validation_ready"] is False
    assert packet["evidence_inventory"]["rt_measurements"] == []


def test_phase3b1_writes_json_and_markdown(tmp_path: Path) -> None:
    registry_path = _write_registry(tmp_path)
    packet = build_phase3b1_packet(registry_path, tmp_path)

    json_path, md_path = write_phase3b1_packet(tmp_path / "out", packet)

    assert json.loads(json_path.read_text(encoding="utf-8"))["phase_id"] == "Phase 3B.1"
    assert "TiON Evidence Reality Check" in md_path.read_text(encoding="utf-8")
