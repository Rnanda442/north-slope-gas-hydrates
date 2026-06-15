from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon

from dashboard.stability_products import (
    PHASE_CURVE_ALLOWED_USE,
    PHASE_CURVE_GAS_COMPOSITION_ASSUMPTION,
    PHASE_CURVE_ID,
    PHASE_CURVE_ROLE,
    build_g10015_temperature_inventory,
    build_public_well_stability_context,
    build_stability_input_scaffold,
    build_stability_temperature_model,
    default_phase_curve_path,
    default_phase_curve_scenario_catalog_path,
    default_stability_temperature_model_path,
    default_stability_input_capability_matrix_path,
    default_stability_osl_pull_triggers_path,
    default_stability_website_product_spec_path,
    default_well_context_path,
    hydrostatic_pressure_mpa_absolute,
    hydrostatic_pressure_mpa_gauge,
    load_arctic_slope_public_wells,
    load_g10015_temperature_profile_points,
    load_phase_curve,
    load_phase_curve_scenario_catalog,
    load_methane_phase_curve,
    parse_g10015_temperature_profile,
    phase_curve_equilibrium_temperature_c,
    stability_input_capability_matrix_frame,
    stability_condition_grid_from_profile,
    stability_osl_pull_triggers_frame,
    stability_parameter_readiness_frame,
    stability_context_summary_frame,
    stability_depth_grid,
    stability_interval_from_condition_grid,
    stability_input_scaffold_summary_frame,
    stability_temperature_model_summary_frame,
    stability_website_product_spec_frame,
    stability_source_control_label,
    temperature_model_from_profile,
    temperature_inventory_summary_frame,
    write_public_stability_products,
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
    product_dir.mkdir(parents=True)
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


def make_phase_curve_scenario_catalog(project_root):
    product_dir = project_root / "data" / "public_stability_products"
    product_dir.mkdir(parents=True)
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


def test_public_stability_product_runner_has_help() -> None:
    result = subprocess.run(
        [sys.executable, "01_pipeline/build_public_stability_products.py", "--help"],
        capture_output=True,
        check=True,
        text=True,
    )

    assert "--source-root" in result.stdout
