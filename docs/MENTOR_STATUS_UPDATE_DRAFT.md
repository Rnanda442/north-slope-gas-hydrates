# Mentor Status Update Draft

Created: 2026-06-15

## Purpose

Public-safe draft language for a mentor update on the current stability-screen
and deliverable direction. This document is for communication planning only. It
does not contain approved well-log rows, core rows, restricted identifiers,
runtime outputs, populated configurations, trained models, or final hydrate
results.

## Short Status Update

The project is now split into two clean working surfaces: OpenScienceLab is the
heavy-data workbench for approved inputs, temperature-profile inventory,
runtime-only outputs, and guarded calculations, while GitHub/Streamlit remains
the public delivery surface for source-backed documentation, diagrams, and
public/synthetic scaffold views.

The current communication baseline is that the public scaffold carries the
North Slope public well set reported for this phase as 8,084 Arctic Slope
public wells. In the G10015 temperature inventory, the intake currently reports
184 temperature profiles across 24 well codes. The OpenScienceLab
temperature-model product reports 16,168 key-depth rows, with status counters
of 919 calculated, 387 extrapolated, 15,249 blocked, and 0 final stability
results in that temperature-input product. A separate guarded baseline
stability-screen product now carries 8,084 screen rows: 22 calculated
admissibility intervals, 8 sufficient-input rows with no modeled stable
interval, 8,054 blocked rows, and every row tagged as not hydrate proof.

The workflow has moved from a general concept into a controlled calculation
path. It now has a cited methane 5 ppt phase curve, a hydrostatic pressure
model, temperature-model logic, source-control confidence labels, and a guarded
stability-screen writer.

The key scientific guardrail is that this is a stability-admissibility screen.
It is not hydrate proof, it is not saturation, and it is not a sweet-spot
ranking. It only identifies where pressure-temperature conditions and data
controls make an interval admissible for later hydrate interpretation once
approved well-log and core evidence are allowed into the runtime workflow.

## One-Paragraph Email Version

The project is now organized around a clean public/runtime split:
OpenScienceLab is the heavy-data workbench for approved inputs and guarded
calculations, while GitHub/Streamlit is the public delivery surface for
source-backed scaffolds and diagrams. The current communication baseline is an
8,084-well public scaffold, a G10015 temperature inventory with 184 profiles
across 24 well codes, an OpenScienceLab temperature-model product tracking
16,168 key-depth rows with 919 calculated, 387 extrapolated, 15,249 blocked,
and 0 final stability results in that temperature-input product, plus a guarded
baseline screen with 22 calculated admissibility intervals and 8,054 blocked
rows. The workflow now has a cited methane 5 ppt phase curve, hydrostatic
pressure model, temperature-model logic, source-control confidence labels, and
a guarded stability-screen writer. I am keeping the language conservative:
this is a stability-admissibility screen only, not hydrate proof, saturation
estimation, or sweet-spot ranking.

## Outside-Stability ML/Schema Update

Outside the stability screen, I have been building the ML data architecture
needed for the approved well-log workflow. I organized the project headers into
measured inputs, derived features, QC fields, calibration/reference fields, and
target-only saturation fields; locked a leakage barrier so `Sgh`, `S_h`, `Sh`,
`NMR_SAT`, hydrate-saturation fields, `Swr`, `S_wr`, and interpreted phase
labels cannot enter the feature matrix; and designed a whole-well validation
pipeline for future occurrence classification and saturation regression.
Because only a subset of the expected 71 datasets is currently available, the
work is framed as schema and model-architecture readiness rather than final
training or performance reporting.

Public-safe artifacts for this layer are now:

- `docs/APPROVED_DATA_SCHEMA_COVERAGE_AND_MODEL_ARCHITECTURE_PLAN.md`
- `data/public_ml_products/approved_schema_coverage_matrix_2026-06-15.csv`

The current V5.3 mentor package translates that work into a presentation and
companion document: the slides use source-backed hydrate/North Slope visuals,
a parameter-range board, a simplified workflow, leakage-safe ML architecture,
and validation/output guardrails, while the companion explains the same
workflow without claiming approved-data training, predictions, saturation
results, or hydrate proof.

- Slides:
  <https://docs.google.com/presentation/d/1kP0icjCLpldXZX80eww27IIokG1s3VbM5bSXiGLk8Sw>
- Companion:
  <https://docs.google.com/document/d/1QcF-31U77_MyPHnrBSYFZSswFyIzO8P3pMLBSTIMgMQ>

## Mentor Questions For Future Decisions

1. Should the official baseline remain 100% methane plus 5 ppt salinity?
2. Do we want to digitize or model the mixed-gas curve from Collett et al.
   (2011) / Holder et al. (1987) as sensitivity only?
3. What phase-curve source or model should replace the digitized figure if a
   stronger source becomes available: CSMHYD, CSMGem, a published table, or
   another USGS source?
4. What control-distance thresholds should define high, medium, and low
   confidence?
5. Should OM-222 permafrost base be digitized next?
6. Which approved well-log and core fields will be allowed later for
   occurrence and saturation validation?
7. For the final ML workflow, should occurrence classification and saturation
   regression be presented as two linked outputs?

## Additional ML/Schema Mentor Questions

1. Which of `Sgh`, `S_h`, `Sh`, or `NMR_SAT` should be treated as the
   authoritative saturation target when multiple exist?
2. Please confirm the recovered sheets consistently store saturation values as
   fractions from 0 to 1.
3. Should occurrence labels be derived from saturation thresholds, interpreted
   phase labels, or mentor-reviewed intervals?
4. Are `MTE`, `IGS`, `MTE_refined`, and `IGS_refined` separate wells, separate
   processing stages, or separate source datasets?
5. Which wells should be held out for blind validation?

## Internal Verification Notes

- The requested stability-specific docs are now present after syncing with
  `origin/main`: `docs/NORTH_SLOPE_PROJECT_BASE.md`,
  `docs/STABILITY_CALCULATION_PLAN.md`, and
  `docs/NEXT_CHAT_STABILITY_PHASE_CURVE_PROMPT.md`.
- The 8,084 count is verified in
  `data/public_stability_products/north_slope_well_stability_context_summary_2026-06-14.csv`
  and `data/public_stability_products/stability_input_scaffold_summary_2026-06-14.csv`.
  Older atlas files still carry broader raw/master-layer counts, so deliverable
  language should say "current public stability scaffold" when using 8,084.
- Keep the temperature-model product and stability-screen product separate: the
  former models temperature key-depth inputs; the latter applies the guarded
  methane 5 ppt admissibility screen.
- Do not convert blocked rows or no-stable-interval rows into no-hydrate
  findings. They are calculation/data-readiness statuses.
