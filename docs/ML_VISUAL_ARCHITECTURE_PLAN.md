# ML Visual Architecture Plan

Last updated: 2026-06-10

## Purpose

Define the machine-learning visuals that should explain the project using the
most concrete references currently available:

- Chong et al. (2022) and its well-log ML feature families;
- the screenshot-derived Excel header roles in `docs/WELL_LOG_REQUIREMENTS_MAP.md`;
- the equation and feature logic in the runtime scaffold;
- the project rule that targets cannot leak into input features.

The visuals are public/synthetic planning visuals. They must not display real
well-log rows, named restricted wells, trained models, or approved-runtime
outputs.

## Visual Set

| Visual | Best surface | Source basis | Reader takeaway |
|---|---|---|---|
| Header-to-model knowledge graph | Website, PowerPoint architecture slide | Excel header roles, Chong feature set, runtime equations | Measured logs, derived physics, targets, model heads, and outputs are separate layers |
| Hydrate interpretation decision tree | Website, methods slide, Word methodology section | Sweet-spot science basis and scientific rules | Hydrate classification happens after QC, stability, reservoir, and multi-log evidence gates |
| Target-leakage barrier | Website, ML slide | Header map target contract | `Sgh`, `S_h`, `NMR_SAT`, phase labels, and rankings are labels or outputs, not inputs |
| Whole-well validation split | Website, validation slide | Runtime validation plan | Future model performance must be tested on unseen wells, not random neighboring depth rows |
| Feature-family matrix | Website table, appendix, methods doc | Header map and runtime schemas | Each curve family has a scientific role, model role, and unresolved workbook question |

## Knowledge Graph Contract

Analytical question: How do the Excel headers and equations become machine
learning outputs without hiding scientific meaning?

Takeaway: The model architecture is a layered graph, not a single black-box
arrow.

Nodes:

- Excel header roles: measured logs, QC/alignment, targets.
- Canonical runtime fields: `GR`, `Rt`, `RHOB`, `NMR`, `Vp`, `Vs`, aligned depth.
- Equation features: density porosity, `Vsh`, `Vp/Vs`, acoustic impedance,
  `lambda-rho`, `mu-rho`, saturation proxies.
- Model heads: phase classification, hydrate-saturation regression,
  uncertainty or abstention.
- Review outputs: occurrence, saturation, reliability, sweet-spot review lane.

Required visual rule: Draw a visible leakage barrier between target columns and
feature columns. Target labels may calibrate or supervise; they cannot become
training inputs.

## Decision Tree Contract

Analytical question: What evidence path turns a depth interval into hydrate,
no-hydrate, gas, non-reservoir, or uncertain?

Takeaway: The workflow should preserve off-ramps instead of forcing every
interesting curve response into a hydrate call.

Gates:

1. QC pass: caliper, depth order, missingness, outliers.
2. Stability context: GHSZ admissibility, not positive proof.
3. Reservoir screen: clean sand and pore volume.
4. Multi-log phase evidence: resistivity, NMR-density separation, velocity,
   density, gamma ray, and competing explanations.
5. Calibration: core or interpreted target where available.
6. Output: phase class, continuous saturation, uncertainty, review priority.

## Implementation Status

- Added `ML_ARCHITECTURE` and `HYDRATE_DECISION_TREE` constants to
  `dashboard/visual_story_data.py`.
- Added Processing-style sketches `ml_architecture` and `decision_tree` in
  `dashboard/processing_visuals.py`.
- Added the website tab `Log Scaffold -> ML Visual Architecture` in
  `dashboard/app.py`.

## Next Use

Use the knowledge graph as the main ML architecture slide. Use the decision tree
as the explanatory methods visual before any results slide. When the approved
data are available, replace the synthetic node labels with verified workbook
mnemonics, curve coverage, target provenance, and held-out model metrics.
