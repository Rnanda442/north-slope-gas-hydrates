from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import pandas as pd

from dashboard.stability_sources import (
    active_stability_source_path,
    load_ggd223_permafrost_points,
    load_hydrate_assessment_units,
)


PRODUCT_DIR_NAME = "public_stability_products"
WELL_CONTEXT_FILE_NAME = "north_slope_well_stability_context_2026-06-14.csv"
WELL_CONTEXT_SUMMARY_FILE_NAME = "north_slope_well_stability_context_summary_2026-06-14.csv"

WELL_SOURCE_RELATIVE_PATH = (
    "raw_data/Wells/Well_Bottom_Hole_Location/Well_Bottom_Hole_Location.shp"
)

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


def write_public_stability_products(
    project_root: Path,
    source_root: Path | None = None,
) -> tuple[Path, Path]:
    product_dir = default_stability_products_dir(project_root)
    product_dir.mkdir(parents=True, exist_ok=True)
    context = build_public_well_stability_context(project_root, source_root)
    summary = stability_context_summary_frame(context)
    context_path = default_well_context_path(project_root)
    summary_path = default_well_context_summary_path(project_root)
    context.to_csv(context_path, index=False)
    summary.to_csv(summary_path, index=False)
    return context_path, summary_path
