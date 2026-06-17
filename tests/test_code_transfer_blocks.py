from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from code_transfer_block.multi_saturation_target_workflow import fit_and_predict_all_saturations


pytest.importorskip("openpyxl")
pytest.importorskip("sklearn")


def test_multi_saturation_transfer_workflow_trains_targets_from_dataset3(tmp_path: Path) -> None:
    rows_one = 12
    rows_two = 10
    log_one = pd.DataFrame(
        {
            "WELL": ["MTE"] * rows_one,
            "DEPTH": [500 + index for index in range(rows_one)],
            "GR": [40 + index % 3 for index in range(rows_one)],
            "RT": [25 + index for index in range(rows_one)],
            "RHOB": [2.22 - index * 0.004 for index in range(rows_one)],
        }
    )
    log_two = pd.DataFrame(
        {
            "WELL": ["IGS"] * rows_two,
            "DEPTH": [550 + index for index in range(rows_two)],
            "GR": [45 + index % 4 for index in range(rows_two)],
            "RT": [30 + index for index in range(rows_two)],
            "RHOB": [2.18 - index * 0.003 for index in range(rows_two)],
        }
    )
    log_one.to_excel(tmp_path / "curated_dataset1.xlsx", sheet_name="#1 well logs", index=False)
    log_two.to_excel(tmp_path / "curated_dataset2.xlsx", sheet_name="#2 well logs", index=False)

    with pd.ExcelWriter(tmp_path / "curated_dataset3.xlsx") as writer:
        pd.DataFrame({"S_h": [0.12 + index * 0.015 for index in range(rows_one)]}).to_excel(
            writer,
            sheet_name="#1",
            index=False,
        )
        pd.DataFrame({"Sh": [0.2 + index * 0.01 for index in range(rows_two)]}).to_excel(
            writer,
            sheet_name="#2",
            index=False,
        )

    result = fit_and_predict_all_saturations(
        tmp_path,
        output_dir=tmp_path / "outputs_runtime" / "multi_saturation_test",
        min_training_rows=5,
    )

    output_dir = Path(result["output_dir"])
    summary = pd.read_csv(output_dir / "run_summary.csv")
    features = pd.read_csv(output_dir / "feature_columns_by_target.csv")

    assert result["trained_target_count"] == 2
    assert set(summary["target_column"]) == {"S_h", "Sh"}
    assert set(summary["alignment_method"]) == {"row_order_aligned"}
    assert "DEPTH" not in set(features["feature_column"])
    assert "depth_m" not in set(features["feature_column"])
    assert any(output_dir.glob("*/predictions_curated_dataset1_*.csv"))
    assert any(output_dir.glob("*/predictions_curated_dataset2_*.csv"))
