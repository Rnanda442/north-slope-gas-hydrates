from __future__ import annotations

from pathlib import Path
import re

import geopandas as gpd
import numpy as np
import pandas as pd

from dashboard.stability_sources import (
    active_stability_source_path,
    load_ggd223_permafrost_points,
    load_hydrate_assessment_units,
)


PRODUCT_DIR_NAME = "public_stability_products"
WELL_CONTEXT_FILE_NAME = "north_slope_well_stability_context_2026-06-14.csv"
WELL_CONTEXT_SUMMARY_FILE_NAME = "north_slope_well_stability_context_summary_2026-06-14.csv"
G10015_INVENTORY_FILE_NAME = "g10015_temperature_profile_inventory_2026-06-14.csv"
G10015_SUMMARY_FILE_NAME = "g10015_temperature_profile_summary_2026-06-14.csv"

WELL_SOURCE_RELATIVE_PATH = (
    "raw_data/Wells/Well_Bottom_Hole_Location/Well_Bottom_Hole_Location.shp"
)
G10015_RELATIVE_PATH = "03_temperature_geothermal/NSIDC_G10015_extracted"
NUMERIC_PROFILE_RE = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s*$")

WELL_CONTEXT_COLUMNS = [
    "object_id",
    "permit_number",
    "api_number",
    "well_name",
    "field",
    "pool",
    "current_status",
    "driller_total_depth_ft",
    "true_vertical_depth_ft",
    "wellhead_latitude",
    "wellhead_longitude",
    "bottomhole_latitude",
    "bottomhole_longitude",
    "depth_basis",
    "depth_basis_ft",
    "depth_basis_m",
    "hydrate_assessment_unit_count",
    "hydrate_assessment_codes",
    "within_hydrate_assessment_unit",
    "nearest_ggd223_code",
    "nearest_ggd223_well",
    "nearest_permafrost_depth_m",
    "nearest_ggd223_distance_km",
    "well_depth_exceeds_nearest_permafrost_control",
    "stability_context_flag",
]


def default_stability_products_dir(project_root: Path) -> Path:
    return project_root / "data" / PRODUCT_DIR_NAME


def default_well_context_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / WELL_CONTEXT_FILE_NAME


def default_well_context_summary_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / WELL_CONTEXT_SUMMARY_FILE_NAME


def default_g10015_inventory_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / G10015_INVENTORY_FILE_NAME


def default_g10015_summary_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / G10015_SUMMARY_FILE_NAME


def load_arctic_slope_public_wells(project_root: Path) -> gpd.GeoDataFrame:
    path = Path(project_root) / WELL_SOURCE_RELATIVE_PATH
    columns = [
        "object_id",
        "permit_number",
        "api_number",
        "well_name",
        "field",
        "pool",
        "current_class",
        "current_status",
        "driller_total_depth_ft",
        "true_vertical_depth_ft",
        "wellhead_latitude",
        "wellhead_longitude",
        "bottomhole_latitude",
        "bottomhole_longitude",
        "geometry",
    ]
    if not path.exists():
        return gpd.GeoDataFrame(columns=columns, geometry="geometry", crs="EPSG:4326")

    wells = gpd.read_file(path)
    wells = wells[wells["Geographic"].eq("ARCTIC SLOPE")].copy()
    wells = wells.rename(
        columns={
            "OBJECTID": "object_id",
            "PermitNumb": "permit_number",
            "APINumber": "api_number",
            "WellName": "well_name",
            "Field": "field",
            "Pools": "pool",
            "CurrentCla": "current_class",
            "CurrentSta": "current_status",
            "DrillerTot": "driller_total_depth_ft",
            "TrueVertic": "true_vertical_depth_ft",
            "WellHeadLa": "wellhead_latitude",
            "WellHeadLo": "wellhead_longitude",
            "BottomHole": "bottomhole_latitude",
            "BottomHo_1": "bottomhole_longitude",
        }
    )
    keep = [column for column in columns if column in wells.columns]
    wells = wells[keep]

    latitude = pd.to_numeric(wells["wellhead_latitude"], errors="coerce")
    longitude = pd.to_numeric(wells["wellhead_longitude"], errors="coerce")
    wells = wells.assign(wellhead_latitude=latitude, wellhead_longitude=longitude)
    wells = wells.dropna(subset=["wellhead_latitude", "wellhead_longitude"]).copy()
    return gpd.GeoDataFrame(
        wells.drop(columns="geometry", errors="ignore"),
        geometry=gpd.points_from_xy(wells["wellhead_longitude"], wells["wellhead_latitude"]),
        crs="EPSG:4326",
    )


def _depth_basis(row: pd.Series) -> pd.Series:
    true_vertical_depth = pd.to_numeric(row.get("true_vertical_depth_ft"), errors="coerce")
    driller_depth = pd.to_numeric(row.get("driller_total_depth_ft"), errors="coerce")
    if pd.notna(true_vertical_depth) and true_vertical_depth > 0:
        return pd.Series({"depth_basis": "TrueVertic", "depth_basis_ft": true_vertical_depth})
    if pd.notna(driller_depth) and driller_depth > 0:
        return pd.Series({"depth_basis": "DrillerTot", "depth_basis_ft": driller_depth})
    return pd.Series({"depth_basis": "missing", "depth_basis_ft": pd.NA})


def _join_assessment_units(
    wells: gpd.GeoDataFrame,
    assessment_units: gpd.GeoDataFrame,
) -> pd.DataFrame:
    if wells.empty or assessment_units.empty:
        return pd.DataFrame(
            {
                "object_id": wells.get("object_id", pd.Series(dtype="int64")),
                "hydrate_assessment_unit_count": 0,
                "hydrate_assessment_codes": "",
                "within_hydrate_assessment_unit": False,
            }
        )

    unit_columns = ["ASSESSCODE", "ASSESSNAME", "geometry"]
    joined = gpd.sjoin(
        wells[["object_id", "geometry"]],
        assessment_units[unit_columns],
        how="left",
        predicate="within",
    )

    def unique_join(values: pd.Series) -> str:
        clean = sorted({str(value) for value in values.dropna() if str(value).strip()})
        return "; ".join(clean)

    grouped = (
        joined.groupby("object_id", dropna=False)
        .agg(
            hydrate_assessment_unit_count=("ASSESSCODE", lambda values: values.dropna().nunique()),
            hydrate_assessment_codes=("ASSESSCODE", unique_join),
        )
        .reset_index()
    )
    grouped["within_hydrate_assessment_unit"] = (
        grouped["hydrate_assessment_unit_count"].fillna(0).astype(int) > 0
    )
    return grouped


def _join_nearest_permafrost_control(
    wells: gpd.GeoDataFrame,
    controls: gpd.GeoDataFrame,
) -> pd.DataFrame:
    columns = [
        "object_id",
        "nearest_ggd223_code",
        "nearest_ggd223_well",
        "nearest_permafrost_depth_m",
        "nearest_ggd223_distance_km",
    ]
    if wells.empty or controls.empty:
        return pd.DataFrame(columns=columns)

    nearest = gpd.sjoin_nearest(
        wells[["object_id", "geometry"]].to_crs("EPSG:3338"),
        controls[
            ["code", "well_designation", "permafrost_depth_m", "geometry"]
        ].to_crs("EPSG:3338"),
        how="left",
        distance_col="nearest_ggd223_distance_m",
    )
    nearest = nearest.sort_values(["object_id", "nearest_ggd223_distance_m"]).drop_duplicates(
        subset=["object_id"],
        keep="first",
    )
    output = nearest.rename(
        columns={
            "code": "nearest_ggd223_code",
            "well_designation": "nearest_ggd223_well",
            "permafrost_depth_m": "nearest_permafrost_depth_m",
        }
    )
    output["nearest_ggd223_distance_km"] = output["nearest_ggd223_distance_m"] / 1000
    return output[columns]


def build_public_well_stability_context(
    project_root: Path,
    source_root: Path | None = None,
) -> pd.DataFrame:
    root = Path(project_root)
    active_source = Path(source_root) if source_root is not None else active_stability_source_path(root)
    wells = load_arctic_slope_public_wells(root)
    controls = load_ggd223_permafrost_points(active_source)
    assessment_units = load_hydrate_assessment_units(active_source)

    if wells.empty:
        return pd.DataFrame()

    base = pd.DataFrame(wells.drop(columns="geometry", errors="ignore"))
    depth = base.apply(_depth_basis, axis=1)
    base = pd.concat([base, depth], axis=1)
    base["depth_basis_m"] = pd.to_numeric(base["depth_basis_ft"], errors="coerce") * 0.3048

    au_context = _join_assessment_units(wells, assessment_units)
    permafrost_context = _join_nearest_permafrost_control(wells, controls)

    context = base.merge(au_context, on="object_id", how="left").merge(
        permafrost_context,
        on="object_id",
        how="left",
    )
    context["hydrate_assessment_unit_count"] = (
        context["hydrate_assessment_unit_count"].fillna(0).astype(int)
    )
    context["within_hydrate_assessment_unit"] = context[
        "within_hydrate_assessment_unit"
    ].fillna(False)
    context["well_depth_exceeds_nearest_permafrost_control"] = (
        pd.to_numeric(context["depth_basis_m"], errors="coerce")
        >= pd.to_numeric(context["nearest_permafrost_depth_m"], errors="coerce")
    )

    context["stability_context_flag"] = "needs_depth_or_permafrost_context"
    context.loc[
        ~context["within_hydrate_assessment_unit"],
        "stability_context_flag",
    ] = "outside_usgs_hydrate_au"
    context.loc[
        context["within_hydrate_assessment_unit"]
        & context["depth_basis_m"].notna()
        & context["nearest_permafrost_depth_m"].notna()
        & ~context["well_depth_exceeds_nearest_permafrost_control"],
        "stability_context_flag",
    ] = "shallower_than_nearest_permafrost_control"
    context.loc[
        context["within_hydrate_assessment_unit"]
        & context["depth_basis_m"].notna()
        & context["nearest_permafrost_depth_m"].notna()
        & context["well_depth_exceeds_nearest_permafrost_control"],
        "stability_context_flag",
    ] = "public_context_candidate"

    sort_columns = ["within_hydrate_assessment_unit", "nearest_ggd223_distance_km", "well_name"]
    context = context.sort_values(sort_columns, ascending=[False, True, True]).reset_index(drop=True)
    return context[[column for column in WELL_CONTEXT_COLUMNS if column in context.columns]]


def stability_context_summary_frame(context: pd.DataFrame) -> pd.DataFrame:
    if context.empty:
        return pd.DataFrame(columns=["metric", "value", "meaning"])

    depth_available = pd.to_numeric(context["depth_basis_m"], errors="coerce").notna()
    rows = [
        {
            "metric": "Arctic Slope public wells",
            "value": int(len(context)),
            "meaning": "Alaska DNR wells filtered to Geographic = ARCTIC SLOPE.",
        },
        {
            "metric": "Inside USGS hydrate AU",
            "value": int(context["within_hydrate_assessment_unit"].sum()),
            "meaning": "Wellhead point falls inside one or more USGS 2019 hydrate assessment units.",
        },
        {
            "metric": "Depth field available",
            "value": int(depth_available.sum()),
            "meaning": "TrueVertic preferred; DrillerTot used only when TrueVertic is unavailable.",
        },
        {
            "metric": "Nearest GGD223 control assigned",
            "value": int(context["nearest_permafrost_depth_m"].notna().sum()),
            "meaning": "Nearest public permafrost-depth control point assigned by projected distance.",
        },
        {
            "metric": "Public context candidates",
            "value": int((context["stability_context_flag"] == "public_context_candidate").sum()),
            "meaning": "Inside a USGS hydrate AU and deeper than the nearest GGD223 permafrost-depth control.",
        },
    ]
    return pd.DataFrame(rows)


def load_public_well_stability_context(project_root: Path) -> pd.DataFrame:
    path = default_well_context_path(project_root)
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def _header_value(lines: list[str], label: str) -> str:
    prefix = f"{label}:"
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(prefix):
            return stripped.split(":", 1)[1].strip()
    return ""


def parse_g10015_temperature_profile(path: Path) -> dict[str, object]:
    lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    records = []
    for line in lines:
        match = NUMERIC_PROFILE_RE.match(line)
        if match:
            records.append((float(match.group(1)), float(match.group(2))))

    well_code = Path(path).stem.split("_", 1)[0]
    result: dict[str, object] = {
        "file_name": Path(path).name,
        "well_code": well_code,
        "well_name": _header_value(lines, "Well name"),
        "profile_file_name": _header_value(lines, "File name"),
        "log_date": _header_value(lines, "Log date"),
        "sample_count": len(records),
        "min_depth_m": pd.NA,
        "max_depth_m": pd.NA,
        "min_temperature_c": pd.NA,
        "max_temperature_c": pd.NA,
        "deepest_temperature_c": pd.NA,
        "deepest_window_gradient_c_per_100m": pd.NA,
    }
    if not records:
        return result

    profile = pd.DataFrame(records, columns=["depth_m", "temperature_c"]).sort_values("depth_m")
    deepest_depth = float(profile["depth_m"].max())
    deepest_window = profile[profile["depth_m"] >= deepest_depth - 100]
    gradient = pd.NA
    if len(deepest_window) >= 3 and deepest_window["depth_m"].nunique() >= 2:
        slope = np.polyfit(
            deepest_window["depth_m"].to_numpy(),
            deepest_window["temperature_c"].to_numpy(),
            1,
        )[0]
        gradient = float(slope * 100)

    result.update(
        {
            "min_depth_m": float(profile["depth_m"].min()),
            "max_depth_m": deepest_depth,
            "min_temperature_c": float(profile["temperature_c"].min()),
            "max_temperature_c": float(profile["temperature_c"].max()),
            "deepest_temperature_c": float(profile.iloc[-1]["temperature_c"]),
            "deepest_window_gradient_c_per_100m": gradient,
        }
    )
    return result


def build_g10015_temperature_inventory(source_root: Path) -> pd.DataFrame:
    profile_dir = Path(source_root) / G10015_RELATIVE_PATH
    if not profile_dir.exists():
        return pd.DataFrame()
    records = [
        parse_g10015_temperature_profile(path)
        for path in sorted(profile_dir.glob("*.txt"))
    ]
    if not records:
        return pd.DataFrame()
    inventory = pd.DataFrame(records)
    return inventory.sort_values(["well_code", "log_date", "file_name"]).reset_index(drop=True)


def temperature_inventory_summary_frame(inventory: pd.DataFrame) -> pd.DataFrame:
    if inventory.empty:
        return pd.DataFrame(columns=["metric", "value", "meaning"])
    gradient_count = pd.to_numeric(
        inventory["deepest_window_gradient_c_per_100m"],
        errors="coerce",
    ).notna()
    rows = [
        {
            "metric": "G10015 profiles",
            "value": int(len(inventory)),
            "meaning": "Processed public borehole temperature log files indexed.",
        },
        {
            "metric": "Unique well codes",
            "value": int(inventory["well_code"].nunique()),
            "meaning": "Unique public G10015/GGD223-style well codes represented by profiles.",
        },
        {
            "metric": "Maximum logged depth m",
            "value": round(float(pd.to_numeric(inventory["max_depth_m"], errors="coerce").max()), 2),
            "meaning": "Deepest depth reached by any indexed public temperature profile.",
        },
        {
            "metric": "Profiles with deepest-window gradient",
            "value": int(gradient_count.sum()),
            "meaning": "Profiles with enough deepest-window samples for a rough C per 100 m context estimate.",
        },
    ]
    return pd.DataFrame(rows)


def stability_parameter_readiness_frame() -> pd.DataFrame:
    rows = [
        {
            "input": "Well location",
            "current_status": "Ready",
            "current_source": "Alaska DNR Well Bottom Hole Location",
            "use_in_stability": "Spatial anchor for public well context and future stability joins.",
            "next_step": "Keep public well identifiers and coordinates separate from any future restricted rows.",
        },
        {
            "input": "Well depth",
            "current_status": "Ready for public context",
            "current_source": "DNR TrueVertic preferred, DrillerTot fallback",
            "use_in_stability": "Depth basis for checking whether a well reaches candidate stability intervals.",
            "next_step": "Confirm final approved depth basis and units when real workbook data arrives.",
        },
        {
            "input": "Base of ice-bearing permafrost",
            "current_status": "Partial",
            "current_source": "Nearest NSIDC GGD223 point controls; OM-222 plate not digitized",
            "use_in_stability": "Upper thermal boundary/context for permafrost-associated hydrate stability.",
            "next_step": "Digitize/georeference OM-222 or locate a ready public GIS derivative.",
        },
        {
            "input": "Temperature context",
            "current_status": "Ready as inventory",
            "current_source": "NSIDC G10015 processed borehole temperature logs",
            "use_in_stability": "Constrains local temperature-depth behavior and geothermal-gradient context.",
            "next_step": "Build well-specific or area-specific geothermal profiles from the inventory.",
        },
        {
            "input": "Geothermal gradient",
            "current_status": "Context only",
            "current_source": "Deepest-window estimates from G10015 profiles",
            "use_in_stability": "Approximate temperature increase with depth.",
            "next_step": "Replace rough estimates with calibrated gradients and uncertainty bands.",
        },
        {
            "input": "Pressure assumption",
            "current_status": "Planned",
            "current_source": "Hydrostatic pressure assumption to be sourced and parameterized",
            "use_in_stability": "Converts depth to pressure for pressure-temperature phase comparison.",
            "next_step": "Add hydrostatic pressure equation, units, density assumption, and scenario toggle.",
        },
        {
            "input": "Hydrate phase curve",
            "current_status": "Planned",
            "current_source": "USGS/NETL methane hydrate phase-boundary sources",
            "use_in_stability": "Defines pressure-temperature conditions where methane hydrate can exist.",
            "next_step": "Add a cited lookup/table or equation and document gas/salinity assumptions.",
        },
        {
            "input": "Stability top/base/thickness",
            "current_status": "Not calculated yet",
            "current_source": "Requires all inputs above",
            "use_in_stability": "Final admissibility-zone result for ML feature engineering and screening.",
            "next_step": "Calculate only after pressure, temperature, permafrost-base, and phase-curve assumptions are locked.",
        },
    ]
    return pd.DataFrame(rows)


def load_g10015_temperature_inventory(project_root: Path) -> pd.DataFrame:
    path = default_g10015_inventory_path(project_root)
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def write_public_stability_products(
    project_root: Path,
    source_root: Path | None = None,
) -> tuple[Path, Path, Path | None, Path | None]:
    product_dir = default_stability_products_dir(project_root)
    product_dir.mkdir(parents=True, exist_ok=True)
    active_source = Path(source_root) if source_root is not None else active_stability_source_path(project_root)
    context = build_public_well_stability_context(project_root, active_source)
    summary = stability_context_summary_frame(context)
    context_path = default_well_context_path(project_root)
    summary_path = default_well_context_summary_path(project_root)
    context.to_csv(context_path, index=False)
    summary.to_csv(summary_path, index=False)

    inventory = build_g10015_temperature_inventory(active_source)
    if inventory.empty:
        return context_path, summary_path, None, None

    inventory_summary = temperature_inventory_summary_frame(inventory)
    inventory_path = default_g10015_inventory_path(project_root)
    inventory_summary_path = default_g10015_summary_path(project_root)
    inventory.to_csv(inventory_path, index=False)
    inventory_summary.to_csv(inventory_summary_path, index=False)
    return context_path, summary_path, inventory_path, inventory_summary_path
