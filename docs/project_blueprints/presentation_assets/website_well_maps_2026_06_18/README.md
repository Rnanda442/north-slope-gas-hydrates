# Website 2D Well Map Captures And Basemap Upgrade Notes

Date: 2026-06-18

## Captured Website Images

These images are 2026-06-18 website and static-builder captures for the
unified `Explore North Slope > Regional Map` section. The original
`website_2d_...` captures document the pre-landmark-overlay public-safe website
state. The `unified_north_slope_...` exports are the current map source for
Slide 2 and Slide 7 orientation/context.

| Image | Current use | Visual QA |
| --- | --- | --- |
| `unified_north_slope_well_stability_context_map_2026_06_18.png` | Main readable export for the unified website map | Supersedes the prior status-only slide map by combining Geoscience Orientation layers, DGGS RI 2018-6 Umiat-Gubik geology preview, GGD223 `pf_depth_m` controls with colorbar, USGS hydrate AU outlines, stability-screen status points, DNR oil/gas unit outlines, AKDOT roads, Dalton/Deadhorse roads, TAPS, communities, and public field labels. |
| `unified_north_slope_slide_export_callout_space_2026_06_18.png` | Slide 2 / Slide 7 map layer with editable-callout room | Same public-safe context stack as the full unified map, cropped into a 16:9 slide plate with a right-side callout lane so labels, circles, and arrows can remain editable in PowerPoint or Google Slides. |
| `slide3_correct_2d_well_stability_map_2026_06_18.png` | Correct slide-3/website-map export for the updated 2D well/stability context | Uses the updated map layers: Alaska DNR oil/gas unit outlines, AKDOT roads with Dalton/Deadhorse roads highlighted, Trans-Alaska Pipeline geometry, Census/GNIS community label context, public well field labels, and a caveat that these overlays are context rather than hydrate evidence. |
| `website_2d_well_map_stability_status_2026_06_18.png` | Guarded methane 5 ppt stability-screen status map | Shows well distribution and screen categories, but the base layer does not make Prudhoe Bay, Kuparuk River, Milne Point, Deadhorse, or the Dalton/TAPS corridor obvious enough for a mentor audience. Use as a placeholder only until landmark overlays are added. |
| `website_2d_well_map_temperature_coverage_2026_06_18.png` | Temperature-profile/proxy coverage diagnostic map | Good for explaining source coverage and blank-row reasons. It should not be used as the main hydrate science map because it is a data-readiness view, not an occurrence/saturation view. |
| `website_2d_well_maps_contact_sheet_2026_06_18.png` | QA contact sheet | Confirms both captures, including the current weak landmark context. |

## Recommended Slide Placement

1. **Unified website map**: use
   `unified_north_slope_well_stability_context_map_2026_06_18.png`. It supports
   "where the public scaffold is," "what the current stability screen covers,"
   "which public context layers orient the wells," and "where the GGD223 and
   USGS AU source controls sit," not a hydrate-proof claim.
2. **Slide 2 / Slide 7 callout map**: use
   `unified_north_slope_slide_export_callout_space_2026_06_18.png` as the
   slide base map. Keep the callout labels/arrows editable in the deck instead
   of baking all explanation into the PNG.
3. **Older Slide 3 / 2D well-stability context**: keep
   `slide3_correct_2d_well_stability_map_2026_06_18.png` as the predecessor
   that established the OSL GIS-layer visual style. It is superseded for main
   map use because it does not show the USGS AU outlines and GGD223
   `pf_depth_m` source controls together.
4. **What we have done / status slide**: use the stability-status map here if
   Slide 2 is already carrying the hydrate definition and source-backed phase
   curve. Caption it as a guarded public stability-admissibility screen.
5. **Later methods/status slide or appendix**: use the temperature-coverage map
   to explain why some wells are direct G10015 temperature matches, proxy
   candidates, or still blank. This map is best for data-readiness discussion.
6. **Slide 3 signal-response rebuild**: do not make either 2D map the main
   visual. Slide 3 should stay focused on depth-aligned log signal movement.
   A small orientation inset is acceptable only if it helps explain stability
   context.

## Unified Map Website Placement

The website now uses **Unified 2D North Slope Map For Slides 2 And 7** as the
main `Explore North Slope > Regional Map` view. The same layer stack is the
public map source for the slide-callout export.

The older maps remain secondary:

- The old geoscience orientation/DGGS views are retained under
  `Reference-only legacy map views and source card`; their core public context
  is now integrated into the main unified map.
- The old status-only 2D screen map is under
  `Reference: status-only 2D screen map`.
- The public source bundle map remains source/reference evidence for GGD223 and
  USGS AU layers.

## Basemap Upgrade Implemented

The website map builders now look for the public GIS package at:

`data/source_library/basemap_landmarks_2026_06_18/`

When that folder is present in OSL or a local run, the stability-status map and
temperature-coverage map add:

- Alaska DNR oil/gas unit outlines.
- AKDOT local roads, with Dalton/Deadhorse roads highlighted.
- Trans-Alaska Pipeline geometry.
- Census/GNIS community labels where available.
- Large public-well field labels derived from the public stability screen
  `field`, `lat`, and `lon` columns.

The maps still fall back to the original point-only view when the local source
folder is absent.

## Remaining Basemap Problem

The old website map base was readable as a well scatter plot but weak as an
orientation map. Mentors asking "where is Prudhoe Bay?" was a valid signal that
the map needed explicit field, community, road, coast, and pipeline labels.
The implemented overlays address the field/community/road/pipeline part. A
future static deck export could still add a cleaner coast, scale bar, north
arrow, and Alaska inset.

Recommended map upgrades:

- Add large labels and leader lines for Prudhoe Bay, Kuparuk River, Milne Point,
  Deadhorse, Nuiqsut, Utqiagvik, Beaufort Sea, Brooks Range, Dalton Highway, and
  the Trans-Alaska Pipeline corridor.
- Add DNR oil/gas unit boundaries as thin gray outlines with only selected labels
  visible.
- Add AKDOT roads, highlighting the Dalton Highway and key North Slope access
  roads.
- Add Census/GNIS place labels for communities and use the existing public well
  `field` column to derive oil-field label centroids.
- Keep the status colors separate from geography. The map should say
  "stability-admissibility screen status," not "hydrate found."
- For static slides, render from local GIS layers in Alaska Albers/EPSG:3338
  instead of relying only on a web tile label layer.

## Local OSL Upload Staging

Public GIS candidates were downloaded to the ignored local folder:

`data/source_library/basemap_landmarks_2026_06_18/`

That folder is not tracked by git. The tracked source matrix in this folder
records the official URLs, local staged filenames, feature counts where checked,
and why each layer helps.

## GitHub-Safe Versus OSL/Drive-Only Layers

GitHub-safe committed or derived layers used in the unified map:

- `data/public_stability_products/stability_screen_2026-06-14_methane_5ppt_v1.csv`
  for public stability-screen status points.
- `data/public_stability_snapshot/north_slope_stability_snapshot_2026-06-13/GasHydrateAUs.geojson`
  for USGS hydrate assessment-unit outlines.
- `data/public_stability_snapshot/north_slope_stability_snapshot_2026-06-13/ggd223_permafrost_controls.csv`
  for GGD223 `pf_depth_m` controls.
- `03_data_final/master_layers/north_slope_master_2d_layers.parquet` for the
  public-safe Geoscience Orientation master context used by the website and
  static export builder.
- `docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_11_dggs_umiat_gubik_geology_layer_slide_map.png`
  for the DGGS RI 2018-6 Umiat-Gubik geology preview/inset.
- Public field labels derived from the committed public stability-screen `field`,
  `lat`, and `lon` columns.
- `unified_north_slope_well_stability_context_map_2026_06_18.png`, the derived
  public-safe slide export.
- `unified_north_slope_slide_export_callout_space_2026_06_18.png`, the derived
  public-safe slide-callout export.

OSL/Drive-only or ignored local layers:

- Raw Alaska DNR unit-boundary package and local North Slope clip.
- Raw/derived AKDOT road GeoJSON.
- Raw/derived DNR TAPS GeoJSON.
- Census/GNIS place source packages.
- Raw DGGS RI 2018-6 shapefile/source package until a clean, simplified,
  public-safe derived geometry layer is intentionally committed. The current
  deck/website export uses only the committed source-backed preview PNG.
- Approved well-log/core/NMR rows, populated runtime configs, trained models,
  and reviewed result maps.

## Extra Local PC Map Search Finding

The 2026-06-18 PC search found these relevant map exports outside or adjacent
to the current unified output:

- `slide3_correct_2d_well_stability_map_2026_06_18.png` in this folder:
  integrated as the visual predecessor and now superseded by the unified map.
- `website_2d_well_map_stability_status_2026_06_18.png` and
  `website_2d_well_map_temperature_coverage_2026_06_18.png` in this folder:
  retained as secondary/reference diagnostics.
- `C:\Users\Writwik\Documents\north-slope-gas-hydrates-slide2-20260617\docs\evidence\slide02_source_bundle_2026_06_17\slide02_selected_08_north_slope_geoscience_orientation_map.png`:
  reference-only old geoscience orientation screenshot; superseded for main map
  styling because it is stretched/sparse.
- `C:\Users\Writwik\Documents\north-slope-gas-hydrates-slide2-20260617\docs\evidence\slide02_source_bundle_2026_06_17\slide02_selected_11_dggs_umiat_gubik_geology_layer_slide_map.png`:
  DGGS RI 2018-6 geology reference preview; kept as source/geology meaning only
  because no clean simplified DGGS geometry layer is committed here.

## Source Guardrail

These map layers are context/orientation layers. They can help the audience
locate public wells, oil/gas units, roads, communities, and the pipeline
corridor. They do not add hydrate occurrence evidence, hydrate saturation
evidence, or trained ML results.
