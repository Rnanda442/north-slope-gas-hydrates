# Mentor Decision Requests

Created: 2026-06-15

## One-Page Project Status

The project is now organized around a public/approved-data boundary. GitHub and
Streamlit show public-safe diagrams, schema tables, source-backed counts,
guarded stability-admissibility products, caveats, and readiness views.
OpenScienceLab and the future approved runtime are where approved LAS/CSV logs,
core, NMR, workbook labels, feature engineering, target mapping, model fitting,
validation, and reviewed outputs belong.

Completed work outside stability includes the public GIS/website scaffold,
source-library organization, public ML feature scaffold, target registry,
leakage guardrails, approved-data schema coverage matrix, V5.3 workflow package,
and the new approved-data field-role/intake/model-plan documents. The current
public scaffold has 8,084 wells. The approved-data schema layer is based on
visible headers/screenshots and about 3 of the expected 71 datasets, which is
enough for architecture design but not training or performance claims.

The stability screen currently contributes pressure-temperature admissibility
context under the methane 5 ppt baseline. It has 22 calculated admissibility
intervals, 8 no-stable-interval rows, and 8,054 blocked rows. It is not hydrate
proof, not occurrence, not saturation, not final stability, not producibility,
and not a sweet-spot rank.

The ML architecture is ready at the method/spec level: measured logs and derived
features flow into `X_allowed`; `Sgh`, `S_h`, `Sh`, `NMR_SAT`, Hydrate
Saturation, `Swr`, phase labels, and occurrence labels stay on a separate
Y-only rail; whole-well/compartment/geographic splits happen before
preprocessing; occurrence classification and saturation regression are linked
but separate tasks.

Blocked work: final training, metrics, occurrence probabilities, saturation
predictions, and public model outputs require approved rows, official target
authority, unit confirmation, complete split policy, and public-release review.

Current V5.3 review copies:

- Slides:
  <https://docs.google.com/presentation/d/1kP0icjCLpldXZX80eww27IIokG1s3VbM5bSXiGLk8Sw>
- Companion:
  <https://docs.google.com/document/d/1QcF-31U77_MyPHnrBSYFZSswFyIzO8P3pMLBSTIMgMQ>

## How Occurrence Should Be Measured

Occurrence is not measured by the stability screen. It should be recorded as an
approved target or validation label from source evidence such as core or
pressure-core observations, NMR/core-derived saturation, validated multi-log
interpretation, or documented seismic indicators. Each label needs a source,
well/depth interval, confidence flag, and caveat before it can train or validate
an occurrence classifier.

Chong et al. 2024 / USGS is useful as an external ML anchor because it uses ANN
models for hydrate occurrence classes and saturation prediction, but it is not
North Slope field truth: <https://pubs.usgs.gov/publication/70250169>.

## Current ML Architecture Decisions And Open Mentor Questions

### A. Ready to encode now

- The first model skeleton should keep occurrence classification and saturation
  regression as linked but separate tasks.
- Numeric predictors should be scaled 0-1 using train-only statistics after a
  whole-well, compartment, or geographic split. Depth remains the
  alignment/context axis unless approved as a predictor.
- Every variable should carry a fingerprint: original header, unit, normalized
  name, role, allowed-in-feature-matrix status, leakage risk, and unresolved
  mentor question.
- `GR`, density porosity, resistivity transforms, `Vp`, `Vs`, `Vp/Vs`,
  impedance, elastic attributes, NMR-density separation, and equation-list
  features can be candidate features only after source, unit, QC, and leakage
  checks pass.
- Caliper coverage should be checked before any washout filtering. Missing
  caliper should create a missing-QC flag, not silent filtering.
- Model progression should be baselines first, tree/boosting second, and
  ANN/Keras third.
- Well-MTE means Mt. Elbert Stratigraphic Test Well and Well-IGS means Ignik
  Sikumi Test Well; both are North Slope / Eileen Gas Hydrate Trend case-study
  wells. `MTE_refined` and `IGS_refined` stay open until workbook metadata
  confirms processing stages: <https://www.osti.gov/servlets/purl/1893637>.
- Missing-log adapters for `Vp` or `RHOB` are optional and validation-required;
  the marine hydrate MDPI example supports the concept but not automatic North
  Slope transfer: <https://www.mdpi.com/1996-1073/16/23/7709>.

### B. Blue mentor questions

- Which saturation field is authoritative: `Sgh`, `S_h`, `Sh`, or `NMR_SAT`?
- Should occurrence use source-style classes, saturation thresholds, or
  mentor-reviewed intervals?
- Are `MTE`/`IGS` separate wells and are `*_refined` processing stages in the
  workbook?
- Do we have enough caliper coverage to apply washout filtering?
- Which wells become blind validation after full recovery?
- Are missing-log adapters allowed, or should missing curves simply block that
  feature set?

## Decisions Needed

1. Phase-curve policy: should official public stability remain methane 5 ppt
   only, or should the project add clearly labeled scenario curves?
2. Target authority: which occurrence and saturation labels are official for
   training and validation when `Sgh`, `S_h`, `Sh`, `NMR_SAT`, Hydrate
   Saturation, core/NMR labels, or phase labels differ?
3. Validation split: should the first defensible test use whole-well holdout,
   compartment holdout, geographic/geologic holdout, or a staged combination?
4. Missing G10015 temperature policy: should wells stay blocked, use
   nearest-control proxy tiers, or use explicit scenario-only gradients?
5. Stability use in ML: is stability approved only as context, mask,
   confidence, caveat, or blocked reason, never as occurrence proof or a
   saturation target?
6. Public website outputs: before approved model validation, which public views
   are acceptable: diagrams, counts, schemas, caveats, blocked reasons,
   synthetic examples, readiness summaries, and/or public-safe aggregate
   reviews?

## Weekday Report Bullets

- Monday: Locked the public/OSL boundary and used the V5.3 package as the project
  explanation foundation.
- Tuesday: Preserved the methane 5 ppt stability screen as admissibility
  context only, with calculated, no-interval, and blocked rows separated.
- Wednesday: Built the approved-data field-role table and intake spec from
  public-safe headers and schema evidence.
- Thursday: Defined the first approved-runtime model experiment without
  training or reporting fake metrics.
- Friday: Prepared mentor decisions for phase curves, target authority,
  validation split, missing temperature coverage, stability use, and public
  website outputs.

## Guardrail Language

Stability is necessary context, not proof. Occurrence evidence must come from
approved target/validation sources such as core or pressure-core observations,
NMR/core-derived saturation, validated log interpretation, or seismic
indicators. Saturation and occurrence labels are Y-only; they must not enter
the predictor matrix.
