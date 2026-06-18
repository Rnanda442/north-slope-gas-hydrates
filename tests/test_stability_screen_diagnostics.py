from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from dashboard.app import (
    build_stability_screen_map,
    build_temperature_proxy_map,
    build_selected_well_phase_audit_figure,
    g10015_temperature_control_crosswalk_frame,
    public_field_label_frame,
    stability_screen_source_method_frame,
    stability_blank_reason_summary_frame,
    temperature_proxy_candidate_audit_frame,
    temperature_proxy_tier_summary_frame,
)
from dashboard.stability_products import (
    load_methane_phase_curve,
    load_g10015_temperature_inventory,
    load_stability_screen,
    load_stability_temperature_model,
)
from dashboard.stability_sources import (
    active_stability_source_path,
    load_ggd223_permafrost_points,
)


def write_feature_collection(path: Path, features: list[dict]) -> None:
    path.write_text(
        json.dumps({"type": "FeatureCollection", "features": features}),
        encoding="utf-8",
    )


def make_landmark_source_dir(tmp_path: Path) -> Path:
    write_feature_collection(
        tmp_path / "alaska_dnr_unit_boundary_current_north_slope_clip.geojson",
        [
            {
                "type": "Feature",
                "properties": {"UnitName": "Prudhoe Bay"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [-149.0, 70.1],
                            [-148.3, 70.1],
                            [-148.3, 70.5],
                            [-149.0, 70.5],
                            [-149.0, 70.1],
                        ]
                    ],
                },
            }
        ],
    )
    write_feature_collection(
        tmp_path / "alaska_akdot_roads_north_slope_clip.geojson",
        [
            {
                "type": "Feature",
                "properties": {"Route_Name": "Dalton Highway"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[-149.2, 69.8], [-148.6, 70.4]],
                },
            }
        ],
    )
    write_feature_collection(
        tmp_path / "alaska_dnr_trans_alaska_pipeline.geojson",
        [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "MultiLineString",
                    "coordinates": [[[-149.1, 69.9], [-148.5, 70.3]]],
                },
            }
        ],
    )
    write_feature_collection(
        tmp_path / "usgs_gnis_places_north_slope_clip.geojson",
        [
            {
                "type": "Feature",
                "properties": {"gaz_name": "City of Nuiqsut"},
                "geometry": {"type": "MultiPoint", "coordinates": [[-151.0, 70.2]]},
            }
        ],
    )
    return tmp_path


def minimal_screen_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "well_name": "PB TEST 1",
                "field": "PRUDHOE BAY",
                "lat": 70.30,
                "lon": -148.70,
                "tvd_m": 1100,
                "stability_result_status": "calculated",
                "stability_confidence": "high_source_control",
                "stability_top_m": 600,
                "stability_base_m": 900,
                "stability_thickness_m": 300,
            },
            {
                "well_name": "KUP TEST 1",
                "field": "KUPARUK RIVER",
                "lat": 70.32,
                "lon": -149.8,
                "tvd_m": 1200,
                "stability_result_status": "blocked_missing_temperature_profile",
                "stability_confidence": "blocked",
                "stability_top_m": None,
                "stability_base_m": None,
                "stability_thickness_m": None,
            },
        ]
    )


def test_2d_well_maps_add_uploaded_landmark_context(tmp_path: Path) -> None:
    landmark_source = make_landmark_source_dir(tmp_path)
    screen = minimal_screen_frame()

    labels = public_field_label_frame(screen)
    assert labels["label"].tolist()[:2] == ["Prudhoe Bay", "Kuparuk River"]

    stability_figure = build_stability_screen_map(screen, landmark_source)
    stability_trace_names = {trace.name for trace in stability_figure.data}
    assert "DNR oil/gas unit outlines" in stability_trace_names
    assert "Dalton/Deadhorse roads" in stability_trace_names
    assert "Trans-Alaska Pipeline" in stability_trace_names

    stability_text = " ".join(
        str(text)
        for trace in stability_figure.data
        for text in (trace.text if getattr(trace, "mode", "") == "text" else [])
    )
    assert "Prudhoe Bay" in stability_text
    assert "Nuiqsut" in stability_text

    proxy = screen.assign(
        temperature_proxy_tier="direct_g10015_profile_match",
        temperature_proxy_tier_label="Direct G10015 profile match",
        nearest_g10015_control_code="SYN",
        nearest_g10015_control_distance_km=12.0,
    )
    proxy_figure = build_temperature_proxy_map(proxy, landmark_source)
    proxy_trace_names = {trace.name for trace in proxy_figure.data}
    assert "DNR oil/gas unit outlines" in proxy_trace_names
    assert "Dalton/Deadhorse roads" in proxy_trace_names
    assert "Trans-Alaska Pipeline" in proxy_trace_names


def test_committed_stability_screen_diagnostics_explain_blanks_and_proxy_tiers() -> None:
    project_root = Path(__file__).resolve().parents[1]
    source_root = active_stability_source_path(project_root)
    screen = load_stability_screen(project_root)
    inventory = load_g10015_temperature_inventory(project_root)
    controls = load_ggd223_permafrost_points(source_root).drop(
        columns="geometry",
        errors="ignore",
    )

    crosswalk = g10015_temperature_control_crosswalk_frame(inventory, controls)
    crosswalk_counts = crosswalk["coordinate_status"].value_counts().to_dict()
    assert crosswalk_counts["located_from_committed_ggd223_control"] == 22
    assert crosswalk_counts["missing_committed_coordinate_crosswalk"] == 2

    blank_summary = stability_blank_reason_summary_frame(screen)
    blank_counts = blank_summary.set_index("status_code")["rows"].to_dict()
    assert blank_counts["blocked_missing_temperature_profile"] == 7113
    assert blank_counts["blocked_missing_depth"] == 505
    assert blank_counts["blocked_phase_curve_range_insufficient"] == 344
    assert blank_counts["outside_au_context"] == 92

    proxy_audit = temperature_proxy_candidate_audit_frame(screen, crosswalk)
    proxy_summary = temperature_proxy_tier_summary_frame(proxy_audit)
    proxy_counts = proxy_summary.set_index("tier_code")["rows"].to_dict()
    assert proxy_counts["direct_g10015_profile_match"] == 483
    assert proxy_counts["proxy_candidate_near_g10015_control"] == 193
    assert proxy_counts["proxy_candidate_regional_g10015_control"] == 4917
    assert proxy_counts["distant_from_g10015_controls"] == 2003


def test_selected_well_phase_audit_figure_uses_public_temperature_and_phase_products() -> None:
    project_root = Path(__file__).resolve().parents[1]
    screen = load_stability_screen(project_root)
    temperature_model = load_stability_temperature_model(project_root)
    phase_curve = load_methane_phase_curve(project_root)
    calculated_row = screen[screen["stability_result_status"].eq("calculated")].iloc[0]
    profile_points = temperature_model[
        temperature_model["object_id"].eq(calculated_row["object_id"])
    ][["temperature_profile_file", "temperature_profile_code", "depth_m", "temperature_model_c"]].rename(
        columns={
            "temperature_profile_file": "file_name",
            "temperature_profile_code": "well_code",
            "temperature_model_c": "temperature_c",
        }
    )
    profile_points["sample_method"] = "test_sampled_points"

    figure = build_selected_well_phase_audit_figure(
        calculated_row,
        temperature_model,
        phase_curve,
        profile_points,
    )

    trace_names = {trace.name for trace in figure.data}
    assert "Methane 5 ppt CSV phase boundary" in trace_names
    assert "G10015 measured temperature profile" in trace_names
    assert "Modeled well temperature key depths" in trace_names
    assert "Screen top/base" in trace_names
    assert "Modeled stability range" in trace_names
    assert any(
        shape.type == "rect"
        and shape.y0 == calculated_row["stability_top_m"]
        and shape.y1 == calculated_row["stability_base_m"]
        for shape in figure.layout.shapes
    )


def test_stability_screen_source_method_frame_separates_phase_curve_from_g10015() -> None:
    project_root = Path(__file__).resolve().parents[1]
    phase_curve = load_methane_phase_curve(project_root)

    frame = stability_screen_source_method_frame(phase_curve)

    joined = " ".join(frame.astype(str).to_numpy().ravel())
    assert "G10015 is the temperature source" in joined
    assert "CSV/PNG curve is a phase-boundary input" in joined
    assert "100 percent methane" in joined
    assert "5" in joined
