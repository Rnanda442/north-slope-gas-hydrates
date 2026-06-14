# North Slope Stability Public Snapshot - 2026-06-13

This folder is a small, Git-safe fallback for the Structural Explorer stability
panel. It lets the public Streamlit website show real stability-context layers
when the full OpenScienceLab source bundle is not present.

## Included Files

| File | Source | Use |
| --- | --- | --- |
| `ggd223_permafrost_controls.csv` | Parsed from NSIDC GGD223 `stnlist.dat`. | Point controls with latitude, longitude, elevation, and `permafrost_depth_m`. |
| `GasHydrateAUs.geojson` | USGS 2019 Northern Alaska gas hydrate assessment units. | Regional hydrate assessment-unit overlay. |

## What This Is Not

This snapshot is not the full source bundle and is not a hydrate prediction.
It supports a stability-admissibility map: where hydrate could be
thermodynamically plausible, not where hydrate is proven or saturated.

Use the full local bundle at
`data/source_library/north_slope_stability_sources_2026-06-13/` for G10015
temperature profiles, OM-222 source-plate evidence, full Alaska DNR well package
files, and source PDFs.
