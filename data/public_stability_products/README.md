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
a rough deepest-window temperature-gradient context estimate. It does not store
the raw profile rows and does not replace a calibrated geothermal model.

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
context only. A real stability product still needs local permafrost-base
surfaces or digitized OM-222 evidence, geothermal-gradient/temperature context,
pressure assumptions, and a methane hydrate phase curve.

The G10015 gradient field is calculated from the deepest 100 m of each
available profile where enough samples exist. Use it as temperature context only
until a proper well-specific geothermal model is built.
