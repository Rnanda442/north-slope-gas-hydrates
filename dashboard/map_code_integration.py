from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

from dashboard import map_v2


PRIMARY_WELL_CASES = ["MTE", "IGS", "Hydrate-01", "HYDRATE 02"]
PHASE_CURVE_RELATIVE_PATH = (
    Path("data")
    / "public_stability_products"
    / "phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1.csv"
)
# Extent used by the code-built slide/reference map so the website view matches
# the map Ro pointed to instead of defaulting to the full North Slope boundary.
CODED_MAP_LON_RANGE = [-155.85, -145.75]
CODED_MAP_LAT_RANGE = [69.10, 71.02]
CODED_FIELD_LABELS = [
    {"label": "Great Mooses Tooth", "lon": -153.15, "lat": 70.14},
    {"label": "Colville River", "lon": -151.35, "lat": 70.33},
    {"label": "Pikka", "lon": -150.55, "lat": 70.42},
    {"label": "Kuparuk River", "lon": -149.80, "lat": 70.28},
    {"label": "Milne Point", "lon": -149.50, "lat": 70.57},
    {"label": "Nikaitchuq", "lon": -149.35, "lat": 70.73},
    {"label": "Prudhoe Bay", "lon": -148.62, "lat": 70.25},
    {"label": "Northstar", "lon": -147.50, "lat": 70.64},
]
CODED_REGIONAL_LABELS = [
    {"label": "Beaufort Sea", "lon": -151.0, "lat": 71.35, "color": "#2563eb"},
    {"label": "NPRA", "lon": -156.0, "lat": 70.25, "color": "#334155"},
    {"label": "Central North Slope fields", "lon": -150.05, "lat": 70.62, "color": "#0f766e"},
    {"label": "Brooks Range", "lon": -151.8, "lat": 68.25, "color": "#7c2d12"},
    {"label": "ANWR", "lon": -143.5, "lat": 69.55, "color": "#334155"},
]
CODED_CORRIDOR_LINES = [
    {
        "name": "TAPS / Dalton corridor",
        "lon": [-148.66, -148.56, -148.50, -148.45, -148.38, -148.34],
        "lat": [70.38, 70.13, 69.88, 69.63, 69.37, 69.12],
        "color": "#92400e",
        "width": 3.2,
        "dash": "solid",
    },
    {
        "name": "Public field trend guide",
        "lon": [-153.40, -152.20, -150.85, -149.60, -148.55, -147.25],
        "lat": [70.04, 70.21, 70.33, 70.43, 70.41, 70.34],
        "color": "rgba(15, 118, 110, 0.62)",
        "width": 2.2,
        "dash": "dot",
    },
]


def _as_number(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _primary_cases(case_index: pd.DataFrame) -> pd.DataFrame:
    if case_index.empty or "well_case" not in case_index.columns:
        return pd.DataFrame()
    frame = case_index[case_index["well_case"].isin(PRIMARY_WELL_CASES)].copy()
    frame = frame[frame["case_role"].isin(map_v2.PRIMARY_CASE_ROLES)].copy()
    frame["well_case"] = pd.Categorical(frame["well_case"], PRIMARY_WELL_CASES, ordered=True)
    return frame.sort_values("well_case")


def _case_rows_for_map(case_index: pd.DataFrame, show_optional_anchors: bool) -> pd.DataFrame:
    if show_optional_anchors:
        return case_index.copy()
    return _primary_cases(case_index)


def _map_context(app_module) -> pd.DataFrame:
    master_2d = getattr(app_module, "MASTER_2D", None)
    columns = ["layer_name", "feature_id", "vertex_order", "lon", "lat", "depth_m", "au_name"]
    if master_2d is not None and Path(master_2d).exists():
        return pd.read_parquet(Path(master_2d), columns=columns).copy()
    return app_module.load_regional_context().copy()


def _sample_rows(app_module, frame: pd.DataFrame, max_rows: int) -> pd.DataFrame:
    if hasattr(app_module, "sample_rows"):
        return app_module.sample_rows(frame, max_rows)
    if len(frame) <= max_rows:
        return frame
    step = max(1, len(frame) // max_rows)
    return frame.iloc[::step].head(max_rows)


def _add_frame_lines(
    figure: go.Figure,
    app_module,
    context: pd.DataFrame,
    layer_name: str,
    trace_name: str,
    color: str,
    width: float,
    max_features: int,
    max_points_per_feature: int,
    fill: bool = False,
) -> None:
    layer = context[context["layer_name"].eq(layer_name)].copy()
    if layer.empty:
        return
    layer["lon"] = _as_number(layer["lon"])
    layer["lat"] = _as_number(layer["lat"])
    layer = layer.dropna(subset=["feature_id", "vertex_order", "lon", "lat"])
    if layer.empty:
        return
    feature_ids = layer["feature_id"].drop_duplicates().tolist()
    if len(feature_ids) > max_features:
        step = max(1, len(feature_ids) // max_features)
        feature_ids = feature_ids[::step][:max_features]
    layer = layer[layer["feature_id"].isin(feature_ids)]
    showlegend = True
    for _, rows in layer.groupby("feature_id", sort=False):
        rows = rows.sort_values("vertex_order")
        rows = _sample_rows(app_module, rows, max_points_per_feature)
        figure.add_trace(
            go.Scatter(
                x=rows["lon"],
                y=rows["lat"],
                mode="lines",
                name=trace_name,
                showlegend=showlegend,
                fill="toself" if fill else None,
                fillcolor="rgba(234, 88, 12, 0.10)" if fill else None,
                line={"color": color, "width": width},
                hovertemplate=f"<b>{trace_name}</b><extra></extra>",
            )
        )
        showlegend = False


def _add_coded_source_layers(figure: go.Figure, map_mode: str) -> None:
    if map_mode == "Full North Slope context":
        labels = CODED_REGIONAL_LABELS
    else:
        labels = CODED_FIELD_LABELS
        for line in CODED_CORRIDOR_LINES:
            figure.add_trace(
                go.Scatter(
                    x=line["lon"],
                    y=line["lat"],
                    mode="lines",
                    name=line["name"],
                    line={
                        "color": line["color"],
                        "width": line["width"],
                        "dash": line["dash"],
                    },
                    hovertemplate=f"<b>{line['name']}</b><br>Code-built context guide<extra></extra>",
                )
            )
    for label in labels:
        figure.add_annotation(
            x=label["lon"],
            y=label["lat"],
            text=label["label"],
            showarrow=False,
            font={"size": 11, "color": label.get("color", "#334155")},
            bgcolor="rgba(255,255,255,0.76)",
            bordercolor="rgba(148,163,184,0.55)",
            borderpad=3,
        )


def _axis_override(
    figure: go.Figure,
    case_index: pd.DataFrame,
    map_mode: str,
) -> None:
    if map_mode == "Code-built source map":
        lon_range, lat_range = CODED_MAP_LON_RANGE, CODED_MAP_LAT_RANGE
    elif map_mode == "Four-well close-up":
        primary = _primary_cases(case_index)
        if primary.empty:
            return
        lon_values = _as_number(primary["bottomhole_longitude"])
        lat_values = _as_number(primary["bottomhole_latitude"])
        lon_pad = max(0.16, float(lon_values.max() - lon_values.min()) * 0.95)
        lat_pad = max(0.08, float(lat_values.max() - lat_values.min()) * 0.95)
        lon_range = [float(lon_values.min()) - lon_pad, float(lon_values.max()) + lon_pad]
        lat_range = [float(lat_values.min()) - lat_pad, float(lat_values.max()) + lat_pad]
    else:
        return

    figure.update_xaxes(range=lon_range)
    figure.update_yaxes(range=lat_range)
    height = 690 if map_mode == "Code-built source map" else 650
    figure.update_layout(
        title={
            "text": f"North Slope public 2D map: {map_mode}",
            "x": 0.01,
            "font": {"size": 17},
        },
        height=height,
        plot_bgcolor="#eef7f8",
        legend={"orientation": "h", "y": -0.14, "x": 0, "font": {"size": 10}},
    )


def _phase_curve(project_root: Path) -> pd.DataFrame:
    path = project_root / PHASE_CURVE_RELATIVE_PATH
    if not path.exists():
        return pd.DataFrame()
    curve = pd.read_csv(path)
    for column in ["source_depth_m", "equilibrium_temperature_c"]:
        curve[column] = _as_number(curve[column])
    return curve.dropna(subset=["source_depth_m", "equilibrium_temperature_c"])


def build_hydrate_stability_inset(project_root: Path) -> go.Figure:
    curve = _phase_curve(project_root)
    figure = go.Figure()
    if not curve.empty:
        figure.add_trace(
            go.Scatter(
                x=curve["equilibrium_temperature_c"],
                y=curve["source_depth_m"],
                mode="lines",
                name="100% methane, 5 ppt salinity",
                line={"color": "#111827", "width": 3},
                hovertemplate=(
                    "Hydrate stability curve<br>Temperature: %{x:.2f} °C"
                    "<br>Depth: %{y:.0f} m<extra></extra>"
                ),
            )
        )
    depths = list(range(0, 3001, 250))
    for gradient, color in [(1.4, "#7c3aed"), (2.0, "#2563eb"), (3.2, "#be123c")]:
        temps = [-10 + (gradient / 100) * depth for depth in depths]
        figure.add_trace(
            go.Scatter(
                x=temps,
                y=depths,
                mode="lines",
                name=f"{gradient:.1f} °C/100 m gradient",
                line={"color": color, "width": 1.8, "dash": "dash"},
                hovertemplate=(
                    f"Geothermal gradient {gradient:.1f} °C/100 m"
                    "<br>Temperature: %{x:.2f} °C<br>Depth: %{y:.0f} m<extra></extra>"
                ),
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
                hovertemplate=f"Permafrost depth marker<br>{depth} m<extra></extra>",
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


def build_interactive_code_map(
    app_module,
    case_index: pd.DataFrame,
    map_mode: str,
    show_background_wells: bool,
    show_assessment_units: bool,
    show_coded_source_layers: bool,
    show_seismic_context: bool,
    show_optional_anchors: bool,
) -> go.Figure:
    context = _map_context(app_module)
    case_rows = _case_rows_for_map(case_index, show_optional_anchors)
    base_focus = map_mode == "Four-well close-up"
    figure = map_v2.build_four_well_2d_context_figure(
        app_module,
        case_rows,
        focus_mode=base_focus,
        show_assessment_units=show_assessment_units,
        show_background_wells=show_background_wells,
        show_associated_wells=show_optional_anchors,
    )

    if show_seismic_context:
        _add_frame_lines(
            figure,
            app_module,
            context,
            "seismic_2d",
            "2D seismic coverage",
            "rgba(14, 165, 233, 0.28)",
            0.7,
            max_features=90,
            max_points_per_feature=260,
        )
        _add_frame_lines(
            figure,
            app_module,
            context,
            "seismic_3d_inventory",
            "3D seismic footprint",
            "rgba(234, 88, 12, 0.50)",
            1.0,
            max_features=36,
            max_points_per_feature=320,
            fill=True,
        )

    if show_coded_source_layers:
        _add_coded_source_layers(figure, map_mode)

    _axis_override(figure, case_index, map_mode)
    return figure


def render_regional_atlas_v3(app_module) -> None:
    st = app_module.st
    project_root = app_module.PROJECT_ROOT
    case_index = map_v2.load_four_well_case_index(project_root)
    context = _map_context(app_module)
    wells = app_module.load_north_slope_wells()
    primary_cases = _primary_cases(case_index)
    optional_cases = (
        case_index[~case_index["well_case"].isin(PRIMARY_WELL_CASES)].copy()
        if not case_index.empty
        else pd.DataFrame()
    )

    st.markdown('<div class="atlas-kicker">Regional context</div>', unsafe_allow_html=True)
    st.title("Regional 2D Map")
    st.write(
        "The code-built North Slope map is now integrated as the interactive website map. "
        "It is centered on the correct four project wells: MTE / Mount Elbert, IGS / Ignik Sikumi, "
        "Hydrate-01, and HYDRATE 02."
    )
    st.warning(
        "Public-source context only: this map does not show approved log rows, core rows, trained models, "
        "predictions, hydrate occurrence, or saturation results."
    )

    metric_cols = st.columns(4)
    metric_cols[0].metric("Correct project wells", f"{len(primary_cases):,}")
    metric_cols[1].metric("Optional associated anchors", f"{len(optional_cases):,}")
    metric_cols[2].metric("Background public wells", f"{len(wells):,}")
    metric_cols[3].metric(
        "Assessment units",
        f"{context[context['layer_name'].eq('assessment_units')]['au_name'].nunique():,}",
    )

    if case_index.empty:
        st.error(
            "The public four-well location index is missing from this checkout. "
            f"Expected: `{map_v2.CASE_INDEX_RELATIVE_PATH.as_posix()}`."
        )

    control_cols = st.columns([1.25, 1, 1, 1, 1, 1])
    with control_cols[0]:
        map_mode = st.radio(
            "Map focus",
            ["Code-built source map", "Four-well close-up", "Full North Slope context"],
            horizontal=False,
            index=0,
        )
    with control_cols[1]:
        show_background_wells = st.checkbox("Public wells", value=True)
    with control_cols[2]:
        show_assessment_units = st.checkbox("Assessment units", value=True)
    with control_cols[3]:
        show_coded_source_layers = st.checkbox("Code-built labels", value=True)
    with control_cols[4]:
        show_seismic_context = st.checkbox("Seismic context", value=True)
    with control_cols[5]:
        show_optional_anchors = st.checkbox("Optional anchors", value=False)

    figure = build_interactive_code_map(
        app_module,
        case_index,
        map_mode=map_mode,
        show_background_wells=show_background_wells,
        show_assessment_units=show_assessment_units,
        show_coded_source_layers=show_coded_source_layers,
        show_seismic_context=show_seismic_context,
        show_optional_anchors=show_optional_anchors,
    )

    if map_mode == "Code-built source map":
        map_col, curve_col = st.columns([2.15, 1])
        with map_col:
            st.plotly_chart(
                figure,
                use_container_width=True,
                config={"displayModeBar": True, "responsive": True},
            )
        with curve_col:
            st.plotly_chart(
                build_hydrate_stability_inset(project_root),
                use_container_width=True,
                config={"displayModeBar": True, "responsive": True},
            )
            st.caption(
                "Inset recreates the source stability concept interactively from the public digitized methane 5 ppt phase curve."
            )
    else:
        st.plotly_chart(
            figure,
            use_container_width=True,
            config={"displayModeBar": True, "responsive": True},
        )

    st.download_button(
        "Download interactive 2D map HTML",
        figure.to_html(include_plotlyjs="cdn", full_html=True).encode("utf-8"),
        "north_slope_code_built_four_well_2d_map.html",
        "text/html",
        key="download_four_well_2d_map_html",
    )

    with st.expander("Correct four project wells", expanded=True):
        if primary_cases.empty:
            st.info("No primary project-well rows are available yet.")
        else:
            display_columns = [
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
            st.dataframe(
                primary_cases[[column for column in display_columns if column in primary_cases.columns]],
                use_container_width=True,
                hide_index=True,
            )

    with st.expander("Optional associated public anchors", expanded=False):
        if optional_cases.empty:
            st.info("No associated public-anchor rows are available.")
        else:
            st.dataframe(
                optional_cases[
                    [
                        column
                        for column in [
                            "well_case",
                            "case_role",
                            "map_label",
                            "verified_public_well_name",
                            "field",
                            "current_status",
                            "website_use_note",
                            "remaining_question",
                        ]
                        if column in optional_cases.columns
                    ]
                ],
                use_container_width=True,
                hide_index=True,
            )
        if not case_index.empty:
            st.download_button(
                "Download four-well public index CSV",
                case_index.to_csv(index=False).encode("utf-8"),
                map_v2.CASE_INDEX_RELATIVE_PATH.name,
                "text/csv",
                key="download_four_well_public_index_csv",
            )

    with st.expander("Reference-only legacy regional scene", expanded=False):
        st.caption(
            "The older full regional map is retained here for broad assessment-unit, seismic, and "
            "notebook-output reference. The code-built four-well map above is now the primary map."
        )
        app_module.render_scene(app_module.REGIONAL_SCENE, height=870)
