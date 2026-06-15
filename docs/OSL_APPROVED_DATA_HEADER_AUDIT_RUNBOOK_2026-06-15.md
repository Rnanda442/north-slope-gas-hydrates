# OSL Approved-Data Header Audit Runbook

Created: 2026-06-15

## Purpose

This runbook explains how to audit approved workbook, LAS, CSV, core, and NMR
headers inside OpenScienceLab without exporting restricted row-level values to
GitHub. The output is a public-safe readiness summary: recognized headers,
unknown headers, role assignments, missing fields, leakage risks, blocked
reasons, and mentor questions.

The audit does not train a model, calculate occurrence probability, predict
saturation, or prove hydrate.

## Command

From the repository root in OpenScienceLab:

```bash
git pull origin main
python 01_pipeline/validate_approved_data_headers.py \
  --source-csv path/to/approved_or_runtime_file.csv \
  --header-only \
  --source-label osl_header_audit_public_safe \
  --output-prefix osl_header_audit_2026-06-15
```

For a pasted/synthetic header list:

```bash
python 01_pipeline/validate_approved_data_headers.py \
  --headers "DEPTH,GR,RHOB,Rt,Sh,NMR_SAT,CAL1" \
  --source-label demo_public_safe \
  --output-prefix demo_header_audit_2026-06-15
```

For a CSV containing one header name per row:

```bash
python 01_pipeline/validate_approved_data_headers.py \
  --headers-csv path/to/header_list.csv \
  --source-label workbook_sheet_headers_public_safe \
  --output-prefix workbook_sheet_header_audit_2026-06-15
```

Use `--x-allowed "DEPTH,GR,RHOB,Rt"` when testing a proposed feature matrix.
If a Y-only target such as `Sh`, `Sgh`, `NMR_SAT`, Hydrate Saturation, `Swr`,
phase label, or occurrence label appears in `--x-allowed`, the report should
emit leakage flags.

## Header-Only Rules

- Use `--header-only` with `--source-csv`. The script reads CSV headers with
  `nrows=0`.
- Do not export approved row values, private workbook rows, restricted well
  identifiers, trained model outputs, or populated runtime configs.
- Do not pass private file names into public reports unless they are already
  approved for public display. By default, the script records only a sanitized
  source label.
- Use `--include-source-name` only when the source path/name is public-safe.

## Workbook And Sheet Header Audit

If the approved data is in Excel, audit headers inside OSL and export only a
header-list CSV, not workbook rows. The safe header-list CSV should contain one
column named `header` and one row per header. Optional public-safe columns can
include sheet role, unit-row text, and caveat summaries only if they do not
contain private row values.

Safe examples:

```text
header
DEPTH
GR
RHOB
Rt
Sh
NMR_SAT
CAL1
```

Then run:

```bash
python 01_pipeline/validate_approved_data_headers.py \
  --headers-csv osl_exported_header_list.csv \
  --source-label mte_refined_header_only \
  --output-prefix mte_refined_header_audit_2026-06-15
```

## Safe To Copy Back To GitHub

These summary artifacts can be copied back after review:

- CLI CSV readiness report;
- CLI JSON readiness report;
- Markdown readiness summary;
- sheet names if approved as public-safe metadata;
- header lists;
- unit-row summaries;
- row counts;
- depth range summaries;
- target-column presence/absence;
- caliper coverage counts;
- MTE/IGS/refined sheet confirmation;
- split candidate identifier summaries, with restricted identifiers anonymized;
- occurrence evidence field presence;
- saturation unit convention summary.

## Must Stay In OSL

Keep these out of GitHub and Streamlit:

- approved LAS/CSV/core/NMR row values;
- private workbook rows;
- restricted well identifiers unless explicitly anonymized and approved;
- raw target values for `Sgh`, `S_h`, `Sh`, `NMR_SAT`, Hydrate Saturation, or
  occurrence labels;
- populated runtime configs;
- trained model files;
- occurrence probabilities, saturation predictions, uncertainty values, or
  performance metrics from approved data before release review.

## What To Collect Next

For each workbook sheet or approved file, collect only public-safe summaries:

- sheet names and sheet roles;
- header lists;
- unit rows or unit metadata;
- row counts;
- depth minimum and maximum summaries;
- target-column presence;
- caliper coverage counts;
- whether `MTE`, `IGS`, `MTE_refined`, and `IGS_refined` are wells, sheets,
  processing stages, or source datasets;
- split candidate identifiers or grouping fields, anonymized if restricted;
- occurrence evidence fields and confidence fields;
- saturation unit convention: fraction or percent;
- whether stability context is allowed only as context, mask, confidence,
  caveat, or blocked reason.

## Scientific Guardrails

- Stability is methane 5 ppt admissibility/context only.
- Stability is not hydrate proof, occurrence, saturation, sweet spots, or
  producibility.
- Occurrence is target/validation evidence only.
- Occurrence evidence can come from core/pressure-core, NMR/core-derived
  saturation, validated multi-log interpretation, or documented seismic
  indicators.
- `Sgh`, `S_h`, `Sh`, `NMR_SAT`, Hydrate Saturation, `Swr`, phase labels, and
  occurrence labels are Y-only target/calibration/validation fields.
- Target-only fields must never enter `X_allowed`.
