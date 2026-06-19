# Full Project ML Workflow Diagram

Created: 2026-06-15

## Purpose

This file records the source language for the V5.5 mentor update workflow
package used for the Word companion and mentor deck. The package keeps the
agreed nine main audience slides, preserves the complex project workflow and
complex ML runtime diagrams inside the main sequence, and adds clearer
mentor-facing sections for the DOE three-dataset prototype, the stability-to-ML
overlay, and what is done / not claimed / next.

The figure connects:

```text
public/source inputs
+ approved runtime inputs
+ stability-admissibility screen
+ well-log/core feature engineering
+ target registry and leakage barrier
+ occurrence classification
+ saturation regression
+ validation and public-safe exports
```

It is a workflow diagram only. It does not claim hydrate proof, final hydrate
stability, hydrate saturation, trained model performance, producibility, or
sweet-spot ranking.

## Current Generated Files

Current V5.5 mentor update slide panels and contact sheet:

```text
docs/project_blueprints/presentation_assets/v5_5_mentor_update_2026_06_17/
docs/project_blueprints/presentation_assets/v5_5_mentor_update_2026_06_17/v5_5_mentor_update_contact_sheet.png
```

Key V5.5 authority panels:

```text
docs/project_blueprints/presentation_assets/v5_5_mentor_update_2026_06_17/slide_04_full_complex_project_workflow_v5_5.png
docs/project_blueprints/presentation_assets/v5_5_mentor_update_2026_06_17/slide_07_complex_ml_runtime_architecture_v5_5.png
docs/project_blueprints/presentation_assets/v5_5_mentor_update_2026_06_17/slide_05_doe_three_dataset_prototype_v5_5.png
docs/project_blueprints/presentation_assets/v5_5_mentor_update_2026_06_17/slide_08_stability_to_ml_overlay_v5_5.png
docs/project_blueprints/presentation_assets/v5_5_mentor_update_2026_06_17/slide_09_done_not_claimed_next_v5_5.png
```

V5.5 PowerPoint package:

```text
docs/project_blueprints/V5_5_MENTOR_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Slides_2026-06-17.pptx
```

Word companion:

```text
docs/project_blueprints/V5_5_MENTOR_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Companion_2026-06-17.docx
```

Previous V5.4 Drive review copies:

```text
V5.4 CORRECTED North Slope Gas Hydrate ML Workflow Slides 2026-06-16
https://docs.google.com/presentation/d/1olavI9-nUSSvYtEm-TjYVOte-Cg-1UgaO9GMl6skDt0

V5.4 CORRECTED North Slope Gas Hydrate ML Workflow Companion 2026-06-16
https://docs.google.com/document/d/1sgl7cyGHOyJyWGoVC9e7LHb0JFnriPIDAmRizyf5wIg
```

V5.4 is retained as the source baseline for V5.5. V5.3 is retained as a flawed
intermediate/reference package only. Neither should override the V5.5 local
deck unless explicitly revived.

Prior V5/V5.2 Drive copies:

```text
V5 COMPLETION Full Workflow ML Diagram 9-Slide North Slope Gas Hydrate Slides 2026-06-15
https://docs.google.com/presentation/d/1Tz_jpQByug6-RhsDwEKsA3AyPHMZdn8d6vnSS1Ndor0

V5 COMPLETION North Slope Gas Hydrate Full ML Workflow Diagram 2026-06-15
https://docs.google.com/document/d/17vxNmye93_W0_VEszEwMWCd7oDuCNLJxmADn9pzw6_Y
```

V5.2 Drive copies:

```text
V5.2 FULL WORKFLOW ML DIAGRAM North Slope Gas Hydrate Slides 2026-06-15
https://docs.google.com/presentation/d/1w9eqANgOc89c1wCUC0xi9eZoBup-3JNllSUI923skgA

V5.2 North Slope Gas Hydrate Full ML Workflow Companion 2026-06-15
https://docs.google.com/document/d/1dWBNYmwGerBV8steCo0v37PbhpIAZzqNQ-Psl78Ypa8
```

Mentor status package around the V5 workflow:

```text
docs/MENTOR_PROJECT_STATUS_PACKAGE_V5_WORKFLOW_2026-06-15.md
docs/project_blueprints/North_Slope_Gas_Hydrate_Mentor_Status_Package_V5_Workflow_2026-06-15.docx
```

Approved-data schema architecture plan and matrix:

```text
docs/APPROVED_DATA_SCHEMA_COVERAGE_AND_MODEL_ARCHITECTURE_PLAN.md
data/public_ml_products/approved_schema_coverage_matrix_2026-06-15.csv
data/public_ml_products/approved_data_field_role_table_2026-06-15.csv
docs/APPROVED_DATA_INTAKE_SPEC_2026-06-15.md
docs/FIRST_MODEL_EXPERIMENT_PLAN_2026-06-15.md
docs/MENTOR_DECISION_REQUESTS_2026-06-15.md
```

Reproducible builder:

```text
docs/project_blueprints/build_full_workflow_diagram_deliverables.py
```

## Flowchart Source

```mermaid
flowchart LR
    subgraph Sources["Source and schema controls"]
        P1["Public/source inputs<br/>Alaska DNR wells<br/>GGD223 permafrost controls<br/>G10015 temperature profiles<br/>USGS hydrate AUs and phase sources"]
        P2["Current public status<br/>8,084 public scaffold wells<br/>43 GGD223 controls<br/>184 G10015 profiles<br/>3 hydrate AUs<br/>483 temperature-profile matches<br/>22 calculated intervals<br/>8 no-stable rows<br/>8,054 blocked screen rows<br/>about 3/71 approved datasets visible for schema only"]
        Q1["Unit, depth, and QC gates<br/>preserve original headers<br/>normalize depth/units<br/>flag washout, missingness, bad alignments"]
        P1 --> Q1 --> P2
    end

    subgraph Features["Stability and physics features"]
        S1["Stability equations<br/>P_abs = P_surface + rho_w*g*z_m/1e6<br/>T_model(z) = G10015 interpolation/extrapolation<br/>T_eq = f(P_abs, CH4, salinity)<br/>stable_candidate = T_model <= T_eq<br/>baseline = methane 5 ppt"]
        S2["Stability branch<br/>calculated / no interval / blocked<br/>context, mask, confidence, and caveat only"]
        A1["Approved inputs later<br/>LAS / CSV logs<br/>core and NMR<br/>workbook labels<br/>headers, units, mnemonics"]
        SC1["Schema coverage<br/>about 3 of 71 datasets available now<br/>headers/screenshots define expected field families"]
        SC2["Role and unit controls<br/>measured inputs / derived features<br/>QC / calibration / unresolved fields"]
        F0["Measured log families<br/>GR, RHOB, Rt<br/>Vp, Vs, NMRPHI<br/>caliper where available"]
        E1["Derived physics equations<br/>Vsh = (GR-GRclean)/(GRshale-GRclean)<br/>phi_D = (rho_ma-RHOB)/(rho_ma-rho_f)<br/>AI = RHOB*Vp<br/>mu_rho = RHOB*Vs^2<br/>lambda_rho = RHOB*(Vp^2-2*Vs^2)"]
        B1["Baseline/check equations<br/>Sh_NMRD = max(0,(phi_D-phi_NMR)/phi_D)<br/>Archie-style saturation only when inputs are approved"]
        F1["Feature matrix<br/>X_allowed = measured logs + derived physics + QC flags + stability context"]
    end

    subgraph Runtime["Leakage-safe ML runtime"]
        T1["Target-only saturation and phase fields<br/>Sgh, S_h, Sh, NMR_SAT<br/>Hydrate Saturation, Swr, S_wr, phase labels"]
        L1["Target registry and leakage barrier<br/>target-only fields bypass feature matrix"]
        V1["Whole-well or compartment split<br/>split before preprocessing, selection, tuning, or calibration"]
        V2["Train-only preprocessing<br/>imputation, scaling, feature selection, and thresholds fit on training wells only"]
        M1["Modeling path<br/>complete-well or compartment split<br/>train-only preprocessing<br/>physics/simple baselines<br/>tree or ANN after controls pass"]
    end

    subgraph Outputs["Validation and reviewed outputs"]
        C1["Occurrence classifier<br/>probability and calibration"]
        R1["Saturation regressor<br/>S_h estimate and residual review"]
        O1["Validated outputs<br/>probability, saturation, uncertainty<br/>QC, mimic, and reason flags<br/>plots, tables, GIS links, manuscript exports"]
    end

    P1 --> S1
    S1 --> S2
    S2 --> F1
    A1 --> SC1
    SC1 --> SC2
    SC2 --> F0
    F0 --> E1
    E1 --> B1
    B1 --> F1
    SC2 --> L1
    SC2 --> T1
    L1 --> F1
    T1 -. labels and validation overlays only .-> M1
    T1 -. validation overlays only .-> O1
    F1 --> V1
    V1 --> V2
    V2 --> M1
    M1 --> C1
    M1 --> R1
    C1 --> O1
    R1 --> O1
```

## Current ML Architecture Decisions And Open Mentor Questions

### A. Ready to encode now

- Keep slide 4 as the full complex V5.5 project workflow architecture plate.
  Do not reduce it to a beginner flowchart. Slide 7 likewise stays the
  complex ML runtime architecture plate.
- Train two linked outputs in the approved runtime: occurrence classification
  and saturation regression. Stability remains context/admissibility only and
  does not create either label.
- Numeric predictors should get train-only 0-1 scaling after the split. Depth
  remains the alignment/context axis unless mentor approves depth as an input
  predictor. Units must remain visible beside original headers.
- The variable fingerprint contract is now part of the runtime handoff:
  original header, unit, normalized name, role, allowed-in-feature-matrix flag,
  leakage risk, and unresolved mentor question.
- Feature entry requires source, unit, QC, and leakage checks for measured
  logs and derived features such as `GR` shale/clean-sand proxy, density
  porosity, resistivity transforms, `Vp`, `Vs`, `Vp/Vs`, impedance, elastic
  attributes, NMR-density separation, and equation-list features.
- Caliper coverage comes first. If `caliper`, `CAL1`, or differential caliper
  coverage is insufficient, use a missing-QC flag instead of applying a washout
  filter.
- Baselines come before tree/boosting models, and ANN/Keras comes after those
  controls. Chong et al. 2024 / USGS supports ANN hydrate occurrence classes
  and saturation prediction as an external ML pattern, not as North Slope model
  performance: <https://pubs.usgs.gov/publication/70250169>.
- Well-MTE is the Mt. Elbert Stratigraphic Test Well and Well-IGS is the Ignik
  Sikumi Test Well; both are Eileen Gas Hydrate Trend case-study wells. Keep
  `MTE_refined` and `IGS_refined` as blue workbook-stage questions until
  metadata confirms them: <https://www.osti.gov/servlets/purl/1893637>.
- Missing-log adapters for `Vp` or `RHOB` are optional and validation-required.
  Naim et al. 2023 / MDPI supports the idea in marine hydrate settings, but it
  does not automatically validate North Slope permafrost use:
  <https://www.mdpi.com/1996-1073/16/23/7709>.

### B. Blue mentor questions

- Which saturation field is authoritative: `Sgh`, `S_h`, `Sh`, or `NMR_SAT`?
- Should occurrence use source-style classes, saturation thresholds, or
  mentor-reviewed intervals?
- Are `MTE`/`IGS` separate wells and are `*_refined` processing stages in the
  workbook?
- Do we have enough caliper coverage to apply washout filtering?
- Which wells become blind validation after full recovery?
- Are missing-log adapters allowed, or should missing curves simply block that
  feature set?

## How To Explain The Diagram

The left side is now source and schema control rather than a public
communication box. It shows the public-source scaffold, the current status
counts, and the unit/depth/QC gates that decide whether a row is usable,
blocked, or still only context.

The center and right side are the OSL and approved-runtime build path. That is
where raw source rebuilds, approved LAS/CSV/core/NMR inputs, target mapping,
model training, validation, and runtime outputs belong.

The equation layer is explicit: hydrostatic absolute pressure, G10015
temperature interpolation/extrapolation, methane 5 ppt phase-boundary lookup,
lithology/reservoir equations, density porosity, velocity conversion,
acoustic impedance, lambda-rho, mu-rho, NMR-density separation, and any
Archie-style saturation baseline are feature or check producers. They do not
create proof by themselves.

The current V5.5 slide export is a mentor-facing explanation package. It uses
the original personal/about-me opener, source-backed hydrate and North Slope
context, a parameter-range board, the full complex project workflow,
equation and unit-gate logic, the full complex ML runtime architecture, a
cleaned DOE three-dataset prototype card, a stability-to-ML overlay, and a
plain done / not claimed / next status close. The data boundary distinguishes
public GitHub/Streamlit communication from OSL or approved-runtime execution,
and the red target-only rail shows that Sgh, S_h, Sh, Swr, S_wr, NMR SAT,
hydrate saturation, and phase labels are Y-side labels rather than predictors.

The V5.5 full workflow plate carries the public counts, approved-OSL boundary,
stability equations and caveats, measured/derived/QC and context feature
families, target-only occurrence and saturation labels, split and train-only
preprocessing controls, baseline-before-ML logic, validation expectations,
runtime/public output rules, and mentor decisions. Use it when the reader
needs the full architecture.

The V5.5 ML runtime visual expands the modeling lane into feature/QC groups,
the X allowed matrix, whole-well split and train-only preprocessing controls,
baselines, ANN/Keras candidate model, occurrence and saturation output heads,
validation, reviewed outputs, and the red target-only rail. It is still an
architecture guide only, not a trained model or result claim.

The V5.5 DOE prototype slide explains the currently available approved-runtime
plumbing without overclaiming it: `curated_dataset1.xlsx` is the default
training workbook, `curated_dataset2.xlsx` and `curated_dataset3.xlsx` are
external-review workbooks or alternate training sources when labels exist, the
visible saturation variants `S_h`, `S_wr`, `Sh`, and `Swr` stay Y-only, and
training-fit metrics are runtime proof only.

The stability branch feeds the ML workflow as context, a mask, a confidence
label, or a reason flag. It is not a hydrate occurrence label and not a
saturation estimate.

The leakage barrier keeps answer-like fields outside the predictor table.
`S_h`, `Sgh`, `NMR_SAT`, phase labels, interpreted saturation, and final ranks
are targets, calibration references, validation overlays, or outputs unless
proven to be independent measured inputs.

The approved-data schema coverage step is a methodology contribution outside
the stability screen. It uses the currently visible subset, about 3 of the
expected 71 datasets, plus header screenshots to decide the pipeline structure:
preserve original headers, assign roles, normalize units, keep QC/alignment
fields separate, and route target-only fields around the feature matrix.

The final ML workflow should show two linked outputs:

```text
occurrence classification + saturation regression
```

These outputs should be validated by complete wells or compartments, not
presented from random depth-row splits as final evidence.

## Current Status Labels Used

| Label | Meaning in the diagram |
|---|---|
| Complete | Public/OSL boundary, cited methane 5 ppt phase curve, hydrostatic pressure model, temperature-model logic, source-control labels, schema/target guardrails, and guarded writer. |
| Calculated | 8,084 public scaffold wells, 43 GGD223 controls, 184 G10015 profiles, 3 hydrate AUs, 483 temperature-profile matches, 22 baseline methane 5 ppt admissibility intervals, and 8 no-stable rows. |
| Blocked | 8,054 stability-screen rows plus approved logs/core/NMR, official occurrence/saturation target authority, trained model metrics, hydrate proof, saturation outputs, and sweet-spot ranking. |

Blocked means the workflow is refusing to overclaim without required inputs. It
does not mean no hydrate.

## Slide Use

Use the generated deck as the active V5.5 mentor update package for local
mentor review. Slides 1-9 are the audience-facing sequence: personal/about-me
opener, gas hydrate and North Slope context, parameter ranges, full complex
project workflow, DOE three-dataset prototype and visual model-run card,
equations/feature engineering and unit gate, complex ML runtime architecture,
stability-to-ML overlay, and current status as done / not claimed / next.

## Word Use

Use the Word companion as a short insert or appendix page. The main Word
document can introduce the diagram before the methodology section, then use it
to explain why stability, reservoir quality, hydrate response, target mapping,
modeling, and validation are separate steps.

For mentor check-ins, use the separate status package to keep the message short:
where the project is now, what has been completed outside the stability screen,
what remains blocked by approved data or label authority, and what decisions
are needed before final ML claims can be made.

## Mentor Decisions

The V5.5 mentor update should keep these questions visible:

1. Phase-curve policy: keep methane 5 ppt as the only official baseline, or add
   a labeled scenario table?
2. Target authority: which saturation and occurrence labels are official for
   training and validation, including the current `S_h`, `S_wr`, `Sh`, and
   `Swr` prototype variants?
3. Validation split: use whole-well, compartment, geographic holdout, or a
   staged combination?
4. Temperature handling: when G10015 is missing, keep rows blocked, use proxy
   tiers, or run scenario-only gradients?
5. ML use of stability: allow the stability screen as context, confidence,
   reason flag, or mask only, never as an occurrence label, saturation target,
   or negative label for blocked rows?
6. Public website outputs: which diagrams, counts, schema, caveat views, and
   readiness views are acceptable before approved model validation?
