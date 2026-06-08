# Project Improvement Strategy

Last updated: 2026-06-08

## Strategic Aim

Improve the North Slope Gas Hydrates project by making the scientific workflow
more understandable, traceable, testable, and useful without weakening the
public-versus-authorized data boundary.

The primary internship deliverables are the detailed Word document and an
approximately eight-slide visual PowerPoint. Streamlit is the working surface
used to prototype reusable figures, explanations, and code behavior for those
deliverables.

The project should not become a collection of disconnected visualizations.
Every major feature should support the evidence chain:

```text
regional context
-> input readiness
-> measured evidence
-> derived features
-> staged interpretation
-> uncertainty
-> decision-ready outputs
```

## Improvement Test

Before adding a feature, ask:

1. Which project goal does it support?
2. What evidence or decision does it make clearer?
3. Is it public, synthetic, or authorized-runtime behavior?
4. What scientific rule or source supports it?
5. How will we test or visually verify it?
6. Does it reduce uncertainty, or merely make the interface busier?

Features that cannot answer these questions should remain ideas rather than
implementation priorities.

## Product Pillars

### 1. Guided Scientific Story

The website should help a new reader understand why regional geology, logs,
core data, uncertainty, and producibility are different parts of one workflow.

High-value improvements:

- a concise workflow overview linking atlas views to well-log decisions;
- plain-language explanations beside technical plots;
- visible labels for measured, derived, interpreted, and placeholder outputs;
- direct links between the roadmap, research framework, and synthetic engine.

### 2. Requirements Before Implementation

The Excel workbook, screenshots, manuscript, and PowerPoint should become an
explicit requirements map before the well-log engine is expanded.

The requirements map should record:

- source sheet or screenshot;
- variable, unit, and curve alias;
- formula and scientific source;
- chart track or table behavior;
- validation and uncertainty rule;
- target code module and website location;
- export and acceptance test.

### 3. Scientific Traceability

Users should be able to see how an output was produced and why it is allowed.

High-value improvements:

- equation-to-source citations;
- measured-to-derived variable lineage;
- staged decision gates for stability, reservoir quality, phase evidence,
  saturation, core confidence, and producibility;
- assumptions and uncertainty displayed with every interpreted output;
- versioned synthetic examples that become regression tests.

### 4. Runtime Readiness

Before showing classification results, the authorized runtime should explain
whether the input data can support them.

The planned Runtime Readiness view should show:

- selected input mode and data-boundary reminder;
- available, missing, and aliased curves;
- depth order, duplicate depth, range, and missingness checks;
- per-well readiness;
- core-to-log match quality;
- outputs that are ready, partial, or blocked;
- corrective action for each issue.

This can be demonstrated with synthetic inputs publicly while approved files
remain local to the authorized environment.

### 5. Decision-Quality Outputs

The system should avoid collapsing distinct scientific questions into one
hydrate score.

Keep separate:

- stability admissibility;
- reservoir quality;
- hydrate-supportive evidence;
- saturation proxy;
- core-calibration confidence;
- uncertainty;
- producibility screen.

Exports should preserve these distinctions and include provenance, assumptions,
units, data classification, and generation date.

### 6. Coherent Deliverables

The website, code, manuscript, and PowerPoint should communicate the same
workflow and terminology.

Important figures and tables should be generated from reusable code rather than
manually recreated in each deliverable. Changes to equations, labels, or
decision stages should trigger a review of all four surfaces.

## Prioritized Roadmap

### Now: Recover and Specify

1. Recover the Excel workbook, screenshots, PowerPoint, equation map, and public
   source files.
2. Classify each item as public, synthetic, or authorized-runtime only.
3. Create `docs/WELL_LOG_REQUIREMENTS_MAP.md`.
4. Capture a small set of representative spreadsheet cases as test scenarios.
5. Compare those requirements with the existing engine and runtime skeleton.

Completion signal: the team can identify exactly what must change and why
without relying on memory or screenshots alone.

### Next: Make Readiness and Evidence Visible

1. Add the Runtime Readiness view using synthetic data.
2. Add curve availability and output-readiness matrices.
3. Connect equations and decision gates to manuscript/source references.
4. Improve the synthetic well-log panel to match the recovered Excel track
   layout and visual conventions.
5. Add uncertainty and provenance to every downloadable output.

Completion signal: a reviewer can follow an input from validation through a
specific interpretation and understand its limitations.

### Then: Implement the Verified Scaffold

1. Add spreadsheet-derived schemas, calculations, plots, and exports.
2. Add regression tests from representative workbook cases.
3. Reconcile terminology and figures across the website, manuscript, and
   PowerPoint.
4. Perform desktop and phone-width visual QA.
5. Validate the complete workflow with approved data only inside the authorized
   environment.

Completion signal: the implementation satisfies the requirements map and
produces reproducible, uncertainty-aware outputs.

### Later: Carefully Introduce ML

ML scaffolding should be built now, but comparative model training should begin
only after the deterministic workflow, data validation, labels, and evaluation
design are stable. Advanced methods are allowed; complexity must earn its place
against transparent baselines on held-out wells.

Required guardrails:

- validation split by well;
- comparison against transparent rule-based baselines;
- class balance and label provenance reporting;
- calibration and uncertainty evaluation;
- out-of-distribution and missing-curve behavior;
- no replacement of expert review with a single unqualified prediction.

## Ideas to Defer

Do not prioritize these until the requirements and readiness layers are stable:

- additional decorative dashboard pages;
- a universal hydrate score;
- opaque automated classification;
- cloud upload of approved inputs;
- complex ML demonstrations without defensible labels and well-level validation;
- new GIS layers that do not affect a defined interpretation question.

## Recommended Next Build

The next implementation milestone should combine two pieces:

1. a completed well-log requirements map based on the recovered Excel design;
2. a synthetic Runtime Readiness page that reports which downstream outputs are
   ready, partial, or blocked.

Together, these create the bridge between the current public demonstration and
the future authorized scientific workflow.
