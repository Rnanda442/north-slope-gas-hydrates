from __future__ import annotations

from collections import Counter
from pathlib import Path
import html

import streamlit as st
import streamlit.components.v1 as components


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = PROJECT_ROOT / "05_exports" / "html"

SCENES = {
    "North Slope master analysis scene": EXPORT_DIR / "north_slope_master_analysis_scene.html",
    "North Slope master scene, full resolution": EXPORT_DIR
    / "north_slope_master_analysis_scene_full_no_simplify.html",
    "Advanced North Slope Plotly view": EXPORT_DIR / "north_slope_plotly_advanced.html",
}

IGNORED_DIRS = {".git", ".ipynb_checkpoints", "__pycache__"}


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


def scene_html(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def render_metric_row(files: list[dict[str, object]]) -> None:
    extensions = Counter(str(row["Type"]) for row in files)
    total_size = sum(int(row["Bytes"]) for row in files)
    cols = st.columns(4)
    cols[0].metric("Tracked project files", f"{len(files):,}")
    cols[1].metric("Project footprint", format_bytes(total_size))
    cols[2].metric("Parquet layers", f"{extensions['.parquet']:,}")
    cols[3].metric("Interactive HTML scenes", f"{extensions['.html']:,}")


def render_overview() -> None:
    st.subheader("North Slope Gas Hydrate Workspace")
    st.write(
        "This dashboard is the URL-accessible front end for the unclassified "
        "Alaska North Slope workspace. The current repository is geospatial: it "
        "organizes public-source structural surfaces, wells, seismic coverage, "
        "assessment units, notebooks, and generated interactive scenes."
    )

    st.info(
        "The future wireline module is intentionally not populated with DOE data. "
        "It will be added as a configurable analysis extension that runs only in "
        "the approved environment."
    )

    st.markdown("#### Scientific framing")
    st.write(
        "The manuscript treats hydrate occurrence as a coupled petroleum-system "
        "and rock-physics outcome. Pressure-temperature stability is necessary, "
        "but it is not sufficient: gas charge, migration access, reservoir "
        "quality, trap geometry, water availability, timing, and geomechanics "
        "must overlap."
    )

    st.markdown("#### Current evidence layers")
    st.markdown(
        """
        - Alaska North Slope extent and assessment-unit geometry
        - Public-source well-bottom-hole locations
        - 2D seismic line coverage and 3D seismic inventory
        - Structural depth grids, including topographic, LCU, Shublik, and basement surfaces
        - Cleaned Parquet layers, GIS-ready surfaces, notebooks, and exported HTML scenes
        """
    )

    st.markdown("#### Interpretation chain")
    st.code(
        "environment -> tectonics -> deposition -> reservoir -> physics -> "
        "logs -> interpretation -> ML -> exploitation",
        language=None,
    )


def render_maps() -> None:
    st.subheader("Interactive Map Scenes")
    st.write(
        "These scenes are generated from the existing notebook workflow. Use the "
        "selector to switch between the lighter analysis view and the larger "
        "full-resolution scene."
    )
    label = st.selectbox("Scene", list(SCENES))
    scene = SCENES[label]
    if not scene.exists():
        st.warning(f"Scene has not been generated yet: {scene.relative_to(PROJECT_ROOT)}")
        return

    st.caption(f"{scene.relative_to(PROJECT_ROOT).as_posix()} | {format_bytes(scene.stat().st_size)}")
    components.html(scene_html(scene), height=820, scrolling=True)


def render_catalog(files: list[dict[str, object]]) -> None:
    st.subheader("Repository Data Catalog")
    st.write(
        "The catalog is generated directly from the checked-out repository. Use "
        "the filters to locate cleaned layers, raw public-source inputs, exports, "
        "and notebooks."
    )
    extensions = sorted({str(row["Type"]) for row in files})
    selected = st.multiselect("File types", extensions, default=extensions)
    query = st.text_input("Path contains", placeholder="Example: gis_ready_surfaces")
    filtered = [
        row
        for row in files
        if str(row["Type"]) in selected and query.lower() in str(row["Path"]).lower()
    ]
    table_rows = [{key: row[key] for key in ("Path", "Type", "Size")} for row in filtered]
    st.dataframe(table_rows, use_container_width=True, hide_index=True)
    st.caption(f"Showing {len(table_rows):,} of {len(files):,} files")


def render_wireline_roadmap() -> None:
    st.subheader("Wireline Hydrate Module Roadmap")
    st.write(
        "This tab records the future extension point without importing or "
        "simulating restricted data. The manuscript calls for transparent, "
        "multi-log interpretation rather than a single hydrate/no-hydrate rule."
    )

    st.markdown("#### Planned inputs")
    st.markdown(
        """
        - Depth and well identifier
        - Gamma ray (`GR`)
        - Bulk density (`RHOB`)
        - Compressional sonic (`DT`) and shear sonic (`DTS`)
        - Resistivity (`Rt`)
        - Porosity and NMR channels where available
        """
    )

    st.markdown("#### Planned outputs")
    st.markdown(
        """
        - Log quality-control flags and unit checks
        - Sand and shale screening
        - Hydrate-consistent, gas-consistent, water-bearing, and uncertain intervals
        - Saturation proxies with explicit assumptions
        - Elastic attributes such as `Vp`, `Vs`, `Vp/Vs`, lambda-rho, and mu-rho
        - Separate occurrence, saturation, and producibility rankings
        """
    )

    st.markdown("#### Guardrails from the manuscript")
    st.warning(
        "GHSZ does not equal hydrate presence. High resistivity alone is not a "
        "hydrate label. Stability, lithology, sonic behavior, NMR evidence where "
        "available, stress state, and reservoir context must remain visible."
    )

    st.markdown("#### Implementation status")
    st.write(
        "The application shell is ready. The next engineering step is a "
        "configurable LAS/CSV ingestion contract and an approved synthetic or "
        "public example dataset for end-to-end testing."
    )


def main() -> None:
    st.set_page_config(
        page_title="North Slope Gas Hydrate Dashboard",
        page_icon=None,
        layout="wide",
    )
    st.title("North Slope Gas Hydrate Dashboard")
    st.caption("Unclassified geospatial workspace and future wireline analysis shell")

    files = project_files()
    render_metric_row(files)

    tabs = st.tabs(["Overview", "Interactive maps", "Data catalog", "Wireline roadmap"])
    with tabs[0]:
        render_overview()
    with tabs[1]:
        render_maps()
    with tabs[2]:
        render_catalog(files)
    with tabs[3]:
        render_wireline_roadmap()

    st.divider()
    st.caption(
        html.escape(
            "Run inside OpenScienceLab. Keep restricted data and credentials out of GitHub."
        )
    )


if __name__ == "__main__":
    main()
