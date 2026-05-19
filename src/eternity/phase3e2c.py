"""Phase 3E.2C Wang bounded de-offseted reproduction fixture."""

from __future__ import annotations

import csv
import json
import math
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from eternity.phase3e2a import DEFAULT_RAW_DIR, TARGET_FILES, _as_float, _column_label, _parse_xlsx
from eternity.phase3e2b import build_phase3e2b_packet


def _round_float(value: float, digits: int = 6) -> float:
    return round(value, digits)


def _deoffset_rows(raw_dir: Path) -> list[dict[str, Any]]:
    rows = _parse_xlsx(raw_dir / TARGET_FILES["fig2f_reflectance"])["Sheet1"]
    thicknesses = [
        int(value)
        for index in range(1, 15, 2)
        if (value := _as_float(rows[1][index])) is not None
    ]
    fixture_rows: list[dict[str, Any]] = []
    for pair_index, thickness_nm in enumerate(thicknesses):
        first_column_index = 1 + 2 * pair_index
        second_column_index = 2 + 2 * pair_index
        offset_added_percent = 70 * (len(thicknesses) - 1 - pair_index)
        for row in rows[3:]:
            if len(row) <= max(first_column_index, second_column_index):
                continue
            wavelength = _as_float(row[0])
            measured_raw = _as_float(row[first_column_index])
            simulated_raw = _as_float(row[second_column_index])
            if wavelength is None or measured_raw is None or simulated_raw is None:
                continue
            measured = measured_raw + offset_added_percent
            simulated = simulated_raw + offset_added_percent
            fixture_rows.append(
                {
                    "wavelength_nm": int(wavelength)
                    if float(wavelength).is_integer()
                    else _round_float(wavelength),
                    "thickness_nm": thickness_nm,
                    "offset_added_percent": offset_added_percent,
                    "inferred_measured_percent": _round_float(measured),
                    "inferred_simulated_percent": _round_float(simulated),
                    "residual_measured_minus_simulated_percent": _round_float(
                        measured - simulated
                    ),
                    "source_measured_column_inferred": _column_label(
                        first_column_index + 1
                    ),
                    "source_simulated_column_inferred": _column_label(
                        second_column_index + 1
                    ),
                    "assignment_status": "inferred_not_workbook_labeled",
                }
            )
    return fixture_rows


def _metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_thickness: dict[int, list[float]] = {}
    for row in rows:
        by_thickness.setdefault(row["thickness_nm"], []).append(
            row["residual_measured_minus_simulated_percent"]
        )

    def metric_block(values: list[float]) -> dict[str, Any]:
        abs_values = [abs(value) for value in values]
        return {
            "point_count": len(values),
            "mae_percent": _round_float(sum(abs_values) / len(abs_values)),
            "rmse_percent": _round_float(
                math.sqrt(sum(value * value for value in values) / len(values))
            ),
            "max_abs_percent": _round_float(max(abs_values)),
            "mean_signed_percent": _round_float(sum(values) / len(values)),
        }

    all_residuals = [row["residual_measured_minus_simulated_percent"] for row in rows]
    return {
        "global": metric_block(all_residuals),
        "by_thickness_nm": {
            str(thickness): metric_block(values)
            for thickness, values in sorted(by_thickness.items())
        },
    }


def build_phase3e2c_packet(raw_dir: Path = DEFAULT_RAW_DIR) -> dict[str, Any]:
    semantics_packet = build_phase3e2b_packet(raw_dir)
    fixture_rows = _deoffset_rows(raw_dir)
    return {
        "phase_id": "Phase 3E.2C",
        "title": "Wang Bounded De-Offseted Reproduction Fixture",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {
            "raw_dir": str(raw_dir),
            "fig2f_workbook": str(raw_dir / TARGET_FILES["fig2f_reflectance"]),
            "semantics_status": semantics_packet["decision"]["status"],
        },
        "fixture_contract": {
            "fixture_kind": "source_data_reproduction_not_validation",
            "deoffset_rule": (
                "add 420, 350, 280, 210, 140, 70, and 0 percent offsets "
                "across the stacked thickness groups"
            ),
            "measured_column_rule": "first y column per thickness pair is inferred measured",
            "simulated_column_rule": "second y column per thickness pair is inferred simulated",
            "residual_quantity": "inferred measured percent minus source simulated percent",
            "fitted_parameters": [],
            "forbidden_uses": [
                "calibrated_linear_evidence",
                "ENZ evidence",
                "absolute reflectance validation",
                "proof that the source simulation was independent of Fig. 2f tuning",
            ],
        },
        "row_count": len(fixture_rows),
        "metrics": _metrics(fixture_rows),
        "decision": {
            "status": "bounded_deoffset_reproduction_fixture_ready",
            "claim_status_ceiling": "literature_reproduction_fixture",
            "phase4_candidate": False,
            "phase4_enz_ready": False,
            "full_no_fit_tmm_validation_allowed": False,
            "assistant_value": (
                "This fixture lets the assistant parse stacked source-data plots, "
                "record inferred line semantics, and compute bounded diagnostics while "
                "preserving the calibrated-evidence gate."
            ),
            "recommended_next_phase": (
                "Phase 3E.2D - Wang lane claim-boundary and assistant handoff"
            ),
        },
    }


def phase3e2c_markdown(packet: dict[str, Any]) -> str:
    metrics = packet["metrics"]
    rows = [
        "| Thickness nm | Points | MAE percent | RMSE percent | Max abs percent |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for thickness, block in metrics["by_thickness_nm"].items():
        rows.append(
            "| "
            + thickness
            + " | "
            + str(block["point_count"])
            + " | "
            + f"{block['mae_percent']:.3f}"
            + " | "
            + f"{block['rmse_percent']:.3f}"
            + " | "
            + f"{block['max_abs_percent']:.3f}"
            + " |"
        )
    decision = packet["decision"]
    global_metrics = metrics["global"]
    return "\n".join(
        [
            "# Phase 3E.2C - Wang Bounded De-Offseted Reproduction Fixture",
            "",
            "## Decision",
            "",
            f"- Status: `{decision['status']}`",
            f"- Claim-status ceiling: `{decision['claim_status_ceiling']}`",
            (
                "- Full no-fit TMM validation allowed: "
                f"`{decision['full_no_fit_tmm_validation_allowed']}`"
            ),
            f"- Recommended next phase: `{decision['recommended_next_phase']}`",
            "",
            decision["assistant_value"],
            "",
            "## Fixture Contract",
            "",
            f"- Fixture kind: `{packet['fixture_contract']['fixture_kind']}`",
            f"- De-offset rule: {packet['fixture_contract']['deoffset_rule']}",
            f"- Measured column rule: {packet['fixture_contract']['measured_column_rule']}",
            f"- Simulated column rule: {packet['fixture_contract']['simulated_column_rule']}",
            "",
            "## Diagnostics",
            "",
            f"- Row count: `{packet['row_count']}`",
            f"- Global MAE: `{global_metrics['mae_percent']:.3f}` percent",
            f"- Global RMSE: `{global_metrics['rmse_percent']:.3f}` percent",
            f"- Global max absolute residual: `{global_metrics['max_abs_percent']:.3f}` percent",
            "",
            *rows,
            "",
            "## Forbidden Uses",
            "",
            *["- " + item for item in packet["fixture_contract"]["forbidden_uses"]],
            "",
        ]
    )


def write_phase3e2c_packet(
    output_dir: Path, packet: dict[str, Any], rows: list[dict[str, Any]] | None = None
) -> tuple[Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3e2c_wang_deoffset_reproduction_fixture.json"
    md_path = output_dir / "phase3e2c_wang_deoffset_reproduction_fixture.md"
    csv_path = output_dir / "phase3e2c_wang_deoffset_reproduction_fixture.csv"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(phase3e2c_markdown(packet), encoding="utf-8")
    fixture_rows = rows if rows is not None else _deoffset_rows(Path(packet["inputs"]["raw_dir"]))
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fixture_rows[0]))
        writer.writeheader()
        writer.writerows(fixture_rows)
    return json_path, md_path, csv_path


def build_phase3e2c_fixture_rows(raw_dir: Path = DEFAULT_RAW_DIR) -> list[dict[str, Any]]:
    return _deoffset_rows(raw_dir)
