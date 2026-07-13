# DOE V20 Three-Version Run Instructions

Date: 2026-07-12

Use this V19-style full DOE/Anaconda notebook:

```text
doe_anaconda_final_kit/DOE_MASTER_ML_PIPELINE_EQUATION_FIRST_V20_THREE_VERSION_COMPARISON_ANN.ipynb
```

The three fixed V20 comparison variants are:

| Version | Role |
|---|---|
| V20A baseline safe | Ridge alpha 10 on safe measured/log-transform inputs; use as the baseline anchor. |
| V20B equation dominance | Primary measured/safe log inputs weight 0.25; equation/geomechanics inputs weight 1.0. |
| V20C HYDRATE-02 core prior | Frozen HYDRATE-02 Table S1 porosity-to-`Sh(IW)` prior used as one auxiliary feature only. |

## Required Private Inputs

Use the same DOE input folder pattern as V15-V19. Place the approved well-log
workbooks and the combined core workbook in:

```text
Downloads/Northslopedatasets06052026
```

The preferred combined core workbook is:

```text
actual_core_data_combined.xlsx
```

V15-V19 auto-detect that combined workbook first. V20 reads HYDRATE-02 candidate
target evidence from sheet `12_Candidate_Sh_Targets`. Those rows stay target-side
only: they are not ordinary `X_allowed` model inputs and are not validation truth
for WellA/WellB/WellC/WellD.

Do not commit approved workbooks, row-level outputs, fitted models, private
identifiers, or runtime logs to Git.

## Notebook Run

1. Download/open the V20 notebook in Anaconda/Jupyter.
2. Run cells in order, like V15-V19.
3. The notebook loads workbooks, computes equations, runs the inherited V19
   transfer/core-aware workflow, then runs section `4B. V20 Three Fixed-Variant
   Comparison`.
4. Optional row-level V20 predictions are written only when
   `V20_WRITE_PREDICTIONS=1`. Do not move row-level predictions to GitHub.

## Expected Outputs

The notebook writes normal full-pipeline outputs to:

```text
Downloads/outputs_runtime/ml_master/
```

Key V20 comparison files:

| File | Meaning |
|---|---|
| `v20_three_variant_manifest_<run_slug>.json` | Run settings, variant definitions, and output paths |
| `v20_saturation_metrics_<run_slug>.csv` | Combined and per-well saturation metrics |
| `v20_occurrence_metrics_<run_slug>.csv` | Combined and per-well occurrence metrics derived from the fixed threshold |
| `v20_saturation_bin_metrics_<run_slug>.csv` | Per-well saturation-bin error/bias checks |
| `v20_feature_weights_<run_slug>.csv` | Exact feature weights used by each V20 version |
| `v20_hydrate02_core_prior_audit_<run_slug>.csv` | HYDRATE-02 core-prior fit status and tiny-core warning |

## Claim Control

Occurrence labels are derived from `hydrate_saturation_reference >= 0.05`.
Balanced-logistic probabilities are classified at `0.5` by default unless a
pre-locked policy changes `V20_CLASS_PROBABILITY_THRESHOLD`.

Use this language:

```text
V20 compares three pre-declared development variants under the known four-well
transfer setup. V20A is the baseline; V20B is an equation-dominance stress
test; V20C is a frozen external HYDRATE-02 core-prior diagnostic. The run is
not blind new-well validation.
```

Do not say that HYDRATE-02 validates the four active wells. It is external
target-side physics evidence unless matching HYDRATE-02 logs and a separate
split policy are approved.
