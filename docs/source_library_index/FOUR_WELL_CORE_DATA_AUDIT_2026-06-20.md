# Four-Well Core Data Audit

Date: 2026-06-20

Purpose: identify which of the four current well/source cases have usable core
or pressure-core evidence in the project source set, Google Drive source set, or
public web sources. This file is a source-audit note only. It does not add raw
core rows, restricted workbook rows, model labels, or approved runtime data.

Four focused cases:

- MTE / Mount Elbert
- IGS / Ignik Sikumi
- Hydrate-01
- HYDRATE 02

## Short Answer

We do not have one clean local spreadsheet that contains row-level core data for
all four wells. The local `UNIFIED_CORE...xlsx` files in Downloads were checked
and are unrelated Mountain Pass / Bayan Obo mineral tables.

What we do have:

- Strong public/source evidence for Mount Elbert core and core-log montage data.
- Strong log/NMR and field-test evidence for Ignik Sikumi, but core-data
  availability remains unresolved until the full field-experiment paper/report
  or supplement is checked.
- Strong Hydrate-01 sidewall pressure-core evidence, including public NETL
  summary values and measurements.
- Strong HYDRATE 02 pressure-core evidence from the Drive Yoneda et al. 2026
  PDF and a public ACS Figshare supplement.

Most important correction: Chong et al. (2022) is the right ML/well list anchor,
but it is not the raw core table. It points to the core papers and uses
NMR-density-derived `Sgh` as the ML target for the ANS wells.

## Well-by-Well Status

| case | public well/source anchor | core-data status | what we can use now | source trail | action |
|---|---|---|---|---|---|
| MTE / Mount Elbert | `MT ELBERT 1`, API `50029233020000` | Confirmed core and log-core montage source exists. Row-level core table is not in the current repo. | Core/log montage evidence, porosity and hydrate-saturation calibration context, Mount Elbert coring/sedimentology source trail. | USGS Mount Elbert overview and USGS Mount Elbert downhole well-log/core montage page. Chong et al. 2022 cites the Mount Elbert core/coring papers. | Retrieve or keep citation to Collett et al. 2011 core montage and Rose et al. 2011 coring operations if we need tables/figures. |
| IGS / Ignik Sikumi | `PRUDHOE BAY UN IGNIK SIKUMI 1`, API `50029234430000` | Log/NMR target data is confirmed. I did not find a local row-level core table or a public page with core rows. | Use as a log/NMR-derived `Sgh` calibration/ML well. Treat core data as "needs full paper/report confirmation" before claiming actual core rows. | Chong et al. 2022 and Singh et al. 2021 use Ignik logs/NMR. USGS/ACS field experiment page and NETL field-trial review document support the field-test/log context, not a raw core table. | Get the full Boswell et al. 2017 Energy & Fuels paper/report or supplement and search for core tables, sedimentology, and geochemistry details. |
| Hydrate-01 | `HYDRATE 01`, API `50029236130000`; associated `KUPARUK ST 7-11-12` source context | Confirmed sidewall pressure-core source. Raw rows remain source/restricted, but public core-analysis summaries are available. | Sidewall pressure-core recovery counts, Unit B/D lithology, porosity, hydrate saturation, intrinsic/effective permeability, NMR T2, X-CT/XRD, triaxial strength, and thermal/core-property context. | USGS Hydrate-01 scientific results page; NETL/Yoneda ICGH10 sidewall pressure-core PDF; Chong et al. 2022 notes Hydrate-01/Kuparuk 7-11-12 and sidewall core analysis. | Keep using Hydrate-01 as a pressure-core/log calibration case, but do not expose row-level core rows without approved source/runtime access. |
| HYDRATE 02 | `HYDRATE 02`, API `50029237280000`; associated production wells `HYDRATE P1`/`HYDRATE P2` | Confirmed pressure-core source for the HYDRATE 02 Geo Data Well. Drive has a full Yoneda et al. 2026 PDF; public ACS Figshare supplement is available. | Pressure-core sample metadata, B1/D1 reservoir/seal context, grain size, mineralogy, petrophysical/geochemical data, NMR T2, permeability/producibility context, and core-log calibration support. | Drive: Yoneda et al. 2026 NMR/permeability PDF. Web: ACS Figshare supplement for HYDRATE 02 core analyses. Aung et al. 2026 Drive PDF supports LWD/well roles. | Pull/download the Figshare supplement or obtain Phillips/Haines/Hiruta/Collett 2026 papers if we need complete core-analysis tables. |

## Chong et al. 2022 Role

Chong et al. (2022), `s10596-022-10151-9.pdf`, is the direct ML anchor for
permafrost-associated hydrate saturation prediction. It says the ML database
uses LWD/wireline logs from five wells/sites:

- Mount Elbert
- Ignik Sikumi
- Kuparuk 7-11-12 / Hydrate-01 context
- Mallik 2L-38
- Mallik 5L-38

The study uses well-log features such as density, density porosity, gamma ray,
resistivity, compressional velocity, and shear velocity, with NMR-density
derived `Sgh` as the target. That makes it highly relevant for the ML workflow,
but it is not the place to get full raw core rows.

## Local File Checks

Checked local project sources:

- `references/ml-sources/2026-06-11/s10596-022-10151-9.pdf`
- `references/hydrate-ml-physics-sources/2026-06-13/singh_seol_myshakin_2021_prediction_gas_hydrate_saturation_ml_optimal_well_logs_osti.pdf`
- `references/hydrate-ml-physics-sources/2026-06-13/source_manifest.csv`
- `references/hydrate-ml-physics-sources/2026-06-13/google_drive_uploaded_sources_2026_06_13.md`
- `data/public_ml_products/four_well_case_location_index_2026-06-19.csv`

Checked local Downloads spreadsheets with misleading names:

- `UNIFIED_CORE_ROWBYGettingthhere5more.xlsx`
- `UNIFIED_CORE_ROWBYGettingthhere5morecleanedup.xlsx`
- `UNIFIED_CORE_ROWBYGettingthhere5morecleanedup (version 1).xlsb.xlsx`
- `UNIFIED_CORE_ROWBYGettingthhere5morecleanedup_GROUPED.xlsx`
- `UNIFIED_CORE_ROWBYGettingthhere5morecleanedup_GROUPED (1).xlsx`
- `UNIFIED_CORE_ROWBY_MINERAL_BO_FILLED_v3_APPENDED85clean.xlsx`

Those workbooks are not North Slope gas-hydrate core workbooks. They contain
Mountain Pass / Bayan Obo rare-earth/mineral tables and did not match MTE,
Ignik, Hydrate-01, HYDRATE 02, Kuparuk, P1, or P2.

## Priority Missing / Next Sources

Highest value if the user can provide or we can retrieve them:

1. Phillips, Waite, Yoneda, Haines, Hiruta, Holland, Schultheiss, and Collett
   2026, lithological control of gas hydrate saturation from pressure-core
   analysis, HYDRATE 02 Geo Data Well.
2. Haines 2026, physical-property measurements linking pressure core and LWD at
   the Alaska North Slope gas hydrate production test site.
3. Collett et al. 2026, HYDRATE 02 Geo Data Well logging, pressure coring, and
   completion operations.
4. Hiruta/Yoneda 2026 HYDRATE 02 sedimentology and geochemistry main article
   and supplement.
5. Boswell et al. 2017 full Ignik Sikumi field-experiment article or final
   technical report for core-analysis details.
6. Rose et al. 2011 Mount Elbert coring operations, core sedimentology, and
   lithostratigraphy, plus Collett et al. 2011 Mount Elbert log/core montage.

## Public Source Links

- Chong et al. 2022 OSTI PDF: <https://www.osti.gov/servlets/purl/1888241>
- USGS Mount Elbert overview: <https://pubs.usgs.gov/publication/70035868>
- USGS Mount Elbert log/core montage: <https://pubs.usgs.gov/publication/70036047>
- USGS Ignik Sikumi field experiment page: <https://pubs.usgs.gov/publication/70179681>
- NETL Ignik Sikumi field-trial review PDF: <https://netl.doe.gov/sites/default/files/netl-file/nt0006553-field-trial-review.pdf>
- USGS Hydrate-01 scientific results page: <https://pubs.usgs.gov/publication/70251258>
- NETL/Yoneda Hydrate-01 sidewall pressure-core PDF: <https://netl.doe.gov/sites/default/files/2020-08/Yoneda-et-al-Sidewall-Pressure-Cores.pdf>
- ACS Figshare HYDRATE 02 core-analysis supplement: <https://acs.figshare.com/articles/journal_contribution/Sedimentology_and_Geochemistry_of_Gas_Hydrate-Bearing_Sands_in_the_Greater_Prudhoe_Bay_Area_Alaska_North_Slope_Insights_from_HYDRATE-02_Geo_Data_Well_Core_Analyses/31437106>
