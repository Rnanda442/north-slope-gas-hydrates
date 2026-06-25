from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from dashboard import map_v2
from dashboard import mapbox_map as base


# Interactive recreation of the original North Slope drawing.  This file does
# not invent a new map; it forces the website map to use the same approximate
# crop, layer stack, opacity hierarchy, and four-well emphasis as the static
# slide/reference map.
base.CODE_MAP_CENTER = {"lat": 70.36, "lon": -150.20, "zoom": 5.18}
base.FOUR_WELL_CENTER = {"lat": 70.36, "lon": -149.30, "zoom": 7.30}
base.AU_COLORS = {
    "Brookian Foreset-Bottomset": "rgba(20, 123, 133, 0.18)",
    "Brookian Topset": "rgba(52, 144, 220, 0.13)",
    "Beaufortian Strata North": "rgba(245, 158, 11, 0.12)",
    "Beaufortian Strata South": "rgba(245, 158, 11, 0.08)",
    "Ellesmerian Strata North": "rgba(111, 105, 190, 0.13)",
    "Ellesmerian Strata South": "rgba(111, 105, 190, 0.09)",
}
base.AU_LINE_COLORS = {
    "Brookian Foreset-Bottomset": "rgba(20, 123, 133, 0.76)",
    "Brookian Topset": "rgba(52, 144, 220, 0.72)",
    "Beaufortian Strata North": "rgba(217, 119, 6, 0.70)",
    "Beaufortian Strata South": "rgba(180, 83, 9, 0.66)",
    "Ellesmerian Strata North": "rgba(111, 105, 190, 0.72)",
    "Ellesmerian Strata South": "rgba(81, 69, 160, 0.66)",
}
base.FIELD_LABELS = [
    {"label": "Great Mooses Tooth", "lon": -153.12, "lat": 70.15},
    {"label": "Colville River", "lon": -151.47, "lat": 70.44},
    {"label": "Pikka", "lon": -150.52, "lat": 70.53},
    {"label": "Kuparuk River", "lon": -149.90, "lat": 70.20},
    {"label": "Milne Point", "lon": -149.55, "lat": 70.68},
    {"label": "Nikaitchuq", "lon": -149.28, "lat": 70.86},
    {"label": "Prudhoe Bay", "lon": -148.57, "lat": 70.30},
    {"label": "Northstar", "lon": -147.48, "lat": 70.78},
]
base.CORRIDOR_LINES = [
    {
        "name": "TAPS / Dalton corridor",
        "lon": [-148.64, -148.56, -148.49, -148.44, -148.38, -148.34],
        "lat": [70.44, 70.17, 69.91, 69.64, 69.38, 69.12],
        "color": "rgba(146, 64, 14, 0.88)",
        "width": 4,
    },
    {
        "name": "Public field trend guide",
        "lon": [-153.45, -152.25, -150.90, -149.60, -148.50, -147.20],
        "lat": [70.03, 70.20, 70.32, 70.42, 70.40, 70.34],
        "color": "rgba(15, 118, 110, 0.52)",
        "width": 2,
    },
]

TEXT_POSITIONS = {
    "MTE": "top left",
    "IGS": "bottom right",
    "Hydrate-01": "bottom left",
    "HYDRATE 02": "top right",
}
SHORT_LABELS = {
    "MTE": "MTE / Mount Elbert",
    "IGS": "IGS / Ignik Sikumi",
    "Hydrate-01": "Hydrate-01",
    "HYDRATE 02": "HYDRATE 02",
}


def _as_number(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _primary_cases(case_index: pd.DataFrame) -> pd.DataFrame:
    if case_index.empty:
        return pd.DataFrame()
    frame = case_index[
        case_index["well_case"].isin(base.PRIMARY_WELLS)
        & case_index["case_role"].isin(map_v2.PRIMARY_CASE_ROLES)
    ].copy()
    frame["well_case"] = pd.Categorical(frame["well_case"], base.PRIMARY_WELLS, ordered=True)
    return frame.sort_values("well_case")


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


def _replicated_add_context_lines(
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
        rows = base._sample_rows(rows.sort_values("vertex_order"), max_points)
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


def _replicated_add_case_points(figure: go.Figure, rows: pd.DataFrame) -> None:
    rows = _with_plot_locations(rows)
    if rows.empty:
        return
    primary = rows[rows["well_case"].isin(base.PRIMARY_WELLS)].copy()
    optional = rows[~rows["well_case"].isin(base.PRIMARY_WELLS)].copy()

    for row in primary.itertuples(index=False):
        well_case = str(row.well_case)
        color = base.WELL_COLORS.get(well_case, "#0f172a")
        label = SHORT_LABELS.get(well_case, str(row.map_label))
        position = TEXT_POSITIONS.get(well_case, "top right")
        figure.add_trace(
            go.Scattermapbox(
                lon=[row.plot_lon],
                lat=[row.plot_lat],
                mode="text",
                showlegend=False,
                text=[label],
                textposition=position,
                textfont={"size": 16, "color": "#ffffff"},
                hoverinfo="skip",
            )
        )
        figure.add_trace(
            go.Scattermapbox(
                lon=[row.plot_lon],
                lat=[row.plot_lat],
                mode="markers+text",
                name=label,
                showlegend=True,
                marker={"size": 16, "color": color, "opacity": 0.98},
                text=[label],
                textposition=position,
                textfont={"size": 12, "color": "#0f172a"},
                customdata=[
                    [
                        row.verified_public_well_name,
                        row.field,
                        row.current_status,
                        row.true_vertical_depth_ft,
                        row.driller_total_depth_ft,
                        row.evidence_status,
                        row.website_use_note,
                    ]
                ],
                hovertemplate=(
                    f"<b>{label}</b><br>"
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

    if optional.empty:
        return
    for role, group in optional.groupby("case_role", dropna=False):
        role_key = str(role)
        figure.add_trace(
            go.Scattermapbox(
                lon=group["plot_lon"],
                lat=group["plot_lat"],
                mode="markers",
                showlegend=False,
                name=base.ROLE_LABELS.get(role_key, role_key),
                marker={"size": 8, "color": base.ROLE_COLORS.get(role_key, "#475569"), "opacity": 0.70},
                text=group["map_label"],
                hovertemplate="<b>%{text}</b><br>Optional associated public anchor<extra></extra>",
            )
        )


def _add_static_style_backdrop(figure: go.Figure) -> None:
    """Add pale ocean/land rectangles to mimic the original drawing's quiet base."""
    # The basemap is still there for interactivity, but these fills make the map
    # read more like the original static drawing and less like a generic web map.
    figure.add_trace(
        go.Scattermapbox(
            lon=[-157.2, -145.4, -145.4, -157.2, -157.2],
            lat=[71.15, 71.15, 68.90, 68.90, 71.15],
            mode="lines",
            fill="toself",
            fillcolor="rgba(218, 235, 239, 0.32)",
            line={"color": "rgba(218,235,239,0.0)", "width": 0},
            showlegend=False,
            hoverinfo="skip",
            name="Pale map backdrop",
        )
    )


def build_reference_replicated_map(
    app_module,
    case_index: pd.DataFrame,
    mode: str,
    show_background_wells: bool,
    show_assessment_units: bool,
    show_labels: bool,
    show_seismic: bool,
    show_optional: bool,
) -> go.Figure:
    context = base._context(app_module)
    rows = case_index.copy() if show_optional else _primary_cases(case_index)
    center = base._center_for_mode(mode, case_index)
    figure = go.Figure()

    # Original drawing order: quiet base -> AU/geology fills -> seismic/unit
    # outlines -> boundary/corridor -> labels -> project wells.
    _add_static_style_backdrop(figure)
    if show_assessment_units:
        base._add_assessment_units(figure, context, True)
    if show_seismic:
        _replicated_add_context_lines(
            figure,
            context,
            "seismic_3d_inventory",
            "3D seismic / public footprint",
            "rgba(234,88,12,0.46)",
            1.0,
            max_features=80,
            max_points=320,
            fill="toself",
            fillcolor="rgba(234,88,12,0.10)",
        )
        _replicated_add_context_lines(
            figure,
            context,
            "seismic_2d",
            "2D seismic coverage",
            "rgba(14,165,233,0.34)",
            0.75,
            max_features=180,
            max_points=240,
        )
    _replicated_add_context_lines(figure, context, "extent", "North Slope study boundary", "#0f172a", 2.2, 8, 50)
    if show_labels:
        base._add_coded_labels(figure, mode, True)
    if show_background_wells:
        base._add_background_wells(figure, app_module, mode, True)
    if not rows.empty:
        # Keep paths very subtle; the original screenshot primarily read as points.
        base._add_well_paths(figure, rows)
        _replicated_add_case_points(figure, rows)

    figure.update_layout(
        title={"text": f"North Slope public 2D map: {mode}", "x": 0.01, "font": {"size": 16}},
        height=660 if mode == "Code-built source map" else 650,
        margin={"l": 0, "r": 0, "t": 45, "b": 0},
        paper_bgcolor="white",
        showlegend=False,
        mapbox={
            "style": "carto-positron",
            "center": {"lat": center["lat"], "lon": center["lon"]},
            "zoom": center["zoom"],
            "bearing": 0,
            "pitch": 0,
        },
    )
    return figure


def render_regional_atlas_clean(app_module) -> None:
    st = app_module.st
    project_root = app_module.PROJECT_ROOT
    case_index = map_v2.load_four_well_case_index(project_root)
    context = base._context(app_module)
    primary = _primary_cases(case_index)
    optional = case_index[~case_index["well_case"].isin(base.PRIMARY_WELLS)].copy() if not case_index.empty else pd.DataFrame()

    st.markdown('<div class="atlas-kicker">Regional context</div>', unsafe_allow_html=True)
    st.title("Regional 2D Map")
    st.write(
        "Interactive recreation of the original North Slope drawing: same central crop, same layer order, same field-label logic, and the correct four project wells shown by default."
    )
    st.warning(
        "Public-source context only: this map does not show approved log rows, core rows, trained models, predictions, hydrate occurrence, or saturation results."
    )

    metrics = st.columns(4)
    metrics[0].metric("Correct project wells", f"{len(primary):,}")
    metrics[1].metric("Optional anchors hidden", f"{len(optional):,}")
    metrics[2].metric("Public wells default", "Off")
    metrics[3].metric("Assessment units", f"{context[context['layer_name'].eq('assessment_units')]['au_name'].nunique():,}")

    controls = st.columns([1.2, 1, 1, 1, 1, 1])
    with controls[0]:
        mode = st.radio(
            "Map focus",
            ["Code-built source map", "Four-well close-up", "Full North Slope context"],
            index=0,
        )
    with controls[1]:
        show_background_wells = st.checkbox("Public wells", value=False)
    with controls[2]:
        show_assessment_units = st.checkbox("Assessment units", value=True)
    with controls[3]:
        show_labels = st.checkbox("Field labels", value=True)
    with controls[4]:
        show_seismic = st.checkbox("Seismic context", value=True)
    with controls[5]:
        show_optional = st.checkbox("Optional anchors", value=False)

    figure = build_reference_replicated_map(
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
        map_col, curve_col = st.columns([2.25, 1])
        with map_col:
            st.plotly_chart(figure, use_container_width=True, config={"displayModeBar": True, "responsive": True})
        with curve_col:
            st.plotly_chart(base.build_stability_inset(project_root), use_container_width=True, config={"displayModeBar": True, "responsive": True})
            st.caption("Inset recreates the public stability concept interactively from the digitized methane 5 ppt phase curve.")
    else:
        st.plotly_chart(figure, use_container_width=True, config={"displayModeBar": True, "responsive": True})

    st.caption(
        "Default layer stack: pale map backdrop, assessment/geology context, 3D footprints, 2D seismic, study boundary, TAPS/field guide, field labels, and the four project wells."
    )

    st.download_button(
        "Download interactive 2D map HTML",
        figure.to_html(include_plotlyjs="cdn", full_html=True).encode("utf-8"),
        "north_slope_reference_replicated_interactive_map.html",
        "text/html",
        key="download_reference_replicated_map_html",
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

    with st.expander("Reference-only legacy regional scene", expanded=False):
        st.caption("The older generated scene is retained only as a reference. The map above is the primary website map.")
        app_module.render_scene(app_module.REGIONAL_SCENE, height=870)
