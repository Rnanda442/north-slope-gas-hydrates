# Slide 2 Instruction Sheet: Gas Hydrate Introduction

Created: 2026-06-12

## Objective

Rebuild slide 2 so it clearly answers one question:

```text
What is a methane gas hydrate, and why is the Alaska North Slope the right
place to screen for it?
```

The slide should teach through visuals first. It should not look like a collage
of small figures. It should move left to right from molecule and sediment, to
pressure-temperature stability, to North Slope map and structural context.

## Current Slide 2 Problems

- The gas hydrate explanation is present, but it is still too abstract. The
  SEM image plus simple CH4 cage does not clearly show methane hydrate inside
  sediment pores.
- The DOE logo is visually large relative to the explanation. It should support
  the energy-security point, not become the main scientific figure.
- The pressure-temperature plot is useful, but it needs clearer labels and a
  short takeaway: stability is required, but stability alone does not prove
  hydrate.
- The 2D North Slope map and Streamlit structural explorer are too small. They
  need to show why regional structure, reservoir sands, source intervals, and
  basement context guide screening.
- The slide does not explain the structural explorer legend enough. Viewers
  need to know what the layers mean and why they matter.
- The current title is acceptable, but the subtitle should say the main idea in
  one sentence instead of using a broad energy-security phrase only.

## Required Message

Use this exact main message as the slide logic:

```text
Methane hydrate is CH4 trapped in water-ice cages. On the North Slope, the
screening question is where methane supply, reservoir sand, pressure-temperature
stability, and structural context overlap.
```

Keep these scientific boundaries visible:

- Target system: methane hydrate, not all possible hydrate guest gases.
- Stability is necessary but not sufficient.
- Public map and structural context guide review.
- Approved runtime well logs and core evidence make the actual hydrate call.
- Do not imply that the public Streamlit map is using restricted well-log rows.

## Proposed Final Slide Title And Copy

Title:

```text
What Gas Hydrates Are and Why the North Slope Matters
```

Subtitle:

```text
Methane can be stored as ice-like water cages where cold temperature, pressure,
sand reservoirs, and gas supply overlap.
```

Use three numbered section labels:

```text
1. Methane hydrate
2. Stability window
3. North Slope screening context
```

Keep body copy to these callouts:

```text
CH4 in H2O cages
Ice-like solid in sediment pores
Stable only in the right pressure-temperature window
Stability guides screening; logs and core evidence confirm
Public map + structural layers show where to investigate
```

Footer source text:

```text
Sources: USGS gas hydrate FAQ and FS 2019-3037; USGS OF 96-272 phase-boundary
discussion; DOE/NETL North Slope hydrate pages; project Streamlit assets.
```

## Layout Specification

Canvas: 16:9 widescreen. For the current generated panels, use 1600 x 900 px.

Safe margins:

- Left/right: 60 px minimum.
- Top title zone: 55 to 145 px.
- Bottom source footer: 830 to 865 px.
- No important text below 820 px except the footer.

Recommended structure:

```text
Top: title and subtitle across the slide.

Left 32%: hydrate identity
- Large conceptual image of methane hydrate in sand pore.
- Small CH4/H2O cage inset.
- One short label: "CH4 in H2O cages".

Middle 30%: pressure-temperature stability
- Large clean pressure-temperature or depth-stability diagram.
- Highlight "hydrate-stable window".
- Add warning tag: "stable does not mean confirmed".

Right 38%: North Slope context
- Use the current Streamlit structural explorer image as the main right-side
  visual.
- Add the 2D North Slope map as a smaller locator inset above or beside it.
- Add a simple legend strip explaining the structural layers.
```

Approximate 1600 x 900 placement:

| Area | Bounds | Contents |
|---|---:|---|
| Title | x 70-1530, y 55-130 | Title and subtitle |
| Hydrate visual | x 75-510, y 175-620 | Methane hydrate in sediment pores plus cage inset |
| Hydrate text | x 80-510, y 635-760 | 2 short callouts |
| Stability visual | x 545-990, y 185-625 | P-T stability diagram |
| Stability text | x 565-970, y 640-760 | necessary/not sufficient warning |
| North Slope context | x 1030-1530, y 175-690 | Large Streamlit structural explorer |
| Locator and legend | x 1030-1530, y 700-805 | 2D map inset and layer legend |
| Footer | x 70-1530, y 835-860 | Sources |

## Visual Direction

Use a clean scientific-Processing style:

- white or very light background;
- one teal vertical accent line to stay consistent with the deck;
- thin gray figure frames only where they help separate visuals;
- teal for hydrate stability and selected structural overlays;
- amber for methane/gas supply;
- green for reservoir sands;
- purple or dark magenta for source interval / Shublik style context;
- gray for basement or structural relief.

Avoid:

- crowded card grids;
- decorative logos as the largest object;
- tiny screenshots that cannot be read;
- unexplained symbols;
- unlabeled axes;
- long paragraphs.

## Required Visual Assets

Use these existing local assets:

| Role | Asset |
|---|---|
| Current Streamlit structural explorer | `references/presentation-revision-2026-06-11/images/project_streamlit_structural_explorer_v2.png` |
| 2D North Slope context map | `raw_data/geology/CNS_AUs/CNS_AUs.jpg` |
| USGS hydrate crystal reference | `references/presentation-revision-2026-06-11/images/usgs_gas_hydrate_crystals_sem_public_domain.jpg` |
| DOE visual reference from Gmail | `references/presentation-revision-2026-06-11/gmail-2026-06-11/gmail_inline_03.png` |

Recommended new generated visual:

- Create a conceptual scientific raster image of methane hydrate in a sand pore:
  sediment grains, blue water-ice cages, amber CH4 molecules, cold/pressure
  cues, no long text. Label it in the slide as conceptual.

Use the USGS SEM image as a small source-backed inset or texture, not as the
only hydrate explanation. The conceptual pore image will be easier for the
audience to understand.

## Source Basis

| Source | Use On Slide |
|---|---|
| USGS FAQ, "What are gas hydrates?" | Plain-language definition: water + gas crystalline solid, methane-rich, Arctic permafrost relevance, energy/hazard/climate importance. |
| USGS Fact Sheet 2019-3037 | North Slope resource framing and why the region matters. |
| USGS OF 96-272 phase-boundary discussion | Pressure-temperature phase boundary and stability-window diagram. |
| DOE Alaska North Slope Gas Hydrates Site Visit | North Slope production-test and energy-security context. |
| NETL Alaska North Slope Gas Hydrate Reservoir Characterization | Reservoir characterization, 3D seismic/log/core context, reservoir sand and production-screening rationale. |
| Project Streamlit assets | Current public/synthetic structural explorer and map context. |

Public URLs:

- https://www.usgs.gov/faqs/what-are-gas-hydrates
- https://pubs.usgs.gov/publication/fs20193037
- https://pubs.usgs.gov/of/1996/of96-272/ch04.html
- https://www.energy.gov/hgeo/articles/alaska-north-slope-gas-hydrates-site-visit
- https://netl.doe.gov/node/6846

## Structural Explorer Legend Instructions

The structural explorer needs a reader-facing legend. Use short labels:

```text
Public wells/boundaries: regional reference only
Reservoir sands: possible hydrate-host intervals
Shublik/source interval: hydrocarbon charge context
Basement/relief: structural framework and migration pathways
Runtime evidence: approved logs/core decide occurrence and saturation
```

If space is limited, use four legend chips:

```text
reservoir sand
source interval
basement relief
runtime logs
```

Do not overstate the map. Say "screening context" or "where to investigate",
not "where hydrate is present".

## Pressure-Temperature Diagram Instructions

Redraw the diagram rather than pasting a low-resolution screenshot.

Required labels:

```text
Pressure / depth
Temperature
hydrate-stable window
geothermal path
too warm / unstable
```

Required annotation:

```text
Stability is a gate, not a label.
```

Design notes:

- Make the stable region a light teal polygon.
- Draw the geothermal path as a red or amber line.
- Use one dark teal phase-boundary line.
- Show a small North Slope/permafrost note if there is room:
  `Arctic permafrost keeps shallow intervals cold`.
- Avoid detailed numeric axes unless exact values are sourced and legible.

## Image Generation Prompt

Use this prompt if generating the hydrate-in-sediment concept visual:

```text
Scientific educational illustration of methane gas hydrate in a sand pore,
wide 4:3 composition, tan rounded sediment grains around the edges, translucent
blue water-ice cage structures in pore spaces, small amber CH4 molecules inside
the cages, subtle cold temperature and pressure cues, clean white background,
high contrast, crisp labels only for CH4 and H2O if labels are included, no
people, no drilling rig, no decorative background, suitable for a university
geoscience presentation.
```

If labels are included in the generated image and they are imperfect, remove
the labels and add clean labels in the slide builder instead.

## Detailed Implementation Prompt

Use this prompt for a future slide edit pass:

```text
Revise slide 2 only. Keep the deck's clean white/teal visual style, but rebuild
the slide around three large visual zones instead of small scattered tiles.

Title the slide "What Gas Hydrates Are and Why the North Slope Matters".
Use the subtitle "Methane can be stored as ice-like water cages where cold
temperature, pressure, sand reservoirs, and gas supply overlap."

Left zone: show a large conceptual methane hydrate in sediment-pore visual,
with a small CH4-in-H2O cage inset and the callouts "CH4 in H2O cages" and
"Ice-like solid in sediment pores". Use the USGS hydrate crystal image only as
a small source-backed inset if helpful.

Middle zone: redraw a clean pressure-temperature stability diagram from the
USGS phase-boundary concept. Label pressure/depth, temperature,
"hydrate-stable window", "geothermal path", and "too warm / unstable". Add the
warning "Stability is a gate, not a label."

Right zone: make the current Streamlit structural explorer the main visual and
add the 2D North Slope map as a locator inset. Add a concise legend explaining
reservoir sand, source interval, basement relief, and runtime logs/core
evidence. Say "screening context", not "hydrate confirmed".

Keep all body text short. Do not use real well-log rows, restricted well names,
approved-runtime data, trained model outputs, or unverified hydrate locations.
Use concise footer sources: USGS gas hydrate FAQ and FS 2019-3037; USGS OF
96-272 phase-boundary discussion; DOE/NETL North Slope hydrate pages; project
Streamlit assets.
```

## Acceptance Checklist

Slide 2 passes only if all are true:

- The viewer can explain what methane hydrate is within 10 seconds.
- The slide clearly says or implies the target is methane hydrate (`CH4`).
- The hydrate visual shows pore-scale or sediment-scale context, not only an
  abstract molecule.
- The pressure-temperature diagram is legible and says stability is not proof.
- The current Streamlit structural explorer is used, not the older image.
- The 2D North Slope map is present as public regional context.
- The structural legend explains at least reservoir sand, source interval,
  basement/relief, and runtime evidence.
- The DOE/NETL material supports the energy/security and characterization
  point without dominating the slide.
- The footer cites official/public sources and project assets.
- No restricted data, approved-runtime rows, trained outputs, or sensitive
  identifiers are shown.
- All text is readable at thumbnail/contact-sheet size.
- No text or visuals are clipped, crowded against the edge, or overlapping.

## Decision For This Slide

Approved in chat on 2026-06-12 for a slide-2-only pass using the source pool
above, Processing-style visuals only, and corrected symbology.

Execution record:

- Rebuilt only slide 2 in
  `docs/project_blueprints/build_processing_slide_assets.py`.
- Used the USGS SEM image as the main hydrate visual anchor and overlaid a
  methane-in-water-cage clathrate symbol.
- Kept the hydrate explanation source-backed with USGS FAQ, USGS Gas Hydrates
  Primer, NETL Methane Hydrate Primer, USGS OF 96-272 P-T boundary, the USGS
  SEM image, and project Streamlit assets.
- Rendered `CH4`, `H2O`, and `CH4.nH2O` with a custom formula helper so digits
  appear as subscripts and the hydrate separator appears as a centered dot in
  the PNG; this avoided missing-glyph boxes from Unicode subscripts in the
  slide font.
- Redrew the P-T stability gate directly in the asset and kept the statement
  that stability is necessary, not proof.
- Used the current Streamlit structural explorer and 2D North Slope map as
  public screening context, not hydrate confirmation.
- Regenerated the local PNG/PPTX and replaced only slide 2 image `p2_i2` in the
  current Drive deck
  `GMAIL VISUAL REVISION 9-SLIDE North Slope Gas Hydrate Slides 2026-06-11`.
- Verified the fresh Google-rendered thumbnail at
  `drive-thumbnails-2026-06-12/slide_p2_thumbnail_after_processing_symbol_redo_final.png`.

Note: `processing-java` was not callable in the current shell, so the execution
uses a reproducible Processing-style raster generated with Pillow rather than
the Processing CLI. The current Drive deck still stores the slide as one
full-slide raster image, matching the existing deck pattern.
