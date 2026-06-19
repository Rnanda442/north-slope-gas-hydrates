# DOE Jupyter Code Package Done / Needed Handoff

## Prompt Worked On

Prompt 12: Build DOE Desktop Code Zip And Jupyter Run Package.

## Done

- Created a reproducible public-safe package builder:
  `01_pipeline/build_doe_jupyter_code_package_2026_06_19.py`
- Generated a DOE/Jupyter code transfer package:
  `outputs_public/doe_jupyter_code_package_2026_06_19/`
- Generated a local zip for transfer/review:
  `outputs_public/doe_jupyter_code_package_2026_06_19.zip`
- Included code only: three-workbook runners, multi-saturation workflow,
  runtime helpers, approved-data intake helper, source visual/model tracker
  helpers, and DOE runbook/dependency docs.
- Added Jupyter-friendly wrappers:
  `run_header_scan.py`, `run_three_dataset_baseline.py`,
  `run_model_run_review_assets.py`, and `run_multi_saturation.py`.
- Added package docs and controls:
  `README_DOE_JUPYTER_CODE_PACKAGE_2026_06_19.md`,
  `.env.example`, `.gitignore`, `PACKAGE_EXCLUDE_RULES.md`,
  `PACKAGE_MANIFEST.json`, and `verify_package.py`.
- Verified the package without reading private data rows.

## Still Needed

- Move the zip or package folder to the DOE desktop / approved runtime machine.
- Place real approved files in a local non-GitHub data folder:
  `curated_dataset1.xlsx`, `curated_dataset2.xlsx`,
  `curated_dataset3.xlsx`, and optional `wellnametodataset.txt`.
- Run Prompt 13 on the DOE desktop or another approved runtime machine.
- Review any generated public-safe summaries before deciding whether they can
  move from ignored runtime folders into GitHub or Drive.

## Package Contents

The generated manifest lists 36 package entries. Key included source areas:

- `01_pipeline/inspect_three_dataset_headers.py`
- `01_pipeline/run_three_dataset_ml_pipeline.py`
- `01_pipeline/export_model_run_review_assets.py`
- `01_pipeline/generate_doe_equation_derived_visuals.py`
- `01_pipeline/generate_slide_paper_visuals_2026_06_18.py`
- `code_transfer_block/inspect_three_dataset_headers_standalone.py`
- `code_transfer_block/multi_saturation_target_workflow.py`
- `dashboard/approved_data_intake.py`
- `dashboard/source_visual_inventory.py`
- `dashboard/parameter_evidence.py`
- `dashboard/runtime/*.py`
- DOE runtime/runbook/dependency docs under `docs/`

## Excluded Items

Excluded from the package and GitHub:

- approved workbook rows and raw workbook files;
- `.xlsx`, `.xls`, `.xlsb`, `.las`, `.dlis`, `.csv`, `.tsv`, `.parquet`,
  `.feather`;
- row-level predictions and runtime scoring tables;
- trained models, fitted scalers, serialized pipelines, and model binaries;
- credentialed PDFs, private screenshots, secrets, and local private configs;
- runtime manifests containing private absolute paths or identifiers.

The local zip is ignored by repository rules because `*.zip` is ignored. It was
created for transfer/review but should not be pushed unless explicitly reviewed
and force-added.

## Validation

Commands run:

```powershell
python 01_pipeline\build_doe_jupyter_code_package_2026_06_19.py
python -m py_compile 01_pipeline\build_doe_jupyter_code_package_2026_06_19.py
python -m py_compile <every copied package .py file>
python outputs_public\doe_jupyter_code_package_2026_06_19\verify_package.py
```

Validation results:

- Package generated: 26 copied files, 10 generated files.
- Package Python compile: 27 package Python files compiled.
- Package verifier: `status = ok`.
- Required files missing: none.
- Forbidden package files: none.
- Import checks passed for:
  `dashboard.approved_data_intake`,
  `dashboard.runtime.three_dataset_pipeline`,
  `dashboard.runtime.model_run_tracker`,
  `dashboard.source_visual_inventory`, and
  `dashboard.parameter_evidence`.
- Zip inventory: 36 entries, forbidden entries: none.
- Zip size: 94,965 bytes.

## Exact DOE Desktop Run Steps

From Anaconda Prompt or Jupyter terminal:

```powershell
conda activate north_slope_hydrates
cd <unzipped package folder>
python verify_package.py
python verify_package.py --data-dir "<approved data folder>"
python run_header_scan.py --data-dir "<approved data folder>"
python run_three_dataset_baseline.py --data-dir "<approved data folder>" --target auto --model baseline
python run_three_dataset_baseline.py --data-dir "<approved data folder>" --target auto --model mlp
python run_model_run_review_assets.py --project-root . --output-dir outputs_runtime/model_run_review_assets_current
```

If a verified target column is identified:

```powershell
python run_three_dataset_baseline.py --data-dir "<approved data folder>" --target "EXACT_TARGET_COLUMN" --model baseline
```

Runtime outputs must stay in ignored local folders such as `outputs_runtime/`
and `models_runtime/` unless separately reviewed and sanitized.

## Branch / Commit

- Branch: `codex/prompts-11-13-laptop-20260619`
- Commit: pending at handoff creation; see final response / branch history.
