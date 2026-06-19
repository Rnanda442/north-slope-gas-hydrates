# Editable Slides 1 And 2 Object Spec

Date: 2026-06-19

Prompt: 17, Editable Slides 1 And 2 Final Context Build.

This is the object-level spec to use once the native editable builder runtime is
available.

## Slide 1: Clean Opener

Purpose: introduce the project as a workflow/readiness and source-backed ML
pipeline, not final predictions.

Editable objects:

| object | type | content |
|---|---|---|
| Title | native text box | `North Slope Gas Hydrate Reservoir Characterization` |
| Subtitle | native text box | `Source-backed logging, core, stability, and ML workflow` |
| Author block | native text box | user name, institution, date placeholder |
| Photo placeholder | native rectangle + editable label | `Photo placeholder` |
| Readiness line | native text box | `Built: source library, public maps, stability context, and approved-runtime code path` |
| Boundary line | native text box | `Not claimed yet: hydrate proof, trained metrics, occurrence or saturation predictions` |

Rules:

- Remove any RapCaviar content.
- Do not use the old personal photo.
- Keep all text editable.
- Keep the photo area blank unless the user supplies a new image.

## Slide 2: Methane Hydrate And North Slope Context

Purpose: explain what the system is and why the Alaska North Slope matters.

Source assets to use:

| asset | path/status | use |
|---|---|---|
| Unified North Slope map | `docs/project_blueprints/presentation_assets/website_well_maps_2026_06_18/unified_north_slope_slide_export_callout_space_2026_06_18.png` if present | Main map/context figure |
| Candidate Slide 2 assets | `docs/project_blueprints/presentation_assets/slide2_methane_context_2026_06_19/` | Source material from prior Slide 2 rebuild |
| Methane 5 ppt P-T diagram | CSV-derived asset from Slide 2 candidate folder if present | Explain pressure-temperature context |
| Structure I/II/H source figure | Use only after caption/rights review | Structure type explanation with editable callout circle |

Editable objects:

| object | type | content |
|---|---|---|
| Slide title | native text box | `Methane hydrate on the Alaska North Slope` |
| Map callouts | editable text boxes/arrows | Prudhoe Bay / Kuparuk / Milne / Eileen trend context as source-backed labels |
| Structure I circle | editable oval | Circle Structure I cleanly, not as baked pixels |
| Structure labels | native text boxes | `Structure I: methane baseline`; `Structure II/H: gas-composition sensitivity` |
| Gas-source tags | native compact labels | `biogenic methane`; `thermogenic gas contribution` |
| P-T label | native text box | `P-T diagram: stability context, not hydrate proof` |
| Resource motivation | native text box | government/source-backed one sentence, citation in notes |
| Caption | native text box | short context-only caveat |

Slide face text:

```text
Methane hydrate is ice-like methane trapped in water cages. On the North Slope,
hydrate discussion is tied to permafrost, pressure-temperature stability,
reservoir-quality sand, and gas charge.
```

Do not put detailed citation blocks on the slide face. Put citations in notes
or the Word companion.

## Layout

Use a 16:9 slide.

- Top: editable title and one-line system definition.
- Left 55-60 percent: unified North Slope map with editable callouts.
- Right top: hydrate structure image with editable Structure I circle.
- Right bottom: P-T diagram with one editable label.
- Bottom: one short context-only caption.

## Validation

When built, run:

```powershell
python docs/project_blueprints/audit_pptx_editability.py <candidate-deck.pptx> `
  --out-md outputs_runtime/editability_audit/slides_1_2.md `
  --out-csv outputs_runtime/editability_audit/slides_1_2.csv
```

Slides 1 and 2 should have editable text shapes and should not be one-picture
full-slide raster slides.
