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

Current local intersection code:
`dashboard/stability_products.py` also includes
`stability_depth_grid(...)`, `stability_condition_grid_from_profile(...)`, and
`stability_interval_from_condition_grid(...)`. Tests cover inclusive depth-grid
construction, interpolated top/base crossings for a synthetic closed interval,
open-below-model bases with extrapolation caveats, and blocked incomplete
pressure-temperature grids. This has not been applied to the public scaffold.

Current local confidence-label code:
`stability_source_control_label(...)` assigns source-control confidence labels
for fixture rows. Tests cover high, medium, low, blocked, and outside-AU cases.
These are not hydrate-confidence labels and do not estimate occurrence,
saturation, producibility, or sweet spots.

Current OSL temperature-product writer:
`01_pipeline/build_public_stability_products.py` now calls
`write_stability_temperature_model_product(...)`. When the active source root
contains raw G10015 processed profile `.txt` files, the pipeline writes
`data/public_stability_products/stability_temperature_model_2026-06-14.csv`
and `stability_temperature_model_summary_2026-06-14.csv`. The product is one
row per scaffold well per modeled key depth and keeps
`stability_top_base_thickness_status = not_calculated`.

Current G10015 parser fix:
`load_g10015_temperature_profile_points(...)` now collapses duplicate
`depth_m` values by averaging `temperature_c`. This fixes the OSL failure in
`usgs_put-25-5fnandahora442.txt`, where duplicate depth `8.23` caused the
inventory build to stop.

Current guarded stability-screen writer:
`write_stability_screen_product(...)` now exists and is called by
`01_pipeline/build_public_stability_products.py` when raw G10015 profile rows
are available. It writes one row per public scaffold well, fills
top/base/thickness only for rows that pass the pressure, temperature,
phase-curve, intersection, and source-control confidence gates, and leaves
blocked rows null. The screen remains a stability-admissibility screen, not
hydrate proof or saturation.

Current website product spec:
`data/public_stability_products/stability_website_product_spec_2026-06-14.csv`
defines the final public website shape for stability: status strip, readiness
tables, map, selected-well audit panel, temperature-phase plot, results table,
scenario controls, and exports/citations.

Next task:
The next work should happen in OSL if the full source bundle is available:
1. keep the input capability matrix and phase lookup metadata current;
2. pull/sync this GitHub state on OSL;
3. run `python 01_pipeline/build_public_stability_products.py` from the repo
   with the full source bundle available;
4. review the `Stability Screen Summary`;
5. commit only derived public outputs, especially the new
   `stability_screen_*.csv` files, after confirming blocked rows remain null
   and every row carries `not_hydrate_proof`.

Do not calculate final top/base/thickness until those implementation gates are
complete. If web research is needed, use primary/public sources and cite them.
```
