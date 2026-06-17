from __future__ import annotations

from pathlib import Path
import json
from typing import Any

import pandas as pd


RUNTIME_OUTPUT_DIR = "outputs_runtime"
RUN_SUMMARY_FILES = (
    "run_summary.csv",
    "train_metrics.csv",
)
FEATURE_FILES = (
    "feature_columns_by_target.csv",
    "feature_columns.csv",
)
EXCLUSION_FILES = (
    "excluded_feature_columns_by_target.csv",
)
DATASET_FILES = (
    "sheet_inventory.csv",
    "dataset_inventory.csv",
)


def read_csv_if_present(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def read_manifest_if_present(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def find_runtime_run_dirs(project_root: Path) -> list[Path]:
    output_root = Path(project_root) / RUNTIME_OUTPUT_DIR
    if not output_root.exists():
        return []
    candidates: list[Path] = []
    for path in output_root.iterdir():
        if not path.is_dir():
            continue
        if any((path / name).exists() for name in (*RUN_SUMMARY_FILES, *FEATURE_FILES, "run_manifest.json")):
            candidates.append(path)
    return sorted(candidates, key=lambda path: path.stat().st_mtime, reverse=True)


def feature_family(feature_column: object) -> str:
    name = str(feature_column).lower()
    if name in {"gr_api", "vshale"} or "gamma" in name:
        return "lithology_shale_proxy"
    if name in {"rt_ohm_m", "archie_hydrate_proxy"} or "res" in name:
        return "resistivity_hydrate_proxy"
    if "porosity" in name or name in {"rhob_g_cc", "nmr_porosity_vv"}:
        return "porosity_density_nmr"
    if name.startswith("vp") or name.startswith("vs") or "velocity" in name or "modulus" in name:
        return "elastic_velocity"
    if "caliper" in name or "washout" in name:
        return "qc_caliper"
    if "stability" in name or "ghsz" in name or "temperature" in name or "pressure" in name:
        return "stability_context"
    return "unresolved_or_local_curve"


def summarize_run_dir(run_dir: Path) -> dict[str, pd.DataFrame | dict[str, Any]]:
    manifest = read_manifest_if_present(run_dir / "run_manifest.json")
    summary_rows: list[dict[str, Any]] = []

    run_summary = read_csv_if_present(run_dir / "run_summary.csv")
    if not run_summary.empty:
        for _, row in run_summary.iterrows():
            summary_rows.append(
                {
                    "run_name": run_dir.name,
                    "run_type": "multi_saturation_targets",
                    "target_column": row.get("target_column", ""),
                    "target_sheet": row.get("target_sheet", ""),
                    "status": row.get("status", ""),
                    "model_kind": "random_forest_regressor",
                    "training_rows": row.get("training_rows", pd.NA),
                    "feature_count": row.get("feature_count", pd.NA),
                    "train_mae": row.get("train_mae", pd.NA),
                    "train_rmse": row.get("train_rmse", pd.NA),
                    "train_r2": row.get("train_r2", pd.NA),
                    "test_status": "not_claimed_training_fit_only",
                    "prediction_file_count": row.get("prediction_file_count", pd.NA),
                    "guardrail": "training-fit prototype; not final validated performance",
                }
            )

    train_metrics = read_csv_if_present(run_dir / "train_metrics.csv")
    if not train_metrics.empty:
        for _, row in train_metrics.iterrows():
            summary_rows.append(
                {
                    "run_name": run_dir.name,
                    "run_type": "three_dataset_split",
                    "target_column": row.get("target_column", ""),
                    "target_sheet": "",
                    "status": "trained",
                    "model_kind": row.get("model_kind", ""),
                    "training_rows": row.get("rows_scored", pd.NA),
                    "feature_count": row.get("feature_count", pd.NA),
                    "train_mae": row.get("mae", pd.NA),
                    "train_rmse": row.get("rmse", pd.NA),
                    "train_r2": row.get("r2", pd.NA),
                    "test_status": "see_test_metrics",
                    "prediction_file_count": pd.NA,
                    "guardrail": "whole-workbook split summary; row-level outputs remain local",
                }
            )

    feature_frames: list[pd.DataFrame] = []
    for file_name in FEATURE_FILES:
        frame = read_csv_if_present(run_dir / file_name)
        if frame.empty:
            continue
        if "feature_column" not in frame.columns:
            continue
        frame = frame.copy()
        frame.insert(0, "run_name", run_dir.name)
        frame["feature_family"] = frame["feature_column"].map(feature_family)
        feature_frames.append(frame)

    exclusion_frames: list[pd.DataFrame] = []
    for file_name in EXCLUSION_FILES:
        frame = read_csv_if_present(run_dir / file_name)
        if frame.empty:
            continue
        frame = frame.copy()
        frame.insert(0, "run_name", run_dir.name)
        exclusion_frames.append(frame)

    dataset_frames: list[pd.DataFrame] = []
    for file_name in DATASET_FILES:
        frame = read_csv_if_present(run_dir / file_name)
        if frame.empty:
            continue
        frame = frame.copy()
        frame.insert(0, "run_name", run_dir.name)
        dataset_frames.append(frame)

    test_metrics = read_csv_if_present(run_dir / "test_metrics.csv")
    if not test_metrics.empty:
        test_metrics = test_metrics.copy()
        test_metrics.insert(0, "run_name", run_dir.name)

    return {
        "manifest": manifest,
        "summary": pd.DataFrame(summary_rows),
        "features": pd.concat(feature_frames, ignore_index=True) if feature_frames else pd.DataFrame(),
        "exclusions": pd.concat(exclusion_frames, ignore_index=True) if exclusion_frames else pd.DataFrame(),
        "datasets": pd.concat(dataset_frames, ignore_index=True) if dataset_frames else pd.DataFrame(),
        "test_metrics": test_metrics,
    }


def load_local_model_run_tracker(project_root: Path, *, max_runs: int = 12) -> dict[str, pd.DataFrame]:
    run_dirs = find_runtime_run_dirs(Path(project_root))[:max_runs]
    summaries: list[pd.DataFrame] = []
    features: list[pd.DataFrame] = []
    exclusions: list[pd.DataFrame] = []
    datasets: list[pd.DataFrame] = []
    tests: list[pd.DataFrame] = []
    manifests: list[dict[str, Any]] = []

    for run_dir in run_dirs:
        parsed = summarize_run_dir(run_dir)
        if isinstance(parsed["summary"], pd.DataFrame) and not parsed["summary"].empty:
            summaries.append(parsed["summary"])
        if isinstance(parsed["features"], pd.DataFrame) and not parsed["features"].empty:
            features.append(parsed["features"])
        if isinstance(parsed["exclusions"], pd.DataFrame) and not parsed["exclusions"].empty:
            exclusions.append(parsed["exclusions"])
        if isinstance(parsed["datasets"], pd.DataFrame) and not parsed["datasets"].empty:
            datasets.append(parsed["datasets"])
        if isinstance(parsed["test_metrics"], pd.DataFrame) and not parsed["test_metrics"].empty:
            tests.append(parsed["test_metrics"])
        manifest = parsed["manifest"]
        if isinstance(manifest, dict) and manifest:
            manifests.append({"run_name": run_dir.name, **manifest})

    return {
        "runs": pd.DataFrame({"run_name": [path.name for path in run_dirs], "run_dir": [str(path) for path in run_dirs]}),
        "summary": pd.concat(summaries, ignore_index=True) if summaries else pd.DataFrame(),
        "features": pd.concat(features, ignore_index=True) if features else pd.DataFrame(),
        "exclusions": pd.concat(exclusions, ignore_index=True) if exclusions else pd.DataFrame(),
        "datasets": pd.concat(datasets, ignore_index=True) if datasets else pd.DataFrame(),
        "test_metrics": pd.concat(tests, ignore_index=True) if tests else pd.DataFrame(),
        "manifests": pd.DataFrame(manifests),
    }


def stability_runtime_integration_plan_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Runtime layer": "Public stability screen",
                "How it enters DOE model review": "Join as well/depth context, admissibility flag, confidence, and caveat.",
                "Allowed claim": "Physically admissible under locked pressure-temperature-phase assumptions.",
                "Not allowed": "Hydrate proof, occurrence label, saturation target, or sweet-spot rank.",
            },
            {
                "Runtime layer": "Feature matrix",
                "How it enters DOE model review": "Measured/derived logs only after target leakage, depth-axis, and helper-column exclusions.",
                "Allowed claim": "Cleaned X_allowed input table for prototype training.",
                "Not allowed": "Target-derived variables or row-random train/test leakage.",
            },
            {
                "Runtime layer": "Targets",
                "How it enters DOE model review": "Saturation columns train separate regression heads; occurrence requires separate evidence.",
                "Allowed claim": "Prototype target contract and target-specific model runs.",
                "Not allowed": "Final occurrence or saturation claims before held-out well validation.",
            },
            {
                "Runtime layer": "Website tracker",
                "How it enters DOE model review": "Reads ignored local run summaries, features, exclusions, and metrics into a review board.",
                "Allowed claim": "Run audit trail and readiness story.",
                "Not allowed": "Public release of row-level predictions, raw workbook rows, or fitted model files.",
            },
        ]
    )
