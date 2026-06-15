# North Slope Gas Hydrate ML Pipeline Status And Forward Workflow

Created: 2026-06-15

## Purpose

This brief explains where the project stands right now and how the current
work leads to the final machine-learning workflow for North Slope gas hydrate
occurrence and saturation. It is written as a Word-document-ready narrative for
mentor review, project planning, and later alignment with the slide deck.

The project is not claiming a trained model result yet. The current defensible
claim is that the team has built a public-safe scaffold, a cited
pressure-temperature stability-admissibility screen, and the structure for a
future approved-data ML workflow.

## One-Sentence Status

The project has moved from a general gas-hydrate ML idea into a controlled
workflow: public GitHub/Streamlit explains the method and displays public-safe
stability status, while OpenScienceLab is the heavy-data workbench for source
bundles, guarded calculations, and later approved well-log/core execution.

## Current Project Position

| Area | Current status | What it means |
|---|---|---|
| Public delivery surface | GitHub repository and Streamlit app are the public-facing scaffold. | Public users can see source-backed GIS context, diagrams, public CSV summaries, and workflow status. |
| Heavy-data workbench | OpenScienceLab is the place for raw source bundles, G10015 profile rows, approved runtime inputs, and guarded calculations. | Large or approved data do not need to live in the public repository. |
| Public well scaffold | The current stability scaffold has 8,084 Arctic Slope public wells. | This is a public screening inventory, not an approved runtime well-log inventory. |
| Temperature inventory | G10015 intake reports 184 temperature profiles across 24 well codes. | The temperature source layer exists, but raw profile rows remain a workbench/source-bundle input. |
| Temperature-model product | 16,168 key-depth rows: 919 calculated, 387 extrapolated, 15,249 blocked, and 0 final stability results. | This product models temperature inputs only; blocked rows are data-readiness status, not no-hydrate conclusions. |
| Guarded stability screen | Baseline methane 5 ppt run has 8,084 rows: 22 calculated admissibility intervals, 8 sufficient-input rows with no modeled stable interval, and 8,054 blocked rows. | This is a pressure-temperature admissibility screen only. It is not hydrate proof, saturation, or sweet-spot ranking. |
| Deliverables | Communication drafts, a weekday report template, a deliverable refresh plan, and a 9-slide local remake draft now exist. | The Word document and slides can now explain the public/OSL split, stability screen, and future ML path consistently. |

## Scientific Target

The working target is pore-filling methane hydrate in sand-rich,
permafrost-associated reservoirs on the Alaska North Slope. That target matters
because it gives the ML workflow a defensible order:

```text
stability context
-> reservoir quality
-> hydrate response
-> occurrence classification and saturation regression
```

The model should not be asked to "magically find hydrates" from a flat
spreadsheet. It should encode the same sequence a geoscientist would use:
first test whether hydrate could exist, then whether the rock can host it, and
then whether the logs show an electrical, elastic, porosity, NMR, or core
response consistent with hydrate-bearing sediment.

## Evidence Tiers

| Tier | Main question | Inputs or evidence | ML role |
|---|---|---|---|
| Stability context | Could methane hydrate be stable here? | Depth, pressure, temperature, permafrost context, phase curve, hydrate AU context. | Context feature, mask, or reason flag; never hydrate proof by itself. |
| Reservoir quality | Can the interval host pore-filling hydrate? | Gamma ray, porosity, density, lithology, caliper QC, core reservoir quality. | Reservoir gate and feature block. |
| Hydrate response | Does the interval behave like hydrate-bearing sediment? | Resistivity, `V_p`, `V_s`, `V_p/V_s`, acoustic impedance, `lambda-rho`, `mu-rho`, NMR/core support. | Main multilog response block for occurrence and saturation models. |
| Targets and validation | What is the answer column? | `S_h`, `Sgh`, `NMR_SAT`, phase labels, interpreted saturation, core/NMR calibration. | Targets, calibration references, or validation overlays only; excluded from predictors. |

## Why Stability Was Built First

Gas hydrate stability is necessary but not sufficient. A pressure-temperature
screen can say where hydrate could be stable under a stated set of assumptions,
but it cannot prove occurrence, estimate saturation, or rank sweet spots. That
is why the stability workflow was built as a guarded admissibility layer.

The current baseline uses:

- public well coordinates and depth fields;
- public permafrost and temperature controls from GGD223 and G10015;
- a hydrostatic pressure assumption;
- a digitized USGS SIR 2008 methane hydrate phase boundary for 100 percent
  methane and 5 ppt salinity;
- source-control confidence labels; and
- a guarded writer that leaves rows null when required gates do not pass.

The screen result should be described as:

```text
pressure-temperature stability-admissibility under the selected methane 5 ppt
baseline
```

It should not be described as:

```text
hydrate proof, saturation, occurrence probability, sweet spot, or final ML
prediction
```

## Public Repository Versus Approved Runtime Boundary

The project has two workspaces because the final science depends on approved
well-log and core data that cannot be placed in public GitHub or a public
Streamlit app.

| Workspace | Allowed content | Not allowed |
|---|---|---|
| Public GitHub / Streamlit | Public sources, public GIS, public stability summaries, source-backed diagrams, synthetic examples, empty runtime adapters, documentation, and reviewed public-safe outputs. | Approved LAS/CSV/core rows, restricted identifiers, populated runtime configs, trained models, private labels, or derived sensitive results. |
| OpenScienceLab / authorized runtime | Raw source bundles, approved logs/core/NMR, source calculations, target mapping, model training, validation, and runtime outputs. | Public release without review and public-safe reduction. |

The deliverable language should make this boundary visible. The public side is
where the method and status are explained. The runtime side is where the final
approved-data execution happens.

## Detailed Forward ML Pipeline

The recommended baseline architecture is:

```text
approved LAS/CSV/core/NMR inputs
-> preserve raw headers, mnemonics, units, and source roles
-> map aliases to canonical fields
-> convert units while retaining originals
-> align logs, core, NMR, and labels by depth
-> run QC and missingness review
-> compute physics-derived features
-> add stability and reservoir context
-> build target registry and leakage barrier
-> split by complete wells or compartments
-> fit train-only preprocessing
-> train occurrence classifier
-> train saturation regressor
-> export probability, saturation, uncertainty, QC, mimic, and review flags
```

### Step 1: Approved Inputs And Header Preservation

The starting point is not a clean ML table. The approved environment will
contain LAS, CSV, workbook, NMR, and core-related inputs with mixed headers,
units, mnemonics, and sampling depths. The runtime must first preserve the raw
field name, source unit, source mnemonic, schema role, and source file before
any conversion.

This matters because fields that look similar can have different roles. For
example, `NMRPHI` may be a measured porosity input, while `NMR_SAT`, `Sgh`, or
`S_h` may be target or calibration fields. The pipeline must fail closed: if a
field might be target-derived, it is excluded from predictors until provenance
is confirmed.

### Step 2: Unit Normalization And Depth Alignment

The runtime converts depth, density, velocity, resistivity, porosity, caliper,
and derived features into canonical units while retaining original values and
units for audit. Depth alignment must keep track of source depth, aligned depth,
matching method, and offset.

This step prevents false precision. Core, NMR, logs, and interpreted labels do
not necessarily sample the same interval thickness. A nearest-depth match is
useful only if the offset and matching rule are recorded.

### Step 3: QC, Missingness, And Bad-Hole Review

Caliper and differential caliper belong to QC, not hydrate evidence. When bit
size and units are confirmed, the runtime can apply source-defined washout
rules. Until then, caliper supports relative QC flags and suspicious-curve
review.

QC outputs should include exclusion flags, downweight flags, missingness flags,
and reason notes. The model should not silently delete intervals or treat
missing-log imputation as measured data.

### Step 4: Measured Log Feature Block

The first predictor block should use measured or supplied logs after unit
checks and QC:

- gamma ray `GR`;
- bulk density `RHOB`;
- density and neutron porosity;
- measured NMR porosity where available;
- deep resistivity `R_t` with source mnemonic retained;
- compressional velocity `V_p`;
- shear velocity `V_s`;
- depth and approved context fields.

These features are interpretable and match the direct and comparative hydrate
ML literature. They are still non-unique: high resistivity, low gamma ray, or
high velocity cannot prove hydrate by themselves.

### Step 5: Physics-Derived Feature Block

After measured logs pass unit and QC checks, the runtime can calculate derived
features:

```text
V_p/V_s
acoustic impedance = rho_b * V_p
G = rho * V_s^2
K = rho * (V_p^2 - 4/3 * V_s^2)
E = 9KG / (3K + G)
nu = (3K - 2G) / (2(3K + G))
lambda = K - 2/3G
mu = G
lambda-rho = lambda * rho
mu-rho = mu * rho
```

These features matter because pore-filling hydrate can stiffen the sediment
frame. Resistivity can be high for hydrate, free gas, ice, tight rock, cement,
or salinity effects, so elastic features such as `V_s`, shear modulus, and
`mu-rho` help separate hydrate-like stiffness from resistivity-only mimics.

Derived features inherit every error from the source curves. If density,
`V_p`, or `V_s` fails QC, the derived features must be flagged or withheld.

### Step 6: Stability And Reservoir Context

The public stability screen becomes a context layer for the approved runtime.
It can become a feature, mask, reason flag, or interpretation context, but it
does not become a hydrate label.

Reservoir context works the same way. Clean sand, low shale response, porosity,
and reservoir-quality core can support the target interpretation, but a clean
sand inside the stability window still is not automatically hydrate-bearing.

### Step 7: Target Registry And Leakage Barrier

Before modeling, every possible answer column must be classified:

| Field family | Role | Predictor status |
|---|---|---|
| `S_h`, `Sgh`, hydrate saturation | Regression target or calibration target. | Excluded from predictors. |
| `NMR_SAT` or NMR-derived saturation | Target or calibration reference unless proven to be measured porosity. | Excluded from predictors. |
| Phase or occurrence label | Classification target. | Excluded from predictors. |
| Core lithology or reservoir label | Calibration, validation, or independent context depending on source. | Allowed only if independent of target interpretation. |
| Permeability or producibility | Separate downstream output. | Not an occurrence or saturation label. |

This is the leakage barrier. It prevents the model from learning the answer
column or using a field derived from the answer as if it were an independent
predictor.

### Step 8: Model Ladder

The first implementation should be baseline-first. Advanced models become
defensible only after inputs, targets, QC, and splits are controlled.

| Model stage | Purpose | Why it belongs |
|---|---|---|
| Physics/rule baseline | Transparent benchmark using stability, reservoir, resistivity, acoustic, and Archie-style logic. | Catches feature mistakes and gives a scientific comparison. |
| Simple supervised baseline | Logistic/linear/SGD style check. | Easy to explain and useful for leakage detection. |
| Tree-based model | Random forest or gradient boosting for tabular log interactions. | Handles nonlinear feature combinations and gives diagnostic importance patterns. |
| ANN/MLP | Directly matches the main hydrate ML analogue. | Can learn nonlinear saturation response when enough labeled wells exist. |
| Optional sequence model | LSTM or depth-sequence model only if continuous depth sequences and grouped validation support it. | Uses vertical pattern, but has high leakage risk. |
| Optional missing-log adapter | Predicts missing `V_p`, `RHOB`, or other curves only as a provenance-flagged support layer. | Expands feature coverage but must not be treated as measured data. |

The recommended final shape is two linked outputs:

```text
occurrence classifier
+ saturation regressor
+ uncertainty / QC / reason flags
```

Occurrence and saturation should stay separate. A model can predict that an
interval is likely hydrate-bearing, and a second model can estimate saturation
where the occurrence/context logic supports that interpretation.

### Step 9: Validation

Final validation should use complete-well or compartment holdouts, not random
depth rows as final evidence. Depth rows from one well are correlated. Random
row splits can make the model look better than it will be on new wells.

Validation must:

- split wells before fitting scalers, imputers, feature selectors, or models;
- fit preprocessing on training wells only;
- report occurrence and saturation performance separately;
- compare known-well outputs against NMR, core, interpreted saturation, and
  phase labels where approved;
- review residuals by well, depth, reservoir class, QC status, and missing-log
  route;
- flag out-of-distribution intervals and generated-feature routes.

### Step 10: Outputs

The final approved-environment workflow should export:

| Output | Meaning | Guardrail |
|---|---|---|
| Occurrence probability | Classifier estimate that an interval is hydrate-bearing. | Not saturation, proof, or producibility. |
| Saturation estimate | Continuous hydrate saturation estimate. | Not an occurrence label by itself. |
| Uncertainty or confidence | Model, feature, QC, target, and source-control status. | Not a guarantee. |
| QC status | Bad-hole, missingness, depth, and outlier review. | Not hydrate evidence. |
| Reason flags | Feature families supporting or weakening the prediction. | Not causal proof. |
| Mimic flags | Gas, ice, cement, shale, tight rock, bad-hole, or missing-feature risk. | Not final rejection by itself. |
| Review exports | Plots, tables, GIS links, and manuscript figures. | Public release only after boundary review. |

## Source Basis

| Source family | Role in this project |
|---|---|
| USGS, DOE, and NETL gas hydrate sources | Hydrate definition, North Slope context, and the rule that pressure, temperature, salinity, and gas composition control stability. |
| USGS SIR 2008-5175 | Method anchor for intersecting wellbore temperature profiles with a methane hydrate phase boundary. |
| NSIDC GGD223 and G10015 | Public permafrost-depth controls and processed Arctic Slope temperature profiles. |
| USGS OM-222 | Preferred future mapped base-of-ice-bearing-permafrost surface after digitizing/georeferencing. |
| Lee and Collett (2011), Haines et al. (2022), Aung et al. (2026), Yoneda et al. (2026) | North Slope hydrate, log-response, NMR/core, reservoir, QC, and producibility context. |
| Chong et al. (2022) | Direct permafrost-associated gas-hydrate ML analogue using well-log inputs and saturation references. |
| Singh et al. (2021) | Comparative saturation ML and optimal well-log feature support. |
| Chong et al. (2024) | Comparative occurrence plus saturation ML architecture support. |
| Tian et al. (2023), Li and Liu (2020), Naim et al. (2023) | Comparative model options for classification, sequence modeling, and missing-log adapters. |
| Cook and Waite (2018) | Archie saturation exponent and petrophysical saturation caution. |
| Project documents | `SCIENCE_TO_ML_LOGIC_LADDER`, `ML_PIPELINE_BASELINE_SOURCE_LEDGER`, `WELL_LOG_REQUIREMENTS_MAP`, `STABILITY_CALCULATION_PLAN`, and runtime docs define the current implementation contract. |

## What Is Complete

- Public GitHub/Streamlit scaffold and public data boundary.
- OpenScienceLab/public-delivery division.
- Public stability scaffold for 8,084 Arctic Slope public wells.
- G10015 temperature inventory summary with 184 profiles across 24 well codes.
- Temperature-model product with calculated, extrapolated, and blocked
  key-depth rows.
- Cited methane 5 ppt phase-curve lookup.
- Hydrostatic pressure helper logic.
- Temperature-model logic and duplicate-depth handling.
- Source-control confidence labels.
- Guarded baseline stability-screen writer and public display.
- Communication drafts and slide remake that preserve the no-proof guardrail.

## What Is Calculated

- 919 temperature key-depth rows are calculated.
- 387 of those calculated key-depth rows are extrapolated below measured
  profile coverage.
- 22 baseline methane 5 ppt stability-admissibility intervals are calculated.
- 8 rows had sufficient inputs but no modeled stable interval under the
  baseline run.

These are calculation statuses. They are not hydrate detections.

## What Is Intentionally Blocked

- 15,249 temperature key-depth rows are blocked because required profile/depth
  inputs are missing or insufficient.
- 8,054 stability-screen rows are blocked because at least one source or
  calculation gate did not pass.
- Approved well-log rows, core rows, target labels, trained models, and
  runtime metrics remain outside public GitHub/Streamlit.
- Final occurrence labels, saturation targets, and project ML metrics remain
  blocked until approved-data execution.

Blocked does not mean no hydrate. Blocked means the workflow is refusing to
make a claim without the required inputs.

## Next Decisions

1. Keep the official baseline as 100 percent methane plus 5 ppt salinity, or
   choose a replacement phase-curve model/source.
2. Decide whether the Collett et al. (2011) / Holder et al. (1987) mixed-gas
   curve should be digitized or model-generated as sensitivity only.
3. Define high, medium, and low source-control thresholds for temperature and
   permafrost control distance.
4. Decide whether OM-222 permafrost base should be digitized next.
5. Confirm which approved well-log/core/NMR fields can be used for occurrence
   labels, saturation regression targets, calibration, and validation.
6. Confirm whether the final ML workflow should always present occurrence
   classification and saturation regression as two linked outputs.
7. Recover the full workbook/formulas so the header map can become a complete
   runtime input contract.

## Near-Term Work Plan

The next practical sequence is:

```text
review this pipeline brief
-> align Word document and 9-slide deck language
-> recover workbook/formula details
-> finalize target registry and leakage barrier
-> configure approved runtime in OpenScienceLab/DOE environment
-> load approved logs/core/NMR
-> run QC, alignment, and feature engineering
-> train baseline occurrence and saturation models
-> validate by complete wells or compartments
-> export approved figures and public-safe summaries
```

Until approved-data validation exists, the public deliverables should emphasize
workflow readiness, source traceability, stability-admissibility, and blocked
states rather than presenting hydrate discoveries or model performance.

## Claims To Avoid

- High resistivity proves hydrate.
- Low gamma ray proves hydrate.
- All clean sand in the stability zone contains hydrate.
- The 22 calculated intervals are hydrate detections.
- Blocked rows are no-hydrate rows.
- Public scaffold wells are approved-runtime training wells.
- Comparative ML papers validate this project's final accuracy.
- Random row validation is final validation.
- `S_h`, `Sgh`, `NMR_SAT`, phase labels, or rankings are predictors.
- Screening ranges are final DOE thresholds.
- The project has final hydrate saturation results before approved-data
  validation.

## Word And Slide Translation

The Word document should use this brief to explain the project in this order:

```text
current status
-> target hydrate system
-> public/runtime boundary
-> stability-admissibility screen
-> evidence tiers
-> ML pipeline
-> validation and outputs
-> open decisions and next work
```

The nine-slide deck should keep slides 1 and 2 from the current Gmail authority
deck, then use slides 3-9 to show:

- evidence tiers, not a flat parameter list;
- public GitHub/Streamlit versus OpenScienceLab;
- why hydrate signals have mimics;
- physics features and stability context;
- public stability products as readiness, not proof;
- complete/calculated/blocked/future status;
- mentor decisions before prediction claims.
