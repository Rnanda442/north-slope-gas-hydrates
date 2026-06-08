from __future__ import annotations

from collections import Counter
from html import escape
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

from dashboard.well_log_engine import (
    CLASSIFICATION_WORKFLOW,
    EQUATION_LIBRARY,
    HEADER_SCHEMA_BLUEPRINT,
    RANGE_GUIDE,
    PUBLIC_SCIENCE_REFERENCES,
    ROCKTYPE_CONTEXT_GUIDE,
    SCREENING_BANDS,
    SYNTHETIC_LABEL,
    SWEET_SPOT_GUIDE,
    SWEET_SPOT_EVIDENCE_MODEL,
    VARIABLES,
    cross_well_range_figure,
    csv_bytes,
    figure_html_bytes,
    load_runtime_data,
    model_placeholder_figures,
    nearby_log_calibration,
    screen_intervals,
    synthetic_core_placeholders,
    variable_range_summary,
    well_log_panel,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = PROJECT_ROOT / "05_exports" / "html"
ARCHITECTURE_PATH = PROJECT_ROOT / "docs" / "PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md"
IGNORED_DIRS = {".git", ".ipynb_checkpoints", "__pycache__"}

REGIONAL_SCENE = EXPORT_DIR / "north_slope_plotly_advanced.html"
STRUCTURAL_SCENES = {
    "Master structural scene": EXPORT_DIR / "north_slope_master_analysis_scene.html",
    "Full-resolution structural scene": EXPORT_DIR
    / "north_slope_master_analysis_scene_full_no_simplify.html",
}
MASTER_3D = PROJECT_ROOT / "03_data_final" / "master_layers" / "north_slope_master_3d_surfaces.parquet"
MASTER_2D = PROJECT_ROOT / "03_data_final" / "master_layers" / "north_slope_master_2d_layers.parquet"
STRUCTURAL_HORIZONS = ["NStopo", "NSLCU", "NSshublik", "NSbasement"]
CONTEXT_OVERLAYS = [
    "North Slope study-area boundary",
    "Assessment-unit outlines",
    "North Slope public wells",
]

SURFACE_CATALOG = {
    "NStopo": {
        "Label": "Topographic reference",
        "Description": "Near-surface reference horizon used to orient the structural stack.",
        "Color": "#4daf4a",
    },
    "NSLCU": {
        "Label": "Lower Cretaceous unconformity",
        "Description": "Regional unconformity surface used as a subsurface structural reference.",
        "Color": "#377eb8",
    },
    "NSshublik": {
        "Label": "Shublik surface",
        "Description": "Regional Shublik structural horizon used for deeper framework context.",
        "Color": "#ff7f00",
    },
    "NSbasement": {
        "Label": "Basement surface",
        "Description": "Deep basement structural reference for regional basin geometry.",
        "Color": "#984ea3",
    },
    "NStopo-LCU": {
        "Label": "Topography to LCU interval",
        "Description": "Thickness-style grid between the topographic reference and LCU.",
        "Color": "#66c2a5",
    },
    "NSLCU-Shublik": {
        "Label": "LCU to Shublik interval",
        "Description": "Thickness-style grid between LCU and the Shublik surface.",
        "Color": "#fc8d62",
    },
    "NSshublik-basement": {
        "Label": "Shublik to basement interval",
        "Description": "Thickness-style grid between the Shublik and basement surfaces.",
        "Color": "#8da0cb",
    },
    "NStopo-basement": {
        "Label": "Topography to basement interval",
        "Description": "Full reference interval between topography and basement.",
        "Color": "#e78ac3",
    },
}

PAGES = [
    "Welcome",
    "Project Roadmap",
    "Regional Atlas",
    "Structural Explorer",
    "Data Library",
    "Research Framework",
    "Future Well-Log Engine",
]

LAYER_CATALOG = [
    {
        "Layer": "Well-bottom-hole locations",
        "Role": "Regional well inventory",
        "Records": "10,250",
        "Geometry": "Point",
        "Status": "Cleaned + enriched",
        "Source category": "Public-source GIS",
        "Boundary tag": "PUBLIC-SOURCE ATLAS",
        "Description": "Well-bottom-hole inventory used for regional orientation and map filtering.",
        "Location": "03_data_final/core_layers/clean_well_locations.parquet",
    },
    {
        "Layer": "2D seismic coverage",
        "Role": "Regional line coverage",
        "Records": "26 surveys",
        "Geometry": "Line / MultiLine",
        "Status": "Cleaned + enriched",
        "Source category": "Public-source GIS",
        "Boundary tag": "PUBLIC-SOURCE ATLAS",
        "Description": "Regional 2D line inventory used to show available seismic context.",
        "Location": "03_data_final/core_layers/clean_2d_seismic.parquet",
    },
    {
        "Layer": "3D seismic inventory",
        "Role": "Survey footprint coverage",
        "Records": "36 surveys",
        "Geometry": "Polygon / MultiPolygon",
        "Status": "Cleaned + enriched",
        "Source category": "Public-source GIS",
        "Boundary tag": "PUBLIC-SOURCE ATLAS",
        "Description": "Polygon footprints showing areas with 3D seismic inventory coverage.",
        "Location": "03_data_final/core_layers/clean_3d_seismic.parquet",
    },
    {
        "Layer": "North Slope assessment units",
        "Role": "Regional petroleum-system framework",
        "Records": "6 units",
        "Geometry": "Polygon / MultiPolygon",
        "Status": "Cleaned + enriched",
        "Source category": "Public-source geology",
        "Boundary tag": "PUBLIC-SOURCE ATLAS",
        "Description": "Regional assessment units used as petroleum-system context.",
        "Location": "03_data_final/core_layers/north_slope_assessment_units.parquet",
    },
    {
        "Layer": "North Slope extent",
        "Role": "Study-area boundary",
        "Records": "1 boundary",
        "Geometry": "Polygon",
        "Status": "Cleaned + enriched",
        "Source category": "Project-derived boundary",
        "Boundary tag": "PUBLIC-SOURCE ATLAS",
        "Description": "Study-area outline for North Slope-focused visualization.",
        "Location": "03_data_final/core_layers/north_slope_extent.parquet",
    },
    {
        "Layer": "Structural depth grids",
        "Role": "Subsurface framework",
        "Records": "8 XYZ grids",
        "Geometry": "Grid points + rasters",
        "Status": "Processed",
        "Source category": "Public-source structural grids",
        "Boundary tag": "PUBLIC-SOURCE ATLAS",
        "Description": "Raw XYZ structural references and interval grids used in the 3D explorer.",
        "Location": "raw_data/north_slope_depth_grids/",
    },
    {
        "Layer": "GIS-ready surfaces",
        "Role": "Topography, Shublik, and basement surfaces",
        "Records": "3 surfaces",
        "Geometry": "Point GeoJSON + Parquet",
        "Status": "Dashboard ready",
        "Source category": "Project-derived GIS output",
        "Boundary tag": "PUBLIC-SOURCE ATLAS",
        "Description": "Processed surface points exported for GIS and lightweight inspection.",
        "Location": "03_data_final/gis_ready_surfaces/",
    },
]

FRAMEWORK_STAGES = [
    ("01", "Environment", "Pressure-temperature boundary conditions"),
    ("02", "Tectonics", "Migration pathways, burial history, and traps"),
    ("03", "Deposition", "Reservoir architecture and sand distribution"),
    ("04", "Reservoir", "Porosity, permeability, continuity, and compartmentalization"),
    ("05", "Physics", "Elastic, electrical, and geomechanical response"),
    ("06", "Logs", "Wireline measurements and derived attributes"),
    ("07", "Interpretation", "Failure-aware phase discrimination"),
    ("08", "ML", "Physics-constrained classification and ranking"),
    ("09", "Exploitation", "Separate resource density from producibility"),
]


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --atlas-navy: #123447;
            --atlas-teal: #167d8d;
            --atlas-ice: #edf7f8;
            --atlas-sand: #f4efe6;
            --atlas-orange: #d9773d;
        }
        .stApp {
            background: linear-gradient(180deg, #f8fbfb 0%, #ffffff 36%);
        }
        [data-testid="stSidebar"] {
            background: #123447;
        }
        [data-testid="stSidebar"] * {
            color: #f7fbfc;
        }
        [data-testid="stSidebar"] .stRadio label {
            padding: 0.18rem 0;
        }
        .atlas-kicker {
            color: #167d8d;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.14em;
            text-transform: uppercase;
        }
        .atlas-hero {
            background: linear-gradient(125deg, #123447 0%, #176477 70%, #167d8d 100%);
            border-radius: 18px;
            color: white;
            padding: 2.4rem 2.7rem;
            margin-bottom: 1.1rem;
        }
        .atlas-hero h1 {
            color: white;
            font-size: 2.45rem;
            line-height: 1.08;
            margin: 0.3rem 0 0.75rem;
        }
        .atlas-hero p {
            color: #e8f6f7;
            font-size: 1.05rem;
            max-width: 860px;
        }
        .atlas-card {
            background: white;
            border: 1px solid #d9e7e8;
            border-radius: 14px;
            min-height: 162px;
            padding: 1.1rem 1.2rem;
        }
        .atlas-card h4 {
            color: #123447;
            margin: 0.1rem 0 0.4rem;
        }
        .atlas-step {
            background: #edf7f8;
            border-left: 4px solid #167d8d;
            border-radius: 8px;
            margin: 0.42rem 0;
            padding: 0.66rem 0.85rem;
        }
        .atlas-step strong {
            color: #123447;
        }
        .atlas-boundary {
            background: #f4efe6;
            border: 1px solid #e4d8c4;
            border-radius: 10px;
            padding: 0.8rem 1rem;
        }
        .roadmap-status {
            background: #ffffff;
            border: 1px solid #d9e7e8;
            border-radius: 12px;
            padding: 0.9rem 1rem;
            margin-bottom: 0.7rem;
        }
        .roadmap-status strong {
            color: #123447;
        }
        .roadmap-next {
            background: linear-gradient(135deg, #edf7f8 0%, #ffffff 100%);
            border: 1px solid #bcdcdf;
            border-left: 5px solid #167d8d;
            border-radius: 12px;
            padding: 1rem 1.1rem;
            margin: 0.8rem 0 1rem;
        }
        .roadmap-next strong {
            color: #123447;
        }
        .roadmap-mobile {
            display: none;
        }
        .roadmap-table {
            border-collapse: collapse;
            font-size: 0.88rem;
            width: 100%;
        }
        .roadmap-table th {
            background: #edf7f8;
            color: #123447;
            text-align: left;
        }
        .roadmap-table th,
        .roadmap-table td {
            border: 1px solid #d9e7e8;
            padding: 0.55rem;
            vertical-align: top;
        }
        .roadmap-card {
            background: #ffffff;
            border: 1px solid #d9e7e8;
            border-radius: 12px;
            padding: 0.9rem 1rem;
            margin-bottom: 0.7rem;
        }
        .roadmap-card-title {
            color: #123447;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }
        .roadmap-pill {
            background: #edf7f8;
            border-radius: 999px;
            color: #166674;
            display: inline-block;
            font-size: 0.76rem;
            font-weight: 700;
            margin-bottom: 0.55rem;
            padding: 0.2rem 0.55rem;
        }
        .roadmap-label {
            color: #527078;
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }
        [data-testid="stDataFrame"] {
            overflow-x: auto;
        }
        [data-baseweb="tab-list"] {
            overflow-x: auto;
            scrollbar-width: thin;
        }
        [data-baseweb="tab"] {
            flex: 0 0 auto;
        }
        @media (max-width: 768px) {
            .block-container {
                padding: 1rem 0.8rem 4rem;
                max-width: 100%;
            }
            .atlas-hero {
                border-radius: 12px;
                padding: 1.35rem 1.1rem;
                margin-bottom: 0.8rem;
            }
            .atlas-hero h1 {
                font-size: 1.85rem;
                line-height: 1.12;
            }
            .atlas-hero p {
                font-size: 0.96rem;
            }
            .atlas-card {
                min-height: auto;
                margin-bottom: 0.65rem;
            }
            h1 {
                font-size: 1.85rem !important;
            }
            h2 {
                font-size: 1.45rem !important;
            }
            h3 {
                font-size: 1.2rem !important;
            }
            [data-testid="stHorizontalBlock"] {
                flex-direction: column;
                gap: 0.55rem;
            }
            [data-testid="stHorizontalBlock"] > div {
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 0 !important;
            }
            [data-testid="stMetric"] {
                border-bottom: 1px solid #e3ecec;
                padding-bottom: 0.45rem;
            }
            iframe {
                max-width: 100%;
            }
            .stButton button,
            .stDownloadButton button {
                width: 100%;
            }
            .roadmap-desktop {
                display: none;
            }
            .roadmap-mobile {
                display: block;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def markdown_section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    if marker not in text:
        return ""
    section = text.split(marker, 1)[1]
    return section.split("\n## ", 1)[0].strip()


def markdown_table(section: str) -> pd.DataFrame:
    lines = [line.strip() for line in section.splitlines() if line.strip().startswith("|")]
    if len(lines) < 2:
        return pd.DataFrame()
    headers = [cell.strip() for cell in lines[0].strip("|").split("|")]
    rows = []
    for line in lines[2:]:
        cells = [cell.strip().replace("`", "") for cell in line.strip("|").split("|")]
        if len(cells) == len(headers):
            rows.append(cells)
    return pd.DataFrame(rows, columns=headers)


def architecture_content() -> str:
    if not ARCHITECTURE_PATH.exists():
        return ""
    return ARCHITECTURE_PATH.read_text(encoding="utf-8")


def roadmap_cards(workstreams: pd.DataFrame) -> str:
    cards = []
    for row in workstreams.to_dict(orient="records"):
        safe = {key: escape(str(value)) for key, value in row.items()}
        cards.append(
            f"""
            <div class="roadmap-card">
              <div class="roadmap-card-title">{safe["ID"]} · {safe["Workstream"]}</div>
              <div class="roadmap-pill">{safe["Status"]}</div>
              <div class="roadmap-label">Next activity</div>
              <div>{safe["Immediate activity"]}</div>
              <div class="roadmap-label" style="margin-top:0.65rem">Dependency</div>
              <div>{safe["Dependency"]}</div>
            </div>
            """
        )
    return '<div class="roadmap-mobile">' + "".join(cards) + "</div>"


def format_bytes(size: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:,.1f} {unit}"
        value /= 1024
    return f"{size:,} B"


@st.cache_data
def project_files() -> list[dict[str, object]]:
    rows = []
    for path in PROJECT_ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(PROJECT_ROOT)
        if any(part in IGNORED_DIRS for part in relative.parts):
            continue
        rows.append(
            {
                "Path": relative.as_posix(),
                "Type": path.suffix.lower() or "(none)",
                "Size": format_bytes(path.stat().st_size),
                "Bytes": path.stat().st_size,
            }
        )
    return sorted(rows, key=lambda row: str(row["Path"]).lower())


@st.cache_data
def read_scene(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


@st.cache_data
def load_structural_surfaces() -> pd.DataFrame:
    return pd.read_parquet(
        MASTER_3D,
        columns=["x_3338", "y_3338", "lon", "lat", "depth_m", "surface_name"],
    )


@st.cache_data
def load_regional_context() -> pd.DataFrame:
    layers = pd.read_parquet(
        MASTER_2D,
        columns=["layer_name", "feature_id", "vertex_order", "lon", "lat", "depth_m", "au_name"],
    )
    return layers[layers["layer_name"].isin(["extent", "assessment_units", "wells"])].copy()


@st.cache_data
def load_north_slope_wells() -> pd.DataFrame:
    context = load_regional_context()
    extent = context[context["layer_name"] == "extent"]
    wells = context[context["layer_name"] == "wells"].copy()
    return wells[
        wells["lon"].between(extent["lon"].min(), extent["lon"].max())
        & wells["lat"].between(extent["lat"].min(), extent["lat"].max())
    ]


def sample_rows(df: pd.DataFrame, max_rows: int) -> pd.DataFrame:
    if len(df) <= max_rows:
        return df
    step = max(1, len(df) // max_rows)
    return df.iloc[::step].head(max_rows)


def grid_surface(surface: pd.DataFrame, max_cells: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    stride = max(1, round((len(surface) / max_cells) ** 0.5))
    index = "y_3338"
    columns = "x_3338"
    lon = surface.pivot(index=index, columns=columns, values="lon").iloc[::stride, ::stride]
    lat = surface.pivot(index=index, columns=columns, values="lat").iloc[::stride, ::stride]
    depth = surface.pivot(index=index, columns=columns, values="depth_m").iloc[::stride, ::stride]
    return lon, lat, depth


def add_context_line(
    figure: go.Figure,
    rows: pd.DataFrame,
    name: str,
    color: str,
    width: int,
    showlegend: bool = True,
) -> None:
    figure.add_trace(
        go.Scatter3d(
            x=rows["lon"],
            y=rows["lat"],
            z=[0] * len(rows),
            mode="lines",
            name=name,
            showlegend=showlegend,
            line={"color": color, "width": width},
            hovertemplate=f"<b>{name}</b><br>Longitude: %{{x:.2f}}<br>Latitude: %{{y:.2f}}<extra></extra>",
        )
    )


def build_geographic_structural_figure(
    selected_surfaces: list[str],
    cells_per_surface: int,
    selected_overlays: list[str],
) -> go.Figure:
    surfaces = load_structural_surfaces()
    figure = go.Figure()

    for surface_name in selected_surfaces:
        surface = surfaces[surfaces["surface_name"] == surface_name]
        lon, lat, depth = grid_surface(surface, cells_per_surface)
        metadata = SURFACE_CATALOG[surface_name]
        figure.add_trace(
            go.Surface(
                x=lon,
                y=lat,
                z=depth,
                name=metadata["Label"],
                colorscale=[[0, metadata["Color"]], [1, metadata["Color"]]],
                opacity=0.72,
                showscale=False,
                showlegend=True,
                hovertemplate=(
                    f"<b>{metadata['Label']}</b><br>"
                    "Longitude: %{x:.2f}<br>"
                    "Latitude: %{y:.2f}<br>"
                    "Depth: %{z:,.0f} m<extra></extra>"
                ),
            )
        )

    context = load_regional_context()
    if "North Slope study-area boundary" in selected_overlays:
        extent = context[context["layer_name"] == "extent"].sort_values("vertex_order")
        add_context_line(figure, extent, "North Slope study-area boundary", "#111111", 8)

    if "Assessment-unit outlines" in selected_overlays:
        assessment_units = context[context["layer_name"] == "assessment_units"]
        for index, (_, rows) in enumerate(assessment_units.groupby("feature_id")):
            rows = rows.sort_values("vertex_order")
            rows = sample_rows(rows, 400)
            add_context_line(
                figure,
                rows,
                "Assessment-unit outlines",
                "#d9773d",
                4,
                showlegend=index == 0,
            )

    if "North Slope public wells" in selected_overlays:
        wells = sample_rows(load_north_slope_wells(), 1800)
        figure.add_trace(
            go.Scatter3d(
                x=wells["lon"],
                y=wells["lat"],
                z=wells["depth_m"],
                mode="markers",
                name="North Slope public wells",
                marker={"size": 2.8, "color": "#111111", "opacity": 0.65},
                hovertemplate=(
                    "<b>North Slope public well</b><br>"
                    "Longitude: %{x:.2f}<br>"
                    "Latitude: %{y:.2f}<extra></extra>"
                ),
            )
        )

    figure.update_layout(
        height=760,
        margin={"l": 0, "r": 0, "t": 40, "b": 0},
        legend={"orientation": "h", "y": 1.02, "x": 0},
        scene={
            "xaxis_title": "Longitude",
            "yaxis_title": "Latitude",
            "zaxis_title": "Depth (m, positive downward)",
            "zaxis": {"autorange": "reversed"},
            "aspectmode": "manual",
            "aspectratio": {"x": 1.8, "y": 1, "z": 0.55},
            "camera": {"eye": {"x": 1.55, "y": -1.75, "z": 1.05}},
        },
    )
    return figure


def render_scene(path: Path, height: int = 830) -> None:
    if not path.exists():
        st.warning(f"Scene has not been generated yet: {path.relative_to(PROJECT_ROOT)}")
        return
    st.caption(f"{path.relative_to(PROJECT_ROOT).as_posix()} | {format_bytes(path.stat().st_size)}")
    components.html(read_scene(path), height=height, scrolling=True)


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown("## North Slope Atlas")
        st.caption("Public-source regional workspace")
        st.markdown("---")
        requested_page = st.query_params.get("page", PAGES[0])
        if requested_page not in PAGES:
            requested_page = PAGES[0]
        page = st.radio(
            "Navigate",
            PAGES,
            index=PAGES.index(requested_page),
            label_visibility="collapsed",
        )
        if st.query_params.get("page") != page:
            st.query_params["page"] = page
        st.markdown("---")
        st.caption("Current milestone")
        st.markdown("**Regional atlas foundation**")
        st.progress(0.45)
        st.caption("Public GIS now. Runtime-only approved well logs later.")
    return page


def render_metric_row(files: list[dict[str, object]]) -> None:
    extensions = Counter(str(row["Type"]) for row in files)
    total_size = sum(int(row["Bytes"]) for row in files)
    cols = st.columns(4)
    cols[0].metric("Public well locations", "10,250")
    cols[1].metric("Seismic inventories", "62 total", "26 2D / 36 3D")
    cols[2].metric("Structural XYZ grids", "8")
    cols[3].metric("Workspace footprint", format_bytes(total_size))
    st.caption(
        f"{len(files):,} repository files | {extensions['.parquet']:,} Parquet layers | "
        f"{extensions['.html']:,} interactive HTML exports"
    )


def render_welcome(files: list[dict[str, object]]) -> None:
    st.markdown(
        """
        <div class="atlas-hero">
          <div class="atlas-kicker" style="color:#aee8ed">Alaska North Slope</div>
          <h1>Gas Hydrate Regional Atlas</h1>
          <p>
            A public-source regional context workspace for understanding the
            geology, wells, seismic coverage, and structural surfaces that will
            support future physics-constrained hydrate interpretation.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_metric_row(files)

    st.markdown("### Start Here")
    cols = st.columns(3)
    cards = [
        (
            "Explore the regional context",
            "Use the Regional Atlas to compare assessment units, seismic coverage, "
            "and well locations across the North Slope.",
        ),
        (
            "Inspect subsurface structure",
            "Open the Structural Explorer to review generated 3D surfaces and "
            "their relationship to the public well inventory.",
        ),
        (
            "Connect the manuscript",
            "Use the Research Framework to keep maps, measurements, future ML, "
            "and producibility logic tied to one scientific chain.",
        ),
    ]
    for col, (title, text) in zip(cols, cards):
        col.markdown(
            f'<div class="atlas-card"><h4>{title}</h4><p>{text}</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown("### What This Atlas Is For")
    st.write(
        "This release organizes the public regional foundation before restricted "
        "well logs arrive. It makes your existing notebook work legible, reusable, "
        "and presentation-ready while preserving a clean boundary around the "
        "future DOE runtime workflow."
    )
    st.markdown(
        """
        <div class="atlas-boundary">
          <strong>Data boundary:</strong> classified, controlled, or restricted
          material is not part of this repository. The future well-log engine will
          load approved data at runtime inside the authorized environment.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_project_roadmap() -> None:
    content = architecture_content()
    st.markdown('<div class="atlas-kicker">Living project plan</div>', unsafe_allow_html=True)
    st.title("Project Architecture & Activity Map")
    st.write(
        "A phone-friendly view of the project structure, current workstreams, "
        "dependencies, blockers, and next actions. This page reads the tracked "
        "project document directly so the website and repository stay aligned."
    )

    if not content:
        st.error("The architecture tracker is not available in this deployment.")
        return

    workstreams = markdown_table(markdown_section(content, "Workstream Activity Map"))
    components = markdown_table(markdown_section(content, "Component Map"))
    blockers = markdown_table(markdown_section(content, "Blockers and Risks"))

    if not workstreams.empty:
        statuses = workstreams["Status"].astype(str)
        cols = st.columns(4)
        cols[0].metric("Workstreams", len(workstreams))
        active = int(
            statuses.str.startswith("In progress").sum()
            + statuses.str.startswith("Partial").sum()
        )
        cols[1].metric("Active", active)
        waiting = int(
            statuses.str.startswith("Waiting").sum()
            + statuses.str.startswith("Blocked").sum()
        )
        cols[2].metric("Waiting / blocked", waiting)
        cols[3].metric("Complete", int(statuses.str.startswith("Complete").sum()))

    st.markdown("### How the System Connects")
    st.markdown(
        """
        <div class="roadmap-status">
          <strong>Public path</strong><br>
          Regional GIS &rarr; processed layers &rarr; Streamlit atlas &rarr;
          public research communication
        </div>
        <div class="roadmap-status">
          <strong>Scientific path</strong><br>
          Sources and manuscript &rarr; equations and interpretation rules &rarr;
          well-log requirements &rarr; tested classification workflow
        </div>
        <div class="roadmap-status">
          <strong>Authorized path</strong><br>
          Approved logs and core data &rarr; validation &rarr; feature engineering
          &rarr; interval screening &rarr; uncertainty-aware results
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Current Priority")
    st.markdown(
        """
        <div class="roadmap-next">
          <strong>Next project move</strong><br>
          Recover the full Excel workbook, PowerPoint, and public source files
          from the source laptop. Then confirm the header specification against
          workbook formulas before calibrating the well-log engine.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(markdown_section(content, "Current Priority"))

    st.markdown("### Workstream Status")
    if workstreams.empty:
        st.info("No workstream table is currently defined.")
    else:
        st.markdown(roadmap_cards(workstreams), unsafe_allow_html=True)
        desktop_table = workstreams.to_html(
            index=False,
            border=0,
            classes=["roadmap-table"],
            escape=True,
        )
        st.markdown(
            f'<div class="roadmap-desktop">{desktop_table}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("### Component Status")
    if not components.empty:
        st.dataframe(components, use_container_width=True, hide_index=True)

    st.markdown("### Blockers and Risks")
    if not blockers.empty:
        st.dataframe(blockers, use_container_width=True, hide_index=True)

    st.markdown("### Near-Term Sequence")
    st.markdown(markdown_section(content, "Near-Term Sequence"))

    with st.expander("Project boundaries and key decisions"):
        st.markdown("#### Data Boundary")
        st.markdown(markdown_section(content, "Data Boundary"))
        st.markdown("#### Key Decisions")
        st.markdown(markdown_section(content, "Key Decisions"))

    st.caption(
        "Source: docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md | "
        "Update the tracked document after important milestones or priority changes."
    )


def render_regional_atlas() -> None:
    st.markdown('<div class="atlas-kicker">Regional context</div>', unsafe_allow_html=True)
    st.title("Regional Atlas")
    st.write(
        "This interactive map is the existing regional visualization from the "
        "notebook workflow. It brings together the North Slope extent, assessment "
        "units, 2D seismic lines, 3D seismic footprints, and well locations."
    )
    cols = st.columns(3)
    cols[0].metric("Assessment units", "6")
    cols[1].metric("2D seismic surveys", "26")
    cols[2].metric("3D seismic footprints", "36")
    st.info(
        "Use the Plotly controls inside the map to zoom and inspect layers. "
        "The well-color selector switches the active well comparison."
    )
    render_scene(REGIONAL_SCENE, height=870)


def render_structural_explorer() -> None:
    st.markdown('<div class="atlas-kicker">Subsurface context</div>', unsafe_allow_html=True)
    st.title("Structural Explorer")
    st.write(
        "Compare regional structural horizons as lightweight surface planes. The "
        "horizontal axes use longitude and latitude, while optional context overlays "
        "connect the subsurface model to the North Slope study area."
    )
    cols = st.columns([2, 1])
    selected_surfaces = cols[0].multiselect(
        "Visible structural horizons",
        STRUCTURAL_HORIZONS,
        default=["NStopo", "NSLCU", "NSshublik", "NSbasement"],
        format_func=lambda name: f"{name} - {SURFACE_CATALOG[name]['Label']}",
    )
    cells_per_surface = cols[1].select_slider(
        "Surface detail",
        options=[1500, 3000, 6000, 12000],
        value=3000,
        format_func=lambda cells: f"Up to {cells:,} cells / horizon",
    )
    selected_overlays = st.multiselect(
        "Regional context overlays",
        CONTEXT_OVERLAYS,
        default=["North Slope study-area boundary", "Assessment-unit outlines"],
    )

    if selected_surfaces:
        st.caption(
            f"Rendering up to {cells_per_surface * len(selected_surfaces):,} surface cells. "
            "Interval-thickness grids remain documented in the Data Library but are "
            "not drawn as structural planes."
        )
        st.plotly_chart(
            build_geographic_structural_figure(
                selected_surfaces,
                cells_per_surface,
                selected_overlays,
            ),
            use_container_width=True,
        )
    else:
        st.info("Select at least one structural layer to draw the 3D view.")

    st.markdown("### Structural Layer Labels")
    surface_rows = [
        {
            "Code": code,
            "Plain-language label": metadata["Label"],
            "Meaning": metadata["Description"],
            "Boundary tag": "PUBLIC-SOURCE ATLAS",
        }
        for code, metadata in SURFACE_CATALOG.items()
    ]
    st.dataframe(surface_rows, use_container_width=True, hide_index=True)

    with st.expander("Advanced fallback: original heavy HTML scenes"):
        st.warning(
            "These notebook exports are preserved for completeness. They can lag "
            "because they embed much larger point collections."
        )
        label = st.selectbox("Original structural scene", list(STRUCTURAL_SCENES))
        if st.button("Load original heavy scene"):
            render_scene(STRUCTURAL_SCENES[label], height=870)


def render_data_library(files: list[dict[str, object]]) -> None:
    st.markdown('<div class="atlas-kicker">Public-source inventory</div>', unsafe_allow_html=True)
    st.title("Data Library")
    st.write(
        "The curated layer catalog explains the analytical role of the main data "
        "products. The repository browser below provides the full file-level view."
    )
    st.dataframe(LAYER_CATALOG, use_container_width=True, hide_index=True)
    st.caption(
        "Boundary tags label the public atlas data products. Future approved "
        "restricted inputs must remain outside this hosted repository."
    )

    st.markdown("### Repository Browser")
    extensions = sorted({str(row["Type"]) for row in files})
    cols = st.columns([1, 1])
    selected = cols[0].multiselect("File types", extensions, default=extensions)
    query = cols[1].text_input("Path contains", placeholder="Example: gis_ready_surfaces")
    filtered = [
        row
        for row in files
        if str(row["Type"]) in selected and query.lower() in str(row["Path"]).lower()
    ]
    st.dataframe(
        [{key: row[key] for key in ("Path", "Type", "Size")} for row in filtered],
        use_container_width=True,
        hide_index=True,
    )
    st.caption(f"Showing {len(filtered):,} of {len(files):,} repository files")

    st.markdown("### Known Quality Notes")
    st.warning(
        "The public well inventory contains 10,250 records. Of these, 9,894 have "
        "point geometry and 356 currently lack usable geometry. The atlas should "
        "preserve that distinction rather than silently treating all records as mappable."
    )


def render_framework() -> None:
    st.markdown('<div class="atlas-kicker">Manuscript blueprint</div>', unsafe_allow_html=True)
    st.title("Research Framework")
    st.write(
        "The manuscript is the scientific backbone of the application. It treats "
        "gas hydrate as a coupled petroleum-system and rock-physics outcome rather "
        "than a single-map or single-log anomaly."
    )
    for number, title, description in FRAMEWORK_STAGES:
        st.markdown(
            f'<div class="atlas-step"><strong>{number} · {title}</strong><br>{description}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("### Decision Rules To Preserve")
    st.markdown(
        """
        1. The gas hydrate stability zone defines where hydrate **can** exist, not where it must exist.
        2. Reservoir capacity, hydrate occupancy, saturation, and recoverability are separate outcomes.
        3. High resistivity alone is not a defensible hydrate label.
        4. Regional geology should constrain interval interpretation, not replace log-derived evidence.
        5. Producibility requires retained permeability, connected pore volume, pressure communication, and mechanical stability.
        """
    )


def render_future_engine() -> None:
    st.markdown('<div class="atlas-kicker">Synthetic planning scaffold</div>', unsafe_allow_html=True)
    st.title("Future Well-Log Engine")
    st.write(
        "This presentation-ready scaffold previews the outputs planned for the later "
        "runtime-only analysis module. It contains synthetic example records only."
    )
    st.warning(
        f"{SYNTHETIC_LABEL}. PUBLIC-SOURCE PLANNING SCAFFOLD. Do not upload approved "
        "well logs, core data, identifiers, populated sensitive outputs, derived "
        "sensitive results, or credentials to this hosted dashboard."
    )

    cols = st.columns(3)
    blocks = [
        (
            "Expected inputs",
            "<code>DEPTH</code>, <code>GR</code>, <code>RHOB</code>, "
            "<code>DT</code>, <code>DTS</code>, <code>Rt</code>, porosity "
            "channels, and NMR where available.",
        ),
        (
            "Derived features",
            "Shale volume, porosity, saturation proxies, <code>Vp</code>, "
            "<code>Vs</code>, <code>Vp/Vs</code>, elastic moduli, stress, "
            "permeability-risk proxy, and QA flags.",
        ),
        (
            "Outputs",
            "Admissibility, reservoir quality, phase evidence, saturation proxy, core confidence, uncertainty, and separate producibility screening.",
        ),
    ]
    for col, (title, text) in zip(cols, blocks):
        col.markdown(
            f'<div class="atlas-card"><h4>{title}</h4><p>{text}</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown("### Scientific Rules Kept Visible")
    st.markdown(
        """
        1. GHSZ is necessary but not sufficient.
        2. High Rt is evidence, not a hydrate label.
        3. Good reservoir sand can contain no hydrate.
        4. Geology and seismic context constrain confidence; they do not replace direct log evidence.
        5. NMR-density saturation is preferred where NMR exists; Archie is a supplementary cross-check with uncertainty flags.
        6. Hydrate occurrence, saturation, and producibility remain separate outputs.
        7. Validation must split by well, not randomly by depth sample.
        8. Maximum hydrate saturation is not automatically the best production target.
        """
    )

    logs = load_runtime_data()
    intervals = screen_intervals(logs)
    core = synthetic_core_placeholders()
    calibrated_core = nearby_log_calibration(logs, core)

    tabs = st.tabs(
        [
            "Variable Range Explorer",
            "Header & Track Blueprint",
            "Sweet-Spot Evidence Model",
            "Equation-to-Decision Map",
            "Hydrate Interpretation Range Guide",
            "Interval Screening Scaffold",
            "Core Calibration Scaffold",
            "Presentation Outputs",
        ]
    )
    with tabs[0]:
        render_variable_range_explorer(logs)
    with tabs[1]:
        render_header_blueprint()
    with tabs[2]:
        render_sweet_spot_evidence_model(intervals)
    with tabs[3]:
        render_equation_decision_map()
    with tabs[4]:
        render_range_guide()
    with tabs[5]:
        render_interval_screen(intervals)
    with tabs[6]:
        render_core_calibration(calibrated_core)
    with tabs[7]:
        render_presentation_outputs(logs, intervals, calibrated_core)

    st.markdown("### Planned Runtime Analysis Sequence")
    sequence = [
        ("1", "Stability admissibility", "Screen pressure-temperature context without using it as a positive label."),
        ("2", "Reservoir screening", "Identify clean reservoir intervals and preserve good-sand/no-hydrate outcomes."),
        ("3", "Phase classification", "Use multi-log evidence to distinguish hydrate, gas, water, and uncertainty."),
        ("4", "Charge and structure", "Apply regional context as a constraint on interval-scale evidence."),
        ("5", "Producibility ranking", "Separate detectability and saturation from pressure communication and flow risk."),
    ]
    for number, title, description in sequence:
        st.markdown(f"**{number}. {title}**  \n{description}")

    st.info(
        "Transfer point: the reusable calculation layer is isolated behind a runtime "
        "configuration adapter. Authorized LAS/CSV loading should be added and run "
        "locally inside the approved DOE environment."
    )


def render_variable_range_explorer(logs: pd.DataFrame) -> None:
    st.subheader("Variable Range Explorer")
    st.caption(f"{SYNTHETIC_LABEL} | Summary statistics are descriptive planning outputs, not universal thresholds.")
    wells = sorted(logs["well_alias"].unique())
    cols = st.columns([1, 1, 2])
    well = cols[0].selectbox("Synthetic location / well alias", wells)
    variable = cols[1].selectbox("Variable", list(VARIABLES), format_func=lambda name: VARIABLES[name][0])
    depth_min, depth_max = logs["depth_m"].min(), logs["depth_m"].max()
    depth_range = cols[2].slider("Depth interval (m)", float(depth_min), float(depth_max), (float(depth_min), float(depth_max)), step=5.0)
    subset = logs[(logs["well_alias"] == well) & logs["depth_m"].between(*depth_range)]
    label, unit = VARIABLES[variable]
    figure = go.Figure(go.Scatter(x=subset[variable], y=subset["depth_m"], mode="lines", name=label))
    figure.update_layout(title=f"{SYNTHETIC_LABEL} | {well} | {label}", xaxis_title=f"{label} ({unit})", yaxis_title="Depth (m)", height=530)
    figure.update_yaxes(autorange="reversed")
    if variable in SCREENING_BANDS:
        x0, x1, note = SCREENING_BANDS[variable]
        figure.add_vrect(
            x0=x0,
            x1=x1,
            fillcolor="rgba(22, 125, 141, 0.15)",
            line_width=0,
            annotation_text="working review band",
            annotation_position="top left",
        )
        figure.add_annotation(
            x=x1,
            y=float(subset["depth_m"].quantile(0.25)),
            text=note,
            showarrow=True,
            arrowhead=2,
            ax=70,
            ay=-45,
            bgcolor="rgba(255,255,255,0.92)",
            bordercolor="#167d8d",
            borderwidth=1,
            font={"size": 11},
        )
    st.plotly_chart(figure, use_container_width=True)
    summary = variable_range_summary(logs, [variable], well, depth_range)
    st.dataframe(summary, use_container_width=True, hide_index=True)
    st.download_button("Download variable-range table (CSV)", csv_bytes(summary), "synthetic_variable_range_table.csv", "text/csv", key="range_explorer_table")

    st.markdown("#### Cross-Well Comparison")
    cross_well = pd.concat(
        [
            variable_range_summary(logs, [variable], alias, depth_range).assign(**{"Well alias": alias})
            for alias in wells
        ],
        ignore_index=True,
    )
    st.plotly_chart(cross_well_range_figure(cross_well, label), use_container_width=True)
    st.dataframe(cross_well, use_container_width=True, hide_index=True)


def render_header_blueprint() -> None:
    st.subheader("Header & Track Blueprint")
    st.caption(
        "Derived from a normalized header-only reference. Names, units, roles, and "
        "layout guide the scaffold; no reference values are used."
    )
    st.warning(
        "Measured inputs, derived features, QC/alignment fields, and targets remain "
        "separate. Hydrate saturation and water-saturation fields are not ML inputs."
    )
    st.dataframe(
        pd.DataFrame(HEADER_SCHEMA_BLUEPRINT),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown(
        """
        **Planned track order:** depth and alignment; borehole QC; lithology;
        porosity; electrical response; elastic response; interpretation and
        calibration; uncertainty and readiness.

        Unit-aware loading is required before these headers can drive scientific
        calculations. In particular, depth appears in feet and meters, while bulk
        density appears in both `g/cc` and `kg/m3` conventions.
        """
    )


def render_sweet_spot_evidence_model(intervals: pd.DataFrame) -> None:
    st.subheader("Synthetic Sweet-Spot Evidence Model")
    st.caption(
        "Research-backed directional logic applied to synthetic data. The working "
        "thresholds are demonstrative and require local calibration before scientific use."
    )
    st.error(
        "A sweet spot is not the row with the largest hydrate-saturation proxy. "
        "It is an interval where hydrate evidence, reservoir quality, retained flow "
        "capacity, QC, and uncertainty remain jointly defensible."
    )
    st.dataframe(
        pd.DataFrame(SWEET_SPOT_EVIDENCE_MODEL),
        use_container_width=True,
        hide_index=True,
    )

    candidates = intervals[
        intervals["Synthetic sweet-spot review lane"].str.contains(
            "candidate sweet-spot",
            na=False,
        )
    ]
    st.markdown("#### Explainable Synthetic Candidates")
    if candidates.empty:
        st.info("No synthetic intervals currently satisfy the complete review lane.")
        return
    st.dataframe(
        candidates[
            [
                "Well alias",
                "Top depth (m)",
                "Base depth (m)",
                "Phase-classification evidence",
                "Hydrate-saturation proxy",
                "Permeability-retention proxy",
                "Evidence domains passed",
                "Blocking domains",
                "Interpretation summary",
                "Uncertainty flags",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


def render_equation_decision_map() -> None:
    st.subheader("Equation-to-Decision Map")
    st.caption(
        "This is the scaffold direction for the real-data project: measured logs become derived "
        "features, derived features feed staged physics gates, and only then does ML classify intervals."
    )
    st.info(
        "The key design choice: every future model feature must keep its physical meaning attached. "
        "That prevents the dashboard from saying 'hydrate' just because one curve looks interesting."
    )
    st.markdown("#### Derived Equation Library")
    st.dataframe(pd.DataFrame(EQUATION_LIBRARY), use_container_width=True, hide_index=True)

    st.markdown("#### Classification Workflow")
    st.dataframe(pd.DataFrame(CLASSIFICATION_WORKFLOW), use_container_width=True, hide_index=True)

    st.markdown("#### Rock-Type and Overburden Context")
    st.write(
        "Rock type and stress change the meaning of the same log value. A high-resistivity, "
        "high-stiffness interval in clean sand means something different than the same response "
        "in ice-bearing sediment, coal, carbonate, or a washed-out borehole."
    )
    st.dataframe(pd.DataFrame(ROCKTYPE_CONTEXT_GUIDE), use_container_width=True, hide_index=True)


def render_range_guide() -> None:
    st.subheader("Hydrate Interpretation Range Guide")
    st.caption(
        "Manuscript-backed working tendencies for planning. These ranges overlap competing "
        "end members and must not be treated as universal thresholds."
    )
    st.error("High resistivity alone is not a hydrate label. Stability is necessary but not sufficient.")
    st.dataframe(pd.DataFrame(RANGE_GUIDE), use_container_width=True, hide_index=True)
    st.markdown("#### Synthetic Sweet-Spot Planning Guide")
    st.write(
        "These saturation-proxy bands are presentation and expert-review lanes. "
        "They are not universal thresholds and they do not replace locally calibrated "
        "multi-log interpretation inside the authorized environment."
    )
    st.dataframe(pd.DataFrame(SWEET_SPOT_GUIDE), use_container_width=True, hide_index=True)
    st.markdown("#### Public Science Anchors")
    st.dataframe(pd.DataFrame(PUBLIC_SCIENCE_REFERENCES), use_container_width=True, hide_index=True)


def render_interval_screen(intervals: pd.DataFrame) -> None:
    st.subheader("Interval Screening Scaffold")
    st.caption(f"{SYNTHETIC_LABEL} | Separate staged outputs preserve good-sand/no-hydrate and expert-review outcomes.")
    well = st.selectbox("Synthetic interval-screen well alias", sorted(intervals["Well alias"].unique()))
    selected = intervals[intervals["Well alias"] == well]
    st.dataframe(selected, use_container_width=True, hide_index=True)
    st.download_button("Download interval-interpretation table (CSV)", csv_bytes(selected), "synthetic_interval_interpretation.csv", "text/csv", key="interval_screen_table")


def render_core_calibration(calibrated_core: pd.DataFrame) -> None:
    st.subheader("Core Calibration Scaffold")
    st.caption(
        f"{SYNTHETIC_LABEL} | Future approved pressure-core observations remain local. "
        "The placeholder table shows depth-match uncertainty and nearby-log linkage."
    )
    st.dataframe(calibrated_core, use_container_width=True, hide_index=True)
    st.download_button("Download core-to-log calibration table (CSV)", csv_bytes(calibrated_core), "synthetic_core_to_log_calibration.csv", "text/csv", key="core_calibration_table")


def render_presentation_outputs(logs: pd.DataFrame, intervals: pd.DataFrame, calibrated_core: pd.DataFrame) -> None:
    st.subheader("Presentation Outputs")
    st.caption(f"{SYNTHETIC_LABEL} | Export-ready placeholders for the existing PowerPoint scaffold.")
    well = st.selectbox("Presentation-output synthetic well", sorted(logs["well_alias"].unique()))
    panel = well_log_panel(logs, well)
    st.plotly_chart(panel, use_container_width=True)
    st.download_button("Download well-log panel (HTML)", figure_html_bytes(panel), "synthetic_well_log_panel.html", "text/html", key="presentation_well_panel")

    range_table = variable_range_summary(logs, well_alias=well)
    st.dataframe(range_table, use_container_width=True, hide_index=True)
    st.download_button("Download variable-range table (CSV)", csv_bytes(range_table), "synthetic_variable_range_table.csv", "text/csv", key="presentation_range_table")

    interval_table = intervals[intervals["Well alias"] == well]
    st.download_button("Download interval-interpretation table (CSV)", csv_bytes(interval_table), "synthetic_interval_interpretation.csv", "text/csv", key="presentation_interval_table")

    cross_well = pd.concat(
        [
            variable_range_summary(logs, ["rt_ohm_m"], alias).assign(**{"Well alias": alias})
            for alias in sorted(logs["well_alias"].unique())
        ],
        ignore_index=True,
    )
    cross_well_figure = cross_well_range_figure(cross_well, "Resistivity Rt")
    st.plotly_chart(cross_well_figure, use_container_width=True)
    st.download_button("Download cross-well comparison (HTML)", figure_html_bytes(cross_well_figure), "synthetic_cross_well_comparison.html", "text/html", key="presentation_cross_well")
    st.download_button("Download core-to-log table (CSV)", csv_bytes(calibrated_core), "synthetic_core_to_log_calibration.csv", "text/csv", key="presentation_core_table")

    uncertainty = intervals[["Data label", "Well alias", "Top depth (m)", "Base depth (m)", "Uncertainty flags"]]
    st.download_button("Download uncertainty summary (CSV)", csv_bytes(uncertainty), "synthetic_uncertainty_summary.csv", "text/csv", key="presentation_uncertainty")

    confusion, calibration = model_placeholder_figures()
    cols = st.columns(2)
    cols[0].plotly_chart(confusion, use_container_width=True)
    cols[1].plotly_chart(calibration, use_container_width=True)
    cols[0].download_button("Download placeholder confusion matrix (HTML)", figure_html_bytes(confusion), "synthetic_placeholder_confusion_matrix.html", "text/html", key="presentation_confusion")
    cols[1].download_button("Download placeholder calibration panel (HTML)", figure_html_bytes(calibration), "synthetic_placeholder_calibration_panel.html", "text/html", key="presentation_calibration")


def main() -> None:
    st.set_page_config(
        page_title="North Slope Gas Hydrate Atlas",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="auto",
    )
    apply_styles()
    files = project_files()
    page = render_sidebar()

    if page == "Welcome":
        render_welcome(files)
    elif page == "Project Roadmap":
        render_project_roadmap()
    elif page == "Regional Atlas":
        render_regional_atlas()
    elif page == "Structural Explorer":
        render_structural_explorer()
    elif page == "Data Library":
        render_data_library(files)
    elif page == "Research Framework":
        render_framework()
    else:
        render_future_engine()

    st.divider()
    st.caption(
        "North Slope Gas Hydrate Regional Atlas | Public-source foundation | "
        "Run inside OpenScienceLab"
    )


if __name__ == "__main__":
    main()
