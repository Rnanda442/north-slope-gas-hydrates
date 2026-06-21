from __future__ import annotations

from pathlib import Path
import tempfile
import urllib.request

import geopandas as gpd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "data" / "public_gis_products"
OUTPUT_GEOJSON = OUTPUT_DIR / "north_slope_borough_boundary_tiger2025.geojson"

TIGER_2025_COUNTY_URL = (
    "https://www2.census.gov/geo/tiger/TIGER2025/COUNTY/tl_2025_us_county.zip"
)


def build_boundary(output_path: Path = OUTPUT_GEOJSON) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="north_slope_tiger_county_") as tmp_dir:
        zip_path = Path(tmp_dir) / "tl_2025_us_county.zip"
        urllib.request.urlretrieve(TIGER_2025_COUNTY_URL, zip_path)
        counties = gpd.read_file(f"zip://{zip_path.resolve()}")

    boundary = counties[
        counties["STATEFP"].astype(str).eq("02")
        & counties["NAME"].astype(str).str.casefold().eq("north slope")
    ].copy()
    if boundary.empty:
        raise RuntimeError("North Slope Borough boundary not found in TIGER county layer.")

    if boundary.crs is not None and boundary.crs.to_epsg() != 4326:
        boundary = boundary.to_crs("EPSG:4326")
    boundary["geometry"] = boundary.geometry.simplify(0.01, preserve_topology=True)
    boundary = boundary[
        [
            "STATEFP",
            "COUNTYFP",
            "GEOID",
            "NAME",
            "NAMELSAD",
            "LSAD",
            "ALAND",
            "AWATER",
            "INTPTLAT",
            "INTPTLON",
            "geometry",
        ]
    ].copy()
    boundary["source_url"] = TIGER_2025_COUNTY_URL
    boundary["source_note"] = (
        "U.S. Census Bureau TIGER/Line 2025 county boundary; filtered to "
        "North Slope Borough, Alaska, and simplified for public website maps."
    )
    boundary.to_file(output_path, driver="GeoJSON")
    return output_path


if __name__ == "__main__":
    print(build_boundary())
