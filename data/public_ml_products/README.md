# Public ML Products

This folder stores public-safe ML schema, architecture, and methodology
products. It is separate from the approved runtime folders and must not contain
approved well-log rows, core rows, restricted well identifiers, populated
runtime configurations, trained models, or model performance metrics.

## Current Product

`approved_schema_coverage_matrix_2026-06-15.csv`

This is a schema-level matrix only. It records visible or expected header
families from the project base, header screenshots, requirements map, and ML
logic docs. It preserves original headers and maps them to canonical roles as
metadata so the future approved-data workflow can separate:

- measured input logs;
- derived features;
- QC and alignment fields;
- target-only saturation and phase-label fields;
- calibration/reference fields;
- unresolved fields that need workbook or mentor review.

The matrix does not include raw data rows. It does not train a model, report
hydrate predictions, report saturation values, or claim performance. The
current public-safe status is schema and model-architecture readiness only.
