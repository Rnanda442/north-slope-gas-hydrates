# DOE V19 Physics-Weighted Transfer Run Instructions

Use this notebook for the next DOE/Anaconda run:

`doe_anaconda_final_kit/DOE_MASTER_ML_PIPELINE_EQUATION_FIRST_V19_PHYSICS_WEIGHTED_TRANSFER_ANN.ipynb`

## Purpose

V19 is a known-four-well development run built from the V15-V18 review results.
It is designed to improve saturation and occurrence scores on the current four
wells while keeping the claim boundary clear.

Before running, read:

`docs/V19_V20_FINAL_TEST_LOCK_PLAN_2026-07-10.md`

Default split remains:

```text
train WellC -> score WellA + WellB + WellD
```

Unlike V18, V19 can rank the selected saturation and occurrence candidates by
the known transfer-well score. This is useful for the current project goal, but
it must be described as development optimization, not blind new-well validation.
The default candidate list is now locked from the V15-V18 evidence review; do
not widen it unless the search is explicitly reopened.

## Key V19 Changes

- Uses `CODE_VERSION = "V19_physics_weighted_transfer_ann"`.
- Adds `V19_TRANSFER_SELECTION_MODE=development_transfer_ranked` by default.
- Separately ranks hydrate saturation and hydrate occurrence candidates, with
  saturation set to RMSE-first / MAE / R2 and occurrence set to balanced
  accuracy / F1 / ROC-AUC.
- Restricts default Ridge candidates to alpha 1 and alpha 10.
- Restricts default core reliability weight testing to strength 2.0.
- Restricts default ANN/WLC comparison to the prior `rho+phi+Rt` WLC/triplet
  with the fixed V15-informed ANN preset.
- Adds one feature-family weighting diagnostic for equation/geomechanics
  features at weight 0.25 after MinMax scaling.
- Applies weight trials after MinMax scaling so weights actually affect Ridge
  style models.
- Enlarges heatmap, annotation, label, and paper-figure font sizes.
- Exports `v19_feature_family_weight_sensitivity_*` tables and heatmaps.
- Keeps the final Outlook draft and `V19_output_review_<RUN_ID>` folder inside
  the notebook so no manual email code block is required.

## Scientific Boundary

Core data remain blocked from ordinary `X` predictors. They may enter only as
auxiliary learning, reliability weighting, and review evidence.

Stability remains context/admissibility only. V19 still writes a stability join
audit, but stability is not allowed into `X` unless the join audit proves a
valid spatial/depth/stratigraphic match.

Do not claim V19 proves transfer to a future unseen well. The correct language
is known-well development optimization unless a future well is truly locked out.

## Outputs To Review First

After the run, inspect:

```text
Downloads/Northslopedatasets06052026/V19_output_review_<RUN_ID>
```

Prioritize:

- `clean_summary_v19_physics_weighted_transfer_ann.xlsx`
- `diagnostic_heatmaps_v19_physics_weighted_transfer_ann.pdf`
- `v19_feature_group_ablation_*`
- `v19_equation_help_harm_*`
- `v19_feature_family_weight_sensitivity_*`
- `v19_core_weight_sensitivity_*`
- `v19_saturation_threshold_sensitivity_*`
- `v19_wellc_to_rest_feature_drift_*`
- `model_selection_audit_*`
- `stability_join_audit_*`
- `v15_core_usage_audit_*`

## Review Questions

1. Which model/feature set wins when V19 ranks by known transfer-well score?
2. Does occurrence need a different feature set or logistic setting than
   saturation, judged by balanced accuracy first?
3. Did the selected candidate hold up across WellA, WellB, and WellD
   separately, or did one well degrade?
4. Do equation/geomechanics down-weights help, hurt, or only help one well?
5. Does the single core reliability strength 2.0 improve transfer metrics
   consistently?
6. Does the stability audit still block stability from `X`?
7. Are the larger heatmaps readable enough for slides and the Word document?

## Email Packet

The final notebook cell creates a local review folder and an Outlook draft. It
does not intentionally auto-send. Review the attachments before sending them
outside the DOE environment.

Only row-free summary outputs should leave DOE/runtime storage. Do not move
row-level predictions, approved rows, runtime logs, fitted models, private
identifiers, or populated runtime configs into GitHub.
