from __future__ import annotations

from pathlib import Path

from dashboard import mapbox_map_clean


STATIC_MAP_CANDIDATES = [
    (
        "Map panel used in Slide 2 source bundle",
        Path("docs")
        / "evidence"
        / "slide02_source_bundle_2026_06_17"
        / "slide02_selected_04_project_website_regional_map_reference.png",
        "This is the best repo candidate for the cropped North Slope map panel inside the slide screenshot.",
    ),
    (
        "Full V5.5 Slide 2 composite PNG",
        Path("docs")
        / "project_blueprints"
        / "presentation_assets"
        / "v5_5_slide2_source_update_2026_06_17"
        / "slide_02_source_context_v5_5.png",
        "This is the full slide-style composite that combines the stability/P-T figure with the North Slope map panel.",
    ),
]


def render_regional_atlas_with_static_png_review(app_module) -> None:
    st = app_module.st
    project_root = app_module.PROJECT_ROOT

    mapbox_map_clean.render_regional_atlas_clean(app_module)

    st.markdown("---")
    st.subheader("Static PNG candidates for the original slide map")
    st.write(
        "Use these tracked PNGs to verify which exact raster image matches the screenshot. "
        "These are repository files, not generated from the live interactive map."
    )

    for title, relative_path, note in STATIC_MAP_CANDIDATES:
        path = project_root / relative_path
        with st.expander(title, expanded=True):
            st.code(relative_path.as_posix())
            st.caption(note)
            if path.exists():
                st.image(str(path), use_container_width=True)
            else:
                st.error(f"Missing in this checkout: {relative_path.as_posix()}")
