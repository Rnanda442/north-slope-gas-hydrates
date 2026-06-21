# Slide-By-Slide Workspace Guide - 2026-06-21

## Active Deck For Manual Cleanup

Current Drive working deck:

`EDITABLE REBUILD WORKING v2 - North Slope Gas Hydrate ML Workflow - 2026-06-20`

Google Slides ID:

`1f-WlVV-EPC8tH3e2vC17jaRU8sQSd8jjdwxNOCiRQ1g`

URL:

`https://docs.google.com/presentation/d/1f-WlVV-EPC8tH3e2vC17jaRU8sQSd8jjdwxNOCiRQ1g`

Reference deck:

`EDITABLE VISUAL MATCH - North Slope Gas Hydrate ML Workflow - 2026-06-19`

Repo-side visual-match artifacts:

`docs/project_blueprints/presentation_assets/editable_visual_match_2026_06_19/`

## Working Rule

Fix one slide at a time. Do not rebuild the whole deck unless the user asks for
a full rebuild. For a single-slide request, edit only that slide in the Drive
working deck, then save any source asset, screenshot, or handoff note in the
repo.

## Per-Slide Workflow

1. Read `docs/AGENT_START_HERE.md` and `docs/CURRENT_ARTIFACT_INDEX.md`.
2. Confirm `git status -sb` in the unified workspace.
3. Inspect the target slide in the active Drive deck and fetch a fresh
   thumbnail before editing.
4. Compare against the relevant reference thumbnail or prior deck slide.
5. Update only the target slide unless the user asks for cross-slide changes.
6. Keep titles, short labels, arrows, circles, callouts, and explanatory text
   editable in Google Slides.
7. Keep maps, P-T plots, source figures, and complex diagrams as high-resolution
   PNG/SVG only when they are better as figures.
8. Export or fetch a post-edit thumbnail and visually compare before declaring
   done.
9. Commit only GitHub-safe source assets, scripts, docs, and public-safe
   generated figures. The Drive-native slide edit itself lives in Drive.

## Slide 2 Current Notes

Latest detailed plan:

`docs/project_blueprints/SLIDE2_DETAILED_REBUILD_PLAN_2026-06-20.md`

Latest focused map insert used in Drive:

`docs/project_blueprints/presentation_assets/website_well_maps_2026_06_18/unified_north_slope_slide2_map_insert_2026_06_21.png`

The map should come from the website/unified map path, not from an older broad
well-dot PNG.

## Map Rule

For map slides, use the unified website map behavior:

- default view: calculated stability-range wells plus the four project/source
  wells;
- optional audit view: full background wells/status context;
- labels/legend/zoom must be readable;
- stability remains context only, not hydrate proof.

## Guardrails

Never commit approved rows, raw workbooks, row-level predictions, trained
models, fitted scalers, private screenshots, raw source bundles, credentialed
PDFs, or unsupported hydrate results.

Use wording such as `context`, `source-case anchor`, `header-verified`, `public
well metadata`, `planned DOE export`, and `not hydrate proof` until approved
runtime and mentor review are complete.
