# Website Navigation and Visual Redesign Plan

Last updated: 2026-06-08

## Objective

Reduce navigation complexity and replace long explanatory sections with a
small number of strong visual stories. The website should function as a visual
working surface for the North Slope project and as a source of reusable figures
for the Word document and PowerPoint.

This document is the required plan before the next website implementation
changes.

## Design Rules

1. Use no more than four top-level navigation choices.
2. Each page answers one primary question.
3. Lead with a visual before explanatory text.
4. Keep introductory paragraphs below 35 words.
5. Keep cards below 18 words, excluding labels and numbers.
6. Use one visual language: restrained government-science colors, simple line
   icons, clear arrows, and consistent evidence-status colors.
7. Do not use decorative imagery that has no scientific or workflow meaning.
8. Every visual must be reusable in the PowerPoint or Word document.
9. Public pages remain synthetic and public-source only.
10. Mobile views must stack into one clear reading order without horizontal
    scrolling.

## Proposed Four-Page Navigation

| New page | Primary question | Existing content merged |
|---|---|---|
| Overview | What is this project, how does it work, and what happens next? | Welcome, high-level Research Framework, roadmap summary |
| Explore North Slope | What regional geology and public data constrain the problem? | Regional Atlas, Structural Explorer, Data Library |
| Analyze Hydrates | How will logs and core data become hydrate and sweet-spot decisions? | North Slope Sweet Spots, Future Well-Log Engine |
| Project Plan | What is built, blocked, decided, and next? | Project Roadmap, detailed Research Framework, source and deliverable status |

The sidebar should show only these four choices. Detailed tools should appear as
sections or a maximum of three tabs inside their owning page.

## Internal Tab Limits

### Explore North Slope

Maximum three tabs:

1. `Regional Map`
2. `3D Structure`
3. `Data & Sources`

### Analyze Hydrates

Maximum three tabs:

1. `Interval Review`
2. `Runtime Readiness`
3. `Methods & Evidence`

Move downloads and detailed tables into expanders inside those tabs. Do not use
a separate tab for every table or calculation family.

### Project Plan

Avoid tabs. Use a vertical summary:

1. current phase;
2. next three actions;
3. workstream status;
4. blockers and decisions;
5. deliverable plan.

## Overview Page Structure

The overview should fit its essential story into six visual sections.

### Visual 1: Hero System Illustration

**Purpose:** Explain the entire project within ten seconds.

**Layout:** Wide 16:7 hero. Alaska North Slope silhouette on the left, a
vertical well/log motif in the center, and an interval decision card on the
right. A single arrow connects the three.

**Visible text:**

- Title: `Constraining North Slope Gas Hydrates`
- Subtitle: `Public geology + approved logs + physics-constrained ML`
- Three labels only: `Regional context`, `Well evidence`, `Interval decisions`

**Detailed generation prompt:**

> Create a clean scientific vector-style hero illustration for an Alaska North
> Slope gas-hydrate machine-learning project. Use a wide horizontal composition
> with three connected stages. Left: a simplified North Slope Alaska silhouette
> with subtle contour lines, a few well-location dots, and one structural
> horizon. Center: a vertical wellbore with six narrow wireline tracks suggesting
> gamma ray, resistivity, density, compressional sonic, shear sonic, and
> saturation; highlight one candidate interval. Right: a compact decision card
> with four stacked outcomes: hydrate detection, saturation, uncertainty, and
> sweet-spot priority. Connect the stages with one continuous directional line.
> Style: modern government scientific briefing, flat vector geometry, no
> photorealism, no decorative background, no gradients that reduce legibility,
> dark navy background, ice blue and teal scientific accents, muted amber for
> uncertainty, off-white labels, generous negative space. Do not include logos,
> people, drilling rigs, flames, or dense text. Make every element legible on a
> phone.

**Implementation preference:** Build as repository-native SVG or HTML/CSS so
labels remain editable and responsive.

**Improvement over current page:** Replaces the long hero paragraph with one
visual showing geography, logs, and the decision output.

### Visual 2: Three-Outcome Mission Strip

**Purpose:** Show that the project does not collapse every result into one
hydrate score.

**Layout:** Three equal icon cards.

**Cards:**

1. `Detect` - identify hydrate-supportive intervals.
2. `Quantify` - estimate saturation with uncertainty.
3. `Rank` - separate sweet spots from producibility.

**Icon prompts:**

- Detect:
  > Minimal line icon combining a vertical well log and a highlighted depth
  > interval, square composition, navy and teal, no text, transparent
  > background.
- Quantify:
  > Minimal line icon showing pore space as circles with a partially filled
  > percentage ring and a small uncertainty band, navy, ice blue, and muted
  > amber, no text, transparent background.
- Rank:
  > Minimal line icon showing three subsurface intervals ordered by evidence,
  > with a separate flow arrow under the highest-priority interval, navy and
  > teal, no trophy or generic business symbols, transparent background.

**Interaction:** Tapping a card expands one sentence and links to the relevant
section of `Analyze Hydrates`.

**Improvement:** Replaces four dense metrics and generic start cards with
scientific outcomes.

### Visual 3: Data-to-Decision Pipeline

**Purpose:** Explain the workflow to a non-ML specialist.

**Layout:** Six connected nodes with simple icons:

`Files -> QC -> Physics -> ML -> Expert review -> Deliverables`

**Visible labels below nodes:**

- `Logs + core`
- `Ready / partial / blocked`
- `Reservoir + elastic + saturation`
- `Held-out wells`
- `Uncertainty + reasons`
- `Word + slides + figures`

**Detailed generation prompt:**

> Design a horizontal scientific workflow diagram with six large circular or
> rounded-square nodes connected by a single line. The stages are source files,
> data quality control, physics-derived features, machine-learning models,
> geoscientist review, and report/presentation outputs. Use recognizable line
> symbols: table/file, check-and-warning grid, rock layers with equations,
> connected model nodes, eye with evidence card, and report with chart. Use very
> short labels and strong visual hierarchy. Color-code measured data in blue,
> derived physics in teal, model outputs in purple-blue, uncertainty in amber,
> and deliverables in off-white. Add a small branch at the QC node showing
> ready, partial, and blocked routing. Add a visual barrier between public
> planning and approved runtime without using alarming security imagery. Style
> should be suitable for a DOE technical presentation and remain readable at
> 390-pixel width when stacked vertically.

**Implementation preference:** Responsive HTML/SVG with nodes becoming a
vertical timeline on mobile.

**Improvement:** Replaces repeated prose descriptions of the analysis chain.

### Visual 4: Subsurface Evidence Stack

**Purpose:** Connect regional geology to interval-scale logs without implying
that maps directly classify hydrate.

**Layout:** Cutaway illustration with four horizontal levels:

1. regional map and structural setting;
2. pressure-temperature and reservoir context;
3. well-log tracks and core sample;
4. hydrate interval decision with uncertainty.

**Detailed generation prompt:**

> Create a clean geoscience cutaway diagram of the Alaska North Slope showing
> the scale transition from regional context to a single well interval. At the
> top, show a simplified map with one fault block and well dots. Below it, show
> layered permafrost and sedimentary units with a translucent gas-hydrate
> stability window. Continue into one vertical well with adjacent gamma-ray,
> resistivity, density, Vp, and Vs tracks and one core marker. Highlight a
> candidate hydrate-bearing sand, a water-bearing sand, and one uncertain
> interval using distinct but restrained colors. End with a small evidence card
> that states visually, not verbally, that regional geology constrains
> confidence while logs and core determine the interval interpretation. Flat
> scientific vector style, accurate stratigraphic layering, no dramatic gas
> bubbles, no photorealistic rig, no unverified formation names, minimal text.

**Implementation preference:** Custom SVG with hover labels for each evidence
layer.

**Improvement:** Makes the central scientific rule visible instead of burying
it in text.

### Visual 5: Current State / Next State Split

**Purpose:** Make project status understandable without a full roadmap table.

**Layout:** Two connected panels.

**Left, `Built now`:**

- public regional atlas;
- synthetic well-log scaffold;
- runtime readiness;
- source-backed equations;
- grouped-well validation plan.

**Right, `Activate with approved data`:**

- exact workbook mapping;
- core-log calibration;
- model training;
- held-out-well results;
- final Word and PowerPoint.

**Detailed generation prompt:**

> Create a two-panel technical roadmap visual. The left panel is labeled Built
> now and contains five completed modular blocks: regional atlas, synthetic
> well-log scaffold, runtime readiness, physics feature library, and grouped-well
> validation design. The right panel is labeled Activate with approved data and
> contains five outlined future blocks: exact input mapping, core-log
> calibration, model training, held-out-well evaluation, and final deliverables.
> Connect matching blocks with thin arrows. Use filled teal blocks for built
> items, outlined blue blocks for pending data-dependent items, and amber only
> for unresolved decisions. Avoid calendar timelines and percentage-complete
> gauges. Make the visual read left-to-right on desktop and top-to-bottom on
> mobile.

**Implementation preference:** HTML/CSS cards with SVG connector lines.

**Improvement:** Replaces the overview's generic repository counts with status
that directly affects project execution.

### Visual 6: Choose a Path

**Purpose:** Give the user three obvious actions without exposing all internal
pages.

**Cards:**

1. `Explore the North Slope`
   - icon: map layers and well dots;
   - destination: `Explore North Slope`.
2. `Review Hydrate Decisions`
   - icon: log tracks and highlighted interval;
   - destination: `Analyze Hydrates`.
3. `See What Happens Next`
   - icon: three-step execution path;
   - destination: `Project Plan`.

**Detailed prompt:**

> Create three matching square vector illustrations for a scientific web
> dashboard. Illustration one shows layered map sheets, well dots, and one
> structural contour. Illustration two shows five vertical well-log tracks with
> a highlighted interval and a small evidence check. Illustration three shows
> three connected implementation blocks leading to a report and slide. Use the
> same stroke weight, navy/teal/ice-blue palette, transparent backgrounds, and
> no embedded words. Keep the shapes simple enough for 96-pixel display.

**Interaction:** Entire card is clickable. The secondary sentence stays below
12 words.

## Icon System

Use one consistent outline icon family. Prefer repository-native SVG icons or a
single established open-source icon package already compatible with the app.
Do not mix emoji, photographs, 3D clip art, and unrelated icon styles.

Required icons:

- map;
- structural layers;
- wellbore;
- log tracks;
- core sample;
- pressure-temperature;
- quality check;
- warning/uncertainty;
- physics equation;
- ML nodes;
- held-out wells;
- expert review;
- Word report;
- presentation slide.

Icons should use `currentColor`, a 1.75-2 pixel stroke, rounded line joins, and
no internal text.

## Color and Meaning

| Color | Meaning |
|---|---|
| Dark navy | Primary background and regional context |
| Ice blue | Measured data and public inputs |
| Teal | Derived physics and ready outputs |
| Muted purple-blue | ML models and predictions |
| Muted amber | Uncertainty, partial readiness, or review |
| Muted red | Blocked or invalid only |
| Off-white | Labels and deliverable outputs |

Color must encode the same meaning everywhere.

## Text Reduction Rules

- One sentence under the hero.
- Maximum three mission cards.
- Maximum six pipeline nodes.
- No paragraph longer than two lines at normal desktop width.
- Put scientific definitions in hover help, expanders, or the Methods section.
- Replace overview tables with diagrams or status cards.
- Keep detailed source matrices, equations, and downloadable tables off the
  overview page.

## Implementation Sequence

### Change Set 1: Navigation Reduction

- Replace eight pages with four.
- Preserve old query-parameter links through a redirect/alias map.
- Merge content without deleting scientific functionality.
- Add tests for route aliases and page rendering.

### Change Set 2: Overview Visual Foundation

- Build the hero system illustration.
- Add the three-outcome mission strip.
- Build the responsive data-to-decision pipeline.
- Replace current repository metrics with project-relevant status.
- Validate desktop and 390-pixel mobile layouts.

### Change Set 3: Explore North Slope Consolidation

- Merge map, structural explorer, and data catalog into three tabs.
- Add a shared layer legend and consistent map/structure icons.
- Keep detailed file inventory in an expander.

### Change Set 4: Analyze Hydrates Consolidation

- Merge sweet-spot and future-engine content into three tabs.
- Lead with an interval review visual.
- Put readiness, source tables, equations, and downloads lower in the page or
  inside expanders.

### Change Set 5: Project Plan Simplification

- Lead with current phase and next three actions.
- Use a visual built-now/activate-later split.
- Keep the full workstream table as an optional detail.
- Add the eight-slide deliverable status.

## Acceptance Criteria

- Four or fewer sidebar choices.
- Three or fewer tabs per page.
- Overview contains six or fewer main visual sections.
- A first-time viewer can identify the project goal, workflow, current state,
  and next action without opening an expander.
- No overview paragraph exceeds 35 words.
- No horizontal overflow at 390-pixel viewport width.
- Every overview visual has a PowerPoint/Word reuse path.
- Existing scientific rules, data boundary, downloads, and source provenance
  remain accessible after consolidation.
