# DOE Anaconda Final Kit

This folder is the clean GitHub-facing handoff lane for DOE/Anaconda notebooks
and scaffolds. It should contain notebooks, small runners, configs, and
instructions only.

## Current Comparison Notebook

Use V22 for the WellA-heldout comparison run:

```text
DOE_MASTER_ML_PIPELINE_EQUATION_FIRST_V22_WELLA_HOLDOUT_3TO1_REPORT_PIPELINE.ipynb
```

V22 keeps the V21 report-pipeline structure but makes the primary split
explicit: train WellB + WellC + WellD, then test held-out WellA. Use it beside
the V21 or earlier WellC-heldout packet to compare area-specific transfer
behavior. V22 outputs use their own `v22_wella_holdout_3to1_report_pipeline`
slug and `V22_output_review_<RUN_ID>` review folder.

## ANN Leave-One-Well-Out Scatter Runner

Use this script when the presentation needs ANN-only scatter plots instead of
linear/Ridge scatter plots:

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

Dependencies:

```powershell
pip install scikit-learn matplotlib pandas numpy pillow
```

Run it on a private model matrix:

```powershell
python doe_anaconda_final_kit/run_ann_loo_scatter_plots.py `
  --model-matrix-csv "C:\path\to\private_model_matrix.csv"
```

Outputs go under ignored `outputs_runtime/ann_loo_scatter_plots/` unless
`--output-dir` is passed. The scatter PNGs are in `figures/`, and the audit
tables include `ann_loo_fold_summary.csv`, `ann_loo_metrics_by_realization.csv`,
and `ann_loo_wlc_feature_weights.csv`.

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
