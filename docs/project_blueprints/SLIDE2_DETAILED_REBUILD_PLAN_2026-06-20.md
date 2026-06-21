# Slide 2 Detailed Rebuild Plan - 2026-06-20

Working deck inspected:

- Google Slides title: `EDITABLE REBUILD WORKING v2 - North Slope Gas Hydrate ML Workflow - 2026-06-20`
- Presentation ID: `1f-WlVV-EPC8tH3e2vC17jaRU8sQSd8jjdwxNOCiRQ1g`
- Target slide object ID: `p2`
- Current slide title: `Gas Hydrates And Why The North Slope Matters`

## Current Slide 2 Readback

The current slide is native/editable in structure, but it is still visually trying to do too much.

Current layout:

- Left column: "What gas hydrate is" with a dense World Atlas / Warrier structure assembly figure.
- Center column: "Why the North Slope" with a focused 2D stability map.
- Right column: "P-T diagram" with selected USGS/DOE stability figure and three interpretation cards.
- Bottom rail: "Why this project" statement plus source footnote.

Main visual problems visible in the current thumbnail:

- The hydrate-structure figure is too complex for an audience intro. It is a technical assembly diagram, not a clear "what is methane hydrate" image.
- The teal Structure I highlight is still competing with the figure instead of clarifying it.
- The slide has too many small labels and captions. Several captions are too small to read from a projected slide.
- The center map is better than the old map, but the currently embedded version is too zoomed out and quiet. It does not clearly read as the focused interactive/website-style 2D well map the user expected.
- The right P-T diagram is cramped and visually secondary; it should stay, but it needs less surrounding prose.
- The bottom source line should move mostly to the Word companion/end material.

## Better Hydrate Image Found

Recommended replacement for the left-column hero image:

- Source: NOAA Ocean Exploration, "What are gas hydrates?"
- Image URL: `https://oceanexplorer.noaa.gov/wp-content/uploads/2013/01/methane-hydrate-800.jpg`
- Local review copy: `C:\Users\gargi\Documents\AI powerpoint\slide2_candidate_noaa_methane_hydrate_cage.jpg`
- Why it is better: it directly shows methane in a water-molecule cage. It is simple, government-source backed, and matches the first sentence of the slide.
- Use: main "what gas hydrate is" visual.

Secondary structure-source option:

- Source: Ghaani, Schicks, and English, 2021, Applied Sciences / MDPI, open access CC BY.
- Figure image URL: `https://mdpi-res.com/applsci/applsci-11-00469/article_deploy/html/images/applsci-11-00469-g001-550.jpg`
- Local review copy: `C:\Users\gargi\Documents\AI powerpoint\slide2_candidate_mdpi_si_sii_sh.jpg`
- Why it helps: it is cleaner than the current World Atlas/Warrier crop for showing sI, sII, and sH.
- Why it should not be the main image: it is still a technical cage assembly figure. Use as source/provenance or as a small optional inset only if needed.

Recommended final approach:

- Do not use the current World Atlas/Warrier structure assembly figure as the left-column hero.
- Use the NOAA methane-hydrate cage image as the hero visual.
- Explain Structure I, Structure II, and Structure H with editable cards or a simplified redraw-after-source mini strip, not with a large copied paper figure.
- Keep Warrier/World Atlas and MDPI as source support in notes/companion material.

## Slide 2 Story Spine

The final slide should answer three questions:

1. What is methane hydrate?
2. Why does the Alaska North Slope matter?
3. Why does the P-T diagram matter before ML?

Keep this spine. Do not add ML architecture, model results, or equation content.

## Proposed Final Layout

Use the same three-column skeleton, but reduce density and make the visuals clearer.

### Left Column: What Methane Hydrate Is

Replace the current Warrier/World Atlas image with the NOAA cage image.

Visual plan:

- Large NOAA methane-hydrate cage image, cropped cleanly so the central methane molecule and water cage fill most of the column.
- One short editable label above or beside image:
  `Methane in water cages`
- One sentence under image:
  `Gas hydrate is an ice-like solid where water cages trap gas under cold, pressurized conditions.`
- Three native/editable mini cards under the image:
  - `Structure I`: `methane-rich baseline`
  - `Structure II`: `larger / mixed gases`
  - `Structure H`: `larger hydrocarbons + methane`
- Add a small editable tag:
  `This project uses methane / Structure I unless gas composition is being tested.`

Remove from the slide face:

- The full cage assembly figure.
- The baked-in teal circle.
- Tiny World Atlas caption bar.
- Long source wording.

Move to Word/end material:

- World Atlas Fig. 1.1 provenance.
- Warrier et al. 2016 source chain.
- MDPI/structure unit-cell details.
- Any rights/caption review caveat.

### Center Column: Why The North Slope

Use the focused interactive-style map, not the wide quiet export.

Current local map candidates:

- Too wide for Slide 2 hero but useful source stack:
  `C:\Users\gargi\Documents\AI powerpoint\north-slope-gas-hydrates-website-map-update\docs\project_blueprints\presentation_assets\website_well_maps_2026_06_18\unified_north_slope_well_stability_context_map_2026_06_18.png`
- Better focused visual style:
  `C:\Users\gargi\Documents\AI powerpoint\north-slope-gas-hydrates-website-map-update\docs\project_blueprints\presentation_assets\website_well_maps_2026_06_18\slide3_correct_2d_well_stability_map_2026_06_18.png`
- Current Slide 2 embedded map appears closer to:
  `unified_north_slope_slide_export_callout_space_2026_06_18.png`, but it is too zoomed out once placed in the column.

Required map rebuild direction:

- Build or export a new Slide 2 map crop from the interactive/OSL-style focused map.
- Keep only stability-relevant points and project anchors.
- Make non-informative gray wells smaller or remove them.
- Keep wells with calculated stability intervals/ranges visible.
- Add the four project wells with names/locations if their public-safe names and coordinates are verified.
- Keep large field/region labels: Prudhoe Bay, Kuparuk River, Milne Point, Pikka, Colville River, Endicott, Deadhorse/TAPS/Dalton corridor.
- Keep DNR unit outlines and key roads/pipeline if they help orientation.
- Use status colors only for stability-screen status, not hydrate occurrence.
- Caption should say:
  `North Slope map: stability-screen context + project wells`
- Do not say `project website`.

Map visual hierarchy:

- Blue or teal: calculated stability interval wells.
- Distinct highlight: four project wells.
- Pale gray: background context only, either much smaller or removed.
- Thin gray outlines: DNR units.
- Brown/black line: TAPS / Dalton corridor.
- Large black labels: key fields/regions.

### Right Column: P-T Diagram

Keep the right column, but simplify.

Use:

- CSV-derived methane 5 ppt P-T diagram where possible.
- If the current USGS/DOE figure is retained, make it larger or crop to the stability curve and legend only.
- Keep the three interpretation cards:
  - `Assumption`: `methane / Structure I / 5 ppt`
  - `Meaning`: `admissible under assumptions`
  - `Guardrail`: `not proof; not saturation`

Change wording:

- Use `P-T diagram`, not `P-T gate`.
- Remove long prose above the diagram.
- Keep one sentence:
  `Stability checks whether hydrate is physically admissible under selected assumptions.`

Move to Word/end material:

- Full source citation for the selected stability figure.
- Details of the digitized methane 5 ppt curve.
- Caveats about salinity, gas composition, pressure gradient, and temperature profile choices.

### Bottom Rail

Current bottom rail is useful but too long.

Replace with:

`Slide takeaway: North Slope hydrate interpretation needs structure chemistry, regional setting, P-T stability, and well/core evidence before any ML claim.`

Move the long source sentence below the slide face into speaker notes or Word companion.

## Exact Text Draft For Slide Face

Title:

`Gas Hydrates And Why The North Slope Matters`

Subtitle:

`Source-backed context: hydrate structure, North Slope setting, and P-T stability before any ML claim.`

Left column:

- Header: `What methane hydrate is`
- Main label: `Methane in water cages`
- Sentence: `Water cages trap methane under cold, pressurized conditions.`
- Cards:
  - `Structure I`: `methane-rich baseline`
  - `Structure II`: `larger / mixed gases`
  - `Structure H`: `larger hydrocarbon scenarios`
- Small note: `I is the project baseline; II/H are gas-composition sensitivity.`

Center column:

- Header: `Why the North Slope`
- Sentence: `Public maps locate stability-screen wells, project wells, fields, roads, units, and the TAPS corridor.`
- Caption: `Focused 2D North Slope map: stability context + project wells`
- Guardrail: `Map context is not occurrence or saturation evidence.`

Right column:

- Header: `P-T diagram`
- Sentence: `Stability tests physical admissibility under selected assumptions.`
- Cards:
  - `Assumption`: `methane / Structure I / 5 ppt`
  - `Meaning`: `admissible under assumptions`
  - `Guardrail`: `not proof; not saturation`

Bottom:

`Takeaway: combine structure chemistry, North Slope context, P-T stability, and well/core evidence before any occurrence or saturation ML claim.`

## Editable Versus Raster Objects

Native editable text/shapes:

- Slide title and subtitle.
- Column headers.
- Number badges.
- All labels/callouts.
- Structure I/II/H cards.
- Map legend bullets or mini legend.
- P-T interpretation cards.
- Bottom takeaway.

Raster/high-resolution image objects:

- NOAA methane-hydrate cage image.
- Focused North Slope map export.
- P-T diagram export.
- Optional small structure figure inset if retained.

Do not bake these into the PNGs:

- Structure I/II/H explanatory text.
- Map callout arrows.
- Project-well labels if they need manual movement.
- P-T assumption/meaning/guardrail text.

## Source Notes

Sources to cite in Word/end material:

- NOAA Ocean Exploration, "What are gas hydrates?", for simple methane hydrate cage image and basic definition.
- USGS Fact Sheet 2007-3041, Waite, for gas hydrate definition and methane hydrate context.
- USGS 2019 Alaska North Slope assessment release for 53.8 Tcf technically recoverable gas hydrate resource estimate.
- Warrier et al. 2016, Journal of Chemical Physics, and World Atlas Fig. 1.1, for the original complex structure figure provenance.
- Ghaani, Schicks, and English 2021, Applied Sciences, for open-access clathrate hydrate structure illustration support.
- Project public stability products and map builder/source inventory for the focused map.

## Acceptance Checklist

Before calling Slide 2 fixed:

- The left image reads immediately as methane in a water cage.
- Structure I/II/H are explained without using the complex assembly figure as the main image.
- The map looks like the focused well map the user remembers, with readable field/region labels.
- Gray/background wells no longer dominate.
- Four project wells are shown only if public-safe names/locations are verified.
- The P-T diagram uses `P-T diagram`, not `P-T gate`.
- The P-T curve is CSV-derived or clearly source-backed.
- No slide text says `project website`.
- No source notes are tiny on the slide face.
- All labels, callouts, circles, and cards are editable.
- Stability is described only as context/admissibility, not proof, occurrence, saturation, producibility, or ranking.
