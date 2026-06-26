# Project Revision Delegation Base

Date: 2026-06-18

Use this file to coordinate the personal PC, OpenScienceLab, Drive, Gmail, and
delegated Codex chats for the next project revision pass. This is broader than
a deck-only pass: it controls the current slide revisions, website/map staging,
four-well ML scope, source recovery, core/lithology evidence, and Word
companion updates.

Source update:

- Gmail self-email subject: `slide updates for the newest deck`
- Sent: 2026-06-18 18:12 CDT
- Attachment noted in Gmail, not committed:
  `V5.5 Slide 3 Signal Response QC-Cleaned North Slope Gas Hydrate ML Workflow Slides 2026-06-17 (1).pptx`
- The attached deck is treated as the best user-reviewed deck so far, but it is
  not a committed local artifact until a future session explicitly downloads,
  verifies, and stages it.
- No private email attachments, inline images, or approved-data rows should be
  committed from this email.

## Current Project Direction

The problem is not that the slides contain screenshots as source evidence. The
problem is that some entire slides are currently raster screenshots of an
actual build, so the user cannot select, edit, or manually adjust specific
text, labels, arrows, and layout elements. The next pass should make each slide
the real build wherever practical: editable text boxes, editable shapes,
editable arrows, and reproducible generated figures. Maps, plots, and source
figures may still be raster exports, but they should be high-resolution,
source-backed, and placed into slides with editable labels/captions when
possible.

The current approved-runtime/data scope is also narrower and deeper than older
docs implied. The three datasheets/workbooks represent the four wells that will
be used for the ML pipeline. Do not plan around a broad 71-dataset training
program as the active near-term scope. The project should focus on doing the
four-well workflow well: verify the well names/aliases from screenshots and
source metadata, recover well locations, find core/NMR/pressure-core/lithology
data for those wells, and use that to explain hydrate saturation and lithology
more clearly.

Cross-slide rules:

- Keep the main presentation to the nine audience slides unless the user asks
  for appendices.
- Do not use whole-slide raster screenshots as final editable slides when the
  user needs to select and adjust text manually.
- Keep source figures, maps, and plots as generated/high-resolution figure
  objects when needed, but keep labels, callouts, titles, and explanatory text
  editable in the slide deck wherever practical.
- Use high-level slide language. Put detailed citations, caveats, and source
  explanations in the Word companion or end material.
- Remove "project website" wording from slides. The website is a source and
  staging surface, not part of the audience story.
- Use source-backed images or data-derived figures. Avoid AI-looking generic
  science art unless the user explicitly asks for illustration.
- Leave weak placeholders blank instead of filling slides with a wrong or
  confusing map.
- Keep stability as pressure-temperature admissibility/context only. It is not
  hydrate proof, occurrence evidence, saturation evidence, producibility, or a
  sweet-spot ranking.
- Keep approved/private rows, row-level predictions, trained models, fitted
  scalers, and approved-data metrics out of GitHub.
- If a visual depends on DOE approved data, add skeleton code or a runtime
  export path in GitHub, then export only reviewed public-safe PNG/CSV summary
  products from the DOE desktop.
- Treat the four wells from the current three datasheets/workbooks as the
  active ML scope until verified otherwise. Do not inflate the scope or claim
  broader training coverage.
- Find and verify the real names, aliases, locations, and coring/lithology data
  for the four wells before building final ML, lithology, or saturation
  explanations.

## Slide-Level Direction From The Email

### Slide 1

- Delete the "rap caviar" content.
- Remove the current personal photo. The user will manually add a more
  professional photo later.

### Slide 2

- Rebuild heavily.
- Use one concise combined North Slope 2D map, not multiple disconnected maps.
- Add the CSV-derived temperature/stability curve as a real plot where
  possible, not a low-resolution screenshot.
- Replace "P-T gate" with "P-T diagram."
- Use the gas hydrate structure source image, but correct the Structure I
  circle and integrate explanation labels directly into the image.
- Return to source literature for Structure II and Structure H wording.
- Explain thermogenic versus biogenic gas hydrate formation with sources.
- Add sourced context for why gas hydrates matter as a major energy resource,
  including the latest government/resource estimate used by the project.
- Use cross sections to explain the map. The current north-south Arctic Alaska
  cross section is not enough by itself; look for or build an east-west
  anticline/stability-zone explanation too.

### Slide 3

- This is the main visual explanation of logging and coring signals.
- Show why `V_s` matters: shear waves are not carried by pore fluid alone, so
  measured shear response is tied to the solid frame, hydrate-bearing sediment,
  cementation/contact stiffness, and geomechanics.
- Make the well-log traces look more like real logs while staying readable.
- Integrate the right-side explanation blocks into the log lines instead of
  leaving them as separate detached cards.
- Add a lithology/rock-type column or source-backed subsurface section near
  the logs so the audience understands why clean sandstone can be a good gas
  hydrate reservoir.
- Use source-backed signal movement, not just broad ranges. Show shifts,
  separations, and directional anomalies tied to Alaska North Slope examples
  where possible.

### Slide 4

- The detailed ML diagram is useful but too complex for the audience.
- Build a simplified audience version showing which boxes combine, what arrows
  matter, and how the story can be explained in about two minutes.

### Slide 5 / Equation Slide

- Replace the old three-dataset prototype slide with an equation-only slide.
- Do not include ML or well-log traces on the equation slide.
- Use actual fraction formatting, not slash notation.
- Place a short word or phrase directly under every symbol so the audience can
  follow what is multiplied, divided, compared, or transformed.
- Make equations large enough to read from a projected slide.
- Highlight symbols that come directly from logs, core, or derived quantities.
- Remove the 2D stability map from this slide.
- Remove "why use it" text if it crowds the equation cards.

### Slide 6

- Keep the content high level and visual.
- Reduce word count and font crowding.
- Integrate images into the visual structure instead of treating them as extra
  attachments.

### Slides 7 To 9

- The new stability map belongs on Slide 7.
- Slide 7 should not be an ML overlay.
- Slides 7 to 9 should become a results/discussion plan, not unsupported
  results.
- Maintain no-proof and no-trained-metric guardrails until approved execution
  and mentor review are complete.

## Delegation Prompts

Copy only one prompt at a time into a delegated Codex chat. Each chat should
report back with files changed, figures produced, tests run, and unresolved
questions. Prompts are intentionally specific so a delegated chat can work
without rereading this whole conversation.

### Prompt 0: PC / OSL Git Sync And Base Check

```text
We are working in Rnanda442/north-slope-gas-hydrates.

Goal: align this machine with the latest project-revision base before doing
any slide, website, source, or ML work.

First run:
git status -sb
git remote -v
git fetch --all --prune
git branch -vv

Then read docs/AGENT_START_HERE.md,
docs/CURRENT_ARTIFACT_INDEX.md,
docs/PROJECT_PROMPT_LIBRARY.md, and
docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md.

Task: report whether this machine is aligned with GitHub and whether it has
uncommitted local work, untracked source packages, OSL-only data, or generated
presentation assets that need to be committed, ignored, or moved to Drive/OSL.

Also check whether the machine has the latest Gmail/Drive deck attachment,
new OSL geopackages, generated map exports, DOE/Anaconda outputs, or source
PDFs that are not reflected in GitHub. Classify each item by where it belongs:
GitHub, Google Drive, OSL/source library, ignored runtime folder, or user
decision.

Do not run git reset, git checkout --, delete files, or overwrite local work.
Do not commit raw approved data, private rows, runtime predictions, trained
models, fitted scalers, credentialed PDFs, or heavy raw source bundles. If a
file is necessary but not GitHub-safe, list where it should live in Drive or
OSL and why.

Output:
1. Current branch and ahead/behind status.
2. Local changes grouped as GitHub-safe, Drive/OSL-only, generated but ignored,
   or needs user decision.
3. Which docs or prompts are outdated compared with this project revision base.
4. Exact pull/commit/push recommendation.
5. A no-action warning for anything that looks risky to delete or overwrite.
```

### Prompt 1: Latest Gmail Deck Intake And Editable-Slide Audit

```text
We are working in Rnanda442/north-slope-gas-hydrates.

First read docs/AGENT_START_HERE.md,
docs/CURRENT_ARTIFACT_INDEX.md, and
docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md.

Task: inspect the latest self-email named "slide updates for the newest deck"
and its attached PPTX. Download the attachment only if the user has explicitly
authorized using Gmail/Drive in this chat. Save it as a reference artifact only
after verifying it is a valid PPTX and contains the expected nine-slide deck.

Important interpretation: the user is not saying "do not use screenshots at
all." The user is saying the whole slide should not be a flat screenshot of a
build when the final deck needs selectable/editable text. Audit each slide for:
editable text boxes, editable labels, editable arrows/shapes, raster-only
panels, embedded images, chart/map resolution, and whether the slide can be
manually adjusted in PowerPoint or Google Slides.

Compare the attachment against the current committed V5.5 Slide 2 source update
package. Do not overwrite the committed deck. Produce a concise delta report:
which slides are better in the email deck, which images/maps should be
recovered, which slides need rebuilding, and which slide text should move to
the Word companion.

For each slide, output:
- current role in the nine-slide deck;
- what is editable now;
- what is flat/raster-only and should be rebuilt;
- visual assets to preserve;
- text that should stay on slide;
- text/citation detail that should move to Word/end material;
- whether a source/data-derived figure is needed before rebuilding.

Guardrails: no private row data, no unsupported results, no raw attachment
commit unless the user confirms it should enter Git. If it is only for review,
record it in docs/CURRENT_ARTIFACT_INDEX.md as a needs-review Gmail/Drive
artifact and keep binary handling explicit.
```

### Prompt 2: Native Editable Deck Rebuild Plan

```text
We are working in Rnanda442/north-slope-gas-hydrates.

First read docs/AGENT_START_HERE.md,
docs/CURRENT_ARTIFACT_INDEX.md,
docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md, and the current deck
builder under docs/project_blueprints/.

Task: create a technical plan for converting the current best deck from
whole-slide screenshot/raster panels into a real editable slide build.

The plan should specify:
- which slide elements must be native editable text boxes;
- which arrows, labels, cards, circles, and callouts must be native editable
  shapes;
- which parts can remain generated high-resolution PNG/SVG figures, such as
  maps, source figures, P-T plots, well-log exports, or equation-rendered
  cards;
- how to keep a visual style consistent while allowing manual text edits;
- whether to use PowerPoint python-pptx, Google Slides connector edits,
  SVG/PNG figure exports, or another reproducible builder path;
- how to test the output so the user can click and edit slide text.

Do not rebuild the deck yet unless explicitly asked. This prompt is for the
plan and implementation strategy only.

Guardrails: no approved rows, no raw private attachments, no fake metrics, no
unsupported hydrate results, and no accidental overwrite of the current best
deck.
```

### Prompt 3: Slide 2 Hydrate And North Slope Context Rebuild

```text
We are working in Rnanda442/north-slope-gas-hydrates.

First read docs/AGENT_START_HERE.md,
docs/CURRENT_ARTIFACT_INDEX.md,
docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md,
docs/STABILITY_CALCULATION_PLAN.md, and
docs/source_library_index/README.md if present.

Task: plan and, if requested, rebuild Slide 2 as a concise source-backed
introduction to methane hydrate and why the Alaska North Slope matters.

Required content:
- One combined 2D North Slope map visual that explains the project setting.
- A CSV-derived temperature/stability curve or P-T diagram.
- A corrected gas hydrate structure visual with Structure I circled cleanly.
- Short source-backed explanation of Structure I, Structure II, and Structure H.
- Short source-backed explanation of thermogenic versus biogenic gas hydrate
  formation.
- A government/source-backed statement on gas hydrate energy importance and
  North Slope resource potential.
- Cross-section context: keep the useful north-south Arctic Alaska cross
  section, but add or plan an east-west anticline/stability-zone explanation
  if a source-backed option is available.

Design logic:
- Slide 2 should explain "what gas hydrates are," "why North Slope matters,"
  and "why P-T stability varies regionally" without crowding the slide with
  tiny source comments.
- Use editable slide labels/callouts on top of source figures, not a whole-slide
  screenshot.
- The P-T diagram should explain the map; cross sections should explain why
  the stability zones vary.
- If the better combined map is not available yet, leave that area blank with
  a build note rather than using the wrong map.

Slide rules:
- Use large visuals and minimal words.
- Do not use "project website" wording.
- Use "P-T diagram," not "P-T gate."
- Integrate explanatory labels into figures instead of adding separate tiny
  text boxes.
- If the combined map is not ready, leave the map region blank with a clear
  build note rather than using a wrong old map.
- Put detailed citations and caveats in the Word companion/end notes.

Guardrails: stability is context only, not hydrate proof. Do not claim final
stability intervals, occurrence, saturation, producibility, or ranking.
```

### Prompt 4: Unified Website And 2D Well Map Integration

```text
We are working in Rnanda442/north-slope-gas-hydrates.

First read docs/AGENT_START_HERE.md,
docs/CURRENT_ARTIFACT_INDEX.md,
docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md,
docs/opensciencelab_runtime_layout.md, and the relevant map code in
dashboard/app.py.

Task: inspect the website maps directly, not local screenshot paths, and build
a plan or implementation for one unified 2D North Slope map section that can
feed Slide 2 and Slide 7.

Map elements to integrate:
- The Geoscience Orientation map: public geology/assessment-unit context,
  seismic coverage, public wells, study-boundary rectangle, and field labels.
- The DGGS RI 2018-6 Umiat-Gubik geology layer: map units, contacts/faults,
  folds, stations, and Umiat/Gubik structural labels.
- The permafrost/hydrate assessment unit context map: GGD223 permafrost-depth
  controls and USGS gas hydrate assessment-unit outlines.
- The 2D Screen Status Map: stability-screen well status points over the
  basemap, with status colors.
- The new OSL desktop GIS context layers: Alaska DNR oil/gas unit outlines,
  AKDOT roads with Dalton/Deadhorse emphasized, Trans-Alaska Pipeline,
  communities, and field labels such as Prudhoe Bay, Kuparuk River, Milne
  Point, Colville River, Pikka, Northstar, and Endicott.

Output requirements:
- One large, readable website map or static export, not four disconnected maps.
- Clear layer legend and source/caveat caption.
- Map extent focused on the North Slope project area; the stability map should
  be large enough to read.
- Distinguish context layers from hydrate evidence.
- Provide a slide-export version with room for editable labels/callouts in the
  deck.
- Provide a website version with layers/legend/caption, but do not use the
  phrase "project website" on the slide itself.
- Add tests for loader/legend behavior if code changes.

Guardrails: do not use private/approved rows. Do not imply that context layers
or stability status points are hydrate occurrence/saturation evidence.
```

### Prompt 5: Four-Well Data, Core, Lithology, And Location Recovery

```text
We are working in Rnanda442/north-slope-gas-hydrates.

First read docs/AGENT_START_HERE.md,
docs/CURRENT_ARTIFACT_INDEX.md,
docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md,
docs/source_library_index/README.md if present,
docs/ML_PIPELINE_BASELINE_SOURCE_LEDGER.md, and the latest Gmail deck update
summary in docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md.

Task: verify the four wells represented by the current three approved
datasheets/workbooks. The user thinks some names may be MLK and ETG, and older
notes mention MTE and IGS, but do not assume any well names. Find the real
well names, aliases, locations, and coring/lithology data from screenshots,
workbook headers, source papers, Drive/OSL source files, or header-only
approved-runtime summaries.

Required research targets:
- verified well name and aliases;
- field/trend/location context;
- which of the three datasheets/workbooks each well appears in;
- available log families for each well;
- available core, NMR, pressure-core, lithology, grain-size, porosity, or
  hydrate saturation evidence;
- whether the source supports clean sandstone, shale, mixed facies, hydrate
  saturation, or calibration discussion;
- what can go into GitHub, what must stay in Drive/OSL, and what can be shown
  in the website.

Output a table with columns:
verified well name | suspected alias | source evidence | location/field/trend |
available log families | core/NMR/lithology evidence | public-safe use |
Drive/OSL-only material | remaining question.

Guardrails:
- Do not copy approved rows, private identifiers, or row-level measurements
  into GitHub.
- Use header-only or source-summary workflows where possible.
- If a source is missing, write a retrieval note instead of guessing.
- Treat the four wells as the active ML scope until the user/mentor verifies
  otherwise.
```

### Prompt 6: Slide 3 Log Signal And Lithology Visual Rebuild

```text
We are working in Rnanda442/north-slope-gas-hydrates.

First read docs/AGENT_START_HERE.md,
docs/CURRENT_ARTIFACT_INDEX.md,
docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md,
docs/SCIENCE_TO_ML_LOGIC_LADDER.md,
docs/ML_PIPELINE_BASELINE_SOURCE_LEDGER.md, and
data/public_ml_products/public_parameter_evidence_registry_2026-06-16.csv.

Task: plan Slide 3 as a visual explanation of logging and coring parameters
and the signal movements that suggest hydrate-compatible intervals in Alaska
North Slope examples.

Important scope rule: Slide 3 should align with the four-well ML scope. Do not
make it look like a broad generic dataset. Use the four-well/core/lithology
recovery prompt if the well names or coring data are not verified yet.

Use sources such as Aung 2026, Yoneda 2026, Collett/Boswell/Waite 2019,
Lijith 2019, Dalvand/Falahat 2021, Rajabi 2023 if available, and Chong/Singh
ML papers only for feature logic. Verify exact source availability before
claiming details.

Required visual idea:
- A central simplified but realistic well-log panel with multiple curves.
- Integrated callouts attached to curve movements, not detached right-side
  blocks.
- A lithology/rock-type column beside the logs showing clean sandstone versus
  shale/mixed intervals, with a source-backed reason that clean sands can host
  pore-filling hydrate.
- A small core/coring evidence strip or icon layer that shows where core/NMR
  or pressure-core data would confirm/log-calibrate the signal.
- A note or visual plan for where verified four-well coring/lithology data will
  enter the graphic once recovered.

Signal movements to analyze and show:
- Gamma ray: cleaner sand generally lower than shale-rich intervals; use as a
  reservoir-quality/lithology cue, not hydrate proof.
- Resistivity: hydrate can increase apparent resistivity by replacing
  conductive pore water, but hydrocarbons, tight rock, invasion, salinity, and
  borehole conditions can mimic this.
- Sonic/velocity: hydrate-bearing sediments can show increased stiffness and
  velocity; `V_s` is especially important because shear response is tied to the
  solid frame and hydrate-bearing contact/cementation behavior rather than
  fluid alone.
- Density/neutron/porosity/NMR: use separations or mismatches as context for
  pore-fluid/pore-solid interpretation, but do not treat one curve as proof.
- Core/coring: use as calibration/target authority, not an input feature unless
  the pipeline explicitly allows that role.

Slide rules:
- No equations on this slide.
- No ML architecture on this slide.
- Do not make the whole slide a flat screenshot; keep text/callouts editable.
- Do not use only broad numeric ranges; show directional shifts and curve
  separations.
- Keep the slide readable with few words and source-backed visuals.
- If real DOE rows are needed for final curve shapes, write skeleton export
  code and leave the final curves as a DOE-runtime output placeholder.

Guardrails: no approved/private rows in GitHub, no hydrate-proof claim from log
signals alone, and no final saturation/occurrence claim.
```

### Prompt 7: Slide 4 Simplified ML Architecture And Script

```text
We are working in Rnanda442/north-slope-gas-hydrates.

First read docs/AGENT_START_HERE.md,
docs/CURRENT_ARTIFACT_INDEX.md,
docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md,
docs/APPROVED_DATA_SCHEMA_COVERAGE_AND_MODEL_ARCHITECTURE_PLAN.md,
docs/FIRST_MODEL_EXPERIMENT_PLAN_2026-06-15.md, and
docs/DOE_THREE_DATASET_ML_PIPELINE_RUNBOOK_2026-06-16.md.

Task: convert the complex ML architecture into a simpler audience-facing Slide
4 plan and a two-minute speaking script.

Important scope rule: the active ML pipeline is for the four wells represented
by the three datasheets/workbooks. Describe depth-aligned four-well analysis,
not a broad abstract data lake. The model architecture can still be general,
but the slide should make clear that this project is going deeper on lithology,
core calibration, and hydrate saturation for those wells.

The simplified slide should show:
- Inputs: logs, core/NMR, stability/context, lithology/QC.
- Preparation: preserve original headers and units, align by depth, QC, build
  variable fingerprints.
- Leakage barrier: measured/derived inputs stay separate from occurrence and
  saturation targets.
- Model path: occurrence classification and saturation regression are linked
  but separate.
- Validation: complete-well or geography-aware split before any metric claim.
- Outputs: reviewed maps, figures, uncertainty, and manuscript/slide exports.

Keep arrows simple. Combine redundant boxes from the complex diagram. Keep the
full complex diagram as a reference/appendix or Word figure, not the audience
slide unless the user asks.

Output:
- simplified slide layout;
- which boxes from the complex diagram are combined;
- exact arrow sequence;
- 2-minute talk track;
- what should remain in the Word companion instead of the slide.

Guardrails: no trained metrics, no occurrence probabilities, no saturation
predictions, no final ranking, and no approved rows.
```

### Prompt 8: Equation Slide Rebuild

```text
We are working in Rnanda442/north-slope-gas-hydrates.

First read docs/AGENT_START_HERE.md,
docs/CURRENT_ARTIFACT_INDEX.md,
docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md,
docs/STABILITY_CALCULATION_PLAN.md, and any equation screenshot/source notes
under docs/evidence/.

Task: rebuild the equation slide that replaces the three-dataset prototype.
This slide is equations only. No ML diagram. No well-log trace panel. No 2D
map.

Required layout:
- Large equation cards using real fraction formatting and correct symbols.
- Under every symbol, place a short word or phrase naming it, such as
  pressure, density, gravity, depth, velocity, resistivity, porosity, hydrate
  saturation, or acoustic impedance.
- Use color or underline style to show whether a symbol comes from logs, core,
  stability/context, or derived calculation.
- Keep each card focused on what the equation converts or compares.
- Prefer source equations and public-safe data-derived mini visuals. If a final
  visual needs DOE data, add skeleton code that will export a PNG from DOE and
  leave a placeholder until that PNG is returned.
- Keep slide text/callouts editable. The equation itself may be rendered as a
  high-quality equation object/image if needed, but labels below symbols should
  be editable or easy to update.

Possible equation families to verify from sources before using:
- Hydrostatic pressure / pressure-depth relation for the stability screen.
- Acoustic impedance or elastic attributes from density and velocity.
- Velocity ratio or shear-related quantities if source-backed for the log/core
  physics explanation.
- Saturation/electrical relation only if the exact source equation, units, and
  target/input role are verified.

Slide rules:
- Remove slash notation like `a/b`; use stacked fractions.
- Increase font size enough for presentation.
- Remove crowded "why use it" prose.
- Do not mention ML on this slide.
- Do not include a map on this slide.
- Do not imply the project is already using final equations on approved data
  unless that has been verified.

Guardrails: no fake formulas, no unsupported variables, no approved rows, no
final stability or saturation claim.
```

### Prompt 9: Slide 6 High-Level Visual Cleanup

```text
We are working in Rnanda442/north-slope-gas-hydrates.

First read docs/AGENT_START_HERE.md,
docs/CURRENT_ARTIFACT_INDEX.md, and
docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md.

Task: plan Slide 6 as a high-level, low-text visual. Identify which current
text can move to speaker notes or the Word companion, which image boxes should
be integrated into the main visual, and which one-sentence takeaway belongs on
the slide.

Rules:
- No tiny text.
- No disconnected source comments on the slide face.
- Use only visuals that are source-backed or generated from project data/code.
- Keep the audience takeaway clear enough to explain in less than one minute.
- Keep text editable; do not make the whole slide a raster screenshot.
- Use the four-well/lithology/core direction if the slide discusses data scope.

Output:
- before/after outline;
- which text moves to Word/speaker notes;
- which visuals stay;
- which visuals need to be rebuilt from sources or project data;
- one sentence takeaway.

Do not rebuild the deck unless the user explicitly asks.
```

### Prompt 10: Slides 7 To 9 Results And Discussion Plan

```text
We are working in Rnanda442/north-slope-gas-hydrates.

First read docs/AGENT_START_HERE.md,
docs/CURRENT_ARTIFACT_INDEX.md,
docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md,
docs/STABILITY_CALCULATION_PLAN.md, and
docs/DOE_RUNTIME_PRESENTATION_AND_MODEL_TRACKING_PLAN_2026-06-16.md.

Task: plan Slides 7 to 9 as a results/discussion sequence without claiming
unsupported results.

Slide 7 should use the new stability map as context only. It should not be an
ML overlay.

Slide 8 should explain the planned four-well result-review logic: what
figures/tables will be produced after DOE approved-runtime execution, how
lithology/core calibration, uncertainty, and false positives are reviewed, and
how occurrence/saturation outputs stay separate.

Slide 9 should close with what is already built, what is not claimed yet, and
the next approved-runtime/mentor actions.

Output:
- Slide 7 layout with stability map and context-only caption.
- Slide 8 layout for planned results/review, not fake results.
- Slide 9 layout for done/not claimed/next.
- Which charts/maps/tables need DOE export later.
- Which points belong in the talk track instead of slide text.

Guardrails: no hydrate proof, no final stability, no trained metrics, no
occurrence or saturation predictions, and no sweet-spot ranking.
```

### Prompt 11: Word Companion Science Support

```text
We are working in Rnanda442/north-slope-gas-hydrates.

First read docs/AGENT_START_HERE.md,
docs/CURRENT_ARTIFACT_INDEX.md,
docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md,
docs/SCIENCE_TO_ML_LOGIC_LADDER.md, and
docs/ML_PIPELINE_BASELINE_SOURCE_LEDGER.md.

Task: expand the Word companion source notes that will support the revised
slides.

Topics to source and explain clearly:
- What Structure I, Structure II, and Structure H mean, and why methane/Structure
  I is the baseline for this project unless gas-composition sensitivity is
  explicitly invoked.
- Thermogenic versus biogenic gas sources and how that matters for North Slope
  hydrate discussion.
- Why gas hydrates matter as an energy resource, including the latest
  government/resource estimate used by this project.
- Why clean sandstone/reservoir quality matters for pore-filling hydrate.
- What lithology/core evidence exists for the four wells being used in the ML
  pipeline, or what is still missing.
- Why `V_s`, resistivity, density/porosity/NMR, gamma ray, and core data are
  complementary rather than one-curve proof.
- Why equations are used as physics/feature transformations or screening
  calculations, not as unsupported final proof.
- Why the current ML scope is four wells from three datasheets/workbooks and
  how that changes the presentation: deeper lithology/core explanation rather
  than broad model-performance claims.

Keep detailed citations in the Word companion or end material. Slides should
receive only short, high-level wording pulled from this source-backed text.

Guardrails: do not overclaim occurrence, saturation, producibility, or final
resource estimates beyond what the cited source supports.
```
