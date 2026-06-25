from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

from dashboard import map_v2


PRIMARY_WELLS = ["MTE", "IGS", "Hydrate-01", "HYDRATE 02"]
PHASE_CURVE_RELATIVE_PATH = (
    Path("data")
    / "public_stability_products"
    / "phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1.csv"
)

# Central North Slope view used by the code-built slide/reference map.
CODE_MAP_CENTER = {"lat": 70.28, "lon": -150.12, "zoom": 5.85}
FOUR_WELL_CENTER = {"lat": 70.36, "lon": -149.30, "zoom": 8.15}
FULL_CENTER = {"lat": 70.10, "lon": -151.10, "zoom": 4.65}
CODE_VIEW_BOUNDS = {
    "lon_min": -155.85,
    "lon_max": -145.75,
    "lat_min": 69.10,
    "lat_max": 71.02,
}

WELL_COLORS = {
    "MTE": "#be123c",
    "IGS": "#0f766e",
    "Hydrate-01": "#7c3aed",
    "HYDRATE 02": "#ea580c",
}
ROLE_LABELS = {
    "workbook_header_anchor": "Header-verified project wells",
    "public_source_case": "Public source-case project wells",
    "associated_source_anchor": "Associated public source anchors",
    "associated_test_well": "Associated HYDRATE 02 test wells",
}
ROLE_COLORS = {
    "workbook_header_anchor": "#be123c",
    "public_source_case": "#0f766e",
    "associated_source_anchor": "#475569",
    "associated_test_well": "#b45309",
}
FIELD_LABELS = [
    {"label": "Great Mooses Tooth", "lon": -153.15, "lat": 70.14},
    {"label": "Colville River", "lon": -151.35, "lat": 70.33},
    {"label": "Pikka", "lon": -150.55, "lat": 70.42},
    {"label": "Kuparuk River", "lon": -149.80, "lat": 70.28},
    {"label": "Milne Point", "lon": -149.50, "lat": 70.57},
    {"label": "Nikaitchuq", "lon": -149.35, "lat": 70.73},
    {"label": "Prudhoe Bay", "lon": -148.62, "lat": 70.25},
    {"label": "Northstar", "lon": -147.50, "lat": 70.64},
]
REGIONAL_LABELS = [
    {"label": "Beaufort Sea", "lon": -151.0, "lat": 71.35},
    {"label": "NPRA", "lon": -156.0, "lat": 70.25},
    {"label": "Central North Slope fields", "lon": -150.05, "lat": 70.62},
    {"label": "Brooks Range", "lon": -151.8, "lat": 68.25},
    {"label": "ANWR", "lon": -143.5, "lat": 69.55},
]
CORRIDOR_LINES = [
    {
        "name": "TAPS / Dalton corridor",
        "lon": [-148.66, -148.56, -148.50, -148.45, -148.38, -148.34],
        "lat": [70.38, 70.13, 69.88, 69.63, 69.37, 69.12],
        "color": "#92400e",
        "width": 4,
    },
    {
        "name": "Public field trend guide",
        "lon": [-153.40, -152.20, -150.85, -149.60, -148.55, -147.25],
        "lat": [70.04, 70.21, 70.33, 70.43, 70.41, 70.34],
        "color": "#0f766e",
        "width": 2,
    },
]
AU_COLORS = {
    "Brookian Foreset-Bottomset": "rgba(20, 123, 133, 0.18)",
    "Brookian Topset": "rgba(52, 144, 220, 0.16)",
    "Beaufortian Strata North": "rgba(245, 158, 11, 0.16)",
    "Beaufortian Strata South": "rgba(245, 158, 11, 0.10)",
    "Ellesmerian Strata North": "rgba(111, 105, 190, 0.16)",
    "Ellesmerian Strata South": "rgba(111, 105, 190, 0.10)",
}
AU_LINE_COLORS = {
    "Brookian Foreset-Bottomset": "#147b85",
    "Brookian Topset": "#3490dc",
    "Beaufortian Strata North": "#d97706",
    "Beaufortian Strata South": "#b45309",
    "Ellesmerian Strata North": "#6f69be",
    "Ellesmerian Strata South": "#5145a0",
}


def _as_number(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _sample_rows(frame: pd.DataFrame, max_rows: int) -> pd.DataFrame:
    if len(frame) <= max_rows:
        return frame
    step = max(1, len(frame) // max_rows)
    return frame.iloc[::step].head(max_rows)


def _context(app_module) -> pd.DataFrame:
    columns = ["layer_name", "feature_id", "vertex_order", "lon", "lat", "depth_m", "au_name"]
    master_2d = getattr(app_module, "MASTER_2D", None)
    if master_2d is not None and Path(master_2d).exists():
        return pd.read_parquet(Path(master_2d), columns=columns).copy()
    return app_module.load_regional_context().copy()


def _primary_cases(case_index: pd.DataFrame) -> pd.DataFrame:
    if case_index.empty:
        return pd.DataFrame()
    frame = case_index[
        case_index["well_case"].isin(PRIMARY_WELLS)
        & case_index["case_role"].isin(map_v2.PRIMARY_CASE_ROLES)
    ].copy()
    frame["well_case"] = pd.Categorical(frame["well_case"], PRIMARY_WELLS, ordered=True)
    return frame.sort_values("well_case")


def _case_rows(case_index: pd.DataFrame, show_optional: bool) -> pd.DataFrame:
    if case_index.empty:
        return pd.DataFrame()
    if show_optional:
        return case_index.copy()
    return _primary_cases(case_index)


def _with_plot_locations(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    for column in [
        "bottomhole_latitude",
        "bottomhole_longitude",
        "wellhead_latitude",
        "wellhead_longitude",
        "true_vertical_depth_ft",
        "driller_total_depth_ft",
    ]:
        if column in frame:
            frame[column] = _as_number(frame[column])
    frame["plot_lat"] = frame["bottomhole_latitude"].fillna(frame["wellhead_latitude"])
    frame["plot_lon"] = frame["bottomhole_longitude"].fillna(frame["wellhead_longitude"])
    return frame.dropna(subset=["plot_lat", "plot_lon"])


def _center_for_mode(mode: str, case_index: pd.DataFrame) -> dict[str, float]:
    if mode == "Four-well close-up":
        primary = _with_plot_locations(_primary_cases(case_index))
        if primary.empty:
            return FOUR_WELL_CENTER
        return {
            "lat": float(primary["plot_lat"].median()),
            "lon": float(primary["plot_lon"].median()),
            "zoom": FOUR_WELL_CENTER["zoom"],
        }
    if mode == "Full North Slope context":
        return FULL_CENTER
    return CODE_MAP_CENTER


def _filter_central_extent(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty or "lon" not in frame or "lat" not in frame:
        return frame
    return frame[
        frame["lon"].between(CODE_VIEW_BOUNDS["lon_min"], CODE_VIEW_BOUNDS["lon_max"])
        & frame["lat"].between(CODE_VIEW_BOUNDS["lat_min"], CODE_VIEW_BOUNDS["lat_max"])
    ].copy()


def _add_context_lines(
    figure: go.Figure,
    context: pd.DataFrame,
    layer_name: str,
    name: str,
    color: str,
    width: float,
    max_features: int,
    max_points: int,
    fill: str | None = None,
    fillcolor: str | None = None,
) -> None:
    layer = context[context["layer_name"].eq(layer_name)].copy()
    if layer.empty:
        return
    layer["lon"] = _as_number(layer["lon"])
    layer["lat"] = _as_number(layer["lat"])
    layer = layer.dropna(subset=["feature_id", "vertex_order", "lon", "lat"])
    feature_ids = layer["feature_id"].drop_duplicates().tolist()
    if len(feature_ids) > max_features:
        step = max(1, len(feature_ids) // max_features)
        feature_ids = feature_ids[::step][:max_features]
    layer = layer[layer["feature_id"].isin(feature_ids)]
    showlegend = True
    for _, rows in layer.groupby("feature_id", sort=False):
        rows = _sample_rows(rows.sort_values("vertex_order"), max_points)
        figure.add_trace(
            go.Scattermapbox(
                lon=rows["lon"],
                lat=rows["lat"],
                mode="lines",
                name=name,
                showlegend=showlegend,
                fill=fill,
                fillcolor=fillcolor,
                line={"color": color, "width": width},
                hovertemplate=f"<b>{name}</b><extra></extra>",
            )
        )
        showlegend = False


def _add_assessment_units(figure: go.Figure, context: pd.DataFrame, visible: bool) -> None:
    if not visible:
        return
    units = context[context["layer_name"].eq("assessment_units")].copy()
    if units.empty:
        return
    units["lon"] = _as_number(units["lon"])
    units["lat"] = _as_number(units["lat"])
    units = units.dropna(subset=["feature_id", "vertex_order", "lon", "lat"])
    for au_name, group in units.groupby("au_name", dropna=True):
        showlegend = True
        for _, rows in group.groupby("feature_id"):
            rows = _sample_rows(rows.sort_values("vertex_order"), 900)
            figure.add_trace(
                go.Scattermapbox(
                    lon=rows["lon"],
                    lat=rows["lat"],
                    mode="lines",
                    name=str(au_name),
                    showlegend=showlegend,
                    fill="toself",
                    fillcolor=AU_COLORS.get(str(au_name), "rgba(148,163,184,0.12)"),
                    line={"color": AU_LINE_COLORS.get(str(au_name), "#64748b"), "width": 1.2},
                    hovertemplate="<b>%{fullData.name}</b><br>Assessment-unit context<extra></extra>",
                )
            )
            showlegend = False


def _add_background_wells(figure: go.Figure, app_module, mode: str, visible: bool) -> None:
    if not visible:
        return
    wells = app_module.load_north_slope_wells().copy()
    wells["lon"] = _as_number(wells["lon"])
    wells["lat"] = _as_number(wells["lat"])
    wells = wells.dropna(subset=["lon", "lat"])
    if mode != "Full North Slope context":
        wells = _filter_central_extent(wells)
    wells = _sample_rows(wells.sort_values(["lon", "lat"]), 1500)
    if wells.empty:
        return
    figure.add_trace(
        go.Scattermapbox(
            lon=wells["lon"],
            lat=wells["lat"],
            mode="markers",
            name="Public well background",
            marker={"size": 4, "color": "rgba(15,23,42,0.30)"},
            hovertemplate="Public well<br>Lon/lat: %{lon:.3f}, %{lat:.3f}<extra></extra>",
        )
    )


def _add_coded_labels(figure: go.Figure, mode: str, visible: bool) -> None:
    if not visible:
        return
    labels = REGIONAL_LABELS if mode == "Full North Slope context" else FIELD_LABELS
    if mode != "Full North Slope context":
        for line in CORRIDOR_LINES:
            figure.add_trace(
                go.Scattermapbox(
                    lon=line["lon"],
                    lat=line["lat"],
                    mode="lines",
                    name=line["name"],
                    line={"color": line["color"], "width": line["width"]},
                    hovertemplate=f"<b>{line['name']}</b><br>Code-built context guide<extra></extra>",
                )
            )
    figure.add_trace(
        go.Scattermapbox(
            lon=[item["lon"] for item in labels],
            lat=[item["lat"] for item in labels],
            mode="text",
            name="Map labels",
            text=[item["label"] for item in labels],
            textfont={"size": 12, "color": "#0f172a"},
            hoverinfo="skip",
            showlegend=False,
        )
    )


def _add_well_paths(figure: go.Figure, rows: pd.DataFrame) -> None:
    rows = rows.dropna(
        subset=[
            "wellhead_latitude",
            "wellhead_longitude",
            "bottomhole_latitude",
            "bottomhole_longitude",
        ]
    )
    showlegend = True
    for row in rows.itertuples(index=False):
        figure.add_trace(
            go.Scattermapbox(
                lon=[row.wellhead_longitude, row.bottomhole_longitude],
                lat=[row.wellhead_latitude, row.bottomhole_latitude],
                mode="lines",
                name="Wellhead-to-bottomhole path",
                showlegend=showlegend,
                line={"color": "rgba(15,23,42,0.55)", "width": 2},
                hovertemplate=f"<b>{row.map_label}</b><br>Public WH to BH path<extra></extra>",
            )
        )
        showlegend = False


def _add_case_points(figure: go.Figure, rows: pd.DataFrame) -> None:
    rows = _with_plot_locations(rows)
    if rows.empty:
        return
    for role, group in rows.groupby("case_role", dropna=False):
        role_key = str(role)
        is_primary = group["well_case"].isin(PRIMARY_WELLS)
        color_values = [WELL_COLORS.get(str(well), ROLE_COLORS.get(role_key, "#475569")) for well in group["well_case"]]
        text_values = group["map_label"].where(is_primary, "")
        custom_columns = [
            "verified_public_well_name",
            "field",
            "current_status",
            "true_vertical_depth_ft",
            "driller_total_depth_ft",
            "evidence_status",
            "website_use_note",
        ]
        custom = group[[column for column in custom_columns if column in group.columns]].fillna("")
        figure.add_trace(
            go.Scattermapbox(
                lon=group["plot_lon"],
                lat=group["plot_lat"],
                mode="markers+text",
                name=ROLE_LABELS.get(role_key, role_key),
                marker={"size": [18 if value else 10 for value in is_primary], "color": color_values, "opacity": 0.96},
                text=text_values,
                textposition="top right",
                textfont={"size": 13, "color": "#0f172a"},
                customdata=custom,
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Public well: %{customdata[0]}<br>"
                    "Field: %{customdata[1]}<br>"
                    "Status: %{customdata[2]}<br>"
                    "TVD / TD: %{customdata[3]} / %{customdata[4]} ft<br>"
                    "Evidence: %{customdata[5]}<br>"
                    "Website use: %{customdata[6]}<br>"
                    "Lon/lat: %{lon:.5f}, %{lat:.5f}<extra></extra>"
                ),
            )
        )


def build_north_slope_mapbox_figure(
    app_module,
    case_index: pd.DataFrame,
    mode: str,
    show_background_wells: bool,
    show_assessment_units: bool,
    show_labels: bool,
    show_seismic: bool,
    show_optional_anchors: bool,
) -> go.Figure:
    context = _context(app_module)
    rows = _case_rows(case_index, show_optional_anchors)
    center = _center_for_mode(mode, case_index)
    figure = go.Figure()

    _add_assessment_units(figure, context, show_assessment_units)
    _add_context_lines(figure, context, "extent", "North Slope study boundary", "#0f172a", 2.6, 8, 50)
    if show_seismic:
        _add_context_lines(figure, context, "seismic_2d", "2D seismic coverage", "rgba(14,165,233,0.38)", 0.9, 160, 240)
        _add_context_lines(
            figure,
            context,
            "seismic_3d_inventory",
            "3D seismic footprint",
            "rgba(234,88,12,0.58)",
            1.2,
            50,
            320,
            fill="toself",
            fillcolor="rgba(234,88,12,0.11)",
        )
    _add_background_wells(figure, app_module, mode, show_background_wells)
    _add_coded_labels(figure, mode, show_labels)
    if not rows.empty:
        _add_well_paths(figure, rows)
        _add_case_points(figure, rows)

    figure.update_layout(
        title={"text": f"North Slope interactive 2D map: {mode}", "x": 0.01, "font": {"size": 17}},
        height=715 if mode == "Code-built source map" else 680,
        margin={"l": 0, "r": 0, "t": 54, "b": 0},
        paper_bgcolor="white",
        legend={"orientation": "h", "y": -0.07, "x": 0, "font": {"size": 10}},
        mapbox={
            "style": "carto-positron",
            "center": {"lat": center["lat"], "lon": center["lon"]},
            "zoom": center["zoom"],
            "bearing": 0,
            "pitch": 0,
        },
    )
    return figure


def _phase_curve(project_root: Path) -> pd.DataFrame:
    path = project_root / PHASE_CURVE_RELATIVE_PATH
    if not path.exists():
        return pd.DataFrame()
    curve = pd.read_csv(path)
    curve["source_depth_m"] = _as_number(curve["source_depth_m"])
    curve["equilibrium_temperature_c"] = _as_number(curve["equilibrium_temperature_c"])
    return curve.dropna(subset=["source_depth_m", "equilibrium_temperature_c"])


def build_stability_inset(project_root: Path) -> go.Figure:
    curve = _phase_curve(project_root)
    figure = go.Figure()
    if not curve.empty:
        figure.add_trace(
            go.Scatter(
                x=curve["equilibrium_temperature_c"],
                y=curve["source_depth_m"],
                mode="lines",
                name="100% methane, 5 ppt stability",
                line={"color": "#111827", "width": 3},
            )
        )
    depths = list(range(0, 3001, 250))
    for gradient, color in [(1.4, "#7c3aed"), (2.0, "#2563eb"), (3.2, "#be123c")]:
        figure.add_trace(
            go.Scatter(
                x=[-10 + (gradient / 100) * depth for depth in depths],
                y=depths,
                mode="lines",
                name=f"{gradient:.1f} °C/100 m gradient",
                line={"color": color, "width": 1.8, "dash": "dash"},
            )
        )
    for depth, symbol in [(305, "circle"), (610, "triangle-up"), (914, "diamond")]:
        figure.add_trace(
            go.Scatter(
                x=[-8.8],
                y=[depth],
                mode="markers",
                name=f"Permafrost depth {depth} m",
                marker={"symbol": symbol, "size": 9, "color": "#111827"},
            )
        )
    figure.update_layout(
        title="Interactive stability inset",
        height=365,
        margin={"l": 48, "r": 16, "t": 45, "b": 45},
        xaxis_title="Temperature (°C)",
        yaxis_title="Depth (m)",
        legend={"orientation": "h", "y": -0.30, "x": 0, "font": {"size": 9}},
        paper_bgcolor="white",
        plot_bgcolor="#f8fbfc",
    )
    figure.update_yaxes(autorange="reversed", range=[3000, 0])
    figure.update_xaxes(range=[-12, 30])
    return figure


def render_regional_atlas_mapbox(app_module) -> None:
    st = app_module.st
    project_root = app_module.PROJECT_ROOT
    case_index = map_v2.load_four_well_case_index(project_root)
    context = _context(app_module)
    primary = _primary_cases(case_index)
    optional = case_index[~case_index["well_case"].isin(PRIMARY_WELLS)].copy() if not case_index.empty else pd.DataFrame()

    st.markdown('<div class="atlas-kicker">Regional context</div>', unsafe_allow_html=True)
    st.title("Regional 2D Map")
    st.write(
        "This view replaces the stretched longitude/latitude chart with a true interactive map. "
        "The default view is centered on the same central North Slope map area as the code-built slide reference and shows only the four project wells unless optional anchors are toggled on."
    )
    st.warning(
        "Public-source context only: this map does not show approved log rows, core rows, trained models, predictions, hydrate occurrence, or saturation results."
    )

    metrics = st.columns(4)
    metrics[0].metric("Correct project wells", f"{len(primary):,}")
    metrics[1].metric("Optional anchors hidden", f"{len(optional):,}")
    metrics[2].metric("Background public wells", f"{len(app_module.load_north_slope_wells()):,}")
    metrics[3].metric("Assessment units", f"{context[context['layer_name'].eq('assessment_units')]['au_name'].nunique():,}")

    controls = st.columns([1.25, 1, 1, 1, 1, 1])
    with controls[0]:
        mode = st.radio(
            "Map focus",
            ["Code-built source map", "Four-well close-up", "Full North Slope context"],
            index=0,
        )
    with controls[1]:
        show_background_wells = st.checkbox("Public wells", value=True)
    with controls[2]:
        show_assessment_units = st.checkbox("Assessment units", value=True)
    with controls[3]:
        show_labels = st.checkbox("Field labels", value=True)
    with controls[4]:
        show_seismic = st.checkbox("Seismic context", value=True)
    with controls[5]:
        show_optional = st.checkbox("Optional anchors", value=False)

    figure = build_north_slope_mapbox_figure(
        app_module,
        case_index,
        mode,
        show_background_wells,
        show_assessment_units,
        show_labels,
        show_seismic,
        show_optional,
    )

    if mode == "Code-built source map":
        map_col, curve_col = st.columns([2.15, 1])
        with map_col:
            st.plotly_chart(figure, use_container_width=True, config={"displayModeBar": True, "responsive": True})
        with curve_col:
            st.plotly_chart(build_stability_inset(project_root), use_container_width=True, config={"displayModeBar": True, "responsive": True})
            st.caption("Inset recreates the public stability concept interactively from the digitized methane 5 ppt phase curve.")
    else:
        st.plotly_chart(figure, use_container_width=True, config={"displayModeBar": True, "responsive": True})

    st.download_button(
        "Download interactive 2D map HTML",
        figure.to_html(include_plotlyjs="cdn", full_html=True).encode("utf-8"),
        "north_slope_correct_four_well_interactive_map.html",
        "text/html",
        key="download_correct_four_well_map_html",
    )

    with st.expander("Correct four project wells", expanded=True):
        columns = [
            "well_case",
            "map_label",
            "verified_public_well_name",
            "field",
            "current_status",
            "wellhead_latitude",
            "wellhead_longitude",
            "bottomhole_latitude",
            "bottomhole_longitude",
            "true_vertical_depth_ft",
            "driller_total_depth_ft",
            "evidence_status",
            "workbook_mapping_status",
            "website_use_note",
        ]
        st.dataframe(primary[[column for column in columns if column in primary.columns]], use_container_width=True, hide_index=True)

    with st.expander("Optional associated public anchors", expanded=False):
        if optional.empty:
            st.info("No associated public-anchor rows are available.")
        else:
            columns = ["well_case", "case_role", "map_label", "verified_public_well_name", "field", "current_status", "website_use_note", "remaining_question"]
            st.dataframe(optional[[column for column in columns if column in optional.columns]], use_container_width=True, hide_index=True)
        if not case_index.empty:
            st.download_button(
                "Download four-well public index CSV",
                case_index.to_csv(index=False).encode("utf-8"),
                map_v2.CASE_INDEX_RELATIVE_PATH.name,
                "text/csv",
                key="download_four_well_public_index_csv",
            )

    with st.expander("Reference-only legacy regional scene", expanded=False):
        st.caption("The older generated scene is retained only as a reference. The map above is the primary website map.")
        app_module.render_scene(app_module.REGIONAL_SCENE, height=870)
