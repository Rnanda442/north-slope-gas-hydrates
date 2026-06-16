# Final New Slide Deck Creation Prompt

Created: 2026-06-15

## Purpose

Use this prompt to create the next North Slope gas hydrate slide deck from the
current conversation, original Gmail deck structure, V5.2 complex architecture
slides, and website visual language.

This prompt replaces the earlier idea of fragmenting the complex V5.2 diagrams.
Those diagrams are important and should stay together as whole-slide
architecture plates.

## Source Materials To Review First

Before building the deck, review these local files:

- `docs/project_blueprints/presentation_assets/processing_revisions_2026_06_11/processing_panel_contact_sheet.jpg`
- `docs/project_blueprints/presentation_assets/processing_revisions_2026_06_11/slide_01_about_me.png`
- `docs/project_blueprints/presentation_assets/processing_revisions_2026_06_11/slide_02_hydrate_intro.png`
- `docs/project_blueprints/presentation_assets/processing_revisions_2026_06_11/slide_03_parameter_scaffold.png`
- `docs/project_blueprints/presentation_assets/processing_revisions_2026_06_11/slide_04_ml_architecture.png`
- `docs/project_blueprints/presentation_assets/processing_revisions_2026_06_11/slide_05_parameter_behavior.png`
- `docs/project_blueprints/presentation_assets/processing_revisions_2026_06_11/slide_06_geomechanics.png`
- `docs/project_blueprints/presentation_assets/processing_revisions_2026_06_11/slide_07_map_context.png`
- `docs/project_blueprints/presentation_assets/processing_revisions_2026_06_11/slide_08_results_plan.png`
- `docs/project_blueprints/presentation_assets/processing_revisions_2026_06_11/slide_09_conclusion.png`
- `docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_15/full_workflow_deck_contact_sheet.png`
- `docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_15/full_project_ml_workflow_flowchart_expanded.png`
- `docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_15/ml_pipeline_network_detail_v5.png`
- `docs/SCIENCE_TO_ML_LOGIC_LADDER.md`
- `docs/ML_PIPELINE_BASELINE_SOURCE_LEDGER.md`
- `docs/WELL_LOG_REQUIREMENTS_MAP.md`
- `docs/APPROVED_DATA_SCHEMA_COVERAGE_AND_MODEL_ARCHITECTURE_PLAN.md`
- `docs/APPROVED_DATA_INTAKE_SPEC_2026-06-15.md`
- `docs/FIRST_MODEL_EXPERIMENT_PLAN_2026-06-15.md`
- `docs/FINAL_DELIVERABLE_CONSOLIDATION_AND_CLEANUP_PLAN_2026-06-15.md`
- `docs/FINAL_NINE_SLIDE_GAP_AND_DIAGRAM_REUSE_PLAN_2026-06-15.md`
- `dashboard/app.py`, especially the four-page website structure and the
  `Analyze Hydrates` tabs: `Public ML Readiness`, `Schema Coverage &
  Architecture`, `Target Registry & Leakage`, `Runtime Readiness`, and
  `Methods & Evidence`.

## Design Rules

- Keep the original Gmail/rule-book nine-slide topic structure.
- Use the Gmail deck's clean raster-panel look: white/light background, thin
  teal side rail, clear title hierarchy, one strong bottom takeaway, compact
  source footer, restrained teal/blue/green/amber/red accents.
- Use the website look as supporting style: public-safe status cards, clean
  tabular readiness language, diagram plates, source counts, caveat boxes, and
  clear public/approved-runtime boundaries.
- Keep the complex V5.2 diagrams together as whole-slide architecture plates.
  Do not crop, fragment, or scatter them across multiple slides.
- If the complex diagrams are hard to read, redraw them at full 16:9
  presentation scale while preserving the complete architecture in one place.
- Preserve original headers when shown. Canonical aliases are metadata only.
- Do not expose approved/raw rows, restricted identifiers, populated runtime
  paths, trained models, performance metrics, occurrence probabilities,
  saturation predictions, hydrate proof, or sweet-spot rankings.
- Blue callouts are for runtime confirmations only, not for decisions already
  settled in the base.

## Required Scientific And ML Decisions To Show

- Occurrence classification and saturation regression are linked but separate
  future ML tasks.
- Occurrence labels come from approved target/validation evidence, not the
  stability screen.
- Saturation/ground-truth fields are target-only: `Sgh`, `S_h`, `Sh`,
  `NMR_SAT`, `Hydrate Saturation`, `Swr`, `S_wr`, interpreted phase labels,
  and occurrence labels never enter `X_allowed`.
- Numeric predictors are train-only normalized 0-1 after the whole-well,
  compartment, or geographic split. Depth stays the unnormalized alignment and
  context axis.
- Units must stay visible above or beside original source headers before
  normalization.
- Every variable needs a fingerprint: original header, unit, normalized name,
  role, feature-matrix permission, leakage risk, unit status, and unresolved
  runtime note.
- Caliper is coverage-first. Show `caliper`, `CAL1`, and differential caliper
  as data that must be gathered before active washout filtering is claimed.
- Candidate features include only source/QC/unit/leakage-cleared features:
  `GR`, density porosity, resistivity transforms, `Vp`, `Vs`, `Vp/Vs`,
  impedance, elastic attributes, NMR-density separation, and equation-list
  features.
- Model order is baselines first, tree/boosting second, ANN/Keras third.
- Stability is context/admissibility only. It is not hydrate proof,
  occurrence, saturation, or a model result.
- Only about 3 of 71 datasets are currently visible, which is enough for
  schema and architecture readiness but not final training or metrics.

## Prompt To Create The Deck

```text
Create a new exact nine-slide North Slope gas hydrate presentation.

Use the original Gmail/rule-book topic structure as the slide structure, the
Gmail deck as the visual style authority, the current website as the supporting
public-safe visual language, and the V5.2 workflow package as the method and
architecture authority. The deck should look polished and scientific, not like
a generic PowerPoint or a crowded website screenshot.

Keep exactly nine slides:

Slide 1 - Title / About Me / Project Promise
Keep the original Gmail about-me structure: title, project framing, personal
photo/drawing/activity elements, and a public-safe boundary note. Do not replace
this with the V5.2 project-only cover. The takeaway should be that the project
builds a defensible workflow for future hydrate occurrence classification and
saturation regression.

Slide 2 - Introduction: What And Why Gas Hydrates
Fix the current slide 2 image problem. Do not use the dark SEM/hydrate image as
the dominant intro visual. Replace it with a cleaner source-backed hydrate
introduction: a clear methane-in-water-cage visual, a small source-backed SEM or
hydrate sample inset, a simple pressure-temperature stability gate, and a small
North Slope context map. Explain methane hydrate as CH4 trapped in H2O cages,
then explain why North Slope occurrence, saturation, reservoir quality, gas
charge, migration, and production are separate questions. Stability is necessary
context only, not proof.

Slide 3 - Parameters And Well-Log Scaffold
Keep this as the parameter/well-log scaffold slide. Correct it so it shows every
type of variable and the sticky variable fingerprint. Include measured inputs,
derived features, QC/alignment fields, context features, calibration/reference
fields, target-only fields, and unresolved fields. Show original headers and
units above the normalized 0-1 value concept. Show depth as the unnormalized
alignment/context axis. Preserve original headers such as DEPTH, True Depth,
Depth_ft, DEPT, Rho_b, RHOB, Density_gpcc, Phi_porosity, phi_den, DPHI, NMRPHI,
phi_nmr, caliper, CAL1, differential caliper, Rt, RES, AO90, GR, Vs, VS1, Vp,
VELP, Ratio Vp/Vs, and impedance. Mark Sgh, S_h, Sh, NMR_SAT, Hydrate
Saturation, Swr, S_wr, interpreted phase labels, and occurrence labels as
target-only.

Slide 4 - ML Methodology And Architecture: Whole Workflow Plate
Keep the complex architecture in one place. Use the V5.2 expanded workflow map
as a whole-slide architecture plate, or redraw it at full-slide scale while
preserving the same complete structure. It must show source/schema controls,
public versus approved-runtime boundary, stability context, feature
engineering, target-only labels, leakage barrier, X_allowed feature matrix,
whole-well split, train-only preprocessing, model ladder, occurrence classifier,
saturation regressor, validation, outputs, blocked/future conditions, and
mentor decisions. Do not fragment this diagram.

Slide 5 - Why Parameters And Model Choices Matter
Use the original Gmail parameter-behavior idea, but strengthen it. Show why no
single log proves hydrate. For each major family, show what it measures, why it
can support hydrate interpretation, what can mimic or hide the signal, and its
ML role. Include GR/lithology, density/porosity, resistivity, Vp, Vs, Vp/Vs,
impedance, NMR/core support, and caliper/QC. Also show why the model sequence is
baselines first, tree/boosting second, ANN/Keras third.

Slide 6 - Geomechanics, Equations, And Unit Gate
Correct the equation slide so it is readable and not a dense formula wall. Show
equation chips with variable names and units: GR shale/clean-sand proxy, density
porosity, resistivity transforms, Vp/Vs, acoustic impedance, lambda-rho, mu-rho,
Young's modulus, Poisson's ratio, brittleness, NMR-density separation, and
Archie/resistivity hydrate proxy where source/QC/unit/leakage checks allow it.
Make clear that features are active only after units, source, QC, and leakage
checks pass.

Slide 7 - Map And Well Context
Keep the original map/context topic. Use the website's clean public-map look:
North Slope context, public regional/stability layers, source coverage, and
future approved-runtime well evidence. Make clear that public maps and the
stability screen guide context and review only. They do not confirm hydrate
occurrence, saturation, producibility, or sweet spots.

Slide 8 - Results, Discussion, And Review Logic: ML Runtime Plate
Keep the V5.2 ML runtime detail as a whole-slide plate. Do not fragment it.
This slide should show X_allowed, the target-only rail, split controls,
train-only preprocessing, baseline gate, tree/boosting/ANN candidate model,
occurrence head, saturation head, validation against approved labels, reviewed
output package, uncertainty/reason flags, and the no-results guardrail. It
should function as the results/review logic slide because it explains how future
outputs will be judged. Do not show fake metrics, fake confusion matrices, fake
saturation tracks, or final performance.

Slide 9 - Conclusion And Next Steps
Close with what has been completed and what remains. State that the current
contribution outside stability is the schema coverage matrix, field-role table,
intake spec, target-leakage barrier, variable fingerprint, header-audit
validator, first model experiment plan, and whole-well validation design. Add
blue runtime-confirmation callouts only for: target priority when multiple
saturation labels exist, fraction-vs-percent convention, occurrence-label
provenance, train/validation/locked-test well assignment, caliper coverage
sufficiency, and missing-log adapter policy.

Acceptance checks:
- Exactly nine slides.
- Original Gmail/rule-book topic sequence is preserved.
- Slide 2 uses a better gas hydrate introduction image/composition than the
  current dark SEM-dominant slide.
- Complex V5.2 architecture slides are kept intact as whole-slide plates.
- Website visual language is visible through clean status cards, source
  boundary language, readiness/caveat boxes, and public-safe diagrams.
- Target-only labels visually bypass X_allowed and never enter the feature
  matrix.
- Occurrence classification and saturation regression are separate future
  outputs.
- Depth is not normalized with other predictors.
- Units stay visible before normalization.
- Caliper is shown as coverage-first, not assumed filtering.
- ANN/Keras appears after baselines and tree/boosting.
- No approved rows, fake results, trained metrics, hydrate proof, occurrence
  probabilities, saturation predictions, or sweet-spot rankings.
- Generate a contact sheet and visually inspect every slide before Drive upload.
```

## Practical Build Notes

- Use `docs/project_blueprints/build_processing_slide_assets.py` for the
  Gmail-style raster-panel build.
- Use `docs/project_blueprints/build_ml_revamp_powerpoint.py` for the
  final PowerPoint rebuild.
- Keep `docs/project_blueprints/build_full_workflow_diagram_deliverables.py`
  as the source for the complex V5.2 architecture plates, not as the final
  topic-order authority.
- Rebuild slide 2 first because its current main image/composition is the most
  visibly wrong part of the original Gmail-style sequence.
