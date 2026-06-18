# North Slope Project Base

Created: 2026-06-12

Use `docs/AGENT_START_HERE.md` as the first read for new sessions. This file is
the broader working base for the Alaska North Slope gas hydrate project. Older
planning files remain in the repo as provenance, but future agents should start
with the short handoff layer before changing the Word document, slides, or
website.

## Current Repository

- Local path varies by machine; current workspace:
  `C:\Users\Writwik\Documents\north-slope-gas-hydrates`
- GitHub: `Rnanda442/north-slope-gas-hydrates`
- Main branch: `main`

## Core Project Goal

Build a source-backed North Slope gas hydrate workflow that can explain, plan, and later run approved well-log/core analysis for hydrate occurrence and saturation.

The public repo should contain:

- public GIS context;
- source-backed science explanation;
- Word and slide deliverables;
- header/schema examples and synthetic scaffold data only if needed later for code testing;
- code skeletons for future approved-runtime work;
- diagrams, parameter logic, and equations.

The public repo should not contain:

- classified or approved well-log/core rows;
- restricted well identifiers;
- real populated runtime configs;
- trained models from approved data;
- model metrics from approved data;
- sensitive derived outputs.

## User Direction Locked So Far

- Main goal is the Word document and 9-slide PowerPoint.
- Website is secondary and should act as a skeleton/middle layer for future DOE/Anaconda execution.
- The website can store structure, schema, diagrams, export layouts, and later optional synthetic examples for code testing.
- Real data work and real model metrics will happen later inside the DOE/approved environment.
- Screenshots of headers, equations, and project overview are acceptable evidence and should stay available in Git.
- The project needs actual ranges, numbers, scientific reasoning, and source backing before major deliverable edits.
- Earlier Gmail-deck feedback treated slide 1 as close and slides 2-9 as needing
  stronger specifics, formatting, syntax, science, and ML pipeline clarity.
- The 2026-06-18 self-email `slide updates for the newest deck` is the latest
  deck-direction layer. It is captured in
  `docs/DECK_REVISION_DELEGATION_BASE_2026-06-18.md` and should be used to
  delegate current slide, website-map, equation, source-research, and PC/OSL
  sync tasks.
- The main audience deck should keep the original nine topic slides; technical
  diagram plates can be appended when explicitly needed to keep complex
  architecture diagrams whole.
- Word first, slides second, website third.
- Do not make fake datasets as the next priority. Focus first on equations, parameter logic, source-backed hydrate constraints, and the ML pipeline design.
- If synthetic/fake data is ever used later, it should only test code structure and must preserve the screenshot header style. It should not drive the science narrative.
- DOE project overview screenshots are official wording/evidence, not casual notes.

## Current Deliverable Inventory

### One File To Read First

- `docs/AGENT_START_HERE.md`

Then use:

- `docs/CURRENT_ARTIFACT_INDEX.md` for active/superseded/reference artifacts
  and edit safety.
- `docs/PROJECT_PROMPT_LIBRARY.md` for reusable slide, Word, website, OSL,
  source research, parameter evidence, stability, and mentor-status prompts.
- `docs/DECK_REVISION_DELEGATION_BASE_2026-06-18.md` for the latest self-email
  deck direction and copyable topic prompts for PC/OSL/delegated Codex chats.
- `docs/NORTH_SLOPE_PROJECT_BASE.md` for the broader project base.

### Slide Authority And Current Deck

- Current mentor-review deck:
  `docs/project_blueprints/V5_5_SLIDE2_SOURCE_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Slides_2026-06-17.pptx`
- Current native Google Slides review copy:
  <https://docs.google.com/presentation/d/1-35vfTIXAnWCiyKTLooJy80HBYliMBliE_z4CbggJC0>
- Current Word companion:
  `docs/project_blueprints/V5_5_SLIDE2_SOURCE_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Companion_2026-06-17.docx`
- Current native Google Docs review copy:
  <https://docs.google.com/document/d/1CyZkRgfAUSOOaRxXni0mcmFN2OQcc5pNOw8TOv44f0Q>

- Latest self-email deck attachment, needs review before it becomes a repo
  artifact:
  Gmail thread `19edc9d8ce7f95f1`, message `19edd022306af325`, attachment
  `V5.5 Slide 3 Signal Response QC-Cleaned North Slope Gas Hydrate ML Workflow Slides 2026-06-17 (1).pptx`.
  The user says this is the best deck so far. Do not commit or overwrite any
  deck with this attachment until a future session downloads, verifies, and
  explicitly stages it.

- `docs/project_blueprints/CURRENT_GMAIL_VISUAL_REVISION_9_SLIDE_North_Slope_Gas_Hydrate_Slides_2026-06-11.pptx`
- Source: Gmail message `19eba86da8752830`
- Subject: `New pressy`
- Sent: 2026-06-12 01:30 CDT
- Verified: valid 9-slide PPTX.
- Use this deck as historical visual authority only. The current review deck is
  the V5.5 mentor update above.
- Cleanup/consolidation control now exists at
  `docs/FINAL_DELIVERABLE_CONSOLIDATION_AND_CLEANUP_PLAN_2026-06-15.md`.
  Use it before opening or deleting any older Word, PPTX, or Drive copy. The
  plan locks the working rule: the original/main nine-slide topic sequence is
  topic authority, the Gmail deck is visual authority, V5.2 supplies method
  content and intact complex architecture slides, Word is the method spine, and the website
  mirrors the final Word/PPT story rather than driving it.
- The slide-by-slide gap and diagram-reuse plan is
  `docs/FINAL_NINE_SLIDE_GAP_AND_DIAGRAM_REUSE_PLAN_2026-06-15.md`.
  Use it to decide what each original slide is lacking and how to keep the
  complex V5.2 diagrams whole without changing the slide topics.
- The final deck-build prompt is
  `docs/FINAL_NEW_SLIDE_DECK_CREATION_PROMPT_2026-06-15.md`.
  It has now been executed locally through
  `docs/project_blueprints/build_processing_slide_assets.py` and
  `docs/project_blueprints/build_ml_revamp_powerpoint.py`. The rebuilt targeted
  Gmail-style deck is
  `docs/project_blueprints/North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview.pptx`,
  with refreshed raster panels under
  `docs/project_blueprints/presentation_assets/processing_revisions_2026_06_11/`.
  The rebuild preserves the original nine-slide topic structure, corrects the
  slide 2 image/composition problem, adds the sticky variable-fingerprint and
  unit-normalization logic, and keeps the V5.2 expanded architecture and ML
  runtime diagrams intact as whole-slide plates. The rebuilt deck was imported
  to Drive as native Google Slides for review:
  <https://docs.google.com/presentation/d/1cWG9ZJvBTQ2hLTbIGJHggcBn46geRrdIUpGY7hWYtd8>.
- Current committed V5.5 Slide 2 source update workflow package:
  `docs/project_blueprints/V5_5_SLIDE2_SOURCE_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Slides_2026-06-17.pptx`.
  It has the agreed nine-slide spine, restores the original personal/about-me
  opener, uses source-backed hydrate and North Slope context visuals, makes
  slide 3 parameter-range-only, restores the full complex project workflow as
  slide 4, adds the cleaned DOE three-dataset prototype and visual model-run
  card on slide 5, centers equations and unit gates on slide 6, restores the
  complex ML runtime architecture as slide 7, adds the stability-to-ML overlay
  on slide 8, and closes with what is done, what is not claimed, and what is
  next on slide 9. It does not include approved rows, trained final model
  metrics, occurrence predictions, saturation predictions, hydrate proof, or
  sweet-spot ranking.
  The previous V5.4 copy is in Drive as a reference/source baseline:
  [V5.4 CORRECTED North Slope Gas Hydrate ML Workflow Slides 2026-06-16](https://docs.google.com/presentation/d/1olavI9-nUSSvYtEm-TjYVOte-Cg-1UgaO9GMl6skDt0).
- V5.3 is a flawed intermediate/reference, not the active mentor deck. Keep it
  for provenance, counts, website captures, and any genuinely improved
  source-backed visual only:
  `docs/project_blueprints/V5_3_North_Slope_Gas_Hydrate_ML_Workflow_Slides_2026-06-16.pptx`.
- Prior V5.2 workflow package:
  `docs/project_blueprints/V5_2_FULL_WORKFLOW_ML_DIAGRAM_North_Slope_Gas_Hydrate_Slides_2026-06-15.pptx`.
  It uses a project-specific cover slide, keeps the methane hydrate intro in
  the Gmail visual format, uses slide 3 as the readable mentor-scale workflow
  map, embeds the expanded architecture map on slide 4, embeds the ML runtime
  detail on slide 7, and uses the other slides for stability context,
  variable-fingerprint decisions, model decision boxes, and mentor decisions.
  Treat the earlier
  `STABILITY_ML_REMAKE_9_SLIDE_North_Slope_Gas_Hydrate_Slides_2026-06-15.pptx`
  as superseded unless the user asks to revive it.
  The V5.2 copy is also in Drive as prior provenance:
  [V5.2 FULL WORKFLOW ML DIAGRAM North Slope Gas Hydrate Slides 2026-06-15](https://docs.google.com/presentation/d/1w9eqANgOc89c1wCUC0xi9eZoBup-3JNllSUI923skgA).
- Current diagram layouts are the V5.5 Slide 2 source update refresh:
  - `docs/project_blueprints/presentation_assets/v5_5_slide2_source_update_2026_06_17/slide_04_full_complex_project_workflow_v5_5.png`
    is the full complex project workflow architecture plate.
  - `docs/project_blueprints/presentation_assets/v5_5_slide2_source_update_2026_06_17/slide_07_complex_ml_runtime_architecture_v5_5.png`
    is the complex ML runtime architecture plate showing feature/QC groups,
    `X_allowed`, validation split, train-only preprocessing, output heads, and
    the target-only rail.
  - `docs/project_blueprints/presentation_assets/v5_5_slide2_source_update_2026_06_17/slide_05_doe_three_dataset_prototype_v5_5.png`
    is the DOE three-dataset prototype and visual model-run card.
  - `docs/project_blueprints/presentation_assets/v5_5_slide2_source_update_2026_06_17/slide_08_stability_to_ml_overlay_v5_5.png`
    is the stability-as-context/mask/confidence/caveat overlay.
  - `docs/project_blueprints/presentation_assets/v5_5_slide2_source_update_2026_06_17/v5_5_slide2_source_update_contact_sheet.png`
    is the current visual QA contact sheet.
  - The generated PPTX and Word companion were rebuilt from
    `docs/project_blueprints/build_full_workflow_diagram_deliverables.py`.

### Current Word Authority

- `docs/project_blueprints/North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview.docx`
- Role: current research overview document.
- Needs next pass after parameter/source logic is made clearer.
- Diagram companion for the current workflow discussion:
  `docs/project_blueprints/V5_5_SLIDE2_SOURCE_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Companion_2026-06-17.docx`.
  This is the current committed V5.5 companion. It explains the updated
  deck slide by slide and includes short source-backed sections on hydrate
  structures, stability as admissibility only, log-response ambiguity, the DOE
  three-dataset prototype, leakage-safe ML, separate saturation targets, and
  what is not claimed.
  The previous V5.4 copy is in Drive as a reference/source baseline:
  [V5.4 CORRECTED North Slope Gas Hydrate ML Workflow Companion 2026-06-16](https://docs.google.com/document/d/1sgl7cyGHOyJyWGoVC9e7LHb0JFnriPIDAmRizyf5wIg).
- Prior diagram companion:
  `docs/project_blueprints/V5_2_North_Slope_Gas_Hydrate_Full_ML_Workflow_Companion_2026-06-15.docx`.
  This is a public-safe one-map explanation of the current public/OSL,
  stability, feature, leakage, occurrence, saturation, validation, and export
  path, with research source anchors, current ML architecture decisions, and
  the variable fingerprint/intake validator contract.
  The V5.2 copy is also in Drive as prior provenance:
  [V5.2 North Slope Gas Hydrate Full ML Workflow Companion 2026-06-15](https://docs.google.com/document/d/1dWBNYmwGerBV8steCo0v37PbhpIAZzqNQ-Psl78Ypa8).

### Current Method / Readiness Docs

- `docs/MENTOR_PROJECT_STATUS_PACKAGE_V5_WORKFLOW_2026-06-15.md`
- `docs/MENTOR_DECISION_REQUESTS_2026-06-15.md`
- `docs/APPROVED_DATA_SCHEMA_COVERAGE_AND_MODEL_ARCHITECTURE_PLAN.md`
- `data/public_ml_products/approved_schema_coverage_matrix_2026-06-15.csv`
- `data/public_ml_products/approved_data_field_role_table_2026-06-15.csv`
- `docs/APPROVED_DATA_INTAKE_SPEC_2026-06-15.md`
- `docs/FIRST_MODEL_EXPERIMENT_PLAN_2026-06-15.md`
- `dashboard/approved_data_intake.py`
- `01_pipeline/validate_approved_data_headers.py`
- `dashboard/runtime/three_dataset_pipeline.py`
- `01_pipeline/inspect_three_dataset_headers.py`
- `01_pipeline/run_three_dataset_ml_pipeline.py`
- `docs/DOE_THREE_DATASET_ML_PIPELINE_RUNBOOK_2026-06-16.md`
- `tests/test_approved_data_intake.py`
- `tests/test_approved_data_intake_cli.py`
- `tests/test_three_dataset_ml_pipeline.py`
- `data/public_ml_products/approved_data_intake_template_2026-06-15.csv`
- `data/public_ml_products/approved_data_intake_validation_schema_2026-06-15.csv`
- `data/public_ml_products/first_model_output_schema_2026-06-15.csv`
- `data/public_ml_products/approved_data_source_column_registry_template_2026-06-15.csv`
- `data/public_ml_products/approved_data_well_depth_index_template_2026-06-15.csv`
- `data/public_ml_products/approved_data_x_allowed_candidate_template_2026-06-15.csv`
- `data/public_ml_products/approved_data_y_target_registry_template_2026-06-15.csv`
- `data/public_ml_products/first_model_output_schema_template_2026-06-15.csv`
- `data/public_ml_products/variable_fingerprint_template_2026-06-15.csv`
- `data/public_ml_products/public_parameter_evidence_registry_2026-06-16.csv`
- `data/public_ml_products/intake_readiness_reports/demo_header_audit_2026-06-15.csv`
- `data/public_ml_products/intake_readiness_reports/demo_header_audit_2026-06-15.json`
- `docs/APPROVED_DATA_INTAKE_READINESS_REPORT_2026-06-15.md`
- `docs/OSL_APPROVED_DATA_HEADER_AUDIT_RUNBOOK_2026-06-15.md`

These are the active public-safe readiness artifacts after the V5.5 mentor update workflow
package. They define and now test the field roles, approved-data intake
contract, first model experiment shape, runtime templates, CLI header audits,
OSL-safe summary handoff, mentor decisions, a normalized parameter evidence
board, and the approved-runtime three-workbook runner without exposing
approved rows in GitHub. The three-workbook runner defaults to
`curated_dataset1.xlsx` for training and `curated_dataset2.xlsx` plus
`curated_dataset3.xlsx` as external tests; it keeps target-like saturation or
occurrence fields out of `X_allowed`, excludes depth as a default predictor,
uses train-only 0-1 scaling, and writes predictions/models only to ignored
runtime folders. The parameter evidence registry is the current
source for slide/website bars showing hydrate-compatible directions, working
screening envelopes, mimics, ML role, and guardrails for stability, GR,
porosity/density, NMR separation, resistivity, sonic/elastic response, caliper
QC, and Y-only targets.

The slide and website visual provenance layer is now tracked in
`data/public_ml_products/source_visual_inventory_2026-06-16.csv`, documented in
`docs/SOURCE_VISUAL_INVENTORY_2026-06-16.md`, loaded by
`dashboard/source_visual_inventory.py`, and displayed under Analyze Hydrates >
Presentation Exports. Use it to choose V5.5 slide-ready panels, V5.4/V5.3
reference panels, website captures, source-backed visuals, authority diagrams, and contact sheets before revising a
deck or Word document. It intentionally flags uncited or AI-looking visuals and
keeps all outputs public-safe.

## Current ML Architecture Decisions And Open Mentor Questions

### A. Ready to encode now

- The approved-runtime skeleton should train two linked but separate outputs:
  occurrence classification and saturation regression.
- Occurrence is target/validation evidence, not a stability-screen
  measurement. Evidence may come from core/pressure-core observations,
  NMR/core-derived saturation, validated log interpretation, or documented
  seismic indicators.
- Numeric predictors get train-only 0-1 scaling after the whole-well,
  compartment, or geographic split. Depth remains the alignment/context axis
  unless mentor approves it as a predictor. Units must stay visible above or
  beside original headers.
- Every variable must carry a fingerprint: original header, unit, normalized
  name, role, allowed-in-feature-matrix flag, leakage risk, and unresolved
  mentor question.
- Caliper coverage comes first. Use `caliper`, `CAL1`, or differential caliper
  for washout QC when coverage is sufficient; otherwise create a missing-QC
  flag rather than filtering.
- Candidate features include `GR` shale/clean-sand proxy, density porosity,
  resistivity transforms, `Vp`, `Vs`, `Vp/Vs`, impedance, elastic attributes,
  NMR-density separation, and equation-list features only after source, unit,
  QC, and leakage checks pass.
- Model order is baselines first, tree/boosting second, and ANN/Keras third.
  Chong et al. 2024 / USGS is the external hydrate ML anchor for ANN occurrence
  classes and saturation prediction:
  <https://pubs.usgs.gov/publication/70250169>.
- Well-MTE means Mt. Elbert Stratigraphic Test Well and Well-IGS means Ignik
  Sikumi Test Well; both are Eileen Gas Hydrate Trend case-study wells. Keep
  `MTE_refined` and `IGS_refined` as workbook-stage questions until metadata
  confirms them: <https://www.osti.gov/servlets/purl/1893637>.
- Missing-log adapters for `Vp` or `RHOB` remain optional and
  validation-required. MDPI/Naim et al. supports the concept in marine hydrate
  settings but not automatic North Slope permafrost transfer:
  <https://www.mdpi.com/1996-1073/16/23/7709>.

### B. Blue slide review callouts

For the next slide rebuild, do not present the architecture choices above as
unanswered. Occurrence and saturation are linked but separate reviewed targets;
target-only saturation and phase-label fields stay out of `X_allowed`; numeric
predictors use train-only 0-1 scaling after whole-well or grouped split; depth
stays an alignment/context axis; units stay visible; caliper is coverage-first
QC; and ANN/Keras belongs after baselines and tree/boosting.

Use blue callouts only for runtime confirmations that still require full
approved-workbook recovery: target priority when multiple saturation labels
exist, fraction-vs-percent convention, occurrence-label provenance, train/
validation/locked-test well assignment, caliper coverage sufficiency, and
missing-log adapter permission.

Use `docs/GMAIL_STYLE_V5_2_SLIDE_REMAKE_PROMPT_2026-06-15.md` as the slide
remake prompt: the original/main nine-slide topic sequence is the topic
authority, the older Gmail deck is the visual authority, V5.2 is the method
content source, and the two complex diagrams should stay intact as
whole-slide architecture plates.

### Other Word Drafts

- `docs/project_blueprints/Alaska_North_Slope_Wireline_ML_Research_Paper_Draft.docx`
- `docs/project_blueprints/Alaska_North_Slope_Wireline_ML_Classification_Methods_Draft.docx`
- Use the classification methods draft for the sharper DOE-style method logic.
- Use the research-paper draft for background and source synthesis.

### Website / App

- `streamlit_app.py`
- `dashboard/app.py`
- Role: public-safe atlas plus runtime skeleton.
- Current pages include Welcome, Regional Atlas, Structural Explorer, Data Library, Research Framework, and Future Well-Log Engine.
- Website should not drive the science during the next pass. It should mirror what the Word/PPT decide.

### Screenshot Evidence

- `docs/evidence/email_screenshots_2026_06_12/`
- Includes:
  - Excel header screenshots;
  - raw Excel table screenshots;
  - MTE, IGS, MTE_refined, IGS_refined examples;
  - geomechanical equation screenshots;
  - project goal/objective screenshots;
  - contact sheet.
- Treat these screenshots as origin evidence supplied by the user. Do not lose them or replace them with generic summaries.

### ML Sources

- `references/ml-sources/2026-06-11/s10596-022-10151-9.pdf`
  - Chong et al. (2022).
  - Direct gas hydrate/well-log ML anchor.
  - Use for ANN/Keras-style saturation workflow, feature table logic, well-log ML structure, and visual diagrams.
- `references/ml-sources/2026-06-11/ML_Project_Reference_and_CreditScoreV4_Case_Notes.docx`
  - General ML reliability notes.
  - Use for leakage, validation, train/test split logic, baselines, monitoring, and data-quality framing.
- `docs/ML_CITATION_PACKET_FOR_DELIVERABLES.md`
  - Current citation packet added by the other PC.

### Revision / Provenance Files

Keep these as supporting sources, but do not force the user to read all of them every time:

- `docs/PROJECT_DIRECTION_LOCK_FOR_REVIEW.md`
- `docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md`
- `docs/NEXT_STEPS_REVIEW_BRIEF.md`
- `docs/deliverable_status_inventory.md`
- `docs/deliverable_revision_base_2026_06_12/`
- `docs/NINE_SLIDE_POWERPOINT_REVISION_WORKFLOW.md`
- `docs/ML_SOURCE_COVERAGE_AND_DELIVERABLE_REVISION_PLAN.md`
- `docs/ML_PARAMETER_TREE_AND_DECK_REVAMP_PLAN.md`
- `docs/WELL_LOG_REQUIREMENTS_MAP.md`
- `docs/FULL_PROJECT_ML_WORKFLOW_DIAGRAM.md`
- `docs/SWEET_SPOT_SOURCE_MATRIX.md`

## Data Header Inventory

Header/source screenshots show these field families.

Measured / input / preprocessing fields:

- `DEPTH`, `True Depth`, `Depth_ft`, `DEPT`
- `Rho_b`, `RHOB`, `Density_gpcc`
- `Phi_porosity`, `phi_den`, `DPHI`
- `NMRPHI`, `phi_nmr`
- differential caliper, `caliper`, `CAL1`
- deep formation resistivity, `Rt`, `RES`, `AO90`
- `GR`
- `Vs`, `VS1`
- `Vp`, `VELP`
- `Ratio Vp/Vs`
- impedance

Label / target / ground-truth fields:

- `Sgh`
- `S_h`
- `Sh`
- `NMR_SAT`
- `Hydrate Saturation`
- `Swr`

Screenshot review notes:

- The header screenshot explicitly marks `Sgh / NMR_SAT` as `GROUND TRUTH`.
- The `MTE` screenshot shows `S_h` and `S_wr` beside measured and derived log fields.
- The `IGS` screenshot shows `Sh` and `Swr`.
- The `MTE_refined` and `IGS_refined` screenshots show `Sgh` / hydrate saturation tied to depth correspondence.
- Working interpretation for now: the target family is hydrate saturation, but the exact column name depends on sheet/well/source context. Preserve original headers and document equivalences rather than renaming them away.
- The screenshots are enough to document the header/schema families and sheet/tab
  names. They are not the actual datasets. Do not spend project energy naming
  datasets in public deliverables; the useful evidence is the header structure,
  equations, official project wording, and target-field roles.
- The visible sheet/tab names include `MTE`, `IGS`, `MTE_refined`, and
  `IGS_refined`. Treat these as evidence of raw/refined table structure until
  the user can safely describe the full workbook organization.

Important working rule:

- The CSV/header scaffold should preserve the screenshot headers.
- Do not internally rename the project away from the origin headers when explaining the deliverables.
- If code eventually needs canonical aliases, keep that mapping visible and secondary. The Word/slides should show the headers as given.
- Label/ground-truth columns should be handled carefully as targets, calibration, validation, or comparison fields.
- We still need to define exactly when a saturation-related field is an input support field versus the target being predicted.
- The current public-safe field role mapping is
  `data/public_ml_products/approved_data_field_role_table_2026-06-15.csv`.
  It is a header/schema table only. It records original headers, normalized
  names, source family, role, unit/dtype expectations, required-model status,
  public-safe display status, and caveats without committing approved data
  values.

## Official DOE Project Overview From Screenshots

Project title from screenshot:

> Gas hydrate occurrence and saturation prediction in permafrost sediments on Alaska North Slope using AI/ML.

Project goals from screenshot:

- Do a literature review and compile AI/ML research methodology applicable for marine and permafrost gas hydrate deposits.
- Analyze well log information to generate a dataset including density, porosity, natural gamma ray, and acoustic wave velocity readings versus depth at wellbores penetrating permafrost gas hydrate deposits.
- Utilize the generated dataset to train machine learning models to predict occurrence and saturation of gas hydrate.
- Calibrate and refine machine learning models using core analysis data by comparing log predictions against core measurements.

Working implication:

- The DOE overview explicitly names both occurrence and saturation prediction.
- The ML workflow should therefore be framed as two related tasks:
  occurrence classification and saturation regression/estimation.
- Do not invent final metrics or labels yet; the real target roles should be
  refined after the parameter logic and external-factor matrix is built.

Learning/workflow wording from screenshot:

- Remove outliers.
- Select relevant depth intervals.
- Process raw well log data for the dataset.
- Use Python code and Keras libraries.
- Perform hyperparameter tuning for an artificial neural network algorithm.
- Run optimization tasks.
- Conduct ML model validation and testing.
- Post-process results into graphical and tabular forms.
- Deduce conclusions and recommendations from results.

Project objective bullets from screenshot:

- Compare historical AI/ML techniques employed for predicting hydrate occurrence and saturation predictions.
- Compare and analyze raw well log readings.
- Perform data pre-processing for generation of the database.
- Carry out hyperparameter tuning.
- Calculate ML model performance metrics for classification and regression analyses.
- Optimize ML model performance.
- Validate ML predictions and test using unseen data.

Use these screenshots as official DOE project-origin language. Rewrite for clarity where needed, but do not change the project meaning.

## Main Scientific Gap

Before major Word/PPT/site edits, identify the real source-backed science logic
for each parameter from the header screenshots and equations. This should become
a high-level Word section first, then a more detailed parameter/source matrix.

The project should not begin by making fake data. The project should begin by
explaining why each logged property matters, what can distort it, and how a
machine-learning pipeline should use it without making unsupported hydrate
claims.

That matrix should answer for each parameter:

- What does it measure?
- What unit is it in?
- What is the expected public/source-backed range?
- What change might support hydrate?
- What false positives could create the same response?
- What external factors can change the reading without proving hydrate?
- What does it become in the ML feature table?
- Is it measured, derived, QC-only, context, or label/target?
- Which source supports the statement?

Priority parameters:

- depth;
- density / bulk density;
- density porosity;
- NMR porosity;
- resistivity;
- gamma ray;
- caliper;
- Vp;
- Vs;
- Vp/Vs;
- impedance;
- hydrate saturation / `Sgh` target family.

External factors to explicitly discuss:

- overburden and effective stress;
- pressure-temperature stability;
- lithology and shale content;
- clean sand versus shale/carbonate/coal/ice/cement effects;
- gas versus hydrate ambiguity;
- salinity and formation water assumptions;
- borehole washout and caliper quality;
- compaction and porosity loss with depth;
- core-to-log depth mismatch;
- missing NMR or missing shear sonic;
- tool/mnemonic differences across sheets.

## Stability Parameter Source Plan

Goal: add a public-source stability layer to the Structural Explorer only after
each stability input has a clear source, unit, and confidence label. This layer
should be described as a **gas hydrate stability admissibility screen**, not as
hydrate detection or saturation prediction.

Core stability equation/workflow:

```text
well location
+ well depth
+ base of ice-bearing permafrost
+ geothermal gradient / temperature context
+ hydrostatic pressure assumption
+ methane hydrate phase curve
= estimated top, base, and thickness of gas hydrate stability zone
```

Current input status:

| Stability input | Current status | Source or proxy plan |
| --- | --- | --- |
| Well location | Available locally | Alaska DNR Well Bottom Hole Location shapefile in `raw_data/Wells/Well_Bottom_Hole_Location/`; use wellhead/bottom-hole `lat`/`lon` for spatial joins. |
| Well depth | Mostly available locally | Use `TrueVertic` first and `DrillerTot` as fallback from the Alaska DNR well file. These are public well-depth fields, not a separate user-downloaded dataset. Confirm units before calculations; working assumption is feet until field documentation confirms otherwise. |
| Base of ice-bearing permafrost | Missing as ready GIS locally | Best source is USGS OM-222, "Map showing depth to the base of deepest ice-bearing permafrost as determined from well logs, North Slope, Alaska." It appears available as a PDF/plate rather than a ready GeoPackage. Search for a digitized derivative; otherwise digitize contours/control points and record that provenance. |
| Geothermal gradient / temperature | Missing as well-specific layer locally | Use public borehole temperature sources: NSIDC G10015 Arctic Slope deep borehole temperature profiles, NSIDC GGD223 borehole/permafrost context, USGS OFR 82-1039, and USGS OFR 82-535. Calculate local gradients where profiles exist; use scenario gradients where not. |
| Pressure | Available as assumption | Use hydrostatic pore-pressure gradient as first-pass source-backed assumption, currently `9.80665 kPa/m` plus atmospheric pressure for absolute phase-curve comparison; flag as assumed rather than measured. |
| Hydrate phase curve | First lookup and scenario catalog available | Use `phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1.csv` as the mentor-approved 100 percent methane baseline, digitized from the methane and 5 ppt salt-water phase boundary in USGS SIR 2008-5175 Figure 1A. The scenario catalog records a Collett et al. (2011) / Holder et al. (1987) mixed-gas source as sensitivity-only until it is digitized or generated from a cited thermodynamic model. |
| Regional hydrate context | Public GIS available | Use USGS 2019 Gas Hydrate Assessment Unit boundaries and input forms for regional context and well/AU joins. This is not direct hydrate proof. |

Current local well-depth coverage check from the Alaska DNR well file:

- statewide well records: `10,250`;
- North Slope / Arctic Slope-ish records checked: about `8,278`;
- positive `DrillerTot`: about `7,730` of `8,278` records, or `93.4%`;
- positive `TrueVertic`: about `7,728` of `8,278` records, or `93.4%`.

`TrueVertic` is preferred for stability because pressure and temperature depend
on vertical depth. `DrillerTot` is useful for reach/depth-availability screening
but can overstate vertical depth in deviated wells.

Stability-source tasks before coding the explorer layer:

1. Download or link the public sources into a stability source ledger.
2. Confirm whether OM-222 or a derivative provides usable GIS contours/control
   points for base of ice-bearing permafrost.
3. Download NSIDC/public borehole temperature data and inspect columns, units,
   depth conventions, and station locations.
4. Define scenario fallbacks:
   - permafrost base: `305`, `610`, and `914 m` unless replaced by mapped data;
   - geothermal gradient: `2.0`, `3.2`, and `4.0 C / 100 m` unless replaced by
     local borehole-derived gradients;
   - pressure gradient: `9.80665 kPa/m` hydrostatic first-pass, with
     atmospheric pressure added for absolute phase-curve comparison.
5. Use `docs/STABILITY_CALCULATION_PLAN.md` as the controlling calculation
   contract before coding the phase-curve step.
6. Build source-control confidence labels from that plan:
   - `high_source_control`: nearby well-specific temperature/permafrost control;
   - `medium_source_control`: mapped/interpolated public source;
   - `low_source_control`: regional scenario assumption only;
   - `blocked_missing_inputs`: no final stability result.

Core output fields for the guarded stability-screen table:

```text
well_id
lat
lon
tvd_m
depth_source
permafrost_base_m
permafrost_source
geothermal_gradient_c_per_100m
temperature_source
pressure_gradient_kpa_m
pressure_source
phase_curve_source
stability_top_m
stability_base_m
stability_thickness_m
reaches_stability_zone
stability_confidence
stability_notes
```

The expanded output schema and caveat codes for `stability_screen_*.csv` are
defined in `docs/STABILITY_CALCULATION_PLAN.md`.

Structural Explorer layer direction:

- show wells colored by `reaches_stability_zone`;
- overlay hydrate assessment units;
- show permafrost-base contours/control points where available;
- show geothermal-gradient or temperature-control confidence;
- include a low/mid/high scenario toggle;
- label every result as "stability admissibility, not hydrate proof."

Public sources to prioritize:

- Alaska DNR Well Bottom Hole Location dataset for well location and depth
  fields;
- USGS OM-222 for base of deepest ice-bearing permafrost from well logs;
- NSIDC G10015 for Arctic Slope borehole temperature profiles;
- NSIDC GGD223 for borehole/permafrost-depth context;
- USGS OFR 82-1039 and OFR 82-535 for North Slope permafrost and thermal
  context;
- USGS SIR 2008-5175 for North Slope gas hydrate prospect/stability method;
- USGS 2019 Gas Hydrate Assessment Unit boundaries and input forms for regional
  hydrate assessment context.

Download/upload inventory:

- The laptop source bundle prepared on 2026-06-13 is documented in
  `docs/source_library_index/stability_source_bundle_2026_06_13.md`.
- Local laptop zip to upload into OpenScienceLab:
  `C:\Users\gargi\Downloads\north_slope_stability_sources_2026-06-13_UPLOAD_TO_OPENSCIENCE.zip`.
- Recommended OpenScienceLab extraction path:
  `data/source_library/north_slope_stability_sources_2026-06-13/`.
- Keep raw downloaded source files out of Git. Commit source maps, parsers,
  setup instructions, and public-safe derived indexes only.
- NSIDC GGD223 is no longer missing locally. Its raw FTP folder was downloaded
  into the bundle with `305` files. Use `stnlist.dat` for point permafrost-depth
  control (`pf_depth` in meters), while the Alaska DNR shapefile remains the
  main well inventory.

Current OpenScienceLab-to-website workflow:

- Treat OpenScienceLab as the heavy-data workbench. Use it for the full
  stability source bundle, raw PDFs, shapefiles, NSIDC temperature profiles,
  GeoPandas parsing, and any future approved/runtime data processing.
- Treat GitHub/Streamlit as the public delivery surface. Push only finished
  public-safe products: compact CSV/GeoJSON layers, stability-screen output
  tables, exported figures, source/provenance notes, tests, and app code.
- Do not spend project time depending on OpenScienceLab external/proxy URLs for
  final presentation access. Those links can fail by environment. Instead,
  build in OpenScienceLab, commit/push the derived public outputs, and let the
  hosted or local website render from those committed outputs.
- Current public fallback product:
  `data/public_stability_snapshot/north_slope_stability_snapshot_2026-06-13/`.
  It contains parsed GGD223 permafrost-depth controls and USGS
  `GasHydrateAUs.geojson`, so the website can show real map context even when
  the full local bundle is absent.
- Current derived well-context product:
  `data/public_stability_products/north_slope_well_stability_context_2026-06-14.csv`.
  It combines public Alaska DNR Arctic Slope well locations/depth fields,
  nearest GGD223 permafrost-depth controls, and USGS hydrate AU membership.
  Current public summary: `8,084` Arctic Slope wells with valid wellhead
  coordinates, `7,992` inside at least one USGS hydrate AU, `7,578` with a
  usable TrueVertic/DrillerTot depth field, and `7,463` first-pass public
  context candidates.
- `public_context_candidate` means "inside a USGS hydrate AU and deeper than
  the nearest GGD223 permafrost-depth control." It is not a hydrate label, not
  a saturation estimate, and not a pressure-temperature stability-zone
  calculation.
- Current derived temperature-profile inventory:
  `data/public_stability_products/g10015_temperature_profile_inventory_2026-06-14.csv`.
  It summarizes `184` public NSIDC G10015 processed borehole temperature logs
  across `24` well codes, with maximum logged depth `882.6 m` and rough
  deepest-window gradient context for each profile. These gradient values are
  context estimates only, not a calibrated geothermal model.
- Current derived stability input scaffold:
  `data/public_stability_products/stability_input_scaffold_2026-06-14.csv`.
  It joins the public well context table to representative G10015 temperature
  profiles through the nearest GGD223 control code and adds a provisional
  hydrostatic pressure estimate using `pressure_mpa = depth_m * 0.00980665`.
  Current summary: `8,084` scaffold wells, `483` rows with a G10015 profile
  match, `374` rows ready for the next phase-curve input step, and `0` final
  stability top/base/thickness results.
  - The Structural Explorer now includes a stability pipeline readiness table
    that marks pressure assumptions and the digitized phase-curve lookup as
    ready public inputs while keeping final top/base/thickness calculation as
    not calculated yet.
- Current full-bundle path remains
  `data/source_library/north_slope_stability_sources_2026-06-13/`, which is
  ignored by Git and should stay local to OpenScienceLab or the laptop.
- To rebuild the public stability products from the full OpenScienceLab bundle,
  run:

```bash
cd ~/north-slope-gas-hydrates
git pull origin main
python 01_pipeline/build_public_stability_products.py
```

  The script prints source metrics and writes only derived outputs under
  `data/public_stability_products/`.

Fresh-chat handoff as of 2026-06-15:

- Latest repository sync for the other PC: start with `git pull origin main`,
  then verify the V5.2 workflow images and deck/doc above exist.
- Previous OSL-derived public-product baseline commit:
  `aedd734 Rebuild stability products with complete G10015 profiles`.
- OpenScienceLab full source bundle is now complete enough for the current
  stability product rebuild: `7/7` tracked source items, `43` GGD223 controls,
  `184` G10015 temperature profiles, and `3` hydrate AUs.
- Local website on the laptop has been restarted and verified at:
  `http://localhost:8517/?page=Explore%20North%20Slope`.
- Verified local website counts after the OSL rebuild:
  `G10015 profiles = 184`, `Well codes = 24`, `Gradient estimates = 184`,
  `Temperature matched = 483`, and `Next-step ready = 374`.
- The next chat should not revisit OpenScienceLab proxy/browser debugging.
  Use OpenScienceLab for source/product rebuilds only, then push derived
  outputs and view them locally or on the hosted public website.
- Current stability calculation plan:
  `docs/STABILITY_CALCULATION_PLAN.md`. It locks the hydrostatic pressure
  equation, G10015/GGD223 temperature model hierarchy, methane 5 ppt phase-curve
  lookup source, confidence labels, caveats, and the `stability_screen_*.csv`
  schema.
- Phase-curve input now exists as
  `data/public_stability_products/phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1.csv`.
- Phase-curve scenario control now exists as
  `data/public_stability_products/phase_curve_scenario_catalog_2026-06-14.csv`:
  official baseline is 100 percent methane; mixed-gas chemistry remains a
  sensitivity candidate only.
- Input capability control now exists as
  `data/public_stability_products/stability_input_capability_matrix_2026-06-14.csv`:
  it separates ready public inputs, baseline assumptions, sensitivity-only
  inputs, and blocked future approved-data inputs.
- OSL pull/rebuild control now exists as
  `data/public_stability_products/stability_osl_pull_triggers_2026-06-14.csv`:
  unit-test fixture work can continue in Git, but real public temperature-model
  products require OSL because raw G10015 profile rows are not committed.
- Local temperature-model helper code now exists in
  `dashboard/stability_products.py`: it parses G10015-style profile points,
  interpolates inside measured depths, extrapolates below profile depth only
  with a supplied gradient, and returns blocked statuses when inputs are
  insufficient. It is tested with fixtures only and has not produced final
  stability top/base/thickness outputs.
- Local stability depth-grid and intersection helper code now exists in
  `dashboard/stability_products.py`: it builds an inclusive depth grid, combines
  temperature, hydrostatic pressure, and phase lookup into per-depth stability
  flags, finds synthetic top/base crossings in fixture tests, and blocks
  incomplete pressure-temperature grids. It has not been applied to the public
  scaffold.
- Local source-control confidence-label helper code now exists in
  `dashboard/stability_products.py`: fixture tests cover high, medium, low,
  blocked, and outside-AU labels. These are source-control labels only, not
  hydrate-confidence or saturation labels.
- The OSL rebuild script is now prepared to write
  `stability_temperature_model_2026-06-14.csv` and
  `stability_temperature_model_summary_2026-06-14.csv` when the full source
  bundle has raw G10015 processed profile `.txt` files. This product is one row
  per scaffold well per modeled key depth and remains
  temperature-input-only, not a stability result.
- G10015 duplicate depth rows are now handled by averaging temperature values at
  the same depth, including the OSL-observed duplicate at `8.23 m`, so the
  inventory and temperature-model rebuild can continue without hiding the
  public-source provenance.
- A guarded baseline stability-screen writer now exists in code and has been
  run in OSL. It writes one row per public scaffold well, calculates
  top/base/thickness only where all source and calculation gates pass, and
  keeps blocked rows null with explicit blocked statuses. The first committed
  baseline methane 5 ppt screen has `8,084` rows, `22` calculated intervals,
  `8` no-stable-interval rows, and `8,054` blocked rows. Every row remains
  tagged `not_hydrate_proof`.
- The first OSL screen run produced `8,084` rows but all were blocked because
  the screen grid required phase-curve coverage from `0 m`. The writer now
  starts at the phase-curve minimum covered depth and still blocks intervals
  that cannot close within the cited phase-curve maximum depth; the rerun
  produced the guarded screen counts above.
- Website end-state control now exists as
  `data/public_stability_products/stability_website_product_spec_2026-06-14.csv`:
  the final public stability view should show run assumptions, readiness gates,
  map status, selected-well audit details, temperature-phase intersections,
  result tables, scenario controls, and exports/citations without claiming
  hydrate proof, saturation, sweet spots, or validated ML results.
- The public app now exposes the guarded baseline screen with summary counts,
  status/confidence breakdowns, calculated interval rows, blocked/no-interval
  sample rows, a 2D well-status map, a calculated interval depth chart, and a
  CSV download. It also now has blank-row diagnostics and a temperature-coverage
  tab: 22 of 24 G10015 codes are located through committed GGD223 controls, 483
  rows have direct profile matches, 193 unmatched rows are within 50 km of a
  located G10015 control, and 4,917 are 50-100 km regional proxy candidates.
  Proxy tiers are planning/sensitivity labels only, not baseline calculations.
- The Calculated Intervals tab includes a selected-well temperature/phase audit
  plot using the committed methane 5 ppt phase boundary, the sampled measured
  G10015 profile points, OSL temperature key-depth product, and screen top/base
  markers where available. The sampled measured profile product has `28,020`
  rows across `184` profiles and is a visualization/audit input only.
- The public ML feature scaffold now exists:
  `data/public_stability_products/public_ml_feature_scaffold_2026-06-15.csv`,
  `public_ml_feature_scaffold_summary_2026-06-15.csv`, and
  `public_ml_feature_dictionary_2026-06-15.csv`. It has `8,084` public well
  rows, `483` matched G10015 temperature-context rows, `22` calculated
  baseline stability-interval feature rows, `8` no-stable-interval rows, and
  `0` validated hydrate occurrence/saturation labels or training-ready rows.
  The `Analyze Hydrates` page now has a Public ML Readiness tab for this real
  public feature scaffold, while synthetic interval review remains separate.
- The public target registry now exists:
  `data/public_stability_products/public_ml_target_registry_2026-06-15.csv`
  and `public_ml_leakage_guardrails_2026-06-15.csv`. It preserves the original
  target headers and codifies the existing rule that `Sgh`, `S_h`, `Sh`,
  `NMR_SAT`, `Hydrate Saturation`, `Swr`, `S_wr`, and interpreted phase labels
  are target/calibration/output fields, not input predictors. The
  `Analyze Hydrates` page now has a Target Registry & Leakage tab for this
  guardrail.
  Next scientific task: keep improving source coverage in OSL and treat any
  future phase-curve/composition variants as cited scenarios. Do not label the
  current screen as hydrate proof, saturation, producibility, or a sweet-spot
  ranking.

## Equations To Preserve

From the screenshots and slide materials, preserve equations for:

- shale volume / gamma-ray interpretation;
- density porosity;
- Vp and Vs conversion where slowness is used;
- Vp/Vs;
- acoustic impedance;
- lambda-rho;
- mu-rho;
- Young's modulus;
- Poisson's ratio;
- brittleness terms;
- NMR-density hydrate proxy;
- Archie/resistivity hydrate proxy where source-backed assumptions exist.

Important:

- Equations create features and screens.
- Equations do not prove hydrate alone.
- The deliverables need to say when an equation is a proxy, a feature, a QC screen, or a label/calibration relation.

## ML Direction

Public repo role:

- build the ML explanation, schema, equations, parameter logic, pipeline, and diagrams;
- do not claim real approved-data performance;
- do not train/report real project metrics from classified data.

Approved environment role:

- load real data;
- run final training/validation;
- compute real metrics;
- generate real outputs.

Model explanation:

- Chong et al. (2022) is the essential direct ML anchor.
- Explain ANN/Keras in plain language: a neural network learns nonlinear relationships among logs and derived features to estimate hydrate saturation.
- Explain model families only after explaining the task.
- Use baseline models as comparison points if/when synthetic or approved data are modeled.
- Validation should be by well/group/compartment rather than random depth rows when the final data allows it.

Plain-language leakage explanation:

- Target leakage means the answer column, or something derived from the answer column, accidentally enters the input features and makes the model look better than it is.
- This is why `Sgh`, `S_h`, `Sh`, `NMR_SAT`, phase labels, and final ranks need a clear role before modeling.

## Website Skeleton Direction

Website should eventually include:

- public map/GIS context;
- runtime readiness checklist;
- header/schema reference using the exact screenshot header style;
- optional synthetic/fake CSV examples only if needed later for code testing, using the same header shapes;
- parameter range explorer;
- equation-to-feature diagrams;
- target registry and leakage warning;
- placeholder model pipeline;
- placeholder outputs for occurrence, saturation, uncertainty, and review rank;
- export formats the user can later run in DOE/Anaconda.

Website should not include:

- real classified rows;
- real restricted well names;
- populated sensitive outputs;
- claims that the public version already validated the model.

## Working Definition Of Runtime

"Runtime" means the environment where the code is actually run against files.

For this project:

- Public runtime = local/GitHub-safe app using header references, public GIS context, and optional synthetic examples only if needed later.
- Approved runtime = DOE/authorized desktop or Anaconda environment where real data is loaded later.

## Work Order For Good Commits

Use small, focused commits:

1. `parameter logic/source matrix`
2. `word document update`
3. `slide deck update`
4. `website scaffold update`
5. `tests/verification`

Before each commit:

- pull/rebase `main`;
- check `git status --short`;
- avoid committing runtime data or temporary Office lock files;
- keep generated binaries only when they are intended deliverables;
- include source notes when a visual or claim changes.

## Next Work Plan

Current top-priority handoff for the PC:

1. Use
   `docs/FINAL_DELIVERABLE_CONSOLIDATION_AND_CLEANUP_PLAN_2026-06-15.md`
   before editing, uploading, deleting, or renaming Word/PowerPoint/Drive
   deliverables.
2. Use `docs/DECK_REVISION_DELEGATION_BASE_2026-06-18.md` to split the next
   work into scoped prompts for the PC, OSL, or delegated Codex chats.
3. Review the committed V5.5 Slide 2 source update presentation at
   `docs/project_blueprints/V5_5_SLIDE2_SOURCE_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Slides_2026-06-17.pptx`
   and companion at
   `docs/project_blueprints/V5_5_SLIDE2_SOURCE_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Companion_2026-06-17.docx`.
   The verified V5.5 native Google Slides and Docs review copies are
   <https://docs.google.com/presentation/d/1-35vfTIXAnWCiyKTLooJy80HBYliMBliE_z4CbggJC0>
   and
   <https://docs.google.com/document/d/1CyZkRgfAUSOOaRxXni0mcmFN2OQcc5pNOw8TOv44f0Q>.
   V5.5 carries forward the final-deck prompt requirements, restores the
   personal opener, uses source-backed slide 2 visuals, keeps slide 3 as a
   parameter-range board, restores complex workflow/runtime architecture on
   slides 4 and 7, adds the DOE prototype/model-run card, keeps stability as
   context/admissibility only, and closes with done/not-claimed/next.
   The 2026-06-18 Gmail deck attachment may supersede some visuals after it is
   downloaded and verified, but it is not committed yet.
   V5.3 is a flawed intermediate/reference, not the active deck.
   Its prior build contracts are `docs/FINAL_NEW_SLIDE_DECK_CREATION_PROMPT_2026-06-15.md`,
   with supporting rules in
   `docs/GMAIL_STYLE_V5_2_SLIDE_REMAKE_PROMPT_2026-06-15.md` and
   `docs/FINAL_NINE_SLIDE_GAP_AND_DIAGRAM_REUSE_PLAN_2026-06-15.md`.
   Do not upload, delete, archive, or rename older deliverables until the
   rebuilt deck and final Word direction are approved.
4. Review the mentor packet in
   `docs/MENTOR_DECISION_REQUESTS_2026-06-15.md` and
   `docs/MENTOR_PROJECT_STATUS_PACKAGE_V5_WORKFLOW_2026-06-15.md`.
5. Use `data/public_ml_products/approved_data_field_role_table_2026-06-15.csv`
   and `docs/APPROVED_DATA_INTAKE_SPEC_2026-06-15.md` as the public-safe
   approved-data intake contract.
6. Use `docs/FIRST_MODEL_EXPERIMENT_PLAN_2026-06-15.md` as the first approved-
   runtime model plan. It separates occurrence classification from saturation
   regression and keeps target labels out of `X_allowed`.
7. Use `dashboard/approved_data_intake.py`,
   `01_pipeline/validate_approved_data_headers.py`, and the public-safe
   templates/reports in `data/public_ml_products/` as the tested header/schema
   contract for later approved-runtime loading.
8. Keep the website in readiness mode only: public counts, diagrams, schemas,
   caveats, blocked reasons, and synthetic examples are acceptable; fake ML
   results, approved rows, trained metrics, occurrence probabilities, and
   saturation predictions are not.

Recommended next build:

1. Get mentor decisions on phase-curve policy, target authority, validation
   split, missing G10015 handling, stability-as-context policy, and public
   website output limits.
2. Recover or inspect the approved workbook/data headers inside the authorized
   environment and run the CLI header audit there using `--header-only`.
3. Confirm units, depth alignment, and target-label authority before training.
4. Copy back only reviewed public-safe readiness summaries, then extend the
   parameter logic/source matrix and Word/PPT narrative using the approved
   intake contract rather than making new synthetic datasets.

## Questions For User

Remaining questions before the next major build.

1. After the parameter logic/source matrix is built, do `Sgh`, `S_h`, `Sh`, and
   `NMR_SAT` behave as equivalent hydrate-saturation labels, or are some of
   them refined/interpreted/calibrated versions?
2. After the parameter logic/source matrix is built, what should "sweet spot"
   mean for this project: occurrence + saturation only, or occurrence +
   saturation + confidence + producibility?
3. Should each parameter's outside factors/false positives become a separate
   required row in the Word document and slide logic, or stay in the source
   matrix only?

## Current Answers Already Given

- 9 main audience topic slides: yes. Appendix plates are acceptable only when
  explicitly needed to keep the complex workflow and ML runtime diagrams whole.
- Slide 1: restore the original personal/about-me opener for the V5.5 mentor
  package.
- Slide 2: rebuild completely with source-backed hydrate/North Slope visuals;
  do not reuse the old AI-looking methane cage or PT sketch.
- Slide direction after 2026-06-17 review: use the V5.5 mentor update
  mentor-facing package, with the complex workflow and ML runtime diagrams
  restored to the main nine-slide sequence.
- Work order: Word first, slides second, website third.
- Website: skeleton for transfer into DOE/Anaconda, not final public science proof.
- Real data: no real rows in public repo; headers/screenshots only for now.
- Metrics: real metrics come later after approved-data execution.
- Fake data: do not build fake data as the next priority.
- Headers: preserve the screenshot/origin headers in the scaffold and deliverables.
- DOE project overview screenshots: official wording/evidence.
- Next build: yes, create the parameter logic/source matrix before Word/PPT.
- Dataset naming: not important right now because we only have headers, not the
  datasets. Do not foreground dataset names.
- Occurrence and saturation: yes, the DOE overview explicitly specifies both.
- Sweet spot: wait to define fully until the parameter logic and external-factor
  reasoning are built.
