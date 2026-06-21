# Editable Rebuild Deck Done / Needed Handoff

## Prompts Worked On

- Editable 9-slide North Slope Gas Hydrate ML Workflow deck rebuild.
- Corrected visual-match rebuild after user feedback that the first editable
  deck did not look enough like the prior V5.5 review deck.
- Slide 2 P-T diagram regeneration from recovered CSV.
- Public four-well/source-case well/API source carry-forward for deck context.
- Editability and no-full-slide-raster QA.

## Done

- Created a new editable 9-slide PowerPoint:
  `docs/project_blueprints/EDITABLE_REBUILD_North_Slope_Gas_Hydrate_ML_Workflow_2026-06-19.pptx`
- Built the deck with PowerPoint COM automation, not the existing `python-pptx`
  full-slide raster assembly path.
- Kept titles, text boxes, labels, cards, arrows, circles, legends, dividers,
  and status cards as native editable PowerPoint objects.
- Used scientific figures/maps/plots only as inserted image objects:
  hydrate structure, North Slope cross-section, unified North Slope map, and
  CSV-derived P-T diagram.
- Rendered every slide to PNG and created a contact sheet:
  `docs/project_blueprints/presentation_assets/editable_rebuild_2026_06_19/editable_rebuild_contact_sheet_2026_06_19.png`
- Created a shape audit:
  `docs/project_blueprints/presentation_assets/editable_rebuild_2026_06_19/editable_rebuild_shape_audit_2026_06_19.csv`
- Confirmed every slide has native editable text/shapes and no slide is only
  one full-slide image.
- Created the requested recovered P-T CSV path:
  `data/public_stability_products/phase_curve_methane_5ppt_screenshot_recovered_2026-06-18.csv`
  as a public-safe copy of the recovered Slide 2 evidence CSV.
- Rendered a clean high-resolution P-T diagram from that CSV:
  `docs/project_blueprints/presentation_assets/editable_rebuild_2026_06_19/slide_02_pt_diagram_from_recovered_csv_2026_06_19.png`
- Pulled in public-safe unified map exports and public case-well/API source
  notes from the latest source-hunt branch.
- Imported the PPTX as a new native Google Slides deck without overwriting the
  prior review deck:
  <https://docs.google.com/presentation/d/1ts1mI95SqQibox5xgkNbH6RdnJ3d5lwosdojr26a4IA>
- Verified the imported deck through connector metadata/readback: native Slides
  MIME type, 9-slide structure, and large thumbnails for slides 1-9.
- Saved Drive-import thumbnail QA assets:
  `docs/project_blueprints/presentation_assets/editable_rebuild_2026_06_19/drive_import_thumbnails/`
  and `docs/project_blueprints/presentation_assets/editable_rebuild_2026_06_19/drive_import_contact_sheet_2026_06_19.png`.
- Updated:
  `docs/project_blueprints/EDITABLE_DECK_REBUILD_SOURCE_OF_TRUTH_2026-06-19.md`
  with final image/source recovery status and QA results.
- Created the corrected active visual-match editable PowerPoint:
  `docs/project_blueprints/EDITABLE_VISUAL_MATCH_North_Slope_Gas_Hydrate_ML_Workflow_2026-06-19.pptx`
- Preserved the exact prior V5.5 Drive review deck look by recovering the
  Drive review slide panels into:
  `docs/project_blueprints/presentation_assets/editable_visual_match_2026_06_19/reference_drive_panels/`
- Cropped reusable figure/photo regions from those panels into:
  `docs/project_blueprints/presentation_assets/editable_visual_match_2026_06_19/cropped_reference_assets/`
- Rebuilt Slide 5's prior equation-card panel as native editable PowerPoint
  cards/text/shapes instead of keeping it as one image.
- Cleanup pass after user review rebuilt Slide 4 as a native editable
  audience workflow instead of a locked image plate.
- Cleanup pass rebuilt Slide 7 as the unified North Slope well + stability
  context map, with the map as one image object and the title, callouts, status
  legend, caveat, and source note editable.
- Slide 2's first hydrate-structure image area is now a native editable
  schematic, removing the messy circle-line source image issue.
- Slide 5 was cleaned up with larger symbol-word labels and no visible
  underscored symbol labels; the pressure, velocity-ratio, and Archie-style
  divisions use visible fraction bars.
- Rendered the visual-match deck, generated local and reference contact sheets,
  and created:
  `docs/project_blueprints/presentation_assets/editable_visual_match_2026_06_19/editable_visual_match_shape_audit_2026_06_19.csv`
- Imported the cleanup v2 visual-match PPTX as a new native Google Slides deck:
  <https://docs.google.com/presentation/d/14l8zzQ8mbxf-adWIMphd1jorepqY3hqKdbGnn-vgb3I>
- Verified that cleanup v2 Drive import by connector readback and fresh
  1600x900 thumbnails for Slides 2, 4, 5, and 7.
- Saved Drive-import visual-match thumbnails and contact sheet under:
  `docs/project_blueprints/presentation_assets/editable_visual_match_2026_06_19/drive_import_thumbnails/`
  and
  `docs/project_blueprints/presentation_assets/editable_visual_match_2026_06_19/drive_import_contact_sheet_2026_06_19.png`.
- Saved cleanup v2 Drive-import thumbnails under:
  `docs/project_blueprints/presentation_assets/editable_visual_match_2026_06_19/drive_import_thumbnails_cleanup_v2/`.

## Still Needed

- Use the visual-match deck as the active review deck. The earlier simplified
  editable rebuild is superseded for slide review, though it remains a useful
  object-editability prototype.
- If the user decides to return to the earlier cleanup rule, Slide 1 can be
  revised again to remove the personal/RapCaviar/photo imagery. For this
  visual-match correction, that content was preserved because the newest user
  instruction was to match the previous deck.
- Hydrate-01 and HYDRATE 02 should remain source-case anchors until header-only
  evidence confirms active workbook membership.
- DOE/Yubi access is still needed for any approved-runtime row-level plots,
  real per-well log panels, final calibration tables, model metrics, occurrence
  outputs, or saturation outputs.
- Public source papers/supplements should be downloaded to Drive/OSL only when
  access/licensing allows; raw tables/PDF bundles should not be committed.

## Files / Assets

- `docs/project_blueprints/EDITABLE_REBUILD_North_Slope_Gas_Hydrate_ML_Workflow_2026-06-19.pptx`
- `docs/project_blueprints/build_editable_rebuild_deck_2026_06_19.ps1`
- `docs/project_blueprints/render_editable_rebuild_assets_2026_06_19.py`
- `docs/project_blueprints/presentation_assets/editable_rebuild_2026_06_19/`
- <https://docs.google.com/presentation/d/1ts1mI95SqQibox5xgkNbH6RdnJ3d5lwosdojr26a4IA>
- `docs/project_blueprints/EDITABLE_VISUAL_MATCH_North_Slope_Gas_Hydrate_ML_Workflow_2026-06-19.pptx`
- `docs/project_blueprints/build_editable_visual_match_deck_2026_06_19.ps1`
- `docs/project_blueprints/render_editable_visual_match_assets_2026_06_19.py`
- `docs/project_blueprints/presentation_assets/editable_visual_match_2026_06_19/`
- <https://docs.google.com/presentation/d/14l8zzQ8mbxf-adWIMphd1jorepqY3hqKdbGnn-vgb3I>
- `data/public_stability_products/phase_curve_methane_5ppt_screenshot_recovered_2026-06-18.csv`
- `data/public_ml_products/four_well_case_location_index_2026-06-19.csv`
- `docs/source_library_index/FOUR_WELL_CASE_LOCATION_INDEX_2026-06-19.md`
- `docs/evidence/email_screenshots_2026_06_19/README.md`
- `docs/project_blueprints/EDITABLE_DECK_REBUILD_SOURCE_OF_TRUTH_2026-06-19.md`

## Branch / Commit

- Branch: `codex/editable-rebuild-deck-output-20260619`
- Commit: cleanup v2 correction commit pending at time of this handoff edit;
  use `git log -1 --oneline` or the final handoff response for the exact hash.

## Slides Affected

- Slides 1-9.

## Main Codex Next Steps

1. Review the contact sheet, PPTX, and imported Google Slides deck manually.
2. Keep the previous Drive review deck untouched.
3. Treat the visual-match deck as the corrected active rebuild and the
   simplified editable deck as superseded/reference.
4. Use the visual-match shape audit as the structural QA baseline for future
   revisions.
5. Replace placeholders only with source-backed visuals or approved-runtime
   row-free exports.
