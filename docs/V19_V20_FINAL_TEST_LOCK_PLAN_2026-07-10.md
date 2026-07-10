# V19/V20 Final Test Lock Plan

Last updated: 2026-07-10

## Purpose

This document locks the allowed final ML tests before running V19 or creating
V20. V19 is designed to test physics/feature-family weight profiles, but V19
has not proven a best weight profile until it is run and reviewed. Treat V15-V18
as exploratory/development evidence and treat the next run as known four-well
development optimization, not blind external validation.

## Boundary

Approved workbook rows, row-level predictions, runtime logs, fitted models,
private well identifiers, populated configs, and detailed depth-index outputs
stay in DOE/runtime-only folders. Git may contain this plan, code, empty
schemas, run instructions, and row-free aggregate summaries only.

## Evidence Locked From V15-V18

- V15 selected saturation benchmark was weak: RF on `safe_normalized`, RMSE
  0.2823, MAE 0.2257, R2 -0.0902.
- V16/V17 selected saturation benchmark improved: Ridge alpha 1 on
  `safe_normalized`, RMSE 0.1907, MAE 0.1541, R2 0.5025.
- V17 transparency rows showed the strongest saturation candidates as Ridge
  alpha 10 on `safe_normalized` and Ridge alpha 10 on
  `all_allowed_except_density_porosity_review`.
- Equation-heavy/all-input branches trailed those two candidates, so V19 keeps
  one downweighted equation/geomechanics diagnostic instead of a broad search.
- Core reliability weighting helped only modestly, so V19 tests one
  evidence-backed core reliability strength by default: 2.0.
- Occurrence selection must not be recall-only. V19 uses balanced accuracy
  first, then F1, then ROC-AUC.

## Metric Lock

Saturation winner:

- Primary metric: lowest combined-transfer RMSE on WellA + WellB + WellD.
- Tie-breakers: lowest MAE, then highest R2.
- Required guardrail: publish WellA, WellB, and WellD separately.

Occurrence winner:

- Primary metric: highest balanced accuracy.
- Tie-breakers: highest F1, then ROC-AUC.
- Required guardrail: show precision and recall separately.

Depth/interval rule:

- Row counts are not independent sample counts because depth rows are
  autocorrelated. Final tables and figure captions must include interval/block
  language.

## Allowed Final Tests

Saturation regression candidates:

1. `ridge_a1` with `safe_normalized`, core weight off.
2. `ridge_a10` with `safe_normalized`, core weight off.
3. `ridge_a10` with `all_allowed_except_density_porosity_review`, core weight
   off.
4. `ridge_a10` with `safe_normalized`, core reliability strength 2.
5. `ridge_a10` with `all_allowed_except_density_porosity_review`, core
   reliability strength 2.
6. One equation/downweighted diagnostic: equation and geomechanics families at
   weight 0.25 after scaling.
7. Chong-style ANN comparison: prior `rho+phi+Rt` WLC/triplet using the fixed
   V15-informed ANN preset only.

Occurrence classification candidates:

1. `logistic_balanced` with `measured_only`.
2. `logistic_balanced` with `safe_normalized`.
3. `logistic_balanced` with `all_allowed_except_density_porosity_review`.
4. One equation/downweighted diagnostic, diagnostic-only unless it improves
   balanced accuracy and per-well behavior.

Do not add new feature families, new WLC grids, new model classes, or new
weight profiles outside this list unless the user explicitly reopens the
search.

## Required Exports

The next V19/V20 output packet must include:

- final test manifest with candidate and metric policy;
- combined-transfer saturation metric table;
- per-well saturation metric table for WellA, WellB, and WellD;
- saturation interval/bin error table;
- occurrence metric table with accuracy, balanced accuracy, precision, recall,
  F1, ROC-AUC, and confusion counts;
- per-well occurrence metric table for WellA, WellB, and WellD;
- feature-drift/domain-shift heatmap and table;
- equation/geomechanics help-harm or feature-family weighting table;
- core reliability-weight sensitivity table;
- stability join audit proving stability remains context/admissibility only
  unless a valid spatial/depth/stratigraphic join is documented.

## Claim Language

Use language like:

```text
The final run is a known-four-well development optimization: WellC is used for
training and WellA, WellB, and WellD are held out for transfer-style review.
Because prior V15-V18 outputs informed the final candidate list, the result is
not blind external validation. Scores are reported by validation well and with
interval/block caveats because depth rows are autocorrelated.
```

Do not say V19 proved the best physical weights until V19 has run, exported the
required tables, and passed the locked metric and per-well checks.

## Stop Rule

After V19 is run with this plan, freeze the feature sets, weights, and model
classes. Create V20 only to fix a runtime/export bug or to package the locked
outputs; do not use V20 to start a new weight/model search.
