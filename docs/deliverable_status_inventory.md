# Deliverable Status Inventory

Updated: 2026-06-12

This inventory summarizes what is currently built in the North Slope repo and what is still outside the repo in local email/download sources.

## Website / Streamlit App

Primary entrypoint:

- `streamlit_app.py` imports and runs `dashboard.app.main`.

Current app pages in `dashboard/app.py`:

- `Welcome`: public-data boundary, project purpose, and atlas entry points.
- `Regional Atlas`: public assessment units, seismic coverage, and public well inventory.
- `Structural Explorer`: Plotly-style 3D structural surface viewer with selectable horizons and public well overlays.
- `Data Library`: curated layer metadata and repository inventory.
- `Research Framework`: manuscript-backed interpretation chain and decision rules.
- `Future Well-Log Engine`: synthetic planning scaffold for future approved runtime well-log analysis.

Current app capabilities:

- Direct atlas page routes through query parameters.
- Public GIS layer browsing.
- Synthetic well-log examples only; no approved or restricted data in Git.
- Variable range explorer.
- Interpretation guidance and error/caveat bands.
- Staged interval screening.
- Core-to-log calibration placeholder.
- Presentation-style synthetic exports: HTML well-log panel, cross-well comparison, CSV tables.

## Runtime / Well-Log Scaffold

Runtime package:

- `dashboard/runtime/schemas.py`
- `dashboard/runtime/loaders.py`
- `dashboard/runtime/validation.py`
- `dashboard/runtime/feature_engineering.py`
- `dashboard/runtime/core_calibration.py`
- `dashboard/runtime/modeling.py`
- `dashboard/runtime/plotting.py`
- `dashboard/runtime/exports.py`

Runtime rules already implemented:

- Approved data belongs in ignored local folders such as `data_runtime/`, `outputs_runtime/`, `models_runtime/`, `logs_runtime/`, and `configs_local/`.
- Public app stays synthetic unless running inside an authorized local environment.
- CSV loader and curve-alias standardization exist.
- LAS loading is a placeholder for local approved-runtime work.
- Validation checks required columns, empty tables, well aliases, depth order, duplicate depths, numeric ranges, and missingness.
- Feature engineering includes standard rock-physics transforms from available logs.
- Rule-based labels exist as a placeholder before approved ML models.

Current schema gap from the June 12 screenshot email:

- Existing runtime aliases cover `depth`, `GR`, `Rt`, `RHOB`, `DT`, `DTS`, `NMRPHI`, caliper, pressure, and temperature.
- The new Excel screenshots also show explicit `Vp`, `Vs`, `Ratio Vp/Vs`, `Impedance`, `Sgh`, `S_h`, `Sh`, and `NMR_SAT`.
- Next scaffold pass should add these as explicit measured/derived/label groups while keeping `Sgh`, `S_h`, `Sh`, and `NMR_SAT` locked out of predictors.

## Word Documents

Tracked Word drafts:

- `docs/project_blueprints/Alaska_North_Slope_Wireline_ML_Research_Paper_Draft.docx`
  - Broader research-paper scaffold built from the manuscript, organized source library, and public-source atlas.
  - Includes conceptual model, source base, research framing, and manuscript-style discussion.
- `docs/project_blueprints/Alaska_North_Slope_Wireline_ML_Classification_Methods_Draft.docx`
  - Sharper DOE-style methods draft.
  - Focuses on measured variables, derived equations, staged classification, ML design, expected outputs, and discussion structure.
  - This is the current working direction for the well-log project.

Supporting docs:

- `docs/project_blueprints/README.md`
- `docs/runtime_skeleton_brief.md`
- `docs/project_inventory.md`
- `docs/data_dictionary.md`
- `docs/source_library_index/source_index.md`
- `docs/source_library_index/source_manifest.csv`

## Slides

No North Slope PPTX slide deck is currently tracked in this repository.

Local slide sources found in `C:\Users\gargi\Downloads`:

- `GMAIL VISUAL REVISION 9-SLIDE North Slope Gas Hydrate Slides 2026-06-11.pptx`
- `FINAL CLASSIFICATION-METHODS ML VISUAL REVISION North Slope Gas Hydrate Slides 2026-06-11.pptx`
- `REVAMPED June 10 North Slope Gas Hydrate ML Parameter Architecture Slides.pptx`
- `UPDATED North Slope Gas Hydrate Reservoir Characterization Research Overview Slides.pptx`

Email source:

- Gmail message `19eba86da8752830`, subject `New pressy`, includes `GMAIL VISUAL REVISION 9-SLIDE North Slope Gas Hydrate Slides 2026-06-11.pptx`.

Slide status:

- The deck exists locally/email-side.
- It has not yet been copied into this Git repo.
- If a PPTX deliverable needs to live in Git, decide whether to track the final small deck or keep the full deck in Drive/email and track only exported screenshots/source manifests.

## Source Evidence And Screenshots

New screenshot evidence folder:

- `docs/evidence/email_screenshots_2026_06_12/`

Key contents:

- Excel header screenshots for incoming data contract.
- Raw Excel table screenshots showing MTE, IGS, MTE_refined, and IGS_refined tabs.
- Geomechanical equations screenshot.
- Project goal and objective screenshots.
- Contact sheet for quick review.

Primary ML/source files kept locally:

- `C:\Users\gargi\Downloads\s10596-022-10151-9.pdf`
- `C:\Users\gargi\Downloads\ML_Project_Reference_and_CreditScoreV4_Case_Notes.docx`
- `C:\Users\gargi\Downloads\Alaska_North_Slope_Wireline_ML_Project_Blueprint_outline.docx`
- `C:\Users\gargi\Downloads\UPDATED North Slope Gas Hydrate Reservoir Characterization Research Overview.docx`

Tracked source-library index:

- `docs/source_library_index/source_index.md`
- `docs/source_library_index/source_manifest.csv`

## Next Work Order

1. Goal and vision section: use the project-goal screenshots plus the research/classification drafts.
2. Well-log scaffold: update schema and app explanation around the Excel header screenshots.
3. Equation scaffold: add geomechanical equations and explain each as a derived feature.
4. ML source integration: tie Chong et al. 2022 and the ML reliability notes to model ladder, validation, leakage prevention, and Keras/ANN explanation.
5. Slide/doc alignment: decide whether the local PPTX deck should be tracked, exported, or referenced through a manifest only.

