from __future__ import annotations

from pathlib import Path
import re

import geopandas as gpd
import numpy as np
import pandas as pd

from dashboard.stability_sources import (
    active_stability_source_path,
    load_ggd223_permafrost_points,
    load_hydrate_assessment_units,
)


PRODUCT_DIR_NAME = "public_stability_products"
WELL_CONTEXT_FILE_NAME = "north_slope_well_stability_context_2026-06-14.csv"
WELL_CONTEXT_SUMMARY_FILE_NAME = "north_slope_well_stability_context_summary_2026-06-14.csv"
G10015_INVENTORY_FILE_NAME = "g10015_temperature_profile_inventory_2026-06-14.csv"
G10015_SUMMARY_FILE_NAME = "g10015_temperature_profile_summary_2026-06-14.csv"
STABILITY_INPUT_SCAFFOLD_FILE_NAME = "stability_input_scaffold_2026-06-14.csv"
STABILITY_INPUT_SCAFFOLD_SUMMARY_FILE_NAME = "stability_input_scaffold_summary_2026-06-14.csv"
STABILITY_INPUT_CAPABILITY_MATRIX_FILE_NAME = "stability_input_capability_matrix_2026-06-14.csv"
STABILITY_OSL_PULL_TRIGGERS_FILE_NAME = "stability_osl_pull_triggers_2026-06-14.csv"
STABILITY_WEBSITE_PRODUCT_SPEC_FILE_NAME = "stability_website_product_spec_2026-06-14.csv"
STABILITY_TEMPERATURE_MODEL_FILE_NAME = "stability_temperature_model_2026-06-14.csv"
STABILITY_TEMPERATURE_MODEL_SUMMARY_FILE_NAME = "stability_temperature_model_summary_2026-06-14.csv"
PHASE_CURVE_FILE_NAME = "phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1.csv"
PHASE_CURVE_SCENARIO_CATALOG_FILE_NAME = "phase_curve_scenario_catalog_2026-06-14.csv"
PHASE_CURVE_ID = "methane_5ppt_sir2008_csmhyd_digitized_v1"
PHASE_CURVE_ROLE = "baseline"
PHASE_CURVE_ALLOWED_USE = "official_public_baseline"
PHASE_CURVE_GAS_COMPOSITION_ASSUMPTION = "100_percent_methane"
PHASE_CURVE_GAS_METHANE_MOL_PCT = 100.0
PHASE_CURVE_GAS_ETHANE_MOL_PCT = 0.0
PHASE_CURVE_GAS_PROPANE_MOL_PCT = 0.0
PHASE_CURVE_GAS_BUTANE_PLUS_MOL_PCT = 0.0
PHASE_CURVE_SALINITY_PPT = 5.0

WELL_SOURCE_RELATIVE_PATH = (
    "raw_data/Wells/Well_Bottom_Hole_Location/Well_Bottom_Hole_Location.shp"
)
G10015_RELATIVE_PATH = "03_temperature_geothermal/NSIDC_G10015_extracted"
NUMERIC_PROFILE_RE = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s*$")
HYDROSTATIC_PRESSURE_MPA_PER_M = 0.00980665
SURFACE_PRESSURE_MPA = 0.101325
TEMPERATURE_MODEL_ID = "g10015_profile_interpolation_v1"
DEFAULT_STABILITY_DEPTH_GRID_STEP_M = 5.0
NEAR_TEMPERATURE_CONTROL_KM = 5.0
MODERATE_TEMPERATURE_CONTROL_KM = 50.0
MINOR_TEMPERATURE_EXTRAPOLATION_M = 100.0
LARGE_TEMPERATURE_EXTRAPOLATION_M = 250.0

PHASE_CURVE_COLUMNS = [
    "phase_curve_id",
    "phase_curve_role",
    "source_depth_m",
    "pressure_mpa_absolute",
    "equilibrium_temperature_c",
    "gas_composition_assumption",
    "gas_methane_mol_pct",
    "gas_ethane_mol_pct",
    "gas_propane_mol_pct",
    "gas_butane_plus_mol_pct",
    "salinity_ppt_assumption",
    "source_citation",
    "source_url",
    "source_extraction_method",
    "source_notes",
]

PHASE_CURVE_SCENARIO_CATALOG_COLUMNS = [
    "phase_curve_id",
    "phase_curve_role",
    "curve_status",
    "gas_composition_assumption",
    "gas_methane_mol_pct",
    "gas_ethane_mol_pct",
    "gas_propane_mol_pct",
    "gas_butane_plus_mol_pct",
    "salinity_ppt_assumption",
    "pressure_gradient_mpa_per_m",
    "source_citation",
    "source_url",
    "source_notes",
    "allowed_use",
]

STABILITY_INPUT_CAPABILITY_MATRIX_COLUMNS = [
    "input_name",
    "capability_status",
    "current_source",
    "current_coverage",
    "supports_now",
    "does_not_support_yet",
    "future_upgrade",
    "screen_role",
    "guardrail",
]

STABILITY_OSL_PULL_TRIGGER_COLUMNS = [
    "trigger",
    "needs_osl",
    "why",
    "expected_action",
    "public_output_after_pull",
]

STABILITY_WEBSITE_PRODUCT_SPEC_COLUMNS = [
    "website_area",
    "final_content",
    "primary_user_action",
    "must_show",
    "must_not_claim",
    "data_dependency",
]

TEMPERATURE_MODEL_COLUMNS = [
    "depth_m",
    "temperature_model_c",
    "temperature_model_method",
    "temperature_extrapolated_below_profile",
    "temperature_extrapolation_below_profile_m",
    "temperature_model_status",
]

STABILITY_CONDITION_GRID_COLUMNS = [
    "depth_m",
    "pressure_mpa_absolute",
    "temperature_model_c",
    "temperature_equilibrium_c",
    "is_stable",
    "temperature_model_method",
    "temperature_extrapolated_below_profile",
    "temperature_extrapolation_below_profile_m",
    "temperature_model_status",
]

STABILITY_INTERVAL_RESULT_COLUMNS = [
    "stability_result_status",
    "stable_depth_grid_step_m",
    "stability_top_m",
    "stability_top_pressure_mpa_absolute",
    "stability_top_temperature_c",
    "stability_base_m",
    "stability_base_pressure_mpa_absolute",
    "stability_base_temperature_c",
    "stability_thickness_m",
    "well_penetrated_stability_thickness_m",
    "reaches_stability_zone",
    "top_boundary_method",
    "base_boundary_method",
    "temperature_extrapolated_below_profile",
    "temperature_extrapolation_below_profile_m",
    "caveat_codes",
]

STABILITY_TEMPERATURE_MODEL_PRODUCT_COLUMNS = [
    "object_id",
    "permit_number",
    "api_number",
    "well_name",
    "temperature_model_id",
    "temperature_model_depth_role",
    "depth_m",
    "temperature_model_c",
    "temperature_model_method",
    "temperature_extrapolated_below_profile",
    "temperature_extrapolation_below_profile_m",
    "temperature_model_status",
    "temperature_profile_code",
    "temperature_profile_file",
    "temperature_profile_max_depth_m",
    "temperature_gradient_c_per_100m",
    "temperature_gradient_source",
    "temperature_profile_link_method",
    "stability_input_readiness",
    "temperature_model_product_role",
    "stability_top_base_thickness_status",
]

WELL_CONTEXT_COLUMNS = [
    "object_id",
    "permit_number",
    "api_number",
    "well_name",
    "field",
    "pool",
    "current_status",
    "driller_total_depth_ft",
    "true_vertical_depth_ft",
    "wellhead_latitude",
    "wellhead_longitude",
    "bottomhole_latitude",
    "bottomhole_longitude",
    "depth_basis",
    "depth_basis_ft",
    "depth_basis_m",
    "hydrate_assessment_unit_count",
    "hydrate_assessment_codes",
    "within_hydrate_assessment_unit",
    "nearest_ggd223_code",
    "nearest_ggd223_well",
    "nearest_permafrost_depth_m",
    "nearest_ggd223_distance_km",
    "well_depth_exceeds_nearest_permafrost_control",
    "stability_context_flag",
]


def default_stability_products_dir(project_root: Path) -> Path:
    return project_root / "data" / PRODUCT_DIR_NAME


def default_well_context_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / WELL_CONTEXT_FILE_NAME


def default_well_context_summary_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / WELL_CONTEXT_SUMMARY_FILE_NAME


def default_g10015_inventory_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / G10015_INVENTORY_FILE_NAME


def default_g10015_summary_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / G10015_SUMMARY_FILE_NAME


def default_stability_input_scaffold_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / STABILITY_INPUT_SCAFFOLD_FILE_NAME


def default_stability_input_scaffold_summary_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / STABILITY_INPUT_SCAFFOLD_SUMMARY_FILE_NAME


def default_stability_input_capability_matrix_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / STABILITY_INPUT_CAPABILITY_MATRIX_FILE_NAME


def default_stability_osl_pull_triggers_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / STABILITY_OSL_PULL_TRIGGERS_FILE_NAME


def default_stability_website_product_spec_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / STABILITY_WEBSITE_PRODUCT_SPEC_FILE_NAME


def default_stability_temperature_model_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / STABILITY_TEMPERATURE_MODEL_FILE_NAME


def default_stability_temperature_model_summary_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / STABILITY_TEMPERATURE_MODEL_SUMMARY_FILE_NAME


def default_phase_curve_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / PHASE_CURVE_FILE_NAME


def default_phase_curve_scenario_catalog_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / PHASE_CURVE_SCENARIO_CATALOG_FILE_NAME


def hydrostatic_pressure_mpa_gauge(
    depth_m: object,
    pressure_gradient_mpa_per_m: float = HYDROSTATIC_PRESSURE_MPA_PER_M,
) -> object:
    depth = pd.to_numeric(depth_m, errors="coerce")
    return depth * pressure_gradient_mpa_per_m


def hydrostatic_pressure_mpa_absolute(
    depth_m: object,
    surface_pressure_mpa: float = SURFACE_PRESSURE_MPA,
    pressure_gradient_mpa_per_m: float = HYDROSTATIC_PRESSURE_MPA_PER_M,
) -> object:
    return surface_pressure_mpa + hydrostatic_pressure_mpa_gauge(
        depth_m,
        pressure_gradient_mpa_per_m,
    )


def load_phase_curve(project_root: Path, phase_curve_id: str = PHASE_CURVE_ID) -> pd.DataFrame:
    path = default_phase_curve_path(project_root)
    if not path.exists():
        return pd.DataFrame(columns=PHASE_CURVE_COLUMNS)

    curve = pd.read_csv(path)
    missing_columns = [column for column in PHASE_CURVE_COLUMNS if column not in curve.columns]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Phase curve lookup is missing required columns: {missing}")

    curve = curve[curve["phase_curve_id"].eq(phase_curve_id)].copy()
    curve["pressure_mpa_absolute"] = pd.to_numeric(
        curve["pressure_mpa_absolute"],
        errors="coerce",
    )
    curve["equilibrium_temperature_c"] = pd.to_numeric(
        curve["equilibrium_temperature_c"],
        errors="coerce",
    )
    curve = curve.dropna(
        subset=["pressure_mpa_absolute", "equilibrium_temperature_c"],
    )
    curve = curve.sort_values("pressure_mpa_absolute").reset_index(drop=True)
    if curve["pressure_mpa_absolute"].duplicated().any():
        raise ValueError("Phase curve lookup has duplicate absolute-pressure values.")
    return curve[PHASE_CURVE_COLUMNS]


def load_methane_phase_curve(project_root: Path) -> pd.DataFrame:
    return load_phase_curve(project_root, PHASE_CURVE_ID)


def load_phase_curve_scenario_catalog(project_root: Path) -> pd.DataFrame:
    path = default_phase_curve_scenario_catalog_path(project_root)
    if not path.exists():
        return pd.DataFrame(columns=PHASE_CURVE_SCENARIO_CATALOG_COLUMNS)

    catalog = pd.read_csv(path)
    missing_columns = [
        column for column in PHASE_CURVE_SCENARIO_CATALOG_COLUMNS if column not in catalog.columns
    ]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Phase curve scenario catalog is missing required columns: {missing}")

    numeric_columns = [
        "gas_methane_mol_pct",
        "gas_ethane_mol_pct",
        "gas_propane_mol_pct",
        "gas_butane_plus_mol_pct",
        "salinity_ppt_assumption",
        "pressure_gradient_mpa_per_m",
    ]
    for column in numeric_columns:
        catalog[column] = pd.to_numeric(catalog[column], errors="coerce")
    return catalog[PHASE_CURVE_SCENARIO_CATALOG_COLUMNS]


def phase_curve_equilibrium_temperature_c(
    phase_curve: pd.DataFrame,
    pressure_mpa_absolute: object,
) -> object:
    if phase_curve.empty:
        return np.nan

    pressures = pd.to_numeric(
        phase_curve["pressure_mpa_absolute"],
        errors="coerce",
    ).to_numpy(dtype=float)
    temperatures = pd.to_numeric(
        phase_curve["equilibrium_temperature_c"],
        errors="coerce",
    ).to_numpy(dtype=float)
    valid = np.isfinite(pressures) & np.isfinite(temperatures)
    pressures = pressures[valid]
    temperatures = temperatures[valid]
    if len(pressures) < 2:
        return np.nan

    order = np.argsort(pressures)
    pressures = pressures[order]
    temperatures = temperatures[order]

    if np.isscalar(pressure_mpa_absolute):
        pressure = pd.to_numeric(pressure_mpa_absolute, errors="coerce")
        if not np.isfinite(pressure) or pressure < pressures[0] or pressure > pressures[-1]:
            return np.nan
        return float(np.interp(float(pressure), pressures, temperatures))

    values = pd.to_numeric(pressure_mpa_absolute, errors="coerce")
    pressure_values = np.asarray(values, dtype=float)
    result = np.full(pressure_values.shape, np.nan, dtype=float)
    in_range = (
        np.isfinite(pressure_values)
        & (pressure_values >= pressures[0])
        & (pressure_values <= pressures[-1])
    )
    result[in_range] = np.interp(pressure_values[in_range], pressures, temperatures)
    if isinstance(pressure_mpa_absolute, pd.Series):
        return pd.Series(result, index=pressure_mpa_absolute.index)
    return result


def stability_depth_grid(
    depth_limit_m: object,
    step_m: object = DEFAULT_STABILITY_DEPTH_GRID_STEP_M,
) -> np.ndarray:
    limit = pd.to_numeric(depth_limit_m, errors="coerce")
    step = pd.to_numeric(step_m, errors="coerce")
    if not np.isfinite(step) or float(step) <= 0:
        raise ValueError("Stability depth-grid step must be a positive number.")
    if not np.isfinite(limit) or float(limit) < 0:
        return np.array([], dtype=float)

    limit_value = float(limit)
    if limit_value == 0:
        return np.array([0.0], dtype=float)

    grid = np.arange(0.0, limit_value, float(step))
    grid = np.append(grid, limit_value)
    return np.unique(np.round(grid, 10)).astype(float)


def stability_condition_grid_from_profile(
    profile_points: pd.DataFrame,
    phase_curve: pd.DataFrame,
    depth_limit_m: object,
    gradient_c_per_100m: object | None = None,
    step_m: object = DEFAULT_STABILITY_DEPTH_GRID_STEP_M,
) -> pd.DataFrame:
    grid = stability_depth_grid(depth_limit_m, step_m)
    if len(grid) == 0:
        return pd.DataFrame(columns=STABILITY_CONDITION_GRID_COLUMNS)

    temperature = temperature_model_from_profile(
        profile_points,
        grid,
        gradient_c_per_100m=gradient_c_per_100m,
    )
    pressure = hydrostatic_pressure_mpa_absolute(temperature["depth_m"])
    equilibrium = phase_curve_equilibrium_temperature_c(phase_curve, pressure)
    frame = temperature.copy()
    frame["pressure_mpa_absolute"] = pd.to_numeric(pressure, errors="coerce")
    frame["temperature_equilibrium_c"] = pd.to_numeric(equilibrium, errors="coerce")
    has_complete_conditions = (
        frame["temperature_model_status"].eq("calculated")
        & frame["temperature_model_c"].notna()
        & frame["temperature_equilibrium_c"].notna()
    )
    frame["is_stable"] = False
    frame.loc[has_complete_conditions, "is_stable"] = (
        frame.loc[has_complete_conditions, "temperature_model_c"]
        <= frame.loc[has_complete_conditions, "temperature_equilibrium_c"]
    )
    return frame[STABILITY_CONDITION_GRID_COLUMNS]


def _zero_crossing_depth(
    shallower_depth: float,
    shallower_delta: float,
    deeper_depth: float,
    deeper_delta: float,
) -> float:
    if deeper_delta == shallower_delta:
        return float(deeper_depth)
    fraction = -shallower_delta / (deeper_delta - shallower_delta)
    return float(shallower_depth + fraction * (deeper_depth - shallower_depth))


def _empty_stability_interval_result(
    status: str,
    caveat_codes: list[str] | None = None,
    step_m: object = pd.NA,
) -> pd.Series:
    caveats = caveat_codes or [
        "hydrostatic_pressure_assumed",
        "phase_curve_methane_5ppt",
        "not_hydrate_proof",
    ]
    return pd.Series(
        {
            "stability_result_status": status,
            "stable_depth_grid_step_m": step_m,
            "stability_top_m": np.nan,
            "stability_top_pressure_mpa_absolute": np.nan,
            "stability_top_temperature_c": np.nan,
            "stability_base_m": np.nan,
            "stability_base_pressure_mpa_absolute": np.nan,
            "stability_base_temperature_c": np.nan,
            "stability_thickness_m": np.nan,
            "well_penetrated_stability_thickness_m": np.nan,
            "reaches_stability_zone": False,
            "top_boundary_method": "not_calculated",
            "base_boundary_method": "not_calculated",
            "temperature_extrapolated_below_profile": False,
            "temperature_extrapolation_below_profile_m": 0.0,
            "caveat_codes": ";".join(caveats),
        },
        index=STABILITY_INTERVAL_RESULT_COLUMNS,
    )


def stability_interval_from_condition_grid(
    condition_grid: pd.DataFrame,
    depth_limit_m: object | None = None,
    step_m: object = DEFAULT_STABILITY_DEPTH_GRID_STEP_M,
) -> pd.Series:
    if condition_grid.empty:
        return _empty_stability_interval_result(
            "blocked_incomplete_pressure_temperature_grid",
            step_m=step_m,
        )

    frame = condition_grid.copy()
    numeric_columns = [
        "depth_m",
        "pressure_mpa_absolute",
        "temperature_model_c",
        "temperature_equilibrium_c",
        "temperature_extrapolation_below_profile_m",
    ]
    for column in numeric_columns:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame = frame.sort_values("depth_m").reset_index(drop=True)
    complete_conditions = (
        frame["temperature_model_status"].eq("calculated")
        & frame["pressure_mpa_absolute"].notna()
        & frame["temperature_model_c"].notna()
        & frame["temperature_equilibrium_c"].notna()
    )
    if not complete_conditions.all():
        caveats = [
            "hydrostatic_pressure_assumed",
            "phase_curve_methane_5ppt",
            "not_hydrate_proof",
        ]
        if frame["temperature_model_status"].astype(str).str.startswith("blocked").any():
            caveats.append("temperature_profile_missing")
        return _empty_stability_interval_result(
            "blocked_incomplete_pressure_temperature_grid",
            caveats,
            step_m,
        )

    stable = frame["is_stable"].astype(bool).to_numpy()
    if not stable.any():
        result = _empty_stability_interval_result(
            "calculated_no_stable_interval",
            step_m=step_m,
        )
        result["well_penetrated_stability_thickness_m"] = 0.0
        return result

    depths = frame["depth_m"].to_numpy(dtype=float)
    deltas = (
        frame["temperature_equilibrium_c"] - frame["temperature_model_c"]
    ).to_numpy(dtype=float)

    start_index = int(np.flatnonzero(stable)[0])
    if start_index == 0:
        top_m = float(depths[start_index])
        top_method = "stable_at_shallowest_grid"
    else:
        top_m = _zero_crossing_depth(
            depths[start_index - 1],
            deltas[start_index - 1],
            depths[start_index],
            deltas[start_index],
        )
        top_method = "interpolated_crossing"

    unstable_after = np.flatnonzero(~stable[start_index:])
    if len(unstable_after) == 0:
        base_m = float(depths[-1])
        base_method = "open_below_model_depth_limit"
    else:
        first_unstable_index = start_index + int(unstable_after[0])
        base_m = _zero_crossing_depth(
            depths[first_unstable_index - 1],
            deltas[first_unstable_index - 1],
            depths[first_unstable_index],
            deltas[first_unstable_index],
        )
        base_method = "interpolated_crossing"

    modeled_depth_limit = depth_limit_m
    if modeled_depth_limit is None:
        modeled_depth_limit = float(depths[-1])
    modeled_depth_limit = pd.to_numeric(modeled_depth_limit, errors="coerce")
    if not np.isfinite(modeled_depth_limit):
        modeled_depth_limit = float(depths[-1])
    modeled_depth_limit = float(modeled_depth_limit)

    reaches_stability_zone = modeled_depth_limit >= top_m
    penetrated_thickness = 0.0
    if reaches_stability_zone:
        penetrated_thickness = max(0.0, min(base_m, modeled_depth_limit) - top_m)

    interval_rows = frame[frame["depth_m"].between(top_m, base_m)]
    extrapolated = bool(interval_rows["temperature_extrapolated_below_profile"].any())
    extrapolation_m = 0.0
    if extrapolated:
        extrapolation_m = float(
            interval_rows["temperature_extrapolation_below_profile_m"].max()
        )

    caveats = [
        "hydrostatic_pressure_assumed",
        "phase_curve_methane_5ppt",
        "not_hydrate_proof",
    ]
    if extrapolated:
        caveats.append("temperature_profile_extrapolated")

    result = pd.Series(
        {
            "stability_result_status": "calculated",
            "stable_depth_grid_step_m": step_m,
            "stability_top_m": top_m,
            "stability_top_pressure_mpa_absolute": float(
                np.interp(top_m, depths, frame["pressure_mpa_absolute"])
            ),
            "stability_top_temperature_c": float(
                np.interp(top_m, depths, frame["temperature_model_c"])
            ),
            "stability_base_m": base_m,
            "stability_base_pressure_mpa_absolute": float(
                np.interp(base_m, depths, frame["pressure_mpa_absolute"])
            ),
            "stability_base_temperature_c": float(
                np.interp(base_m, depths, frame["temperature_model_c"])
            ),
            "stability_thickness_m": max(0.0, base_m - top_m),
            "well_penetrated_stability_thickness_m": penetrated_thickness,
            "reaches_stability_zone": reaches_stability_zone,
            "top_boundary_method": top_method,
            "base_boundary_method": base_method,
            "temperature_extrapolated_below_profile": extrapolated,
            "temperature_extrapolation_below_profile_m": extrapolation_m,
            "caveat_codes": ";".join(caveats),
        },
        index=STABILITY_INTERVAL_RESULT_COLUMNS,
    )
    return result


def _series_value(row: pd.Series | dict[str, object], *names: str, default: object = pd.NA) -> object:
    for name in names:
        if name in row and pd.notna(row[name]):
            return row[name]
    return default


def stability_source_control_label(row: pd.Series | dict[str, object]) -> str:
    inside_au = bool(_series_value(row, "within_hydrate_assessment_unit", default=False))
    if not inside_au:
        return "outside_public_au_context"

    depth_basis = str(_series_value(row, "depth_source", "depth_basis", default="")).strip()
    phase_status = str(_series_value(row, "phase_curve_status", default="")).strip()
    temperature_status = str(_series_value(row, "temperature_model_status", default="")).strip()
    result_status = str(_series_value(row, "stability_result_status", default="")).strip()

    if (
        not depth_basis
        or depth_basis == "missing"
        or phase_status != "applied"
        or temperature_status != "calculated"
        or result_status.startswith("blocked")
    ):
        return "blocked_missing_inputs"

    allowed_use = str(_series_value(row, "phase_curve_allowed_use", default="")).strip()
    if allowed_use and allowed_use != PHASE_CURVE_ALLOWED_USE:
        return "low_source_control"

    control_distance = pd.to_numeric(
        _series_value(
            row,
            "temperature_control_distance_km",
            "permafrost_control_distance_km",
            "nearest_ggd223_distance_km",
            default=np.nan,
        ),
        errors="coerce",
    )
    extrapolation_m = pd.to_numeric(
        _series_value(row, "temperature_extrapolation_below_profile_m", default=0.0),
        errors="coerce",
    )
    if not np.isfinite(control_distance):
        control_distance = np.inf
    if not np.isfinite(extrapolation_m):
        extrapolation_m = np.inf

    is_true_vertical = depth_basis == "TrueVertic"
    is_driller_fallback = depth_basis == "DrillerTot"
    minor_extrapolation = extrapolation_m <= MINOR_TEMPERATURE_EXTRAPOLATION_M
    moderate_extrapolation = extrapolation_m <= LARGE_TEMPERATURE_EXTRAPOLATION_M

    if (
        is_true_vertical
        and control_distance <= NEAR_TEMPERATURE_CONTROL_KM
        and minor_extrapolation
    ):
        return "high_source_control"
    if (
        is_true_vertical
        and control_distance <= MODERATE_TEMPERATURE_CONTROL_KM
        and moderate_extrapolation
    ):
        return "medium_source_control"
    if is_driller_fallback or result_status == "calculated":
        return "low_source_control"
    return "blocked_missing_inputs"


def load_arctic_slope_public_wells(project_root: Path) -> gpd.GeoDataFrame:
    path = Path(project_root) / WELL_SOURCE_RELATIVE_PATH
    columns = [
        "object_id",
        "permit_number",
        "api_number",
        "well_name",
        "field",
        "pool",
        "current_class",
        "current_status",
        "driller_total_depth_ft",
        "true_vertical_depth_ft",
        "wellhead_latitude",
        "wellhead_longitude",
        "bottomhole_latitude",
        "bottomhole_longitude",
        "geometry",
    ]
    if not path.exists():
        return gpd.GeoDataFrame(columns=columns, geometry="geometry", crs="EPSG:4326")

    wells = gpd.read_file(path)
    wells = wells[wells["Geographic"].eq("ARCTIC SLOPE")].copy()
    wells = wells.rename(
        columns={
            "OBJECTID": "object_id",
            "PermitNumb": "permit_number",
            "APINumber": "api_number",
            "WellName": "well_name",
            "Field": "field",
            "Pools": "pool",
            "CurrentCla": "current_class",
            "CurrentSta": "current_status",
            "DrillerTot": "driller_total_depth_ft",
            "TrueVertic": "true_vertical_depth_ft",
            "WellHeadLa": "wellhead_latitude",
            "WellHeadLo": "wellhead_longitude",
            "BottomHole": "bottomhole_latitude",
            "BottomHo_1": "bottomhole_longitude",
        }
    )
    keep = [column for column in columns if column in wells.columns]
    wells = wells[keep]

    latitude = pd.to_numeric(wells["wellhead_latitude"], errors="coerce")
    longitude = pd.to_numeric(wells["wellhead_longitude"], errors="coerce")
    wells = wells.assign(wellhead_latitude=latitude, wellhead_longitude=longitude)
    wells = wells.dropna(subset=["wellhead_latitude", "wellhead_longitude"]).copy()
    return gpd.GeoDataFrame(
        wells.drop(columns="geometry", errors="ignore"),
        geometry=gpd.points_from_xy(wells["wellhead_longitude"], wells["wellhead_latitude"]),
        crs="EPSG:4326",
    )


def _depth_basis(row: pd.Series) -> pd.Series:
    true_vertical_depth = pd.to_numeric(row.get("true_vertical_depth_ft"), errors="coerce")
    driller_depth = pd.to_numeric(row.get("driller_total_depth_ft"), errors="coerce")
    if pd.notna(true_vertical_depth) and true_vertical_depth > 0:
        return pd.Series({"depth_basis": "TrueVertic", "depth_basis_ft": true_vertical_depth})
    if pd.notna(driller_depth) and driller_depth > 0:
        return pd.Series({"depth_basis": "DrillerTot", "depth_basis_ft": driller_depth})
    return pd.Series({"depth_basis": "missing", "depth_basis_ft": pd.NA})


def _join_assessment_units(
    wells: gpd.GeoDataFrame,
    assessment_units: gpd.GeoDataFrame,
) -> pd.DataFrame:
    if wells.empty or assessment_units.empty:
        return pd.DataFrame(
            {
                "object_id": wells.get("object_id", pd.Series(dtype="int64")),
                "hydrate_assessment_unit_count": 0,
                "hydrate_assessment_codes": "",
                "within_hydrate_assessment_unit": False,
            }
        )

    unit_columns = ["ASSESSCODE", "ASSESSNAME", "geometry"]
    joined = gpd.sjoin(
        wells[["object_id", "geometry"]],
        assessment_units[unit_columns],
        how="left",
        predicate="within",
    )

    def unique_join(values: pd.Series) -> str:
        clean = sorted({str(value) for value in values.dropna() if str(value).strip()})
        return "; ".join(clean)

    grouped = (
        joined.groupby("object_id", dropna=False)
        .agg(
            hydrate_assessment_unit_count=("ASSESSCODE", lambda values: values.dropna().nunique()),
            hydrate_assessment_codes=("ASSESSCODE", unique_join),
        )
        .reset_index()
    )
    grouped["within_hydrate_assessment_unit"] = (
        grouped["hydrate_assessment_unit_count"].fillna(0).astype(int) > 0
    )
    return grouped


def _join_nearest_permafrost_control(
    wells: gpd.GeoDataFrame,
    controls: gpd.GeoDataFrame,
) -> pd.DataFrame:
    columns = [
        "object_id",
        "nearest_ggd223_code",
        "nearest_ggd223_well",
        "nearest_permafrost_depth_m",
        "nearest_ggd223_distance_km",
    ]
    if wells.empty or controls.empty:
        return pd.DataFrame(columns=columns)

    nearest = gpd.sjoin_nearest(
        wells[["object_id", "geometry"]].to_crs("EPSG:3338"),
        controls[
            ["code", "well_designation", "permafrost_depth_m", "geometry"]
        ].to_crs("EPSG:3338"),
        how="left",
        distance_col="nearest_ggd223_distance_m",
    )
    nearest = nearest.sort_values(["object_id", "nearest_ggd223_distance_m"]).drop_duplicates(
        subset=["object_id"],
        keep="first",
    )
    output = nearest.rename(
        columns={
            "code": "nearest_ggd223_code",
            "well_designation": "nearest_ggd223_well",
            "permafrost_depth_m": "nearest_permafrost_depth_m",
        }
    )
    output["nearest_ggd223_distance_km"] = output["nearest_ggd223_distance_m"] / 1000
    return output[columns]


def build_public_well_stability_context(
    project_root: Path,
    source_root: Path | None = None,
) -> pd.DataFrame:
    root = Path(project_root)
    active_source = Path(source_root) if source_root is not None else active_stability_source_path(root)
    wells = load_arctic_slope_public_wells(root)
    controls = load_ggd223_permafrost_points(active_source)
    assessment_units = load_hydrate_assessment_units(active_source)

    if wells.empty:
        return pd.DataFrame()

    base = pd.DataFrame(wells.drop(columns="geometry", errors="ignore"))
    depth = base.apply(_depth_basis, axis=1)
    base = pd.concat([base, depth], axis=1)
    base["depth_basis_m"] = pd.to_numeric(base["depth_basis_ft"], errors="coerce") * 0.3048

    au_context = _join_assessment_units(wells, assessment_units)
    permafrost_context = _join_nearest_permafrost_control(wells, controls)

    context = base.merge(au_context, on="object_id", how="left").merge(
        permafrost_context,
        on="object_id",
        how="left",
    )
    context["hydrate_assessment_unit_count"] = (
        context["hydrate_assessment_unit_count"].fillna(0).astype(int)
    )
    context["within_hydrate_assessment_unit"] = context[
        "within_hydrate_assessment_unit"
    ].fillna(False)
    context["well_depth_exceeds_nearest_permafrost_control"] = (
        pd.to_numeric(context["depth_basis_m"], errors="coerce")
        >= pd.to_numeric(context["nearest_permafrost_depth_m"], errors="coerce")
    )

    context["stability_context_flag"] = "needs_depth_or_permafrost_context"
    context.loc[
        ~context["within_hydrate_assessment_unit"],
        "stability_context_flag",
    ] = "outside_usgs_hydrate_au"
    context.loc[
        context["within_hydrate_assessment_unit"]
        & context["depth_basis_m"].notna()
        & context["nearest_permafrost_depth_m"].notna()
        & ~context["well_depth_exceeds_nearest_permafrost_control"],
        "stability_context_flag",
    ] = "shallower_than_nearest_permafrost_control"
    context.loc[
        context["within_hydrate_assessment_unit"]
        & context["depth_basis_m"].notna()
        & context["nearest_permafrost_depth_m"].notna()
        & context["well_depth_exceeds_nearest_permafrost_control"],
        "stability_context_flag",
    ] = "public_context_candidate"

    sort_columns = ["within_hydrate_assessment_unit", "nearest_ggd223_distance_km", "well_name"]
    context = context.sort_values(sort_columns, ascending=[False, True, True]).reset_index(drop=True)
    return context[[column for column in WELL_CONTEXT_COLUMNS if column in context.columns]]


def stability_context_summary_frame(context: pd.DataFrame) -> pd.DataFrame:
    if context.empty:
        return pd.DataFrame(columns=["metric", "value", "meaning"])

    depth_available = pd.to_numeric(context["depth_basis_m"], errors="coerce").notna()
    rows = [
        {
            "metric": "Arctic Slope public wells",
            "value": int(len(context)),
            "meaning": "Alaska DNR wells filtered to Geographic = ARCTIC SLOPE.",
        },
        {
            "metric": "Inside USGS hydrate AU",
            "value": int(context["within_hydrate_assessment_unit"].sum()),
            "meaning": "Wellhead point falls inside one or more USGS 2019 hydrate assessment units.",
        },
        {
            "metric": "Depth field available",
            "value": int(depth_available.sum()),
            "meaning": "TrueVertic preferred; DrillerTot used only when TrueVertic is unavailable.",
        },
        {
            "metric": "Nearest GGD223 control assigned",
            "value": int(context["nearest_permafrost_depth_m"].notna().sum()),
            "meaning": "Nearest public permafrost-depth control point assigned by projected distance.",
        },
        {
            "metric": "Public context candidates",
            "value": int((context["stability_context_flag"] == "public_context_candidate").sum()),
            "meaning": "Inside a USGS hydrate AU and deeper than the nearest GGD223 permafrost-depth control.",
        },
    ]
    return pd.DataFrame(rows)


def load_public_well_stability_context(project_root: Path) -> pd.DataFrame:
    path = default_well_context_path(project_root)
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def _header_value(lines: list[str], label: str) -> str:
    prefix = f"{label}:"
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(prefix):
            return stripped.split(":", 1)[1].strip()
    return ""


def load_g10015_temperature_profile_points(path: Path) -> pd.DataFrame:
    lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    records = []
    for line in lines:
        match = NUMERIC_PROFILE_RE.match(line)
        if match:
            records.append((float(match.group(1)), float(match.group(2))))

    profile = pd.DataFrame(records, columns=["depth_m", "temperature_c"])
    if profile.empty:
        return profile

    profile = profile.sort_values("depth_m").reset_index(drop=True)
    if profile["depth_m"].duplicated().any():
        profile = (
            profile.groupby("depth_m", as_index=False, sort=True)
            .agg(temperature_c=("temperature_c", "mean"))
            .reset_index(drop=True)
        )
    return profile


def temperature_model_from_profile(
    profile_points: pd.DataFrame,
    depth_m: object,
    gradient_c_per_100m: object | None = None,
) -> pd.DataFrame:
    depth = pd.to_numeric(depth_m, errors="coerce")
    if isinstance(depth_m, pd.Series):
        depth_values = pd.Series(depth, index=depth_m.index, dtype="float64")
    elif np.isscalar(depth_m):
        depth_values = pd.Series([depth], dtype="float64")
    else:
        depth_values = pd.Series(np.asarray(depth, dtype=float), dtype="float64")

    result = pd.DataFrame({"depth_m": depth_values.to_numpy(dtype=float)})
    result["temperature_model_c"] = np.nan
    result["temperature_model_method"] = "not_calculated"
    result["temperature_extrapolated_below_profile"] = False
    result["temperature_extrapolation_below_profile_m"] = 0.0
    result["temperature_model_status"] = "not_calculated"

    missing_depth = result["depth_m"].isna()
    result.loc[missing_depth, ["temperature_model_method", "temperature_model_status"]] = (
        "blocked_missing_depth"
    )

    required_columns = {"depth_m", "temperature_c"}
    if profile_points.empty or not required_columns.issubset(profile_points.columns):
        modeled = ~missing_depth
        result.loc[modeled, ["temperature_model_method", "temperature_model_status"]] = (
            "blocked_no_temperature_profile"
        )
        return result[TEMPERATURE_MODEL_COLUMNS]

    profile = profile_points[["depth_m", "temperature_c"]].copy()
    profile["depth_m"] = pd.to_numeric(profile["depth_m"], errors="coerce")
    profile["temperature_c"] = pd.to_numeric(profile["temperature_c"], errors="coerce")
    profile = profile.dropna(subset=["depth_m", "temperature_c"]).sort_values("depth_m")
    if len(profile) < 2 or profile["depth_m"].nunique() < 2:
        modeled = ~missing_depth
        result.loc[modeled, ["temperature_model_method", "temperature_model_status"]] = (
            "blocked_no_temperature_profile"
        )
        return result[TEMPERATURE_MODEL_COLUMNS]
    if profile["depth_m"].duplicated().any():
        raise ValueError("Temperature profile points must not contain duplicate depths.")

    profile_depth = profile["depth_m"].to_numpy(dtype=float)
    profile_temperature = profile["temperature_c"].to_numpy(dtype=float)
    shallowest_depth = float(profile_depth[0])
    deepest_depth = float(profile_depth[-1])
    deepest_temperature = float(profile_temperature[-1])

    valid_depth = result["depth_m"].notna()
    above_profile = valid_depth & (result["depth_m"] < shallowest_depth)
    in_profile = valid_depth & result["depth_m"].between(shallowest_depth, deepest_depth)
    below_profile = valid_depth & (result["depth_m"] > deepest_depth)

    if in_profile.any():
        result.loc[in_profile, "temperature_model_c"] = np.interp(
            result.loc[in_profile, "depth_m"].to_numpy(dtype=float),
            profile_depth,
            profile_temperature,
        )
        result.loc[in_profile, "temperature_model_method"] = "measured_profile_interpolated"
        result.loc[in_profile, "temperature_model_status"] = "calculated"

    if above_profile.any():
        result.loc[above_profile, ["temperature_model_method", "temperature_model_status"]] = (
            "blocked_above_profile_range"
        )

    gradient = pd.to_numeric(gradient_c_per_100m, errors="coerce")
    if np.isscalar(gradient) and np.isfinite(gradient):
        if below_profile.any():
            extrapolation_m = result.loc[below_profile, "depth_m"] - deepest_depth
            result.loc[below_profile, "temperature_model_c"] = (
                deepest_temperature + extrapolation_m * float(gradient) / 100
            )
            result.loc[below_profile, "temperature_model_method"] = (
                "measured_profile_plus_gradient_extrapolation"
            )
            result.loc[below_profile, "temperature_model_status"] = "calculated"
            result.loc[below_profile, "temperature_extrapolated_below_profile"] = True
            result.loc[
                below_profile,
                "temperature_extrapolation_below_profile_m",
            ] = extrapolation_m
    elif below_profile.any():
        result.loc[below_profile, ["temperature_model_method", "temperature_model_status"]] = (
            "blocked_below_profile_no_gradient"
        )

    return result[TEMPERATURE_MODEL_COLUMNS]


def parse_g10015_temperature_profile(path: Path) -> dict[str, object]:
    lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    profile = load_g10015_temperature_profile_points(path)

    well_code = Path(path).stem.split("_", 1)[0]
    result: dict[str, object] = {
        "file_name": Path(path).name,
        "well_code": well_code,
        "well_name": _header_value(lines, "Well name"),
        "profile_file_name": _header_value(lines, "File name"),
        "log_date": _header_value(lines, "Log date"),
        "sample_count": len(profile),
        "min_depth_m": pd.NA,
        "max_depth_m": pd.NA,
        "min_temperature_c": pd.NA,
        "max_temperature_c": pd.NA,
        "deepest_temperature_c": pd.NA,
        "deepest_window_gradient_c_per_100m": pd.NA,
    }
    if profile.empty:
        return result

    deepest_depth = float(profile["depth_m"].max())
    deepest_window = profile[profile["depth_m"] >= deepest_depth - 100]
    gradient = pd.NA
    if len(deepest_window) >= 3 and deepest_window["depth_m"].nunique() >= 2:
        slope = np.polyfit(
            deepest_window["depth_m"].to_numpy(),
            deepest_window["temperature_c"].to_numpy(),
            1,
        )[0]
        gradient = float(slope * 100)

    result.update(
        {
            "min_depth_m": float(profile["depth_m"].min()),
            "max_depth_m": deepest_depth,
            "min_temperature_c": float(profile["temperature_c"].min()),
            "max_temperature_c": float(profile["temperature_c"].max()),
            "deepest_temperature_c": float(profile.iloc[-1]["temperature_c"]),
            "deepest_window_gradient_c_per_100m": gradient,
        }
    )
    return result


def build_g10015_temperature_inventory(source_root: Path) -> pd.DataFrame:
    profile_dir = Path(source_root) / G10015_RELATIVE_PATH
    if not profile_dir.exists():
        return pd.DataFrame()
    records = [
        parse_g10015_temperature_profile(path)
        for path in sorted(profile_dir.glob("*.txt"))
    ]
    if not records:
        return pd.DataFrame()
    inventory = pd.DataFrame(records)
    return inventory.sort_values(["well_code", "log_date", "file_name"]).reset_index(drop=True)


def temperature_inventory_summary_frame(inventory: pd.DataFrame) -> pd.DataFrame:
    if inventory.empty:
        return pd.DataFrame(columns=["metric", "value", "meaning"])
    gradient_count = pd.to_numeric(
        inventory["deepest_window_gradient_c_per_100m"],
        errors="coerce",
    ).notna()
    rows = [
        {
            "metric": "G10015 profiles",
            "value": int(len(inventory)),
            "meaning": "Processed public borehole temperature log files indexed.",
        },
        {
            "metric": "Unique well codes",
            "value": int(inventory["well_code"].nunique()),
            "meaning": "Unique public G10015/GGD223-style well codes represented by profiles.",
        },
        {
            "metric": "Maximum logged depth m",
            "value": round(float(pd.to_numeric(inventory["max_depth_m"], errors="coerce").max()), 2),
            "meaning": "Deepest depth reached by any indexed public temperature profile.",
        },
        {
            "metric": "Profiles with deepest-window gradient",
            "value": int(gradient_count.sum()),
            "meaning": "Profiles with enough deepest-window samples for a rough C per 100 m context estimate.",
        },
    ]
    return pd.DataFrame(rows)


def stability_parameter_readiness_frame() -> pd.DataFrame:
    rows = [
        {
            "input": "Well location",
            "current_status": "Ready",
            "current_source": "Alaska DNR Well Bottom Hole Location",
            "use_in_stability": "Spatial anchor for public well context and future stability joins.",
            "next_step": "Keep public well identifiers and coordinates separate from any future restricted rows.",
        },
        {
            "input": "Well depth",
            "current_status": "Ready for public context",
            "current_source": "DNR TrueVertic preferred, DrillerTot fallback",
            "use_in_stability": "Depth basis for checking whether a well reaches candidate stability intervals.",
            "next_step": "Confirm final approved depth basis and units when real workbook data arrives.",
        },
        {
            "input": "Base of ice-bearing permafrost",
            "current_status": "Partial",
            "current_source": "Nearest NSIDC GGD223 point controls; OM-222 plate not digitized",
            "use_in_stability": "Upper thermal boundary/context for permafrost-associated hydrate stability.",
            "next_step": "Digitize/georeference OM-222 or locate a ready public GIS derivative.",
        },
        {
            "input": "Temperature context",
            "current_status": "Ready as inventory",
            "current_source": "NSIDC G10015 processed borehole temperature logs",
            "use_in_stability": "Constrains local temperature-depth behavior and geothermal-gradient context.",
            "next_step": "Build well-specific or area-specific geothermal profiles from the inventory.",
        },
        {
            "input": "Geothermal gradient",
            "current_status": "Context only",
            "current_source": "Deepest-window estimates from G10015 profiles",
            "use_in_stability": "Approximate temperature increase with depth.",
            "next_step": "Replace rough estimates with calibrated gradients and uncertainty bands.",
        },
        {
            "input": "Pressure assumption",
            "current_status": "Ready as public assumption",
            "current_source": (
                "Freshwater hydrostatic equation; absolute pressure adds "
                "surface_pressure_mpa = 0.101325"
            ),
            "use_in_stability": "Converts depth to pressure for pressure-temperature phase comparison.",
            "next_step": (
                "Keep assumption code visible and replace only with a cited measured-pressure "
                "or brine-density scenario run."
            ),
        },
        {
            "input": "Hydrate phase curve",
            "current_status": "Ready as digitized lookup",
            "current_source": (
                "USGS SIR 2008-5175 Figure 1A 100 percent methane + 5 ppt "
                "baseline; Collett et al. 2011 mixed-gas source cataloged as sensitivity-only"
            ),
            "use_in_stability": "Defines pressure-temperature conditions where methane hydrate can exist.",
            "next_step": (
                "Keep 100 percent methane as the official baseline; add mixed-gas "
                "lookup only after digitizing or generating a cited curve."
            ),
        },
        {
            "input": "Stability top/base/thickness",
            "current_status": "Not calculated yet",
            "current_source": "Requires all inputs above",
            "use_in_stability": "Final admissibility-zone result for ML feature engineering and screening.",
            "next_step": "Calculate only after pressure, temperature, permafrost-base, and phase-curve assumptions are locked.",
        },
    ]
    return pd.DataFrame(rows)


def stability_input_capability_matrix_frame() -> pd.DataFrame:
    rows = [
        {
            "input_name": "Public well location",
            "capability_status": "ready_public_input",
            "current_source": "Alaska DNR Well Bottom Hole Location",
            "current_coverage": "8,084 Arctic Slope public wells in current scaffold",
            "supports_now": "Map joins, AU context, nearest public permafrost/temperature control joins.",
            "does_not_support_yet": "Bottom-hole path, deviation survey, or approved well-log depth alignment.",
            "future_upgrade": "Approved well coordinates, deviation surveys, and interval-level joins.",
            "screen_role": "Spatial context and control-distance confidence input.",
            "guardrail": "Location context is not hydrate evidence.",
        },
        {
            "input_name": "Public well depth",
            "capability_status": "ready_public_input_with_caveat",
            "current_source": "DNR TrueVertic preferred; DrillerTot fallback",
            "current_coverage": "Public depth available for 7,578 scaffold wells",
            "supports_now": "Pressure-at-depth estimates and reach tests for candidate intervals.",
            "does_not_support_yet": "Final log-depth datums, measured-depth to TVD conversion, or interval picks.",
            "future_upgrade": "Approved workbook/LAS depth basis and datum reconciliation.",
            "screen_role": "Depth basis for public stability screening.",
            "guardrail": "DrillerTot fallback is lower-confidence than TrueVertic.",
        },
        {
            "input_name": "Permafrost point control",
            "capability_status": "partial_public_input",
            "current_source": "NSIDC GGD223 nearest permafrost-depth controls",
            "current_coverage": "43 public controls; nearest control assigned to 8,084 scaffold wells",
            "supports_now": "Permafrost context and control-distance confidence labels.",
            "does_not_support_yet": "Continuous base-of-ice-bearing-permafrost surface.",
            "future_upgrade": "Digitized/georeferenced USGS OM-222 or another public GIS surface.",
            "screen_role": "Thermal-context input and caveat source.",
            "guardrail": "Nearest point control is not a mapped permafrost-base surface.",
        },
        {
            "input_name": "Temperature profiles",
            "capability_status": "partial_public_input",
            "current_source": "NSIDC G10015 processed borehole temperature logs",
            "current_coverage": "184 profiles; 483 scaffold rows matched; 374 rows ready for phase-curve inputs",
            "supports_now": "Temperature interpolation and limited gradient extrapolation for matched rows.",
            "does_not_support_yet": "Final stability calculation for unmatched wells.",
            "future_upgrade": "Well-specific temperature models and uncertainty bands.",
            "screen_role": "Primary temperature model source for the first public screen.",
            "guardrail": "Rows without a matched profile stay blocked or scenario-only.",
        },
        {
            "input_name": "Hydrostatic pressure",
            "capability_status": "ready_baseline_assumption",
            "current_source": "Freshwater hydrostatic equation plus atmospheric pressure for absolute P-T comparison",
            "current_coverage": "Available for scaffold rows with public depth or permafrost-control depth",
            "supports_now": "Gauge and absolute pressure estimates for phase-curve lookup.",
            "does_not_support_yet": "Measured formation pressure, overpressure, salinity-density, or gas-column effects.",
            "future_upgrade": "Approved pressure data or versioned brine-density scenarios.",
            "screen_role": "Baseline pressure model.",
            "guardrail": "Hydrostatic pressure is an assumption, not measured reservoir pressure.",
        },
        {
            "input_name": "100 percent methane phase curve",
            "capability_status": "ready_official_baseline",
            "current_source": "USGS SIR 2008-5175 Figure 1A digitized lookup",
            "current_coverage": "41 monotonic lookup rows; official_public_baseline",
            "supports_now": "Baseline methane hydrate pressure-temperature equilibrium lookup.",
            "does_not_support_yet": "Mixed gas, measured gas, or alternate salinity final runs.",
            "future_upgrade": "Direct CSMHYD/CSMGem export if obtained.",
            "screen_role": "Official mentor-approved phase-curve baseline.",
            "guardrail": "Baseline stability is necessary but not sufficient for hydrate presence.",
        },
        {
            "input_name": "Mixed-gas phase curve",
            "capability_status": "scenario_candidate_only",
            "current_source": "Collett et al. 2011 / Holder et al. 1987 mixed-gas figure",
            "current_coverage": "Source identified for 98% methane, 1.5% ethane, 0.5% propane; no lookup yet",
            "supports_now": "Justifies variable-capable architecture and sensitivity planning.",
            "does_not_support_yet": "Final stability outputs or freeform composition interpolation.",
            "future_upgrade": "Digitize the curve or generate it from a cited thermodynamic model.",
            "screen_role": "Sensitivity candidate only.",
            "guardrail": "Do not apply until a versioned lookup or model export exists.",
        },
        {
            "input_name": "Gas composition",
            "capability_status": "future_approved_or_scenario_input",
            "current_source": "Baseline assumption and literature scenario only",
            "current_coverage": "Baseline methane fraction is fixed at 100%; no measured well gas composition in repo",
            "supports_now": "Baseline and cataloged sensitivity metadata.",
            "does_not_support_yet": "Measured-gas stability calculation.",
            "future_upgrade": "Approved gas composition fields or cited composition-specific model curves.",
            "screen_role": "Phase-curve selector metadata.",
            "guardrail": "No freeform gas slider without thermodynamic-model support.",
        },
        {
            "input_name": "Salinity",
            "capability_status": "baseline_assumption_only",
            "current_source": "USGS SIR 2008-5175 methane + 5 ppt salt-water curve",
            "current_coverage": "Baseline salinity fixed at 5 ppt for current lookup",
            "supports_now": "Official baseline phase-curve assumption.",
            "does_not_support_yet": "Well-specific salinity or alternate salinity final runs.",
            "future_upgrade": "Approved formation-water salinity or versioned salinity scenarios.",
            "screen_role": "Phase-curve assumption metadata.",
            "guardrail": "Changing salinity requires a new curve/run ID.",
        },
        {
            "input_name": "Hydrate assessment units",
            "capability_status": "ready_public_context",
            "current_source": "USGS 2019 Northern Alaska gas hydrate assessment unit polygons",
            "current_coverage": "3 hydrate AUs; 7,992 scaffold wells inside one or more AUs",
            "supports_now": "Regional context and outside-AU caveat labels.",
            "does_not_support_yet": "Direct hydrate occurrence, saturation, or reservoir quality.",
            "future_upgrade": "Approved interval evidence and reservoir-quality data.",
            "screen_role": "Regional context filter, not proof.",
            "guardrail": "AU membership is not a detection.",
        },
        {
            "input_name": "Approved logs and core labels",
            "capability_status": "blocked_future_approved_data",
            "current_source": "Not present in public repo",
            "current_coverage": "No real well-log rows, core rows, or authoritative saturation labels committed",
            "supports_now": "Architecture and schema planning only.",
            "does_not_support_yet": "Occurrence classification, saturation regression, or sweet-spot ranking.",
            "future_upgrade": "Approved runtime workbook/LAS/core tables and target registry.",
            "screen_role": "Future ML input and target source.",
            "guardrail": "Do not train or claim model results from public scaffold rows.",
        },
    ]
    return pd.DataFrame(rows, columns=STABILITY_INPUT_CAPABILITY_MATRIX_COLUMNS)


def stability_osl_pull_triggers_frame() -> pd.DataFrame:
    rows = [
        {
            "trigger": "Develop temperature-model logic with unit-test fixtures",
            "needs_osl": "no",
            "why": "Synthetic or tiny fixture profiles are enough to test interpolation, extrapolation, and blocked-row behavior.",
            "expected_action": "Implement and test local functions without rebuilding public products.",
            "public_output_after_pull": "None.",
        },
        {
            "trigger": "Build real public temperature-model products from G10015 rows",
            "needs_osl": "yes",
            "why": "The repo commits only the compact G10015 inventory; raw processed profile rows remain in the full OSL/source bundle.",
            "expected_action": "Pull or sync the full OSL source bundle, then run the product builder against `data/source_library/north_slope_stability_sources_2026-06-13/`.",
            "public_output_after_pull": "Versioned temperature-model product and updated summaries under `data/public_stability_products/`.",
        },
        {
            "trigger": "Regenerate well context, GGD223 joins, G10015 inventory, or AU joins from raw public sources",
            "needs_osl": "yes",
            "why": "Those rebuilds require raw shapefiles, raw NSIDC files, and source bundle folder structure that are intentionally not committed to Git.",
            "expected_action": "Run `python 01_pipeline/build_public_stability_products.py` from a workspace with the full bundle present.",
            "public_output_after_pull": "Refreshed public-safe context/scaffold CSVs.",
        },
        {
            "trigger": "Add OM-222 digitized/georeferenced permafrost-base surface",
            "needs_osl": "yes",
            "why": "The source plate and any GIS digitizing workflow belong in the heavy-data workbench before compact derived layers are committed.",
            "expected_action": "Digitize/georeference in OSL or local GIS, record provenance, export a compact public-safe surface/control product.",
            "public_output_after_pull": "Versioned OM-222-derived permafrost product plus source/provenance note.",
        },
        {
            "trigger": "Replace digitized SIR phase curve with direct CSMHYD/CSMGem or a new digitized source",
            "needs_osl": "maybe",
            "why": "No OSL pull is needed for metadata or tests, but heavy external model files, PDFs, or digitization artifacts should live outside Git.",
            "expected_action": "Generate or digitize the new curve, save only the compact versioned lookup and catalog metadata in Git.",
            "public_output_after_pull": "New `phase_curve_*_v*.csv` plus updated scenario catalog and tests.",
        },
        {
            "trigger": "Run approved well-log/core ML workflow",
            "needs_osl": "no_public_repo_pull",
            "why": "Approved/runtime data are outside the public Git workflow and should not be pulled into this repo.",
            "expected_action": "Run only inside the authorized environment; export public-safe summaries only if approved.",
            "public_output_after_pull": "No raw approved data; possibly approved-safe aggregate figures/tables later.",
        },
    ]
    return pd.DataFrame(rows, columns=STABILITY_OSL_PULL_TRIGGER_COLUMNS)


def stability_website_product_spec_frame() -> pd.DataFrame:
    rows = [
        {
            "website_area": "Top status strip",
            "final_content": "Run ID, baseline/scenario role, phase-curve ID, pressure model, temperature model, and final-result count.",
            "primary_user_action": "Verify what assumptions the displayed screen is using.",
            "must_show": "`official_public_baseline` for the default 100 percent methane run.",
            "must_not_claim": "Do not call the run hydrate proof or a validated ML result.",
            "data_dependency": "Scenario catalog, pressure model metadata, temperature-model product, future stability screen.",
        },
        {
            "website_area": "Input readiness and capability",
            "final_content": "Readiness table plus capability matrix showing ready, partial, scenario-only, and blocked inputs.",
            "primary_user_action": "See why some rows can be calculated and others are blocked.",
            "must_show": "Rows without matched temperature profiles are blocked or scenario-only.",
            "must_not_claim": "Do not imply every public well has enough temperature control for final stability.",
            "data_dependency": "Capability matrix and scaffold summary.",
        },
        {
            "website_area": "Map view",
            "final_content": "Wells colored by stability result status or confidence, hydrate AU outlines, GGD223 controls, and later OM-222 surface/context.",
            "primary_user_action": "Scan where baseline-eligible, blocked, and outside-AU wells are located.",
            "must_show": "Legend entries for calculated, blocked, scenario-only, and outside-AU rows.",
            "must_not_claim": "Do not color a point as hydrate occurrence or saturation.",
            "data_dependency": "Well context, scaffold, future stability screen, public snapshot/bundle layers.",
        },
        {
            "website_area": "Well detail panel",
            "final_content": "Selected well summary with depth basis, nearest permafrost control, matched temperature profile, pressure assumption, phase curve, result status, caveats, and notes.",
            "primary_user_action": "Audit why a single well is calculated, blocked, or scenario-only.",
            "must_show": "Control distance, temperature profile code/file, extrapolation flag, caveat codes.",
            "must_not_claim": "Do not hide DrillerTot fallback, extrapolation, or missing-profile caveats.",
            "data_dependency": "Scaffold, temperature-model product, future stability screen.",
        },
        {
            "website_area": "Temperature and phase plot",
            "final_content": "Depth-temperature profile with measured and extrapolated temperature segments plus selected phase-boundary curve.",
            "primary_user_action": "Visually inspect the top/base intersection logic for a selected calculated row.",
            "must_show": "Measured versus extrapolated segments and the selected phase-curve source.",
            "must_not_claim": "Do not draw intersections for rows with missing temperature models.",
            "data_dependency": "Raw/profile-derived temperature model from OSL and phase lookup.",
        },
        {
            "website_area": "Results table",
            "final_content": "Downloadable `stability_screen_*.csv` preview with top/base/thickness only for rows that pass the gates; nulls and blocked reasons for the rest.",
            "primary_user_action": "Filter by result status, confidence, caveat code, AU, and temperature-control status.",
            "must_show": "Run ID, phase-curve role, confidence, caveat codes, and blocked reasons.",
            "must_not_claim": "Do not fill top/base/thickness for blocked rows.",
            "data_dependency": "Future tested stability-screen product.",
        },
        {
            "website_area": "Scenario controls",
            "final_content": "Disabled or clearly caveated controls for mixed gas, salinity, pressure-density, and regional-gradient scenarios until their lookups/models exist.",
            "primary_user_action": "Understand which assumptions are baseline and which are sensitivity-only.",
            "must_show": "Mixed-gas source is cataloged but not applied until a lookup/model export exists.",
            "must_not_claim": "No freeform gas slider without thermodynamic-model backing.",
            "data_dependency": "Scenario catalog and future versioned lookups.",
        },
        {
            "website_area": "Exports and citations",
            "final_content": "Download buttons for scaffold, capability matrix, scenario catalog, phase curve, and future stability screen, plus source/caveat citations.",
            "primary_user_action": "Export public-safe products and cite assumptions.",
            "must_show": "USGS SIR 2008-5175, NSIDC G10015/GGD223, USGS AU source, and Collett et al. 2011 for sensitivity planning.",
            "must_not_claim": "Do not expose raw source bundles or approved runtime rows.",
            "data_dependency": "Committed public products and docs.",
        },
    ]
    return pd.DataFrame(rows, columns=STABILITY_WEBSITE_PRODUCT_SPEC_COLUMNS)


def load_g10015_temperature_inventory(project_root: Path) -> pd.DataFrame:
    path = default_g10015_inventory_path(project_root)
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def load_stability_temperature_model(project_root: Path) -> pd.DataFrame:
    path = default_stability_temperature_model_path(project_root)
    if not path.exists():
        return pd.DataFrame(columns=STABILITY_TEMPERATURE_MODEL_PRODUCT_COLUMNS)
    return pd.read_csv(path)


def representative_temperature_profiles(inventory: pd.DataFrame) -> pd.DataFrame:
    if inventory.empty:
        return pd.DataFrame()

    frame = inventory.copy()
    numeric_columns = [
        "sample_count",
        "max_depth_m",
        "deepest_temperature_c",
        "deepest_window_gradient_c_per_100m",
    ]
    for column in numeric_columns:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")

    frame["profile_count_for_code"] = frame.groupby("well_code")["file_name"].transform("count")
    frame = frame.sort_values(
        [
            "well_code",
            "max_depth_m",
            "sample_count",
            "file_name",
        ],
        ascending=[True, False, False, True],
    )
    return frame.drop_duplicates("well_code", keep="first").reset_index(drop=True)


def _profile_points_from_source(
    source_root: Path,
    file_name: object,
    cache: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    if pd.isna(file_name) or not str(file_name).strip():
        return pd.DataFrame(columns=["depth_m", "temperature_c"])
    name = str(file_name)
    if name not in cache:
        path = Path(source_root) / G10015_RELATIVE_PATH / name
        if path.exists():
            cache[name] = load_g10015_temperature_profile_points(path)
        else:
            cache[name] = pd.DataFrame(columns=["depth_m", "temperature_c"])
    return cache[name]


def build_stability_temperature_model(
    project_root: Path,
    source_root: Path,
) -> pd.DataFrame:
    scaffold = load_stability_input_scaffold(project_root)
    if scaffold.empty:
        return pd.DataFrame(columns=STABILITY_TEMPERATURE_MODEL_PRODUCT_COLUMNS)

    profile_cache: dict[str, pd.DataFrame] = {}
    rows: list[dict[str, object]] = []
    key_depths = [
        ("nearest_permafrost_control", "nearest_permafrost_depth_m"),
        ("depth_basis", "depth_basis_m"),
    ]
    for _, row in scaffold.iterrows():
        profile_points = _profile_points_from_source(
            source_root,
            row.get("nearest_temperature_profile_file"),
            profile_cache,
        )
        gradient = pd.to_numeric(row.get("rough_geothermal_gradient_c_per_100m"), errors="coerce")
        gradient_source = "deepest_window_g10015_inventory"
        if not np.isfinite(gradient):
            gradient = None
            gradient_source = "none"

        for depth_role, depth_column in key_depths:
            model = temperature_model_from_profile(
                profile_points,
                row.get(depth_column),
                gradient_c_per_100m=gradient,
            ).iloc[0]
            rows.append(
                {
                    "object_id": row.get("object_id"),
                    "permit_number": row.get("permit_number"),
                    "api_number": row.get("api_number"),
                    "well_name": row.get("well_name"),
                    "temperature_model_id": TEMPERATURE_MODEL_ID,
                    "temperature_model_depth_role": depth_role,
                    "depth_m": model["depth_m"],
                    "temperature_model_c": model["temperature_model_c"],
                    "temperature_model_method": model["temperature_model_method"],
                    "temperature_extrapolated_below_profile": model[
                        "temperature_extrapolated_below_profile"
                    ],
                    "temperature_extrapolation_below_profile_m": model[
                        "temperature_extrapolation_below_profile_m"
                    ],
                    "temperature_model_status": model["temperature_model_status"],
                    "temperature_profile_code": row.get("nearest_temperature_profile_code"),
                    "temperature_profile_file": row.get("nearest_temperature_profile_file"),
                    "temperature_profile_max_depth_m": row.get("temperature_profile_max_depth_m"),
                    "temperature_gradient_c_per_100m": gradient,
                    "temperature_gradient_source": gradient_source,
                    "temperature_profile_link_method": row.get("temperature_profile_link_method"),
                    "stability_input_readiness": row.get("stability_input_readiness"),
                    "temperature_model_product_role": "temperature_input_only_not_stability_result",
                    "stability_top_base_thickness_status": "not_calculated",
                }
            )

    if not rows:
        return pd.DataFrame(columns=STABILITY_TEMPERATURE_MODEL_PRODUCT_COLUMNS)
    model = pd.DataFrame(rows)
    return model[STABILITY_TEMPERATURE_MODEL_PRODUCT_COLUMNS]


def stability_temperature_model_summary_frame(model: pd.DataFrame) -> pd.DataFrame:
    if model.empty:
        return pd.DataFrame(columns=["metric", "value", "meaning"])

    calculated = model["temperature_model_status"].eq("calculated")
    extrapolated = model["temperature_extrapolated_below_profile"].fillna(False).astype(bool)
    rows = [
        {
            "metric": "Temperature model rows",
            "value": int(len(model)),
            "meaning": "One row per scaffold well per modeled key depth.",
        },
        {
            "metric": "Calculated key depths",
            "value": int(calculated.sum()),
            "meaning": "Key-depth temperatures calculated from profile interpolation or gradient extrapolation.",
        },
        {
            "metric": "Extrapolated key depths",
            "value": int((calculated & extrapolated).sum()),
            "meaning": "Calculated key depths below measured profile coverage.",
        },
        {
            "metric": "Blocked key depths",
            "value": int((~calculated).sum()),
            "meaning": "Key-depth rows left without modeled temperature because required profile/depth inputs are missing.",
        },
        {
            "metric": "Final stability results",
            "value": 0,
            "meaning": "This product models temperature inputs only; top/base/thickness remain uncalculated.",
        },
    ]
    return pd.DataFrame(rows)


def build_stability_input_scaffold(project_root: Path) -> pd.DataFrame:
    context = load_public_well_stability_context(project_root)
    inventory = load_g10015_temperature_inventory(project_root)
    if context.empty:
        return pd.DataFrame()

    representative_profiles = representative_temperature_profiles(inventory)
    profile_columns = [
        "well_code",
        "file_name",
        "well_name",
        "log_date",
        "profile_count_for_code",
        "max_depth_m",
        "deepest_temperature_c",
        "deepest_window_gradient_c_per_100m",
    ]
    if representative_profiles.empty:
        profile_lookup = pd.DataFrame(columns=profile_columns)
    else:
        profile_lookup = representative_profiles[
            [column for column in profile_columns if column in representative_profiles.columns]
        ].rename(
            columns={
                "well_code": "nearest_temperature_profile_code",
                "file_name": "nearest_temperature_profile_file",
                "well_name": "nearest_temperature_profile_well",
                "log_date": "nearest_temperature_profile_log_date",
                "profile_count_for_code": "temperature_profile_count_for_code",
                "max_depth_m": "temperature_profile_max_depth_m",
                "deepest_temperature_c": "temperature_profile_deepest_temperature_c",
                "deepest_window_gradient_c_per_100m": "rough_geothermal_gradient_c_per_100m",
            }
        )

    scaffold = context.merge(
        profile_lookup,
        left_on="nearest_ggd223_code",
        right_on="nearest_temperature_profile_code",
        how="left",
    )

    scaffold["temperature_profile_link_method"] = "no_matching_g10015_profile_for_nearest_ggd223_code"
    scaffold.loc[
        scaffold["nearest_temperature_profile_code"].notna(),
        "temperature_profile_link_method",
    ] = "matched_nearest_ggd223_code"

    depth_m = pd.to_numeric(scaffold["depth_basis_m"], errors="coerce")
    permafrost_m = pd.to_numeric(scaffold["nearest_permafrost_depth_m"], errors="coerce")
    scaffold["hydrostatic_pressure_mpa_at_depth_basis"] = hydrostatic_pressure_mpa_gauge(depth_m)
    scaffold["hydrostatic_pressure_mpa_at_nearest_permafrost_control"] = (
        hydrostatic_pressure_mpa_gauge(permafrost_m)
    )
    scaffold["hydrostatic_pressure_mpa_absolute_at_depth_basis"] = (
        hydrostatic_pressure_mpa_absolute(depth_m)
    )
    scaffold["hydrostatic_pressure_mpa_absolute_at_nearest_permafrost_control"] = (
        hydrostatic_pressure_mpa_absolute(permafrost_m)
    )
    scaffold["pressure_assumption_code"] = (
        "hydrostatic_freshwater_0p00980665_mpa_per_m_surface_0p101325_mpa"
    )
    scaffold["phase_curve_status"] = "not_applied"
    scaffold["planned_phase_curve_id"] = PHASE_CURVE_ID
    scaffold["planned_phase_curve_role"] = PHASE_CURVE_ROLE
    scaffold["planned_phase_curve_allowed_use"] = PHASE_CURVE_ALLOWED_USE
    scaffold["planned_gas_composition_assumption"] = PHASE_CURVE_GAS_COMPOSITION_ASSUMPTION
    scaffold["planned_gas_methane_mol_pct"] = PHASE_CURVE_GAS_METHANE_MOL_PCT
    scaffold["planned_gas_ethane_mol_pct"] = PHASE_CURVE_GAS_ETHANE_MOL_PCT
    scaffold["planned_gas_propane_mol_pct"] = PHASE_CURVE_GAS_PROPANE_MOL_PCT
    scaffold["planned_gas_butane_plus_mol_pct"] = PHASE_CURVE_GAS_BUTANE_PLUS_MOL_PCT
    scaffold["planned_salinity_ppt_assumption"] = PHASE_CURVE_SALINITY_PPT
    scaffold["stability_top_base_thickness_status"] = "not_calculated"

    scaffold["stability_input_readiness"] = "missing_depth_or_permafrost_context"
    scaffold.loc[
        ~scaffold["within_hydrate_assessment_unit"],
        "stability_input_readiness",
    ] = "outside_usgs_hydrate_au"
    scaffold.loc[
        scaffold["within_hydrate_assessment_unit"]
        & depth_m.notna()
        & permafrost_m.notna()
        & scaffold["nearest_temperature_profile_code"].isna(),
        "stability_input_readiness",
    ] = "needs_temperature_profile_match"
    scaffold.loc[
        scaffold["within_hydrate_assessment_unit"]
        & depth_m.notna()
        & permafrost_m.notna()
        & scaffold["nearest_temperature_profile_code"].notna(),
        "stability_input_readiness",
    ] = "ready_for_phase_curve_inputs"

    keep_columns = [
        "object_id",
        "permit_number",
        "api_number",
        "well_name",
        "field",
        "pool",
        "wellhead_latitude",
        "wellhead_longitude",
        "depth_basis",
        "depth_basis_m",
        "hydrate_assessment_codes",
        "within_hydrate_assessment_unit",
        "nearest_ggd223_code",
        "nearest_ggd223_well",
        "nearest_permafrost_depth_m",
        "nearest_ggd223_distance_km",
        "nearest_temperature_profile_code",
        "nearest_temperature_profile_file",
        "nearest_temperature_profile_well",
        "nearest_temperature_profile_log_date",
        "temperature_profile_count_for_code",
        "temperature_profile_max_depth_m",
        "temperature_profile_deepest_temperature_c",
        "rough_geothermal_gradient_c_per_100m",
        "temperature_profile_link_method",
        "hydrostatic_pressure_mpa_at_depth_basis",
        "hydrostatic_pressure_mpa_at_nearest_permafrost_control",
        "hydrostatic_pressure_mpa_absolute_at_depth_basis",
        "hydrostatic_pressure_mpa_absolute_at_nearest_permafrost_control",
        "pressure_assumption_code",
        "phase_curve_status",
        "planned_phase_curve_id",
        "planned_phase_curve_role",
        "planned_phase_curve_allowed_use",
        "planned_gas_composition_assumption",
        "planned_gas_methane_mol_pct",
        "planned_gas_ethane_mol_pct",
        "planned_gas_propane_mol_pct",
        "planned_gas_butane_plus_mol_pct",
        "planned_salinity_ppt_assumption",
        "stability_top_base_thickness_status",
        "stability_input_readiness",
    ]
    return scaffold[[column for column in keep_columns if column in scaffold.columns]]


def stability_input_scaffold_summary_frame(scaffold: pd.DataFrame) -> pd.DataFrame:
    if scaffold.empty:
        return pd.DataFrame(columns=["metric", "value", "meaning"])

    rows = [
        {
            "metric": "Wells in input scaffold",
            "value": int(len(scaffold)),
            "meaning": "Public Arctic Slope wells carried into the stability-input scaffold.",
        },
        {
            "metric": "Temperature profile matched",
            "value": int(scaffold["nearest_temperature_profile_code"].notna().sum()),
            "meaning": "Rows where the nearest GGD223 permafrost-control code has a G10015 profile inventory match.",
        },
        {
            "metric": "Ready for phase-curve inputs",
            "value": int((scaffold["stability_input_readiness"] == "ready_for_phase_curve_inputs").sum()),
            "meaning": "Rows with AU context, depth, permafrost control, and temperature-profile context.",
        },
        {
            "metric": "Needs temperature profile match",
            "value": int((scaffold["stability_input_readiness"] == "needs_temperature_profile_match").sum()),
            "meaning": "Rows with public depth/permafrost context but no matching G10015 inventory code yet.",
        },
        {
            "metric": "Final stability results",
            "value": 0,
            "meaning": "Top/base/thickness are intentionally not calculated until phase-curve and pressure-temperature assumptions are locked.",
        },
    ]
    return pd.DataFrame(rows)


def load_stability_input_scaffold(project_root: Path) -> pd.DataFrame:
    path = default_stability_input_scaffold_path(project_root)
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def write_stability_temperature_model_product(
    project_root: Path,
    source_root: Path | None = None,
) -> tuple[Path, Path] | tuple[None, None]:
    active_source = Path(source_root) if source_root is not None else active_stability_source_path(project_root)
    profile_dir = active_source / G10015_RELATIVE_PATH
    if not profile_dir.exists() or not any(profile_dir.glob("*.txt")):
        return None, None

    model = build_stability_temperature_model(project_root, active_source)
    if model.empty:
        return None, None

    product_dir = default_stability_products_dir(project_root)
    product_dir.mkdir(parents=True, exist_ok=True)
    model_summary = stability_temperature_model_summary_frame(model)
    model_path = default_stability_temperature_model_path(project_root)
    model_summary_path = default_stability_temperature_model_summary_path(project_root)
    model.to_csv(model_path, index=False)
    model_summary.to_csv(model_summary_path, index=False)
    return model_path, model_summary_path


def write_public_stability_products(
    project_root: Path,
    source_root: Path | None = None,
) -> tuple[Path, Path, Path | None, Path | None, Path | None, Path | None]:
    product_dir = default_stability_products_dir(project_root)
    product_dir.mkdir(parents=True, exist_ok=True)
    active_source = Path(source_root) if source_root is not None else active_stability_source_path(project_root)
    context = build_public_well_stability_context(project_root, active_source)
    summary = stability_context_summary_frame(context)
    context_path = default_well_context_path(project_root)
    summary_path = default_well_context_summary_path(project_root)
    context.to_csv(context_path, index=False)
    summary.to_csv(summary_path, index=False)

    inventory = build_g10015_temperature_inventory(active_source)
    if inventory.empty:
        return context_path, summary_path, None, None, None, None

    inventory_summary = temperature_inventory_summary_frame(inventory)
    inventory_path = default_g10015_inventory_path(project_root)
    inventory_summary_path = default_g10015_summary_path(project_root)
    inventory.to_csv(inventory_path, index=False)
    inventory_summary.to_csv(inventory_summary_path, index=False)

    scaffold = build_stability_input_scaffold(project_root)
    scaffold_summary = stability_input_scaffold_summary_frame(scaffold)
    scaffold_path = default_stability_input_scaffold_path(project_root)
    scaffold_summary_path = default_stability_input_scaffold_summary_path(project_root)
    scaffold.to_csv(scaffold_path, index=False)
    scaffold_summary.to_csv(scaffold_summary_path, index=False)
    return (
        context_path,
        summary_path,
        inventory_path,
        inventory_summary_path,
        scaffold_path,
        scaffold_summary_path,
    )
