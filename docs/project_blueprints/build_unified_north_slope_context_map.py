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
SLIDE_PNG_PATH = ASSET_DIR / "unified_north_slope_slide_export_callout_space_2026_06_18.png"
PUBLIC_STABILITY = ROOT / "data" / "public_stability_products"
PUBLIC_GIS_PRODUCTS = ROOT / "data" / "public_gis_products"
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
BOROUGH_BOUNDARY_GEOJSON = PUBLIC_GIS_PRODUCTS / "north_slope_borough_boundary_tiger2025.geojson"
MASTER_2D = ROOT / "03_data_final" / "master_layers" / "north_slope_master_2d_layers.parquet"
DGGS_PREVIEW = (
    ROOT
    / "docs"
    / "evidence"
    / "slide02_source_bundle_2026_06_17"
    / "slide02_selected_11_dggs_umiat_gubik_geology_layer_slide_map.png"
)

W, H = 3800, 2200
MAP_BOX = (150, 330, 2785, 1680)
SIDE_PANEL = (2850, 330, 3655, 1680)
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
SEISMIC = (14, 165, 233)
SEISMIC_3D = (234, 88, 12)
ASSESSMENT_CONTEXT = (20, 123, 133)

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


def load_master_2d_context() -> pd.DataFrame:
    if not MASTER_2D.exists():
        return pd.DataFrame(
            columns=["layer_name", "feature_id", "vertex_order", "lon", "lat", "depth_m", "au_name"]
        )
    return pd.read_parquet(
        MASTER_2D,
        columns=["layer_name", "feature_id", "vertex_order", "lon", "lat", "depth_m", "au_name"],
    )


def draw_frame_lines(
    draw: ImageDraw.ImageDraw,
    frame: pd.DataFrame,
    layer_name: str,
    color: tuple[int, int, int],
    width: int,
    max_features: int,
    max_points_per_feature: int,
) -> None:
    if frame.empty:
        return
    layer = frame[frame["layer_name"].eq(layer_name)].copy()
    if layer.empty:
        return
    layer["lon"] = pd.to_numeric(layer["lon"], errors="coerce")
    layer["lat"] = pd.to_numeric(layer["lat"], errors="coerce")
    layer = layer.dropna(subset=["feature_id", "vertex_order", "lon", "lat"])
    if layer.empty:
        return
    feature_ids = layer["feature_id"].drop_duplicates().tolist()
    if len(feature_ids) > max_features:
        step = max(1, len(feature_ids) // max_features)
        feature_ids = feature_ids[::step][:max_features]
    layer = layer[layer["feature_id"].isin(feature_ids)]
    for _, rows in layer.groupby("feature_id", sort=False):
        rows = rows.sort_values("vertex_order")
        if len(rows) > max_points_per_feature:
            step = max(1, len(rows) // max_points_per_feature)
            rows = rows.iloc[::step].copy()
        projected = []
        for row in rows.itertuples():
            lon, lat = float(row.lon), float(row.lat)
            if in_extent(lon, lat, pad=0.35):
                projected.append(project(lon, lat))
        if len(projected) >= 2:
            draw.line(projected, fill=color, width=width, joint="curve")


def draw_public_well_reference_points(
    draw: ImageDraw.ImageDraw,
    frame: pd.DataFrame,
    max_points: int = 1800,
) -> None:
    if frame.empty:
        return
    wells = frame[frame["layer_name"].eq("wells")].copy()
    if wells.empty:
        return
    wells["lon"] = pd.to_numeric(wells["lon"], errors="coerce")
    wells["lat"] = pd.to_numeric(wells["lat"], errors="coerce")
    wells = wells.dropna(subset=["lon", "lat"]).sort_values(["lon", "lat"])
    if len(wells) > max_points:
        step = max(1, len(wells) // max_points)
        wells = wells.iloc[::step].head(max_points)
    for row in wells.itertuples():
        lon, lat = float(row.lon), float(row.lat)
        if in_extent(lon, lat):
            draw_circle(draw, project(lon, lat), 2, (100, 116, 139), 72, outline=None)


def paste_image_fit(
    base: Image.Image,
    path: Path,
    box: tuple[int, int, int, int],
    cover: bool = False,
) -> None:
    draw = ImageDraw.Draw(base, "RGBA")
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=18, fill=WHITE + (255,), outline=(205, 218, 225), width=2)
    if not path.exists():
        draw_text(draw, (x1 + 22, y1 + 22), "DGGS preview missing", 28, AMBER, True, width=x2 - x1 - 44)
        return
    img = Image.open(path).convert("RGB")
    bw, bh = x2 - x1 - 24, y2 - y1 - 24
    scale = max(bw / img.width, bh / img.height) if cover else min(bw / img.width, bh / img.height)
    resized = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.Resampling.LANCZOS)
    if cover:
        left = max(0, (resized.width - bw) // 2)
        top = max(0, (resized.height - bh) // 2)
        resized = resized.crop((left, top, left + bw, top + bh))
    px = x1 + 12 + (bw - resized.width) // 2
    py = y1 + 12 + (bh - resized.height) // 2
    base.paste(resized, (px, py))


def draw_side_panel(base: Image.Image) -> None:
    draw = ImageDraw.Draw(base, "RGBA")
    x1, y1, x2, y2 = SIDE_PANEL
    draw.rounded_rectangle(SIDE_PANEL, radius=22, fill=(255, 255, 255, 245), outline=(196, 214, 221), width=3)
    draw_text(draw, (x1 + 34, y1 + 34), "Integrated source layers", 38, NAVY, True, width=x2 - x1 - 68)
    y = y1 + 92
    layers = [
        ("Regional Boundary", "Census/TIGER North Slope Borough edge"),
        ("Geoscience Orientation", "study boundary, public wells, 2D/3D seismic"),
        ("DGGS RI 2018-6", "Umiat-Gubik units, contacts/faults, folds"),
        ("Stability controls", "GGD223 pf_depth_m + USGS hydrate AUs"),
        ("OSL landmarks", "DNR units, AKDOT roads, TAPS, communities"),
    ]
    colors = [BLACK, ASSESSMENT_CONTEXT, SEISMIC_3D, TEAL, PIPE]
    for (header, body), color in zip(layers, colors):
        draw.rounded_rectangle((x1 + 34, y, x1 + 64, y + 30), radius=6, fill=color + (255,))
        draw_text(draw, (x1 + 82, y - 2), header, 26, NAVY, True, width=x2 - x1 - 120)
        y = draw_text(draw, (x1 + 82, y + 30), body, 22, MUTED, width=x2 - x1 - 120, line_gap=5) + 16

    draw_text(draw, (x1 + 34, y + 10), "DGGS Umiat-Gubik geology preview", 27, NAVY, True)
    paste_image_fit(base, DGGS_PREVIEW, (x1 + 34, y + 55, x2 - 34, y + 390), cover=False)
    draw_text(
        draw,
        (x1 + 34, y + 418),
        "Source/caveat: Herriott et al. 2018, Alaska DGGS RI 2018-6. "
        "Geology and structure context only; not hydrate occurrence or saturation.",
        22,
        MUTED,
        width=x2 - x1 - 68,
    )


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
        ("North Slope Borough boundary", BLACK, 6),
        ("Public assessment context", ASSESSMENT_CONTEXT, 4),
        ("2D seismic coverage", SEISMIC, 3),
        ("3D seismic footprints", SEISMIC_3D, 3),
        ("DNR oil/gas units", GRAY, 4),
        ("USGS hydrate AU outlines", TEAL, 5),
        ("AKDOT roads", ROAD, 4),
        ("Dalton/Deadhorse roads", BLACK, 5),
        ("TAPS corridor", PIPE, 5),
    ]
    for index, (label, color, width) in enumerate(line_items):
        if index == 4:
            x, y = 160, 255
        draw.line((x, y + 14, x + 62, y + 14), fill=color, width=width)
        draw.text((x + 75, y), label, font=font(23), fill=INK)
        x += 440

    x, y = 160, 1718
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
        draw.text((x + 42, y), style["label"], font=font(23), fill=INK)
        x += 460 if status != "blocked_missing_temperature_profile" else 565

    bar_x, bar_y, bar_w, bar_h = 3080, 210, 330, 26
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
    borough_boundary = load_geojson(BOROUGH_BOUNDARY_GEOJSON)
    gnis = load_geojson(LANDMARK_DIR / "usgs_gnis_places_north_slope_clip.geojson")
    master_context = load_master_2d_context()

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

    draw_frame_lines(draw, master_context, "assessment_units", ASSESSMENT_CONTEXT, 2, 80, 420)
    draw_frame_lines(draw, master_context, "seismic_2d", SEISMIC, 1, 260, 130)
    draw_frame_lines(draw, master_context, "seismic_3d_inventory", SEISMIC_3D, 2, 120, 180)
    draw_frame_lines(draw, master_context, "extent", BLACK, 4, 8, 20)
    draw_geojson_lines(draw, borough_boundary, BLACK, 7, max_points=2600)
    draw_public_well_reference_points(draw, master_context)

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
        "Census/TIGER North Slope Borough boundary, geoscience orientation, DGGS Umiat-Gubik preview, GGD223 controls, USGS hydrate AUs, screen status, DNR units, roads, TAPS, and field labels.",
        29,
        MUTED,
    )
    draw_legend(draw, ggd_min, ggd_max)
    draw_side_panel(img)
    draw_text(
        draw,
        (130, 1925),
        "Context/orientation only. Stability-screen status does not prove hydrate occurrence, saturation, or trained-model evidence.",
        29,
        NAVY,
        True,
        width=3350,
    )
    draw_text(
        draw,
        (130, 1975),
        "GitHub-safe layers: Census/TIGER North Slope Borough boundary, public master geoscience context, committed stability screen, USGS AU snapshot, GGD223 public snapshot, DGGS preview PNG, and this derived PNG. OSL/Drive-only raw layers: full DNR/AKDOT/TAPS/Census/GNIS/DGGS packages and any approved well-log/core/runtime data.",
        24,
        MUTED,
        width=3450,
    )
    img.convert("RGB").save(PNG_PATH, quality=96)
    draw_slide_callout_export(img.convert("RGB"))
    return PNG_PATH


def draw_slide_callout_export(full_map: Image.Image) -> Path:
    slide_w, slide_h = 3200, 1800
    slide = Image.new("RGB", (slide_w, slide_h), PALE)
    draw = ImageDraw.Draw(slide, "RGBA")
    draw_text(draw, (92, 54), "Unified 2D North Slope Map", 54, NAVY, True)
    draw_text(
        draw,
        (94, 122),
        "Slide export leaves a right-side lane for editable callouts in PowerPoint or Google Slides.",
        30,
        MUTED,
        width=2700,
    )

    map_crop = full_map.crop((0, 300, 2825, 1690))
    map_resized = map_crop.resize((2160, 1100), Image.Resampling.LANCZOS)
    draw.rounded_rectangle((90, 230, 2290, 1435), radius=18, fill=WHITE, outline=(190, 210, 218), width=3)
    slide.paste(map_resized, (110, 300))

    panel = (2350, 230, 3110, 1505)
    draw.rounded_rectangle(panel, radius=18, fill=(255, 255, 255), outline=(190, 210, 218), width=3)
    draw_text(draw, (2388, 270), "Editable callout lane", 38, NAVY, True, width=650)
    y = 344
    callouts = [
        ("1", "North Slope edge", "Census/TIGER borough boundary"),
        ("2", "Geology context", "DGGS Umiat-Gubik units + structures"),
        ("3", "P-T controls", "GGD223 + hydrate AU source controls"),
        ("4", "Screen status", "admissibility only; not hydrate proof"),
    ]
    colors = [ASSESSMENT_CONTEXT, SEISMIC_3D, TEAL, AMBER]
    for (number, header, body), color in zip(callouts, colors):
        draw.ellipse((2388, y, 2440, y + 52), fill=color)
        draw_text(draw, (2404, y + 10), number, 26, WHITE, True)
        draw_text(draw, (2460, y - 2), header, 27, NAVY, True, width=570)
        y = draw_text(draw, (2460, y + 34), body, 23, MUTED, width=570) + 38

    paste_image_fit(slide, DGGS_PREVIEW, (2388, 1044, 3072, 1325), cover=False)
    draw_text(
        draw,
        (2388, 1350),
        "Keep labels/circles/arrows editable in the deck. This PNG is the map layer only.",
        23,
        MUTED,
        width=650,
    )
    draw_text(
        draw,
        (92, 1580),
        "Context/orientation only. Stability-screen status does not prove hydrate occurrence, saturation, producibility, or trained-model evidence.",
        29,
        NAVY,
        True,
        width=3000,
    )
    draw_text(
        draw,
        (92, 1630),
        "Sources/layers: Census/TIGER North Slope Borough boundary, public master geoscience context, DGGS RI 2018-6 preview, GGD223 controls, USGS hydrate assessment units, public stability screen, and OSL-staged DNR/AKDOT/TAPS/community/field landmarks.",
        24,
        MUTED,
        width=3000,
    )
    slide.save(SLIDE_PNG_PATH, quality=96)
    return SLIDE_PNG_PATH


if __name__ == "__main__":
    print(draw_map())
