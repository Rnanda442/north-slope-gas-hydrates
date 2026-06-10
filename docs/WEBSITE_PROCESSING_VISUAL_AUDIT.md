# North Slope Website Processing Visual Audit

Last updated: 2026-06-10

Implementation status: implemented in `dashboard/app.py`,
`dashboard/processing_visuals.py`, and `dashboard/visual_story_data.py` on
2026-06-10. The document remains as the design/audit record for future polish.

## Purpose

This is the pre-implementation inventory for making the North Slope website use
many fewer words and many more interactive visuals built in the Processing
style. For the web implementation, "Processing" should mean p5.js-style canvas
sketches embedded in Streamlit with `components.html`, backed only by public or
synthetic data.

This document does not authorize loading approved runtime data into the public
site. The public website remains a public-source atlas and synthetic
demonstration.

## Local Review Basis

Reviewed locally at `http://localhost:8503/?page=...` from the current
`dashboard/app.py` Streamlit app.

Current navigation has eight pages:

- `Welcome`
- `Project Roadmap`
- `North Slope Sweet Spots`
- `Log Scaffold`
- `Regional Atlas`
- `Structural Explorer`
- `Data Library`
- `Research Framework`

The existing approved redesign direction in
`docs/WEBSITE_VISUAL_REDESIGN_PLAN.md` reduces this to four pages:

- `Overview`
- `Explore North Slope`
- `Analyze Hydrates`
- `Project Plan`

## Current Site Pattern

The current site is scientifically useful but reads like a documentation portal.
Most pages lead with explanatory text, metrics, tables, warnings, or tabs before
the strongest visual appears.

Existing visual assets worth retaining:

- regional Plotly/HTML map iframe on `Regional Atlas`;
- generated Plotly 3D structural view on `Structural Explorer`;
- synthetic interval ranking and evidence-profile charts on
  `North Slope Sweet Spots`;
- synthetic well-log panel and placeholder model figures on `Log Scaffold`;
- source-backed tables that should remain available as drill-down evidence.

Current structural problems:

- sidebar exposes eight choices before the user understands the story;
- overview has no real project visual;
- `Log Scaffold` has nine tabs and reads like a technical appendix;
- roadmap and framework pages are mostly prose and tables;
- warnings are necessary but visually dominate several pages;
- visual language is mixed: Streamlit metrics, Plotly figures, HTML iframes,
  dataframes, markdown cards, and almost no intentional icon/canvas system.

## Page Inventory and Target Format

| Current page | Current format seen on site | Main issue | Target page | Target Processing/p5.js visual |
|---|---|---|---|---|
| `Welcome` | Hero text block, four Streamlit metrics, four text cards, data-boundary paragraph | No project visual; first impression is words and counts | `Overview` | Full-width animated system sketch: North Slope map outline -> well-log column -> interval decision panel |
| `Project Roadmap` | Long markdown-derived plan, metrics, five tables, many headings | Too much project management text for public first read | `Project Plan` | Built-now / activate-next board with animated connectors and status colors |
| `North Slope Sweet Spots` | Metrics, ranked dataframe, selected interval metrics, Plotly evidence bar, four tabs, source tables | Good decision logic but table-first and text-heavy | `Analyze Hydrates` | Interactive interval decision board: depth column, evidence rings, uncertainty flags, and rank lane |
| `Log Scaffold` | Three text cards, eight rules, nine tabs, 26 tables, many warnings, Plotly log panels | Most important workflow is buried; too many tabs | `Analyze Hydrates` | Processing well-log sketch: synchronized tracks, highlighted interval, live evidence glyphs, QC badges |
| `Regional Atlas` | Three metrics, short guidance text, embedded regional HTML map iframe | Existing map is valuable but not integrated into a story | `Explore North Slope` | Processing layer-map overview with simplified public layers and click-to-focus cards; keep full Plotly map below |
| `Structural Explorer` | Controls first, Plotly 3D view, layer-label table, fallback expander | Strong visual exists but starts with controls and prose | `Explore North Slope` | Processing/Three-like structure preview: rotating layered surfaces, wells, and boundary overlays; keep Plotly control view |
| `Data Library` | Layer dataframe, repository browser, quality warning | Correct as evidence appendix, not top-level story | `Explore North Slope` | Compact source coverage matrix: layer tiles, public/restricted boundary, geometry completeness meter |
| `Research Framework` | Stage cards and numbered decision rules | Important rules are word-heavy and isolated from visuals | `Overview` and `Project Plan` | Four-level evidence stack sketch: regional context, stability/reservoir, logs/core, decision/uncertainty |

## Target Four-Page Experience

### 1. Overview

Primary question: what is this project and how does evidence become a decision?

Use four visible sections only:

1. animated system hero;
2. three outcome icons: detect, quantify, rank;
3. data-to-decision pipeline;
4. choose-a-path cards.

Move detailed counts, repository footprint, and long data-boundary wording out
of the first viewport. Keep the boundary as a compact badge plus an expandable
detail.

Processing sketches:

- `system_flow_sketch`: map dots pulse into well-log tracks, then into four
  outcome blocks;
- `mission_icons_sketch`: three simple line icons with hover states;
- `pipeline_sketch`: six nodes with animated routing through ready, partial,
  and blocked states.

### 2. Explore North Slope

Primary question: what public regional data constrains the problem?

Tabs should be limited to:

- `Regional Map`
- `3D Structure`
- `Data & Sources`

Processing sketches:

- `north_slope_layer_sketch`: simplified map with assessment units, seismic
  coverage, well dots, and missing-geometry count;
- `structure_stack_sketch`: lightweight layered surface preview with toggles for
  public horizons;
- `source_boundary_sketch`: public-source layer tiles on one side, authorized
  runtime-only inputs on the other side.

Keep the existing Plotly map and structural explorer as deeper interactive
tools, but the page should lead with the simplified visual story.

### 3. Analyze Hydrates

Primary question: how do logs and core become hydrate, saturation, uncertainty,
and sweet-spot decisions?

Tabs should be limited to:

- `Interval Review`
- `Runtime Readiness`
- `Methods & Evidence`

Processing sketches:

- `well_log_tracks_sketch`: depth-aligned tracks for GR, Rt, RHOB, Vp, Vs, NMR
  where available, with highlighted interval bands;
- `evidence_radar_sketch`: reservoir, hydrate evidence, saturation proxy, flow,
  QC, and stability as interpretable glyphs;
- `target_boundary_sketch`: measured inputs, derived features, targets, and
  forbidden leakage paths shown visually;
- `cohort_split_sketch`: known wells, validation wells, locked test wells, and
  prediction wells as whole-well blocks.

Keep full tables and downloads inside expanders below the visual. Default view
should show one synthetic well/interval story without needing to open nine tabs.

### 4. Project Plan

Primary question: what is built, blocked, and next?

Use a visual status board first, then optional details.

Processing sketches:

- `built_next_sketch`: left side built-now modules, right side approved-data
  activation modules, connected by thin arrows;
- `blocker_sketch`: blockers as amber/red cards connected to the workstream they
  affect;
- `deliverable_sketch`: Word, PowerPoint, website figures, and future approved
  results as output blocks.

Keep the full architecture map and tables available under "Detailed tracker".

## Visual Conversion Rules

1. Replace introductory paragraphs with a visual plus one sentence.
2. Replace metric rows with visual counters only when the count changes the
   viewer's decision.
3. Replace roadmap tables with status boards; keep the tables as optional
   evidence.
4. Replace long rule lists with interactive evidence diagrams.
5. Use canvas visuals for story and flow; use Plotly where scientific axes and
   precise inspection matter.
6. Every visual must have a static export path for PowerPoint and Word.
7. p5.js sketches must use synthetic/public data constants, not runtime folders.
8. Accessibility text must summarize what the canvas shows because canvas text is
   not enough for screen readers.

## Suggested Implementation Shape

Add a small visual layer rather than scattering raw HTML strings across page
functions:

- `dashboard/processing_visuals.py`: helpers that render p5.js sketches through
  `components.html`;
- `dashboard/visual_story_data.py`: public/synthetic constants used by sketches;
- `dashboard/static/processing/`: optional standalone sketch templates if the
  inline component becomes too large;
- tests that assert the four-page aliases render and old page links still
  redirect to their owning page.

Each sketch should expose:

- title;
- short accessibility summary;
- fixed public/synthetic data payload;
- responsive width and height;
- static export strategy.

## Migration Order

1. Collapse navigation to four pages with route aliases for old links.
2. Build the Overview hero and pipeline sketches.
3. Consolidate `Regional Atlas`, `Structural Explorer`, and `Data Library` into
   `Explore North Slope`.
4. Consolidate `North Slope Sweet Spots` and `Log Scaffold` into
   `Analyze Hydrates`.
5. Rebuild `Project Roadmap` and `Research Framework` into `Project Plan`.
6. Run browser QA at desktop and 390-pixel mobile widths.

## Acceptance Checklist

- Sidebar has four top-level choices.
- No first-viewport page depends on a dataframe for meaning.
- Overview has at least three canvas/SVG visual sections and no long prose block.
- `Analyze Hydrates` starts with a well-log/evidence visual, not a table.
- `Explore North Slope` starts with a map/layer visual, not metrics.
- `Project Plan` starts with status visuals, not markdown tables.
- No page has more than three tabs.
- All detailed tables remain available but are below the main visual story.
- Public-source versus authorized-runtime boundary remains visible.
- No authorized well logs, core data, named restricted identifiers, derived
  sensitive outputs, populated runtime configs, or trained models are loaded.
