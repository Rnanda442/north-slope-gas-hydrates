from __future__ import annotations

from pathlib import Path

import pandas as pd

from dashboard.approved_data_intake import (
    EXPECTED_ROLES,
    build_intake_readiness_report,
    build_variable_fingerprints,
    intake_validation_report_frame,
    load_field_role_table,
    load_approved_data_field_role_table,
    validate_caliper_gate,
    validate_missing_log_strategy,
    validate_saturation_target_authority,
    validate_x_allowed,
    validate_approved_data_intake,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_field_role_table_loads_expected_roles():
    table = load_field_role_table(PROJECT_ROOT)

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
        [
            "DEPTH",
            "GR",
            "RHOB",
            "Rt",
            "Sgh",
            "S_h",
            "Sh",
            "NMR_SAT",
            "Hydrate Saturation",
            "Swr",
            "interpreted phase label",
        ],
        project_root=PROJECT_ROOT,
        x_allowed_columns=[
            "DEPTH",
            "GR",
            "Sgh",
            "S_h",
            "Hydrate Saturation",
            "Swr",
            "interpreted phase label",
        ],
    )

    assert report["target_leakage_risk"] is True
    assert set(report["target_leakage_fields"]) == {
        "Sgh",
        "S_h",
        "Hydrate Saturation",
        "Swr",
        "interpreted phase label",
    }
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


def test_variable_fingerprint_contract_marks_targets_and_unresolved_fields():
    table = load_approved_data_field_role_table(PROJECT_ROOT)
    fingerprints = build_variable_fingerprints(table)

    assert {
        "original_header",
        "unit",
        "normalized",
        "role",
        "allowed_in_feature_matrix",
        "leakage_risk",
        "unresolved_mentor_question",
    }.issubset(fingerprints.columns)
    sgh = fingerprints[fingerprints["original_header"].eq("Sgh")].iloc[0]
    ao90 = fingerprints[fingerprints["original_header"].eq("AO90")].iloc[0]
    assert bool(sgh["allowed_in_feature_matrix"]) is False
    assert sgh["leakage_risk"] == "high"
    assert bool(ao90["allowed_in_feature_matrix"]) is False
    assert ao90["role"] == "unresolved"


def test_validate_x_allowed_blocks_target_calibration_unresolved_and_unknown():
    table = load_approved_data_field_role_table(PROJECT_ROOT)
    report = validate_x_allowed(["DEPTH", "GR", "Sgh", "Swr", "AO90", "mystery"], table)

    assert report["valid"] is False
    assert "Sgh" in report["blocked_headers"]
    assert "Swr" in report["blocked_headers"]
    assert "AO90" in report["blocked_headers"]
    assert "mystery" in report["unknown_headers"]
    assert any(flag.startswith("target_only_in_x_allowed:Sgh") for flag in report["leakage_flags"])


def test_new_readiness_report_keeps_schema_design_separate_from_training():
    table = load_approved_data_field_role_table(PROJECT_ROOT)
    report = build_intake_readiness_report(
        ["DEPTH", "GR", "RHOB", "Rt", "core hydrate observation", "Sh"],
        table,
        options={
            "metadata": {
                "occurrence_evidence_source": "core",
                "occurrence_confidence": "mentor_reviewed",
                "occurrence_interval_policy": "well_depth_interval",
                "authoritative_saturation_field": "Sh",
                "saturation_unit_convention": "fraction",
            },
            "split_policy_confirmed": True,
            "validation_plan_confirmed": True,
        },
    )

    assert report["ready_for_schema_design"] is True
    assert report["ready_for_training"] is False
    assert "approved_rows_not_loaded_public_safe_validator" in report["blocked_reasons"]
    assert report["occurrence_target_authority"]["authority_present"] is True
    assert report["saturation_target_authority"]["authority_present"] is True


def test_caliper_missing_warns_without_auto_filtering():
    missing = validate_caliper_gate(["DEPTH", "GR", "RHOB", "Rt"])
    present = validate_caliper_gate(["DEPTH", "GR", "RHOB", "Rt", "CAL1"])

    assert missing["missing_qc_flag_required"] is True
    assert missing["washout_qc_filter_allowed"] is False
    assert present["has_caliper_coverage"] is True
    assert present["washout_qc_filter_allowed"] is True


def test_missing_log_adapter_requires_explicit_option():
    blocked = validate_missing_log_strategy(["DEPTH", "GR", "Rt"], allow_missing_log_adapters=False)
    allowed = validate_missing_log_strategy(["DEPTH", "GR", "Rt"], allow_missing_log_adapters=True)

    assert set(blocked["missing_optimal_logs"]) == {"Vp", "RHOB"}
    assert "missing_log_adapter_blocked_until_mentor_approval" in blocked["blocked_reasons"]
    assert allowed["missing_log_adapter_allowed"] is True
    assert allowed["validation_required"] is True


def test_new_saturation_authority_requires_authoritative_field_and_unit():
    table = load_approved_data_field_role_table(PROJECT_ROOT)
    blocked = validate_saturation_target_authority(["DEPTH", "GR", "Sh"], table)
    ready = validate_saturation_target_authority(
        ["DEPTH", "GR", "Sh"],
        table,
        metadata={"authoritative_saturation_field": "Sh", "saturation_unit_convention": "percent"},
    )

    assert blocked["authority_present"] is False
    assert ready["authority_present"] is True


def test_split_and_validation_policy_required_before_training_readiness():
    table = load_approved_data_field_role_table(PROJECT_ROOT)
    report = build_intake_readiness_report(
        ["DEPTH", "GR", "RHOB", "Rt", "Sh"],
        table,
        options={
            "metadata": {
                "authoritative_saturation_field": "Sh",
                "saturation_unit_convention": "fraction",
            },
            "approved_rows_available": True,
        },
    )

    assert report["ready_for_training"] is False
    assert "whole_well_compartment_or_geographic_split_policy_required" in report["blocked_reasons"]
    assert "validation_plan_required_before_training" in report["blocked_reasons"]
