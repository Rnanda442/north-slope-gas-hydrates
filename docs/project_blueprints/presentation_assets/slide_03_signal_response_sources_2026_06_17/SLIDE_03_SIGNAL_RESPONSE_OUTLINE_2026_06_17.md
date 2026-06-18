# Slide 3 Signal-Response Outline - 2026-06-17

This is a source-backed plan for a future Slide 3 rebuild. Do not edit the
PPTX from this file alone.

## Recommended Slide Title

Hydrate Signals Move Together Across Depth

## One-Sentence Message

A hydrate-compatible interval is not defined by one parameter range; it is a
depth-aligned agreement among stability context, clean porous sand, electrical
response, elastic/geomechanical stiffness, NMR/core calibration, and mimic
guardrails.

## Current Deck Fit

- Use the latest active V5.5 Slide 3 signal-response update deck as the build
  baseline.
- Do not use older V5.3 decks except as flawed-reference context.
- Current Slide 3 is the co-moving signal interpretation slide; this outline
  records the source logic and latest mentor changes.
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
   `Stability (P-T/BGHS)`, `Clean sand (GR/gamma)`,
   `Pore space (phi/RHOB)`, `Resistivity (Rt)`,
   `P-wave speed (Vp)`, `Rigidity (Vs/mu-rho)`, and
   `Fluid check (NMR/core)`.
2. Right-side decoder panel, about 25 percent of slide width.
   Four compact decoder cards:
   `Host rock`, `Hydrate support`, `What throws us off`, and
   `Fluid + target check`.
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
| Stability (P-T/BGHS) | Leftmost context track | Inside/outside band or BGHS line | Pressure-temperature hydrate admissibility context only. It cannot prove occurrence or saturation. |
| Clean sand (GR/gamma) | First log evidence track | Low or left shift in clean sand | Clean sand host proxy. Low GR is not hydrate proof. |
| Pore space (phi/RHOB) | Host-capacity track | Porosity present; density shift subtle | Pore volume support. Host capacity only, not proof. |
| Resistivity (Rt) | Electrical response track | High or right shift | Hydrate support when co-moving with host and stiffness; also free gas, ice, tight rock, cement, salinity, and invasion mimic. |
| P-wave speed (Vp) | Elastic response track | Higher or right shift | Stiffness support, but ice/cement/lithology can mimic. |
| Rigidity (Vs/mu-rho) | Geomechanical stiffness track | Higher or right shift in hydrate-compatible interval | Helps separate hydrate-like frame stiffening from free-gas resistivity mimic. Missing or estimated Vs lowers confidence unless provenance is clear. |
| Fluid check (NMR/core) | Calibration/support track | Mobile-fluid reduction or NMR-density separation; core tie marks | NMR means nuclear magnetic resonance fluid response; core means sample/lab tie. `NMR_SAT`, `Sgh`, and `Sh` are target/calibration only, never predictors. |

## Required Signal Movements

- Hydrate-compatible clean sand:
  low GR, usable porosity, high Rt, higher Vp, higher Vs or mu-rho, and NMR/core
  support inside the stability context.
- Free gas or resistive mimic:
  low GR and high Rt may look similar to hydrate, but Vp/Vs/mu-rho do not show
  the same stiffness agreement and NMR/core may indicate mobile fluid or gas.
- Stability/BGHS:
  show as a thin context band or left track. Label it `admissibility only`.

Caliper/washout/bad-hole QC should not be shown on the active Slide 3 because
the mentor clarified that those checks are already handled upstream. Keep the
QC policy in notes or companion text only unless the raw-preprocessing story is
reopened.

## Source Examples To Support The Slide

| Example Area | Source Support | Slide Use |
| --- | --- | --- |
| Mount Elbert / Milne Point | Lee and Collett 2011 USGS source page and project source manifest. Supports NMR, P-wave, S-wave, resistivity, and core/log saturation-estimation logic. | Source badge and speaker-note anchor for classic ANS multi-log hydrate interpretation. Do not embed publisher figure crops without license clearance. |
| Eileen / Tarn | Chong et al. 2022 permafrost hydrate ML source and Zyrianova et al. 2024 trend/source-page context. | Source badge for trend-scale North Slope context and ML feature logic. Do not treat trend context as depth-specific proof. |
| PBU L-Pad / HYDRATE-02 | Aung et al. 2026 Drive PDF text supports LWD track suite, B1/D1 sands, GR plus resistivity, sonic/NMR, caliper/QC, and gas-response guardrails. Yoneda et al. 2026 supports NMR/core calibration and permeability context. | Main source badge for the modern project-specific example. Use text-level citation unless figure license is cleared. |
| Generic public-domain logs | USGS public-domain geophysical log crops in this folder. | Retain as package/reference provenance only. The active slide should not use the caliper/QC crop as a visible panel. |
| Stability curve | Project CSV-derived methane 5 ppt image in this folder. | Small stability context visual only. Do not use raw paper stability screenshots. |
| Project website 2D stability map | Project public website map screenshot in this folder. | Small source/context badge showing the public project stability scaffold, not occurrence evidence. |
| Lijith, Malagar, and Singh 2019 | Gas-hydrate geomechanical review. | Broad source support for saying hydrate-bearing sediments can show stiffness/geomechanical support; keep explanation equation-free. |
| Dalvand and Falahat 2021 | Rock-physics model for estimating shear velocity. | Source support for measured/estimated Vs provenance language. |
| Collett et al. 2019 USGS FS 2019-3037 | North Slope gas hydrate resource assessment context. | Regional/source badge or speaker-note support only, not depth-specific proof. |

## Exact Slide Labels

Use short labels only:

- `Hydrate-compatible clean sand`
- `Resistive mimic: Rt high, stiffness/core disagree`
- `Stability (P-T/BGHS)`
- `Clean sand (GR/gamma)`
- `Pore space (phi/RHOB)`
- `Resistivity (Rt)`
- `P-wave speed (Vp)`
- `Rigidity (Vs/mu-rho)`
- `Fluid check (NMR/core)`
- `NMR = nuclear magnetic resonance`
- `Core = sample/lab tie`
- `BGHS/stability = admissibility only`
- `Target-only rail: Sgh, Sh, Hydrate Saturation, NMR_SAT, Swr`

## What To Exclude

- Do not make Slide 3 a simple parameter-range table.
- Do not use AI-generated hydrate cage art or AI-looking pressure-temperature art.
- Do not use raw paper stability screenshots. Use only the project CSV-derived
  methane 5 ppt stability curve.
- Do not show caliper washout or bad-hole hatches on the active Slide 3 unless
  the mentor asks to reopen raw-QC explanation; current assumption is that
  those issues are already preprocessed upstream.
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
Finally apply the guardrails: free gas, ice, tight or cemented rock, shale,
missing or estimated Vs, missing NMR/core, and target-leakage rules. The point
is not that one log proves hydrate. The point is that a hydrate-compatible
interpretation becomes more defensible only when several independent signals
line up and the known mimics are controlled.
