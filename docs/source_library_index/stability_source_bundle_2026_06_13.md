# Stability Source Bundle - 2026-06-13

This file records the local public-source bundle prepared for the
OpenScienceLab Structural Explorer stability layer. The raw files are not
committed to Git because they are downloaded source assets and should be
uploaded into the authorized runtime environment as local reference data.

## Local Bundle

- Laptop folder:
  `C:\Users\gargi\Downloads\north_slope_stability_sources_2026-06-13`
- Upload zip:
  `C:\Users\gargi\Downloads\north_slope_stability_sources_2026-06-13_UPLOAD_TO_OPENSCIENCE.zip`
- Approximate zip size: `71.6 MB`
- Recommended OpenScienceLab target:
  `data/source_library/north_slope_stability_sources_2026-06-13/`

After uploading, unzip the bundle inside the Streamlit project and keep the
folder name unchanged so setup scripts and source notes can use stable paths.

## What The Bundle Contains

| Folder | Source contents | Stability use |
| --- | --- | --- |
| `01_wells_public/` | Alaska DNR Well Bottom Hole Location shapefile package copied from the local public source package. | Well locations, public depth fields, `TrueVertic`, and `DrillerTot`. |
| `02_permafrost_base/` | USGS OM-222 oversized plate PDF for base of deepest ice-bearing permafrost. | Primary base-of-ice-bearing-permafrost evidence; needs georeferencing or digitizing before GIS use. |
| `03_temperature_geothermal/` | NSIDC G10015 borehole temperatures, NSIDC GGD223 raw FTP files, GGD223 user guide/metadata, USGS OFR 82-1039, USGS OFR 82-535. | Temperature profiles, geothermal-gradient context, and permafrost-depth control points. |
| `04_hydrate_assessment_units/` | USGS 2019 Northern Alaska gas hydrate assessment unit files, including `GasHydrateAUs.geojson`, GDB zip, forms, and input spreadsheets. | Regional hydrate assessment unit overlays and well-to-AU context. |
| `05_stability_method_phase/` | USGS SIR 2008-5175, USGS DDS-69-CC CD-ROM zip, and ScienceBase stability-zone reference image. | Stability method, hydrate prospect framing, and published P-T/regional assessment support. |
| `06_optional_context/` | USGS offshore/subsea permafrost catalog page. | Optional offshore context only; not the main onshore base-of-permafrost source. |

## Important Download Result

NSIDC GGD223 is now downloaded. The NSIDC page routes to an FTP file system:

`ftp://sidads.colorado.edu/pub/DATASETS/fgdc/ggd223_boreholes_alaska/`

The downloaded local folder contains `305` files. The most immediately useful
file is:

`03_temperature_geothermal/NSIDC_GGD223_raw_ftp/stnlist.dat`

`stnlist.dat` includes well designation, code, latitude, longitude, elevation,
and `pf_depth` in meters. Treat it as a permafrost-depth control source, not as
the main well inventory. The main well inventory remains the Alaska DNR well
bottom-hole shapefile.

## Structural Explorer Setup Order

1. Upload and unzip the source bundle into:
   `data/source_library/north_slope_stability_sources_2026-06-13/`
2. Confirm that `source_ledger.csv` is present in the unzipped bundle.
3. Load the Alaska DNR shapefile as the public well/depth layer.
4. Parse `NSIDC_GGD223_raw_ftp/stnlist.dat` into point features with
   `pf_depth_m`.
5. Load `GasHydrateAUs.geojson` as the hydrate assessment unit overlay.
6. Load or reference G10015 borehole temperature files for temperature-control
   confidence and geothermal-gradient context.
7. Keep OM-222 as a source plate until its permafrost-base evidence is
   georeferenced or digitized.
8. Add labels that clearly say the result is a stability admissibility screen,
   not hydrate proof and not saturation prediction.

## Future Explorer Fields

The public-safe explorer table should eventually support:

```text
well_id
lat
lon
tvd_m
depth_source
permafrost_base_m
permafrost_source
geothermal_gradient_c_per_100m
temperature_source
pressure_gradient_kpa_m
pressure_source
phase_curve_source
stability_top_m
stability_base_m
stability_thickness_m
reaches_stability_zone
stability_confidence
stability_notes
```

## Git Boundary

Commit this source map and code that reads the public files. Do not commit the
downloaded source bundle itself unless a future decision is made to vendor a
small, license-safe subset.
