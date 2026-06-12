# Nine-Slide PowerPoint Revision Workflow

Last updated: 2026-06-12

## Purpose

Rebuild the current Drive-reviewed PowerPoint into a crisp nine-slide deck while
preserving the newer visuals the user liked. The final pass restores the older
topic sequence and folds the detailed parameter, equation, ML workflow, and
error-review material into those nine topics.

## User Corrections To Implement

1. The final deck must contain exactly nine slides.
2. The first slide must restore the user's profile photo from the earlier
   PowerPoint source.
3. Slide 4 must correctly define each parameter using project sources. The
   language must distinguish:
   - what the parameter measures;
   - why it helps identify or quantify hydrate;
   - what geologic, borehole, fluid, or processing conditions can mask or mimic
     a hydrate response;
   - how the parameter enters the ML workflow.
4. Do not describe a parameter itself as the mask. For example, deep
   resistivity is not a mask; gas, ice, carbonate/cement, shale correction,
   low-porosity rock, water-resistivity assumptions, and bad-hole response are
   caveats or masking conditions for interpreting deep resistivity as hydrate
   evidence.
5. The parameter slide must fit on one slide and use icons or compact
   process-sketch visuals for every parameter family.
6. The ML architecture must visually show equations and define each variable by
   name, not just list abbreviations.
7. The detailed ML decision map must explain the actual ML workflow:
   preprocessing, train/validation/test splits by complete well, baseline
   models, tree or boosting models, ANN/Keras saturation testing, parallel
   classification and regression heads, error analysis, uncertainty, and
   target-leakage prevention.
8. The format must be cleaner than the previous revamp: stronger hierarchy,
   fewer draft-like boxes, consistent spacing, and source captions that are
   short enough to read.

## Source Basis

Use only public-safe and repository-tracked sources:

- `docs/WELL_LOG_REQUIREMENTS_MAP.md` for headers, roles, units, and target
  leakage rules.
- `docs/project_blueprints/Alaska_North_Slope_Wireline_ML_Classification_Methods_Draft.docx`
  for staged classification, model-ladder, well/compartment validation,
  probability/reason-code outputs, expert-review labels, and results/discussion
  framing.
- `docs/project_blueprints/ml_parameter_effect_tree.csv` for the parameter
  families, planning weights, hydrate response, caveats, source basis, and model
  role.
- `docs/source_library_index/source_index.md` and
  `docs/SWEET_SPOT_SOURCE_MATRIX.md` for source provenance.
- `dashboard/runtime/feature_engineering.py` and `dashboard/runtime/schemas.py`
  for the currently implemented feature equations, target contract, and
  Chong-style ML feature list.
- Chong et al. (2022) as the direct ML saturation paper anchor.
- `references/ml-sources/2026-06-11/` for the recovered Gmail ML sources:
  Chong et al. (2022) PDF and the user-supplied general ML methodology notes.
- `docs/project_blueprints/Alaska_North_Slope_Wireline_ML_Research_Paper_Draft.docx`
  as broader source synthesis and research framing.
- Lee and Collett (2011) and Haines et al. (2022) as North Slope log-based
  saturation and multi-log interpretation anchors.
- Local equation/range documents indexed in source group
  `04_wireline_equations_ranges`.

No real approved well-log rows, core rows, named restricted identifiers, trained
models, or populated runtime outputs may be used.

## Nine-Slide Target Sequence

| Slide | Title | Required content |
|---|---|---|
| 1 | Gas Hydrate Occurrence and Saturation Prediction | Minimal title, project framing, restored profile photo, and public-safe boundary note |
| 2 | Introduction: What and Why Gas Hydrates | Explain hydrate, North Slope value, characterization goal, and why occurrence, saturation, reservoir quality, gas charge, migration, and production are separate questions |
| 3 | Parameters: Well-Log Scaffold | One-slide packed parameter scaffold with icons/process sketches, measured property, caveats or masking conditions, and ML role |
| 4 | ML Methodology: Architecture | Visual pipeline connecting approved logs, QC gates, equations, feature table, complete-well split policy, model ladder, classification, saturation regression, uncertainty, leakage barrier, and prediction output |
| 5 | ML Methodology: Why These Parameters | One-slide parameter rationale table linking equation/feature, physical reason, caveat or error, and ML use; includes why baselines, trees/boosting, and ANN/Keras are used |
| 6 | Geomechanical Feature Sketch | Rock-physics feature equations and caveats showing why high resistivity or high velocity is evidence to review, not a hydrate label by itself |
| 7 | 3D Map and Well Context | Public structural/well context, boundary between public map context and runtime-only approved well evidence, and how map context connects to ML review |
| 8 | Results and Discussion Plan | Expected figures, outputs, discussion points, and review flags while keeping current figures public/synthetic placeholders |
| 9 | Conclusion | Scientific value, ML value, energy value, final message, and next work for workbook formulas, labels, approved-data validation, and runtime figures |

## Parameter Wording Rules

Every parameter family should use the same compact grammar:

```text
Measures: physical/tool property.
Hydrate use: expected hydrate-supportive response when the surrounding evidence agrees.
Caveats: non-hydrate conditions or processing issues that can mimic, hide, or distort that response.
ML role: input, derived feature, QC gate, calibration/label, or context variable.
```

Avoid vague labels such as `mask: Deep resistivity`. Use `Caveats:` or
`Can be mimicked by:` followed by specific geologic, fluid, tool, or processing
conditions.

## Visual Quality Checklist

- Exactly nine slides.
- Slide 1 contains the earlier user profile photo.
- Slide 3 contains all parameter families on one slide.
- Parameter icons are actual small drawings or process sketches, not empty
  placeholder letters.
- Equations show both symbols and variable names.
- ML-specific slide explains why the model families are used and what errors
  are expected.
- All source notes remain public-safe and concise.
- No slide uses approved-runtime data, real well rows, trained-model metrics, or
  sensitive identifiers.
- Run the local test suite after the rebuild.
- Verify the final PPTX locally before importing or replacing any Drive copy.

## Completion Record

Completed on 2026-06-11:

- regenerated `docs/project_blueprints/North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview.pptx`
  as a 9-slide deck;
- restored the slide 1 profile photo from the earlier Google Slides deck;
- restored the older nine-slide topic sequence while keeping exactly 9 slides;
- rebuilt the parameter logic as one-slide scaffold/rationale surfaces with
  measurement, hydrate signal, caveat, and ML-role language;
- added named equations for Vshale, density porosity, Vp, Vs, Vp/Vs,
  acoustic impedance, elastic moduli, NMR-density separation, and the
  Archie-style screening proxy within the ML architecture and parameter
  rationale slides;
- incorporated the Classification Methods Draft into slides 4, 5, and 8 with
  six interpretation gates, well/compartment validation, model-ladder rationale,
  probability calibration, reason-code outputs, and expert-review flags;
- imported the final native Google Slides deck as
  `FINAL CLASSIFICATION-METHODS ML VISUAL REVISION North Slope Gas Hydrate
  Slides 2026-06-11`;
- verified the local PPTX structure, connector readback, high-risk thumbnails,
  Drive metadata, and project tests.

Additional local enrichment on 2026-06-11:

- recovered the latest Gmail ML sources into `references/ml-sources/2026-06-11/`;
- kept the slide count fixed at nine slides;
- strengthened slide 3 with explicit measured-property, hydrate-use, caveat,
  and ML-role language for every parameter family;
- strengthened slides 4, 5, and 8 with the Chong et al. ANN workflow specifics,
  Keras/feature-combination context, train-only preprocessing, data-quality
  checks, complete-well validation, metrics, calibration, residual, drift, and
  review-flag language;
- regenerated the local PPTX only; no Drive import was performed in this pass.

All-slide visual execution on 2026-06-11:

- executed the visual-revision package in
  `references/presentation-revision-2026-06-11/` across all nine slides;
- added about-me activity icons, the current Streamlit structural explorer,
  public gas-hydrate/log visuals, reusable parameter symbol chips, behavior
  panels, a geomechanical sketch, results visuals, and conclusion graphics;
- corrected slide 4 into a clearer architecture with a separate QC-gate lane
  and visible connections into equations, feature table, split policy, model
  ladder, outputs, and target-leakage barrier;
- imported the corrected PPTX as native Google Slides named `FINAL VISUAL
  REVISION 9-SLIDE North Slope Gas Hydrate Slides 2026-06-11`;
- verified the local PPTX has exactly nine slides, no out-of-bounds elements,
  and a valid PPTX archive, then verified Drive metadata/readback and
  Google-rendered thumbnails for all nine slides.

Latest Gmail visual-feedback execution on 2026-06-12:

- recovered the user's newest Gmail instructions and inline visual references
  for all nine slides;
- generated nine source-backed Processing-style raster panels with the provided
  drawing/music/World Cup references, DOE visual reference, USGS/NETL hydrate
  sources, current Streamlit structural explorer, 2D North Slope map context,
  shared-gate ML architecture, behavior panels, geomechanical equations, result
  flow, and conclusion graphic;
- rebuilt `docs/project_blueprints/North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview.pptx`
  through `docs/project_blueprints/build_ml_revamp_powerpoint.py`;
- imported the corrected PPTX as native Google Slides named `GMAIL VISUAL
  REVISION 9-SLIDE North Slope Gas Hydrate Slides 2026-06-11`;
- verified Drive metadata, connector readback, all nine large
  Google-rendered thumbnails, and the 23-test project suite;
- noted that the current Drive deck preserves the visual revisions as
  full-slide raster panels, so a later pass would be needed if each text/icon
  element must be separately editable in Google Slides.
