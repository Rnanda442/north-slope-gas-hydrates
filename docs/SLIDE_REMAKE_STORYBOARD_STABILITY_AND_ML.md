# Slide Remake Storyboard: Stability And ML

Created: 2026-06-15

## Purpose

This is the creative execution plan for remaking the current nine-slide Gmail
deck. It keeps the latest Gmail deck as the slide authority, locks slides 1 and
2 exactly as they are, and replaces slides 3-9 with a clearer visual story:

```text
-> where the public/OSL workflow lives
-> how pressure-temperature admissibility is screened
-> how data readiness controls confidence
-> how approved logs/core later feed occurrence and saturation ML
```

The deck must stay public-safe. It must not show approved well-log rows, core
rows, restricted identifiers, populated runtime paths, trained models, hydrate
proof, saturation outputs, sweet-spot rankings, or final validated ML metrics.

## Current Slide Authority

Use this deck as the starting point:

```text
docs/project_blueprints/CURRENT_GMAIL_VISUAL_REVISION_9_SLIDE_North_Slope_Gas_Hydrate_Slides_2026-06-11.pptx
```

Inspection result:

- 9 slides.
- Each slide is one full-slide `1600 x 900` raster panel.
- The remake should therefore generate new slide panels and rebuild or replace
  the raster panels, rather than manually editing PowerPoint text boxes.

## Generated Local Draft

First local draft generated: 2026-06-15

```text
docs/project_blueprints/STABILITY_ML_REMAKE_9_SLIDE_North_Slope_Gas_Hydrate_Slides_2026-06-15.pptx
```

Builder and panel assets:

```text
docs/project_blueprints/build_stability_ml_slide_remake.py
docs/project_blueprints/presentation_assets/stability_ml_remake_2026_06_15/
```

Verification:

- regenerated from the builder after the latest stability-screen pull;
- verified as exactly 9 slides;
- each slide contains one full-slide `13.33 x 7.5 in` raster panel;
- slides 1 and 2 are copied from the current Gmail authority deck and verified
  by matching embedded-image hashes;
- full-size spot checks covered the public/OSL bridge, public-products status,
  readiness board, and conclusion decision slide;
- contact-sheet review covered all nine active panels.

Review status:

- Local draft is ready for user/mentor review with slides 1-2 locked.
- Drive upload or replacement is intentionally still blocked pending approval.
- The deck remains public-safe and does not claim hydrate proof, saturation,
  sweet-spot ranking, or validated ML performance.

User review update on 2026-06-15:

- The first local draft should not be used as the next presentation direction.
  The user asked for one full project ML flowchart instead of separate
  stability/workbench/status slides.
- The replacement direction is recorded in
  `docs/FULL_PROJECT_ML_WORKFLOW_DIAGRAM.md`.
- The new diagram-first generated deck is:

```text
docs/project_blueprints/FULL_WORKFLOW_ML_DIAGRAM_9_SLIDE_North_Slope_Gas_Hydrate_Slides_2026-06-15.pptx
```

- Slides 1 and 2 remain preserved from the current Gmail authority deck, while
  slide 3 becomes the full connected workflow map and slides 4-9 become
  zoom-ins on the same map.

## Visual Direction

Use a clean technical-control-room style:

- slides 1 and 2 keep the current Gmail deck visuals unchanged;
- mostly white or very light backgrounds for generated slides 3, 5, 6, 8, and
  9;
- one dark systems slide for the ML architecture;
- one map/workbench split slide with a strong public/OSL boundary;
- repeated left-to-right flow language;
- one persistent color grammar:
  - teal: public workflow and source-backed context;
  - ice blue: pressure-temperature/stability;
  - green: reservoir-quality or passing gate;
  - amber: uncertainty, extrapolation, pending decision;
  - red: blocked, leakage barrier, not-public data boundary;
  - charcoal/navy: final labels and non-negotiable guardrails.

Design rule:

Every slide should answer one question in the title and one sentence in the
subtitle. Details belong in the diagram, not in paragraphs.

## Slide 1: Title / About Me / Project Promise

Status: locked from the current Gmail deck.

Working title:

```text
Gas Hydrate Occurrence and Saturation Prediction
```

Main message:

The current Gmail slide is the authority for title/about-me framing.

Visual concept:

- Do not redesign in this pass.
- Preserve the current full-slide raster panel exactly.

Do not show:

- any edited replacement for this slide until the user explicitly unlocks it.

## Slide 2: What Methane Hydrate Is

Status: locked from the current Gmail deck.

Working title:

```text
Methane Hydrate Is A Stability-Gated Material
```

Main message:

The current Gmail slide is the authority for the methane-hydrate introduction.

Visual concept:

- Do not redesign in this pass.
- Preserve the current full-slide raster panel exactly.

Speaker takeaway:

The first calculation is not a discovery claim; it only asks whether hydrate
could be stable under the selected assumptions.

## Slide 3: From Parameters To Evidence Tiers

Working title:

```text
The Model Sees Evidence Tiers, Not A Flat Parameter List
```

Main message:

The workflow checks stability context first, reservoir quality second, and
hydrate response third.

Visual concept:

Replace the nine parameter cards with a vertical decision ladder:

```text
1. Stability context
   depth | pressure | temperature | phase curve

2. Reservoir quality
   GR | porosity | RHOB | caliper QC | clean sand context

3. Hydrate response
   Rt | Vp | Vs | Vp/Vs | AI | mu-rho | NMR/core support
```

Put target fields outside the ladder in a red rail:

```text
S_h / Sgh / NMR_SAT / phase labels = labels or calibration only
```

Do not show:

- normalized 0-1 bars as if they were final thresholds;
- target columns inside model inputs.

## Slide 4: Public-To-OSL Workflow And ML Architecture

Working title:

```text
Two Workspaces, One Guarded Pipeline
```

Main message:

OpenScienceLab is the heavy-data workbench; GitHub/Streamlit is the public
delivery surface.

Visual concept:

Use a split-screen architecture:

```text
GitHub / Streamlit public side
public GIS | source docs | diagrams | public stability products

        reviewed summaries only
        no approved rows cross this boundary

OpenScienceLab workbench side
raw source bundles | approved logs/core later | runtime outputs
```

Then show the future ML branch:

```text
schema + units
-> QC + depth alignment
-> features + stability context
-> target registry / leakage barrier
-> occurrence classifier
-> saturation regressor
-> uncertainty + reason flags
```

Do not show:

- a single mixed "phase/S_h/probability" output box;
- any approved field values.

## Slide 5: Why A Single Log Cannot Prove Hydrate

Working title:

```text
Hydrate Signals Have Mimics
```

Main message:

The model should learn multi-log agreement after stability, reservoir quality,
QC, and false-positive checks.

Visual concept:

Instead of six small cards, show one synthetic depth interval with stacked
tracks and transparent overlays:

```text
clean sand
hydrate-supportive response
free gas mimic
ice/cement mimic
shale/clay issue
bad-hole QC
```

Use arrows to show why:

- `Rt` high can mean hydrate, gas, ice, tight/cemented rock, or salinity issues.
- `Vp`/`Vs` stiffness can support hydrate but can also reflect ice, cement,
  compaction, or lithology.
- `GR` helps reservoir context but is not a hydrate label.

Do not show:

- one parameter as a decision rule;
- sweet-spot ranking.

## Slide 6: Physics Features And Stability Screen

Working title:

```text
Physics Features Keep The ML Honest
```

Main message:

Feature equations turn raw logs into interpretable evidence, while the
stability screen stays a separate admissibility gate.

Visual concept:

Three connected bands:

```text
raw logs
RHOB | Vp | Vs | Rt | GR | CAL

derived features
AI | Vp/Vs | G | K | mu-rho | lambda-rho

stability screen
hydrostatic pressure + temperature model + methane 5 ppt phase curve
```

Put one compact equation cluster, not the whole equation list:

```text
AI = rho_b * Vp
G = rho * Vs^2
P_abs = 0.101325 + 0.00980665 * z_m
stable when T_model <= T_eq(P_abs)
```

Do not show:

- equations as proof;
- all formulas competing for attention.

## Slide 7: Public Stability Products Are Delivery, Not Proof

Working title:

```text
The Public Site Shows Readiness And Context
```

Main message:

The public website can show where the workflow stands, but logs/core in the
approved runtime still decide occurrence and saturation.

Visual concept:

Use a public-to-OSL bridge plus status counts:

```text
8,084 public stability scaffold wells
184 G10015 temperature profiles
24 well codes
16,168 temperature key-depth rows
22 calculated baseline admissibility intervals
8,054 blocked screen rows
```

Place a red label across the bottom:

```text
All rows remain not hydrate proof
```

Do not show:

- public candidates as hydrate-bearing wells;
- map dots as results.

## Slide 8: Results Slots And Validation Plan

Working title:

```text
What Is Complete, Calculated, And Still Blocked
```

Main message:

The project can now report workflow readiness and stability-screen status; ML
results wait for approved target validation.

Visual concept:

Use a three-column readiness board:

```text
Complete
public/OSL boundary
phase curve baseline
hydrostatic pressure
temperature model
guarded writer

Calculated
temperature key depths
baseline admissibility intervals
source-control labels

Blocked / future
approved log/core validation
occurrence labels
saturation targets
trained ML metrics
sweet-spot ranking
```

Below it, show the future result slots:

```text
occurrence probability | saturation estimate | uncertainty | review flags
```

Do not show:

- fake confusion matrices;
- fake saturation tracks;
- final model performance.

## Slide 9: Conclusion And Mentor Decisions

Working title:

```text
A Defensible Workflow Before A Prediction Claim
```

Main message:

The project is strongest when stability, occurrence, saturation, uncertainty,
and producibility stay separate.

Visual concept:

Use one central pipeline with six decision flags around it:

```text
baseline curve?
mixed-gas sensitivity?
confidence thresholds?
OM-222 digitization?
approved validation fields?
two linked ML outputs?
```

End sentence:

```text
The next deliverable should show a guarded workflow that is ready for approved
validation, not a premature hydrate claim.
```

Do not show:

- "sweet spots" as final;
- hydrate proof language;
- final saturation language.

## Execution Plan

1. Update the Word document language first with the same slide spine.
2. Preserve slides 1 and 2 from the current Gmail authority deck. Done for the
   local first draft and verified by image hashes.
3. Generate new `1600 x 900` raster panels for slides 3-9. Done for the local
   first draft.
4. Rebuild or replace the Gmail deck panels while keeping exactly nine slides.
   Done as a separate local draft, not as a Drive replacement.
5. Inspect every generated slide image locally before using the PPTX. Done for
   the first draft.
6. Verify the PPTX has exactly nine slides. Done for the first draft.
7. Upload/replace Drive only after local approval.

## Acceptance Criteria

- Every slide has one clear question/message.
- Slide 4 visibly separates GitHub/Streamlit from OpenScienceLab.
- Slide 7 clearly says public stability products are context/readiness, not
  hydrate evidence.
- Slide 8 separates complete, calculated, blocked, and future work.
- Slide 9 ends with mentor decisions, not fake results.
- No slide claims hydrate proof, saturation results, sweet spots, or validated
  ML performance.
