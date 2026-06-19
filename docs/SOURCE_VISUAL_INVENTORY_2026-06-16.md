# Source Visual Inventory 2026-06-16

This file documents the public-safe visual provenance layer used by the
website, V5.5 mentor update slide deck, and V5.5 Word companion.

## Product

- Inventory CSV:
  `data/public_ml_products/source_visual_inventory_2026-06-16.csv`
- Loader and QA checks:
  `dashboard/source_visual_inventory.py`
- Website surface:
  `Analyze Hydrates > Presentation Exports`
- Tests:
  `tests/test_source_visual_inventory.py`

## Purpose

The inventory prevents the slide and website workflow from drifting back to
uncited or AI-looking visuals. It tracks the current V5.5 slide panels, current
website captures, source-backed figures, authority diagrams, V5.4/V5.3
reference panels, and the V5.5 contact sheet with:

- local path or URL;
- slide/site use;
- visual type;
- source status;
- provenance;
- allowed use;
- QA status;
- replacement flag;
- project guardrail.

## Current QA Rule

Rows must pass these checks before being treated as active deck/website
visuals:

- all required columns exist;
- every local path exists;
- no row is marked uncited, AI-looking, or AI-generated;
- QA status is one of the allowed public-safe values;
- guardrail text prevents unsupported hydrate-proof, occurrence-prediction,
  saturation-prediction, model-metric, or approved-row claims.

The current inventory passes those checks. V5.5 slide 2 is now source-backed by
the selected USGS/DOE page-3 source screenshot and cropped stability curve, the
project digitized methane 5 ppt CSV inset, and the project website regional map
capture. Captions must stay tied to those source anchors, and the slide must
continue to say that stability is pressure-temperature admissibility context
only, not hydrate proof, occurrence evidence, or saturation evidence.

## Use In Future Deck/Doc Work

Use these visuals first:

- North Slope map/context:
  `docs/project_blueprints/presentation_assets/v5_3_website_captures/02_explore_regional_map.png`
- hydrate context:
  `docs/project_blueprints/presentation_assets/v5_5_slide2_source_update_2026_06_17/slide_02_source_context_v5_5.png`
- Slide 2 source bundle:
  `docs/evidence/slide02_source_bundle_2026_06_17/`
- parameter ranges:
  `docs/project_blueprints/presentation_assets/v5_5_slide2_source_update_2026_06_17/slide_03_parameter_ranges_v5_5.png`
- DOE three-dataset prototype and model-run card:
  `docs/project_blueprints/presentation_assets/v5_5_slide2_source_update_2026_06_17/slide_05_doe_three_dataset_prototype_v5_5.png`
- equations and unit gate:
  `docs/project_blueprints/presentation_assets/v5_5_slide2_source_update_2026_06_17/slide_06_equations_feature_unit_gate_v5_5.png`
- full complex workflow:
  `docs/project_blueprints/presentation_assets/v5_5_slide2_source_update_2026_06_17/slide_04_full_complex_project_workflow_v5_5.png`
- stability-to-ML overlay:
  `docs/project_blueprints/presentation_assets/v5_5_slide2_source_update_2026_06_17/slide_08_stability_to_ml_overlay_v5_5.png`
- ML runtime detail:
  `docs/project_blueprints/presentation_assets/v5_5_slide2_source_update_2026_06_17/slide_07_complex_ml_runtime_architecture_v5_5.png`
- done / not claimed / next:
  `docs/project_blueprints/presentation_assets/v5_5_slide2_source_update_2026_06_17/slide_09_done_not_claimed_next_v5_5.png`

Do not add untracked slide visuals to a final deck without updating this
inventory and rerunning tests.
