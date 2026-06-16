from __future__ import annotations

from pathlib import Path

from dashboard.source_visual_inventory import (
    SOURCE_VISUAL_INVENTORY_COLUMNS,
    load_source_visual_inventory,
    source_visual_inventory_summary_frame,
    validate_source_visual_inventory,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_source_visual_inventory_loads_current_v5_3_visuals():
    inventory = load_source_visual_inventory(PROJECT_ROOT)

    assert not inventory.empty
    assert set(SOURCE_VISUAL_INVENTORY_COLUMNS).issubset(set(inventory.columns))
    assert {
        "v53_slide_02_context",
        "v53_slide_03_parameter_ranges",
        "v53_slide_06_stability",
        "v53_expanded_workflow_png",
        "v53_ml_runtime_png",
        "website_regional_map",
    }.issubset(set(inventory["visual_id"]))


def test_source_visual_inventory_local_paths_exist_and_pass_qa():
    inventory = load_source_visual_inventory(PROJECT_ROOT)
    validation = validate_source_visual_inventory(inventory, PROJECT_ROOT)

    assert validation["valid"] is True
    assert validation["missing_columns"] == []
    assert validation["missing_local_paths"] == []
    assert validation["uncited_or_ai_looking_rows"] == []
    assert validation["invalid_qa_status_rows"] == []


def test_source_visual_inventory_summary_tracks_review_and_website_captures():
    inventory = load_source_visual_inventory(PROJECT_ROOT)
    summary = source_visual_inventory_summary_frame(inventory, PROJECT_ROOT)
    lookup = dict(zip(summary["metric"], summary["value"]))

    assert lookup["Visual inventory rows"] == len(inventory)
    assert lookup["Inventory validation"] == "pass"
    assert lookup["Website capture visuals"] >= 5
    assert lookup["Project-generated visuals"] >= 10
