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

Current slide authority:

- `docs/project_blueprints/CURRENT_GMAIL_VISUAL_REVISION_9_SLIDE_North_Slope_Gas_Hydrate_Slides_2026-06-11.pptx`
  - Current slide starting point, per user clarification on 2026-06-12.
  - Copied from the Gmail-sourced local deck:
    `C:\Users\gargi\Downloads\GMAIL VISUAL REVISION 9-SLIDE North Slope Gas Hydrate Slides 2026-06-11.pptx`.
  - Email source: Gmail message `19eba86da8752830`, subject `New pressy`, sent
    2026-06-12 01:30 CDT.
  - Verified as a valid 9-slide PPTX.

Prior tracked slide deliverable:

- `docs/project_blueprints/North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview.pptx`
  - Older tracked PowerPoint deliverable path.
  - The live working Drive deck has been repeatedly imported as native Google
    Slides during the June 2026 revision passes.

Tracked slide builders and safe public assets:

- `docs/project_blueprints/build_ml_revamp_powerpoint.py`
- `docs/project_blueprints/build_processing_slide_assets.py`
- `docs/project_blueprints/presentation_assets/processing_revisions_2026_06_11/`
  - Public-safe generated panels for slides 2-9 are tracked.
  - Slide 1 generated/about-me panels that contain personal visual material are
    ignored.
- `references/presentation-revision-2026-06-11/`
  - Source manifest, icon registry, USGS/public images, slide 2 plan, and
    detailed revision prompt.

Local-only slide assets intentionally ignored:

- `docs/project_blueprints/presentation_assets/rohan_profile_photo.jpg`
- `references/presentation-revision-2026-06-11/gmail-2026-06-11/`
- `references/presentation-revision-2026-06-11/drive-thumbnails-2026-06-12/`

Slide status:

- The Gmail visual revision deck is now tracked and should be opened first for
  slide review.
- The prior deck and script-generated panels remain useful as provenance and
  rebuild tools, but they are not the latest user-approved slide starting point.
- The next slide pass should follow
  `docs/PROJECT_DIRECTION_LOCK_FOR_REVIEW.md` and
  `docs/deliverable_revision_base_2026_06_12/`.

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

1. Review and revise `docs/PROJECT_DIRECTION_LOCK_FOR_REVIEW.md`.
2. Update the Word document first using the direction file and revision base.
3. Rebuild the nine-slide deck second using the Word/source plan.
4. Update the website/app skeleton only where it supports the accepted
   Word/PPT workflow.
5. Decide whether personal slide-1 visuals stay Drive/local only or can be
   tracked in Git.

