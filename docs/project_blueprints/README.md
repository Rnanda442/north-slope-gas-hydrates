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
  - Research-paper-style overview reintegrated on 2026-06-10 from the updated
    Gmail-sent DOE copy.
  - Frames gas hydrates as an energy-resource characterization and energy-security
    project, with the current public scaffold clearly marked as header-derived
    synthetic records from three Excel header/schema references.
  - Current version fills the abstract and introduction, then expands Parameters,
    Methodology, Machine-Learning Framework, Error and Validation, and Discussion
    with the same parameter signal, masking, target-leakage, normalization,
    complete-well validation, and overburden-context logic used in the rebuilt
    ML architecture deck. The 2026-06-11 local refresh also adds the recovered
    ML-source specifics: Chong et al.'s five-well ANN saturation workflow,
    approved-data feature-table controls, train-only preprocessing, model
    ladder, calibration, residual review, and data-quality/drift checks.
    Results-bearing claims remain placeholders until approved-data execution.
  - Imported to the connected Google Drive account on 2026-06-11 as
    [ENRICHED ML PIPELINE North Slope Gas Hydrate Research Overview 2026-06-11](https://docs.google.com/document/d/1V3kZuu4euP6IhHwfnwscAh7RxDAqWMNu2tEf7wC_pW4).
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
  - Imported to the connected Google Drive account on 2026-06-11 as
    [ENRICHED 9-SLIDE ML PIPELINE North Slope Gas Hydrate Slides 2026-06-11](https://docs.google.com/presentation/d/1jazq9ZLc6G9DlM2n6QZq9rKsjDcBuw-3KrTZb4-kzJ0).
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

## Direction

Use the classification-methods draft as the working direction for the DOE-style
well-log project. Use the broader research-paper draft as background context and
source synthesis.

## Boundary

These are public-source planning artifacts only. Do not add classified,
restricted, credentialed, approved-environment-only well logs, populated result
figures, or derived sensitive outputs to this repository.
