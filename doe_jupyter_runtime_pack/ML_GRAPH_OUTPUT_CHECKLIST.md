# ML Graph Output Checklist For Word And Slides

Use this checklist after running the DOE Jupyter notebook or runner. Outputs
stay local in `outputs_runtime/` until reviewed.

## Data And Schema Readiness

- Dataset/workbook inventory summary.
- Sheet/header inventory.
- Target-header hints.
- Schema/header coverage visual.
- Feature-family coverage chart.
- Target-only leakage audit visual.
- Excluded-column reason chart.
- Train/test/external workbook split summary.

## Model Run Review

- Model run tracker summary.
- Target-by-target model cards.
- Feature-family count bar chart.
- Validation-status chart.
- Run comparison table.
- Public-safe model run review brief.

These are audit and workflow outputs. Training-fit metrics, if exported
locally, are not final model performance claims.

## Equation-Derived Figures

- Equation-to-ML-feature map.
- Equation symbol readiness table/visual.
- Equation-derived distribution plots.
- Equation output crossplots.
- Optional stability-margin plot when local temperature and pressure inputs
  are available.

## Optional DOE-Local Figures

These can be generated locally for internal review, but should not be pushed
unless sanitized and approved:

- Anonymized well-log panels.
- Core-log calibration crossplots.
- Prediction-vs-target plots.
- Residual plots.
- Well or geography holdout maps.
- Uncertainty/caveat flag summaries.

## Public-Safe Return To GitHub

Usually safe after review:

- source code updates;
- empty templates;
- row-free schema summaries;
- row-free graph specifications;
- public-safe method diagrams;
- reviewed aggregate summaries.

Keep DOE-only:

- approved workbook rows;
- well identifiers that are not cleared;
- row-level predictions;
- fitted models, scalers, and model binaries;
- populated local configs;
- private runtime manifests;
- unreviewed metric tables.

