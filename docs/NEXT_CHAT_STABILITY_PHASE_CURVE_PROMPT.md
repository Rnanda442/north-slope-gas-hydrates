# Next Chat Prompt - Stability Phase Curve Step

Use this prompt to start the next Codex chat.

```text
We are working in the GitHub repo `Rnanda442/north-slope-gas-hydrates`.
Start by reading `docs/NORTH_SLOPE_PROJECT_BASE.md`, `PROJECT_CONTEXT.md`,
and `docs/source_library_index/stability_source_bundle_2026_06_13.md`.

Current state:
- OpenScienceLab is the heavy-data workbench.
- GitHub/Streamlit is the public delivery surface.
- Raw source files stay out of Git under `data/source_library/`.
- Derived public outputs live under `data/public_stability_products/`.
- Previous complete OSL-derived product baseline commit:
  `aedd734 Rebuild stability products with complete G10015 profiles`.
- Full source bundle status after the missing G10015 upload:
  `7/7` source categories, `43` GGD223 controls, `184` G10015 profiles,
  `3` hydrate AUs.
- Current public stability products:
  `north_slope_well_stability_context_2026-06-14.csv`
  `g10015_temperature_profile_inventory_2026-06-14.csv`
  `stability_input_scaffold_2026-06-14.csv`
- Current scaffold summary:
  `8,084` wells, `483` temperature-profile matches, `374` rows ready for
  phase-curve inputs, `7,113` rows needing temperature profile match, and
  `0` final stability results.
- The local website is viewed at:
  `http://localhost:8517/?page=Explore%20North%20Slope`
  in `Explore North Slope -> Structural Explorer`.

Important guardrail:
Do not call the current scaffold hydrate proof, saturation, or final stability.
It is only an input scaffold. Final `stability_top_m`,
`stability_base_m`, and `stability_thickness_m` should remain uncalculated
until pressure, temperature, and hydrate phase-curve assumptions are locked and
cited.

Current plan:
`docs/STABILITY_CALCULATION_PLAN.md` now documents the source-backed stability
calculation contract: hydrostatic pressure equation, G10015/GGD223 temperature
model hierarchy, methane 5 ppt phase-curve lookup, source-control confidence
labels, caveats, and the future `stability_screen_*.csv` schema.

Current phase-curve artifact:
`data/public_stability_products/phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1.csv`
is the first cited lookup and the official mentor-approved baseline. It is
digitized from USGS SIR 2008-5175 Figure 1A for the methane and 5 ppt
salt-water phase boundary and should be replaced by a direct CSMHYD/CSMGem
export if one is obtained.

Current phase-curve scenario catalog:
`data/public_stability_products/phase_curve_scenario_catalog_2026-06-14.csv`
keeps the public workflow variable-capable. It marks the 100 percent methane
curve as `official_public_baseline` and records the Collett et al. (2011) /
Holder et al. (1987) 98 percent methane / 1.5 percent ethane / 0.5 percent
propane curve as `sensitivity_only_not_final` until it has a versioned lookup
or thermodynamic-model export.

Current input capability matrix:
`data/public_stability_products/stability_input_capability_matrix_2026-06-14.csv`
defines what current public inputs can support now, what remains
scenario-only, and what must wait for approved runtime data.

Current OSL pull trigger matrix:
`data/public_stability_products/stability_osl_pull_triggers_2026-06-14.csv`
defines when to use the public repo versus the full OSL/source bundle. Local
unit-test work for temperature interpolation does not need OSL. Real public
temperature-model products do need OSL because the raw G10015 profile rows are
not committed to Git.

Current local temperature-model code:
`dashboard/stability_products.py` includes
`load_g10015_temperature_profile_points(...)` and
`temperature_model_from_profile(...)`. Tests cover G10015-style depth/
temperature parsing, measured-profile interpolation, below-profile
gradient-based extrapolation, missing-gradient blocking, empty-profile
blocking, and missing-depth blocking. This is still fixture-only code; no real
public temperature-model product has been rebuilt from OSL yet.

Current website product spec:
`data/public_stability_products/stability_website_product_spec_2026-06-14.csv`
defines the final public website shape for stability: status strip, readiness
tables, map, selected-well audit panel, temperature-phase plot, results table,
scenario controls, and exports/citations.

Next task:
Build the stability-depth-grid and intersection tests before calculating any
final top/base/thickness fields:
1. keep the input capability matrix and phase lookup metadata current;
2. design the stability-depth grid and boundary-crossing tests using the
   tested temperature-model helper plus the methane phase lookup;
3. implement confidence-label and caveat-code tests;
4. decide when to pull OSL to build real public temperature-model products from
   raw G10015 rows;
5. keep `phase_curve_status = not_applied` and top/base/thickness null until
   temperature, pressure, phase-curve, and confidence-label tests are ready.

Do not calculate final top/base/thickness until those implementation gates are
complete. If web research is needed, use primary/public sources and cite them.
```
