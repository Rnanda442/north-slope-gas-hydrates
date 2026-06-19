# Editable Deck Rebuild Source Of Truth

Date: 2026-06-19

This file records the current user direction for the next deck pass. The first
job is not another raster-panel refresh. The first job is to rebuild the best
Drive deck as real editable slide content so the user can click a box, label,
arrow, circle, or text line and move/edit only that object.

## Source Deck And Email Context

Latest user email reviewed:

- Gmail subject: `slide updates for the newest deck`
- Gmail thread: `19edc9d8ce7f95f1`
- Gmail message: `19edd022306af325`
- Sent: 2026-06-18 18:12 CDT
- Attached deck named by user as best review deck so far:
  `V5.5 Slide 3 Signal Response QC-Cleaned North Slope Gas Hydrate ML Workflow Slides 2026-06-17 (1).pptx`

Latest Drive review deck inspected:

- Title: `REVIEW - 9-slide V5.5 with local Slide 5 equation cards - 2026-06-19`
- Google Slides ID: `1ge6xYeiUTx1q1gFQcYGfMR1qv3uvOjKVG0YtipzwEsI`
- Link: <https://docs.google.com/presentation/d/1ge6xYeiUTx1q1gFQcYGfMR1qv3uvOjKVG0YtipzwEsI>
- Connector revision inspected: `cnNOmG19CdEbsQ`
- Connector finding: 9 slides, each slide contains one full-slide image object
  and no editable slide-face text/shapes. Slide descriptions are:
  `slide_01_personal_about_me_v5_5.png`,
  `slide_02_source_context_v5_5.png`,
  `slide_03_parameter_ranges_v5_5.png`,
  `slide_04_full_complex_project_workflow_v5_5.png`,
  `slide_05_equation_cards_v5_5.png`,
  `slide_06_equations_feature_unit_gate_v5_5.png`,
  `slide_07_complex_ml_runtime_architecture_v5_5.png`,
  `slide_08_stability_to_ml_overlay_v5_5.png`, and
  `slide_09_done_not_claimed_next_v5_5.png`.

The user said "best 8 from Drive," but the inspected best candidate is a
9-slide review deck. Treat the Drive deck above as the visual reference until
the user confirms whether the final deliverable should keep 9 slides or merge
the close/results material down to 8.

## Meaning Of Movable / Editable

Final slide faces should not be one screenshot of a designed slide.

Use native editable objects for:

- slide titles and subtitles;
- paragraph text and short labels;
- boxes/cards/panels;
- arrows and connectors;
- circles, emphasis rings, highlights, and callouts;
- legends and simple icons;
- source/caveat captions that remain on-slide.

Generated or source-backed figures may remain as images when they are the
actual evidence or data visualization:

- maps and GIS exports;
- P-T or stability plots;
- source figures that must preserve scientific content;
- well-log panels exported from project code or DOE runtime;
- equation renderings if native equation formatting is not reliable.

Even when a figure is an image, slide labels around it should remain editable
where practical. Do not flatten figure labels, captions, arrows, or explanatory
text into a full-slide screenshot.

## Slide Rebuild Requirements

| slide | current raster reference | required rebuild direction | figure/image pieces allowed | native editable pieces required |
|---|---|---|---|---|
| 1 | Personal/about-me opener | Delete the rap-caviar content. Remove the current personal photo and leave a clean photo slot for the user to replace manually. | Optional blank photo placeholder only. | Name/title, affiliation, subtitle, photo frame, accent shapes. |
| 2 | Source/context panel | Rebuild as a concise methane hydrate and North Slope setting slide. Use one combined 2D map, a real P-T diagram/stability curve, a corrected hydrate-structure visual, and cross-section context. | Combined map export, source hydrate-structure figure, P-T plot, cross-section image. | Title, labels integrated over figures, corrected Structure I circle, short hydrate/formation labels, source/caveat notes moved off slide unless essential. |
| 3 | Parameter/log-signal range panel | Rebuild as a visual logging/coring signal explanation. Show realistic log movement, lithology/rock-type column, clean sandstone versus shale/mixed facies, core/NMR/pressure-core calibration strip, and why `V_s` matters. | Project-generated well-log/lithology panel, source-backed subsurface/coring visual. | Curve callouts, lithology labels, `V_s` explanation, signal-direction annotations, small legend. No equations or ML architecture here. |
| 4 | Full complex project workflow | Simplify for audience. Combine redundant boxes into inputs, preparation, leakage barrier, model path, validation, and outputs. Keep full complex diagram for Word/appendix. | Optional small background/reference iconography only. | All workflow boxes, arrows, labels, and two-minute-script language should be native text/shapes. |
| 5 | Equation cards | Equation-only slide replacing the three-dataset prototype. Use large equations, stacked fractions, and words directly below every symbol. Remove the 2D map and remove crowded "why use it" prose. | Equation renderings only if needed for clean symbols/fractions. | Equation-card titles, symbol-under-word labels, color/source-role key, short phrase per equation. No ML and no well-log traces. |
| 6 | Equation/unit gate / evidence panel | Make this high-level and low text. Integrate images into the main visual instead of detached boxes. Move detailed source comments to notes/Word. | Source-backed or project-generated visuals only. | One-sentence takeaway, major labels, minimal callouts, simple frame/flow objects. |
| 7 | Complex ML runtime architecture in current deck | Replace with the new stability map as context only. It should not be an ML overlay. | New unified stability/context map export. | Title, context-only caption, legend/callouts if not already in figure, no-proof wording. |
| 8 | Stability-to-ML overlay in current deck | Convert to planned four-well results/review logic after DOE runtime: what figures/tables will be produced and how lithology/core calibration is reviewed. | Placeholder thumbnails or future DOE-export slots only. | Review steps, uncertainty/check labels, occurrence and saturation separation. No fake results. |
| 9 | Done/not-claimed/next | Close with what is built, what is not claimed, and next actions. If final deck must be 8 slides, merge this into slide 8 or a concise final close. | None required. | All text, checkmarks, dividers, and next-action boxes should be editable. |

## Email Change List To Preserve

- Slide 1: remove rap-caviar content and current personal photo.
- Slide 2: combine the 2D well maps into one readable map; add the
  CSV-derived temperature/stability curve as a real plot; use "P-T diagram,"
  not "P-T gate"; enlarge and simplify the gas hydrate explanation; fix the
  Structure I circle; explain Structure II/H, thermogenic versus biogenic gas,
  and why hydrates matter with source-backed language; use cross sections to
  explain regional stability variability; remove tiny source comments from the
  slide face.
- Slide 3: integrate explanation blocks into well-log/lithology visuals; make
  logs look more like real logs; show why `V_s` is important; explain clean
  sandstone, shale/mixed facies, coring, and hydrate-compatible signal
  movements visually.
- Slide 4: simplify the complex ML diagram into an audience-facing flow and a
  two-minute script.
- Slide 5: equation-only; large real fractions; word/phrase under every
  symbol; no 2D map; no ML; no crowded "why use it" prose.
- Slide 6: reduce word count and font crowding; integrate images into the
  visual structure.
- Slide 7: use the new stability map; do not make it an ML overlay.
- Slides 7-9: plan results/discussion without unsupported results.
- Project scope: the ML story is the four wells from the three
  datasheets/workbooks until verified otherwise; find well names, locations,
  and core/lithology/NMR/pressure-core evidence before finalizing lithology or
  saturation claims.

## Recommended Build Path

1. Preserve the Drive review deck as a visual reference. Do not overwrite it.
2. Create a new deck named `EDITABLE REBUILD - North Slope Gas Hydrate ML Workflow - 2026-06-19`.
3. Rebuild slide-by-slide using native slide objects for text/shapes and only
   source-backed/project-generated figure exports for true figures.
4. For each slide, keep a small source/notes ledger stating which source,
   website export, project figure, or email requirement supports the content.
5. Verify editability structurally: connector or PPTX inspection should show
   text boxes/shapes/lines/images as separate objects, not one full-slide image
   per slide.
6. Verify visually with thumbnails/renders. The visual style may follow the
   V5.5 reference deck, but the object model must be editable.

## Immediate Next Step

Build an editable skeleton first, before perfecting content. The skeleton
should have the correct slide titles, native text boxes, native image frames,
native callout placeholders, and blank figure slots where the right map/plot or
DOE export is still missing. Once the skeleton is movable, fix content and
visual quality slide by slide.

## Final Rebuild Status

Updated: 2026-06-19

Local editable rebuild output:

- `docs/project_blueprints/EDITABLE_REBUILD_North_Slope_Gas_Hydrate_ML_Workflow_2026-06-19.pptx`
- Builder: `docs/project_blueprints/build_editable_rebuild_deck_2026_06_19.ps1`
- P-T/contact-sheet helper: `docs/project_blueprints/render_editable_rebuild_assets_2026_06_19.py`
- Rendered slides and contact sheet:
  `docs/project_blueprints/presentation_assets/editable_rebuild_2026_06_19/`
- Shape audit:
  `docs/project_blueprints/presentation_assets/editable_rebuild_2026_06_19/editable_rebuild_shape_audit_2026_06_19.csv`

Native Google Slides import:

- Title: `EDITABLE REBUILD - North Slope Gas Hydrate ML Workflow - 2026-06-19`
- Link: <https://docs.google.com/presentation/d/1ts1mI95SqQibox5xgkNbH6RdnJ3d5lwosdojr26a4IA>
- Google Slides ID: `1ts1mI95SqQibox5xgkNbH6RdnJ3d5lwosdojr26a4IA`
- Connector metadata verified MIME type:
  `application/vnd.google-apps.presentation`
- Drive-import thumbnails:
  `docs/project_blueprints/presentation_assets/editable_rebuild_2026_06_19/drive_import_thumbnails/`
- Drive-import contact sheet:
  `docs/project_blueprints/presentation_assets/editable_rebuild_2026_06_19/drive_import_contact_sheet_2026_06_19.png`

Build method note: the final deck was built through PowerPoint COM automation
so slide text, boxes, arrows, callouts, circles, dividers, and status cards are
native PowerPoint objects. The prior `python-pptx` full-slide raster assembly
path was not used for the final PPTX. Scientific figures/maps/plots remain
inserted image objects where appropriate.

## Image / Source Recovery Status

| slide | final figure/source status | editable object status | placeholder / caveat |
|---|---|---|---|
| 1 | No photo source used; user-requested photo placeholder left blank. | Title, subtitle, status cards, chips, and photo frame are native editable objects. | User should replace the blank photo slot manually. |
| 2 | Hydrate structure image recovered from `docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_14_world_atlas_fig1_1_structure_types_clean.png`; cross-section from `slide02_selected_06_usgs_arctic_alaska_cross_section_fig2_crop.png`; unified map from `docs/project_blueprints/presentation_assets/website_well_maps_2026_06_18/unified_north_slope_well_stability_context_map_2026_06_18.png`; P-T diagram rendered from `data/public_stability_products/phase_curve_methane_5ppt_screenshot_recovered_2026-06-18.csv`. | Title, labels, Structure I circle, callouts, and caveats are native editable objects. | P-T diagram is source/data-derived from the recovered CSV; detailed citations remain for Word/end material. |
| 3 | Final visual is a native editable schematic log/lithology/core panel, not approved DOE rows. | Log curves, lithology blocks, core strip, callouts, arrows, and labels are native editable objects. | Replace with DOE runtime export later if approved row-level curves are cleared. |
| 4 | Complex full workflow retained as source/Word reference; audience slide rebuilt as simplified native workflow. | All boxes, arrows, labels, and summary cards are native editable objects. | Two-minute script is in slide notes. |
| 5 | Equation content derived from public-safe stability/equation/source notes; no map or ML visual used. | Equation cards, fraction line, symbol labels, role chips, and caveat are native editable objects. | Saturation/electrical equation excluded until exact source equation and input/target role are approved. |
| 6 | High-level unit/evidence gate rebuilt from public-safe header-role logic. | Gate cards, arrows, takeaway, and summary cards are native editable objects. | Detailed header tables/screenshots stay in companion/source docs. |
| 7 | Unified context map from `unified_north_slope_slide_export_callout_space_2026_06_18.png`. | Title, context cards, and no-proof caveat are native editable objects around the map image. | Map is context only; not an ML overlay or occurrence/saturation evidence. |
| 8 | Public four-well/source-case names from header/source handoffs and public well/API index. | Four case cards, review-flow boxes, arrows, and future-output note are native editable objects. | Hydrate-01 and HYDRATE 02 remain source-case anchors until header evidence confirms active workbook membership. |
| 9 | No source figure needed. | Built/not-claimed/next columns, final message, and footer are native editable objects. | No final claims; next actions depend on DOE/Yubi access and mentor review. |

## QA Results

- Rendered every slide through PowerPoint export.
- Created contact sheet:
  `docs/project_blueprints/presentation_assets/editable_rebuild_2026_06_19/editable_rebuild_contact_sheet_2026_06_19.png`
- Imported the PPTX as a new native Google Slides deck without overwriting the
  prior Drive review deck.
- Connector readback verified the imported deck title, native Slides MIME type,
  and 9-slide structure.
- Fetched and saved large Drive-rendered thumbnails for slides 1-9, then built
  `drive_import_contact_sheet_2026_06_19.png` for conversion QA.
- Shape audit confirms all nine slides have native editable text/shapes and
  `only_full_slide_image = False`.
- Slide 2 P-T diagram uses the recovered CSV path requested for the rebuild.
- No slide claims hydrate proof, final stability, trained metrics,
  occurrence/saturation predictions, or sweet-spot ranking.
