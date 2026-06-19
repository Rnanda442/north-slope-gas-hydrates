# main_codex_prompt2_editable_deck Done / Needed Handoff

## Prompts Worked On

- Prompt 2: Native editable deck rebuild plan.

## Done

- Read the required project orientation docs:
  - `docs/AGENT_START_HERE.md`
  - `docs/CURRENT_ARTIFACT_INDEX.md`
  - `docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md`
- Read the current deck builder:
  - `docs/project_blueprints/build_full_workflow_diagram_deliverables.py`
- Read the available Presentations skill guidance and noted that final editable
  PPTX work should use native editable objects rather than full-slide bitmaps.
- Audited the active V5.5 deck:
  - `docs/project_blueprints/V5_5_SLIDE2_SOURCE_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Slides_2026-06-17.pptx`
- Confirmed all 9 slides currently contain one picture shape and zero editable
  text shapes.
- Identified the core technical issue in the builder: it generates PNG panels
  and assembles the deck by inserting each PNG as a full-slide image.
- Identified the builder functions involved:
  - `v55_build_panels()`
  - `rebuild_deck()`
  - `verify_deck()`
- Created a technical conversion plan:
  - Keep generated PNG/SVG figures for maps, P-T plots, source crops, well-log
    panels, equation renderings, and complex reference diagrams.
  - Rebuild titles, subtitles, labels, arrows, callouts, circles, legends,
    workflow boxes, captions, and status cards as native editable slide objects.
  - Use a hybrid path: figure-generation code for visuals, but a native editable
    presentation builder for the final deck.
  - Use artifact-tool for the final PPTX rebuild path rather than continuing
    the current python-pptx full-slide-raster assembly pattern.
- Specified a slide-by-slide editability plan for Slides 1-9.
- Specified editability QA:
  - programmatic shape audit;
  - manual click/edit test;
  - rendered-slide/contact-sheet QA;
  - source/claim QA;
  - visual-style comparison against the current V5.5 contact sheet.
- Captured the 2026-06-19 source-image recovery addition in:
  - `docs/project_blueprints/EDITABLE_DECK_REBUILD_SOURCE_OF_TRUTH_2026-06-19.md`
- Ran a local source/evidence/source-index pass plus bounded Drive/Gmail checks
  for the current image-source gaps:
  - Drive searches found HYDRATE 02 NMR/permeability PDFs, Aung et al. 2026
    LWD PDFs, V5.5 Slide 3 Signal Response decks/companions, and comparative
    ML source PDFs.
  - Gmail June 17-19 attachment search found the latest `slide updates for the
    newest deck` message, the V5.5 Slide 3 QC-cleaned PPTX attachment, DOE
    import Slide 2/Slide 3 PPTX attachments, the equation-focused DOCX, and
    the `source_screenshot_share_2026_06_18.zip` source bundle.

## Image / Source Recovery Table

Do not finalize a slide visual until the relevant row below is resolved as
`found` or a deliberate placeholder is documented. Source figures may remain
high-quality image objects, but surrounding labels, captions, arrows, and
callouts should be native editable objects.

| slide | needed image/figure | found? | source/location | resolution/quality | allowed use | rebuild role | still needed |
|---|---|---|---|---|---|---|---|
| 1 | Personal photo | placeholder by design | Remove current personal photo; use native empty photo frame. | N/A | GitHub | Editable placeholder frame | User can manually add final photo. |
| 2 | Hydrate structure/source image | yes | `docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_14_world_atlas_fig1_1_structure_types_clean.png`; alternate `slide02_selected_09_world_atlas_fig1_1_full_structure_types_si_highlighted.png`. | 1312 x 1042; clean crop. | GitHub, citation/license recheck | Source-backed figure object with editable Structure I callout/ring. | Confirm final citation/rights wording; no AI hydrate cage art. |
| 2 | North Slope geology/context map | yes | DGGS RI 2018-6 derived previews in `docs/evidence/slide02_source_bundle_2026_06_17/`; source documented in `docs/OSL_GIS_LAYER_CANDIDATES_FOR_SLIDE2_2026-06-18.md`. | 1280 x 555 preview; 1100 x 475 slide map. | GitHub for derived preview; OSL only for raw GIS | Source-backed map with editable labels/caption. | If used large, export higher-res static map from source package. |
| 2 | North Slope cross-section figure | yes | `docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_06_usgs_arctic_alaska_cross_section_fig2_crop.png`. | 1093 x 605; usable small/medium. | GitHub | Source-backed cross-section image with editable labels. | Record exact USGS figure citation in source notes. |
| 2 | P-T/stability curve or CSV-derived plot | yes | Canonical slide-rebuild CSV: `data/public_stability_products/phase_curve_methane_5ppt_screenshot_recovered_2026-06-18.csv`; source CSVs: `data/public_stability_products/phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1.csv` and `docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_03_project_digitized_methane_5ppt_curve.csv`; low-res crop exists. | 41 rows; full methane 5 ppt depth-pressure-temperature lookup with June 18 email/source-bundle provenance. Crop is only 276 x 436. | GitHub | Recreate clean high-resolution P-T plot from recovered CSV. | Generate/export final plot; do not use low-res crop except as source reference. |
| 2 | Combined 2D well/stability map | yes | `docs/project_blueprints/presentation_assets/website_well_maps_2026_06_18/slide3_correct_2d_well_stability_map_2026_06_18.png`. | 3600 x 2240; high-quality. | GitHub for derived map; OSL only for raw basemap packages | Figure object with editable labels/callouts outside map. | Caption as stability/context only, not hydrate proof. |
| 3 | Realistic well-log/source-signal figure | partial | USGS public-domain log images in `references/presentation-revision-2026-06-11/images/`; project `synthetic_well_log_panel.png`; Chong et al. 2022 PDF supports method. | USGS images 605 x 456 to 1097 x 1806; synthetic panel reference only. | GitHub for USGS/project visuals; Drive only for paper figures | Project-generated/source-backed log panel image plus editable callouts. | Recover or generate clean depth-aligned log/lithology panel. |
| 3 | Lithology/core/NMR/pressure-core visuals | partial | Drive search found Yoneda et al. 2026 NMR/permeability PDFs; manifest lists Aung et al. 2026 and missing Phillips/Haines 2026 pressure-core/lithology papers. | Source PDFs available; exact figures not extracted or GitHub-cleared. | Drive only; OSL only for approved/runtime/core exports | Use documented placeholders until exact figures are recovered. | Export allowed clean figures or state exactly which visual is missing. |
| 4 | Full workflow/architecture visual | reference found | V5.2/V5.5 workflow plates in `docs/project_blueprints/presentation_assets/`. | Reference panels are slide-sized, but not final editable content. | GitHub | Rebuild as native boxes, arrows, dividers, and text. | Use old plate only as visual reference or appendix source. |
| 5 | Equation screenshots/source equations | partial | `docs/project_blueprints/North_Slope_Gas_Hydrate_Equation_Focused_Research_Overview_Paper_Sources_Only_2026-06-17.docx`, source-index equation docs, June 18 Gmail equation-focused DOCX. | Text/equation sources exist; clean equation renderings not exported. | GitHub for project equation docs; Drive only for publisher figures | Prefer native editable equations/labels; image render only if needed. | Lock final equation list, units, and symbol-under-word labels. |
| 6 | Evidence/unit-gate visuals | partial | V5.5 slide 6 reference panel and public USGS log images. | Existing panel is 1600 x 900 reference only. | GitHub for project/public images | Native high-level evidence board with source-backed small figures only if needed. | Decide exact visuals to keep; move detailed comments to notes/Word. |
| 7 | Stability map / unified well map | yes | `docs/project_blueprints/presentation_assets/website_well_maps_2026_06_18/slide3_correct_2d_well_stability_map_2026_06_18.png`; status/temperature maps in same folder. | 3600 x 2240 primary map; 792 px screenshots fallback only. | GitHub for derived map; OSL only for raw source layers | Context-only figure object with editable caption/legend/callouts. | Do not make it an ML overlay or proof map. |
| 8 | Planned four-well results/review thumbnails | placeholder needed | No approved DOE result figures are public; future exports belong in ignored runtime/OSL until reviewed. | N/A | GitHub for empty placeholders only; OSL only for real runtime outputs until review | Native editable review slots and blank thumbnails. | After DOE run, export row-free public-safe summaries only if approved. |
| 9 | Done/not-claimed/next visuals | no figure needed | Native editable status boxes only. | N/A | GitHub | Native text, checkmarks, dividers, and next-action boxes. | None unless a cited icon/source visual is deliberately added. |

## Still Needed

- Do not rebuild the deck yet until the user explicitly asks for implementation.
- Treat source-image recovery as a required gate before final slide visuals:
  search repo/evidence, `docs/source_library_index/`, Drive source folders,
  Gmail June 17-19 attachments, website exports, identified PDFs/papers, then
  official/public online pages only when needed.
- Save clean high-resolution source copies/exports only when allowed; otherwise
  use Drive-only or OSL-only references and document placeholders.
- Do not use low-resolution screenshots, generic AI images, or whole-slide
  screenshots for scientific figures.
- Decide whether the editable rebuild should:
  - create a new artifact-tool builder from scratch, or
  - wrap/reuse existing figure-generation functions and replace only the deck
    assembly layer.
- Inspect the latest Gmail/Drive deck attachment before selecting the final
  source deck if that attachment is still considered the best reviewed deck.
- Create the actual native editable deck with real text boxes, shapes, arrows,
  callouts, and figure placements.
- Update QA so future builds fail if a slide is accidentally reduced to one
  full-slide image.
- Decide which complex visuals stay as high-resolution figure objects and which
  should become simplified native diagrams.
- Keep the original best deck untouched and write the editable rebuild to a new
  output path/branch.

## Files / Assets

Created by this handoff:

- `docs/delegated_work/2026-06-19/main_codex_prompt2_editable_deck_done_needed.md`

Files inspected:

- `docs/project_blueprints/build_full_workflow_diagram_deliverables.py`
- `docs/project_blueprints/V5_5_SLIDE2_SOURCE_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Slides_2026-06-17.pptx`
- `docs/project_blueprints/presentation_assets/v5_5_slide2_source_update_2026_06_17/`

No deck, builder, image, or source asset was intentionally edited for this
Prompt 2 planning task.

Existing local modified files were observed in the worktree, including deck
binaries, builder code, generated PNG panels, source visual inventory, and
tests. Those changes were not created by this handoff and should be reviewed
separately before being committed.

## Branch / Commit

- Branch: `codex/delegated-main_codex_thread-20260618`
- Commit containing this handoff: see final response from this chat after push.

## Slides Affected

- Slides 1-9.
- The main finding applies to the whole deck: every current slide is a
  full-slide raster image and needs native editable text/shapes for final
  manual editing.

Slide-specific notes:

- Slide 1: title/name/photo placement should become editable.
- Slide 2: map, P-T diagram, hydrate structure, and cross-section can stay as
  figure assets; labels/callouts/captions should be editable.
- Slide 3: well-log/lithology/core panel can be generated; callouts and labels
  should be editable.
- Slide 4: simplified ML architecture should be built mostly as native shapes.
- Slide 5: equations may be rendered figures, but symbol labels/card text
  should be editable.
- Slide 6: evidence-review board should be native shapes/text.
- Slide 7: stability map can be a figure; labels/caption should be editable.
- Slide 8: planned result-review structure should be native editable boxes.
- Slide 9: built/not-claimed/next close should be native editable boxes.

## Main Codex Next Steps

1. Use this plan when implementing the editable deck rebuild.
2. Preserve the current V5.5 deck as a reference and output the editable rebuild
   to a new file.
3. Reuse existing generated PNG/SVG assets only as figure layers, not as full
   slide backgrounds.
4. Build native slide objects for all text, arrows, callouts, labels, circles,
   legends, and status cards.
5. Add an editability test that checks each final slide has native text/shapes
   and is not only one full-slide picture.
6. Render the rebuilt deck and compare the contact sheet against the current
   V5.5 visual style before sending it to Drive or the main deck.
