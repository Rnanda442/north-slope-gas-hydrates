# V20 Three-Version Package

Date: 2026-07-12

This folder contains the Git-safe V20 scaffold for three fixed comparison
versions:

| Version | Short name | Purpose |
|---|---|---|
| V20A | `baseline_safe` | Re-run the lower-bias V19-style baseline: Ridge alpha 10 on `safe_normalized`, plus logistic balanced occurrence using the same feature family. |
| V20B | `equation_dominance` | Stress-test the user's reversed-weight idea: primary measured/safe log variables get weight 0.25 and equation/geomechanics variables get weight 1.0. |
| V20C | `hydrate02_core_prior` | Use the HYDRATE-02 Table S1 core `Sh(IW)` rows only as a frozen external porosity-to-saturation prior/auxiliary feature. This is not target backfill and not validation truth for the four active wells. |

## Boundary

GitHub contains only this scaffold, configs, and run instructions. Approved
workbook rows, model matrices, row-level predictions, runtime logs, fitted
models, private identifiers, and populated runtime configs stay outside Git in
ignored runtime folders.

The single core-data workbook expected by the DOE-facing code is:

```text
actual_core_data_combined.xlsx
```

Put it in the DOE input folder:

```text
Downloads/Northslopedatasets06052026
```

V20 reads the HYDRATE-02 prior from sheet `12_Candidate_Sh_Targets` inside that
combined workbook. The older runtime CSV remains a fallback only when the
combined workbook is missing. Workbook rows and fallback CSV rows are ignored by
Git and read only inside the local/DOE runtime.

## Expected Private Input

The runner needs a private, standardized model matrix CSV exported from the DOE
runtime notebook or workbook processing step. It must include:

```text
well_alias
hydrate_saturation_reference
```

Useful feature columns include any of:

```text
gr_api
rhob_g_cc
density_porosity_vv
neutron_porosity_vv
rt_ohm_m
vp_m_s
vs_m_s
nmr_porosity_vv
log10_rt
clean_sand_score
vp_vs_ratio
acoustic_impedance
shear_impedance
shear_modulus_gpa
bulk_modulus_gpa
youngs_modulus_gpa
poisson_ratio
lambda_rho
mu_rho
vsh_larionov_tertiary
```

If the matrix is missing, the runner can still print the plan:

```powershell
python doe_anaconda_final_kit/v20_three_versions/run_v20_three_versions.py --print-plan
```

To run the actual comparison:

```powershell
python doe_anaconda_final_kit/v20_three_versions/run_v20_three_versions.py `
  --model-matrix-csv "C:\path\to\private_model_matrix.csv"
```

Optional override if the combined workbook is not in the default Downloads
folder:

```powershell
python doe_anaconda_final_kit/v20_three_versions/run_v20_three_versions.py `
  --model-matrix-csv "C:\path\to\private_model_matrix.csv" `
  --core-workbook "C:\path\to\actual_core_data_combined.xlsx"
```

Outputs are written under ignored `outputs_runtime/v20_three_versions/` unless
you pass `--output-dir`.

Occurrence metrics use labels derived from `hydrate_saturation_reference >=
0.05` and balanced-logistic probabilities classified at `0.5` by default.

## Interpretation Rules

- V20A is the baseline.
- V20B is a physics stress test, not an automatic winner candidate.
- V20C is a frozen external core-prior check, not proof that HYDRATE-02 validates
  WellA/WellB/WellC/WellD.
- Do not choose future weights or thresholds by repeatedly ranking on WellA,
  WellB, and WellD.
- Report combined metrics, per-well metrics, and saturation-bin bias together.
