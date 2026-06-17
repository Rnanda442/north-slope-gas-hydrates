# Slide 3 Signal-Response Outline - 2026-06-17

This is a source-backed plan for a future Slide 3 rebuild. Do not edit the
PPTX from this file alone.

## Recommended Slide Title

Hydrate Signals Move Together Across Depth

## One-Sentence Message

A hydrate-compatible interval is not defined by one parameter range; it is a
depth-aligned agreement among stability context, clean porous sand, electrical
response, elastic stiffness, NMR/core calibration, and QC guardrails.

## Current Deck Fit

- Use the latest active V5.5 Slide 2 source update deck as the build baseline.
- Do not use older V5.3 decks except as flawed-reference context.
- Current Slide 3 is a parameter-range board. The future rebuild should become
  the co-moving signal interpretation slide.
- Slide 5 already explains why individual parameters matter and where mimics
  enter.
- Slide 6 already owns equations, feature engineering, unit gates, and the
  leakage stop.
- Therefore Slide 3 should not be another range table or equation slide. It
  should show how evidence lines up vertically across depth.

## Exact Layout Plan

Use a 3-part layout:

1. Central depth stack, about 70 percent of slide width.
   Tracks from left to right:
   `Stability/BGHS`, `GR`, `Caliper QC`, `Phi/RHOB`, `Rt`, `Vp`,
   `Vs/mu-rho`, `NMR/core`.
2. Right-side decoder panel, about 25 percent of slide width.
   Four compact decoder cards:
   `Hydrate-compatible clean sand`, `Free gas / resistive mimic`,
   `Bad-hole QC`, `Stability context only`.
3. Bottom source and leakage rail.
   Include source badges:
   `Mount Elbert / Milne Point`, `Eileen / Tarn`, `PBU L-Pad / HYDRATE-02`.
   Include target-only rail:
   `Sgh`, `S_h`, `Sh`, `Hydrate Saturation`, `NMR_SAT`, `Swr`, and phase
   labels stay out of `X_allowed`.

Use `slide03_signal_response_stack_schematic_public_safe.png` as the visual
template for the deck rebuild, not as final polished slide art unless the style
already matches the active deck.

## Parameter Placement

| Track | Placement | Visual Movement | Meaning |
| --- | --- | --- | --- |
| Stability/BGHS | Leftmost context track | Inside/outside band or BGHS line | Hydrate admissibility context only. It cannot prove occurrence or saturation. |
| GR | First log evidence track | Low or left shift in clean sand | Clean sand host proxy. Low GR is not hydrate proof. |
| Caliper QC | Before density/sonic/resistivity trust | Washout spike plus hatch overlay | Bad-hole or tool-standoff risk. Downweight or exclude affected interval. |
| Phi/RHOB | Host-capacity track | Porosity present; density shift subtle | Pore volume support. Host capacity only, not proof. |
| Rt | Electrical response track | High or right shift | Hydrate support when co-moving with host and stiffness; also free gas, ice, tight rock, cement, salinity, invasion, and washout mimic. |
| Vp | Elastic response track | Higher or right shift | Stiffness support, but ice/cement/lithology can mimic. |
| Vs/mu-rho | Rigidity track | Higher or right shift in hydrate-compatible interval | Helps separate hydrate-like frame stiffening from free-gas resistivity mimic. Missing Vs lowers confidence. |
| NMR/core | Calibration/support track | Mobile-fluid reduction or NMR-density separation; core tie marks | Independent support where available. `NMR_SAT`, `Sgh`, and `Sh` are target/calibration only, never predictors. |

## Required Signal Movements

- Hydrate-compatible clean sand:
  low GR, usable porosity, high Rt, higher Vp, higher Vs or mu-rho, and NMR/core
  support inside the stability context.
- Free gas or resistive mimic:
  low GR and high Rt may look similar to hydrate, but Vp/Vs/mu-rho do not show
  the same stiffness agreement and NMR/core may indicate mobile fluid or gas.
- Bad-hole QC:
  caliper washout should appear as a hatched interval crossing the affected
  tracks. The label should say `downweight/exclude`, not `hydrate`.
- Stability/BGHS:
  show as a thin context band or left track. Label it `admissibility only`.

## Source Examples To Support The Slide

| Example Area | Source Support | Slide Use |
| --- | --- | --- |
| Mount Elbert / Milne Point | Lee and Collett 2011 USGS source page and project source manifest. Supports NMR, P-wave, S-wave, resistivity, and core/log saturation-estimation logic. | Source badge and speaker-note anchor for classic ANS multi-log hydrate interpretation. Do not embed publisher figure crops without license clearance. |
| Eileen / Tarn | Chong et al. 2022 permafrost hydrate ML source and Zyrianova et al. 2024 trend/source-page context. | Source badge for trend-scale North Slope context and ML feature logic. Do not treat trend context as depth-specific proof. |
| PBU L-Pad / HYDRATE-02 | Aung et al. 2026 Drive PDF text supports LWD track suite, B1/D1 sands, GR plus resistivity, sonic/NMR, caliper/QC, and gas-response guardrails. Yoneda et al. 2026 supports NMR/core calibration and permeability context. | Main source badge for the modern project-specific example. Use text-level citation unless figure license is cleared. |
| Generic public-domain logs | USGS public-domain geophysical log crops in this folder. | Small visual references for tracks and QC only. Label as generic USGS examples, not hydrate proof and not ANS field evidence. |
| Stability curve | Project CSV-derived methane 5 ppt image in this folder. | Small stability context visual only. Do not use raw paper stability screenshots. |

## Exact Slide Labels

Use short labels only:

- `Hydrate-compatible clean sand`
- `Free gas / resistive mimic`
- `Bad-hole QC`
- `Stability context only`
- `Low GR = clean host, not proof`
- `High Rt = support or mimic`
- `Vp + Vs/mu-rho = stiffness support`
- `NMR/core = calibration support`
- `Caliper washout = downweight/exclude`
- `BGHS/stability = admissibility only`
- `Target-only rail: Sgh, Sh, Hydrate Saturation, NMR_SAT, Swr`

## What To Exclude

- Do not make Slide 3 a simple parameter-range table.
- Do not use AI-generated hydrate cage art or AI-looking pressure-temperature art.
- Do not use raw paper stability screenshots. Use only the project CSV-derived
  methane 5 ppt stability curve.
- Do not show `Sgh`, `S_h`, `Sh`, `Hydrate Saturation`, `NMR_SAT`, `Swr`, or
  phase labels as predictors.
- Do not claim high Rt, low GR, stability, or any single curve proves hydrate.
- Do not cite quick-look saturation values from Aung, Lee/Collett, or other
  sources as this project's result.
- Do not commit approved well-log/core rows, private workbook outputs, fitted
  models, predictions, or row-level sensitive derivatives.
- Do not embed Drive-only or publisher-controlled paper figure crops unless a
  separate public-use license decision clears that specific image.

## Beginner-Readable Explanation For Speaker Notes

Read Slide 3 as a vertical checklist. First ask whether the depth is inside the
stability context. Then ask whether the rock is a clean porous host. Then ask
whether independent electrical, elastic, and NMR/core evidence move together.
Finally apply the guardrails: free gas, ice, tight rock, shale, washout, missing
Vs, missing NMR, and target-leakage rules. The point is not that one log proves
hydrate. The point is that a hydrate-compatible interpretation becomes more
defensible only when several independent signals line up and the known mimics
are controlled.
