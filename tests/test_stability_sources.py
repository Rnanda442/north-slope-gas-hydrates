from __future__ import annotations

import json

from streamlit.testing.v1 import AppTest

from dashboard.stability_sources import (
    active_stability_source_path,
    default_stability_bundle_path,
    default_stability_snapshot_path,
    load_ggd223_permafrost_points,
    load_hydrate_assessment_units,
    stability_bundle_metrics,
    stability_source_kind,
    stability_source_status_frame,
)


def make_stability_bundle(tmp_path):
    bundle = tmp_path / "north_slope_stability_sources_2026-06-13"
    ggd223 = bundle / "03_temperature_geothermal" / "NSIDC_GGD223_raw_ftp"
    ggd223.mkdir(parents=True)
    (ggd223 / "stnlist.dat").write_text(
        "\n".join(
            [
                "Table 1: Permafrost depths from wells with multiple temperature logs.",
                "Well Designation    Code    Latitude        Longitude   Elev pf_depth",
                "Atigaru             ATI   70 33 22.03 N  151 43 01.85 W    2   405",
                "Canning River A-1   CNR   69 36 00    N  146 21 30    W  282   280",
            ]
        ),
        encoding="utf-8",
    )

    au_dir = bundle / "04_hydrate_assessment_units"
    au_dir.mkdir(parents=True)
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "ASSESSCODE": "50010203",
                    "ASSESSNAME": "Nanushuk Formation Gas Hydrate",
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [-151.0, 70.0],
                            [-150.0, 70.0],
                            [-150.0, 71.0],
                            [-151.0, 71.0],
                            [-151.0, 70.0],
                        ]
                    ],
                },
            }
        ],
    }
    (au_dir / "GasHydrateAUs.geojson").write_text(json.dumps(geojson), encoding="utf-8")

    (bundle / "01_wells_public" / "Well_Bottom_Hole_Location").mkdir(parents=True)
    (bundle / "02_permafrost_base").mkdir()
    (bundle / "03_temperature_geothermal" / "NSIDC_G10015_extracted").mkdir()
    (bundle / "03_temperature_geothermal" / "NSIDC_G10015_extracted" / "ATI_02AUG16a.txt").write_text(
        "depth temperature\n",
        encoding="utf-8",
    )
    (bundle / "05_stability_method_phase").mkdir()
    (bundle / "source_ledger.csv").write_text("category,file_name\n", encoding="utf-8")
    return bundle


def make_public_snapshot(tmp_path):
    snapshot = tmp_path / "data" / "public_stability_snapshot" / "north_slope_stability_snapshot_2026-06-13"
    snapshot.mkdir(parents=True)
    (snapshot / "ggd223_permafrost_controls.csv").write_text(
        "\n".join(
            [
                "well_designation,code,latitude,longitude,elevation_m,permafrost_depth_m,source",
                "Atigaru,ATI,70.55611944444445,-151.71718055555556,2,405,NSIDC GGD223 stnlist.dat",
            ]
        ),
        encoding="utf-8",
    )
    (snapshot / "GasHydrateAUs.geojson").write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {
                            "ASSESSCODE": "50010203",
                            "ASSESSNAME": "Nanushuk Formation Gas Hydrate",
                        },
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [
                                    [-151.0, 70.0],
                                    [-150.0, 70.0],
                                    [-150.0, 71.0],
                                    [-151.0, 71.0],
                                    [-151.0, 70.0],
                                ]
                            ],
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (snapshot / "README.md").write_text("public snapshot\n", encoding="utf-8")
    return snapshot


def test_default_stability_bundle_path_uses_project_source_library(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("NORTH_SLOPE_STABILITY_SOURCE_DIR", raising=False)

    assert default_stability_bundle_path(tmp_path) == (
        tmp_path / "data" / "source_library" / "north_slope_stability_sources_2026-06-13"
    )


def test_active_stability_source_path_falls_back_to_public_snapshot(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("NORTH_SLOPE_STABILITY_SOURCE_DIR", raising=False)
    snapshot = make_public_snapshot(tmp_path)

    assert default_stability_snapshot_path(tmp_path) == snapshot
    assert active_stability_source_path(tmp_path) == snapshot
    assert stability_source_kind(snapshot) == "Public snapshot"


def test_ggd223_stnlist_parser_returns_permafrost_control_points(tmp_path) -> None:
    bundle = make_stability_bundle(tmp_path)
    controls = load_ggd223_permafrost_points(bundle)

    assert len(controls) == 2
    assert controls.crs.to_epsg() == 4326
    atigaru = controls.loc[controls["code"] == "ATI"].iloc[0]
    assert atigaru["well_designation"] == "Atigaru"
    assert round(float(atigaru["latitude"]), 4) == 70.5561
    assert round(float(atigaru["longitude"]), 4) == -151.7172
    assert int(atigaru["permafrost_depth_m"]) == 405


def test_hydrate_assessment_units_load_as_geodataframe(tmp_path) -> None:
    bundle = make_stability_bundle(tmp_path)
    units = load_hydrate_assessment_units(bundle)

    assert len(units) == 1
    assert units.crs.to_epsg() == 4326
    assert units.iloc[0]["ASSESSNAME"] == "Nanushuk Formation Gas Hydrate"


def test_stability_source_status_and_metrics_are_source_aware(tmp_path) -> None:
    bundle = make_stability_bundle(tmp_path)
    status = stability_source_status_frame(bundle)
    metrics = stability_bundle_metrics(bundle)

    assert "NSIDC GGD223 permafrost controls" in status["Item"].tolist()
    assert metrics["Bundle"] == "Full local bundle"
    assert metrics["GGD223 controls"] == 2
    assert metrics["G10015 profiles"] == 1
    assert metrics["Hydrate AUs"] == 1


def test_public_snapshot_loads_mappable_stability_layers(tmp_path) -> None:
    snapshot = make_public_snapshot(tmp_path)
    status = stability_source_status_frame(snapshot)
    metrics = stability_bundle_metrics(snapshot)
    controls = load_ggd223_permafrost_points(snapshot)
    units = load_hydrate_assessment_units(snapshot)

    assert status["Status"].tolist() == ["Ready", "Ready", "Ready"]
    assert metrics["Bundle"] == "Public snapshot"
    assert metrics["GGD223 controls"] == 1
    assert metrics["Hydrate AUs"] == 1
    assert len(controls) == 1
    assert len(units) == 1


def test_explore_page_renders_stability_source_panel(monkeypatch) -> None:
    monkeypatch.delenv("NORTH_SLOPE_STABILITY_SOURCE_DIR", raising=False)
    app = AppTest.from_file("streamlit_app.py", default_timeout=45)
    app.query_params["page"] = "Explore North Slope"
    app.run(timeout=45)

    assert not app.exception
    assert "Explore North Slope" in [title.value for title in app.title]
    metric_labels = [metric.label for metric in app.metric]
    assert "Source items" in metric_labels
    assert "GGD223 controls" in metric_labels
    assert "Hydrate AUs" in metric_labels
