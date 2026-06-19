# DOE Real-Data Runtime Execution Done / Needed Handoff

## Prompt Worked On

Prompt 13: DOE Jupyter Real-Data Runtime Execution And Public-Safe Export.

## Status

Blocked on this laptop. This prompt must be completed on the DOE desktop or
another approved runtime machine that has the real local approved datasets.

## Done

- Ran the required Git checks in the clean worktree for this prompt.
- Confirmed the current branch is:
  `codex/prompts-11-13-laptop-20260619`
- Fetched all remotes.
- Checked for the expected approved-runtime filenames without opening workbook
  content:
  `curated_dataset1.xlsx`, `curated_dataset2.xlsx`,
  `curated_dataset3.xlsx`, and `wellnametodataset.txt`.
- Targeted laptop search found no matching approved-runtime dataset files in:
  `%USERPROFILE%\Downloads\Northslopedatasets06052026`,
  `%USERPROFILE%\Downloads`, `%USERPROFILE%\Documents`, or
  `C:\Users\gargi\Documents\AI powerpoint`.
- Prompt 12 produced a ready code package for the DOE/approved machine:
  `outputs_public/doe_jupyter_code_package_2026_06_19/`
- Prompt 12 also produced a local ignored zip:
  `outputs_public/doe_jupyter_code_package_2026_06_19.zip`

## Not Run

The real-data runtime was not run on this laptop because the required approved
workbooks were not found and this machine is not confirmed as the DOE approved
runtime machine for those files.

Not run here:

- header inspection against real workbooks;
- schema discovery against real workbook sheets;
- target-only leakage audit against real columns;
- train/test/external-score workflow;
- train-only preprocessing/scaling;
- baseline or MLP/ANN fitting;
- model run tracker summaries from real runs;
- feature-family, validation-readiness, target-coverage, or model-review graph
  generation from real DOE data.

## Still Needed On DOE / Approved Runtime Machine

1. Move or unzip the Prompt 12 package on the DOE desktop.
2. Keep real data in a local approved folder outside GitHub.
3. Verify expected filenames:
   `curated_dataset1.xlsx`, `curated_dataset2.xlsx`,
   `curated_dataset3.xlsx`, and optional `wellnametodataset.txt`.
4. Run package verification:

```powershell
python verify_package.py --data-dir "<approved data folder>"
```

5. Run header inspection:

```powershell
python run_header_scan.py --data-dir "<approved data folder>"
```

6. Review header inventory and target-like column inventory before model runs.
7. Run baseline only after target role, units, and leakage exclusions are clear:

```powershell
python run_three_dataset_baseline.py --data-dir "<approved data folder>" --target auto --model baseline
```

8. If baseline setup succeeds and dependencies support it, run MLP:

```powershell
python run_three_dataset_baseline.py --data-dir "<approved data folder>" --target auto --model mlp
```

9. Export row-free model-run review assets:

```powershell
python run_model_run_review_assets.py --project-root . --output-dir outputs_runtime/model_run_review_assets_current
```

10. Keep all runtime outputs under ignored local folders such as
    `outputs_runtime/`, `models_runtime/`, `logs_runtime/`, and
    `configs_local/`.

## Public-Safe Review Candidates

After DOE runtime execution, only row-free, reviewed summaries should be
considered for GitHub or Drive. Candidate review outputs may include:

- workbook/sheet/header inventory with no rows;
- target-like column inventory with no row values;
- feature-exclusion audit at column-summary level;
- model run tracker summary with no row-level predictions;
- feature-family coverage plot;
- validation-readiness plot;
- target coverage plot;
- model-run review brief.

Do not push these until they are checked for private identifiers, local paths,
row-level predictions, sensitive tokens, raw approved values, model binaries, or
unsupported hydrate claims.

## Guardrails

- Do not commit approved workbook rows or raw workbook files.
- Do not commit row-level predictions, fitted models, fitted scalers, or
  serialized pipelines.
- Do not commit private runtime manifests, private well identifiers, local
  machine paths, secrets, credentialed PDFs, or private screenshots.
- Stability remains context/admissibility only; it is not proof of hydrate
  occurrence, saturation, producibility, or ranking.
- Training-fit metrics are not final model performance claims.

## Branch / Commit

- Branch: `codex/prompts-11-13-laptop-20260619`
- Commit: pending at handoff creation; see final response / branch history.
