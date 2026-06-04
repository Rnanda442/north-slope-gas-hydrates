from __future__ import annotations

import pandas as pd

from dashboard.runtime.schemas import REQUIRED_LOG_COLUMNS, RuntimeReadinessReport, ValidationIssue


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
