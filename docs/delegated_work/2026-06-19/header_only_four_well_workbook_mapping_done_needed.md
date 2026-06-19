# Header-Only Four-Well Workbook Mapping Done / Needed Handoff

## Prompts Worked On

- Header-only verification from screenshot email attachments.
- Four-well/source-case name, API, and public North Slope location lookup.
- Website incorporation of verified public case-well anchors into the unified North Slope map.

## Done

- Located the latest self-email titled `screenshots` from 2026-06-19. The body says the attachments cover the four dataset headers, temperature gradient, and equations.
- Downloaded the ten PNG attachments into ignored local storage: `data/source_library/email_screenshot_headers_2026_06_19/`.
- Created a GitHub-safe screenshot manifest at `docs/evidence/email_screenshots_2026_06_19/README.md`; no raw screenshots were committed.
- Verified from screenshot metadata that the visible workbook tabs are `MTE`, `IGS`, `MTE_refined`, and `IGS_refined`.
- Confirmed `MTE` and `IGS` are actual workbook well sheets by visible active tabs and headers.
- Confirmed `MTE_refined` and `IGS_refined` are refined/processed target/depth-alignment sheets, not separate wells by screenshot evidence.
- Confirmed `MLK` and `ETG` do not appear in the latest screenshot set.
- Added a public well/API/location index at `data/public_ml_products/four_well_case_location_index_2026-06-19.csv`.
- Documented the source and boundary at `docs/source_library_index/FOUR_WELL_CASE_LOCATION_INDEX_2026-06-19.md`.
- Updated `dashboard/app.py` so `Explore North Slope > Regional Map` loads the public case-location CSV as a separate `ML/source case well anchors` map layer and exposes the table/download.

## Still Needed

- When DOE/OSL access returns, confirm raw workbook formulas, units, depth alignment, and actual workbook membership without moving row-level values into GitHub.
- Confirm whether Hydrate-01 and HYDRATE 02 are active ML workbook sheets or public source-case anchors only.
- Confirm the source-paper relationship between `HYDRATE 01` and `KUPARUK ST 7-11-12` before final slide wording.
- Confirm HYDRATE P1/P2 roles from the HYDRATE 02 operations/data paper before emphasizing them in the deck.
- Download source papers/supplements into Drive/OSL only where access/licensing allows; keep raw PDFs, supplements, and tables out of GitHub unless public-safe and lightweight.

## Files / Assets

- Added: `docs/evidence/email_screenshots_2026_06_19/README.md`
- Added: `docs/delegated_work/2026-06-19/header_only_four_well_workbook_mapping_done_needed.md`
- Added: `docs/source_library_index/FOUR_WELL_CASE_LOCATION_INDEX_2026-06-19.md`
- Added: `data/public_ml_products/four_well_case_location_index_2026-06-19.csv`
- Edited: `dashboard/app.py`
- Local-only ignored raw screenshots: `data/source_library/email_screenshot_headers_2026_06_19/`

## Branch / Commit

- Branch: `codex/four-well-core-data-source-hunt-20260619`
- Commit: pending in this handoff until the website/doc update is committed.

## Slides Affected

- Slide 2: North Slope context and well-name/API orientation.
- Slide 3: Header-derived log-family and target/calibration separation.
- Slide 7: Unified North Slope stability/context map.
- Slide 8: Planned result-review logic and four-case/source-case separation.
- Slide 9: Built/not-claimed/next-action status.

## Main Codex Next Steps

1. Use `docs/evidence/email_screenshots_2026_06_19/README.md` as the header-only source of truth for screenshot-derived sheet/header claims.
2. Use `data/public_ml_products/four_well_case_location_index_2026-06-19.csv` for public website labels and API/location orientation.
3. Keep `MTE` and `IGS` as screenshot-verified workbook well sheets; treat `MTE_refined` and `IGS_refined` as processed versions.
4. Treat Hydrate-01 and HYDRATE 02 as public source-case anchors until approved header evidence confirms active workbook membership.
5. Do not commit the raw screenshots, raw workbooks, source tables, licensed papers, approved runtime rows, trained models, or fitted scalers.
