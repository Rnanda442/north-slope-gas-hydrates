from __future__ import annotations

from pathlib import Path

from dashboard.source_visual_inventory import (
    SOURCE_CARD_COLUMNS,
    SOURCE_VISUAL_INVENTORY_COLUMNS,
    load_source_visual_inventory,
    source_card_frame,
    source_visual_inventory_summary_frame,
    validate_source_visual_inventory,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_source_visual_inventory_loads_current_v5_5_visuals():
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
        "v55_slide_05_doe_prototype",
        "v55_slide_08_stability_overlay",
        "v55_slide_09_done_next",
        "v55_contact_sheet",
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


def test_source_cards_expose_reuse_claims_and_guardrails():
    inventory = load_source_visual_inventory(PROJECT_ROOT)
    cards = source_card_frame(inventory)

    assert set(SOURCE_CARD_COLUMNS).issubset(cards.columns)
    assert len(cards) == len(inventory)
    assert cards[SOURCE_CARD_COLUMNS].replace("", None).notna().all().all()

    methane_curve = cards[
        cards["public_safe_link_or_path"].str.contains(
            "phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1.csv",
            regex=False,
        )
    ].iloc[0]
    assert methane_curve["source_category"] == "Source-backed data"
    assert "admissibility" in methane_curve["not_allowed_use"].lower()
    assert "occurrence" in methane_curve["not_allowed_use"].lower()
    assert "saturation" in methane_curve["not_allowed_use"].lower()
