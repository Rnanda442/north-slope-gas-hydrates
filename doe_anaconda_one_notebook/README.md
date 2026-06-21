# DOE Anaconda one-notebook pipeline

This folder is for the DOE desktop / Anaconda workflow when Git is unavailable.

Open `DOE_integrated_full_pipeline.ipynb` in Jupyter. The notebook is intentionally self-contained: it includes the header scan, Excel loading, alias mapping, feature engineering, target detection, leakage-safe feature selection, training/prediction, dataset-3-as-training option, and all-saturation-target workflow in notebook cells.

Expected local workbook folder by default:

```text
C:\Users\rohan.nanda\Downloads\Northslopedatasets06052026
```

Expected workbook names:

```text
curated_dataset1.xlsx
curated_dataset2.xlsx
curated_dataset3.xlsx
```

Required Anaconda packages:

```text
pandas
numpy
scikit-learn
openpyxl
joblib
```

The notebook writes local outputs to `outputs_runtime/` and fitted models to `models_runtime/`. Those folders are ignored by Git and should stay local because they may contain approved-runtime data products.
