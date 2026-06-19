# DOE Jupyter Code Package 2026-06-19

This package is a GitHub-safe code transfer bundle for running the
North Slope three-workbook ML workflow on the DOE desktop or another
approved runtime machine. It contains code, docs, wrappers, and package
manifests only. It does not contain approved workbook rows, LAS files,
private well identifiers, runtime predictions, fitted models, fitted
scalers, credentialed PDFs, or private configs.

## Expected Local Data Files

Place the real approved files in a local folder outside GitHub, such as
a DOE-approved data directory:

- `curated_dataset1.xlsx`
- `curated_dataset2.xlsx`
- `curated_dataset3.xlsx`
- `wellnametodataset.txt` optional, if approved and available

Do not copy those files into this package folder unless the folder is
outside the Git worktree. Never commit them.

## Quick Start In Anaconda Prompt

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

The wrapper scripts forward arguments to the original repo entry
points while preserving the package-root import layout.

## Jupyter-Friendly Use

In a notebook cell, use shell commands from the package root:

```python
!python verify_package.py --data-dir r"<approved data folder>"
!python run_header_scan.py --data-dir r"<approved data folder>"
!python run_three_dataset_baseline.py --data-dir r"<approved data folder>" --target auto --model baseline
```

If the header scan finds a verified target column, rerun with the exact
target:

```python
!python run_three_dataset_baseline.py --data-dir r"<approved data folder>" --target "EXACT_TARGET_COLUMN" --model baseline
```

## Runtime Output Boundary

Runtime outputs belong under ignored local folders:

- `outputs_runtime/`
- `models_runtime/`
- `logs_runtime/`
- `configs_local/`

Do not push raw data, row-level predictions, trained model files,
fitted scalers, private runtime manifests, or private well identifiers
to GitHub. Public-safe summaries must be reviewed before publication.

## Included Code Areas

- Three-workbook header inspection and ML runners under `01_pipeline/`
- Multi-saturation workflow under `code_transfer_block/`
- Runtime helpers under `dashboard/runtime/`
- Approved-data intake and row-free source/model helpers under `dashboard/`
- DOE runtime/runbook docs under `docs/`

See `PACKAGE_MANIFEST.json` for the exact file list and checksums.
