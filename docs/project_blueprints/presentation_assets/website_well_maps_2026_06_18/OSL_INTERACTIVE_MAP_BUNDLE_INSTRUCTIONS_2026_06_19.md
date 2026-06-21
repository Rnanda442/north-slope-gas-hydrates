# OSL Interactive Map Bundle Instructions

Goal: restore the website 2D North Slope well map as a real interactive layer
map while keeping the full PNG as slide/export fallback only.

## Pull This Branch On OSL / PC

```powershell
git fetch --all --prune
git checkout codex/stability-map-focus-20260619
git pull
```

## Verify The OSL Source Folder Exists

Expected ignored/raw source folder:

```text
data/source_library/basemap_landmarks_2026_06_18/
```

Expected public source files inside that folder:

```text
alaska_dnr_unit_boundary_current_north_slope_clip.geojson
alaska_akdot_roads_north_slope_clip.geojson
alaska_dnr_trans_alaska_pipeline.geojson
usgs_gnis_places_north_slope_clip.geojson
census_tiger_2025_alaska_places.zip
```

The Census zip is optional for labels. The first four files are required for
the full interactive landmark layer bundle.

## Export The Public-Safe Website Bundle

```powershell
python 01_pipeline\export_public_basemap_landmarks_2026_06_19.py
```

This writes the tracked website-runtime bundle here:

```text
data/public_gis_products/basemap_landmarks_2026_06_18/
```

Expected generated files:

```text
alaska_dnr_unit_boundary_current_north_slope_clip.geojson
alaska_akdot_roads_north_slope_clip.geojson
alaska_dnr_trans_alaska_pipeline.geojson
usgs_gnis_places_north_slope_clip.geojson
census_tiger_2025_alaska_places_north_slope_clip.geojson
manifest.json
README.md
```

## Validate

```powershell
python -m py_compile dashboard\app.py 01_pipeline\export_public_basemap_landmarks_2026_06_19.py
python -m pytest tests\test_stability_screen_diagnostics.py tests\test_stability_products.py
streamlit run streamlit_app.py
```

Open:

```text
http://localhost:8501/?page=Explore%20North%20Slope
```

The page should default to the interactive unified map when the public bundle
is present. The combined PNG should remain available as a fallback/export, not
the main website map.

## Commit Only Public-Safe Outputs

Safe to commit:

```text
data/public_gis_products/basemap_landmarks_2026_06_18/*.geojson
data/public_gis_products/basemap_landmarks_2026_06_18/manifest.json
data/public_gis_products/basemap_landmarks_2026_06_18/README.md
```

Do not commit:

```text
data/source_library/basemap_landmarks_2026_06_18/
raw statewide GIS zips unless explicitly approved
approved DOE rows
private screenshots or workbooks
row-level predictions
trained models
fitted scalers
credentialed PDFs
```

Suggested commit:

```powershell
git add data\public_gis_products\basemap_landmarks_2026_06_18
git commit -m "data: add public interactive basemap landmark bundle"
git push
```

## Optional Static PNG Refresh

After the public bundle exists, the PC can also refresh the slide/export PNGs:

```powershell
python docs\project_blueprints\build_unified_north_slope_context_map.py
```

Only do this where the OSL source layers are present, otherwise the generated
PNG can lose DNR/road/TAPS/community context.
