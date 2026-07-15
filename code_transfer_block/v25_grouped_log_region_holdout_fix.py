# V25 grouped-log region holdout fix
#
# Paste this over the V25 grouped-log helper block in the V25 notebook, or run
# it in a new cell after the leave-one-well-out V25 tables have been created.
# It fixes the crash:
#
#     ValueError: cannot insert task_type, already exists
#
# Cause: the candidate metrics tables may already contain a task_type column.
# Fix: assign task/task_type and then reorder columns, instead of using
# DataFrame.insert on names that may already be present.

from typing import Any

import numpy as np
import pandas as pd


V25_REGION_HOLDOUT_LABELS = {
    "WellA": "Canada/Mallik WellA holdout",
    "WellC": "Alaska North Slope WellC holdout",
}

if "V25_REGION_HOLDOUT_WELLS" not in globals():
    V25_REGION_HOLDOUT_WELLS = ["WellA", "WellC"]

if "V25_GROUPED_LOG_FEATURE_SETS" not in globals():
    V25_GROUPED_LOG_FEATURE_SETS = [
        "safe_normalized",
        "all_allowed_except_density_porosity_review",
        "all_allowed_inputs_review",
        "equation_proxy_review",
        "measured_only",
    ]


def v25_feature_group_role(feature_set: Any) -> str:
    name = str(feature_set)
    if name == "safe_normalized":
        return "baseline_safe_logs"
    if name == "all_allowed_except_density_porosity_review":
        return "grouped_logs_without_density_porosity_family"
    if name == "all_allowed_inputs_review":
        return "all_allowed_logs_and_safe_equations"
    if name == "equation_proxy_review":
        return "equation_proxy_package"
    if name == "measured_only":
        return "measured_log_only_baseline"
    return "other_candidate_feature_set"


def v25_pick_best_grouped_log_rows(
    frame: pd.DataFrame,
    *,
    task: str,
    task_type: str,
) -> pd.DataFrame:
    if frame is None or frame.empty:
        return pd.DataFrame()
    required = {"v25_heldout_well", "v25_train_wells", "feature_set"}
    if not required.issubset(frame.columns):
        return pd.DataFrame()

    work = frame.copy()
    work = work[work["v25_heldout_well"].astype(str).isin(V25_REGION_HOLDOUT_WELLS)].copy()
    work = work[work["feature_set"].astype(str).isin(V25_GROUPED_LOG_FEATURE_SETS)].copy()
    if work.empty:
        return pd.DataFrame()

    numeric_columns = [
        "rmse",
        "mae",
        "r2",
        "bias",
        "saturation_precision",
        "saturation_recall",
        "saturation_f1",
        "saturation_accuracy",
        "accuracy",
        "balanced_accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
        "validation_rows",
        "train_rows",
        "feature_count",
    ]
    for column in numeric_columns:
        if column in work.columns:
            work[column] = pd.to_numeric(work[column], errors="coerce")

    rows: list[pd.Series] = []
    for (_heldout_well, _feature_set), group in work.groupby(
        ["v25_heldout_well", "feature_set"],
        dropna=False,
    ):
        group = group.copy()
        if task_type == "regression":
            sort_cols = [c for c in ["rmse", "mae", "r2"] if c in group.columns]
            ascending = [c in {"rmse", "mae"} for c in sort_cols]
        else:
            sort_cols = [c for c in ["f1", "balanced_accuracy", "accuracy", "roc_auc"] if c in group.columns]
            ascending = [False] * len(sort_cols)
        if sort_cols:
            group = group.sort_values(sort_cols, ascending=ascending, na_position="last")
        rows.append(group.iloc[0])

    if not rows:
        return pd.DataFrame()

    out = pd.DataFrame(rows).reset_index(drop=True)

    # Assign instead of insert so reruns and existing metric columns are safe.
    out["v25_region_question"] = (
        "WellA Canada/Mallik holdout vs WellC Alaska holdout grouped-log comparison"
    )
    out["task"] = task
    out["task_type"] = task_type
    out["v25_region_holdout_label"] = (
        out["v25_heldout_well"]
        .map(V25_REGION_HOLDOUT_LABELS)
        .fillna(out["v25_heldout_well"].astype(str))
    )
    out["v25_feature_group_role"] = out["feature_set"].map(v25_feature_group_role)
    out["v25_selection_guardrail"] = (
        "External held-out metrics are summarized after train-pool CV selection; "
        "this table is diagnostic evidence, not a held-out-row winner selection rule."
    )
    out["v25_claim_boundary"] = (
        "Known-four-well development comparison; not blind new-well validation "
        "or gas-origin proof by itself."
    )

    metric_cols = [
        "rmse",
        "mae",
        "r2",
        "bias",
        "saturation_precision",
        "saturation_recall",
        "saturation_f1",
        "saturation_accuracy",
        "accuracy",
        "balanced_accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
    ]
    out["baseline_feature_set"] = "safe_normalized"

    for (_heldout_well, _task_group), idxs in out.groupby(
        ["v25_heldout_well", "task_type"],
        dropna=False,
    ).groups.items():
        idxs = list(idxs)
        subset = out.loc[idxs]
        baseline_rows = subset[subset["feature_set"].astype(str).eq("safe_normalized")]
        if baseline_rows.empty:
            baseline_rows = subset.head(1)
            out.loc[idxs, "baseline_feature_set"] = str(
                baseline_rows.iloc[0].get("feature_set", "")
            )
        baseline = baseline_rows.iloc[0]
        for column in metric_cols:
            if column not in out.columns:
                continue
            base_value = pd.to_numeric(
                pd.Series([baseline.get(column, np.nan)]),
                errors="coerce",
            ).iloc[0]
            out.loc[idxs, f"baseline_{column}"] = base_value
            out.loc[idxs, f"delta_{column}_vs_baseline"] = (
                pd.to_numeric(out.loc[idxs, column], errors="coerce") - base_value
            )

    if "delta_rmse_vs_baseline" in out.columns:
        out["rmse_improvement_vs_baseline"] = -out["delta_rmse_vs_baseline"]

    ordered_first = [
        "v25_region_question",
        "task",
        "task_type",
        "v25_region_holdout_label",
        "v25_heldout_well",
        "v25_train_wells",
        "feature_set",
        "v25_feature_group_role",
        "model",
        "validation_scope",
        "selection_stage",
        "feature_count",
        "train_rows",
        "validation_rows",
        "baseline_feature_set",
    ]
    ordered: list[str] = []

    def add_ordered_column(column: str) -> None:
        if column in out.columns and column not in ordered:
            ordered.append(column)

    for column in ordered_first:
        add_ordered_column(column)
    for column in out.columns:
        if (
            column in metric_cols
            or column.startswith("baseline_")
            or column.startswith("delta_")
            or column.endswith("_improvement_vs_baseline")
        ):
            add_ordered_column(column)
    for column in ["v25_selection_guardrail", "v25_claim_boundary"]:
        add_ordered_column(column)
    for column in out.columns:
        add_ordered_column(column)
    return out[ordered].reset_index(drop=True)


def v25_build_region_holdout_grouped_log_comparison() -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    hydrate_all = globals().get("v25_loo_hydrate_all_metrics_df", pd.DataFrame())
    occurrence_all = globals().get("v25_loo_occurrence_all_metrics_df", pd.DataFrame())

    hydrate = v25_pick_best_grouped_log_rows(
        hydrate_all,
        task="hydrate_saturation",
        task_type="regression",
    )
    if not hydrate.empty:
        frames.append(hydrate)

    occurrence = v25_pick_best_grouped_log_rows(
        occurrence_all,
        task="hydrate_occurrence",
        task_type="classification",
    )
    if not occurrence.empty:
        frames.append(occurrence)

    if not frames:
        return pd.DataFrame(
            [
                {
                    "v25_region_question": (
                        "WellA Canada/Mallik holdout vs WellC Alaska holdout "
                        "grouped-log comparison"
                    ),
                    "status": "no_rows_available",
                    "reason": (
                        "Leave-one-well-out candidate metrics were empty or "
                        "V25_REGION_HOLDOUT_WELLS/V25_GROUPED_LOG_FEATURE_SETS "
                        "did not match available rows."
                    ),
                    "requested_holdout_wells": "+".join(V25_REGION_HOLDOUT_WELLS),
                    "requested_feature_sets": "+".join(V25_GROUPED_LOG_FEATURE_SETS),
                    "v25_selection_guardrail": "No external heldout metrics were used for model selection.",
                }
            ]
        )

    return pd.concat(frames, ignore_index=True, sort=False)


v25_region_holdout_grouped_log_df = v25_build_region_holdout_grouped_log_comparison()

print("V25 grouped-log region holdout comparison rebuilt:")
print(v25_region_holdout_grouped_log_df.shape)
if "display" in globals():
    display(v25_region_holdout_grouped_log_df)
