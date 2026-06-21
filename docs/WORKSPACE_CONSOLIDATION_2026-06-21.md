# Workspace Consolidation - 2026-06-21

## Canonical Workspace

Use this local path for new slide, website, source, and handoff work:

`C:\Users\gargi\Documents\AI powerpoint\north-slope-gas-hydrates-unified`

Branch:

`codex/unified-slide-workspace-20260621`

The older sibling directories are preserved as safety worktrees. Do not use
them for new slide edits unless this unified branch is missing a file and the
missing file is explicitly copied forward.

## Merged Branches

The unified branch merges the pushed safe work from:

- `main` local unpushed commit `5c42f95`
- `origin/codex/source-alignment-publish`
- `origin/codex/delegated-main_codex_thread-20260618`
- `origin/codex/delegated-slide-intake-20260618`
- `origin/codex/prompt-execution-audit-20260619`
- `origin/codex/prompts-11-20-audit-20260619`
- `origin/codex/prompts-11-13-laptop-20260619`
- `origin/codex/prompts-14-17-20260619`
- `origin/codex/prompt15-visible-header-mapping-20260619`
- `origin/codex/editable-deck-rebuild-source-20260619`
- `origin/codex/four-well-core-data-source-hunt-20260619`
- `origin/codex/editable-rebuild-deck-output-20260619`
- `origin/codex/doe-equation-visual-generator`
- `origin/codex/stability-map-focus-20260619`

## Local-Only Items Brought Forward

- `docs/project_blueprints/SLIDE2_DETAILED_REBUILD_PLAN_2026-06-20.md`
- `docs/project_blueprints/presentation_assets/v5_5_slide2_source_update_2026_06_17/slide_05_equation_cards_v5_5.png`
- `docs/source_library_index/FOUR_WELL_CORE_DATA_AUDIT_2026-06-20.md`
- `.gitignore` entry for website map `_tile_cache/`
- `docs/source_library_index/FOUR_WELL_CASE_LOCATION_INDEX_2026-06-19.md` link to the core/source audit

## Not Auto-Merged

The dirty original `north-slope-gas-hydrates` worktree still has modified V5.5
builder outputs and older deck binaries. Those were not copied over because the
current slide-cleanup path is the Drive-native editable deck, not overwriting
the older V5.5 baseline package. Keep that worktree until the user approves
archiving/removing it.

The dirty `north-slope-gas-hydrates-website-map-update` worktree still has:

- `references/hydrate-ml-physics-sources/2026-06-13/s13202-022-01531-z.pdf`
- `references/hydrate-ml-physics-sources/2026-06-13/rajabi_2023_shear_velocity_screenshots/`
- `tmp/`
- local Rajabi source-manifest edits pointing to the raw PDF/screenshots

Those are excluded from GitHub for now as raw/heavy source material. If Rajabi
is needed later, add a public-safe source note or Drive/OSL pointer without
committing the raw bundle.

## Pull Command

On another machine after this branch is pushed:

```bash
git fetch origin
git switch -c codex/unified-slide-workspace-20260621 origin/codex/unified-slide-workspace-20260621
```

If the branch already exists locally:

```bash
git fetch origin
git switch codex/unified-slide-workspace-20260621
git pull --ff-only
```

## Cleanup Rule

Do not delete old worktrees yet. After the user confirms the unified branch has
everything needed, the old worktrees can be archived or removed in a separate
explicit cleanup step.
