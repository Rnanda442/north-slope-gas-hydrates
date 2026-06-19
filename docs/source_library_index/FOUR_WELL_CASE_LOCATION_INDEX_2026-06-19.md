# Four-Well / Source-Case Public Location Index

Date: 2026-06-19

Scope: public well-name, API, permit, field, status, and coordinate anchors for the current ML/source-case discussion. Source rows come from the committed public Alaska DNR-derived well context table, not from approved runtime workbooks.

Public CSV: `data/public_ml_products/four_well_case_location_index_2026-06-19.csv`

## Verified Public Well Anchors

| well/case | public well name | API number | field | website role | evidence status |
|---|---|---:|---|---|---|
| MTE / Mount Elbert | MT ELBERT 1 | 50029233020000 | MILNE POINT | Header-verified ML well anchor | Latest screenshot email shows `MTE` as a visible workbook sheet; public well table provides API/location. |
| IGS / Ignik Sikumi | PRUDHOE BAY UN IGNIK SIKUMI 1 | 50029234430000 | PRUDHOE BAY | Header-verified ML well anchor | Latest screenshot email shows `IGS` as a visible workbook sheet; public well table provides API/location. |
| Hydrate-01 | HYDRATE 01 | 50029236130000 | *EXPLORATORY | Public source-case anchor | Public well table and source index verify the well/case; latest screenshots do not show a `Hydrate-01` workbook sheet. |
| Hydrate-01 associated anchor | KUPARUK ST 7-11-12 | 50029200620000 | PRUDHOE BAY | Associated source-location note | Public well table places this source anchor near HYDRATE 01; final wording needs paper confirmation before treating it as equivalent. |
| HYDRATE 02 | HYDRATE 02 | 50029237280000 | *EXPLORATORY | Public source-case anchor | Public well table and 2026 source index verify the well/case; latest screenshots do not show a `HYDRATE 02` workbook sheet. |
| HYDRATE 02 associated well | HYDRATE P1 | 50029237370000 | *EXPLORATORY | Associated test-site context | Public well table provides API/location; source-paper role still needs confirmation. |
| HYDRATE 02 associated well | HYDRATE P2 | 50029237320000 | *EXPLORATORY | Associated test-site context | Public well table provides API/location; source-paper role still needs confirmation. |

## Website Use

The unified website map now loads the CSV as a separate `ML/source case well anchors` marker group. The marker colors are separate from the stability-screen status colors so the public well/API labels do not imply hydrate occurrence, saturation, producibility, or trained-model evidence.

The map hover shows the public well name, API number, permit number, field, current status, and evidence status. The Regional Map panel also exposes the table and a CSV download.

## GitHub-Safe vs Drive/OSL-Only

GitHub-safe:

- Public Alaska well metadata already used in `data/public_stability_products/north_slope_well_stability_context_2026-06-14.csv`.
- Header-only screenshot summaries: visible sheet names, column headers, and public-safe source notes.
- The derived location/API CSV and this documentation.

Drive/OSL-only:

- Raw workbook files, workbook rows, approved well-log/core rows, pressure-core tables, NMR/core data values, private screenshots that show row-level data, runtime manifests, predictions, trained models, fitted scalers, and licensed PDFs/supplements.

## Remaining Questions

- Confirm from DOE/OSL workbook headers whether Hydrate-01 and HYDRATE 02 are active ML workbook sheets or only public source-case anchors.
- Confirm the exact relationship between `HYDRATE 01` and `KUPARUK ST 7-11-12` from source papers before final deck wording.
- Confirm HYDRATE P1/P2 roles from the HYDRATE 02 operations/data paper before emphasizing them in the deck.
- Recheck all workbook formulas, units, and row-level depth alignment only inside approved/OSL runtime when access returns.
