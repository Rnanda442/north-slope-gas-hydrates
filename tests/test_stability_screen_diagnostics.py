from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from shapely.geometry import Polygon

from dashboard.app import (
    build_unified_north_slope_context_map,
    build_stability_screen_map,
    build_temperature_proxy_map,
    build_selected_well_phase_audit_figure,
    basemap_landmark_bundle_is_available,
    default_basemap_landmark_source_dir,
    g10015_temperature_control_crosswalk_frame,
    unified_context_map_layer_inventory_frame,
    unified_context_map_source_caveat_caption,
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


def test_basemap_landmark_source_prefers_tracked_public_bundle(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.delenv("NORTH_SLOPE_BASEMAP_SOURCE_DIR", raising=False)
    project_root = tmp_path
    raw_dir = project_root / "data" / "source_library" / "basemap_landmarks_2026_06_18"
    public_dir = (
        project_root
        / "data"
        / "public_gis_products"
        / "basemap_landmarks_2026_06_18"
    )

    assert default_basemap_landmark_source_dir(project_root) == raw_dir
    public_dir.mkdir(parents=True)
    for name in [
        "alaska_dnr_unit_boundary_current_north_slope_clip.geojson",
        "alaska_akdot_roads_north_slope_clip.geojson",
        "alaska_dnr_trans_alaska_pipeline.geojson",
        "usgs_gnis_places_north_slope_clip.geojson",
    ]:
        (public_dir / name).write_text('{"type":"FeatureCollection","features":[]}', encoding="utf-8")

    assert basemap_landmark_bundle_is_available(public_dir)
    assert default_basemap_landmark_source_dir(project_root) == public_dir

    override_dir = tmp_path / "custom_osl_bundle"
    monkeypatch.setenv("NORTH_SLOPE_BASEMAP_SOURCE_DIR", str(override_dir))
    assert default_basemap_landmark_source_dir(project_root) == override_dir


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
            {
                "well_name": "GMT TEST 1",
                "field": "GREATER MOOSES TOOTH",
                "lat": 70.18,
                "lon": -151.69,
                "tvd_m": 1150,
                "stability_result_status": "blocked_phase_curve_range_insufficient",
                "stability_confidence": "blocked",
                "stability_top_m": None,
                "stability_base_m": None,
                "stability_thickness_m": None,
            },
            {
                "well_name": "BADAMI TEST 1",
                "field": "BADAMI",
                "lat": 70.15,
                "lon": -147.09,
                "tvd_m": 1250,
                "stability_result_status": "blocked_missing_depth",
                "stability_confidence": "blocked",
                "stability_top_m": None,
                "stability_base_m": None,
                "stability_thickness_m": None,
            },
        ]
    )


def minimal_case_well_index() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "well_case": "MTE",
                "case_role": "workbook_header_anchor",
                "map_label": "MTE / Mount Elbert",
                "verified_public_well_name": "MT ELBERT 1",
                "api_number": "50029233020000",
                "permit_number": "2060330",
                "field": "MILNE POINT",
                "current_status": "Plugged & Abandoned",
                "wellhead_latitude": 70.455636,
                "wellhead_longitude": -149.410798,
                "evidence_status": "Header-only screenshot verifies MTE.",
                "website_use_note": "Show as project well anchor.",
            },
            {
                "well_case": "IGS",
                "case_role": "workbook_header_anchor",
                "map_label": "IGS / Ignik Sikumi",
                "verified_public_well_name": "PRUDHOE BAY UN IGNIK SIKUMI 1",
                "api_number": "50029234430000",
                "permit_number": "2110270",
                "field": "PRUDHOE BAY",
                "current_status": "Plugged & Abandoned",
                "wellhead_latitude": 70.348712,
                "wellhead_longitude": -149.317096,
                "evidence_status": "Header-only screenshot verifies IGS.",
                "website_use_note": "Show as project well anchor.",
            },
            {
                "well_case": "Hydrate-01",
                "case_role": "public_source_case",
                "map_label": "Hydrate-01",
                "verified_public_well_name": "HYDRATE 01",
                "api_number": "50029236130000",
                "permit_number": "2181250",
                "field": "*EXPLORATORY",
                "current_status": "Suspended well",
                "wellhead_latitude": 70.316936,
                "wellhead_longitude": -149.200104,
                "evidence_status": "Public source-case anchor.",
                "website_use_note": "Show as source-case anchor.",
            },
            {
                "well_case": "HYDRATE 02",
                "case_role": "public_source_case",
                "map_label": "HYDRATE 02",
                "verified_public_well_name": "HYDRATE 02",
                "api_number": "50029237280000",
                "permit_number": "2221140",
                "field": "*EXPLORATORY",
                "current_status": "Gas well, single completion",
                "wellhead_latitude": 70.317174,
                "wellhead_longitude": -149.200285,
                "evidence_status": "Public source-case anchor.",
                "website_use_note": "Show as source-case anchor.",
            },
            {
                "well_case": "HYDRATE 02 associated well",
                "case_role": "associated_test_well",
                "map_label": "HYDRATE P1",
                "verified_public_well_name": "HYDRATE P1",
                "api_number": "50029237370000",
                "permit_number": "2221410",
                "field": "*EXPLORATORY",
                "current_status": "Observation well",
                "wellhead_latitude": 70.317056,
                "wellhead_longitude": -149.200186,
                "evidence_status": "Associated test-site well.",
                "website_use_note": "Only show in full context.",
            },
        ]
    )


def minimal_permafrost_points() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "well_designation": "Synthetic GGD223 Control",
                "code": "SYN",
                "latitude": 70.25,
                "longitude": -149.25,
                "elevation_m": 8,
                "permafrost_depth_m": 520,
            }
        ]
    )


def minimal_assessment_units() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "ASSESSNAME": "Synthetic gas hydrate assessment unit",
                "geometry": Polygon(
                    [
                        (-150.4, 69.95),
                        (-148.1, 69.95),
                        (-148.1, 70.65),
                        (-150.4, 70.65),
                        (-150.4, 69.95),
                    ]
                ),
            }
        ]
    )


def minimal_geoscience_context() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "layer_name": "extent",
                "feature_id": "extent",
                "vertex_order": 1,
                "lon": -150.5,
                "lat": 69.9,
                "depth_m": None,
                "au_name": None,
            },
            {
                "layer_name": "extent",
                "feature_id": "extent",
                "vertex_order": 2,
                "lon": -148.0,
                "lat": 69.9,
                "depth_m": None,
                "au_name": None,
            },
            {
                "layer_name": "extent",
                "feature_id": "extent",
                "vertex_order": 3,
                "lon": -148.0,
                "lat": 70.7,
                "depth_m": None,
                "au_name": None,
            },
            {
                "layer_name": "extent",
                "feature_id": "extent",
                "vertex_order": 4,
                "lon": -150.5,
                "lat": 70.7,
                "depth_m": None,
                "au_name": None,
            },
            {
                "layer_name": "extent",
                "feature_id": "extent",
                "vertex_order": 5,
                "lon": -150.5,
                "lat": 69.9,
                "depth_m": None,
                "au_name": None,
            },
            {
                "layer_name": "assessment_units",
                "feature_id": "au1",
                "vertex_order": 1,
                "lon": -150.2,
                "lat": 70.0,
                "depth_m": None,
                "au_name": "Synthetic public AU context",
            },
            {
                "layer_name": "assessment_units",
                "feature_id": "au1",
                "vertex_order": 2,
                "lon": -148.2,
                "lat": 70.5,
                "depth_m": None,
                "au_name": "Synthetic public AU context",
            },
            {
                "layer_name": "seismic_2d",
                "feature_id": "line1",
                "vertex_order": 1,
                "lon": -150.1,
                "lat": 70.1,
                "depth_m": None,
                "au_name": None,
            },
            {
                "layer_name": "seismic_2d",
                "feature_id": "line1",
                "vertex_order": 2,
                "lon": -148.4,
                "lat": 70.45,
                "depth_m": None,
                "au_name": None,
            },
            {
                "layer_name": "seismic_3d_inventory",
                "feature_id": "survey1",
                "vertex_order": 1,
                "lon": -149.8,
                "lat": 70.2,
                "depth_m": None,
                "au_name": None,
            },
            {
                "layer_name": "seismic_3d_inventory",
                "feature_id": "survey1",
                "vertex_order": 2,
                "lon": -148.8,
                "lat": 70.35,
                "depth_m": None,
                "au_name": None,
            },
            {
                "layer_name": "wells",
                "feature_id": "well1",
                "vertex_order": 1,
                "lon": -149.0,
                "lat": 70.3,
                "depth_m": 1200,
                "au_name": None,
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


def test_unified_context_map_combines_status_source_and_landmark_layers(
    tmp_path: Path,
) -> None:
    landmark_source = make_landmark_source_dir(tmp_path)
    figure = build_unified_north_slope_context_map(
        minimal_screen_frame(),
        minimal_permafrost_points(),
        minimal_assessment_units(),
        landmark_source,
        minimal_geoscience_context(),
        case_well_index=minimal_case_well_index(),
    )

    trace_names = {trace.name for trace in figure.data}
    assert "North Slope Borough boundary" in trace_names
    assert "Public assessment-unit context" in trace_names
    assert "2D seismic coverage" in trace_names
    assert "3D seismic footprints" in trace_names
    assert "North Slope study boundary" in trace_names
    assert "Public well reference points" not in trace_names
    assert "DNR oil/gas unit outlines" in trace_names
    assert "Dalton/Deadhorse roads" in trace_names
    assert "Trans-Alaska Pipeline" in trace_names
    assert "USGS hydrate AU outlines" in trace_names
    assert "GGD223 pf_depth_m controls" in trace_names
    assert "Calculated screen interval" in trace_names
    assert "Background: no temperature profile" not in trace_names
    assert "Header-verified project wells" in trace_names
    assert "Public source-case project wells" in trace_names
    assert "Associated HYDRATE 02 test wells" not in trace_names
    assert "Project well labels" in trace_names
    assert "Regional orientation labels" in trace_names
    assert "Public well field labels" in trace_names
    assert (
        figure.layout.title.text
        == "Focused 2D North Slope Map: calculated stability ranges and project wells"
    )

    pf_trace = next(
        trace for trace in figure.data if trace.name == "GGD223 pf_depth_m controls"
    )
    assert pf_trace.marker.colorbar.title.text == "pf_depth_m"
    calculated_trace = next(
        trace for trace in figure.data if trace.name == "Calculated screen interval"
    )
    assert len(calculated_trace.lat) == 1
    project_label_trace = next(
        trace for trace in figure.data if trace.name == "Project well labels"
    )
    assert "MTE / Mount Elbert" in set(project_label_trace.text)
    assert "HYDRATE 02" in set(project_label_trace.text)
    field_label_trace = next(
        trace for trace in figure.data if trace.name == "Public well field labels"
    )
    assert "Greater Mooses Tooth" in set(field_label_trace.text)
    assert "Badami" in set(field_label_trace.text)

    inventory = unified_context_map_layer_inventory_frame(Path("missing_dggs_preview.png"))
    assert "Regional Boundary" in set(inventory["layer_group"])
    assert "DGGS RI 2018-6" in set(inventory["layer_group"])
    assert "Geoscience Orientation" in set(inventory["layer_group"])
    assert "missing preview" in set(inventory["shown_as"])

    caption = unified_context_map_source_caveat_caption(landmark_source)
    assert "do not prove hydrate occurrence" in caption
    assert "saturation" in caption


def test_unified_context_map_full_context_restores_background_layers(
    tmp_path: Path,
) -> None:
    landmark_source = make_landmark_source_dir(tmp_path)
    figure = build_unified_north_slope_context_map(
        minimal_screen_frame(),
        minimal_permafrost_points(),
        minimal_assessment_units(),
        landmark_source,
        minimal_geoscience_context(),
        case_well_index=minimal_case_well_index(),
        focused=False,
        include_public_reference_points=True,
        include_associated_case_wells=True,
    )

    trace_names = {trace.name for trace in figure.data}
    assert "Public well reference points" in trace_names
    assert "Background: no temperature profile" in trace_names
    assert "Associated HYDRATE 02 test wells" in trace_names
    assert (
        figure.layout.title.text
        == "Unified 2D North Slope Map: geology, controls, landmarks, and stability status"
    )

    public_reference_trace = next(
        trace for trace in figure.data if trace.name == "Public well reference points"
    )
    assert public_reference_trace.marker.size == 1.8
    assert public_reference_trace.marker.opacity == 0.14
    background_trace = next(
        trace for trace in figure.data if trace.name == "Background: no temperature profile"
    )
    assert background_trace.marker.size == 2.4
    assert background_trace.marker.opacity == 0.16


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
