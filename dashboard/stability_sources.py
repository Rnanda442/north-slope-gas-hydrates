from __future__ import annotations

import os
import re
from pathlib import Path

import geopandas as gpd
import pandas as pd


BUNDLE_DIR_NAME = "north_slope_stability_sources_2026-06-13"

SOURCE_ITEMS = [
    {
        "Item": "Alaska DNR well package",
        "Relative path": "01_wells_public/Well_Bottom_Hole_Location",
        "Stability use": "Well locations and public depth fields.",
    },
    {
        "Item": "USGS OM-222 permafrost plate",
        "Relative path": "02_permafrost_base/USGS_OM222_base_deepest_ice_bearing_permafrost_plate.pdf",
        "Stability use": "Base of deepest ice-bearing permafrost source evidence.",
    },
    {
        "Item": "NSIDC G10015 borehole temperatures",
        "Relative path": "03_temperature_geothermal/NSIDC_G10015_extracted",
        "Stability use": "Temperature-profile and geothermal-gradient context.",
    },
    {
        "Item": "NSIDC GGD223 permafrost controls",
        "Relative path": "03_temperature_geothermal/NSIDC_GGD223_raw_ftp/stnlist.dat",
        "Stability use": "Point permafrost-depth controls with pf_depth in meters.",
    },
    {
        "Item": "USGS gas hydrate assessment units",
        "Relative path": "04_hydrate_assessment_units/GasHydrateAUs.geojson",
        "Stability use": "Regional hydrate assessment unit overlay.",
    },
    {
        "Item": "USGS SIR 2008-5175 method source",
        "Relative path": "05_stability_method_phase/USGS_SIR_2008_5175_gas_hydrate_prospects_north_slope.pdf",
        "Stability use": "North Slope stability/prospect method framing.",
    },
    {
        "Item": "Source ledger",
        "Relative path": "source_ledger.csv",
        "Stability use": "File-level provenance and intended use.",
    },
]

GGD223_ROW_RE = re.compile(
    r"^(?P<well>.+?)\s{2,}"
    r"(?P<code>[A-Z0-9]+)\s+"
    r"(?P<lat_deg>\d{1,2})\s+"
    r"(?P<lat_min>\d{1,2})\s+"
    r"(?P<lat_sec>\d+(?:\.\d+)?)\s+"
    r"(?P<lat_hem>[NS])\s+"
    r"(?P<lon_deg>\d{1,3})\s+"
    r"(?P<lon_min>\d{1,2})\s+"
    r"(?P<lon_sec>\d+(?:\.\d+)?)\s+"
    r"(?P<lon_hem>[EW])\s+"
    r"(?P<elev>-?\d+)\s+"
    r"(?P<pf_depth>-?\d+)\s*$"
)


def default_stability_bundle_path(project_root: Path) -> Path:
    configured = os.environ.get("NORTH_SLOPE_STABILITY_SOURCE_DIR")
    if configured:
        return Path(configured).expanduser()
    return project_root / "data" / "source_library" / BUNDLE_DIR_NAME


def stability_source_status_frame(bundle_root: Path) -> pd.DataFrame:
    root = Path(bundle_root)
    rows = []
    for item in SOURCE_ITEMS:
        path = root / item["Relative path"]
        file_count = 0
        if path.is_file():
            status = "Ready"
            file_count = 1
        elif path.is_dir():
            status = "Ready"
            file_count = sum(1 for child in path.rglob("*") if child.is_file())
        else:
            status = "Missing"
        rows.append(
            {
                **item,
                "Status": status,
                "Files": file_count,
            }
        )
    return pd.DataFrame(rows)


def _empty_geodataframe(columns: list[str]) -> gpd.GeoDataFrame:
    geometry = gpd.GeoSeries([], crs="EPSG:4326")
    return gpd.GeoDataFrame(columns=columns + ["geometry"], geometry=geometry, crs="EPSG:4326")


def _dms_to_decimal(degrees: str, minutes: str, seconds: str, hemisphere: str) -> float:
    value = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
    if hemisphere in {"S", "W"}:
        value *= -1
    return value


def load_ggd223_permafrost_points(bundle_root: Path) -> gpd.GeoDataFrame:
    columns = [
        "well_designation",
        "code",
        "latitude",
        "longitude",
        "elevation_m",
        "permafrost_depth_m",
        "source",
    ]
    path = (
        Path(bundle_root)
        / "03_temperature_geothermal"
        / "NSIDC_GGD223_raw_ftp"
        / "stnlist.dat"
    )
    if not path.exists():
        return _empty_geodataframe(columns)

    records = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = GGD223_ROW_RE.match(line.rstrip())
        if not match:
            continue
        groups = match.groupdict()
        latitude = _dms_to_decimal(
            groups["lat_deg"],
            groups["lat_min"],
            groups["lat_sec"],
            groups["lat_hem"],
        )
        longitude = _dms_to_decimal(
            groups["lon_deg"],
            groups["lon_min"],
            groups["lon_sec"],
            groups["lon_hem"],
        )
        records.append(
            {
                "well_designation": groups["well"].strip(),
                "code": groups["code"],
                "latitude": latitude,
                "longitude": longitude,
                "elevation_m": int(groups["elev"]),
                "permafrost_depth_m": int(groups["pf_depth"]),
                "source": "NSIDC GGD223 stnlist.dat",
            }
        )

    if not records:
        return _empty_geodataframe(columns)
    frame = pd.DataFrame(records)
    return gpd.GeoDataFrame(
        frame,
        geometry=gpd.points_from_xy(frame["longitude"], frame["latitude"]),
        crs="EPSG:4326",
    )


def load_hydrate_assessment_units(bundle_root: Path) -> gpd.GeoDataFrame:
    columns = ["ASSESSCODE", "ASSESSNAME", "geometry"]
    path = Path(bundle_root) / "04_hydrate_assessment_units" / "GasHydrateAUs.geojson"
    if not path.exists():
        return _empty_geodataframe(columns[:-1])
    try:
        units = gpd.read_file(path)
    except Exception:
        return _empty_geodataframe(columns[:-1])
    if units.empty:
        return _empty_geodataframe(columns[:-1])
    if units.crs is None:
        units = units.set_crs("EPSG:4326")
    else:
        units = units.to_crs("EPSG:4326")
    return units


def stability_bundle_metrics(bundle_root: Path) -> dict[str, object]:
    root = Path(bundle_root)
    status = stability_source_status_frame(root)
    permafrost_points = load_ggd223_permafrost_points(root)
    assessment_units = load_hydrate_assessment_units(root)
    g10015_dir = root / "03_temperature_geothermal" / "NSIDC_G10015_extracted"
    well_dir = root / "01_wells_public" / "Well_Bottom_Hole_Location"

    return {
        "Bundle": "Found" if root.exists() else "Missing",
        "Ready source items": int((status["Status"] == "Ready").sum()),
        "Total source items": int(len(status)),
        "GGD223 controls": int(len(permafrost_points)),
        "G10015 profiles": int(len(list(g10015_dir.glob("*.txt"))) if g10015_dir.exists() else 0),
        "Hydrate AUs": int(len(assessment_units)),
        "Well package files": int(len(list(well_dir.glob("*"))) if well_dir.exists() else 0),
    }
