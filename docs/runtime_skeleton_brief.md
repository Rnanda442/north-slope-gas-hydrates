# DOE Runtime Skeleton Brief

## Goal

Build the public Streamlit atlas so it is ready to accept approved DOE well-log
and core data later without putting that data in Git, Streamlit Community Cloud,
or any public showcase page.

The intended chain is:

```text
approved LAS/CSV/core files
-> runtime loaders
-> standardized log/core tables
-> validation readiness report
-> manuscript-backed feature engineering
-> core-log calibration
-> interval screening and model adapters
-> GIS-linked figures, exports, and manuscript graphics
```

## Boundary

The repository remains a public-source planning scaffold. The tracked code can
define schemas, adapters, validation, synthetic examples, plotting, and export
templates. Approved well logs, pressure-core data, populated local configs,
trained models, derived sensitive outputs, credentials, and named restricted
identifiers must stay in `data_runtime/`, `outputs_runtime/`, `models_runtime/`,
`logs_runtime/`, or `configs_local/` inside the authorized environment.

## Runtime Package

The skeleton lives in `dashboard/runtime/`.

- `schemas.py`: runtime config, canonical column names, Chong et al. feature
  contract, target-label provenance, and validation report types
- `loaders.py`: CSV loader, curve alias standardization, LAS adapter placeholder
- `validation.py`: readiness checks for required columns, depth order, ranges,
  missingness, well counts, curve coverage, output readiness, and complete-well
  split planning
- `feature_engineering.py`: reusable manuscript-backed feature transforms plus
  caliper upper-tail washout and source-feature completeness flags
- `core_calibration.py`: nearest-depth core-to-log matching and offset flags
- `modeling.py`: rule-based labels now, approved ML adapter interface later
- `plotting.py`: generic well-log and core-log plotting helpers
- `exports.py`: CSV and HTML figure export helpers

The existing public app API remains in `dashboard/well_log_engine.py`. That file
keeps the current synthetic dashboard behavior and calls the runtime loader
behind the scenes.

## Implementation Rules

1. Treat the manuscript as the scientific source of truth.
2. Keep gas hydrate stability as an admissibility screen, not a positive label.
3. Keep reservoir quality, occurrence, saturation, and producibility separate.
4. Require multi-log evidence before a hydrate-supportive label.
5. Use core calibration to adjust confidence, not to silently overwrite logs.
6. Split future model validation by well, not random depth rows.
7. Keep GIS context as a constraint and visualization layer, not a replacement
   for direct log/core evidence.

## Implemented Readiness View

The `Runtime Readiness & ML Plan` tab inside the Future Well-Log Engine now
shows:

- required and optional curve coverage;
- source-backed decision roles;
- ready, partial, and blocked downstream outputs;
- NMR-density versus electrical saturation routing;
- caliper-based washout QC;
- complete-well train/validation/test assignments;
- target-label provenance and leakage exclusions;
- the six-feature Chong et al. machine-learning contract.

Current project assumptions:

- approximately 71 wells;
- approximately 14 known wells for development and 57 wells for prediction;
- complete-well train, validation, and locked-test separation inside the known
  cohort;
- no expected NMR;
- separate phase-classification and continuous-saturation outputs;
- normalized multivariable log and physics features rather than one fixed
  percentage rule.

All fitted preprocessing, including normalization, imputation, feature
selection, and learned weighting, must use training wells only.

## Next Upgrade

After workbook recovery:

- apply exact units, mnemonics, and missing-value conventions;
- add per-well core-log match readiness;
- confirm the authoritative non-NMR saturation and classification targets;
- implement baseline and ANN evaluation using grouped wells;
- generate approved-environment metrics and figures without exporting runtime
  data to the public application.
