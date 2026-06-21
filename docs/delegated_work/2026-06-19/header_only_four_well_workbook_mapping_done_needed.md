# Header-Only Four-Well Workbook Mapping Done / Needed Handoff

## Prompts Worked On

- Prompt 15: Header-only four-well workbook mapping.
- Header-only verification from the latest screenshot email attachments.
- Four-well/source-case name, API, and public North Slope location lookup.
- Website incorporation of verified public case-well anchors into the unified North Slope map.
- This consolidated handoff combines the local exact-filename search, screenshot manifest, public-safe visible-header mapping, and public well/API/location index.
- It does not claim that the live DOE Excel workbook metadata has been re-read on this laptop.

## Evidence Boundary

- No approved workbook rows, cell values, row-level predictions, trained models, fitted scalers, raw screenshots, or private local workbook paths are committed here.
- The latest self-email titled `screenshots` from 2026-06-19 says the attachments cover the four dataset headers, temperature gradient, and equations.
- The ten PNG attachments were downloaded into ignored local storage: `data/source_library/email_screenshot_headers_2026_06_19/`.
- GitHub contains only the public-safe manifest at `docs/evidence/email_screenshots_2026_06_19/README.md`; raw screenshots remain Drive/OSL/local-only.
- This report uses GitHub-safe committed evidence:
  - `docs/evidence/email_screenshots_2026_06_12/README.md`
  - `docs/evidence/email_screenshots_2026_06_19/README.md`
  - `data/public_ml_products/approved_data_field_role_table_2026-06-15.csv`
  - `data/public_ml_products/approved_schema_coverage_matrix_2026-06-15.csv`
  - `data/public_ml_products/four_well_case_location_index_2026-06-19.csv`
  - `dashboard/well_log_engine.py`
  - `docs/deliverable_status_inventory.md`

## Done

- Searched local `Documents`, `Downloads`, and `OneDrive` folders for the expected approved-runtime filenames:
  - `curated_dataset1.xlsx`
  - `curated_dataset2.xlsx`
  - `curated_dataset3.xlsx`
  - `wellnametodataset.txt`
- Confirmed this laptop does not have the expected curated workbook filenames available by exact-name search.
- Located the latest self-email screenshot set and committed only the GitHub-safe manifest.
- Verified from screenshot metadata that the visible workbook tabs are `MTE`, `IGS`, `MTE_refined`, and `IGS_refined`.
- Confirmed `MTE` and `IGS` are actual workbook well sheets by visible active tabs and headers.
- Confirmed `MTE_refined` and `IGS_refined` are refined/processed target/depth-alignment sheets, not separate wells by screenshot evidence.
- Confirmed `MLK` and `ETG` do not appear in the latest screenshot set.
- Confirmed a source-backed visible-header grouping for the current ML/log scaffold.
- Confirmed target-like and calibration-like fields that must stay out of predictors.
- Added a public well/API/location index at `data/public_ml_products/four_well_case_location_index_2026-06-19.csv`.
- Documented the source and boundary at `docs/source_library_index/FOUR_WELL_CASE_LOCATION_INDEX_2026-06-19.md`.
- Updated the website Regional Map so public case-location CSV records display as a separate `ML/source case well anchors` map layer and table/download.

## Visible Header Mapping

| visible group | visible headers | current role | public-safe use | blocked or prohibited use | confidence | remaining question |
| --- | --- | --- | --- | --- | --- | --- |
| Depth and alignment | `DEPTH`, `DEPT`, `True Depth`, `Depth_ft`, `Depth (ft)`, `depths_unitD`, `depths_unitC`, `Depth correspondence at ML data` | index / QC / alignment | Show as depth-alignment and interval-registration metadata. | Do not expose row-level depths or create false precision around matching method. | high for header presence; medium for exact alignment meaning | What interpolation, unit conversion, or matching rule produced the refined depth correspondence? |
| Borehole quality | `caliper`, `CAL1`, `differential caliper` | measured QC | Use as bad-hole / washout QC context in the log scaffold. | Do not treat as hydrate evidence. | high | What reference hole size and units apply per workbook? |
| Lithology | `GR` | measured input / lithology cue | Use as clean-sand versus shale-rich context. | Do not use as proof of hydrate occurrence. | high | Confirm API units and local shale/sand calibration by well. |
| Density and porosity | `Rho_b`, `RHOB`, `Density_gpcc`, `Phi_porosity`, `phi_den`, `DPHI`, `NPHI`, `phi_neut`, `NMRPHI`, `phi_nmr` | measured or derived input family | Show density, neutron, density-porosity, and NMR-porosity as input-capable when independently measured. | Do not confuse `NMRPHI` / `phi_nmr` with `NMR_SAT`. | high for header presence; medium for unit convention | Confirm fraction versus percent for porosity fields by workbook. |
| Electrical response | `Rt`, `RES`, `Deep formation resistivity`, `AO90`, `AF90` | measured input or unresolved mnemonic | Use `Rt`/`RES` as resistivity input/context when units and tool channel are confirmed. | Keep `AO90` and `AF90` blocked until the tool mnemonic is verified. | high for header presence; medium for mnemonic role | Is the screenshot/header spelling `AO90` or `A090`, and what tool channel does it represent? |
| Elastic response | `Vp`, `VP`, `VELP`, `Vs`, `VS`, `VS1` | measured or supplied velocity family | Use for sonic/elastic context and derived attributes when units are standardized. | Do not infer hydrate from velocity alone. | high for header presence; medium for unit convention | Confirm whether velocities are measured, supplied, or calculated in each workbook. |
| Derived elastic attributes | `Ratio Vp/Vs`, `Impedance` | derived feature family | Use as explainable derived attributes in Slide 3 / equation slides. | Do not present derived features as cleaner than their density/velocity inputs. | high for header presence | Should stored ratio/impedance be trusted or recalculated from canonical `Vp`, `Vs`, and density? |
| Saturation / labels | `Sgh`, `S_h`, `Sh`, `Hydrate Saturation`, `NMR_SAT` | target-only / calibration / validation | Use only as supervised target, calibration, validation, or post-prediction review labels. | Never put these in `X_allowed` predictors, feature normalization, ranking inputs, or slide language implying proof by stability/log response alone. | high | Which saturation field is authoritative when multiple labels coexist? |
| Irreducible water / calibration | `Swr`, `S_wr` | calibration-reference unless proven otherwise | Mention only as calibration/reference context after source review. | Do not use as predictor until role is source-verified. | medium | Are these independent measured values, derived labels, or interpretation outputs? |

## Workbook / Case Identity Status

| name or label | evidence status | safe current wording | unresolved issue |
| --- | --- | --- | --- |
| `MTE` / `Well-MTE` | Screenshot-verified workbook well sheet; public notes support Mount Elbert / MTE context. | Use as a screenshot-verified workbook case and public-safe Mount Elbert/MTE label where the cited notes support it. | Confirm exact approved workbook membership and units from DOE metadata. |
| `IGS` / `Well-IGS` | Screenshot-verified workbook well sheet; public notes support Ignik Sikumi / IGS context. | Use as a screenshot-verified workbook case and public-safe Ignik Sikumi/IGS label where the cited notes support it. | Confirm exact approved workbook membership and units from DOE metadata. |
| `MTE_refined` | Screenshot-visible refined/processed sheet. | Treat as a refined processing/alignment view, not a separate well. | Confirm the exact refinement, target, and depth-alignment rule. |
| `IGS_refined` | Screenshot-visible refined/processed sheet. | Treat as a refined processing/alignment view, not a separate well. | Confirm the exact refinement, target, and depth-alignment rule. |
| `MLK` | Mentioned by the user as a suspected name; not present in the latest screenshot set. | Keep unresolved. | Does `MLK` appear in another header screenshot, workbook tab, source document, or well-name mapping file? |
| `ETG` | Mentioned by the user as a suspected name; not present in the latest screenshot set and may be confused with Eileen Gas Hydrate Trend. | Keep unresolved unless a workbook/source explicitly uses it as a well/case name. | Is `ETG` a well/case alias, trend name, or shorthand? |
| `Hydrate-01` | Public source-case anchor with API/location index entry. | Use as public source-case / calibration context unless approved header evidence confirms workbook membership. | Confirm relationship to `KUPARUK ST 7-11-12` before final slide wording. |
| `HYDRATE 02` | Public source-case anchor with API/location index entry. | Use as public source-case / calibration context unless approved header evidence confirms workbook membership. | Confirm HYDRATE P1/P2 roles from operations/data papers before emphasizing them. |
| `curated_dataset1.xlsx`, `curated_dataset2.xlsx`, `curated_dataset3.xlsx` | Runtime/runbook filenames; not found by exact-name search on this laptop. | Use as workbook placeholders until the DOE/PC header-only scan confirms actual membership. | Which sheets/cases/wells are inside each real workbook? |

## Still Needed

- When DOE/OSL access returns, inspect only workbook metadata, sheet names, visible headers, named ranges, safe workbook properties, formulas, and units.
- Export only workbook metadata, not row values.
- Confirm whether Hydrate-01 and HYDRATE 02 are active ML workbook sheets or public source-case anchors only.
- Confirm the authoritative saturation target among `Sgh`, `S_h`, `Sh`, `Hydrate Saturation`, and `NMR_SAT`.
- Confirm units for porosity, velocities, resistivity, density, and saturation without exporting row values.
- Download source papers/supplements into Drive/OSL only where access/licensing allows; keep raw PDFs, supplements, screenshots, and tables out of GitHub unless reviewed as public-safe and lightweight.

## Files / Assets

- Added: `docs/evidence/email_screenshots_2026_06_19/README.md`
- Added/merged: `docs/delegated_work/2026-06-19/header_only_four_well_workbook_mapping_done_needed.md`
- Added: `docs/source_library_index/FOUR_WELL_CASE_LOCATION_INDEX_2026-06-19.md`
- Added: `data/public_ml_products/four_well_case_location_index_2026-06-19.csv`
- Edited: `dashboard/app.py`
- Local-only ignored raw screenshots: `data/source_library/email_screenshot_headers_2026_06_19/`
- No raw screenshot, workbook, source PDF, or data-row asset was added.

## Branch / Commit

- Source branches:
  - `codex/prompts-14-17-20260619`
  - `codex/prompt15-visible-header-mapping-20260619`
  - `codex/four-well-core-data-source-hunt-20260619`
- Final integration commit is recorded in the unified slide workspace branch.

## Slides Affected

- Slide 2: North Slope context and well-name/API orientation.
- Slide 3: log signal, lithology, header-derived log-family, and target/calibration separation.
- Slide 4: ML architecture leakage guardrails and feature/target separation.
- Slide 5: equation/derived-attribute cards.
- Slide 6/7: evidence review and stability/context language.
- Slide 8: planned result-review logic and DOE export placeholders.
- Slide 9: built/not-claimed/next-action status.

## Main Codex Next Steps

1. Use `docs/evidence/email_screenshots_2026_06_19/README.md` as the header-only source of truth for screenshot-derived sheet/header claims.
2. Use `data/public_ml_products/four_well_case_location_index_2026-06-19.csv` for public website labels and API/location orientation.
3. Keep `MTE` and `IGS` as screenshot-verified workbook well sheets; treat `MTE_refined` and `IGS_refined` as processed versions.
4. Treat Hydrate-01 and HYDRATE 02 as public source-case anchors until approved header evidence confirms active workbook membership.
5. Do not wait on raw rows to rebuild editable slide structure.
6. Before final well naming or DOE-calibrated model claims, import the PC/DOE header-only workbook metadata output and update the identity/status table.
7. Do not commit raw screenshots, raw workbooks, source tables, licensed papers, approved runtime rows, trained models, or fitted scalers.
