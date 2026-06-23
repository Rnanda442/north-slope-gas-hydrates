# ML Equation-First V4 Status

Date: 2026-06-23

Current notebook: `notebooks/DOE_MASTER_ML_PIPELINE_EQUATION_FIRST_V4.ipynb`.

The current workflow is equation-first: standardize approved-runtime workbook columns, compute physics features before model training, run hydrate-saturation regression, run secondary water-saturation regression, and produce a rule-based hydrate-occurrence screen. A supervised occurrence classifier remains the next step once an independent occurrence label or an explicitly marked weak saturation-derived occurrence label is added.

Public repo boundary: keep real runtime inputs, outputs, predictions, configs, and trained models out of Git. Runtime outputs stay under ignored local folders.

## Current target structure

| Output | Type | Current status |
|---|---|---|
| Hydrate saturation | Regression | Active |
| Water / residual-water saturation | Regression | Active as secondary two-well transfer |
| Hydrate occurrence | Rule-based screen | Active as screen only; supervised classifier pending occurrence labels |

## Current runtime output set

```text
outputs_runtime/ml_master/model_results.xlsx
outputs_runtime/ml_master/predictions.csv
outputs_runtime/ml_master/paper_figures.pdf
outputs_runtime/ml_master/run_manifest.json
models_runtime/ml_master/selected_models.joblib
```

These runtime outputs are intentionally ignored and should not be committed.
