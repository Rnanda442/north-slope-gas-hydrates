# Final Nine-Slide Gap And Diagram Reuse Plan

Created: 2026-06-15

## Purpose

This plan identifies what is lacking in the original/main nine-slide structure
and how to use the current Gmail-style deck, older V2 topic-aligned builder,
V5.2 method package, and complex diagram assets without letting the diagram
deck replace the original slide topics.

The rule is:

```text
original/main nine-slide topics stay fixed
Gmail deck controls visual style
older V2 topic-aligned builder controls slide structure
V5.2 supplies method content and intact complex architecture slides
complex diagrams stay together as whole-slide plates where they matter
```

No approved well-log rows, core rows, restricted identifiers, trained models,
model metrics, occurrence probabilities, saturation predictions, hydrate proof,
or sweet-spot rankings may be added.

## Materials To Use

### Topic And Visual Sources

- `docs/deliverable_revision_base_2026_06_12/01_email_instruction_digest.md`
- `docs/deliverable_revision_base_2026_06_12/05_slide_word_alignment_matrix.md`
- `docs/NINE_SLIDE_POWERPOINT_REVISION_WORKFLOW.md`
- `docs/project_blueprints/build_ml_revamp_powerpoint.py`
  - The `v2_slide_*` functions preserve the older topic-aligned structure.
- `docs/project_blueprints/build_processing_slide_assets.py`
  - Current Gmail-style raster-panel build path.
- `docs/project_blueprints/presentation_assets/processing_revisions_2026_06_11/`
  - Current Gmail-style slide panels.

### V5.2 Method And Diagram Sources

- `docs/project_blueprints/V5_2_FULL_WORKFLOW_ML_DIAGRAM_North_Slope_Gas_Hydrate_Slides_2026-06-15.pptx`
- `docs/project_blueprints/V5_2_North_Slope_Gas_Hydrate_Full_ML_Workflow_Companion_2026-06-15.docx`
- `docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_15/full_project_ml_workflow_flowchart.png`
- `docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_15/full_project_ml_workflow_flowchart_expanded.png`
- `docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_15/ml_pipeline_network_detail_v5.png`
- `docs/APPROVED_DATA_SCHEMA_COVERAGE_AND_MODEL_ARCHITECTURE_PLAN.md`
- `docs/APPROVED_DATA_INTAKE_SPEC_2026-06-15.md`
- `docs/FIRST_MODEL_EXPERIMENT_PLAN_2026-06-15.md`

## Diagram Reuse Policy

The complex V5/V5.2 diagram slides are important because they keep the whole
workflow in one place. Do not fragment, crop, or scatter them across the deck.
Use them as whole-slide architecture plates, and improve surrounding slides so
the audience is prepared to read them.

| Asset or slide family | Final use | Do not do |
|---|---|---|
| `full_project_ml_workflow_flowchart.png` | Use as the readable whole-project orientation if the expanded poster is too dense for the main architecture slide. | Do not chop it into fragments. |
| `full_project_ml_workflow_flowchart_expanded.png` | Keep intact as the whole-slide detailed architecture reference. Regenerate/redraw at presentation scale if needed, but keep the complete workflow together. | Do not crop it into small fragments. |
| `ml_pipeline_network_detail_v5.png` | Keep intact as the whole-slide ML runtime detail showing `X_allowed`, target-only rail, split, preprocessing, model heads, and validation. | Do not crop it into partial lanes. |
| V5.2 variable-fingerprint decision slide | Merge into original slide 3 as the variable "sticky fingerprint" rule. | Do not make it a separate replacement topic. |
| V5.2 model decision boxes | Split between original slide 4, slide 5, and slide 8. | Do not put all model decisions only on the conclusion slide. |
| V5.2 status and mentor decisions | Use only as slide 9 next-step language and blue review callouts. | Do not reopen known architecture decisions as if they are unanswered. |

## Slide-By-Slide Gap Plan

| Slide | Original topic | What is lacking now | Use from what we have | Treatment of complex diagrams | Final action |
|---|---|---|---|---|---|
| 1 | Title/about-me/project promise | Mostly not lacking. Risk is replacing the personal opener with a project-only V5.2 cover. | Keep Gmail slide 1/about-me authority and profile/photo style. | None. | Preserve the Gmail opener. Only adjust title/subtitle if needed to name occurrence classification and saturation regression. |
| 2 | Introduction: what and why gas hydrates | Needs a clearer "why this matters" link: hydrate definition, North Slope value, and why occurrence, saturation, reservoir quality, gas charge, migration, and production are different questions. | Keep the updated hydrate cage/SEM/P-T idea from Gmail-style slide 2. Use USGS/DOE/NETL source language and the science-to-ML ladder. | Use stability only as a small context gate. | Rebuild as an intro slide, not a stability-results slide. Make stability necessary but not proof. |
| 3 | Parameters and well-log scaffold | Still needs the sticky variable fingerprint and every variable type: measured input, derived feature, QC field, target-only field, calibration/reference field, context feature, unresolved field. It also needs units above normalized 0-1 value tracks. | Use the older V2 parameter scaffold topic, `ml_parameter_effect_tree.csv`, schema coverage matrix, field-role table, and visible original headers. | Use no large V5.2 diagram. Pull only the variable-fingerprint idea from V5.2. | Make this the main "we know every variable type" slide: original header, unit, normalized name, role, `X_allowed`, leakage risk, unit status, unresolved runtime note. |
| 4 | ML methodology and architecture | This is the most important weak slide. It must show the whole ML method in one place: ingestion, schema preservation, unit/QC, caliper coverage, leakage barrier, `X_allowed`, target rail, whole-well split, train-only scaling, baseline/tree/ANN, occurrence and saturation heads, validation. | Use the intact `full_project_ml_workflow_flowchart_expanded.png` or redraw it as a presentation-readable whole-slide architecture plate. | Keep the complex workflow together as one full-slide architecture map. | Rebuild the architecture as a coherent whole-slide diagram. Target-only fields visually bypass the feature matrix. |
| 5 | Why parameters and model choices matter | The slide can become only behavior panels, but it also needs model-choice rationale: why one log is not enough, why baselines first, why tree/boosting second, why ANN/Keras third. | Use current parameter behavior panel, science-to-ML ladder, ML ledger, and Chong-style ANN anchor. | No full diagram. Use small model ladder chip if needed. | Pair parameter mimics with model rationale. Each family should say measures, hydrate use, caveat, ML role. |
| 6 | Geomechanics, equations, and format cleanup | Needs equation features to be readable and connected to unit checks. It should not become a dense equation poster. | Use equation list from the ledger and well-log requirements: density porosity, resistivity transforms, `Vp/Vs`, impedance, elastic attributes, NMR-density separation, Archie/resistivity hydrate proxy where allowed. | No full diagram. Use V5.2 "unit/source/QC/leakage checks" as a small gate strip. | Use equation chips plus variable names and unit status. Depth stays unnormalized alignment/context; other numeric predictors are train-only 0-1 scaled after split. |
| 7 | Map and well context | Needs to explain what the map contributes without implying hydrate occurrence. Also needs the relation between public context, OSL/approved runtime, and future blind wells. | Use current map context slide, public stability screen context, public GIS layers, and source coverage language. | Do not use the complex diagrams here; use only short stability/context wording if needed. | Keep it as a map/context slide. Say map and stability guide review/context, not labels or proof. |
| 8 | Results, discussion, and review logic | Needs planned outputs and review logic, not fake results. It should show occurrence and saturation outputs as future reviewed outputs, plus calibration, residual review, uncertainty, and reason flags. | Use first model output schema, first model experiment plan, ML notes, and the intact V5.2 runtime detail. | Keep `ml_pipeline_network_detail_v5.png` intact as the full-slide runtime/review logic plate. | Show the whole ML runtime detail: occurrence head, saturation head, target-only rail, validation, reviewed output package, and no-results guardrail. |
| 9 | Conclusion and next steps | Needs to close with what is complete outside stability and what is still needed. Risk is becoming generic or too many mentor questions. | Use mentor status draft, V5.2 status slide, approved-data readiness docs, and cleanup plan. | Use no complex diagram except maybe a tiny three-step summary strip. | Close on: schema architecture, target leakage barrier, variable fingerprints, intake validator, whole-well validation plan, and blue runtime-confirmation callouts. |

## What To Do With The Existing Decks

| Existing item | Decision |
|---|---|
| Gmail visual deck and processing panels | Keep as the visual baseline and rebuild target. |
| Older V2 topic-aligned builder functions | Use as the structural guide for the final nine-slide order. |
| V5.2 workflow deck | Keep as method-reference package, not final presentation. |
| V5.2 expanded poster slide | Keep as a whole-slide architecture plate in the final deck if readable; otherwise redraw the same complete content at presentation scale. |
| V5.2 ML runtime detail | Keep as a whole-slide ML runtime plate in the final deck. |
| Diagram-first deck | Archive after final deck is accepted. It solved architecture, but not final presentation structure. |
| Stability-only remake | Archive/delete candidate after approval. It is too narrow for the final project story. |

## Build Sequence

1. Keep the original nine slide topics fixed.
2. For each slide, write a one-sentence takeaway before editing visuals.
3. Pull V5.2 decisions into the matching original topic, not into new slide
   names.
4. Keep the complex V5.2 diagrams intact as whole-slide plates. Redraw them
   only if needed for readability, while preserving their complete structure:
   source/header/QC lane, `X_allowed` versus target-only rail, model ladder and
   output heads, and validation/review lane.
5. Rebuild with `docs/project_blueprints/build_processing_slide_assets.py` and
   `docs/project_blueprints/build_ml_revamp_powerpoint.py`, not with the
   diagram-first builder.
6. Generate and inspect the contact sheet before any Drive upload.
7. Keep the V5.2 full diagram deck available in Drive as a backup method
   reference until the final Gmail-style deck is accepted.
8. Only then archive/delete superseded local and Drive versions.

## Final Slide Takeaways To Draft First

| Slide | Draft takeaway |
|---|---|
| 1 | This project builds a defensible North Slope workflow for future hydrate occurrence classification and saturation regression. |
| 2 | Methane hydrate is only interpretable when hydrate physics, North Slope context, and reservoir evidence are separated. |
| 3 | Every approved-data column gets a variable fingerprint before it can become an input, target, QC field, or context feature. |
| 4 | The ML architecture separates measured inputs from target-only saturation/occurrence labels before training. |
| 5 | Hydrate-supporting log responses have mimics, so the model must combine physics-backed features instead of one threshold. |
| 6 | Equation features are allowed only after units, source, QC, and leakage checks are clear. |
| 7 | Public maps and stability context guide review, but approved well evidence must drive labels and validation. |
| 8 | Future outputs will be reviewed occurrence and saturation results with calibration, residual, uncertainty, and locked-well checks. |
| 9 | The current contribution is schema, leakage-barrier, and ML-method readiness, not final model performance. |
