from __future__ import annotations

import json

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon

from dashboard.stability_products import (
    build_public_well_stability_context,
    default_well_context_path,
    load_arctic_slope_public_wells,
    stability_context_summary_frame,
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
    make_public_snapshot(tmp_path)

    context_path, summary_path = write_public_stability_products(tmp_path)

    assert context_path == default_well_context_path(tmp_path)
    assert context_path.exists()
    assert summary_path.exists()
    context = pd.read_csv(context_path)
    assert context["well_name"].tolist() == ["TEST NORTH SLOPE 1"]
