from __future__ import annotations

from pathlib import Path

from dashboard.parameter_evidence import (
    TARGET_TIER,
    load_parameter_evidence_registry,
    parameter_evidence_summary_frame,
    validate_parameter_evidence_registry,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_parameter_evidence_registry_loads_core_families():
    registry = load_parameter_evidence_registry(PROJECT_ROOT)

    assert not registry.empty
    assert {
        "Pressure-temperature stability",
        "Gamma ray clean-sand proxy",
        "Deep resistivity response",
        "NMR porosity and NMR-density separation",
        "Occurrence and saturation labels",
    }.issubset(set(registry["parameter_family"]))


def test_parameter_evidence_registry_windows_are_valid_and_targets_are_y_only():
    registry = load_parameter_evidence_registry(PROJECT_ROOT)
    validation = validate_parameter_evidence_registry(registry)

    assert validation["valid"] is True
    target_rows = registry[registry["tier"].eq(TARGET_TIER)]
    assert len(target_rows) == 1
    assert target_rows["hydrate_window_norm_start"].iloc[0] == 0
    assert target_rows["hydrate_window_norm_end"].iloc[0] == 0
    assert "never enter the feature matrix" in target_rows["public_guardrail"].iloc[0]


def test_parameter_evidence_summary_separates_working_ranges_from_directional_rows():
    registry = load_parameter_evidence_registry(PROJECT_ROOT)
    summary = parameter_evidence_summary_frame(registry)
    lookup = dict(zip(summary["metric"], summary["value"]))

    assert lookup["Parameter evidence rows"] == len(registry)
    assert lookup["Registry validation"] == "pass"
    assert lookup["Y-only target rows"] == 1
    assert lookup["Working screening-envelope rows"] >= 5
    assert lookup["Directional-only rows"] >= 2


def test_resistivity_and_stability_guardrails_prevent_overclaiming():
    registry = load_parameter_evidence_registry(PROJECT_ROOT)
    resistivity = registry[registry["parameter_family"].eq("Deep resistivity response")].iloc[0]
    stability = registry[registry["parameter_family"].eq("Pressure-temperature stability")].iloc[0]

    assert "High resistivity alone is not hydrate proof." == resistivity["public_guardrail"]
    assert "Admissible is not proof" in stability["public_guardrail"]
    assert "10-100+" in resistivity["working_screening_envelope"]
