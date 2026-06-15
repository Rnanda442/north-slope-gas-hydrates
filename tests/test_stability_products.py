from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon

from dashboard.stability_products import (
    APPROVED_SCHEMA_COVERAGE_MATRIX_COLUMNS,
    PHASE_CURVE_ALLOWED_USE,
    PHASE_CURVE_GAS_COMPOSITION_ASSUMPTION,
    PHASE_CURVE_ID,
    PHASE_CURVE_ROLE,
    build_g10015_temperature_inventory,
    build_g10015_temperature_profile_points_product,
    build_public_well_stability_context,
    build_public_ml_feature_scaffold,
    build_stability_input_scaffold,
    build_stability_screen,
    build_stability_temperature_model,
    default_g10015_profile_points_path,
    default_g10015_profile_points_summary_path,
    default_approved_schema_coverage_matrix_path,
    default_public_ml_feature_dictionary_path,
    default_public_ml_leakage_guardrails_path,
    default_public_ml_feature_scaffold_path,
    default_public_ml_feature_scaffold_summary_path,
    default_public_ml_target_registry_path,
    default_phase_curve_path,
    default_phase_curve_scenario_catalog_path,
    default_stability_screen_path,
    default_stability_screen_summary_path,
    default_stability_temperature_model_path,
    default_stability_input_capability_matrix_path,
    default_stability_osl_pull_triggers_path,
    default_stability_website_product_spec_path,
    default_well_context_path,
    hydrostatic_pressure_mpa_absolute,
    hydrostatic_pressure_mpa_gauge,
    load_arctic_slope_public_wells,
    load_approved_schema_coverage_matrix,
    load_g10015_temperature_profile_points,
    load_phase_curve,
    load_phase_curve_scenario_catalog,
    load_methane_phase_curve,
    parse_g10015_temperature_profile,
    phase_curve_equilibrium_temperature_c,
    g10015_temperature_profile_points_summary_frame,
    public_ml_feature_dictionary_frame,
    public_ml_feature_scaffold_summary_frame,
    public_ml_leakage_guardrails_frame,
    public_ml_target_registry_frame,
    stability_input_capability_matrix_frame,
    stability_condition_grid_from_profile,
    stability_osl_pull_triggers_frame,
    stability_parameter_readiness_frame,
    stability_context_summary_frame,
    stability_depth_grid,
    stability_interval_from_condition_grid,
    stability_input_scaffold_summary_frame,
    stability_screen_summary_frame,
    stability_temperature_model_summary_frame,
    stability_website_product_spec_frame,
    stability_source_control_label,
    temperature_model_from_profile,
    temperature_inventory_summary_frame,
    write_public_stability_products,
    write_public_ml_feature_products,
    write_public_ml_target_registry_products,
    write_g10015_temperature_profile_points_product,
    write_stability_screen_product,
    write_stability_temperature_model_product,
)


def make_public_well_package(tmp_path):
    well_dir = tmp_path / "raw_data" / "Wells" / "Well_Bottom_Hole_Location"
    well_dir.mkdir(parents=True)
    wells = gpd.GeoDataFrame(
        [
            {
                "OBJECTID": 1,
                "PermitNumb": "100",
                "APINumber": "500001",
                "WellName": "TEST NORTH SLOPE 1",
                "Geographic": "ARCTIC SLOPE",
                "Field": "*EXPLORATORY",
                "Pools": "Unknown",
                "CurrentCla": "Exploratory",
                "CurrentSta": "Plugged & Abandoned",
                "DrillerTot": 3000.0,
                "TrueVertic": 2500.0,
                "WellHeadLa": 70.1,
                "WellHeadLo": -150.1,
                "BottomHole": 70.1,
                "BottomHo_1": -150.1,
                "geometry": Point(-150.1, 70.1),
            },
            {
                "OBJECTID": 2,
                "PermitNumb": "200",
                "APINumber": "500002",
                "WellName": "TEST COOK INLET 1",
                "Geographic": "COOK INLET BASIN",
                "Field": "*EXPLORATORY",
                "Pools": "Unknown",
                "CurrentCla": "Exploratory",
                "CurrentSta": "Plugged & Abandoned",
                "DrillerTot": 1000.0,
                "TrueVertic": 900.0,
                "WellHeadLa": 61.1,
                "WellHeadLo": -149.9,
                "BottomHole": 61.1,
                "BottomHo_1": -149.9,
                "geometry": Point(-149.9, 61.1),
            },
        ],
        crs="EPSG:4326",
    ).to_crs("EPSG:3338")
    wells.to_file(well_dir / "Well_Bottom_Hole_Location.shp")


def make_public_snapshot(tmp_path):
    snapshot = tmp_path / "data" / "public_stability_snapshot" / "north_slope_stability_snapshot_2026-06-13"
    snapshot.mkdir(parents=True)
    pd.DataFrame(
        [
            {
                "well_designation": "Synthetic GGD223 Control",
                "code": "SYN",
                "latitude": 70.11,
                "longitude": -150.11,
                "elevation_m": 10,
                "permafrost_depth_m": 300,
                "source": "NSIDC GGD223 stnlist.dat",
            }
        ]
    ).to_csv(snapshot / "ggd223_permafrost_controls.csv", index=False)
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "ASSESSCODE": "50010203",
                    "ASSESSNAME": "Nanushuk Formation Gas Hydrate",
                },
                "geometry": Polygon(
                    [
                        (-151, 69.5),
                        (-149, 69.5),
                        (-149, 70.5),
                        (-151, 70.5),
                        (-151, 69.5),
                    ]
                ).__geo_interface__,
            }
        ],
    }
    (snapshot / "GasHydrateAUs.geojson").write_text(json.dumps(geojson), encoding="utf-8")
    (snapshot / "README.md").write_text("snapshot\n", encoding="utf-8")
    return snapshot


def make_temperature_profile(source_root):
    profile_dir = source_root / "03_temperature_geothermal" / "NSIDC_G10015_extracted"
    profile_dir.mkdir(parents=True)
    profile = profile_dir / "SYN_24JUN14.txt"
    profile.write_text(
        "\n".join(
            [
                "Temperature Log Information:",
                "  Well name:   Synthetic Test Well",
                "  File name:   SYN_24JUN14_c_d",
                "  Log date:    14-JUN-2026",
                "",
                " Depth  Temperature",
                "  0.00  -10.0",
                " 50.00  -7.0",
                "100.00  -4.0",
                "150.00  -1.0",
            ]
        ),
        encoding="utf-8",
    )
    return profile


def make_phase_curve_lookup(project_root):
    product_dir = project_root / "data" / "public_stability_products"
    product_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(
        [
            {
                "phase_curve_id": PHASE_CURVE_ID,
                "source_depth_m": 500,
                "pressure_mpa_absolute": 6.0,
                "equilibrium_temperature_c": 8.0,
                "phase_curve_role": "baseline",
                "gas_composition_assumption": "100_percent_methane",
                "gas_methane_mol_pct": 100,
                "gas_ethane_mol_pct": 0,
                "gas_propane_mol_pct": 0,
                "gas_butane_plus_mol_pct": 0,
                "salinity_ppt_assumption": 5,
                "source_citation": "Synthetic phase-curve test row",
                "source_url": "https://example.test/source",
                "source_extraction_method": "unit_test_fixture",
                "source_notes": "synthetic",
            },
            {
                "phase_curve_id": PHASE_CURVE_ID,
                "source_depth_m": 100,
                "pressure_mpa_absolute": 2.0,
                "equilibrium_temperature_c": 0.0,
                "phase_curve_role": "baseline",
                "gas_composition_assumption": "100_percent_methane",
                "gas_methane_mol_pct": 100,
                "gas_ethane_mol_pct": 0,
                "gas_propane_mol_pct": 0,
                "gas_butane_plus_mol_pct": 0,
                "salinity_ppt_assumption": 5,
                "source_citation": "Synthetic phase-curve test row",
                "source_url": "https://example.test/source",
                "source_extraction_method": "unit_test_fixture",
                "source_notes": "synthetic",
            },
            {
                "phase_curve_id": PHASE_CURVE_ID,
                "source_depth_m": 300,
                "pressure_mpa_absolute": 4.0,
                "equilibrium_temperature_c": 4.0,
                "phase_curve_role": "baseline",
                "gas_composition_assumption": "100_percent_methane",
                "gas_methane_mol_pct": 100,
                "gas_ethane_mol_pct": 0,
                "gas_propane_mol_pct": 0,
                "gas_butane_plus_mol_pct": 0,
                "salinity_ppt_assumption": 5,
                "source_citation": "Synthetic phase-curve test row",
                "source_url": "https://example.test/source",
                "source_extraction_method": "unit_test_fixture",
                "source_notes": "synthetic",
            },
        ]
    ).to_csv(default_phase_curve_path(project_root), index=False)


def make_broad_phase_curve_lookup(project_root):
    product_dir = project_root / "data" / "public_stability_products"
    product_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for depth_m, equilibrium_temperature_c in [(0.0, -5.0), (500.0, 7.5), (1000.0, 20.0)]:
        rows.append(
            {
                "phase_curve_id": PHASE_CURVE_ID,
                "source_depth_m": depth_m,
                "pressure_mpa_absolute": hydrostatic_pressure_mpa_absolute(depth_m),
                "equilibrium_temperature_c": equilibrium_temperature_c,
                "phase_curve_role": "baseline",
                "gas_composition_assumption": "100_percent_methane",
                "gas_methane_mol_pct": 100,
                "gas_ethane_mol_pct": 0,
                "gas_propane_mol_pct": 0,
                "gas_butane_plus_mol_pct": 0,
                "salinity_ppt_assumption": 5,
                "source_citation": "Synthetic broad phase-curve test row",
                "source_url": "https://example.test/broad",
                "source_extraction_method": "unit_test_fixture",
                "source_notes": "synthetic",
            }
        )
    pd.DataFrame(rows).to_csv(default_phase_curve_path(project_root), index=False)


def make_phase_curve_with_shallow_gap(project_root):
    product_dir = project_root / "data" / "public_stability_products"
    product_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for depth_m, equilibrium_temperature_c in [(100.0, 5.0), (500.0, 15.0), (1000.0, 20.0)]:
        rows.append(
            {
                "phase_curve_id": PHASE_CURVE_ID,
                "source_depth_m": depth_m,
                "pressure_mpa_absolute": hydrostatic_pressure_mpa_absolute(depth_m),
                "equilibrium_temperature_c": equilibrium_temperature_c,
                "phase_curve_role": "baseline",
                "gas_composition_assumption": "100_percent_methane",
                "gas_methane_mol_pct": 100,
                "gas_ethane_mol_pct": 0,
                "gas_propane_mol_pct": 0,
                "gas_butane_plus_mol_pct": 0,
                "salinity_ppt_assumption": 5,
                "source_citation": "Synthetic shallow-gap phase-curve test row",
                "source_url": "https://example.test/shallow-gap",
                "source_extraction_method": "unit_test_fixture",
                "source_notes": "synthetic",
            }
        )
    pd.DataFrame(rows).to_csv(default_phase_curve_path(project_root), index=False)


def make_phase_curve_scenario_catalog(project_root):
    product_dir = project_root / "data" / "public_stability_products"
    product_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(
        [
            {
                "phase_curve_id": PHASE_CURVE_ID,
                "phase_curve_role": "baseline",
                "curve_status": "available_digitized_lookup",
                "gas_composition_assumption": "100_percent_methane",
                "gas_methane_mol_pct": 100,
                "gas_ethane_mol_pct": 0,
                "gas_propane_mol_pct": 0,
                "gas_butane_plus_mol_pct": 0,
                "salinity_ppt_assumption": 5,
                "pressure_gradient_mpa_per_m": 0.00980665,
                "source_citation": "Synthetic baseline source",
                "source_url": "https://example.test/baseline",
                "source_notes": "synthetic",
                "allowed_use": "official_public_baseline",
            },
            {
                "phase_curve_id": "mixed_gas_pending",
                "phase_curve_role": "sensitivity_candidate",
                "curve_status": "source_identified_not_digitized",
                "gas_composition_assumption": (
                    "98_percent_methane_1p5_percent_ethane_0p5_percent_propane"
                ),
                "gas_methane_mol_pct": 98,
                "gas_ethane_mol_pct": 1.5,
                "gas_propane_mol_pct": 0.5,
                "gas_butane_plus_mol_pct": 0,
                "salinity_ppt_assumption": pd.NA,
                "pressure_gradient_mpa_per_m": 0.009795,
                "source_citation": "Synthetic sensitivity source",
                "source_url": "https://example.test/sensitivity",
                "source_notes": "synthetic",
                "allowed_use": "sensitivity_only_not_final",
            },
        ]
    ).to_csv(default_phase_curve_scenario_catalog_path(project_root), index=False)


def make_linear_phase_curve_from_depth_temperatures(depth_temperatures):
    rows = []
    for depth_m, equilibrium_temperature_c in depth_temperatures:
        rows.append(
            {
                "pressure_mpa_absolute": hydrostatic_pressure_mpa_absolute(depth_m),
                "equilibrium_temperature_c": equilibrium_temperature_c,
            }
        )
    return pd.DataFrame(rows)


def test_hydrostatic_pressure_helpers_track_gauge_and_absolute_pressure() -> None:
    assert round(float(hydrostatic_pressure_mpa_gauge(1000)), 6) == 9.80665
    assert round(float(hydrostatic_pressure_mpa_absolute(1000)), 6) == 9.907975


def test_phase_curve_lookup_loads_sorted_and_interpolates(tmp_path) -> None:
    make_phase_curve_lookup(tmp_path)

    curve = load_methane_phase_curve(tmp_path)

    assert curve["pressure_mpa_absolute"].is_monotonic_increasing
    assert set(curve["phase_curve_role"]) == {"baseline"}
    assert set(curve["gas_methane_mol_pct"]) == {100}
    assert phase_curve_equilibrium_temperature_c(curve, 3.0) == 2.0
    assert pd.isna(phase_curve_equilibrium_temperature_c(curve, 1.0))
    assert pd.isna(phase_curve_equilibrium_temperature_c(curve, 7.0))


def test_phase_curve_loader_can_select_by_versioned_curve_id(tmp_path) -> None:
    make_phase_curve_lookup(tmp_path)

    curve = load_phase_curve(tmp_path, PHASE_CURVE_ID)
    missing_curve = load_phase_curve(tmp_path, "not_present")

    assert len(curve) == 3
    assert missing_curve.empty


def test_phase_curve_scenario_catalog_marks_mixed_gas_as_sensitivity_only(tmp_path) -> None:
    make_phase_curve_scenario_catalog(tmp_path)

    catalog = load_phase_curve_scenario_catalog(tmp_path)
    baseline = catalog.loc[catalog["phase_curve_role"] == "baseline"].iloc[0]
    mixed = catalog.loc[catalog["phase_curve_role"] == "sensitivity_candidate"].iloc[0]

    assert baseline["phase_curve_id"] == PHASE_CURVE_ID
    assert baseline["allowed_use"] == "official_public_baseline"
    assert mixed["curve_status"] == "source_identified_not_digitized"
    assert mixed["allowed_use"] == "sensitivity_only_not_final"
    assert mixed["gas_methane_mol_pct"] == 98


def test_stability_input_capability_matrix_locks_ready_scenario_and_blocked_inputs() -> None:
    matrix = stability_input_capability_matrix_frame()

    methane = matrix.loc[matrix["input_name"] == "100 percent methane phase curve"].iloc[0]
    mixed = matrix.loc[matrix["input_name"] == "Mixed-gas phase curve"].iloc[0]
    approved = matrix.loc[matrix["input_name"] == "Approved logs and core labels"].iloc[0]

    assert methane["capability_status"] == "ready_official_baseline"
    assert "official" in methane["screen_role"].lower()
    assert mixed["capability_status"] == "scenario_candidate_only"
    assert "Do not apply" in mixed["guardrail"]
    assert approved["capability_status"] == "blocked_future_approved_data"
    assert "Do not train" in approved["guardrail"]


def test_committed_stability_input_capability_matrix_matches_contract() -> None:
    project_root = Path(__file__).resolve().parents[1]

    matrix = pd.read_csv(default_stability_input_capability_matrix_path(project_root))

    assert len(matrix) == 11
    assert set(stability_input_capability_matrix_frame().columns) == set(matrix.columns)
    assert "Temperature profiles" in matrix["input_name"].tolist()
    assert "Gas composition" in matrix["input_name"].tolist()


def test_osl_pull_triggers_distinguish_fixture_work_from_real_temperature_products() -> None:
    triggers = stability_osl_pull_triggers_frame()

    fixture = triggers.loc[
        triggers["trigger"] == "Develop temperature-model logic with unit-test fixtures"
    ].iloc[0]
    real_temperature = triggers.loc[
        triggers["trigger"] == "Build real public temperature-model products from G10015 rows"
    ].iloc[0]

    assert fixture["needs_osl"] == "no"
    assert real_temperature["needs_osl"] == "yes"
    assert "raw processed profile rows" in real_temperature["why"]


def test_website_product_spec_keeps_final_screen_claims_bounded() -> None:
    spec = stability_website_product_spec_frame()

    map_view = spec.loc[spec["website_area"] == "Map view"].iloc[0]
    plot_view = spec.loc[spec["website_area"] == "Temperature and phase plot"].iloc[0]
    scenario = spec.loc[spec["website_area"] == "Scenario controls"].iloc[0]

    assert "hydrate occurrence" in map_view["must_not_claim"]
    assert "missing temperature models" in plot_view["must_not_claim"]
    assert "No freeform gas slider" in scenario["must_not_claim"]


def test_committed_osl_and_website_specs_match_contract() -> None:
    project_root = Path(__file__).resolve().parents[1]

    triggers = pd.read_csv(default_stability_osl_pull_triggers_path(project_root))
    website_spec = pd.read_csv(default_stability_website_product_spec_path(project_root))

    assert len(triggers) == len(stability_osl_pull_triggers_frame())
    assert set(triggers.columns) == set(stability_osl_pull_triggers_frame().columns)
    assert len(website_spec) == len(stability_website_product_spec_frame())
    assert set(website_spec.columns) == set(stability_website_product_spec_frame().columns)
    assert "Results table" in website_spec["website_area"].tolist()


def test_committed_phase_curve_lookup_preserves_sir_figure_anchor() -> None:
    project_root = Path(__file__).resolve().parents[1]

    curve = load_methane_phase_curve(project_root)
    west_sak_base_pressure = hydrostatic_pressure_mpa_absolute(741.0)

    assert len(curve) >= 30
    assert curve["pressure_mpa_absolute"].is_monotonic_increasing
    assert set(curve["phase_curve_role"]) == {"baseline"}
    assert set(curve["gas_methane_mol_pct"]) == {100}
    assert 10.0 <= phase_curve_equilibrium_temperature_c(curve, west_sak_base_pressure) <= 11.0


def test_committed_phase_curve_catalog_keeps_baseline_official_and_mixed_gas_pending() -> None:
    project_root = Path(__file__).resolve().parents[1]

    catalog = load_phase_curve_scenario_catalog(project_root)
    baseline = catalog.loc[catalog["phase_curve_id"] == PHASE_CURVE_ID].iloc[0]
    mixed = catalog.loc[
        catalog["phase_curve_id"] == "mixed_gas_collett2011_holder1987_pending"
    ].iloc[0]

    assert baseline["phase_curve_role"] == "baseline"
    assert baseline["curve_status"] == "available_digitized_lookup"
    assert baseline["allowed_use"] == "official_public_baseline"
    assert mixed["phase_curve_role"] == "sensitivity_candidate"
    assert mixed["curve_status"] == "source_identified_not_digitized"
    assert mixed["allowed_use"] == "sensitivity_only_not_final"


def test_load_arctic_slope_public_wells_filters_source_package(tmp_path) -> None:
    make_public_well_package(tmp_path)

    wells = load_arctic_slope_public_wells(tmp_path)

    assert len(wells) == 1
    assert wells.crs.to_epsg() == 4326
    assert wells.iloc[0]["well_name"] == "TEST NORTH SLOPE 1"


def test_build_public_well_stability_context_assigns_science_context(tmp_path) -> None:
    make_public_well_package(tmp_path)
    make_public_snapshot(tmp_path)

    context = build_public_well_stability_context(tmp_path)
    summary = stability_context_summary_frame(context)

    assert len(context) == 1
    row = context.iloc[0]
    assert row["depth_basis"] == "TrueVertic"
    assert row["hydrate_assessment_codes"] == "50010203"
    assert row["nearest_ggd223_code"] == "SYN"
    assert row["well_depth_exceeds_nearest_permafrost_control"]
    assert row["stability_context_flag"] == "public_context_candidate"
    assert summary.loc[summary["metric"] == "Public context candidates", "value"].iloc[0] == 1


def test_write_public_stability_products_creates_csv_outputs(tmp_path) -> None:
    make_public_well_package(tmp_path)
    snapshot = make_public_snapshot(tmp_path)
    make_temperature_profile(snapshot)

    (
        context_path,
        summary_path,
        inventory_path,
        inventory_summary_path,
        scaffold_path,
        scaffold_summary_path,
    ) = write_public_stability_products(tmp_path)

    assert context_path == default_well_context_path(tmp_path)
    assert context_path.exists()
    assert summary_path.exists()
    assert inventory_path is not None
    assert inventory_path.exists()
    assert inventory_summary_path is not None
    assert inventory_summary_path.exists()
    assert scaffold_path is not None
    assert scaffold_path.exists()
    assert scaffold_summary_path is not None
    assert scaffold_summary_path.exists()
    context = pd.read_csv(context_path)
    assert context["well_name"].tolist() == ["TEST NORTH SLOPE 1"]


def test_g10015_temperature_profile_inventory_summarizes_processed_logs(tmp_path) -> None:
    snapshot = make_public_snapshot(tmp_path)
    profile = make_temperature_profile(snapshot)

    parsed = parse_g10015_temperature_profile(profile)
    inventory = build_g10015_temperature_inventory(snapshot)
    summary = temperature_inventory_summary_frame(inventory)

    assert parsed["well_code"] == "SYN"
    assert parsed["well_name"] == "Synthetic Test Well"
    assert parsed["sample_count"] == 4
    assert parsed["max_depth_m"] == 150.0
    assert round(float(parsed["deepest_window_gradient_c_per_100m"]), 2) == 6.0
    assert len(inventory) == 1
    assert summary.loc[summary["metric"] == "G10015 profiles", "value"].iloc[0] == 1


def test_load_g10015_temperature_profile_points_reads_depth_temperature_rows(tmp_path) -> None:
    snapshot = make_public_snapshot(tmp_path)
    profile = make_temperature_profile(snapshot)

    points = load_g10015_temperature_profile_points(profile)

    assert points.columns.tolist() == ["depth_m", "temperature_c"]
    assert points["depth_m"].tolist() == [0.0, 50.0, 100.0, 150.0]
    assert points["temperature_c"].tolist() == [-10.0, -7.0, -4.0, -1.0]


def test_g10015_temperature_profile_points_average_duplicate_depths(tmp_path) -> None:
    source_root = tmp_path
    profile_dir = source_root / "03_temperature_geothermal" / "NSIDC_G10015_extracted"
    profile_dir.mkdir(parents=True)
    profile = profile_dir / "DUP_24JUN14.txt"
    profile.write_text(
        "\n".join(
            [
                "Temperature Log Information:",
                "  Well name:   Duplicate Depth Test Well",
                "  File name:   DUP_24JUN14_c_d",
                "  Log date:    14-JUN-2026",
                "",
                " Depth  Temperature",
                "  0.00  -10.0",
                "  8.23  -9.0",
                "  8.23  -7.0",
                " 50.00  -5.0",
            ]
        ),
        encoding="utf-8",
    )

    points = load_g10015_temperature_profile_points(profile)
    inventory = build_g10015_temperature_inventory(source_root)

    duplicate_row = points.loc[points["depth_m"] == 8.23].iloc[0]
    assert points["depth_m"].tolist() == [0.0, 8.23, 50.0]
    assert duplicate_row["temperature_c"] == -8.0
    assert len(inventory) == 1
    assert inventory.iloc[0]["sample_count"] == 3


def test_g10015_temperature_profile_points_product_samples_public_curves(tmp_path) -> None:
    snapshot = make_public_snapshot(tmp_path)
    make_temperature_profile(snapshot)

    points = build_g10015_temperature_profile_points_product(
        snapshot,
        max_points_per_profile=3,
    )
    summary = g10015_temperature_profile_points_summary_frame(points)

    assert len(points) == 3
    assert points["depth_m"].tolist() == [0.0, 100.0, 150.0]
    assert set(points["sample_method"]) == {"evenly_sampled_max_3_points"}
    assert set(points["public_product_role"]) == {
        "temperature_curve_visualization_only_not_stability_result"
    }
    assert summary.loc[summary["metric"] == "Sampled profile rows", "value"].iloc[0] == 3


def test_write_g10015_temperature_profile_points_product_creates_public_safe_csv(
    tmp_path,
) -> None:
    snapshot = make_public_snapshot(tmp_path)
    make_temperature_profile(snapshot)

    points_path, summary_path = write_g10015_temperature_profile_points_product(
        tmp_path,
        snapshot,
        max_points_per_profile=3,
    )

    assert points_path == default_g10015_profile_points_path(tmp_path)
    assert points_path is not None
    assert points_path.exists()
    assert summary_path == default_g10015_profile_points_summary_path(tmp_path)
    assert summary_path is not None
    assert summary_path.exists()
    points = pd.read_csv(points_path)
    assert len(points) == 3
    assert "stability_top_m" not in points.columns


def test_temperature_model_interpolates_measured_profile() -> None:
    profile_points = pd.DataFrame(
        {
            "depth_m": [0.0, 100.0, 200.0],
            "temperature_c": [-10.0, -4.0, 2.0],
        }
    )

    model = temperature_model_from_profile(profile_points, [50.0, 150.0])

    assert model["temperature_model_c"].tolist() == [-7.0, -1.0]
    assert set(model["temperature_model_method"]) == {"measured_profile_interpolated"}
    assert set(model["temperature_model_status"]) == {"calculated"}
    assert not model["temperature_extrapolated_below_profile"].any()


def test_temperature_model_extrapolates_below_profile_with_gradient() -> None:
    profile_points = pd.DataFrame(
        {
            "depth_m": [0.0, 100.0, 200.0],
            "temperature_c": [-10.0, -4.0, 2.0],
        }
    )

    model = temperature_model_from_profile(profile_points, [250.0], gradient_c_per_100m=6.0)

    row = model.iloc[0]
    assert row["temperature_model_c"] == 5.0
    assert row["temperature_model_method"] == "measured_profile_plus_gradient_extrapolation"
    assert row["temperature_model_status"] == "calculated"
    assert row["temperature_extrapolated_below_profile"]
    assert row["temperature_extrapolation_below_profile_m"] == 50.0


def test_temperature_model_blocks_below_profile_without_gradient() -> None:
    profile_points = pd.DataFrame(
        {
            "depth_m": [0.0, 100.0, 200.0],
            "temperature_c": [-10.0, -4.0, 2.0],
        }
    )

    model = temperature_model_from_profile(profile_points, [250.0])

    row = model.iloc[0]
    assert pd.isna(row["temperature_model_c"])
    assert row["temperature_model_method"] == "blocked_below_profile_no_gradient"
    assert row["temperature_model_status"] == "blocked_below_profile_no_gradient"
    assert not row["temperature_extrapolated_below_profile"]


def test_temperature_model_blocks_empty_profile_and_missing_depth() -> None:
    empty_profile = pd.DataFrame(columns=["depth_m", "temperature_c"])

    model = temperature_model_from_profile(empty_profile, [100.0, pd.NA])

    usable_depth = model.iloc[0]
    missing_depth = model.iloc[1]
    assert pd.isna(usable_depth["temperature_model_c"])
    assert usable_depth["temperature_model_status"] == "blocked_no_temperature_profile"
    assert pd.isna(missing_depth["temperature_model_c"])
    assert missing_depth["temperature_model_status"] == "blocked_missing_depth"


def test_stability_depth_grid_includes_modeled_depth_limit() -> None:
    grid = stability_depth_grid(125.0, step_m=50.0)

    assert grid.tolist() == [0.0, 50.0, 100.0, 125.0]


def test_stability_depth_grid_can_start_at_phase_curve_minimum() -> None:
    grid = stability_depth_grid(225.0, step_m=50.0, start_depth_m=100.0)

    assert grid.tolist() == [100.0, 150.0, 200.0, 225.0]


def test_stability_interval_finds_interpolated_top_and_base() -> None:
    profile_points = pd.DataFrame(
        {
            "depth_m": [0.0, 100.0, 200.0],
            "temperature_c": [5.0, 5.0, 25.0],
        }
    )
    phase_curve = make_linear_phase_curve_from_depth_temperatures(
        [(0.0, 0.0), (100.0, 10.0), (200.0, 20.0)]
    )

    condition_grid = stability_condition_grid_from_profile(
        profile_points,
        phase_curve,
        depth_limit_m=200.0,
        step_m=100.0,
    )
    interval = stability_interval_from_condition_grid(
        condition_grid,
        depth_limit_m=200.0,
        step_m=100.0,
    )

    assert condition_grid["is_stable"].tolist() == [False, True, False]
    assert interval["stability_result_status"] == "calculated"
    assert interval["stability_top_m"] == 50.0
    assert interval["stability_base_m"] == 150.0
    assert interval["stability_thickness_m"] == 100.0
    assert interval["well_penetrated_stability_thickness_m"] == 100.0
    assert interval["top_boundary_method"] == "interpolated_crossing"
    assert interval["base_boundary_method"] == "interpolated_crossing"
    assert "not_hydrate_proof" in interval["caveat_codes"]


def test_stability_interval_marks_open_base_and_extrapolation_caveat() -> None:
    profile_points = pd.DataFrame(
        {
            "depth_m": [0.0, 100.0],
            "temperature_c": [0.0, 0.0],
        }
    )
    phase_curve = make_linear_phase_curve_from_depth_temperatures(
        [(0.0, 0.0), (100.0, 10.0), (200.0, 20.0)]
    )

    condition_grid = stability_condition_grid_from_profile(
        profile_points,
        phase_curve,
        depth_limit_m=200.0,
        gradient_c_per_100m=0.0,
        step_m=100.0,
    )
    interval = stability_interval_from_condition_grid(
        condition_grid,
        depth_limit_m=200.0,
        step_m=100.0,
    )

    assert condition_grid["is_stable"].tolist() == [True, True, True]
    assert interval["stability_result_status"] == "calculated"
    assert interval["stability_top_m"] == 0.0
    assert interval["stability_base_m"] == 200.0
    assert interval["base_boundary_method"] == "open_below_model_depth_limit"
    assert interval["temperature_extrapolated_below_profile"]
    assert interval["temperature_extrapolation_below_profile_m"] == 100.0
    assert "temperature_profile_extrapolated" in interval["caveat_codes"]


def test_stability_interval_blocks_incomplete_pressure_temperature_grid() -> None:
    profile_points = pd.DataFrame(
        {
            "depth_m": [0.0, 100.0],
            "temperature_c": [0.0, 0.0],
        }
    )
    phase_curve = make_linear_phase_curve_from_depth_temperatures(
        [(0.0, 0.0), (100.0, 10.0), (200.0, 20.0)]
    )

    condition_grid = stability_condition_grid_from_profile(
        profile_points,
        phase_curve,
        depth_limit_m=200.0,
        step_m=100.0,
    )
    interval = stability_interval_from_condition_grid(
        condition_grid,
        depth_limit_m=200.0,
        step_m=100.0,
    )

    assert condition_grid["temperature_model_status"].tolist() == [
        "calculated",
        "calculated",
        "blocked_below_profile_no_gradient",
    ]
    assert interval["stability_result_status"] == "blocked_incomplete_pressure_temperature_grid"
    assert pd.isna(interval["stability_top_m"])
    assert pd.isna(interval["stability_base_m"])
    assert "temperature_profile_missing" in interval["caveat_codes"]


def test_stability_source_control_label_assigns_high_medium_low_and_blocked() -> None:
    high = {
        "within_hydrate_assessment_unit": True,
        "depth_basis": "TrueVertic",
        "phase_curve_status": "applied",
        "phase_curve_allowed_use": PHASE_CURVE_ALLOWED_USE,
        "temperature_model_status": "calculated",
        "stability_result_status": "calculated",
        "temperature_control_distance_km": 3.0,
        "temperature_extrapolation_below_profile_m": 0.0,
    }
    medium = high | {
        "temperature_control_distance_km": 20.0,
        "temperature_extrapolation_below_profile_m": 150.0,
    }
    low = high | {
        "depth_basis": "DrillerTot",
        "temperature_control_distance_km": 75.0,
        "temperature_extrapolation_below_profile_m": 300.0,
    }
    blocked = high | {
        "temperature_model_status": "blocked_no_temperature_profile",
    }

    assert stability_source_control_label(high) == "high_source_control"
    assert stability_source_control_label(medium) == "medium_source_control"
    assert stability_source_control_label(low) == "low_source_control"
    assert stability_source_control_label(blocked) == "blocked_missing_inputs"


def test_stability_source_control_label_keeps_outside_au_separate() -> None:
    outside = {
        "within_hydrate_assessment_unit": False,
        "depth_basis": "TrueVertic",
        "phase_curve_status": "applied",
        "temperature_model_status": "calculated",
        "stability_result_status": "calculated",
    }

    assert stability_source_control_label(outside) == "outside_public_au_context"


def test_stability_parameter_readiness_keeps_final_zone_as_pending() -> None:
    readiness = stability_parameter_readiness_frame()

    assert "Hydrate phase curve" in readiness["input"].tolist()
    phase_row = readiness.loc[readiness["input"] == "Hydrate phase curve"].iloc[0]
    assert phase_row["current_status"] == "Ready as digitized lookup"
    assert "USGS SIR 2008-5175" in phase_row["current_source"]
    final_row = readiness.loc[readiness["input"] == "Stability top/base/thickness"].iloc[0]
    assert final_row["current_status"] == "Not calculated yet"
    assert "pressure" in final_row["next_step"].lower()


def test_stability_input_scaffold_links_pressure_and_temperature_without_final_zone(tmp_path) -> None:
    make_public_well_package(tmp_path)
    snapshot = make_public_snapshot(tmp_path)
    make_temperature_profile(snapshot)
    write_public_stability_products(tmp_path)

    scaffold = build_stability_input_scaffold(tmp_path)
    summary = stability_input_scaffold_summary_frame(scaffold)

    assert len(scaffold) == 1
    row = scaffold.iloc[0]
    assert row["nearest_temperature_profile_code"] == "SYN"
    assert row["temperature_profile_link_method"] == "matched_nearest_ggd223_code"
    assert row["phase_curve_status"] == "not_applied"
    assert row["planned_phase_curve_id"] == PHASE_CURVE_ID
    assert row["planned_phase_curve_role"] == PHASE_CURVE_ROLE
    assert row["planned_phase_curve_allowed_use"] == PHASE_CURVE_ALLOWED_USE
    assert row["planned_gas_composition_assumption"] == PHASE_CURVE_GAS_COMPOSITION_ASSUMPTION
    assert row["planned_gas_methane_mol_pct"] == 100.0
    assert row["planned_gas_ethane_mol_pct"] == 0.0
    assert row["planned_gas_propane_mol_pct"] == 0.0
    assert row["planned_salinity_ppt_assumption"] == 5.0
    assert row["stability_top_base_thickness_status"] == "not_calculated"
    assert row["stability_input_readiness"] == "ready_for_phase_curve_inputs"
    assert row["hydrostatic_pressure_mpa_at_depth_basis"] > 0
    assert (
        row["hydrostatic_pressure_mpa_absolute_at_depth_basis"]
        > row["hydrostatic_pressure_mpa_at_depth_basis"]
    )
    assert summary.loc[summary["metric"] == "Final stability results", "value"].iloc[0] == 0


def test_stability_temperature_model_builds_key_depth_rows_from_osl_profiles(tmp_path) -> None:
    make_public_well_package(tmp_path)
    snapshot = make_public_snapshot(tmp_path)
    make_temperature_profile(snapshot)
    write_public_stability_products(tmp_path)

    model = build_stability_temperature_model(tmp_path, snapshot)
    summary = stability_temperature_model_summary_frame(model)

    assert len(model) == 2
    assert set(model["temperature_model_depth_role"]) == {
        "nearest_permafrost_control",
        "depth_basis",
    }
    assert set(model["temperature_model_status"]) == {"calculated"}
    assert model["temperature_extrapolated_below_profile"].all()
    assert set(model["temperature_model_product_role"]) == {
        "temperature_input_only_not_stability_result"
    }
    assert set(model["stability_top_base_thickness_status"]) == {"not_calculated"}
    assert summary.loc[summary["metric"] == "Final stability results", "value"].iloc[0] == 0


def test_write_stability_temperature_model_product_creates_public_safe_csv(tmp_path) -> None:
    make_public_well_package(tmp_path)
    snapshot = make_public_snapshot(tmp_path)
    make_temperature_profile(snapshot)
    write_public_stability_products(tmp_path)

    model_path, summary_path = write_stability_temperature_model_product(tmp_path, snapshot)

    assert model_path == default_stability_temperature_model_path(tmp_path)
    assert model_path is not None
    assert model_path.exists()
    assert summary_path is not None
    assert summary_path.exists()
    model = pd.read_csv(model_path)
    assert len(model) == 2
    assert "stability_top_m" not in model.columns
    assert set(model["stability_top_base_thickness_status"]) == {"not_calculated"}


def test_write_stability_temperature_model_product_requires_raw_profile_rows(tmp_path) -> None:
    snapshot = make_public_snapshot(tmp_path)

    assert write_stability_temperature_model_product(tmp_path, snapshot) == (None, None)


def test_stability_screen_calculates_only_when_all_gates_pass(tmp_path) -> None:
    make_public_well_package(tmp_path)
    snapshot = make_public_snapshot(tmp_path)
    make_temperature_profile(snapshot)
    write_public_stability_products(tmp_path)
    make_broad_phase_curve_lookup(tmp_path)

    screen = build_stability_screen(tmp_path, snapshot, grid_step_m=25.0)
    summary = stability_screen_summary_frame(screen)

    assert len(screen) == 1
    row = screen.iloc[0]
    assert row["phase_curve_status"] == "applied"
    assert row["stability_result_status"] == "calculated"
    assert row["stability_top_m"] == 0.0
    assert 125.0 <= row["stability_base_m"] <= 175.0
    assert row["stability_thickness_m"] > 0
    assert row["stability_confidence"] in {"high_source_control", "medium_source_control"}
    assert "not_hydrate_proof" in row["caveat_codes"]
    assert summary.loc[summary["metric"] == "Calculated stability intervals", "value"].iloc[0] == 1


def test_stability_screen_starts_grid_at_phase_curve_minimum_depth(tmp_path) -> None:
    make_public_well_package(tmp_path)
    snapshot = make_public_snapshot(tmp_path)
    make_temperature_profile(snapshot)
    write_public_stability_products(tmp_path)
    make_phase_curve_with_shallow_gap(tmp_path)

    screen = build_stability_screen(tmp_path, snapshot, grid_step_m=25.0)

    row = screen.iloc[0]
    assert row["phase_curve_status"] == "applied"
    assert row["stability_result_status"] == "calculated"
    assert row["stability_top_m"] >= 100.0
    assert pd.notna(row["stability_base_m"])


def test_stability_screen_blocks_when_phase_curve_range_is_insufficient(tmp_path) -> None:
    make_public_well_package(tmp_path)
    snapshot = make_public_snapshot(tmp_path)
    make_temperature_profile(snapshot)
    write_public_stability_products(tmp_path)
    make_phase_curve_lookup(tmp_path)

    screen = build_stability_screen(tmp_path, snapshot, grid_step_m=25.0)

    row = screen.iloc[0]
    assert row["stability_result_status"] == "blocked_phase_curve_range_insufficient"
    assert row["phase_curve_status"] == "blocked_phase_curve_range_insufficient"
    assert pd.isna(row["stability_top_m"])
    assert pd.isna(row["stability_base_m"])
    assert row["stability_confidence"] == "blocked_missing_inputs"


def test_write_stability_screen_product_requires_raw_profile_rows(tmp_path) -> None:
    snapshot = make_public_snapshot(tmp_path)

    assert write_stability_screen_product(tmp_path, snapshot) == (None, None)


def test_write_stability_screen_product_creates_guarded_public_csv(tmp_path) -> None:
    make_public_well_package(tmp_path)
    snapshot = make_public_snapshot(tmp_path)
    make_temperature_profile(snapshot)
    write_public_stability_products(tmp_path)
    make_broad_phase_curve_lookup(tmp_path)

    screen_path, summary_path = write_stability_screen_product(tmp_path, snapshot)

    assert screen_path == default_stability_screen_path(tmp_path)
    assert screen_path is not None
    assert screen_path.exists()
    assert summary_path is not None
    assert summary_path.exists()
    screen = pd.read_csv(screen_path)
    assert len(screen) == 1
    assert set(screen["stability_result_status"]) == {"calculated"}
    assert "not_hydrate_proof" in screen.iloc[0]["caveat_codes"]


def test_public_ml_feature_scaffold_uses_stability_as_feature_not_label(tmp_path) -> None:
    make_public_well_package(tmp_path)
    snapshot = make_public_snapshot(tmp_path)
    make_temperature_profile(snapshot)
    write_public_stability_products(tmp_path)
    make_broad_phase_curve_lookup(tmp_path)
    write_stability_temperature_model_product(tmp_path, snapshot)
    write_stability_screen_product(tmp_path, snapshot)

    features = build_public_ml_feature_scaffold(tmp_path)
    summary = public_ml_feature_scaffold_summary_frame(features)
    dictionary = public_ml_feature_dictionary_frame()

    assert len(features) == 1
    row = features.iloc[0]
    assert row["public_product_role"] == "public_ml_feature_scaffold_not_training_labels"
    assert row["stability_interval_calculated"]
    assert row["public_ml_feature_readiness"] == "feature_ready_with_calculated_stability_interval"
    assert row["hydrate_occurrence_label_status"] == "not_available_in_public_scaffold"
    assert row["hydrate_saturation_label_status"] == "not_available_in_public_scaffold"
    assert row["ml_training_readiness"] == "not_training_ready_no_validated_hydrate_labels"
    assert "not as hydrate occurrence" in row["label_guardrail"]
    assert summary.loc[summary["metric"] == "Rows training-ready for occurrence/saturation ML", "value"].iloc[0] == 0
    assert set(dictionary["column_name"]) == set(features.columns)
    assert dictionary.loc[
        dictionary["column_name"] == "stability_top_m",
        "prohibited_use",
    ].iloc[0].startswith("Do not use as a hydrate occurrence")


def test_write_public_ml_feature_products_creates_scaffold_dictionary_and_summary(
    tmp_path,
) -> None:
    make_public_well_package(tmp_path)
    snapshot = make_public_snapshot(tmp_path)
    make_temperature_profile(snapshot)
    write_public_stability_products(tmp_path)
    make_broad_phase_curve_lookup(tmp_path)
    write_stability_temperature_model_product(tmp_path, snapshot)
    write_stability_screen_product(tmp_path, snapshot)

    scaffold_path, summary_path, dictionary_path = write_public_ml_feature_products(tmp_path)

    assert scaffold_path == default_public_ml_feature_scaffold_path(tmp_path)
    assert summary_path == default_public_ml_feature_scaffold_summary_path(tmp_path)
    assert dictionary_path == default_public_ml_feature_dictionary_path(tmp_path)
    assert scaffold_path.exists()
    assert summary_path.exists()
    assert dictionary_path.exists()
    scaffold = pd.read_csv(scaffold_path)
    assert len(scaffold) == 1
    assert "hydrate_present" not in scaffold.columns
    assert scaffold["allowed_ml_use"].eq("feature_engineering_and_coverage_readiness_only").all()


def test_public_ml_target_registry_marks_saturation_family_as_targets() -> None:
    registry = public_ml_target_registry_frame()
    guardrails = public_ml_leakage_guardrails_frame()

    expected_targets = {
        "Sgh",
        "S_h",
        "Sh",
        "NMR_SAT",
        "Hydrate Saturation",
        "Swr",
        "S_wr",
    }
    assert expected_targets.issubset(set(registry["original_header"]))
    saturation_rows = registry[registry["original_header"].isin(expected_targets)]
    assert saturation_rows["prohibited_use"].str.contains("input feature").all()
    assert saturation_rows["leakage_policy"].str.contains(
        "exclude|exclude_until",
        regex=True,
    ).all()
    assert registry.loc[
        registry["original_header"] == "NMR_SAT",
        "notes",
    ].iloc[0] == "NMRPHI can be an input if measured; NMR_SAT is target-only."
    assert guardrails["blocked_inputs"].str.contains("Sgh").any()
    assert guardrails["rule"].str.contains("Do not derive predictor features").any()


def test_write_public_ml_target_registry_products_creates_public_policy_csvs(
    tmp_path,
) -> None:
    registry_path, guardrails_path = write_public_ml_target_registry_products(tmp_path)

    assert registry_path == default_public_ml_target_registry_path(tmp_path)
    assert guardrails_path == default_public_ml_leakage_guardrails_path(tmp_path)
    assert registry_path.exists()
    assert guardrails_path.exists()
    registry = pd.read_csv(registry_path)
    guardrails = pd.read_csv(guardrails_path)
    assert "Sgh" in registry["original_header"].tolist()
    assert "Hydrate Saturation" in registry["original_header"].tolist()
    assert guardrails["guardrail_id"].tolist() == ["LG-01", "LG-02", "LG-03", "LG-04", "LG-05"]


def test_committed_stability_screen_preserves_guardrails() -> None:
    project_root = Path(__file__).resolve().parents[1]
    screen = pd.read_csv(default_stability_screen_path(project_root))

    assert len(screen) == 8084
    status_counts = screen["stability_result_status"].value_counts().to_dict()
    assert status_counts["calculated"] == 22
    assert status_counts["calculated_no_stable_interval"] == 8
    assert status_counts["blocked_missing_temperature_profile"] == 7113
    assert status_counts["blocked_missing_depth"] == 505
    assert status_counts["blocked_phase_curve_range_insufficient"] == 344
    assert status_counts["outside_au_context"] == 92

    blocked = ~screen["stability_result_status"].isin(
        ["calculated", "calculated_no_stable_interval"]
    )
    protected_columns = ["stability_top_m", "stability_base_m", "stability_thickness_m"]
    assert screen.loc[blocked, protected_columns].isna().all().all()
    assert screen["caveat_codes"].fillna("").str.contains("not_hydrate_proof").all()

    calculated = screen.loc[screen["stability_result_status"].eq("calculated")]
    assert calculated[protected_columns].notna().all().all()
    assert (calculated["stability_thickness_m"] > 0).all()


def test_committed_stability_screen_summary_matches_screen_counts() -> None:
    project_root = Path(__file__).resolve().parents[1]
    screen = pd.read_csv(default_stability_screen_path(project_root))
    summary = pd.read_csv(default_stability_screen_summary_path(project_root))
    values = summary.set_index("metric")["value"].astype(int).to_dict()

    calculated = screen["stability_result_status"].eq("calculated")
    no_interval = screen["stability_result_status"].eq("calculated_no_stable_interval")
    blocked = ~(calculated | no_interval)

    assert values["Screen rows"] == len(screen)
    assert values["Calculated stability intervals"] == int(calculated.sum())
    assert values["No stable interval found"] == int(no_interval.sum())
    assert values["Blocked rows"] == int(blocked.sum())
    assert values["Not hydrate proof"] == len(screen)


def test_committed_public_ml_feature_scaffold_preserves_label_guardrails() -> None:
    project_root = Path(__file__).resolve().parents[1]
    features = pd.read_csv(default_public_ml_feature_scaffold_path(project_root))
    dictionary = pd.read_csv(default_public_ml_feature_dictionary_path(project_root))

    assert len(features) == 8084
    assert set(dictionary["column_name"]) == set(features.columns)
    assert features["temperature_profile_matched"].sum() == 483
    assert features["stability_interval_calculated"].sum() == 22
    assert features["no_stable_interval_under_baseline"].sum() == 8
    assert features["hydrate_occurrence_label_status"].eq(
        "not_available_in_public_scaffold"
    ).all()
    assert features["hydrate_saturation_label_status"].eq(
        "not_available_in_public_scaffold"
    ).all()
    assert features["ml_training_readiness"].eq(
        "not_training_ready_no_validated_hydrate_labels"
    ).all()


def test_committed_public_ml_target_registry_preserves_target_only_rule() -> None:
    project_root = Path(__file__).resolve().parents[1]
    registry = pd.read_csv(default_public_ml_target_registry_path(project_root))
    guardrails = pd.read_csv(default_public_ml_leakage_guardrails_path(project_root))

    expected_targets = {
        "Sgh",
        "S_h",
        "Sh",
        "NMR_SAT",
        "Hydrate Saturation",
        "Swr",
        "S_wr",
        "interpreted phase label",
    }
    assert set(registry["original_header"]) == expected_targets
    assert registry["prohibited_use"].str.contains("input feature|predictor", regex=True).all()
    assert guardrails["guardrail_id"].tolist() == ["LG-01", "LG-02", "LG-03", "LG-04", "LG-05"]
    assert guardrails["blocked_inputs"].str.contains("Sgh").any()


def test_committed_approved_schema_coverage_matrix_preserves_roles_and_leakage() -> None:
    project_root = Path(__file__).resolve().parents[1]
    matrix = load_approved_schema_coverage_matrix(project_root)

    expected_headers = {
        "DEPTH",
        "True Depth",
        "Depth_ft",
        "DEPT",
        "Rho_b",
        "RHOB",
        "Density_gpcc",
        "Phi_porosity",
        "phi_den",
        "DPHI",
        "NMRPHI",
        "phi_nmr",
        "caliper",
        "CAL1",
        "differential caliper",
        "Rt",
        "RES",
        "AO90",
        "GR",
        "Vs",
        "VS1",
        "Vp",
        "VELP",
        "Ratio Vp/Vs",
        "impedance",
        "Sgh",
        "S_h",
        "Sh",
        "NMR_SAT",
        "Hydrate Saturation",
        "Swr",
        "S_wr",
        "interpreted phase labels",
    }
    expected_roles = {
        "measured_input",
        "derived_feature",
        "qc_field",
        "target_only",
        "calibration_reference",
        "context_feature",
        "unresolved",
    }

    assert default_approved_schema_coverage_matrix_path(project_root).exists()
    assert matrix.columns.tolist() == APPROVED_SCHEMA_COVERAGE_MATRIX_COLUMNS
    assert expected_headers.issubset(set(matrix["original_header"]))
    assert expected_roles.issubset(set(matrix["role"]))
    assert {"well_name", "target_value", "raw_value"}.isdisjoint(matrix.columns)

    target_rows = matrix[matrix["role"].isin(["target_only", "calibration_reference"])]
    assert target_rows["leakage_risk"].eq("high").all()
    assert target_rows["prohibited_use"].str.contains(
        "predictor|feature matrix|input",
        case=False,
        regex=True,
    ).all()


def test_public_stability_product_runner_has_help() -> None:
    result = subprocess.run(
        [sys.executable, "01_pipeline/build_public_stability_products.py", "--help"],
        capture_output=True,
        check=True,
        text=True,
    )

    assert "--source-root" in result.stdout
