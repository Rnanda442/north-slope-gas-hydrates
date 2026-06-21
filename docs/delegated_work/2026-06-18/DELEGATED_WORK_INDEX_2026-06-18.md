# Delegated Work Index

Date: 2026-06-18

Integration branch: `codex/delegated-slide-intake-20260618`

Base branch inspected before intake: `website-map-update-2026-06-18`

Base commit: `1c9996a` - `Add North Slope Borough boundary to unified map`

## Branch Intake Result

After running `git fetch --all --prune`, the first local search did not show
matching delegated branches. A later explicit remote check found one matching
remote branch, which was fetched and inspected:

```text
codex/delegated-*-20260618
```

Commands used to verify and fetch:

```text
git branch -a --list "*codex/delegated-*-20260618"
git branch -a | rg "delegated|20260618|slide|intake"
git for-each-ref --format="%(refname:short) %(objectname:short) %(subject)" refs/remotes/origin | rg "codex/delegated|delegated-|20260618|slide"
git ls-remote --heads origin | rg "codex/delegated|delegated-|20260618|slide"
git fetch origin codex/delegated-main_codex_thread-20260618:refs/remotes/origin/codex/delegated-main_codex_thread-20260618
```

Matching delegated branch imported:

| delegated branch | commit | prompt coverage | intake action | safety result |
|---|---:|---|---|---|
| `origin/codex/delegated-main_codex_thread-20260618` | `0c49412` | Prompts 5, 7, 9, and coordination handoff | Imported only `docs/delegated_work/2026-06-18/main_codex_thread_PROMPT_RESULTS.md` | Markdown handoff only; no approved rows, raw workbooks, row-level predictions, trained models, fitted scalers, runtime manifests, credentialed PDFs, private screenshots, or heavy raw source bundles. |

Non-matching related branches:

| branch | commit | status for this intake |
|---|---:|---|
| `origin/codex/doe-equation-visual-generator` | `d79393b` | Already part of the project-revision base workstream; not a `delegated-*-20260618` branch. |
| `origin/codex/source-intake-20260617` | `0ce599f` | Older source-intake branch; not matched by requested pattern. |
| `origin/codex/delegated-slide-intake-20260618` | `f19aa6e` | Existing remote integration branch found after push rejection; it was based on an older project base. Its handoff docs were inspected, but the branch was not merged wholesale because that would remove newer unified-map files from the current base. |

No older-base deletes or non-handoff file changes were merged. This branch
imports the public-safe delegated Markdown report and keeps the current map
update base intact.

## Delegated Chats And Prompt Coverage

The integration branch now contains the imported delegated main-thread report,
the current main-thread done/needed handoffs, the Word companion science-support
handoff, and the current unified-map asset work. Some prompt numbers still have
no dedicated report, so those remain explicitly marked as missing rather than
treated as complete.

| prompt | topic | branch/report found? | intake status |
|---:|---|---|---|
| 0 | PC / OSL Git sync and base check | No | Not imported. Main session still needs current-machine/source sync if new artifacts exist elsewhere. |
| 1 | Latest Gmail deck intake and editable-slide audit | No | Not imported. Latest Gmail attachment remains needs-review and not committed. |
| 2 | Native editable deck rebuild plan | No | Not imported. Main session needs to choose the builder/manual edit path. |
| 3 | Slide 2 hydrate and North Slope context rebuild | No | Not imported. Current Slide 2 source-update baseline remains active. |
| 4 | Unified website and 2D well map integration | No delegated branch, but current base has completed map assets | Use current committed unified-map assets. |
| 5 | Four-well data, core, lithology, and location recovery | Yes, `main_codex_thread` | Imported source-safe finding: MTE/IGS are supported aliases; `MTE_refined`/`IGS_refined` remain workbook-stage questions; four-well mapping still needs OSL/header confirmation. |
| 6 | Slide 3 log signal and lithology visual rebuild | Yes, `main_codex_slide5_integration` handoff | Planned realistic multi-curve log panel with lithology column and core/NMR/coring strip; final build still needs verified four-well evidence. |
| 7 | Slide 4 simplified ML architecture and script | Yes, `main_codex_thread` | Imported layout guidance: inputs, preparation, leakage barrier, separate occurrence/saturation paths, validation, reviewed outputs. |
| 8 | Equation slide rebuild | Yes, `main_codex_slide5_integration` handoff | Slide 5 was rebuilt locally as equation-only review cards and validated, but the dirty slide-builder/assets still need a commit or native rebuild decision. |
| 9 | Slide 6 high-level visual cleanup | Yes, `main_codex_thread` | Imported before/after recommendation: make Slide 6 a high-level evidence-review board after moving equations to Slide 5. |
| 10 | Slides 7-9 results and discussion plan | No | Not imported. Use `SLIDE_FINISHING_NEEDS_2026-06-18.md` as the checklist seed. |
| 11 | Word companion science support | Yes, `word_companion_science_support` handoff | Word companion source-note appendix was generated and tested; main Codex should preserve it after future companion rebuilds. |

## Report Files In This Integration Branch

| report file | purpose | GitHub-safe? |
|---|---|---|
| `docs/delegated_work/2026-06-18/main_codex_thread_PROMPT_RESULTS.md` | Imported delegated report covering Prompts 5, 7, 9, and coordination handoff. | Yes |
| `docs/delegated_work/2026-06-18/DELEGATED_WORK_INDEX_2026-06-18.md` | Consolidated intake status, slide findings, asset inventory, missing items, decisions, and next actions. | Yes |
| `docs/delegated_work/2026-06-18/SLIDE_FINISHING_NEEDS_2026-06-18.md` | Concise slide-finishing checklist for the main Codex session. | Yes |
| `docs/delegated_work/2026-06-19/main_codex_thread_done_needed.md` | Done/needed handoff for Prompts 5, 7, 9, and coordination. | Yes |
| `docs/delegated_work/2026-06-19/word_companion_science_support_done_needed.md` | Done/needed handoff for Prompt 11 Word companion science support. | Yes |
| `docs/delegated_work/2026-06-19/main_codex_slide5_integration_done_needed.md` | Done/needed handoff for Prompts 5, 6, 8, and delegated integration status. | Yes |

## Slide-By-Slide Findings For Slides 2-9

| slide | current finding | use now | still needed |
|---:|---|---|---|
| 2 | Current V5.5 Slide 2 source update is the active baseline. It has a source-backed hydrate/context structure, but the 2026-06-18 direction asks for a stronger combined map, P-T diagram, gas hydrate structure labels, thermogenic/biogenic explanation, resource motivation, and cross-section context. | Use existing Slide 2 as baseline, not as final locked content. Use unified map assets where helpful. | Editable rebuild with concise source-backed labels; better P-T diagram/curve; corrected Structure I/II/H visual; thermogenic/biogenic and resource text in Word or notes. |
| 3 | The requested Slide 3 direction is a realistic multi-curve log/lithology/coring explanation. The main-thread and Slide 5 integration handoffs reinforce signal movement plus lithology/core context. | Use public parameter registry and header evidence as planning sources only. | Generate or build a simplified editable log panel, lithology column, curve-callout logic, and core/NMR calibration strip without approved rows after four-well evidence is verified. |
| 4 | The detailed ML runtime plate is too complex for the audience. `main_codex_thread` supplies the simplified layout and talk-track direction. | Keep complex diagram for Word/reference; use it as source material. | Build an editable simplified flow: inputs, prep/QC, leakage barrier, separate occurrence/saturation paths, validation, reviewed outputs. |
| 5 | The old three-dataset prototype slide should be replaced by an equation-only slide. A local rebuild exists and is documented, but it is not yet promoted into this integration branch's slide assets. | Use the Prompt 8 handoff plus stability/equation source docs as source, not result claims. | Decide whether to commit/promote the local equation-card rebuild, revise it, or rebuild it natively with editable labels. |
| 6 | Needs high-level visual cleanup, lower text, and source-backed visuals. `main_codex_thread` recommends a four-well evidence-review board after equations move to Slide 5. | Keep only the strongest current visual concept. | Move citations/details to Word/speaker notes; rebuild disconnected image boxes into one visual story. |
| 7 | The new unified North Slope map belongs here as context only. Current map exports exist. | Use `unified_north_slope_slide_export_callout_space_2026_06_18.png` or `unified_north_slope_well_stability_context_map_2026_06_18.png`. | Add editable caption/callouts: context only, not ML overlay, not hydrate proof, not occurrence/saturation evidence. |
| 8 | Should be a planned four-well result-review logic slide, not fake results. No delegated report found. | Use DOE runtime tracker plan and public templates for structure. | Show planned figures/tables: feature exclusion audit, log/lithology/core review, separate occurrence and saturation review, uncertainty and false-positive checks. |
| 9 | Should close with built/not claimed/next. Current V5.5 already has this idea, but the next pass should align it with the updated slide direction. | Use current V5.5 close as reference. | Make the close explicit: built scaffolds, no unsupported claims, next DOE/mentor actions. |

## Assets Available Now

| asset | location | allowed use |
|---|---|---|
| Delegated Prompt 5/7/9 handoff | `docs/delegated_work/2026-06-18/main_codex_thread_PROMPT_RESULTS.md` | Use for four-well verification caveats, Slide 4 simplified architecture, and Slide 6 cleanup direction. |
| Unified North Slope map exports | `docs/project_blueprints/presentation_assets/website_well_maps_2026_06_18/` | Slide 2 and Slide 7 map source. Context/admissibility only. |
| Unified map source candidates and README | `docs/project_blueprints/presentation_assets/website_well_maps_2026_06_18/README.md` plus CSVs in same folder | Source/layer provenance and GitHub-safe versus OSL-only layer notes. |
| Active V5.5 Slide 2 source update deck | `docs/project_blueprints/V5_5_SLIDE2_SOURCE_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Slides_2026-06-17.pptx` | Current committed deck baseline; edit through builder when possible. |
| Active V5.5 companion | `docs/project_blueprints/V5_5_SLIDE2_SOURCE_UPDATE_North_Slope_Gas_Hydrate_ML_Workflow_Companion_2026-06-17.docx` | Word baseline for detailed caveats/source logic. |
| V5.5 generated slide panels/contact sheet | `docs/project_blueprints/presentation_assets/v5_5_slide2_source_update_2026_06_17/` | Visual reference for current slide state. |
| Public ML schema and target leakage products | `data/public_ml_products/` and `data/public_stability_products/` | Public-safe schema, target-only, feature, and review templates. |
| DOE runtime code and tracker | `dashboard/runtime/`, `01_pipeline/`, `code_transfer_block/` | Public-safe code for approved-runtime execution and row-free review summaries. |

## Assets Still Missing

- Dedicated handoff reports for Prompts 0, 1, 2, 3, and 10.
- Latest Gmail attachment verified as a source/reference deck.
- Header-only workbook export from DOE/OSL mapping `curated_dataset1/2/3.xlsx`
  to visible sheets and target headers.
- Verified four-well names, aliases, locations, and core/NMR/pressure-core or
  lithology evidence.
- Slide 3 log/lithology/coring visual export or editable build.
- Native editable Slide 4 simplified audience ML diagram. The talk-track plan
  exists, but the editable slide is not built.
- Committed/natively editable Slide 5 equation-only asset. A local candidate is
  documented but still dirty outside this integration branch.
- Slide 6 high-level cleanup build. The plan exists, but the slide is not built.
- DOE row-free model-run review exports for Slide 8.
- Mentor-approved validation split, target authority, and public-safe summary
  approval.

## Decisions Needed From User Or Mentor

1. Confirm whether missing reports for Prompts 0, 1, 2, 3, and 10 should still
   be pushed or whether the main Codex should proceed from current repo assets
   and the existing handoff files.
2. Decide whether the latest Gmail deck attachment should be downloaded and
   treated as a reference artifact.
3. Confirm the slide rebuild path: reproducible `python-pptx` builder, manual
   PowerPoint cleanup, Google Slides connector edits, or hybrid.
4. Confirm four-well identities and whether the current public-safe evidence
   is enough to name only MTE/IGS until DOE header exports arrive.
5. Confirm target authority among `S_h`, `Sh`, `Sgh`, `Hydrate Saturation`,
   and `NMR_SAT`.
6. Confirm occurrence-label policy versus saturation-regression policy.
7. Confirm validation split: complete-well, geography-aware, or locked-test
   approach.
8. Confirm whether any DOE row-free model-run summaries can be copied back to
   GitHub after review.

## Destination Rules

| destination | belongs there |
|---|---|
| GitHub | Public-safe handoff docs, source summaries, code scaffolds, public GIS/map exports, schema/header templates, row-free review templates, generated public-safe figures. |
| Drive | Review decks/docs, Gmail attachment copies after verification, mentor-facing PPTX/DOCX copies, non-public but shareable source/reference material. |
| OSL / approved runtime | Approved workbooks, LAS/CSV/core/NMR rows, private identifiers, raw heavy GIS/source bundles, row-level predictions, fitted models, fitted scalers, runtime manifests. |
| Website | Public context maps, schema readiness, target leakage guardrails, row-free local tracker summaries when run inside DOE, source/caveat panels. |
| Word companion | Detailed citations, science support notes, source caveats, equations provenance, hydrate structure/gas-composition detail, false-positive logic. |
| Slides | High-level editable story, large map/plot/source figures, minimal caveats, no private rows, no unsupported result claims. |

## Exact Next Actions For Main Codex

1. Pull this integration branch and read the imported delegated handoff report:
   `git pull origin codex/delegated-slide-intake-20260618`.
2. Ask the user whether additional missing `codex/delegated-*-20260618`
   branches should be pushed or whether to proceed from current assets plus
   `main_codex_thread`.
3. Inspect the latest Gmail deck attachment only if the user authorizes
   Gmail/Drive access for that session.
4. Use the unified map export for Slide 7 with a context-only caption.
5. Build Slide 8 as a planned result-review logic slide using row-free DOE
   export placeholders.
6. Build Slide 9 as built / not claimed / next approved-runtime actions.
7. Keep details and citations in the Word companion; keep slide text concise
   and editable.
8. Do not import any raw workbooks, approved rows, runtime predictions, fitted
   models, fitted scalers, runtime manifests, credentialed PDFs, or heavy raw
   source bundles into GitHub.

## Unsafe Items Excluded

Only the public-safe delegated Markdown handoff was imported from
`origin/codex/delegated-main_codex_thread-20260618`. Older-base non-handoff
changes from `origin/codex/delegated-slide-intake-20260618` were not merged.
The integration branch intentionally excludes:

- approved/private rows;
- raw workbooks;
- private screenshots containing row values;
- row-level predictions;
- trained models or fitted scalers;
- runtime manifests;
- credentialed PDFs;
- heavy raw source bundles.
