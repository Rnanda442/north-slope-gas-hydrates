# Eight-Slide North Slope ML Presentation Specification

Last updated: 2026-06-09

## Purpose

Convert the recovered 12-slide scaffold into an approximately eight-slide,
visual DOE presentation. The deck should explain the machine-learning workflow
to energy and geoscience specialists who may not know the technical ML details.

Do not use screenshots of the Streamlit website as the main visuals. Reuse
generated diagrams, maps, log panels, and evaluation figures directly.

## Slide Plan

| Slide | Decision purpose | Primary visual | Source and implementation basis | Populate now | Populate after approved data |
|---|---|---|---|---|---|
| 1. Goal and final product | Explain the project in one sentence | North Slope map plus compact input-to-output chain | June 8 project answers; project vision | Public map, project title, workflow objective | Approved well count and study extent |
| 2. Data and labels | Show what enters the model and what must be predicted | Two-column measurement/label architecture | Email answers; Chong et al. (2022); Excel header map | Canonical curve families and target contract | Exact mnemonics, units, coverage, and label provenance |
| 3. Physics-constrained features | Explain how measurements become scientific evidence | Layered flow diagram from logs to reservoir, elastic, saturation, and stress features | Manuscript equations; Chong feature set | Equation families and synthetic examples | Calibrated parameters and feature distributions |
| 4. Runtime readiness and QC | Show why data quality controls the model route | Readiness matrix with ready/partial/blocked outputs | Chong washout QC; missing-curve requirements | Synthetic curve coverage, caliper washout, routing rules | Per-well approved-data readiness |
| 5. Model ladder | Show how baseline and advanced models will be compared | Model ladder from rules to trees to ANN/ensembles | June 8 answers; Chong ANN study | Candidate model families and selection criteria | Tuned models and feature-combination results |
| 6. Validation without leakage | Prove that performance testing is defensible | Train/validation/test wells diagram | Project scientific rules; paper comparison | Complete-well split example and metric plan | Held-out-well metrics, calibration, and failure analysis |
| 7. Interval result and sweet spots | Show the output a geoscientist will inspect | Multi-track well-log panel with highlighted interval and evidence card | Excel header layout; sweet-spot evidence model | Synthetic interval example | Approved classification, saturation, uncertainty, and core match |
| 8. Results, limitations, and next execution | Close with what is built and what happens when data arrive | Three-column built/activate/deliver panel | Project Q&A and architecture map | Current scaffold, code transfer plan, unresolved decisions | Final scientific findings and mentor recommendations |

## Required Slide Content

### Slide 1

Working message:

> Use physics-constrained machine learning to detect and quantify North Slope
> gas hydrate from well logs and core evidence, then explain each interval-level
> decision.

Keep occurrence, saturation, sweet-spot ranking, and producibility visually
separate.

### Slide 2

Input families:

- depth and location;
- gamma ray;
- density and density porosity;
- neutron porosity where present;
- resistivity;
- compressional and shear sonic;
- NMR as an available input and potential saturation-calibration source;
- caliper and borehole QC;
- core porosity, permeability, hydrate saturation, lithology, and quality.

Target families:

- continuous hydrate saturation from a supplied or core-calibrated known-well target;
- hydrate / gas / water / non-reservoir class;
- uncertain or expert-review state;
- separate sweet-spot priority;
- separate producibility output.

### Slide 3

Show measured, derived, interpreted, and target variables as distinct layers.
Target-derived columns must never feed model inputs.

### Slide 4

Include:

- curve coverage;
- unit and alias checks;
- monotonic and duplicate depth checks;
- caliper upper-tail washout flag;
- missing-curve routes;
- core-log depth-match quality;
- ready, partial, or blocked downstream outputs.

### Slide 5

Model ladder:

1. physics rules and linear baseline;
2. random forest or gradient boosting;
3. ANN saturation model;
4. ensembles or advanced methods only if held-out-well performance improves.

Chong et al. (2022) is the direct ANN comparison anchor. The paper reports
approximately 80-90% predictive performance for selected two- or three-log
combinations against NMR-derived saturation. This project now expects NMR
availability, so the workflow must explicitly separate NMR input curves from any
NMR-derived supervised saturation target.

### Slide 6

Do not present random depth-row accuracy as field generalization. Neighboring
depth samples are correlated. Of approximately 71 wells, the current plan uses
approximately 14 known wells for development and predicts the remaining 57.
Reserve complete wells inside the 14-well development cohort for validation and
locked testing before predicting the 57-well cohort.

Report:

- regression: R2, MAE, RMSE, calibration by saturation band;
- classification: per-class precision, recall, F1, and confusion matrix;
- scientific review: abstention rate, missing-curve performance, and named
  failure modes.

### Slide 7

The result card must include:

- depth interval;
- phase class;
- saturation estimate;
- reservoir quality;
- key supporting logs;
- core-match confidence;
- uncertainty and competing explanations;
- sweet-spot priority;
- separate producibility screen.

### Slide 8

Current:

- public-source atlas;
- synthetic well-log scaffold;
- runtime schemas and readiness logic;
- source-traced feature and decision model;
- recovered Word and PowerPoint blueprints;
- new concise research-overview Word document and eight-slide PowerPoint.

Activate after approved data:

- exact input mapping;
- core-log calibration;
- grouped-well model training;
- approved interval plots and metrics;
- final Word report and presentation.

## Source Footer

Use a short source footer on technical slides:

`Chong et al. (2022), doi:10.1007/s10596-022-10151-9; USGS North Slope studies; project manuscript and equation map.`

Do not describe the attached paper's randomized row split as the final project
validation design. The project standard is complete-well holdout evaluation.
