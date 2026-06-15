# Science-To-ML Logic Ladder

Created: 2026-06-13

## Purpose

This document captures the next Word and PowerPoint spine: explain the hydrate
system first, then the physical logging response, then the ML workflow. The
project should not present the well-log variables as a flat parameter list.

Main narrative:

```text
We are not asking the model to magically find hydrates. We are teaching it the
same logic a geoscientist would use: first check whether hydrate can exist,
then whether the rock can host it, then whether the logs show the electrical
and mechanical response of hydrate.
```

## Hydrate System Definition

The DOE workflow is mainly built for pore-filling methane hydrate in sand-rich
permafrost-associated reservoirs on the Alaska North Slope.

This matters because pore-filling hydrate in reservoir-quality sand has the
cleanest connection to the project's log and ML logic:

- stability context says whether hydrate can exist;
- clean sand and porosity say whether the rock can host hydrate;
- resistivity, sonic velocity, shear rigidity, impedance, and NMR/core targets
  say whether the interval behaves like hydrate-bearing sediment.

## Hydrate Habits

| Hydrate habit | Log/ML meaning |
|---|---|
| Pore-filling sand hydrate | Best fit for this project. Logs can detect resistivity, sonic stiffness, and porosity changes when the interval is clean enough and inside the stability context. |
| Fracture or vein hydrate | Harder for ML because thin fractures can be averaged out by log-tool response and may not follow clean sand reservoir logic. |
| Massive or nodular hydrate | Less cleanly tied to sand-reservoir interpretation; more common in some marine settings and not the main DOE North Slope workflow target here. |

## Three-Tier Parameter Structure

| Tier | Parameters | Purpose |
|---|---|---|
| Stability context | depth, temperature gradient, pressure, permafrost depth, overburden context | Can hydrate exist here? |
| Reservoir quality | `GR`, porosity, density, lithology, caliper QC, core reservoir quality | Is there a clean sand body that can host hydrate? |
| Hydrate response | resistivity, `V_p`, `V_s`, `V_p/V_s`, impedance, `lambda-rho`, `mu-rho`, NMR/core saturation targets | Does the interval behave like hydrate-bearing sediment? |

The Word document and slides should move through these tiers in this order. A
parameter range belongs inside the ladder only after its physical reason,
hydrate signal, false positives, and ML role are stated.

## Repeated Parameter Grammar

For every parameter family, use this pattern:

```text
Parameter -> physical reason -> hydrate signal -> false positives -> ML role
```

Example:

```text
Resistivity:
Hydrate replaces conductive pore water, so Rt rises. But free gas, ice, tight
rock, carbonates, salinity assumptions, and bad-hole effects can also produce
high or misleading resistivity. Therefore Rt is useful only when paired with
Vp/Vs, Vs, GR, porosity, NMR/core targets, QC, and stability-zone context.
ML role: log-transform Rt and use it as one feature, never as a standalone
hydrate rule.
```

## Parameter Logic Matrix

| Parameter family | Physical reason | Hydrate signal | False positives or masks | ML role |
|---|---|---|---|---|
| Depth, pressure, temperature, permafrost | Methane hydrate is stable only within a pressure-temperature window | Interval is admissible if it sits inside the stability context | Local thermal gradient, abnormal pressure, depth-unit errors, structural uncertainty | Context and masking feature; not normalized like multivariable log curves |
| Overburden and burial | Compaction and stress shift density and velocity baselines | Helps decide whether stiffness is anomalous or just burial-related | Lithology stack, cementation, stress anisotropy | Context feature and cross-well normalization cue |
| Gamma ray `GR` | Natural gamma radiation separates cleaner sand from shale-prone intervals | Low `GR` can support reservoir-quality sand | Clean sand without hydrate, radioactive minerals, thin shale laminations, depth mismatch | Reservoir gate and input feature; never a hydrate label |
| Caliper / differential caliper | Borehole size controls whether density, neutron, sonic, and resistivity logs are trustworthy | In-gauge intervals support use of other curves | Washout, rugosity, tool standoff, bit-size reference errors | QC exclusion, downweighting, or missingness flag |
| Density `RHOB` and density porosity | Density constrains porosity and elastic calculations | Porous sand with plausible density porosity can host pore-filling hydrate | Shale, carbonate, coal, mineralogy, compaction, unit confusion, washout | Input feature and equation input; provenance required |
| Neutron porosity `NPHI` | Hydrogen response helps characterize pore fluids and clay-bound water | Porosity support when paired with density, NMR, and lithology | Gas effect, shale/clay water, tool environment | Input feature and porosity cross-check |
| NMR porosity / `NMR_SAT` | NMR distinguishes mobile pore fluid response and can support independent saturation estimates | NMR-density separation or NMR-derived saturation can support hydrate | Missing NMR, clay-bound water, processing settings, depth mismatch | `NMRPHI` can be an input if measured; `NMR_SAT`/`Sgh` are targets or calibration references only |
| Deep resistivity `R_t` | Hydrate replaces conductive pore water, increasing formation resistivity | Higher `R_t` in clean porous sand can support hydrate response | Free gas, ice, tight rock, carbonates/cement, salinity assumptions, invasion, shale correction, washout | Log-transform and combine with elastic, lithology, porosity, QC, and stability context |
| Compressional velocity `V_p` | Hydrate can stiffen the sediment frame and raise compressional velocity | Higher `V_p` with clean sand and `V_s` support can indicate hydrate-bearing sediment | Ice, cement, carbonate, compaction, competent lithology, stress, unit conversion | Input feature and source for impedance and elastic moduli |
| Shear velocity `V_s` | Hydrate increases rigidity; free gas does not stiffen the frame the same way | Higher `V_s` supports hydrate-related frame stiffening | Ice, cement, carbonate, lithology, stress, missing shear sonic | Input feature and source for `mu-rho`, shear modulus, and `V_p/V_s` |
| `V_p/V_s` | Ratio captures coupled compressional and shear behavior | Hydrate can trend toward stiffer, lower-ratio behavior than gas in some contexts | Strong overlap among gas, water, shale, ice, and lithology effects | Derived crossplot feature; useful only with source curves and context |
| Acoustic impedance `rho_b * V_p` | Combines density and compressional velocity | Hydrate-bearing sand can show higher stiffness/impedance than gas sand | Compaction, lithology, cement, units, bad density or velocity | Derived feature with inherited provenance |
| `lambda-rho` and `mu-rho` | Elastic attributes separate incompressibility and rigidity behavior | `mu-rho` is especially useful where hydrate increases shear rigidity | Gas, lithology, stress, shale, carbonate, input errors | Derived elastic features for crossplots and model inputs |
| Core porosity, permeability, lithology | Direct reservoir-quality and calibration evidence | Confirms sand quality, pore system, and calibration where available | Sparse core, depth mismatch, core disturbance, sampling bias | Calibration and validation evidence; not continuous truth by itself |

## Screening Envelopes, Not Cutoffs

These ranges are first-pass, user-reported working screening envelopes from the
prior local source-doc synthesis. They are not hard DOE thresholds and must be
verified against the recovered source docs, then calibrated against approved
well logs, NMR, core, and authoritative saturation targets before being used
for final decisions.

Use them to guide:

- feature engineering;
- crossplots;
- QC review;
- false-positive checks;
- physically honest ML training.

Do not use them as single-parameter hydrate labels.

## Primary Log Screening Ranges

| Parameter | Water sand | Hydrate sand | Gas sand | Ice/frozen sediment | Shale / clay issue |
|---|---:|---:|---:|---:|---:|
| Bulk density `RHOB` | 2.10-2.40 g/cc | 2.00-2.30 | 1.80-2.20 | 1.95-2.30 | shale 2.30-2.70 |
| `V_p` | 2.0-3.0 km/s | 2.5-4.0 | 1.5-2.5 | 3.0-4.2 | shale 2.5-4.5 |
| `V_s` | 0.5-1.5 km/s | 1.0-2.5 | 0.3-1.0 | 1.5-2.4 | shale 1.0-3.0 |
| Resistivity `R_t` | 1-5 ohm-m | 10-100+ | 10-100+ | 100-1000+ | shale 1-10; clay-rich 0.5-5 |
| Neutron porosity `NPHI` | 0.25-0.40 v/v | 0.20-0.35 | 0.05-0.20 | 0.10-0.30 | clay-rich 0.35-0.55 |
| Porosity `phi` | 0.25-0.40 | 0.20-0.35 | 0.25-0.45 | 0.10-0.35 | shale 0.05-0.20 |
| P-impedance `rho * V_p` | 4.5-7.0 | 5.5-8.5 | 3.0-5.5 | 6.0-9.0 | shale 6.0-11.0 |

## Derived Elastic Screening Ranges

| Feature | Hydrate sand | Gas sand | Water sand | Why it matters |
|---|---:|---:|---:|---|
| Shear modulus `G = rho V_s^2` | 5-25 GPa | 0.5-5 | 1-10 | Hydrate stiffens the frame; gas does not. |
| Bulk modulus `K` | 10-40 GPa | 2-15 | 5-20 | Helps separate incompressibility behavior. |
| Young's modulus `E` | 15-50 GPa | 2-20 | 5-25 | General stiffness indicator. |
| Poisson's ratio `nu` | 0.20-0.30 | 0.30-0.45 | 0.25-0.35 | Gas tends higher; hydrate trends lower/stiffer. |
| `lambda-rho` | 12-55 GPa*g/cc | 2-25 | 8-35 | Incompressibility-sensitive. |
| `mu-rho` | 10-55 GPa*g/cc | 1-10 | 2-20 | Strong hydrate discriminator because rigidity rises. |
| `V_p/V_s` | 1.6-2.4 | 2.0-4.5 | 1.8-3.2 | Useful but overlapping; never use alone. |

Important working conflict:

- The broader full-suite working range gives hydrate `V_p/V_s = 1.6-2.4`.
- The lambda-density crossplot note gives a tighter hydrate hypothesis of
  `V_p/V_s = 1.4-1.6` and `mu-rho = 13-42`.

Use the broad range for screening. Use the tighter range only as a crossplot
hypothesis pending approved-data calibration.

## P-T And Overburden Context Ranges

| Item | Working range |
|---|---:|
| Permafrost depth scenarios | 305 m, 610 m, 914 m |
| Geothermal gradient scenarios | 2.0, 3.2, 4.0 deg C / 100 m |
| Pore-pressure gradient | 9.795 kPa/m hydrostatic |
| Surface or shallow thermal anchor | about -10 deg C |
| Overburden stress gradient | about 16.7-27.5 MPa/km depending on lithology stack |

## Core Equations

Use unit-aware versions of these equations. If `DT` and `DTS` are slowness
curves, convert their units before taking the reciprocal.

```text
V_p = 1 / DT
V_s = 1 / DTS
G = rho * V_s^2
K = rho * (V_p^2 - 4/3 * V_s^2)
E = 9KG / (3K + G)
nu = (3K - 2G) / (2(3K + G))
lambda = K - 2/3G
mu = G
lambda-rho = lambda * rho
mu-rho = mu * rho
V_p/V_s = V_p / V_s
S_w^n = a R_w / (R_t * phi^m)
S_h approximates 1 - S_w
```

Equation caution:

- density and velocity units must be consistent;
- Archie-style saturation depends on formation-water resistivity, cementation,
  saturation exponent, shale correction, and calibration;
- `S_h`, `Sgh`, `NMR_SAT`, and interpreted phase labels are targets,
  calibration references, or outputs, not predictors.

## ML Pipeline Contract

The next Word/PPT pipeline should be:

```text
raw headers
-> preserve original units and mnemonics
-> convert units
-> remove bad borehole intervals using caliper/washout logic
-> calculate derived features
-> apply stability and reservoir context
-> train occurrence classifier
-> train saturation regressor
-> validate against Sgh/NMR/core targets
```

Expanded runtime form:

```text
approved LAS/CSV/core inputs
-> schema and alias mapping
-> unit normalization with original values preserved
-> depth alignment
-> caliper, missingness, and outlier QC
-> physics-derived features
-> target registry and leakage barrier
-> complete-well train/validation/test split
-> train-only preprocessing
-> occurrence classifier
-> saturation regressor
-> uncertainty and review outputs
-> validation against NMR/core/interpreted saturation
```

## Chong Et Al. 2022 ML Anchor

Chong et al. (2022) supports the use of density, density porosity, gamma ray,
resistivity, `V_p`, and `V_s` as ML inputs with NMR-derived `Sgh` as ground
truth in a permafrost-associated gas-hydrate workflow. It also supports
caliper screening, washout removal, and outlier detection before modeling.

Strong feature combinations reported in the user's synthesis include:

- `GR + V_p`;
- `R_t + V_p`;
- `phi + GR + V_p`;
- `phi + R_t + V_p`.

Project guardrail:

```text
headers -> unit normalization -> QC/caliper/washout removal
-> physics-derived features
-> leakage barrier: Sgh/Sh/NMR_SAT are targets only
-> occurrence classifier
-> saturation regressor
-> validation against NMR/core/interpreted saturation
```

## Word And Slide Implications

Word document:

- define the hydrate system and hydrate habits before parameters;
- organize parameters by stability, reservoir quality, and hydrate response;
- use the repeated parameter grammar for each family;
- label the numeric ranges as screening envelopes, not final cutoffs;
- explain target leakage and complete-well validation in the methodology.

Nine-slide deck:

- Slide 2: methane hydrate system, North Slope setting, stability gate.
- Slide 3: three-tier parameter ladder instead of a flat parameter grid.
- Slide 4: raw headers to leakage-safe ML architecture.
- Slide 5: physical parameter behavior and false positives.
- Slide 6: equations, derived elastic features, and crossplot hypotheses.
- Slide 8: validation and error-review outputs without fake metrics.

## Source Status

Verified locally in this repository:

- `references/ml-sources/2026-06-11/s10596-022-10151-9.pdf`
- `docs/WELL_LOG_REQUIREMENTS_MAP.md`
- `docs/project_blueprints/ml_parameter_effect_tree.csv`
- `docs/ML_CITATION_PACKET_FOR_DELIVERABLES.md`
- `docs/ML_SOURCE_COVERAGE_AND_DELIVERABLE_REVISION_PLAN.md`

User-reported source docs for the numeric ranges:

- `C:/Users/gargi/Downloads/hydrate_property_ranges_full_suite.docx`
- `C:/Users/gargi/Downloads/lambda_density_pt_overburden_ranges.docx`
- `C:/Users/gargi/Downloads/hydrate_wireline_equation_map.docx`
- `C:/Users/gargi/Downloads/north_slope_overburden_framework_field_oriented.docx`

Local verification note:

As of 2026-06-13, those four `C:/Users/gargi/Downloads/` paths are not present
on this machine. The ranges above are therefore recorded as user-supplied,
project-synthesis screening envelopes pending recovery of the named source
documents into the appropriate public or authorized source location.
