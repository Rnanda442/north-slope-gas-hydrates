# North Slope Gas Hydrates Project Context

Last updated: 2026-06-15

## Purpose

This file is the living project memory for people and agents working in this
repository. Read it before starting work and update it after meaningful changes.
The detailed architecture, workstream status, dependencies, and next activities
live in `docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md`.

## Project Goal

Build a scientifically defensible North Slope gas-hydrate research workflow that
connects public regional GIS context with an authorized, runtime-only well-log
and core-analysis system. The immediate coordination goal is to review and lock
the shared Word/PowerPoint/website direction in
`docs/PROJECT_DIRECTION_LOCK_FOR_REVIEW.md` before the next major deliverable
edit.

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

Use `docs/PROJECT_DIRECTION_LOCK_FOR_REVIEW.md` and
`docs/SCIENCE_TO_ML_LOGIC_LADDER.md` as the review base for the next work
session. Use `docs/ML_PIPELINE_BASELINE_SOURCE_LEDGER.md` as the working
decision ledger for pipeline options, source-backed reasons, screening ranges,
model choices, guardrails, validation, and output design. The current local
Word/PPT pass explains the DOE workflow as a science-to-ML ladder: define the
North Slope pore-filling sand-hydrate system, separate hydrate habits, move
through stability context, reservoir quality, and hydrate response, then
explain leakage-safe occurrence classification and saturation regression.
Continue recovering the full workbook, source range docs, and formulas before
changing scientific calculations or claiming model results.
For the stability-screen communication pass, use
`docs/MENTOR_STATUS_UPDATE_DRAFT.md`,
`docs/WEEKDAY_PROGRESS_REPORT_TEMPLATE.md`, and
`docs/DELIVERABLE_REFRESH_PLAN_STABILITY_AND_ML.md` to keep the
OpenScienceLab workbench, public GitHub/Streamlit delivery surface, and
stability-admissibility guardrail aligned. The local 2026-06-15 slide-remake
draft preserves the current Gmail deck's first two slides and rebuilds slides
3-9 around the public/OSL workflow, guarded stability screen, readiness labels,
and later approved-data ML path. The 2026-06-15 pipeline status Word brief is
the current plain-language review draft for explaining where the project stands
now and how the approved-data ML pipeline should reach occurrence
classification and saturation regression.

## Current State

- The public Streamlit regional atlas is implemented.
- The website now uses a four-page, visual-first Streamlit structure with
  Processing-style public/synthetic canvas sketches.
- The synthetic well-log planning page and reusable calculation layer are
  implemented in `dashboard/well_log_engine.py`.
- The authorized runtime skeleton is implemented in `dashboard/runtime/`.
- OpenScienceLab is the intended heavy-data workbench for approved inputs and
  guarded runtime calculations; GitHub/Streamlit remains the public delivery
  surface for source-backed documentation, public GIS, and synthetic/public
  scaffold views.
- Tests exist in `tests/test_well_log_engine.py` and
  `tests/test_runtime_skeleton.py`.
- The full project test suite passed on 2026-06-12: 23 tests passed.
- Public GIS layers, notebooks, structural surfaces, and Plotly exports are
  present.
- Two working Word drafts and a rebuilt 2026-06-13 local research-overview
  Word/PPT deliverable pair are present in `docs/project_blueprints/`.
- The current local presentation baseline is the public-safe 2026-06-13
  science-to-ML 9-slide revision rebuilt from
  `docs/project_blueprints/build_ml_revamp_powerpoint.py`; it keeps the
  full-slide raster-panel format but reframes the deck around the hydrate
  system, parameter movement patterns, screening envelopes, leakage-safe
  targets, occurrence classification, saturation regression, and calibrated
  validation.
- The 2026-06-13 science-to-ML local DOCX/PPTX rebuild was imported to the
  connected Google Drive account as native files:
  [SCIENCE-TO-ML North Slope Gas Hydrate Research Overview 2026-06-13](https://docs.google.com/document/d/1Ft0wgKV3p8HK1F7X4_WYVAp1jOtBYuCntdRP-Z84e5k)
  and
  [SCIENCE-TO-ML 9-SLIDE North Slope Gas Hydrate Slides 2026-06-13](https://docs.google.com/presentation/d/1GztudvOcJnZh28lAflNp6ZH2fMPhRgtTJgXX9ufPW24).
- The latest Gmail ML sources were recovered into
  `references/ml-sources/2026-06-11/` and used to enrich the local Word/PPTX
  builders with Chong et al. ANN workflow specifics, leakage-safe
  preprocessing, model validation, data-quality, calibration, residual, and
  drift-review controls while preserving the 9-slide deck count.
- A follow-up hydrate ML and physics source intake is present in
  `references/hydrate-ml-physics-sources/2026-06-13/`. It adds locally
  verified OSTI PDFs for Singh et al. (2021) and Chong et al. (2024), official
  source-page backups for Lee and Collett (2011), Cook and Waite (2018), and
  Chong et al. (2024), Google Drive PDF source references for five
  user-uploaded papers, and a manifest of papers that still require
  user-provided or legitimate institutional PDFs.
- The enriched local DOCX/PPTX were imported to the connected Google Drive
  account as native Google Docs/Slides files:
  `ENRICHED ML PIPELINE North Slope Gas Hydrate Research Overview 2026-06-11`
  and `ENRICHED 9-SLIDE ML PIPELINE North Slope Gas Hydrate Slides
  2026-06-11`.
- The public source-library index is present in `docs/source_library_index/`.
- The 2026-06-13 stability source bundle is documented, locally uploaded in
  OpenScienceLab under `data/source_library/`, and connected to the Structural
  Explorer through `dashboard/stability_sources.py`. The app now also falls
  back to the committed public snapshot under
  `data/public_stability_snapshot/north_slope_stability_snapshot_2026-06-13/`
  so hosted/browser views can still show GGD223 permafrost controls and USGS
  hydrate assessment units when the full local bundle is unavailable. A derived
  public well-context product is also present under
  `data/public_stability_products/`, joining Arctic Slope public wells to
  nearest GGD223 controls and USGS hydrate AU membership for screening context
  only. The same product folder includes a compact G10015 temperature-profile
  inventory for geothermal context; it summarizes public logs and rough
  deepest-window gradients without committing raw profile rows. A stability
  input scaffold now combines public well depth, nearest permafrost control,
  matched G10015 context where available, and provisional hydrostatic pressure,
  but keeps phase-curve and top/base/thickness results explicitly uncalculated.
- `docs/STABILITY_CALCULATION_PLAN.md` now locks the source-backed plan for the
  stability screen: hydrostatic pressure equation, G10015/GGD223
  temperature-model hierarchy, methane 5 ppt phase-curve lookup source,
  source-control confidence labels, caveats, and the
  `stability_screen_*.csv` output schema.
- `data/public_stability_products/phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1.csv`
  is now the first cited phase-curve lookup input, digitized from USGS SIR
  2008-5175 Figure 1A for methane and 5 ppt salt water. Pressure helper tests
  now distinguish gauge and absolute hydrostatic pressure, and phase-curve
  interpolation tests preserve the guardrail that final stability
  top/base/thickness remain uncalculated.
- `data/public_stability_products/phase_curve_scenario_catalog_2026-06-14.csv`
  now makes the phase-curve system variable-capable while keeping the mentor-
  approved 100 percent methane curve as the official public baseline. The
  Collett et al. (2011) / Holder et al. (1987) mixed-gas curve is recorded as a
  sensitivity candidate only until it is digitized or regenerated from a cited
  thermodynamic model.
- `data/public_stability_products/stability_input_capability_matrix_2026-06-14.csv`
  now records what current public inputs can support, what remains
  scenario-only, and what must wait for approved runtime data before any
  stability or ML claim is made.
- `data/public_stability_products/stability_osl_pull_triggers_2026-06-14.csv`
  records when the public repo is enough versus when the full OSL/source bundle
  is needed. Real public temperature-model products require OSL because raw
  G10015 profile rows are not committed to Git.
- Local fixture-based temperature-model helpers now exist in
  `dashboard/stability_products.py`. They parse G10015-style depth/temperature
  rows, interpolate within measured profile depth, extrapolate below the deepest
  measured point only when a numeric gradient is supplied, and return blocked
  statuses for missing depth, missing profiles, above-range depths, or
  below-profile depths without a gradient. They do not calculate stability
  top/base/thickness.
- Local fixture-based stability depth-grid and intersection helpers now exist.
  They combine modeled temperature, absolute hydrostatic pressure, and the
  phase lookup into per-depth stability flags, test synthetic top/base
  crossings and open-base cases, and block incomplete pressure-temperature
  grids. They now support the OSL-derived guarded public
  `stability_screen_*.csv`.
- Local source-control confidence-label helpers now exist for fixture rows.
  Tests cover high, medium, low, blocked, and outside-AU labels, but these are
  source-control labels only and do not imply hydrate occurrence, saturation,
  producibility, or sweet spots.
- The public stability rebuild pipeline is now ready for the OSL step. When it
  runs with the full source bundle and raw G10015 profile `.txt` files present,
  it writes a compact temperature-model product at key scaffold depths while
  keeping final stability top/base/thickness uncalculated.
- The G10015 parser now collapses duplicate depth rows by averaging
  `temperature_c`, fixing the OSL inventory failure triggered by duplicate
  depth `8.23` in `usgs_put-25-5fnandahora442.txt`.
- A guarded baseline stability-screen writer now exists and has been run in
  OSL. It requires raw G10015 profile rows, applies the cited methane 5 ppt
  phase lookup, leaves blocked rows null, and keeps every row tagged
  `not_hydrate_proof`.
- The first OSL screen run produced all blocked rows because the screen grid
  demanded phase-curve coverage from `0 m`. The writer now starts at the phase
  lookup's minimum covered depth and blocks only where the interval cannot close
  within the lookup's maximum covered depth. The committed rerun produced
  `8,084` screen rows, `22` calculated intervals, `8` no-stable-interval rows,
  and `8,054` blocked rows.
- `data/public_stability_products/stability_website_product_spec_2026-06-14.csv`
  defines the target public website shape for the stability screen:
  status strip, readiness/capability, map, selected-well audit panel,
  temperature-phase plot, results table, scenario controls, and exports.
- The Structural Explorer now displays the guarded baseline methane 5 ppt
  stability screen with summary counts, status/confidence breakdowns,
  calculated interval rows, blocked/no-interval sample rows, and a CSV download
  while preserving the no-proof caveat.
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
- `docs/STABILITY_CALCULATION_PLAN.md`: source-backed pressure-temperature
  stability-screen plan and `stability_screen_*.csv` schema
- `docs/source_recovery_status.md`: Drive search results, original paths, and
  recovery checklist
- `docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md`: authoritative architecture,
  priorities, workstream status, blockers, and next-work sequence
- `docs/PROJECT_DIRECTION_LOCK_FOR_REVIEW.md`: reviewable shared direction for
  the Word document, nine-slide deck, website/app skeleton, scientific rules,
  ML rules, open decisions, and acceptance criteria before the next major edit
- `docs/SCIENCE_TO_ML_LOGIC_LADDER.md`: hydrate-system-first narrative,
  parameter tiers, screening-envelope ranges, equations, and ML pipeline spine
  for the next Word/PPT pass
- `docs/ML_PIPELINE_BASELINE_SOURCE_LEDGER.md`: source-backed decision ledger
  for baseline ML pipeline options, parameter movement patterns, screening
  envelopes, target leakage, guardrails, model choices, validation, and outputs
- `docs/MENTOR_STATUS_UPDATE_DRAFT.md`: public-safe mentor status language and
  future decision questions for the stability-screen phase
- `docs/WEEKDAY_PROGRESS_REPORT_TEMPLATE.md`: short mentor-facing weekday
  update template
- `docs/DELIVERABLE_REFRESH_PLAN_STABILITY_AND_ML.md`: planned Word and
  nine-slide deck refresh diagrams for the stability and future ML workflow
- `docs/PIPELINE_STATUS_AND_ML_WORKFLOW_BRIEF.md`: Word-ready status and
  forward workflow narrative for the current project position, stability
  guardrail, source-backed evidence tiers, and future approved-data ML pipeline
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
- 2026-06-12: Added `docs/PROJECT_DIRECTION_LOCK_FOR_REVIEW.md` as the
  reviewable goal lock before further Word, PowerPoint, or website edits.
- 2026-06-13: Added the OpenScienceLab stability source-bundle loader and
  Structural Explorer source-status/map panel for GGD223 permafrost controls and
  USGS gas hydrate assessment units.
- 2026-06-14: Added the source-backed stability calculation plan for the public
  stability-screen workflow before committing guarded screen outputs.
- 2026-06-13: Added `docs/SCIENCE_TO_ML_LOGIC_LADDER.md` and wired it into the
  deliverable revision base so the next Word/PPT pass uses a hydrate-system,
  parameter-tier, screening-envelope, and leakage-safe ML narrative instead of
  a flat parameter list.
- 2026-06-13: Added the hydrate ML and physics source intake folder with two
  downloaded OSTI PDFs, official source-page backups, and a retrieval manifest
  listing the remaining papers that need user-provided or institutional access.
- 2026-06-13: Recorded the five user-uploaded Google Drive source PDFs:
  Aung et al. (2026), Yoneda et al. (2026), Tian et al. (2023), Li and Liu
  (2020), and Naim et al. (2023), with source roles and guardrails in the June
  13 hydrate ML/physics source intake.
- 2026-06-13: Added `docs/ML_PIPELINE_BASELINE_SOURCE_LEDGER.md` to preserve
  the source-backed baseline pipeline decisions, option tradeoffs, parameter
  movement patterns, screening envelopes, guardrails, model ladder, validation
  rules, and Word-document implications before rebuilding deliverables.
- 2026-06-13: Rebuilt the local research-overview DOCX and 9-slide PPTX from
  the science-to-ML ladder and baseline source ledger, without claiming model
  results or importing a new Drive copy.
- 2026-06-13: Imported the science-to-ML rebuild to Google Drive as native
  Docs/Slides files and verified Google connector readback plus all nine slide
  thumbnails.
- 2026-06-14: Added local G10015-style temperature-profile parsing and
  interpolation/extrapolation helpers with fixture tests, while keeping real
  temperature-model products and final stability outputs gated behind OSL
  source rebuilds and boundary/confidence tests.
- 2026-06-14: Added local fixture tests for stability depth grids, synthetic
  phase-boundary intersections, open-base/extrapolation caveats, and blocked
  incomplete pressure-temperature grids without calculating public
  top/base/thickness outputs.
- 2026-06-14: Added source-control confidence-label helper tests for high,
  medium, low, blocked, and outside-AU cases before creating the public
  stability screen outputs.
- 2026-06-14: Added an OSL-ready temperature-model product writer to the public
  stability pipeline. It writes temperature-input rows only when raw G10015
  profile files are present and does not create final stability-screen outputs.
- 2026-06-14: Fixed G10015 duplicate-depth handling so OSL profile rows with
  repeated depths are averaged deterministically instead of stopping the
  inventory/product rebuild.
- 2026-06-14: Added a guarded baseline stability-screen writer with fixture
  tests for calculated, phase-range-blocked, and raw-profile-missing behavior,
  then generated the first OSL-derived guarded screen from raw G10015 profile
  rows.
- 2026-06-14: Relaxed the guarded screen grid to begin at the cited phase-curve
  minimum depth after the first OSL screen run correctly produced only blocked
  rows under the earlier over-strict `0 m` coverage gate.
- 2026-06-14: Committed the guarded methane 5 ppt stability-admissibility
  screen: 8,084 rows, 22 calculated intervals, 8 no-stable-interval rows, and
  8,054 blocked rows, with no hydrate-proof claim.
- 2026-06-14: Exposed the guarded stability screen in the public Structural
  Explorer with summary metrics, status/confidence counts, calculated interval
  preview, blocked/no-interval sample, and download.
- 2026-06-14: Added visual stability-screen views to the Structural Explorer:
  a 2D well-status map and a calculated interval depth chart that explain the
  22 baseline intervals without implying hydrate proof.
- 2026-06-14: Added website diagnostics for blank stability rows and
  temperature-coverage/proxy candidates: 22 of 24 G10015 codes have committed
  GGD223 coordinate crosswalks, 483 screen rows have direct profiles, 193 are
  within 50 km of a located G10015 control, and 4,917 are 50-100 km regional
  candidates. Proxy tiers remain planning/sensitivity labels only.
- 2026-06-14: Added a selected-well temperature/phase audit plot using the
  committed methane 5 ppt phase boundary, OSL temperature key-depth product,
  and screen top/base markers where available. It is explicitly not the full
  raw measured G10015 temperature profile.
- 2026-06-14: Prepared the OSL sampled G10015 profile-point export. The next
  OSL rebuild should write
  `g10015_temperature_profile_points_sampled_2026-06-14.csv` and its summary,
  enabling measured G10015 curve traces in the selected-well audit plot.
- 2026-06-15: Added public-safe stability-screen communication drafts for the
  mentor update, weekday reporting template, and Word/PPT refresh plan while
  preserving the guardrail that the current screen is stability-admissibility
  only, not hydrate proof, saturation, or sweet-spot ranking.
- 2026-06-15: Added a creative slide-remake storyboard for the current Gmail
  nine-slide deck, shifting the visual story toward public/OSL workflow,
  stability-screen readiness, data-confidence labels, and guarded future ML
  outputs.
- 2026-06-15: Added a Word-ready pipeline status and forward workflow brief
  explaining the current project status, public/runtime boundary, guarded
  stability-admissibility layer, and leakage-safe ML path toward occurrence
  classification and saturation regression.
