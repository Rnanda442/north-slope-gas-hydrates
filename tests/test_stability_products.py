from __future__ import annotations

import json

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon

from dashboard.stability_products import (
    build_g10015_temperature_inventory,
    build_public_well_stability_context,
    default_well_context_path,
    load_arctic_slope_public_wells,
    parse_g10015_temperature_profile,
    stability_context_summary_frame,
    temperature_inventory_summary_frame,
    write_public_stability_products,
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

    context_path, summary_path, inventory_path, inventory_summary_path = write_public_stability_products(
        tmp_path
    )

    assert context_path == default_well_context_path(tmp_path)
    assert context_path.exists()
    assert summary_path.exists()
    assert inventory_path is not None
    assert inventory_path.exists()
    assert inventory_summary_path is not None
    assert inventory_summary_path.exists()
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
