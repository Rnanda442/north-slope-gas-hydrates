# Slide Finishing Needs

Date: 2026-06-18

| slide | needed asset/content | source/location | owner | GitHub-safe? | status | blocker |
|---:|---|---|---|---|---|---|
| 2 | Combined North Slope context map, P-T diagram/curve, corrected hydrate structure labels, thermogenic/biogenic and resource context | Current Slide 2 baseline; `docs/project_blueprints/presentation_assets/website_well_maps_2026_06_18/`; stability calculation docs; Word companion sources | Main Codex plus user/mentor source review | Partly | In progress | Latest Gmail deck not verified; P-T and structure visuals need source-backed editable rebuild. |
| 3 | Realistic multi-curve log panel with integrated callouts, lithology column, core/NMR calibration strip | Public parameter registry; screenshot/header evidence; DOE export placeholder for real curves; `main_codex_thread_PROMPT_RESULTS.md` | Main Codex; DOE later for approved data | Partly | Needed | Four-well well/source/core/lithology evidence is not fully verified; no approved rows can enter GitHub. |
| 4 | Simplified audience ML architecture and two-minute script | Complex ML runtime plate; approved-data schema docs; DOE runtime runbook; `main_codex_thread_PROMPT_RESULTS.md` | Main Codex | Yes | Handoff available; build needed | Must avoid broad data-lake framing and unsupported metrics. |
| 5 | Equation-only slide with stacked fractions, symbol labels, and source-role coloring | `docs/STABILITY_CALCULATION_PLAN.md`; equation screenshot/source notes; current builders | Main Codex | Yes if formulas are source-backed | Needed | Need source verification for each equation; no final stability or saturation claim. |
| 6 | High-level four-well evidence-review board with reduced text and integrated images | Current V5.5/V5.4 panels, source visual inventory, and `main_codex_thread_PROMPT_RESULTS.md` | Main Codex | Yes | Handoff available; build needed | Need decide which text moves to Word/speaker notes and verify four-well evidence. |
| 7 | New unified stability/context map with editable labels and context-only caption | `unified_north_slope_slide_export_callout_space_2026_06_18.png` or `unified_north_slope_well_stability_context_map_2026_06_18.png` | Main Codex | Yes | Asset available | Must not add ML overlay, prediction colors, or sweet-spot ranking. |
| 8 | Planned four-well result-review logic: DOE figures/tables, lithology/core calibration, uncertainty, false-positive checks, separate occurrence/saturation lanes | DOE runtime tracker plan; public model-run templates; future DOE row-free exports | DOE runtime plus Main Codex | Partly | Needed | No DOE row-free exports currently imported; four-well identity/source evidence still needs confirmation. |
| 9 | Built / not claimed / next actions close | Current V5.5 close; artifact index; runtime and stability guardrails | Main Codex | Yes | Needed | Must avoid claiming final stability, trained metrics, occurrence/saturation predictions, or ranking. |

## Later DOE Export Checklist

| export | purpose | GitHub-safe? | blocker |
|---|---|---|---|
| `workbook_sheet_inventory.csv` | Verify workbook-to-sheet structure. | Only after header-only review and path sanitization | Approved workbooks must remain in DOE/OSL. |
| `workbook_column_inventory.csv` | Verify original headers and target-like fields. | Only header-only, no row values | Approved workbooks must remain in DOE/OSL. |
| `target_header_hints.csv` | Identify possible Y-only target variants. | Yes if header-only | Target authority still needs mentor review. |
| `run_summary.csv` | Local runtime run status by target. | Row-free summary only | No row-level predictions or runtime manifest. |
| `feature_columns_by_target.csv` | Show cleaned feature families per target. | Yes after review | Must exclude target-like fields and helper/depth columns. |
| `excluded_feature_columns_by_target.csv` | Show why fields were excluded. | Yes after review | Must not include private rows or raw data values. |
| `sheet_inventory.csv` | Summarize workbook/sheet availability. | Header/metadata only | Avoid private paths and row-level content. |
| `public_safe_model_run_summary.csv` | Mentor-facing row-free summary. | Yes after review | Do not include final trained metric claims unless approved. |
| `feature_family_coverage.png` | Slide/Word figure for feature families. | Yes after review | Must be row-free and non-claiming. |
| `validation_status_summary.png` | Show validation readiness/status categories. | Yes after review | Do not imply final validation performance. |
| DOE well-log/lithology/core panels | Slide 3 and Slide 8 visuals. | Only if cleared as public-safe PNG/summary | Approved rows and private identifiers must stay in DOE/OSL. |
