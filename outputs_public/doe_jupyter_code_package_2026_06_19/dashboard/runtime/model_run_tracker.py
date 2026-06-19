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
TRAINING_FIT_WARNING = "training-fit only; not validated model performance"
FINAL_CLAIM_REQUIREMENTS = (
    "Needs mentor-approved target authority, fraction-vs-percent units, "
    "whole-well or whole-workbook validation with target-bearing held-out rows, "
    "stability-context join review, and public-release approval."
)
STABILITY_JOIN_PLACEHOLDER = "not_joined_placeholder"


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


def _column_values(frame: pd.DataFrame, column: str) -> pd.Series:
    if column not in frame.columns:
        return pd.Series(dtype=object)
    return frame[column].dropna().astype(str)


def _status_set(frame: pd.DataFrame) -> set[str]:
    return {value.lower() for value in _column_values(frame, "status")}


def _numeric_sum(frame: pd.DataFrame, column: str) -> int:
    if column not in frame.columns:
        return 0
    return int(pd.to_numeric(frame[column], errors="coerce").fillna(0).sum())


def validation_metadata(test_metrics: pd.DataFrame, target_column: object = "") -> dict[str, Any]:
    if test_metrics.empty:
        return {
            "validation_status": "training_fit_only_no_external_metrics",
            "has_external_or_whole_workbook_validation": False,
            "external_scored_rows": 0,
            "external_metric_rows": 0,
            "final_claim_ready": False,
            "final_claim_needed": FINAL_CLAIM_REQUIREMENTS,
        }

    scoped = test_metrics.copy()
    if target_column and "target_column" in scoped.columns:
        matches = scoped["target_column"].astype(str).eq(str(target_column))
        if matches.any():
            scoped = scoped.loc[matches].copy()

    statuses = _status_set(scoped)
    external_metric_rows = int(scoped["status"].astype(str).str.lower().eq("scored").sum()) if "status" in scoped else 0
    scored_rows = _numeric_sum(scoped, "rows_scored")
    if "scored" in statuses:
        validation_status = "external_or_whole_workbook_metrics_present"
        has_validation = True
    elif "predicted_unlabeled" in statuses:
        validation_status = "external_workbook_scored_without_target_metrics"
        has_validation = False
    elif "blocked" in statuses:
        validation_status = "external_validation_blocked"
        has_validation = False
    else:
        validation_status = "training_fit_only_no_external_metrics"
        has_validation = False

    return {
        "validation_status": validation_status,
        "has_external_or_whole_workbook_validation": has_validation,
        "external_scored_rows": scored_rows,
        "external_metric_rows": external_metric_rows,
        "final_claim_ready": False,
        "final_claim_needed": FINAL_CLAIM_REQUIREMENTS,
    }


def annotate_summary(summary: pd.DataFrame, test_metrics: pd.DataFrame) -> pd.DataFrame:
    if summary.empty:
        return summary
    annotated = summary.copy()
    records: list[dict[str, Any]] = []
    for _, row in annotated.iterrows():
        validation = validation_metadata(test_metrics, row.get("target_column", ""))
        records.append(
            {
                "metric_scope": "training_fit_only",
                "training_metric_warning": TRAINING_FIT_WARNING,
                "validation_status": validation["validation_status"],
                "has_external_or_whole_workbook_validation": validation[
                    "has_external_or_whole_workbook_validation"
                ],
                "external_scored_rows": validation["external_scored_rows"],
                "external_metric_rows": validation["external_metric_rows"],
                "final_claim_ready": validation["final_claim_ready"],
                "final_claim_needed": validation["final_claim_needed"],
                "stability_join_status": STABILITY_JOIN_PLACEHOLDER,
                "stability_join_needed": (
                    "Join by approved well/depth interval after coordinate, depth, "
                    "temperature, pressure, and phase-curve assumptions are reviewed."
                ),
            }
        )
    return pd.concat([annotated.reset_index(drop=True), pd.DataFrame(records)], axis=1)


def _target_feature_subset(features: pd.DataFrame, run_name: str, target_id: object) -> pd.DataFrame:
    if features.empty:
        return pd.DataFrame()
    scoped = features.loc[features["run_name"].astype(str).eq(str(run_name))].copy()
    if target_id and "target_id" in scoped.columns:
        matches = scoped["target_id"].astype(str).eq(str(target_id))
        if matches.any():
            return scoped.loc[matches].copy()
    return scoped


def _target_exclusion_subset(exclusions: pd.DataFrame, run_name: str, target_id: object) -> pd.DataFrame:
    if exclusions.empty:
        return pd.DataFrame()
    scoped = exclusions.loc[exclusions["run_name"].astype(str).eq(str(run_name))].copy()
    if target_id and "target_id" in scoped.columns:
        matches = scoped["target_id"].astype(str).eq(str(target_id))
        if matches.any():
            return scoped.loc[matches].copy()
    return scoped


def _family_count_label(frame: pd.DataFrame) -> str:
    if frame.empty or "feature_family" not in frame.columns:
        return ""
    counts = frame["feature_family"].fillna("unknown").value_counts().sort_index()
    return "; ".join(f"{family}: {count}" for family, count in counts.items())


def build_target_cards(
    summary: pd.DataFrame,
    features: pd.DataFrame,
    exclusions: pd.DataFrame,
    test_metrics: pd.DataFrame,
) -> pd.DataFrame:
    if summary.empty:
        return pd.DataFrame()

    rows: list[dict[str, Any]] = []
    for _, row in summary.iterrows():
        run_name = str(row.get("run_name", ""))
        target_id = row.get("target_id", "")
        target_features = _target_feature_subset(features, run_name, target_id)
        target_exclusions = _target_exclusion_subset(exclusions, run_name, target_id)
        validation = validation_metadata(test_metrics, row.get("target_column", ""))
        excluded_count = 0
        if not target_exclusions.empty:
            if "decision" in target_exclusions.columns:
                excluded_count = int(target_exclusions["decision"].astype(str).eq("excluded").sum())
            else:
                excluded_count = len(target_exclusions)
        rows.append(
            {
                "run_name": run_name,
                "run_type": row.get("run_type", ""),
                "target_id": target_id,
                "target_column": row.get("target_column", ""),
                "target_sheet": row.get("target_sheet", ""),
                "status": row.get("status", ""),
                "model_kind": row.get("model_kind", ""),
                "training_rows": row.get("training_rows", pd.NA),
                "feature_count": row.get("feature_count", len(target_features)),
                "unique_feature_families": int(target_features["feature_family"].nunique())
                if "feature_family" in target_features
                else 0,
                "feature_family_counts": _family_count_label(target_features),
                "excluded_column_count": excluded_count,
                "exclusion_reason_count": int(target_exclusions["reason"].nunique())
                if "reason" in target_exclusions
                else 0,
                "train_r2": row.get("train_r2", pd.NA),
                "metric_scope": "training_fit_only",
                "training_metric_warning": TRAINING_FIT_WARNING,
                "validation_status": validation["validation_status"],
                "has_external_or_whole_workbook_validation": validation[
                    "has_external_or_whole_workbook_validation"
                ],
                "external_scored_rows": validation["external_scored_rows"],
                "external_metric_rows": validation["external_metric_rows"],
                "stability_join_status": STABILITY_JOIN_PLACEHOLDER,
                "stability_allowed_use": "context, mask, confidence, and caveat only",
                "final_claim_ready": validation["final_claim_ready"],
                "final_claim_needed": validation["final_claim_needed"],
            }
        )
    return pd.DataFrame(rows)


def build_run_comparison(target_cards: pd.DataFrame, features: pd.DataFrame, exclusions: pd.DataFrame) -> pd.DataFrame:
    if target_cards.empty:
        return pd.DataFrame()

    rows: list[dict[str, Any]] = []
    for run_name, group in target_cards.groupby("run_name", dropna=False):
        run_features = features.loc[features["run_name"].astype(str).eq(str(run_name))] if not features.empty else pd.DataFrame()
        run_exclusions = (
            exclusions.loc[exclusions["run_name"].astype(str).eq(str(run_name))]
            if not exclusions.empty
            else pd.DataFrame()
        )
        rows.append(
            {
                "run_name": run_name,
                "run_types": ", ".join(sorted(set(group["run_type"].dropna().astype(str)))),
                "trained_target_runs": int(group["status"].astype(str).eq("trained").sum()),
                "target_columns": ", ".join(sorted(set(group["target_column"].dropna().astype(str)))),
                "mean_train_r2": pd.to_numeric(group.get("train_r2"), errors="coerce").mean(),
                "unique_feature_columns": int(run_features["feature_column"].nunique())
                if "feature_column" in run_features
                else 0,
                "feature_families": int(run_features["feature_family"].nunique())
                if "feature_family" in run_features
                else 0,
                "excluded_columns_audited": int(run_exclusions["decision"].astype(str).eq("excluded").sum())
                if "decision" in run_exclusions
                else len(run_exclusions),
                "validation_statuses": "; ".join(sorted(set(group["validation_status"].dropna().astype(str)))),
                "has_external_or_whole_workbook_validation": bool(
                    group["has_external_or_whole_workbook_validation"].astype(bool).any()
                ),
                "stability_join_status": STABILITY_JOIN_PLACEHOLDER,
                "final_claim_ready": bool(group["final_claim_ready"].astype(bool).all()) if len(group) else False,
                "final_claim_needed": FINAL_CLAIM_REQUIREMENTS,
            }
        )
    return pd.DataFrame(rows)


def build_public_safe_summary(target_cards: pd.DataFrame) -> pd.DataFrame:
    if target_cards.empty:
        return pd.DataFrame()
    public_columns = [
        "run_name",
        "run_type",
        "target_column",
        "target_sheet",
        "status",
        "model_kind",
        "training_rows",
        "feature_count",
        "unique_feature_families",
        "feature_family_counts",
        "excluded_column_count",
        "exclusion_reason_count",
        "metric_scope",
        "validation_status",
        "has_external_or_whole_workbook_validation",
        "external_scored_rows",
        "external_metric_rows",
        "stability_join_status",
        "stability_allowed_use",
        "final_claim_ready",
        "final_claim_needed",
    ]
    return target_cards[[column for column in public_columns if column in target_cards.columns]].copy()


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
                    "target_id": row.get("target_id", ""),
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
                    "target_id": row.get("target_column", ""),
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

    summary = annotate_summary(pd.DataFrame(summary_rows), test_metrics)

    return {
        "manifest": manifest,
        "summary": summary,
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

    summary = pd.concat(summaries, ignore_index=True) if summaries else pd.DataFrame()
    feature_frame = pd.concat(features, ignore_index=True) if features else pd.DataFrame()
    exclusion_frame = pd.concat(exclusions, ignore_index=True) if exclusions else pd.DataFrame()
    dataset_frame = pd.concat(datasets, ignore_index=True) if datasets else pd.DataFrame()
    test_frame = pd.concat(tests, ignore_index=True) if tests else pd.DataFrame()
    target_cards = build_target_cards(summary, feature_frame, exclusion_frame, test_frame)
    run_comparison = build_run_comparison(target_cards, feature_frame, exclusion_frame)
    public_safe_summary = build_public_safe_summary(target_cards)

    return {
        "runs": pd.DataFrame({"run_name": [path.name for path in run_dirs], "run_dir": [str(path) for path in run_dirs]}),
        "summary": summary,
        "target_cards": target_cards,
        "run_comparison": run_comparison,
        "public_safe_summary": public_safe_summary,
        "features": feature_frame,
        "exclusions": exclusion_frame,
        "datasets": dataset_frame,
        "test_metrics": test_frame,
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
