# Delegated Work Index

Date: 2026-06-18

Integration branch: `codex/delegated-slide-intake-20260618`

Purpose: consolidate GitHub-safe delegated slide handoffs and public-safe
assets so the main Codex session can pull one branch and continue finishing the
slide deck.

## Branch Intake

| delegated branch | source | head commit | status | prompt coverage | included? | safety result |
|---|---|---:|---|---|---|---|
| `codex/delegated-main_codex_thread-20260618` | local and `origin` branch | `0c49412` | found and merged | Prompts 5, 7, 9, plus coordination handoff | yes | Public-safe handoff report plus docs, code, tests, source-backed PNG assets, and a small source-only DOCX from its history. No approved rows, raw workbook files, runtime outputs, model binaries, fitted scalers, private screenshots, or row-level predictions found in changed paths. |

Delegated branch search result:

- Matching branch found: `codex/delegated-main_codex_thread-20260618`.
- Remote ref present after final verification:
  `origin/codex/delegated-main_codex_thread-20260618` at `0c49412`.
- No other `codex/delegated-*-20260618` branches were found.

## Included Commits

| branch/commit | commit | summary |
|---|---:|---|
| `codex/delegated-main_codex_thread-20260618` | `0c49412` | docs: add main_codex_thread delegated prompt handoff |
| same branch | `d79393b` | Update project base with editable-slide and four-well rules |
| same branch | `3d781bb` | Expand project revision prompts and four-well scope |
| same branch | `2f4a7cd` | Add deck delegation base from latest email |
| same branch | `3bb855b` | Fix Slide 2 OSL GIS map and hydrate circle |
| same branch | `aa7e8da` | Update Slide 2 stability context map |
| same branch | `b663414` | Add source-only research overview paper |
| same branch | `a340b28` | Add DOE equation-derived visual generator |
| same branch | `630f905` | Add DOE equation-derived visual generator |

The integration branch was created from current `origin/main` and merged the
local delegated branch before this index was added.

## Report Files

| report file | source branch | prompt numbers covered | status |
|---|---|---|---|
| `docs/delegated_work/2026-06-18/main_codex_thread_PROMPT_RESULTS.md` | `codex/delegated-main_codex_thread-20260618` | Prompt 5, Prompt 7, Prompt 9, coordination prompt | Included |
| `docs/delegated_work/2026-06-18/DELEGATED_WORK_INDEX_2026-06-18.md` | integration branch | aggregator | Added by integration pass |
| `docs/delegated_work/2026-06-18/SLIDE_FINISHING_NEEDS_2026-06-18.md` | integration branch | aggregator | Added by integration pass |

## Slide-By-Slide Findings

| slide | finding | assets available now | assets still missing | decision needed |
|---|---|---|---|---|
| Slide 2 | Needs concise hydrate and North Slope context with one combined 2D map, P-T diagram language, corrected Structure I circle, source-backed Structure I/II/H wording, gas-origin context, and cross-section explanation. | Updated Slide 2 builder inputs, `slide02_selected_12_stability_screen_status_2d_well_map.png`, `slide02_selected_13_osl_gis_stability_context_map_crop.png`, `slide02_selected_14_world_atlas_fig1_1_structure_types_clean.png`, and website well-map exports. | Final combined map that integrates all desired GeoPackage layers; east-west anticline/stability-zone explanation if source-backed. | Decide whether the current OSL/website stability map is acceptable as a temporary slide asset or leave the map region blank until the combined map is ready. |
| Slide 3 | Should explain log-signal movement plus lithology and core/coring authority, not equations or architecture. | Parameter registry, science logic ladder, baseline source ledger, and public-safe report guidance. | Verified four-well names and source-backed core/NMR/lithology evidence; final realistic multi-curve log scaffold. | Run or import Prompt 5 OSL/header verification before finalizing well names and lithology/core strip. |
| Slide 4 | Current full architecture is too dense for the audience. Rebuild as a simplified four-well workflow. | Prompt 7 handoff: six major blocks, arrow sequence, and two-minute script. | Native editable slide implementation. | Decide whether full complex architecture moves to Word, appendix, or backup slide only. |
| Slide 5 | Equation-only slide replaces the old three-dataset prototype. | Equation-source docs and generator scaffold from branch; current main worktree also has uncommitted equation-card deck work not included in this integration branch. | Final source-approved equation set and native editable implementation. | Decide whether to promote the current local equation-card rebuild, revise it, or rebuild natively. |
| Slide 6 | Should become high-level four-well evidence-review visual because equations move to Slide 5. | Prompt 9 before/after plan. | Verified four-well evidence, core/lithology strip, and simplified editable design. | Decide the one-sentence takeaway and what moves to Word/speaker notes. |
| Slide 7 | New stability map belongs here as context only. It should not be an ML overlay. | Website/OSL well-map exports and stability map candidates. | Final combined map with new GeoPackage layers, plus context-only caption. | Choose the accepted Slide 7 map export and legend/caption language. |
| Slide 8 | Should explain planned four-well results/review logic without fake results. | DOE runtime tracking plan and Prompt 10 direction in delegation base. | Planned review/export visuals from DOE approved runtime after review. | Decide which future figures/tables are promised and which stay in Word. |
| Slide 9 | Should close with done, not claimed, and next actions. | Delegation base and guardrail language. | Updated native/editable close slide after Slides 2-8 settle. | Decide final mentor-facing next actions and avoid any final metric or prediction claim. |

## Assets Available Now

| asset | path | GitHub-safe use |
|---|---|---|
| Delegated Prompt 5/7/9 report | `docs/delegated_work/2026-06-18/main_codex_thread_PROMPT_RESULTS.md` | Main handoff source for four-well verification needs, Slide 4 plan, and Slide 6 plan. |
| Delegation base and prompt set | `docs/PROJECT_REVISION_DELEGATION_BASE_2026-06-18.md` | Cross-slide rules and prompt library for remaining delegated work. |
| DOE equation-derived visual generator | `01_pipeline/generate_doe_equation_derived_visuals.py` | Public-safe generator scaffold; no approved rows committed. |
| DOE equation-derived visual tests | `tests/test_doe_equation_derived_visuals.py` | Synthetic test coverage for generator behavior. |
| Structure types clean image | `docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_14_world_atlas_fig1_1_structure_types_clean.png` | Slide 2 source figure candidate after rights/caption review. |
| Stability map crop | `docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_13_osl_gis_stability_context_map_crop.png` | Context-only stability map candidate. |
| Stability screen status map | `docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_12_stability_screen_status_2d_well_map.png` | Context-only stability status visual. |
| Website well-map package | `docs/project_blueprints/presentation_assets/website_well_maps_2026_06_18/` | Public-safe map exports and source-candidate CSVs. |
| Source-only research overview DOCX | `docs/project_blueprints/North_Slope_Gas_Hydrate_Equation_Focused_Research_Overview_Paper_Sources_Only_2026-06-17.docx` | Word/source support, not raw approved data. |

## Assets Still Missing

- Remote branches matching `codex/delegated-*-20260618`.
- Final combined North Slope map with all new GeoPackage layers.
- Header-only verification tying the three approved workbooks to the active
  four wells.
- Verified source-backed core, NMR, pressure-core, lithology, grain-size,
  porosity, and hydrate-saturation authority for each active well.
- Final realistic Slide 3 log scaffold and Slide 6 evidence-review board.
- Native editable slide builder output for final manual text editing.

## Placement Decisions

| destination | belongs there | does not belong there |
|---|---|---|
| GitHub | Public-safe handoff reports, source-backed docs, public map exports, source manifests, generator scaffolds, tests, synthetic/header-only examples. | Approved rows, raw workbooks, row-level predictions, trained models, fitted scalers, runtime manifests, credentials, private screenshots, heavy raw source bundles. |
| Drive | Latest self-email deck attachment, review decks, source PDFs/figures that need rights/caption review, shareable ZIPs from the PC. | Runtime model artifacts or raw approved rows unless access is explicitly controlled. |
| OpenScienceLab | Raw approved workbooks, LAS/CSV/core/NMR rows, header-only scans, DOE runtime outputs, model experiments, reviewed public-safe exports before release. | Public website-only generated placeholders that can be reproduced in GitHub. |
| Website | Public-safe maps, source inventories, schema readiness, guardrails, presentation exports, non-result planning visuals. | Private rows, row-level predictions, final metrics, or hydrate proof claims. |
| Word | Detailed citations, caveats, formula derivations, source explanations, full complex architecture, rights/caption notes. | Crowded slide-face text. |
| Slides | Large visuals, editable labels/callouts, concise claims, source-backed figures, guarded context notes. | Tiny citations, raw source tables, unsupported results, or whole-slide screenshots when manual editing is required. |

## Decisions Needed From User Or Mentor

1. Confirm which four wells are actually represented by the three approved
   workbooks.
2. Confirm whether `MLK` and `ETG` are real active well aliases or confusion
   with other project/source labels.
3. Choose the final Slide 2/Slide 7 combined map export after the new
   GeoPackage layers are integrated.
4. Decide whether the current local equation-card Slide 5 rebuild should be
   promoted or rebuilt natively.
5. Decide whether the full complex architecture remains in the main deck, Word,
   appendix, or backup material.
6. Confirm the final equation set and whether the Archie baseline should stay
   on-slide or move to Word until parameters are approved.

## Exact Next Actions For Main Codex

1. Pull this integration branch into a clean working tree.
2. Read `docs/delegated_work/2026-06-18/main_codex_thread_PROMPT_RESULTS.md`
   and `docs/delegated_work/2026-06-18/SLIDE_FINISHING_NEEDS_2026-06-18.md`.
3. Reconcile the separate current local Slide 5 equation-card work if it is
   still uncommitted in the main checkout.
4. Run the four-well header/source verification path before final Slide 3 and
   Slide 6 content.
5. Build or import the final combined map before finalizing Slide 2 and Slide 7.
6. Convert high-level slide text, labels, arrows, callouts, and simple shapes
   to native editable deck elements where practical.
7. Keep detailed citations, caveats, and source explanations in Word/end
   material.
8. Run `git diff --check` and targeted tests after the final slide-builder pass.

## Unsafe Items Excluded

No matching delegated branch contained changed file paths for approved rows,
raw workbooks, LAS files, row-level prediction outputs, trained models, fitted
scalers, runtime manifests, credential files, or heavy raw source bundles.

The current dirty main checkout contained uncommitted Slide 5 equation-card
changes and regenerated deck assets. Those local uncommitted changes were not
merged by this integration pass because they are outside the committed
delegated branch intake and need their own review/commit decision.
