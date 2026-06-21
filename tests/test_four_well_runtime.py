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
    load_four_well_log_csvs,
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


def write_screenshot_style_runtime_inputs(data_dir: Path) -> None:
    data_dir.mkdir(parents=True)
    pd.DataFrame(
        {
            "Depth_ft": [2006.5, 2007.0, 2011.0, 2014.0],
            "Density_gpcc": [2.1406, 2.146, 2.0038, 2.1194],
            "phi_den": [0.3087, 0.3055, 0.3916, 0.3216],
            "phi_nmr": [0.3025, 0.3014, 0.3839, 0.3204],
            "S_h": [0.02017, 0.01327, 0.01975, 0.00365],
            "S_wr": [0.8017, 0.8054, 0.8482, 0.7410],
            "GR": [57.52, 67.98, 80.57, 70.81],
            "phi_neut": [0.5818, 0.5841, 0.6102, 0.5273],
            "CAL1": [8.5602, 8.6696, 8.8493, 9.1212],
            "A090": [10.5649, 11.5460, 10.7956, 0.8448],
            "VELP": [2080.4171, 2059.2915, 2008.9875, 2061.6797],
            "VS1": [712.4422, 700.4006, 708.2964, 726.7069],
            "depths_unitD": [2015, 2015.5, 2016, 2016.5],
            "depths_unitC": [2130, 2130.5, 2131, 2131.5],
        }
    ).to_csv(data_dir / "MTE.csv", index=False)

    pd.DataFrame(
        {
            "DEPT": [1775.5, 1776.5, 1777.5, 1779.0],
            "RHOB": [2.0803, 2.0732, 2.0705, 2.0514],
            "NPHI": [0.5122, 0.5283, 0.5347, 0.4914],
            "DPHI": [0.3599, 0.3562, 0.3629, 0.3828],
            "NMRPHI": [0.3545, 0.3575, 0.3564, 0.3764],
            "GR": [56.8281, 56.1337, 59.2144, 62.4692],
            "caliper": [-0.0757, -0.0757, -0.099, 0.0493],
            "RES": [22.7361, 23.2096, 23.7485, 24.542],
            "VP": [1948.108, 1948.858, 1956.58, 1932.996],
            "VS": [604.9273, 598.4517, 590.9512, 576.5146],
            "Sh": [0.015, 0, 0.01791, 0.01672],
            "Swr": [0.1842, 0.1723, 0.166, 0.1475],
        }
    ).to_csv(data_dir / "IGS.csv", index=False)

    refined_rows = [
        ["", "Unit D", "", "", "Unit D", "", "", "", "Unit C", "", "", "Unit C", ""],
        ["", "Depth, ft", "Sgh", "", "Depth correspondence at ML data", "Sgh", "", "", "Depth, ft", "Sgh", "", "Depth correspondence at ML data", "Sgh"],
        ["", 2015.70698, 0.07601, "", 2015.5, 0.076013, "", "", 2131.7093, 0.08892, "", 2131.5, 0.08892],
        ["", 2015.87365, 0.1069, "", 2016.0, 0.106899, "", "", 2131.87597, 0.10902, "", 2132.0, 0.10902],
        ["", 2016.04032, 0.14472, "", 2016.0, 0.144722, "", "", 2132.04264, 0.15074, "", 2132.0, 0.15074],
    ]
    pd.DataFrame(refined_rows).to_csv(data_dir / "MTE_refined.csv", index=False, header=False)

    igs_refined_rows = [
        ["", "", "Depth (ft)", "Hydrate Saturation"],
        ["", "", "", "Sgh"],
        ["", "", 1890.167, 0],
        ["", "", 1890.667, 0],
        ["", "", 1891.167, 0],
    ]
    pd.DataFrame(igs_refined_rows).to_csv(data_dir / "IGS_refined.csv", index=False, header=False)


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


def test_four_well_loader_accepts_screenshot_style_flat_and_refined_csvs(tmp_path: Path) -> None:
    data_dir = tmp_path / "approved_runtime" / "four_well"
    write_screenshot_style_runtime_inputs(data_dir)

    logs = load_four_well_log_csvs(
        data_dir,
        ("MTE.csv", "IGS.csv", "MTE_refined.csv", "IGS_refined.csv"),
    )

    assert {"MTE", "IGS"}.issubset(set(logs["well_alias"]))
    assert {"flat_log_table", "refined_depth_saturation_pairs"}.issubset(set(logs["source_table_format"]))
    mte_flat = logs[logs["dataset_file"].eq("MTE.csv")].iloc[0]
    igs_flat = logs[logs["dataset_file"].eq("IGS.csv")].iloc[0]
    refined = logs[logs["dataset_file"].eq("MTE_refined.csv")]

    assert round(float(mte_flat["depth_m"]), 3) == round(2006.5 * 0.3048, 3)
    assert mte_flat["rt_source_mnemonic"] == "A090"
    assert pd.notna(mte_flat["rt_ohm_m"])
    assert pd.notna(igs_flat["rt_ohm_m"])
    assert {"source_depth", "ml_depth_correspondence"}.issubset(set(refined["source_depth_kind"]))
    assert {"Unit D", "Unit C"}.issubset(set(refined["source_unit_label"]))
    assert "Sgh" in logs.columns
    assert "S_h" in logs.columns


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
    assert "log_rows" in manifest_template["input_name"].tolist()
    assert "IGS" in evidence["well_case"].tolist()
    assert evidence.loc[evidence["well_case"].eq("IGS"), "current_status"].str.contains("core|log", case=False).any()
