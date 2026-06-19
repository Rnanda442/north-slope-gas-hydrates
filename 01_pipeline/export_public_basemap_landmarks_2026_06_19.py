from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LANDMARK_DIR_NAME = "basemap_landmarks_2026_06_18"
DEFAULT_SOURCE_DIR = ROOT / "data" / "source_library" / LANDMARK_DIR_NAME
DEFAULT_OUTPUT_DIR = ROOT / "data" / "public_gis_products" / LANDMARK_DIR_NAME

BBOX = {
    "min_lon": -157.5,
    "max_lon": -144.5,
    "min_lat": 68.5,
    "max_lat": 71.7,
}

LAYER_SPECS = {
    "units": {
        "source": "alaska_dnr_unit_boundary_current_north_slope_clip.geojson",
        "output": "alaska_dnr_unit_boundary_current_north_slope_clip.geojson",
        "keep_properties": [
            "UnitName",
            "UNIT_NAME",
            "Unit_Name",
            "NAME",
            "Name",
            "OBJECTID",
        ],
        "required": True,
    },
    "roads": {
        "source": "alaska_akdot_roads_north_slope_clip.geojson",
        "output": "alaska_akdot_roads_north_slope_clip.geojson",
        "keep_properties": [
            "Route_Name",
            "Route_Name_Unique",
            "Route_Name_Desc_1",
            "Route_Name_Desc_2",
            "Route_ID",
            "OBJECTID",
        ],
        "required": True,
    },
    "pipeline": {
        "source": "alaska_dnr_trans_alaska_pipeline.geojson",
        "output": "alaska_dnr_trans_alaska_pipeline.geojson",
        "keep_properties": ["Name", "NAME", "OBJECTID"],
        "required": True,
    },
    "gnis_places": {
        "source": "usgs_gnis_places_north_slope_clip.geojson",
        "output": "usgs_gnis_places_north_slope_clip.geojson",
        "keep_properties": ["gaz_name", "FEATURE_NAME", "NAME", "Name", "OBJECTID"],
        "required": True,
    },
}

CENSUS_PLACES_ZIP = "census_tiger_2025_alaska_places.zip"
CENSUS_PLACES_OUTPUT = "census_tiger_2025_alaska_places_north_slope_clip.geojson"


def load_feature_collection(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("type") != "FeatureCollection":
        raise ValueError(f"{path} is not a GeoJSON FeatureCollection")
    return payload


def geometry_coordinate_paths(geometry: dict[str, Any]) -> list[list[list[float]]]:
    geometry_type = geometry.get("type")
    coordinates = geometry.get("coordinates")
    if not coordinates:
        return []
    if geometry_type == "Point":
        return [[coordinates]]
    if geometry_type == "MultiPoint":
        return [[point] for point in coordinates]
    if geometry_type == "LineString":
        return [coordinates]
    if geometry_type == "MultiLineString":
        return list(coordinates)
    if geometry_type == "Polygon":
        return list(coordinates)
    if geometry_type == "MultiPolygon":
        return [ring for polygon in coordinates for ring in polygon]
    return []


def point_inside_bbox(point: list[float], pad: float = 0.25) -> bool:
    if not isinstance(point, list | tuple) or len(point) < 2:
        return False
    try:
        lon = float(point[0])
        lat = float(point[1])
    except (TypeError, ValueError):
        return False
    return (
        BBOX["min_lon"] - pad <= lon <= BBOX["max_lon"] + pad
        and BBOX["min_lat"] - pad <= lat <= BBOX["max_lat"] + pad
    )


def geometry_intersects_bbox(geometry: dict[str, Any]) -> bool:
    return any(
        point_inside_bbox(point)
        for path in geometry_coordinate_paths(geometry)
        for point in path
    )


def sanitize_feature(feature: dict[str, Any], keep_properties: list[str]) -> dict[str, Any] | None:
    geometry = feature.get("geometry")
    if not isinstance(geometry, dict) or not geometry_intersects_bbox(geometry):
        return None
    properties = feature.get("properties", {}) or {}
    clean_properties = {
        key: properties.get(key)
        for key in keep_properties
        if properties.get(key) not in (None, "")
    }
    return {
        "type": "Feature",
        "properties": clean_properties,
        "geometry": geometry,
    }


def write_feature_collection(path: Path, features: list[dict[str, Any]]) -> None:
    path.write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "features": features,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def export_geojson_layer(
    source_dir: Path,
    output_dir: Path,
    layer_name: str,
    spec: dict[str, Any],
) -> dict[str, Any]:
    source_path = source_dir / spec["source"]
    output_path = output_dir / spec["output"]
    if not source_path.exists():
        if spec["required"]:
            raise FileNotFoundError(f"Missing required public source layer: {source_path}")
        return {
            "layer": layer_name,
            "source": str(source_path),
            "output": str(output_path),
            "features": 0,
            "status": "missing optional source",
        }

    payload = load_feature_collection(source_path)
    features = [
        clean_feature
        for feature in payload.get("features", [])
        if isinstance(feature, dict)
        for clean_feature in [sanitize_feature(feature, spec["keep_properties"])]
        if clean_feature is not None
    ]
    write_feature_collection(output_path, features)
    return {
        "layer": layer_name,
        "source": str(source_path),
        "output": str(output_path),
        "features": len(features),
        "status": "exported",
    }


def clean_label(value: object) -> str:
    return " ".join(str(value or "").replace("City of ", "").strip().split())


def export_census_place_points(source_dir: Path, output_dir: Path) -> dict[str, Any]:
    source_path = source_dir / CENSUS_PLACES_ZIP
    output_path = output_dir / CENSUS_PLACES_OUTPUT
    if not source_path.exists():
        return {
            "layer": "census_places",
            "source": str(source_path),
            "output": str(output_path),
            "features": 0,
            "status": "missing optional source",
        }

    try:
        import geopandas as gpd
    except Exception as exc:
        return {
            "layer": "census_places",
            "source": str(source_path),
            "output": str(output_path),
            "features": 0,
            "status": f"skipped; geopandas unavailable: {exc}",
        }

    places = gpd.read_file(f"zip://{source_path.resolve()}")
    if places.crs is not None and places.crs.to_epsg() != 4326:
        places = places.to_crs("EPSG:4326")

    features: list[dict[str, Any]] = []
    for _, row in places.iterrows():
        label = clean_label(row.get("NAME") or row.get("NAMELSAD"))
        if not label:
            continue
        try:
            lat = float(row.get("INTPTLAT"))
            lon = float(row.get("INTPTLON"))
        except (TypeError, ValueError):
            centroid = row.geometry.centroid if row.geometry is not None else None
            if centroid is None:
                continue
            lon = float(centroid.x)
            lat = float(centroid.y)
        if not point_inside_bbox([lon, lat], pad=0):
            continue
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "label": label,
                    "lat": lat,
                    "lon": lon,
                    "source": "US Census TIGER/Line Alaska Places",
                },
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
            }
        )

    write_feature_collection(output_path, features)
    return {
        "layer": "census_places",
        "source": str(source_path),
        "output": str(output_path),
        "features": len(features),
        "status": "exported",
    }


def write_bundle_readme(output_dir: Path, manifest: dict[str, Any]) -> None:
    lines = [
        "# Public Basemap Landmark Bundle",
        "",
        "Generated from public OSL-staged GIS layers for the interactive North Slope website map.",
        "",
        "Guardrails:",
        "- Public geospatial context only.",
        "- No approved DOE rows, private workbooks, well-log attachments, row-level predictions, trained models, or fitted scalers.",
        "- Website use is orientation/context only; these layers do not prove hydrate occurrence, saturation, producibility, or ML results.",
        "",
        "Files:",
    ]
    for layer in manifest["layers"]:
        lines.append(f"- `{Path(layer['output']).name}`: {layer['features']} features, {layer['status']}")
    lines.extend(
        [
            "",
            "The website prefers this tracked bundle for the interactive layer map.",
            "The raw source package remains in `data/source_library/` or OSL/Drive and is not required at website runtime.",
            "",
        ]
    )
    output_dir.joinpath("README.md").write_text("\n".join(lines), encoding="utf-8")


def export_bundle(source_dir: Path, output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    layer_results = [
        export_geojson_layer(source_dir, output_dir, layer_name, spec)
        for layer_name, spec in LAYER_SPECS.items()
    ]
    layer_results.append(export_census_place_points(source_dir, output_dir))

    manifest = {
        "bundle_id": LANDMARK_DIR_NAME,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_dir": str(source_dir),
        "output_dir": str(output_dir),
        "bbox": BBOX,
        "layers": layer_results,
        "guardrails": [
            "public geospatial context only",
            "no approved rows",
            "no private workbooks",
            "no row-level predictions",
            "no trained models or fitted scalers",
            "not hydrate occurrence or saturation evidence",
        ],
    }
    output_dir.joinpath("manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_bundle_readme(output_dir, manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export a public-safe interactive basemap bundle from OSL-staged GIS layers."
    )
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest = export_bundle(args.source_dir, args.output_dir)
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
