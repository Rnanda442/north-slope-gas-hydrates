# Gmail-Style V5.2 Slide Remake Prompt

Created: 2026-06-15

## Review Finding

The latest method-content authority is the V5.2 workflow package:

- `docs/project_blueprints/V5_2_FULL_WORKFLOW_ML_DIAGRAM_North_Slope_Gas_Hydrate_Slides_2026-06-15.pptx`
- `docs/project_blueprints/V5_2_North_Slope_Gas_Hydrate_Full_ML_Workflow_Companion_2026-06-15.docx`
- `docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_15/`

The best visual authority is still the older Gmail-style nine-slide deck:

- `docs/project_blueprints/CURRENT_GMAIL_VISUAL_REVISION_9_SLIDE_North_Slope_Gas_Hydrate_Slides_2026-06-11.pptx`
- Gmail-style raster panels under `docs/project_blueprints/presentation_assets/processing_revisions_2026_06_11/`

Use V5.2 for the decisions, source logic, public/runtime boundary, and ML
architecture. Do not use V5.2 as the slide-topic authority. The topic authority
is still the original/main nine-slide sequence from the Gmail/rule-book pass:
title/about-me; gas hydrate introduction; parameters and well-log scaffold; ML
methodology and architecture; why parameters/model choices matter;
geomechanics/equations; map and well context; results/discussion/review logic;
and conclusion.

Use the Gmail deck for the look: large readable title, one main visual per
slide, clean white or light background, restrained teal/blue/green/amber/red
accents, a strong bottom takeaway, and limited dense text.

The two complex V5.2 diagrams are important whole-slide architecture plates.
Keep them together where they matter instead of fragmenting them across the
deck. If readability is not good enough, redraw the same complete diagram at
presentation scale; do not crop it into unrelated pieces.

## Known Decisions To Display

Do not treat these as unanswered mentor questions in the slide architecture.
Show them as settled project method choices, while still saying that final
training waits for approved data.

- Train toward two linked but separate reviewed targets:
  occurrence classification and saturation regression.
- Occurrence is a target or validation label from approved evidence, not a
  stability-screen measurement. Evidence can include core/pressure-core
  observations, NMR/core-derived saturation, validated log interpretation, or
  documented seismic indicators.
- Saturation target headers are Y-only: `Sgh`, `S_h`, `Sh`, `NMR_SAT`,
  `Hydrate Saturation`, `Swr`, `S_wr`, and interpreted phase labels cannot
  enter `X_allowed`.
- Numeric predictors are scaled 0-1 with train-only statistics after the
  whole-well, compartment, or geographic split. Depth remains the alignment and
  context axis unless explicitly approved as a predictor.
- Units stay visible above or beside the original headers before normalization.
- Every variable gets a fingerprint: original header, source unit, normalized
  name, role, allowed-in-feature-matrix flag, leakage risk, unit status, and
  unresolved runtime note.
- Caliper is coverage-first. Gather `caliper`, `CAL1`, and differential caliper
  availability before showing washout filtering as active. Missing caliper
  creates a missing-QC flag rather than an automatic filter.
- Candidate features may include the full equation list only when source,
  unit, QC, and leakage checks pass: gamma-ray shale/clean-sand proxy, density
  porosity, resistivity transforms, `Vp`, `Vs`, `Vp/Vs`, acoustic impedance,
  elastic attributes, NMR-density separation, and Archie/resistivity hydrate
  proxy.
- Model order is baselines first, tree or gradient boosting second, and
  ANN/Keras third. Include ANN visually, but do not claim trained ANN results.
- Stability can be shown as public/context features, mask, caveat, confidence,
  or blocked reason only. It is not hydrate proof, not occurrence, and not
  saturation.
- MTE and IGS are separate North Slope case-study wells. Treat `MTE_refined`
  and `IGS_refined` as workbook or processing-stage tables until approved
  metadata confirms the exact source relationship.
- The planning cohort is approximately 71 wells, with approximately 14
  known/development wells and 57 prediction wells. The known wells must still
  be split by whole well into training, validation, and locked testing before
  any performance claim.
- Only about 3 of 71 datasets are visible now. That is enough for schema and
  architecture design, not final training, metrics, hydrate prediction
  accuracy, occurrence probabilities, or saturation predictions.

## Blue Mentor Callouts

Use blue callouts for review checkpoints, not for decisions already encoded in
the base documents. Suggested blue callout text:

- Confirm the official target field priority when multiple saturation labels
  appear in the same approved sheet.
- Confirm whether each saturation column is stored as fraction 0-1 or percent
  0-100 before scaling and target reporting.
- Confirm whether the workbook's occurrence labels come from source-style
  classes, mentor-reviewed intervals, saturation thresholds, or a combination.
- Confirm which wells belong in train, validation, and locked-test groups after
  the full approved inventory is recovered.
- Confirm when missing-log adapters are allowed, and when missing curves should
  block a feature family.

Render these callouts in blue, for example `#1f6feb`, so they read as review
questions instead of red blockers.

## Prompt To Rebuild The Slides

Use this prompt for the next slide-build pass:

```text
Remake the North Slope gas hydrate deck as an exact nine-slide, public-safe
presentation. Preserve the original/main nine-slide topic sequence. Use the
V5.2 workflow package as updated method content and use the older Gmail visual
deck as the style authority.

Keep the Gmail look: one full-slide raster panel per slide, large readable
title, concise subtitle, one dominant visual, light background, clean grid
alignment, restrained teal/blue/green/amber/red accents, and one strong bottom
takeaway. Do not make every slide a dense flowchart. Use the V5.2 expanded
architecture and runtime diagrams as intact architecture slides where they fit.
Do not let the V5.2 deck rename the final slide topics.

Do not expose approved/raw rows, restricted identifiers, populated runtime paths,
trained models, model metrics, hydrate proof, occurrence probabilities,
saturation predictions, or sweet-spot rankings. Preserve original headers from
screenshots and datasets when shown. Canonical names are metadata only.

Slide 1: Title and about-me authority.
Use the Gmail deck's strong personal/project opener unless explicitly unlocked.
Keep the title focused on gas hydrate occurrence and saturation prediction.

Slide 2: Introduction - what and why gas hydrates.
Show hydrate as a water-cage methane solid and explain why North Slope gas
hydrate occurrence and saturation matter. Pressure-temperature stability is
necessary context only, not proof. Keep the visual simple and readable.

Slide 3: Parameters and well-log scaffold.
Keep this as the parameter/scaffold topic, not a pure schema slide. Show the
sticky variable fingerprint inside the scaffold: original header, unit above
the normalized 0-1 value track, normalized name, role, X_allowed flag, leakage
risk, unit status, and unresolved runtime note. Include the visible header
families such as GR/lithology, density/porosity, resistivity, Vp, Vs, Vp/Vs,
impedance, NMR/core support, depth alignment, and caliper/QC. Show that only
about 3 of 71 datasets are visible now, enough for schema architecture but not
final training.

Slide 4: ML methodology and architecture.
Keep this as the ML methodology slide. Show GitHub/Streamlit as public-safe
delivery and OpenScienceLab/approved runtime as the heavy-data workbench. Show
original headers moving through source/unit/QC gates, caliper coverage review,
feature engineering, `X_allowed`, the target-leakage barrier, whole-well split,
train-only 0-1 scaling, baseline models, tree/boosting, and ANN/Keras. Show two
linked heads: occurrence classification from reviewed occurrence labels and
saturation regression from reviewed saturation labels. The target-only rail for
Sgh, S_h, Sh, NMR_SAT, Hydrate Saturation, Swr, S_wr, interpreted phase labels,
and occurrence labels must bypass the feature matrix and go only to training
labels/validation.

Slide 5: Why the parameters and model choices matter.
Use behavior panels or a compact table to show why the model cannot rely on one
log. For each family show what it measures, why it may support hydrate, what can
mimic it, and why baselines, trees/boosting, and ANN/Keras are staged rather
than claimed as final results.

Slide 6: Geomechanics, equations, and format cleanup.
Show the equation list as readable feature chips or a compact flow: GR
shale/clean-sand proxy, density porosity, resistivity transforms, Vp/Vs,
acoustic impedance, lambda-rho, mu-rho, Young's modulus, Poisson's ratio,
brittleness, NMR-density separation, and Archie/resistivity hydrate proxy. Only
show a feature as active after unit, source, QC, and leakage checks. Units must
stay visible above or beside source headers; numeric predictors are normalized
0-1 after split, while depth stays the unnormalized alignment axis.

Slide 7: Map and well context.
Keep this as the regional/map topic. Show public North Slope context, stability
screening as context/admissibility only, source coverage, public well/map
layers, and where approved-runtime well evidence will connect later. Do not
imply that GIS or stability confirms hydrate occurrence.

Slide 8: Results, discussion, and review logic.
Show future result slots and review logic: occurrence classification output,
saturation regression output, calibration plots, residual review, uncertainty
flags, reason flags, target-source caveats, and blind/locked-well validation.
Use empty or planned result slots only. Do not show fake metrics, fake confusion
matrices, fake saturation tracks, or final performance.

Slide 9: Conclusion and next steps.
Summarize the scientific value, ML value, energy value, and immediate next
approved-data tasks. State what is complete outside stability: schema coverage
matrix, field-role table, intake spec, target leakage barrier, variable
fingerprint, first model experiment plan, and V5.2 workflow package. Blue
callouts should ask only for runtime confirmations that still depend on the
full approved inventory: target priority, saturation fraction/percent
convention, occurrence-label provenance, well split, and missing-log adapter
policy.

Acceptance criteria:
- Exactly nine slides.
- Original/main slide topics are preserved.
- Gmail visual rhythm is obvious.
- V5.2 decisions are visible inside the original topics, with the complex
  architecture diagrams kept intact as whole-slide plates.
- Occurrence and saturation are both displayed as separate future ML outputs.
- Target-only labels visually bypass the feature matrix.
- Depth is shown as alignment/context and not normalized with other values.
- Units and variable fingerprints are visible.
- Caliper is shown as coverage-first QC, not an assumed available filter.
- ANN/Keras appears after baselines and tree/boosting.
- Blue questions are review callouts only.
- No unsupported results claims.
```

## What To Tell The Mentor

The deck is being remade so the visual language returns to the stronger Gmail
style while preserving the newer V5.2 science and ML decisions. The main
message is that the project has moved beyond the stability screen by defining a
public-safe schema, variable-fingerprint, target-leakage, feature-engineering,
and whole-well validation architecture for later approved-data occurrence and
saturation modeling. It is not yet a results deck.
