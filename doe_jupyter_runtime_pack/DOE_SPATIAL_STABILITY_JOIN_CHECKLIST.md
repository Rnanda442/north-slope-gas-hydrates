# DOE Spatial Stability Join Checklist

Use this when the DOE desktop needs to compare the four active/case wells
against the public stability-screen context and generate local maps.

## Minimum Files Needed

These should come with the GitHub repo:

- `data/public_ml_products/four_well_case_location_index_2026-06-19.csv`
- `data/public_stability_products/stability_screen_2026-06-14_methane_5ppt_v1.csv`
- `data/public_stability_products/public_ml_feature_scaffold_2026-06-15.csv`
- `data/public_stability_products/stability_temperature_model_2026-06-14.csv`
- `data/public_stability_products/phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1.csv`
- `data/public_stability_snapshot/north_slope_stability_snapshot_2026-06-13/ggd223_permafrost_controls.csv`
- `data/public_stability_snapshot/north_slope_stability_snapshot_2026-06-13/GasHydrateAUs.geojson`
- `data/public_gis_products/north_slope_borough_boundary_tiger2025.geojson`

## DOE-Local Files Needed

These should stay on the DOE desktop or approved runtime storage:

- `curated_dataset1.xlsx`
- `curated_dataset2.xlsx`
- `curated_dataset3.xlsx`
- optional `wellnametodataset.txt`
- the local temperature-gradient CSV if it is newer or more specific than the
  public scaffold
- any local approved case-well coordinate table if the public four-well index
  is not the correct runtime authority

## Optional OSL/GIS Layers For Better Maps

These are not required for the nearest stability join, but they are needed if
you want DOE to rebuild the richer map with roads, TAPS, field labels, and
landmark context:

- `data/source_library/basemap_landmarks_2026_06_18/alaska_dnr_unit_boundary_current_north_slope_clip.geojson`
- `data/source_library/basemap_landmarks_2026_06_18/alaska_akdot_roads_north_slope_clip.geojson`
- `data/source_library/basemap_landmarks_2026_06_18/alaska_dnr_trans_alaska_pipeline.geojson`
- `data/source_library/basemap_landmarks_2026_06_18/usgs_gnis_places_north_slope_clip.geojson`
- DGGS RI 2018-6 Umiat-Gubik geology GeoPackage/shapefile package, if DOE
  should rebuild the geology layer instead of using the committed preview
- any approved DOE-only GIS layers needed for internal review

Do not push OSL-only or DOE-only raw GIS packages unless the source, size, and
license/public-safety status are approved.

## Command

From the repo root in DOE Anaconda:

```bash
python doe_jupyter_runtime_pack/run_spatial_stability_join.py
```

With local data paths:

```bash
python doe_jupyter_runtime_pack/run_spatial_stability_join.py ^
  --case-wells-csv data/public_ml_products/four_well_case_location_index_2026-06-19.csv ^
  --temperature-gradient-csv "D:/DOE/local_temperature_gradient.csv" ^
  --output-dir outputs_runtime/doe_spatial_stability_join_current
```

If the approved runtime has its own four-well coordinate table, use:

```bash
python doe_jupyter_runtime_pack/run_spatial_stability_join.py ^
  --case-wells-csv "D:/DOE/approved_runtime/four_well_locations.csv" ^
  --output-dir outputs_runtime/doe_spatial_stability_join_current
```

## Outputs

The script writes local-only files:

- `case_well_stability_context.csv`
- `nearby_stability_screen_points.csv`
- `case_well_stability_context_map.html`
- optional `case_well_stability_context_map.png`
- `spatial_stability_join_manifest.json`

These are review artifacts. They should stay local until checked for public
safety.

## Guardrails

- Stability-screen rows are P-T admissibility/context only.
- A nearby calculated stability interval is not hydrate occurrence proof.
- Outside or blocked stability context is not automatically a negative hydrate
  label.
- Do not use stability status as a target label.
- First use stability as a post-model overlay. Only later test it as optional
  context features with ablation.

