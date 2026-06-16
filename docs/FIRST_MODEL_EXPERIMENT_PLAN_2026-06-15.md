# First Model Experiment Plan

Created: 2026-06-15

## Purpose

This plan defines the first approved-runtime ML experiment to run later. It is
not a training result and does not claim model performance. It specifies the
dataset shape, split, baselines, candidate models, leakage checks, metrics, and
outputs needed before occurrence classification or saturation regression can be
reported.

## Current Status

The public repo is ready for model architecture and schema design only. The
public side has diagrams, counts, target-leakage rules, schema tables, and
guarded stability-admissibility context. It has zero approved occurrence or
saturation label rows and no training-ready public rows.

The first real experiment waits for approved LAS/CSV/core/NMR/workbook rows in
the authorized runtime.

The V5.2 deck and Word companion are the current mentor-facing explanation of
this plan. They show occurrence classification and saturation regression as
linked but separate future tasks, with stability retained as context,
confidence, caveat, mask, or blocked reason only.

The public repo now has a tested intake validator in
`dashboard/approved_data_intake.py`. It is a header/metadata check only: it can
say whether an approved-runtime dataset has the required column families,
target-leakage barrier, target authority metadata, unit policy, and split
readiness, but it does not train a model or inspect approved row values.

The validator now has a command-line header-audit runner:
`01_pipeline/validate_approved_data_headers.py`. It accepts inline headers,
header-list CSVs, or CSV headers with `--source-csv ... --header-only`, then
writes public-safe CSV/JSON readiness reports. The demo report under
`data/public_ml_products/intake_readiness_reports/` confirms the current public
state: schema design can proceed, but training remains false until approved
rows, target authority, split policy, validation plan, and release review are
available.

## Current ML Architecture Decisions And Open Mentor Questions

### A. Ready to encode now

- Train two linked tasks, not one blended target: occurrence classification
  outputs `P(hydrate)` or class labels, while saturation regression outputs
  `Sh_pred` only where an approved saturation target exists.
- Occurrence evidence can come from core or pressure-core observations,
  NMR/core-derived saturation, validated log interpretation, or documented
  seismic indicators. Stability remains context/admissibility only.
- Split by whole well, compartment, or geography before preprocessing. Numeric
  predictors get train-only 0-1 scaling after split. Depth remains the
  alignment/context axis unless mentor approves it as a predictor.
- Preserve units above or beside original headers. Every variable must pass the
  fingerprint contract: original header, unit, normalized name, role, feature
  permission, leakage risk, and unresolved mentor question.
- Use caliper coverage first. If `caliper`, `CAL1`, or differential caliper is
  not available at useful coverage, carry a missing-QC flag instead of applying
  a washout filter.
- Use source-checked feature families when data supports them: `GR`
  shale/clean-sand proxy, density porosity, resistivity transforms, `Vp`, `Vs`,
  `Vp/Vs`, impedance, elastic attributes, NMR-density separation, and approved
  equation-list features.
- Run baselines first, tree/boosting second, and ANN/Keras third. Chong et al.
  2024 is an external hydrate ML anchor for ANN occurrence classes and
  saturation prediction, not a North Slope performance claim:
  <https://pubs.usgs.gov/publication/70250169>.
- Keep missing-log strategy as a decision box. Alternate log combinations are
  preferred when optimal logs are missing; missing-log adapter models for `Vp`
  or `RHOB` are optional and validation-required. MDPI/Naim et al. supports the
  concept in marine hydrate settings but not automatic North Slope transfer:
  <https://www.mdpi.com/1996-1073/16/23/7709>.
- Well-MTE and Well-IGS can be described as Mt. Elbert and Ignik Sikumi case
  study wells in the Eileen Gas Hydrate Trend. `MTE_refined` and `IGS_refined`
  remain workbook-stage questions until approved metadata confirms them:
  <https://www.osti.gov/servlets/purl/1893637>.

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

## Dataset Shape Needed

Minimum training table shape:

| Table | Grain | Required content |
|---|---|---|
| `X_allowed_candidate` | well-depth sample | Measured logs, derived features, QC fields, and approved context only. |
| `Y_occurrence` | well-depth interval or aligned depth sample | Occurrence labels from approved phase/core/log interpretation policy only. |
| `Y_saturation` | well-depth sample or interval | Approved saturation target such as `Sgh`, `S_h`, `Sh`, `NMR_SAT`, or `Hydrate Saturation`. |
| `split_registry` | whole well or geologic group | Train/validation/test assignment made before preprocessing. |
| `source_confidence` | row or interval | Source, unit, alignment, QC, and label confidence flags. |

Minimum row requirements before any training claim:

- at least two split groups with complete wells;
- enough positive and negative occurrence labels to measure precision and
  recall;
- enough saturation labels to report regression metrics by held-out wells;
- source-resolved units for depth, density, porosity, resistivity, and velocity;
- explicit missingness/QC flags.

## Separate Tasks

Occurrence and saturation are linked but separate tasks.

| Task | Output | Target authority needed |
|---|---|---|
| Occurrence classification | `P(hydrate)` and calibrated occurrence class | Mentor-approved occurrence label policy from core/pressure-core observations, NMR/core-derived saturation threshold, validated log interpretation, or seismic indicator policy. |
| Saturation regression | `Sh_pred` with uncertainty | Mentor-approved saturation target among `Sgh`, `S_h`, `Sh`, `NMR_SAT`, or `Hydrate Saturation`, including fraction/percent convention. |

Stability cannot create either target. Stability may enter `X_allowed` only as
context, mask, confidence, caveat, or blocked reason if approved.

## Occurrence Evidence Policy

Occurrence should be treated as an approved label or validation target, not as a
quantity produced by the stability screen. In the sources and future approved
runtime, occurrence evidence can come from:

- core or pressure-core observations of hydrate;
- NMR/core-derived saturation that exceeds a mentor-approved occurrence
  threshold;
- validated multi-log interpretation with documented method, interval, and QC;
- regional seismic indicators only when spatial/depth support and allowed use
  are documented.

Each occurrence label needs a source, well/depth interval, evidence type,
confidence flag, and uncertainty/caveat. If those fields are missing, the row
stays blocked for occurrence training.

## Split Strategy

Default split policy:

1. Assign split by whole well before preprocessing.
2. If the mentor prefers stronger spatial testing, use compartment or
   geographic/geologic holdout.
3. Keep a locked test split untouched until target authority and preprocessing
   are fixed.
4. Fit imputation, scaling, feature selection, thresholds, and model weights on
   training wells only.

Random depth-row splits are not acceptable for final claims because adjacent
depth samples from the same well can leak geology, tool response, and target
patterns across train/test boundaries.

## Feature Blocks

Allowed candidate predictors:

- measured logs: depth, `GR`, `RHOB`/`Rho_b`, `Rt`/confirmed resistivity,
  `Vp`, `Vs`, `NMRPHI`, caliper where available;
- derived features: `Vsh`, density porosity, `Vp/Vs`, acoustic impedance,
  lambda-rho, mu-rho, NMR-density separation, approved resistivity transforms;
- QC fields: missingness, washout/caliper, outlier status, depth alignment,
  source confidence;
- context: hydrate AU, permafrost context, stability status, caveat and blocked
  reason fields if mentor approves context-only use.

Excluded from predictors:

- `Sgh`, `S_h`, `Sh`, `NMR_SAT`, `Hydrate Saturation`, `Swr`, `S_wr`;
- occurrence labels, interpreted phase labels, core-confirmed labels;
- target-derived ranks, final sweet-spot labels, or final model outputs.

## Baselines First

Run transparent baselines before candidate ML:

| Baseline | Purpose |
|---|---|
| Majority/stratified occurrence baseline | Checks whether the classifier beats trivial class frequency. |
| Simple threshold/logistic baseline | Tests whether a small set of source-backed features explains occurrence. |
| Linear or ridge saturation regression | Gives a transparent saturation reference before complex models. |
| Physics/proxy checks | NMR-density separation or Archie-style checks only when inputs and assumptions are approved. |

If candidate ML does not beat these baselines on held-out wells, do not present
it as the project model.

## Candidate Models

After leakage controls pass:

- tree model or gradient boosting for tabular baselines and feature importance;
- random forest or boosted trees for nonlinear log interactions;
- ANN/Keras model as the Chong-style direct gas hydrate ML anchor;
- two-head architecture only if shared feature blocks improve validated
  occurrence and saturation performance without leakage.

## Evaluation Metrics

Occurrence classification:

- precision;
- recall;
- F1 or balanced accuracy when class imbalance is strong;
- calibration curve / reliability;
- false-positive review by well, lithology, QC, and mimic risk.

Saturation regression:

- RMSE;
- MAE;
- R2 only where approved labels exist;
- residual plots by well, depth, lithology, QC, source confidence, and target
  source.

Do not report metrics from public scaffold rows, synthetic examples, or
stability-screen outputs.

## Leakage Checks

Required checks before training:

1. Assert no target-only column appears in `X_allowed`.
2. Assert target-derived columns are absent from feature selection.
3. Assert split is assigned before preprocessing.
4. Assert imputation/scaling/feature selection are fit only on training wells.
5. Assert duplicate or adjacent rows from a held-out well do not appear in
   training data.
6. Assert stability status is not used as occurrence proof or saturation target.
7. Assert public outputs are reviewed before any row-level prediction leaves the
   approved runtime.

## Output Schema

Approved runtime outputs later:

| Output | Grain | Notes |
|---|---|---|
| `occurrence_probability` | well-depth sample or interval | Probability output from classifier, not proof. |
| `occurrence_class` | well-depth sample or interval | Only after threshold/calibration policy is approved. |
| `Sh_pred` | well-depth sample or interval | Saturation estimate with uncertainty and target-source caveat. |
| `prediction_uncertainty` | well-depth sample or interval | Model and data-quality uncertainty. |
| `reason_flags` | well-depth sample or interval | Top supporting features, missingness, caveats, mimic risks. |
| `blocked_reason` | row/interval | Why the row cannot be predicted or validated. |
| `public_release_status` | row/output package | Whether output is approved for public summary only. |

The schema-only public template for these future outputs is:

```text
data/public_ml_products/first_model_output_schema_2026-06-15.csv
```

Public outputs before validation:

- diagrams;
- source-backed counts;
- schema and field-role tables;
- caveats and blocked reasons;
- synthetic examples clearly labeled;
- public-safe summaries only.

No public output should claim trained ML performance, hydrate proof, saturation
prediction, or sweet-spot ranking until approved validation and release review
are complete.
