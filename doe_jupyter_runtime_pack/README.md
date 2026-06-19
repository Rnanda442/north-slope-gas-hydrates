# DOE Jupyter Runtime Pack

This folder is the GitHub-downloadable handoff for running the North Slope gas
hydrate ML workflow on the DOE desktop in Anaconda/Jupyter.

It contains code and templates only. It does not contain approved workbook
rows, raw DOE data, row-level predictions, fitted models, credentials, or
runtime outputs.

## Intended Use

1. Download or pull the full GitHub repo on the DOE desktop.
2. Open this folder in JupyterLab or Anaconda Prompt.
3. Copy `runtime_config.template.json` to a local ignored file such as
   `configs_local/doe_jupyter_runtime_config.json`.
4. Edit the local config so `data_dir` points to the DOE folder containing:
   - `curated_dataset1.xlsx`
   - `curated_dataset2.xlsx`
   - `curated_dataset3.xlsx`
   - optional `wellnametodataset.txt`
5. Open `DOE_JUPYTER_RUNTIME_ML_GRAPHS.ipynb` and run the cells.

If you prefer the command line, run:

```bash
python doe_jupyter_runtime_pack/run_public_safe_ml_graph_exports.py --config configs_local/doe_jupyter_runtime_config.json
```

## What This Pack Runs

The notebook and runner call the existing repo scripts:

- `01_pipeline/inspect_three_dataset_headers.py`
- `code_transfer_block/multi_saturation_target_workflow.py`
- `01_pipeline/run_three_dataset_ml_pipeline.py` when a target is chosen
- `01_pipeline/export_model_run_review_assets.py`
- `01_pipeline/generate_slide_paper_visuals_2026_06_18.py`
- `01_pipeline/generate_doe_equation_derived_visuals.py` when an approved
  equation-input table is supplied locally

## Main Outputs

Runtime outputs are written under ignored local folders:

- `outputs_runtime/doe_jupyter_pack_<timestamp>/header_scan/`
- `outputs_runtime/doe_jupyter_pack_<timestamp>/multi_saturation/`
- `outputs_runtime/doe_jupyter_pack_<timestamp>/single_target_pipeline/`
- `outputs_runtime/doe_jupyter_pack_<timestamp>/model_run_review_assets/`
- `outputs_runtime/doe_jupyter_pack_<timestamp>/equation_visuals/`

The Word/slide graph families are listed in
`ML_GRAPH_OUTPUT_CHECKLIST.md`.

## Guardrails

- Saturation-like columns are Y-only targets, not predictors:
  `Sgh`, `S_h`, `Sh`, `NMR_SAT`, `Hydrate Saturation`, `Swr`, `S_wr`,
  interpreted phase labels, occurrence labels, and similar target variants.
- Depth is an alignment/context axis unless mentor review approves predictor
  use.
- Numeric predictors are scaled inside train-only pipelines, not globally
  before splitting.
- Stability is admissibility/context only. It is not hydrate proof,
  occurrence proof, saturation proof, or producibility proof.
- Do not push runtime outputs, raw workbooks, row-level predictions, fitted
  models, local configs, or approved identifiers back to GitHub.

