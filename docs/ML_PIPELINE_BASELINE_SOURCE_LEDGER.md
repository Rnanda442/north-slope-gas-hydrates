# ML Pipeline Baseline Source Ledger

Created: 2026-06-13

## Purpose

This document preserves the baseline scientific and ML decisions before the
next Word document, PowerPoint, or runtime-model pass. It is a source-backed
working ledger for:

- what the project is claiming now;
- why each input family belongs in the pipeline;
- which options are available for feature engineering, targets, models,
  validation, and outputs;
- what benefits, issues, and source guardrails apply to each option;
- which numeric ranges are screening envelopes rather than final cutoffs.

This is not meant to become the Word document as-is. The Word document should
use this ledger for citations, decisions, and diagrams, then explain the logic
in prose.

## Public Boundary

This file is public-planning safe. It must not include approved runtime well-log
rows, core rows, restricted well identifiers, trained models, populated runtime
configs, or sensitive derived outputs.

Public source well and test-site names that appear in papers may be cited when
needed. Private or approved-runtime well names must stay in the ignored runtime
folders.

## Current Baseline Claim

The project is not claiming a trained North Slope model result yet.

The current defensible claim is:

```text
The planned DOE workflow targets pore-filling methane hydrate in sand-rich,
permafrost-associated Alaska North Slope reservoirs. The ML pipeline should
encode the same sequence a geoscientist would use: first test whether hydrate
can exist, then whether the interval can host hydrate, then whether the logs
show an electrical, elastic, and porosity response consistent with hydrate.
```

This supports a pipeline architecture, not a final prediction result.

## Evidence Tiers

| Tier | Sources | What they support | Guardrail |
|---|---|---|---|
| Direct ANS logging, NMR, core, and reservoir workflow | Aung et al. (2026); Yoneda et al. (2026); Lee and Collett (2011); Haines et al. (2022); Zyrianova et al. (2024); Collett and related North Slope sources | ANS log suites, QC issues, hydrate-bearing sand interpretation, NMR/core calibration, reservoir vs seal, producibility context | Do not use field quick-look values as this project's results |
| Direct permafrost hydrate ML | Chong et al. (2022) | Permafrost-associated well-log ML saturation workflow, feature families, NMR-derived saturation target concept, QC/outlier logic | Do not copy source-paper metrics as project performance |
| Comparative hydrate ML | Singh et al. (2021); Chong et al. (2024); Tian et al. (2023); Li and Liu (2020); Naim et al. (2023) | Model options, occurrence plus saturation heads, optimal log sets, classification comparisons, LSTM option, missing-log adapter option | Method support only; not North Slope field truth unless the paper is ANS-specific |
| Project synthesis | `docs/SCIENCE_TO_ML_LOGIC_LADDER.md`; `docs/WELL_LOG_REQUIREMENTS_MAP.md`; `docs/project_blueprints/ml_parameter_effect_tree.csv`; runtime docs | Parameter grammar, schema roles, feature equations, target leakage barrier, public/runtime boundary | Planning support, not independent scientific proof |

## Recommended Baseline Pipeline

Use this as the reference architecture until the recovered workbook and approved
runtime data force a more specific implementation:

```text
approved LAS/CSV/core/NMR inputs
-> preserve raw headers, units, mnemonics, and source roles
-> map aliases to canonical fields
-> convert units with originals retained
-> align curves, core, and labels by depth with offset flags
-> run QC and missingness review
-> compute physics-derived features
-> build target registry and leakage barrier
-> add stability and reservoir context
-> train occurrence classifier
-> train saturation regressor
-> validate by complete wells or compartments
-> export probability, saturation, uncertainty, QC, and review flags
```

The key decision is to keep hydrate occurrence, hydrate saturation, reservoir
quality, permeability/producibility, and uncertainty as separate outputs.

## What The ML Is Allowed To Learn

The model should learn multivariable patterns from approved labeled data. It
should not be asked to invent the geoscience logic from a flat spreadsheet.

Allowed:

- use measured log curves as predictors;
- use source-backed derived elastic features as predictors;
- use stability and reservoir context as features, gates, masks, or reason
  flags;
- learn nonlinear combinations of resistivity, porosity, `GR`, `V_p`, `V_s`,
  `V_p/V_s`, impedance, and NMR/core support;
- output occurrence probability, saturation, uncertainty, and review flags.

Not allowed:

- use `S_h`, `Sgh`, `NMR_SAT`, phase labels, or interpreted saturation as input
  predictors;
- treat high resistivity, low `GR`, high velocity, or a stability-zone interval
  as hydrate proof by itself;
- validate by random depth rows as the final standard;
- treat missing-log imputation as measured data without provenance;
- publish approved runtime data or private identifiers in public deliverables.

## Step 1: Inputs And Header Preservation

Baseline choice:

Preserve original headers, mnemonics, units, descriptions, and schema roles
before converting anything.

Why:

The recovered screenshots show mixed headers and units, including depth in feet
or meters, density in possible g/cc or kg/m3, direct velocity fields, possible
slowness-derived velocity fields, resistivity tool mnemonics such as `A090` and
`AF90`, NMR fields, caliper fields, and target-like saturation fields.

Benefits:

- avoids silent unit mistakes;
- preserves tool provenance for later review;
- lets the runtime distinguish measured curves, derived features, QC fields,
  alignment fields, and targets;
- supports clean Word/PPT language about source-to-model traceability.

Issues:

- exact workbook formulas and alias conventions are not fully recovered;
- `A090` and `AF90` need tool confirmation before they become the selected deep
  resistivity curve;
- `S_h`, `Sgh`, `NMR_SAT`, and phase labels must be locked as targets or
  outputs unless a specific source proves a field is a measured input.

Source basis:

`docs/WELL_LOG_REQUIREMENTS_MAP.md`; `docs/runtime_skeleton_brief.md`; Chong et
al. (2022); Aung et al. (2026).

## Step 2: Unit Normalization And Depth Alignment

Baseline choice:

Normalize to canonical units while retaining raw values and original units.
Align all curves, core intervals, NMR-derived labels, and interpreted labels by
depth with a recorded matching method.

Benefits:

- makes feature equations physically valid;
- prevents feet/meters and g/cc/kg/m3 mistakes;
- keeps ML rows traceable back to source depth;
- supports later core-log and NMR-log residual review.

Issues:

- depth correspondence rules from the workbook are not recovered yet;
- core and log measurements have different sampling scales;
- nearest-depth matching can create false precision if offset flags are not
  retained.

Pipeline effect:

The ML table should include canonical features plus metadata such as source
depth, aligned depth, source unit, converted unit, and depth-offset flag. The
model may use canonical features; the review layer uses metadata.

## Step 3: QC With And Without Caliper Thresholds

Baseline choice:

Use caliper as a QC feature when available, but do not invent exact caliper
washout thresholds until bit size, caliper unit, and differential-caliper
definition are confirmed.

Three operating modes:

| Available information | QC action | What to say |
|---|---|---|
| Bit size plus caliper or differential caliper are confirmed | Use absolute or differential washout rules, plus density/sonic/resistivity consistency checks | "Bad-hole intervals are screened using source-defined caliper logic." |
| Caliper exists but bit size or sign convention is missing | Use per-well relative high-tail flags and suspicious-curve conflict flags | "Caliper supports relative QC, but exact washout thresholds remain pending." |
| Caliper is missing | Set caliper status to missing and rely on missingness, outlier, and curve-conflict review | "The pipeline cannot claim caliper-based washout removal for these intervals." |

Benefits:

- matches Chong et al. (2022) and Aung et al. (2026) emphasis on log quality;
- protects density, neutron, sonic, and resistivity from bad-hole artifacts;
- lets the model learn from a QC flag without hiding exclusions.

Issues:

- caliper is not hydrate evidence;
- exact thresholding requires tool and borehole context;
- removing too much data can bias the known-well training set.

Pipeline effect:

QC should create exclusion flags, downweight flags, and missing-QC flags. It
should not silently delete rows without an audit trail.

## Step 4: Physics Feature Engineering Options

### Option A: Measured Log Features

Recommended baseline:

Use measured `GR`, deep resistivity `R_t`, `RHOB`, porosity fields, `NPHI`,
`NMRPHI` where measured, `V_p`, `V_s`, depth, and available context fields.

Why:

These are the common bridge between direct ANS logging sources and hydrate ML
papers. Aung et al. (2026) documents current ANS LWD logging and QC context.
Chong et al. (2022) supports density, porosity, gamma ray, resistivity, `V_p`,
and `V_s` as permafrost-hydrate ML inputs. Singh et al. (2021), Chong et al.
(2024), Tian et al. (2023), Li and Liu (2020), and Naim et al. (2023) support
selected subsets as comparative ML inputs.

Benefits:

- interpretable;
- source-common;
- close to real instrument measurements;
- easier to defend in Word and slides than opaque feature sets.

Issues:

- resistivity is non-unique;
- density has small hydrate-water contrast and strong lithology/compaction
  effects;
- NMR may be missing or quality-limited;
- sonic response can be affected by ice, cement, stress, lithology, and gas;
- `GR` is a reservoir/lithology gate, not hydrate evidence.

Pipeline role:

Use measured logs as the first feature block. Apply transforms only where
physically justified, such as log-transforming resistivity.

### Option B: Derived Elastic Features

Recommended baseline:

Compute derived elastic features when the source curves are available and
unit-checked:

```text
V_p/V_s
acoustic impedance = rho * V_p
G = rho * V_s^2
K = rho * (V_p^2 - 4/3 * V_s^2)
E = 9KG / (3K + G)
nu = (3K - 2G) / (2(3K + G))
lambda = K - 2/3G
mu = G
lambda-rho = lambda * rho
mu-rho = mu * rho
```

Why:

Hydrate can stiffen the sediment frame. Shear-related features such as `V_s`,
`G`, and `mu-rho` are especially useful because free gas can raise resistivity
but does not stiffen the frame the same way.

Benefits:

- helps separate hydrate-like stiffness from gas-like resistivity;
- creates features that match geoscience crossplot logic;
- supports diagramming from raw logs to physics features to ML.

Issues:

- derived features inherit all errors from density and sonic inputs;
- ice, cement, carbonate, compaction, stress, and lithology can mimic stiffness;
- missing shear sonic limits `V_s`, `G`, `mu-rho`, and `V_p/V_s`;
- unit conversion errors can make moduli meaningless.

Pipeline role:

Use derived elastic features as a second feature block with provenance flags.
Do not include a derived feature when its source curves fail QC.

### Option C: Archie Or Petrophysical Saturation Baseline

Recommended baseline:

Use Archie-style saturation as a physics baseline, comparison feature, or
post-model review reference only after `R_w`, porosity, shale correction, and
Archie parameters are documented. Do not let Archie-derived `S_h` leak into
the feature matrix when it is also the target.

Core relation:

```text
S_w^n = a * R_w / (R_t * phi^m)
S_h approximates 1 - S_w
```

Benefits:

- gives a transparent petrophysical baseline;
- helps compare ML predictions against known hydrate interpretation methods;
- supports physically honest error analysis.

Issues:

- depends on formation-water resistivity, cementation exponent, saturation
  exponent, and shale correction;
- can overstate hydrate if gas, ice, tight rock, or salinity assumptions drive
  high resistivity;
- should be calibrated against NMR/core where available.

Source basis:

Cook and Waite (2018); Lee and Collett (2011); Haines et al. (2022); Chong et
al. (2022); project equation maps pending recovery.

### Option D: NMR, Core, And Permeability Features

Recommended baseline:

Separate NMR and core roles carefully:

- `NMRPHI` can be an input if it is a measured porosity curve;
- `NMR_SAT`, `Sgh`, interpreted hydrate saturation, and phase labels are
  targets or calibration references;
- core porosity, lithology, and saturation support calibration and validation;
- permeability belongs mainly to producibility, not hydrate occurrence.

Benefits:

- NMR/core data give independent calibration where available;
- core and pressure-core data help identify reservoir vs seal behavior;
- permeability can explain whether a hydrate-bearing interval is producible.

Issues:

- NMR tool quality and processing settings matter;
- pressure-core data are sparse and depth-matching matters;
- permeability can change after dissociation and is sediment-type dependent;
- producibility is not the same as occurrence.

Source basis:

Yoneda et al. (2026); Aung et al. (2026); Lee and Collett (2011); Haines et
al. (2022); Chong et al. (2022).

### Option E: Missing-Log Adapter

Recommended baseline:

Treat missing-log prediction as an optional adapter, not the first version of
the hydrate model. Use it only when missing `V_p`, `RHOB`, or other required
curves block a source-backed feature block.

Benefits:

- can expand usable intervals where one curve is missing;
- gives a documented path for incomplete wells;
- Naim et al. (2023) supports `V_p` or density prediction as a hydrate-log ML
  method option.

Issues:

- generated curves are not measured curves;
- imputation can leak information if trained across validation/test wells;
- model error can propagate into hydrate prediction;
- marine-source behavior does not become ANS truth.

Pipeline role:

If used, the feature table must keep separate fields for measured and estimated
curves, plus a source flag. Final validation should report results with and
without the adapter.

## Step 5: Parameter Movement Patterns

Use this as the internal "what should move and why" guide. The Word document
can turn this into prose or a clean left-to-right diagram.

| Scenario | Expected movement | Why it matters for ML |
|---|---|---|
| Pore-filling hydrate in clean sand | `GR` low; porosity present; `R_t` up; `V_p` up; `V_s` up; `mu-rho` and impedance up; NMR mobile-fluid response reduced or NMR-density separation possible; density shift subtle | Main target pattern. Needs multi-log agreement plus stability and reservoir context. |
| Water-bearing clean sand | `GR` low; porosity present; `R_t` low to moderate; velocities lower than hydrate-bearing sand; NMR mobile-fluid response present | Main no-hydrate reservoir analogue. Helps model learn clean sand without hydrate. |
| Free gas in sand | `GR` can be low; `R_t` can be high; `V_p` often lower; `V_s` does not increase like hydrate; `V_p/V_s` can rise; density/neutron gas effects may appear | Major false positive for resistivity. Elastic features are critical. |
| Ice or frozen sediment | `R_t` very high; `V_p` and `V_s` can be high; may overlap with hydrate stiffness | Needs permafrost/stability/depth context and reservoir-quality checks. |
| Tight, cemented, carbonate, or low-porosity rock | `R_t` can be high; `V_p`, `V_s`, and impedance can be high; porosity low; NMR mobile fluid low | Can mimic hydrate electrically and mechanically. Porosity and lithology gates matter. |
| Shale or clay-rich interval | `GR` high; neutron porosity can read high from bound water; resistivity can be low to moderate or misleading; sonic can be anisotropic; NMR can include clay-bound effects | Usually not target reservoir logic. Needs reservoir gate and shale/clay caveats. |
| Fracture or vein hydrate | Thin or anisotropic responses; log tools may average the signal; not necessarily tied to clean sand logic | Route to uncertainty or out-of-domain flags unless sources and labels support it. |
| Massive or nodular hydrate | Strong local response possible but less cleanly tied to sand reservoir features | Not the main DOE North Slope ML target here; should not dominate training assumptions. |

## Step 6: Screening Ranges

These ranges are working screening envelopes from the project synthesis in
`docs/SCIENCE_TO_ML_LOGIC_LADDER.md`. They are not final DOE thresholds. Use
them for QC, feature engineering, crossplots, and review flags. Calibrate them
against approved saturation, NMR, core, and known-well labels before making
results claims.

| Parameter | Water sand | Hydrate sand | Gas sand | Ice or frozen sediment | Shale or clay issue |
|---|---:|---:|---:|---:|---:|
| `RHOB` | 2.10-2.40 g/cc | 2.00-2.30 | 1.80-2.20 | 1.95-2.30 | shale 2.30-2.70 |
| `V_p` | 2.0-3.0 km/s | 2.5-4.0 | 1.5-2.5 | 3.0-4.2 | shale 2.5-4.5 |
| `V_s` | 0.5-1.5 km/s | 1.0-2.5 | 0.3-1.0 | 1.5-2.4 | shale 1.0-3.0 |
| `R_t` | 1-5 ohm-m | 10-100+ | 10-100+ | 100-1000+ | shale 1-10; clay-rich 0.5-5 |
| `NPHI` | 0.25-0.40 v/v | 0.20-0.35 | 0.05-0.20 | 0.10-0.30 | clay-rich 0.35-0.55 |
| Porosity `phi` | 0.25-0.40 | 0.20-0.35 | 0.25-0.45 | 0.10-0.35 | shale 0.05-0.20 |
| P-impedance | 4.5-7.0 | 5.5-8.5 | 3.0-5.5 | 6.0-9.0 | shale 6.0-11.0 |

| Derived feature | Hydrate sand | Gas sand | Water sand | Use |
|---|---:|---:|---:|---|
| `G = rho * V_s^2` | 5-25 GPa | 0.5-5 | 1-10 | Rigidity response |
| `K` | 10-40 GPa | 2-15 | 5-20 | Incompressibility response |
| `E` | 15-50 GPa | 2-20 | 5-25 | General stiffness |
| `nu` | 0.20-0.30 | 0.30-0.45 | 0.25-0.35 | Gas/hydrate elastic separation |
| `lambda-rho` | 12-55 GPa*g/cc | 2-25 | 8-35 | Incompressibility-sensitive crossplot |
| `mu-rho` | 10-55 GPa*g/cc | 1-10 | 2-20 | Strong rigidity discriminator |
| `V_p/V_s` | 1.6-2.4 | 2.0-4.5 | 1.8-3.2 | Useful but overlapping |

Working conflict:

The broad hydrate screening range gives `V_p/V_s = 1.6-2.4`. A tighter
crossplot hypothesis gives `V_p/V_s = 1.4-1.6` and `mu-rho = 13-42`. Use the
broad range for screening and the tighter range only as a crossplot hypothesis
until approved-data calibration supports or rejects it.

P-T and overburden context:

| Item | Working envelope |
|---|---:|
| Permafrost depth scenarios | 305 m, 610 m, 914 m |
| Geothermal gradient scenarios | 2.0, 3.2, 4.0 deg C / 100 m |
| Pore-pressure gradient | 9.795 kPa/m hydrostatic |
| Surface or shallow thermal anchor | about -10 deg C |
| Overburden stress gradient | about 16.7-27.5 MPa/km depending on lithology stack |

## Step 7: Target Registry And Leakage Barrier

Baseline choice:

Create a target registry before modeling. Every possible label field must be
classified as one of these roles:

| Target or label type | Role | Examples | Predictor status |
|---|---|---|---|
| Hydrate saturation | Regression target or calibration target | `S_h`, `Sgh`, hydrate saturation | Excluded from predictors |
| NMR-derived saturation | Target or calibration reference | `NMR_SAT`, NMR-density-derived `Sgh` | Excluded from predictors unless the field is proven to be measured `NMRPHI` |
| Occurrence or phase label | Classification target | hydrate present/absent; uncertain label; phase class | Excluded from predictors |
| Core lithology and reservoir quality | Calibration, validation, or context | sand, shale, reservoir, seal | Predictor only if encoded from independent input data and not derived from the target |
| Permeability/producibility | Separate downstream output | permeability, pressure-core permeability, producibility class | Not an occurrence label |

Benefits:

- prevents the model from learning the answer column;
- makes the Word methodology defensible;
- supports separate occurrence and saturation heads.

Issues:

- authoritative saturation field is not confirmed yet;
- fraction vs percent convention is not confirmed;
- uncertain labels and known/prediction well roles are not confirmed;
- NMR fields can be either measured inputs or derived targets, depending on
  processing.

Pipeline effect:

The target registry should fail closed. If a field might be a target-derived
column, exclude it from predictors until provenance is confirmed.

## Step 8: Context Gates And Guardrails

The word "guardrail" should mean two things:

1. **Admissibility guardrails:** cases where the model should be warned,
   masked, downweighted, or excluded because hydrate is physically unlikely or
   the data are not trustworthy.
2. **Mimic guardrails:** cases where a non-hydrate condition can look similar
   to hydrate in one or two logs.

Near-certain no-hydrate from logs alone is rare. The safer public language is:

```text
The pipeline marks intervals as hydrate-admissible, hydrate-supportive,
hydrate-mimic risk, poor-quality, or out-of-domain. It does not declare
"impossible hydrate" from one curve.
```

Recommended guardrails:

| Guardrail | Action | Reason |
|---|---|---|
| Outside stability context | Mask or strong negative context flag | Hydrate stability is necessary, though not sufficient |
| High `GR` / shale-prone interval | Reservoir-quality negative flag | Main target is pore-filling hydrate in sand-rich intervals |
| Severe washout or bad-hole QC | Exclude, downweight, or flag | Bad hole corrupts density, neutron, sonic, and resistivity |
| High `R_t` without porosity or elastic support | Hydrate-mimic flag | Tight rock, ice, cement, gas, or salinity can mimic high resistivity |
| High stiffness without resistivity or reservoir support | Hydrate-mimic flag | Cement, carbonate, ice, compaction, or lithology can mimic stiffness |
| Missing `V_s` | Reduced elastic confidence | `mu-rho`, `G`, and `V_p/V_s` become unavailable or imputed |
| Missing NMR/core target | Lower calibration confidence | Hydrate saturation label may be less independent |
| Generated missing-log feature | Provenance flag and sensitivity test | Predicted curves are not measured curves |

## Step 9: Model Options

Recommended order:

1. Physics and rule baseline.
2. Simple supervised baseline.
3. Tree-based tabular model.
4. ANN or MLP model.
5. Optional sequence model.
6. Optional missing-log adapter.

| Model option | Why choose it | Benefits | Issues | Source support |
|---|---|---|---|---|
| Physics/rule baseline | Needed before advanced ML | Transparent; catches obvious feature mistakes; compares against Archie/acoustic logic | Not flexible enough for final saturation prediction | Cook and Waite (2018); Lee and Collett (2011); Haines et al. (2022); Singh et al. (2021) |
| Logistic/linear/SGD baseline | Simple supervised benchmark | Easy to explain; good leakage check | May miss nonlinear hydrate behavior | Singh et al. (2021); general ML controls |
| Random forest or gradient boosting | Strong for tabular logs and nonlinear interactions | Handles feature interactions; gives feature importance and partial-dependence style diagnostics | Can overfit wells if validation is weak; extrapolation risk | Tian et al. (2023); Naim et al. (2023); comparative ML literature |
| ANN/MLP | Directly matches main hydrate ML analogues | Learns nonlinear saturation response; aligns with Chong et al. (2022) and Chong et al. (2024) | Needs strict validation, scaling, and enough labeled wells | Chong et al. (2022); Singh et al. (2021); Chong et al. (2024) |
| LSTM or sequence model | Uses depth order explicitly | Can learn vertical patterns if continuous depth sequences are reliable | High row-leakage risk; needs enough complete wells and careful grouped splits | Li and Liu (2020) |
| Missing-log model | Fills blocked feature sets | Can support wells missing `V_p`, `RHOB`, or other curves | Predicted input uncertainty can propagate; must not be mixed with measured logs silently | Naim et al. (2023) |

Current recommendation:

Build the first real implementation as a baseline-first, leakage-safe system
with a separate occurrence classifier and saturation regressor. Use tree/ANN
models only after target registry, grouped splits, unit normalization, and QC
are working.

## Step 10: Validation

Baseline choice:

Use complete-well or compartment holdouts for final validation. Use random row
splits only as an internal debugging check, not as final evidence.

Required validation controls:

- split wells before fitting scalers, imputers, feature selectors, or models;
- keep preprocessing train-only;
- report occurrence and saturation metrics separately;
- review residuals by well, depth, lithology/reservoir class, and QC status;
- compare predictions against NMR/core/interpreted targets when available;
- show calibration or reliability for occurrence probabilities;
- flag out-of-distribution intervals and missing-feature routes.

Why:

Depth rows from the same well are highly correlated. Random row splits can make
the model look better than it will be on a new well.

Source basis:

Chong et al. (2022) supports hydrate ML with well-log features and target
calibration; Chong et al. (2024) supports separate occurrence and saturation
outputs; Li and Liu (2020) and Naim et al. (2023) show the importance of
held-out wells/sites; project ML controls require train-only preprocessing.

## Step 11: Outputs

Recommended outputs:

| Output | Meaning | Do not confuse with |
|---|---|---|
| Occurrence probability | Probability that an interval is hydrate-bearing according to the trained classifier | Saturation, producibility, or proof |
| Saturation estimate | Continuous predicted hydrate saturation where occurrence/context allow it | Occurrence label |
| Uncertainty or confidence | Model, feature, QC, and target-confidence summary | A guarantee |
| QC status | Whether interval passed borehole, missingness, depth, and outlier checks | Hydrate evidence |
| Reason flags | Main feature families supporting or weakening prediction | Causal proof |
| Mimic flags | Gas, ice, tight rock, shale, bad-hole, or missing-feature risk | Final rejection |
| Producibility/permeability note | Reservoir/seal and flow context when core/NMR/permeability support it | Occurrence or saturation |

The first approved-data results section should show:

- well-log panel with measured and derived curves;
- occurrence probability track;
- saturation prediction track;
- known-label/target overlay where allowed;
- error or residual plot for known wells;
- calibration plot for classifier probabilities;
- feature/QC/reason flag summary;
- map or interval summary that does not expose restricted identifiers publicly.

## What This Means For The Word Document

The Word document should not become a wall of tables. Use this ledger as the
back-end reference and write the document around three moves:

1. Define the target hydrate system.
2. Explain the physics response and false positives.
3. Show how the ML pipeline turns that logic into guarded features, labels,
   models, validation, and outputs.

Recommended Word structure:

```text
Introduction and objective
-> evidence tiers and source boundary
-> target hydrate system and hydrate habits
-> stability, reservoir quality, and hydrate response
-> parameter behavior and false positives
-> feature engineering and target registry
-> model ladder: baseline, classifier, regressor
-> validation by complete wells
-> planned outputs and open data questions
```

Use dense tables only in appendices or internal docs. In the main Word text,
prefer short paragraphs, diagrams, and compact "why this matters for ML"
callouts.

## Current Open Decisions

- Which field is the authoritative hydrate-saturation target?
- Are target values fractions or percentages?
- Which labels define hydrate occurrence, no hydrate, uncertain hydrate, and
  possible hydrate habit?
- Which wells are training, validation, locked-test, and prediction wells?
- Which intervals are excluded for bad hole, missing curves, depth mismatch, or
  outlier behavior?
- Which exact `A090`/`AF90` or other resistivity curve is the preferred deep
  resistivity predictor?
- Are `V_p` and `V_s` supplied directly or derived from `DT` and `DTS`?
- Which NMR fields are measured inputs and which are derived targets?
- Which caliper thresholds are valid after bit size and unit confirmation?
- Which public source documents contain the final numeric range provenance?

## Short Citation Phrases

Use these compact source roles in drafts:

- Chong et al. (2022): direct permafrost hydrate ML analogue using well-log
  inputs and saturation targets.
- Singh et al. (2021): comparative saturation ML and optimal well-log feature
  support.
- Chong et al. (2024): comparative occurrence plus saturation ML architecture.
- Aung et al. (2026): direct ANS LWD acquisition, QC, and current log-suite
  workflow support.
- Yoneda et al. (2026): direct ANS NMR, pressure-core permeability, reservoir
  and producibility support.
- Tian et al. (2023): comparative hydrate/non-hydrate classification model
  comparison.
- Li and Liu (2020): optional depth-sequence saturation model support.
- Naim et al. (2023): optional missing-log prediction and feature-completeness
  support.
- Lee and Collett (2011) and Haines et al. (2022): ANS log-response and
  saturation-comparison support.
- Cook and Waite (2018): Archie exponent and petrophysical saturation caution.

## Claims To Avoid

- "High resistivity proves hydrate."
- "Low gamma ray proves hydrate."
- "All clean sand in the stability zone contains hydrate."
- "Permeability proves hydrate occurrence."
- "NMR-derived saturation is available for every interval."
- "The comparative marine papers validate North Slope performance."
- "Random row validation is final validation."
- "Generated missing logs are equivalent to measured logs."
- "The screening ranges are final DOE thresholds."
- "This project has model accuracy results before approved-data validation."
