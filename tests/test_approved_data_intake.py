from __future__ import annotations

from pathlib import Path

import pandas as pd

from dashboard.approved_data_intake import (
    EXPECTED_ROLES,
    intake_validation_report_frame,
    load_approved_data_field_role_table,
    validate_approved_data_intake,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_field_role_table_loads_expected_roles():
    table = load_approved_data_field_role_table(PROJECT_ROOT)

    assert not table.empty
    assert set(table["role"]).issubset(EXPECTED_ROLES)
    assert {"Sgh", "Sh", "NMR_SAT", "Hydrate Saturation"}.issubset(
        set(table["original_header"])
    )


def test_valid_minimal_predictor_headers_are_recognized_but_not_training_ready():
    report = validate_approved_data_intake(
        ["DEPTH", "GR", "RHOB", "Rt"],
        project_root=PROJECT_ROOT,
        split_registry_present=True,
    )

    assert report["unknown_headers"] == []
    assert report["minimum_viable_predictor_coverage"]["ready"] is True
    assert report["training_ready"] is False
    assert "approved_rows_not_loaded_public_safe_validator" in report["blocked_reasons"]
    assert "no_approved_target_authority_for_training" in report["blocked_reasons"]


def test_missing_depth_blocks_intake():
    report = validate_approved_data_intake(["GR", "RHOB", "Rt"], project_root=PROJECT_ROOT)

    assert "depth_basis" in report["missing_required_fields"]
    assert "missing_required_field:depth_basis" in report["blocked_reasons"]
    assert report["minimum_viable_predictor_coverage"]["ready"] is False


def test_target_only_fields_are_rejected_from_x_allowed():
    report = validate_approved_data_intake(
        ["DEPTH", "GR", "RHOB", "Rt", "Sgh", "Sh", "NMR_SAT", "Hydrate Saturation"],
        project_root=PROJECT_ROOT,
        x_allowed_columns=["DEPTH", "GR", "Sgh", "Hydrate Saturation"],
    )

    assert report["target_leakage_risk"] is True
    assert set(report["target_leakage_fields"]) == {"Sgh", "Hydrate Saturation"}
    assert "target_leakage_risk_in_x_allowed" in report["blocked_reasons"]


def test_unconfirmed_resistivity_aliases_remain_unresolved():
    report = validate_approved_data_intake(["DEPTH", "GR", "AO90", "AF90"], project_root=PROJECT_ROOT)

    assert set(report["unresolved_header_fields"]) == {"AO90", "AF90"}
    assert "unresolved_header:AO90" in report["blocked_reasons"]
    assert "unresolved_header:AF90" in report["blocked_reasons"]


def test_stability_fields_are_context_only_and_allowed_in_x_allowed():
    report = validate_approved_data_intake(
        pd.DataFrame(columns=["DEPTH", "GR", "RHOB", "Rt", "public stability context"]),
        project_root=PROJECT_ROOT,
        x_allowed_columns=["DEPTH", "GR", "RHOB", "Rt", "public stability context"],
    )

    assert report["target_leakage_risk"] is False
    assert report["stability_context_fields"] == ["public stability context"]
    assert "public stability context" not in report["target_only_fields_detected"]


def test_occurrence_targets_require_source_confidence_interval_policy():
    report = validate_approved_data_intake(
        ["DEPTH", "GR", "Rt", "core hydrate observation"],
        project_root=PROJECT_ROOT,
    )

    assert report["occurrence_target_fields"] == ["core hydrate observation"]
    assert report["occurrence_target_authority_present"] is False
    assert (
        "occurrence_target_requires_source_confidence_interval_policy"
        in report["blocked_reasons"]
    )

    approved_report = validate_approved_data_intake(
        ["DEPTH", "GR", "Rt", "core hydrate observation"],
        project_root=PROJECT_ROOT,
        occurrence_policy_present=True,
    )
    assert approved_report["occurrence_target_authority_present"] is True


def test_saturation_targets_require_fraction_or_percent_policy():
    report = validate_approved_data_intake(
        ["DEPTH", "GR", "Rt", "Sh"],
        project_root=PROJECT_ROOT,
    )

    assert report["saturation_target_fields"] == ["Sh"]
    assert report["saturation_target_authority_present"] is False
    assert "saturation_target_requires_fraction_or_percent_unit_policy" in report["blocked_reasons"]

    approved_report = validate_approved_data_intake(
        ["DEPTH", "GR", "Rt", "Sh"],
        project_root=PROJECT_ROOT,
        saturation_unit_convention="fraction",
    )
    assert approved_report["saturation_target_authority_present"] is True


def test_whole_well_split_required_before_train_only_preprocessing_ready():
    report = validate_approved_data_intake(
        ["DEPTH", "GR", "RHOB", "Rt"],
        project_root=PROJECT_ROOT,
        train_only_preprocessing_requested=True,
    )

    assert report["train_only_preprocessing_ready"] is False
    assert (
        "whole_well_split_required_before_train_only_preprocessing"
        in report["blocked_reasons"]
    )

    split_report = validate_approved_data_intake(
        ["DEPTH", "GR", "RHOB", "Rt"],
        project_root=PROJECT_ROOT,
        split_registry_present=True,
        train_only_preprocessing_requested=True,
    )
    assert split_report["train_only_preprocessing_ready"] is True


def test_validation_report_frame_is_compact_and_public_safe():
    report = validate_approved_data_intake(["DEPTH", "GR", "RHOB", "Rt"], project_root=PROJECT_ROOT)
    frame = intake_validation_report_frame(report)

    assert list(frame.columns) == ["check", "value", "meaning"]
    assert "training_ready" in set(frame["check"])
