# Project State Handoff — ML Pipeline

Date: 2026-06-23

This note records where the project is after the equation-first V4 notebook work. It is intended as the short handoff to read before changing the repo, notebook, Word document, slides, or website.

## Where we are now

The active ML direction is an equation-first approved-runtime workflow for gas hydrate occurrence and saturation. The notebook is being run locally in the approved/DOE environment, while GitHub remains public-safe.

Current working pipeline:

1. Load four approved-runtime workbook inputs using neutral well aliases.
2. Standardize raw headers into canonical log variables.
3. Compute physics/equation-derived features before ML.
4. Train hydrate-saturation regression.
5. Train secondary water/residual-water saturation regression.
6. Produce a rule-based occurrence screen.
7. Export compact runtime outputs locally.

The project should no longer be described as a random-forest-only or audit-first workflow. The current model ladder is baselines, Ridge/SGD, Random Forest, Gradient Boosting, and ANN/MLP.

## Current outputs and targets

Active targets:

- Hydrate saturation regression: active primary ML output.
- Water/residual-water saturation regression: active secondary test, limited by only two wells.
- Hydrate occurrence: active as rule-based screen; supervised classifier is pending a real occurrence label or an explicitly named weak saturation-derived label.

Expected local outputs:

```text
outputs_runtime/ml_master/model_results.xlsx
outputs_runtime/ml_master/predictions.csv
outputs_runtime/ml_master/paper_figures.pdf
outputs_runtime/ml_master/run_manifest.json
models_runtime/ml_master/selected_models.joblib
```

These outputs stay local and ignored. Do not commit them.

## Current repo updates

Current PR branch:

```text
ml-equation-first-v4-20260623
```

Current PR:

```text
#4 Document equation-first V4 ML runtime
```

Files added in the PR:

```text
docs/ML_EQUATION_FIRST_V4_STATUS_2026-06-23.md
docs/PROJECT_STATE_ML_HANDOFF_2026-06-23.md
docs/archive_review/ML_LEGACY_CLEANUP_CANDIDATES_2026-06-23.md
notebooks/README.md
requirements-ml.txt
```

## What still needs to be done

1. Finish the current V4 run in the DOE/local environment.
2. Confirm the runtime outputs are created and review `model_results.xlsx`, especially `summary`, `metrics`, `equations_used`, `archie_metadata`, `feature_importance`, and `occurrence_screen`.
3. Confirm the notebook has no embedded approved rows, unrestricted predictions, or local secrets before committing the `.ipynb` itself.
4. Add occurrence-target support:
   - first search for independent occurrence labels;
   - if none exist, add `weak_occurrence_from_saturation` as a clearly labeled temporary target;
   - export classification metrics separately from saturation-regression metrics.
5. Review the legacy cleanup list and decide what to archive or delete.
6. Update the Word document to match the new V4 pipeline.
7. Update slides only after the notebook and Word direction are stable.
8. Update the Streamlit/website layer only where it mirrors the approved public-safe workflow.

## Legacy cleanup rule

Do not delete older files blindly. Use:

```text
docs/archive_review/ML_LEGACY_CLEANUP_CANDIDATES_2026-06-23.md
```

First check references from docs, tests, and the website. Then either archive old artifacts into a dated review folder or delete them after review.

## Current scientific wording

Use this wording when explaining the project:

> The current pipeline is an equation-first, leakage-controlled ML workflow for North Slope gas hydrate occurrence and saturation. Hydrate saturation is treated as a regression target, water/residual-water saturation is treated as a secondary regression target, and hydrate occurrence is currently a rule-based screen until independent occurrence labels or a clearly marked weak saturation-derived occurrence target are approved.

Avoid saying:

- stability proves hydrate;
- high resistivity alone proves hydrate;
- occurrence is already a supervised classifier;
- water saturation is the main target;
- the old random-forest-only notebooks are the current pipeline.
