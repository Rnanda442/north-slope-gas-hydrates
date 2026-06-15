# Full Project ML Workflow Diagram

Created: 2026-06-15

## Purpose

This file records the source language for the V5 workflow-diagram package used
for the Word document and nine-slide mentor deck. The package has three levels:
a readable slide-sized overview, a detailed expanded poster, and a focused ML
runtime detail.

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

Slide-sized workflow summary image:

```text
docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_15/full_project_ml_workflow_flowchart.png
```

Expanded V5 visual architecture poster image for website review and mentor
discussion:

```text
docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_15/full_project_ml_workflow_flowchart_expanded.png
```

ML architecture detail image:

```text
docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_15/ml_pipeline_network_detail_v5.png
```

V5 PowerPoint package:

```text
docs/project_blueprints/FULL_WORKFLOW_ML_DIAGRAM_9_SLIDE_North_Slope_Gas_Hydrate_Slides_2026-06-15.pptx
```

Word companion:

```text
docs/project_blueprints/North_Slope_Gas_Hydrate_Full_ML_Workflow_Diagram_2026-06-15.docx
```

Revised Drive review copies:

```text
REVISED V5 FULL WORKFLOW ML DIAGRAM 9-SLIDE North Slope Gas Hydrate Slides 2026-06-15
https://docs.google.com/presentation/d/1VjVXmaIckAIl6JptU06NYM8Y7qgfGMF-Xupbd1JkwK0

REVISED V5 North Slope Gas Hydrate Full ML Workflow Diagram 2026-06-15
https://docs.google.com/document/d/1w--XY9SobY-kadNby8ABBu-odXVveSm6l9wi_hdcSsw
```

V5 completion Drive copies:

```text
V5 COMPLETION Full Workflow ML Diagram 9-Slide North Slope Gas Hydrate Slides 2026-06-15
https://docs.google.com/presentation/d/1Tz_jpQByug6-RhsDwEKsA3AyPHMZdn8d6vnSS1Ndor0

V5 COMPLETION North Slope Gas Hydrate Full ML Workflow Diagram 2026-06-15
https://docs.google.com/document/d/17vxNmye93_W0_VEszEwMWCd7oDuCNLJxmADn9pzw6_Y
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

The current V5 slide export is a mentor-scale workflow summary. It keeps the
same V5 logic but uses five readable cards: source/schema controls, stability
context, feature engineering, leakage-safe ML, and reviewed outputs. The data
boundary band distinguishes public GitHub/Streamlit communication from OSL or
approved-runtime execution, and the red target-only rail shows that Sgh, Sh,
NMR SAT, and phase labels are Y-side labels rather than predictors.

The expanded V5 poster is the detailed reference. It carries the public counts,
approved-OSL boundary, stability equations and caveats, measured/derived/QC and
context feature families, target-only occurrence and saturation labels, split
and train-only preprocessing controls, baseline-before-ML logic, validation
expectations, runtime/public output rules, and mentor decisions. Use it when the
reader needs the full architecture, not as the main slide-scale view.

The companion ML architecture visual expands the modeling lane into feature/QC
groups, the X allowed matrix, whole-well split and train-only preprocessing
controls, a simplified candidate model, occurrence and saturation output heads,
validation, reviewed outputs, and the red target-only rail. It is still an
architecture guide only, not a trained model or result claim.

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

Use the generated deck as the active V5 workflow package for mentor review.
Slides 1 and 2 are preserved from the current Gmail authority deck. Slide 3 is
the readable workflow summary; the expanded poster remains a separate detailed
reference. Slides 4 through 8 are zoom-ins for the same map, and slide 9
summarizes what is complete, calculated, blocked, and pending mentor decision.

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

The V5 package should keep these questions visible:

1. Phase-curve policy: keep methane 5 ppt as the only official baseline, or add
   a labeled scenario table?
2. Target authority: which saturation and occurrence labels are official for
   training and validation?
3. Validation split: use whole-well, compartment, geographic holdout, or a
   staged combination?
4. Temperature handling: when G10015 is missing, keep rows blocked, use proxy
   tiers, or run scenario-only gradients?
5. ML use of stability: allow the stability screen as context, confidence,
   reason flag, or mask only, never as an occurrence label?
6. Public website outputs: which diagrams, counts, schema, caveat views, and
   readiness views are acceptable before approved model validation?
