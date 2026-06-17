# DOE Runtime Presentation And Model Tracking Plan

Last updated: 2026-06-16

This plan turns the approved three-dataset work into something reviewable on a
website instead of a loose `R2` screenshot. The goal is to show the mentor what
has been built, what ran, what was excluded, how stability fits, and what
unlocks after the DOE Anaconda package request is approved.

## Current Position

- The public GitHub/Streamlit side has the regional/public products: North
  Slope context, public well scaffold, public stability screen, source-backed
  methodology, slide/Word assets, schema contracts, and code.
- The DOE/approved runtime side has the three workbook package:
  `curated_dataset1.xlsx`, `curated_dataset2.xlsx`, and
  `curated_dataset3.xlsx`.
- A first local DOE/Jupyter pass trained separate saturation regressors for the
  currently visible target variants `S_h`, `S_wr`, `Sh`, and `Swr`.
- The first useful result is not the high training-fit `R2`. The useful result
  is that the runtime now separates target-only saturation columns from
  `X_allowed`, cleans helper columns, and creates a repeatable run audit.

## What The Website Should Show

The Streamlit app now has an `Analyze Hydrates > Model Run Tracker` tab. In the
DOE environment it reads ignored local outputs under `outputs_runtime/` and
shows:

- run folders detected;
- trained target runs;
- target column, model kind, feature count, and training-fit metrics;
- feature families used by each target;
- excluded columns and exclusion reasons;
- dataset/sheet inventory summaries;
- stability-to-ML contract.

The tracker is intentionally local-runtime aware. GitHub carries the code and
templates. DOE carries the actual workbook rows, row-level predictions, fitted
models, and detailed runtime folders.

## Stability Use In The ML Pipeline

Stability should be used as context, not as proof.

Allowed uses:

- `stability_status` as an admissibility/context flag;
- `stability_confidence` as a source-control confidence label;
- stability caveats as reviewer notes;
- top/base/thickness only where the public stability screen has a calculated
  interval under the locked pressure, temperature, and methane 5 ppt phase
  assumptions;
- map/plot filters that separate predictions inside and outside the current
  admissible screen.

Not allowed:

- using stability as occurrence;
- using stability as saturation;
- using stability as a hydrate-present target;
- calling a stable interval hydrate proof;
- treating blocked stability rows as negative hydrate labels.

The eventual DOE model should be reviewed in two layers:

1. Model outputs from approved logs/targets: saturation regression and later
   occurrence classification.
2. Stability overlay: whether those outputs sit inside, outside, or beyond the
   current pressure-temperature admissibility context.

## Current Run Story To Tell

Use this language for mentor review:

> We now have a local approved-runtime prototype that can scan the three
> available workbooks, identify saturation target variants, train separate
> saturation regressors, and score available unlabeled sheets. The important
> progress is the audit trail: saturation stays Y-only, depth stays an
> alignment/context axis, spreadsheet helper columns are excluded, and canonical
> feature families are tracked. The current metrics are training-fit/runtime
> proof only, not final validated model performance.

What is ready:

- local runtime path for the three approved workbooks;
- multi-saturation target handling;
- cleaned feature matrix;
- exclusion audit;
- website tracker for local run summaries;
- source-backed public stability context.

What is not ready:

- final occurrence model;
- final saturation model;
- locked blind validation;
- row-level public release;
- final stability-integrated prediction map;
- trained neural network package beyond small scikit-learn prototypes.

## What Unlocks After DOE Package Access

Once the requested Anaconda packages are approved, the DOE runtime can advance
from proof-of-plumbing to reviewable science outputs:

- `lasio`: load LAS curves directly instead of workbook-only tables.
- `geopandas`, `shapely`, `pyproj`, `fiona`, `pyogrio`, `rtree`: local map and
  stability overlay joining.
- `plotly`, `streamlit`: interactive DOE website with run tracker, feature
  audit, maps, and well plots.
- `scikit-learn`, `joblib`: baseline models, saved local pipelines, whole-well
  validation.
- `tensorflow` or `keras` if approved: neural-network experiments after the
  baseline model and feature table are stable.
- `shap` if approved: explainability for feature influence by target/run.
- `python-pptx`, `python-docx`: regenerate mentor slides/docs from current
  website outputs and reviewed summaries.

## Recommended Next DOE Steps

1. Rerun `code_transfer_block/multi_saturation_target_workflow.py`.
2. Confirm the output folder name starts with
   `multi_saturation_clean_features_`.
3. Open `feature_columns_by_target.csv` and confirm there are no `Depth_ft`,
   `DEPT`, `depths_unit*`, `Unnamed:*`, raw `GR`, raw `RES`, raw `RHOB`, raw
   `VP`, or raw `VS` feature rows.
4. Open `excluded_feature_columns_by_target.csv` and review why columns were
   removed.
5. Run the Streamlit app locally in DOE and open `Analyze Hydrates > Model Run
   Tracker`.
6. Use the tracker for mentor discussion, but do not copy raw predictions,
   fitted models, or approved workbook rows back to GitHub.

## Commands

From the repository root in DOE Anaconda:

```bash
python code_transfer_block\multi_saturation_target_workflow.py --data-dir "%USERPROFILE%\Downloads\Northslopedatasets06052026"
```

Then, if Streamlit is available:

```bash
streamlit run streamlit_app.py
```

If Streamlit is not available yet, open the runtime CSV summaries directly:

- `run_summary.csv`
- `feature_columns_by_target.csv`
- `excluded_feature_columns_by_target.csv`
- `sheet_inventory.csv`

## Public-Safe Templates

The public-safe templates for this tracker are in `data/public_ml_products/`:

- `model_run_tracker_summary_template_2026-06-16.csv`
- `model_run_feature_audit_template_2026-06-16.csv`
- `model_run_stability_join_template_2026-06-16.csv`

They describe the shape of the review outputs. They do not contain approved
workbook rows, row-level predictions, fitted models, or final performance
claims.
