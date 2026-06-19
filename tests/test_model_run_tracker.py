from __future__ import annotations

from pathlib import Path

import pandas as pd

from dashboard.runtime.model_run_tracker import (
    feature_family,
    load_local_model_run_tracker,
    stability_runtime_integration_plan_frame,
)


def test_model_run_tracker_loads_local_multi_saturation_summary(tmp_path: Path) -> None:
    run_dir = tmp_path / "outputs_runtime" / "multi_saturation_clean_features_test"
    run_dir.mkdir(parents=True)
    pd.DataFrame(
        [
            {
                "target_id": "dataset3_sheet1_S_h",
                "target_column": "S_h",
                "target_sheet": "#1",
                "status": "trained",
                "training_rows": 822,
                "feature_count": 12,
                "train_mae": 0.01,
                "train_rmse": 0.02,
                "train_r2": 0.99,
                "prediction_file_count": 2,
            }
        ]
    ).to_csv(run_dir / "run_summary.csv", index=False)
    pd.DataFrame(
        [
            {"target_id": "dataset3_sheet1_S_h", "feature_column": "gr_api"},
            {"target_id": "dataset3_sheet1_S_h", "feature_column": "vp_vs_ratio"},
            {"target_id": "dataset3_sheet1_S_h", "feature_column": "archie_hydrate_proxy"},
        ]
    ).to_csv(run_dir / "feature_columns_by_target.csv", index=False)
    pd.DataFrame(
        [
            {
                "target_id": "dataset3_sheet1_S_h",
                "feature_policy_version": "clean_feature_matrix_v3_2026_06_16",
                "column": "Depth_ft",
                "canonical_feature": "depth_m",
                "decision": "excluded",
                "reason": "context_depth_unit_or_spreadsheet_helper",
                "numeric_rows": 822,
            }
        ]
    ).to_csv(run_dir / "excluded_feature_columns_by_target.csv", index=False)
    pd.DataFrame([{"workbook": "curated_dataset3.xlsx", "sheet_name": "#1", "rows": 822, "columns": 19}]).to_csv(
        run_dir / "sheet_inventory.csv",
        index=False,
    )

    tracker = load_local_model_run_tracker(tmp_path)

    assert tracker["summary"].loc[0, "target_column"] == "S_h"
    assert tracker["summary"].loc[0, "test_status"] == "not_claimed_training_fit_only"
    assert set(tracker["features"]["feature_family"]) == {
        "lithology_shale_proxy",
        "elastic_velocity",
        "resistivity_hydrate_proxy",
    }
    assert tracker["exclusions"].loc[0, "reason"] == "context_depth_unit_or_spreadsheet_helper"
    assert tracker["datasets"].loc[0, "rows"] == 822
    assert tracker["target_cards"].loc[0, "metric_scope"] == "training_fit_only"
    assert tracker["target_cards"].loc[0, "stability_join_status"] == "not_joined_placeholder"
    assert not bool(tracker["target_cards"].loc[0, "final_claim_ready"])
    assert "prediction_file_count" not in tracker["public_safe_summary"].columns


def test_model_run_tracker_compares_runs_and_validation_status(tmp_path: Path) -> None:
    multi_dir = tmp_path / "outputs_runtime" / "multi_saturation_clean_features_test"
    three_dir = tmp_path / "outputs_runtime" / "three_dataset_ml_run_test"
    multi_dir.mkdir(parents=True)
    three_dir.mkdir(parents=True)

    pd.DataFrame(
        [
            {
                "target_id": "dataset3_sheet1_S_h",
                "target_column": "S_h",
                "target_sheet": "#1",
                "status": "trained",
                "training_rows": 822,
                "feature_count": 3,
                "train_mae": 0.01,
                "train_rmse": 0.02,
                "train_r2": 0.99,
                "prediction_file_count": 2,
            }
        ]
    ).to_csv(multi_dir / "run_summary.csv", index=False)
    pd.DataFrame(
        [
            {"target_id": "dataset3_sheet1_S_h", "feature_column": "gr_api"},
            {"target_id": "dataset3_sheet1_S_h", "feature_column": "vp_vs_ratio"},
            {"target_id": "dataset3_sheet1_S_h", "feature_column": "archie_hydrate_proxy"},
        ]
    ).to_csv(multi_dir / "feature_columns_by_target.csv", index=False)

    pd.DataFrame(
        [
            {
                "dataset": "curated_dataset1",
                "split": "train",
                "task": "regression",
                "target_column": "Sgh",
                "model_kind": "baseline",
                "feature_count": 4,
                "rows_scored": 120,
                "mae": 0.1,
                "rmse": 0.2,
                "r2": 0.75,
            }
        ]
    ).to_csv(three_dir / "train_metrics.csv", index=False)
    pd.DataFrame(
        [
            {
                "dataset": "curated_dataset2",
                "split": "test",
                "task": "regression",
                "target_column": "Sgh",
                "model_kind": "baseline",
                "feature_count": 4,
                "rows_scored": 50,
                "status": "scored",
                "mae": 0.2,
                "rmse": 0.3,
                "r2": 0.5,
                "blocked_reason": "",
            },
            {
                "dataset": "curated_dataset3",
                "split": "test",
                "task": "regression",
                "target_column": "Sgh",
                "model_kind": "baseline",
                "feature_count": 4,
                "rows_scored": 75,
                "status": "predicted_unlabeled",
                "blocked_reason": "target column not present in test workbook",
            },
        ]
    ).to_csv(three_dir / "test_metrics.csv", index=False)
    pd.DataFrame(
        [
            {"feature_column": "gr_api", "non_null_rows": 120},
            {"feature_column": "rt_ohm_m", "non_null_rows": 120},
            {"feature_column": "rhob_g_cc", "non_null_rows": 120},
            {"feature_column": "vp_vs_ratio", "non_null_rows": 120},
        ]
    ).to_csv(three_dir / "feature_columns.csv", index=False)
    pd.DataFrame(
        [
            {
                "source_dataset": "curated_dataset1",
                "split": "train",
                "file_name": "curated_dataset1.xlsx",
                "sheet_name": "#1 well logs",
                "rows": 120,
                "columns": 15,
            }
        ]
    ).to_csv(three_dir / "dataset_inventory.csv", index=False)

    tracker = load_local_model_run_tracker(tmp_path)
    target_cards = tracker["target_cards"]
    run_comparison = tracker["run_comparison"]
    public_summary = tracker["public_safe_summary"]

    assert set(run_comparison["run_name"]) == {"multi_saturation_clean_features_test", "three_dataset_ml_run_test"}
    three_card = target_cards.loc[target_cards["run_name"].eq("three_dataset_ml_run_test")].iloc[0]
    assert three_card["validation_status"] == "external_or_whole_workbook_metrics_present"
    assert bool(three_card["has_external_or_whole_workbook_validation"])
    assert three_card["external_scored_rows"] == 125
    assert public_summary["stability_join_status"].eq("not_joined_placeholder").all()
    assert public_summary["final_claim_ready"].eq(False).all()


def test_model_run_tracker_stability_plan_keeps_guardrail_visible() -> None:
    plan = stability_runtime_integration_plan_frame()

    assert "Public stability screen" in set(plan["Runtime layer"])
    assert plan["Not allowed"].str.contains("Hydrate proof", case=False).any()
    assert feature_family("caliper_in") == "qc_caliper"
