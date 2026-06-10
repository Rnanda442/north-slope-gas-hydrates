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
  - Current version fills the abstract and introduction, then keeps Parameters,
    Methodology, Machine-Learning Framework, Error and Validation, Discussion,
    and Conclusion as outline sections for future approved-data results.
- `North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview.pptx`
  - Twelve-slide visual companion deck rebuilt on 2026-06-10 from the latest
    Drive PowerPoint export.
  - Current version reduces text and emphasizes parameter signal bars,
    conceptual importance weights, parameter masking/effect trees, a dark
    MLOps-style ML architecture, classification and saturation-regression
    branches, overburden-map context, and predicted sweet-spot review outputs.
  - The deck remains public-safe: it uses public sources, equation/header
    references, and conceptual/sample visuals only, not real approved well rows
    or trained model outputs.
- `build_ml_revamp_powerpoint.py`
  - Reproducible builder for the current visual-first ML parameter architecture
    PowerPoint.
  - Uses the latest Drive export as a local base when present, but can rebuild
    the tracked deck from a blank 16:9 presentation using
    `ml_parameter_effect_tree.csv`.
- `ml_parameter_effect_tree.csv`
  - Machine-readable public-safe parameter/effect/masking matrix and conceptual
    importance weighting for the rebuilt deck.
- `DOE_sent_UPDATED_North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview.docx`
  and `DOE_sent_UPDATED_North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview_Slides.pptx`
  - Source copies recovered from the user's Gmail sent message to the DOE account
    on 2026-06-10.
  - Kept as provenance inputs for the tracked integrated DOCX/PPTX above.
- `build_research_overview_deliverables.py`
  - Reproducible builder for the new Word and PowerPoint deliverables.

## Direction

Use the classification-methods draft as the working direction for the DOE-style
well-log project. Use the broader research-paper draft as background context and
source synthesis.

## Boundary

These are public-source planning artifacts only. Do not add classified,
restricted, credentialed, approved-environment-only well logs, populated result
figures, or derived sensitive outputs to this repository.
