# ML Parameter Tree and Deck Revamp Plan

Last updated: 2026-06-11

## Source Instruction

This plan follows the user's self-sent Gmail message
`North slope gas hydrates new changes and instructions` from 2026-06-10.
It was updated after the user's Drive review requests to correct the 12-slide
revamped deck into an exactly 9-slide revision, then restore the older
topic sequence while keeping the improved visuals and ML detail. It now also
incorporates the user's June 11 Gmail ML sources recovered into
`references/ml-sources/2026-06-11/`.

The priority has changed:

1. Put the website aside for now.
2. Rebuild the PowerPoint and Word document around clearer ML visuals.
3. Use the ML paper, ML architecture/source documents, Excel header references,
   and equation documents as the concrete basis.
4. Do not use real well data in this repository.

## Approved Direction

- Deck style: hybrid. Use dark MLOps-style architecture visuals, but keep
  scientific parameter slides clean and readable.
- Parameter slide: one packed slide, not one slide per parameter. Each entry
  must separate what the curve measures from what can mask or caveat hydrate
  interpretation.
- Architecture depth: two-level. Start with a readable overview, then show the
  detailed ML architecture.
- Model framing: parallel classification and saturation-regression branches
  fed by shared physical features.
- Work order: build the architecture/parameter plan first, then rebuild the
  PowerPoint.

## Core Correction

The ML architecture should not be a generic nodes-and-edges pipeline. It should
show scientific evidence logic:

```text
parameter -> hydrate effect -> masking rock/condition -> QC/context decision
```

Examples:

- Density is affected by porosity, hydrate occupancy, mineralogy, and overburden
  compaction. It cannot be read as hydrate by itself.
- Resistivity may increase with hydrate, but gas, ice, carbonate, low porosity,
  or water-salinity assumptions can create similar high-resistivity responses.
- Vp and Vs may increase with hydrate stiffness, but overburden pressure,
  cementation, carbonate, ice, and competent lithology can mask that response.

## Parameter Signal Slide Contract

The parameter slide should use a packed visual grid. Each parameter gets:

- an icon or mini-scene;
- the measured property;
- the hydrate-supportive interpretation;
- a visible caveat or masking-condition line;
- the ML role, such as input feature, derived feature, QC gate, calibration
  anchor, or context variable.

The weights are planning priors for visual emphasis only, not trained model
feature importance. They remain in the CSV as planning context until approved
data are available, but the final slide emphasizes measurement/caveat clarity
over showing numeric weights.

The current planning matrix lives at:

`docs/project_blueprints/ml_parameter_effect_tree.csv`

## Initial Planning Weights

| Parameter family | Weight | Why it gets visual priority |
|---|---:|---|
| Deep resistivity | 18% | Strong hydrate-sensitive signal, but highly non-unique |
| NMR porosity / NMR saturation support | 16% | Best route for saturation support where measured and aligned |
| Vp / compressional velocity | 13% | Core Chong feature and hydrate/gas discriminator with context |
| Vs / shear velocity | 11% | Important stiffness/rigidity feature; helps separate hydrate from gas |
| Density and density porosity | 11% | Required for porosity, impedance, and elastic features |
| Gamma ray / lithology | 10% | Reservoir gate that prevents shale/non-reservoir false positives |
| Caliper / differential caliper | 8% | Bad-hole gate that protects every downstream curve |
| Vp/Vs and acoustic impedance | 5% | Derived elastic evidence; useful but depends on input quality |
| Core porosity/permeability/lithology | 4% | Calibration and validation anchor where approved data exist |
| Depth / P-T / overburden context | 4% | Stability and compaction context; depth remains un-normalized |

## Overburden Map Need

The future overburden map should not be treated as a hydrate classifier. Its
role is to explain how burial pressure and stratigraphic load can shift density,
porosity, Vp, Vs, impedance, and geomechanical baselines across the Alaska North
Slope.

When OpenScienceLab shapefiles are available, the map should support:

- structural position;
- stratigraphic load;
- expected compaction trend;
- local context for velocity and density baselines;
- visual explanation of why one universal threshold is not enough.

## ML Architecture Slide Contract

The architecture slide should follow the reference-image feel:

```text
Input parameters + core labels
-> unit handling and normalization
-> QC and masking review
-> feature engineering equations
-> target-leakage barrier
-> classification branch
-> saturation-regression branch
-> whole-well validation
-> predicted sweet spots
```

Required visible decisions:

- depth is retained as depth/alignment context and is not normalized in the same
  way as the other privacy-protected values;
- non-depth values may be normalized for privacy and model training;
- target fields such as `Sgh`, `S_h`, `NMR_SAT`, phase labels, and final
  sweet-spot rankings are not inputs;
- classification and saturation regression are parallel outputs from shared
  physics-backed features;
- validation is by held-out wells, not random neighboring depth rows;
- output is predicted sweet spots with uncertainty and masking explanations.
- the Classification Methods Draft requires the model to act like a disciplined
  interpreter: QC, pressure-temperature admissibility, reservoir quality,
  multi-log phase evidence, competing rock-type explanations, and producibility
  risk are explicit interpretation gates before final labels or sweet-spot
  ranking.

## Final Topic-Aligned 9-Slide Sequence

1. Gas Hydrate Occurrence and Saturation Prediction.
2. Introduction: What and Why Gas Hydrates.
3. Parameters: Well-Log Scaffold.
4. ML Methodology: Architecture.
5. ML Methodology: Why These Parameters.
6. Geomechanical Feature Sketch.
7. 3D Map and Well Context.
8. Results and Discussion Plan.
9. Conclusion.

The earlier final-revision requirements are folded into this restored sequence:
slide 3 carries the one-slide parameter scaffold, slide 4 connects equations to
the ML pipeline, slide 5 explains equation/feature, physical reason, caveat or
error, and ML use, and slide 6 shows the geomechanical equation sketch and
non-hydrate caveats.

## Word Document Effect

The Word document should not become a slide script. It should document the same
logic in methodology language:

- parameter families and physical meanings;
- masking conditions and uncertainty;
- normalization and privacy rule;
- target-leakage rule;
- classification/regression branch logic;
- overburden map role once shapefiles are available.

## Implementation Status

- `docs/project_blueprints/build_ml_revamp_powerpoint.py` rebuilt the tracked
  PowerPoint as the final topic-aligned 9-slide revision with the profile photo,
  parameter measurement/caveat/model-role logic, named feature equations,
  equation-connected ML workflow, Classification Methods Draft gates,
  model-family rationale, well/compartment validation, calibration/error-control
  language, and public-safe probability/reason-code output summary.
- `docs/project_blueprints/build_research_overview_deliverables.py` now reads
  `docs/project_blueprints/ml_parameter_effect_tree.csv` for the Word document,
  expands the Parameters, Methodology, Machine-Learning Framework, Error and
  Validation, and Discussion sections, and keeps the current website/source
  integration summary.
- The Word builder default now regenerates the DOCX only. The current deck is
  rebuilt with `build_ml_revamp_powerpoint.py` so the older PPT helper cannot
  accidentally overwrite the visual-first ML deck during routine Word updates.
- The final Drive import is
  `FINAL CLASSIFICATION-METHODS ML VISUAL REVISION North Slope Gas Hydrate
  Slides 2026-06-11`.
- The June 11 local enrichment recovered `s10596-022-10151-9.pdf` and
  `ML_Project_Reference_and_CreditScoreV4_Case_Notes.docx` from Gmail into
  `references/ml-sources/2026-06-11/`, then updated the reproducible PPTX and
  DOCX builders with source-specific ML pipeline details: Chong et al.'s
  five-well ANN saturation workflow, density/porosity/GR/Rt/Vp/Vs feature
  families, caliper/outlier preprocessing, Keras/feature-combination context,
  train-only transforms, baseline-first model selection, complete-well
  validation, model metrics, calibration, residual review, and data-quality or
  drift checks.
