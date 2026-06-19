# Header-Only Four-Well Workbook Mapping Done / Needed Handoff

## Prompts Worked On

Prompt 15: Header-Only Four-Well Workbook Mapping.

## Done

- Searched local `Documents`, `Downloads`, and `OneDrive` folders for the
  expected approved-runtime filenames:
  - `curated_dataset1.xlsx`
  - `curated_dataset2.xlsx`
  - `curated_dataset3.xlsx`
  - `wellnametodataset.txt`
- Searched the repo for workbook mapping references, MTE/IGS/refined sheet
  metadata, and existing header-only plans.
- Confirmed this machine does not have the expected curated workbook filenames
  available by exact-name search.
- Confirmed existing repo metadata still treats `MTE_refined` and
  `IGS_refined` as unresolved workbook-stage/sheet questions, not verified
  additional wells.

## Still Needed

- Run Prompt 15 on the DOE desktop or approved runtime machine where the three
  curated workbooks actually exist.
- Export only workbook metadata: sheet names, headers, named ranges, safe
  workbook properties, target-like headers, feature-like headers, and
  depth/alignment columns.
- Confirm whether `MTE_refined`, `IGS_refined`, `MLK`, `ETG`, or other labels
  are wells, sheets, aliases, processing stages, or unresolved.
- Confirm whether saturation targets are stored as fractions 0-1 from workbook
  metadata or safe header/unit rows, without exporting row data.

## Files / Assets

| file path | status | why it matters |
|---|---|---|
| `docs/delegated_work/2026-06-19/header_only_four_well_workbook_mapping_done_needed.md` | created | Explicitly records that Prompt 15 cannot be completed on this machine |

## Branch / Commit

Branch pending at handoff creation: `codex/prompts-14-17-20260619`.

## Slides Affected

- Slide 3: actual well labels, lithology/core strips, and signal examples.
- Slide 4: four-well scope wording.
- Slide 6: evidence-review board.
- Slide 8: DOE export placeholders.

## Main Codex Next Steps

- Do not treat local Downloads workbook-like files as the active three curated
  DOE workbooks without user confirmation.
- Ask the DOE desktop chat to run the header-only scanner against the exact
  `curated_dataset1/2/3.xlsx` files.
- Merge only the sanitized header report back into GitHub.
