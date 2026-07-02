# main_codex_thread Done / Needed Handoff

## Prompts Worked On

- Prompt 5: four-well data, core, lithology, and location recovery.
- Prompt 7: Slide 4 simplified ML architecture and two-minute script.
- Prompt 9: Slide 6 high-level visual cleanup.
- Delegation/coordination prompts for collecting PC/laptop chat reports.

## Done

- Verified from the committed source-safe notes that `MTE` / `Well-MTE` maps to
  Mount Elbert and `IGS` / `Well-IGS` maps to Ignik Sikumi.
- Identified `MTE_refined` and `IGS_refined` as unresolved workbook-stage
  questions, not verified separate wells.
- Flagged `MLK` and `ETG` as unverified names because they were not found in
  the committed docs reviewed here.
- Planned Slide 4 as a simple audience-facing workflow: inputs, preparation,
  leakage barrier, separate occurrence/saturation paths, validation, and
  reviewed exports.
- Wrote a two-minute Slide 4 talk track.
- Planned Slide 6 as a high-level four-well evidence-review visual instead of
  the current crowded equation/unit-gate raster panel.
- Confirmed current Slide 6 in the active V5.5 deck is a single picture shape,
  meaning it is not editable as native slide text/shapes.
- Created and pushed the earlier handoff report:
  `docs/delegated_work/2026-06-18/main_codex_thread_PROMPT_RESULTS.md`.

## Still Needed

- Pull the actual four PC/laptop chat reports once those chats provide branch,
  commit, and report paths.
- Confirm the real four-well mapping from the three approved workbooks using
  header-only workbook metadata or `wellnametodataset.txt`.
- Decide whether `MTE_refined` and `IGS_refined` are refined sheets or separate
  wells.
- Verify whether `MLK` or `ETG` are real well aliases from screenshots,
  workbook metadata, or source captions.
- Review the existing local uncommitted deck/builder/PNG changes separately;
  this thread did not claim ownership of those changes.
- Build the actual editable Slide 4 and Slide 6 in the deck.
- Confirm final source-backed equation set for Slide 5.
- Confirm which unified map export is accepted for Slide 2 and Slide 7.

## Files / Assets

Created by this thread:

- `docs/delegated_work/2026-06-18/main_codex_thread_PROMPT_RESULTS.md`
- `docs/delegated_work/2026-06-19/main_codex_thread_done_needed.md`

Pre-existing local modified files observed but not created or staged by this
handoff:

- `data/public_ml_products/source_visual_inventory_2026-06-16.csv`
- `docs/CURRENT_ARTIFACT_INDEX.md`
- `docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md`
- `docs/project_blueprints/build_full_workflow_diagram_deliverables.py`
- active V5.5 deck and companion binaries
- multiple regenerated V5.5 slide panel PNGs
- untracked `slide_05_equation_cards_v5_5.png`
- `tests/test_source_visual_inventory.py`

## Branch / Commit

Earlier pushed handoff:

- Branch: `codex/delegated-main_codex_thread-20260618`
- Commit: `0c49412ab6ff09d39f48ef62cef8416318a82926`

This 2026-06-19 done/needed report should be committed on the same branch unless
the user asks for a separate branch.

## Slides Affected

- Slide 3: needs four-well log-signal, lithology, and core/NMR source
  verification.
- Slide 4: ready to build from the simplified ML architecture plan and
  two-minute script.
- Slide 5: needs final source-backed equation set.
- Slide 6: should become a high-level four-well evidence-review visual.
- Slide 7: should use stability map as context only.
- Slides 8-9: should stay guarded results/discussion plan slides, not final
  results.

## Main Codex Next Steps

1. Get the four PC/laptop chat branch names, commit hashes, and report paths.
2. Pull the actual delegated reports and create one accumulated slide next-step
   overview.
3. Review the local uncommitted equation/deck-builder changes before deciding
   whether to keep them.
4. Verify four-well identities and core/lithology/NMR evidence before finalizing
   Slides 3 and 6.
5. Build editable Slide 4 and Slide 6 from the plans already produced here.
