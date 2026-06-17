# Slide 3 Signal-Response Source Package - 2026-06-17

This folder prepares source-backed material for a future rebuild of Slide 3.
It does not redesign or edit the PPTX.

## Scope

Slide 3 should shift from a parameter-range board to a depth-aligned signal
movement explanation. The core message is that hydrate interpretation depends
on co-moving evidence and guardrails:

1. Stability context: can hydrate exist under the assumed pressure-temperature
   screen?
2. Clean sand plus porosity: can the rock host pore-filling hydrate?
3. Electrical, elastic, NMR, and core response: does the interval behave like
   hydrate-bearing sediment?
4. Guardrails: free gas, ice, tight or cemented rock, shale or clay, bad hole,
   missing Vs, and missing NMR or core support.

The requested `docs/SOURCE_ACCESS_MAP_2026-06-17.md` file was not present in
this worktree. Source status was therefore checked against the current artifact
index, source-library index, source manifest, baseline source ledger, public
evidence registry, and the recorded Google Drive source PDFs.

## Files

| File | Status | Use |
| --- | --- | --- |
| `slide03_signal_response_stack_schematic_public_safe.png` | Safe to push | Public-safe synthetic log-stack sketch for the proposed Slide 3 layout. It uses public project rules only and no approved row-level data. |
| `project_csv_methane_5ppt_phase_curve_context_only.png` | Safe to push | CSV-derived methane 5 ppt stability curve. Use as stability context only. |
| `project_website_regional_map_context.png` | Safe to push | Project website regional context reference. Use as a small source/context badge only if space allows. |
| `usgs_public_domain_multilog_caliper_gamma_resistivity_crop.png` | Safe to push | USGS public-domain geophysical log crop showing caliper, gamma, and resistivity-style tracks. Generic log visual, not ANS field proof. |
| `usgs_public_domain_caliper_washout_qc_crop.png` | Safe to push | USGS public-domain caliper/log crop for explaining borehole QC and washout. Generic visual, not ANS field proof. |
| `slide_03_source_to_visual_matrix_2026_06_17.csv` | Safe to push | Source-to-visual matrix and push-status table. |
| `SLIDE_03_SIGNAL_RESPONSE_OUTLINE_2026_06_17.md` | Safe to push | Build-ready outline for the future Slide 3 revision. |

## Source And License Notes

Public-safe images in this folder are either project-generated from public
rules/CSV files or copied/cropped from USGS public-domain visual references
already recorded in `references/presentation-revision-2026-06-11/source_manifest.csv`.

Drive-only or publisher-controlled sources were used as text/source support
only. Their exact figure crops were not committed:

- Aung et al. 2026, Energy & Fuels, Drive PDF: strong PBU L-Pad/HYDRATE-02 LWD
  source for GR, resistivity, caliper, density/neutron porosity, sonic, NMR,
  MAD, and gas-response guardrails. Do not push paper figure crops without a
  separate license decision.
- Yoneda et al. 2026, Energy & Fuels, Drive PDF: strong HYDRATE-02 NMR/core
  calibration and permeability source. Do not push paper figure crops without a
  separate license decision.
- Lee and Collett 2011, USGS publication page for Mount Elbert: strong ANS
  multi-log saturation-estimation source. The official source page is safe as a
  citation anchor, but the publisher article figures should not be pushed here.
- Haines et al. 2022 and Zyrianova et al. 2024: useful ANS source anchors, but
  local figure-ready PDFs were not available in this worktree.
- Chong et al. 2022, Singh et al. 2021, and Chong et al. 2024: useful ML/log
  method anchors, but not committed as figure crops because their visual reuse
  rights were not clear enough for this source package.

## Stability Visual Rule

For Slide 3 stability context, use only:

`project_csv_methane_5ppt_phase_curve_context_only.png`

This image is generated from:

`data/public_stability_products/phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1.csv`

Do not use raw paper stability screenshots as the final Slide 3 stability
visual. Stability remains an admissibility/context screen only, not hydrate
proof, occurrence evidence, saturation evidence, or validation truth.

## Recommended Next Build Use

The next slide-build prompt should use the synthetic stack as the central visual
template, then rebuild it in the active deck style with source badges and small
inset support images. Keep exact paper figures out of the slide unless a
public-use license is confirmed for that figure.
