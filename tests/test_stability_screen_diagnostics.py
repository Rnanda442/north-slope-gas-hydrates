from __future__ import annotations

from pathlib import Path

from dashboard.app import (
    build_selected_well_phase_audit_figure,
    g10015_temperature_control_crosswalk_frame,
    stability_blank_reason_summary_frame,
    temperature_proxy_candidate_audit_frame,
    temperature_proxy_tier_summary_frame,
)
from dashboard.stability_products import (
    load_methane_phase_curve,
    load_g10015_temperature_inventory,
    load_stability_screen,
    load_stability_temperature_model,
)
from dashboard.stability_sources import (
    active_stability_source_path,
    load_ggd223_permafrost_points,
)


def test_committed_stability_screen_diagnostics_explain_blanks_and_proxy_tiers() -> None:
    project_root = Path(__file__).resolve().parents[1]
    source_root = active_stability_source_path(project_root)
    screen = load_stability_screen(project_root)
    inventory = load_g10015_temperature_inventory(project_root)
    controls = load_ggd223_permafrost_points(source_root).drop(
        columns="geometry",
        errors="ignore",
    )

    crosswalk = g10015_temperature_control_crosswalk_frame(inventory, controls)
    crosswalk_counts = crosswalk["coordinate_status"].value_counts().to_dict()
    assert crosswalk_counts["located_from_committed_ggd223_control"] == 22
    assert crosswalk_counts["missing_committed_coordinate_crosswalk"] == 2

    blank_summary = stability_blank_reason_summary_frame(screen)
    blank_counts = blank_summary.set_index("status_code")["rows"].to_dict()
    assert blank_counts["blocked_missing_temperature_profile"] == 7113
    assert blank_counts["blocked_missing_depth"] == 505
    assert blank_counts["blocked_phase_curve_range_insufficient"] == 344
    assert blank_counts["outside_au_context"] == 92

    proxy_audit = temperature_proxy_candidate_audit_frame(screen, crosswalk)
    proxy_summary = temperature_proxy_tier_summary_frame(proxy_audit)
    proxy_counts = proxy_summary.set_index("tier_code")["rows"].to_dict()
    assert proxy_counts["direct_g10015_profile_match"] == 483
    assert proxy_counts["proxy_candidate_near_g10015_control"] == 193
    assert proxy_counts["proxy_candidate_regional_g10015_control"] == 4917
    assert proxy_counts["distant_from_g10015_controls"] == 2003


def test_selected_well_phase_audit_figure_uses_public_temperature_and_phase_products() -> None:
    project_root = Path(__file__).resolve().parents[1]
    screen = load_stability_screen(project_root)
    temperature_model = load_stability_temperature_model(project_root)
    phase_curve = load_methane_phase_curve(project_root)
    calculated_row = screen[screen["stability_result_status"].eq("calculated")].iloc[0]

    figure = build_selected_well_phase_audit_figure(
        calculated_row,
        temperature_model,
        phase_curve,
    )

    trace_names = {trace.name for trace in figure.data}
    assert "Methane 5 ppt phase boundary" in trace_names
    assert "OSL modeled temperature key depths" in trace_names
    assert "Screen top/base" in trace_names
