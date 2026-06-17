# North Slope Gas Hydrate Mentor Companion Brief

Created: 2026-06-15
Updated: 2026-06-16

## Purpose

This brief explains where the project stands now for mentor review. It connects
the public website, source-backed stability screen, V5.4 workflow package, and
the first DOE three-dataset prototype without claiming final hydrate proof,
final stability, occurrence prediction, saturation prediction, or validated
model performance.

The current defensible claim is that the project has a public-safe source and
method scaffold plus an approved-runtime prototype that can audit target
leakage and feature construction. The value today is traceability and
controlled workflow design, not a final R2 value.

## Project Vision And Goal

The project goal is to build a scientifically defensible North Slope gas
hydrate workflow for future occurrence classification and saturation
regression. The workflow should follow the same logic a geoscientist would use:
first test whether methane hydrate is physically admissible, then check whether
the interval can host pore-filling hydrate, then evaluate whether well logs and
core or NMR context show a hydrate-compatible response.

The target system remains pore-filling methane hydrate in sand-rich,
permafrost-associated Alaska North Slope reservoirs. The public website and
documents explain the method. Final model execution belongs in the DOE or other
approved runtime after data access, label authority, and validation policy are
settled.

## Current Position

| Area | Current status | Mentor-ready meaning |
|---|---|---|
| Public website and GitHub | Public GIS, source cards, stability products, schema templates, diagrams, and tests are available. | The public side explains the method and provenance without exposing approved rows. |
| Source and visual provenance | `source_visual_inventory_2026-06-16.csv` tracks slide panels, website captures, source-backed images/data, allowed use, and guardrails. | Visuals now have reuse context instead of being detached illustrations. |
| Stability screen | The public methane 5 ppt screen has 8,084 scaffold rows, including 22 calculated admissibility intervals, 8 no-stable-interval rows, and 8,054 blocked rows. | This is pressure-temperature admissibility under stated assumptions only. |
| Approved data visibility | About 3 of the expected 71 approved datasets are currently visible for schema and runtime-prototype work. | Enough for pipeline structure, feature audit, and target-leakage checks; not enough for final claims. |
| DOE prototype | Three workbooks can be scanned and routed through a local runtime workflow with dataset 1 as training and datasets 2 and 3 as external/test-style inputs when targets exist. | Useful as an audit trail and plumbing proof, not validated science performance. |
| Current deliverables | V5.4 corrected slides, Word companion, website sections, source cards, and model-run tracker language are aligned around guardrails. | The mentor can review the method, boundary, current blockers, and decision requests. |

## Public Versus DOE/Approved Runtime Boundary

The project intentionally uses two workspaces.

| Workspace | Allowed content | Not allowed content |
|---|---|---|
| Public GitHub / Streamlit | Public sources, public GIS, public stability summaries, source-backed diagrams, source cards, synthetic examples, schema templates, and reviewed public-safe summaries. | Approved LAS/CSV/core rows, private workbook rows, restricted identifiers, populated runtime configs, trained models, row-level predictions, or sensitive derived outputs. |
| DOE / approved runtime | Approved well logs, workbook rows, core, NMR, label mapping, source rebuilds, training, validation, runtime outputs, and fitted model objects. | Public release without review and row-free reduction. |

The public side should be treated as a method and provenance surface. The
approved runtime is where final data handling, target mapping, and model
validation happen.

## Source-Backed Stability Screen And Guardrails

The current stability screen is a source-backed admissibility layer. It uses
public well coordinates and depth fields, GGD223 permafrost controls, G10015
temperature-profile context, a hydrostatic pressure assumption, and a digitized
USGS SIR 2008 methane hydrate phase boundary for 100 percent methane and 5 ppt
salinity.

The screen answers one limited question:

```text
Under the selected public pressure, temperature, methane, and salinity
assumptions, does the modeled depth interval intersect methane hydrate
stability conditions?
```

Allowed use:

- context feature, mask, source-control label, or reviewer reason flag;
- public explanation of why pressure-temperature logic belongs upstream of ML;
- source-backed caveat layer for later approved-runtime outputs.

Not allowed use:

- hydrate proof;
- final stability top/base/thickness;
- hydrate occurrence label;
- hydrate saturation estimate;
- sweet-spot ranking;
- no-hydrate label for blocked rows.

Blocked means the calculation refused to claim a result because a source or
calculation gate did not pass. It does not mean no hydrate.

## Three-Dataset DOE Prototype

The DOE prototype is the first approved-runtime plumbing test. It is designed
around three available workbooks:

| Dataset | Prototype role | Current use |
|---|---|---|
| `curated_dataset1.xlsx` | Training-style workbook | Used to detect target variants and train small prototype regressors when usable targets exist. |
| `curated_dataset2.xlsx` | External/test-style workbook | Scored or inventoried separately, depending on target and feature availability. |
| `curated_dataset3.xlsx` | External/test-style workbook | Scored or inventoried separately, depending on target and feature availability. |

The prototype can scan sheets, identify target-looking saturation columns,
train separate target runs for visible variants such as `S_h`, `S_wr`, `Sh`,
or `Swr`, and write row-free run summaries for the website tracker.

The important result is the audit trail:

- saturation-like columns are treated as Y-only unless proven otherwise;
- depth is treated as alignment/context rather than a default predictor;
- spreadsheet helper columns and duplicate raw aliases are excluded;
- feature families are recorded target by target;
- exclusions carry reasons rather than disappearing silently;
- validation status is separated from training-fit metrics.

Any training-fit R2 from this prototype is a runtime check only. It is not
final validated North Slope performance.

## Cleaned Feature Matrix And Leakage Prevention

The cleaned feature matrix is the main technical contribution that can be
reviewed now. It makes the future ML workflow defensible before the final model
exists.

| Control | What it does | Why it matters |
|---|---|---|
| Original header preservation | Keeps source header, unit, and role visible before normalization. | Prevents silent unit mistakes and makes workbook review possible. |
| `X_allowed` contract | Allows only measured logs, approved derived physics, QC/context flags, and non-leaking metadata. | Stops answer-like columns from entering predictors. |
| Y-only registry | Routes `S_h`, `Sgh`, `Sh`, `NMR_SAT`, `Swr`, `S_wr`, hydrate saturation, and phase labels outside predictors. | Prevents target leakage and false model skill. |
| Helper-column exclusion | Removes unnamed spreadsheet artifacts, duplicated raw aliases, unit helper columns, and depth fields when they are not approved predictors. | Reduces accidental leakage and spreadsheet noise. |
| Train-only preprocessing | Fits scaling, imputation, and feature selection only after the split. | Keeps validation honest when final grouped splits are used. |

The current matrix can support a mentor conversation about what fields belong
in `X_allowed`, what fields are targets, and what still needs source review.

## How Stability Connects To ML Later

Stability should connect to ML as context, not as a label. In the approved
runtime, stability can be joined to model rows as:

- `stability_status`;
- `stability_confidence`;
- caveat codes;
- inside/outside/blocked context;
- reason flags for reviewer plots;
- optional mask only if the mentor approves that policy.

The occurrence classifier and saturation regressor must still learn from
approved labels and validated well-log/core/NMR evidence. Stability can explain
whether a prediction is physically admissible under the current assumptions,
but it cannot create occurrence or saturation by itself.

## What The Three Datasets Can Support Now

The current three-dataset package can support:

- workbook and sheet inventory;
- target-variant discovery;
- schema and feature-family audit;
- cleaned feature matrix construction;
- target-leakage testing;
- train-only preprocessing proof;
- row-free model-run tracker summaries;
- mentor review of exclusions, labels, and blockers.

It cannot yet support final claims about hydrate occurrence, hydrate
saturation, producibility, regional sweet spots, or validated model performance.

## What Cannot Be Claimed Yet

The project should not claim:

- hydrate proof;
- final stability boundaries or thickness;
- occurrence predictions;
- saturation predictions;
- validated occurrence or saturation model metrics;
- final target-label authority;
- public release of row-level approved data;
- public maps of private predictions;
- final sweet-spot or producibility ranking.

Preferred language is: public-safe scaffold, schema readiness,
stability-admissibility, working screening envelope, target-only label, runtime
confirmation needed, mentor review needed, and not hydrate proof.

## Packages And Access That Unlock Next

The next step depends on DOE package and data access.

| Package or access | What it unlocks | Public-safe output after review |
|---|---|---|
| `lasio` | Direct LAS loading instead of workbook-only tables. | Header and curve-coverage summaries. |
| `geopandas`, `shapely`, `pyproj`, `fiona`, `pyogrio`, `rtree` | Local spatial joins for stability and map overlays. | Row-free spatial coverage summaries and public maps. |
| `scikit-learn`, `joblib` | Baseline models, saved local pipelines, grouped validation. | Public-safe model-run summaries after review. |
| `plotly`, `streamlit` | DOE-local review website with tracker, maps, and well plots. | Screenshots or summaries only after row/privacy review. |
| `tensorflow` or `keras` | Neural-network experiments after baseline controls pass. | Architecture and validation summaries, not raw models. |
| `shap` | Feature-influence diagnostics by run and target. | Aggregated explanation summaries after approval. |
| `python-docx`, `python-pptx` | Regenerated mentor documents from reviewed summaries. | Updated public-safe Word/PPT deliverables. |
| Full approved data and label authority | Complete target registry, grouped validation, and final model review. | Final public-safe claims only after mentor approval. |

## Mentor Questions And Decisions

These decisions should be reviewed before the next model-claim step:

1. Which saturation field is authoritative for training and validation:
   `Sgh`, `S_h`, `Sh`, `NMR_SAT`, or another reviewed label?
2. Are saturation targets stored as fractions, percentages, or mixed
   conventions by sheet?
3. How should occurrence be defined: phase labels, saturation threshold,
   source classes, or mentor-reviewed intervals?
4. Which wells or compartments become training, validation, and locked-test
   groups?
5. Should depth stay only as alignment/context, or can a reviewed depth/context
   feature enter `X_allowed`?
6. Which resistivity fields, such as `A090` or `AF90`, are the preferred deep
   resistivity predictors?
7. Which NMR fields are measured inputs versus target-derived labels?
8. Is caliper coverage sufficient for washout filtering, or should it remain a
   missing-QC flag?
9. Are missing-log adapters allowed, and if so, how should measured versus
   generated curves be flagged?
10. Should stability be used only as context/confidence/reason flag, or also as
    a mentor-approved mask?

## Near-Term Work Plan

```text
review this companion brief
-> inspect DOE prototype audit outputs
-> confirm target authority and units
-> lock X_allowed / Y-only field policy
-> choose grouped validation split
-> join stability context as non-label metadata
-> rerun baseline models in DOE
-> review external or whole-workbook validation
-> export only row-free public-safe summaries
```

Until approved-data validation exists, the website, slides, and Word documents
should emphasize workflow readiness, source traceability, auditability,
stability-admissibility, and blocked states rather than presenting discoveries
or model performance.
