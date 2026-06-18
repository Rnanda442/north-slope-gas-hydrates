# Website 2D Well Map Captures And Basemap Upgrade Notes

Date: 2026-06-18

## Captured Website Images

These images are 2026-06-18 website captures from
`Explore North Slope > 3D Structure`. The original `website_2d_...` captures
document the pre-landmark-overlay public-safe website state. The
`slide3_correct_...` export is the corrected slide-ready map generated after
the landmark overlay pass.

| Image | Current use | Visual QA |
| --- | --- | --- |
| `slide3_correct_2d_well_stability_map_2026_06_18.png` | Correct slide-3/website-map export for the updated 2D well/stability context | Uses the updated map layers: Alaska DNR oil/gas unit outlines, AKDOT roads with Dalton/Deadhorse roads highlighted, Trans-Alaska Pipeline geometry, Census/GNIS community label context, public well field labels, and a caveat that these overlays are context rather than hydrate evidence. |
| `website_2d_well_map_stability_status_2026_06_18.png` | Guarded methane 5 ppt stability-screen status map | Shows well distribution and screen categories, but the base layer does not make Prudhoe Bay, Kuparuk River, Milne Point, Deadhorse, or the Dalton/TAPS corridor obvious enough for a mentor audience. Use as a placeholder only until landmark overlays are added. |
| `website_2d_well_map_temperature_coverage_2026_06_18.png` | Temperature-profile/proxy coverage diagnostic map | Good for explaining source coverage and blank-row reasons. It should not be used as the main hydrate science map because it is a data-readiness view, not an occurrence/saturation view. |
| `website_2d_well_maps_contact_sheet_2026_06_18.png` | QA contact sheet | Confirms both captures, including the current weak landmark context. |

## Recommended Slide Placement

1. **Slide 3 / 2D well-stability context**: use
   `slide3_correct_2d_well_stability_map_2026_06_18.png`. It supports "where
   the public scaffold is," "what the current stability screen covers," and
   "which public context layers orient the wells," not a hydrate-proof claim.
2. **What we have done / status slide**: use the stability-status map here if
   Slide 2 is already carrying the hydrate definition and source-backed phase
   curve. Caption it as a guarded public stability-admissibility screen.
3. **Later methods/status slide or appendix**: use the temperature-coverage map
   to explain why some wells are direct G10015 temperature matches, proxy
   candidates, or still blank. This map is best for data-readiness discussion.
4. **Slide 3 signal-response rebuild**: do not make either 2D map the main
   visual. Slide 3 should stay focused on depth-aligned log signal movement.
   A small orientation inset is acceptable only if it helps explain stability
   context.

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

## Source Guardrail

These map layers are context/orientation layers. They can help the audience
locate public wells, oil/gas units, roads, communities, and the pipeline
corridor. They do not add hydrate occurrence evidence, hydrate saturation
evidence, or trained ML results.
