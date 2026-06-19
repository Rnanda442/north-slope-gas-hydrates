# Slide 2 Methane Hydrate Context Rebuild Done / Needed Handoff

## Prompts Worked On

- Prompt 3 / Slide 2 hydrate and North Slope context rebuild.
- Topic: concise source-backed introduction to methane hydrate and why the Alaska North Slope matters.

## Done

- Built a new Slide 2 rebuild package without overwriting the active V5.5 deck.
- Created a full nine-slide V5.5 deck copy with Slide 2 replaced by editable PowerPoint labels, cards, callouts, and guardrails over source/data figure objects.
- Created a one-slide editable PPTX for Slide 2 only.
- Created a PNG preview for quick visual review.
- Used one combined 2D North Slope map crop from the unified public map stack.
- Generated a CSV-derived methane 5 ppt P-T diagram from `data/public_stability_products/phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1.csv`.
- Used the cleaned Structure I/II/H hydrate-structure figure and added an editable Structure I highlight/callout in the PPTX.
- Added concise source-backed wording for:
  - Structure I as methane-rich baseline;
  - Structure II as larger gases / mixed gas;
  - Structure H as larger hydrocarbon plus methane;
  - biogenic methane versus thermogenic C2+ gas shifting stability;
  - USGS 2018 mean estimate of about 54 Tcf technically recoverable North Slope hydrate gas.
- Used the existing USGS Arctic Alaska regional cross-section crop for source-backed cross-section context.
- Kept detailed source notes off the slide face and in companion/handoff material.
- Preserved guardrail language: stability context only, not hydrate proof, occurrence, saturation, producibility, or ranking.
- Added the new Slide 2 preview, P-T diagram, and unified map crop to `data/public_ml_products/source_visual_inventory_2026-06-16.csv`.

## Still Needed

- Main Codex should decide whether this Slide 2 rebuild replaces the active V5.5 Slide 2 or stays as a candidate.
- A source-backed east-west anticline/stability-zone cross-section was not found in the local indexed evidence. Do not invent it. Add it only if a source figure or defensible redraw-after-source basis is recovered.
- Figure/caption rights still need review for the World Atlas Structure I/II/H source image before public release.
- If this deck is imported to Google Slides, verify the editable text boxes, cards, circle, and callouts remain editable after import.
- The final slide should pull detailed citations from the Word companion, not add tiny source text on the slide.

## Files / Assets

- Created: `docs/project_blueprints/build_slide2_methane_hydrate_context_rebuild.py`
- Created: `docs/project_blueprints/V5_5_SLIDE2_METHANE_CONTEXT_REBUILD_North_Slope_Gas_Hydrate_ML_Workflow_Slides_2026-06-19.pptx`
- Created: `docs/project_blueprints/presentation_assets/slide2_methane_context_2026_06_19/slide_02_methane_hydrate_context_editable_2026_06_19.pptx`
- Created: `docs/project_blueprints/presentation_assets/slide2_methane_context_2026_06_19/slide_02_methane_hydrate_context_rebuild_2026_06_19.png`
- Created: `docs/project_blueprints/presentation_assets/slide2_methane_context_2026_06_19/methane_5ppt_pt_diagram_from_csv_2026_06_19.png`
- Created: `docs/project_blueprints/presentation_assets/slide2_methane_context_2026_06_19/unified_north_slope_map_crop_slide2_2026_06_19.png`
- Created: `docs/project_blueprints/presentation_assets/slide2_methane_context_2026_06_19/hydrate_structure_i_ii_h_crop_slide2_2026_06_19.png`
- Edited: `data/public_ml_products/source_visual_inventory_2026-06-16.csv`
- Created: `docs/delegated_work/2026-06-19/slide2_methane_hydrate_context_rebuild_done_needed.md`

## Branch / Commit

- Branch: `codex/delegated-slide-intake-20260618`
- Commit: see final response or `git log -1 --oneline` for the pushed commit hash.

## Slides Affected

- Slide 2 directly.
- Slide 7 indirectly because the same unified North Slope map family can feed Slide 7, but this work did not rebuild Slide 7.

## Main Codex Next Steps

- Inspect the PNG preview and open the one-slide editable PPTX.
- If acceptable, use the full deck copy as the next candidate deck or port the editable Slide 2 objects into the final deck.
- Keep the P-T wording as `P-T diagram`, not `P-T gate`.
- Do not add `project website` wording to the slide.
- Keep the east-west anticline/stability-zone visual as a source-recovery item until a real source-backed section is found.
- Run a Google Slides or PowerPoint editability check before declaring this final.
