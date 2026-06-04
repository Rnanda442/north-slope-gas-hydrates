from __future__ import annotations

import pandas as pd

from dashboard.runtime.core_calibration import match_core_to_nearest_logs
from dashboard.runtime.feature_engineering import add_standard_features
from dashboard.runtime.loaders import load_csv_logs, standardize_curve_columns
from dashboard.runtime.modeling import rule_based_interval_labels
from dashboard.runtime.schemas import RuntimeConfig
from dashboard.runtime.validation import validate_log_table
from dashboard.well_log_engine import generate_synthetic_logs, load_runtime_data


def test_curve_alias_standardization_keeps_doe_shaped_inputs_canonical() -> None:
    raw = pd.DataFrame(
        {
            "WELL_NAME": ["DOE-WELL-A", "DOE-WELL-A"],
            "DEPTH": [500.0, 505.0],
            "GR": [42.0, 44.0],
            "RDEP": [25.0, 28.0],
            "RHOB": [2.18, 2.16],
            "DTC": [92.0, 90.0],
            "DTS": [180.0, 178.0],
        }
    )
    standardized = standardize_curve_columns(raw)
    assert {"well_alias", "depth_m", "gr_api", "rt_ohm_m", "rhob_g_cc", "dt_us_ft", "dts_us_ft"}.issubset(
        standardized.columns
    )
    assert standardized.loc[0, "well_alias"] == "DOE-WELL-A"


def test_approved_csv_runtime_path_loads_and_validates(tmp_path) -> None:
    csv_path = tmp_path / "approved_shape.csv"
    pd.DataFrame(
        {
            "WELL": ["DOE-WELL-A", "DOE-WELL-A"],
            "MD": [500.0, 505.0],
            "GR": [42.0, 44.0],
            "RT": [25.0, 28.0],
            "RHOB": [2.18, 2.16],
        }
    ).to_csv(csv_path, index=False)

    logs = load_csv_logs((str(csv_path),))
    report = validate_log_table(logs)

    assert report.is_ready
    assert report.rows == 2
    assert report.wells == 1


def test_runtime_config_preserves_synthetic_default() -> None:
    logs = load_runtime_data(RuntimeConfig())
    assert len(logs) == len(generate_synthetic_logs())
    assert set(logs["well_alias"]) == {"SYNTH-WELL-01", "SYNTH-WELL-02", "SYNTH-WELL-03"}


def test_feature_model_and_core_skeletons_connect() -> None:
    logs = pd.DataFrame(
        {
            "well_alias": ["DOE-WELL-A", "DOE-WELL-A"],
            "depth_m": [500.0, 505.0],
            "gr_api": [42.0, 44.0],
            "rt_ohm_m": [25.0, 28.0],
            "rhob_g_cc": [2.18, 2.16],
            "dt_us_ft": [92.0, 90.0],
            "dts_us_ft": [180.0, 178.0],
        }
    )
    features = add_standard_features(logs)
    labels = rule_based_interval_labels(features)
    core = pd.DataFrame(
        {
            "well_alias": ["DOE-WELL-A"],
            "sample_depth_m": [503.0],
            "porosity_vv": [0.29],
            "hydrate_saturation_vv": [0.45],
        }
    )
    matches = match_core_to_nearest_logs(features, core, max_offset_m=3.0)

    assert {"vp_km_s", "vs_km_s", "density_porosity_vv", "archie_hydrate_proxy"}.issubset(features.columns)
    assert labels["runtime_phase_label"].iloc[0] == "hydrate-supportive multi-log response"
    assert matches.loc[0, "match_status"] == "matched"
