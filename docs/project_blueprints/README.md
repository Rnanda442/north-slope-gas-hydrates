# Project Blueprints

This folder contains unclassified planning documents for the Alaska North Slope
wireline machine-learning project.

## Current Drafts

- `Alaska_North_Slope_Wireline_ML_Research_Paper_Draft.docx`
  - Broader research-paper scaffold built from the source accumulation and
    manuscript synthesis.
- `Alaska_North_Slope_Wireline_ML_Classification_Methods_Draft.docx`
  - Sharper project-facing methods draft.
  - Focuses on measured variables, derived equations, staged classification,
    machine-learning design, expected outputs, and results/discussion structure.
- `North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview.docx`
  - Research-paper-style overview rebuilt locally on 2026-06-13 from the
    science-to-ML ladder and baseline source ledger.
  - Frames the project as a DOE-style workflow for pore-filling gas hydrate in
    sand-rich North Slope permafrost reservoirs, then separates stability
    context, reservoir quality, and hydrate response before defining the ML
    pipeline.
  - Current version emphasizes physical reasons for each parameter, hydrate and
    mimic movement patterns, screening envelopes rather than hard thresholds,
    target leakage controls, occurrence classification, saturation regression,
    validation, and output discipline. Results-bearing claims remain
    placeholders until approved-data execution.
  - Imported to the connected Google Drive account on 2026-06-11 as
    [ENRICHED ML PIPELINE North Slope Gas Hydrate Research Overview 2026-06-11](https://docs.google.com/document/d/1V3kZuu4euP6IhHwfnwscAh7RxDAqWMNu2tEf7wC_pW4).
  - The 2026-06-13 rebuild was imported to the connected Google Drive account
    as
    [SCIENCE-TO-ML North Slope Gas Hydrate Research Overview 2026-06-13](https://docs.google.com/document/d/1Ft0wgKV3p8HK1F7X4_WYVAp1jOtBYuCntdRP-Z84e5k).
- `North_Slope_Gas_Hydrate_ML_Pipeline_Status_And_Forward_Workflow_2026-06-15.docx`
  - Word-ready pipeline status brief generated from
    `docs/PIPELINE_STATUS_AND_ML_WORKFLOW_BRIEF.md`.
  - Explains where the project stands now, why the stability screen is an
    admissibility layer, how the public GitHub/Streamlit surface and
    OpenScienceLab workbench connect, and how the later approved-data ML
    workflow should move from headers/units/QC into occurrence classification,
    saturation regression, uncertainty, QC, mimic, and review outputs.
  - Uses the current source-backed project base: `SCIENCE_TO_ML_LOGIC_LADDER`,
    `ML_PIPELINE_BASELINE_SOURCE_LEDGER`, `STABILITY_CALCULATION_PLAN`,
    `WELL_LOG_REQUIREMENTS_MAP`, `ML_CITATION_PACKET_FOR_DELIVERABLES`, and
    the runtime skeleton brief.
  - Public-safe planning brief only. It does not contain approved log/core
    rows, trained model results, hydrate proof, saturation results, or
    sweet-spot ranking.
- `V5_2_North_Slope_Gas_Hydrate_Full_ML_Workflow_Companion_2026-06-15.docx`
  - Word companion for the V5.2 workflow package requested after review of the
    first stability/ML slide remake.
  - Embeds the readable slide overview, the expanded poster reference, and the
    ML runtime detail while explaining source/schema controls,
    OSL/approved-runtime inputs, stability-admissibility equations and
    caveats, feature engineering, target-only labels, occurrence
    classification, saturation regression, validation, public-safe outputs,
    and mentor decisions.
  - Public-safe planning artifact only. It does not include approved log/core
    rows, model metrics, hydrate proof, saturation results, or sweet-spot
    ranking.
  - Imported to the connected Google Drive account as
    [North Slope Gas Hydrate Full ML Workflow Diagram 2026-06-15](https://docs.google.com/document/d/1MJeWz0WDQvXBo80rYps76cuPZmJrP_BTQSka1Np5lyA).
  - Revised V5 copy with the readable slide-sized summary and simplified ML
    runtime detail was imported to the connected Google Drive account as
    [REVISED V5 North Slope Gas Hydrate Full ML Workflow Diagram 2026-06-15](https://docs.google.com/document/d/1w--XY9SobY-kadNby8ABBu-odXVveSm6l9wi_hdcSsw).
  - V5 completion copy with the expanded poster and six mentor decisions was
    imported to the connected Google Drive account as
    [V5 COMPLETION North Slope Gas Hydrate Full ML Workflow Diagram 2026-06-15](https://docs.google.com/document/d/17vxNmye93_W0_VEszEwMWCd7oDuCNLJxmADn9pzw6_Y).
  - V5.2 copy with research source anchors, current ML architecture decisions,
    and the variable fingerprint/intake validator contract was imported as
    [V5.2 North Slope Gas Hydrate Full ML Workflow Companion 2026-06-15](https://docs.google.com/document/d/1dWBNYmwGerBV8steCo0v37PbhpIAZzqNQ-Psl78Ypa8).
- `V5_5_SLIDE2_SOURCE_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Companion_2026-06-17.docx`
  - Current mentor-facing V5.5 companion generated with
    `build_full_workflow_diagram_deliverables.py`.
  - Explains the targeted Slide 2 source rebuild: selected USGS/DOE page-3
    stability screenshot/crop as the primary phase visual, DGGS RI 2018-6
    Umiat-Gubik geology-layer preview for North Slope context, digitized
    methane 5 ppt CSV as a project input inset, World Atlas Structure I/II/H
    guardrails with Structure I highlighted, methane-baseline framing, and
    stability as pressure-temperature admissibility context only.
  - Public-safe planning artifact only. It does not include approved rows,
    trained model metrics, hydrate proof, saturation outputs, occurrence
    predictions, or sweet-spot ranking.
  - Imported to Drive as native Google Docs:
    [V5.5 SLIDE2 SOURCE UPDATE North Slope Gas Hydrate ML Workflow Companion 2026-06-17](https://docs.google.com/document/d/1CyZkRgfAUSOOaRxXni0mcmFN2OQcc5pNOw8TOv44f0Q).
  - Companion deck imported to Drive as native Google Slides:
    [V5.5 SLIDE2 SOURCE UPDATE North Slope Gas Hydrate ML Workflow Slides 2026-06-17](https://docs.google.com/presentation/d/1-35vfTIXAnWCiyKTLooJy80HBYliMBliE_z4CbggJC0).
- `V5_5_MENTOR_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Companion_2026-06-17.docx`
  - Previous mentor-facing V5.5 companion generated with
    `build_full_workflow_diagram_deliverables.py`.
  - Explains the V5.5 nine-slide deck slide by slide, including source-backed
    hydrate/North Slope context, the DOE three-dataset prototype, visual
    model-run card, stability-to-ML overlay, leakage-safe ML design, and
    done/not-claimed/next guardrails.
  - Public-safe planning artifact only. It does not include approved rows,
    trained model metrics, hydrate proof, saturation outputs, occurrence
    predictions, or sweet-spot ranking. Superseded by the V5.5 Slide 2 source
    update companion for mentor review.
- `V5_4_CORRECTED_North_Slope_Gas_Hydrate_ML_Workflow_Companion_2026-06-16.docx`
  - Previous corrected companion retained as the source baseline for V5.5.
  - Imported to the connected Google Drive account as a reference copy:
    [V5.4 CORRECTED North Slope Gas Hydrate ML Workflow Companion 2026-06-16](https://docs.google.com/document/d/1sgl7cyGHOyJyWGoVC9e7LHb0JFnriPIDAmRizyf5wIg).
- `V5_3_North_Slope_Gas_Hydrate_ML_Workflow_Companion_2026-06-16.docx`
  - Flawed intermediate/reference companion generated with
    `build_full_workflow_diagram_deliverables.py`.
  - Rewrites the companion around project purpose, public vs OSL boundary, gas
    hydrate science and North Slope context, gas chemistry and hydrate
    structure type, parameter evidence, stability method, leakage-safe ML
    workflow, website outputs, complete/future work, and mentor decisions.
  - Public-safe planning artifact only. It does not include approved rows,
    trained model metrics, hydrate proof, saturation outputs, occurrence
    predictions, or sweet-spot ranking.
  - Imported to the connected Google Drive account as
    [V5.3 North Slope Gas Hydrate ML Workflow Companion 2026-06-16](https://docs.google.com/document/d/1QcF-31U77_MyPHnrBSYFZSswFyIzO8P3pMLBSTIMgMQ).
- `North_Slope_Gas_Hydrate_Mentor_Status_Package_V5_Workflow_2026-06-15.docx`
  - Short mentor-facing status package built from
    `docs/MENTOR_PROJECT_STATUS_PACKAGE_V5_WORKFLOW_2026-06-15.md`.
  - Summarizes where the project is now, what is complete outside stability,
    what remains blocked by approved data and label authority, the mentor
    decision questions, and one-sentence weekday report bullets.
  - Public-safe planning artifact only. It does not include approved rows,
    trained model metrics, hydrate proof, saturation outputs, or sweet-spot
    ranking.
- `North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview.pptx`
  - Prior tracked 9-slide visual companion deck rebuilt on 2026-06-11 from the latest
    Drive review feedback and imported to Drive as
    `FINAL CLASSIFICATION-METHODS ML VISUAL REVISION North Slope Gas Hydrate
    Slides 2026-06-11`.
  - Current version restores the older nine-slide topic sequence, restores the
    profile photo, keeps parameter measurement/caveat/model-role logic on
    one-slide surfaces, connects named ML feature equations to the visual model
    workflow, explains model-family rationale and error modes using the
    Classification Methods Draft, Chong et al. (2022), and the broader ML
    research-paper draft, and ends with the public-safe output/next-work
    summary.
  - The 2026-06-11 local refresh keeps exactly 9 slides and enriches the
    parameter, ML architecture, model-rationale, and results/discussion slides
    using the recovered Gmail ML sources in `references/ml-sources/2026-06-11/`.
  - The related 2026-06-13 local 9-slide visual companion deck was rebuilt from
    `build_ml_revamp_powerpoint.py` and the Processing-style raster slide asset
    generator.
  - That version keeps exactly 9 full-slide raster panels and reframes the
    story around hydrate-system definition, parameter tiers, hydrate/mimic
    signal movement, derived elastic features, screening envelopes, target
    leakage, occurrence classification, saturation regression, uncertainty, and
    validation.
  - Imported to the connected Google Drive account on 2026-06-11 as
    [ENRICHED 9-SLIDE ML PIPELINE North Slope Gas Hydrate Slides 2026-06-11](https://docs.google.com/presentation/d/1jazq9ZLc6G9DlM2n6QZq9rKsjDcBuw-3KrTZb4-kzJ0).
  - The 2026-06-13 rebuild was imported to the connected Google Drive account
    as
    [SCIENCE-TO-ML 9-SLIDE North Slope Gas Hydrate Slides 2026-06-13](https://docs.google.com/presentation/d/1GztudvOcJnZh28lAflNp6ZH2fMPhRgtTJgXX9ufPW24).
  - The deck remains public-safe: it uses public sources, equation/header
    references, and conceptual/sample visuals only, not real approved well rows
    or trained model outputs.
- `CURRENT_GMAIL_VISUAL_REVISION_9_SLIDE_North_Slope_Gas_Hydrate_Slides_2026-06-11.pptx`
  - Current slide authority as of the user's 2026-06-12 clarification.
  - Copied from `C:\Users\gargi\Downloads\GMAIL VISUAL REVISION 9-SLIDE North
    Slope Gas Hydrate Slides 2026-06-11.pptx`.
  - Email source: Gmail message `19eba86da8752830`, subject `New pressy`, sent
    2026-06-12 01:30 CDT.
  - Verified locally as a valid 9-slide PPTX.
  - Use this deck as the starting point for slide review and edits. Treat the
    older tracked PPTX and builder outputs as context/provenance unless the user
    explicitly chooses to rebuild from the script.
- `STABILITY_ML_REMAKE_9_SLIDE_North_Slope_Gas_Hydrate_Slides_2026-06-15.pptx`
  - Local first-draft remake of the current nine-slide deck for the stability
    and guarded-ML communication pass.
  - Built from
    `docs/project_blueprints/build_stability_ml_slide_remake.py` as nine active
    full-slide `1600 x 900` raster panels under
    `presentation_assets/stability_ml_remake_2026_06_15/`.
  - Preserves slides 1 and 2 from the current Gmail authority deck exactly; the
    builder verifies their embedded-image hashes after rebuilding.
  - Reframes slides 3-9 around the public GitHub/Streamlit delivery surface,
    the OpenScienceLab heavy-data workbench, the methane 5 ppt stability
    screen, data-readiness/confidence gates, and later approved-data occurrence
    classification plus saturation regression.
  - Uses public stability-product counts only: 8,084 scaffold wells, 184
    G10015 profiles across 24 well codes, 16,168 temperature key-depth rows,
    919 calculated key depths, 387 extrapolated key depths, 15,249 blocked key
    depths, 22 baseline admissibility intervals, and 8,054 blocked screen
    rows.
  - This is a review draft, not a Drive-published final deck. It must keep the
    guardrail that the current result is stability-admissibility only, not
    hydrate proof, saturation, sweet-spot ranking, or validated ML output.
  - User review on 2026-06-15 rejected this as the next direction because it did
    not show the whole project in one connected workflow.
- `V5_5_SLIDE2_SOURCE_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Slides_2026-06-17.pptx`
  - Current V5.5 Slide 2 source update mentor-facing workflow deck generated from
    `docs/project_blueprints/build_full_workflow_diagram_deliverables.py`.
  - Preserves the original personal/about-me opener and the nine-slide V5.5
    spine. Slide 2 is rebuilt from the selected USGS/DOE stability source
    screenshot/crop, project website map, and digitized methane 5 ppt CSV
    inset; it explains Structure I methane baseline, Structure II/H caveats,
    and stability as admissibility context only.
  - Keeps slide 3 as parameter ranges only, restores the complex project
    workflow on slide 4, adds the cleaned DOE three-dataset prototype and
    visual model-run card on slide 5, centers equations and unit gates on
    slide 6, restores the complex ML runtime architecture on slide 7, adds the
    stability-to-ML overlay on slide 8, and closes with done/not-claimed/next
    on slide 9.
  - Generated panels and the contact sheet are under
    `docs/project_blueprints/presentation_assets/v5_5_slide2_source_update_2026_06_17/`.
  - Public-safe planning artifact only. It does not include approved rows,
    final trained model metrics, hydrate proof, saturation outputs, occurrence
    predictions, row-level predictions, or sweet-spot ranking.
  - Imported to the connected Google Drive account as:
    [V5.5 SLIDE2 SOURCE UPDATE North Slope Gas Hydrate ML Workflow Slides 2026-06-17](https://docs.google.com/presentation/d/1-35vfTIXAnWCiyKTLooJy80HBYliMBliE_z4CbggJC0).
- `V5_5_MENTOR_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Slides_2026-06-17.pptx`
  - Previous V5.5 mentor-facing workflow deck retained as provenance before
    the targeted Slide 2 source rebuild.
  - Superseded by the V5.5 Slide 2 source update deck for mentor review.
- `V5_4_CORRECTED_North_Slope_Gas_Hydrate_ML_Workflow_Slides_2026-06-16.pptx`
  - Previous corrected mentor-facing workflow deck retained as the source
    baseline for V5.5.
  - Imported to the connected Google Drive account as a reference copy:
    [V5.4 CORRECTED North Slope Gas Hydrate ML Workflow Slides 2026-06-16](https://docs.google.com/presentation/d/1olavI9-nUSSvYtEm-TjYVOte-Cg-1UgaO9GMl6skDt0).
- `V5_3_North_Slope_Gas_Hydrate_ML_Workflow_Slides_2026-06-16.pptx`
  - Flawed intermediate/reference workflow deck generated from
    `docs/project_blueprints/build_full_workflow_diagram_deliverables.py`.
  - Uses nine main audience slides plus two appendix plates. The appendix
    plates keep `full_project_ml_workflow_flowchart_expanded.png` and
    `ml_pipeline_network_detail_v5.png` whole instead of fragmenting the
    complex diagrams.
  - Replaces old/AI-looking hydrate visuals with source-backed hydrate/North
    Slope context, makes slide 3 a parameter-range-only board, simplifies the
    workflow for non-ML audiences on slide 4, adds visual evidence and
    validation/output panels, and keeps stability as admissible under
    assumptions rather than occurrence or saturation proof.
  - Generated panels, appendix diagrams, and the contact sheet are under
    `docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_16_v5_3/`.
  - Imported to the connected Google Drive account as
    [V5.3 North Slope Gas Hydrate ML Workflow Slides 2026-06-16](https://docs.google.com/presentation/d/1kP0icjCLpldXZX80eww27IIokG1s3VbM5bSXiGLk8Sw).
- `V5_2_FULL_WORKFLOW_ML_DIAGRAM_North_Slope_Gas_Hydrate_Slides_2026-06-15.pptx`
  - Prior V5.2 workflow package generated after the user asked for one connected
    ML workflow with all inputs, stability logic, feature engineering, leakage
    barrier, occurrence classification, saturation regression, validation, and
    public-safe exports connected.
  - Slide 1 is now project-specific rather than a personal/about-me cover.
    Slide 2 keeps the methane hydrate intro in the Gmail visual format. Slide 3
    uses a readable V5.2 mentor-scale workflow summary: source/schema controls,
    stability context, feature engineering, leakage-safe ML, reviewed outputs,
    a public/OSL boundary band, and a red target-only rail.
  - Slide 4 embeds `full_project_ml_workflow_flowchart_expanded.png` inside the
    deck as the expanded architecture reference. Slide 7 embeds
    `ml_pipeline_network_detail_v5.png` inside the deck as the ML runtime
    detail. Slides 5, 6, 8, and 9 explain the stability, fingerprint,
    model-decision, and mentor-decision details in readable zoom panels.
  - The same asset folder also preserves
    `full_project_ml_workflow_flowchart_expanded.png`, the detailed
    poster-scale V5 architecture map with public/source and approved-OSL
    inputs, current counts, stability equations and guardrails, feature/QC and
    context families, target-only labels, validation controls, public-safe
    output rules, mentor decisions, visual mini-panels, and separate solid
    predictor/context arrows versus dashed target-only arrows.
  - The same builder now also exports `ml_pipeline_network_detail_v5.png`, a
    companion architecture visual showing feature/QC groups, compact log-track
    and X allowed matrix handoff, whole-well/compartment/geographic split
    controls, train-only preprocessing, a baseline gate, a simplified candidate
    model, occurrence and saturation heads, validation against approved labels
    only, reviewed outputs, and the target-only rail.
  - Slides 1 and 2 are preserved exactly from the current Gmail authority deck.
    Slide 3 is the readable workflow summary. Slides 4-9 zoom into
    inputs/boundary, stability, feature engineering, leakage/modeling,
    outputs/validation, and complete/calculated/blocked next decisions.
  - Generated from
    `docs/project_blueprints/build_full_workflow_diagram_deliverables.py` with
    panels under
    `docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_15/`.
  - Public-safe review draft only; no approved rows, trained model results,
    hydrate proof, saturation output, or sweet-spot ranking.
  - Imported to the connected Google Drive account as
    [FULL WORKFLOW ML DIAGRAM 9-SLIDE North Slope Gas Hydrate Slides 2026-06-15](https://docs.google.com/presentation/d/1zrWGi9bf9J2dukiZPqFQVvBCm7jCgOz1mTSIxiv8qzI).
  - Revised V5 copy with the readable slide 3 workflow summary was imported
    to the connected Google Drive account as
    [REVISED V5 FULL WORKFLOW ML DIAGRAM 9-SLIDE North Slope Gas Hydrate Slides 2026-06-15](https://docs.google.com/presentation/d/1VjVXmaIckAIl6JptU06NYM8Y7qgfGMF-Xupbd1JkwK0).
  - V5 completion copy was imported to the connected Google Drive account as
    [V5 COMPLETION Full Workflow ML Diagram 9-Slide North Slope Gas Hydrate Slides 2026-06-15](https://docs.google.com/presentation/d/1Tz_jpQByug6-RhsDwEKsA3AyPHMZdn8d6vnSS1Ndor0).
  - V5.2 copy was imported to the connected Google Drive account as
    [V5.2 FULL WORKFLOW ML DIAGRAM North Slope Gas Hydrate Slides 2026-06-15](https://docs.google.com/presentation/d/1w9eqANgOc89c1wCUC0xi9eZoBup-3JNllSUI923skgA).
- `build_ml_revamp_powerpoint.py`
  - Reproducible builder for the current 9-slide visual-first ML parameter
    architecture PowerPoint.
  - Uses the latest Drive export as a local base when present, but can rebuild
    the tracked deck from a blank 16:9 presentation using
    `ml_parameter_effect_tree.csv`.
- `ml_parameter_effect_tree.csv`
  - Machine-readable public-safe parameter/effect/caveat matrix and conceptual
    importance weighting for the rebuilt deck.
- `DOE_sent_UPDATED_North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview.docx`
  and `DOE_sent_UPDATED_North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview_Slides.pptx`
  - Source copies recovered from the user's Gmail sent message to the DOE account
    on 2026-06-10.
  - Kept as provenance inputs for the tracked integrated DOCX/PPTX above.
- `build_research_overview_deliverables.py`
  - Reproducible builder for the current Word deliverable.
  - The default script entry point now regenerates the DOCX only so it does not
    overwrite the visual-first ML deck. The legacy PPTX helper remains in the
    file for reference, but the current deck should be rebuilt with
    `build_ml_revamp_powerpoint.py`.
- `build_pipeline_status_word_brief.py`
  - Reproducible builder for the 2026-06-15 pipeline status and forward
    workflow Word brief.
- `build_full_workflow_diagram_deliverables.py`
  - Reproducible builder for the current V5.5 mentor-facing slide deck,
    audience PNG panels, contact sheet, and Word companion.

## Direction

Use the classification-methods draft as the working direction for the DOE-style
well-log project. Use the broader research-paper draft as background context and
source synthesis.

For the current approved-data readiness layer outside the deck builders, use
`docs/APPROVED_DATA_INTAKE_SPEC_2026-06-15.md`,
`docs/FIRST_MODEL_EXPERIMENT_PLAN_2026-06-15.md`,
`docs/MENTOR_DECISION_REQUESTS_2026-06-15.md`, and
`data/public_ml_products/approved_data_field_role_table_2026-06-15.csv`.
Those files define the next method step after the completed V5.5 mentor update workflow
package; they do not contain approved rows or trained model results.

## Boundary

These are public-source planning artifacts only. Do not add classified,
restricted, credentialed, approved-environment-only well logs, populated result
figures, or derived sensitive outputs to this repository.
