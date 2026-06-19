from __future__ import annotations

from pathlib import Path

import pandas as pd


PUBLIC_PARAMETER_EVIDENCE_REGISTRY_FILE_NAME = (
    "public_parameter_evidence_registry_2026-06-16.csv"
)

PARAMETER_EVIDENCE_COLUMNS = [
    "evidence_order",
    "tier",
    "parameter_family",
    "canonical_fields",
    "display_unit",
    "low_axis_label",
    "high_axis_label",
    "hydrate_window_norm_start",
    "hydrate_window_norm_end",
    "hydrate_direction_label",
    "opposing_or_mimic_label",
    "working_screening_envelope",
    "comparison_envelopes",
    "physical_reason",
    "hydrate_support",
    "false_positives_or_masks",
    "ml_role",
    "source_basis",
    "source_status",
    "public_guardrail",
]

FEATURE_TIERS = {
    "Stability context",
    "Reservoir quality",
    "Hydrate response",
    "QC and review",
}

TARGET_TIER = "Targets and validation"


def default_public_ml_products_dir(project_root: Path) -> Path:
    return project_root / "data" / "public_ml_products"


def default_parameter_evidence_registry_path(project_root: Path) -> Path:
    return default_public_ml_products_dir(project_root) / PUBLIC_PARAMETER_EVIDENCE_REGISTRY_FILE_NAME


def load_parameter_evidence_registry(project_root: Path) -> pd.DataFrame:
    path = default_parameter_evidence_registry_path(project_root)
    if not path.exists():
        return pd.DataFrame(columns=PARAMETER_EVIDENCE_COLUMNS)

    registry = pd.read_csv(path)
    for column in PARAMETER_EVIDENCE_COLUMNS:
        if column not in registry.columns:
            registry[column] = ""

    registry = registry[PARAMETER_EVIDENCE_COLUMNS].copy()
    registry["evidence_order"] = pd.to_numeric(registry["evidence_order"], errors="coerce")
    for column in ["hydrate_window_norm_start", "hydrate_window_norm_end"]:
        registry[column] = pd.to_numeric(registry[column], errors="coerce")

    return registry.sort_values("evidence_order", kind="stable").reset_index(drop=True)


def validate_parameter_evidence_registry(registry: pd.DataFrame) -> dict[str, object]:
    missing_columns = [column for column in PARAMETER_EVIDENCE_COLUMNS if column not in registry.columns]
    if missing_columns:
        return {
            "valid": False,
            "missing_columns": missing_columns,
            "invalid_window_rows": [],
            "target_rows_with_window": [],
            "feature_rows_without_guardrail": [],
        }

    invalid_window_rows: list[str] = []
    target_rows_with_window: list[str] = []
    feature_rows_without_guardrail: list[str] = []

    for _, row in registry.iterrows():
        family = str(row["parameter_family"])
        start = row["hydrate_window_norm_start"]
        end = row["hydrate_window_norm_end"]
        tier = str(row["tier"])
        guardrail = str(row["public_guardrail"]).strip()

        if pd.isna(start) or pd.isna(end) or start < 0 or end > 1 or start > end:
            invalid_window_rows.append(family)

        if tier == TARGET_TIER and (start != 0 or end != 0):
            target_rows_with_window.append(family)

        if tier in FEATURE_TIERS and not guardrail:
            feature_rows_without_guardrail.append(family)

    return {
        "valid": not invalid_window_rows
        and not target_rows_with_window
        and not feature_rows_without_guardrail,
        "missing_columns": [],
        "invalid_window_rows": invalid_window_rows,
        "target_rows_with_window": target_rows_with_window,
        "feature_rows_without_guardrail": feature_rows_without_guardrail,
    }


def parameter_evidence_summary_frame(registry: pd.DataFrame) -> pd.DataFrame:
    if registry.empty:
        return pd.DataFrame(columns=["metric", "value", "meaning"])

    validation = validate_parameter_evidence_registry(registry)
    target_rows = registry["tier"].eq(TARGET_TIER)
    directional_rows = registry["source_status"].fillna("").str.contains(
        "directional", case=False, regex=False
    )
    working_range_rows = registry["source_status"].fillna("").str.contains(
        "working_screening_envelope", case=False, regex=False
    )

    rows = [
        {
            "metric": "Parameter evidence rows",
            "value": int(len(registry)),
            "meaning": "Public-safe parameter families available for slide, website, and method visuals.",
        },
        {
            "metric": "Feature/context/QC rows",
            "value": int((~target_rows).sum()),
            "meaning": "Rows that can describe input evidence or context after source, unit, QC, and leakage checks.",
        },
        {
            "metric": "Y-only target rows",
            "value": int(target_rows.sum()),
            "meaning": "Rows that belong to target/calibration/validation only and never enter X_allowed.",
        },
        {
            "metric": "Working screening-envelope rows",
            "value": int(working_range_rows.sum()),
            "meaning": "Rows with current numeric working envelopes from project synthesis, not final DOE cutoffs.",
        },
        {
            "metric": "Directional-only rows",
            "value": int(directional_rows.sum()),
            "meaning": "Rows where the current public source support is directional rather than a locked numeric threshold.",
        },
        {
            "metric": "Registry validation",
            "value": "pass" if validation["valid"] else "review",
            "meaning": "Checks normalized windows, target-only leakage, required columns, and guardrail text.",
        },
    ]
    return pd.DataFrame(rows)
