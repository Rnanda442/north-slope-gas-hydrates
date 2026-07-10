# DOE V18 Targeted-Tuning Run Instructions

Use this notebook for the next focused DOE/Anaconda run:

`doe_anaconda_final_kit/DOE_MASTER_ML_PIPELINE_EQUATION_FIRST_V18_TARGETED_TUNING_FINAL_FOCUS_ANN.ipynb`

## Purpose

V18 is a targeted tuning update to V17, not a return to the V15 full
sensitivity sweep. It keeps the strict one-well transfer design:

```text
train WellC -> validate WellA + WellB + WellD
```

It uses V15/V16/V17 outputs to tune only the controls that looked worth
testing:

- Ridge alpha candidates: `0.3, 1, 3, 10, 30`
- logistic C candidates: `0.3, 1, 3`
- ANN fixed-parameter preset default: V15 WellC-best internal-CV setting
- core reliability-weight strengths: `0.5, 1, 2, 4`
- the same V17 diagnostic heatmaps, now written as V18 outputs

## Scientific Boundary

Do not treat V18 as a new blind discovery sweep. It is a focused follow-up
using lessons from V15/V16/V17.

Core data remain blocked from ordinary `X` predictors. They may enter only as
auxiliary learning, reliability weighting, and review evidence. Direct
core-based hydrate-saturation target filling remains blocked unless reviewed
`core_hydrate_saturation_vv` rows exist.

Stability remains context/admissibility only. V18 still writes a stability join
audit, but stability is not allowed into `X` unless the join audit proves a
valid spatial/depth/stratigraphic match.

## Recommended Default Run

Run the notebook as-is first.

Default V18 settings:

```python
CODE_VERSION = "V18_targeted_tuning_final_focus_ann"
TARGETED_RIDGE_ALPHAS = [0.3, 1, 3, 10, 30]
TARGETED_LOGISTIC_C_VALUES = [0.3, 1, 3]
CHONG_FIXED_ANN_PARAM_PRESET = "v15_wellc_best"
CORE_AWARE_WEIGHT_STRENGTHS = [0.5, 1, 2, 4]
```

The V15-informed ANN preset is:

```text
learning_rate = 0.003
hidden_layers = 2
nodes_per_layer = 50
batch_size = 100
epochs = 500
dropout = 0.5
```

To rerun the exact V16/V17 Chong-style ANN setting instead:

```python
import os
os.environ["CHONG_FIXED_ANN_PARAM_PRESET"] = "chong_fixed"
```

## Runtime Expectation

V18 should stay much closer to V17 runtime than V15 runtime because it does not
run the V15 full WLC/hyperparameter grid. It adds fast Ridge/logistic candidates
and changes the fixed ANN preset for the focused WLC suite.

## Outputs To Review

After the run, inspect the review folder created under the DOE input/downloads
folder:

```text
V18_output_review_<RUN_ID>
```

Prioritize:

- `clean_summary_v18_targeted_tuning_final_focus_ann.xlsx`
- `diagnostic_heatmaps_v18_targeted_tuning_final_focus_ann.pdf`
- `v18_feature_group_ablation_*`
- `v18_core_weight_sensitivity_*`
- `v18_saturation_threshold_sensitivity_*`
- `v18_wellc_to_rest_feature_drift_*`
- `stability_join_audit_*`
- `v15_core_usage_audit_*`

Key questions:

1. Did Ridge alpha `10` or another alpha become selected by train-safe CV?
2. Did `safe_normalized` or `all_allowed_except_density_porosity_review` improve
   saturation transfer without target leakage?
3. Did occurrence improve with safe-normalized/logistic C candidates?
4. Did core weight strength `4` help more than `2`, or does the gain plateau?
5. Does the stability audit still block stability from `X`?

## Email Packet

The final notebook cell creates a local review folder and an Outlook draft. It
does not intentionally auto-send. Review the attachments before sending them
outside the DOE environment.

Only row-free summary outputs should leave DOE/runtime storage. Do not move
row-level predictions, approved rows, runtime logs, fitted models, private
identifiers, or populated runtime configs into GitHub.
