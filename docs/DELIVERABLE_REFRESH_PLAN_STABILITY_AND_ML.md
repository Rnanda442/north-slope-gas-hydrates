# Deliverable Refresh Plan: Stability And ML

Created: 2026-06-15

## Purpose

Plan the next Word document and nine-slide deck refresh around the new
stability-screen communication layer while preserving the public-source versus
authorized-runtime boundary.

This plan does not modify the DOCX or PPTX directly. It records what should be
added when the deliverable builders are updated.

Use `docs/SLIDE_REMAKE_STORYBOARD_STABILITY_AND_ML.md` as the detailed
slide-by-slide creative plan before rebuilding the current Gmail deck.

User review on 2026-06-15 rejected the first stability/ML slide-remake draft
as too disconnected from the whole project. The refresh direction is now
diagram-first: use `docs/FULL_PROJECT_ML_WORKFLOW_DIAGRAM.md` and the generated
full-workflow visual as the main project map, then use any additional slides
only as zoom-ins on that one map.

## Boundary Rule

The refreshed deliverables may show public-safe workflow diagrams, cited
methods, status counters, and intentionally blocked states. They must not show
approved well-log rows, core rows, restricted well identifiers, populated
runtime paths, trained models, final hydrate stability results, hydrate proof,
saturation outputs, or sweet-spot rankings.

## Current Message To Carry Forward

| Category | Communicate as | Do not imply |
|---|---|---|
| Complete | Public/runtime split, cited methane 5 ppt phase curve, hydrostatic pressure model, temperature-model logic, source-control confidence labels, guarded stability-screen writer | Final hydrate discovery or final phase model |
| Temperature model | 16,168 key-depth rows, 919 calculated, 387 extrapolated, 15,249 blocked, and 0 final stability results in the temperature-input product | Hydrate occurrence, saturation, or final stability-zone proof |
| Guarded screen | 8,084 baseline methane 5 ppt screen rows: 22 calculated admissibility intervals, 8 sufficient-input rows with no modeled stable interval, 8,054 blocked rows, and every row marked not hydrate proof | Hydrate proof, saturation, validated sweet spots, or occurrence ranking |
| Public scaffold | Current public stability scaffold reports 8,084 Arctic Slope public wells | Approved runtime well-log inventory |
| Authorized inventory | G10015 temperature inventory reports 184 temperature profiles across 24 well codes | Public repo data or publishable restricted identifiers |

## Primary Diagram: Full Project ML Workflow

Goal: show the whole project on one connected flowchart.

Current generated source:

```text
docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_15/full_project_ml_workflow_flowchart.png
```

Suggested structure:

```text
public/source inputs
+ approved runtime inputs
+ stability-admissibility screen
+ well-log/core feature engineering
+ target registry and leakage barrier
+ occurrence classification
+ saturation regression
+ validation and public-safe exports
```

Required labels:

- `OpenScienceLab / approved-runtime build path`
- `Public GitHub / Streamlit / Word / Slides`
- `100% methane + 5 ppt salinity baseline`
- `stability-admissibility only`
- `target registry and leakage barrier`
- `occurrence classifier`
- `saturation regressor`
- `reviewed public-safe summaries only`
- `not hydrate proof, not saturation, not sweet-spot ranking`

## Supporting Zoom-Ins

Use additional slides or Word subsections only to zoom into parts of the same
primary diagram:

- input and data-boundary zoom;
- pressure-temperature stability branch zoom;
- well-log feature and QC zoom;
- target registry / leakage barrier / model-training zoom;
- occurrence, saturation, validation, and export zoom;
- complete / calculated / blocked / decision status board.

## Word Document Update Plan

Add a short status subsection near the methodology or workflow section:

- OpenScienceLab as the heavy-data workbench.
- GitHub/Streamlit as the public delivery surface.
- Stability screen as a guarded admissibility calculation.
- Current reported counters, keeping the temperature-model product separate
  from the guarded baseline stability-screen product.
- Blocked states explained as intentional data-readiness controls, not
  no-hydrate findings.
- Future mentor decisions: baseline phase curve, mixed-gas sensitivity,
  confidence thresholds, OM-222 permafrost base, and approved validation
  fields.

Keep the main scientific sequence from `docs/SCIENCE_TO_ML_LOGIC_LADDER.md`:

```text
stability context
-> reservoir quality
-> hydrate response
-> leakage-safe occurrence and saturation ML
```

## Nine-Slide Deck Update Plan

Keep exactly nine slides unless the user changes the deck count.

| Slide | Refresh action |
|---|---|
| 1 | Keep title/about-me concise; do not add runtime status detail here |
| 2 | Add clearer pressure-temperature stability screen language and the methane 5 ppt baseline caveat |
| 3 | Make the one full workflow flowchart the central slide: public inputs, OSL inputs, stability branch, feature engineering, leakage barrier, occurrence classifier, saturation regressor, validation, and public-safe exports |
| 4 | Zoom into public inputs, approved runtime inputs, and the boundary rule |
| 5 | Zoom into the pressure-temperature stability branch and explain why it is context only |
| 6 | Zoom into well-log/core QC, unit normalization, and physics-derived feature blocks |
| 7 | Zoom into target registry, leakage barrier, complete-well split, and model ladder |
| 8 | Zoom into occurrence, saturation, uncertainty, validation, and export outputs |
| 9 | End with what is complete, what is calculated, what is intentionally blocked, and which mentor decisions remain |

## Acceptance Checks Before Publication

- The 8,084 public-scaffold label is described as the current public stability
  scaffold count, not the broader raw atlas well count.
- Temperature-model status counters are not presented as final hydrate results.
- The 22 calculated screen intervals are described only as baseline methane
  5 ppt stability-admissibility intervals.
- Blocked rows are explained as guarded workflow status, not no-hydrate
  determinations.
- The Word document and slide deck both say stability-admissibility only.
- Occurrence classification and saturation regression remain separate linked
  future ML outputs.
- No approved well-log/core fields are named as allowed validation fields until
  the mentor or approved environment confirms them.
