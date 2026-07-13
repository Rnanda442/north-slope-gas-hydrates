# DOE V20 Three-Version Run Instructions

Date: 2026-07-12

Use this Git-safe V20 scaffold:

```text
doe_anaconda_final_kit/v20_three_versions/
```

The three fixed versions are:

| Version | Role |
|---|---|
| V20A baseline safe | Ridge alpha 10 on `safe_normalized`; use as the baseline anchor. |
| V20B equation dominance | Primary measured/safe log inputs weight 0.25; equation/geomechanics inputs weight 1.0. |
| V20C HYDRATE-02 core prior | Frozen HYDRATE-02 Table S1 porosity-to-`Sh(IW)` prior used as an auxiliary feature only. |

## Required Private Input

The runner needs a standardized private model-matrix CSV from the approved DOE
runtime. It must include:

```text
well_alias
hydrate_saturation_reference
```

Recommended feature columns are listed in:

```text
doe_anaconda_final_kit/v20_three_versions/README.md
```

Do not commit the model matrix to Git.

Use one combined core-data workbook for all core context and Hydrate-02
candidate target evidence:

```text
actual_core_data_combined.xlsx
```

Place that workbook in:

```text
Downloads/Northslopedatasets06052026
```

V15-V18 now auto-detect that combined workbook first. V20 reads its
HYDRATE-02 prior from sheet `12_Candidate_Sh_Targets`. The older standalone
candidate CSV remains a fallback only when the combined workbook is missing.

## Plan-Only Check

From the repo root:

```powershell
python doe_anaconda_final_kit/v20_three_versions/run_v20_three_versions.py --print-plan
```

## Run With Private Matrix

```powershell
python doe_anaconda_final_kit/v20_three_versions/run_v20_three_versions.py `
  --model-matrix-csv "C:\path\to\private_model_matrix.csv"
```

Optional explicit workbook override:

```powershell
python doe_anaconda_final_kit/v20_three_versions/run_v20_three_versions.py `
  --model-matrix-csv "C:\path\to\private_model_matrix.csv" `
  --core-workbook "C:\path\to\actual_core_data_combined.xlsx"
```

Optional:

```powershell
python doe_anaconda_final_kit/v20_three_versions/run_v20_three_versions.py `
  --model-matrix-csv "C:\path\to\private_model_matrix.csv" `
  --write-predictions
```

`--write-predictions` writes row-level predictions only under ignored
`outputs_runtime/`. Do not move those predictions to GitHub.

## Expected Outputs

The runner writes to:

```text
outputs_runtime/v20_three_versions/<timestamp>/
```

Key files:

| File | Meaning |
|---|---|
| `v20_run_manifest.json` | Run settings, variant definitions, and output paths |
| `v20_saturation_metrics.csv` | Combined and per-well saturation metrics |
| `v20_occurrence_metrics.csv` | Combined and per-well occurrence metrics derived from the fixed threshold |
| `v20_saturation_bin_metrics.csv` | Per-well saturation-bin error/bias checks |
| `v20_feature_weights.csv` | Exact feature weights used by each V20 version |
| `v20_hydrate02_core_prior_audit.csv` | HYDRATE-02 core-prior fit status and tiny-core warning |

## Claim Control

Occurrence labels are derived from `hydrate_saturation_reference >= 0.05`.
Balanced-logistic probabilities are classified at `0.5` by default unless a
pre-locked policy changes `--class-probability-threshold`.

Use this language:

```text
V20 compares three pre-declared development variants under the known four-well
transfer setup. V20A is the baseline; V20B is an equation-dominance stress
test; V20C is a frozen external HYDRATE-02 core-prior diagnostic. The run is
not blind new-well validation.
```

Do not say that HYDRATE-02 validates the four active wells. It is external
target-side physics evidence unless matching Hydrate-02 logs and a separate
split policy are approved.
