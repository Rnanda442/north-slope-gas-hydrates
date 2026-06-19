# Anaconda Dependency Request 2026-06-16

This is the requested Anaconda/Python environment for running the North Slope
gas hydrate project from the DOE/approved-data workstation. It covers the
public Streamlit website, GIS/stability notebooks, source-backed slide and Word
builders, and the future approved well-log/core ML runtime.

Recommended base:

- Python 3.11
- Conda channel: `conda-forge`
- Environment name suggestion: `north_slope_hydrates`

## Core Public Website And Data Tables

These are required for the current Streamlit website and public CSV/Parquet
products:

- `streamlit>=1.40,<2`
- `pandas>=2.2,<3`
- `numpy`
- `plotly>=5.20,<7`
- `pyarrow>=15,<25`
- `pyyaml`
- `pytest`

## Geospatial, Stability, And Map Products

These are required for the North Slope GIS layers, stability products, map
figures, Parquet/GeoParquet, and raster/depth-grid notebooks:

- `geopandas>=1.1,<2`
- `shapely`
- `pyproj`
- `pyogrio`
- `fiona`
- `gdal`
- `rasterio`
- `rtree`
- `scipy`
- `matplotlib`
- `contextily`
- `folium`
- `ipyleaflet`
- `mapclassify`
- `xyzservices`

Conda-forge should resolve low-level GIS libraries such as GEOS, PROJ, GDAL,
and libspatialindex.

## Notebooks And Interactive Work

These are needed because current project work is moving into Anaconda/Jupyter:

- `jupyterlab`
- `notebook`
- `ipykernel`
- `ipywidgets`
- `nbformat`
- `nbconvert`
- `jupytergis` optional, but useful for the GIS notebook that imports it.
- `jupyter_bokeh` optional, for richer notebook-side interactive displays if
  available.

## Slides, Word Docs, Figures, And Source Visuals

These are required to rebuild the PPTX/DOCX deliverables, generated slide PNGs,
contact sheets, and source-backed visuals:

- `pillow`
- `python-pptx`
- `python-docx`
- `lxml`
- `openpyxl`
- `xlsxwriter`
- `xlrd`
- `pyxlsb`
- `odfpy`
- `pypdf`
- `pymupdf`
- `pdfplumber`
- `reportlab`
- `kaleido`

`openpyxl`, `xlrd`, and `pyxlsb` cover modern Excel workbooks, older `.xls`
files, and binary Excel workbooks if any are recovered.

## Approved Well-Log/Core Runtime And ML

These are required or strongly recommended for the future approved-data runtime
that will ingest LAS/CSV/core/NMR rows, create feature matrices, and train
occurrence-classification and saturation-regression models:

- `lasio`
- `scikit-learn`
- `joblib`
- `imbalanced-learn`
- `xgboost`
- `lightgbm`
- `tensorflow`
- `keras`
- `statsmodels`
- `seaborn`
- `scikeras`
- `tensorboard`
- `h5py`
- `optuna`
- `shap`
- `mlflow`

The project should use transparent baselines and tree/boosting before ANN/Keras
models. `tensorflow`/`keras`, `scikeras`, `tensorboard`, and `h5py` are the
Keras/ANN stack for the future neural-network path, not for current public
claims. `optuna`, `shap`, and `mlflow` support tuning, explanation, and
experiment tracking when approved-data modeling begins.

## Optional Alternative Neural-Network Stack

If DOE already supports PyTorch or if TensorFlow is difficult to approve on the
workstation, also request access to:

- `pytorch`
- `torchvision`
- `torchaudio`

The current project plan names ANN/Keras because the source-backed hydrate ML
reference uses ANN-style models, but PyTorch is a reasonable backup for future
custom neural-network experiments.

## Optional Drive/Cloud Export Helpers

These are optional. They are only needed if the DOE workstation should upload or
sync generated PPTX/DOCX/PDF files to Google Drive programmatically instead of
using a browser or external connector:

- `google-api-python-client`
- `google-auth`
- `google-auth-oauthlib`
- `google-auth-httplib2`

Do not store credentials in Git. Any credentials must stay in approved local
configuration folders.

## Helpful Non-Python Tools

These are not Python packages, but they are useful for full reproduction of the
website, slide, Word, PDF, and Git workflow:

- `git`
- `pandoc`
- `libreoffice` or Microsoft Office for PPTX/DOCX/PDF review/export
- `poppler` for PDF-to-image workflows if needed
- `graphviz` optional for future architecture diagrams
- `nodejs` optional for local browser/visual QA tooling

## Suggested Conda Command

```bash
conda create -n north_slope_hydrates -c conda-forge python=3.11 \
  streamlit pandas numpy plotly pyarrow pyyaml pytest \
  geopandas shapely pyproj pyogrio fiona gdal rasterio rtree scipy matplotlib contextily folium ipyleaflet mapclassify xyzservices \
  jupyterlab notebook ipykernel ipywidgets nbformat nbconvert \
  pillow python-pptx python-docx lxml openpyxl xlsxwriter xlrd pyxlsb odfpy pypdf pymupdf pdfplumber reportlab kaleido \
  lasio scikit-learn joblib imbalanced-learn xgboost lightgbm tensorflow keras scikeras tensorboard h5py statsmodels seaborn optuna shap mlflow
```

Optional after environment creation:

```bash
conda install -n north_slope_hydrates -c conda-forge jupytergis \
  google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2
```

Optional PyTorch backup:

```bash
conda install -n north_slope_hydrates -c conda-forge pytorch torchvision torchaudio
```

## Verification Commands

From the repository root:

```bash
python -m py_compile dashboard/app.py dashboard/source_visual_inventory.py docs/project_blueprints/build_full_workflow_diagram_deliverables.py
python -m pytest
streamlit run streamlit_app.py
```

Expected current public test result as of 2026-06-16: `114 passed`.

## Data Boundary Reminder

Approved LAS/CSV/core/NMR rows, runtime configs, trained models, derived
approved outputs, and credentials must remain in ignored local runtime folders
or the DOE-approved workspace. GitHub/Streamlit should receive only public-safe
summaries, schema/header reports, docs, diagrams, and reviewed public products.
