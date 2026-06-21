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

## Source Image Recovery Gate

The editable rebuild is not a trace-over exercise. Before a slide is rebuilt
with final visuals, recover the original or closest verified source-backed image
for every scientific figure, map, plot, equation, and source visual. Do not use
low-resolution screenshots when a source figure, data file, or project export
can be recovered. Do not use generic AI images for scientific visuals. Do not
use whole-slide screenshots as final slide faces.

Search in this order:

1. Repo source folders and evidence folders.
2. `docs/source_library_index/`.
3. Google Drive source folders.
4. Gmail attachments from June 17-19, 2026.
5. Project website exports.
6. Already identified source PDFs and papers.
7. Official/public online source pages only when the image is not already in
   project sources.

For each source image or figure, record:

- original source or closest verified source;
- local clean high-resolution copy/export when allowed;
- source path, Drive URL, Gmail attachment, paper, or OSL source location;
- allowed use as `GitHub`, `Drive only`, or `OSL only`;
- whether the rebuild should use the source image itself, a CSV-derived
  recreated plot, native editable shapes, or a documented placeholder.

Use these boundaries:

- `GitHub`: public-domain, official public, project-generated public-safe, or
  already tracked public-safe derived assets.
- `Drive only`: user-uploaded or publisher-source PDFs/figures where citation
  is acceptable for review but public GitHub redistribution is not confirmed.
- `OSL only`: raw heavy source bundles, approved/runtime data, restricted
  identifiers, or source packages intentionally excluded from Git.

## Image / Source Recovery Table

This is the starting recovery ledger for the editable rebuild. Update it before
finalizing any slide visual.

| slide | needed image/figure | found? | source/location | resolution/quality | allowed use | rebuild role | still needed |
|---|---|---|---|---|---|---|---|
| 1 | Personal photo | placeholder by design | Current photo should be removed; use a native empty photo frame only. | N/A | GitHub | Editable placeholder frame | User can manually add a final photo later. |
| 2 | Hydrate structure/source image | yes | `docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_14_world_atlas_fig1_1_structure_types_clean.png` and `slide02_selected_09_world_atlas_fig1_1_full_structure_types_si_highlighted.png`; provenance recorded in source visual inventory as World Atlas Fig. 1.1 structure types. | 1312 x 1042; clean crop, good for slide use. | GitHub, citation/license recheck before final public release | Source-backed figure object with editable Structure I callout/ring and labels around it. | Confirm final citation/rights wording; do not replace with AI hydrate cage art. |
| 2 | North Slope geology/context map | yes | DGGS RI 2018-6 Umiat-Gubik derived previews: `slide02_selected_10_dggs_umiat_gubik_geology_layer_preview.png`, `slide02_selected_11_dggs_umiat_gubik_geology_layer_slide_map.png`; source package documented in `docs/OSL_GIS_LAYER_CANDIDATES_FOR_SLIDE2_2026-06-18.md`. | 1280 x 555 preview; 1100 x 475 slide map; acceptable as compact context, not full-screen. | GitHub for derived preview; OSL only for raw GIS package | Source-backed map figure with editable slide labels/caption. | If used large, export a higher-resolution static map from the DGGS source package. |
| 2 | North Slope cross-section figure | yes | `docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_06_usgs_arctic_alaska_cross_section_fig2_crop.png`. | 1093 x 605; usable small/medium. | GitHub | Source-backed cross-section object with editable explanatory labels. | Record exact USGS figure citation in final source notes. |
| 2 | P-T/stability curve or CSV-derived plot | yes | Canonical slide-rebuild CSV: `data/public_stability_products/phase_curve_methane_5ppt_screenshot_recovered_2026-06-18.csv`; source CSVs: `data/public_stability_products/phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1.csv` and `docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_03_project_digitized_methane_5ppt_curve.csv`; low-res crop: `slide02_selected_02_usgs_hydrate_stability_curve_crop.png`. | 41 rows; full methane 5 ppt depth-pressure-temperature lookup with June 18 email/source-bundle provenance. Crop is only 276 x 436 and should not be final. | GitHub | Recreate as a clean high-resolution editable/native or image plot from CSV. | Generate/export final high-res P-T diagram from the recovered CSV; use crop only as source reference. |
| 2 | Combined 2D North Slope well/stability map | yes | `docs/project_blueprints/presentation_assets/website_well_maps_2026_06_18/slide3_correct_2d_well_stability_map_2026_06_18.png`; map source notes in same folder. | 3600 x 2240; high-quality slide-ready export. | GitHub for derived map; OSL only for raw basemap packages | Map figure object with editable labels/callouts outside the map. | Add final caption that it is stability/context only, not hydrate proof. |
| 3 | Realistic well-log/source-signal figure | partial | Public-domain USGS log images in `references/presentation-revision-2026-06-11/images/` plus project `synthetic_well_log_panel.png`; ML/log source PDFs include Chong et al. 2022 local PDF. | USGS images range 605 x 456 to 1097 x 1806; synthetic panel is reference only. | GitHub for USGS/project-generated assets; Drive only for paper figures | Use project-generated/source-backed log panel as image; keep callouts, arrows, and labels editable. | Recover or generate a clean depth-aligned log/lithology panel; do not reuse old slide raster panel as final. |
| 3 | Lithology, core, NMR, and pressure-core visuals | partial | Drive search found `yoneda_etal_2026_ans_hydrate02_nmr_permeability_energyfuels.pdf` and `acs.energyfuels.5c05321.pdf`; source manifest lists Aung et al. 2026 and missing Phillips/Haines 2026 pressure-core/lithology papers. | Source PDFs available in Drive; exact figures not extracted or cleared for GitHub. | Drive only; OSL only for any approved/runtime/core-source exports | Use documented placeholders until exact figures are recovered; final labels/callouts editable. | Find/export allowed clean figures or make explicit placeholders saying which NMR/core/pressure-core visual is missing. |
| 4 | Full workflow/architecture visual | reference found | V5.2/V5.5 workflow plates in `docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_15/` and V5.5 slide 4 panel. | Reference panels are 1600 x 900 or larger, but slide should not remain a raster plate. | GitHub | Rebuild as native editable boxes, arrows, dividers, and text. | Use old plate only as visual reference or appendix source, not as the final slide face. |
| 5 | Equation screenshots/source equations | partial | Equation source docs and attachments: `docs/project_blueprints/North_Slope_Gas_Hydrate_Equation_Focused_Research_Overview_Paper_Sources_Only_2026-06-17.docx`, source-index equation docs, and June 18 Gmail attachment with the same equation-focused doc. | Text/equation sources exist; clean equation renderings not yet exported. | GitHub for project equation docs; Drive only for any publisher-paper equation figures | Prefer native editable equation text/labels; render equations as high-quality image objects only if native formatting is unreliable. | Lock final equation list, units, and symbol-under-word labels; export clean equations if needed. |
| 6 | Evidence/unit-gate visuals | partial | V5.5 slide 6 panel and public USGS log images are local references; source docs support equations and feature roles. | Existing panel is 1600 x 900 reference only. | GitHub for project-generated/public images | Rebuild as native high-level evidence board; use only source-backed small figures if needed. | Identify exact visuals to keep versus native rebuild; remove detailed source comments from slide face. |
| 7 | Stability map / unified well map | yes | `docs/project_blueprints/presentation_assets/website_well_maps_2026_06_18/slide3_correct_2d_well_stability_map_2026_06_18.png`; supporting status and temperature maps in same folder. | 3600 x 2240 primary map; 792 px website screenshots are fallback/status only. | GitHub for derived map; OSL only for raw basemap/source layers | Context-only figure object with editable title, caption, legend/callouts as needed. | Do not make this an ML overlay or proof map; add source/caveat caption. |
| 8 | Planned four-well results/review thumbnails | placeholder needed | No approved DOE result figures are public. Future outputs belong in ignored runtime/OSL until reviewed. | N/A until DOE runtime exports exist. | GitHub for empty placeholders only; OSL only for real runtime outputs until public-safe review | Native editable review slots and labels; optional blank thumbnail placeholders. | After DOE run, export row-free public-safe summaries only if approved. |
| 9 | Done/not-claimed/next visuals | no figure needed | Native editable status boxes only. | N/A | GitHub | Native text, checkmarks, dividers, and next-action boxes. | None unless a source/status icon is deliberately added and cited. |

External checks completed for this table on 2026-06-19:

- Google Drive search found the HYDRATE 02 NMR/permeability PDFs, Aung et al.
  2026 LWD PDFs, the V5.5 Slide 3 Signal Response decks/companions, and
  comparative ML source PDFs.
- Gmail search for June 17-19, 2026 attachments found the latest `slide updates
  for the newest deck` message, the V5.5 Slide 3 QC-cleaned PPTX attachment,
  DOE import Slide 2/Slide 3 PPTX attachments, the equation-focused DOCX, and
  the `source_screenshot_share_2026_06_18.zip` source bundle.

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
