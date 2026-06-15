# Public ML Products

This folder stores public-safe ML schema, architecture, and methodology
products. It is separate from the approved runtime folders and must not contain
approved well-log rows, core rows, restricted well identifiers, populated
runtime configurations, trained models, or model performance metrics.

## Current Products

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

`approved_data_field_role_table_2026-06-15.csv`

This is the public-safe header role table used by
`dashboard/approved_data_intake.py`. It records original headers, normalized
names, source families, units, dtypes, model roles, public-display status, and
caveats. It includes V5.1 variable-fingerprint and mentor-question metadata,
but no approved row values.

## Public-Safe Templates

The schema-only templates are:

- `approved_data_intake_template_2026-06-15.csv`
- `approved_data_intake_validation_schema_2026-06-15.csv`
- `first_model_output_schema_2026-06-15.csv`
- `approved_data_source_column_registry_template_2026-06-15.csv`
- `approved_data_well_depth_index_template_2026-06-15.csv`
- `approved_data_x_allowed_candidate_template_2026-06-15.csv`
- `approved_data_y_target_registry_template_2026-06-15.csv`
- `first_model_output_schema_template_2026-06-15.csv`
- `variable_fingerprint_template_2026-06-15.csv`

These files are headers/schema only. They do not contain approved LAS/CSV/core
rows, private workbook rows, occurrence probabilities, saturation predictions,
trained model metrics, or sensitive identifiers.
