from __future__ import annotations

import pandas as pd


LOG_MATCH_COLUMNS = (
    "gr_api",
    "rt_ohm_m",
    "rhob_g_cc",
    "density_porosity_vv",
    "nmr_porosity_vv",
    "vp_km_s",
    "vs_km_s",
)


def _numeric_or_none(value: object) -> float | None:
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return None
    return float(numeric)


def normalize_core_depth_intervals(core: pd.DataFrame) -> pd.DataFrame:
    normalized = core.copy()
    for column in ("sample_depth_m", "sample_top_m", "sample_base_m"):
        if column in normalized.columns:
            normalized[column] = pd.to_numeric(normalized[column], errors="coerce")

    if "sample_depth_m" not in normalized.columns:
        normalized["sample_depth_m"] = pd.NA
    if "sample_top_m" not in normalized.columns:
        normalized["sample_top_m"] = pd.NA
    if "sample_base_m" not in normalized.columns:
        normalized["sample_base_m"] = pd.NA

    midpoint = (normalized["sample_top_m"] + normalized["sample_base_m"]) / 2.0
    normalized["sample_depth_m"] = pd.to_numeric(normalized["sample_depth_m"], errors="coerce").fillna(midpoint)
    normalized["sample_top_m"] = pd.to_numeric(normalized["sample_top_m"], errors="coerce").fillna(
        normalized["sample_depth_m"]
    )
    normalized["sample_base_m"] = pd.to_numeric(normalized["sample_base_m"], errors="coerce").fillna(
        normalized["sample_depth_m"]
    )

    swapped = normalized["sample_top_m"] > normalized["sample_base_m"]
    top = normalized.loc[swapped, "sample_top_m"].copy()
    normalized.loc[swapped, "sample_top_m"] = normalized.loc[swapped, "sample_base_m"]
    normalized.loc[swapped, "sample_base_m"] = top
    return normalized


def _nearest_log_row(well_logs: pd.DataFrame, depth_m: float) -> pd.Series:
    offsets = (pd.to_numeric(well_logs["depth_m"], errors="coerce") - depth_m).abs()
    return well_logs.loc[offsets.idxmin()]


def match_core_intervals_to_nearest_logs(
    logs: pd.DataFrame,
    core: pd.DataFrame,
    max_offset_m: float = 3.0,
) -> pd.DataFrame:
    normalized_core = normalize_core_depth_intervals(core)
    log_depths = logs.copy()
    if "depth_m" in log_depths.columns:
        log_depths["depth_m"] = pd.to_numeric(log_depths["depth_m"], errors="coerce")

    rows = []
    for _, sample in normalized_core.iterrows():
        well_logs = log_depths[log_depths["well_alias"].astype(str) == str(sample["well_alias"])].copy()
        if well_logs.empty:
            rows.append(
                {
                    **sample.to_dict(),
                    "match_status": "missing well",
                    "match_method": "none",
                    "nearest_log_depth_m": None,
                    "depth_offset_m": None,
                    "log_rows_inside_core_interval": 0,
                }
            )
            continue

        sample_depth = _numeric_or_none(sample.get("sample_depth_m"))
        top = _numeric_or_none(sample.get("sample_top_m"))
        base = _numeric_or_none(sample.get("sample_base_m"))
        if sample_depth is None:
            rows.append(
                {
                    **sample.to_dict(),
                    "match_status": "missing core depth",
                    "match_method": "none",
                    "nearest_log_depth_m": None,
                    "depth_offset_m": None,
                    "log_rows_inside_core_interval": 0,
                }
            )
            continue

        interval_logs = pd.DataFrame()
        if top is not None and base is not None:
            interval_logs = well_logs[well_logs["depth_m"].between(top, base, inclusive="both")]

        if not interval_logs.empty:
            nearest = _nearest_log_row(interval_logs, sample_depth)
            match_method = "interval_overlap"
            offset = float(nearest["depth_m"] - sample_depth)
            match_status = "matched"
        else:
            nearest = _nearest_log_row(well_logs, sample_depth)
            match_method = "nearest_depth"
            offset = float(nearest["depth_m"] - sample_depth)
            match_status = "matched" if abs(offset) <= max_offset_m else "depth review"

        output = {
            **sample.to_dict(),
            "nearest_log_depth_m": float(nearest["depth_m"]),
            "depth_offset_m": round(offset, 2),
            "match_status": match_status,
            "match_method": match_method,
            "log_rows_inside_core_interval": int(len(interval_logs)),
        }
        for column in LOG_MATCH_COLUMNS:
            if column in nearest:
                output[f"nearest_{column}"] = nearest.get(column)
        rows.append(output)
    return pd.DataFrame(rows)


def match_core_to_nearest_logs(
    logs: pd.DataFrame,
    core: pd.DataFrame,
    max_offset_m: float = 3.0,
) -> pd.DataFrame:
    return match_core_intervals_to_nearest_logs(logs, core, max_offset_m=max_offset_m)
