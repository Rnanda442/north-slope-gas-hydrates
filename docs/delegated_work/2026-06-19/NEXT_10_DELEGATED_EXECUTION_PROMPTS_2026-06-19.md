# Next 10 Delegated Execution Prompts 2026-06-19

These prompts continue from `docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md`
and `docs/delegated_work/2026-06-19/ALL_PROMPTS_GITHUB_VISIBILITY_AUDIT_2026-06-19.md`.

Use one prompt per delegated chat. The goal is to keep four working chats moving
together: laptop source-search chats, PC/DOE runtime chats, deck-build chats,
and GitHub integration chats.

Common rules for all prompts:

- Do not assume laptop paths exist on the PC, DOE desktop, or another machine.
- First discover the repo and relevant source/data locations on that machine.
- Use GitHub for public-safe code, prompts, manifests, builders, tests, and
  row-free derived assets.
- Keep approved data rows, private identifiers, raw workbooks, runtime outputs,
  row-level predictions, trained models, fitted scalers, credentialed PDFs, and
  heavy raw source bundles out of GitHub.
- Whole-slide screenshots are not acceptable as final editable slides. Final
  deck builds should use editable text boxes, labels, arrows, cards, circles,
  legends, and callouts wherever practical. Maps/source figures/plots may
  remain high-resolution image objects.
- Stability is context/admissibility only. Do not claim hydrate proof,
  occurrence, saturation, producibility, final stability, trained metrics, or
  sweet-spot ranking.
- Each delegated chat must write a `done_needed` handoff under
  `docs/delegated_work/2026-06-19/`, commit/push public-safe outputs when asked,
  and report branch, commit, files, tests, done, and needed.

## Prompt 12: Build DOE Desktop Code Zip And Jupyter Run Package

```text
We are working in Rnanda442/north-slope-gas-hydrates.

Goal:
Create a GitHub-safe code package that can be moved to the DOE desktop and run
in Anaconda/Jupyter against the real local datasets. This prompt packages code,
not data.

First:
1. Find REPO_ROOT on this machine by locating `docs/AGENT_START_HERE.md`,
   `PROJECT_CONTEXT.md`, `01_pipeline`, `dashboard`, and `code_transfer_block`.
2. Run:
   git status -sb
   git remote -v
   git fetch --all --prune
   git branch -vv
3. Read:
   docs/AGENT_START_HERE.md
   docs/CURRENT_ARTIFACT_INDEX.md
   docs/opensciencelab_runtime_layout.md
   docs/DOE_THREE_DATASET_ML_PIPELINE_RUNBOOK_2026-06-16.md
   docs/DOE_RUNTIME_PRESENTATION_AND_MODEL_TRACKING_PLAN_2026-06-16.md
   docs/delegated_work/2026-06-19/ALL_PROMPTS_GITHUB_VISIBILITY_AUDIT_2026-06-19.md

Task:
Create a DOE transfer package under a public-safe folder such as
`dist/doe_jupyter_code_package_2026_06_19/` or
`outputs_public/doe_jupyter_code_package_2026_06_19/`.

The package should include:
- source code needed to run the three-workbook ML workflow;
- notebook or Jupyter-friendly `.py` runner wrappers;
- a README with exact commands;
- expected dataset filenames, never hardcoded paths;
- `.env.example` or config template with blank values only;
- a manifest listing every included file;
- a verification script that checks imports and expected filenames;
- clear instructions for where real DOE data should be placed locally;
- a `.gitignore` or package note confirming datasets, runtime outputs, models,
  fitted scalers, row predictions, and private configs are excluded.

Include or reference these code areas if present:
- `01_pipeline/inspect_three_dataset_headers.py`
- `01_pipeline/run_three_dataset_ml_pipeline.py`
- `code_transfer_block/multi_saturation_target_workflow.py`
- `dashboard/runtime/three_dataset_pipeline.py`
- `dashboard/runtime/model_run_tracker.py`
- `dashboard/approved_data_intake.py`
- graph/visual export code under `01_pipeline/` and `dashboard/runtime/`
- source visual inventory / model tracker helpers needed for row-free exports.

Create a zip file from the package, but do not include real datasets or runtime
outputs. Use a manifest to prove what is inside the zip.

Validation:
- Run `python -m py_compile` on every copied `.py` file if practical.
- Run any lightweight no-data smoke test.
- Inspect the zip manifest to confirm no `.xlsx`, `.las`, `.csv` data rows,
  model binaries, secrets, runtime predictions, or private paths are included.

GitHub outputs:
- Commit only the package builder script, README, manifest template, and/or
  public-safe zip if small enough and confirmed safe.
- If the zip is too large or should stay local, commit only the builder and
  manifest, and report the local zip path.

Handoff:
Write `docs/delegated_work/2026-06-19/doe_jupyter_code_package_done_needed.md`
with branch, commit, package path, zip path, tests, included files, excluded
items, and exact DOE desktop run steps.
```

## Prompt 13: DOE Jupyter Real-Data Runtime Execution And Public-Safe Export

```text
We are working on the DOE desktop or approved runtime machine.

Goal:
Run the GitHub code against the real local DOE datasets in Anaconda/Jupyter and
produce local ML graphs, summaries, and audit outputs. Do not push raw data or
row-level outputs.

First:
1. Locate REPO_ROOT on this machine. Do not assume any laptop path.
2. Locate the real local datasets by filename or user-provided folder. Expected
   names may include:
   curated_dataset1.xlsx
   curated_dataset2.xlsx
   curated_dataset3.xlsx
   wellnametodataset.txt
3. Run:
   git status -sb
   git fetch --all --prune
   git branch -vv
4. Read:
   docs/AGENT_START_HERE.md
   docs/opensciencelab_runtime_layout.md
   docs/DOE_THREE_DATASET_ML_PIPELINE_RUNBOOK_2026-06-16.md
   docs/DOE_RUNTIME_PRESENTATION_AND_MODEL_TRACKING_PLAN_2026-06-16.md
   docs/delegated_work/2026-06-19/ALL_PROMPTS_GITHUB_VISIBILITY_AUDIT_2026-06-19.md

Task:
Run the approved-runtime workflow locally using the real datasets:
- header inspection;
- schema discovery;
- target-only leakage audit;
- train/test/external-score setup according to the existing code;
- train-only preprocessing/scaling;
- baseline and ANN/MLP workflow if supported by the repo and installed packages;
- model run tracker summaries;
- graph/visual generation for feature coverage, excluded features, validation
  readiness, target coverage, and model-run review.

Important:
- Runtime outputs stay under ignored folders such as `outputs_runtime/` and
  `models_runtime/`.
- Do not copy raw rows, row-level predictions, fitted models, fitted scalers,
  runtime manifests with private paths, or private well identifiers into GitHub.
- If a summary can be public-safe, create a reviewed export folder such as
  `outputs_runtime/public_safe_review_candidates/` and list it for mentor/user
  review before pushing anything.

Expected local outputs:
- workbook/sheet/header inventory;
- target-like column inventory;
- feature-exclusion audit;
- leakage audit;
- model run tracker summary;
- feature-family coverage plots;
- validation-readiness plots;
- equation-derived visual plots if available;
- no row-level predictions in GitHub.

Validation:
- Run the repo tests that do not require private data.
- Run the pipeline smoke check with real local paths.
- Open generated graphs locally and note which are useful for Slide 8 / Word.

Handoff:
Write `docs/delegated_work/2026-06-19/doe_real_data_runtime_execution_done_needed.md`.
Commit only the handoff and any reviewed public-safe code fixes/templates.
Do not commit runtime data outputs unless explicitly reviewed and sanitized.
```

## Prompt 14: Four-Well Core, Lithology, NMR, And Location Source Hunt

```text
We are working in Rnanda442/north-slope-gas-hydrates on either laptop or PC.

Goal:
Find source evidence for the four-well ML scope: real well names, aliases,
locations, lithology, core/NMR/pressure-core evidence, saturation explanation,
and field/trend context.

First:
1. Do not assume paths. Search local, OneDrive, Downloads, Drive-mounted, and
   repo folders for source packages and screenshots.
2. Run:
   git status -sb
   git fetch --all --prune
3. Read:
   docs/AGENT_START_HERE.md
   docs/CURRENT_ARTIFACT_INDEX.md
   docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md
   docs/delegated_work/2026-06-19/ALL_PROMPTS_GITHUB_VISIBILITY_AUDIT_2026-06-19.md
   docs/ML_PIPELINE_BASELINE_SOURCE_LEDGER.md
   docs/SCIENCE_TO_ML_LOGIC_LADDER.md
   docs/source_library_index/README.md if present

Search targets:
- MTE, Mount Elbert, Mt. Elbert, Well-MTE
- IGS, Ignik Sikumi, Well-IGS
- MLK, ETG, Eileen Gas Hydrate Trend
- Hydrate-01, Hydrate-02, Kuparuk, Prudhoe Bay, Milne Point, Mount Elbert,
  Ignik Sikumi
- pressure core, NMR, T2, permeability, lithology, clean sandstone, core,
  porosity, hydrate saturation, grain size
- Aung 2026, Yoneda 2026, Collett, Boswell, Waite, Lee, Haines, Dallimore,
  Hunter, Ruppel, USGS, NETL, DOE, OSTI

Task:
Create a source-evidence table with:
verified well name | alias | source title | local/Drive path | page/figure/table |
location/field/trend | lithology evidence | core/NMR/pressure-core evidence |
saturation evidence | public-safe use | Drive/OSL-only restriction |
remaining gap.

Rules:
- Use formal papers/reports/datasets for scientific claims.
- Screenshots can be evidence pointers but not formal manuscript citations.
- Do not transcribe approved rows or private values.
- If the source shows row-level private data, summarize only the source type and
  leave the details Drive/OSL-only.

Output:
- `docs/source_library_index/FOUR_WELL_CORE_LITHOLOGY_SOURCE_HUNT_2026-06-19.md`
- optional CSV source table under `docs/source_library_index/` if public-safe.
- `docs/delegated_work/2026-06-19/four_well_core_lithology_source_hunt_done_needed.md`

Commit and push only public-safe manifests/notes. Do not push raw PDFs unless
license/size/public-safe status is explicitly approved.
```

## Prompt 15: Header-Only Four-Well Workbook Mapping

```text
We are working on the DOE desktop or approved runtime machine.

Goal:
Use the real local Excel workbooks to create a header-only mapping from the
three curated datasets to the four active wells or working cases. This is a
metadata export only, not a data export.

First:
1. Find REPO_ROOT and dataset locations. Do not assume paths.
2. Read:
   docs/AGENT_START_HERE.md
   docs/opensciencelab_runtime_layout.md
   docs/DOE_THREE_DATASET_ML_PIPELINE_RUNBOOK_2026-06-16.md
   docs/APPROVED_DATA_INTAKE_SPEC_2026-06-15.md
   docs/delegated_work/2026-06-19/ALL_PROMPTS_GITHUB_VISIBILITY_AUDIT_2026-06-19.md
3. Run:
   git status -sb
   git fetch --all --prune

Task:
Inspect only workbook metadata, sheet names, headers, named ranges if visible,
and safe workbook properties. Do not export data rows.

Produce:
- sheet inventory;
- workbook-to-well/case mapping if names/aliases are visible;
- original headers by workbook/sheet;
- target-like headers;
- feature-like headers;
- depth/alignment columns;
- whether `MTE_refined`, `IGS_refined`, MLK, ETG, or other names are sheets,
  wells, aliases, processing stages, or unresolved;
- unit row/header notes if visible without exposing data rows;
- whether saturation targets are fractions 0-1, as stated by user, if workbook
  metadata confirms it.

Allowed outputs:
- Header-only CSV/JSON under ignored runtime first.
- After review, sanitized public-safe summary CSV/MD under `data/public_ml_products/`
  or `docs/delegated_work/`.

Not allowed:
- Raw data rows.
- Private workbook paths in committed outputs.
- Named restricted identifiers unless already public-safe or sanitized.
- Row-level predictions, fitted models, or runtime metrics.

Handoff:
Write `docs/delegated_work/2026-06-19/header_only_four_well_workbook_mapping_done_needed.md`.
Commit only sanitized metadata reports and the handoff after review.
```

## Prompt 16: Native Editable Deck Master Builder

```text
We are working in Rnanda442/north-slope-gas-hydrates.

Goal:
Create the master native-editable deck rebuild system so the user can manually
move text, labels, arrows, callouts, and cards in PowerPoint/Google Slides.
Do not rely on old whole-slide screenshot panels as final slides.

First:
1. Run:
   git status -sb
   git fetch --all --prune
   git branch -vv
2. Read:
   docs/AGENT_START_HERE.md
   docs/CURRENT_ARTIFACT_INDEX.md
   docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md
   docs/delegated_work/2026-06-19/ALL_PROMPTS_GITHUB_VISIBILITY_AUDIT_2026-06-19.md
   docs/delegated_work/2026-06-19/main_codex_prompt2_editable_deck_done_needed.md
     from `origin/codex/delegated-main_codex_thread-20260618` if not local
   docs/FINAL_NINE_SLIDE_GAP_AND_DIAGRAM_REUSE_PLAN_2026-06-15.md

Task:
Build a new editable-deck generator or rebuild path. The output should be a
new candidate deck, not an overwrite of the active V5.5 baseline.

Requirements:
- Keep the nine-slide spine.
- Keep source figures/maps/plots as high-resolution image objects.
- Make titles, subtitles, callouts, labels, arrows, legends, cards, circles,
  and status text native editable objects.
- Add an editability audit that reports per slide:
  slide number, shape count, picture count, text shape count, connector count,
  whether it is a one-picture full-slide raster, and pass/fail.
- Generate a contact sheet and PNG previews for visual QA.
- Write an implementation note explaining how manual PowerPoint/Google Slides
  edits should be made.

Do not finalize science content in this prompt. This is the reusable build
system for Prompts 17-21.

Validation:
- Run py_compile on the builder.
- Run or add tests for the editability audit.
- Verify no slide is only one full-slide image unless it is explicitly marked
  as a complex appendix/reference slide.

Outputs:
- new builder under `docs/project_blueprints/`;
- new candidate PPTX under `docs/project_blueprints/`;
- previews under `docs/project_blueprints/presentation_assets/`;
- `docs/delegated_work/2026-06-19/native_editable_deck_master_builder_done_needed.md`.

Guardrails:
No approved rows, raw attachments, fake metrics, final predictions, or
unsupported hydrate claims.
```

## Prompt 17: Editable Slides 1 And 2 Final Context Build

```text
We are working in Rnanda442/north-slope-gas-hydrates.

Goal:
Build Slides 1 and 2 as editable candidate slides using the native editable
deck builder. Slide 1 is the clean opener. Slide 2 is methane hydrate and
Alaska North Slope context.

First read:
docs/AGENT_START_HERE.md
docs/CURRENT_ARTIFACT_INDEX.md
docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md
docs/delegated_work/2026-06-19/slide2_methane_hydrate_context_rebuild_done_needed.md
docs/project_blueprints/SLIDE2_CONTEXT_IMPLEMENTATION_NOTES_2026-06-17.md if present
docs/STABILITY_CALCULATION_PLAN.md

Slide 1 requirements:
- Remove any RapCaviar content.
- Do not use the old personal photo.
- Leave a clean editable photo placeholder for the user to manually replace.
- Keep title, subtitle, author/name/institution/date as editable text.
- Keep guardrail wording concise: workflow/readiness, not final predictions.

Slide 2 requirements:
- Use the current candidate Slide 2 rebuild assets as source material:
  `docs/project_blueprints/presentation_assets/slide2_methane_context_2026_06_19/`
- Use the unified 2D North Slope map.
- Use a CSV-derived P-T diagram.
- Use the Structure I/II/H source figure only after caption/rights review; keep
  Structure I callout editable.
- Include thermogenic vs biogenic gas language and resource motivation.
- Keep source citations in notes/Word, not tiny slide text.
- Do not use "project website" wording.
- Use "P-T diagram", not "P-T gate".
- Stability remains context/admissibility only.

Output:
- editable Slides 1-2 in the candidate deck;
- PNG preview/contact sheet;
- editability audit for Slides 1-2;
- handoff `docs/delegated_work/2026-06-19/editable_slides_1_2_done_needed.md`.

Validation:
- Programmatically verify Slides 1 and 2 contain editable text and shapes.
- Visually inspect previews.
- Run relevant builder tests.
```

## Prompt 18: Editable Slide 3 Log Signal, Core, And Lithology Build

```text
We are working in Rnanda442/north-slope-gas-hydrates.

Goal:
Build Slide 3 as the main visual explanation of log signals, lithology, and
core/NMR calibration. It must be editable enough for the user to move labels
and callouts manually.

First read:
docs/AGENT_START_HERE.md
docs/CURRENT_ARTIFACT_INDEX.md
docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md
docs/delegated_work/2026-06-19/ALL_PROMPTS_GITHUB_VISIBILITY_AUDIT_2026-06-19.md
docs/delegated_work/2026-06-19/main_codex_slide5_integration_done_needed.md
data/public_ml_products/public_parameter_evidence_registry_2026-06-16.csv
docs/SCIENCE_TO_ML_LOGIC_LADDER.md
docs/ML_PIPELINE_BASELINE_SOURCE_LEDGER.md

Task:
Create an editable Slide 3 candidate. If verified real four-well/core data are
not available yet, build a source-backed placeholder scaffold with no private
rows and clear "DOE export placeholder" areas.

Required visual:
- central well-log style panel with tracks for GR, resistivity, density/porosity,
  NMR/density separation if available, Vp, Vs, Vp/Vs, and impedance/stiffness;
- lithology column showing clean sand, shale/mixed, and uncertain intervals;
- core/NMR/pressure-core calibration strip as target/reference evidence;
- caliper/washout QC strip as caution only;
- integrated editable callouts attached to curve movement;
- no equations and no ML architecture on this slide.

If DOE real-data exports are available:
- Use only reviewed public-safe PNG/summary exports.
- Do not commit row-level data, private depth rows, or private identifiers.

If DOE real-data exports are not available:
- Create a visually honest scaffold labeled as a placeholder/export target.
- Do not imply final data or final hydrate intervals.

Output:
- editable Slide 3 candidate in deck;
- visual export PNG;
- any skeleton DOE export script needed to create future public-safe log panels;
- source/claim notes;
- handoff `docs/delegated_work/2026-06-19/editable_slide3_log_lithology_done_needed.md`.
```

## Prompt 19: Editable Slides 4 And 5 Architecture And Equations Build

```text
We are working in Rnanda442/north-slope-gas-hydrates.

Goal:
Build Slide 4 as a simplified audience ML architecture and Slide 5 as an
equation-only slide. Both must be editable enough for manual layout changes.

First read:
docs/AGENT_START_HERE.md
docs/CURRENT_ARTIFACT_INDEX.md
docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md
docs/APPROVED_DATA_SCHEMA_COVERAGE_AND_MODEL_ARCHITECTURE_PLAN.md
docs/FIRST_MODEL_EXPERIMENT_PLAN_2026-06-15.md
docs/DOE_THREE_DATASET_ML_PIPELINE_RUNBOOK_2026-06-16.md
docs/STABILITY_CALCULATION_PLAN.md
docs/delegated_work/2026-06-19/main_codex_thread_done_needed.md
docs/delegated_work/2026-06-19/main_codex_slide5_integration_done_needed.md

Slide 4 requirements:
- simple audience-facing workflow with editable boxes/arrows;
- inputs: logs, core/NMR, stability/context, lithology/QC;
- preparation: original headers/units, depth alignment, QC, fingerprints;
- leakage barrier separating X inputs from occurrence/saturation targets;
- two model outputs: occurrence classification and saturation regression;
- validation before metrics;
- reviewed outputs only.

Slide 5 requirements:
- equations only;
- no map, no ML diagram, no well-log panel;
- real fraction formatting or high-quality equation objects;
- editable labels under symbols;
- source-role coloring for logs/core/context/derived;
- equation candidates: pressure-depth, P-T stability lookup, Vp/Vs, acoustic
  impedance, mu-rho, lambda-rho, density porosity, and Archie-style relation
  only if source/input/target role is verified.

Validation:
- Run editability audit for Slides 4-5.
- Verify no fake formulas or unsupported final claims.
- Run py_compile/tests for any builder changes.

Output:
- editable Slides 4-5 candidate;
- PNG previews/contact sheet;
- equation source note;
- handoff `docs/delegated_work/2026-06-19/editable_slides_4_5_architecture_equations_done_needed.md`.
```

## Prompt 20: Editable Slides 6 And 7 Evidence Review And Stability Context

```text
We are working in Rnanda442/north-slope-gas-hydrates.

Goal:
Build Slide 6 as a high-level evidence-review board and Slide 7 as the
stability/context map slide. Both must be editable enough for manual movement.

First read:
docs/AGENT_START_HERE.md
docs/CURRENT_ARTIFACT_INDEX.md
docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md
docs/STABILITY_CALCULATION_PLAN.md
docs/delegated_work/2026-06-18/SLIDE_FINISHING_NEEDS_2026-06-18.md
docs/project_blueprints/presentation_assets/website_well_maps_2026_06_18/README.md
docs/delegated_work/2026-06-19/main_codex_thread_done_needed.md

Slide 6 requirements:
- high-level four-well evidence-review board;
- no dense equation grid;
- integrated visual lanes for lithology/core, logs, QC, stability context, and
  target-only review;
- concise one-sentence takeaway;
- details and citations moved to Word/speaker notes.

Slide 7 requirements:
- use the unified North Slope map or stability/context map;
- map is context only, not an ML overlay;
- no occurrence/saturation/producibility/ranking language;
- editable caption, legend labels, arrows, and callouts;
- room for manual label movement.

Output:
- editable Slides 6-7 candidate;
- PNG previews/contact sheet;
- source/caveat notes;
- handoff `docs/delegated_work/2026-06-19/editable_slides_6_7_evidence_map_done_needed.md`.

Validation:
- Editability audit for Slides 6-7.
- Visual check for no tiny text and no overlapping boxes.
- Source/caveat review.
```

## Prompt 21: Editable Slides 8 And 9, Final Deck Assembly, And Word Sync

```text
We are working in Rnanda442/north-slope-gas-hydrates.

Goal:
Build Slides 8 and 9 as guarded results/discussion and close slides, then
assemble the latest editable candidate deck and sync the Word companion notes.

First read:
docs/AGENT_START_HERE.md
docs/CURRENT_ARTIFACT_INDEX.md
docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md
docs/delegated_work/2026-06-19/ALL_PROMPTS_GITHUB_VISIBILITY_AUDIT_2026-06-19.md
docs/DOE_RUNTIME_PRESENTATION_AND_MODEL_TRACKING_PLAN_2026-06-16.md
docs/project_blueprints/append_v55_companion_source_notes.py
docs/delegated_work/2026-06-19/word_companion_science_support_done_needed.md

Slide 8 requirements:
- planned result-review logic, not fake results;
- show what DOE runtime will export: feature audit, excluded features, target
  coverage, validation readiness, uncertainty flags, core/log/lithology review,
  and separate occurrence/saturation lanes;
- use placeholders or reviewed row-free summaries only;
- no trained metrics or final predictions unless mentor-reviewed and approved.

Slide 9 requirements:
- clear built / not claimed / next actions close;
- built: public maps, stability context, schema/runtime scaffold, source-backed
  slide/Word system, DOE code path;
- not claimed: hydrate proof, final stability, occurrence predictions,
  saturation predictions, trained metrics, producibility/ranking;
- next: DOE run, four-well verification, mentor target authority, validation
  split, public-safe output approval.

Final assembly:
- combine Slides 1-9 into the latest editable candidate deck;
- generate PNG previews and contact sheet;
- run editability audit across all slides;
- verify no slide is only one full-slide screenshot unless explicitly allowed
  as a complex reference figure;
- rerun `append_v55_companion_source_notes.py` or update the companion so
  detailed science/source notes stay in Word/end material;
- update artifact/source visual indexes if the candidate deck becomes the new
  review package.

Validation:
- py_compile changed builders;
- relevant pytest subset;
- visual inspection of every slide preview;
- scan for forbidden claims and private-data leakage.

Output:
- final editable candidate PPTX;
- Word companion update or sync note;
- contact sheet and slide PNGs;
- editability audit CSV/MD;
- handoff `docs/delegated_work/2026-06-19/editable_slides_8_9_final_assembly_done_needed.md`.

Guardrails:
Do not commit approved rows, row-level predictions, runtime metrics unless
approved as public-safe, trained models, fitted scalers, raw Gmail attachments,
or heavy raw source bundles.
```
