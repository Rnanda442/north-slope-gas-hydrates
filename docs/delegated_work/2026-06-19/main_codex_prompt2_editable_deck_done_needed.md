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

## Still Needed

- Do not rebuild the deck yet until the user explicitly asks for implementation.
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
