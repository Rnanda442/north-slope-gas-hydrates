from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go


CASE_INDEX_RELATIVE_PATH = (
    Path("data")
    / "public_ml_products"
    / "four_well_case_location_index_2026-06-19.csv"
)
PRIMARY_CASE_ROLES = {"workbook_header_anchor", "public_source_case"}
ROLE_STYLES = {
    "workbook_header_anchor": {
        "label": "Header-verified project wells",
        "color": "#be123c",
        "size": 15,
        "symbol": "star",
    },
    "public_source_case": {
        "label": "Public source-case project wells",
        "color": "#0f766e",
        "size": 14,
        "symbol": "diamond",
    },
    "associated_source_anchor": {
        "label": "Associated public source anchors",
        "color": "#475569",
        "size": 10,
        "symbol": "circle-open",
    },
    "associated_test_well": {
        "label": "Associated HYDRATE 02 test wells",
        "color": "#b45309",
        "size": 10,
        "symbol": "square-open",
    },
}
CASE_LABEL_OFFSETS = {
    "MTE": {"lat": 0.030, "lon": -0.120},
    "IGS": {"lat": -0.035, "lon": 0.120},
    "Hydrate-01": {"lat": 0.055, "lon": -0.125},
    "HYDRATE 02": {"lat": -0.050, "lon": 0.130},
}
FOCUS_LABELS = [
    {"label": "Milne Point / Mount Elbert", "lon": -149.47, "lat": 70.49},
    {"label": "Prudhoe Bay / Ignik Sikumi", "lon": -149.34, "lat": 70.37},
    {"label": "Hydrate 01 / 02 test area", "lon": -149.19, "lat": 70.30},
]
REGIONAL_LABELS = [
    {"label": "Beaufort Sea", "lon": -151.0, "lat": 71.35, "color": "#2563eb"},
    {"label": "NPRA", "lon": -156.0, "lat": 70.25, "color": "#334155"},
    {"label": "Central North Slope fields", "lon": -150.05, "lat": 70.62, "color": "#0f766e"},
    {"label": "Brooks Range", "lon": -151.8, "lat": 68.25, "color": "#7c2d12"},
    {"label": "ANWR", "lon": -143.5, "lat": 69.55, "color": "#334155"},
]
AU_COLORS = {
    "Brookian Foreset-Bottomset": "rgba(20, 123, 133, 0.22)",
    "Brookian Topset": "rgba(52, 144, 220, 0.20)",
    "Beaufortian Strata North": "rgba(245, 158, 11, 0.20)",
    "Beaufortian Strata South": "rgba(245, 158, 11, 0.12)",
    "Ellesmerian Strata North": "rgba(111, 105, 190, 0.18)",
    "Ellesmerian Strata South": "rgba(111, 105, 190, 0.11)",
}
AU_LINE_COLORS = {
    "Brookian Foreset-Bottomset": "#147b85",
    "Brookian Topset": "#3490dc",
    "Beaufortian Strata North": "#d97706",
    "Beaufortian Strata South": "#b45309",
    "Ellesmerian Strata North": "#6f69be",
    "Ellesmerian Strata South": "#5145a0",
}


def patch_app(app_module) -> None:
    """Replace the regional 2D atlas renderer with the four-well public map."""

    app_module.render_regional_atlas = lambda: render_regional_atlas_v2(app_module)


def _as_number(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def load_four_well_case_index(project_root: Path) -> pd.DataFrame:
    path = project_root / CASE_INDEX_RELATIVE_PATH
    if not path.exists():
        return pd.DataFrame()
    frame = pd.read_csv(
        path,
        dtype={"permit_number": "string", "api_number": "string", "object_id": "string"},
    )
    for column in [
        "wellhead_latitude",
        "wellhead_longitude",
        "bottomhole_latitude",
        "bottomhole_longitude",
        "true_vertical_depth_ft",
        "driller_total_depth_ft",
    ]:
        if column in frame.columns:
            frame[column] = _as_number(frame[column])
    return frame


def _sample_rows(app_module, frame: pd.DataFrame, max_rows: int) -> pd.DataFrame:
    if hasattr(app_module, "sample_rows"):
        return app_module.sample_rows(frame, max_rows)
    if len(frame) <= max_rows:
        return frame
    step = max(1, len(frame) // max_rows)
    return frame.iloc[::step].head(max_rows)


def _primary_cases(case_index: pd.DataFrame) -> pd.DataFrame:
    if case_index.empty or "case_role" not in case_index.columns:
        return pd.DataFrame()
    return case_index[case_index["case_role"].isin(PRIMARY_CASE_ROLES)].copy()


def _valid_case_locations(case_index: pd.DataFrame) -> pd.DataFrame:
    required = ["bottomhole_latitude", "bottomhole_longitude"]
    if case_index.empty or any(column not in case_index.columns for column in required):
        return pd.DataFrame()
    return case_index.dropna(subset=required).copy()


def _focus_axis_ranges(case_index: pd.DataFrame, extent: pd.DataFrame) -> tuple[list[float], list[float]]:
    locations = _valid_case_locations(case_index)
    if locations.empty:
        lon_values = _as_number(extent["lon"])
        lat_values = _as_number(extent["lat"])
        return [float(lon_values.min()) - 0.7, float(lon_values.max()) + 0.7], [
            float(lat_values.min()) - 0.4,
            float(lat_values.max()) + 0.4,
        ]
    lon_values = _as_number(locations["bottomhole_longitude"])
    lat_values = _as_number(locations["bottomhole_latitude"])
    lon_pad = max(0.16, float(lon_values.max() - lon_values.min()) * 0.95)
    lat_pad = max(0.08, float(lat_values.max() - lat_values.min()) * 0.95)
    return [float(lon_values.min()) - lon_pad, float(lon_values.max()) + lon_pad], [
        float(lat_values.min()) - lat_pad,
        float(lat_values.max()) + lat_pad,
    ]


def _add_assessment_units(figure: go.Figure, app_module, context: pd.DataFrame) -> None:
    assessment_units = context[context["layer_name"] == "assessment_units"]
    for au_name, au_rows in assessment_units.groupby("au_name", dropna=True):
        showlegend = True
        for _, rows in au_rows.groupby("feature_id"):
            rows = _sample_rows(app_module, rows.sort_values("vertex_order"), 900)
            figure.add_trace(
                go.Scatter(
                    x=rows["lon"],
                    y=rows["lat"],
                    mode="lines",
                    fill="toself",
                    name=str(au_name),
                    showlegend=showlegend,
                    fillcolor=AU_COLORS.get(str(au_name), "rgba(148, 163, 184, 0.14)"),
                    line={"color": AU_LINE_COLORS.get(str(au_name), "#64748b"), "width": 1.0},
                    hovertemplate=(
                        "<b>%{fullData.name}</b><br>"
                        "Public geology / assessment-unit context<extra></extra>"
                    ),
                )
            )
            showlegend = False


def _add_background_wells(
    figure: go.Figure,
    app_module,
    focus_mode: bool,
    lon_range: list[float],
    lat_range: list[float],
) -> None:
    wells = app_module.load_north_slope_wells().sort_values(["lon", "lat"]).copy()
    if focus_mode:
        wells = wells[
            wells["lon"].between(lon_range[0], lon_range[1])
            & wells["lat"].between(lat_range[0], lat_range[1])
        ]
        wells = _sample_rows(app_module, wells, 900)
    else:
        wells = _sample_rows(app_module, wells, 1800)
    if wells.empty:
        return
    figure.add_trace(
        go.Scatter(
            x=wells["lon"],
            y=wells["lat"],
            mode="markers",
            name="Public well background",
            marker={"size": 3.0, "color": "rgba(15, 23, 42, 0.30)"},
            hovertemplate=(
                "<b>Public well context</b><br>"
                "Longitude: %{x:.3f}<br>Latitude: %{y:.3f}<extra></extra>"
            ),
        )
    )


def _add_well_paths(figure: go.Figure, case_index: pd.DataFrame) -> None:
    locations = case_index.dropna(
        subset=[
            "wellhead_latitude",
            "wellhead_longitude",
            "bottomhole_latitude",
            "bottomhole_longitude",
        ]
    ).copy()
    if locations.empty:
        return
    for index, row in enumerate(locations.itertuples(index=False)):
        figure.add_trace(
            go.Scatter(
                x=[row.wellhead_longitude, row.bottomhole_longitude],
                y=[row.wellhead_latitude, row.bottomhole_latitude],
                mode="lines",
                name="Wellhead to bottomhole path",
                showlegend=index == 0,
                line={"color": "rgba(15, 23, 42, 0.45)", "width": 1.2, "dash": "dot"},
                hovertemplate=(
                    f"<b>{row.map_label}</b><br>"
                    "Public WH→BH line from Alaska well metadata<extra></extra>"
                ),
            )
        )


def _add_case_points(
    figure: go.Figure,
    case_index: pd.DataFrame,
    show_associated: bool,
) -> None:
    locations = _valid_case_locations(case_index)
    if locations.empty:
        return
    if not show_associated:
        locations = locations[locations["case_role"].isin(PRIMARY_CASE_ROLES)].copy()
    for role, rows in locations.groupby("case_role", dropna=False):
        style = ROLE_STYLES.get(
            str(role),
            {"label": str(role), "color": "#475569", "size": 9, "symbol": "circle"},
        )
        custom_columns = [
            "verified_public_well_name",
            "field",
            "current_status",
            "true_vertical_depth_ft",
            "driller_total_depth_ft",
            "evidence_status",
            "website_use_note",
        ]
        custom = rows[[column for column in custom_columns if column in rows.columns]].fillna("")
        figure.add_trace(
            go.Scatter(
                x=rows["bottomhole_longitude"],
                y=rows["bottomhole_latitude"],
                mode="markers",
                name=style["label"],
                marker={
                    "size": style["size"],
                    "color": style["color"],
                    "symbol": style["symbol"],
                    "line": {"color": "white", "width": 1.3},
                },
                text=rows["map_label"],
                customdata=custom,
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Public well: %{customdata[0]}<br>"
                    "Field: %{customdata[1]}<br>"
                    "Status: %{customdata[2]}<br>"
                    "TVD / TD: %{customdata[3]} / %{customdata[4]} ft<br>"
                    "Evidence: %{customdata[5]}<br>"
                    "Website use: %{customdata[6]}<br>"
                    "Bottomhole lon/lat: %{x:.5f}, %{y:.5f}<extra></extra>"
                ),
            )
        )


def _add_case_labels(figure: go.Figure, case_index: pd.DataFrame) -> None:
    primary = _valid_case_locations(_primary_cases(case_index))
    for row in primary.itertuples(index=False):
        offset = CASE_LABEL_OFFSETS.get(
            str(row.well_case),
            {"lon": 0.08, "lat": 0.035},
        )
        figure.add_annotation(
            x=float(row.bottomhole_longitude) + offset["lon"],
            y=float(row.bottomhole_latitude) + offset["lat"],
            text=str(row.map_label),
            showarrow=True,
            ax=0,
            ay=0,
            arrowhead=2,
            arrowsize=0.8,
            arrowwidth=1.0,
            arrowcolor="#334155",
            font={"size": 12, "color": "#0f172a"},
            bgcolor="rgba(255,255,255,0.82)",
            bordercolor="rgba(148,163,184,0.7)",
            borderpad=3,
        )


def build_four_well_2d_context_figure(
    app_module,
    case_index: pd.DataFrame,
    focus_mode: bool,
    show_assessment_units: bool,
    show_background_wells: bool,
    show_associated_wells: bool,
) -> go.Figure:
    context = app_module.load_regional_context()
    extent = context[context["layer_name"] == "extent"].sort_values("vertex_order")
    figure = go.Figure()

    if show_assessment_units:
        _add_assessment_units(figure, app_module, context)

    lon_range, lat_range = _focus_axis_ranges(case_index, extent) if focus_mode else (
        [float(_as_number(extent["lon"]).min()) - 0.7, float(_as_number(extent["lon"]).max()) + 0.7],
        [float(_as_number(extent["lat"]).min()) - 0.4, float(_as_number(extent["lat"]).max()) + 0.4],
    )

    if show_background_wells:
        _add_background_wells(figure, app_module, focus_mode, lon_range, lat_range)

    if not extent.empty:
        figure.add_trace(
            go.Scatter(
                x=extent["lon"],
                y=extent["lat"],
                mode="lines",
                name="North Slope study boundary",
                line={"color": "#0f172a", "width": 2.4},
                hovertemplate="<b>North Slope study boundary</b><extra></extra>",
            )
        )

    if not case_index.empty:
        _add_well_paths(figure, case_index)
        _add_case_points(figure, case_index, show_associated_wells)
        _add_case_labels(figure, case_index)

    for label in FOCUS_LABELS if focus_mode else REGIONAL_LABELS:
        figure.add_annotation(
            x=label["lon"],
            y=label["lat"],
            text=label["label"],
            showarrow=False,
            font={"size": 11, "color": label.get("color", "#334155")},
            bgcolor="rgba(255,255,255,0.70)",
            bordercolor="rgba(148,163,184,0.50)",
            borderpad=3,
        )

    title_suffix = "four-well focus" if focus_mode else "regional context"
    figure.update_layout(
        title={
            "text": f"North Slope public 2D map: {title_suffix}",
            "x": 0.01,
            "font": {"size": 17},
        },
        height=650 if focus_mode else 620,
        margin={"l": 12, "r": 12, "t": 56, "b": 26},
        paper_bgcolor="white",
        plot_bgcolor="#f8fbfc",
        legend={"orientation": "h", "y": -0.10, "x": 0, "font": {"size": 10}},
        xaxis={
            "title": "Longitude",
            "range": lon_range,
            "showgrid": True,
            "gridcolor": "rgba(148,163,184,0.22)",
            "zeroline": False,
        },
        yaxis={
            "title": "Latitude",
            "range": lat_range,
            "showgrid": True,
            "gridcolor": "rgba(148,163,184,0.22)",
            "zeroline": False,
            "scaleanchor": "x",
            "scaleratio": 0.55,
        },
    )
    return figure


def render_regional_atlas_v2(app_module) -> None:
    st = app_module.st
    project_root = app_module.PROJECT_ROOT
    case_index = load_four_well_case_index(project_root)
    context = app_module.load_regional_context()
    wells = app_module.load_north_slope_wells()
    primary_cases = _primary_cases(case_index)
    associated_cases = case_index[~case_index["case_role"].isin(PRIMARY_CASE_ROLES)].copy() if not case_index.empty else pd.DataFrame()

    st.markdown('<div class="atlas-kicker">Regional context</div>', unsafe_allow_html=True)
    st.title("Regional 2D Map")
    st.write(
        "A cleaned public map focused on the North Slope wells currently driving the project: "
        "MTE, IGS, Hydrate-01, and HYDRATE 02. Seismic and heavy regional context are kept out "
        "of the main view so the four project wells and their public wellhead-to-bottomhole paths "
        "are readable."
    )
    st.warning(
        "Public-source context only: this map does not show approved log rows, core rows, trained models, "
        "predictions, hydrate occurrence, or saturation results."
    )

    metric_cols = st.columns(4)
    metric_cols[0].metric("Project focus wells", f"{len(primary_cases):,}")
    metric_cols[1].metric("Associated public anchors", f"{len(associated_cases):,}")
    metric_cols[2].metric("Background public wells", f"{len(wells):,}")
    metric_cols[3].metric(
        "Assessment units",
        f"{context[context['layer_name'].eq('assessment_units')]['au_name'].nunique():,}",
    )

    if case_index.empty:
        st.error(
            "The public four-well location index is missing from this checkout. "
            f"Expected: `{CASE_INDEX_RELATIVE_PATH.as_posix()}`."
        )

    control_cols = st.columns([1.2, 1, 1, 1])
    with control_cols[0]:
        focus_choice = st.radio(
            "Map focus",
            ["Four-well focus", "Full North Slope context"],
            horizontal=False,
            index=0,
        )
    with control_cols[1]:
        show_background_wells = st.checkbox("Public well background", value=True)
    with control_cols[2]:
        show_assessment_units = st.checkbox("Assessment units", value=True)
    with control_cols[3]:
        show_associated_wells = st.checkbox("Associated anchors", value=True)

    figure = build_four_well_2d_context_figure(
        app_module,
        case_index,
        focus_mode=focus_choice == "Four-well focus",
        show_assessment_units=show_assessment_units,
        show_background_wells=show_background_wells,
        show_associated_wells=show_associated_wells,
    )
    st.plotly_chart(
        figure,
        use_container_width=True,
        config={"displayModeBar": True, "responsive": True},
    )
    st.download_button(
        "Download 2D map HTML",
        figure.to_html(include_plotlyjs="cdn", full_html=True).encode("utf-8"),
        "north_slope_four_well_2d_map.html",
        "text/html",
        key="download_four_well_2d_map_html",
    )

    with st.expander("Public-safe four-well location index", expanded=True):
        if case_index.empty:
            st.info("No case-location rows are available yet.")
        else:
            display_columns = [
                "well_case",
                "case_role",
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
                "remaining_question",
            ]
            st.dataframe(
                case_index[[column for column in display_columns if column in case_index.columns]],
                use_container_width=True,
                hide_index=True,
            )
            st.download_button(
                "Download four-well public index CSV",
                case_index.to_csv(index=False).encode("utf-8"),
                CASE_INDEX_RELATIVE_PATH.name,
                "text/csv",
                key="download_four_well_public_index_csv",
            )

    with st.expander("Reference-only legacy regional scene", expanded=False):
        st.caption(
            "The older full regional map is retained here for broad assessment-unit, seismic, and "
            "notebook-output reference. It is no longer the first 2D map because it is too busy for "
            "the four-well project discussion."
        )
        app_module.render_scene(app_module.REGIONAL_SCENE, height=870)
