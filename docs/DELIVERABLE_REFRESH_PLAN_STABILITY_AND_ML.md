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

## Diagram 1: Public-To-OSL Workflow

Goal: show where each type of work belongs.

Suggested structure:

```text
Public sources + GitHub repo
-> Streamlit public scaffold and diagrams
-> communication deliverables

Approved data in OpenScienceLab
-> temperature inventory and runtime calculations
-> guarded outputs and status counters
-> public-safe summaries only after review
```

Visual notes:

- Draw GitHub/Streamlit on the left as public delivery.
- Draw OpenScienceLab on the right as the heavy-data workbench.
- Put a visible boundary between them: no approved rows, restricted
  identifiers, populated configs, trained models, or derived sensitive outputs
  cross into public deliverables.
- Allow only reviewed public-safe status summaries and method diagrams to flow
  back to the Word document and slide deck.

## Diagram 2: Pressure-Temperature Stability Pipeline

Goal: make the stability screen legible without claiming hydrate proof.

Suggested structure:

```text
depth
-> hydrostatic pressure
-> temperature profile or extrapolated temperature model
-> cited methane 5 ppt phase curve
-> stability-admissibility comparison
-> guarded writer
-> status output: calculated admissibility interval, no modeled stable interval,
   blocked, or not hydrate proof
```

Required labels:

- `100% methane + 5 ppt salinity baseline, pending mentor decision`
- `hydrostatic pressure model`
- `temperature model with source-control confidence`
- `stability-admissibility only`
- `not hydrate proof, not saturation, not sweet-spot ranking`

## Diagram 3: Data-Readiness And Confidence-Label Pipeline

Goal: show why many rows can be intentionally blocked.

Suggested structure:

```text
temperature source inventory
-> well-code/profile matching
-> key-depth target rows
-> nearest/control-distance review
-> confidence label: high, medium, low, blocked
-> block reason or calculation route
-> reviewed export status
```

Open mentor decision:

Define the control-distance thresholds for high, medium, and low confidence.
Until those thresholds are approved, confidence labels should be described as
source-control labels rather than final scientific certainty.

## Diagram 4: Guarded ML Pipeline

Goal: connect the stability-screen work to the future ML deliverable without
leaking targets or overclaiming results.

Suggested structure:

```text
approved well logs + core/NMR context
-> schema and unit mapping
-> depth alignment
-> QC gates
-> physics-derived features
-> stability-admissibility and reservoir context
-> target registry and leakage barrier
-> occurrence classification
-> saturation regression
-> uncertainty, QC, reason flags, and review outputs
```

Required guardrails:

- `S_h`, `Sgh`, `NMR_SAT`, phase labels, and final rankings are labels,
  calibration references, or outputs, not predictors.
- Occurrence classification and saturation regression should be presented as
  linked but separate outputs.
- Final validation must use complete wells or compartments, not random depth
  rows as final evidence.
- No project model metrics should appear until approved-data validation exists.

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
| 3 | Keep the three-tier parameter ladder; add a small status cue that stability is context, not a label |
| 4 | Add the guarded public-to-OSL workflow and target-leakage barrier |
| 5 | Keep parameter behavior and false positives; emphasize stability, reservoir, and response as separate evidence tiers |
| 6 | Add the P-T stability pipeline or confidence-label pipeline if space allows |
| 7 | Keep map/context as public screening context only |
| 8 | Replace any results-like placeholders with calculated/blocked/readiness status and future validation slots |
| 9 | End with next decisions: phase-curve baseline, confidence thresholds, OM-222 permafrost base, and approved validation fields |

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
