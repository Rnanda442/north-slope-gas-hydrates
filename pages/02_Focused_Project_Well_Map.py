from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PRODUCTS = PROJECT_ROOT / "data" / "public_stability_products"
FOCUS_POINTS_PATH = PUBLIC_PRODUCTS / "project_well_focus_points_2026-06-23.csv"
WELL_PATHS_PATH = PUBLIC_PRODUCTS / "project_well_paths_public_simplified_2026-06-23.csv"
MASTER_2D_PATH = PROJECT_ROOT / "03_data_final" / "master_layers" / "north_slope_master_2d_layers.parquet"
MASTER_3D_PATH = PROJECT_ROOT / "03_data_final" / "master_layers" / "north_slope_master_3d_surfaces.parquet"

LAYER_STYLE = {
    "assessment": {"color": "rgba(14, 116, 144, 0.55)", "width": 2.0, "fill": "rgba(14, 116, 144, 0.08)"},
    "field": {"color": "rgba(71, 85, 105, 0.78)", "width": 1.6, "fill": "rgba(148, 163, 184, 0.10)"},
    "road": {"color": "rgba(249, 115, 22, 0.72)", "width": 1.5, "fill": None},
    "taps": {"color": "rgba(120, 53, 15, 0.85)", "width": 2.8, "fill": None},
    "pipeline": {"color": "rgba(120, 53, 15, 0.85)", "width": 2.8, "fill": None},
    "fault": {"color": "rgba(220, 38, 38, 0.75)", "width": 1.4, "fill": None},
    "fold": {"color": "rgba(124, 58, 237, 0.65)", "width": 1.2, "fill": None},
    "contact": {"color": "rgba(15, 118, 110, 0.65)", "width": 1.1, "fill": None},
    "seismic_2d": {"color": "rgba(14, 165, 233, 0.34)", "width": 0.7, "fill": None},
    "seismic_3d": {"color": "rgba(234, 88, 12, 0.55)", "width": 0.9, "fill": "rgba(249, 115, 22, 0.10)"},
    "extent": {"color": "rgba(15, 23, 42, 0.85)", "width": 2.2, "fill": None},
}


def _safe_read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_focus_points(path_text: str) -> pd.DataFrame:
    points = _safe_read_csv(Path(path_text))
    if points.empty:
        points = pd.DataFrame(
            [
                ["MTE / Mt. Elbert", 70.4918022, -148.6963651, "#b31942", "fallback focus marker"],
                ["IGS / Ignik Sikumi", 70.5150, -148.6820, "#0f766e", "fallback focus marker"],
                ["Hydrate-01", 70.4550, -148.5600, "#7c3aed", "fallback focus marker"],
                ["HYDRATE 02", 70.6100, -148.1200, "#f97316", "fallback focus marker"],
            ],
            columns=["well_label", "latitude", "longitude", "marker_color", "coordinate_note"],
        )
    points["latitude"] = pd.to_numeric(points["latitude"], errors="coerce")
    points["longitude"] = pd.to_numeric(points["longitude"], errors="coerce")
    return points.dropna(subset=["latitude", "longitude"])


@st.cache_data(show_spinner=False)
def load_well_paths(path_text: str) -> pd.DataFrame:
    paths = _safe_read_csv(Path(path_text))
    if paths.empty:
        return paths
    paths["latitude"] = pd.to_numeric(paths["latitude"], errors="coerce")
    paths["longitude"] = pd.to_numeric(paths["longitude"], errors="coerce")
    paths["measured_depth_ft"] = pd.to_numeric(paths.get("measured_depth_ft"), errors="coerce")
    return paths.dropna(subset=["latitude", "longitude"]).sort_values(["api_number", "measured_depth_ft"])


@st.cache_data(show_spinner=False)
def load_master_context(path_text: str) -> pd.DataFrame:
    path = Path(path_text)
    if not path.exists():
        return pd.DataFrame()
    try:
        frame = pd.read_parquet(path)
    except Exception:
        return pd.DataFrame()
    for column in ["lon", "lat"]:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
    if "vertex_order" in frame.columns:
        frame["vertex_order"] = pd.to_numeric(frame["vertex_order"], errors="coerce")
    return frame.dropna(subset=["lon", "lat"])


def layer_matches(layer_name: str, keywords: list[str]) -> bool:
    text = str(layer_name).lower().replace("-", "_").replace(" ", "_")
    return any(keyword in text for keyword in keywords)


def add_context_layer(fig: go.Figure, context: pd.DataFrame, keywords: list[str], label: str, style_key: str) -> int:
    if context.empty or "layer_name" not in context.columns or "feature_id" not in context.columns:
        return 0
    layer_names = [name for name in context["layer_name"].dropna().unique() if layer_matches(name, keywords)]
    if not layer_names:
        return 0
    subset = context[context["layer_name"].isin(layer_names)].copy()
    if subset.empty:
        return 0
    style = LAYER_STYLE.get(style_key, {"color": "#64748b", "width": 1.2, "fill": None})
    count = 0
    showlegend = True
    for _, rows in subset.groupby("feature_id", dropna=False):
        rows = rows.sort_values("vertex_order") if "vertex_order" in rows.columns else rows
        fill = "toself" if style.get("fill") and len(rows) > 2 else None
        fig.add_trace(
            go.Scattermapbox(
                lon=rows["lon"],
                lat=rows["lat"],
                mode="lines",
                fill=fill,
                fillcolor=style.get("fill"),
                name=label,
                legendgroup=label,
                showlegend=showlegend,
                line={"color": style["color"], "width": style["width"]},
                hovertemplate=f"<b>{label}</b><br>Public context layer<extra></extra>",
            )
        )
        showlegend = False
        count += 1
    return count


def add_well_paths(fig: go.Figure, paths: pd.DataFrame) -> int:
    if paths.empty:
        return 0
    count = 0
    for api_number, rows in paths.groupby("api_number", dropna=False):
        label = f"well path API {api_number}"
        has_tvd = "tvd_ft" in rows.columns
        fig.add_trace(
            go.Scattermapbox(
                lon=rows["longitude"],
                lat=rows["latitude"],
                mode="lines",
                name=label,
                legendgroup="public directional well paths",
                showlegend=count == 0,
                line={"color": "rgba(6, 95, 70, 0.72)", "width": 2.1},
                customdata=rows[["measured_depth_ft", "tvd_ft"]] if has_tvd else rows[["measured_depth_ft"]],
                hovertemplate=(
                    f"<b>{label}</b><br>MD: %{{customdata[0]:,.0f}} ft"
                    "<br>TVD: %{customdata[1]:,.0f} ft<extra></extra>"
                ) if has_tvd else f"<b>{label}</b><br>MD: %{{customdata[0]:,.0f}} ft<extra></extra>",
            )
        )
        count += 1
    return count


def add_focus_points(fig: go.Figure, points: pd.DataFrame) -> None:
    for _, row in points.iterrows():
        label = str(row.get("well_label", "Project well"))
        fig.add_trace(
            go.Scattermapbox(
                lon=[row["longitude"]],
                lat=[row["latitude"]],
                mode="markers+text",
                name=label,
                text=[label],
                textposition="top center",
                marker={
                    "size": 14,
                    "color": row.get("marker_color", "#0f766e"),
                    "opacity": 0.96,
                    "line": {"color": "white", "width": 2},
                },
                hovertemplate=(
                    f"<b>{label}</b><br>Role: {row.get('map_role', 'project focus marker')}"
                    f"<br>Note: {row.get('coordinate_note', 'public context marker')}<extra></extra>"
                ),
            )
        )


def build_focused_project_map(
    points: pd.DataFrame,
    paths: pd.DataFrame,
    context: pd.DataFrame,
    show_well_paths: bool,
    show_assessment_units: bool,
    show_fields_roads_taps: bool,
    show_faults_geology: bool,
    show_seismic: bool,
    show_extent: bool,
) -> tuple[go.Figure, dict[str, int]]:
    fig = go.Figure()
    counts: dict[str, int] = {}

    if show_assessment_units:
        counts["assessment_units"] = add_context_layer(fig, context, ["assessment", "au"], "Hydrate assessment-unit context", "assessment")
    if show_fields_roads_taps:
        counts["fields"] = add_context_layer(fig, context, ["field", "unit", "pool"], "Field / unit outline", "field")
        counts["roads"] = add_context_layer(fig, context, ["road"], "Road corridor", "road")
        counts["taps"] = add_context_layer(fig, context, ["taps", "pipeline"], "TAPS / pipeline corridor", "taps")
    if show_faults_geology:
        counts["faults"] = add_context_layer(fig, context, ["fault"], "Faults", "fault")
        counts["folds"] = add_context_layer(fig, context, ["fold"], "Fold axes", "fold")
        counts["contacts"] = add_context_layer(fig, context, ["contact", "geology"], "Contacts / geology lines", "contact")
    if show_seismic:
        counts["seismic_2d"] = add_context_layer(fig, context, ["seismic_2d", "2d_seismic"], "2D seismic line", "seismic_2d")
        counts["seismic_3d"] = add_context_layer(fig, context, ["seismic_3d", "3d_seismic"], "3D seismic footprint", "seismic_3d")
    if show_extent:
        counts["extent"] = add_context_layer(fig, context, ["extent", "boundary"], "North Slope study boundary", "extent")
    if show_well_paths:
        counts["well_paths"] = add_well_paths(fig, paths)

    add_focus_points(fig, points)

    all_lats = list(points["latitude"])
    all_lons = list(points["longitude"])
    if show_well_paths and not paths.empty:
        all_lats.extend(paths["latitude"].tolist())
        all_lons.extend(paths["longitude"].tolist())
    center_lat = float(pd.Series(all_lats).median()) if all_lats else 70.45
    center_lon = float(pd.Series(all_lons).median()) if all_lons else -148.7

    fig.update_layout(
        title={
            "text": "Focused project well map: four anchors, well paths, and public context layers",
            "x": 0.01,
            "font": {"size": 18},
        },
        height=710,
        margin={"l": 0, "r": 0, "t": 54, "b": 0},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.01, "xanchor": "left", "x": 0, "font": {"size": 10}},
        mapbox={"style": "open-street-map", "center": {"lat": center_lat, "lon": center_lon}, "zoom": 7.4},
    )
    return fig, counts


def available_layer_summary(context: pd.DataFrame) -> pd.DataFrame:
    if context.empty or "layer_name" not in context.columns:
        return pd.DataFrame(columns=["layer_name", "features", "vertices"])
    return (
        context.groupby("layer_name", dropna=False)
        .agg(features=("feature_id", "nunique"), vertices=("lat", "size"))
        .reset_index()
        .sort_values(["layer_name"])
    )


st.set_page_config(page_title="Focused Project Well Map", layout="wide")
st.markdown("## Focused Project Well Map")
st.caption(
    "Interactive Slide 2 companion: project wells, public directional paths, stability/geology context, and optional seismic. "
    "Map context only; stability and location context are not hydrate proof, occurrence labels, or saturation predictions."
)

points = load_focus_points(str(FOCUS_POINTS_PATH))
paths = load_well_paths(str(WELL_PATHS_PATH))
context = load_master_context(str(MASTER_2D_PATH))

control_cols = st.columns([1.2, 1.2, 1.2, 1.2, 1.2, 1.2])
show_well_paths = control_cols[0].checkbox("well paths", value=True)
show_assessment_units = control_cols[1].checkbox("hydrate AU context", value=True)
show_fields_roads_taps = control_cols[2].checkbox("fields / roads / TAPS", value=True)
show_faults_geology = control_cols[3].checkbox("faults / geology", value=False)
show_seismic = control_cols[4].checkbox("seismic coverage", value=False)
show_extent = control_cols[5].checkbox("study boundary", value=True)

fig, counts = build_focused_project_map(
    points,
    paths,
    context,
    show_well_paths,
    show_assessment_units,
    show_fields_roads_taps,
    show_faults_geology,
    show_seismic,
    show_extent,
)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True, "responsive": True})

metric_cols = st.columns(4)
metric_cols[0].metric("Focus markers", f"{len(points):,}")
metric_cols[1].metric("Public path APIs", f"{paths['api_number'].nunique() if not paths.empty else 0:,}")
metric_cols[2].metric("Path stations", f"{len(paths):,}")
metric_cols[3].metric("Context layers found", f"{context['layer_name'].nunique() if not context.empty and 'layer_name' in context.columns else 0:,}")

st.markdown("### Updated legend")
st.markdown(
    """
- **Project focus markers:** MTE / Mt. Elbert, IGS / Ignik Sikumi, Hydrate-01, and HYDRATE 02.
- **Public well paths:** simplified public directional-survey station paths where available.
- **Hydrate AU context:** USGS/public assessment-unit outlines when present in the committed atlas layer table.
- **Fields / roads / TAPS:** shown only if matching public layer names exist in the local checkout.
- **Faults / geology:** optional; intended for DGGS/USGS geology layers staged through OSL and exported as public-safe derivatives.
- **Seismic coverage:** optional and off by default so the four-well map stays readable.
"""
)
st.warning(
    "Coordinate and label caveat: MTE and IGS are verified public project anchors, but Hydrate-01/HYDRATE 02 remain working labels until the refined workbook metadata is separately verified."
)

with st.expander("Layer audit and OSL upgrade targets", expanded=False):
    st.write("Context-layer traces added in the current view:")
    st.dataframe(pd.DataFrame([{"layer_group": k, "features_drawn": v} for k, v in counts.items()]), use_container_width=True, hide_index=True)
    st.write("Available committed 2D master layers:")
    st.dataframe(available_layer_summary(context), use_container_width=True, hide_index=True)
    st.markdown(
        """
**Next OSL layer candidates:** DGGS/USGS faults, contacts, fold axes, geologic map units, field/unit outlines, roads, and TAPS/pipeline corridors. Keep raw shapefiles in `data/source_library/`; commit only public-safe derived GeoJSON/Parquet/CSV products.
"""
    )

with st.expander("Download public map inputs", expanded=False):
    if not points.empty:
        st.download_button("Download focus markers CSV", points.to_csv(index=False).encode("utf-8"), file_name=FOCUS_POINTS_PATH.name, mime="text/csv")
    if not paths.empty:
        st.download_button("Download simplified public well paths CSV", paths.to_csv(index=False).encode("utf-8"), file_name=WELL_PATHS_PATH.name, mime="text/csv")
    if MASTER_3D_PATH.exists():
        st.info("3D structure product detected. Use the Structural Explorer page for the full 3D surface view; this page keeps the 2D focus map readable.")
    else:
        st.info("3D structure product was not found in this checkout. Run the structural surface build before adding a 2D structure footprint overlay.")
