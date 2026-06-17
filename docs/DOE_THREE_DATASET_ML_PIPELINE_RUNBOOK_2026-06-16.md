# DOE Three-Dataset ML Pipeline Runbook

Last updated: 2026-06-16

This runbook is for the approved DOE/Anaconda runtime only. It is designed for
the currently available three workbook package:

- `curated_dataset1.xlsx`
- `curated_dataset2.xlsx`
- `curated_dataset3.xlsx`
- optional context file: `wellnametodataset.txt`

The default experiment treats `curated_dataset1.xlsx` as the training workbook
and `curated_dataset2.xlsx` plus `curated_dataset3.xlsx` as external test
workbooks. This is intentionally stricter than a random row split because it
keeps entire recovered workbook groups separate.

## Guardrails

- Do not commit the approved workbooks, row-level predictions, fitted scalers,
  trained models, or runtime manifests.
- Runtime inputs stay in the approved DOE folder or an ignored runtime folder.
- Runtime outputs stay under `outputs_runtime/` and `models_runtime/`, which
  are ignored by Git.
- Saturation and occurrence columns are target-only. They must not enter
  `X_allowed`.
- Depth is retained for alignment/context and output review, not as a default
  normalized predictor.
- Stability remains context/admissibility only, not occurrence proof,
  saturation, or a model target.

## Default Command

From the repository root in Anaconda Prompt:

```bash
python 01_pipeline/inspect_three_dataset_headers.py
```

Run this first if the target column is unclear. It writes local CSVs under
`outputs_runtime/three_dataset_header_scan_*`:

- `workbook_sheet_inventory.csv`
- `workbook_column_inventory.csv`
- `target_header_hints.csv`
- `suggested_commands.txt`

Then run the model command:

```bash
python 01_pipeline/run_three_dataset_ml_pipeline.py --data-dir "%USERPROFILE%\Downloads\Northslopedatasets06052026"
```

That command will:

1. read the first non-empty sheet from each workbook;
2. standardize known well-log headers into canonical names;
3. detect target-like columns such as `Sgh`, `S_h`, `Sh`, `NMR_SAT`,
   `Hydrate Saturation`, occurrence, phase, or interpreted-label fields;
4. build leakage-safe numeric features from non-target predictors;
5. train a baseline model on `curated_dataset1.xlsx` if a target is available;
6. score `curated_dataset2.xlsx` and `curated_dataset3.xlsx` separately;
7. write local-only outputs under `outputs_runtime/three_dataset_ml_run_*`;
8. write the fitted model under `models_runtime/three_dataset_ml_run_*`.

## Useful Variants

If the target column is known:

```bash
python 01_pipeline/run_three_dataset_ml_pipeline.py --data-dir "%USERPROFILE%\Downloads\Northslopedatasets06052026" --target Sgh --target-task regression
```

If the scanner finds the target only in `curated_dataset3.xlsx`, use dataset 3
as training and datasets 1/2 as unlabeled prediction/external-review sets:

```bash
python 01_pipeline/run_three_dataset_ml_pipeline.py --data-dir "%USERPROFILE%\Downloads\Northslopedatasets06052026" --train curated_dataset3.xlsx --test curated_dataset1.xlsx curated_dataset2.xlsx --target S_h --target-task regression
```

If the approved target is an occurrence or phase label:

```bash
python 01_pipeline/run_three_dataset_ml_pipeline.py --data-dir "%USERPROFILE%\Downloads\Northslopedatasets06052026" --target phase_label --target-task classification
```

For a small neural-network prototype using scikit-learn MLP:

```bash
python 01_pipeline/run_three_dataset_ml_pipeline.py --data-dir "%USERPROFILE%\Downloads\Northslopedatasets06052026" --target Sgh --target-task regression --model mlp
```

Use TensorFlow/Keras later only after the environment package request is
approved and the baseline feature/target tables are confirmed.

## Multi-Saturation Prototype Command

If the available labels are all saturation variants, use the standalone transfer
workflow. It treats every saturation-like column as a separate Y-only target and
writes a feature/exclusion audit for each target:

```bash
python code_transfer_block\multi_saturation_target_workflow.py --data-dir "%USERPROFILE%\Downloads\Northslopedatasets06052026"
```

The cleaned run folder should start with:

```text
outputs_runtime\multi_saturation_clean_features_...
```

Review these files:

- `run_summary.csv` - one row per trained or blocked saturation target;
- `feature_columns_by_target.csv` - cleaned canonical X columns by target;
- `excluded_feature_columns_by_target.csv` - target-only, depth, unit/helper,
  unnamed, and raw-alias exclusions;
- `sheet_inventory.csv` - workbook/sheet row and column counts.

The cleaned feature file should not include `Depth_ft`, `DEPT`,
`depths_unit*`, `Unnamed:*`, raw `GR`, raw `RES`, raw `RHOB`, raw `VP`, or raw
`VS` as model inputs. If those appear, the old notebook cell or an older script
was run.

## Website Review Surface

After running either workflow, open the website and use:

```text
Analyze Hydrates > Model Run Tracker
```

This tab reads ignored local runtime folders under `outputs_runtime/` and shows
the run story in a presentable way:

- which run folders exist;
- which target columns trained;
- model kind, training rows, feature count, and training-fit metrics;
- run-to-run comparison across multiple local output folders;
- target-by-target cards that keep training-fit metrics separate from
  external/whole-workbook validation status;
- feature families used;
- excluded columns and why they were excluded;
- sheet/dataset inventory;
- placeholder stability-join status and how the public stability screen may
  enter the DOE workflow;
- a public-safe summary download with no row-level predictions, fitted models,
  approved workbook rows, or runtime manifest contents.

Training-fit metrics are runtime proof only. Final model claims require
whole-well validation or a locked test set.

## Expected Local Outputs

Each run writes a new ignored folder with:

- `dataset_inventory.csv` - workbook rows, columns, wells, and depth coverage;
- `schema_readiness.csv` - required-column, range, missingness, and duplicate
  checks on the feature side;
- `target_detection.csv` - detected saturation/occurrence/phase target
  candidates and the selected target;
- `feature_columns.csv` - leakage-safe numeric feature columns used by the
  model, after excluding target-like fields and depth;
- `train_metrics.csv` - training-set metric summary when training runs;
- `test_metrics.csv` - separate test metrics for dataset 2 and dataset 3;
- `predictions_curated_dataset*.csv` - local-only row-level predictions;
- `run_manifest.json` - target, model, feature, and output summary.

When a test workbook has features but no target column, the script writes
predictions and marks that workbook as `predicted_unlabeled` in
`test_metrics.csv`. That status means the model scored rows, but no held-out
metric can be claimed for that workbook.

If no target column is detected, the script still writes inventory, readiness,
target-detection, feature-column, and manifest outputs, then reports
`readiness_only`.

## What Can Be Brought Back To GitHub

After mentor or data-owner review, only public-safe summaries should be copied
back, such as:

- a row-free statement of which headers were detected;
- target-column choice and unit convention;
- feature family coverage by workbook;
- high-level metric ranges if approved for public communication;
- updated documentation, code, tests, and diagrams.

Do not copy row-level predictions, raw workbook rows, fitted models, or local
approved identifiers into GitHub or Streamlit.
