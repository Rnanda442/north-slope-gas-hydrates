from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from code_transfer_block.multi_saturation_target_workflow import fit_and_predict_all_saturations


pytest.importorskip("openpyxl")
pytest.importorskip("sklearn")


def test_multi_saturation_transfer_workflow_trains_targets_from_dataset3(tmp_path: Path) -> None:
    rows_one = 12
    rows_two = 10
    log_one = pd.DataFrame(
        {
            "WELL": ["MTE"] * rows_one,
            "Depth_ft": [1650 + index * 3 for index in range(rows_one)],
            "depths_unitD": ["ft"] * rows_one,
            "depths_unitC": ["ft"] * rows_one,
            "GR": [40 + index % 3 for index in range(rows_one)],
            "RES": [0 if index == 0 else 25 + index for index in range(rows_one)],
            "Density_gpcc": [2.22 - index * 0.004 for index in range(rows_one)],
            "phi_den": [0.24 + index * 0.001 for index in range(rows_one)],
            "phi_nmr": [0.18 + index * 0.001 for index in range(rows_one)],
            "phi_neut": [0.21 + index * 0.001 for index in range(rows_one)],
            "CAL1": [8.5 + index * 0.01 for index in range(rows_one)],
            "AO90": [70 + index for index in range(rows_one)],
            "VELP": [2500 + index * 5 for index in range(rows_one)],
            "VS1": [1200 + index * 4 for index in range(rows_one)],
            "Unnamed: 14": [index for index in range(rows_one)],
            "Unnamed: 15": [index + 100 for index in range(rows_one)],
        }
    )
    log_two = pd.DataFrame(
        {
            "WELL": ["IGS"] * rows_two,
            "DEPT": [550 + index for index in range(rows_two)],
            "GR": [45 + index % 4 for index in range(rows_two)],
            "RES": [0 if index == 0 else 30 + index for index in range(rows_two)],
            "RHOB": [2.18 - index * 0.003 for index in range(rows_two)],
            "NPHI": [0.20 + index * 0.002 for index in range(rows_two)],
            "DPHI": [0.23 + index * 0.002 for index in range(rows_two)],
            "NMRPHI": [0.16 + index * 0.002 for index in range(rows_two)],
            "caliper": [8.6 + index * 0.01 for index in range(rows_two)],
            "VP": [2600 + index * 5 for index in range(rows_two)],
            "VS": [1250 + index * 4 for index in range(rows_two)],
            "Unnamed: 12": [index for index in range(rows_two)],
            "Unnamed: 13": [index + 100 for index in range(rows_two)],
        }
    )
    log_one.to_excel(tmp_path / "curated_dataset1.xlsx", sheet_name="#1 well logs", index=False)
    log_two.to_excel(tmp_path / "curated_dataset2.xlsx", sheet_name="#2 well logs", index=False)

    with pd.ExcelWriter(tmp_path / "curated_dataset3.xlsx") as writer:
        pd.DataFrame({"S_h": [0.12 + index * 0.015 for index in range(rows_one)]}).to_excel(
            writer,
            sheet_name="#1",
            index=False,
        )
        pd.DataFrame({"Sh": [0.2 + index * 0.01 for index in range(rows_two)]}).to_excel(
            writer,
            sheet_name="#2",
            index=False,
        )

    result = fit_and_predict_all_saturations(
        tmp_path,
        output_dir=tmp_path / "outputs_runtime" / "multi_saturation_test",
        min_training_rows=5,
    )

    output_dir = Path(result["output_dir"])
    summary = pd.read_csv(output_dir / "run_summary.csv")
    features = pd.read_csv(output_dir / "feature_columns_by_target.csv")
    audit = pd.read_csv(output_dir / "excluded_feature_columns_by_target.csv")

    assert result["feature_policy_version"] == "clean_feature_matrix_v3_2026_06_16"
    assert result["trained_target_count"] == 2
    assert set(summary["target_column"]) == {"S_h", "Sh"}
    assert set(summary["alignment_method"]) == {"row_order_aligned"}
    feature_names = set(features["feature_column"])
    assert "Depth_ft" not in feature_names
    assert "DEPT" not in feature_names
    assert "depth_m" not in feature_names
    assert "depths_unitD" not in feature_names
    assert "depths_unitC" not in feature_names
    assert "Unnamed: 14" not in feature_names
    assert "Unnamed: 15" not in feature_names
    assert "GR" not in feature_names
    assert "RES" not in feature_names
    assert "RHOB" not in feature_names
    assert "VP" not in feature_names
    assert "VS" not in feature_names
    assert {"gr_api", "rt_ohm_m", "caliper_in", "vp_km_s", "vs_km_s", "vp_vs_ratio"}.issubset(feature_names)
    assert {"density_porosity_vv", "neutron_porosity_vv", "nmr_porosity_vv"}.issubset(feature_names)
    excluded = audit[audit["decision"] == "excluded"]
    assert {"Depth_ft", "DEPT", "depths_unitD", "Unnamed: 14", "GR", "RES", "RHOB", "VP", "VS"}.issubset(
        set(excluded["column"])
    )
    assert "raw_alias_duplicate_of_gr_api" in set(excluded["reason"])
    assert "context_depth_unit_or_spreadsheet_helper" in set(excluded["reason"])
    assert any(output_dir.glob("*/predictions_curated_dataset1_*.csv"))
    assert any(output_dir.glob("*/predictions_curated_dataset2_*.csv"))
