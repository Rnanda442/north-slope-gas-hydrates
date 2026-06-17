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


def test_model_run_tracker_stability_plan_keeps_guardrail_visible() -> None:
    plan = stability_runtime_integration_plan_frame()

    assert "Public stability screen" in set(plan["Runtime layer"])
    assert plan["Not allowed"].str.contains("Hydrate proof", case=False).any()
    assert feature_family("caliper_in") == "qc_caliper"
