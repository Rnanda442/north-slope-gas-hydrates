# DOE Anaconda final kit

Use this folder on the DOE desktop when Git is not available.

Open only:

```text
DOE_MASTER_FULL_PIPELINE.ipynb
```

The folder is intentionally a one-notebook execution kit. The master notebook now contains both the ML training workflow and the trained-model output/figure export workflow.

Default input folder:

```text
C:\Users\rohan.nanda\Downloads\Northslopedatasets06052026
```

Expected Excel inputs:

```text
curated_dataset1.xlsx
curated_dataset2.xlsx
curated_dataset3.xlsx
```

Project assumptions built into the notebook:

- The three Excel workbooks are the only Excel tables used.
- The workbooks hold the normalized data for the four wells.
- The workflow does not require Git on the DOE desktop.
- The workflow assumes no real measured NMR variable is required.
- NMR-style support is handled through well-log proxy features only.
- Optional moisture/temperature CSV context can be added later, but the current priority outputs are trained ML outputs.
- Outputs write to local `outputs_runtime/` and `models_runtime/` folders.
- Paper/slide-ready ML summaries and figures write to `outputs_runtime/paper_slide_model_exports/`.

Expected Anaconda packages:

```text
pandas
numpy
scikit-learn
openpyxl
joblib
matplotlib
```

Notebook sections:

1. Setup and package check
2. Chong-inspired ML result plot plan
3. Schema, aliases, and project assumptions
4. Loading and header standardization
5. Validation/readiness checks
6. Feature engineering and proxy features
7. Header scan
8. Main three-dataset ML run
9. Dataset 3 as training run
10. All saturation-like target run
11. Integrated trained-output review and export
12. End-of-pipeline ML figures for Word/PowerPoint

Generated ML result tables and figures include:

```text
model_run_inventory.csv
combined_model_metrics.csv
prediction_file_inventory.csv
combined_feature_columns.csv
combined_feature_policy_audits.csv
model_feature_importance.csv
combined_saturation_target_run_summary.csv
figure_predicted_vs_reference.png
figure_residual_histogram.png
figure_predicted_output_by_depth.png
figure_top_feature_importance.png
figure_model_mae.png
figure_model_rmse.png
figure_model_r2.png
figure_all_saturation_train_mae.png
figure_all_saturation_train_rmse.png
figure_all_saturation_train_r2.png
figure_manifest.csv
paper_slide_deliverable_manifest.csv
```

Do not commit approved workbook rows, prediction rows, fitted models, or local runtime outputs back to GitHub unless they have been reviewed and reduced to public-safe summaries.
