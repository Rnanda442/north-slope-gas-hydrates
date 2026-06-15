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
leakage guardrails, approved-data schema coverage matrix, V5 workflow package,
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

## How Occurrence Should Be Measured

Occurrence is not measured by the stability screen. It should be recorded as an
approved target or validation label from source evidence such as core or
pressure-core observations, NMR/core-derived saturation, validated multi-log
interpretation, or documented seismic indicators. Each label needs a source,
well/depth interval, confidence flag, and caveat before it can train or validate
an occurrence classifier.

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

- Monday: Locked the public/OSL boundary and used the V5 package as the project
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
