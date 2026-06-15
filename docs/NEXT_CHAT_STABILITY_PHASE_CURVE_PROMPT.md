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
labels, caveats, and the `stability_screen_*.csv` schema.

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

Current phase-curve range fix:
The first OSL screen run wrote `8,084` screen rows but all were blocked. The
cause was over-strict grid coverage: the screen grid started at `0 m`, while
the cited phase lookup begins deeper. The writer now starts the calculation
grid at the minimum depth covered by the phase lookup and still blocks any row
whose modeled interval cannot close within the lookup's maximum covered depth.
The committed OSL rerun now has `8,084` screen rows, `22` calculated baseline
intervals, `8` no-stable-interval rows, and `8,054` blocked rows. Every row
must keep `not_hydrate_proof`.

Current website product spec:
`data/public_stability_products/stability_website_product_spec_2026-06-14.csv`
defines the final public website shape for stability: status strip, readiness
tables, map, selected-well audit panel, temperature-phase plot, results table,
scenario controls, and exports/citations.

Current website state:
The public Structural Explorer now exposes the guarded screen as a baseline
methane 5 ppt stability-admissibility screen, with summary counts,
status/confidence breakdowns, calculated interval preview, blocked/no-interval
sample, a 2D well-status map, a calculated interval depth chart, and CSV
download. It also has tabs explaining why rows are blank, the G10015/GGD223
coordinate crosswalk, nearest located G10015 control distances, proxy-candidate
tiers, and source anchors. The Calculated Intervals tab has a selected-well
temperature/phase audit plot using the committed methane 5 ppt phase boundary,
OSL modeled temperature key-depth product, and screen top/base markers where
available; it is not the full raw measured G10015 profile. Do not call it
hydrate proof, saturation, producibility, or a sweet-spot ranking. Do not use
proxy tiers to fill top/base/thickness unless the mentor approves a separately
versioned sensitivity screen.

Current sampled temperature-curve export:
`data/public_stability_products/g10015_temperature_profile_points_sampled_2026-06-14.csv`
and its summary are committed from OSL. The sampled product has `28,020` rows,
`184` profiles, `24` well codes, and a maximum of `160` sampled points per
profile. The selected-well temperature/phase audit plot can now show the
sampled measured G10015 curve along with the methane 5 ppt phase boundary,
OSL modeled key-depth temperatures, and screen top/base markers.

Current public ML feature scaffold:
`data/public_stability_products/public_ml_feature_scaffold_2026-06-15.csv`,
`public_ml_feature_scaffold_summary_2026-06-15.csv`, and
`public_ml_feature_dictionary_2026-06-15.csv` now exist. The scaffold has
`8,084` public well rows, `483` matched G10015 temperature-context rows, `22`
calculated baseline stability-interval feature rows, `8` no-stable-interval
rows, and `0` validated hydrate occurrence/saturation labels or training-ready
rows. The `Analyze Hydrates` page has a `Public ML Readiness` tab for this
real public feature scaffold. Treat stability as a physics-derived feature and
coverage/readiness signal only, not a model label.

Next task:
Continue from the public ML-readiness layer. Good next options are:
1. QA the hosted Streamlit `Analyze Hydrates -> Public ML Readiness` panel.
2. Add mentor-facing screenshots/figures from the public ML feature scaffold.
3. Build an approved-data target registry plan that maps screenshot target
   fields (`Sgh`, `S_h`, `Sh`, `NMR_SAT`) to occurrence/saturation roles without
   exposing raw rows.
4. Improve source coverage in OSL: refine temperature matches, add better
   permafrost/base controls if public and cited, digitize/model approved
   phase-curve sensitivities, then rerun the same guarded writer and compare
   counts.

If web research is needed, use primary/public sources and cite them.
```
