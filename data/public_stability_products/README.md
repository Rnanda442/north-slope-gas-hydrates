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
