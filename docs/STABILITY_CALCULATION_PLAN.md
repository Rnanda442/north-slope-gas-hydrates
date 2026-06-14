# North Slope Stability Calculation Plan

Created: 2026-06-14

Status: source-backed calculation plan only. Do not calculate or publish
`stability_top_m`, `stability_base_m`, or `stability_thickness_m` until the
phase-curve lookup table and pressure-temperature assumptions below are
implemented with tests.

## Purpose

The future `stability_screen_*.csv` should be a gas hydrate stability
admissibility screen. It answers:

```text
Given a public well location, public vertical-depth basis, public permafrost and
temperature controls, an explicit pressure model, and a cited methane hydrate
phase boundary, does the modeled well depth intersect pressure-temperature
conditions where methane hydrate could be stable?
```

It does not prove hydrate occurrence, estimate hydrate saturation, identify
reservoir quality, or replace future approved well-log/core interpretation.

## Source Trail

Use the existing source bundle map in
`docs/source_library_index/stability_source_bundle_2026_06_13.md` as the local
file ledger. The calculation plan is tied to these public sources:

| Source | Project use | Current repo product |
| --- | --- | --- |
| Alaska DNR Well Bottom Hole Location | Public well coordinates and public depth fields. Prefer `TrueVertic`; use `DrillerTot` only as fallback. | `north_slope_well_stability_context_2026-06-14.csv` and `stability_input_scaffold_2026-06-14.csv` |
| NSIDC GGD223, Clow (1998), DOI `10.7265/3wjq-zt12` | Point permafrost-depth controls, including `pf_depth` in meters. | `ggd223_permafrost_controls.csv`, nearest-control joins |
| NSIDC G10015, Clow (2015), DOI `10.5065/D6N014HK` | Processed Arctic Slope borehole temperature profiles, 1973-2014. | `g10015_temperature_profile_inventory_2026-06-14.csv` |
| USGS OM-222, DOI `10.3133/om222` | Base of deepest ice-bearing permafrost from well logs. Use as the preferred mapped source after digitizing/georeferencing. | Source plate only; not yet digitized |
| USGS SIR 2008-5175, Lee, Collett, and Agena (2008) | North Slope method anchor for determining top and base of the gas hydrate stability zone from measured temperature data and a methane hydrate phase boundary. | Source in local bundle; `phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1.csv` |
| Collett et al. (2011), DOI `10.1016/j.marpetgeo.2009.12.001` | Alaska North Slope gas-hydrate occurrence synthesis; Figure 1 shows gas-chemistry sensitivity using 100 percent methane and 98 percent methane / 1.5 percent ethane / 0.5 percent propane curves modified from Holder et al. (1987). | Scenario catalog only; mixed-gas curve is not digitized or applied |
| USGS Data Series 69, Chapter CC / DDS-69-CC | Regional gas hydrate assessment and published Northern Alaska stability-zone context. | Local bundle and AU context |
| USGS 2019 gas hydrate AU data release | Assessment-unit polygons and input forms for regional context only. | `GasHydrateAUs.geojson` and AU joins |
| NETL methane hydrate primer | Public explanation that pressure, temperature, salinity, and gas composition shift methane hydrate stability. | Caveat/source language only |

Useful public source URLs:

- USGS SIR 2008-5175: https://pubs.usgs.gov/sir/2008/5175/
- USGS OM-222: https://www.usgs.gov/maps/map-showing-depth-base-deepest-ice-bearing-permafrost-determined-well-logs-north-slope-alaska
- NSIDC G10015: https://nsidc.org/data/g10015/versions/1
- NSIDC GGD223: https://nsidc.org/data/ggd223/versions/1
- USGS 2019 gas hydrate AU data release: https://data.usgs.gov/datacatalog/data/USGS%3A5d6005a6e4b01d82ce9853e3
- USGS Northern Alaska stability-zone contour data: https://data.usgs.gov/datacatalog/data/USGS%3A60abf6d1d34ea221ce51f606
- NETL methane hydrate primer: https://www.netl.doe.gov/sites/default/files/netl-file/2017-Methane-Hydrate-Primer%5B1%5D.pdf

## Locked Calculation Choices

### 0. Input Capability Gate

Before applying pressure-temperature intersections, use
`data/public_stability_products/stability_input_capability_matrix_2026-06-14.csv`
as the public input contract. It records which inputs can support a baseline
screen, which inputs are scenario-only, and which inputs remain blocked until
approved runtime data arrive.

The current gate is:

- ready for baseline screening: public well location/depth, GGD223 point
  permafrost context, matched G10015 temperature profiles, hydrostatic pressure
  assumption, USGS SIR 2008 100 percent methane + 5 ppt phase lookup, and USGS
  hydrate AU context;
- scenario-only: mixed-gas phase curve and alternate gas/salinity assumptions
  until each has a versioned lookup or cited thermodynamic-model export;
- blocked/future approved data: real well-log rows, core rows, authoritative
  saturation labels, measured gas composition, measured formation pressure, and
  sweet-spot ranking.

Rows or runs that depend on scenario-only inputs must not be labeled final
stability results. Rows or runs that depend on blocked inputs must remain null
or carry a blocked status.

Use `data/public_stability_products/stability_osl_pull_triggers_2026-06-14.csv`
to decide when to work from the public repo versus the OpenScienceLab/source
bundle. Unit-test fixture work does not need OSL. Real temperature-model
products do need OSL because the raw G10015 profile rows are not committed to
Git.

Use `data/public_stability_products/stability_website_product_spec_2026-06-14.csv`
as the website end-state contract. The final public site should show the run
assumptions, readiness/capability gates, map status, selected-well audit trail,
temperature-versus-phase intersection plot, result table, scenario controls,
and exports/citations, while explicitly avoiding hydrate-proof, saturation,
sweet-spot, or validated-ML claims.

### 1. Pressure Model

Use hydrostatic pore pressure as the first public-screen assumption. Store the
assumption explicitly so later approved-runtime pressure data can replace it.

```text
pressure_gradient_mpa_per_m = (rho_w_kg_m3 * g_m_s2) / 1,000,000

pressure_mpa_gauge(z) =
    pressure_gradient_mpa_per_m * z_m

pressure_mpa_absolute(z) =
    surface_pressure_mpa + pressure_mpa_gauge(z)
```

Initial public-screen constants:

| Parameter | Value | Notes |
| --- | ---: | --- |
| `rho_w_kg_m3` | `1000.0` | Freshwater first pass. Brine scenarios require a new run ID. |
| `g_m_s2` | `9.80665` | Standard gravity. |
| `pressure_gradient_mpa_per_m` | `0.00980665` | Equivalent to `9.80665 kPa/m`; matches the current scaffold constant. |
| `surface_pressure_mpa` | `0.101325` | Include for phase-curve comparison because phase diagrams use absolute pressure. |

Current scaffold fields such as `hydrostatic_pressure_mpa_at_depth_basis` are
provisional gauge-pressure estimates. The future stability screen should keep
those inputs but add absolute pressure fields used for phase-curve comparison.

Pressure caveats:

- This is not measured formation pressure.
- It ignores overpressure, underpressure, capillary pressure, salinity-density
  effects, gas columns, and pressure communication.
- It should not be used as a producibility or reservoir-pressure result.

### 2. Temperature Model

Use G10015 measured temperature profiles wherever possible, with GGD223 and
OM-222 providing permafrost-depth context.

For a well with a matched representative G10015 profile:

1. Build a depth grid from `0` to `depth_basis_m` using a recorded
   `stable_depth_grid_step_m`, initially `1` to `5 m`.
2. Interpolate measured G10015 temperature over the profile's measured depth
   interval.
3. If the expected phase-boundary base is deeper than the measured profile,
   extrapolate below the deepest measured point using the documented
   `rough_geothermal_gradient_c_per_100m`.
4. Mark every extrapolated boundary with
   `temperature_extrapolated_below_profile = true`.

For a well without a matched G10015 profile:

1. Do not calculate final top/base/thickness in the first implementation.
2. Keep the row as `needs_temperature_profile_match` or
   `temperature_scenario_only`.
3. Later, allow explicit low-confidence scenarios using regional gradients only
   if the website labels them as scenarios rather than calculated results.

Temperature source hierarchy:

| Label | Inputs | Use |
| --- | --- | --- |
| `measured_profile_interpolated` | G10015 profile covers the modeled boundary depth. | Highest-quality public temperature input. |
| `measured_profile_plus_gradient_extrapolation` | G10015 profile plus deepest-window gradient below profile. | Acceptable with caveat if extrapolation distance is recorded. |
| `nearest_profile_same_control_code` | Well joined to representative G10015 profile through nearest GGD223 code. | Current path for the 374 ready rows. |
| `regional_gradient_scenario` | No matching profile; uses regional scenario gradient. | Low-confidence future scenario only. |
| `blocked_no_temperature_model` | No usable temperature control. | No stability result. |

Implemented local helper status:

- `load_g10015_temperature_profile_points(path)` reads numeric depth and
  temperature rows from a G10015-style processed profile file and returns
  sorted `depth_m` / `temperature_c` points.
- `temperature_model_from_profile(...)` returns modeled temperature at requested
  depths only. It does not calculate stability top, base, thickness, occurrence,
  or saturation.
- Inside the measured profile interval, the helper uses linear interpolation
  and marks rows as `measured_profile_interpolated` / `calculated`.
- Below the deepest measured profile point, the helper extrapolates only when a
  numeric `gradient_c_per_100m` is supplied and records
  `temperature_extrapolated_below_profile = true` plus the extrapolation
  distance.
- Below-profile rows without a gradient return
  `blocked_below_profile_no_gradient`; rows above the measured profile range
  return `blocked_above_profile_range`; missing-depth rows return
  `blocked_missing_depth`; empty or unusable profiles return
  `blocked_no_temperature_profile`.

SIR 2008-5175 supports this workflow: it determines GHSZ boundaries by
intersecting measured or extrapolated wellbore temperature profiles with a
theoretical gas hydrate phase boundary, and it notes that below-permafrost
thermal gradients can be treated as nearly constant for many investigated
North Slope wells. Use that as a method anchor, while keeping each extrapolation
visible.

### 3. Methane Hydrate Phase Curve

Use a versioned lookup table, not a hidden fitted equation, for the first
public implementation.

Initial phase-curve assumption:

```text
phase_curve_id = methane_5ppt_sir2008_csmhyd_digitized_v1
phase_curve_role = baseline
phase_curve_allowed_use = official_public_baseline
gas_composition_assumption = 100_percent_methane
gas_methane_mol_pct = 100
gas_ethane_mol_pct = 0
gas_propane_mol_pct = 0
gas_butane_plus_mol_pct = 0
salinity_ppt_assumption = 5
phase_curve_method = pressure-to-equilibrium-temperature lookup with linear interpolation
```

Why this choice:

- USGS SIR 2008-5175 used a theoretical gas hydrate phase boundary generated
  with CSMHYD, assuming 100 percent methane gas and 5 ppt salinity, to estimate
  North Slope GHSZ top and base.
- A lookup table keeps the numeric curve auditable, versioned, and replaceable.
- NETL and USGS public materials make clear that salinity and non-methane gases
  shift the phase boundary, so the curve assumptions must be visible.
- The official baseline should remain 100 percent methane unless the mentor or
  approved runtime data explicitly selects a different curve.
- Mixed-gas curves should be treated as scenario or sensitivity curves until
  the gas composition and curve source are locked.

Required phase-curve artifact before calculation:

```text
data/public_stability_products/phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1.csv
```

Minimum columns:

```text
phase_curve_id
phase_curve_role
pressure_mpa_absolute
equilibrium_temperature_c
gas_composition_assumption
gas_methane_mol_pct
gas_ethane_mol_pct
gas_propane_mol_pct
gas_butane_plus_mol_pct
salinity_ppt_assumption
source_citation
source_extraction_method
source_notes
```

Allowed extraction paths:

- Prefer a published table or machine-readable source if one exists in the
  USGS/CSMHYD/NETL source set.
- If only a figure is available, digitize the curve, record the source image,
  axis calibration, digitizer, date, and maximum estimated extraction error.
- Keep the lookup monotonic in pressure before interpolation.

Current artifact status: the committed first-pass lookup is digitized from
USGS SIR 2008-5175 Figure 1A, the green curve labeled methane and 5 ppt salt
water. Replace it with a direct CSMHYD/CSMGem export if one is obtained, and
increment the lookup ID rather than overwriting this version.

The public products also include
`data/public_stability_products/phase_curve_scenario_catalog_2026-06-14.csv`.
That catalog makes the system variable-capable without implying that every
composition can be freely interpolated. The current official row is the
100-percent-methane baseline above. A second row records the Collett et al.
(2011) / Holder et al. (1987) mixed-gas example
(`98_percent_methane_1p5_percent_ethane_0p5_percent_propane`) as
`source_identified_not_digitized` and `sensitivity_only_not_final`.

Do not calculate top/base/thickness until this table exists, source metadata
remain attached, and tests confirm that interpolation is stable across the
expected pressure range.

### 4. Stability Intersection Rule

For each depth sample `z_m`:

```text
P_abs = pressure_mpa_absolute(z_m)
T_model = temperature_model_c(z_m)
T_eq = phase_curve_equilibrium_temperature_c(P_abs)

is_stable = T_model <= T_eq
```

Then:

```text
stability_top_m =
    shallowest depth where a stable interval begins

stability_base_m =
    deepest depth in the same stable interval before T_model exceeds T_eq,
    or modeled depth limit if the base is not crossed

stability_thickness_m =
    stability_base_m - stability_top_m

well_penetrated_stability_thickness_m =
    max(0, min(stability_base_m, tvd_m) - stability_top_m)

reaches_stability_zone =
    tvd_m >= stability_top_m
```

If the well does not reach the modeled top, set
`reaches_stability_zone = false` and leave penetrated thickness as `0`. If the
temperature model or phase curve does not cover the required range, set
`stability_result_status = not_calculated` and leave all top/base/thickness
fields null.

Implemented local helper status:

- `stability_depth_grid(...)` creates an inclusive depth grid from `0` to the
  modeled depth limit and always includes the modeled limit even when it is not
  an exact multiple of the grid step.
- `stability_condition_grid_from_profile(...)` combines the tested temperature
  model, absolute hydrostatic pressure, and phase-curve equilibrium-temperature
  lookup into per-depth `is_stable` flags.
- `stability_interval_from_condition_grid(...)` finds the first stable interval
  with interpolated top/base crossings for fixture tests only. It returns
  `blocked_incomplete_pressure_temperature_grid` if any grid row lacks a
  calculated temperature or phase-curve value.
- The helper can mark open-below-model bases and temperature extrapolation
  caveats, but no real public `stability_screen_*.csv` has been written.

## Confidence Labels

These labels describe source control for a stability-admissibility screen. They
are not hydrate-confidence labels.

| Label | Required conditions |
| --- | --- |
| `high_source_control` | `TrueVertic` depth; inside a USGS hydrate AU; same-code or very near GGD223/G10015 control; temperature profile covers both top and base intersections or only minor extrapolation; phase lookup applied. |
| `medium_source_control` | `TrueVertic` depth; mapped or nearest permafrost control; G10015 profile match exists but at least one boundary is extrapolated, or the permafrost source is interpolated/digitized rather than same-control. |
| `low_source_control` | Driller total depth fallback, regional gradient scenario, large distance to permafrost/temperature controls, or phase result depends mainly on extrapolation. |
| `blocked_missing_inputs` | Missing vertical depth, coordinates, permafrost context, temperature model, or phase lookup. No stability result. |
| `outside_public_au_context` | Outside current USGS hydrate assessment units. Keep row for inventory, but do not imply hydrate potential from the public screen. |

Suggested numeric flags for later implementation:

| Flag | Initial threshold |
| --- | ---: |
| `near_temperature_control_km` | `<= 5 km` |
| `moderate_temperature_control_km` | `> 5 km and <= 50 km` |
| `large_extrapolation_m` | `> 250 m below measured profile max depth` |
| `minor_extrapolation_m` | `<= 100 m below measured profile max depth` |

Adjust these thresholds only with a documented reason and test update.

Implemented local helper status:

- `stability_source_control_label(...)` assigns
  `high_source_control`, `medium_source_control`, `low_source_control`,
  `blocked_missing_inputs`, or `outside_public_au_context` from fixture rows.
- Tests cover TrueVertic/near-control high confidence, moderate
  extrapolation/distance medium confidence, DrillerTot or large extrapolation
  low confidence, missing temperature blocking, and outside-AU separation.
- These labels are source-control labels only. They are not hydrate-confidence,
  saturation, producibility, or sweet-spot labels.

## Required Caveats For Website And CSV

Every displayed or exported stability result must carry caveat language:

- Stability admissibility is necessary but not sufficient for hydrate presence.
- The screen does not prove hydrate, estimate saturation, or rank sweet spots.
- The public calculation uses public well coordinates/depth fields and public
  regional controls, not approved well-log/core rows.
- Hydrostatic pressure is assumed unless a later approved pressure source is
  explicitly supplied.
- The initial phase curve assumes methane and 5 ppt salinity. Different gas
  composition, pore-water salinity, or inhibitors can shift the stability
  boundary.
- Mixed-gas phase curves are nonlinear thermodynamic scenarios. Do not create a
  freeform gas-composition slider unless the curve is generated by a cited
  hydrate phase model or a source table/figure has been digitized and tested.
- G10015 temperature profiles may require extrapolation beyond measured depths.
- OM-222 is not yet digitized in the public product; nearest GGD223 controls are
  point evidence, not a continuous permafrost-base surface.
- Well depth fields can be measured from different reference datums; public
  `TrueVertic` is preferred but must be checked before approved-runtime use.
- Regional USGS hydrate assessment units are context polygons, not direct
  hydrate detections.

Recommended caveat codes:

```text
hydrostatic_pressure_assumed
phase_curve_methane_5ppt
temperature_profile_extrapolated
temperature_profile_missing
permafrost_point_control_only
om222_not_digitized
driller_total_depth_fallback
outside_usgs_hydrate_au
not_hydrate_proof
```

## Future `stability_screen_*.csv` Schema

The output should be one row per public well per calculation run. Do not reuse a
file name for changed assumptions; create a new dated output and increment
`screen_version`.

| Column | Type | Required | Meaning |
| --- | --- | --- | --- |
| `screen_run_id` | string | yes | Stable ID for the calculation run, for example `stability_screen_2026_06_14_methane_5ppt_v1`. |
| `screen_version` | string | yes | Version of the schema and assumptions. |
| `object_id` | integer | yes | Alaska DNR public well object ID when available. |
| `permit_number` | string | yes | Public permit number from the well source. |
| `api_number` | string | yes | Public API number when available. |
| `well_name` | string | yes | Public well name from the DNR source. |
| `field` | string | no | Public field value. |
| `pool` | string | no | Public pool value. |
| `lat` | float | yes | Wellhead latitude used for public spatial join. |
| `lon` | float | yes | Wellhead longitude used for public spatial join. |
| `tvd_m` | float | conditional | Vertical depth used for pressure and reach tests. |
| `depth_source` | string | yes | `TrueVertic`, `DrillerTot`, or approved-runtime source. |
| `depth_basis_ft` | float | no | Original public depth in feet when available. |
| `depth_reference_note` | string | yes | Datum/reference caveat for public depth field. |
| `hydrate_assessment_codes` | string | no | USGS hydrate AU codes joined to the well. |
| `within_hydrate_assessment_unit` | boolean | yes | Public AU context flag. |
| `permafrost_base_m` | float | conditional | Base of ice-bearing permafrost or nearest control depth. |
| `permafrost_source` | string | conditional | `GGD223 nearest control`, `OM-222 digitized`, or scenario label. |
| `permafrost_control_code` | string | no | GGD223 code used for nearest-control context. |
| `permafrost_control_distance_km` | float | no | Distance from well to permafrost control. |
| `permafrost_confidence` | string | yes | Source-control label for permafrost context. |
| `temperature_model_id` | string | conditional | Versioned temperature model identifier. |
| `temperature_source` | string | conditional | G10015 profile, extrapolated profile, regional scenario, or blocked. |
| `temperature_profile_code` | string | no | G10015/GGD223-style code used for profile match. |
| `temperature_profile_file` | string | no | Representative profile file name when available. |
| `temperature_profile_max_depth_m` | float | no | Deepest measured profile depth. |
| `temperature_gradient_c_per_100m` | float | conditional | Gradient used below measured profile. |
| `temperature_gradient_source` | string | conditional | Deepest-window, regional median, scenario, or none. |
| `temperature_extrapolated_below_profile` | boolean | yes | Whether a boundary or result depends on extrapolated temperature. |
| `temperature_extrapolation_below_profile_m` | float | no | Maximum extrapolation distance used in the result. |
| `temperature_model_confidence` | string | yes | Source-control label for temperature model. |
| `pressure_model_id` | string | yes | Versioned pressure equation identifier. |
| `pressure_source` | string | yes | Hydrostatic assumption or measured pressure source. |
| `pore_fluid_density_kg_m3` | float | yes | Density used in pressure equation. |
| `gravity_m_s2` | float | yes | Gravity used in pressure equation. |
| `surface_pressure_mpa` | float | yes | Atmospheric/surface pressure added for absolute pressure. |
| `pressure_gradient_mpa_per_m` | float | yes | Hydrostatic pressure gradient. |
| `pressure_at_tvd_mpa_absolute` | float | conditional | Absolute pressure at `tvd_m`. |
| `phase_curve_id` | string | conditional | Versioned phase lookup ID. |
| `phase_curve_role` | string | yes | `baseline`, `sensitivity_candidate`, `approved_runtime`, or another documented role. |
| `phase_curve_allowed_use` | string | yes | Initial value: `official_public_baseline`; scenario values must say when they are sensitivity-only. |
| `phase_curve_source` | string | conditional | Citation/path for lookup source. |
| `gas_composition_assumption` | string | conditional | Initial value: `100_percent_methane`. |
| `gas_methane_mol_pct` | float | conditional | Methane mole percent for the selected curve. |
| `gas_ethane_mol_pct` | float | conditional | Ethane mole percent for the selected curve. |
| `gas_propane_mol_pct` | float | conditional | Propane mole percent for the selected curve. |
| `gas_butane_plus_mol_pct` | float | conditional | Butanes-and-heavier mole percent when the selected curve requires it. |
| `salinity_ppt_assumption` | float | conditional | Initial value: `5`. |
| `phase_curve_status` | string | yes | `not_applied`, `applied`, or `blocked_missing_lookup`. |
| `stable_depth_grid_step_m` | float | conditional | Depth-grid resolution for intersection search. |
| `stability_top_m` | float | conditional | Top of modeled stable interval; null if not calculated. |
| `stability_top_pressure_mpa_absolute` | float | no | Absolute pressure at modeled top. |
| `stability_top_temperature_c` | float | no | Modeled temperature at top. |
| `stability_base_m` | float | conditional | Base of modeled stable interval; null if not calculated. |
| `stability_base_pressure_mpa_absolute` | float | no | Absolute pressure at modeled base. |
| `stability_base_temperature_c` | float | no | Modeled temperature at base. |
| `stability_thickness_m` | float | conditional | Modeled stability interval thickness. |
| `well_penetrated_stability_thickness_m` | float | conditional | Modeled stable thickness actually reached by public well depth. |
| `reaches_stability_zone` | boolean | conditional | Whether the public well depth reaches the modeled top. |
| `top_boundary_method` | string | no | Interpolated, extrapolated, scenario, or not calculated. |
| `base_boundary_method` | string | no | Interpolated, extrapolated, scenario, open below model, or not calculated. |
| `stability_result_status` | string | yes | `not_calculated`, `calculated`, `outside_au_context`, or blocked reason. |
| `stability_confidence` | string | yes | Overall source-control label. |
| `caveat_codes` | string | yes | Semicolon-separated caveat codes. |
| `stability_notes` | string | yes | Short public-safe explanation of limitations. |

## Implementation Gates

Do these before creating a non-empty `stability_screen_*.csv`:

1. Keep the input capability matrix current and tested.
2. Keep the phase-curve lookup artifact source metadata complete and tested.
3. Add pressure-equation tests, including absolute versus gauge pressure.
4. Add phase-curve interpolation tests across the expected pressure range.
5. Add temperature-model tests for interpolation, extrapolation, and blocked
   rows.
6. Add depth-grid and boundary-crossing tests for closed intervals, open bases,
   and blocked incomplete pressure-temperature grids.
7. Add confidence-label tests that preserve the guardrail that stability is not
   hydrate proof.
8. Build the real public temperature-model product from the full OSL/source
   bundle before applying the interval helper to public rows.
9. Update the Structural Explorer to show the run ID, phase-curve source,
   pressure assumption, confidence label, and caveat codes beside any result.

Current implementation status:

- Gates 1 through 7 now have local code/tests for the public input contract,
  absolute/gauge pressure helpers, phase-curve lookup interpolation, and
  fixture-based G10015 temperature interpolation/extrapolation behavior,
  depth-grid construction, stable-interval crossing, open-base handling, and
  blocked incomplete-grid behavior, plus source-control confidence labels.
- The real public temperature-model product still requires the full
  OpenScienceLab/source bundle because raw G10015 profile rows are not committed
  to Git.
- Real OSL-derived temperature-model products, a guarded public
  `stability_screen_*.csv` writer, and website result display remain required
  before any non-null public stability top/base/thickness output is written.
- The OSL rebuild script now has a guarded temperature-model writer that emits
  `stability_temperature_model_2026-06-14.csv` and its summary only when raw
  G10015 profile `.txt` rows are available in the active source bundle. This is
  a temperature-input product, not a stability-screen result.

Until those gates are complete, the public scaffold remains an input scaffold:
`phase_curve_status = not_applied` and
`stability_top_base_thickness_status = not_calculated`.
