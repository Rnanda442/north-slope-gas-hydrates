from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

from dashboard import map_v2
from dashboard import mapbox_map as base


PRIMARY_WELL_CASES = ["MTE", "IGS", "Hydrate-01", "HYDRATE 02"]
PROJECT_WELL_COLORS = {
    "MTE": "#be123c",
    "IGS": "#0f766e",
    "Hydrate-01": "#7c3aed",
    "HYDRATE 02": "#ea580c",
}
DISPLAY_OFFSETS = {
    # marker offsets are only for readability on the public presentation map;
    # hover text keeps the public bottomhole coordinate available.
    "MTE": {"lon": -0.035, "lat": 0.030, "position": "top left"},
    "IGS": {"lon": -0.020, "lat": -0.020, "position": "bottom right"},
    "Hydrate-01": {"lon": -0.070, "lat": -0.055, "position": "bottom left"},
    "HYDRATE 02": {"lon": 0.070, "lat": 0.050, "position": "top right"},
}
FIELD_LABELS = [
    {"label": "Greater Mooses Tooth", "lon": -153.15, "lat": 70.05, "size": 13},
    {"label": "Colville River", "lon": -151.55, "lat": 70.39, "size": 13},
    {"label": "Pikka", "lon": -150.65, "lat": 70.46, "size": 13},
    {"label": "Kuparuk River", "lon": -149.95, "lat": 70.17, "size": 13},
    {"label": "Milne Point", "lon": -149.55, "lat": 70.66, "size": 13},
    {"label": "Nikaitchuq", "lon": -149.28, "lat": 70.84, "size": 13},
    {"label": "Prudhoe Bay", "lon": -148.58, "lat": 70.23, "size": 13},
    {"label": "Northstar", "lon": -147.48, "lat": 70.78, "size": 13},
]
MANUAL_TAPS_LINE = {
    "lon": [-148.63, -148.57, -148.51, -148.46, -148.40, -148.35],
    "lat": [70.45, 70.18, 69.92, 69.64, 69.38, 69.14],
}
FIELD_TREND_GUIDES = [
    {
        "name": "Public field trend guide",
        "lon": [-153.4, -152.1, -150.85, -149.65, -148.45, -147.25],
        "lat": [70.02, 70.20, 70.32, 70.41, 70.39, 70.33],
        "color": "rgba(15, 118, 110, 0.58)",
        "width": 2.4,
    },
    {
        "name": "Regional structural guide",
        "lon": [-153.6, -152.5, -151.4, -150.1, -148.9, -147.7],
        "lat": [69.50, 69.62, 69.78, 69.95, 70.05, 70.10],
        "color": "rgba(8, 83, 104, 0.45)",
        "width": 1.6,
    },
]
CENTER_FOR_REFERENCE = {"lat": 70.28, "lon": -149.95, "zoom": 5.65}
FULL_CONTEXT_CENTER = {"lat": 70.1, "lon": -151.1, "zoom": 4.7}
FOUR_WELL_CENTER = {"lat": 70.36, "lon": -149.3, "zoom": 7.6}
LAYER_STYLES = {
    "assessment": {
        "line": "rgba(8, 83, 104, 0.70)",
        "width": 2.0,
        "fill": "rgba(20, 123, 133, 0.12)",
    },
    "field_unit": {
        "line": "rgba(100, 116, 139, 0.72)",
        "width": 1.2,
        "fill": "rgba(148, 163, 184, 0.08)",
    },
    "road": {"line": "rgba(234, 88, 12, 0.60)", "width": 1.0, "fill": None},
    "extent": {"line": "rgba(8, 83, 104, 0.96)", "width": 3.2, "fill": None},
    "fault_contact": {"line": "rgba(8, 83, 104, 0.46)", "width": 1.3, "fill": None},
}


def _as_number(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _sample_rows(frame: pd.DataFrame, max_rows: int) -> pd.DataFrame:
    if len(frame) <= max_rows:
        return frame
    step = max(1, len(frame) // max_rows)
    return frame.iloc[::step].head(max_rows)


def _context(app_module) -> pd.DataFrame:
    master_2d = getattr(app_module, "MASTER_2D", None)
    columns = ["layer_name", "feature_id", "vertex_order", "lon", "lat", "depth_m", "au_name"]
    if master_2d is not None and Path(master_2d).exists():
        return pd.read_parquet(Path(master_2d), columns=columns).copy()
    return app_module.load_regional_context().copy()


def _primary_cases(case_index: pd.DataFrame) -> pd.DataFrame:
    if case_index.empty:
        return pd.DataFrame()
    frame = case_index[
        case_index["well_case"].isin(PRIMARY_WELL_CASES)
        & case_index["case_role"].isin(map_v2.PRIMARY_CASE_ROLES)
    ].copy()
    frame["well_case"] = pd.Categorical(frame["well_case"], PRIMARY_WELL_CASES, ordered=True)
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
        if column in frame.columns:
            frame[column] = _as_number(frame[column])
    frame["plot_lat"] = frame["bottomhole_latitude"].fillna(frame["wellhead_latitude"])
    frame["plot_lon"] = frame["bottomhole_longitude"].fillna(frame["wellhead_longitude"])
    return frame.dropna(subset=["plot_lat", "plot_lon"])


def _layer_matches(layer_name: str, keywords: list[str], exclude: list[str] | None = None) -> bool:
    text = str(layer_name).lower().replace("-", "_").replace(" ", "_")
    if exclude and any(word in text for word in exclude):
        return False
    return any(word in text for word in keywords)


def _add_layer_by_keywords(
    figure: go.Figure,
    context: pd.DataFrame,
    keywords: list[str],
    label: str,
    style_key: str,
    max_features: int = 90,
    max_points: int = 500,
    exclude: list[str] | None = None,
) -> int:
    if context.empty or "layer_name" not in context.columns or "feature_id" not in context.columns:
        return 0
    names = [name for name in context["layer_name"].dropna().unique() if _layer_matches(str(name), keywords, exclude)]
    if not names:
        return 0
    layer = context[context["layer_name"].isin(names)].copy()
    layer["lon"] = _as_number(layer["lon"])
    layer["lat"] = _as_number(layer["lat"])
    layer = layer.dropna(subset=["feature_id", "lon", "lat"])
    if layer.empty:
        return 0
    style = LAYER_STYLES[style_key]
    feature_ids = layer["feature_id"].drop_duplicates().tolist()
    if len(feature_ids) > max_features:
        step = max(1, len(feature_ids) // max_features)
        feature_ids = feature_ids[::step][:max_features]
    layer = layer[layer["feature_id"].isin(feature_ids)]
    count = 0
    showlegend = True
    for _, rows in layer.groupby("feature_id", sort=False):
        if "vertex_order" in rows.columns:
            rows = rows.sort_values("vertex_order")
        rows = _sample_rows(rows, max_points)
        fill = "toself" if style.get("fill") and len(rows) > 2 else None
        figure.add_trace(
            go.Scattermapbox(
                lon=rows["lon"],
                lat=rows["lat"],
                mode="lines",
                fill=fill,
                fillcolor=style.get("fill"),
                name=label,
                showlegend=showlegend,
                legendgroup=label,
                line={"color": style["line"], "width": style["width"]},
                hovertemplate=f"<b>{label}</b><br>Public map context layer<extra></extra>",
            )
        )
        showlegend = False
        count += 1
    return count


def _add_manual_lines(figure: go.Figure) -> None:
    figure.add_trace(
        go.Scattermapbox(
            lon=MANUAL_TAPS_LINE["lon"],
            lat=MANUAL_TAPS_LINE["lat"],
            mode="lines",
            name="TAPS / Dalton corridor",
            line={"color": "rgba(120, 53, 15, 0.94)", "width": 4.0},
            hovertemplate="<b>TAPS / Dalton corridor</b><extra></extra>",
        )
    )
    for line in FIELD_TREND_GUIDES:
        figure.add_trace(
            go.Scattermapbox(
                lon=line["lon"],
                lat=line["lat"],
                mode="lines",
                name=line["name"],
                showlegend=False,
                line={"color": line["color"], "width": line["width"]},
                hovertemplate=f"<b>{line['name']}</b><extra></extra>",
            )
        )


def _add_field_labels(figure: go.Figure) -> None:
    # white halo pass
    figure.add_trace(
        go.Scattermapbox(
            lon=[item["lon"] for item in FIELD_LABELS],
            lat=[item["lat"] for item in FIELD_LABELS],
            text=[item["label"] for item in FIELD_LABELS],
            mode="text",
            showlegend=False,
            hoverinfo="skip",
            textfont={"size": 15, "color": "#ffffff"},
        )
    )
    figure.add_trace(
        go.Scattermapbox(
            lon=[item["lon"] for item in FIELD_LABELS],
            lat=[item["lat"] for item in FIELD_LABELS],
            text=[item["label"] for item in FIELD_LABELS],
            mode="text",
            showlegend=False,
            hoverinfo="skip",
            textfont={"size": 13, "color": "#0f172a"},
        )
    )


def _add_project_wells(figure: go.Figure, case_index: pd.DataFrame) -> None:
    wells = _with_plot_locations(_primary_cases(case_index))
    if wells.empty:
        return
    for row in wells.itertuples(index=False):
        well_case = str(row.well_case)
        color = PROJECT_WELL_COLORS.get(well_case, "#0f172a")
        offset = DISPLAY_OFFSETS.get(well_case, {"lon": 0.0, "lat": 0.0, "position": "top right"})
        display_lon = float(row.plot_lon) + float(offset["lon"])
        display_lat = float(row.plot_lat) + float(offset["lat"])
        label = str(row.map_label)
        position = str(offset["position"])
        # subtle connector only when display point is offset from the public coordinate
        if abs(display_lon - float(row.plot_lon)) > 0.001 or abs(display_lat - float(row.plot_lat)) > 0.001:
            figure.add_trace(
                go.Scattermapbox(
                    lon=[row.plot_lon, display_lon],
                    lat=[row.plot_lat, display_lat],
                    mode="lines",
                    showlegend=False,
                    hoverinfo="skip",
                    line={"color": color, "width": 1.2},
                )
            )
        figure.add_trace(
            go.Scattermapbox(
                lon=[display_lon],
                lat=[display_lat],
                text=[label],
                mode="text",
                showlegend=False,
                hoverinfo="skip",
                textposition=position,
                textfont={"size": 16, "color": "#ffffff"},
            )
        )
        figure.add_trace(
            go.Scattermapbox(
                lon=[display_lon],
                lat=[display_lat],
                text=[label],
                mode="markers+text",
                name=label,
                showlegend=False,
                textposition=position,
                textfont={"size": 12, "color": color},
                marker={"size": 17, "color": color, "opacity": 0.98, "line": {"color": "white", "width": 1.6}},
                customdata=[
                    [
                        row.verified_public_well_name,
                        row.field,
                        row.current_status,
                        row.true_vertical_depth_ft,
                        row.driller_total_depth_ft,
                        row.evidence_status,
                        row.website_use_note,
                        row.plot_lon,
                        row.plot_lat,
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
                    "Public coordinate lon/lat: %{customdata[7]:.5f}, %{customdata[8]:.5f}<extra></extra>"
                ),
            )
        )


def _add_optional_public_wells(figure: go.Figure, app_module) -> int:
    wells = app_module.load_north_slope_wells().copy()
    if wells.empty:
        return 0
    wells["lon"] = _as_number(wells["lon"])
    wells["lat"] = _as_number(wells["lat"])
    wells = wells.dropna(subset=["lon", "lat"])
    wells = wells[wells["lon"].between(-154.5, -146.7) & wells["lat"].between(69.2, 71.0)]
    wells = _sample_rows(wells.sort_values(["lon", "lat"]), 650)
    if wells.empty:
        return 0
    figure.add_trace(
        go.Scattermapbox(
            lon=wells["lon"],
            lat=wells["lat"],
            mode="markers",
            name="Public well background",
            marker={"size": 3.0, "color": "rgba(15,23,42,0.20)"},
            hovertemplate="Public well<br>Lon/lat: %{lon:.3f}, %{lat:.3f}<extra></extra>",
        )
    )
    return len(wells)


def build_reference_style_no_seismic_map(
    app_module,
    case_index: pd.DataFrame,
    mode: str,
    show_assessment_units: bool,
    show_units_roads_taps: bool,
    show_geologic_lines: bool,
    show_public_wells: bool,
    show_extent: bool,
) -> tuple[go.Figure, dict[str, int]]:
    context = _context(app_module)
    figure = go.Figure()
    counts: dict[str, int] = {}

    if show_assessment_units:
        counts["assessment_units"] = _add_layer_by_keywords(
            figure,
            context,
            ["assessment", "au"],
            "Hydrate assessment-unit context",
            "assessment",
            max_features=80,
            max_points=700,
            exclude=["seismic"],
        )
    if show_units_roads_taps:
        counts["field_unit_outlines"] = _add_layer_by_keywords(
            figure,
            context,
            ["field", "unit", "pool"],
            "Field / unit outline",
            "field_unit",
            max_features=120,
            max_points=500,
            exclude=["seismic"],
        )
        counts["road_corridor"] = _add_layer_by_keywords(
            figure,
            context,
            ["road"],
            "Road corridor",
            "road",
            max_features=80,
            max_points=500,
            exclude=["seismic"],
        )
    if show_geologic_lines:
        counts["fault_contacts_geology"] = _add_layer_by_keywords(
            figure,
            context,
            ["fault", "contact", "geology", "fold"],
            "Fault/contact/geology line",
            "fault_contact",
            max_features=120,
            max_points=500,
            exclude=["seismic"],
        )
    if show_extent:
        counts["study_boundary"] = _add_layer_by_keywords(
            figure,
            context,
            ["extent", "boundary"],
            "North Slope study boundary",
            "extent",
            max_features=8,
            max_points=80,
            exclude=["seismic"],
        )

    _add_manual_lines(figure)
    _add_field_labels(figure)
    if show_public_wells:
        counts["public_wells"] = _add_optional_public_wells(figure, app_module)
    _add_project_wells(figure, case_index)

    center = CENTER_FOR_REFERENCE
    if mode == "Four-well close-up":
        center = FOUR_WELL_CENTER
    elif mode == "Full North Slope context":
        center = FULL_CONTEXT_CENTER

    figure.update_layout(
        title={"text": "North Slope reference-style project well map", "x": 0.01, "font": {"size": 17}},
        height=680 if mode == "Code-built source map" else 650,
        margin={"l": 0, "r": 0, "t": 48, "b": 0},
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
    return figure, counts


def render_regional_atlas_clean(app_module) -> None:
    st = app_module.st
    project_root = app_module.PROJECT_ROOT
    case_index = map_v2.load_four_well_case_index(project_root)
    primary = _primary_cases(case_index)

    st.markdown('<div class="atlas-kicker">Regional context</div>', unsafe_allow_html=True)
    st.title("Regional 2D Map")
    st.write(
        "Reference-style rebuild of the North Slope map: same central crop/label logic as the slide map, corrected four-well names, and seismic layers removed from the default map."
    )
    st.warning(
        "Public-source context only. This map does not show approved log rows, core rows, trained models, predictions, hydrate occurrence, or saturation results."
    )

    metric_cols = st.columns(4)
    metric_cols[0].metric("Correct project wells", f"{len(primary):,}")
    metric_cols[1].metric("Seismic layers", "Removed")
    metric_cols[2].metric("Public wells default", "Off")
    metric_cols[3].metric("Map purpose", "Context only")

    controls = st.columns([1.25, 1, 1, 1, 1, 1])
    with controls[0]:
        mode = st.radio(
            "Map focus",
            ["Code-built source map", "Four-well close-up", "Full North Slope context"],
            index=0,
        )
    with controls[1]:
        show_assessment_units = st.checkbox("Assessment units", value=True)
    with controls[2]:
        show_units_roads_taps = st.checkbox("Units / TAPS", value=True)
    with controls[3]:
        show_geologic_lines = st.checkbox("Geology lines", value=True)
    with controls[4]:
        show_public_wells = st.checkbox("Public wells", value=False)
    with controls[5]:
        show_extent = st.checkbox("Study boundary", value=True)

    figure, counts = build_reference_style_no_seismic_map(
        app_module,
        case_index,
        mode=mode,
        show_assessment_units=show_assessment_units,
        show_units_roads_taps=show_units_roads_taps,
        show_geologic_lines=show_geologic_lines,
        show_public_wells=show_public_wells,
        show_extent=show_extent,
    )

    if mode == "Code-built source map":
        map_col, curve_col = st.columns([2.35, 1])
        with map_col:
            st.plotly_chart(figure, use_container_width=True, config={"displayModeBar": True, "responsive": True})
        with curve_col:
            st.plotly_chart(base.build_stability_inset(project_root), use_container_width=True, config={"displayModeBar": True, "responsive": True})
            st.caption("Inset is public thermodynamic context only; it is not hydrate proof.")
    else:
        st.plotly_chart(figure, use_container_width=True, config={"displayModeBar": True, "responsive": True})

    st.caption(
        "Default visible layers: assessment context, unit/field outlines where available, TAPS/field-guide lines, geologic/context lines, study boundary, manual field labels, and the four project wells. Seismic layers are not drawn."
    )

    with st.expander("Correct four project wells", expanded=True):
        if primary.empty:
            st.info("No primary project-well rows were found in the public four-well index.")
        else:
            columns = [
                "well_case",
                "map_label",
                "verified_public_well_name",
                "field",
                "current_status",
                "bottomhole_latitude",
                "bottomhole_longitude",
                "true_vertical_depth_ft",
                "driller_total_depth_ft",
                "evidence_status",
                "website_use_note",
            ]
            st.dataframe(primary[[column for column in columns if column in primary.columns]], use_container_width=True, hide_index=True)

    with st.expander("Layer counts and audit", expanded=False):
        st.dataframe(pd.DataFrame([{"layer_group": key, "features_drawn": value} for key, value in counts.items()]), use_container_width=True, hide_index=True)

    st.download_button(
        "Download reference-style map HTML",
        figure.to_html(include_plotlyjs="cdn", full_html=True).encode("utf-8"),
        "north_slope_reference_style_no_seismic_map.html",
        "text/html",
        key="download_reference_style_no_seismic_map_html",
    )
