# DOE Anaconda final kit

Use this folder on the DOE desktop when Git is not available.

Open:

```text
DOE_MASTER_FULL_PIPELINE.ipynb
```

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
- Optional moisture/temperature CSV context is auto-searched from Downloads, the workbook folder, or the notebook folder when a filename contains moisture/water and temperature/temp.
- Outputs write to local `outputs_runtime/` and `models_runtime/` folders.

Expected Anaconda packages:

```text
pandas
numpy
scikit-learn
openpyxl
joblib
```

Notebook sections:

1. Setup and package check
2. Schema, aliases, project assumptions
3. Loading and header standardization
4. Moisture/temperature CSV context
5. Validation/readiness checks
6. Feature engineering and proxy features
7. Header scan
8. Main three-dataset ML run
9. Dataset 3 as training run
10. All saturation-like target run
11. Output review checklist

Do not commit approved workbook rows, prediction rows, fitted models, or local runtime outputs back to GitHub unless they have been reviewed and reduced to public-safe summaries.
