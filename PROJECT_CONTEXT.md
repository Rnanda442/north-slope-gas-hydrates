# North Slope Gas Hydrates Project Context

Last updated: 2026-06-12

## Purpose

This file is the living project memory for people and agents working in this
repository. Read it before starting work and update it after meaningful changes.
The detailed architecture, workstream status, dependencies, and next activities
live in `docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md`.

## Project Goal

Build a scientifically defensible North Slope gas-hydrate research workflow that
connects public regional GIS context with an authorized, runtime-only well-log
and core-analysis system. The immediate goal is to finish the well-log
scaffolding using the user's Excel-based design as a visual and functional
reference.

The intended analysis chain is:

```text
regional geology and stability context
-> approved LAS/CSV/core inputs
-> schema mapping and quality control
-> standardized well-log and core tables
-> manuscript-backed feature engineering
-> core-log calibration
-> interval screening and classification
-> uncertainty-aware plots, tables, GIS links, and manuscript exports
```

## Current Focus

Use the recovered normalized Excel header screenshots to define the canonical
well-log schema, unit conversions, curve roles, track groups, and target-leakage
guardrails. Continue recovering the workbook and formulas before changing
scientific calculations.

## Current State

- The public Streamlit regional atlas is implemented.
- The website now uses a four-page, visual-first Streamlit structure with
  Processing-style public/synthetic canvas sketches.
- The synthetic well-log planning page and reusable calculation layer are
  implemented in `dashboard/well_log_engine.py`.
- The authorized runtime skeleton is implemented in `dashboard/runtime/`.
- Tests exist in `tests/test_well_log_engine.py` and
  `tests/test_runtime_skeleton.py`.
- The full project test suite passed on 2026-06-12: 23 tests passed.
- Public GIS layers, notebooks, structural surfaces, and Plotly exports are
  present.
- Two working Word drafts and a new research-overview Word/PPT deliverable pair
  are present in `docs/project_blueprints/`.
- The current presentation baseline is the public-safe Gmail visual-feedback
  9-slide revision imported to Drive as `GMAIL VISUAL REVISION 9-SLIDE North
  Slope Gas Hydrate Slides 2026-06-11`; it applies the latest Gmail
  instructions with user-provided about-me visuals, the current Streamlit
  structural explorer, gas-hydrate stability visuals, parameter symbols, a
  shared-gate ML architecture, behavior panels, geomechanics, results visuals,
  and conclusion graphics. The current Drive deck preserves these
  Processing-style revisions as full-slide raster panels.
- The latest Gmail ML sources were recovered into
  `references/ml-sources/2026-06-11/` and used to enrich the local Word/PPTX
  builders with Chong et al. ANN workflow specifics, leakage-safe
  preprocessing, model validation, data-quality, calibration, residual, and
  drift-review controls while preserving the 9-slide deck count.
- The enriched local DOCX/PPTX were imported to the connected Google Drive
  account as native Google Docs/Slides files:
  `ENRICHED ML PIPELINE North Slope Gas Hydrate Research Overview 2026-06-11`
  and `ENRICHED 9-SLIDE ML PIPELINE North Slope Gas Hydrate Slides
  2026-06-11`.
- The public source-library index is present in `docs/source_library_index/`.
- Three Excel header references were reviewed from the user's email. The images
  are not stored in Git or shown on the website; their public-safe schema
  derivative is maintained in `docs/WELL_LOG_REQUIREMENTS_MAP.md`.
- No real well-log rows, core rows, or calibrated target values were supplied
  from those Excel references. Website and test rows are header-derived
  synthetic examples generated only to exercise layout, validation, and visuals.
- The user confirmed that NMR and all fields listed in the recovered screenshots
  are available for the future approved-data workflow.
- The user's full Excel workbook has not yet been recovered into this official
  folder.
- The open-source PowerPoint scaffold was recovered from Gmail into
  `docs/project_blueprints/Alaska_North_Slope_Wireline_ML_Presentation_Scaffold_outline.pptx`.
- The June 6 source migration targeted a local fake-Drive folder and did not
  upload the source library: 211 of 212 files were missing and 1 was blocked.
- Several supporting research documents were found on the connected Google
  Drive, but the connected account does not currently expose the named North
  Slope PowerPoint or source-library folder. See
  `docs/source_recovery_status.md`.
- The working tree was recovered on 2026-06-07 from a prior Codex session
  archive.
- This official folder is connected to
  `https://github.com/Rnanda442/north-slope-gas-hydrates.git`; local `main` and
  `origin/main` were synchronized on 2026-06-08.

## Website

Primary entry point: `streamlit_app.py`

Main application: `dashboard/app.py`

Hosted deployment:
`https://north-slope-gas-hydrates-vj67xkke9ksfzveon8ldt2.streamlit.app/`

As checked on 2026-06-08, the deployment is public and anonymous visitors can
open it without Streamlit sign-in.

Current public views:

- Overview
- Explore North Slope
- Analyze Hydrates
- Project Plan

Legacy query links for the prior eight-page structure route into the four
current pages.

The hosted website must remain a public-source atlas and synthetic demonstration.
It must not load or expose authorized well-log or core data.

## Scientific Rules

1. Gas-hydrate stability is necessary but not sufficient for hydrate presence.
2. Hydrate occurrence, saturation, reservoir quality, and producibility are
   separate outputs.
3. High resistivity alone is not a defensible hydrate label.
4. Classification should use multiple logs plus geological context.
5. Core calibration adjusts confidence and should not silently overwrite logs.
6. Future model validation must split by well, not by random depth rows.
7. GIS context constrains and visualizes interpretation; it does not replace
   direct log or core evidence.

## Authoritative Project Files

- `README.md`: repository and website orientation
- `docs/project_inventory.md`: current asset inventory and engineering stages
- `docs/runtime_skeleton_brief.md`: runtime package design and scientific rules
- `docs/opensciencelab_runtime_layout.md`: authorized-data folder boundary
- `docs/data_dictionary.md`: public atlas layer definitions
- `docs/project_blueprints/Alaska_North_Slope_Wireline_ML_Classification_Methods_Draft.docx`:
  primary working methods direction
- `docs/project_blueprints/Alaska_North_Slope_Wireline_ML_Research_Paper_Draft.docx`:
  broader manuscript and source synthesis
- `docs/source_library_index/source_index.md`: source orientation
- `docs/source_library_index/source_manifest.csv`: source inventory
- `docs/source_recovery_status.md`: Drive search results, original paths, and
  recovery checklist
- `docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md`: authoritative architecture,
  priorities, workstream status, blockers, and next-work sequence
- `docs/PROJECT_IMPROVEMENT_STRATEGY.md`: principles and phased improvement
  strategy for keeping product changes aligned with the scientific goal
- `docs/PROJECT_VISION_GOALS_AND_NEXT_STEPS.md`: email-derived project vision,
  deliverable priority, expected inputs, ML direction, and ordered next steps
- `docs/EIGHT_SLIDE_PRESENTATION_SPEC.md`: source-backed visual structure for
  reducing the recovered 12-slide scaffold to the requested eight-slide deck
- `docs/WEBSITE_VISUAL_REDESIGN_PLAN.md`: approved pre-implementation plan for
  reducing navigation, rebuilding the overview, and specifying each visual
- `docs/ML_VISUAL_ARCHITECTURE_PLAN.md`: source-backed plan for ML knowledge
  graph, hydrate decision tree, target-leakage barrier, and validation visuals
- `docs/ML_PARAMETER_TREE_AND_DECK_REVAMP_PLAN.md`: user-approved revamp plan
  for parameter signal visuals, masking trees, ML architecture, and deck order
- `docs/NINE_SLIDE_POWERPOINT_REVISION_WORKFLOW.md`: specific correction
  workflow for the final 9-slide Drive deck revision
- `docs/WELL_LOG_REQUIREMENTS_MAP.md`: screenshot-derived header schema,
  scaffold requirements, track groups, and unresolved questions
- `docs/SWEET_SPOT_SCIENCE_BASIS.md`: research-backed directional relationships,
  synthetic implementation logic, and calibration requirements
- `docs/SWEET_SPOT_SOURCE_MATRIX.md`: primary evidence, source tiers, indexed
  library coverage, and provenance rules for the sweet-spot scaffold

## Source Intake

Place public or synthetic design references in `references/` using descriptive
names. Spreadsheet screenshots belong in `references/well-log-spreadsheet/`.

For each screenshot or workbook, record:

- original filename and date
- sheet or screen represented
- visible columns, units, formulas, and chart tracks
- whether values are public, synthetic, or restricted
- intended dashboard or runtime behavior
- unresolved questions

Restricted or approved-environment-only data must not be copied into this
repository. Record only a non-sensitive description and keep the actual file in
the authorized runtime environment.

## Next Actions

The current ordered plan is maintained in
`docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md`.

## Update Protocol

Keep this file concise and factual. Maintain detailed status, dependencies,
blockers, and next activities in the architecture/activity map.

## Decision Log

- 2026-06-07: This folder was designated the official project folder.
- 2026-06-07: `PROJECT_CONTEXT.md` is the canonical living project memory.
- 2026-06-07: The classification-methods Word draft is the primary manuscript
  direction; the broader research-paper draft is supporting context.
- 2026-06-07: The public website remains synthetic/public-source only, while
  approved well-log and core inputs remain runtime-only.

## Change Log

- 2026-06-07: Recovered the project working tree from the June 6 Codex archive.
- 2026-06-07: Added agent instructions, project context, and source-intake
  guidance.
- 2026-06-07: Verified the recovered well-log and runtime scaffold with 8 passing
  tests.
- 2026-06-07: Searched the connected Google Drive and documented that the June 6
  migration was a failed local test rather than a real Drive upload.
- 2026-06-08: Added the project architecture and activity map as the
  authoritative next-work tracker.
- 2026-06-08: Published the architecture/activity map inside Streamlit and added
  responsive phone-width styling.
- 2026-06-08: Recorded the hosted Streamlit URL and found that its initial
  sharing state required sign-in.
- 2026-06-08: Verified the official folder's Git remote and history are
  synchronized, and improved the roadmap's phone-width workstream view.
- 2026-06-08: Changed the hosted Streamlit deployment to public access and
  verified that an anonymous request reaches the app without an access-denied
  response.
- 2026-06-08: Established a phased improvement strategy centered on guided
  scientific communication, requirements traceability, runtime readiness, and
  decision-quality outputs.
- 2026-06-08: Reviewed three Excel header references and created the initial
  well-log requirements map without using any values as real sample data.
- 2026-06-08: Removed the screenshot binaries from Git, reviewed connected Drive
  research, and added an explainable synthetic sweet-spot evidence model.
- 2026-06-08: Added a dedicated North Slope Sweet Spots page with synthetic
  interval ranking, all current input-variable roles, geomechanics, competing
  explanations, uncertainty, and research-backed decision logic.
- 2026-06-08: Corrected the sweet-spot provenance model to distinguish ten
  primary public references, 28 indexed artifacts, and the four-document Drive
  review subset.
- 2026-06-08: Integrated the project-direction emails and Chong et al. (2022)
  into a tracked vision/next-steps document and recovered the PowerPoint
  scaffold from Gmail.
- 2026-06-08: Implemented source-driven Runtime Readiness, target contracts,
  caliper washout QC, complete-well split planning, and an eight-slide
  presentation specification.
- 2026-06-08: Defined the website redesign plan before implementation, including
  four-page navigation, low-text overview visuals, generation prompts, and
  staged acceptance criteria.
- 2026-06-08: Recorded the initial working ML cohort assumptions:
  approximately 71 wells, approximately 20% known wells for development, 80%
  prediction wells, and separate classification and saturation outputs.
- 2026-06-09: Updated the deliverable assumptions after the user confirmed NMR
  and all screenshot-listed fields are available, and created a new
  research-overview Word document plus eight-slide PowerPoint.
- 2026-06-09: Revised the Word/PPT deliverables from the user's emailed
  instructions: filled only the abstract and introduction, converted the Word
  file to a section-outline format with process sketches, and changed the deck
  to a nine-slide structure with about-me, parameter, ML, map/results, and
  conclusion slides.
- 2026-06-09: Upgraded the nine-slide deck with embedded project visuals from
  the website/scaffold, including a 3D regional context image, synthetic
  well-log panel, ML validation placeholder, and sweet-spot ranking graphic.
- 2026-06-09: Strengthened the live Google Slides deck and reproducible PPTX
  with Chong et al. ANN architecture context, classification/regression
  branches, target-leakage guardrails, complete-well validation, and the current
  Streamlit Structural Explorer 3D map asset plus live-app link.
- 2026-06-09: Re-exposed the website well-log scaffold as a first-class
  `Log Scaffold` page, kept the old `Future Well-Log Engine` query alias, and
  added a visible welcome-page link.
- 2026-06-10: Implemented the Processing-style website redesign with four
  top-level pages, visual-first canvas sketches, route aliases for old page
  links, and browser QA at desktop and 390-pixel mobile widths.
- 2026-06-10: Clarified that the Excel material provides header/schema
  information only; synthetic website/test rows are generated from those headers
  and source logic, not from user-supplied sample data.
- 2026-06-10: Rebuilt the research-overview Word document and nine-slide
  PowerPoint with the four-page website workflow, source anchors, subsurface
  evidence stack, and header-derived synthetic-data provenance.
- 2026-06-10: Recovered the user's updated Gmail-sent DOE Word document and
  PowerPoint, then reintegrated the tracked deliverables from those copies with
  the latest website visuals and header-derived synthetic-data boundary.
- 2026-06-10: Added ML visual architecture planning and implemented Processing-style
  website sketches for a header-to-model knowledge graph and staged hydrate
  interpretation decision tree.
- 2026-06-10: Incorporated the user's new revamp instructions: prioritize the
  Word/PPT deliverables, create parameter signal/masking trees before deck
  rebuild, use a hybrid dark/clean visual style, and treat classification and
  saturation regression as parallel branches.
- 2026-06-10: Rebuilt the latest Drive PowerPoint into a public-safe 12-slide
  visual ML architecture deck for Drive review.
- 2026-06-11: Corrected the Drive deck into a verified final 9-slide native
  Google Slides revision with the profile photo restored, slide 4 rebuilt as a
  measurement/caveat/model-role grid, named ML feature equations, detailed ML
  workflow/error slides, and public-source/runtime-boundary language.
- 2026-06-11: Restored the older nine-slide topic sequence for the Drive deck
  while preserving the newer visual style, profile photo, parameter caveats,
  equation-connected ML workflow, complete-well validation, and public-safe
  source boundary.
- 2026-06-11: Folded the Classification Methods Draft into the verified
  nine-slide Drive deck by strengthening the ML workflow gates, model ladder,
  well/compartment validation split, probability calibration, reason-code
  outputs, and results/discussion review flags.
- 2026-06-11: Recovered the user's latest Gmail ML sources into
  `references/ml-sources/2026-06-11/`, documented their public-safe intake, and
  enriched the local Word/PPTX builders with gas-hydrate-specific ANN workflow
  details plus general ML pipeline quality controls.
- 2026-06-11: Imported the enriched local Word and PowerPoint deliverables to
  Google Drive as native Google Docs/Slides files in the connected account and
  verified the Slides deck readback has exactly nine slides.
- 2026-06-11: Executed the all-nine-slide visual revision package, rebuilt the
  local PPTX with current Streamlit, gas-hydrate, well-log, parameter-icon,
  architecture, behavior, geomechanics, results, and conclusion visuals,
  imported it as a native Google Slides deck named `FINAL VISUAL REVISION
  9-SLIDE North Slope Gas Hydrate Slides 2026-06-11`, and verified 9-slide
  Drive readback plus Google-rendered thumbnails.
- 2026-06-12: Processed the user's latest Gmail visual-feedback instructions,
  generated source-backed Processing-style panels for all nine slides, rebuilt
  the local PPTX, imported it to the connected Google Drive as `GMAIL VISUAL
  REVISION 9-SLIDE North Slope Gas Hydrate Slides 2026-06-11`, verified native
  Slides metadata/readback and all nine Google-rendered thumbnails, and
  confirmed 23 project tests pass.
