# North Slope Gas Hydrates Project Context

Last updated: 2026-06-17

## Purpose

This file is the living project memory for people and agents working in this
repository. New sessions should read `docs/AGENT_START_HERE.md` first, then
use this file for concise project orientation. Update it after meaningful
changes. The detailed architecture, workstream status, dependencies, and next
activities live in `docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md`.

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
stability-admissibility guardrail aligned. User review on 2026-06-15 rejected
the first stability/ML slide-remake draft as too disconnected from the whole
project, then rejected the diagram-first replacement as changing too much of
the prior Gmail deck. Those rebuild plans remain provenance for the visual
direction, but the active local review package is now the V5.5 mentor update
deck and companion generated on 2026-06-17 from the V5.4 corrected deck. V5.4
is the source baseline, and V5.3 is a flawed intermediate/reference because it
demoted the complex diagrams and did not restore the agreed personal opener.
The deliverable cleanup and final build plan is
`docs/FINAL_DELIVERABLE_CONSOLIDATION_AND_CLEANUP_PLAN_2026-06-15.md`; use it
before editing, uploading, deleting, or renaming any older Word, PPTX, or Drive
copy. It classifies what to pull forward from Gmail, V5.2, the rule books, and
the website, and it lists deletion/archive candidates that still need explicit
approval. The earlier Gmail-style prompt, gap plan, and rebuilt 2026-06-15
deck remain provenance. Do not delete or archive them until cleanup is
explicitly approved.
The current mentor-facing rebuild is V5.5. It keeps the original Gmail-style
personal/about-me opener, keeps source-backed USGS/public hydrate and North
Slope visuals, rebuilds slide 3 as a co-moving signal-response stack across
depth, restores the complex project workflow on slide 4, adds a cleaned DOE
three-dataset prototype and visual model-run card on slide 5, centers equations
and unit gates on slide 6, restores the complex ML runtime architecture on
slide 7, adds a stability-to-ML overlay on slide 8, and closes with a clear
what-done / what-not-claimed / what-next section on slide 9. It keeps stability
as context/admissibility only rather than proof or prediction, and it frames
DOE prototype metrics as training-fit/runtime proof only.
The
2026-06-15 pipeline status Word brief remains the plain-language review draft
for explaining where the project stands now and how the approved-data ML
pipeline should reach occurrence classification and saturation regression.
The non-stability ML/schema readiness baseline is now
`docs/APPROVED_DATA_SCHEMA_COVERAGE_AND_MODEL_ARCHITECTURE_PLAN.md` and
`data/public_ml_products/approved_schema_coverage_matrix_2026-06-15.csv`.
Only about 3 of the expected 71 datasets are currently available, which is
enough for schema and architecture design but not final training, performance
metrics, or hydrate prediction claims.
The practical next-products layer is now defined by
`data/public_ml_products/approved_data_field_role_table_2026-06-15.csv`,
`docs/APPROVED_DATA_INTAKE_SPEC_2026-06-15.md`,
`docs/FIRST_MODEL_EXPERIMENT_PLAN_2026-06-15.md`, and
`docs/MENTOR_DECISION_REQUESTS_2026-06-15.md`. These files turn the visible
headers/screenshots into a public-safe intake contract, separate
occurrence-classification and saturation-regression tasks, and list the mentor
decisions needed before approved-runtime model training.
The intake contract is now operationalized in
`dashboard/approved_data_intake.py`, with synthetic tests in
`tests/test_approved_data_intake.py` and schema-only public templates under
`data/public_ml_products/approved_data_intake_template_2026-06-15.csv`,
`approved_data_intake_validation_schema_2026-06-15.csv`, and
`first_model_output_schema_2026-06-15.csv`. The V5.2 skeleton keeps explicit
variable-fingerprint templates, source-column registry, well-depth index,
`X_allowed`, `Y_target_registry`, and first-output schema templates under the
same public-safe folder. The header audit can now be run from
`01_pipeline/validate_approved_data_headers.py`, which reads inline headers,
header-list CSVs, or CSV headers with `--header-only`, writes public-safe
CSV/JSON readiness summaries under
`data/public_ml_products/intake_readiness_reports/`, and is documented for OSL
use in `docs/OSL_APPROVED_DATA_HEADER_AUDIT_RUNBOOK_2026-06-15.md`.
The approved-runtime three-workbook ML runner is now scaffolded in
`dashboard/runtime/three_dataset_pipeline.py` with the header-scan CLI
`01_pipeline/inspect_three_dataset_headers.py`, the model CLI
`01_pipeline/run_three_dataset_ml_pipeline.py`, and runbook
`docs/DOE_THREE_DATASET_ML_PIPELINE_RUNBOOK_2026-06-16.md`. It defaults to
`curated_dataset1.xlsx` for training and `curated_dataset2.xlsx` plus
`curated_dataset3.xlsx` as external tests, can inspect all workbook sheets for
target-looking headers, detects saturation/occurrence targets, excludes
target-like fields and depth from `X_allowed`, applies train-only 0-1 scaling,
and writes row-level predictions/models only to ignored runtime folders.
The DOE/Jupyter multi-saturation transfer workflow now trains separate
prototype regressors for visible saturation target variants while excluding
depth, unit/helper columns, unnamed spreadsheet artifacts, and duplicate raw
aliases from `X_allowed`. The website now has an
`Analyze Hydrates > Model Run Tracker` tab backed by
`dashboard/runtime/model_run_tracker.py`; it reads ignored local
`outputs_runtime/` summaries and shows run comparisons, target-by-target review
cards, feature families, exclusion reasons, validation-status flags,
dataset/sheet inventory, final-claim blockers, public-safe summary export, and
the stability-to-ML contract without committing approved rows or row-level
predictions.
The parameter evidence board is now implemented as a public-safe registry at
`data/public_ml_products/public_parameter_evidence_registry_2026-06-16.csv`,
with loader/validation logic in `dashboard/parameter_evidence.py`, tests in
`tests/test_parameter_evidence_registry.py`, and a Streamlit display under
Analyze Hydrates > Schema Coverage & Architecture. Use this registry as the
source for the next slide 3 and slide 5 parameter-range visuals: it separates
stability, reservoir quality, hydrate-response logs, QC, and Y-only targets;
marks numeric values as working screening envelopes rather than final DOE
cutoffs; and keeps the guardrails that stability, high resistivity, low GR, and
target labels are not hydrate proof.
The slide/website visual layer now has a public-safe source inventory at
`data/public_ml_products/source_visual_inventory_2026-06-16.csv`, with QA logic
in `dashboard/source_visual_inventory.py`, tests in
`tests/test_source_visual_inventory.py`, and a Streamlit display under Analyze
Hydrates > Presentation Exports. Use this inventory before changing deck or
Word visuals: it tracks V5.5 slide panels, V5.4/V5.3 reference panels,
website captures, source-backed figures, authority diagrams, and contact
sheets, and it flags uncited or AI-looking visuals before they enter the
mentor-facing package.

The active mentor-facing workflow package is now the V5.5 Slide 3
signal-response update
under
`docs/project_blueprints/presentation_assets/v5_5_slide3_signal_response_update_2026_06_17/`.
Use `slide_04_full_complex_project_workflow_v5_5.png` as the full project
architecture plate, `slide_07_complex_ml_runtime_architecture_v5_5.png` as
the ML runtime plate, `slide_05_doe_three_dataset_prototype_v5_5.png` as the
DOE prototype/model-run card, and
`slide_08_stability_to_ml_overlay_v5_5.png` as the stability overlay. The
Slide 2 context panel was rebuilt from the selected USGS/DOE source screenshot
and curve crop, the project website regional map, and the project digitized
methane 5 ppt CSV inset. It explicitly says stability is
pressure-temperature admissibility context only, not hydrate proof,
occurrence evidence, or saturation evidence. Slide 3 is rebuilt from the local
Slide 3 signal-response source package with a public-safe cleaned depth stack,
CSV methane 5 ppt stability inset, project website 2D stability map context,
and source badges for Mount Elbert/Milne Point, Eileen/Tarn, and PBU L-Pad
context. It explains co-moving stability context, clean sand (GR/gamma), pore
space (phi/RHOB), resistivity (Rt), P-wave speed (Vp), rigidity
(Vs/mu-rho), and fluid/core checks (NMR/core) while keeping stability as
context and Sgh, S_h, Sh, Hydrate Saturation, NMR_SAT, Swr, and phase labels
on the Y-only rail. Caliper/washout/bad-hole QC is treated as upstream
preprocessing for this slide rather than a visible interpretation track. The
V5.5 PPTX plus Word companion are regenerated from
`docs/project_blueprints/build_full_workflow_diagram_deliverables.py`.
The current local deliverables are
`docs/project_blueprints/V5_5_SLIDE3_SIGNAL_RESPONSE_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Slides_2026-06-17.pptx`
and
`docs/project_blueprints/V5_5_SLIDE3_SIGNAL_RESPONSE_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Companion_2026-06-17.docx`.
The verified native Google Slides/Docs imports are:
`https://docs.google.com/presentation/d/1MuMBhO_IQ0sXGCr5IKcdLRUlEm_CHKsrHWSHCzB3DCA`
and
`https://docs.google.com/document/d/180KwTmIQlkQr2Zbu5MUt78oL1nj9Zh_y-3KahtQbpMw`.
Do not reopen OSL unless a source/product rebuild is actually needed.

## Current ML Architecture Decisions And Open Mentor Questions

### A. Ready to encode now

- Keep occurrence classification and saturation regression linked but separate.
- Occurrence is target/validation evidence from approved sources, not stability
  proof. Stability remains methane 5 ppt admissibility/context only.
- Numeric predictors use train-only 0-1 scaling after a whole-well,
  compartment, or geographic split. Depth is the alignment/context axis unless
  mentor approves predictor use, and units stay visible with original headers.
- Every variable needs a fingerprint: original header, unit, normalized name,
  role, feature-matrix permission, leakage risk, and unresolved mentor question.
- Caliper coverage is checked before washout filtering. Missing caliper creates
  a missing-QC flag rather than automatic row filtering.
- Candidate features are allowed only after source, unit, QC, and leakage
  checks: `GR`, density porosity, resistivity transforms, `Vp`, `Vs`, `Vp/Vs`,
  impedance, elastic attributes, NMR-density separation, and equation features.
- Model order is baselines first, tree/boosting second, ANN/Keras third.
  Chong et al. 2024 / USGS is an external hydrate ML anchor for occurrence
  classes and saturation prediction: <https://pubs.usgs.gov/publication/70250169>.
- Well-MTE is Mt. Elbert Stratigraphic Test Well and Well-IGS is Ignik Sikumi
  Test Well; `MTE_refined` and `IGS_refined` remain workbook-stage questions:
  <https://www.osti.gov/servlets/purl/1893637>.
- Missing-log adapters for `Vp` or `RHOB` are optional and
  validation-required; the MDPI marine hydrate example is background, not North
  Slope validation: <https://www.mdpi.com/1996-1073/16/23/7709>.

### B. Slide review callouts

For slide work, treat the items above as known architecture decisions rather
than unanswered questions. Blue callouts should be used only for runtime
confirmations that depend on full approved-workbook recovery: target priority
when multiple saturation labels exist, fraction-vs-percent target convention,
occurrence-label provenance, train/validation/locked-test well assignment,
caliper coverage sufficiency, and missing-log adapter permission.

The 2026-06-15 Gmail-style prompt remains provenance for the visual direction.
For current mentor review, start from the V5.5 deck and companion generated by
`docs/project_blueprints/build_full_workflow_diagram_deliverables.py`; keep
V5.4 as the source baseline and V5.3 as flawed reference only.

## Current State

- The public Streamlit regional atlas is implemented.
- The website now uses a four-page, visual-first Streamlit structure with
  Processing-style public/synthetic canvas sketches.
- The synthetic well-log planning page and reusable calculation layer are
  implemented in `dashboard/well_log_engine.py`.
- The authorized runtime skeleton is implemented in `dashboard/runtime/`.
- The DOE three-dataset approved-runtime runner is implemented in
  `dashboard/runtime/three_dataset_pipeline.py` with CLI entry point
  `01_pipeline/run_three_dataset_ml_pipeline.py` plus header inspector
  `01_pipeline/inspect_three_dataset_headers.py`. It trains on dataset 1 and
  scores datasets 2 and 3 separately when an approved target column exists;
  otherwise it writes readiness/header outputs only.
- The DOE local model-run tracker is implemented in
  `dashboard/runtime/model_run_tracker.py` and exposed on the website under
  `Analyze Hydrates > Model Run Tracker`. It is the current review surface for
  local run summaries, cleaned feature families, exclusion audits, and
  stability-as-context guardrails.
- OpenScienceLab is the intended heavy-data workbench for approved inputs and
  guarded runtime calculations; GitHub/Streamlit remains the public delivery
  surface for source-backed documentation, public GIS, and synthetic/public
  scaffold views.
- Tests exist in `tests/test_well_log_engine.py` and
  `tests/test_runtime_skeleton.py`.
- The full project test suite passed after the DOE model-run tracker
  review-board update and V5.5 deck update: 117 tests passed and 2 were
  skipped after adding the tracker review-board tests and regenerating the
  V5.5 deck, companion, slide panels, contact sheet, source visual inventory,
  and Presentation Exports wiring. Update this count only after a fresh local
  pytest run.
- Public GIS layers, notebooks, structural surfaces, and Plotly exports are
  present.
- Two working Word drafts and a rebuilt 2026-06-13 local research-overview
  Word/PPT deliverable pair are present in `docs/project_blueprints/`.
- The current local presentation baseline is the V5.5 Slide 3 signal-response
  update
  workflow deck rebuilt from `docs/project_blueprints/build_full_workflow_diagram_deliverables.py`:
  `docs/project_blueprints/V5_5_SLIDE3_SIGNAL_RESPONSE_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Slides_2026-06-17.pptx`.
  It keeps the agreed nine-slide spine, restores the personal/about-me opener,
  rebuilds Slide 2 with selected USGS/DOE source-backed stability visuals,
  the project website map, methane/Structure I baseline language, and the
  stability-not-proof guardrail, rebuilds Slide 3 as a co-moving signal
  response stack with mimic/QC/Y-only guardrails, restores complex workflow and
  ML runtime architecture plates on slides 4 and 7, adds a DOE three-dataset
  prototype/model-run card on slide 5, adds a stability-to-ML overlay on slide
  8, and closes with what is done, what is not claimed, and what is next on
  slide 9. The current deck and companion were
  imported to Drive as native Google Slides/Docs:
  <https://docs.google.com/presentation/d/1MuMBhO_IQ0sXGCr5IKcdLRUlEm_CHKsrHWSHCzB3DCA>
  and
  <https://docs.google.com/document/d/180KwTmIQlkQr2Zbu5MUt78oL1nj9Zh_y-3KahtQbpMw>.
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
- `data/public_stability_products/public_ml_feature_scaffold_2026-06-15.csv`,
  `public_ml_feature_scaffold_summary_2026-06-15.csv`, and
  `public_ml_feature_dictionary_2026-06-15.csv` now turn the public stability
  products into a future-ML feature and coverage scaffold. The scaffold has
  `8,084` public well rows, `483` G10015 temperature-profile matches, `22`
  calculated baseline stability-interval feature rows, `8` no-stable-interval
  rows, and `0` validated occurrence/saturation labels or training-ready rows.
  These products are feature engineering and readiness context only, not model
  labels or predictions.
- `data/public_stability_products/public_ml_target_registry_2026-06-15.csv`
  and `public_ml_leakage_guardrails_2026-06-15.csv` now codify the existing
  base-file decision that all saturation/ground-truth header families are
  target-only. `Sgh`, `S_h`, `Sh`, `NMR_SAT`, `Hydrate Saturation`, `Swr`,
  `S_wr`, and interpreted phase labels are targets, calibration references, or
  outputs, not input predictors. No approved target rows are committed.
- `docs/APPROVED_DATA_SCHEMA_COVERAGE_AND_MODEL_ARCHITECTURE_PLAN.md` and
  `data/public_ml_products/approved_schema_coverage_matrix_2026-06-15.csv`
  now provide a public-safe schema coverage and model architecture layer
  outside the stability screen. The matrix preserves original headers, maps
  canonical roles as metadata, separates measured inputs, derived features,
  QC/alignment fields, target-only fields, calibration/reference fields, and
  unresolved fields, and keeps the workflow results-free until broader
  approved-data coverage exists.
- `data/public_ml_products/approved_data_field_role_table_2026-06-15.csv`,
  `docs/APPROVED_DATA_INTAKE_SPEC_2026-06-15.md`, and
  `docs/FIRST_MODEL_EXPERIMENT_PLAN_2026-06-15.md` now define the minimum
  approved-data intake contract and first model experiment plan. They are
  header/schema products only: no approved rows, saturation values, trained
  metrics, occurrence probabilities, or public sensitive outputs are committed.
- `dashboard/approved_data_intake.py` and
  `tests/test_approved_data_intake.py` now provide a tested public-safe intake
  validator. The validator accepts header lists or synthetic/test DataFrames,
  reports recognized and unknown headers, target leakage, unresolved fields,
  minimum predictor coverage, occurrence/saturation target authority, split
  readiness, and blocked reasons without reading approved row values.
- Public-safe runtime templates now exist under `data/public_ml_products/` for
  the approved-data intake table contract, intake validation checks, and first
  model output schema.
- The `Analyze Hydrates` page now includes a `Schema Coverage & Architecture`
  tab that shows the about-3-of-71 coverage status, current public counts,
  public-now versus OSL-later contract, blocked reasons, mentor decisions,
  intake validator contract, runtime template downloads, role counts,
  target-only separation, approved-data field roles, and architecture path
  without exposing approved rows or model metrics.
- The same page now includes a `Model Run Tracker` tab that reads ignored local
  runtime summaries in DOE, shows model-run comparisons and target cards,
  tracks feature/exclusion audits, flags training-fit-only metrics versus
  external/whole-workbook validation, exports row-free public-safe summaries,
  and keeps stability framed as context, mask, confidence, and caveat rather
  than hydrate proof.
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
- `docs/APPROVED_DATA_SCHEMA_COVERAGE_AND_MODEL_ARCHITECTURE_PLAN.md`:
  non-stability ML/schema readiness plan for preserving approved-data headers,
  mapping roles, blocking target leakage, and designing whole-well validation
  before final training
- `docs/APPROVED_DATA_INTAKE_SPEC_2026-06-15.md`: minimum approved-data intake
  contract for well/depth alignment, required curves, optional curves, target
  labels, QC fields, unit conversions, and blocked conditions
- `docs/FIRST_MODEL_EXPERIMENT_PLAN_2026-06-15.md`: results-free first model
  experiment plan separating occurrence classification from saturation
  regression
- `docs/MENTOR_DECISION_REQUESTS_2026-06-15.md`: concise mentor update,
  decision questions, and weekday report bullets
- `dashboard/approved_data_intake.py`: public-safe header/schema validator for
  the approved-data intake contract
- `tests/test_approved_data_intake.py`: synthetic tests for the intake
  validator, target leakage barrier, target authority checks, stability context
  rule, and split-before-preprocessing rule
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

Immediate 2026-06-17 handoff: review the local V5.5 PPTX, Word companion,
PNG panels, and contact sheet as the current mentor-facing package. The deck
has the expected nine-slide spine, preserves the complex architecture diagrams
in the main sequence, adds the cleaned DOE three-dataset prototype card, and
keeps stability as context/mask/confidence/caveat only. The next
approved-runtime step is still to run the header/schema validator against
approved workbook/LAS/CSV/core/NMR sources using the header-only CLI/runbook,
then run the three-workbook local ML runner against the approved curated Excel
folder, review the `Model Run Tracker`, safely bring back summary artifacts
only, and confirm target authority, units, well/depth alignment, validation
split policy, and whether stability may enter `X_allowed` only as context,
mask, confidence, caveat, or blocked reason.

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

- 2026-06-16: Added `docs/AGENT_START_HERE.md`,
  `docs/CURRENT_ARTIFACT_INDEX.md`, and `docs/PROJECT_PROMPT_LIBRARY.md` as
  the first-read handoff layer for future Codex, PC, and OpenScienceLab
  sessions.
- 2026-06-16: Added the approved-runtime three-dataset ML pipeline scaffold,
  CLI, header inspector, runbook, and synthetic Excel tests for training on
  `curated_dataset1.xlsx` and externally scoring `curated_dataset2.xlsx` plus
  `curated_dataset3.xlsx` without committing approved rows or predictions.
- 2026-06-16: Added the DOE local model-run tracker, public-safe tracker
  templates, and `docs/DOE_RUNTIME_PRESENTATION_AND_MODEL_TRACKING_PLAN_2026-06-16.md`
  so cleaned saturation prototype runs can be explained through the website
  with feature exclusions and stability context instead of relying on loose
  metric screenshots.
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
  committed methane 5 ppt phase boundary, sampled G10015 CSV profile points,
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
- 2026-06-15: Superseded the first stability/ML slide-remake draft with a
  diagram-first deliverable refresh: one full project ML workflow flowchart, a
  9-slide PPTX that keeps slides 1-2 locked and uses the map plus zoom-ins for
  slides 3-9, and a Word companion explaining the same workflow without
  claiming hydrate proof, saturation, validated ML results, or sweet spots.
- 2026-06-15: Added a public-safe approved-data schema coverage and model
  architecture layer outside the stability screen, including a schema matrix,
  an Analyze Hydrates tab, mentor-facing language, and target-leakage controls
  that keep saturation/phase labels out of the feature matrix until approved
  training and validation are possible.
- 2026-06-15: Improved the workflow visuals to V5 and pushed commit `738ff48`.
  The full project architecture now includes visual mini-panels for source
  packages, pressure-temperature stability checking, log-track feature
  construction, target-safe model runtime, and reviewed outputs. The companion
  ML architecture diagram now shows feature/QC groups, compact log tracks,
  the `X_allowed` matrix handoff, neural-network-style layers, occurrence and
  saturation heads, baseline comparison, validation, and target-only rail.
- 2026-06-15: Returned the active slide build to the previous Gmail-style
  nine-slide deck instead of the diagram-first replacement. Rebuilt the local
  PPTX and Processing panels with an improved gas-hydrate definition/stability
  slide, symbol-clean parameter scaffold, full workflow diagram on the ML
  methodology slide, expanded parameter rationale, stronger geomechanics and
  map-stack visuals, and corrected occurrence/saturation explanation in the
  results/discussion and conclusion slides.
- 2026-06-15: Built the V5 mentor status package around the new workflow
  diagrams, including a short Markdown update, a Word export, strengthened V5
  Word companion language, and exact mentor decisions for phase-curve policy,
  target authority, validation split, missing-temperature handling, and ML use
  of stability as context or mask only.
- 2026-06-15: Improved the current V5 diagram implementation so the slide deck
  uses a readable mentor-scale workflow summary instead of a shrunken poster,
  while the expanded architecture poster remains available separately. The ML
  runtime detail was simplified around feature families, X allowed, whole-well
  split controls, target-only labels, occurrence/saturation heads, and reviewed
  outputs without adding result claims.
- 2026-06-15: Imported the revised V5 workflow deck and Word companion to the
  connected Google Drive account as native Google Slides/Docs for review:
  `REVISED V5 FULL WORKFLOW ML DIAGRAM 9-SLIDE North Slope Gas Hydrate Slides
  2026-06-15` and `REVISED V5 North Slope Gas Hydrate Full ML Workflow Diagram
  2026-06-15`.
- 2026-06-15: Completed the V5 workflow package pass. The expanded poster now
  carries the public counts, approved-OSL boundary, stability equations and
  guardrails, feature/QC/context families, target-only occurrence and saturation
  labels, split/preprocess/model controls, validation checks, public-safe output
  rules, and mentor decisions. The PPTX, DOCX, PNG panels, ML runtime detail,
  and contact sheet were regenerated without adding hydrate-proof, saturation,
  sweet-spot, or trained-ML claims.
- 2026-06-15: Imported the V5 completion PPTX and DOCX to the connected Google
  Drive account as native Google Slides/Docs and verified Drive metadata plus
  representative slide thumbnails/doc readback:
  `V5 COMPLETION Full Workflow ML Diagram 9-Slide North Slope Gas Hydrate
  Slides 2026-06-15` and `V5 COMPLETION North Slope Gas Hydrate Full ML
  Workflow Diagram 2026-06-15`.
- 2026-06-15: Added the next practical approved-data readiness layer: a
  public-safe field-role table, minimum approved-data intake spec, first model
  experiment plan, mentor decision packet, and website readiness tables. These
  keep occurrence and saturation as separate future tasks, keep target labels
  out of `X_allowed`, and do not expose approved rows or claim model results.
- 2026-06-15: Operationalized the approved-data readiness layer with
  `dashboard/approved_data_intake.py`, synthetic validator tests, public-safe
  intake and output schema templates, and an expanded Schema Coverage website
  section for required column families, leakage rules, blocked conditions, and
  downloads.
- 2026-06-15: Refreshed the workflow package to V5.2. The PPTX now has a
  project-specific cover, embeds the expanded architecture map on slide 4 and
  the ML runtime detail on slide 7, and adds readable decision-box slides for
  variable fingerprints, X allowed/Y-only labels, train-only scaling, depth
  policy, caliper-first QC, missing-log adapters, and model order. The Word
  companion now includes current ML architecture decisions, the variable
  fingerprint/intake validator contract, and research source anchors. Native
  Google Slides/Docs imports were verified in Drive without adding approved
  rows or ML-result claims.
- 2026-06-15: Added a Gmail-style V5.2 slide-remake prompt that preserves the
  original/main slide-topic sequence, uses V5.2 science/ML decisions as method
  content, restores the older Gmail deck as the visual authority, and converts
  prior blue mentor questions into runtime confirmation callouts where the base
  already gives the architecture decision.
- 2026-06-15: Added a final deliverable consolidation and cleanup plan after
  reviewing local PPTX/DOCX versions, Drive copies, slide/Word rule books,
  website structure, and the base. The plan defines the final build path as
  Word method spine first, Gmail-style slide rebuild second, website wording
  sync third, with exact local and Drive cleanup candidates held for approval.
- 2026-06-15: Corrected the final slide-rebuild instructions so the
  original/main nine-slide topic sequence remains the slide-topic authority;
  V5.2 is used for updated method content and intact complex architecture
  slides only.
- 2026-06-15: Added a final nine-slide gap and diagram-reuse plan that maps
  each original slide topic to its weak spots, source materials, and allowed
  use of the complex V5.2 workflow and ML runtime diagrams as whole-slide
  architecture plates.
- 2026-06-15: Added the final new-slide-deck creation prompt that corrects the
  slide 2 image/composition problem, keeps the original Gmail topic structure,
  uses the website visual language, and preserves the complex V5.2 architecture
  diagrams as intact whole-slide plates.
- 2026-06-15: Executed the final new-slide-deck prompt locally by patching the
  Gmail-style raster builder, regenerating the nine slide panels and PPTX,
  preserving the original topic sequence, replacing the weak hydrate intro,
  adding the sticky variable-fingerprint/unit logic, and embedding the intact
  V5.2 expanded architecture and ML runtime plates without adding approved rows,
  fake metrics, hydrate proof, or model-result claims.
- 2026-06-15: Imported the rebuilt final Gmail-style PPTX to Drive as native
  Google Slides and verified Drive metadata, nine-slide readback, and large
  thumbnails for the corrected intro, expanded architecture plate, ML runtime
  plate, and conclusion.
- 2026-06-16: Rebuilt the workflow package as V5.3 for mentor review. The
  package uses actual website captures and source-backed hydrate/North Slope
  visuals, makes slide 3 a parameter-range board, simplifies the non-ML
  workflow explanation, keeps the expanded architecture and ML runtime diagrams
  whole as appendix plates, rewrites the Word companion for a mentor audience,
  imports both files to Drive as native Google Slides/Docs, and keeps stability
  as context/admissibility only with no approved rows, predictions, or model
  metrics.
- 2026-06-17: Rebuilt the active local mentor deck and companion as V5.5 from
  the V5.4 corrected baseline. The nine-slide sequence preserves the personal
  opener, source-backed context, full complex workflow, and complex ML runtime
  plates, then adds the cleaned DOE three-dataset prototype/model-run card,
  stability-to-ML overlay, and clear done/not-claimed/next close without adding
  approved rows, hydrate proof, final stability claims, trained metrics,
  occurrence predictions, or saturation predictions.
te structure, and the base. The plan defines the final build path as
  Word method spine first, Gmail-style slide rebuild second, website wording
  sync third, with exact local and Drive cleanup candidates held for approval.
- 2026-06-15: Corrected the final slide-rebuild instructions so the
  original/main nine-slide topic sequence remains the slide-topic authority;
  V5.2 is used for updated method content and intact complex architecture
  slides only.
- 2026-06-15: Added a final nine-slide gap and diagram-reuse plan that maps
  each original slide topic to its weak spots, source materials, and allowed
  use of the complex V5.2 workflow and ML runtime diagrams as whole-slide
  architecture plates.
- 2026-06-15: Added the final new-slide-deck creation prompt that corrects the
  slide 2 image/composition problem, keeps the original Gmail topic structure,
  uses the website visual language, and preserves the complex V5.2 architecture
  diagrams as intact whole-slide plates.
- 2026-06-15: Executed the final new-slide-deck prompt locally by patching the
  Gmail-style raster builder, regenerating the nine slide panels and PPTX,
  preserving the original topic sequence, replacing the weak hydrate intro,
  adding the sticky variable-fingerprint/unit logic, and embedding the intact
  V5.2 expanded architecture and ML runtime plates without adding approved rows,
  fake metrics, hydrate proof, or model-result claims.
- 2026-06-15: Imported the rebuilt final Gmail-style PPTX to Drive as native
  Google Slides and verified Drive metadata, nine-slide readback, and large
  thumbnails for the corrected intro, expanded architecture plate, ML runtime
  plate, and conclusion.
- 2026-06-16: Rebuilt the workflow package as V5.3 for mentor review. The
  package uses actual website captures and source-backed hydrate/North Slope
  visuals, makes slide 3 a parameter-range board, simplifies the non-ML
  workflow explanation, keeps the expanded architecture and ML runtime diagrams
  whole as appendix plates, rewrites the Word companion for a mentor audience,
  imports both files to Drive as native Google Slides/Docs, and keeps stability
  as context/admissibility only with no approved rows, predictions, or model
  metrics.
