# DOE Anaconda final kit pipeline rundown

This folder is the Git-free DOE desktop execution kit. The core inputs stay on the DOE desktop; the notebook code lives in GitHub.

## Core local inputs

Default workbook folder:

```text
C:\Users\rohan.nanda\Downloads\Northslopedatasets06052026
```

Expected Excel workbooks:

```text
curated_dataset1.xlsx
curated_dataset2.xlsx
curated_dataset3.xlsx
```

Current project assumptions:

- The three Excel workbooks are the only Excel table inputs.
- They contain the normalized well-log data for the four wells.
- Inputs are treated as already normalized; scaling is disabled by default for the random-forest baseline.
- A real measured NMR variable is not required by default.
- NMR-style support is represented by proxy features from available log parameters.
- The optional moisture/temperature CSV is searched locally from the notebook folder, workbook folder, and Downloads when a filename contains moisture/water and temperature/temp.

## Notebook 1: DOE_MASTER_FULL_PIPELINE.ipynb

### Block 0: Opening markdown

States that this is the integrated DOE desktop notebook. It explains that the notebook handles header scan, validation, proxy feature engineering, leakage-safe target handling, main train/predict runs, dataset-3 training mode, and all-saturation runs.

### Block 1: Package check and setup

Uses:

```text
pandas, numpy, scikit-learn, openpyxl, joblib
```

Creates local output folders:

```text
outputs_runtime/
models_runtime/
```

Defines:

```text
DATA_DIR
WORKBOOKS
EXPECTED_WELL_COUNT = 4
NORMALIZED_INPUTS = True
USE_REAL_NMR_IF_PRESENT = False
```

### Block 2: Schema, aliases, and contracts

Defines canonical log names, target-only columns, and header aliases. This is where messy Excel headers are mapped into model-ready names such as:

```text
GR -> gr_api
RT / RES / RDEP -> rt_ohm_m
RHOB / DEN / DENSITY -> rhob_g_cc
Vp -> vp_m_s or vp_km_s
Vs -> vs_m_s or vs_km_s
```

Also marks target-like fields such as hydrate saturation, phase labels, and occurrence labels so they do not leak into model features.

### Block 3: Loading and standardization

Reads the first non-empty sheet from each Excel workbook unless a sheet is specified. Standardizes headers and converts numeric-looking values into numeric arrays.

### Block 4: Optional moisture/temperature CSV context

Searches for a local CSV whose filename suggests moisture/water and temperature/temp. If found, it writes a preview and inventory to:

```text
outputs_runtime/moisture_temperature_context/
```

This is context-only unless later promoted into a feature workflow.

### Block 5: Validation and readiness

Checks:

- required columns
- target-only leakage fields in feature-side data
- empty tables
- missing well aliases
- expected four-well count
- depth monotonicity and duplicate depths
- missingness in normalized inputs

Writes readiness/coverage output during model runs.

### Block 6: Feature engineering and leakage policy

Creates model-side features and proxy variables. Because real NMR is disabled by default, the notebook does not require an actual NMR column. It creates proxy hydrate indicators from available normalized log variables, such as density/resistivity and density/sonic combinations when present.

It excludes:

- target columns
- target-like columns
- well/depth identifiers
- spreadsheet helper columns
- duplicate raw aliases
- real NMR columns when `USE_REAL_NMR_IF_PRESENT = False`

### Block 7: Header scan and target detection

Scans all three workbooks and writes:

```text
workbook_sheet_inventory.csv
workbook_column_inventory.csv
target_header_hints.csv
header_scan_manifest.json
```

The user should review `target_header_hints.csv` before choosing a target.

### Block 8: Main three-dataset pipeline

Default split:

```text
train: curated_dataset1.xlsx
test/predict: curated_dataset2.xlsx, curated_dataset3.xlsx
```

This block:

- loads all three workbooks
- detects or accepts the selected target
- builds leakage-safe features
- validates schema/readiness
- trains a baseline model
- writes predictions
- writes train/test metrics
- saves `model.joblib`
- writes `run_manifest.json`

### Block 9: Dataset 3 as training workflow

Used when target labels exist only in `curated_dataset3.xlsx`. It trains on dataset 3 and predicts/scans datasets 1 and 2.

### Block 10: All-saturation target workflow

Finds every saturation-like target column in every workbook/sheet and runs separate regressors. It writes:

```text
saturation_target_inventory.csv
sheet_inventory.csv
run_summary.csv
feature_columns_by_target.csv
excluded_feature_columns_by_target.csv
per-target predictions_*.csv
per-target metrics_by_sheet.csv
run_manifest.json
```

## Notebook 2: DOE_MODEL_OUTPUTS_REVIEW_AND_EXPORT.ipynb

Run this after the master notebook. It does not retrain. It reads outputs from:

```text
outputs_runtime/
models_runtime/
```

It creates paper/slide-ready files under:

```text
outputs_runtime/paper_slide_model_exports/
```

Exports include:

```text
model_run_inventory.csv
combined_model_metrics.csv
prediction_file_inventory.csv
combined_feature_columns.csv
combined_feature_policy_audits.csv
model_feature_importance.csv
figure_model_mae.png
figure_model_rmse.png
figure_model_r2.png
figure_top_feature_importance.png
figure_manifest.csv
paper_slide_deliverable_manifest.csv
```

The prediction inventory avoids displaying raw prediction rows by default. The full prediction CSVs stay in local runtime folders.

## What the final kit does not include

The final kit does not include the Streamlit UI itself, public website navigation, or full GIS atlas rendering code. Those are separate public-communication tools in the main repo. For Word/PowerPoint, this kit focuses first on trained model outputs, metrics, feature tables, and local model figures. GIS/Streamlit figure export can be added as a separate presentation-asset notebook if needed.
