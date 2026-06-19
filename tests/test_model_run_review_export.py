from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = PROJECT_ROOT / "01_pipeline" / "export_model_run_review_assets.py"


def test_model_run_review_export_writes_row_free_summary_assets(tmp_path: Path) -> None:
    run_dir = tmp_path / "outputs_runtime" / "three_dataset_ml_run_review_test"
    output_dir = tmp_path / "review_assets"
    run_dir.mkdir(parents=True)

    pd.DataFrame(
        [
            {
                "dataset": "curated_dataset1",
                "split": "train",
                "task": "regression",
                "target_column": "Sgh",
                "model_kind": "baseline",
                "feature_count": 3,
                "rows_scored": 20,
                "mae": 0.1,
                "rmse": 0.2,
                "r2": 0.75,
            }
        ]
    ).to_csv(run_dir / "train_metrics.csv", index=False)
    pd.DataFrame(
        [
            {
                "dataset": "curated_dataset2",
                "split": "test",
                "task": "regression",
                "target_column": "Sgh",
                "model_kind": "baseline",
                "feature_count": 3,
                "rows_scored": 8,
                "status": "scored",
                "mae": 0.2,
                "rmse": 0.3,
                "r2": 0.5,
                "blocked_reason": "",
            }
        ]
    ).to_csv(run_dir / "test_metrics.csv", index=False)
    pd.DataFrame(
        [
            {"feature_column": "gr_api", "non_null_rows": 20},
            {"feature_column": "rt_ohm_m", "non_null_rows": 20},
            {"feature_column": "vp_vs_ratio", "non_null_rows": 20},
        ]
    ).to_csv(run_dir / "feature_columns.csv", index=False)

    result = subprocess.run(
        [
            sys.executable,
            str(CLI_SCRIPT),
            "--project-root",
            str(tmp_path),
            "--output-dir",
            str(output_dir),
        ],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Review assets written" in result.stdout
    manifest = json.loads((output_dir / "asset_manifest.json").read_text(encoding="utf-8"))
    assert manifest["target_run_count"] == 1
    assert "row-level predictions" in manifest["not_exported"]
    assert (output_dir / "public_safe_model_run_summary.csv").exists()
    assert (output_dir / "public_safe_run_comparison.csv").exists()
    assert (output_dir / "feature_family_counts.csv").exists()
    assert (output_dir / "model_run_review_brief.md").exists()

    comparison = pd.read_csv(output_dir / "public_safe_run_comparison.csv")
    assert "mean_train_r2" not in comparison.columns
    summary_text = (output_dir / "public_safe_model_run_summary.csv").read_text(encoding="utf-8")
    assert "prediction" not in summary_text.lower()
