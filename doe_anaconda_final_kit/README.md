# DOE Anaconda Final Kit

This folder is the clean GitHub-facing handoff lane for DOE/Anaconda notebooks
and scaffolds. It should contain notebooks, small runners, configs, and
instructions only.

## Current Comparison Notebook

Use V26 for the ANN scatter packet:

```text
DOE_MASTER_ML_PIPELINE_EQUATION_FIRST_V26_ANN_LOO_SCATTER_PACKET.ipynb
```

V26 is based on the V22 WellA-held-out ANN run family, which is the run family
tied to the high WellA ANN result. It keeps the DOE/Anaconda raw-data loader and
review-packet pattern, then runs ANN-only leave-one-well-out splits for WellA,
WellB, WellC, and WellD. Its default WLC is
`EQ_full_except_density_porosity_no_target_leakage`.

Use V22 for the WellA-heldout comparison run:

```text
DOE_MASTER_ML_PIPELINE_EQUATION_FIRST_V22_WELLA_HOLDOUT_3TO1_REPORT_PIPELINE.ipynb
```

V22 keeps the V21 report-pipeline structure but makes the primary split
explicit: train WellB + WellC + WellD, then test held-out WellA. Use it beside
the V21 or earlier WellC-heldout packet to compare area-specific transfer
behavior. V22 outputs use their own `v22_wella_holdout_3to1_report_pipeline`
slug and `V22_output_review_<RUN_ID>` review folder.

## Optional ANN Leave-One-Well-Out Scatter Runner

The normal DOE/Anaconda handoff is the V26 notebook above. This script is a
small helper for cases where a private model matrix has already been exported
or where the V26 notebook has already built the in-memory `features_df` model
matrix:

```text
run_ann_loo_scatter_plots.py
```

It trains ANN saturation models four times by default: hold out WellA, WellB,
WellC, and WellD; train on the other three wells; then save one scatter plot per
held-out well. The default WLC is the final high-performing WLC:

```text
EQ_full_except_density_porosity_no_target_leakage
```

That is the same WLC family tied to the ~0.917 WellA ANN summary and ~0.763
WellC ANN summary in the final review workbooks.

View the plan without reading private data:

```powershell
python doe_anaconda_final_kit/run_ann_loo_scatter_plots.py --print-plan
```

If the runner is called from inside a Jupyter notebook, it safely ignores the
kernel `-f/--f kernel.json` argument that Jupyter adds automatically. Real
unknown runner flags still fail. When no `--model-matrix-csv` is provided, the
runner also looks for the V26 notebook's in-memory `features_df` dataframe and
uses it as the model matrix.

Dependencies:

```powershell
pip install scikit-learn matplotlib pandas numpy pillow openpyxl
```

Run it on a private model matrix:

```powershell
python doe_anaconda_final_kit/run_ann_loo_scatter_plots.py `
  --model-matrix-csv "C:\path\to\private_model_matrix.csv"
```

Or, after running the V26 notebook cells that build `features_df`, run the
updated helper from a notebook cell without exporting a CSV first:

```python
%run -i ./run_ann_loo_scatter_plots.py --copy-slide8-excel-to-downloads
```

To put the slide 8 Excel workbook somewhere easy to upload to Drive, add:

```powershell
python doe_anaconda_final_kit/run_ann_loo_scatter_plots.py `
  --model-matrix-csv "C:\path\to\private_model_matrix.csv" `
  --copy-slide8-excel-to-downloads
```

Or copy it directly to a synced folder:

```powershell
python doe_anaconda_final_kit/run_ann_loo_scatter_plots.py `
  --model-matrix-csv "C:\path\to\private_model_matrix.csv" `
  --slide8-excel-copy-dir "C:\path\to\Google Drive\North Slope"
```

Outputs go under ignored `outputs_runtime/ann_loo_scatter_plots/` unless
`--output-dir` is passed. The scatter PNGs are in `figures/`, and the audit
tables include `ann_loo_fold_summary.csv`, `ann_loo_metrics_by_realization.csv`,
`ann_loo_selected_saturation_bin_bias.csv`, and
`ann_loo_wlc_feature_weights.csv`. The runner also writes
`ann_loo_slide8_saturation_bin_bias.xlsx`, with `slide8_bias_long` and
`slide8_bias_wide` sheets for rebuilding Slide 8 across WellA, WellB, WellC,
and WellD. The fold summary includes the selected ANN
occurrence-style scores derived from the saturation threshold, so Slides 8-9 can
use ANN bin-bias and ANN occurrence checks after the next run.

The runner also creates an email packet by default:

```text
outputs_runtime/ann_loo_scatter_plots/<run_time>/ann_loo_email_packet/
```

That folder contains `share_packet_V26_ann_loo_scatter_plots.zip`, a contact
sheet PNG, the fold summary CSV, the selected saturation-bin bias CSV,
the Slide 8 Excel workbook, individual scatter PNGs, and
`open_outlook_draft_V26_ann_loo_scatter_plots.ps1`. On Windows it tries to open
an Outlook draft automatically, using `PERSONAL_REVIEW_EMAIL` if that
environment variable is set. To make the packet but not open Outlook, add:

```powershell
--no-open-outlook-draft
```

Important wording: the WLC feature weights are input-feature weights, not raw
neural-network hidden-layer weights. If `best_r2` scatter selection is used,
use the figure as a best-realization visual rather than an unbiased
model-selection claim.

## Current Final Report Notebook

Use V21 for the final report pipeline:

```text
DOE_MASTER_ML_PIPELINE_EQUATION_FIRST_V21_FINAL_3TO1_REPORT_PIPELINE.ipynb
```

V21 trains on three active wells and tests one held-out well by default. It
also exports leave-one-well-out 3-to-1 report sheets, paper figures, diagnostic
heatmaps, a compact share packet, a review folder, and a final Outlook draft
helper.

## References

- V15 is the first actual core-aware multi-task baseline.
- V16 and V17 are final-focus references.
- V18 is the targeted Ridge/logistic/core-weight tuning reference.
- `v20_three_versions/` is the V20 fixed-variant scaffold and negative
  stress-test comparison, not the final notebook.
- V22 is the WellA-heldout comparison copy of V21, with V22-named outputs and
  run instructions under `docs/current_source_bundle_2026_06_26/`.

Runtime outputs stay outside GitHub under ignored DOE/runtime folders. Do not
commit approved workbooks, row-level predictions, fitted models, runtime logs,
private identifiers, ZIP share packets, or populated runtime configs.
