# Public Stability Products

This folder stores derived, public-safe outputs created from public North Slope
sources. It is intentionally different from `data/source_library/`, which is
the ignored local folder for raw bundles, PDFs, shapefiles, and large source
downloads.

## Current Product

`north_slope_well_stability_context_2026-06-14.csv`

This table combines:

- Alaska DNR Well Bottom Hole Location records filtered to
  `Geographic = ARCTIC SLOPE`;
- NSIDC GGD223 permafrost-depth controls parsed from `stnlist.dat`;
- USGS 2019 Northern Alaska gas hydrate assessment unit polygons.

The output is a context layer for public discussion and website visualization.
It is not a gas hydrate prediction, not a saturation result, and not a full
pressure-temperature stability-zone calculation.

`g10015_temperature_profile_inventory_2026-06-14.csv`

This table summarizes public NSIDC G10015 processed borehole temperature logs.
It stores per-file metadata, depth/temperature ranges, deepest temperature, and
a rough deepest-window temperature-gradient context estimate. It does not
replace a calibrated geothermal model.

`g10015_temperature_profile_points_sampled_2026-06-14.csv`

`g10015_temperature_profile_points_sampled_summary_2026-06-14.csv`

These OpenScienceLab-derived products are prepared for the next rebuild. They
export sampled measured G10015 depth/temperature points, up to 160 points per
profile, for website temperature-curve visualization. They are public G10015
curve context only, not a stability result, saturation result, or calibrated
geothermal model.

`stability_input_scaffold_2026-06-14.csv`

This table is the next-step input scaffold for future stability calculations.
It joins the public well context product to the compact G10015 inventory through
the nearest GGD223 control code, then adds a provisional hydrostatic pressure
estimate:

```text
pressure_mpa_gauge = depth_m * 0.00980665
pressure_mpa_absolute = 0.101325 + pressure_mpa_gauge
```

This is a convenience scaffold, not a final stability result. It intentionally
keeps `phase_curve_status = not_applied` and
`stability_top_base_thickness_status = not_calculated`.

`phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1.csv`

This table is the first cited methane hydrate pressure-temperature lookup for
the public stability workflow. It is digitized from USGS SIR 2008-5175 Figure
1A, using the curve labeled for methane and 5 ppt salt water. It is an
auditable lookup input, not a fitted equation and not a final stability result.
Replace it with a direct CSMHYD/CSMGem export if one becomes available, using a
new versioned file name.

`phase_curve_scenario_catalog_2026-06-14.csv`

This table records which phase-curve scenarios are allowed to be selected. The
current official baseline is the mentor-approved 100 percent methane curve from
USGS SIR 2008-5175. A mixed-gas Alaska North Slope source is also recorded from
Collett et al. (2011), modified from Holder et al. (1987), but it is marked as
`source_identified_not_digitized` and `sensitivity_only_not_final`. Do not use a
mixed-gas curve for final stability until it has a versioned lookup or a cited
thermodynamic-model export.

`stability_input_capability_matrix_2026-06-14.csv`

This table records what each current input can support now, what remains
scenario-only, and what must wait for approved runtime data. It is the guardrail
between public stability screening and future ML claims: public well/depth,
GGD223, G10015, hydrostatic pressure, and the 100 percent methane phase curve
can support a baseline screen, while mixed-gas chemistry, well-specific salinity,
and approved log/core labels remain future or sensitivity inputs.

`stability_osl_pull_triggers_2026-06-14.csv`

This table records when the public repository is enough and when the full
OpenScienceLab/source bundle is required. Temperature-model logic can be built
with unit-test fixtures in Git, but real public temperature-model products need
the raw G10015 profile rows from the full source bundle because Git commits only
the compact inventory.

`stability_temperature_model_2026-06-14.csv`

`stability_temperature_model_summary_2026-06-14.csv`

These OpenScienceLab-derived products model temperature at key scaffold depths
from the public G10015 processed profile rows. They are temperature-input
products only. They do not assert hydrate occurrence and do not by themselves
calculate stability top, base, or thickness.

`stability_screen_2026-06-14_methane_5ppt_v1.csv`

`stability_screen_summary_2026-06-14_methane_5ppt_v1.csv`

These OpenScienceLab-derived products are the first guarded baseline methane
5 ppt stability-admissibility screen. The run has 8,084 public scaffold rows,
22 calculated baseline intervals, 8 rows where no stable interval was found,
and 8,054 blocked rows. Blocked rows keep top/base/thickness null. Every row
keeps `not_hydrate_proof` in `caveat_codes`.

`public_ml_feature_scaffold_2026-06-15.csv`

`public_ml_feature_scaffold_summary_2026-06-15.csv`

`public_ml_feature_dictionary_2026-06-15.csv`

These derived products convert the guarded public stability products into a
future-ML feature and coverage scaffold. The scaffold has one row per public
well, joins public well/depth/AU/permafrost/temperature/pressure/phase-curve
context, and carries the baseline stability-screen status as a physics-derived
feature. It has 8,084 rows, 483 rows with matched G10015 temperature context,
22 rows with calculated baseline stability-interval features, 8 rows with no
stable interval under the baseline run, and 0 validated hydrate occurrence or
saturation labels. It is not training data and must not be used as a hydrate
present/absent label, saturation target, producibility result, or sweet-spot
ranking.

`public_ml_target_registry_2026-06-15.csv`

`public_ml_leakage_guardrails_2026-06-15.csv`

These public schema/policy products preserve the workbook/screenshot target
headers and lock the target-only rule. `Sgh`, `S_h`, `Sh`, `NMR_SAT`,
`Hydrate Saturation`, `Swr`, `S_wr`, and interpreted phase labels are targets,
calibration references, or outputs, not input predictors. They remain
header/schema evidence only in the public repo: no approved target rows are
committed. The leakage guardrails require the saturation/label family to stay
out of the feature matrix, require whole-well splitting before model fitting,
and block ad hoc occurrence labels from stability, resistivity alone, or final
rankings.

`stability_website_product_spec_2026-06-14.csv`

This table defines the intended final website shape for the public stability
screen: status strip, readiness/capability tables, map view, well detail panel,
temperature-phase plot, results table, scenario controls, and export/citation
area. Each row also states what that website area must not claim.

The source-backed calculation contract for `stability_screen_*.csv` lives in
`docs/STABILITY_CALCULATION_PLAN.md`. The current baseline screen writes
non-null top/base/thickness only where the pressure, temperature, phase-curve,
intersection, and source-control gates pass.

The local code now includes fixture-tested temperature-model helpers in
`dashboard/stability_products.py`. These helpers parse G10015-style profile
points, interpolate within measured profile depth, extrapolate below measured
depth only when a numeric gradient is supplied, and return explicit blocked
statuses when inputs are insufficient. They are not a real public temperature
model product until the raw G10015 profile rows are rebuilt from the full
OpenScienceLab/source bundle.

The same module now includes fixture-tested stability depth-grid and
intersection helpers. They can combine modeled temperature, absolute
hydrostatic pressure, and the methane phase lookup for synthetic test cases,
and they now support the guarded OSL-generated public stability screen. No
committed product in this folder is hydrate proof, saturation evidence, or a
producibility result.

Fixture-tested source-control confidence labels also exist for stability-screen
rows. They separate high, medium, low, blocked, and outside-AU source control.
They do not label hydrate occurrence, saturation, reservoir quality, or sweet
spots.

The OSL rebuild pipeline is now prepared to write the sampled G10015 profile
points product plus
`stability_temperature_model_2026-06-14.csv` and
`stability_temperature_model_summary_2026-06-14.csv` when the full source
bundle contains raw G10015 processed profile `.txt` files. The temperature
model product is one row per scaffold well per key modeled depth, currently
nearest permafrost control depth and well depth. It remains a temperature-input
product only and keeps top/base/thickness uncalculated.

G10015 source profiles can contain duplicate depth rows. The public parser now
averages temperature values at repeated depths before interpolation so a single
source-file duplicate does not stop the OSL rebuild.

The guarded stability-screen writer has been run in OSL, where raw G10015
profile rows are available. It fills top/base/thickness only for rows passing
all calculation gates and leaves blocked rows null.

## Assessment Unit Codes

| Code | Name |
| --- | --- |
| `50010201` | Sagavanirktok Formation Gas Hydrate |
| `50010202` | Tuluvak-Schrader Bluff-Prince Creek Formations Gas Hydrate |
| `50010203` | Nanushuk Formation Gas Hydrate |

## Key Caveat

`public_context_candidate` means the wellhead is inside a USGS hydrate
assessment unit and the selected public well-depth field is deeper than the
nearest GGD223 permafrost-depth control. This is a first-pass admissibility
context only. The current baseline screen adds public temperature, pressure,
and phase-curve gates, but it still is not hydrate proof. Final interpretation
still needs local permafrost-base surfaces or digitized OM-222 evidence,
well-specific temperature/pressure calibration, and direct hydrate evidence.

The G10015 gradient field is calculated from the deepest 100 m of each
available profile where enough samples exist. Use it as temperature context only
until a proper well-specific geothermal model is built.

The stability scaffold is ready for the next phase-curve step only where it has
public AU membership, public well depth, nearest GGD223 permafrost context, and
a matching G10015 temperature profile. Rows without a profile match remain
useful for inventory and gap analysis, not calculation.
