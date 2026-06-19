# DOE ML Pipeline GitHub Reproduction Prompt Pack

Created: 2026-06-19

## Purpose

This file turns the current repo state into copyable prompts for getting the
full North Slope gas hydrate ML pipeline code onto GitHub, then running it on
the DOE laptop with the real approved datasets. It also records what can be
done with headers only and what has already been implemented in the repo.

Boundary rule: GitHub carries code, docs, schemas, templates, and row-free
public-safe review assets. The DOE laptop carries approved rows, raw workbooks,
row-level predictions, fitted scalers, trained models, local runtime manifests,
and any sensitive identifiers.

## What Already Exists In The Repo

| Area | Existing file(s) | What it does now | Needs real rows? | Current gap |
|---|---|---|---|---|
| Header scan | `01_pipeline/inspect_three_dataset_headers.py`, `dashboard/runtime/three_dataset_pipeline.py` | Scans `curated_dataset1/2/3.xlsx`, inventories sheets/headers, finds target-like columns, writes suggested model commands | Reads local approved workbooks in DOE; can also be adapted from header-only CSVs | Needs a DOE orchestration command that runs this first and records status |
| Header-only intake | `01_pipeline/validate_approved_data_headers.py`, `dashboard/approved_data_intake.py` | Validates header lists, roles, target-only fields, saturation unit convention, leakage barriers | No, headers only | Good for public GitHub and screenshots; cannot train or make real plots |
| Three-dataset ML runner | `01_pipeline/run_three_dataset_ml_pipeline.py`, `dashboard/runtime/three_dataset_pipeline.py` | Trains on one workbook, scores test workbooks, excludes target-like fields/depth/helper columns, writes metrics/predictions locally | Yes | Needs end-to-end run packaging, stronger graph exports, and final validation policy |
| Multi-saturation workflow | `code_transfer_block/multi_saturation_target_workflow.py` | Trains separate prototype regressors for each saturation-like target; writes target-by-target feature/exclusion audit | Yes | Needs to be unified with main runner outputs and review export |
| Feature engineering | `dashboard/runtime/feature_engineering.py` | Adds `vshale`, density porosity, Vp/Vs, mu-rho, lambda-rho, NMR-density separation, Archie proxy, caliper flag, stability context | Needs rows for actual values; can inspect feasibility from headers | Needs unit/QC review with real workbook metadata |
| Runtime plotting helpers | `dashboard/runtime/plotting.py` | Builds Plotly log panels and core-log crossplots from runtime dataframes | Yes | No dedicated CLI yet to export DOE well-log panels safely |
| Model run tracker | `dashboard/runtime/model_run_tracker.py`, `dashboard/app.py` | Reads ignored runtime summaries into Analyze Hydrates > Model Run Tracker | Needs local runtime summaries, not raw rows | Good for DOE local review; public deployment must not load DOE runtime |
| Row-free review export | `01_pipeline/export_model_run_review_assets.py` | Exports public-safe run summaries, feature family counts, validation counts, and PNG bar charts | Needs local summary CSVs only | Good, but should be called by a master DOE orchestrator |
| Equation-derived visuals | `01_pipeline/generate_doe_equation_derived_visuals.py` | Creates equation-derived distributions, crossplots, symbol-readiness PNG, and manifest from private table | Yes | Needs encoding cleanup in symbol labels and integration into master orchestrator |
| Slide/paper visual export | `01_pipeline/generate_slide_paper_visuals_2026_06_18.py` | Generates schema, workflow, leakage, source, limitation, and runtime-summary visuals/manifests | Can run headers/public docs; richer with DOE summaries | Needs clearer "do not commit outputs_runtime" instruction in DOE prompt |
| Tests | `tests/test_three_dataset_ml_pipeline.py`, `tests/test_model_run_tracker.py`, `tests/test_model_run_review_export.py`, `tests/test_doe_equation_derived_visuals.py`, intake/source tests | Synthetic tests cover header scan, ML runner, review export, equation visuals, source inventory | No real rows | Need tests for any new orchestrator/export CLI |

## What Can Be Done With Headers Only

Headers and screenshots are enough for:

- preserving original headers and sheet names;
- classifying columns into measured inputs, derived features, QC/context, target-only, calibration/reference, and unresolved;
- finding target leakage risks such as `Sgh`, `S_h`, `Sh`, `NMR_SAT`, `Hydrate Saturation`, `Swr`, `S_wr`, phase labels, occurrence labels;
- checking which feature families appear possible: GR, resistivity, RHOB/density porosity, NMRPHI, Vp, Vs, Vp/Vs, AI, caliper/QC, temperature/pressure/stability context;
- writing the model architecture, leakage barrier, validation plan, split policy, and DOE runtime commands;
- creating empty/schema-only output templates;
- building schematic or header-count visuals;
- deciding what code must run later on DOE.

Headers and screenshots are not enough for:

- final model training;
- real feature distributions;
- real log panels;
- real core-log crossplots;
- saturation/occurrence metrics;
- validated occurrence probabilities;
- validated saturation predictions;
- final whole-well validation;
- public row-level figures.

## Source Support For "Has This Been Done Before?"

Use these as method anchors, not project-result claims:

- Chong et al. 2022: permafrost-associated hydrate ML with well logs and NMR-derived saturation concepts; supports the feature families and leakage-safe target logic.
- Singh et al. 2021: hydrate saturation ML and optimal well-log input discussion; supports saturation regression architecture and feature selection caution.
- Chong et al. 2024 / USGS: ANN-style hydrate occurrence classification and saturation prediction architecture; supports ANN/Keras as a later method anchor, not current results.
- Aung et al. 2026: direct Alaska North Slope LWD/logging/QC context; supports GR, resistivity, sonic, NMR, and caliper/QC discussion.
- Yoneda et al. 2026: direct Alaska North Slope pressure-core/NMR/permeability support; supports core/NMR calibration and permeability/lithology review.
- Tian et al. 2023 and Li/Liu 2020: comparative hydrate ML approaches; useful for model comparison language only.
- Naim/Cook/Moortgat 2023, Dalvand/Falahat 2021, Rajabi et al. 2023: missing-log or shear-velocity estimation literature; use only if mentor approves imputation/adapters and validation.

Do not copy these papers' metrics as this project's performance. The repo can
say the code architecture follows published hydrate ML patterns, but the North
Slope model results still require DOE execution and mentor-reviewed validation.

## Prompt A - GitHub Code Audit For DOE Reproduction

```text
We are working in Rnanda442/north-slope-gas-hydrates.

Goal:
Audit whether GitHub contains every code file needed to reproduce the North
Slope gas hydrate DOE ML workflow and every row-free graph/analysis export on
the DOE laptop.

Read first:
- docs/AGENT_START_HERE.md
- docs/CURRENT_ARTIFACT_INDEX.md
- docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md
- docs/DOE_THREE_DATASET_ML_PIPELINE_RUNBOOK_2026-06-16.md
- docs/DOE_RUNTIME_PRESENTATION_AND_MODEL_TRACKING_PLAN_2026-06-16.md
- docs/opensciencelab_runtime_layout.md
- docs/ANACONDA_DEPENDENCY_REQUEST_2026-06-16.md

Inspect:
- 01_pipeline/inspect_three_dataset_headers.py
- 01_pipeline/run_three_dataset_ml_pipeline.py
- 01_pipeline/export_model_run_review_assets.py
- 01_pipeline/generate_doe_equation_derived_visuals.py
- 01_pipeline/generate_slide_paper_visuals_2026_06_18.py
- code_transfer_block/multi_saturation_target_workflow.py
- dashboard/runtime/*.py
- dashboard/approved_data_intake.py
- tests/test_three_dataset_ml_pipeline.py
- tests/test_model_run_tracker.py
- tests/test_model_run_review_export.py
- tests/test_doe_equation_derived_visuals.py

Output:
Create docs/DOE_ML_REPRODUCTION_CODE_AUDIT_2026-06-19.md with:
- code inventory table;
- what each script produces;
- command examples;
- whether it needs real DOE rows or headers only;
- what graphs/tables are already reproducible;
- what code is missing;
- what must never be committed.

Run:
- python -m py_compile all inspected 01_pipeline and dashboard/runtime scripts
- python -m pytest tests/test_three_dataset_ml_pipeline.py tests/test_model_run_tracker.py tests/test_model_run_review_export.py tests/test_doe_equation_derived_visuals.py tests/test_approved_data_intake.py

Commit and push only public-safe code/docs.
```

## Prompt B - Add One Master DOE Reproduction Orchestrator

```text
We are working in Rnanda442/north-slope-gas-hydrates.

Goal:
Create one DOE-side command that runs the full approved-runtime workflow from
real data and writes a reproducible local package under ignored outputs_runtime.
This command must not commit or expose approved rows.

Add:
- 01_pipeline/run_doe_ml_reproduction_package.py
- tests/test_doe_ml_reproduction_package.py
- docs/DOE_ML_REPRODUCTION_PACKAGE_RUNBOOK_2026-06-19.md

The orchestrator should accept:
- --data-dir
- --output-root outputs_runtime
- --model-root models_runtime
- --target auto or explicit target
- --target-task auto/regression/classification
- --model baseline/mlp
- --run-label
- --skip-model
- --skip-equation-visuals
- --skip-review-assets
- --public-safe-review-only

It should run, in order:
1. inspect_three_dataset_headers.py
2. validate/record target hints and feature families
3. run_three_dataset_ml_pipeline.py unless skipped
4. code_transfer_block/multi_saturation_target_workflow.py if saturation variants exist
5. generate_doe_equation_derived_visuals.py on a selected local feature table or workbook sheet when enough columns exist
6. export_model_run_review_assets.py
7. generate_slide_paper_visuals_2026_06_18.py for row-free slide/paper summaries
8. write a final manifest with paths, statuses, blockers, and public-safe export guidance

Guardrails:
- Do not copy raw workbook rows into GitHub paths.
- Do not write row-level predictions outside ignored outputs_runtime.
- Do not write models outside ignored models_runtime.
- Public-safe review folder must exclude predictions_*.csv, model.joblib, raw run_manifest paths, private source paths, and well identifiers unless sanitized.
- Stability remains context only.

Tests:
- Use synthetic Excel workbooks in tmp_path.
- Assert outputs_runtime/model_runtime paths are used.
- Assert public-safe review manifest excludes row-level predictions and model binaries.
- Assert target-only columns are excluded from X_allowed.

Run:
- python -m py_compile 01_pipeline/run_doe_ml_reproduction_package.py
- python -m pytest tests/test_doe_ml_reproduction_package.py tests/test_three_dataset_ml_pipeline.py tests/test_model_run_review_export.py

Commit and push.
```

## Prompt C - Add DOE Graph Export CLI For Well Logs And ML Review Figures

```text
We are working in Rnanda442/north-slope-gas-hydrates.

Goal:
Add a DOE-local graph exporter that can produce every graph needed for the
slides/Word from real data, while keeping all row-level data in ignored runtime
folders.

Add:
- 01_pipeline/export_doe_ml_graphs.py
- tests/test_export_doe_ml_graphs.py
- docs/DOE_ML_GRAPH_EXPORT_RUNBOOK_2026-06-19.md

Graph families:
1. Header/schema coverage summary.
2. Target-only leakage audit.
3. Feature-family coverage.
4. Train/test/external workbook split summary.
5. Model run tracker summary.
6. Feature-family count bar chart.
7. Exclusion reason count bar chart.
8. Validation status chart.
9. Equation-derived distributions from generate_doe_equation_derived_visuals.py.
10. Equation output crossplots.
11. Equation symbol readiness.
12. Optional well-log panels by anonymized/sanitized well label.
13. Optional core-log crossplots when approved core summary tables exist.

Inputs:
- local outputs_runtime run folders;
- local approved workbook directory;
- optional public-safe summary CSVs;
- no hardcoded laptop paths.

Outputs:
- outputs_runtime/graph_exports_<timestamp>/
- PNG and SVG where possible;
- manifest CSV and JSON;
- graph_readme.md with usage and caveats.

Safety:
- The default export must be row-free summaries only.
- Well-log panels and core-log crossplots are local DOE review only unless a
  reviewer explicitly marks them public-safe.
- Add a --sanitize-labels option that replaces well names with Well A/B/C/D.
- No private depths or raw row tables should be copied into GitHub.

Tests:
- Synthetic runtime summary tests.
- Synthetic log dataframe tests with anonymized labels.
- Assert manifest classifies each figure as public-safe, DOE-local-only, or review-required.

Run:
- python -m py_compile 01_pipeline/export_doe_ml_graphs.py
- python -m pytest tests/test_export_doe_ml_graphs.py tests/test_model_run_review_export.py

Commit and push.
```

## Prompt D - Create DOE Code Transfer Zip Without Data

```text
We are working in Rnanda442/north-slope-gas-hydrates.

Goal:
Create a GitHub-safe code-transfer package that the user can move to the DOE
laptop and run in Jupyter/Anaconda with the real datasets. The zip must contain
code, docs, templates, and tests only. It must not contain data, outputs,
models, secrets, raw PDFs, approved workbooks, row-level predictions, or private
identifiers.

Add:
- 01_pipeline/build_doe_code_transfer_package.py
- tests/test_build_doe_code_transfer_package.py
- docs/DOE_CODE_TRANSFER_PACKAGE_README_2026-06-19.md

The package should include:
- 01_pipeline/*.py needed for ML, graph, equation, and review exports;
- dashboard/runtime/*.py;
- dashboard/approved_data_intake.py;
- dashboard/parameter_evidence.py;
- code_transfer_block/*.py;
- docs runbooks and prompt packs;
- data/public_ml_products templates and registries;
- tests for runtime and exports;
- requirements/conda dependency note.

The package should exclude:
- *.xlsx, *.xls, *.xlsm, *.las, *.dlis;
- outputs_runtime, models_runtime, logs_runtime, configs_local;
- data_runtime, approved_runtime, approved_data, Northslopedatasets06052026;
- row_level_predictions, predictions_runtime, DOE_exports;
- .env files, caches, raw source bundles, heavy PDFs unless explicitly public-safe.

It should write:
- dist_runtime/north_slope_hydrates_doe_code_only_<date>.zip
- dist_runtime/code_transfer_manifest_<date>.csv
- dist_runtime/code_transfer_readme_<date>.md

Run tests and commit only the script/docs/tests, not the generated zip unless
explicitly approved.
```

## Prompt E - DOE Laptop Real-Data Execution

```text
You are running on the DOE laptop/desktop, not the public laptop. Do not assume
any absolute paths. First locate the repo and data by filename search.

Goal:
Run the North Slope gas hydrate ML workflow on the real approved three
workbooks and generate local row-free review assets for slides/Word.

Find the repo by searching for:
- north-slope-gas-hydrates
- docs/AGENT_START_HERE.md
- 01_pipeline/run_three_dataset_ml_pipeline.py
- dashboard/runtime/three_dataset_pipeline.py

Find the data by searching for:
- curated_dataset1.xlsx
- curated_dataset2.xlsx
- curated_dataset3.xlsx
- wellnametodataset.txt
- Northslopedatasets06052026

Do not copy the workbooks into GitHub. Keep them where they are or move them
only into an approved ignored DOE folder.

From the repo root:
1. git pull origin main
2. git status -sb
3. python -m py_compile 01_pipeline/inspect_three_dataset_headers.py 01_pipeline/run_three_dataset_ml_pipeline.py 01_pipeline/export_model_run_review_assets.py 01_pipeline/generate_doe_equation_derived_visuals.py code_transfer_block/multi_saturation_target_workflow.py
4. python 01_pipeline/inspect_three_dataset_headers.py --data-dir "PATH_TO_DATA"
5. Review outputs_runtime/.../target_header_hints.csv.
6. Run the best target command, for example:
   python 01_pipeline/run_three_dataset_ml_pipeline.py --data-dir "PATH_TO_DATA" --target S_h --target-task regression --model baseline --run-label doe_baseline_S_h
7. Run:
   python code_transfer_block/multi_saturation_target_workflow.py --data-dir "PATH_TO_DATA"
8. Run:
   python 01_pipeline/export_model_run_review_assets.py --project-root . --output-dir outputs_runtime/model_run_review_assets_current
9. If a reviewed local feature table exists, run:
   python 01_pipeline/generate_doe_equation_derived_visuals.py --input "PATH_TO_FEATURE_TABLE_OR_WORKBOOK" --out-dir outputs_runtime/equation_visuals_current
10. If Streamlit is available:
   streamlit run streamlit_app.py
   Then open Analyze Hydrates > Model Run Tracker.

Report:
- repo path;
- data path used;
- run folders created;
- detected target columns;
- selected target and unit convention;
- X feature columns used;
- excluded target/depth/helper columns;
- whether dataset2/3 had target labels or were predicted_unlabeled;
- row-free review assets produced;
- anything blocked.

Do not paste raw rows, predictions, well identifiers, model binaries, fitted
scalers, private paths, or approved data values into chat or GitHub.
```

## Prompt F - Headers-Only Fallback If Real Data Is Not Available

```text
We are working in Rnanda442/north-slope-gas-hydrates.

Goal:
Use only approved-data headers/screenshots/schema notes to create a public-safe
readiness package. Do not read or export row values.

Run:
python 01_pipeline/validate_approved_data_headers.py --headers "DEPTH,GR,RHOB,Rt,Vp,Vs,NMRPHI,S_h,NMR_SAT,Hydrate Saturation" --authoritative-saturation-field S_h --saturation-unit-convention fraction --output-dir outputs_runtime/header_audits --output-prefix headers_only_review

Also inspect:
- data/public_ml_products/approved_data_field_role_table_2026-06-15.csv
- data/public_ml_products/approved_schema_coverage_matrix_2026-06-15.csv
- data/public_ml_products/public_parameter_evidence_registry_2026-06-16.csv

Create:
- a header coverage table;
- a variable fingerprint table;
- X_allowed/Y-only target table;
- missing feature family list;
- code/run blockers list;
- DOE real-data execution command list.

Do not claim:
- trained model results;
- validation metrics;
- occurrence predictions;
- saturation predictions;
- real log trends.
```

## Prompt G - Source Research Check For ML Method Claims

```text
We are working in Rnanda442/north-slope-gas-hydrates.

Goal:
Check whether the planned code and figures are backed by the project source
library, and identify which source supports each model/graph decision.

Read:
- docs/SCIENCE_TO_ML_LOGIC_LADDER.md
- docs/ML_PIPELINE_BASELINE_SOURCE_LEDGER.md
- docs/ML_CITATION_PACKET_FOR_DELIVERABLES.md
- docs/source_library_index/source_manifest.csv
- docs/source_library_index/source_inventory_2026-06-17.csv if present
- references/hydrate-ml-physics-sources/2026-06-13/source_manifest.csv if present

Create:
- docs/DOE_ML_CODE_SOURCE_SUPPORT_MATRIX_2026-06-19.md

Matrix columns:
- code or graph output
- source-backed reason
- source/paper/report
- what it supports
- what it does not support
- allowed slide/Word language
- forbidden overclaim

Include at least:
- GR/lithology/reservoir quality;
- Rt/resistivity;
- RHOB/density porosity;
- NMR/NMR_SAT target logic;
- Vp/Vs/AI/mu-rho/lambda-rho;
- caliper/QC;
- P-T stability context;
- occurrence classification;
- saturation regression;
- baselines/tree models;
- ANN/Keras later;
- missing-log adapters only if mentor-approved.

Do not cite internal docs as research-paper sources. Use internal docs only as
orientation and cite real papers/reports for manuscript claims.
```

## Immediate Recommendation

Run Prompt A first to verify no code has drifted. Then run Prompt B and Prompt
C on this GitHub-side machine to add the missing orchestrator and graph export
CLI. After those are pushed, run Prompt D to build the code-only zip. Prompt E
is the DOE laptop execution prompt with real data. Prompt F is the fallback
when only headers are available. Prompt G supports the Word/slides source
matrix.
