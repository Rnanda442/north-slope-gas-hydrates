# DOE V10 Run And Upload Instructions - 2026-06-27

Run this version first:

`docs/current_source_bundle_2026_06_26/DOE_MASTER_ML_PIPELINE_EQUATION_FIRST_V10_CHONG_DPHI_LOCK.ipynb`

Keep this as the fallback only if V10 fails before it produces outputs:

`docs/current_source_bundle_2026_06_26/DOE_MASTER_ML_PIPELINE_EQUATION_FIRST_V9_GEOMECH_CHONG_ANN.ipynb`

## Single Execution Prompt

Run the V10 notebook on the DOE desktop against `~/Downloads/Northslopedatasets06052026`. Use the normal full run if the machine can sit for it. If the full Chong ANN sensitivity is too slow, restart the kernel, run `import os; os.environ["CHONG_RUNTIME_MODE"] = "quick_test"` in a temporary first cell before the notebook setup cell, then run V10 only as a smoke test. If PyTorch is unavailable in the DOE kernel, V10 should mark the Chong ANN tables as skipped/failed for that dependency and still continue to the export cell.

After V10 finishes, the easiest handoff is one file from `~/Downloads/outputs_runtime/ml_master/`:

- `share_packet_v10_chong_dphi_lock.zip`

Use this clean workbook for slides, Word, and quick review:

- `clean_summary_v10_chong_dphi_lock.xlsx`

The detailed runtime files are still written for debugging, but the ZIP is the
main thing to paste back into Codex or email to yourself for review.

Also capture screenshots of these notebook outputs:

- startup prints showing `CODE_VERSION`, active wells, input/output paths, and density-porosity policy
- `Source header contracts`
- `Density-porosity source counts`
- `Correctness checks`
- `Chong ANN WLC summary`

Do not upload row-level outputs until reviewed:

- `predictions_v10_chong_dphi_lock.csv`
- `selected_predictions_v10_chong_dphi_lock.csv`
- `occurrence_predictions_v10_chong_dphi_lock.csv`
- `chong_ann_selected_predictions_v10_chong_dphi_lock.csv`
- `model_results_v10_chong_dphi_lock.xlsx`
- `chong_ann_results_v10_chong_dphi_lock.xlsx`
- `selected_models_v10_chong_dphi_lock.joblib`

If Outlook is available on the DOE desktop, V10 also writes:

- `draft_share_packet_email_v10_chong_dphi_lock.ps1`

That script opens a draft email with the share packet attached. It does not send
automatically. Set the `PERSONAL_REVIEW_EMAIL` environment variable first if
you want the `To:` field prefilled.

## Header Evidence To Check

V10 treats the source screenshots as two separate data contracts:

- Mallik stacked header format:
  `docs/evidence/email_screenshots_2026_06_12/screenshot_2026-06-05_131418.png`
  and `screenshot_2026-06-05_131426.png`
- Alaska MTE/IGS direct-header and refined target formats:
  `screenshot_2026-06-08_111056.png`, `screenshot_2026-06-08_111108.png`,
  `screenshot_2026-06-08_111117.png`, and `screenshot_2026-06-08_111124.png`

The important V10 check is that `density_porosity_policy_summary_v10_chong_dphi_lock.csv`
shows source density porosity mapped for the wells where the headers provide
`Phi_porosity`, `phi_den`, or `DPHI`. RHOB-derived `phi_density_calc` should be
the fallback/proxy, not the first-choice Chong `phi`.
