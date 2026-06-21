from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any

import numpy as np
import pandas as pd

from dashboard.runtime.core_calibration import match_core_intervals_to_nearest_logs
from dashboard.runtime.loaders import standardize_curve_columns
from dashboard.runtime.three_dataset_pipeline import (
    TargetSpec,
    build_model_pipeline,
    choose_target,
    clean_numeric_frame,
    clean_numeric_series,
    evaluate_predictions,
    make_feature_matrix,
    sanitize_label,
)


FOUR_WELL_LOCATION_INDEX = "four_well_case_location_index_2026-06-19.csv"
FOUR_WELL_CORE_EVIDENCE_REGISTRY = "four_well_core_evidence_registry_2026-06-20.csv"
FOUR_WELL_LOG_TEMPLATE = "four_well_log_table_template_2026-06-20.csv"
FOUR_WELL_CORE_TEMPLATE = "four_well_core_sample_template_2026-06-20.csv"
FOUR_WELL_SPLIT_TEMPLATE = "four_well_split_registry_template_2026-06-20.csv"
FOUR_WELL_RUNTIME_MANIFEST_TEMPLATE = "four_well_runtime_manifest_template_2026-06-20.csv"
PUBLIC_ML_FEATURE_SCAFFOLD = "public_ml_feature_scaffold_2026-06-15.csv"
STABILITY_SCREEN = "stability_screen_2026-06-14_methane_5ppt_v1.csv"
WELL_STABILITY_CONTEXT = "north_slope_well_stability_context_2026-06-14.csv"

DEFAULT_LOG_FILE = "four_well_logs.csv"
DEFAULT_CORE_FILE = "four_well_core_samples.csv"
DEFAULT_SPLIT_FILE = "four_well_split_registry.csv"

DEPTH_FT_HEADER_HINTS = {
    "depthft",
    "depthfeet",
    "depthinfeet",
    "depthfttvd",
    "truedepthft",
    "mdft",
    "tvdft",
}
DEPTH_UNIT_HEADER_HINTS = {"depthunit", "depthunits", "depthsunit", "depthsunitd", "depthsunitc"}
API_HEADER_HINTS = {"api", "apinumber", "api_number", "apiuwi", "uwi"}
OBJECT_ID_HEADER_HINTS = {"objectid", "object_id"}
SPLIT_VALUES = {"train", "validation", "validate", "test", "predict", "review", "holdout"}

FOUR_WELL_ALLOWED_CONTEXT_FEATURES = {
    "inside_public_hydrate_au",
    "stability_interval_available",
    "depth_inside_stability_window",
    "well_reaches_stability_zone",
    "tvd_m",
    "permafrost_base_m",
    "permafrost_control_distance_km",
    "pressure_at_tvd_mpa_absolute",
    "stability_top_m",
    "stability_base_m",
    "stability_thickness_m",
    "well_penetrated_stability_thickness_m",
    "depth_minus_stability_top_m",
    "stability_base_minus_depth_m",
}

FOUR_WELL_BLOCKED_FEATURE_COLUMNS = {
    "object_id",
    "permit_number",
    "api_number",
    "api_number_normalized",
    "well_case",
    "case_role",
    "map_label",
    "verified_public_well_name",
    "suspected_aliases",
    "field",
    "pool",
    "current_status",
    "hydrate_assessment_codes",
    "depth_source",
    "split",
    "split_reason",
    "locked_for_validation",
    "stability_result_status",
    "stability_confidence",
    "public_ml_feature_readiness",
    "ml_training_readiness",
    "hydrate_occurrence_label_status",
    "hydrate_saturation_label_status",
    "allowed_ml_use",
    "prohibited_ml_use",
    "label_guardrail",
    "blank_or_block_reason",
    "caveat_codes",
}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str), encoding="utf-8")


def normalize_header_name(column: object) -> str:
    return "".join(character for character in str(column).lower() if character.isalnum())


def normalize_identifier(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return "".join(character for character in text if character.isdigit())


def normalize_alias(value: object) -> str:
    if pd.isna(value):
        return ""
    return "".join(character for character in str(value).lower() if character.isalnum())


def default_public_ml_products_dir(project_root: Path) -> Path:
    return Path(project_root) / "data" / "public_ml_products"


def default_public_stability_products_dir(project_root: Path) -> Path:
    return Path(project_root) / "data" / "public_stability_products"


def _read_csv_if_exists(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def load_four_well_location_index(project_root: Path) -> pd.DataFrame:
    path = default_public_ml_products_dir(project_root) / FOUR_WELL_LOCATION_INDEX
    registry = _read_csv_if_exists(path)
    if registry.empty:
        return registry
    registry = registry.copy()
    registry["api_number_normalized"] = registry.get("api_number", pd.Series(dtype=object)).map(normalize_identifier)
    registry["object_id_normalized"] = registry.get("object_id", pd.Series(dtype=object)).map(normalize_identifier)
    return registry


def load_four_well_core_evidence_registry(project_root: Path) -> pd.DataFrame:
    path = default_public_ml_products_dir(project_root) / FOUR_WELL_CORE_EVIDENCE_REGISTRY
    return _read_csv_if_exists(path)


def load_four_well_stability_context(project_root: Path) -> pd.DataFrame:
    stability_dir = default_public_stability_products_dir(project_root)
    preferred = _read_csv_if_exists(stability_dir / PUBLIC_ML_FEATURE_SCAFFOLD)
    if preferred.empty:
        preferred = _read_csv_if_exists(stability_dir / STABILITY_SCREEN)
    if preferred.empty:
        preferred = _read_csv_if_exists(stability_dir / WELL_STABILITY_CONTEXT)
    if preferred.empty:
        return preferred

    stability = preferred.copy()
    stability["api_number_normalized"] = stability.get("api_number", pd.Series(dtype=object)).map(normalize_identifier)
    stability["object_id_normalized"] = stability.get("object_id", pd.Series(dtype=object)).map(normalize_identifier)
    rename_map = {
        "lat": "wellhead_latitude",
        "lon": "wellhead_longitude",
        "tvd_m": "depth_basis_m",
        "permafrost_base_m": "nearest_permafrost_depth_m",
        "permafrost_control_distance_km": "nearest_ggd223_distance_km",
    }
    for source, target in rename_map.items():
        if source in stability.columns and target not in stability.columns:
            stability[target] = stability[source]
    keep_columns = [
        "object_id_normalized",
        "api_number_normalized",
        "object_id",
        "permit_number",
        "api_number",
        "well_name",
        "field",
        "pool",
        "current_status",
        "wellhead_latitude",
        "wellhead_longitude",
        "depth_basis_m",
        "depth_source",
        "depth_basis_ft",
        "hydrate_assessment_codes",
        "within_hydrate_assessment_unit",
        "nearest_permafrost_depth_m",
        "nearest_ggd223_code",
        "nearest_ggd223_distance_km",
        "temperature_profile_matched",
        "temperature_profile_code",
        "temperature_profile_file",
        "pressure_at_tvd_mpa_absolute",
        "stability_result_status",
        "stability_confidence",
        "stability_interval_calculated",
        "stability_top_m",
        "stability_base_m",
        "stability_thickness_m",
        "well_penetrated_stability_thickness_m",
        "reaches_stability_zone",
        "public_ml_feature_readiness",
        "ml_training_readiness",
        "blank_or_block_reason",
        "caveat_codes",
    ]
    return stability[[column for column in keep_columns if column in stability.columns]].drop_duplicates(
        subset=[column for column in ("object_id_normalized", "api_number_normalized") if column in stability.columns]
    )


def alias_lookup_from_registry(registry: pd.DataFrame) -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    if registry.empty:
        return lookup
    for _, row in registry.iterrows():
        aliases: list[str] = []
        for column in ("well_case", "map_label", "verified_public_well_name"):
            value = row.get(column)
            if pd.notna(value):
                aliases.append(str(value))
        suspected = row.get("suspected_aliases")
        if pd.notna(suspected):
            aliases.extend(part.strip() for part in str(suspected).split(";"))
        for alias in aliases:
            normalized = normalize_alias(alias)
            if normalized:
                lookup[normalized] = row.to_dict()
    return lookup


def find_first_header(frame: pd.DataFrame, hints: set[str]) -> str | None:
    for column in frame.columns:
        if normalize_header_name(column) in hints:
            return str(column)
    return None


def source_depth_unit(frame: pd.DataFrame) -> str:
    unit_column = find_first_header(frame, DEPTH_UNIT_HEADER_HINTS)
    if unit_column is None:
        return ""
    values = frame[unit_column].dropna().astype(str).str.lower()
    if values.empty:
        return ""
    first = values.iloc[0]
    if "ft" in first or "feet" in first:
        return "ft"
    if first in {"m", "meter", "meters", "metre", "metres"}:
        return "m"
    return first


def standardize_four_well_log_frame(frame: pd.DataFrame) -> pd.DataFrame:
    raw = frame.copy()
    api_column = find_first_header(raw, API_HEADER_HINTS)
    if api_column is not None and "api_number" not in raw.columns:
        raw["api_number"] = raw[api_column]
    object_column = find_first_header(raw, OBJECT_ID_HEADER_HINTS)
    if object_column is not None and "object_id" not in raw.columns:
        raw["object_id"] = raw[object_column]

    standardized = standardize_curve_columns(raw)
    if "api_number" in raw.columns:
        standardized["api_number"] = raw["api_number"].map(normalize_identifier)
    if "object_id" in raw.columns:
        standardized["object_id"] = raw["object_id"].map(normalize_identifier)

    depth_ft_column = find_first_header(raw, DEPTH_FT_HEADER_HINTS)
    unit = source_depth_unit(raw)
    if depth_ft_column is not None:
        standardized["source_depth_value"] = pd.to_numeric(raw[depth_ft_column], errors="coerce")
        standardized["source_depth_unit"] = "ft"
        standardized["depth_m"] = standardized["source_depth_value"] * 0.3048
    elif "depth_m" in standardized.columns:
        depth_values = pd.to_numeric(standardized["depth_m"], errors="coerce")
        standardized["source_depth_value"] = depth_values
        standardized["source_depth_unit"] = unit or "m_assumed"
        if unit == "ft":
            standardized["depth_m"] = depth_values * 0.3048
        else:
            standardized["depth_m"] = depth_values

    if "rhob_g_cc" in standardized.columns:
        rhob = pd.to_numeric(standardized["rhob_g_cc"], errors="coerce")
        if rhob.dropna().median() > 10:
            standardized["rhob_g_cc"] = rhob / 1000.0
            standardized["rhob_unit_normalization"] = "kg_m3_to_g_cc"
        else:
            standardized["rhob_unit_normalization"] = "g_cc_or_already_normalized"
    return standardized


def load_four_well_log_csv(data_dir: Path, logs_file: str = DEFAULT_LOG_FILE) -> pd.DataFrame:
    path = Path(data_dir) / logs_file
    if not path.exists():
        raise FileNotFoundError(f"Four-well log CSV does not exist: {path}")
    frame = pd.read_csv(path)
    standardized = standardize_four_well_log_frame(frame)
    standardized["source_dataset"] = Path(logs_file).stem
    standardized["dataset_file"] = Path(logs_file).name
    standardized["row_index"] = np.arange(len(standardized))
    if "well_alias" not in standardized.columns:
        standardized["well_alias"] = standardized.get("well_case", "unknown_well").astype(str)
    return standardized


def load_four_well_core_csv(data_dir: Path, core_file: str | None = DEFAULT_CORE_FILE) -> pd.DataFrame:
    if not core_file:
        return pd.DataFrame()
    path = Path(data_dir) / core_file
    if not path.exists():
        return pd.DataFrame()
    core = pd.read_csv(path)
    if "api_number" in core.columns:
        core["api_number"] = core["api_number"].map(normalize_identifier)
    if "well_alias" not in core.columns and "well_case" in core.columns:
        core["well_alias"] = core["well_case"].astype(str)
    return core


def load_split_registry(data_dir: Path, split_file: str | None = DEFAULT_SPLIT_FILE) -> pd.DataFrame:
    if not split_file:
        return pd.DataFrame()
    path = Path(data_dir) / split_file
    if path.exists():
        split = pd.read_csv(path)
    else:
        public_template = default_public_ml_products_dir(Path(__file__).resolve().parents[2]) / FOUR_WELL_SPLIT_TEMPLATE
        split = _read_csv_if_exists(public_template)
    if split.empty:
        return split
    split = split.copy()
    if "api_number" in split.columns:
        split["api_number_normalized"] = split["api_number"].map(normalize_identifier)
    if "split" in split.columns:
        split["split"] = split["split"].astype(str).str.lower().replace({"validate": "validation"})
    return split


def attach_four_well_identity(logs: pd.DataFrame, registry: pd.DataFrame) -> pd.DataFrame:
    if registry.empty:
        output = logs.copy()
        output["well_case"] = output.get("well_alias", pd.Series(["unmatched"] * len(output))).astype(str)
        return output

    output = logs.copy()
    output["api_number_normalized"] = output.get("api_number", pd.Series([""] * len(output))).map(normalize_identifier)
    output["object_id_normalized"] = output.get("object_id", pd.Series([""] * len(output))).map(normalize_identifier)
    output["well_alias_normalized"] = output.get("well_alias", pd.Series([""] * len(output))).map(normalize_alias)

    registry_by_api = registry.dropna(subset=["api_number_normalized"]).set_index("api_number_normalized", drop=False)
    registry_by_object = registry.dropna(subset=["object_id_normalized"]).set_index("object_id_normalized", drop=False)
    alias_lookup = alias_lookup_from_registry(registry)

    rows: list[dict[str, Any]] = []
    registry_columns = [
        "well_case",
        "case_role",
        "map_label",
        "verified_public_well_name",
        "object_id",
        "permit_number",
        "api_number",
        "field",
        "pool",
    ]
    for _, log_row in output.iterrows():
        matched: dict[str, Any] = {}
        object_key = log_row.get("object_id_normalized", "")
        api_key = log_row.get("api_number_normalized", "")
        alias_key = log_row.get("well_alias_normalized", "")
        if object_key and object_key in registry_by_object.index:
            matched = registry_by_object.loc[object_key].to_dict()
        elif api_key and api_key in registry_by_api.index:
            matched = registry_by_api.loc[api_key].to_dict()
        elif alias_key and alias_key in alias_lookup:
            matched = alias_lookup[alias_key]
        merged = log_row.to_dict()
        for column in registry_columns:
            if column in matched and (column not in merged or pd.isna(merged.get(column)) or merged.get(column) == ""):
                merged[column] = matched[column]
        merged["four_well_identity_status"] = "matched" if matched else "unmatched"
        rows.append(merged)
    return pd.DataFrame(rows)


def attach_stability_context(logs: pd.DataFrame, stability: pd.DataFrame) -> pd.DataFrame:
    if stability.empty:
        return logs.copy()
    output = logs.copy()
    output["api_number_normalized"] = output.get("api_number", pd.Series([""] * len(output))).map(normalize_identifier)
    output["object_id_normalized"] = output.get("object_id", pd.Series([""] * len(output))).map(normalize_identifier)

    stability_columns = [
        column
        for column in stability.columns
        if column not in {"api_number", "object_id", "well_name"}
    ]
    if output["object_id_normalized"].astype(str).str.len().gt(0).any() and "object_id_normalized" in stability:
        merged = output.merge(
            stability[stability_columns],
            on="object_id_normalized",
            how="left",
            suffixes=("", "_stability"),
        )
    else:
        merged = output.copy()
    missing_stability = merged.get("stability_result_status", pd.Series([pd.NA] * len(merged))).isna()
    if missing_stability.any() and "api_number_normalized" in stability:
        api_join = output.loc[missing_stability].merge(
            stability[stability_columns],
            on="api_number_normalized",
            how="left",
            suffixes=("", "_stability"),
        )
        for column in api_join.columns:
            if column not in merged.columns:
                merged[column] = pd.NA
        merged.loc[missing_stability, api_join.columns] = api_join.to_numpy()
    return merged


def add_four_well_context_features(frame: pd.DataFrame) -> pd.DataFrame:
    features = frame.copy()
    if "within_hydrate_assessment_unit" in features.columns:
        features["inside_public_hydrate_au"] = features["within_hydrate_assessment_unit"].astype(str).str.lower().isin(
            {"true", "1", "yes"}
        )
    for column in (
        "depth_m",
        "stability_top_m",
        "stability_base_m",
        "stability_thickness_m",
        "well_penetrated_stability_thickness_m",
        "depth_basis_m",
        "nearest_permafrost_depth_m",
        "nearest_ggd223_distance_km",
        "pressure_at_tvd_mpa_absolute",
    ):
        if column in features.columns:
            features[column] = pd.to_numeric(features[column], errors="coerce")

    if "depth_basis_m" in features.columns and "tvd_m" not in features.columns:
        features["tvd_m"] = features["depth_basis_m"]
    if "nearest_permafrost_depth_m" in features.columns and "permafrost_base_m" not in features.columns:
        features["permafrost_base_m"] = features["nearest_permafrost_depth_m"]
    if "nearest_ggd223_distance_km" in features.columns and "permafrost_control_distance_km" not in features.columns:
        features["permafrost_control_distance_km"] = features["nearest_ggd223_distance_km"]

    if {"stability_top_m", "stability_base_m"}.issubset(features.columns):
        top = pd.to_numeric(features["stability_top_m"], errors="coerce")
        base = pd.to_numeric(features["stability_base_m"], errors="coerce")
        features["stability_interval_available"] = top.notna() & base.notna()
        if "depth_m" in features.columns:
            depth = pd.to_numeric(features["depth_m"], errors="coerce")
            features["depth_inside_stability_window"] = features["stability_interval_available"] & depth.between(top, base)
            features["depth_minus_stability_top_m"] = depth - top
            features["stability_base_minus_depth_m"] = base - depth
    else:
        features["stability_interval_available"] = False

    if "reaches_stability_zone" in features.columns:
        features["well_reaches_stability_zone"] = features["reaches_stability_zone"].astype(str).str.lower().isin(
            {"true", "1", "yes"}
        )
    return features


def attach_split(logs: pd.DataFrame, split_registry: pd.DataFrame) -> pd.DataFrame:
    output = logs.copy()
    if split_registry.empty:
        output["split"] = "review"
        output["split_reason"] = "no split registry supplied"
        return output

    split = split_registry.copy()
    if "well_case" in split.columns:
        by_case = split.dropna(subset=["well_case"]).set_index("well_case", drop=False)
    else:
        by_case = pd.DataFrame()
    if "api_number_normalized" in split.columns:
        by_api = split.dropna(subset=["api_number_normalized"]).set_index("api_number_normalized", drop=False)
    else:
        by_api = pd.DataFrame()

    split_values: list[str] = []
    split_reasons: list[str] = []
    for _, row in output.iterrows():
        matched: pd.Series | None = None
        well_case = row.get("well_case")
        api_key = normalize_identifier(row.get("api_number"))
        if not by_case.empty and pd.notna(well_case) and str(well_case) in by_case.index:
            matched = by_case.loc[str(well_case)]
        elif not by_api.empty and api_key in by_api.index:
            matched = by_api.loc[api_key]
        if matched is None:
            split_values.append("review")
            split_reasons.append("not listed in split registry")
        else:
            split_value = str(matched.get("split", "review")).lower()
            split_values.append(split_value if split_value in SPLIT_VALUES else "review")
            split_reasons.append(str(matched.get("split_reason", "")))
    output["split"] = split_values
    output["split_reason"] = split_reasons
    return output


def four_well_feature_matrix(
    frame: pd.DataFrame,
    *,
    target_columns: set[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    feature_matrix, inventory = make_feature_matrix(frame, target_columns=target_columns)
    selected_columns: list[str] = []
    rows: list[dict[str, Any]] = []
    for column in feature_matrix.columns.astype(str):
        normalized = normalize_header_name(column)
        identity_like = (
            column in FOUR_WELL_BLOCKED_FEATURE_COLUMNS
            or normalized.endswith("id")
            or normalized.endswith("number")
            or "api" in normalized
            or "permit" in normalized
            or "latitude" in normalized
            or "longitude" in normalized
        )
        if identity_like and column not in FOUR_WELL_ALLOWED_CONTEXT_FEATURES:
            continue
        selected_columns.append(column)
        source_row = inventory[inventory["feature_column"].astype(str).eq(column)]
        if source_row.empty:
            rows.append(
                {
                    "feature_column": column,
                    "non_null_rows": int(feature_matrix[column].notna().sum()),
                    "coverage_fraction": round(float(feature_matrix[column].notna().mean()), 4),
                    "minimum": float(feature_matrix[column].min(skipna=True)),
                    "maximum": float(feature_matrix[column].max(skipna=True)),
                    "role": "numeric_model_input",
                    "normalized_by_pipeline": True,
                    "four_well_guardrail": "allowed_context_feature"
                    if column in FOUR_WELL_ALLOWED_CONTEXT_FEATURES
                    else "allowed_log_or_physics_feature",
                }
            )
        else:
            row = source_row.iloc[0].to_dict()
            row["four_well_guardrail"] = (
                "allowed_context_feature"
                if column in FOUR_WELL_ALLOWED_CONTEXT_FEATURES
                else "allowed_log_or_physics_feature"
            )
            rows.append(row)
    return clean_numeric_frame(feature_matrix[selected_columns].copy()), pd.DataFrame(rows)


def prepare_four_well_supervised_table(
    frame: pd.DataFrame,
    *,
    target: TargetSpec,
    feature_columns: list[str],
    target_columns: set[str],
) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    if target.column is None:
        raise ValueError("Cannot prepare a supervised table without a target column.")
    X_all, _ = four_well_feature_matrix(frame, target_columns=target_columns)
    for column in feature_columns:
        if column not in X_all.columns:
            X_all[column] = np.nan
    X = clean_numeric_frame(X_all[feature_columns].copy())
    y_raw = frame[target.column]
    y = clean_numeric_series(y_raw) if target.task == "regression" else y_raw.astype("string")
    mask = y.notna() & X.notna().any(axis=1)
    return X.loc[mask].reset_index(drop=True), y.loc[mask].reset_index(drop=True), frame.loc[mask].reset_index(drop=True)


def prepare_four_well_feature_only_table(
    frame: pd.DataFrame,
    *,
    feature_columns: list[str],
    target_columns: set[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    X_all, _ = four_well_feature_matrix(frame, target_columns=target_columns)
    for column in feature_columns:
        if column not in X_all.columns:
            X_all[column] = np.nan
    X = clean_numeric_frame(X_all[feature_columns].copy())
    mask = X.notna().any(axis=1)
    return X.loc[mask].reset_index(drop=True), frame.loc[mask].reset_index(drop=True)


def four_well_prediction_frame(
    source_frame: pd.DataFrame,
    *,
    y_true: pd.Series | None,
    y_pred: np.ndarray,
    task: str,
    model: Any,
    X: pd.DataFrame,
    target_column: str,
) -> pd.DataFrame:
    output = pd.DataFrame(
        {
            "well_case": source_frame.get("well_case", pd.Series([""] * len(source_frame))).astype(str),
            "api_number": source_frame.get("api_number", pd.Series([""] * len(source_frame))).astype(str),
            "well_alias": source_frame.get("well_alias", pd.Series([""] * len(source_frame))).astype(str),
            "split": source_frame.get("split", pd.Series([""] * len(source_frame))).astype(str),
            "row_index": source_frame.get("row_index", pd.Series(range(len(source_frame)))),
        }
    )
    if "depth_m" in source_frame:
        output["depth_m"] = source_frame["depth_m"]
    output["target_column"] = target_column
    if y_true is not None:
        output["y_true"] = y_true.to_numpy()
    output["y_pred"] = y_pred
    if task == "classification" and hasattr(model, "predict_proba"):
        try:
            probabilities = model.predict_proba(X)
            output["y_pred_probability_max"] = probabilities.max(axis=1)
        except Exception:
            pass
    return output


def dataset_inventory_frame(logs: pd.DataFrame, core: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {
            "table": "logs",
            "rows": int(len(logs)),
            "columns": int(len(logs.columns)),
            "wells": int(logs["well_case"].nunique()) if "well_case" in logs else 0,
            "target_like_columns": ";".join(
                column
                for column in logs.columns.astype(str)
                if re.search(r"sgh|s_h|sh$|nmr_sat|hydrate.*sat", column, re.IGNORECASE)
            ),
        },
        {
            "table": "core",
            "rows": int(len(core)),
            "columns": int(len(core.columns)) if not core.empty else 0,
            "wells": int(core["well_alias"].nunique()) if "well_alias" in core and not core.empty else 0,
            "target_like_columns": "hydrate_saturation_vv" if "hydrate_saturation_vv" in core.columns else "",
        },
    ]
    return pd.DataFrame(rows)


def run_four_well_runtime_pipeline(
    *,
    project_root: Path,
    data_dir: Path,
    logs_file: str = DEFAULT_LOG_FILE,
    core_file: str | None = DEFAULT_CORE_FILE,
    split_file: str | None = DEFAULT_SPLIT_FILE,
    requested_target: str = "auto",
    requested_task: str = "auto",
    model_kind: str = "baseline",
    output_root: Path | None = None,
    model_root: Path | None = None,
    run_label: str | None = None,
    random_state: int = 42,
    max_core_offset_m: float = 3.0,
) -> dict[str, Any]:
    project_root = Path(project_root)
    data_dir = Path(data_dir).expanduser()
    output_root = Path(output_root) if output_root is not None else project_root / "outputs_runtime"
    model_root = Path(model_root) if model_root is not None else project_root / "models_runtime"

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    label = sanitize_label(run_label or f"four_well_runtime_{timestamp}")
    run_dir = output_root / label
    model_dir = model_root / label
    run_dir.mkdir(parents=True, exist_ok=True)
    model_dir.mkdir(parents=True, exist_ok=True)

    registry = load_four_well_location_index(project_root)
    stability = load_four_well_stability_context(project_root)
    evidence = load_four_well_core_evidence_registry(project_root)
    split_registry = load_split_registry(data_dir, split_file)
    logs = load_four_well_log_csv(data_dir, logs_file)
    logs = attach_four_well_identity(logs, registry)
    logs = attach_stability_context(logs, stability)
    logs = add_four_well_context_features(logs)
    logs = attach_split(logs, split_registry)

    core = load_four_well_core_csv(data_dir, core_file)
    if not core.empty:
        core = attach_four_well_identity(core, registry)
    core_matches = (
        match_core_intervals_to_nearest_logs(logs, core, max_offset_m=max_core_offset_m)
        if not core.empty and "depth_m" in logs.columns and "well_alias" in core.columns
        else pd.DataFrame()
    )

    target, target_candidates = choose_target(
        logs,
        requested_target=requested_target,
        requested_task=requested_task,
    )
    target_columns = {str(column) for column in target_candidates.get("column", pd.Series(dtype=str)).astype(str)}
    if target.column:
        target_columns.add(target.column)

    feature_matrix, feature_inventory = four_well_feature_matrix(logs, target_columns=target_columns)
    feature_columns = feature_matrix.columns.astype(str).tolist()
    status = "readiness_only"
    blocked_reason = ""
    written: dict[str, str] = {}

    outputs = {
        "dataset_inventory": run_dir / "dataset_inventory.csv",
        "four_well_enriched_log_rows": run_dir / "four_well_enriched_log_rows.csv",
        "four_well_core_log_matches": run_dir / "four_well_core_log_matches.csv",
        "four_well_core_evidence_registry": run_dir / "four_well_core_evidence_registry.csv",
        "target_detection": run_dir / "target_detection.csv",
        "feature_columns": run_dir / "feature_columns.csv",
        "split_registry_used": run_dir / "split_registry_used.csv",
    }
    dataset_inventory_frame(logs, core).to_csv(outputs["dataset_inventory"], index=False)
    logs.to_csv(outputs["four_well_enriched_log_rows"], index=False)
    core_matches.to_csv(outputs["four_well_core_log_matches"], index=False)
    evidence.to_csv(outputs["four_well_core_evidence_registry"], index=False)
    target_candidates.to_csv(outputs["target_detection"], index=False)
    feature_inventory.to_csv(outputs["feature_columns"], index=False)
    split_registry.to_csv(outputs["split_registry_used"], index=False)
    written.update({key: str(path) for key, path in outputs.items()})

    train_metrics_rows: list[dict[str, Any]] = []
    eval_metrics_rows: list[dict[str, Any]] = []
    model_path: Path | None = None

    train_frame = logs[logs["split"].eq("train")].copy() if "split" in logs else pd.DataFrame()
    if not target.is_available:
        blocked_reason = target.reason
    elif not feature_columns:
        blocked_reason = "no numeric non-target feature columns detected after four-well guardrails"
    elif train_frame.empty:
        blocked_reason = "no rows assigned to split=train in the split registry"
    else:
        X_train, y_train, train_rows = prepare_four_well_supervised_table(
            train_frame,
            target=target,
            feature_columns=feature_columns,
            target_columns=target_columns,
        )
        if len(X_train) < 3:
            blocked_reason = "fewer than three target-bearing training rows after preprocessing"
        elif target.task == "classification" and y_train.nunique() < 2:
            blocked_reason = "classification target has fewer than two classes in training rows"
        else:
            model = build_model_pipeline(target.task, model_kind, random_state)
            model.fit(X_train, y_train)
            train_pred = model.predict(X_train)
            train_metrics = evaluate_predictions(y_train, train_pred, task=target.task)
            train_metrics.update(
                {
                    "split": "train",
                    "task": target.task,
                    "target_column": target.column,
                    "model_kind": model_kind,
                    "feature_count": len(feature_columns),
                    "well_cases": ";".join(sorted(train_rows["well_case"].astype(str).unique())),
                }
            )
            train_metrics_rows.append(train_metrics)
            train_predictions_path = run_dir / "predictions_train.csv"
            four_well_prediction_frame(
                train_rows,
                y_true=y_train,
                y_pred=train_pred,
                task=target.task,
                model=model,
                X=X_train,
                target_column=target.column or "",
            ).to_csv(train_predictions_path, index=False)
            written["predictions_train"] = str(train_predictions_path)

            for split_name, split_frame in logs.groupby("split", dropna=False):
                split_name = str(split_name)
                if split_name == "train" or split_frame.empty:
                    continue
                X_eval, y_eval, eval_rows = prepare_four_well_supervised_table(
                    split_frame,
                    target=target,
                    feature_columns=feature_columns,
                    target_columns=target_columns,
                )
                if X_eval.empty:
                    X_pred, pred_rows = prepare_four_well_feature_only_table(
                        split_frame,
                        feature_columns=feature_columns,
                        target_columns=target_columns,
                    )
                    if X_pred.empty:
                        eval_metrics_rows.append(
                            {
                                "split": split_name,
                                "task": target.task,
                                "target_column": target.column,
                                "model_kind": model_kind,
                                "feature_count": len(feature_columns),
                                "rows_scored": 0,
                                "status": "blocked",
                                "blocked_reason": "no feature rows available",
                            }
                        )
                        continue
                    pred = model.predict(X_pred)
                    prediction_path = run_dir / f"predictions_{sanitize_label(split_name)}.csv"
                    four_well_prediction_frame(
                        pred_rows,
                        y_true=None,
                        y_pred=pred,
                        task=target.task,
                        model=model,
                        X=X_pred,
                        target_column=target.column or "",
                    ).to_csv(prediction_path, index=False)
                    written[f"predictions_{split_name}"] = str(prediction_path)
                    eval_metrics_rows.append(
                        {
                            "split": split_name,
                            "task": target.task,
                            "target_column": target.column,
                            "model_kind": model_kind,
                            "feature_count": len(feature_columns),
                            "rows_scored": int(len(X_pred)),
                            "status": "predicted_unlabeled",
                            "blocked_reason": "target column is absent or empty for this split",
                        }
                    )
                    continue
                pred = model.predict(X_eval)
                metrics = evaluate_predictions(y_eval, pred, task=target.task)
                metrics.update(
                    {
                        "split": split_name,
                        "task": target.task,
                        "target_column": target.column,
                        "model_kind": model_kind,
                        "feature_count": len(feature_columns),
                        "status": "scored",
                        "blocked_reason": "",
                        "well_cases": ";".join(sorted(eval_rows["well_case"].astype(str).unique())),
                    }
                )
                eval_metrics_rows.append(metrics)
                prediction_path = run_dir / f"predictions_{sanitize_label(split_name)}.csv"
                four_well_prediction_frame(
                    eval_rows,
                    y_true=y_eval,
                    y_pred=pred,
                    task=target.task,
                    model=model,
                    X=X_eval,
                    target_column=target.column or "",
                ).to_csv(prediction_path, index=False)
                written[f"predictions_{split_name}"] = str(prediction_path)

            from joblib import dump

            model_path = model_dir / "model.joblib"
            dump(
                {
                    "model": model,
                    "feature_columns": feature_columns,
                    "target": asdict(target),
                    "model_kind": model_kind,
                    "four_well_guardrail": "stability context is feature/caveat only; core rows are overlays unless target policy is approved.",
                },
                model_path,
            )
            written["model"] = str(model_path)
            status = "trained"

    train_metrics_path = run_dir / "train_metrics.csv"
    eval_metrics_path = run_dir / "eval_metrics.csv"
    pd.DataFrame(train_metrics_rows).to_csv(train_metrics_path, index=False)
    pd.DataFrame(eval_metrics_rows).to_csv(eval_metrics_path, index=False)
    written["train_metrics"] = str(train_metrics_path)
    written["eval_metrics"] = str(eval_metrics_path)

    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": status,
        "blocked_reason": blocked_reason,
        "data_dir": str(data_dir),
        "logs_file": logs_file,
        "core_file": core_file,
        "split_file": split_file,
        "target": asdict(target),
        "model_kind": model_kind,
        "feature_count": len(feature_columns),
        "feature_columns": feature_columns,
        "guardrail": (
            "Four-well runtime outputs may contain approved/local rows. Keep outputs_runtime, models_runtime, "
            "approved_runtime, and doe_runtime out of Git unless a release review explicitly clears summaries."
        ),
        "outputs": written,
    }
    manifest_path = run_dir / "run_manifest.json"
    write_json(manifest_path, manifest)
    written["run_manifest"] = str(manifest_path)

    return {
        "status": status,
        "blocked_reason": blocked_reason,
        "run_dir": str(run_dir),
        "model_dir": str(model_dir),
        "model_path": str(model_path) if model_path else None,
        "target": asdict(target),
        "feature_count": len(feature_columns),
        "outputs": written,
    }
