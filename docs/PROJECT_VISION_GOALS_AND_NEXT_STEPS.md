# Project Vision, Goals, and Next Steps

Last updated: 2026-06-08

## Project Vision

Build a reusable, physics-constrained machine-learning workflow that can accept
approved North Slope well-log and core data, identify gas-hydrate-bearing
intervals, estimate hydrate saturation, rank sweet spots, and explain why each
result was produced.

The project should be ready before approved data arrive: schemas, quality
checks, feature calculations, model interfaces, visual templates, and reporting
code should be transferable into a Python/Conda Linux environment with minimal
rework.

## Primary Goal

The primary scientific task is hydrate detection and saturation prediction from
depth-indexed well logs. Sweet-spot ranking is also required. Producibility is a
separate, later-stage output informed by porosity, permeability, continuity,
pressure, saturation, and geomechanics.

The intended output sequence is:

```text
input readiness
-> quality-controlled logs and core labels
-> physics-derived features
-> reservoir and phase classification
-> hydrate saturation prediction
-> uncertainty and expert-review routing
-> sweet-spot ranking
-> separate producibility screen
```

## Deliverable Priority

1. **Word document:** detailed scientific and technical explanation of the
   workflow, equations, model choices, validation, uncertainty, and results.
2. **PowerPoint:** approximately eight visually dense slides for a DOE energy
   audience that understands gas hydrates but may not know the ML methods.
3. **Reusable code skeleton:** Python modules and configuration that can be
   transferred into the approved Linux/Conda workspace.
4. **Streamlit website:** a working and prototyping surface for testing visuals,
   explanations, and app components before they are reused in the deliverables.
   Its public deployment remains synthetic and public-source only.

The website is supporting infrastructure, not the primary internship
deliverable.

## Audience and Communication Goal

The main audience is DOE internship participants, managers, geoscientists, and
people working at the front of AI integration in energy.

The presentation should:

- make the data-to-decision workflow understandable to non-ML specialists;
- use diagrams, log panels, maps, and model architecture visuals instead of
  long text;
- distinguish what is already built from what becomes active when approved
  data arrive;
- invite technical discussion about how far the workflow can be extended.

## Expected Approved Inputs

Current planning assumptions from the June 8 project answers:

- CSV and Excel well-log exports rather than seismic inputs;
- depth and location fields;
- gamma ray, density, neutron/porosity, resistivity, and sonic measurements;
- possible shear sonic and NMR, with missing-curve routing required;
- core porosity, permeability, hydrate saturation, lithology descriptions, and
  pressure-core quality;
- normalized or otherwise controlled values for external planning examples.

The recovered workbook must confirm exact headers, units, aliases, formulas,
and label availability.

## ML Direction

The project is physics-constrained and baseline-first for scientific reasons,
not because advanced models are out of scope.

Required model ladder:

1. transparent rule-based and linear baselines;
2. tree-based baselines such as random forest or gradient boosting;
3. artificial neural networks for nonlinear saturation prediction;
4. advanced or ensemble methods only when held-out-well error analysis shows a
   measurable benefit.

Required validation:

- split by complete well, not random neighboring depth rows;
- keep an untouched final test-well set;
- report per-well and per-class performance;
- compare calibration, uncertainty, and abstention behavior;
- preserve ambiguous or expert-review intervals;
- test missing-curve and out-of-distribution behavior;
- prevent target-derived columns from entering model inputs.

## New Research Anchor

Chong et al. (2022), *Application of machine learning to characterize gas
hydrate reservoirs in Mackenzie Delta (Canada) and on the Alaska north slope
(USA)*, provides a direct implementation reference:

- more than 10,000 depth points from five wells;
- density, porosity, resistivity, gamma ray, Vp, and Vs as candidate inputs;
- NMR-density-derived hydrate saturation as the supervised target;
- caliper-based washout screening and multivariate outlier removal;
- ANN models with selected two- or three-log combinations reporting
  approximately 80-90% predictive performance;
- evidence that models trained on Alaska wells can transfer to the Mallik
  basin.

The paper used randomized 80/20 depth samples during validation. This project
will use complete-well holdouts because adjacent depth rows are correlated and
random row splitting can overstate field generalization.

Public source:
<https://doi.org/10.1007/s10596-022-10151-9>

## Immediate Next Steps

1. Inventory the recovered PowerPoint and reduce its current 12-slide scaffold
   toward the requested approximately eight-slide visual story.
2. Recover the full Excel workbook and confirm headers, units, formulas, labels,
   and depth-alignment rules.
3. Define the label contract: NMR-derived saturation, core saturation,
   interpreted hydrate intervals, lithology, and uncertain/expert-review labels.
4. Build a synthetic Runtime Readiness page for curve coverage, units,
   missingness, bad-hole checks, core-log alignment, and blocked outputs.
5. Implement a reproducible model-evaluation skeleton with grouped
   train/validation/test wells and baseline comparisons.
6. Generate reusable visual components for the PowerPoint and Word document:
   input-to-output workflow, grouped validation, interval log panel, confusion
   matrix, calibration, uncertainty, and sweet-spot ranking.
7. Reconcile the Word document, PowerPoint, website, and code terminology.

## Decisions Still Needed

- Confirm the official project title.
- Confirm whether the mentor expects 20% training and 80% prediction, or the
  conventional 80% training and 20% validation described in the research
  paper. These are materially different workflows.
- Confirm whether NMR exists in the approved dataset.
- Confirm which saturation or interval interpretation is the authoritative
  training target.
- Confirm whether the final deliverable requires classification only,
  continuous saturation prediction, or both.
- Confirm the number of wells and which wells can be reserved as untouched
  validation and test wells.

## Source Note

This document summarizes two June 8 project-question emails, a separate source
email, and the attached Chong et al. paper. A shared ChatGPT research link was
included in the source email but did not expose readable content during this
review; it remains a pending source until its citations or transcript are
available directly.
