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

`public_parameter_evidence_registry_2026-06-16.csv`

This is the public-safe parameter evidence board for the website and next
slide/Word pass. It turns the science-to-ML logic ladder into normalized visual
bars for stability, reservoir quality, hydrate-response logs, QC, and Y-only
targets. Numeric ranges are working screening envelopes from the project
synthesis, not final DOE cutoffs; directional rows stay directional until
source recovery and approved-data calibration confirm thresholds.

`source_visual_inventory_2026-06-16.csv`

This is the public-safe visual provenance and QA inventory for the V5.4
corrected website, slide, and Word visual layer. It tracks V5.4 slide panels,
V5.3 reference panels, website captures, source-backed visuals, authority
diagrams, and contact sheets with source status,
provenance, allowed use, QA status, replacement flags, and guardrails. It is
displayed in Analyze Hydrates > Presentation Exports and is tested by
`tests/test_source_visual_inventory.py`.

`model_run_tracker_summary_template_2026-06-16.csv`

`model_run_feature_audit_template_2026-06-16.csv`

`model_run_stability_join_template_2026-06-16.csv`

These are public-safe templates for the DOE local model-run tracker. The
website can read actual ignored runtime summaries from `outputs_runtime/` inside
the approved environment, while GitHub carries only the expected summary shape,
feature/exclusion audit shape, and stability-join contract. The tracker summary
template is row-free: it records run/target status, feature-family counts,
validation status, stability-join placeholder, and final-claim blockers without
prediction rows or fitted model paths. Do not populate
these templates with approved workbook rows, row-level predictions, fitted
models, or final performance claims.

`approved_data_field_role_table_2026-06-15.csv`

This is the public-safe header role table used by
`dashboard/approved_data_intake.py`. It records original headers, normalized
names, source families, units, dtypes, model roles, public-display status, and
caveats. It includes V5.1 variable-fingerprint and mentor-question metadata,
but no approved row values.

`four_well_core_evidence_registry_2026-06-20.csv`

This is the public-safe evidence-status table for MTE, IGS, Hydrate-01, and
HYDRATE 02. It records which wells currently have log/NMR support, core or
pressure-core support, source-only support, or unresolved core-row status. It
does not contain row-level core measurements.

`four_well_log_table_template_2026-06-20.csv`

`four_well_core_sample_template_2026-06-20.csv`

`four_well_split_registry_template_2026-06-20.csv`

`four_well_runtime_manifest_template_2026-06-20.csv`

These are the DOE/local runtime templates used by
`01_pipeline/run_four_well_ml_pipeline.py`. Copy them into an ignored local
runtime folder such as `approved_runtime/four_well/`, populate them with
approved rows on the DOE laptop, and keep the populated copies out of Git.

`intake_readiness_reports/demo_header_audit_2026-06-15.csv`

`intake_readiness_reports/demo_header_audit_2026-06-15.json`

These are demo outputs from the public-safe CLI header audit runner:
`01_pipeline/validate_approved_data_headers.py`. The demo uses synthetic/project
safe headers only. It shows schema design readiness, training not ready, blocked
reasons, and mentor questions without approved row values.

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
- `model_run_tracker_summary_template_2026-06-16.csv`
- `model_run_feature_audit_template_2026-06-16.csv`
- `model_run_stability_join_template_2026-06-16.csv`
- `four_well_log_table_template_2026-06-20.csv`
- `four_well_core_sample_template_2026-06-20.csv`
- `four_well_split_registry_template_2026-06-20.csv`
- `four_well_runtime_manifest_template_2026-06-20.csv`

These files are headers/schema only. They do not contain approved LAS/CSV/core
rows, private workbook rows, occurrence probabilities, saturation predictions,
trained model metrics, or sensitive identifiers.

## Header Audit CLI

Run from the repository root:

```bash
python 01_pipeline/validate_approved_data_headers.py \
  --headers "DEPTH,GR,RHOB,Rt,Sh,NMR_SAT,CAL1" \
  --source-label demo_public_safe \
  --output-prefix demo_header_audit_2026-06-15
```

When using `--source-csv`, pass `--header-only`. The script reads only CSV
headers with `nrows=0`; it never prints or writes row values. Private-looking
paths are sanitized by default unless `--include-source-name` is explicitly
used for a public-safe source name.
