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
