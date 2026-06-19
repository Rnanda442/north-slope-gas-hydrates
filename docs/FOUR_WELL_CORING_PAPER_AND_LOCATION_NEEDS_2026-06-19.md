# Coring Paper and Well-Location Needs

Created: 2026-06-19

## Purpose

This note lists the papers/source files still needed locally for the coring,
core-property, NMR, lithology, and pressure-core evidence tied to the North
Slope wells currently visible in public project products and screenshot/source
evidence. It also records the public well-location rows already found locally.

Boundary: the location values below are public scaffold/source-context rows,
not approved private runtime data. Do not treat them as approved training rows,
hydrate labels, or confidential OSL values.

Important 2026-06-19 correction: do not finalize this as a strict four-well
set until the original workbook/screenshot source is checked for `MLK` and
probable `EIT` / `E1T` / `ETG`. The public scaffold has locations for Mount
Elbert, Ignik Sikumi, Hydrate-01, and Hydrate-02, but the user reports that
`MLK` and an `EIT`-like name are also separate wells in screenshots.

## Public Locations Found So Far

Focused repo CSV:
`data/public_stability_products/focused_well_location_recovery_2026-06-19.csv`

Official Alaska map/source services checked on 2026-06-19:

- Alaska DNR Open Data / Alaska Division of Oil and Gas, Well Surface Hole
  Location:
  `https://services1.arcgis.com/7HDiw78fcUiM2BWn/arcgis/rest/services/Well_Surface_Hole_Location/FeatureServer/0`
- Alaska DNR Open Data / Alaska Division of Oil and Gas, Well Bottom Hole
  Location:
  `https://services1.arcgis.com/7HDiw78fcUiM2BWn/arcgis/rest/services/Well_Bottom_Hole_Location/FeatureServer/0`
- Alaska Oil and Gas Conservation Commission data page / Data Miner:
  `https://www.commerce.alaska.gov/web/aogcc/data.aspx`

The "well path" currently recovered is a straight public surface-to-bottomhole
segment from those two official services. It is not a full measured wellbore
deviation survey.

| project role | current alias/status | public well name | API | field/area | wellhead lat/lon | bottomhole lat/lon | public depth m | surface-to-bottomhole segment | status |
|---|---|---|---|---|---|---|---:|---:|---|
| Mount Elbert case-study well | `Well-MTE` / `MTE`; mapping confirmed in project docs | `MT ELBERT 1` | `50029233020000` | Milne Point | 70.45563616, -149.41079781 | 70.45564162, -149.41072442 | 914.4 | 2.8 m | Official surface and bottomhole points found |
| Ignik Sikumi case-study well | `Well-IGS` / `IGS`; mapping confirmed in project docs | `PRUDHOE BAY UN IGNIK SIKUMI 1` | `50029234430000` | Prudhoe Bay | 70.34871222, -149.31709625 | 70.34868492, -149.31707172 | 791.5656 | 3.2 m | Official surface and bottomhole points found |
| Hydrate-01 stratigraphic test well | Public well row; workbook alias not confirmed | `HYDRATE 01` | `50029236130000` | `*EXPLORATORY` | 70.31693632, -149.20010365 | 70.31783739, -149.19263623 | 1032.9672 | 297.1 m | Official surface and bottomhole points found |
| Hydrate-02 geo data well | Public well row; workbook alias not confirmed | `HYDRATE 02` | `50029237280000` | `*EXPLORATORY` | 70.31717387, -149.20028453 | 70.31808587, -149.19693678 | 1064.3616 | 161.3 m | Official surface and bottomhole points found |

## Screenshot-Observed Candidate Wells Still Needing Locations

| candidate alias | source evidence | current interpretation | location status | next recovery action |
|---|---|---|---|---|
| `MLK` | User reports this appears in the screenshots as a separate well. Current text search did not find it in public-safe docs. A visible red header in `screenshot_2026-06-05_131418.png` reads `ML INPUT`, so do not rely on that header alone as `MLK`. | Treat as a separate candidate well until the original workbook/screenshot source proves whether it is a well alias, sheet tab, or OCR/misread label. | No public API/lat/lon mapped yet | Inspect the original workbook or higher-resolution screenshot; then search public well files by official name/API once spelling is confirmed |
| probable `EIT` / `E1T` / `ETG` | User reports an `EIT`-like screenshot name as a separate well. Older notes mention `ETG`, but local text docs also use Eileen Gas Hydrate Trend, so `ETG` may be ambiguous. | Treat as a separate candidate well from `MLK`; do not merge into Hydrate-01/Hydrate-02 without source proof. | No public API/lat/lon mapped yet | Verify exact spelling from original workbook/screenshot tabs or captions; then recover official well name and public location |

Confirmed screenshot tabs from the local `email_screenshots_2026_06_12` bundle:
`MTE`, `IGS`, `MTE_refined`, and `IGS_refined`. These do not eliminate the
reported `MLK`/`EIT` candidates; they only show that the currently visible local
bundle is not enough to map those aliases.

## Papers To Get Locally

Recommended source folder for new metadata and source-page notes:
`references/hydrate-ml-physics-sources/2026-06-19/`

PDF policy: journal PDFs from ACS, Elsevier, SPE/OTC, or other publishers should
go in Drive, OSL, or a local do-not-commit source folder unless redistribution
rights are explicit. GitHub can keep metadata, official public pages, notes, and
open government/OSTI/USGS PDFs where allowed.

| priority | well(s) | paper/source to get locally | source link / DOI | current local status | why needed for coring/core data | allowed use |
|---:|---|---|---|---|---|---|
| 1 | Hydrate-02 | Sedimentology and Geochemistry of Gas Hydrate-Bearing Sands in the Greater Prudhoe Bay Area, Alaska North Slope: Insights from HYDRATE-02 Geo Data Well Core Analyses | https://doi.org/10.1021/acs.energyfuels.5c04943 | Not found locally as PDF; DOI found by Crossref query | Direct Hydrate-02 core analyses: lithology, sedimentology, geochemistry, reservoir sand context | Drive/OSL/local-only PDF unless license permits GitHub; metadata safe in GitHub |
| 1 | Hydrate-02 | Permeability Evolution of Gas Hydrate-Bearing Pressure Core Sediment Recovered from the Alaska North Slope HYDRATE 02 Geo Data Well | https://doi.org/10.1021/acs.energyfuels.5c06126 | Not found locally as PDF; DOI found by Crossref query | Direct Hydrate-02 pressure-core permeability evolution | Drive/OSL/local-only PDF unless license permits GitHub; metadata safe in GitHub |
| 1 | Hydrate-02 | Permeability Evaluation of Hydrate Reservoirs Based on NMR T2 Relaxation Time from Both Log and Laboratory Data, Alaska North Slope HYDRATE 02 Geo Data Well | https://doi.org/10.1021/acs.energyfuels.5c05321 | Drive PDF already recorded in `references/hydrate-ml-physics-sources/2026-06-13/google_drive_uploaded_sources_2026_06_13.md` | Direct NMR T2, lab/core permeability, reservoir/seal calibration | Drive PDF already available; do not copy to public Git unless rights are confirmed |
| 1 | Hydrate-01 | Permeability Measurement and Prediction with Nuclear Magnetic Resonance Analysis of Gas Hydrate-Bearing Sediments Recovered from Alaska North Slope 2018 Hydrate-01 Stratigraphic Test Well | https://doi.org/10.1021/acs.energyfuels.1c03810 | Not found locally as PDF | Direct Hydrate-01 recovered sediment/core plus NMR permeability source | Drive/OSL/local-only PDF unless license permits GitHub; metadata safe in GitHub |
| 1 | Mount Elbert | Mount Elbert Gas Hydrate Stratigraphic Test Well, Alaska North Slope: Coring Operations, Core Sedimentology, and Lithostratigraphy | https://doi.org/10.1016/j.marpetgeo.2010.02.001 | Not found locally as PDF | Primary Mount Elbert coring operations, core sedimentology, and lithostratigraphy source | Drive/OSL/local-only PDF unless license permits GitHub; metadata safe in GitHub |
| 2 | Mount Elbert | Gas Hydrate Characterization and Grain-Scale Imaging of Recovered Cores from the Mount Elbert Gas Hydrate Stratigraphic Test Well, Alaska North Slope | https://doi.org/10.1016/j.marpetgeo.2009.08.003 | Not found locally as PDF | Mount Elbert recovered-core hydrate texture and grain-scale characterization | Drive/OSL/local-only PDF unless license permits GitHub; metadata safe in GitHub |
| 2 | Mount Elbert | Formation History and Physical Properties of Sediments from the Mount Elbert Gas Hydrate Stratigraphic Test Well, Alaska North Slope | https://doi.org/10.1016/j.marpetgeo.2010.03.005 | Not found locally as PDF | Mount Elbert physical properties and sediment context for core-to-log interpretation | Drive/OSL/local-only PDF unless license permits GitHub; metadata safe in GitHub |
| 2 | Mount Elbert | Downhole Well Log and Core Montages from the Mount Elbert Gas Hydrate Stratigraphic Test Well, Alaska North Slope | https://doi.org/10.1016/j.marpetgeo.2010.03.016 | Not found locally as PDF | Mount Elbert source figures tying core intervals to log response | Drive/OSL/local-only PDF unless license permits GitHub; metadata safe in GitHub |
| 2 | Mount Elbert | In-Situ Gas Hydrate Saturation Estimated from Various Well Logs at the Mount Elbert Gas Hydrate Stratigraphic Test Well, Alaska North Slope | https://pubs.usgs.gov/publication/70036903 ; https://doi.org/10.1016/j.marpetgeo.2009.06.007 | Official USGS page saved at `references/hydrate-ml-physics-sources/2026-06-13/lee_collett_2011_mount_elbert_usgs_page.html`; full PDF not local | Multi-log saturation source using NMR, sonic, resistivity, and core context | USGS page safe in GitHub; publisher PDF Drive/OSL/local-only unless rights permit |
| 2 | Hydrate-01 | Gas Hydrate Saturation Estimates, Gas Hydrate Occurrence, and Reservoir Characteristics Based on Well Log Data from the Hydrate-01 Stratigraphic Test Well, Alaska North Slope | https://www.usgs.gov/publications/gas-hydrate-saturation-estimates-gas-hydrate-occurrence-and-reservoir-characteristics ; https://doi.org/10.1021/acs.energyfuels.1c04100 | Listed in `references/hydrate-ml-physics-sources/2026-06-13/source_manifest.csv` as `needs_user_pdf` | Hydrate-01 saturation, occurrence, reservoir characteristics, and log interpretation | USGS page/metadata safe in GitHub; publisher PDF Drive/OSL/local-only unless rights permit |
| 2 | Hydrate-01 | Geological Reservoir Characterization of a Gas Hydrate Prospect Associated with the Hydrate-01 Stratigraphic Test Well, Alaska North Slope | https://doi.org/10.1021/acs.energyfuels.2c00336 | Not found locally as PDF | Hydrate-01 reservoir characterization and geologic context around the well | Drive/OSL/local-only PDF unless license permits GitHub; metadata safe in GitHub |
| 2 | Hydrate-02 | Alaska North Slope Extended-Duration Gas Hydrate Production Test Site Logging-While-Drilling Data Acquisition | https://doi.org/10.1021/acs.energyfuels.5c06115 | Drive PDF already recorded in `references/hydrate-ml-physics-sources/2026-06-13/google_drive_uploaded_sources_2026_06_13.md` | Hydrate-02 production-test-site LWD acquisition, QC, log suite, and completion-selection context | Drive PDF already available; do not copy to public Git unless rights are confirmed |
| 2 | Hydrate-02 | Comparison between Pressure Core and Remolded Tetrahydrofuran-Hydrate-Bearing Core Testing Using Sediments Recovered from the Alaska North Slope | https://doi.org/10.1021/acs.energyfuels.5c05467 | Not found locally as PDF | Pressure-core versus remolded-core comparison for ANS sediments; useful for interpreting lab/core transferability | Drive/OSL/local-only PDF unless license permits GitHub; metadata safe in GitHub |
| 2 | Hydrate-02 | Consolidation and Permeability of the B1 and D1 Gas Hydrate Bearing Sands and Associated Seal Sediments of the Extended-Duration Gas Production Test Site on the Alaska North Slope | https://doi.org/10.1021/acs.energyfuels.5c03159 | Not found locally as PDF | Hydrate-02 / production-test-site core mechanics, sand/seal behavior, permeability context | Drive/OSL/local-only PDF unless license permits GitHub; metadata safe in GitHub |
| 3 | Ignik Sikumi | The Ignik Sikumi Field Experiment, Alaska North Slope: Design, Operations, and Implications for CO2-CH4 Exchange in Gas Hydrate Reservoirs | https://doi.org/10.1021/acs.energyfuels.6b01909 | Not found locally as PDF | Best confirmed Ignik Sikumi operations/reservoir context found so far; not a dedicated coring paper | Drive/OSL/local-only PDF unless license permits GitHub; metadata safe in GitHub |
| 3 | Ignik Sikumi | Guest Molecule Exchange Kinetics for the 2012 Ignik Sikumi Gas Hydrate Field Trial | https://doi.org/10.4043/25374-MS | Not found locally as PDF | Field-trial context if Ignik Sikumi needs production-test/source-history support; not primary core data | Drive/OSL/local-only PDF unless license permits GitHub; metadata safe in GitHub |
| 3 | Hydrate-02 | Lithological Control of Gas Hydrate Saturation Determined by Pressure Core Analysis in Subpermafrost Reservoirs of the Alaska North Slope (HYDRATE 02 Geo Data Well) | Existing manifest title only; DOI not verified in this pass | Listed in `references/hydrate-ml-physics-sources/2026-06-13/source_manifest.csv` as `needs_user_pdf`; exact DOI/source page still missing | Existing project manifest says this is a key lithology/core calibration source, but title/source needs verification | Treat as Drive/OSL/local-only until source and rights are confirmed |
| 3 | Hydrate-02 | Linking Physical Property Measurements from Pressure Core and Logging-While-Drilling Data Sets at the Alaska North Slope Gas Hydrate Production Test Site | Existing manifest title only; DOI not verified in this pass | Listed in `references/hydrate-ml-physics-sources/2026-06-13/source_manifest.csv` as `needs_user_pdf`; exact DOI/source page still missing | Existing project manifest says this is a core-to-LWD linkage source, but title/source needs verification | Treat as Drive/OSL/local-only until source and rights are confirmed |

## Immediate Retrieval Checklist

1. Get the Hydrate-02 core-analysis and pressure-core PDFs first:
   `10.1021/acs.energyfuels.5c04943`, `10.1021/acs.energyfuels.5c06126`,
   `10.1021/acs.energyfuels.5c05467`, and `10.1021/acs.energyfuels.5c03159`.
2. Get the Hydrate-01 recovered-sediment/NMR paper:
   `10.1021/acs.energyfuels.1c03810`.
3. Verify `MLK` and probable `EIT` / `E1T` / `ETG` from the original
   workbook/screenshot source before calling the location list final.
4. Get the Mount Elbert core operations/lithostratigraphy paper:
   `10.1016/j.marpetgeo.2010.02.001`.
5. Then collect the Mount Elbert supporting core/log papers and Hydrate-01
   reservoir/log papers.
6. Use the Ignik Sikumi field-experiment papers for location/operations
   context unless a dedicated Ignik core/coring paper is found.
7. If the user has PDFs for the two manifest-only 2026 titles, import them and
   update the manifest with DOI, source page, local/Drive file ID, and allowed
   use.

## Still Needed

- Confirm exact spelling and source role for `MLK` and probable `EIT` / `E1T` /
  `ETG`. The user reports these are separate wells; local public-safe docs do
  not yet map them to official names, APIs, or coordinates.
- Confirm whether the coring set means Mount Elbert, Ignik Sikumi, Hydrate-01,
  Hydrate-02, plus `MLK`/`EIT` candidates, or whether workbook metadata maps the
  approved wells differently.
- Add a 2026-06-19 source manifest after PDFs are received, with columns:
  `id`, `title`, `authors`, `year`, `well`, `local_or_drive_path`, `source_url`,
  `allowed_use`, `rebuild_role`, and `notes`.
