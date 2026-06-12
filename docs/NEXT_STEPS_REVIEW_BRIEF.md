# North Slope Next Steps Review Brief

Created: 2026-06-12

Purpose: one working document that consolidates the current project direction, the user's saved review comments, the slide/doc/website work order, and the questions that need answers before changing the Word document, slides, or website.

## Current Source Of Truth

Repository:

- `C:\Users\gargi\OneDrive\Documents\ai north slope gas hydrates`
- GitHub repo: `Rnanda442/north-slope-gas-hydrates`

Current slide authority:

- `docs/project_blueprints/CURRENT_GMAIL_VISUAL_REVISION_9_SLIDE_North_Slope_Gas_Hydrate_Slides_2026-06-11.pptx`
- This is the Gmail visual deck and should be opened first for slide review.
- The deck must stay at exactly 9 slides unless the user explicitly changes that.
- Slide 1 is considered ready enough as the about-me/title slide. Slides 2-9 need stronger science, source grounding, parameter logic, format, syntax, and visual clarity.

Current Word authority:

- `docs/project_blueprints/North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview.docx`
- Word should lead the next pass because it locks the science, source logic, parameter meaning, method sequence, and validation language.

Current website authority:

- `streamlit_app.py`
- `dashboard/app.py`
- The website is secondary for now. It is a skeleton and transfer structure for later DOE/authorized environment work, not the main deliverable.

## User Clarifications To Preserve

- Main goal: slides and Word document first.
- Website role: a skeleton/middle layer that can eventually be brought into the DOE virtual desktop or Anaconda environment and connected to real approved data there.
- Public repo must not include actual classified or approved well-log/core rows.
- The current screenshots are acceptable because they show headers, equations, project overview, and data shape without exposing the full data.
- The user currently has access to only 3 of 71 datasets, so final well lists, validation splits, and model metrics cannot be completed yet.
- The project should first build quantitative parameter logic: ranges, changes, physical reasoning, false positives, and how gas hydrate constraints relate to each variable.
- `Sgh`, `S_h`, `Sh`, `NMR_SAT`, and hydrate saturation fields exist in the data context, but the exact authoritative target and target/feature rules still need to be clarified.
- The ML paper by Chong et al. (2022) is essential for the diagrams, visual pipeline, ANN/Keras explanation, and hydrate saturation workflow.
- Singh et al. (2021) and Chong et al. (2024) are useful comparative ML/method sources.
- Synthetic/fake data is acceptable for testing app skeletons if it uses duplicate header formats and reasonable scientific ranges.
- Real results and real metrics will be created later inside the approved environment by the user.

## What The Website Should Become

The website should not try to be the final scientific proof yet. It should be a public-safe scaffold that contains:

- public regional GIS context;
- skeleton pages for future approved data intake;
- schema and curve-alias mapping;
- synthetic/fake datasets with the same header structure as the real Excel sheets;
- parameter range and behavior explanations;
- equations and feature engineering diagrams;
- QC and leakage-barrier explanations;
- placeholder output layouts for occurrence, saturation, uncertainty, and sweet-spot review;
- exports and plots that can later be run on approved data inside DOE/anaconda.

Plain-language definition of runtime:

- "Runtime" means the local environment where the code is actually pointed at real files and executed.
- For this project, the public GitHub repo can hold the code skeleton, fake data, configs, and instructions.
- The real DOE data should be loaded only later inside the DOE virtual desktop or another approved local environment.

## Scientific Work Needed Before Major Deliverable Edits

The next science pass should build the parameter logic before making big Word/PPT changes.

Needed:

- Define each input parameter in plain language.
- Define likely hydrate-supportive behavior for each parameter.
- Define false positives and outside factors for each parameter.
- Define units and expected ranges from public sources.
- Define how changes across depth matter, not just absolute values.
- Define which values are measured, derived, QC-only, contextual, or label/ground truth.
- Tie equations to features and visual diagrams.
- Tie each parameter to sources.

Priority parameters from screenshots:

- `DEPTH` / `Depth_ft`
- `Rho_b` / `RHOB` / `Density_gpcc`
- `Phi_porosity` / `phi_den` / `DPHI`
- `NMRPHI` / `phi_nmr`
- differential caliper / `caliper` / `CAL1`
- deep formation resistivity / `Rt` / `RES` / `AO90`
- `GR`
- `Vs` / `VS1`
- `Vp` / `VELP`
- `Ratio Vp/Vs`
- impedance
- `Sgh`, `S_h`, `Sh`, `NMR_SAT`, hydrate saturation labels

## ML Work Needed Before Major Deliverable Edits

The ML section should not pretend we already trained a real model in the public repo.

Needed:

- Explain model purpose before model names.
- Explain ANN/Keras using Chong et al. (2022): a neural network learns relationships among well-log features to estimate hydrate saturation.
- Explain why the model must be tested on unseen wells or held-out groups.
- Explain target leakage in plain language: do not let the answer column leak into the inputs used to predict that answer.
- Explain why synthetic data may be used only for skeleton testing, not for scientific claims.
- Explain that real model metrics come later in the approved environment.

Suggested wording:

> The public version builds the model pipeline and visual logic. The approved-data version will later run the real training, validation, and metrics inside the DOE environment.

## Work Order

1. Resolve the questions below.
2. Build the parameter logic table/source matrix.
3. Update the Word document from that table.
4. Update the 9-slide Gmail deck from the Word/source plan.
5. Update the website skeleton so it mirrors the approved Word/PPT logic.
6. Use focused commits:
   - source/parameter logic commit;
   - Word update commit;
   - slide update commit;
   - website skeleton update commit.

## Questions For User

1. For the real datasets, is `Sgh`, `S_h`, `Sh`, or `NMR_SAT` the main hydrate saturation target, or are these different versions from different tabs/sources?
2. Should the fake/synthetic test datasets use exactly the screenshot headers, even if the internal code maps them to cleaner names like `depth_m`, `rhob_g_cc`, and `rt_ohm_m`?
3. Do you want the next pass to make a parameter logic table first, before touching the Word/PPT?
4. For the website, should the fake-data testing be built around 3 synthetic datasets to mirror the 3 real datasets you currently have access to, or around a larger fake set representing the future 71 datasets?
5. Are the three current real datasets from different wells, different tabs, or different processed versions of the same well/log family?
6. Should slide 1 remain untouched unless there is a formatting issue?
7. When we say "sweet spot," should it mean best hydrate saturation, best producibility, best confidence, or a combined review rank?
8. Are the project overview screenshots the official wording for the Word abstract/introduction, or should they be treated as source notes that we rewrite into a cleaner DOE style?

## Immediate Next Action

Recommended next step: answer questions 1, 2, 3, 4, and 7 first. Those decide the scaffold shape.

After that, build `docs/PARAMETER_LOGIC_AND_SOURCE_MATRIX.md` as the main source-backed table for the Word, slides, and website.

