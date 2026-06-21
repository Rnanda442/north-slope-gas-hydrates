from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from dashboard.runtime.core_calibration import match_core_intervals_to_nearest_logs
from dashboard.runtime.four_well_runtime import (
    FOUR_WELL_CORE_EVIDENCE_REGISTRY,
    FOUR_WELL_CORE_TEMPLATE,
    FOUR_WELL_LOG_TEMPLATE,
    FOUR_WELL_RUNTIME_MANIFEST_TEMPLATE,
    FOUR_WELL_SPLIT_TEMPLATE,
    run_four_well_runtime_pipeline,
)


pytest.importorskip("sklearn")


def write_four_well_public_products(project_root: Path) -> None:
    ml_dir = project_root / "data" / "public_ml_products"
    stability_dir = project_root / "data" / "public_stability_products"
    ml_dir.mkdir(parents=True)
    stability_dir.mkdir(parents=True)

    pd.DataFrame(
        [
            {
                "well_case": "MTE",
                "case_role": "workbook_header_anchor",
                "map_label": "MTE / Mount Elbert",
                "verified_public_well_name": "MT ELBERT 1",
                "suspected_aliases": "MTE; Well-MTE; Mount Elbert",
                "object_id": "6085",
                "permit_number": "2060330",
                "api_number": "50029233020000",
                "field": "MILNE POINT",
                "pool": "Unknown",
            },
            {
                "well_case": "IGS",
                "case_role": "workbook_header_anchor",
                "map_label": "IGS / Ignik Sikumi",
                "verified_public_well_name": "PRUDHOE BAY UN IGNIK SIKUMI 1",
                "suspected_aliases": "IGS; Well-IGS; Ignik Sikumi",
                "object_id": "6310",
                "permit_number": "2110270",
                "api_number": "50029234430000",
                "field": "PRUDHOE BAY",
                "pool": "Unknown",
            },
            {
                "well_case": "HYDRATE 02",
                "case_role": "public_source_case",
                "map_label": "HYDRATE 02",
                "verified_public_well_name": "HYDRATE 02",
                "suspected_aliases": "HYDRATE 02; HYDRATE 02 Geo Data Well",
                "object_id": "6596",
                "permit_number": "2221140",
                "api_number": "50029237280000",
                "field": "*EXPLORATORY",
                "pool": "UNDEFINED GAS",
            },
        ]
    ).to_csv(ml_dir / "four_well_case_location_index_2026-06-19.csv", index=False)

    pd.DataFrame(
        [
            {
                "well_case": "MTE",
                "map_label": "MTE / Mount Elbert",
                "api_number": "50029233020000",
                "object_id": "6085",
                "evidence_type": "core_and_log_core_montage",
                "source_type": "public_source_trail",
                "row_level_available": "false",
                "approved_runtime_needed": "true",
                "allowed_ml_use": "calibration_context_only",
                "prohibited_ml_use": "do_not_claim_row_level_core_training_labels",
                "current_status": "confirmed_source_no_local_rows",
                "source_anchor": "unit test source",
                "next_action": "retrieve rows",
                "notes": "synthetic public-safe evidence row",
            }
        ]
    ).to_csv(ml_dir / FOUR_WELL_CORE_EVIDENCE_REGISTRY, index=False)

    stability_rows = []
    for object_id, api_number, well_name, tvd_m in [
        ("6085", "50029233020000", "MT ELBERT 1", 914.4),
        ("6310", "50029234430000", "PRUDHOE BAY UN IGNIK SIKUMI 1", 791.5656),
        ("6596", "50029237280000", "HYDRATE 02", 1064.3616),
    ]:
        stability_rows.append(
            {
                "object_id": object_id,
                "permit_number": "permit",
                "api_number": api_number,
                "well_name": well_name,
                "field": "*EXPLORATORY",
                "pool": "Unknown",
                "current_status": "Test status",
                "lat": 70.0,
                "lon": -150.0,
                "tvd_m": tvd_m,
                "depth_source": "TrueVertic",
                "hydrate_assessment_codes": "50010201",
                "within_hydrate_assessment_unit": True,
                "permafrost_base_m": 450.0,
                "permafrost_control_distance_km": 10.0,
                "pressure_at_tvd_mpa_absolute": 9.0,
                "stability_result_status": "blocked_missing_temperature_profile",
                "stability_confidence": "blocked_missing_inputs",
                "stability_interval_calculated": False,
                "stability_top_m": pd.NA,
                "stability_base_m": pd.NA,
                "stability_thickness_m": pd.NA,
                "well_penetrated_stability_thickness_m": pd.NA,
                "reaches_stability_zone": pd.NA,
                "public_ml_feature_readiness": "blocked_missing_temperature_profile",
                "ml_training_readiness": "not_training_ready_no_validated_hydrate_labels",
                "blank_or_block_reason": "blocked_missing_temperature_profile",
                "caveat_codes": "not_hydrate_proof",
            }
        )
    pd.DataFrame(stability_rows).to_csv(
        stability_dir / "public_ml_feature_scaffold_2026-06-15.csv",
        index=False,
    )


def write_runtime_inputs(data_dir: Path) -> None:
    data_dir.mkdir(parents=True)
    rows = []
    for well_case, api_number, start_depth, offset, include_target in [
        ("MTE", "50029233020000", 500, 0.0, True),
        ("IGS", "50029234430000", 540, 2.0, True),
        ("HYDRATE 02", "50029237280000", 560, 6.0, False),
    ]:
        for index in range(8):
            rows.append(
                {
                    "well_alias": well_case,
                    "api_number": api_number,
                    "depth_m": start_depth + index * 2,
                    "GR": 42 + (index % 3),
                    "RT": 20 + offset + index * 1.2,
                    "RHOB": 2.24 - index * 0.006,
                    "Vp": 2800 + index * 12,
                    "Vs": 1300 + index * 7,
                    "Sgh": 0.18 + index * 0.015 + offset * 0.002 if include_target else pd.NA,
                }
            )
    pd.DataFrame(rows).to_csv(data_dir / "four_well_logs.csv", index=False)

    pd.DataFrame(
        [
            {
                "well_alias": "MTE",
                "api_number": "50029233020000",
                "sample_top_m": 503.5,
                "sample_base_m": 506.5,
                "hydrate_saturation_vv": 0.24,
                "sample_type": "core_interval",
                "allowed_target_use": "overlay_only",
            }
        ]
    ).to_csv(data_dir / "four_well_core_samples.csv", index=False)

    pd.DataFrame(
        [
            {"well_case": "MTE", "api_number": "50029233020000", "split": "train", "split_reason": "unit test train"},
            {"well_case": "IGS", "api_number": "50029234430000", "split": "train", "split_reason": "unit test train"},
            {"well_case": "HYDRATE 02", "api_number": "50029237280000", "split": "test", "split_reason": "unit test holdout"},
        ]
    ).to_csv(data_dir / "four_well_split_registry.csv", index=False)


def test_core_interval_match_prefers_log_rows_inside_core_interval() -> None:
    logs = pd.DataFrame(
        {
            "well_alias": ["MTE"] * 4,
            "depth_m": [500.0, 504.0, 506.0, 512.0],
            "gr_api": [45, 43, 42, 60],
            "rt_ohm_m": [10, 30, 31, 8],
            "rhob_g_cc": [2.2, 2.1, 2.12, 2.3],
        }
    )
    core = pd.DataFrame(
        {
            "well_alias": ["MTE"],
            "sample_top_m": [503.0],
            "sample_base_m": [507.0],
            "hydrate_saturation_vv": [0.25],
        }
    )

    matches = match_core_intervals_to_nearest_logs(logs, core)

    row = matches.iloc[0]
    assert row["match_status"] == "matched"
    assert row["match_method"] == "interval_overlap"
    assert row["log_rows_inside_core_interval"] == 2
    assert row["nearest_log_depth_m"] in {504.0, 506.0}


def test_four_well_runtime_trains_and_keeps_identity_columns_out_of_features(tmp_path: Path) -> None:
    write_four_well_public_products(tmp_path)
    data_dir = tmp_path / "approved_runtime" / "four_well"
    write_runtime_inputs(data_dir)

    result = run_four_well_runtime_pipeline(
        project_root=tmp_path,
        data_dir=data_dir,
        output_root=tmp_path / "outputs_runtime",
        model_root=tmp_path / "models_runtime",
        run_label="unit_four_well",
        random_state=11,
    )

    run_dir = Path(result["run_dir"])
    features = pd.read_csv(run_dir / "feature_columns.csv")
    eval_metrics = pd.read_csv(run_dir / "eval_metrics.csv")
    core_matches = pd.read_csv(run_dir / "four_well_core_log_matches.csv")
    enriched = pd.read_csv(run_dir / "four_well_enriched_log_rows.csv")

    assert result["status"] == "trained"
    assert result["target"]["column"] == "Sgh"
    assert result["target"]["task"] == "regression"
    assert "object_id" not in set(features["feature_column"])
    assert "api_number" not in set(features["feature_column"])
    assert "well_alias" not in set(features["feature_column"])
    assert "inside_public_hydrate_au" in set(features["feature_column"])
    assert set(eval_metrics["status"]) == {"predicted_unlabeled"}
    assert (run_dir / "predictions_test.csv").exists()
    assert core_matches.loc[0, "match_method"] == "interval_overlap"
    assert enriched["four_well_identity_status"].eq("matched").all()


def test_committed_four_well_templates_exist_with_expected_headers() -> None:
    project_root = Path(__file__).resolve().parents[1]
    product_dir = project_root / "data" / "public_ml_products"

    log_template = pd.read_csv(product_dir / FOUR_WELL_LOG_TEMPLATE)
    core_template = pd.read_csv(product_dir / FOUR_WELL_CORE_TEMPLATE)
    split_template = pd.read_csv(product_dir / FOUR_WELL_SPLIT_TEMPLATE)
    manifest_template = pd.read_csv(product_dir / FOUR_WELL_RUNTIME_MANIFEST_TEMPLATE)
    evidence = pd.read_csv(product_dir / FOUR_WELL_CORE_EVIDENCE_REGISTRY)

    assert {"well_alias", "api_number", "depth_m", "Sgh", "NMR_SAT"}.issubset(log_template.columns)
    assert {"sample_top_m", "sample_base_m", "hydrate_saturation_vv"}.issubset(core_template.columns)
    assert {"well_case", "split", "locked_for_validation"}.issubset(split_template.columns)
    assert "combined_log_rows" in manifest_template["input_name"].tolist()
    assert "IGS" in evidence["well_case"].tolist()
    assert evidence.loc[evidence["well_case"].eq("IGS"), "current_status"].str.contains("core|log", case=False).any()
