# Slide and Word Alignment Matrix

Created: 2026-06-12

The next rebuild should keep the Word document and nine-slide deck synchronized.
This matrix defines the intended role of each slide, the source basis, the
visual direction, and the matching Word section.

## Slide Alignment

| Slide | Goal | Current issue to avoid | Source basis | Visual direction | Matching Word section |
|---|---|---|---|---|---|
| 1 | Introduce Rohan, project title, and personal context | Do not turn this into a methods slide | User instruction and profile photo asset | Clean title/about-me panel with drawing and physical-activity cues | Title page or short author/project context |
| 2 | Explain what methane hydrate is and why North Slope matters | Do not make the structural explorer the main hydrate visual | USGS FAQ/primer, USGS SEM image, USGS FS 2019-3037, DOE/NETL pages, USGS phase-boundary source | SEM/cage visual, `CH4 + H2O`, stability gate, 2D Alaska/North Slope context, small app-context inset | Introduction |
| 3 | Teach the science-to-ML parameter ladder | Avoid a packed flat parameter list and wrong symbols | Science-to-ML ladder, well-log requirements map, parameter/effect tree, USGS log images, Haines/Lee/Chong sources | Three tiers: stability context, reservoir quality, hydrate response; each card shows symbol, physical reason, QC/source cue, and ML role | Hydrate system, parameters, and data inputs |
| 4 | Explain the ML pipeline | Avoid vague boxes and decorative arrows | Science-to-ML ladder, baseline source ledger, Chong et al. (2022), ML notes, runtime skeleton, ML visual architecture plan | Raw headers -> preserve mnemonics/units -> unit conversion -> caliper/washout QC -> features -> stability/reservoir context -> target registry -> split -> classifier/regressor -> validation | Methodology and ML framework |
| 5 | Explain why parameter behavior matters | Avoid isolated rectangles without physical behavior | Science-to-ML ladder, baseline source ledger, Lee and Collett, Haines, Helmold/LePain, parameter/effect tree | Behavior panels for clean sand, shale, gas, hydrate, ice/frozen sediment, bad hole, cement/tight rock; each panel shows signal, caveat, model effect | Parameter rationale and interpretation caveats |
| 6 | Explain geomechanics, equations, and screening envelopes | Avoid symbol clutter without definitions or hard-threshold language | Science-to-ML ladder, baseline source ledger, feature engineering code, equation docs, sonic/log sources, Lee/Haines | Equation strip with `AI`, `V_p/V_s`, `mu-rho`, `lambda-rho`; show broad screening envelopes and tighter crossplot hypotheses as calibration-needed | Feature engineering and geomechanics |
| 7 | Show regional map/context | Avoid implying GIS confirms hydrate | USGS/NETL North Slope context, source matrix, public GIS assets | 2D map plus screening layers: stability, reservoir fairway, structure, well/context markers | Regional context and evidence base |
| 8 | Show future results/discussion logic | Avoid fake performance metrics | Runtime skeleton, ML notes, validation/source plan | Empty result slots: log panel, saturation curve, occurrence probability, residuals, calibration, review flags | Results and discussion plan |
| 9 | Close with value and next steps | Avoid generic conclusion | Entire source stack and data-boundary rules | Compact workflow summary and next tasks: workbook, target fields, approved validation, final figures | Conclusion and next work |

## Word Document Section Alignment

| Word section | Must include | Source base |
|---|---|---|
| Abstract | Objective, approved-data ML goal, public-safe scaffold, no claimed model results | Project context, user constraints |
| Introduction | Gas-hydrate definition, North Slope relevance, reservoir characterization problem, why logs/core/ML are needed | USGS, DOE, NETL, North Slope source matrix |
| Source coverage and evidence base | Evidence tiers and why comparative ML sources do not replace North Slope calibration | `docs/SWEET_SPOT_SOURCE_MATRIX.md`, `docs/ML_SOURCE_COVERAGE_AND_DELIVERABLE_REVISION_PLAN.md` |
| Hydrate system and habits | Pore-filling sand hydrate as main workflow target; fracture/vein and massive/nodular habits as caveats | `docs/SCIENCE_TO_ML_LOGIC_LADDER.md`, USGS/DOE/NETL hydrate sources |
| Data and parameters | Stability context, reservoir quality, hydrate response tiers; parameter physical reason, hydrate signal, false positives, ML role, source roles | `docs/SCIENCE_TO_ML_LOGIC_LADDER.md`, `docs/ML_PIPELINE_BASELINE_SOURCE_LEDGER.md`, `ml_parameter_effect_tree.csv`, `WELL_LOG_REQUIREMENTS_MAP.md`, USGS/log sources |
| Methodology | Raw headers, source mnemonics/units, unit conversion, depth alignment, caliper/washout QC, features, stability/reservoir context, target registry, classifier/regressor | Runtime skeleton, feature engineering, ML paper, science-to-ML ladder, baseline source ledger |
| ML framework | Baselines, ANN/advanced candidates, optional sequence and missing-log adapters, classification/regression split, leakage-safe preprocessing, grouped wells | Baseline source ledger, Chong et al. (2022), Singh et al. (2021), Chong et al. (2024), Tian et al. (2023), Li and Liu (2020), Naim et al. (2023), ML notes |
| Validation and error | Target leakage, row leakage, washout, depth mismatch, missing NMR/Vs, gas/ice/cement/shale mimics, generated-log provenance, calibration and residual review | Baseline source ledger, ML notes, runtime validation, parameter/effect tree |
| Results and discussion plan | Planned figures and decision outputs without fake results | Baseline source ledger, runtime skeleton, and output readiness plan |
| Conclusion | What the workflow enables and what data/tasks remain | Full source stack and blockers |

## App/Website Boundary For This Pass

Use app/runtime material only for:

- explaining how approved data will enter the system;
- showing that the code has a skeleton for loaders, validation, feature
  engineering, modeling adapters, plotting, and exports;
- generating or reusing public-safe visual sketches.

Do not spend this pass polishing website pages, changing public navigation, or
turning the Word/PPT into a website report.
