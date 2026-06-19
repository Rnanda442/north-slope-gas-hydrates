from __future__ import annotations

from pathlib import Path

import pandas as pd

from doe_jupyter_runtime_pack.run_spatial_stability_join import (
    DEFAULT_CASE_ROLES,
    spatial_join_case_wells,
)


def test_spatial_join_prefers_api_match_then_nearest() -> None:
    case_wells = pd.DataFrame(
        [
            {
                "well_case": "CASE_A",
                "case_role": "workbook_header_anchor",
                "map_label": "Case A",
                "api_number": "000123",
                "wellhead_latitude": 70.0,
                "wellhead_longitude": -150.0,
            },
            {
                "well_case": "CASE_B",
                "case_role": "public_source_case",
                "map_label": "Case B",
                "api_number": "",
                "wellhead_latitude": 70.2,
                "wellhead_longitude": -150.2,
            },
        ]
    )
    screen = pd.DataFrame(
        [
            {
                "well_name": "API match far away",
                "api_number": "123",
                "lat": 71.0,
                "lon": -151.0,
                "stability_result_status": "calculated",
                "stability_confidence": "medium",
            },
            {
                "well_name": "Nearest point",
                "api_number": "999",
                "lat": 70.21,
                "lon": -150.21,
                "stability_result_status": "blocked_missing_temperature_profile",
                "stability_confidence": "blocked",
            },
        ]
    )

    context, nearby = spatial_join_case_wells(case_wells, screen, nearby_count=2)

    case_a = context[context["case_label"].eq("Case A")].iloc[0]
    assert case_a["stability_join_method"] == "api_match"
    assert case_a["screen_well_name"] == "API match far away"

    case_b = context[context["case_label"].eq("Case B")].iloc[0]
    assert case_b["stability_join_method"] == "nearest_screen_point"
    assert case_b["screen_well_name"] == "Nearest point"
    assert len(nearby) == 4


def test_default_case_roles_select_four_public_case_wells() -> None:
    project_root = Path(__file__).resolve().parents[1]
    case_wells = pd.read_csv(
        project_root / "data/public_ml_products/four_well_case_location_index_2026-06-19.csv"
    )
    selected_roles = case_wells[case_wells["case_role"].isin(DEFAULT_CASE_ROLES)]

    assert set(selected_roles["well_case"]) == {"MTE", "IGS", "Hydrate-01", "HYDRATE 02"}

