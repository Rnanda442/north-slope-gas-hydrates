# Agent Start Here

Last updated: 2026-06-18

Use this file as the first read for future Codex, PC, and OpenScienceLab
sessions. It should be updated only when the project orientation,
authoritative artifacts, guardrails, tests, or next actions materially change.

## Read Order

1. `docs/AGENT_START_HERE.md`
2. `docs/CURRENT_ARTIFACT_INDEX.md`
3. `docs/PROJECT_PROMPT_LIBRARY.md` when starting a repeated workflow
4. `docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md` for current
   project/deck revision and delegated-chat work
5. `PROJECT_CONTEXT.md`
6. `docs/NORTH_SLOPE_PROJECT_BASE.md`
7. `docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md`
8. The technical docs named below for the specific task

Always run `git status --short` before edits and preserve unrelated local
changes.

## Project Purpose

- Build a scientifically defensible North Slope gas hydrate workflow for future
  occurrence classification and saturation regression.
- Connect public regional geology, permafrost, stability, well-context, and GIS
  products with a later approved-runtime well-log/core workflow.
- Keep GitHub and Streamlit public-safe: source notes, schemas, diagrams,
  public GIS/products, synthetic examples, and tested code scaffolds only.
- Keep OpenScienceLab and approved runtime as the heavy-data workbench for raw
  source bundles, approved logs/core/NMR rows, row-level calculations, training,
  and reviewed outputs.
- Preserve original headers and source context while building normalized
  variable fingerprints, `X_allowed` feature contracts, and Y-only target
  registries.
- Explain hydrate-compatible evidence using stability context, reservoir
  quality, hydrate-response logs, QC, mimics, leakage controls, and validation
  gates.
- Maintain the current Word, PowerPoint, and website story without claiming
  final scientific results before approved data and mentor review.

## Current Public vs OSL Boundary

Public GitHub / Streamlit may contain:

- public GIS layers, public stability summaries, and public ML scaffold
  products;
- source-backed docs, diagrams, prompts, builders, and reproducible figures;
- header/schema references, public-safe templates, and synthetic test rows;
- validation code that checks headers and schema readiness without reading
  approved rows;
- Word/PPTX planning deliverables that contain no approved private rows.

OpenScienceLab / approved runtime only may contain:

- approved well-log, LAS, CSV, core, pressure-core, and NMR rows;
- named restricted identifiers or private workbook rows;
- raw heavy source bundles that are ignored by Git;
- populated runtime configs, runtime logs, trained models, fitted scalers, and
  approved-data metrics;
- sensitive derived outputs, occurrence predictions, saturation predictions,
  and reviewed result maps/tables.

Copy back only reviewed public-safe summaries, schema/header reports, compact
public products, source manifests, and documentation. The runtime folder layout
and ignored-data rules are in `docs/opensciencelab_runtime_layout.md`.

## Current Authoritative Docs

- `docs/AGENT_START_HERE.md` - first-read handoff and guardrails.
- `docs/CURRENT_ARTIFACT_INDEX.md` - artifact authority, status, and edit
  safety.
- `docs/PROJECT_PROMPT_LIBRARY.md` - reusable prompts for repeated workflows.
- `docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md` - latest self-email
  project/deck direction, editable-slide rule, four-well ML scope, and copyable
  prompts for PC/OSL/delegated Codex chats.
- `docs/project_blueprints/EDITABLE_DECK_REBUILD_SOURCE_OF_TRUTH_2026-06-19.md`
  - current Drive/Gmail deck audit and the rule that the next deck pass must
  rebuild slide faces as native movable/editable objects, not full-slide
  screenshots.
- `PROJECT_CONTEXT.md` - concise living project memory.
- `docs/NORTH_SLOPE_PROJECT_BASE.md` - broader project base and deliverable
  inventory.
- `docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md` - architecture, workstreams,
  priorities, decisions, and activity log.
- `docs/FINAL_DELIVERABLE_CONSOLIDATION_AND_CLEANUP_PLAN_2026-06-15.md` -
  required before uploading, deleting, archiving, or renaming Word/PPT/Drive
  deliverables.
- `docs/FULL_PROJECT_ML_WORKFLOW_DIAGRAM.md` - current V5.5 mentor update
  workflow package source language, generated file paths, and slide-use rules.
- `docs/FINAL_NINE_SLIDE_GAP_AND_DIAGRAM_REUSE_PLAN_2026-06-15.md`,
  `docs/FINAL_NEW_SLIDE_DECK_CREATION_PROMPT_2026-06-15.md`, and
  `docs/GMAIL_STYLE_V5_2_SLIDE_REMAKE_PROMPT_2026-06-15.md` - provenance for
  the corrected V5.4/V5.5 visual/topic decisions and the older Gmail/V5.2 spine.
- `docs/APPROVED_DATA_SCHEMA_COVERAGE_AND_MODEL_ARCHITECTURE_PLAN.md`,
  `docs/APPROVED_DATA_INTAKE_SPEC_2026-06-15.md`, and
  `docs/FIRST_MODEL_EXPERIMENT_PLAN_2026-06-15.md` - current ML/schema
  readiness contract.
- `docs/OSL_APPROVED_DATA_HEADER_AUDIT_RUNBOOK_2026-06-15.md` - approved
  environment header-audit handoff.
- `docs/STABILITY_CALCULATION_PLAN.md` - stability-screen method and
  guardrails.
- `docs/SCIENCE_TO_ML_LOGIC_LADDER.md` and
  `docs/ML_PIPELINE_BASELINE_SOURCE_LEDGER.md` - science-to-ML narrative and
  source-backed pipeline decisions.
- `docs/SOURCE_VISUAL_INVENTORY_2026-06-16.md` - current slide/website visual
  provenance and QA layer.
- `docs/ANACONDA_DEPENDENCY_REQUEST_2026-06-16.md` - DOE/Anaconda environment
  package request for website, GIS, slides/docs, and future approved runtime.
- `docs/DOE_THREE_DATASET_ML_PIPELINE_RUNBOOK_2026-06-16.md` - approved-runtime
  command guide for using `curated_dataset1.xlsx` as training and
  `curated_dataset2.xlsx` / `curated_dataset3.xlsx` as external tests.
- `docs/DOE_RUNTIME_PRESENTATION_AND_MODEL_TRACKING_PLAN_2026-06-16.md` -
  current plan for showing DOE local model runs, feature exclusions, stability
  context, and package-unlocked next steps in a mentor-readable website view.

## Current Authoritative Slide and Doc Assets

- Current V5.5 Slide 2 source update mentor-facing deck:
  `docs/project_blueprints/V5_5_SLIDE2_SOURCE_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Slides_2026-06-17.pptx`
- Current V5.5 Slide 2 source update mentor-facing companion:
  `docs/project_blueprints/V5_5_SLIDE2_SOURCE_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Companion_2026-06-17.docx`
- Current V5.5 Slide 2 source update slide panels and contact sheet:
  `docs/project_blueprints/presentation_assets/v5_5_slide2_source_update_2026_06_17/`
- Current editable-deck rebuild source of truth:
  `docs/project_blueprints/EDITABLE_DECK_REBUILD_SOURCE_OF_TRUTH_2026-06-19.md`
- Verified native Google Slides/Docs review copies:
  <https://docs.google.com/presentation/d/1-35vfTIXAnWCiyKTLooJy80HBYliMBliE_z4CbggJC0>
  and
  <https://docs.google.com/document/d/1CyZkRgfAUSOOaRxXni0mcmFN2OQcc5pNOw8TOv44f0Q>
- Slide 2 source bundle:
  `docs/evidence/slide02_source_bundle_2026_06_17/`
- V5.4 corrected slide panels and contact sheet are now the source baseline
  for V5.5:
  `docs/project_blueprints/presentation_assets/v5_4_corrected_2026_06_16/`
- V5.3 mentor-facing workflow package is a flawed intermediate/reference,
  not the active mentor deck. Use it only for current counts, website captures,
  the source-visual inventory trail, and any genuinely improved source-backed
  visual:
  `docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_16_v5_3/`
- Prior Gmail-style and V5.2 workflow decks remain provenance:
  `docs/project_blueprints/North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview.pptx`,
  `docs/project_blueprints/V5_2_FULL_WORKFLOW_ML_DIAGRAM_North_Slope_Gas_Hydrate_Slides_2026-06-15.pptx`,
  and
  `docs/project_blueprints/V5_2_North_Slope_Gas_Hydrate_Full_ML_Workflow_Companion_2026-06-15.docx`.
- Current research overview Word document:
  `docs/project_blueprints/North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview.docx`
- Current pipeline status brief:
  `docs/project_blueprints/North_Slope_Gas_Hydrate_ML_Pipeline_Status_And_Forward_Workflow_2026-06-15.docx`
- Current mentor status package:
  `docs/project_blueprints/North_Slope_Gas_Hydrate_Mentor_Status_Package_V5_Workflow_2026-06-15.docx`

Latest user project/deck-direction update:

- The 2026-06-18 self-email titled `slide updates for the newest deck`
  identifies the attached
  `V5.5 Slide 3 Signal Response QC-Cleaned North Slope Gas Hydrate ML Workflow Slides 2026-06-17 (1).pptx`
  as the best review deck so far. The attachment is not committed and should
  be treated as a needs-review Gmail/Drive artifact until a future session
  explicitly downloads, verifies, and stages it.
- The next project/deck pass should follow
  `docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md`: convert whole-slide
  screenshot/raster panels into editable slide builds where practical, use
  larger source-backed or data-derived visuals, reduce on-slide source comments,
  keep high-level text editable, use a unified North Slope map, rebuild Slide 3
  around log-signal movement plus lithology/coring context, replace the
  three-dataset prototype with an equation-only slide, and make Slides 7-9 a
  guarded results/discussion plan without unsupported model or hydrate claims.
- The current ML scope is the four wells represented by the three available
  datasheets/workbooks. Future work must verify the well names/aliases,
  locations, and core/NMR/pressure-core/lithology evidence for those wells
  before finalizing the lithology, saturation, website, or model story.

Do not directly edit generated PPTX/DOCX binaries unless the user explicitly
asks. Prefer the documented builders and regenerate deliverables reproducibly.

## Current Website Sections

Primary Streamlit sections in `dashboard/app.py`:

- `Overview`
- `Explore North Slope`
  - `Regional Map`
  - `3D Structure`
  - `Data & Sources`
- `Analyze Hydrates`
  - `Public ML Readiness`
  - `Mentor Review`
  - `Schema Coverage & Architecture`
  - `Target Registry & Leakage`
  - `Interval Review`
  - `Runtime Readiness`
  - `Model Run Tracker`
  - `Presentation Exports`
  - `Methods & Evidence`
- `Project Plan`

Legacy aliases still route into these sections, including `Welcome`,
`Regional Atlas`, `Structural Explorer`, `Data Library`, `Research Framework`,
`Log Scaffold`, and `Future Well-Log Engine`.

## Current Public Data Products

Public ML products in `data/public_ml_products/`:

- `public_parameter_evidence_registry_2026-06-16.csv`
- `source_visual_inventory_2026-06-16.csv`
- `approved_schema_coverage_matrix_2026-06-15.csv`
- `approved_data_field_role_table_2026-06-15.csv`
- `approved_data_intake_template_2026-06-15.csv`
- `approved_data_intake_validation_schema_2026-06-15.csv`
- `first_model_output_schema_2026-06-15.csv`
- `approved_data_source_column_registry_template_2026-06-15.csv`
- `approved_data_well_depth_index_template_2026-06-15.csv`
- `approved_data_x_allowed_candidate_template_2026-06-15.csv`
- `approved_data_y_target_registry_template_2026-06-15.csv`
- `first_model_output_schema_template_2026-06-15.csv`
- `variable_fingerprint_template_2026-06-15.csv`
- `model_run_tracker_summary_template_2026-06-16.csv`
- `model_run_feature_audit_template_2026-06-16.csv`
- `model_run_stability_join_template_2026-06-16.csv`
- `intake_readiness_reports/demo_header_audit_2026-06-15.csv`
- `intake_readiness_reports/demo_header_audit_2026-06-15.json`

Public stability and ML scaffold products in `data/public_stability_products/`:

- `north_slope_well_stability_context_2026-06-14.csv`
- `g10015_temperature_profile_inventory_2026-06-14.csv`
- `g10015_temperature_profile_points_sampled_2026-06-14.csv`
- `stability_input_scaffold_2026-06-14.csv`
- `stability_temperature_model_2026-06-14.csv`
- `phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1.csv`
- `phase_curve_scenario_catalog_2026-06-14.csv`
- `stability_screen_2026-06-14_methane_5ppt_v1.csv`
- `stability_input_capability_matrix_2026-06-14.csv`
- `stability_osl_pull_triggers_2026-06-14.csv`
- `stability_website_product_spec_2026-06-14.csv`
- `public_ml_feature_scaffold_2026-06-15.csv`
- `public_ml_feature_dictionary_2026-06-15.csv`
- `public_ml_target_registry_2026-06-15.csv`
- `public_ml_leakage_guardrails_2026-06-15.csv`

These products are public-safe scaffolds, summaries, schemas, or guardrail
tables. They are not approved-data predictions.

## Current Tests and Expected Count

Run the full suite before committing meaningful changes:

```bash
python -m pytest
```

Expected current result: `122 passed, 2 skipped` as of the 2026-06-18
project-revision-base merge with the unified website map update. Update this
count only after verifying it locally.

Current test files:

- `tests/test_well_log_engine.py`
- `tests/test_runtime_skeleton.py`
- `tests/test_project_roadmap.py`
- `tests/test_sweet_spot_page.py`
- `tests/test_stability_sources.py`
- `tests/test_stability_products.py`
- `tests/test_stability_screen_diagnostics.py`
- `tests/test_approved_data_intake.py`
- `tests/test_approved_data_intake_cli.py`
- `tests/test_code_transfer_blocks.py`
- `tests/test_parameter_evidence_registry.py`
- `tests/test_source_visual_inventory.py`
- `tests/test_three_dataset_ml_pipeline.py`
- `tests/test_model_run_tracker.py`

## Current Guardrails

- Keep OpenScienceLab as the heavy-data workbench and GitHub/Streamlit as the
  public delivery surface.
- Do not commit approved/private rows, raw restricted bundles, populated
  runtime configs, credentials, trained models, or approved-data outputs.
- Preserve original headers and units; normalized names are secondary metadata.
- Keep `Sgh`, `S_h`, `Sh`, `NMR_SAT`, `Hydrate Saturation`, `Swr`, `S_wr`, and
  interpreted phase labels on the Y-only/target side until approved target
  authority is reviewed.
- Treat stability as admissibility/context only. It is not occurrence,
  saturation, producibility, or hydrate proof.
- Use whole-well, compartment, or geography-aware validation plans before any
  approved-data metric claim.
- Use blue slide callouts only for runtime confirmations that depend on
  approved workbook/data recovery.
- Do not delete, archive, upload, rename, or supersede older Word/PPT/Drive
  deliverables without the cleanup plan and explicit user direction.

## What Not To Claim

Do not claim:

- hydrate proof;
- final stability;
- final stability top/base/thickness;
- trained ML metrics;
- occurrence probabilities or occurrence predictions;
- saturation predictions;
- validated sweet spots, producibility, or reservoir ranking;
- final target-label authority;
- final mixed-gas or gas-composition scenario policy;
- that a file, Drive copy, test result, count, or output exists without
  verifying it locally or through the connector used.

Preferred language: `public-safe scaffold`, `schema readiness`,
`stability-admissibility`, `working screening envelope`, `target-only label`,
`runtime confirmation needed`, `mentor review needed`, and `not hydrate proof`.

## Before Editing Slides, Docs, or Website

1. Run `git pull origin main`.
2. Read this file and `docs/CURRENT_ARTIFACT_INDEX.md`.
3. Run `git status --short` and preserve unrelated changes.
4. For slides/docs, read
   `docs/FINAL_DELIVERABLE_CONSOLIDATION_AND_CLEANUP_PLAN_2026-06-15.md`,
   `docs/FINAL_NINE_SLIDE_GAP_AND_DIAGRAM_REUSE_PLAN_2026-06-15.md`, and the
   relevant prompt in `docs/PROJECT_PROMPT_LIBRARY.md`. For current delegated
   slide work, also read
   `docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md`.
5. For ML/schema work, read the approved-data intake spec, first model plan,
   field-role table, parameter evidence registry, and leakage guardrails.
6. For stability work, read `docs/STABILITY_CALCULATION_PLAN.md`, the public
   stability products README, and the OSL pull triggers.
7. Verify source files and generated assets exist before referencing them.
8. Use builders for PPTX/DOCX assets when possible, then inspect outputs.
9. Run `python -m pytest`.
10. Update `docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md` only for meaningful
    milestones, blockers, dependencies, priorities, or next-action changes.

## Where To Put New Work

- New public source packages:
  `references/<topic>/<YYYY-MM-DD>/` with a `README.md` or `source_manifest.csv`.
- Public source indexes and source-bundle notes:
  `docs/source_library_index/`.
- User-provided screenshot evidence:
  `docs/evidence/<source_or_date>/`.
- Public-safe ML schema/products:
  `data/public_ml_products/`.
- Public-safe stability/scaffold products:
  `data/public_stability_products/`.
- Public fallback map/source snapshots:
  `data/public_stability_snapshot/`.
- Raw heavy source bundles and approved runtime inputs:
  ignored OSL/runtime folders described in `docs/opensciencelab_runtime_layout.md`.
- Short copy/paste handoff snippets for DOE/Jupyter:
  `code_transfer_block/`.
- Reusable prompts:
  `docs/PROJECT_PROMPT_LIBRARY.md` for short reusable prompts, or a dated
  `docs/*_PROMPT_YYYY-MM-DD.md` file for long one-off build prompts.
- Website code:
  `dashboard/app.py`, `streamlit_app.py`, and focused helper modules under
  `dashboard/`.
- Tests:
  `tests/`, with synthetic fixtures only.
