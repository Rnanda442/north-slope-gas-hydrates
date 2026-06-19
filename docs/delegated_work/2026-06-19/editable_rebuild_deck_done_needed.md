# Editable Rebuild Deck Done / Needed Handoff

## Prompts Worked On

- Editable 9-slide North Slope Gas Hydrate ML Workflow deck rebuild.
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

## Still Needed

- User should replace the Slide 1 blank photo placeholder manually.
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
- `data/public_stability_products/phase_curve_methane_5ppt_screenshot_recovered_2026-06-18.csv`
- `data/public_ml_products/four_well_case_location_index_2026-06-19.csv`
- `docs/source_library_index/FOUR_WELL_CASE_LOCATION_INDEX_2026-06-19.md`
- `docs/evidence/email_screenshots_2026_06_19/README.md`
- `docs/project_blueprints/EDITABLE_DECK_REBUILD_SOURCE_OF_TRUTH_2026-06-19.md`

## Branch / Commit

- Branch: `codex/editable-rebuild-deck-output-20260619`
- Commit: created in this run; use `git log -1 --oneline` or the final
  handoff response for the exact hash.

## Slides Affected

- Slides 1-9.

## Main Codex Next Steps

1. Review the contact sheet, PPTX, and imported Google Slides deck manually.
2. Keep the previous Drive review deck untouched.
3. Use the shape audit as the structural QA baseline for future revisions.
4. Replace placeholders only with source-backed visuals or approved-runtime row-free exports.
