# DOE Publishable Analytics And GitHub Handoff Plan

Created: 2026-06-18

## Purpose

This plan defines how the project should move from "the model ran on the DOE
desktop" to a publishable analytics package with slide-ready figures,
paper-ready graphs, and source-backed interpretation.

The key idea is that GitHub carries the public-safe scaffold, code, templates,
source manifests, and reviewed summary outputs. The DOE desktop carries the
approved rows, raw workbooks, source PDFs, fitted models, row-level predictions,
and full runtime products until review. After the model is done, only a
reviewed, row-free analytics package comes back to GitHub.

## Operating Boundary

### GitHub can contain

- Source intake inventories, source-use notes, source-to-feature maps, and
  prompt/runbooks.
- Public-safe code for source intake, header audits, model-run tracking,
  plotting, and export packaging.
- Public GIS/stability products and Excel/CSV-derived stability screenshots.
- Schema templates, feature-role tables, target registries, leakage-check
  templates, and synthetic/demo rows.
- Slide-ready and paper-ready figures only after release review confirms they
  contain no approved row-level values, private identifiers, restricted paths,
  fitted model paths, or raw predictions.
- Row-free metrics summaries when approved for public communication.
- Figure sidecars that record source ids, figure purpose, data grain, release
  status, and caveats.

### GitHub must not contain

- Raw DOE workbooks, LAS files, core/NMR row tables, or approved private rows.
- Row-level model predictions, fitted models, scalers, SHAP row matrices, local
  runtime manifests, or private output paths.
- Gmail exports, private Drive exports, raw source PDFs with unclear license, or
  large source bundles.
- Any figure that lets a viewer reconstruct private row values or restricted
  well identifiers before review.

### DOE desktop contains

- Approved workbook/LAS/core/NMR/source rows.
- Drive/Gmail source PDFs and screenshots for review.
- Full local model run folders under ignored runtime paths.
- Fitted models and local prediction tables.
- High-resolution diagnostic plots before public-safe review.
- The final reviewed export package before the allowed subset is copied back to
  GitHub.

## Source-Backed ML Interpretation Map

The sources should define what the analytics look for. They should not become
automatic labels unless the approved data owner or mentor has approved that
target policy.

| Evidence family | What the source-backed signal looks like | ML use | Figure use |
|---|---|---|---|
| Clean reservoir gate | Gamma ray lower/cleaner interval, reservoir-quality lithology context, not a hydrate proof by itself. | Feature family, lithology/reservoir gate, false-positive control. | Log track panel and feature family coverage heatmap. |
| Resistivity response | Resistivity shifts right/high across a candidate interval. Needs porosity, lithology, stability, NMR/core, and mimic checks. | Candidate hydrate-response predictor and interaction feature. | Depth-aligned log-response panel with mimic labels. |
| Sonic/elastic response | Vp, Vs, impedance, Vp/Vs, lambda-rho, or mu-rho shifts that may reflect stiffening, but can also reflect lithology, cement, ice, or compaction. | Predictor family and derived-feature audit. | Elastic response inset and feature importance grouped by family. |
| NMR/core support | NMR T2, NMR porosity, core, pressure-core, or lab calibration supports pore-scale hydrate or reservoir properties. | Target authority, calibration, validation, or source-confidence field depending on data owner rules. | NMR/core confirmation strip beside log tracks. |
| Caliper/QC | In-gauge interval is more trustworthy; washout or poor borehole condition blocks or downweights log interpretation. | QC flag, exclusion reason, missingness feature, or blocked reason. | QC band in well-depth evidence stack. |
| Missing-log adapters | Vp, Vs, or density can be estimated only with validation and clear caveats. | Optional model-derived feature; never treated as measured without provenance. | Missing-log caveat badge and measured-vs-derived feature coverage. |
| Stability context | Excel/CSV-derived methane 5 ppt stability curve defines admissibility/context only. | Context flag, mask, caveat, or review overlay. Not occurrence or saturation. | Stability overlay panel using project-derived curve screenshots only. |

## Priority Sources To Drive The Analytics

| Source id | Source role | What DOE should inspect |
|---|---|---|
| `SRC_DRIVE_004` Aung et al. 2026 | Direct Alaska North Slope LWD source. | Log tracks, GR/resistivity/sonic/NMR/caliper/QC patterns, completion or interval-selection figures, captions that explain signal movements. |
| `SRC_DRIVE_002` Yoneda et al. 2026 | Direct Alaska North Slope NMR/core/permeability source. | NMR T2, log/lab calibration, permeability or core comparison figures, how NMR evidence supports reservoir interpretation. |
| `SRC_EXISTING_001` Chong et al. 2022 | Direct Alaska North Slope/Mackenzie ML source. | Feature families, model structure, how ANS examples connect log-derived features to hydrate characterization. |
| `SRC_EXISTING_002` Singh et al. 2021 | Saturation ML and optimal well logs. | Which logs were useful for saturation ML, leakage-safe separation of target saturation from predictors. |
| `SRC_NEW_001` Singh et al. 2020 | Automated log processing and lithology classification. | Preprocessing, lithology gate, optimal-feature logic. |
| `SRC_NEW_003` Rajabi et al. 2023 | Vs prediction from conventional logs. | Missing Vs strategy and uncertainty language. |
| `SRC_NEW_005` Dalvand and Falahat 2021 | Rock-physics shear velocity estimation. | Shear velocity derivation caveats and equation/feature provenance. |
| `SRC_DRIVE_001` Naim et al. 2023 | Vp/RHOB missing-log ML. | Missing Vp/RHOB workflow and transfer caveats. |
| `SRC_NEW_002` Collett et al. 2019 | Comparative field program. | Logging/coring integration examples; comparative context only. |

## DOE Publishable Analytics Package

After a DOE model run, create one ignored local folder:

```text
outputs_runtime/publishable_analytics_<YYYYMMDD_HHMM>/
```

Recommended structure:

```text
00_release_review/
  release_checklist.md
  public_safe_export_manifest.csv
  blocked_items.csv
01_source_signal_reference/
  source_signal_matrix.csv
  source_signal_matrix.png
  slide_03_log_signal_storyboard.md
02_model_inputs/
  feature_family_coverage.csv
  feature_family_coverage.png
  target_and_leakage_audit.csv
  target_and_leakage_audit.png
03_validation/
  model_metric_summary.csv
  model_metric_summary.png
  external_test_or_holdout_status.csv
  residuals_by_well_or_group.png
04_interpretability/
  feature_importance_by_family.csv
  feature_importance_by_family.png
  shap_or_permutation_summary_if_approved.png
05_well_panels/
  well_depth_evidence_stack_review_only.png
  slide_safe_log_response_panel.png
06_stability_overlay/
  stability_context_overlay.csv
  stability_context_overlay.png
  stability_caveats.md
07_paper_figures/
  fig_01_source_to_ml_workflow.png
  fig_02_log_signal_response.png
  fig_03_feature_target_leakage_matrix.png
  fig_04_validation_metrics.png
  fig_05_feature_importance.png
  fig_06_stability_context_overlay.png
08_slide_imports/
  slide_03_log_signal_response_panel.png
  slide_06_model_inputs_and_leakage.png
  slide_07_model_validation_summary.png
  slide_08_outputs_uncertainty_and_stability.png
09_public_safe_for_github/
  reviewed_model_summary_<date>.csv
  reviewed_feature_family_coverage_<date>.csv
  reviewed_figure_manifest_<date>.csv
  README_PUBLIC_SAFE_EXPORT_<date>.md
```

The first version can be generated by scripts after the existing model pipeline
runs. Until the exporter exists, DOE can manually assemble this structure from
the current runtime outputs and website screenshots.

## Slide-Ready Output Plan

Every slide import should be a 16:9 PNG, preferably 1920 x 1080 or larger, with
a matching sidecar record in `reviewed_figure_manifest_<date>.csv`.

| Slide output | Purpose | Inputs | Source relation |
|---|---|---|---|
| `slide_03_log_signal_response_panel.png` | Replace old parameter-range slide with signal-movement story. | Aung/Yoneda/Chong source review plus approved-safe synthetic or reviewed log track illustration. | Shows what hydrate-compatible signal movement looks like, not a final prediction. |
| `slide_03_source_signal_matrix.png` | Compact matrix of GR, resistivity, sonic/elastic, NMR/core, caliper/QC, stability. | Source signal matrix. | Directly connects each signal to source ids. |
| `slide_06_model_inputs_and_leakage.png` | Explain `X_allowed`, target-only fields, exclusions, and feature families. | Feature audit and target/leakage audit. | Mirrors what ML sources use while proving no leakage. |
| `slide_07_model_validation_summary.png` | Show training vs external/holdout status honestly. | Model metric summary and validation status. | Similar to source ML papers, but marked as current project run status. |
| `slide_08_outputs_uncertainty_and_stability.png` | Show predictions, uncertainty, blocked reasons, and stability context. | Public-safe summary and stability overlay. | Stability remains context only. |

Slide 3 should visually read left to right:

```text
Source signal examples -> depth-aligned log movement -> ML feature family -> caveat/mimic check
```

The slide should not be a table of static parameter ranges. It should show
movement: low GR gate, resistivity right-shift, sonic/elastic right-shift, NMR
or core support, in-gauge caliper, and stability-context strip.

## Paper Figure Plan

Paper figures should be exportable at publication resolution, with simple
captions and no private row-level data unless explicitly approved.

| Paper figure | Message | Notes |
|---|---|---|
| Figure 1: Source-to-ML workflow | The project converts source-backed hydrate indicators into a leakage-controlled ML workflow. | Can be public-safe immediately if it uses schema and workflow diagrams. |
| Figure 2: Log signal response concept | Hydrate-compatible interpretation needs aligned movements across lithology, resistivity, sonic/elastic, NMR/core, QC, and stability. | Use source-backed or synthetic/reviewed illustration. |
| Figure 3: Feature family and target audit | Predictors, targets, QC fields, and blocked fields are separated before modeling. | Row-free feature coverage only. |
| Figure 4: Validation summary | Model claims depend on held-out/whole-workbook or whole-well validation, not training fit. | Publish only approved high-level metrics. |
| Figure 5: Feature importance by family | ML is interpreted by feature family, not just individual spreadsheet columns. | Prefer grouped importance to avoid private feature leakage. |
| Figure 6: Stability context overlay | Stability screen is an admissibility/context overlay, not proof or label. | Use only Excel/CSV-derived stability curve screenshots/products. |

## Figure Sidecar Requirements

Every figure that leaves DOE should have one row in a manifest with these
fields:

```text
figure_id
file_name
intended_use
source_ids
data_source
data_grain
contains_private_rows
contains_row_level_predictions
contains_private_paths
approved_release_status
reviewer
caption
caveat
github_destination
```

Allowed `approved_release_status` values:

```text
approved_public_summary
approved_internal_only
blocked_private_rows
blocked_source_license
blocked_unclear_caption
blocked_needs_mentor_review
```

Only `approved_public_summary` files should be copied into GitHub.

## DOE Run Sequence

1. Pull the latest GitHub repo on the DOE desktop.
2. Put raw PDFs from Drive/Gmail into the ignored local source library.
3. Run the source inventory:

```powershell
python 01_pipeline\build_source_intake_inventory.py `
  --source-dir "data\source_library" `
  --source-dir "docs\evidence\slide02_source_bundle_2026_06_17" `
  --output-dir "docs\source_library_index" `
  --date-tag 2026-06-18
```

4. Review Aung 2026, Yoneda 2026, Chong 2022, Singh 2021/2020, and missing-log
   sources for the signal matrix.
5. Run the header scan and model pipeline from
   `docs/DOE_THREE_DATASET_ML_PIPELINE_RUNBOOK_2026-06-16.md`.
6. Open the local website Model Run Tracker and verify:
   - target-only fields are excluded from `X_allowed`;
   - depth is alignment/context unless mentor approved otherwise;
   - feature families are recorded;
   - external/holdout validation status is separate from training fit;
   - stability is context only.
7. Build the `publishable_analytics_<date>` folder.
8. Review every figure and CSV against the release checklist.
9. Copy only `09_public_safe_for_github/` and approved figure assets back into
   GitHub.
10. Update the main slide deck and paper from the approved slide/paper figure
    folders.

## GitHub Return Package

When DOE finishes a reviewed run, copy back this public-safe subset:

```text
data/public_ml_products/reviewed_model_summary_<date>.csv
data/public_ml_products/reviewed_feature_family_coverage_<date>.csv
docs/source_library_index/source_inventory_<date>.csv
docs/source_library_index/SOURCE_ORGANIZATION_REPORT_<date>.md
docs/project_blueprints/presentation_assets/doe_model_run_<date>/
docs/project_blueprints/paper_assets/doe_model_run_<date>/
docs/DOE_PUBLISHABLE_ANALYTICS_RUN_REPORT_<date>.md
```

Do not copy back:

```text
outputs_runtime/
models_runtime/
data_runtime/
approved workbooks
row-level predictions
fitted models
raw PDFs
private Drive/Gmail exports
private path manifests
```

## Definition Of Done

The analytics package is ready to support the main deck and research paper when:

- The source signal matrix names the paper/source for every visual claim.
- Slide 3 has a clear log-signal movement panel, not parameter ranges alone.
- Feature coverage and leakage audits prove targets stayed out of predictors.
- Model metrics are separated into training fit, external test, holdout, or
  blocked/no-label status.
- Any feature importance or SHAP-style output is grouped and release-reviewed.
- Stability visuals come only from the Excel/CSV-derived project products.
- Every slide/paper figure has a manifest row and an approved release status.
- The GitHub return package contains no private rows, raw predictions, fitted
  models, raw source PDFs, credentials, or private paths.
