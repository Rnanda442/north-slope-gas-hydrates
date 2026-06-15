# Approved-Data Intake Spec

Created: 2026-06-15

## Purpose

This is the minimum viable intake contract for the later approved runtime. It
turns the visible headers/screenshots and current schema matrix into a concrete
checklist for loading approved LAS/CSV/core/NMR/workbook data without exposing
approved rows in the public repo.

This document is public-safe. It contains header names, roles, unit rules,
blocked conditions, and output schema expectations only.

## Public Boundary

Public GitHub and Streamlit may show:

- source-backed counts and diagrams;
- header names and field roles;
- unit and dtype expectations;
- feature dictionaries and caveats;
- public stability/admissibility context;
- synthetic examples clearly labeled as synthetic.

Public GitHub and Streamlit must not show:

- approved well-log/core/NMR rows;
- restricted well identifiers or private workbook rows;
- trained models or approved-data metrics;
- occurrence probabilities, saturation predictions, or sweet-spot rankings from
  approved data.

## Current ML Architecture Decisions And Open Mentor Questions

### A. Ready to encode now

- Train two linked but separate outputs: occurrence classification and
  saturation regression. Occurrence is a target/validation label, not something
  measured by the stability screen.
- Use train-only 0-1 scaling for numeric predictors after the validation split.
  Depth stays the well/depth alignment and context axis, not automatically a
  normalized predictor. Units must stay visible beside original headers.
- Use a variable fingerprint before model entry: original header, unit,
  normalized name, role, allowed-in-feature-matrix flag, leakage risk, and any
  unresolved mentor question.
- Apply caliper coverage first. If enough `caliper`, `CAL1`, or differential
  caliper exists, use it for washout QC; otherwise create a missing-QC flag,
  not an automatic filter.
- Allow measured and derived features only after fingerprint, unit, leakage,
  and source checks: `GR`, density porosity, resistivity transforms, `Vp`,
  `Vs`, `Vp/Vs`, impedance, elastic attributes, NMR-density separation, and
  equation-list features.
- Model order is baselines first, tree/boosting second, and ANN/Keras third.
  Chong et al. 2024 supports ANN-style hydrate occurrence classes and
  saturation prediction as an external ML anchor:
  <https://pubs.usgs.gov/publication/70250169>.
- Treat Well-MTE as the Mt. Elbert Stratigraphic Test Well and Well-IGS as the
  Ignik Sikumi Test Well, both North Slope / Eileen Gas Hydrate Trend case
  study wells. Keep `MTE_refined` and `IGS_refined` as workbook-structure
  questions until metadata confirms raw/refined stages:
  <https://www.osti.gov/servlets/purl/1893637>.
- Keep missing-log adapters as optional and validation-required. The MDPI
  missing `Vp`/`RHOB` work is relevant background, but it does not automatically
  validate North Slope permafrost use:
  <https://www.mdpi.com/1996-1073/16/23/7709>.

### B. Blue mentor questions

- Which saturation field is authoritative: `Sgh`, `S_h`, `Sh`, or `NMR_SAT`?
- Should occurrence use source-style classes, saturation thresholds, or
  mentor-reviewed intervals?
- Are `MTE`/`IGS` separate wells and are `*_refined` processing stages in the
  workbook?
- Do we have enough caliper coverage to apply washout filtering?
- Which wells become blind validation after full recovery?
- Are missing-log adapters allowed, or should missing curves simply block that
  feature set?

## Field Role Table

The public-safe field-role table is:

```text
data/public_ml_products/approved_data_field_role_table_2026-06-15.csv
```

Required columns in that table:

| Column | Meaning |
|---|---|
| `original_header` | Header exactly as visible in screenshots or schema notes. |
| `normalized_name` | Runtime-safe alias used after provenance is preserved. |
| `source_dataset` | Public-safe sheet/dataset family, not private row data. |
| `role` | `predictor`, `derived_feature`, `QC`, `context`, `target_only`, `calibration_reference`, or `unresolved`. |
| `unit` | Expected unit or unit-review status. |
| `expected_dtype` | Runtime dtype expectation. |
| `required_for_model` | Whether the field is required, optional, target-only, or blocked pending review. |
| `public_safe_to_show` | Whether public outputs may show header/metadata only or public summaries. |
| `caveats` | Specific unit, leakage, provenance, or unresolved-rule warning. |

## Runnable Public-Safe Validator

The header-only validator module is:

```text
dashboard/approved_data_intake.py
```

It loads the field-role table and can validate a list of source columns or a
synthetic/test DataFrame. It reports recognized headers, unknown headers,
missing required families, target-only fields, target-leakage risk in
`X_allowed`, unresolved mnemonics, unresolved unit fields, minimum viable
predictor coverage, occurrence/saturation target authority, split readiness,
training readiness, and blocked reasons.

The validator is metadata-only. It does not require or expose approved row
values.

## Command-Line Header Audit

The public-safe CLI runner is:

```text
01_pipeline/validate_approved_data_headers.py
```

It supports:

```bash
python 01_pipeline/validate_approved_data_headers.py --headers "DEPTH,GR,RHOB,Rt,Sh"
python 01_pipeline/validate_approved_data_headers.py --headers-csv path/to/header_list.csv
python 01_pipeline/validate_approved_data_headers.py --source-csv path/to/data.csv --header-only
```

When `--source-csv` is used, `--header-only` is required and the script reads
only `nrows=0`. It writes public-safe CSV and JSON readiness reports to:

```text
data/public_ml_products/intake_readiness_reports/
```

The demo report is:

```text
data/public_ml_products/intake_readiness_reports/demo_header_audit_2026-06-15.csv
data/public_ml_products/intake_readiness_reports/demo_header_audit_2026-06-15.json
docs/APPROVED_DATA_INTAKE_READINESS_REPORT_2026-06-15.md
```

The demo uses only synthetic/project-safe headers. It shows schema design is
ready, training is not ready, target authority remains blocked, split and
validation policy are still required, and no approved row values are present.

The OSL runbook is:

```text
docs/OSL_APPROVED_DATA_HEADER_AUDIT_RUNBOOK_2026-06-15.md
```

## Minimum Required Columns

The approved runtime should refuse model training unless each loaded source can
resolve these fields or an explicit approved substitute:

| Requirement | Accepted headers or source | Runtime rule |
|---|---|---|
| Well/source identity | well id, source file, sheet, or approved runtime identifier | Required for grouped split and provenance; public exports must anonymize or remove restricted identifiers. |
| Depth | `DEPTH`, `DEPT`, `Depth_ft`, `True Depth` | Required. Convert to `depth_m` with source unit recorded. |
| Depth alignment/provenance | `Depth correspondence at ML data`, `depths_unitD`, `depths_unitC`, source sampling fields | Required for refined tables and core/NMR alignment. |
| At least one lithology/reservoir curve | `GR`, density/porosity family | Required for baseline occurrence interpretation. |
| At least one hydrate-response curve family | resistivity, NMR, sonic/elastic, or core/NMR target evidence | Required before any occurrence/saturation modeling. |
| Target authority | `Sgh`, `S_h`, `Sh`, `NMR_SAT`, `Hydrate Saturation`, phase/core labels | Required for training/validation; target fields remain Y-only. |
| QC status | caliper/differential caliper, missingness, outlier flags, source confidence | Required for review and filtering; missing QC must be flagged. |

## Required Log Curves For First Runtime Build

Minimum measured predictors:

- depth in feet or meters, standardized to `depth_m`;
- `GR`;
- `RHOB` / `Rho_b` / density;
- deep resistivity such as `Rt` or confirmed `RES`;
- at least one porosity curve or approved density-porosity calculation.

Optional but valuable predictors:

- `NMRPHI` / `phi_nmr`;
- `Vp` / `VELP`;
- `Vs` / `VS1`;
- `Ratio Vp/Vs`;
- impedance;
- caliper / `CAL1` / differential caliper;
- approved public context fields such as hydrate AU, permafrost context, and
  stability-admissibility status.

Target/calibration fields:

- `Sgh`, `S_h`, `Sh`, `NMR_SAT`, `Hydrate Saturation`;
- `Swr` / `S_wr` only as calibration/reference unless mentor confirms a
  non-leaking use;
- interpreted phase/core labels only as occurrence labels or validation
  evidence after target authority is approved.

Occurrence-label intake fields:

- evidence source such as core, pressure core, NMR/core-derived saturation,
  validated log interpretation, or documented seismic indicator;
- well/depth interval or alignment basis;
- binary/categorical occurrence label after mentor-approved policy;
- confidence and uncertainty/caveat fields;
- threshold or interpretation rule when occurrence is derived from saturation
  or log interpretation.

Stability-admissibility status cannot fill any occurrence-label field.

## Unit Conversion Rules

| Family | Rule |
|---|---|
| Depth | Preserve original feet/meters flag; canonical runtime depth is meters. |
| Density | Convert kg/m3 to g/cc when equations expect g/cc; preserve source unit. |
| Porosity/saturation | Record whether source is fraction 0-1 or percent 0-100 before modeling. |
| Sonic/velocity | Distinguish direct velocity from slowness-derived velocity; do not mix `DT`/`DTS` with `Vp`/`Vs` without provenance. |
| Resistivity | Preserve tool mnemonic; unconfirmed `AO90`/`AF90` stays blocked from predictors. |
| Caliper | Preserve inches/mm and reference hole diameter before washout flags. |
| Stability context | Keep pressure-temperature context as admissibility/mask/confidence/caveat only. |

## Blocked Conditions

The approved runtime should mark a well/depth row blocked, not silently impute,
when any of these apply:

- no usable depth basis;
- source unit is unknown for a required curve;
- target-only field would enter `X_allowed`;
- target authority is unresolved for training labels;
- split assignment is missing before preprocessing;
- train/validation/test split is random by depth row for final claims;
- required model family has no approved label rows;
- G10015 temperature coverage is missing and no mentor-approved proxy/scenario
  policy exists;
- public-release review has not approved an output.

## Intake Output Schema

The approved runtime intake should produce these tables inside the authorized
environment:

| Table | Grain | Role |
|---|---|---|
| `source_column_registry` | one row per source column | Original headers, normalized names, units, roles, and caveats. |
| `well_depth_index` | one row per well-depth sample | Standardized depth, source identity, split group, and alignment status. |
| `X_allowed_candidate` | one row per well-depth sample | Predictor, derived-feature, QC, and approved context columns only. |
| `Y_target_registry` | one row per target field/source | Target authority, task, unit, confidence, and allowed use. |
| `blocked_intake_rows` | one row per blocked source row | Blocked reason, source, and required fix. |

No public export should include approved row-level values until boundary review
explicitly approves it.

## Public-Safe Templates

The public repo now includes schema-only CSV templates for the future approved
runtime:

```text
data/public_ml_products/approved_data_intake_template_2026-06-15.csv
data/public_ml_products/approved_data_intake_validation_schema_2026-06-15.csv
data/public_ml_products/first_model_output_schema_2026-06-15.csv
data/public_ml_products/approved_data_source_column_registry_template_2026-06-15.csv
data/public_ml_products/approved_data_well_depth_index_template_2026-06-15.csv
data/public_ml_products/approved_data_x_allowed_candidate_template_2026-06-15.csv
data/public_ml_products/approved_data_y_target_registry_template_2026-06-15.csv
data/public_ml_products/first_model_output_schema_template_2026-06-15.csv
data/public_ml_products/variable_fingerprint_template_2026-06-15.csv
```

These templates define expected table columns, validation checks, blocked
reasons, and future model-output fields. They contain no approved rows,
well-log values, private workbook rows, trained metrics, predictions, or
sensitive identifiers.
