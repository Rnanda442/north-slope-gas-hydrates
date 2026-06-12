# ML Citation Packet For Deliverables

Created: 2026-06-12

## Purpose

This packet makes the ML citation layer ready for the next Word document and
nine-slide deck pass. It records the exact sources, the specific claims each
source can support, and the guardrails that prevent comparative ML papers from
being overused as North Slope field evidence.

Use this file with:

- `docs/PROJECT_DIRECTION_LOCK_FOR_REVIEW.md`
- `docs/ML_SOURCE_COVERAGE_AND_DELIVERABLE_REVISION_PLAN.md`
- `docs/deliverable_revision_base_2026_06_12/`
- `references/ml-sources/2026-06-11/`

## Source Hierarchy

| Tier | Sources | Use |
|---|---|---|
| Direct permafrost gas-hydrate ML | Chong et al. (2022) | Main ML analogue for Alaska North Slope and Mackenzie Delta well-log saturation prediction |
| Comparative gas-hydrate ML | Singh et al. (2021); Chong et al. (2024) | Method support for feature choices, model ladder, ANN/regression framing, and occurrence plus saturation prediction |
| General ML controls | `ML_Project_Reference_and_CreditScoreV4_Case_Notes.docx` | Leakage-safe preprocessing, validation, calibration, monitoring, and baseline-first language |
| North Slope hydrate science | Source matrix and USGS/DOE/NETL sources | Field truth, reservoir context, hydrate occurrence, log response, stability, and resource framing |

## Ready-To-Cite ML Sources

### Chong et al. (2022)

Working citation:

Chong, L., Singh, H., Creason, C.G., Seol, Y., and Myshakin, E.M., 2022,
Application of machine learning to characterize gas hydrate reservoirs in
Mackenzie Delta (Canada) and on the Alaska North Slope (USA): Computational
Geosciences, https://doi.org/10.1007/s10596-022-10151-9.

Local file:

- `references/ml-sources/2026-06-11/s10596-022-10151-9.pdf`

Use in this project:

- Main direct ML anchor for permafrost-associated gas hydrate reservoirs.
- Supports use of ANN-style models to predict gas hydrate saturation from
  well-log combinations.
- Supports a feature family built from density, porosity, electrical
  resistivity, natural gamma radiation, and acoustic-wave velocity.
- Supports NMR-derived or NMR-density-derived saturation as a target or
  calibration reference when available.
- Supports the idea that useful ML models can be trained and tested across ANS
  and Mackenzie Delta wells, but only as an analogue for this project until the
  approved North Slope data and validation splits are known.

Allowed Word language:

Chong et al. (2022) is the strongest direct analogue for this project because it
uses permafrost-associated gas hydrate well logs from Alaska North Slope and
Mackenzie Delta settings to evaluate machine-learning prediction of hydrate
saturation. The paper supports a workflow where measured logs and derived
feature combinations are connected to an independently defined saturation
reference rather than allowing target-derived columns to leak into predictors.

Allowed slide language:

- Direct ML anchor: ANS + Mackenzie Delta.
- ANN saturation workflow from well-log combinations.
- Keep `S_h` / `Sgh` as target or calibration reference, not predictor.

Guardrail:

Do not copy reported accuracy values as this project's result. Treat the paper
as workflow evidence until approved project data, target fields, and complete
well splits are confirmed.

### Singh et al. (2021)

Working citation:

Singh, H., Seol, Y., and Myshakin, E.M., 2021, Prediction of gas hydrate
saturation using machine learning and optimal set of well-logs: Computational
Geosciences, v. 25, p. 267-283, https://doi.org/10.1007/s10596-020-10004-3.

Primary source pages:

- DOE OSTI / DOE PAGES record:
  `https://www.osti.gov/pages/biblio/1893637`
- Springer record:
  `https://link.springer.com/article/10.1007/s10596-020-10004-3`

Use in this project:

- Comparative ML method support for predicting hydrate saturation from a small,
  optimal well-log set.
- Supports the need to compare ML saturation prediction against physics-driven
  resistivity/acoustic approaches and to acknowledge limitations of each.
- Supports model-family language around neural networks and stochastic gradient
  descent regression.
- Supports feature logic around porosity, bulk density, and compressional-wave
  velocity as useful non-NMR inputs.
- Supports the importance of NMR-density saturation references where available.

Allowed Word language:

Singh et al. (2021) supports the project's model-ladder rationale by showing
that hydrate saturation can be predicted from selected routine well logs using
machine-learning methods, while also explaining why common resistivity and
acoustic approaches can require assumptions or calibration that should not be
hidden from the workflow.

Allowed slide language:

- Comparative ML: optimal well-log set for `S_h`.
- Useful non-NMR features: porosity, bulk density, `V_p`.
- Supports model comparison, not project results.

Guardrail:

This paper supports method design and feature selection. It should not be used
as North Slope interval evidence or as a substitute for this project's approved
validation.

### Chong et al. (2024)

Working citation:

Chong, L., Collett, T., Creason, C.G., Seol, Y., and Myshakin, E., 2024,
Machine learning application to assess occurrence and saturations of methane
hydrate in marine deposits offshore India: Interpretation, v. 12, p. T63-T75,
https://doi.org/10.1190/int-2023-0056.1.

Primary source page:

- USGS Publications Warehouse:
  `https://pubs.usgs.gov/publication/70250169`

Use in this project:

- Comparative ML source for predicting both hydrate occurrence and hydrate
  saturation.
- Supports the idea that occurrence classification and saturation regression are
  separate outputs.
- Supports use of ANN models with logs including density, porosity,
  resistivity, gamma radiation, and acoustic velocity.
- Supports balanced-accuracy language for occurrence classification.
- Supports a slide-4 architecture with parallel occurrence and saturation heads.

Allowed Word language:

Chong et al. (2024) is useful as a comparative marine hydrate ML example because
it separates occurrence classification from saturation prediction and evaluates
well-log combinations against reference data. In this North Slope project, it
should support architecture design rather than replace permafrost-specific or
North Slope calibration evidence.

Allowed slide language:

- Comparative ML: occurrence plus saturation.
- ANN with density, porosity, resistivity, gamma, acoustic velocity.
- Supports separate classification and regression branches.

Guardrail:

This is an offshore India marine-hydrate source. It should not be used to claim
North Slope reservoir behavior, North Slope model performance, or validated
project accuracy.

## How To Use These Sources In The Word Document

Add a short ML literature paragraph in the Methodology or ML Framework section:

Chong et al. (2022) should be introduced first as the direct permafrost
gas-hydrate ML analogue because it includes Alaska North Slope and Mackenzie
Delta well-log settings. Singh et al. (2021) should then be used to justify a
small, defensible feature-set and baseline/advanced model comparison for
saturation prediction. Chong et al. (2024) should be used to justify separating
hydrate occurrence classification from hydrate saturation prediction. Together,
these sources support the planned ML architecture, but they do not replace
project-specific target mapping, leakage-safe preprocessing, and complete-well
validation.

## How To Use These Sources In The Slides

| Slide | Recommended citation use |
|---|---|
| 3 Parameters | Chong et al. (2022), Singh et al. (2021), Lee/Collett/Haines for log response |
| 4 ML Architecture | Chong et al. (2022) as direct anchor; Chong et al. (2024) for occurrence plus saturation heads |
| 5 Why Parameters | Chong et al. (2022), Singh et al. (2021), parameter effect tree, North Slope log-response sources |
| 6 Geomechanics | Feature-equation docs, sonic/log sources, Lee/Collett/Haines; Singh et al. (2021) only for `V_p`/density/porosity ML relevance |
| 8 Results Plan | Chong et al. (2024) for balanced-accuracy framing; ML notes for calibration/residual/drift review |

Short source footer options:

- `ML sources: Chong et al. 2022; Singh et al. 2021; Chong et al. 2024`
- `Direct analogue: Chong et al. 2022; comparative ML: Singh 2021, Chong 2024`
- `Targets stay locked: S_h/Sgh/NMR_SAT are labels or calibration references`

## Claims To Avoid

- Do not say this project has achieved the accuracy reported in any source.
- Do not say offshore India results validate Alaska North Slope predictions.
- Do not say high `R_t`, high `V_p`, or low `GR` proves hydrate.
- Do not say NMR-derived saturation is available for every interval until the
  approved workbook/data confirm coverage.
- Do not present `S_h`, `Sgh`, `NMR_SAT`, phase labels, or final sweet-spot
  rankings as predictors.
- Do not use random row splits as the final validation standard.

## Source-Backed ML Architecture Statement

The architecture should be described as:

```text
approved logs and core context
-> schema/unit mapping
-> depth alignment
-> QC gates
-> feature equations
-> target registry and leakage barrier
-> train-only preprocessing
-> complete-well split
-> baseline and advanced model ladder
-> separate occurrence, saturation, uncertainty, and review outputs
```

This statement is consistent with the direct permafrost ML source, the
comparative occurrence/saturation ML source, and the general ML controls, while
still preserving the public-versus-authorized data boundary.

## Citation URLs Used For Verification

- Singh et al. (2021), DOE OSTI:
  `https://www.osti.gov/pages/biblio/1893637`
- Singh et al. (2021), Springer:
  `https://link.springer.com/article/10.1007/s10596-020-10004-3`
- Chong et al. (2022), Springer:
  `https://link.springer.com/article/10.1007/s10596-022-10151-9`
- Chong et al. (2022), OSTI accepted manuscript:
  `https://www.osti.gov/servlets/purl/1888241`
- Chong et al. (2024), USGS Publications Warehouse:
  `https://pubs.usgs.gov/publication/70250169`
