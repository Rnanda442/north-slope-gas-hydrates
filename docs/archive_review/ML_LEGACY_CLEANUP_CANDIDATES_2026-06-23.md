# ML Legacy Cleanup Candidates

Date: 2026-06-23

Purpose: collect older ML/runtime artifacts that may conflict with the new equation-first V4 workflow. This is a review list only; do not delete until reviewed.

## Current source of truth

- `docs/ML_EQUATION_FIRST_V4_STATUS_2026-06-23.md`
- `notebooks/DOE_MASTER_ML_PIPELINE_EQUATION_FIRST_V4.ipynb` once committed
- local ignored runtime folders for real outputs and models

## Candidate legacy paths to review before delete/archive

These appear to describe earlier random-forest-only, audit-first, three-dataset, or duplicated notebook workflows:

```text
doe_anaconda_final_kit/DOE_MASTER_FULL_PIPELINE.ipynb
doe_anaconda_final_kit/DOE_MASTER_FULL_PIPELINE (1).ipynb
doe_anaconda_final_kit/DOE_MASTER_FULL_PIPELINE_V2.ipynb
doe_anaconda_final_kit/DOE_MASTER_ML_PIPELINE_REBUILT.ipynb
doe_anaconda_final_kit/DOE_MASTER_ML_PIPELINE_REBUILT_FIXED.ipynb
doe_anaconda_final_kit/PIPELINE_RUNDOWN.md
doe_anaconda_final_kit/README.md
docs/DOE_THREE_DATASET_ML_PIPELINE_RUNBOOK_2026-06-16.md
dashboard/runtime/three_dataset_pipeline.py
01_pipeline/run_three_dataset_ml_pipeline.py
01_pipeline/inspect_three_dataset_headers.py
code_transfer_block/inspect_three_dataset_headers_standalone.py
code_transfer_block/notebook_header_scan_cell.py
```

## Review rule

Move or delete only after confirming that the file is not referenced by the current website, tests, or documentation. Older files can be moved into a dated archive folder if they are useful provenance; otherwise delete them after review.

## Scientific reason

The V4 direction is equation-first and separates hydrate-saturation regression, secondary water/residual-water saturation regression, and occurrence screening now. Supervised occurrence classification should wait for independent labels or a clearly marked weak saturation-derived label.
