# Next Execution Checklist

Created: 2026-06-12

Use this checklist before rebuilding the Word document or slide deck.

## Before Editing Deliverables

- Read this revision base directory.
- Read `docs/SCIENCE_TO_ML_LOGIC_LADDER.md`.
- Read `docs/ML_PIPELINE_BASELINE_SOURCE_LEDGER.md`.
- Read `docs/ML_SOURCE_COVERAGE_AND_DELIVERABLE_REVISION_PLAN.md`.
- Read `docs/SWEET_SPOT_SOURCE_MATRIX.md`.
- Read `docs/WELL_LOG_REQUIREMENTS_MAP.md`.
- Read `docs/runtime_skeleton_brief.md`.
- Read `docs/project_blueprints/ml_parameter_effect_tree.csv`.
- Confirm `git status --short` and preserve unrelated user changes.
- Confirm no approved runtime data, restricted identifiers, trained model
  outputs, or sensitive derived outputs are being inserted into public files.

## Source Coverage Tasks

- Add or verify citation details for Singh et al. (2021).
- Add or verify citation details for Chong et al. (2024).
- Keep Chong et al. (2022) as the direct permafrost/well-log ML anchor.
- Keep USGS/DOE/NETL as the hydrate definition, stability, and North Slope
  context anchors.
- Keep comparative ML sources clearly labeled as method support.
- Keep project synthesis and ML notes clearly labeled as planning/methodology
  support.
- Use the baseline source ledger to distinguish recommended choices from
  optional future choices, especially for caliper QC, derived elastic features,
  Archie baselines, NMR/core target use, missing-log adapters, and sequence
  models.

## Word Document Tasks

- Update the Word builder first.
- Fill the Abstract and Introduction in paragraph form.
- Add a source-coverage/evidence-tier section.
- Rebuild the parameter section using repeated grammar:
  `physical reason`, `hydrate signal`, `false positives`, `ML role`,
  `source basis`.
- Add the three-tier parameter structure:
  stability context, reservoir quality, hydrate response.
- Label all numeric ranges as working screening envelopes for QC, feature
  engineering, and crossplots, not final cutoffs.
- Strengthen the methodology section around:
  - approved data intake;
  - unit and alias mapping;
  - depth alignment;
  - QC gates;
  - feature equations;
  - target registry and leakage barrier;
  - train-only preprocessing;
  - complete-well validation;
  - occurrence, saturation, uncertainty, and review outputs.
- Explain model options as a ladder: physics/rule baseline, simple supervised
  baseline, tree-based tabular model, ANN/MLP, optional LSTM only if complete
  depth sequences support it, and optional missing-log adapter only with
  provenance flags.
- Move website material to a short app/runtime-skeleton note or remove it from
  the main narrative.
- Keep results as planned output placeholders until approved-data validation is
  done.
- Regenerate the DOCX and inspect the section order.

## PowerPoint Tasks

- Update the slide visual builder second, using the Word plan as authority.
- Keep exactly nine slides.
- Preserve slide 1 as title/about-me.
- Keep slide 2 source-backed and methane-hydrate focused.
- Rebuild slide 3 around the three-tier science-to-ML parameter ladder.
- Rebuild slide 4 as raw headers -> QC/features/context -> classifier and
  regressor -> validation architecture.
- Rebuild slide 5 around physical behavior panels and false positives.
- Rebuild slide 6 around equations, geomechanics, broad screening envelopes,
  and crossplot hypotheses.
- Keep slide 7 as screening/context, not proof.
- Keep slide 8 as future outputs and error-review logic, not fake metrics.
- Keep slide 9 as conclusion plus next approved-data tasks.
- Regenerate the PPTX and inspect the raster panels.

## Verification Tasks

- Confirm the local PPTX has exactly 9 slides.
- Confirm changed slide panels render correctly at presentation size.
- Confirm the local DOCX exists and opens with expected section order.
- If uploaded to Drive, verify Drive readback and Google-rendered thumbnails.
- Run `git diff --check`.
- Run tests if code/builders/runtime behavior changed.

## Open Questions To Keep Visible

- Which field is the authoritative hydrate-saturation target?
- Is saturation supplied, NMR-derived, core-calibrated, interpreted, or a
  combination?
- Are saturation values fractions or percentages?
- Which phase labels and uncertain-label conventions are supplied?
- Which wells are known-label development wells, validation wells, locked-test
  wells, and prediction wells?
- Which intervals are excluded for bad-hole, missing curve, depth mismatch, or
  outlier reasons?
- What exact unit and alias mappings are used in the full workbook formulas?
