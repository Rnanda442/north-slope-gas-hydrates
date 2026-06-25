from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from dashboard import map_v2
from dashboard import mapbox_map as base


# Cleaner mobile-first view after visual QA.  The previous map was technically
# interactive but still looked too crowded on a phone because background wells,
# labels, and primary-well text were all plotted in the same place.
base.CODE_MAP_CENTER = {"lat": 70.30, "lon": -150.05, "zoom": 5.35}
base.FOUR_WELL_CENTER = {"lat": 70.36, "lon": -149.28, "zoom": 7.70}
base.FIELD_LABELS = [
    {"label": "Great Mooses Tooth", "lon": -153.05, "lat": 70.10},
    {"label": "Colville River", "lon": -151.30, "lat": 70.37},
    {"label": "Pikka", "lon": -150.58, "lat": 70.50},
    {"label": "Kuparuk River", "lon": -149.92, "lat": 70.16},
    {"label": "Milne Point", "lon": -149.58, "lat": 70.66},
    {"label": "Nikaitchuq", "lon": -149.34, "lat": 70.83},
    {"label": "Prudhoe Bay", "lon": -148.55, "lat": 70.24},
    {"label": "Northstar", "lon": -147.58, "lat": 70.77},
]
base.CORRIDOR_LINES = [
    {
        "name": "TAPS / Dalton corridor",
        "lon": [-148.60, -148.54, -148.49, -148.44, -148.38, -148.34],
        "lat": [70.39, 70.15, 69.90, 69.64, 69.38, 69.12],
        "color": "#92400e",
        "width": 4,
    },
    {
        "name": "Public field trend guide",
        "lon": [-153.40, -152.20, -150.85, -149.60, -148.55, -147.25],
        "lat": [70.02, 70.20, 70.31, 70.41, 70.39, 70.33],
        "color": "#0f766e",
        "width": 2,
    },
]

PRIMARY_LABEL_POINTS = {
    "MTE": {"lon": -149.82, "lat": 70.63, "label": "MTE / Mount Elbert"},
    "IGS": {"lon": -148.88, "lat": 70.12, "label": "IGS / Ignik Sikumi"},
    "Hydrate-01": {"lon": -149.88, "lat": 70.00, "label": "Hydrate-01"},
    "HYDRATE 02": {"lon": -148.56, "lat": 70.58, "label": "HYDRATE 02"},
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


def _clean_add_case_points(figure: go.Figure, rows: pd.DataFrame) -> None:
    rows = _with_plot_locations(rows)
    if rows.empty:
        return

    primary = rows[rows["well_case"].isin(base.PRIMARY_WELLS)].copy()
    optional = rows[~rows["well_case"].isin(base.PRIMARY_WELLS)].copy()

    for row in primary.itertuples(index=False):
        well_case = str(row.well_case)
        color = base.WELL_COLORS.get(well_case, "#0f172a")
        label_point = PRIMARY_LABEL_POINTS.get(
            well_case,
            {"lon": row.plot_lon + 0.15, "lat": row.plot_lat + 0.10, "label": str(row.map_label)},
        )
        figure.add_trace(
            go.Scattermapbox(
                lon=[row.plot_lon, label_point["lon"]],
                lat=[row.plot_lat, label_point["lat"]],
                mode="lines",
                name="Project-well label leader",
                showlegend=False,
                line={"color": color, "width": 2},
                hoverinfo="skip",
            )
        )
        figure.add_trace(
            go.Scattermapbox(
                lon=[row.plot_lon],
                lat=[row.plot_lat],
                mode="markers",
                name=str(row.map_label),
                marker={"size": 18, "color": color, "opacity": 0.98},
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
                    f"<b>{row.map_label}</b><br>"
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
        # Plot a white halo text layer first so the label stays readable on mobile.
        figure.add_trace(
            go.Scattermapbox(
                lon=[label_point["lon"]],
                lat=[label_point["lat"]],
                mode="text",
                showlegend=False,
                text=[label_point["label"]],
                textfont={"size": 16, "color": "#ffffff"},
                hoverinfo="skip",
            )
        )
        figure.add_trace(
            go.Scattermapbox(
                lon=[label_point["lon"]],
                lat=[label_point["lat"]],
                mode="text",
                showlegend=False,
                text=[label_point["label"]],
                textfont={"size": 14, "color": "#0f172a"},
                hoverinfo="skip",
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
                name=base.ROLE_LABELS.get(role_key, role_key),
                marker={"size": 9, "color": base.ROLE_COLORS.get(role_key, "#475569"), "opacity": 0.78},
                text=group["map_label"],
                hovertemplate="<b>%{text}</b><br>Optional associated public anchor<extra></extra>",
            )
        )


def render_regional_atlas_clean(app_module) -> None:
    # Patch the internal point renderer before building the map.
    base._add_case_points = _clean_add_case_points

    st = app_module.st
    project_root = app_module.PROJECT_ROOT
    case_index = map_v2.load_four_well_case_index(project_root)
    context = base._context(app_module)
    primary = _primary_cases(case_index)
    optional = case_index[~case_index["well_case"].isin(base.PRIMARY_WELLS)].copy() if not case_index.empty else pd.DataFrame()

    st.markdown('<div class="atlas-kicker">Regional context</div>', unsafe_allow_html=True)
    st.title("Regional 2D Map")
    st.write(
        "This cleaned default view is designed to match the reference map: central North Slope extent, readable field labels, the TAPS/Dalton corridor, seismic and assessment context, and only the four project wells shown by default."
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

    figure = base.build_north_slope_mapbox_figure(
        app_module,
        case_index,
        mode,
        show_background_wells,
        show_assessment_units,
        show_labels,
        show_seismic,
        show_optional,
    )
    figure.update_layout(
        title={"text": f"North Slope public 2D map: {mode}", "x": 0.01, "font": {"size": 17}},
        legend={"orientation": "h", "y": -0.09, "x": 0, "font": {"size": 9}},
        height=700 if mode == "Code-built source map" else 670,
    )

    if mode == "Code-built source map":
        map_col, curve_col = st.columns([2.15, 1])
        with map_col:
            st.plotly_chart(figure, use_container_width=True, config={"displayModeBar": True, "responsive": True})
        with curve_col:
            st.plotly_chart(base.build_stability_inset(project_root), use_container_width=True, config={"displayModeBar": True, "responsive": True})
            st.caption("Inset recreates the public stability concept interactively from the digitized methane 5 ppt phase curve.")
    else:
        st.plotly_chart(figure, use_container_width=True, config={"displayModeBar": True, "responsive": True})

    st.download_button(
        "Download interactive 2D map HTML",
        figure.to_html(include_plotlyjs="cdn", full_html=True).encode("utf-8"),
        "north_slope_clean_four_well_interactive_map.html",
        "text/html",
        key="download_clean_four_well_map_html",
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
