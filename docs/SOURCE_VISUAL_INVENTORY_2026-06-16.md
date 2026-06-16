# Source Visual Inventory 2026-06-16

This file documents the public-safe visual provenance layer used by the
website, V5.3 slide deck, and V5.3 Word companion.

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
uncited or AI-looking visuals. It tracks the current V5.3 slide panels, current
website captures, the expanded architecture plate, the ML runtime plate, and
the V5.3 contact sheet with:

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

The current inventory passes those checks. Slide 2 remains marked
`review_caption_only` because it includes source-backed hydrate and pressure-
temperature context visuals whose captions must stay tied to cited source
anchors.

## Use In Future Deck/Doc Work

Use these visuals first:

- North Slope map/context:
  `docs/project_blueprints/presentation_assets/v5_3_website_captures/02_explore_regional_map.png`
- parameter ranges:
  `docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_16_v5_3/slide_03_parameter_ranges_v5_3.png`
- parameter evidence:
  `docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_16_v5_3/slide_05_parameter_evidence_visuals_v5_3.png`
- stability schematic:
  `docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_16_v5_3/slide_06_stability_physics_v5_3.png`
- simplified workflow:
  `docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_16_v5_3/slide_04_simplified_workflow_v5_3.png`
- validation outputs:
  `docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_16_v5_3/slide_08_validation_uncertainty_outputs_v5_3.png`
- expanded architecture:
  `docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_16_v5_3/full_project_ml_workflow_flowchart_expanded.png`
- ML runtime detail:
  `docs/project_blueprints/presentation_assets/full_workflow_diagram_2026_06_16_v5_3/ml_pipeline_network_detail_v5.png`

Do not add untracked slide visuals to a final deck without updating this
inventory and rerunning tests.
