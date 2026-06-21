# Four-Well Runtime ML Pipeline

Created: 2026-06-20

Purpose: make the current four-well Mount Elbert / Ignik Sikumi / Hydrate-01 /
HYDRATE 02 workflow runnable on a DOE laptop without committing approved row
values, core rows, trained models, or predictions.

## What This Adds

The runtime runner is:

```text
01_pipeline/run_four_well_ml_pipeline.py
```

It reads approved local CSVs, joins committed public-safe context, and writes
runtime outputs under ignored folders:

```text
approved_runtime/four_well/
outputs_runtime/
models_runtime/
```

Those folders are intentionally ignored by Git.

## Required Local CSVs

Copy these public templates into `approved_runtime/four_well/`, then fill them
with DOE/approved rows on the laptop:

```text
data/public_ml_products/four_well_log_table_template_2026-06-20.csv
data/public_ml_products/four_well_core_sample_template_2026-06-20.csv
data/public_ml_products/four_well_split_registry_template_2026-06-20.csv
data/public_ml_products/four_well_runtime_manifest_template_2026-06-20.csv
```

Expected local names for the simplest combined-table path:

```text
approved_runtime/four_well/four_well_logs.csv
approved_runtime/four_well/four_well_core_samples.csv
approved_runtime/four_well/four_well_split_registry.csv
```

The core CSV is optional. The logs CSV is required.

The runner also accepts separate screenshot-style CSV exports, so you do not
have to hand-merge them first:

```text
approved_runtime/four_well/MTE.csv
approved_runtime/four_well/IGS.csv
approved_runtime/four_well/MTE_refined.csv
approved_runtime/four_well/IGS_refined.csv
```

Supported log CSV shapes:

- flat MTE-style table with headers such as `Depth_ft`, `Density_gpcc`,
  `phi_den`, `phi_nmr`, `S_h`, `S_wr`, `GR`, `phi_neut`, `CAL1`, `A090`,
  `VELP`, `VS1`, `depths_unitD`, and `depths_unitC`;
- flat IGS-style table with headers such as `DEPT`, `RHOB`, `NPHI`, `DPHI`,
  `NMRPHI`, `GR`, `caliper`, `RES`, `VP`, `VS`, `Sh`, and `Swr`;
- refined MTE-style paired depth/Sgh blocks for Unit D and Unit C, including
  `Depth correspondence at ML data`;
- refined IGS-style `Depth (ft)` / `Hydrate Saturation` / `Sgh` pair tables;
- a role/mnemonic/unit/description header block where the mnemonic row is the
  usable column-header row.

## Command

From the repository root:

```powershell
python 01_pipeline\run_four_well_ml_pipeline.py `
  --data-dir approved_runtime\four_well `
  --logs four_well_logs.csv `
  --core four_well_core_samples.csv `
  --split four_well_split_registry.csv `
  --target auto `
  --target-task auto `
  --model baseline `
  --run-label four_well_pilot
```

Use an explicit target if the authoritative field is already known:

```powershell
python 01_pipeline\run_four_well_ml_pipeline.py `
  --data-dir approved_runtime\four_well `
  --target Sgh `
  --target-task regression `
  --run-label four_well_sgh_regression
```

For separate CSV exports from the screenshot-style workbook:

```powershell
python 01_pipeline\run_four_well_ml_pipeline.py `
  --data-dir approved_runtime\four_well `
  --logs MTE.csv IGS.csv MTE_refined.csv IGS_refined.csv `
  --core four_well_core_samples.csv `
  --split four_well_split_registry.csv `
  --target auto `
  --run-label four_well_screenshot_exports
```

## Join Logic

The runner joins local rows to the committed four-well index by:

1. `object_id`
2. `api_number`
3. normalized aliases such as `MTE`, `Well-MTE`, `MT ELBERT 1`, `IGS`,
   `MTE_refined`, `IGS_refined`, `Ignik Sikumi`, `Hydrate-01`, and
   `HYDRATE 02`

The public identity spine is:

```text
data/public_ml_products/four_well_case_location_index_2026-06-19.csv
```

## Stability Map Use

The runner joins public stability context from:

```text
data/public_stability_products/public_ml_feature_scaffold_2026-06-15.csv
```

Stability fields are context, coverage, caveat, or feature candidates only.
They are not hydrate occurrence labels and are not saturation targets.

Current committed status for the four primary wells is still:

```text
blocked_missing_temperature_profile
```

That means the current map can provide public AU/depth/permafrost context, but
not final stability top/base/thickness for these wells until the temperature
profile/source bundle gap is resolved.

## Core Data Use

The committed core evidence registry is:

```text
data/public_ml_products/four_well_core_evidence_registry_2026-06-20.csv
```

The runtime core CSV can include point samples or intervals:

```text
sample_depth_m
sample_top_m
sample_base_m
```

Core rows are matched to the nearest log row or to log rows inside the sample
interval. The output is an overlay:

```text
four_well_core_log_matches.csv
```

The runner does not silently spread sparse core values into continuous log
targets. Use core hydrate saturation as a training target only after the source
and label policy are explicitly approved.

## Outputs

Each run writes:

```text
dataset_inventory.csv
four_well_enriched_log_rows.csv
four_well_core_log_matches.csv
four_well_core_evidence_registry.csv
target_detection.csv
feature_columns.csv
split_registry_used.csv
train_metrics.csv
eval_metrics.csv
predictions_*.csv
run_manifest.json
```

If a target is missing, training is blocked but readiness files are still
written. If a non-training split has features but no target values, predictions
are written with `predicted_unlabeled` status.

## Guardrails

- `Sgh`, `S_h`, `Sh`, `NMR_SAT`, `Hydrate Saturation`, occurrence labels, and
  phase labels are target-only.
- API numbers, object IDs, coordinates, field names, and source IDs are not
  model features.
- `A090`, `AO90`, and `AF90` are mapped to canonical `rt_ohm_m` for this
  four-well runtime, with `rt_source_mnemonic` retained for review.
- Refined depth/Sgh pair tables are target overlays. They should not be used
  as continuous feature rows unless they are matched to feature-bearing logs
  under an approved alignment policy.
- Whole-well split is applied before fitting preprocessing or model weights.
- IGS is log/NMR-supported but remains unresolved for actual core rows.
- Hydrate-01 and HYDRATE 02 pressure-core rows should be validation or
  calibration overlays unless approved target policy says otherwise.
- Do not commit `approved_runtime`, `outputs_runtime`, or `models_runtime`.
