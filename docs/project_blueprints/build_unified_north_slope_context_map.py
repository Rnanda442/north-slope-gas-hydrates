from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import pandas as pd
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
ASSET_DIR = (
    ROOT
    / "docs"
    / "project_blueprints"
    / "presentation_assets"
    / "website_well_maps_2026_06_18"
)
PNG_PATH = ASSET_DIR / "unified_north_slope_well_stability_context_map_2026_06_18.png"
PUBLIC_STABILITY = ROOT / "data" / "public_stability_products"
PUBLIC_SNAPSHOT = (
    ROOT
    / "data"
    / "public_stability_snapshot"
    / "north_slope_stability_snapshot_2026-06-13"
)
LANDMARK_DIR = ROOT / "data" / "source_library" / "basemap_landmarks_2026_06_18"

SCREEN_CSV = PUBLIC_STABILITY / "stability_screen_2026-06-14_methane_5ppt_v1.csv"
GGD223_CSV = PUBLIC_SNAPSHOT / "ggd223_permafrost_controls.csv"
AU_GEOJSON = PUBLIC_SNAPSHOT / "GasHydrateAUs.geojson"

W, H = 3200, 2000
MAP_BOX = (155, 300, 3045, 1660)
LON_MIN, LON_MAX = -157.7, -145.0
LAT_MIN, LAT_MAX = 68.9, 71.35

NAVY = (12, 34, 49)
INK = (25, 48, 60)
MUTED = (87, 105, 118)
LINE = (150, 165, 178)
PALE = (244, 248, 249)
LAND = (248, 248, 244)
OCEAN = (220, 239, 248)
GRID = (203, 218, 226)
WHITE = (255, 255, 255)
TEAL = (11, 118, 142)
TEAL_DARK = (8, 83, 104)
GRAY = (121, 137, 150)
ROAD = (178, 188, 198)
PIPE = (180, 83, 9)
BLACK = (17, 24, 39)
BLUE = (37, 99, 235)
AMBER = (217, 119, 6)
PURPLE = (124, 58, 237)

STATUS_STYLES = {
    "blocked_missing_temperature_profile": {
        "label": "Blocked: missing temperature profile",
        "color": (148, 163, 184),
        "size": 4,
        "alpha": 95,
    },
    "blocked_missing_depth": {
        "label": "Blocked: missing depth",
        "color": (100, 116, 139),
        "size": 5,
        "alpha": 135,
    },
    "outside_au_context": {
        "label": "Outside public AU context",
        "color": PURPLE,
        "size": 5,
        "alpha": 145,
    },
    "blocked_phase_curve_range_insufficient": {
        "label": "Blocked: phase curve range",
        "color": AMBER,
        "size": 6,
        "alpha": 190,
    },
    "calculated_no_stable_interval": {
        "label": "Calculated, no stable interval",
        "color": BLACK,
        "size": 7,
        "alpha": 205,
    },
    "calculated": {
        "label": "Calculated screen interval",
        "color": BLUE,
        "size": 9,
        "alpha": 235,
    },
}

FIELD_LABEL_ORDER = [
    "PRUDHOE BAY",
    "KUPARUK RIVER",
    "MILNE POINT",
    "COLVILLE RIVER",
    "PIKKA",
    "ENDICOTT",
    "NORTHSTAR",
]

VIRIDIS = [
    (68, 1, 84),
    (59, 82, 139),
    (33, 145, 140),
    (94, 201, 98),
    (253, 231, 37),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "arialbd.ttf" if bold else "arial.ttf",
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "calibrib.ttf" if bold else "calibri.ttf",
    ]
    roots = [Path("C:/Windows/Fonts"), Path("/usr/share/fonts/truetype/dejavu")]
    for root in roots:
        for name in candidates:
            path = root / name
            if path.exists():
                return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    value: str,
    size: int,
    fill: tuple[int, int, int] = INK,
    bold: bool = False,
    width: int | None = None,
    line_gap: int = 6,
) -> int:
    f = font(size, bold)
    if width is None:
        draw.text(xy, value, font=f, fill=fill)
        return xy[1] + size + line_gap
    lines: list[str] = []
    for raw in value.splitlines():
        current = ""
        for word in raw.split():
            candidate = f"{current} {word}".strip()
            if not current or draw.textlength(candidate, font=f) <= width:
                current = candidate
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
    y = xy[1]
    for line in lines:
        draw.text((xy[0], y), line, font=f, fill=fill)
        y += size + line_gap
    return y


def project(lon: float, lat: float) -> tuple[int, int]:
    left, top, right, bottom = MAP_BOX
    x = left + (lon - LON_MIN) / (LON_MAX - LON_MIN) * (right - left)
    y = bottom - (lat - LAT_MIN) / (LAT_MAX - LAT_MIN) * (bottom - top)
    return int(round(x)), int(round(y))


def in_extent(lon: float, lat: float, pad: float = 0.1) -> bool:
    return (
        LON_MIN - pad <= lon <= LON_MAX + pad
        and LAT_MIN - pad <= lat <= LAT_MAX + pad
    )


def load_geojson(path: Path) -> list[dict]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("type") != "FeatureCollection":
        return []
    return [feature for feature in payload.get("features", []) if feature.get("geometry")]


def geometry_paths(geometry: dict) -> Iterable[list[list[float]]]:
    coordinates = geometry.get("coordinates") or []
    geometry_type = geometry.get("type")
    if geometry_type == "LineString":
        yield coordinates
    elif geometry_type == "MultiLineString":
        yield from coordinates
    elif geometry_type == "Polygon":
        yield from coordinates
    elif geometry_type == "MultiPolygon":
        for polygon in coordinates:
            yield from polygon


def draw_geojson_lines(
    draw: ImageDraw.ImageDraw,
    features: list[dict],
    color: tuple[int, int, int],
    width: int,
    max_points: int = 1000,
) -> None:
    for feature in features:
        for path in geometry_paths(feature.get("geometry", {})):
            projected: list[tuple[int, int]] = []
            step = max(1, len(path) // max_points)
            for point in path[::step]:
                if not isinstance(point, (list, tuple)) or len(point) < 2:
                    continue
                lon, lat = float(point[0]), float(point[1])
                if in_extent(lon, lat):
                    projected.append(project(lon, lat))
            if len(projected) >= 2:
                draw.line(projected, fill=color, width=width, joint="curve")


def road_name(feature: dict) -> str:
    props = feature.get("properties", {}) or {}
    fields = [
        "Route_Name",
        "Route_Name_Unique",
        "Route_Name_Desc_1",
        "Route_Name_Desc_2",
        "Route_ID",
    ]
    return " ".join(str(props.get(field) or "") for field in fields).lower()


def color_scale(value: float, vmin: float, vmax: float) -> tuple[int, int, int]:
    if vmax <= vmin:
        return VIRIDIS[-1]
    t = max(0.0, min(1.0, (value - vmin) / (vmax - vmin)))
    scaled = t * (len(VIRIDIS) - 1)
    i = min(len(VIRIDIS) - 2, int(scaled))
    frac = scaled - i
    c0, c1 = VIRIDIS[i], VIRIDIS[i + 1]
    return tuple(int(c0[j] + frac * (c1[j] - c0[j])) for j in range(3))


def draw_circle(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    radius: int,
    fill: tuple[int, int, int],
    alpha: int = 255,
    outline: tuple[int, int, int] | None = WHITE,
) -> None:
    x, y = xy
    color = fill + (alpha,)
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)
    if outline:
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline=outline, width=2)


def draw_label(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    label: str,
    size: int,
    fill: tuple[int, int, int] = NAVY,
) -> None:
    f = font(size, True)
    x, y = xy
    bbox = draw.textbbox((x, y), label, font=f, anchor="mm")
    pad_x, pad_y = 9, 5
    box = (bbox[0] - pad_x, bbox[1] - pad_y, bbox[2] + pad_x, bbox[3] + pad_y)
    draw.rounded_rectangle(box, radius=8, fill=(255, 255, 255, 220), outline=(205, 218, 225), width=1)
    draw.text((x, y), label, font=f, fill=fill, anchor="mm")


def clean_label(value: object) -> str:
    return " ".join(str(value or "").replace("City of ", "").title().split())


def field_label_frame(screen: pd.DataFrame) -> pd.DataFrame:
    labels = screen[["field", "lat", "lon"]].copy()
    labels["field"] = labels["field"].fillna("").astype(str).str.strip()
    labels["lat"] = pd.to_numeric(labels["lat"], errors="coerce")
    labels["lon"] = pd.to_numeric(labels["lon"], errors="coerce")
    labels = labels.dropna(subset=["field", "lat", "lon"])
    labels = labels[
        labels["field"].ne("")
        & ~labels["field"].str.startswith("*")
        & labels["field"].str.lower().ne("nan")
    ]
    grouped = labels.groupby("field", as_index=False).agg(
        well_count=("field", "size"),
        lat=("lat", "median"),
        lon=("lon", "median"),
    )
    grouped = grouped[
        grouped["field"].isin(FIELD_LABEL_ORDER) | grouped["well_count"].ge(20)
    ].copy()
    order = {name: index for index, name in enumerate(FIELD_LABEL_ORDER)}
    grouped["sort_order"] = grouped["field"].map(order).fillna(99).astype(int)
    grouped["label"] = grouped["field"].map(clean_label)
    return grouped.sort_values(["sort_order", "well_count"], ascending=[True, False]).head(10)


def draw_legend(draw: ImageDraw.ImageDraw, ggd_min: int, ggd_max: int) -> None:
    x, y = 160, 210
    line_items = [
        ("DNR oil/gas units", GRAY, 4),
        ("USGS hydrate AU outlines", TEAL, 5),
        ("AKDOT roads", ROAD, 4),
        ("Dalton/Deadhorse roads", BLACK, 5),
        ("TAPS corridor", PIPE, 5),
    ]
    for label, color, width in line_items:
        draw.line((x, y + 14, x + 62, y + 14), fill=color, width=width)
        draw.text((x + 75, y), label, font=font(27), fill=INK)
        x += 410

    x, y = 160, 1688
    for status in [
        "calculated",
        "calculated_no_stable_interval",
        "blocked_phase_curve_range_insufficient",
        "blocked_missing_temperature_profile",
        "blocked_missing_depth",
        "outside_au_context",
    ]:
        style = STATUS_STYLES[status]
        draw_circle(draw, (x + 16, y + 16), style["size"] + 3, style["color"], style["alpha"])
        draw.text((x + 42, y), style["label"], font=font(25), fill=INK)
        x += 460 if status != "blocked_missing_temperature_profile" else 565

    bar_x, bar_y, bar_w, bar_h = 2480, 214, 330, 26
    for i in range(bar_w):
        value = ggd_min + (ggd_max - ggd_min) * (i / max(1, bar_w - 1))
        draw.line(
            (bar_x + i, bar_y, bar_x + i, bar_y + bar_h),
            fill=color_scale(value, ggd_min, ggd_max),
            width=1,
        )
    draw.rectangle((bar_x, bar_y, bar_x + bar_w, bar_y + bar_h), outline=LINE, width=2)
    draw.text((bar_x, bar_y - 35), "GGD223 pf_depth_m", font=font(24, True), fill=INK)
    draw.text((bar_x, bar_y + 34), f"{ggd_min} m", font=font(22), fill=MUTED)
    draw.text((bar_x + bar_w - 68, bar_y + 34), f"{ggd_max} m", font=font(22), fill=MUTED)


def draw_map() -> Path:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    screen = pd.read_csv(
        SCREEN_CSV,
        usecols=[
            "well_name",
            "field",
            "lat",
            "lon",
            "stability_result_status",
            "stability_confidence",
        ],
    )
    screen["lat"] = pd.to_numeric(screen["lat"], errors="coerce")
    screen["lon"] = pd.to_numeric(screen["lon"], errors="coerce")
    screen = screen.dropna(subset=["lat", "lon"])
    ggd = pd.read_csv(GGD223_CSV)
    ggd["permafrost_depth_m"] = pd.to_numeric(ggd["permafrost_depth_m"], errors="coerce")
    ggd_min = int(ggd["permafrost_depth_m"].min())
    ggd_max = int(ggd["permafrost_depth_m"].max())

    dnr_units = load_geojson(LANDMARK_DIR / "alaska_dnr_unit_boundary_current_north_slope_clip.geojson")
    roads_all = load_geojson(LANDMARK_DIR / "alaska_akdot_roads_north_slope_clip.geojson")
    key_roads = [feature for feature in roads_all if any(term in road_name(feature) for term in ["dalton", "deadhorse"])]
    local_roads = [feature for feature in roads_all if feature not in key_roads]
    taps = load_geojson(LANDMARK_DIR / "alaska_dnr_trans_alaska_pipeline.geojson")
    aus = load_geojson(AU_GEOJSON)
    gnis = load_geojson(LANDMARK_DIR / "usgs_gnis_places_north_slope_clip.geojson")

    img = Image.new("RGBA", (W, H), PALE + (255,))
    draw = ImageDraw.Draw(img, "RGBA")
    draw.rectangle(MAP_BOX, fill=LAND + (255,), outline=(91, 111, 124), width=3)
    left, top, right, bottom = MAP_BOX
    draw.rectangle((left, top, right, top + 315), fill=OCEAN + (255,))

    for lon in range(-157, -144, 2):
        x, _ = project(lon, LAT_MIN)
        draw.line((x, top, x, bottom), fill=GRID + (150,), width=1)
        draw.text((x - 33, bottom + 15), f"{lon}W", font=font(20), fill=MUTED)
    for lat_tenths in range(690, 714, 5):
        lat = lat_tenths / 10
        _, y = project(LON_MIN, lat)
        draw.line((left, y, right, y), fill=GRID + (150,), width=1)
        draw.text((left - 80, y - 12), f"{lat:.1f}N", font=font(20), fill=MUTED)

    draw_geojson_lines(draw, dnr_units, GRAY, 3, max_points=800)
    draw_geojson_lines(draw, aus, TEAL, 5, max_points=1400)
    draw_geojson_lines(draw, local_roads, ROAD, 3, max_points=900)
    draw_geojson_lines(draw, key_roads, BLACK, 6, max_points=1600)
    draw_geojson_lines(draw, taps, PIPE, 6, max_points=1600)

    for row in ggd.itertuples():
        lon, lat = float(row.longitude), float(row.latitude)
        if not in_extent(lon, lat):
            continue
        color = color_scale(float(row.permafrost_depth_m), ggd_min, ggd_max)
        draw_circle(draw, project(lon, lat), 10, color, 235)

    for status, style in STATUS_STYLES.items():
        subset = screen[screen["stability_result_status"].eq(status)]
        for row in subset.itertuples():
            lon, lat = float(row.lon), float(row.lat)
            if not in_extent(lon, lat):
                continue
            draw_circle(
                draw,
                project(lon, lat),
                style["size"],
                style["color"],
                style["alpha"],
                outline=None if style["size"] <= 4 else WHITE,
            )

    label_offsets = {
        "Prudhoe Bay": (65, 45),
        "Kuparuk River": (-35, 52),
        "Milne Point": (15, -55),
        "Colville River": (-70, -35),
        "Pikka": (-20, -55),
        "Endicott": (75, -35),
        "Northstar": (40, -55),
    }
    for row in field_label_frame(screen).itertuples():
        lon, lat = float(row.lon), float(row.lat)
        if not in_extent(lon, lat):
            continue
        px, py = project(lon, lat)
        dx, dy = label_offsets.get(row.label, (0, -48))
        draw_label(draw, (px + dx, py + dy), row.label, 31)

    for feature in gnis:
        props = feature.get("properties", {}) or {}
        label = clean_label(props.get("gaz_name"))
        for path in geometry_paths(feature.get("geometry", {})):
            for point in path:
                lon, lat = float(point[0]), float(point[1])
                if in_extent(lon, lat):
                    draw_label(draw, project(lon, lat), label, 23, MUTED)

    draw_text(draw, (130, 55), "Unified North Slope Well + Stability Context Map", 54, NAVY, True)
    draw_text(
        draw,
        (132, 122),
        "Public well status, USGS hydrate AUs, GGD223 pf_depth_m controls, DNR units, roads, TAPS, and field labels.",
        29,
        MUTED,
    )
    draw_legend(draw, ggd_min, ggd_max)
    draw_text(
        draw,
        (130, 1838),
        "Context/orientation only. Stability-screen status does not prove hydrate occurrence, saturation, or trained-model evidence.",
        29,
        NAVY,
        True,
        width=2700,
    )
    draw_text(
        draw,
        (130, 1885),
        "GitHub-safe layers: committed public stability screen, USGS AU snapshot, GGD223 public snapshot, and this derived PNG. OSL/Drive-only raw layers: full DNR/AKDOT/TAPS/Census/GNIS packages and any approved well-log/core/runtime data.",
        24,
        MUTED,
        width=2870,
    )
    img.convert("RGB").save(PNG_PATH, quality=96)
    return PNG_PATH


if __name__ == "__main__":
    print(draw_map())
