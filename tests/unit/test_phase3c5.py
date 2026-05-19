import json
import zipfile
from pathlib import Path

from eternity.phase3c5 import build_phase3c5_parity_packet, write_phase3c5_parity_packet


def _write_phase3c5_inputs(tmp_path: Path) -> tuple[Path, Path, Path]:
    run_dir = tmp_path / "results" / "runs" / "run_failed"
    run_dir.mkdir(parents=True)
    (run_dir / "sample_stack.json").write_text(
        json.dumps(
            {
                "stack": {
                    "layers": [
                        {"role": "incident_medium", "material": "air"},
                        {
                            "role": "film",
                            "material": "TiN",
                            "thickness": {"value": 50.0, "unit": "nm"},
                        },
                        {"role": "substrate", "material": "glass"},
                    ]
                }
            }
        ),
        encoding="utf-8",
    )
    (run_dir / "resolved_spec.json").write_text(
        json.dumps({"geometry": {"substrate": "glass", "polarization": "TE"}}),
        encoding="utf-8",
    )

    triage_json = tmp_path / "phase3c4.json"
    triage_json.write_text(
        json.dumps(
            {
                "decision": {"status": "failure_triaged_no_promotion"},
                "dominant_failure_windows": [{"window_nm": [400.0, 450.0]}],
            }
        ),
        encoding="utf-8",
    )

    archive_path = tmp_path / "standrews.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr(
            "TiN-data_Pure/Ellipsometry/raw file/50nm-MTiN-50c.mod",
            "\n".join(
                [
                    "Cauchy model for Glass Substrate, with Surface Roughness",
                    "\t114.6\tT\t-100.0\t200.0\tF\t'Roughness'",
                    "\t5.0\tT\t0.0\t20.0\tF\t'# Back Reflections'",
                    "\t100.0\tT\t0.0\t100.0\tF\t'% 1st Reflection'",
                    "\t0.0\tF\t0.0\t100.0\tF\t'% Thickness Non-uniformity'",
                    "\t417.3\tT\t200.0\t1500.0\tF\t'Thickness # 1'",
                    "\t'Layer'\t'TIN 3 (Lorentz)'",
                    "\t1.5\tT\t0.1\t10.0\tF\t'A'",
                    "\t-0.01\tT\t-2.0\t2.0\tF\t'B'",
                    "\t0.001\tT\t-1.0\t1.0\tF\t'C'",
                    "\t0.0\tF\t0.0\t10.0\tF\t'k Amplitude'",
                    "\t1.5\tF\t0.0\t10.0\tF\t'Exponent'",
                ]
            ),
        )
        archive.writestr("TiN-data_Pure/Ellipsometry/raw file/50nm-MTiN-50c.SE", "binary-ish")

    pairing_json = tmp_path / "pairing.json"
    pairing_json.write_text(
        json.dumps(
            {
                "source_archive": {"path": str(archive_path)},
                "selected_pairing": {
                    "selected_material_member": "TiN-data_Pure/Ellipsometry/50nm-MTiN-50c.txt"
                },
            }
        ),
        encoding="utf-8",
    )
    return triage_json, pairing_json, run_dir


def test_phase3c5_records_source_model_parity_gaps(tmp_path: Path) -> None:
    triage_json, pairing_json, run_dir = _write_phase3c5_inputs(tmp_path)

    packet = build_phase3c5_parity_packet(triage_json, pairing_json, run_dir)

    assert packet["phase_id"] == "Phase 3C.5"
    assert packet["decision"]["status"] == "source_model_parity_gaps_recorded"
    assert packet["decision"]["can_feed_serious_core"] is False
    assert packet["source_model"]["film_thickness_raw"] == 417.3
    assert "roughness_model" in packet["blocking_parity_gaps"]
    assert packet["inputs"]["raw_se_member"].endswith("50nm-MTiN-50c.SE")


def test_phase3c5_writes_packet_artifacts(tmp_path: Path) -> None:
    triage_json, pairing_json, run_dir = _write_phase3c5_inputs(tmp_path)
    packet = build_phase3c5_parity_packet(triage_json, pairing_json, run_dir)

    json_path, md_path = write_phase3c5_parity_packet(tmp_path / "out", packet)

    assert json.loads(json_path.read_text())["phase_id"] == "Phase 3C.5"
    assert "Source-Model Parity" in md_path.read_text()
