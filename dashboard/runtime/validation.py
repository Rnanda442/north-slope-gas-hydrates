from __future__ import annotations

import pandas as pd

from dashboard.runtime.schemas import (
    CHONG_ML_FEATURE_COLUMNS,
    OPTIONAL_LOG_COLUMNS,
    REQUIRED_LOG_COLUMNS,
    RuntimeReadinessReport,
    ValidationIssue,
)


RANGE_CHECKS = {
    "depth_m": (0, 10000),
    "gr_api": (0, 300),
    "rt_ohm_m": (0.01, 100000),
    "rhob_g_cc": (1.0, 3.2),
    "dt_us_ft": (30, 250),
    "dts_us_ft": (50, 500),
    "nmr_porosity_vv": (0, 0.7),
    "caliper_in": (4, 24),
    "temperature_c": (-30, 120),
    "pressure_mpa": (0, 150),
}


def validate_log_table(logs: pd.DataFrame) -> RuntimeReadinessReport:
    issues: list[ValidationIssue] = []
    for column in REQUIRED_LOG_COLUMNS:
        if column not in logs.columns:
            issues.append(ValidationIssue("error", column, "Missing required log column."))

    if logs.empty:
        issues.append(ValidationIssue("error", "table", "No log rows were loaded."))

    if "well_alias" in logs and logs["well_alias"].isna().any():
        issues.append(ValidationIssue("error", "well_alias", "Well aliases contain missing values."))

    if {"well_alias", "depth_m"}.issubset(logs.columns):
        for alias, well in logs.groupby("well_alias", dropna=False):
            if not well["depth_m"].is_monotonic_increasing:
                issues.append(
                    ValidationIssue(
                        "warning",
                        "depth_m",
                        f"Depth is not monotonic for well {alias}; sort or inspect duplicates.",
                    )
                )
            if well["depth_m"].duplicated().any():
                issues.append(ValidationIssue("warning", "depth_m", f"Duplicate depths found for well {alias}."))

    for column, (minimum, maximum) in RANGE_CHECKS.items():
        if column not in logs:
            continue
        numeric = pd.to_numeric(logs[column], errors="coerce")
        if numeric.notna().any() and (~numeric.dropna().between(minimum, maximum)).any():
            issues.append(
                ValidationIssue(
                    "warning",
                    column,
                    f"Values fall outside expected planning range {minimum} to {maximum}.",
                )
            )
        if numeric.isna().mean() > 0.25:
            issues.append(
                ValidationIssue(
                    "warning",
                    column,
                    f"Column is {numeric.isna().mean() * 100:.1f}% missing.",
                )
            )

    status = "blocked" if any(issue.severity == "error" for issue in issues) else "ready"
    wells = logs["well_alias"].nunique() if "well_alias" in logs else 0
    return RuntimeReadinessReport(status=status, rows=len(logs), wells=int(wells), issues=tuple(issues))


def readiness_frame(report: RuntimeReadinessReport) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Severity": issue.severity,
                "Column": issue.column,
                "Message": issue.message,
            }
            for issue in report.issues
        ]
    )


def curve_coverage_frame(logs: pd.DataFrame) -> pd.DataFrame:
    roles = {
        "well_alias": "Grouping and leakage prevention",
        "depth_m": "Depth alignment",
        "gr_api": "Lithology and reservoir screening",
        "rt_ohm_m": "Electrical hydrate evidence",
        "rhob_g_cc": "Density and porosity",
        "density_porosity_vv": "Reservoir capacity and NMR-density target",
        "neutron_porosity_vv": "Porosity and lithology cross-check",
        "dt_us_ft": "Compressional velocity",
        "dts_us_ft": "Shear velocity and gas/hydrate discrimination",
        "nmr_porosity_vv": "Preferred saturation target support",
        "caliper_in": "Washout and bad-hole QC",
        "temperature_c": "Stability context",
        "pressure_mpa": "Stability and effective-stress context",
    }
    rows = []
    for column in REQUIRED_LOG_COLUMNS + OPTIONAL_LOG_COLUMNS:
        present = column in logs.columns
        coverage = float(logs[column].notna().mean() * 100) if present and len(logs) else 0.0
        rows.append(
            {
                "Canonical column": column,
                "Requirement": "Required" if column in REQUIRED_LOG_COLUMNS else "Optional / routed",
                "Present": "Yes" if present else "No",
                "Coverage %": round(coverage, 1),
                "Decision role": roles.get(column, "Supporting evidence"),
            }
        )
    return pd.DataFrame(rows)


def output_readiness_frame(features: pd.DataFrame) -> pd.DataFrame:
    available = set(features.columns)

    def status(required: tuple[str, ...], preferred: tuple[str, ...] = ()) -> tuple[str, str]:
        missing_required = [
            column
            for column in required
            if column not in available or not features[column].notna().any()
        ]
        missing_preferred = [
            column
            for column in preferred
            if column not in available or not features[column].notna().any()
        ]
        if missing_required:
            return "Blocked", ", ".join(missing_required)
        partial_required = [
            f"{column} ({features[column].isna().mean() * 100:.1f}% missing)"
            for column in required
            if features[column].isna().any()
        ]
        partial_preferred = [
            f"{column} ({features[column].isna().mean() * 100:.1f}% missing)"
            for column in preferred
            if column in available and features[column].notna().any() and features[column].isna().any()
        ]
        if missing_preferred or partial_required or partial_preferred:
            details = missing_preferred + partial_required + partial_preferred
            return "Partial", ", ".join(details)
        return "Ready", "None"

    rows = []
    specifications = [
        (
            "Reservoir screening",
            ("gr_api", "density_porosity_vv"),
            ("neutron_porosity_vv",),
            "Clean-sand and storage-capacity screen",
        ),
        (
            "Electrical saturation proxy",
            ("rt_ohm_m", "density_porosity_vv"),
            (),
            "Archie remains a calibrated supplementary cross-check",
        ),
        (
            "Acoustic phase support",
            ("vp_km_s",),
            ("vs_km_s",),
            "Vp is usable alone; Vs materially improves hydrate-versus-gas review",
        ),
        (
            "NMR-density saturation",
            ("density_porosity_vv", "nmr_porosity_vv"),
            (),
            "Preferred saturation target where NMR and depth alignment are defensible",
        ),
        (
            "Chong-style ML feature set",
            (),
            CHONG_ML_FEATURE_COLUMNS,
            "Two or three logs can support experiments; all six enable the full comparison",
        ),
        (
            "Bad-hole exclusion",
            ("caliper_washout_flag",),
            (),
            "Caliper upper-tail screening follows the attached paper's QC direction",
        ),
    ]
    for output, required, preferred, note in specifications:
        if output == "Chong-style ML feature set":
            count = sum(column in available for column in CHONG_ML_FEATURE_COLUMNS)
            output_status = "Ready" if count >= 3 else "Partial" if count >= 2 else "Blocked"
            missing = ", ".join(column for column in CHONG_ML_FEATURE_COLUMNS if column not in available) or "None"
        else:
            output_status, missing = status(required, preferred)
        rows.append(
            {
                "Output": output,
                "Status": output_status,
                "Missing or preferred": missing,
                "Scientific use": note,
            }
        )
    return pd.DataFrame(rows)


def grouped_well_split_frame(logs: pd.DataFrame) -> pd.DataFrame:
    if "well_alias" not in logs.columns:
        return pd.DataFrame(columns=["Well alias", "Split", "Rows", "Depth min (m)", "Depth max (m)"])

    wells = sorted(str(alias) for alias in logs["well_alias"].dropna().unique())
    if len(wells) < 3:
        assignments = {alias: "insufficient wells for train/validation/test" for alias in wells}
    else:
        assignments = {alias: "train" for alias in wells}
        assignments[wells[-2]] = "validation"
        assignments[wells[-1]] = "test"

    rows = []
    for alias in wells:
        well = logs[logs["well_alias"].astype(str) == alias]
        depth = pd.to_numeric(well.get("depth_m"), errors="coerce")
        rows.append(
            {
                "Well alias": alias,
                "Split": assignments[alias],
                "Rows": len(well),
                "Depth min (m)": round(float(depth.min()), 1) if depth.notna().any() else None,
                "Depth max (m)": round(float(depth.max()), 1) if depth.notna().any() else None,
            }
        )
    return pd.DataFrame(rows)


def project_cohort_plan_frame(total_wells: int = 71, known_fraction: float = 0.20) -> pd.DataFrame:
    if total_wells < 5:
        raise ValueError("At least five wells are required for a development and prediction plan.")
    if not 0 < known_fraction < 1:
        raise ValueError("Known-well fraction must be between 0 and 1.")

    development_wells = max(3, round(total_wells * known_fraction))
    prediction_wells = total_wells - development_wells
    validation_wells = max(1, round(development_wells * 0.15))
    test_wells = max(1, round(development_wells * 0.15))
    training_wells = development_wells - validation_wells - test_wells

    return pd.DataFrame(
        [
            {
                "Cohort": "Development - train",
                "Approximate wells": training_wells,
                "Labels visible during development": "Yes",
                "Purpose": "Fit classification and saturation models",
            },
            {
                "Cohort": "Development - validation",
                "Approximate wells": validation_wells,
                "Labels visible during development": "Yes",
                "Purpose": "Tune features, hyperparameters, thresholds, and abstention",
            },
            {
                "Cohort": "Development - locked test",
                "Approximate wells": test_wells,
                "Labels visible during development": "Hidden until final model selection",
                "Purpose": "Estimate performance before deployment",
            },
            {
                "Cohort": "Prediction / deployment",
                "Approximate wells": prediction_wells,
                "Labels visible during development": "No",
                "Purpose": "Predict classification and saturation for the remaining wells",
            },
        ]
    )
