# North Slope Project Base

Created: 2026-06-12

Use this file as the main working base for the Alaska North Slope gas hydrate project. Older planning files remain in the repo as provenance, but this is the one file to read first before changing the Word document, slides, or website.

## Current Repository

- Local path: `C:\Users\gargi\OneDrive\Documents\ai north slope gas hydrates`
- GitHub: `Rnanda442/north-slope-gas-hydrates`
- Main branch: `main`

## Core Project Goal

Build a source-backed North Slope gas hydrate workflow that can explain, plan, and later run approved well-log/core analysis for hydrate occurrence and saturation.

The public repo should contain:

- public GIS context;
- source-backed science explanation;
- Word and slide deliverables;
- header/schema examples and synthetic scaffold data only if needed later for code testing;
- code skeletons for future approved-runtime work;
- diagrams, parameter logic, and equations.

The public repo should not contain:

- classified or approved well-log/core rows;
- restricted well identifiers;
- real populated runtime configs;
- trained models from approved data;
- model metrics from approved data;
- sensitive derived outputs.

## User Direction Locked So Far

- Main goal is the Word document and 9-slide PowerPoint.
- Website is secondary and should act as a skeleton/middle layer for future DOE/Anaconda execution.
- The website can store structure, schema, diagrams, export layouts, and later optional synthetic examples for code testing.
- Real data work and real model metrics will happen later inside the DOE/approved environment.
- Screenshots of headers, equations, and project overview are acceptable evidence and should stay available in Git.
- The project needs actual ranges, numbers, scientific reasoning, and source backing before major deliverable edits.
- Slide 1 of the latest Gmail deck is basically ready. Slides 2-9 need stronger specifics, formatting, syntax, science, and ML pipeline clarity.
- The deck must stay exactly 9 slides.
- Word first, slides second, website third.
- Do not make fake datasets as the next priority. Focus first on equations, parameter logic, source-backed hydrate constraints, and the ML pipeline design.
- If synthetic/fake data is ever used later, it should only test code structure and must preserve the screenshot header style. It should not drive the science narrative.
- DOE project overview screenshots are official wording/evidence, not casual notes.

## Current Deliverable Inventory

### One File To Read First

- `docs/NORTH_SLOPE_PROJECT_BASE.md`

### Latest Slide Authority

- `docs/project_blueprints/CURRENT_GMAIL_VISUAL_REVISION_9_SLIDE_North_Slope_Gas_Hydrate_Slides_2026-06-11.pptx`
- Source: Gmail message `19eba86da8752830`
- Subject: `New pressy`
- Sent: 2026-06-12 01:30 CDT
- Verified: valid 9-slide PPTX.
- Use this deck first. Older decks and generated panels are context unless rebuilding from scripts.

### Current Word Authority

- `docs/project_blueprints/North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview.docx`
- Role: current research overview document.
- Needs next pass after parameter/source logic is made clearer.

### Other Word Drafts

- `docs/project_blueprints/Alaska_North_Slope_Wireline_ML_Research_Paper_Draft.docx`
- `docs/project_blueprints/Alaska_North_Slope_Wireline_ML_Classification_Methods_Draft.docx`
- Use the classification methods draft for the sharper DOE-style method logic.
- Use the research-paper draft for background and source synthesis.

### Website / App

- `streamlit_app.py`
- `dashboard/app.py`
- Role: public-safe atlas plus runtime skeleton.
- Current pages include Welcome, Regional Atlas, Structural Explorer, Data Library, Research Framework, and Future Well-Log Engine.
- Website should not drive the science during the next pass. It should mirror what the Word/PPT decide.

### Screenshot Evidence

- `docs/evidence/email_screenshots_2026_06_12/`
- Includes:
  - Excel header screenshots;
  - raw Excel table screenshots;
  - MTE, IGS, MTE_refined, IGS_refined examples;
  - geomechanical equation screenshots;
  - project goal/objective screenshots;
  - contact sheet.
- Treat these screenshots as origin evidence supplied by the user. Do not lose them or replace them with generic summaries.

### ML Sources

- `references/ml-sources/2026-06-11/s10596-022-10151-9.pdf`
  - Chong et al. (2022).
  - Direct gas hydrate/well-log ML anchor.
  - Use for ANN/Keras-style saturation workflow, feature table logic, well-log ML structure, and visual diagrams.
- `references/ml-sources/2026-06-11/ML_Project_Reference_and_CreditScoreV4_Case_Notes.docx`
  - General ML reliability notes.
  - Use for leakage, validation, train/test split logic, baselines, monitoring, and data-quality framing.
- `docs/ML_CITATION_PACKET_FOR_DELIVERABLES.md`
  - Current citation packet added by the other PC.

### Revision / Provenance Files

Keep these as supporting sources, but do not force the user to read all of them every time:

- `docs/PROJECT_DIRECTION_LOCK_FOR_REVIEW.md`
- `docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md`
- `docs/NEXT_STEPS_REVIEW_BRIEF.md`
- `docs/deliverable_status_inventory.md`
- `docs/deliverable_revision_base_2026_06_12/`
- `docs/NINE_SLIDE_POWERPOINT_REVISION_WORKFLOW.md`
- `docs/ML_SOURCE_COVERAGE_AND_DELIVERABLE_REVISION_PLAN.md`
- `docs/ML_PARAMETER_TREE_AND_DECK_REVAMP_PLAN.md`
- `docs/WELL_LOG_REQUIREMENTS_MAP.md`
- `docs/SWEET_SPOT_SOURCE_MATRIX.md`

## Data Header Inventory

Header/source screenshots show these field families.

Measured / input / preprocessing fields:

- `DEPTH`, `True Depth`, `Depth_ft`, `DEPT`
- `Rho_b`, `RHOB`, `Density_gpcc`
- `Phi_porosity`, `phi_den`, `DPHI`
- `NMRPHI`, `phi_nmr`
- differential caliper, `caliper`, `CAL1`
- deep formation resistivity, `Rt`, `RES`, `AO90`
- `GR`
- `Vs`, `VS1`
- `Vp`, `VELP`
- `Ratio Vp/Vs`
- impedance

Label / target / ground-truth fields:

- `Sgh`
- `S_h`
- `Sh`
- `NMR_SAT`
- `Hydrate Saturation`
- `Swr`

Screenshot review notes:

- The header screenshot explicitly marks `Sgh / NMR_SAT` as `GROUND TRUTH`.
- The `MTE` screenshot shows `S_h` and `S_wr` beside measured and derived log fields.
- The `IGS` screenshot shows `Sh` and `Swr`.
- The `MTE_refined` and `IGS_refined` screenshots show `Sgh` / hydrate saturation tied to depth correspondence.
- Working interpretation for now: the target family is hydrate saturation, but the exact column name depends on sheet/well/source context. Preserve original headers and document equivalences rather than renaming them away.

Important working rule:

- The CSV/header scaffold should preserve the screenshot headers.
- Do not internally rename the project away from the origin headers when explaining the deliverables.
- If code eventually needs canonical aliases, keep that mapping visible and secondary. The Word/slides should show the headers as given.
- Label/ground-truth columns should be handled carefully as targets, calibration, validation, or comparison fields.
- We still need to define exactly when a saturation-related field is an input support field versus the target being predicted.

## Official DOE Project Overview From Screenshots

Project title from screenshot:

> Gas hydrate occurrence and saturation prediction in permafrost sediments on Alaska North Slope using AI/ML.

Project goals from screenshot:

- Do a literature review and compile AI/ML research methodology applicable for marine and permafrost gas hydrate deposits.
- Analyze well log information to generate a dataset including density, porosity, natural gamma ray, and acoustic wave velocity readings versus depth at wellbores penetrating permafrost gas hydrate deposits.
- Utilize the generated dataset to train machine learning models to predict occurrence and saturation of gas hydrate.
- Calibrate and refine machine learning models using core analysis data by comparing log predictions against core measurements.

Learning/workflow wording from screenshot:

- Remove outliers.
- Select relevant depth intervals.
- Process raw well log data for the dataset.
- Use Python code and Keras libraries.
- Perform hyperparameter tuning for an artificial neural network algorithm.
- Run optimization tasks.
- Conduct ML model validation and testing.
- Post-process results into graphical and tabular forms.
- Deduce conclusions and recommendations from results.

Project objective bullets from screenshot:

- Compare historical AI/ML techniques employed for predicting hydrate occurrence and saturation predictions.
- Compare and analyze raw well log readings.
- Perform data pre-processing for generation of the database.
- Carry out hyperparameter tuning.
- Calculate ML model performance metrics for classification and regression analyses.
- Optimize ML model performance.
- Validate ML predictions and test using unseen data.

Use these screenshots as official DOE project-origin language. Rewrite for clarity where needed, but do not change the project meaning.

## Main Scientific Gap

Before major Word/PPT/site edits, build a parameter logic and source matrix.

That matrix should answer for each parameter:

- What does it measure?
- What unit is it in?
- What is the expected public/source-backed range?
- What change might support hydrate?
- What false positives could create the same response?
- What does it become in the ML feature table?
- Is it measured, derived, QC-only, context, or label/target?
- Which source supports the statement?

Priority parameters:

- depth;
- density / bulk density;
- density porosity;
- NMR porosity;
- resistivity;
- gamma ray;
- caliper;
- Vp;
- Vs;
- Vp/Vs;
- impedance;
- hydrate saturation / `Sgh` target family.

## Equations To Preserve

From the screenshots and slide materials, preserve equations for:

- shale volume / gamma-ray interpretation;
- density porosity;
- Vp and Vs conversion where slowness is used;
- Vp/Vs;
- acoustic impedance;
- lambda-rho;
- mu-rho;
- Young's modulus;
- Poisson's ratio;
- brittleness terms;
- NMR-density hydrate proxy;
- Archie/resistivity hydrate proxy where source-backed assumptions exist.

Important:

- Equations create features and screens.
- Equations do not prove hydrate alone.
- The deliverables need to say when an equation is a proxy, a feature, a QC screen, or a label/calibration relation.

## ML Direction

Public repo role:

- build the ML explanation, schema, equations, parameter logic, pipeline, and diagrams;
- do not claim real approved-data performance;
- do not train/report real project metrics from classified data.

Approved environment role:

- load real data;
- run final training/validation;
- compute real metrics;
- generate real outputs.

Model explanation:

- Chong et al. (2022) is the essential direct ML anchor.
- Explain ANN/Keras in plain language: a neural network learns nonlinear relationships among logs and derived features to estimate hydrate saturation.
- Explain model families only after explaining the task.
- Use baseline models as comparison points if/when synthetic or approved data are modeled.
- Validation should be by well/group/compartment rather than random depth rows when the final data allows it.

Plain-language leakage explanation:

- Target leakage means the answer column, or something derived from the answer column, accidentally enters the input features and makes the model look better than it is.
- This is why `Sgh`, `S_h`, `Sh`, `NMR_SAT`, phase labels, and final ranks need a clear role before modeling.

## Website Skeleton Direction

Website should eventually include:

- public map/GIS context;
- runtime readiness checklist;
- header/schema reference using the exact screenshot header style;
- optional synthetic/fake CSV examples only if needed later for code testing, using the same header shapes;
- parameter range explorer;
- equation-to-feature diagrams;
- target registry and leakage warning;
- placeholder model pipeline;
- placeholder outputs for occurrence, saturation, uncertainty, and review rank;
- export formats the user can later run in DOE/Anaconda.

Website should not include:

- real classified rows;
- real restricted well names;
- populated sensitive outputs;
- claims that the public version already validated the model.

## Working Definition Of Runtime

"Runtime" means the environment where the code is actually run against files.

For this project:

- Public runtime = local/GitHub-safe app using header references, public GIS context, and optional synthetic examples only if needed later.
- Approved runtime = DOE/authorized desktop or Anaconda environment where real data is loaded later.

## Work Order For Good Commits

Use small, focused commits:

1. `parameter logic/source matrix`
2. `word document update`
3. `slide deck update`
4. `website scaffold update`
5. `tests/verification`

Before each commit:

- pull/rebase `main`;
- check `git status --short`;
- avoid committing runtime data or temporary Office lock files;
- keep generated binaries only when they are intended deliverables;
- include source notes when a visual or claim changes.

## Next Work Plan

Recommended next build:

1. Create `docs/PARAMETER_LOGIC_AND_SOURCE_MATRIX.md`.
2. Fill it with the parameter table, equation table, target-role table, and source links.
3. Use that matrix to rewrite the Word document.
4. Use the revised Word logic to revise the 9-slide Gmail deck.
5. Use the revised Word/slide logic to update the website skeleton.

## Questions For User

Please answer these before the next major build.

1. For the target family, should we describe `Sgh`, `S_h`, `Sh`, and `NMR_SAT` as equivalent hydrate-saturation labels across different sheets, or do they each mean something slightly different in your files?
2. For the three wells you currently have access to, what public-safe names should we use: `Dataset 1`, `Dataset 2`, `Dataset 3`, or anonymous well-style names?
3. When the DOE wording says "occurrence and saturation prediction," should the deliverables show this as two model heads/tasks: occurrence classification and saturation regression?
4. For "sweet spot," should the first definition be tied directly to the DOE goal: hydrate occurrence plus saturation, then later add confidence, producibility, and uncertainty?
5. Do you want every parameter in the matrix to have a required "outside factors / false positives" row?

## Current Answers Already Given

- 9 slides: yes, keep exactly 9.
- Slide 1: yes, latest Gmail deck slide 1 is the intended starting point.
- Work order: Word first, slides second, website third.
- Website: skeleton for transfer into DOE/Anaconda, not final public science proof.
- Real data: no real rows in public repo; headers/screenshots only for now.
- Metrics: real metrics come later after approved-data execution.
- Fake data: do not build fake data as the next priority.
- Headers: preserve the screenshot/origin headers in the scaffold and deliverables.
- DOE project overview screenshots: official wording/evidence.
- Next build: yes, create the parameter logic/source matrix before Word/PPT.
