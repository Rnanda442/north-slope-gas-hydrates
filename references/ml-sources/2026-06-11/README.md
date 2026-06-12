# June 11, 2026 ML Source Intake

## Source

Gmail message: `ML sources`

Sender: project owner Gmail account

Message timestamp: 2026-06-11 14:29:20 America/Chicago

## Files

| File | Classification | Use in this project |
|---|---|---|
| `s10596-022-10151-9.pdf` | Public peer-reviewed source | Gas-hydrate ANN/well-log workflow anchor: Chong et al. (2022), five permafrost-associated wells, NMR-density Sgh target, density/porosity/GR/resistivity/Vp/Vs features, caliper washout and outlier screening, min-max normalization, hyperparameter tuning, and model validation. |
| `ML_Project_Reference_and_CreditScoreV4_Case_Notes.docx` | User-supplied public-safe general ML methodology note | General ML workflow controls: baseline-first model selection, leakage-safe preprocessing, train-only transforms, validation scheme matching production use, data-quality checks, drift triage, calibration, and monitoring language. |

## Boundary

These files are used only as public/reference methodology sources. They do not
contain approved North Slope runtime well-log rows, core rows, trained models,
restricted identifiers, populated runtime configurations, credentials, or
derived sensitive outputs.

## Deliverable Use

- PowerPoint: enrich the fixed 9-slide ML deck without changing slide count,
  especially the parameter, architecture, parameter-rationale, and
  results/discussion slides.
- Word document: preserve the current outline while adding the specific ML
  pipeline expected for approved North Slope data.
- Documentation: record the intake and source role in the project activity map
  and relevant deliverable notes.

## Unresolved

- The full Excel workbook and authoritative target fields are still missing.
- The exact known-well labels, saturation target provenance, phase classes, and
  prediction-well blind-evaluation plan still need to be confirmed before real
  model training.
