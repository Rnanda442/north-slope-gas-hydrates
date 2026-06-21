# Native Editable Deck Master Builder Implementation Note

Date: 2026-06-19

Prompt: 16, Native Editable Deck Master Builder.

## Runtime Status

The required Presentations skill runtime contract requires
`@oai/artifact-tool`. On this machine:

```text
node -e "require.resolve('@oai/artifact-tool')"
```

failed with `Cannot find module '@oai/artifact-tool'`, and:

```text
npm view @oai/artifact-tool version
```

returned `404 Not Found`.

Because of that, this pass does not generate a new candidate PPTX. Creating a
final candidate deck through `python-pptx` would violate the current
Presentations skill contract for final deck output.

## What Was Added Instead

`docs/project_blueprints/audit_pptx_editability.py` is a reusable inspection
utility. It reads a PPTX and reports, per slide:

- slide number;
- total shape count;
- picture count;
- editable text-shape count;
- connector-like shape count;
- full-slide picture count;
- whether the slide is a one-picture full-slide raster;
- pass/fail editability status.

Example:

```powershell
python docs/project_blueprints/audit_pptx_editability.py `
  docs/project_blueprints/V5_5_SLIDE2_SOURCE_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Slides_2026-06-17.pptx `
  --out-md outputs_runtime/editability_audit/v5_5_slide2_source_update.md `
  --out-csv outputs_runtime/editability_audit/v5_5_slide2_source_update.csv
```

## Builder Requirements For The Next Runtime

The actual native builder should be created in an environment where
`@oai/artifact-tool` resolves. It should:

1. Create a new nine-slide candidate deck, not overwrite the active V5.5 deck.
2. Keep title, subtitle, cards, arrows, labels, callouts, circles, captions,
   status text, and legends as native editable text/shapes/connectors.
3. Keep maps, source figures, P-T plots, and other dense visuals as high
   resolution image objects.
4. Export PNG previews, a contact sheet, and layout JSON for QA.
5. Run the editability audit and fail if any main slide is only one full-slide
   image.
6. Keep detailed citations and source notes in notes/Word, not tiny slide-face
   text.

## Suggested Object Spine

| slide | editable objects | image objects |
|---:|---|---|
| 1 | title, subtitle, name/date, photo placeholder, concise readiness line | none unless user supplies photo later |
| 2 | title, map labels, Structure I callout circle, P-T diagram label, gas-source labels, captions | unified North Slope map, P-T plot, structure source figure after rights review |
| 3 | log-track labels, lithology labels, curve callouts, core/NMR strip labels | generated/source-backed log panel or DOE export |
| 4 | workflow boxes and arrows | optional simplified icon/figure backgrounds |
| 5 | symbol labels, role tags, equation card titles | equation renderings if native equation objects are unavailable |
| 6 | evidence-board labels, lane headings, takeaway | source-backed evidence visuals |
| 7 | map callouts, context caption, legend labels | unified stability/context map |
| 8 | planned output lanes, review flags, placeholders | future reviewed DOE export figures |
| 9 | built/not claimed/next boxes | optional simple source-backed close visual |

## QA Gate

Run:

```powershell
python -m py_compile docs/project_blueprints/audit_pptx_editability.py
python -m pytest tests/test_pptx_editability_audit.py -q
```

Then run the audit on any generated deck before upload/import to Drive.
