from __future__ import annotations

from collections import Counter
from html import escape
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

from dashboard.runtime.feature_engineering import add_standard_features
from dashboard.runtime.schemas import (
    CHONG_ML_FEATURE_COLUMNS,
    PROJECT_COHORT_ASSUMPTIONS,
    TARGET_LABEL_CONTRACT,
)
from dashboard.runtime.validation import (
    curve_coverage_frame,
    grouped_well_split_frame,
    output_readiness_frame,
    project_cohort_plan_frame,
    readiness_frame,
    validate_log_table,
)
from dashboard.well_log_engine import (
    CLASSIFICATION_WORKFLOW,
    EQUATION_LIBRARY,
    HEADER_SCHEMA_BLUEPRINT,
    RANGE_GUIDE,
    PUBLIC_SCIENCE_REFERENCES,
    ROCKTYPE_CONTEXT_GUIDE,
    SCREENING_BANDS,
    SOURCE_LIBRARY_COVERAGE,
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
    sweet_spot_review_table,
    synthetic_core_placeholders,
    variable_range_summary,
    well_log_panel,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = PROJECT_ROOT / "05_exports" / "html"
ARCHITECTURE_PATH = PROJECT_ROOT / "docs" / "PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md"
VISION_PATH = PROJECT_ROOT / "docs" / "PROJECT_VISION_GOALS_AND_NEXT_STEPS.md"
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
    "North Slope Sweet Spots",
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


def vision_content() -> str:
    if not VISION_PATH.exists():
        return ""
    return VISION_PATH.read_text(encoding="utf-8")


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
    vision = vision_content()
    st.markdown('<div class="atlas-kicker">Living project plan</div>', unsafe_allow_html=True)
    st.title("Project Vision, Goals & Next Steps")
    st.write(
        "The current scientific objective, deliverable priorities, ML direction, "
        "workstreams, blockers, and ordered next actions. This page reads the "
        "tracked project documents directly so the website and repository stay aligned."
    )

    if not content or not vision:
        st.error("The vision or architecture tracker is not available in this deployment.")
        return

    st.markdown("### Project Vision")
    st.markdown(markdown_section(vision, "Project Vision"))
    st.markdown("### Primary Goal")
    st.markdown(markdown_section(vision, "Primary Goal"))

    goal_cols = st.columns(3)
    goal_cols[0].metric("Primary outputs", "Detection + saturation")
    goal_cols[1].metric("Presentation target", "~8 visual slides")
    goal_cols[2].metric("Validation unit", "Held-out wells")

    with st.expander("Deliverables, inputs, and ML direction", expanded=True):
        st.markdown("#### Deliverable Priority")
        st.markdown(markdown_section(vision, "Deliverable Priority"))
        st.markdown("#### Expected Approved Inputs")
        st.markdown(markdown_section(vision, "Expected Approved Inputs"))
        st.markdown("#### ML Direction")
        st.markdown(markdown_section(vision, "ML Direction"))

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
          Recover the full Excel workbook, confirm the target labels and units,
          and convert the recovered presentation into the requested concise,
          visual deliverable. Build grouped-well evaluation before model tuning.
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

    st.markdown("### Immediate Next Steps")
    st.markdown(markdown_section(vision, "Immediate Next Steps"))

    with st.expander("Decisions still needed"):
        st.markdown(markdown_section(vision, "Decisions Still Needed"))

    with st.expander("Project boundaries and key decisions"):
        st.markdown("#### Data Boundary")
        st.markdown(markdown_section(content, "Data Boundary"))
        st.markdown("#### Key Decisions")
        st.markdown(markdown_section(content, "Key Decisions"))

    st.caption(
        "Sources: docs/PROJECT_VISION_GOALS_AND_NEXT_STEPS.md and "
        "docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md | "
        "Update the tracked document after important milestones or priority changes."
    )


def render_sweet_spot_page() -> None:
    st.markdown('<div class="atlas-kicker">Synthetic decision workspace</div>', unsafe_allow_html=True)
    st.title("North Slope Gas-Hydrate Sweet Spots")
    st.write(
        "A focused, research-aligned review of synthetic intervals using the full "
        "well-log, reservoir, pressure-temperature, and geomechanical scaffold. "
        "This page demonstrates how future approved data will be evaluated."
    )
    st.warning(
        f"{SYNTHETIC_LABEL}. Review priorities are workflow-triage aids, not hydrate "
        "probabilities, reserves, or calibrated North Slope thresholds."
    )

    logs = load_runtime_data()
    intervals = screen_intervals(logs)
    ranked = sweet_spot_review_table(intervals)
    candidates = intervals[
        intervals["Synthetic sweet-spot review lane"].str.contains(
            "candidate sweet-spot",
            na=False,
        )
    ]

    metric_cols = st.columns(4)
    metric_cols[0].metric("Synthetic intervals", len(intervals))
    metric_cols[1].metric("Review-lane candidates", len(candidates))
    metric_cols[2].metric(
        "Hydrate-supportive",
        int(intervals["Phase-classification evidence"].str.startswith("hydrate").sum()),
    )
    metric_cols[3].metric(
        "Good sand, no hydrate",
        int((intervals["Phase-classification evidence"] == "good sand, no hydrate").sum()),
    )

    st.markdown("### Ranked Review Queue")
    st.caption(
        "Priority balances reservoir quality, multi-log hydrate evidence, retained "
        "flow capacity, moderate-occupancy preference, QC, stability, and stress context."
    )
    st.dataframe(ranked, use_container_width=True, hide_index=True)

    interval_labels = {
        f'{row["Well alias"]} | {row["Top depth (m)"]}-{row["Base depth (m)"]} m': index
        for index, row in intervals.iterrows()
    }
    selected_label = st.selectbox(
        "Inspect a synthetic interval",
        list(interval_labels),
        index=0,
    )
    selected = intervals.loc[interval_labels[selected_label]]

    st.markdown("### Selected Interval Decision")
    decision_cols = st.columns(4)
    decision_cols[0].metric("Review priority", f'{selected["Synthetic review priority"]:.2f}')
    decision_cols[1].metric("Reservoir quality", f'{selected["Reservoir-quality score"]:.2f}')
    decision_cols[2].metric("Hydrate evidence", f'{selected["Hydrate-evidence score"]:.2f}')
    decision_cols[3].metric(
        "Flow retention",
        f'{selected["Permeability-retention proxy"]:.2f}',
    )
    st.info(str(selected["Interpretation summary"]))
    st.write(
        f'**Review lane:** {selected["Synthetic sweet-spot review lane"]}  \n'
        f'**Passed evidence:** {selected["Evidence domains passed"]}  \n'
        f'**Blocking domains:** {selected["Blocking domains"]}  \n'
        f'**Uncertainty:** {selected["Uncertainty flags"]}'
    )

    evidence_values = {
        "Reservoir": selected["Reservoir-quality score"],
        "Hydrate evidence": selected["Hydrate-evidence score"],
        "Saturation proxy": selected["Hydrate-saturation proxy"],
        "Flow retention": selected["Permeability-retention proxy"],
        "QC": 0 if "borehole QC review" in selected["Uncertainty flags"] else 1,
        "Stability": 0 if selected["Stability admissibility"] == "outside / uncertain" else 1,
    }
    evidence_figure = go.Figure(
        go.Bar(
            x=list(evidence_values.values()),
            y=list(evidence_values),
            orientation="h",
            marker_color=["#167d8d", "#d9773d", "#4c78a8", "#59a14f", "#8f6bb3", "#76b7b2"],
            text=[f"{value:.2f}" for value in evidence_values.values()],
            textposition="auto",
        )
    )
    evidence_figure.update_layout(
        title="Evidence Profile",
        xaxis={"range": [0, 1], "title": "Synthetic normalized support"},
        yaxis={"autorange": "reversed"},
        height=390,
        margin={"l": 0, "r": 0, "t": 45, "b": 0},
    )
    st.plotly_chart(evidence_figure, use_container_width=True)

    tabs = st.tabs(
        [
            "Input Variables",
            "Geomechanics",
            "Competing Explanations",
            "Science and Sources",
        ]
    )
    with tabs[0]:
        input_rows = [
            ("GR", selected["GR median (API)"], "API", "Lithology and clean-sand screen"),
            ("Rt", selected["Rt median (ohm m)"], "ohm m", "Electrical hydrate evidence; non-unique"),
            ("RHOB", selected["RHOB median (g/cc)"], "g/cc", "Density and porosity constraint"),
            ("Density porosity", selected["Density porosity median"], "v/v", "Reservoir capacity"),
            ("NMR porosity", selected["NMR porosity median"], "v/v", "Mobile-fluid response where available"),
            ("Vp", selected["Vp median (km/s)"], "km/s", "Compressional stiffness and gas discrimination"),
            ("Vs", selected["Vs median (km/s)"], "km/s", "Rigidity and hydrate-versus-gas support"),
            ("Vp/Vs", selected["Vp/Vs median"], "ratio", "Elastic phase context"),
            ("Hydrate saturation proxy", selected["Hydrate-saturation proxy"], "fraction", selected["Proxy source"]),
        ]
        st.dataframe(
            pd.DataFrame(input_rows, columns=["Variable", "Interval median", "Unit", "Decision role"]),
            use_container_width=True,
            hide_index=True,
        )
    with tabs[1]:
        geomechanics = pd.DataFrame(
            [
                ("Shear modulus", selected["Shear modulus (GPa)"], "GPa", "Rigidity"),
                ("Bulk modulus", selected["Bulk modulus (GPa)"], "GPa", "Compressibility"),
                ("Young's modulus", selected["Young's modulus (GPa)"], "GPa", "Stiffness"),
                ("Poisson ratio", selected["Poisson ratio"], "ratio", "Elastic behavior"),
                ("Lambda-rho", selected["Lambda-rho"], "GPa g/cc", "Fluid/compressibility context"),
                ("Mu-rho", selected["Mu-rho"], "GPa g/cc", "Rigidity context"),
                ("Vertical stress", selected["Vertical stress (MPa)"], "MPa", "Overburden"),
                ("Effective stress", selected["Effective stress (MPa)"], "MPa", "Compaction and flow risk"),
            ],
            columns=["Property", "Synthetic interval median", "Unit", "Interpretation role"],
        )
        st.dataframe(geomechanics, use_container_width=True, hide_index=True)
        st.caption(
            "High stiffness can support hydrate interpretation, but burial, effective "
            "stress, ice, cementation, and competent lithology can mimic the response."
        )
    with tabs[2]:
        st.dataframe(
            pd.DataFrame(ROCKTYPE_CONTEXT_GUIDE),
            use_container_width=True,
            hide_index=True,
        )
        st.error(
            "High resistivity plus low Vp remains gas-supportive. High stiffness "
            "without reservoir and pore-fluid agreement remains a lithology/stress review."
        )
    with tabs[3]:
        source_metrics = st.columns(3)
        source_metrics[0].metric("Primary public references", len(PUBLIC_SCIENCE_REFERENCES))
        source_metrics[1].metric(
            "Indexed project artifacts",
            sum(row["Indexed artifacts"] for row in SOURCE_LIBRARY_COVERAGE),
        )
        source_metrics[2].metric("Source groups", len(SOURCE_LIBRARY_COVERAGE))
        st.caption(
            "The four connected-Drive documents were one synthesis subset. "
            "They are not the project's total source base."
        )
        st.dataframe(
            pd.DataFrame(SWEET_SPOT_EVIDENCE_MODEL),
            use_container_width=True,
            hide_index=True,
        )
        st.subheader("Source Library Coverage")
        st.dataframe(
            pd.DataFrame(SOURCE_LIBRARY_COVERAGE),
            use_container_width=True,
            hide_index=True,
        )
        st.subheader("Verified Primary Public References")
        st.dataframe(
            pd.DataFrame(PUBLIC_SCIENCE_REFERENCES),
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            "Project manuscripts, equation maps, and Drive synthesis documents organize "
            "the workflow but are not counted as independent confirmation. Final "
            "thresholds require source-by-source verification and authorized-data calibration."
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
            "Runtime Readiness & ML Plan",
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
        render_runtime_readiness(logs)
    with tabs[1]:
        render_variable_range_explorer(logs)
    with tabs[2]:
        render_header_blueprint()
    with tabs[3]:
        render_sweet_spot_evidence_model(intervals)
    with tabs[4]:
        render_equation_decision_map()
    with tabs[5]:
        render_range_guide()
    with tabs[6]:
        render_interval_screen(intervals)
    with tabs[7]:
        render_core_calibration(calibrated_core)
    with tabs[8]:
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


def render_runtime_readiness(logs: pd.DataFrame) -> None:
    st.subheader("Runtime Readiness & ML Plan")
    st.caption(
        f"{SYNTHETIC_LABEL} | Source-driven readiness demonstration based on the "
        "June 8 project answers and Chong et al. (2022)."
    )
    features = add_standard_features(logs)
    report = validate_log_table(logs)
    coverage = curve_coverage_frame(logs)
    outputs = output_readiness_frame(features)
    splits = grouped_well_split_frame(logs)

    ready_outputs = int((outputs["Status"] == "Ready").sum())
    partial_outputs = int((outputs["Status"] == "Partial").sum())
    blocked_outputs = int((outputs["Status"] == "Blocked").sum())
    metrics = st.columns(4)
    metrics[0].metric("Input status", report.status.title())
    metrics[1].metric("Ready outputs", ready_outputs)
    metrics[2].metric("Partial outputs", partial_outputs)
    metrics[3].metric("Blocked outputs", blocked_outputs)

    st.markdown("#### Curve Coverage and Routing")
    st.dataframe(coverage, use_container_width=True, hide_index=True)

    st.markdown("#### Output Readiness")
    st.dataframe(outputs, use_container_width=True, hide_index=True)
    st.info(
        "NMR-density saturation is preferred when NMR exists. Missing NMR does "
        "not block the full workflow: electrical saturation remains a flagged "
        "cross-check, and the model can test other log combinations."
    )

    st.markdown("#### Complete-Well Evaluation Split")
    st.dataframe(splits, use_container_width=True, hide_index=True)
    st.error(
        "Do not randomly split neighboring depth rows across train and test. "
        "The final model must demonstrate performance on wells excluded from training."
    )

    st.markdown("#### Planned 71-Well Cohort Design")
    cohort_plan = project_cohort_plan_frame(
        total_wells=PROJECT_COHORT_ASSUMPTIONS["Estimated total wells"],
        known_fraction=PROJECT_COHORT_ASSUMPTIONS["Known development fraction"],
    )
    st.dataframe(cohort_plan, use_container_width=True, hide_index=True)
    st.caption(
        "Working estimate: 14 known wells support model development and 57 wells "
        "form the prediction cohort. Final counts depend on label completeness and "
        "whether all wells contain compatible curves."
    )
    st.warning(
        "The 20% known-well cohort cannot be used entirely for fitting. Whole wells "
        "inside that cohort must remain unseen for validation and a locked test."
    )
    st.caption(
        "Normalization ranges, imputers, feature selection, and any learned variable "
        "weights must be fitted on training wells only, then applied unchanged to "
        "validation, locked-test, and prediction wells."
    )

    st.markdown("#### Supervised Target Contract")
    st.dataframe(pd.DataFrame(TARGET_LABEL_CONTRACT), use_container_width=True, hide_index=True)
    st.info(
        "Current assumption: NMR and the screenshot-listed fields are available. "
        "Saturation training must still identify the authoritative target as supplied, "
        "NMR-derived, core-calibrated, or documented interpreted saturation. The same "
        "normalized log families may support both outputs, but classification and "
        "saturation remain separate models or model heads."
    )

    st.markdown("#### Attached-Paper Feature Contract")
    st.write(
        "The source paper tests density, porosity, resistivity, gamma ray, Vp, "
        "and Vs. The runtime keeps each feature physically interpretable and "
        "records missing-curve routes instead of silently inventing measurements."
    )
    st.code("\n".join(CHONG_ML_FEATURE_COLUMNS), language="text")

    issues = readiness_frame(report)
    if issues.empty:
        st.success("No blocking synthetic input issues were detected.")
    else:
        st.markdown("#### Input Issues")
        st.dataframe(issues, use_container_width=True, hide_index=True)


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
    elif page == "North Slope Sweet Spots":
        render_sweet_spot_page()
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
