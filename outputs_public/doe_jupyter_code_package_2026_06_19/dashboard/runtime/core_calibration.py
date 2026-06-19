from __future__ import annotations

import pandas as pd


def match_core_to_nearest_logs(
    logs: pd.DataFrame,
    core: pd.DataFrame,
    max_offset_m: float = 3.0,
) -> pd.DataFrame:
    rows = []
    for _, sample in core.iterrows():
        well = logs[logs["well_alias"] == sample["well_alias"]].copy()
        if well.empty:
            rows.append({**sample.to_dict(), "match_status": "missing well", "depth_offset_m": None})
            continue
        nearest = well.iloc[(well["depth_m"] - sample["sample_depth_m"]).abs().argmin()]
        offset = float(nearest["depth_m"] - sample["sample_depth_m"])
        rows.append(
            {
                **sample.to_dict(),
                "nearest_log_depth_m": float(nearest["depth_m"]),
                "depth_offset_m": round(offset, 2),
                "match_status": "matched" if abs(offset) <= max_offset_m else "depth review",
                "nearest_gr_api": nearest.get("gr_api"),
                "nearest_rt_ohm_m": nearest.get("rt_ohm_m"),
                "nearest_rhob_g_cc": nearest.get("rhob_g_cc"),
            }
        )
    return pd.DataFrame(rows)
