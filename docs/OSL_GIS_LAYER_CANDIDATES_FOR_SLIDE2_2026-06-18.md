# OSL GIS Layer Candidates For Slide 2 - 2026-06-18

## Why This Note Exists

The previous Slide 2 map was a public well/seismic orientation map generated from existing project layers. It was useful as a locator, but it was not the geologic GIS layer the slide needs for a geoscience-facing North Slope context panel.

Slide 2 should use a real public geology layer where possible, then keep the well/seismic orientation map as a fallback or secondary website view.

## Recommended First OSL Upload

**Herriott et al. 2018, Alaska DGGS RI 2018-6**

- Title: Geologic map of the Umiat-Gubik area, central North Slope, Alaska
- DOI: `10.14509/30099`
- Source page: `https://dggs.alaska.gov/pubs/id/30099`
- Project page: `https://dggs.alaska.gov/pubs/project/868`
- Metadata: `https://dggs.alaska.gov/webpubs/metadata/RI2018-6.faq.html`
- Shapefile package: `https://dggs.alaska.gov/webpubs/data/ri2018_006_umiat_gems_shapefile_pkg.zip`
- Size checked locally: about `1.16 MB`
- Local review-only unpacked path: `docs/evidence/slide02_source_bundle_2026_06_17/gis_sources_local_only/`

Use this first because it is North Slope specific, compact, and contains the right geoscience-facing layers:

- `GM_MapUnitPolys`: geologic map units
- `GM_ContactsAndFaults`: contacts and faults
- `GM_GeologicLines`: key beds and geologic linework
- `GM_StructureLines`: fold axes, including Umiat/Gubik structural labels
- `GM_Stations`: field stations
- `DescriptionOfMapUnits.csv`: map-unit names, ages, descriptions, colors

Current derived preview assets:

- Slide-ready map: `docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_11_dggs_umiat_gubik_geology_layer_slide_map.png`
- Handoff preview with legend: `docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_10_dggs_umiat_gubik_geology_layer_preview.png`

Guardrail: this is geology context only. It is not hydrate occurrence, saturation, validation, or a model output.

## Prepared OSL Upload Package

A local OSL-ready package has been prepared at:

```text
osl_upload_packages/slide2_north_slope_geology_osl_upload_2026_06_18.zip
```

Status: user reported the OSL upload step complete on 2026-06-18. The GitHub
website side now points to the public-safe DGGS-derived preview and source
handoff notes; the raw public GIS package remains an OSL/source-library asset.

Recommended OSL destination:

```text
data/source_library/slide2_north_slope_geology_2026_06_18/
```

Package contents:

- `00_README_OSL_UPLOAD.md`: upload and use instructions
- `source_manifest_slide2_gis_2026_06_18.csv`: source manifest
- `file_manifest_sha256.csv`: checksum manifest
- `01_raw_public_sources/ri2018_006_umiat_gems_shapefile_pkg.zip`
- `01_raw_public_sources/ri2018_006_umiat_ak_gems_db_pkg.zip`
- `02_preview_assets/`: derived slide/OSL preview PNGs
- `03_osl_loader/preview_dggs_umiat_gubik_layer.py`: quick OSL extraction/preview script
- `04_source_metadata/`: DGGS metadata and USGS statewide fallback metadata
- `05_extracted_working/` and `06_osl_preview_outputs/`: tested local extraction and preview outputs

The loader was tested locally with:

```bash
python 03_osl_loader/preview_dggs_umiat_gubik_layer.py
```

It extracted the DGGS layers, wrote `06_osl_preview_outputs/dggs_umiat_gubik_layer_summary.csv`, and wrote `06_osl_preview_outputs/dggs_umiat_gubik_quick_preview.png`.

## Statewide Fallback Layer

**Wilson, Hults, Mull, and Karl 2015, USGS SIM 3340**

- Title: Geologic map of Alaska
- DOI: `10.3133/sim3340`
- USGS source page: `https://pubs.usgs.gov/publication/sim3340`
- Detailed metadata: `https://pubs.usgs.gov/sim/3340/sim3340_detailed.html`
- Statewide shapefile package: `https://pubs.usgs.gov/sim/3340/sim3340_shp.zip`
- Size checked locally by HTTP HEAD: about `711 MB`
- ArcGIS item: `https://www.arcgis.com/home/item.html?id=54a186063939411c8eef46cef42dab19`
- FeatureServer: `https://services.arcgis.com/v01gqwM5QqNysAAi/arcgis/rest/services/Geologic_map_of_Alaska_FeatureLayer/FeatureServer`
- Useful layers verified:
  - `5`: Contacts and Faults
  - `6`: Geologic Units

Use this when the website needs a statewide Alaska/North Slope geologic base layer. It is heavier than the DGGS Umiat-Gubik package and should be clipped/simplified before being used in a slide or Streamlit panel.

## Website Update Path

1. Upload the DGGS RI 2018-6 shapefile package to OpenScienceLab as a public source layer.
2. In OSL, load `GM_MapUnitPolys`, `GM_ContactsAndFaults`, `GM_GeologicLines`, and `GM_StructureLines`.
3. Export a simplified public-safe derived layer or static PNG for the website.
4. Add the layer to `Explore North Slope > Regional Map` as a geology-layer view.
5. Keep the current public well/seismic orientation map as a separate view, not the geology-layer substitute.
6. If the mentor wants a broader statewide context, add the USGS SIM 3340 FeatureServer/geologic units layer as a separate OSL/website option.

## Slide 2 Decision

Use the DGGS Umiat-Gubik geology preview in the current Slide 2 North Slope panel. It better matches the requested geoscience layer than the generated well/seismic map. Keep the prior website-generated map as fallback provenance only.
