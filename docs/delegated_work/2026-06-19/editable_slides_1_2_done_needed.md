# Editable Slides 1 And 2 Done / Needed Handoff

## Prompts Worked On

Prompt 17: Editable Slides 1 And 2 Final Context Build.

## Done

- Identified dependency on Prompt 16 native editable builder.
- Confirmed the required `@oai/artifact-tool` runtime is not available in this
  thread, so a compliant candidate PPTX could not be produced here.
- Created `docs/project_blueprints/EDITABLE_SLIDES_1_2_OBJECT_SPEC_2026-06-19.md`
  with exact editable objects, source assets, slide-face wording, and validation
  requirements.
- Confirmed Slide 1 should be a clean opener with a blank editable photo
  placeholder and no RapCaviar/old personal photo content.
- Confirmed Slide 2 should use the unified North Slope map, CSV-derived P-T
  diagram, structure figure after rights/caption review, thermogenic/biogenic
  wording, and source-backed resource motivation.

## Still Needed

- Build the actual editable Slides 1 and 2 candidate in a runtime with
  `@oai/artifact-tool`.
- Verify candidate Slide 2 assets exist and pick the final map/P-T/structure
  image versions.
- Review rights/caption status for the Structure I/II/H source figure before
  using it in the final deck.
- Render PNG previews/contact sheet and run the editability audit.

## Files / Assets

| file path | status | why it matters |
|---|---|---|
| `docs/project_blueprints/EDITABLE_SLIDES_1_2_OBJECT_SPEC_2026-06-19.md` | created | Object-level build spec for Slides 1-2 |
| `docs/delegated_work/2026-06-19/editable_slides_1_2_done_needed.md` | created | Handoff for main Codex |

## Branch / Commit

Branch pending at handoff creation: `codex/prompts-14-17-20260619`.

## Slides Affected

Slides 1 and 2.

## Main Codex Next Steps

- Use the object spec as the exact build checklist for a future editable deck
  build.
- Do not upload a whole-slide screenshot version as the final editable Slides
  1-2 package.
- Keep citations in notes/Word and slide text minimal.
