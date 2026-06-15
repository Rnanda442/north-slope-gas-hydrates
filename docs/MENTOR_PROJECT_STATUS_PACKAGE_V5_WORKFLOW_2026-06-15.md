# Mentor Project Status Package: V5 Workflow Diagrams

Created: 2026-06-15

## Purpose

This is a short public-safe mentor update around the V5 workflow diagrams. It
summarizes where the project stands, what has been completed, what remains
blocked by approved data and label authority, and which mentor decisions are
needed before the workflow becomes a results-bearing ML project.

This document does not contain approved well-log rows, core rows, restricted
identifiers, trained models, model metrics, hydrate predictions, saturation
outputs, or sweet-spot rankings.

## High-Level Status

The project is now organized as a two-surface workflow. OpenScienceLab is the
heavy-data workbench for source bundles, approved inputs, guarded calculations,
and later ML execution. GitHub and Streamlit are the public delivery surface
for diagrams, source-backed documentation, public scaffold counts, public-safe
CSV summaries, and website views. The V5 workflow diagrams now connect the
public scaffold, the stability-admissibility screen, schema coverage, feature
engineering, target leakage controls, future occurrence classification,
saturation regression, validation, and reviewed outputs in one architecture.

## What Has Been Completed

- Built the V5 full workflow diagram and ML architecture detail visual.
- Generated the diagram-first 9-slide PowerPoint companion and Word companion.
- Confirmed the current public scaffold has 8,084 wells.
- Preserved the guarded baseline methane 5 ppt stability screen with 22
  calculated admissibility intervals, 8 no-stable-interval rows, and 8,054
  blocked rows.
- Kept the stability language limited to pressure-temperature admissibility,
  source confidence, caveats, and blocked states.
- Built the non-stability schema coverage layer for the future approved ML
  workflow.
- Separated measured inputs, derived features, QC/alignment fields,
  calibration/reference fields, target-only saturation/phase fields, and
  unresolved fields.
- Locked the target-leakage rule that fields such as Sgh, S_h, Sh, NMR_SAT,
  Hydrate Saturation, Swr, S_wr, and interpreted phase labels are labels,
  calibration references, or validation overlays, not predictor features.
- Added Streamlit views for Schema Coverage & Architecture, Public ML
  Readiness, and Target Registry & Leakage.

## What Remains Blocked

- Approved LAS, CSV, core, NMR, workbook rows, and restricted runtime outputs
  cannot be committed to public GitHub or exposed through the public Streamlit
  app.
- Official occurrence labels are not yet locked.
- Official saturation target authority is not yet locked when Sgh, S_h, Sh,
  NMR_SAT, or hydrate-saturation columns differ.
- Final model training, validation metrics, saturation estimates, occurrence
  probabilities, and sweet-spot ranking remain blocked until approved data,
  labels, validation splits, and boundary review are complete.
- Temperature handling is still blocked for wells without adequate G10015
  control unless the mentor approves a scenario-only or proxy policy.

## Mentor Decisions Needed

1. Phase-curve policy: should the official public baseline remain methane
   5 ppt only, or should the deliverables include a clearly labeled scenario
   table?
2. Target authority: which saturation and occurrence labels are official for
   model training and validation?
3. Validation split: should final validation use whole-well holdout,
   compartment holdout, geographic holdout, or a staged combination?
4. Temperature handling: when G10015 is missing, should wells stay blocked, use
   nearest-control proxy tiers, or use explicit scenario-only gradients?
5. ML use of stability: is the stability screen allowed as context, confidence,
   reason flag, or mask only, never as a hydrate occurrence label?

## Weekday Report Bullets

- Monday: Organized the project around the V5 workflow that separates public
  delivery from the OSL approved-data workbench.
- Tuesday: Verified the guarded stability screen as pressure-temperature
  admissibility only, with calculated, no-interval, and blocked states kept
  separate.
- Wednesday: Added the schema and target-leakage layer so measured inputs,
  derived features, QC fields, and saturation labels have distinct roles.
- Thursday: Aligned the V5 PowerPoint and Word companion to explain how
  stability context can feed future feature engineering without becoming proof.
- Friday: Prepared mentor decisions on phase-curve policy, target authority,
  validation split, missing-temperature handling, and allowed ML use of
  stability context.

## Safe Mentor Language

The stability screen is a guarded admissibility layer. It can say that a public
well interval is pressure-temperature admissible under the methane 5 ppt
baseline and available source controls. It cannot prove hydrate occurrence,
estimate saturation, confirm final stability, validate ML performance, or rank
sweet spots. Occurrence and saturation remain future approved-runtime outputs
after target authority, whole-well validation, and public-release review.

