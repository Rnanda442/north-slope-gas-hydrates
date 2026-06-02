from __future__ import annotations

import pandas as pd

from dashboard.well_log_engine import (
    SYNTHETIC_LABEL,
    generate_synthetic_logs,
    screen_intervals,
    variable_range_summary,
)


def test_synthetic_generation_has_runtime_schema_and_neutral_aliases() -> None:
    logs = generate_synthetic_logs()
    required = {
        "depth_m",
        "location_alias",
        "well_alias",
        "gr_api",
        "rt_ohm_m",
        "rhob_g_cc",
        "density_porosity_vv",
        "dt_us_ft",
        "vp_km_s",
        "dts_us_ft",
        "vs_km_s",
        "nmr_porosity_vv",
        "caliper_in",
        "borehole_qc",
        "temperature_c",
        "pressure_mpa",
        "core_calibration_placeholder",
    }
    assert required.issubset(logs.columns)
    assert set(logs["well_alias"]) == {"SYNTH-WELL-01", "SYNTH-WELL-02", "SYNTH-WELL-03"}
    assert set(logs["data_boundary"]) == {SYNTHETIC_LABEL}
    assert logs[logs["well_alias"] == "SYNTH-WELL-03"]["nmr_porosity_vv"].isna().all()


def test_range_summary_reports_missingness_and_percentiles() -> None:
    logs = generate_synthetic_logs()
    summary = variable_range_summary(
        logs,
        variables=["rt_ohm_m", "nmr_porosity_vv"],
        well_alias="SYNTH-WELL-03",
        depth_interval=(500, 900),
    ).set_index("Column")
    assert summary.loc["rt_ohm_m", "Minimum"] <= summary.loc["rt_ohm_m", "Median"]
    assert summary.loc["rt_ohm_m", "Median"] <= summary.loc["rt_ohm_m", "Maximum"]
    assert summary.loc["nmr_porosity_vv", "Missingness %"] == 100.0
    assert summary.loc["nmr_porosity_vv", "QC status"] == "REVIEW"


def test_interval_screen_preserves_separate_outcomes() -> None:
    intervals = screen_intervals(generate_synthetic_logs(), interval_m=40)
    phases = set(intervals["Phase-classification evidence"])
    assert "hydrate-supportive multi-log response" in phases
    assert "good sand, no hydrate" in phases
    assert "ambiguous / expert review" in phases
    assert "Stability admissibility" in intervals
    assert "Reservoir quality" in intervals
    assert "Hydrate-saturation proxy" in intervals
    assert "Core-calibration confidence" in intervals
    assert "Producibility screen" in intervals
    assert "Synthetic sweet-spot review lane" in intervals
    assert "Uncertainty flags" in intervals
    assert intervals["Synthetic sweet-spot review lane"].str.contains("sweet-spot").any()


def test_interval_screen_uses_archie_only_as_supplement_when_nmr_is_missing() -> None:
    intervals = screen_intervals(generate_synthetic_logs(), interval_m=40)
    well_three = intervals[intervals["Well alias"] == "SYNTH-WELL-03"]
    assert (well_three["Proxy source"] == "Archie supplementary cross-check").all()
    assert well_three["Uncertainty flags"].str.contains("NMR unavailable").all()
