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
- The screenshots are enough to document the header/schema families and sheet/tab
  names. They are not the actual datasets. Do not spend project energy naming
  datasets in public deliverables; the useful evidence is the header structure,
  equations, official project wording, and target-field roles.
- The visible sheet/tab names include `MTE`, `IGS`, `MTE_refined`, and
  `IGS_refined`. Treat these as evidence of raw/refined table structure until
  the user can safely describe the full workbook organization.

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

Working implication:

- The DOE overview explicitly names both occurrence and saturation prediction.
- The ML workflow should therefore be framed as two related tasks:
  occurrence classification and saturation regression/estimation.
- Do not invent final metrics or labels yet; the real target roles should be
  refined after the parameter logic and external-factor matrix is built.

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

Before major Word/PPT/site edits, identify the real source-backed science logic
for each parameter from the header screenshots and equations. This should become
a high-level Word section first, then a more detailed parameter/source matrix.

The project should not begin by making fake data. The project should begin by
explaining why each logged property matters, what can distort it, and how a
machine-learning pipeline should use it without making unsupported hydrate
claims.

That matrix should answer for each parameter:

- What does it measure?
- What unit is it in?
- What is the expected public/source-backed range?
- What change might support hydrate?
- What false positives could create the same response?
- What external factors can change the reading without proving hydrate?
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

External factors to explicitly discuss:

- overburden and effective stress;
- pressure-temperature stability;
- lithology and shale content;
- clean sand versus shale/carbonate/coal/ice/cement effects;
- gas versus hydrate ambiguity;
- salinity and formation water assumptions;
- borehole washout and caliper quality;
- compaction and porosity loss with depth;
- core-to-log depth mismatch;
- missing NMR or missing shear sonic;
- tool/mnemonic differences across sheets.

## Stability Parameter Source Plan

Goal: add a public-source stability layer to the Structural Explorer only after
each stability input has a clear source, unit, and confidence label. This layer
should be described as a **gas hydrate stability admissibility screen**, not as
hydrate detection or saturation prediction.

Core stability equation/workflow:

```text
well location
+ well depth
+ base of ice-bearing permafrost
+ geothermal gradient / temperature context
+ hydrostatic pressure assumption
+ methane hydrate phase curve
= estimated top, base, and thickness of gas hydrate stability zone
```

Current input status:

| Stability input | Current status | Source or proxy plan |
| --- | --- | --- |
| Well location | Available locally | Alaska DNR Well Bottom Hole Location shapefile in `raw_data/Wells/Well_Bottom_Hole_Location/`; use wellhead/bottom-hole `lat`/`lon` for spatial joins. |
| Well depth | Mostly available locally | Use `TrueVertic` first and `DrillerTot` as fallback from the Alaska DNR well file. These are public well-depth fields, not a separate user-downloaded dataset. Confirm units before calculations; working assumption is feet until field documentation confirms otherwise. |
| Base of ice-bearing permafrost | Missing as ready GIS locally | Best source is USGS OM-222, "Map showing depth to the base of deepest ice-bearing permafrost as determined from well logs, North Slope, Alaska." It appears available as a PDF/plate rather than a ready GeoPackage. Search for a digitized derivative; otherwise digitize contours/control points and record that provenance. |
| Geothermal gradient / temperature | Missing as well-specific layer locally | Use public borehole temperature sources: NSIDC G10015 Arctic Slope deep borehole temperature profiles, NSIDC GGD223 borehole/permafrost context, USGS OFR 82-1039, and USGS OFR 82-535. Calculate local gradients where profiles exist; use scenario gradients where not. |
| Pressure | Available as assumption | Use hydrostatic pore-pressure gradient as first-pass source-backed assumption, currently `9.795 kPa/m`; flag as assumed rather than measured. |
| Hydrate phase curve | Available from literature | Use a published methane hydrate pressure-temperature phase curve or lookup. USGS SIR 2008-5175 and USGS phase-boundary sources support the stability-screen framing. |
| Regional hydrate context | Public GIS available | Use USGS 2019 Gas Hydrate Assessment Unit boundaries and input forms for regional context and well/AU joins. This is not direct hydrate proof. |

Current local well-depth coverage check from the Alaska DNR well file:

- statewide well records: `10,250`;
- North Slope / Arctic Slope-ish records checked: about `8,278`;
- positive `DrillerTot`: about `7,730` of `8,278` records, or `93.4%`;
- positive `TrueVertic`: about `7,728` of `8,278` records, or `93.4%`.

`TrueVertic` is preferred for stability because pressure and temperature depend
on vertical depth. `DrillerTot` is useful for reach/depth-availability screening
but can overstate vertical depth in deviated wells.

Stability-source tasks before coding the explorer layer:

1. Download or link the public sources into a stability source ledger.
2. Confirm whether OM-222 or a derivative provides usable GIS contours/control
   points for base of ice-bearing permafrost.
3. Download NSIDC/public borehole temperature data and inspect columns, units,
   depth conventions, and station locations.
4. Define scenario fallbacks:
   - permafrost base: `305`, `610`, and `914 m` unless replaced by mapped data;
   - geothermal gradient: `2.0`, `3.2`, and `4.0 C / 100 m` unless replaced by
     local borehole-derived gradients;
   - pressure gradient: `9.795 kPa/m` hydrostatic first-pass.
5. Decide the phase-curve implementation: formula, lookup table, or digitized
   published curve.
6. Build confidence labels:
   - `high`: nearby well-specific temperature/permafrost control;
   - `medium`: mapped/interpolated public source;
   - `low`: regional scenario assumption only.

Target output fields for a future stability table:

```text
well_id
lat
lon
tvd_m
depth_source
permafrost_base_m
permafrost_source
geothermal_gradient_c_per_100m
temperature_source
pressure_gradient_kpa_m
pressure_source
phase_curve_source
stability_top_m
stability_base_m
stability_thickness_m
reaches_stability_zone
stability_confidence
stability_notes
```

Structural Explorer layer direction:

- show wells colored by `reaches_stability_zone`;
- overlay hydrate assessment units;
- show permafrost-base contours/control points where available;
- show geothermal-gradient or temperature-control confidence;
- include a low/mid/high scenario toggle;
- label every result as "stability admissibility, not hydrate proof."

Public sources to prioritize:

- Alaska DNR Well Bottom Hole Location dataset for well location and depth
  fields;
- USGS OM-222 for base of deepest ice-bearing permafrost from well logs;
- NSIDC G10015 for Arctic Slope borehole temperature profiles;
- NSIDC GGD223 for borehole/permafrost-depth context;
- USGS OFR 82-1039 and OFR 82-535 for North Slope permafrost and thermal
  context;
- USGS SIR 2008-5175 for North Slope gas hydrate prospect/stability method;
- USGS 2019 Gas Hydrate Assessment Unit boundaries and input forms for regional
  hydrate assessment context.

Download/upload inventory:

- The laptop source bundle prepared on 2026-06-13 is documented in
  `docs/source_library_index/stability_source_bundle_2026_06_13.md`.
- Local laptop zip to upload into OpenScienceLab:
  `C:\Users\gargi\Downloads\north_slope_stability_sources_2026-06-13_UPLOAD_TO_OPENSCIENCE.zip`.
- Recommended OpenScienceLab extraction path:
  `data/source_library/north_slope_stability_sources_2026-06-13/`.
- Keep raw downloaded source files out of Git. Commit source maps, parsers,
  setup instructions, and public-safe derived indexes only.
- NSIDC GGD223 is no longer missing locally. Its raw FTP folder was downloaded
  into the bundle with `305` files. Use `stnlist.dat` for point permafrost-depth
  control (`pf_depth` in meters), while the Alaska DNR shapefile remains the
  main well inventory.

Current OpenScienceLab-to-website workflow:

- Treat OpenScienceLab as the heavy-data workbench. Use it for the full
  stability source bundle, raw PDFs, shapefiles, NSIDC temperature profiles,
  GeoPandas parsing, and any future approved/runtime data processing.
- Treat GitHub/Streamlit as the public delivery surface. Push only finished
  public-safe products: compact CSV/GeoJSON layers, stability-screen output
  tables, exported figures, source/provenance notes, tests, and app code.
- Do not spend project time depending on OpenScienceLab external/proxy URLs for
  final presentation access. Those links can fail by environment. Instead,
  build in OpenScienceLab, commit/push the derived public outputs, and let the
  hosted or local website render from those committed outputs.
- Current public fallback product:
  `data/public_stability_snapshot/north_slope_stability_snapshot_2026-06-13/`.
  It contains parsed GGD223 permafrost-depth controls and USGS
  `GasHydrateAUs.geojson`, so the website can show real map context even when
  the full local bundle is absent.
- Current full-bundle path remains
  `data/source_library/north_slope_stability_sources_2026-06-13/`, which is
  ignored by Git and should stay local to OpenScienceLab or the laptop.

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

1. Review the header screenshots, equation screenshots, DOE project overview
   screenshots, citation packet, and source-library index.
2. Create a high-level Word-ready parameter science section: what each
   screenshot parameter measures, why it matters for gas hydrate, and what
   external factors can mimic or distort the signal.
3. Then create `docs/PARAMETER_LOGIC_AND_SOURCE_MATRIX.md` as the detailed
   working table behind the Word/slides/website.
4. Use that logic to rewrite the Word document.
5. Use the revised Word logic to revise the 9-slide Gmail deck.
6. Use the revised Word/slide logic to update the website skeleton.

## Questions For User

Remaining questions before the next major build.

1. After the parameter logic/source matrix is built, do `Sgh`, `S_h`, `Sh`, and
   `NMR_SAT` behave as equivalent hydrate-saturation labels, or are some of
   them refined/interpreted/calibrated versions?
2. After the parameter logic/source matrix is built, what should "sweet spot"
   mean for this project: occurrence + saturation only, or occurrence +
   saturation + confidence + producibility?
3. Should each parameter's outside factors/false positives become a separate
   required row in the Word document and slide logic, or stay in the source
   matrix only?

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
- Dataset naming: not important right now because we only have headers, not the
  datasets. Do not foreground dataset names.
- Occurrence and saturation: yes, the DOE overview explicitly specifies both.
- Sweet spot: wait to define fully until the parameter logic and external-factor
  reasoning are built.
