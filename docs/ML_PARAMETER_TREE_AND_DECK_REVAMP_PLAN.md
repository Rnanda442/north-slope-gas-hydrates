# ML Parameter Tree and Deck Revamp Plan

Last updated: 2026-06-10

## Source Instruction

This plan follows the user's self-sent Gmail message
`North slope gas hydrates new changes and instructions` from 2026-06-10.

The priority has changed:

1. Put the website aside for now.
2. Rebuild the PowerPoint and Word document around clearer ML visuals.
3. Use the ML paper, ML architecture/source documents, Excel header references,
   and equation documents as the concrete basis.
4. Do not use real well data in this repository.

## Approved Direction

- Deck style: hybrid. Use dark MLOps-style architecture visuals, but keep
  scientific parameter slides clean and readable.
- Parameter slide: one packed slide, not one slide per parameter.
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
- a horizontal signal line;
- a negative/ambiguous side on the left;
- a hydrate-supportive side on the right;
- a visible masking-condition callout;
- a planning importance weight.

The weights are planning priors for visual emphasis only, not trained model
feature importance. They must stay labeled as conceptual until approved data are
available.

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

## Next Slide Sequence

1. Parameter signal grid.
2. ML architecture overview.
3. Detailed architecture map with decision branches.
4. Target-leakage and normalization rule.
5. Classification versus saturation-regression branch.
6. Masking/failure-mode examples: gas, ice, shale, carbonate, overburden,
   bad-hole response.
7. Predicted sweet-spot output concept.

## Word Document Effect

The Word document should not become a slide script. It should document the same
logic in methodology language:

- parameter families and physical meanings;
- masking conditions and uncertainty;
- normalization and privacy rule;
- target-leakage rule;
- classification/regression branch logic;
- overburden map role once shapefiles are available.
