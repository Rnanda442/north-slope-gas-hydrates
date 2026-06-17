from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from dashboard.runtime.three_dataset_pipeline import run_three_dataset_pipeline, scan_three_dataset_headers


pytest.importorskip("openpyxl")
pytest.importorskip("sklearn")


def write_dataset(path: Path, *, well: str, start_depth: int, rows: int, offset: float = 0.0) -> None:
    depths = [start_depth + index * 2 for index in range(rows)]
    frame = pd.DataFrame(
        {
            "WELL": [well] * rows,
            "DEPTH": depths,
            "depths_unitD": ["m"] * rows,
            "Unnamed: 12": [index for index in range(rows)],
            "gr_api": [41 + (index % 5) for index in range(rows)],
            "GR": [42 + (index % 5) for index in range(rows)],
            "RT": [0 if index == 0 else 35 + offset + index * 1.5 for index in range(rows)],
            "RHOB": [2.24 - index * 0.006 for index in range(rows)],
            "DTC": [0 if index == 1 else 92 - index * 0.25 for index in range(rows)],
            "DTS": [180 - index * 0.35 for index in range(rows)],
            "Sgh": [0.18 + offset * 0.002 + index * 0.01 for index in range(rows)],
        }
    )
    frame.to_excel(path, index=False)


def test_three_dataset_pipeline_trains_on_dataset1_and_scores_two_external_tests(tmp_path: Path) -> None:
    write_dataset(tmp_path / "curated_dataset1.xlsx", well="MTE_refined", start_depth=500, rows=24)
    write_dataset(tmp_path / "curated_dataset2.xlsx", well="IGS_refined", start_depth=550, rows=14, offset=3)
    write_dataset(tmp_path / "curated_dataset3.xlsx", well="Dataset3", start_depth=600, rows=16, offset=5)

    result = run_three_dataset_pipeline(
        data_dir=tmp_path,
        output_root=tmp_path / "outputs_runtime",
        model_root=tmp_path / "models_runtime",
        random_state=7,
        run_label="unit_test_run",
    )

    assert result["status"] == "trained"
    assert result["target"]["column"] == "Sgh"
    assert result["target"]["task"] == "regression"
    assert result["feature_count"] > 0

    run_dir = Path(result["run_dir"])
    train_metrics = pd.read_csv(run_dir / "train_metrics.csv")
    test_metrics = pd.read_csv(run_dir / "test_metrics.csv")
    features = pd.read_csv(run_dir / "feature_columns.csv")

    assert train_metrics.loc[0, "dataset"] == "curated_dataset1"
    assert set(test_metrics["dataset"]) == {"curated_dataset2", "curated_dataset3"}
    assert (test_metrics["rows_scored"] > 0).all()
    assert "Sgh" not in set(features["feature_column"])
    assert "depth_m" not in set(features["feature_column"])
    assert "DEPTH" not in set(features["feature_column"])
    assert "depths_unitD" not in set(features["feature_column"])
    assert "Unnamed: 12" not in set(features["feature_column"])
    assert "GR" not in set(features["feature_column"])
    assert "gr_api" in set(features["feature_column"])
    assert (run_dir / "predictions_curated_dataset2.csv").exists()
    assert (run_dir / "predictions_curated_dataset3.csv").exists()


def test_three_dataset_pipeline_writes_readiness_when_no_target_is_available(tmp_path: Path) -> None:
    frame = pd.DataFrame(
        {
            "WELL": ["MTE"] * 5,
            "DEPTH": [500, 502, 504, 506, 508],
            "GR": [40, 42, 41, 43, 44],
            "RT": [20, 22, 24, 26, 28],
            "RHOB": [2.2, 2.19, 2.18, 2.17, 2.16],
        }
    )
    for index in range(1, 4):
        frame.to_excel(tmp_path / f"curated_dataset{index}.xlsx", index=False)

    result = run_three_dataset_pipeline(
        data_dir=tmp_path,
        output_root=tmp_path / "outputs_runtime",
        model_root=tmp_path / "models_runtime",
        run_label="readiness_only_run",
    )

    run_dir = Path(result["run_dir"])
    assert result["status"] == "readiness_only"
    assert "no target-like" in result["blocked_reason"]
    assert (run_dir / "dataset_inventory.csv").exists()
    assert (run_dir / "schema_readiness.csv").exists()
    assert (run_dir / "feature_columns.csv").exists()


def test_three_dataset_pipeline_can_train_on_labeled_dataset3_and_predict_unlabeled_others(tmp_path: Path) -> None:
    feature_frame = pd.DataFrame(
        {
            "WELL": ["MTE"] * 12,
            "DEPTH": [500 + index * 2 for index in range(12)],
            "GR": [40 + (index % 4) for index in range(12)],
            "RT": [20 + index for index in range(12)],
            "RHOB": [2.22 - index * 0.005 for index in range(12)],
        }
    )
    feature_frame.to_excel(tmp_path / "curated_dataset1.xlsx", index=False)
    feature_frame.assign(WELL="IGS", RT=lambda frame: frame["RT"] + 5).to_excel(
        tmp_path / "curated_dataset2.xlsx",
        index=False,
    )
    feature_frame.assign(
        WELL="Labeled",
        S_h=[0.15 + index * 0.02 for index in range(12)],
    ).to_excel(tmp_path / "curated_dataset3.xlsx", index=False)

    result = run_three_dataset_pipeline(
        data_dir=tmp_path,
        train_file="curated_dataset3.xlsx",
        test_files=("curated_dataset1.xlsx", "curated_dataset2.xlsx"),
        requested_target="S_h",
        requested_task="regression",
        output_root=tmp_path / "outputs_runtime",
        model_root=tmp_path / "models_runtime",
        run_label="dataset3_train_run",
    )

    run_dir = Path(result["run_dir"])
    test_metrics = pd.read_csv(run_dir / "test_metrics.csv")
    predictions = pd.read_csv(run_dir / "predictions_curated_dataset1.csv")

    assert result["status"] == "trained"
    assert result["target"]["column"] == "S_h"
    assert set(test_metrics["status"]) == {"predicted_unlabeled"}
    assert set(test_metrics["dataset"]) == {"curated_dataset1", "curated_dataset2"}
    assert (test_metrics["rows_scored"] > 0).all()
    assert "y_pred" in predictions.columns
    assert "y_true" not in predictions.columns
    assert (run_dir / "predictions_curated_dataset2.csv").exists()


def test_three_dataset_header_scan_finds_target_hints_across_workbook_sheets(tmp_path: Path) -> None:
    for index in range(1, 4):
        workbook_path = tmp_path / f"curated_dataset{index}.xlsx"
        with pd.ExcelWriter(workbook_path) as writer:
            pd.DataFrame(
                {
                    "WELL": ["MTE"],
                    "DEPTH": [500],
                    "GR": [42],
                    "RT": [35],
                    "RHOB": [2.2],
                }
            ).to_excel(writer, sheet_name="logs", index=False)
            pd.DataFrame(
                {
                    "WELL": ["MTE"],
                    "DEPTH": [500],
                    "Class": ["hydrate"],
                    "Hydrate_Sat": [0.25],
                }
            ).to_excel(writer, sheet_name="targets", index=False)

    result = scan_three_dataset_headers(
        tmp_path,
        output_root=tmp_path / "outputs_runtime",
        run_label="header_scan_test",
    )

    run_dir = Path(result["run_dir"])
    target_hints = pd.read_csv(run_dir / "target_header_hints.csv")
    columns = pd.read_csv(run_dir / "workbook_column_inventory.csv")

    assert result["target_hint_count"] >= 6
    assert {"Class", "Hydrate_Sat"}.issubset(set(target_hints["original_header"]))
    assert "candidate_feature_or_context" in set(columns["role_hint"])
    assert (run_dir / "suggested_commands.txt").read_text(encoding="utf-8").startswith(
        "python 01_pipeline\\run_three_dataset_ml_pipeline.py"
    )


def test_three_dataset_header_scan_suggests_training_workbook_that_has_target(tmp_path: Path) -> None:
    logs = pd.DataFrame({"WELL": ["MTE"], "DEPTH": [500], "GR": [42], "RT": [35], "RHOB": [2.2]})
    logs.to_excel(tmp_path / "curated_dataset1.xlsx", index=False)
    logs.to_excel(tmp_path / "curated_dataset2.xlsx", index=False)
    logs.assign(S_h=[0.25]).to_excel(tmp_path / "curated_dataset3.xlsx", index=False)

    result = scan_three_dataset_headers(
        tmp_path,
        output_root=tmp_path / "outputs_runtime",
        run_label="dataset3_target_scan",
    )

    command = (Path(result["run_dir"]) / "suggested_commands.txt").read_text(encoding="utf-8")
    assert "--train curated_dataset3.xlsx" in command
    assert "--test curated_dataset1.xlsx curated_dataset2.xlsx" in command
    assert '--target "S_h"' in command
