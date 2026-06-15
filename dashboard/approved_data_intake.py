from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


PUBLIC_ML_PRODUCTS_DIR_NAME = "public_ml_products"
APPROVED_DATA_FIELD_ROLE_TABLE_FILE_NAME = "approved_data_field_role_table_2026-06-15.csv"
APPROVED_DATA_INTAKE_TEMPLATE_FILE_NAME = "approved_data_intake_template_2026-06-15.csv"
APPROVED_DATA_INTAKE_VALIDATION_SCHEMA_FILE_NAME = (
    "approved_data_intake_validation_schema_2026-06-15.csv"
)
FIRST_MODEL_OUTPUT_SCHEMA_FILE_NAME = "first_model_output_schema_2026-06-15.csv"
APPROVED_DATA_SOURCE_COLUMN_REGISTRY_TEMPLATE_FILE_NAME = (
    "approved_data_source_column_registry_template_2026-06-15.csv"
)
APPROVED_DATA_WELL_DEPTH_INDEX_TEMPLATE_FILE_NAME = (
    "approved_data_well_depth_index_template_2026-06-15.csv"
)
APPROVED_DATA_X_ALLOWED_CANDIDATE_TEMPLATE_FILE_NAME = (
    "approved_data_x_allowed_candidate_template_2026-06-15.csv"
)
APPROVED_DATA_Y_TARGET_REGISTRY_TEMPLATE_FILE_NAME = (
    "approved_data_y_target_registry_template_2026-06-15.csv"
)
FIRST_MODEL_OUTPUT_SCHEMA_TEMPLATE_FILE_NAME = "first_model_output_schema_template_2026-06-15.csv"
VARIABLE_FINGERPRINT_TEMPLATE_FILE_NAME = "variable_fingerprint_template_2026-06-15.csv"

EXPECTED_ROLES = {
    "predictor",
    "derived_feature",
    "QC",
    "context",
    "target_only",
    "calibration_reference",
    "unresolved",
}

FIELD_ROLE_COLUMNS = [
    "original_header",
    "normalized_name",
    "source_dataset",
    "role",
    "unit",
    "expected_dtype",
    "required_for_model",
    "public_safe_to_show",
    "caveats",
]

DEPTH_ALIASES = {
    "depth",
    "dept",
    "depth_ft",
    "true depth",
    "depth_m",
    "depth value",
}
LITHOLOGY_ALIASES = {"gr", "gamma ray", "rhob", "rho_b", "density_gpcc", "density"}
DENSITY_OR_POROSITY_ALIASES = {
    "rhob",
    "rho_b",
    "density_gpcc",
    "phi_porosity",
    "phi_den",
    "dphi",
    "nphi",
    "nmrphi",
    "phi_nmr",
    "density porosity",
}
HYDRATE_RESPONSE_ALIASES = {
    "rt",
    "res",
    "nmrphi",
    "phi_nmr",
    "vp",
    "velp",
    "vs",
    "vs1",
    "ratio vp/vs",
    "impedance",
}
SPLIT_ALIASES = {
    "split_group",
    "split registry",
    "whole_well_split",
    "validation_split",
    "train_validation_test_split",
}
OCCURRENCE_METADATA_ALIASES = {
    "occurrence_evidence_type",
    "source_evidence_type",
    "occurrence_interval_policy",
    "occurrence_confidence",
    "confidence",
    "interval_top_m",
    "interval_base_m",
    "depth_interval",
}
SATURATION_UNIT_ALIASES = {
    "saturation_unit_convention",
    "target_unit_convention",
    "unit_convention",
    "fraction_or_percent_policy",
}
STABILITY_CONTEXT_ALIASES = {
    "public stability context",
    "stability_context_features",
    "stability_result_status",
    "stability_confidence",
    "stability_caveat",
    "stability_caveats",
    "stability_blocked_reason",
    "blocked_reason",
    "stability_mask",
    "stability_admissibility_status",
}
CALIPER_ALIASES = {
    "caliper",
    "cal1",
    "differential caliper",
    "differential_caliper",
}
MISSING_LOG_ADAPTER_ALIASES = {
    "missing-log adapter flag",
    "missing_log_adapter_flag",
    "vp missing-log adapter",
    "vp_missing_log_adapter",
    "rhob missing-log adapter",
    "rhob_missing_log_adapter",
}
VP_ALIASES = {"vp", "velp", "compressional velocity", "compressional_velocity"}
RHOB_ALIASES = {"rhob", "rho_b", "density_gpcc", "bulk density", "bulk_density"}


def default_public_ml_products_dir(project_root: Path) -> Path:
    return project_root / "data" / PUBLIC_ML_PRODUCTS_DIR_NAME


def default_approved_data_field_role_table_path(project_root: Path) -> Path:
    return default_public_ml_products_dir(project_root) / APPROVED_DATA_FIELD_ROLE_TABLE_FILE_NAME


def default_approved_data_intake_template_path(project_root: Path) -> Path:
    return default_public_ml_products_dir(project_root) / APPROVED_DATA_INTAKE_TEMPLATE_FILE_NAME


def default_approved_data_intake_validation_schema_path(project_root: Path) -> Path:
    return default_public_ml_products_dir(project_root) / APPROVED_DATA_INTAKE_VALIDATION_SCHEMA_FILE_NAME


def default_first_model_output_schema_path(project_root: Path) -> Path:
    return default_public_ml_products_dir(project_root) / FIRST_MODEL_OUTPUT_SCHEMA_FILE_NAME


def default_approved_data_source_column_registry_template_path(project_root: Path) -> Path:
    return default_public_ml_products_dir(project_root) / APPROVED_DATA_SOURCE_COLUMN_REGISTRY_TEMPLATE_FILE_NAME


def default_approved_data_well_depth_index_template_path(project_root: Path) -> Path:
    return default_public_ml_products_dir(project_root) / APPROVED_DATA_WELL_DEPTH_INDEX_TEMPLATE_FILE_NAME


def default_approved_data_x_allowed_candidate_template_path(project_root: Path) -> Path:
    return default_public_ml_products_dir(project_root) / APPROVED_DATA_X_ALLOWED_CANDIDATE_TEMPLATE_FILE_NAME


def default_approved_data_y_target_registry_template_path(project_root: Path) -> Path:
    return default_public_ml_products_dir(project_root) / APPROVED_DATA_Y_TARGET_REGISTRY_TEMPLATE_FILE_NAME


def default_first_model_output_schema_template_path(project_root: Path) -> Path:
    return default_public_ml_products_dir(project_root) / FIRST_MODEL_OUTPUT_SCHEMA_TEMPLATE_FILE_NAME


def default_variable_fingerprint_template_path(project_root: Path) -> Path:
    return default_public_ml_products_dir(project_root) / VARIABLE_FINGERPRINT_TEMPLATE_FILE_NAME


def normalize_header(header: object) -> str:
    return " ".join(str(header).strip().lower().replace("_", " ").split())


def _compact_header(header: object) -> str:
    return normalize_header(header).replace(" ", "_")


def _headers_from_source(source: Iterable[str] | pd.DataFrame) -> list[str]:
    if isinstance(source, pd.DataFrame):
        return [str(column) for column in source.columns]
    return [str(column) for column in source]


def load_approved_data_field_role_table(project_root: Path) -> pd.DataFrame:
    path = default_approved_data_field_role_table_path(project_root)
    if not path.exists():
        return pd.DataFrame(columns=FIELD_ROLE_COLUMNS)
    table = pd.read_csv(path)
    for column in FIELD_ROLE_COLUMNS:
        if column not in table.columns:
            table[column] = ""
    return table[FIELD_ROLE_COLUMNS]


def load_field_role_table(project_root: Path) -> pd.DataFrame:
    """Compatibility wrapper for the V5.1 intake contract naming."""

    return load_approved_data_field_role_table(project_root)


def load_public_ml_template(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def _role_lookup(field_roles: pd.DataFrame) -> dict[str, pd.Series]:
    lookup: dict[str, pd.Series] = {}
    for _, row in field_roles.iterrows():
        original = row.get("original_header", "")
        normalized = row.get("normalized_name", "")
        for key in {normalize_header(original), normalize_header(normalized), _compact_header(normalized)}:
            if key:
                lookup[key] = row
    return lookup


def _field_rows_for_headers(headers: list[str], field_roles: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    lookup = _role_lookup(field_roles)
    rows = []
    unknown = []
    for header in headers:
        keys = [normalize_header(header), _compact_header(header)]
        row = next((lookup[key] for key in keys if key in lookup), None)
        if row is None:
            if normalize_header(header) in STABILITY_CONTEXT_ALIASES or _compact_header(header) in STABILITY_CONTEXT_ALIASES:
                rows.append(
                    {
                        "source_column": header,
                        "original_header": header,
                        "normalized_name": _compact_header(header),
                        "source_dataset": "Public context products",
                        "role": "context",
                        "unit": "public_product_units",
                        "expected_dtype": "mixed",
                        "required_for_model": "optional_context_after_mentor_approval",
                        "public_safe_to_show": "yes_public_summary_only",
                        "caveats": "Stability context or mask only; not proof or target evidence.",
                    }
                )
            else:
                unknown.append(header)
            continue
        row_dict = row.to_dict()
        row_dict["source_column"] = header
        rows.append(row_dict)
    if not rows:
        return pd.DataFrame(columns=["source_column", *FIELD_ROLE_COLUMNS]), unknown
    return pd.DataFrame(rows), unknown


def _has_any(headers: set[str], aliases: set[str]) -> bool:
    normalized_aliases = {normalize_header(alias) for alias in aliases} | {_compact_header(alias) for alias in aliases}
    return bool(headers & normalized_aliases)


def _target_rows(rows: pd.DataFrame) -> pd.DataFrame:
    if rows.empty or "role" not in rows.columns:
        return pd.DataFrame(columns=rows.columns)
    return rows[rows["role"].isin(["target_only", "calibration_reference"])].copy()


def _occurrence_rows(rows: pd.DataFrame) -> pd.DataFrame:
    if rows.empty:
        return pd.DataFrame(columns=rows.columns)
    names = rows["normalized_name"].fillna("").astype(str).str.lower()
    headers = rows["original_header"].fillna("").astype(str).str.lower()
    return rows[names.str.contains("occurrence|phase_class") | headers.str.contains("phase label")].copy()


def _saturation_rows(rows: pd.DataFrame) -> pd.DataFrame:
    if rows.empty:
        return pd.DataFrame(columns=rows.columns)
    names = rows["normalized_name"].fillna("").astype(str).str.lower()
    headers = rows["original_header"].fillna("").astype(str).str.lower()
    return rows[
        names.str.contains("saturation")
        | headers.str.contains("sgh|s_h|^sh$|nmr_sat|hydrate saturation|swr|s_wr", regex=True)
    ].copy()


def _role_headers(rows: pd.DataFrame, role: str) -> list[str]:
    if rows.empty or "role" not in rows.columns:
        return []
    return rows.loc[rows["role"].eq(role), "source_column"].tolist()


def _metadata_has(metadata: dict[str, object] | None, required_keys: Iterable[str]) -> bool:
    if not metadata:
        return False
    normalized = {_compact_header(key): value for key, value in metadata.items()}
    return all(bool(normalized.get(_compact_header(key))) for key in required_keys)


def build_variable_fingerprints(field_role_table: pd.DataFrame) -> pd.DataFrame:
    """Build public-safe per-header fingerprints from the field-role table."""

    if field_role_table.empty:
        return pd.DataFrame(
            columns=[
                "original_header",
                "unit",
                "normalized",
                "normalized_name",
                "role",
                "allowed_in_feature_matrix",
                "leakage_risk",
                "unresolved_mentor_question",
                "source_dataset",
                "caveats",
            ]
        )

    rows = []
    for _, row in field_role_table.iterrows():
        role = str(row.get("role", "")).strip()
        original_header = str(row.get("original_header", "")).strip()
        normalized_name = str(row.get("normalized_name", "")).strip()
        unit = str(row.get("unit", "")).strip()
        required_for_model = str(row.get("required_for_model", "")).strip()
        caveats = str(row.get("caveats", "")).strip()
        original_key = normalize_header(original_header)

        target_like = role in {"target_only", "calibration_reference"}
        unresolved_like = role == "unresolved" or "blocked_until" in required_for_model
        depth_like = original_key in {normalize_header(alias) for alias in DEPTH_ALIASES}
        stability_like = original_key in {normalize_header(alias) for alias in STABILITY_CONTEXT_ALIASES}

        allowed_in_feature_matrix = role in {"predictor", "derived_feature", "QC", "context"}
        if target_like or unresolved_like:
            allowed_in_feature_matrix = False

        leakage_risk = "high" if target_like else "medium" if unresolved_like else "low"
        if stability_like:
            leakage_risk = "low_when_context_only"
        if depth_like:
            leakage_risk = "mentor_review_if_used_as_predictor"

        mentor_question = ""
        caveat_text = f"{required_for_model} {caveats}".lower()
        if unresolved_like:
            mentor_question = "Resolve header meaning or processing stage before model use."
        elif target_like:
            mentor_question = "Confirm target authority, unit convention, and validation use."
        elif depth_like:
            mentor_question = "Confirm whether depth is alignment/context only or allowed as a predictor."
        elif "caliper" in original_key:
            mentor_question = "Confirm caliper coverage before washout filtering."

        rows.append(
            {
                "original_header": original_header,
                "unit": unit,
                "normalized": bool(normalized_name),
                "normalized_name": normalized_name,
                "role": role,
                "allowed_in_feature_matrix": allowed_in_feature_matrix,
                "leakage_risk": leakage_risk,
                "unresolved_mentor_question": mentor_question,
                "source_dataset": row.get("source_dataset", ""),
                "caveats": caveats,
            }
        )

    return pd.DataFrame(rows)


def classify_source_headers(headers: Iterable[str] | pd.DataFrame, field_role_table: pd.DataFrame) -> dict[str, object]:
    source_headers = _headers_from_source(headers)
    rows, unknown_headers = _field_rows_for_headers(source_headers, field_role_table)
    unresolved_rows = rows[rows["role"].eq("unresolved")].copy() if not rows.empty else rows
    calibration_rows = rows[rows["role"].eq("calibration_reference")].copy() if not rows.empty else rows

    return {
        "recognized_headers": rows,
        "unknown_headers": unknown_headers,
        "predictor_headers": _role_headers(rows, "predictor"),
        "derived_feature_headers": _role_headers(rows, "derived_feature"),
        "qc_headers": _role_headers(rows, "QC"),
        "context_headers": _role_headers(rows, "context"),
        "target_only_headers": _role_headers(rows, "target_only"),
        "calibration_reference_headers": calibration_rows["source_column"].tolist() if not calibration_rows.empty else [],
        "unresolved_headers": unresolved_rows["source_column"].tolist() if not unresolved_rows.empty else [],
    }


def validate_x_allowed(headers: Iterable[str] | pd.DataFrame, field_role_table: pd.DataFrame) -> dict[str, object]:
    classification = classify_source_headers(headers, field_role_table)
    rows: pd.DataFrame = classification["recognized_headers"]
    blocked_rows = (
        rows[rows["role"].isin(["target_only", "calibration_reference", "unresolved"])].copy()
        if not rows.empty
        else rows
    )
    leakage_rows = (
        rows[rows["role"].isin(["target_only", "calibration_reference"])].copy()
        if not rows.empty
        else rows
    )
    stability_target_misuse = [
        header
        for header in classification["target_only_headers"]
        if normalize_header(header) in {normalize_header(alias) for alias in STABILITY_CONTEXT_ALIASES}
    ]
    leakage_flags = []
    leakage_flags.extend(f"target_only_in_x_allowed:{header}" for header in leakage_rows["source_column"].tolist())
    leakage_flags.extend(f"stability_target_misuse:{header}" for header in stability_target_misuse)
    leakage_flags.extend(f"unknown_x_allowed_header:{header}" for header in classification["unknown_headers"])
    leakage_flags.extend(
        f"unresolved_x_allowed_header:{header}" for header in classification["unresolved_headers"]
    )

    allowed_rows = (
        rows[rows["role"].isin(["predictor", "derived_feature", "QC", "context"])].copy()
        if not rows.empty
        else rows
    )
    return {
        "valid": not leakage_flags,
        "allowed_headers": allowed_rows["source_column"].tolist() if not allowed_rows.empty else [],
        "blocked_headers": blocked_rows["source_column"].tolist() if not blocked_rows.empty else [],
        "unknown_headers": classification["unknown_headers"],
        "leakage_flags": leakage_flags,
    }


def validate_target_only_separation(headers: Iterable[str] | pd.DataFrame, field_role_table: pd.DataFrame) -> dict[str, object]:
    x_report = validate_x_allowed(headers, field_role_table)
    target_like = [
        flag.split(":", 1)[1]
        for flag in x_report["leakage_flags"]
        if flag.startswith("target_only_in_x_allowed:")
    ]
    return {
        "valid": not target_like,
        "target_only_fields_in_x_allowed": target_like,
        "leakage_flags": x_report["leakage_flags"],
    }


def validate_minimum_predictor_coverage(headers: Iterable[str] | pd.DataFrame, field_role_table: pd.DataFrame) -> dict[str, object]:
    source_headers = _headers_from_source(headers)
    recognized, _unknown_headers = _field_rows_for_headers(source_headers, field_role_table)
    header_keys = {normalize_header(column) for column in source_headers} | {
        _compact_header(column) for column in source_headers
    }
    has_depth = _has_any(header_keys, DEPTH_ALIASES)
    has_lithology = _has_any(header_keys, LITHOLOGY_ALIASES)
    has_density_or_porosity = _has_any(header_keys, DENSITY_OR_POROSITY_ALIASES)
    has_hydrate_response = _has_any(header_keys, HYDRATE_RESPONSE_ALIASES)
    ready = has_depth and (has_lithology or has_density_or_porosity) and has_hydrate_response
    missing_required_fields = []
    if not has_depth:
        missing_required_fields.append("depth_basis")
    if not (has_lithology or has_density_or_porosity):
        missing_required_fields.append("lithology_or_reservoir_curve")
    if not has_hydrate_response:
        missing_required_fields.append("hydrate_response_curve_family")

    return {
        "has_depth": has_depth,
        "has_lithology_or_reservoir_curve": has_lithology or has_density_or_porosity,
        "has_density_or_porosity_basis": has_density_or_porosity,
        "has_hydrate_response_curve_family": has_hydrate_response,
        "predictor_like_headers": int(recognized["role"].isin(["predictor", "derived_feature"]).sum())
        if not recognized.empty
        else 0,
        "missing_required_fields": missing_required_fields,
        "ready": ready,
    }


def validate_occurrence_target_authority(
    headers: Iterable[str] | pd.DataFrame,
    field_role_table: pd.DataFrame | dict[str, object] | None = None,
    metadata: dict[str, object] | None = None,
    project_root: Path | None = None,
) -> dict[str, object]:
    if isinstance(field_role_table, dict) and metadata is None:
        metadata = field_role_table
        field_role_table = None
    if field_role_table is None:
        if project_root is None:
            project_root = Path(__file__).resolve().parents[1]
        field_role_table = load_field_role_table(project_root)
    rows, _unknown_headers = _field_rows_for_headers(_headers_from_source(headers), field_role_table)
    occurrence_fields = _occurrence_rows(rows)["source_column"].tolist()
    required_metadata = [
        "occurrence_evidence_source",
        "occurrence_confidence",
        "occurrence_interval_policy",
    ]
    metadata_ready = _metadata_has(metadata, required_metadata)
    return {
        "target_fields": occurrence_fields,
        "authority_present": bool(occurrence_fields) and metadata_ready,
        "required_metadata": required_metadata,
        "missing_metadata": []
        if metadata_ready
        else [key for key in required_metadata if not _metadata_has(metadata, [key])],
        "blocked_reason": ""
        if bool(occurrence_fields) and metadata_ready
        else "occurrence_target_requires_source_confidence_interval_policy",
    }


def validate_saturation_target_authority(
    headers: Iterable[str] | pd.DataFrame,
    field_role_table: pd.DataFrame | dict[str, object] | None = None,
    metadata: dict[str, object] | None = None,
    project_root: Path | None = None,
) -> dict[str, object]:
    if isinstance(field_role_table, dict) and metadata is None:
        metadata = field_role_table
        field_role_table = None
    if field_role_table is None:
        if project_root is None:
            project_root = Path(__file__).resolve().parents[1]
        field_role_table = load_field_role_table(project_root)
    rows, _unknown_headers = _field_rows_for_headers(_headers_from_source(headers), field_role_table)
    saturation_fields = _saturation_rows(rows)["source_column"].tolist()
    authoritative_field = str((metadata or {}).get("authoritative_saturation_field", "")).strip()
    unit_convention = str((metadata or {}).get("saturation_unit_convention", "")).strip().lower()
    authority_ready = authoritative_field in saturation_fields and unit_convention in {"fraction", "percent"}
    return {
        "target_fields": saturation_fields,
        "authority_present": bool(saturation_fields) and authority_ready,
        "authoritative_field": authoritative_field,
        "unit_convention": unit_convention,
        "blocked_reason": ""
        if bool(saturation_fields) and authority_ready
        else "saturation_target_requires_authoritative_field_and_fraction_or_percent_policy",
    }


def validate_caliper_gate(headers: Iterable[str] | pd.DataFrame) -> dict[str, object]:
    header_keys = {normalize_header(column) for column in _headers_from_source(headers)} | {
        _compact_header(column) for column in _headers_from_source(headers)
    }
    has_caliper = _has_any(header_keys, CALIPER_ALIASES)
    return {
        "has_caliper_coverage": has_caliper,
        "washout_qc_filter_allowed": has_caliper,
        "missing_qc_flag_required": not has_caliper,
        "status": "caliper_coverage_available_for_washout_qc"
        if has_caliper
        else "caliper_missing_create_missing_qc_flag_not_filter",
    }


def validate_missing_log_strategy(
    headers: Iterable[str] | pd.DataFrame,
    allow_missing_log_adapters: bool = False,
) -> dict[str, object]:
    header_keys = {normalize_header(column) for column in _headers_from_source(headers)} | {
        _compact_header(column) for column in _headers_from_source(headers)
    }
    has_vp = _has_any(header_keys, VP_ALIASES)
    has_rhob = _has_any(header_keys, RHOB_ALIASES)
    missing_optimal_logs = []
    if not has_vp:
        missing_optimal_logs.append("Vp")
    if not has_rhob:
        missing_optimal_logs.append("RHOB")
    blocked_reasons = []
    if missing_optimal_logs and not allow_missing_log_adapters:
        blocked_reasons.append("missing_log_adapter_blocked_until_mentor_approval")
    return {
        "missing_optimal_logs": missing_optimal_logs,
        "alternate_log_combinations_required": bool(missing_optimal_logs),
        "missing_log_adapter_allowed": bool(missing_optimal_logs) and allow_missing_log_adapters,
        "validation_required": bool(missing_optimal_logs) and allow_missing_log_adapters,
        "blocked_reasons": blocked_reasons,
    }


def build_intake_readiness_report(
    headers: Iterable[str] | pd.DataFrame,
    field_role_table: pd.DataFrame,
    options: dict[str, object] | None = None,
) -> dict[str, object]:
    options = options or {}
    metadata = options.get("metadata")
    source_headers = _headers_from_source(headers)
    classification = classify_source_headers(source_headers, field_role_table)
    x_allowed_headers = options.get("x_allowed_headers")
    if x_allowed_headers is None:
        x_allowed_headers = (
            classification["predictor_headers"]
            + classification["derived_feature_headers"]
            + classification["qc_headers"]
            + classification["context_headers"]
        )
    x_report = validate_x_allowed(x_allowed_headers, field_role_table)
    target_report = validate_target_only_separation(x_allowed_headers, field_role_table)
    coverage = validate_minimum_predictor_coverage(source_headers, field_role_table)
    occurrence = validate_occurrence_target_authority(source_headers, field_role_table, metadata=metadata)
    saturation = validate_saturation_target_authority(source_headers, field_role_table, metadata=metadata)
    caliper = validate_caliper_gate(source_headers)
    missing_logs = validate_missing_log_strategy(
        source_headers,
        allow_missing_log_adapters=bool(options.get("allow_missing_log_adapters", False)),
    )

    approved_rows_available = bool(options.get("approved_rows_available", False))
    split_policy_confirmed = bool(options.get("split_policy_confirmed", False))
    validation_plan_confirmed = bool(options.get("validation_plan_confirmed", False))
    public_release_review_complete = bool(options.get("public_release_review_complete", False))

    missing_required_fields = list(coverage["missing_required_fields"])
    blocked_reasons = []
    blocked_reasons.extend(f"missing_required_field:{field}" for field in missing_required_fields)
    blocked_reasons.extend(f"unknown_header:{header}" for header in classification["unknown_headers"])
    blocked_reasons.extend(f"unresolved_header:{header}" for header in classification["unresolved_headers"])
    blocked_reasons.extend(x_report["leakage_flags"])
    if classification["target_only_headers"] and not occurrence["authority_present"] and not saturation["authority_present"]:
        blocked_reasons.append("target_authority_not_confirmed")
    if occurrence["target_fields"] and not occurrence["authority_present"]:
        blocked_reasons.append(occurrence["blocked_reason"])
    if saturation["target_fields"] and not saturation["authority_present"]:
        blocked_reasons.append(saturation["blocked_reason"])
    if not approved_rows_available:
        blocked_reasons.append("approved_rows_not_loaded_public_safe_validator")
    if not split_policy_confirmed:
        blocked_reasons.append("whole_well_compartment_or_geographic_split_policy_required")
    if not validation_plan_confirmed:
        blocked_reasons.append("validation_plan_required_before_training")
    blocked_reasons.extend(missing_logs["blocked_reasons"])

    mentor_questions = [
        "Which saturation field is authoritative: Sgh, S_h, Sh, or NMR_SAT?",
        "Should occurrence use source-style classes, saturation thresholds, or mentor-reviewed intervals?",
        "Are MTE/IGS separate wells and are *_refined processing stages in the workbook?",
        "Do we have enough caliper coverage to apply washout filtering?",
        "Which wells become blind validation after full recovery?",
        "Are missing-log adapters allowed, or should missing curves simply block that feature set?",
    ]
    if caliper["missing_qc_flag_required"]:
        mentor_questions.append("Caliper is absent in this header set; should the runtime carry a missing-QC flag?")

    ready_for_schema_design = bool(len(classification["recognized_headers"]))
    ready_for_training = (
        ready_for_schema_design
        and bool(coverage["ready"])
        and approved_rows_available
        and split_policy_confirmed
        and validation_plan_confirmed
        and not x_report["leakage_flags"]
        and not classification["unresolved_headers"]
        and (occurrence["authority_present"] or saturation["authority_present"])
        and not missing_logs["blocked_reasons"]
    )
    ready_for_public_release = ready_for_training and public_release_review_complete

    return {
        "recognized_headers": classification["recognized_headers"],
        "unknown_headers": classification["unknown_headers"],
        "predictor_headers": classification["predictor_headers"],
        "derived_feature_headers": classification["derived_feature_headers"],
        "qc_headers": classification["qc_headers"],
        "context_headers": classification["context_headers"],
        "target_only_headers": classification["target_only_headers"],
        "unresolved_headers": classification["unresolved_headers"],
        "leakage_flags": x_report["leakage_flags"],
        "missing_required_fields": missing_required_fields,
        "blocked_reasons": sorted(dict.fromkeys(blocked_reasons)),
        "mentor_questions": mentor_questions,
        "minimum_predictor_coverage": coverage,
        "occurrence_target_authority": occurrence,
        "saturation_target_authority": saturation,
        "caliper_gate": caliper,
        "missing_log_strategy": missing_logs,
        "ready_for_schema_design": ready_for_schema_design,
        "ready_for_training": ready_for_training,
        "ready_for_public_release": ready_for_public_release,
    }


def validate_approved_data_intake(
    source: Iterable[str] | pd.DataFrame,
    *,
    field_roles: pd.DataFrame | None = None,
    project_root: Path | None = None,
    x_allowed_columns: Iterable[str] | pd.DataFrame | None = None,
    approved_rows_available: bool = False,
    split_registry_present: bool = False,
    train_only_preprocessing_requested: bool = False,
    occurrence_policy_present: bool = False,
    saturation_unit_convention: str | None = None,
) -> dict[str, object]:
    """Validate headers for a future approved-data intake without reading private rows."""

    if field_roles is None:
        if project_root is None:
            project_root = Path(__file__).resolve().parents[1]
        field_roles = load_approved_data_field_role_table(project_root)

    source_columns = _headers_from_source(source)
    normalized_headers = {normalize_header(column) for column in source_columns}
    compact_headers = {_compact_header(column) for column in source_columns}
    all_header_keys = normalized_headers | compact_headers

    recognized, unknown_headers = _field_rows_for_headers(source_columns, field_roles)

    if x_allowed_columns is None:
        x_allowed_list: list[str] = []
    else:
        x_allowed_list = _headers_from_source(x_allowed_columns)
    x_allowed_rows, x_allowed_unknown = _field_rows_for_headers(x_allowed_list, field_roles)
    x_target_rows = _target_rows(x_allowed_rows)

    target_rows = _target_rows(recognized)
    occurrence_rows = _occurrence_rows(recognized)
    saturation_rows = _saturation_rows(recognized)
    unresolved_rows = recognized[recognized["role"].eq("unresolved")].copy() if not recognized.empty else recognized
    context_rows = recognized[recognized["role"].eq("context")].copy() if not recognized.empty else recognized

    has_depth = _has_any(all_header_keys, DEPTH_ALIASES)
    has_lithology = _has_any(all_header_keys, LITHOLOGY_ALIASES)
    has_density_or_porosity = _has_any(all_header_keys, DENSITY_OR_POROSITY_ALIASES)
    has_hydrate_response = _has_any(all_header_keys, HYDRATE_RESPONSE_ALIASES)
    has_split = split_registry_present or _has_any(all_header_keys, SPLIT_ALIASES)
    has_occurrence_metadata = occurrence_policy_present or len(all_header_keys & {normalize_header(a) for a in OCCURRENCE_METADATA_ALIASES}) >= 3
    has_saturation_unit = bool(saturation_unit_convention) or _has_any(all_header_keys, SATURATION_UNIT_ALIASES)

    minimum_viable_predictor_coverage = {
        "has_depth": has_depth,
        "has_lithology_or_reservoir_curve": has_lithology or has_density_or_porosity,
        "has_density_or_porosity_basis": has_density_or_porosity,
        "has_hydrate_response_curve_family": has_hydrate_response,
        "predictor_like_headers": int(recognized["role"].isin(["predictor", "derived_feature"]).sum())
        if not recognized.empty
        else 0,
        "ready": has_depth and (has_lithology or has_density_or_porosity) and has_hydrate_response,
    }

    missing_required_fields: list[str] = []
    if not has_depth:
        missing_required_fields.append("depth_basis")
    if not (has_lithology or has_density_or_porosity):
        missing_required_fields.append("lithology_or_reservoir_curve")
    if not has_hydrate_response:
        missing_required_fields.append("hydrate_response_curve_family")

    target_leakage_fields = x_target_rows["source_column"].tolist() if not x_target_rows.empty else []
    unresolved_header_fields = unresolved_rows["source_column"].tolist() if not unresolved_rows.empty else []
    unresolved_unit_fields = (
        recognized[
            recognized["unit"].fillna("").str.contains("or|unresolved|unit_aware", case=False, regex=True)
        ]["source_column"].tolist()
        if not recognized.empty
        else []
    )
    target_only_fields_detected = target_rows["source_column"].tolist() if not target_rows.empty else []
    occurrence_target_fields = occurrence_rows["source_column"].tolist() if not occurrence_rows.empty else []
    saturation_target_fields = saturation_rows["source_column"].tolist() if not saturation_rows.empty else []
    stability_context_fields = context_rows["source_column"].tolist() if not context_rows.empty else []

    occurrence_target_authority_present = bool(occurrence_target_fields) and has_occurrence_metadata
    saturation_target_authority_present = bool(saturation_target_fields) and has_saturation_unit
    train_only_preprocessing_ready = not train_only_preprocessing_requested or has_split

    blocked_reasons: list[str] = []
    blocked_reasons.extend(f"missing_required_field:{field}" for field in missing_required_fields)
    blocked_reasons.extend(f"unknown_header:{header}" for header in unknown_headers)
    blocked_reasons.extend(f"unresolved_header:{header}" for header in unresolved_header_fields)
    if target_leakage_fields:
        blocked_reasons.append("target_leakage_risk_in_x_allowed")
    if occurrence_target_fields and not has_occurrence_metadata:
        blocked_reasons.append("occurrence_target_requires_source_confidence_interval_policy")
    if saturation_target_fields and not has_saturation_unit:
        blocked_reasons.append("saturation_target_requires_fraction_or_percent_unit_policy")
    if train_only_preprocessing_requested and not has_split:
        blocked_reasons.append("whole_well_split_required_before_train_only_preprocessing")
    if not approved_rows_available:
        blocked_reasons.append("approved_rows_not_loaded_public_safe_validator")
    if not (occurrence_target_authority_present or saturation_target_authority_present):
        blocked_reasons.append("no_approved_target_authority_for_training")

    training_ready = (
        minimum_viable_predictor_coverage["ready"]
        and approved_rows_available
        and has_split
        and not target_leakage_fields
        and not unresolved_header_fields
        and (occurrence_target_authority_present or saturation_target_authority_present)
    )

    return {
        "source_columns": source_columns,
        "recognized_headers": recognized,
        "unknown_headers": unknown_headers,
        "missing_required_fields": missing_required_fields,
        "target_only_fields_detected": target_only_fields_detected,
        "target_leakage_risk": bool(target_leakage_fields),
        "target_leakage_fields": target_leakage_fields,
        "unresolved_header_fields": unresolved_header_fields,
        "unresolved_unit_fields": unresolved_unit_fields,
        "stability_context_fields": stability_context_fields,
        "minimum_viable_predictor_coverage": minimum_viable_predictor_coverage,
        "occurrence_target_authority_present": occurrence_target_authority_present,
        "occurrence_target_fields": occurrence_target_fields,
        "saturation_target_authority_present": saturation_target_authority_present,
        "saturation_target_fields": saturation_target_fields,
        "saturation_target_unit_convention_present": has_saturation_unit,
        "split_registry_present": has_split,
        "train_only_preprocessing_ready": train_only_preprocessing_ready,
        "training_ready": training_ready,
        "blocked_reasons": sorted(dict.fromkeys(blocked_reasons)),
        "x_allowed_unknown_headers": x_allowed_unknown,
    }


def intake_validation_report_frame(report: dict[str, object]) -> pd.DataFrame:
    coverage = report.get("minimum_viable_predictor_coverage", {})
    rows = [
        ("recognized_headers", len(report.get("recognized_headers", [])), "Headers found in field-role table."),
        ("unknown_headers", len(report.get("unknown_headers", [])), "Headers not recognized by the public-safe mapping."),
        (
            "target_leakage_risk",
            bool(report.get("target_leakage_risk")),
            "True when Y-only fields appear in X_allowed.",
        ),
        (
            "minimum_predictor_coverage",
            bool(coverage.get("ready", False)),
            "Depth plus reservoir/lithology plus hydrate-response family.",
        ),
        (
            "occurrence_target_authority",
            bool(report.get("occurrence_target_authority_present")),
            "Requires occurrence label plus source/confidence/interval policy.",
        ),
        (
            "saturation_target_authority",
            bool(report.get("saturation_target_authority_present")),
            "Requires saturation target plus fraction/percent policy.",
        ),
        (
            "train_only_preprocessing_ready",
            bool(report.get("train_only_preprocessing_ready")),
            "Requires whole-well or approved group split before preprocessing.",
        ),
        ("training_ready", bool(report.get("training_ready")), "False for public header-only validation."),
        ("blocked_reasons", len(report.get("blocked_reasons", [])), "; ".join(report.get("blocked_reasons", []))),
    ]
    return pd.DataFrame(rows, columns=["check", "value", "meaning"])


def intake_validator_contract_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Contract area": "Required column families",
                "Requirement": "Depth basis, reservoir/lithology curve, hydrate-response family, QC/alignment, target registry, split group before preprocessing.",
                "Blocked if missing": "depth_basis; lithology_or_reservoir_curve; hydrate_response_curve_family; whole_well_split_required_before_train_only_preprocessing",
            },
            {
                "Contract area": "Target-only leakage rule",
                "Requirement": "Sgh, S_h, Sh, NMR_SAT, Hydrate Saturation, Swr, phase labels, and occurrence labels never enter X_allowed.",
                "Blocked if missing": "target_leakage_risk_in_x_allowed",
            },
            {
                "Contract area": "Occurrence authority",
                "Requirement": "Occurrence target needs source evidence, interval policy, confidence, and caveat metadata.",
                "Blocked if missing": "occurrence_target_requires_source_confidence_interval_policy",
            },
            {
                "Contract area": "Saturation authority",
                "Requirement": "Saturation targets need approved target source and fraction/percent unit convention.",
                "Blocked if missing": "saturation_target_requires_fraction_or_percent_unit_policy",
            },
            {
                "Contract area": "Stability context",
                "Requirement": "Stability may be context, mask, confidence, caveat, or blocked reason only.",
                "Blocked if missing": "stability_used_as_occurrence_or_saturation_target",
            },
        ]
    )
