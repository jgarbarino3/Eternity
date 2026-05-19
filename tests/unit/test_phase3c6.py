import csv
import json
import zipfile
from pathlib import Path

from eternity.phase3c6 import build_phase3c6_packet, write_phase3c6_packet


def _write_phase3c6_inputs(tmp_path: Path) -> tuple[Path, Path, Path]:
    archive_path = tmp_path / "standrews.zip"
    selected_member = "TiN-data_Pure/Ellipsometry/50nm-MTiN-50c.txt"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr(
            selected_member,
            "\n".join(
                [
                    "400 4.0 2.0",
                    "500 4.2 2.1",
                    "600 4.4 2.2",
                    "700 4.6 2.3",
                ]
            ),
        )

    pairing_json = tmp_path / "pairing.json"
    pairing_json.write_text(
        json.dumps(
            {
                "source_archive": {"path": str(archive_path)},
                "selected_pairing": {"selected_material_member": selected_member},
            }
        ),
        encoding="utf-8",
    )

    run_dir = tmp_path / "run_failed"
    run_dir.mkdir()
    with (run_dir / "comparison_table.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["wavelength_nm", "measurement"])
        writer.writeheader()
        writer.writerows(
            [
                {"wavelength_nm": 400.0, "measurement": 0.80},
                {"wavelength_nm": 500.0, "measurement": 0.82},
                {"wavelength_nm": 600.0, "measurement": 0.84},
                {"wavelength_nm": 700.0, "measurement": 0.86},
            ]
        )

    parity_json = tmp_path / "phase3c5.json"
    parity_json.write_text(
        json.dumps(
            {
                "inputs": {"triage_json": str(tmp_path / "unused.json")},
                "clean_run_model": {
                    "threshold_metrics": [
                        {
                            "name": "root_mean_square_error",
                            "comparator": "less_equal",
                            "threshold": 0.001,
                        }
                    ]
                },
                "source_model": {
                    "film_thickness_raw": 417.3,
                    "roughness_raw": 114.6,
                    "back_reflections_count": 5.0,
                    "first_reflection_percent": 100.0,
                    "substrate_model": {
                        "kind": "Float Glass - Air (Cauchy)",
                        "cauchy_A": 1.505,
                        "cauchy_B": -0.018,
                        "cauchy_C": -0.0008,
                    },
                },
            }
        ),
        encoding="utf-8",
    )
    return parity_json, pairing_json, run_dir


def _write_phase3c6_inputs_with_triage_thresholds(
    tmp_path: Path,
) -> tuple[Path, Path, Path]:
    parity_json, pairing_json, run_dir = _write_phase3c6_inputs(tmp_path)
    triage_json = tmp_path / "phase3c4.json"
    triage_json.write_text(
        json.dumps(
            {
                "current_run": {
                    "threshold_evaluation": {
                        "metrics": [
                            {
                                "name": "root_mean_square_error",
                                "comparator": "less_equal",
                                "threshold": 0.001,
                            }
                        ]
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    parity = json.loads(parity_json.read_text(encoding="utf-8"))
    parity["inputs"]["triage_json"] = str(triage_json)
    parity["clean_run_model"].pop("threshold_metrics")
    parity_json.write_text(json.dumps(parity), encoding="utf-8")
    return parity_json, pairing_json, run_dir


def test_phase3c6_stops_when_roughness_and_backside_are_underdetermined(
    tmp_path: Path,
) -> None:
    parity_json, pairing_json, run_dir = _write_phase3c6_inputs(tmp_path)

    packet = build_phase3c6_packet(parity_json, pairing_json, run_dir)

    assert packet["phase_id"] == "Phase 3C.6A"
    assert (
        packet["decision"]["status"]
        == "parity_variants_failed_roughness_back_reflection_underdetermined"
    )
    assert packet["decision"]["phase4_ready"] is False
    assert packet["resolved_status"]["roughness"] is False
    assert packet["resolved_status"]["back_reflection"] is False
    assert packet["threshold_summary"]["all_variants_failed"] is True
    assert {
        "source_cauchy_thickness_roughness_ema",
        "source_cauchy_thickness_roughness_backside_estimate",
    }.issubset({variant["name"] for variant in packet["variants"]})


def test_phase3c6_writes_json_markdown_and_csv(tmp_path: Path) -> None:
    parity_json, pairing_json, run_dir = _write_phase3c6_inputs(tmp_path)
    packet = build_phase3c6_packet(parity_json, pairing_json, run_dir)

    json_path, md_path, csv_path = write_phase3c6_packet(tmp_path / "out", packet)

    assert json.loads(json_path.read_text(encoding="utf-8"))["phase_id"] == "Phase 3C.6A"
    assert "Bounded St Andrews Source-Model Parity" in md_path.read_text(encoding="utf-8")
    assert "source_cauchy_thickness_roughness_backside_estimate" in csv_path.read_text(
        encoding="utf-8"
    )


def test_phase3c6_uses_string_triage_json_fallback(tmp_path: Path) -> None:
    parity_json, pairing_json, run_dir = _write_phase3c6_inputs_with_triage_thresholds(
        tmp_path
    )

    packet = build_phase3c6_packet(parity_json, pairing_json, run_dir)

    assert packet["threshold_summary"]["all_variants_failed"] is True
