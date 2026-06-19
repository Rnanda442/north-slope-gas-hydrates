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
PUBLIC_ML_PRODUCTS_DIR_NAME = "public_ml_products"
WELL_CONTEXT_FILE_NAME = "north_slope_well_stability_context_2026-06-14.csv"
WELL_CONTEXT_SUMMARY_FILE_NAME = "north_slope_well_stability_context_summary_2026-06-14.csv"
G10015_INVENTORY_FILE_NAME = "g10015_temperature_profile_inventory_2026-06-14.csv"
G10015_SUMMARY_FILE_NAME = "g10015_temperature_profile_summary_2026-06-14.csv"
G10015_PROFILE_POINTS_FILE_NAME = "g10015_temperature_profile_points_sampled_2026-06-14.csv"
G10015_PROFILE_POINTS_SUMMARY_FILE_NAME = (
    "g10015_temperature_profile_points_sampled_summary_2026-06-14.csv"
)
STABILITY_INPUT_SCAFFOLD_FILE_NAME = "stability_input_scaffold_2026-06-14.csv"
STABILITY_INPUT_SCAFFOLD_SUMMARY_FILE_NAME = "stability_input_scaffold_summary_2026-06-14.csv"
STABILITY_INPUT_CAPABILITY_MATRIX_FILE_NAME = "stability_input_capability_matrix_2026-06-14.csv"
STABILITY_OSL_PULL_TRIGGERS_FILE_NAME = "stability_osl_pull_triggers_2026-06-14.csv"
STABILITY_WEBSITE_PRODUCT_SPEC_FILE_NAME = "stability_website_product_spec_2026-06-14.csv"
STABILITY_TEMPERATURE_MODEL_FILE_NAME = "stability_temperature_model_2026-06-14.csv"
STABILITY_TEMPERATURE_MODEL_SUMMARY_FILE_NAME = "stability_temperature_model_summary_2026-06-14.csv"
STABILITY_SCREEN_RUN_ID = "stability_screen_2026_06_14_methane_5ppt_v1"
STABILITY_SCREEN_VERSION = "2026-06-14.v1"
STABILITY_SCREEN_FILE_NAME = "stability_screen_2026-06-14_methane_5ppt_v1.csv"
STABILITY_SCREEN_SUMMARY_FILE_NAME = "stability_screen_summary_2026-06-14_methane_5ppt_v1.csv"
PUBLIC_ML_FEATURE_SCAFFOLD_VERSION = "2026-06-15.v1"
PUBLIC_ML_FEATURE_SCAFFOLD_FILE_NAME = "public_ml_feature_scaffold_2026-06-15.csv"
PUBLIC_ML_FEATURE_SCAFFOLD_SUMMARY_FILE_NAME = "public_ml_feature_scaffold_summary_2026-06-15.csv"
PUBLIC_ML_FEATURE_DICTIONARY_FILE_NAME = "public_ml_feature_dictionary_2026-06-15.csv"
PUBLIC_ML_TARGET_REGISTRY_FILE_NAME = "public_ml_target_registry_2026-06-15.csv"
PUBLIC_ML_LEAKAGE_GUARDRAILS_FILE_NAME = "public_ml_leakage_guardrails_2026-06-15.csv"
APPROVED_SCHEMA_COVERAGE_MATRIX_FILE_NAME = (
    "approved_schema_coverage_matrix_2026-06-15.csv"
)
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

G10015_PROFILE_POINTS_PRODUCT_COLUMNS = [
    "well_code",
    "well_name",
    "file_name",
    "profile_file_name",
    "log_date",
    "depth_m",
    "temperature_c",
    "point_index",
    "source_sample_count",
    "sampled_point_count",
    "sample_method",
    "profile_point_role",
    "public_product_role",
]

STABILITY_SCREEN_COLUMNS = [
    "screen_run_id",
    "screen_version",
    "object_id",
    "permit_number",
    "api_number",
    "well_name",
    "field",
    "pool",
    "lat",
    "lon",
    "tvd_m",
    "depth_source",
    "depth_basis_ft",
    "depth_reference_note",
    "hydrate_assessment_codes",
    "within_hydrate_assessment_unit",
    "permafrost_base_m",
    "permafrost_source",
    "permafrost_control_code",
    "permafrost_control_distance_km",
    "permafrost_confidence",
    "temperature_model_id",
    "temperature_source",
    "temperature_profile_code",
    "temperature_profile_file",
    "temperature_profile_max_depth_m",
    "temperature_gradient_c_per_100m",
    "temperature_gradient_source",
    "temperature_extrapolated_below_profile",
    "temperature_extrapolation_below_profile_m",
    "temperature_model_confidence",
    "pressure_model_id",
    "pressure_source",
    "pore_fluid_density_kg_m3",
    "gravity_m_s2",
    "surface_pressure_mpa",
    "pressure_gradient_mpa_per_m",
    "pressure_at_tvd_mpa_absolute",
    "phase_curve_id",
    "phase_curve_role",
    "phase_curve_allowed_use",
    "phase_curve_source",
    "gas_composition_assumption",
    "gas_methane_mol_pct",
    "gas_ethane_mol_pct",
    "gas_propane_mol_pct",
    "gas_butane_plus_mol_pct",
    "salinity_ppt_assumption",
    "phase_curve_status",
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
    "stability_result_status",
    "stability_confidence",
    "caveat_codes",
    "stability_notes",
]

PUBLIC_ML_FEATURE_SCAFFOLD_COLUMNS = [
    "public_ml_feature_scaffold_version",
    "public_product_role",
    "ml_row_grain",
    "object_id",
    "permit_number",
    "api_number",
    "well_name",
    "field",
    "pool",
    "lat",
    "lon",
    "current_status",
    "hydrate_assessment_codes",
    "hydrate_assessment_unit_count",
    "within_hydrate_assessment_unit",
    "tvd_m",
    "depth_source",
    "depth_basis_ft",
    "depth_available",
    "permafrost_base_m",
    "permafrost_control_code",
    "permafrost_control_distance_km",
    "permafrost_confidence",
    "well_depth_exceeds_nearest_permafrost_control",
    "well_depth_minus_permafrost_control_m",
    "temperature_profile_matched",
    "temperature_profile_code",
    "temperature_profile_file",
    "temperature_profile_count_for_code",
    "temperature_profile_max_depth_m",
    "temperature_gradient_c_per_100m",
    "temperature_gradient_source",
    "temperature_profile_link_method",
    "temperature_at_permafrost_control_c",
    "temperature_at_permafrost_control_method",
    "temperature_at_permafrost_control_status",
    "temperature_at_permafrost_control_extrapolated",
    "temperature_at_permafrost_control_extrapolation_m",
    "temperature_at_depth_basis_c",
    "temperature_at_depth_basis_method",
    "temperature_at_depth_basis_status",
    "temperature_at_depth_basis_extrapolated",
    "temperature_at_depth_basis_extrapolation_m",
    "pressure_model_id",
    "pressure_at_tvd_mpa_absolute",
    "pressure_at_permafrost_control_mpa_absolute",
    "phase_curve_id",
    "phase_curve_role",
    "phase_curve_allowed_use",
    "gas_composition_assumption",
    "gas_methane_mol_pct",
    "salinity_ppt_assumption",
    "stability_input_readiness",
    "stability_result_status",
    "stability_confidence",
    "stability_interval_calculated",
    "no_stable_interval_under_baseline",
    "stability_top_m",
    "stability_base_m",
    "stability_thickness_m",
    "well_penetrated_stability_thickness_m",
    "reaches_stability_zone",
    "caveat_codes",
    "blank_or_block_reason",
    "public_ml_feature_readiness",
    "ml_training_readiness",
    "hydrate_occurrence_label_status",
    "hydrate_saturation_label_status",
    "allowed_ml_use",
    "prohibited_ml_use",
    "label_guardrail",
]

PUBLIC_ML_FEATURE_DICTIONARY_COLUMNS = [
    "column_name",
    "feature_group",
    "source_product",
    "source_column",
    "current_status",
    "allowed_ml_use",
    "prohibited_use",
    "upgrade_needed",
    "notes",
]

PUBLIC_ML_TARGET_REGISTRY_COLUMNS = [
    "original_header",
    "canonical_target_family",
    "target_task",
    "target_role",
    "source_evidence",
    "allowed_use",
    "prohibited_use",
    "leakage_policy",
    "current_public_status",
    "unit_or_scale_status",
    "future_resolution_needed",
    "notes",
]

PUBLIC_ML_LEAKAGE_GUARDRAIL_COLUMNS = [
    "guardrail_id",
    "pipeline_stage",
    "rule",
    "target_headers_covered",
    "allowed_inputs",
    "blocked_inputs",
    "reason",
    "implementation_status",
]

APPROVED_SCHEMA_COVERAGE_MATRIX_COLUMNS = [
    "source_reference",
    "sheet_or_dataset_name",
    "original_header",
    "canonical_alias",
    "role",
    "feature_family",
    "unit_status",
    "required_for_model",
    "available_in_current_subset",
    "expected_in_future_71_dataset_collection",
    "leakage_risk",
    "allowed_use",
    "prohibited_use",
    "unresolved_question",
    "notes",
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


def default_public_ml_products_dir(project_root: Path) -> Path:
    return project_root / "data" / PUBLIC_ML_PRODUCTS_DIR_NAME


def default_well_context_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / WELL_CONTEXT_FILE_NAME


def default_well_context_summary_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / WELL_CONTEXT_SUMMARY_FILE_NAME


def default_g10015_inventory_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / G10015_INVENTORY_FILE_NAME


def default_g10015_summary_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / G10015_SUMMARY_FILE_NAME


def default_g10015_profile_points_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / G10015_PROFILE_POINTS_FILE_NAME


def default_g10015_profile_points_summary_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / G10015_PROFILE_POINTS_SUMMARY_FILE_NAME


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


def default_stability_screen_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / STABILITY_SCREEN_FILE_NAME


def default_stability_screen_summary_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / STABILITY_SCREEN_SUMMARY_FILE_NAME


def default_public_ml_feature_scaffold_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / PUBLIC_ML_FEATURE_SCAFFOLD_FILE_NAME


def default_public_ml_feature_scaffold_summary_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / PUBLIC_ML_FEATURE_SCAFFOLD_SUMMARY_FILE_NAME


def default_public_ml_feature_dictionary_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / PUBLIC_ML_FEATURE_DICTIONARY_FILE_NAME


def default_public_ml_target_registry_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / PUBLIC_ML_TARGET_REGISTRY_FILE_NAME


def default_public_ml_leakage_guardrails_path(project_root: Path) -> Path:
    return default_stability_products_dir(project_root) / PUBLIC_ML_LEAKAGE_GUARDRAILS_FILE_NAME


def default_approved_schema_coverage_matrix_path(project_root: Path) -> Path:
    return default_public_ml_products_dir(project_root) / APPROVED_SCHEMA_COVERAGE_MATRIX_FILE_NAME


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


def phase_curve_max_depth_m(
    phase_curve: pd.DataFrame,
    surface_pressure_mpa: float = SURFACE_PRESSURE_MPA,
    pressure_gradient_mpa_per_m: float = HYDROSTATIC_PRESSURE_MPA_PER_M,
) -> float:
    if phase_curve.empty:
        return np.nan
    max_pressure = pd.to_numeric(
        phase_curve["pressure_mpa_absolute"],
        errors="coerce",
    ).max()
    if pd.isna(max_pressure):
        return np.nan
    return float((max_pressure - surface_pressure_mpa) / pressure_gradient_mpa_per_m)


def phase_curve_min_depth_m(
    phase_curve: pd.DataFrame,
    surface_pressure_mpa: float = SURFACE_PRESSURE_MPA,
    pressure_gradient_mpa_per_m: float = HYDROSTATIC_PRESSURE_MPA_PER_M,
) -> float:
    if phase_curve.empty:
        return np.nan
    min_pressure = pd.to_numeric(
        phase_curve["pressure_mpa_absolute"],
        errors="coerce",
    ).min()
    if pd.isna(min_pressure):
        return np.nan
    return float((min_pressure - surface_pressure_mpa) / pressure_gradient_mpa_per_m)


def stability_depth_grid(
    depth_limit_m: object,
    step_m: object = DEFAULT_STABILITY_DEPTH_GRID_STEP_M,
    start_depth_m: object = 0.0,
) -> np.ndarray:
    limit = pd.to_numeric(depth_limit_m, errors="coerce")
    step = pd.to_numeric(step_m, errors="coerce")
    start = pd.to_numeric(start_depth_m, errors="coerce")
    if not np.isfinite(step) or float(step) <= 0:
        raise ValueError("Stability depth-grid step must be a positive number.")
    if not np.isfinite(limit) or float(limit) < 0 or not np.isfinite(start):
        return np.array([], dtype=float)

    limit_value = float(limit)
    start_value = max(0.0, float(start))
    if limit_value < start_value:
        return np.array([], dtype=float)
    if limit_value == start_value:
        return np.array([start_value], dtype=float)

    grid = np.arange(start_value, limit_value, float(step))
    grid = np.append(grid, limit_value)
    return np.unique(np.round(grid, 10)).astype(float)


def stability_condition_grid_from_profile(
    profile_points: pd.DataFrame,
    phase_curve: pd.DataFrame,
    depth_limit_m: object,
    gradient_c_per_100m: object | None = None,
    step_m: object = DEFAULT_STABILITY_DEPTH_GRID_STEP_M,
    start_depth_m: object = 0.0,
) -> pd.DataFrame:
    grid = stability_depth_grid(depth_limit_m, step_m, start_depth_m=start_depth_m)
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


def sample_g10015_temperature_profile_points(
    profile_points: pd.DataFrame,
    max_points: int = 160,
) -> tuple[pd.DataFrame, str]:
    if profile_points.empty:
        return profile_points.copy(), "empty_profile"
    if max_points <= 1:
        raise ValueError("max_points must be greater than 1.")

    points = profile_points.sort_values("depth_m").reset_index(drop=True)
    if len(points) <= max_points:
        return points.copy(), "all_points"

    selected = np.unique(np.round(np.linspace(0, len(points) - 1, max_points)).astype(int))
    sampled = points.iloc[selected].copy().reset_index(drop=True)
    return sampled, f"evenly_sampled_max_{max_points}_points"


def build_g10015_temperature_profile_points_product(
    source_root: Path,
    max_points_per_profile: int = 160,
) -> pd.DataFrame:
    profile_dir = Path(source_root) / G10015_RELATIVE_PATH
    if not profile_dir.exists():
        return pd.DataFrame(columns=G10015_PROFILE_POINTS_PRODUCT_COLUMNS)

    rows: list[dict[str, object]] = []
    for path in sorted(profile_dir.glob("*.txt")):
        metadata = parse_g10015_temperature_profile(path)
        profile_points = load_g10015_temperature_profile_points(path)
        if profile_points.empty:
            continue
        sampled, sample_method = sample_g10015_temperature_profile_points(
            profile_points,
            max_points=max_points_per_profile,
        )
        sampled_point_count = len(sampled)
        for point_index, row in enumerate(sampled.itertuples(index=False), start=1):
            rows.append(
                {
                    "well_code": metadata.get("well_code"),
                    "well_name": metadata.get("well_name"),
                    "file_name": metadata.get("file_name"),
                    "profile_file_name": metadata.get("profile_file_name"),
                    "log_date": metadata.get("log_date"),
                    "depth_m": float(row.depth_m),
                    "temperature_c": float(row.temperature_c),
                    "point_index": point_index,
                    "source_sample_count": int(metadata.get("sample_count", len(profile_points))),
                    "sampled_point_count": sampled_point_count,
                    "sample_method": sample_method,
                    "profile_point_role": "sampled_measured_g10015_profile_point",
                    "public_product_role": "temperature_curve_visualization_only_not_stability_result",
                }
            )

    if not rows:
        return pd.DataFrame(columns=G10015_PROFILE_POINTS_PRODUCT_COLUMNS)
    frame = pd.DataFrame(rows, columns=G10015_PROFILE_POINTS_PRODUCT_COLUMNS)
    return frame.sort_values(["well_code", "log_date", "file_name", "depth_m"]).reset_index(
        drop=True
    )


def g10015_temperature_profile_points_summary_frame(points: pd.DataFrame) -> pd.DataFrame:
    if points.empty:
        return pd.DataFrame(columns=["metric", "value", "meaning"])

    source_counts = pd.to_numeric(points["source_sample_count"], errors="coerce")
    sampled_counts = (
        points.groupby("file_name")["sampled_point_count"].max()
        if "file_name" in points.columns
        else pd.Series(dtype=float)
    )
    rows = [
        {
            "metric": "Sampled profile rows",
            "value": int(len(points)),
            "meaning": "Rows exported for public website temperature-curve visualization.",
        },
        {
            "metric": "Profiles represented",
            "value": int(points["file_name"].nunique()),
            "meaning": "Unique public G10015 processed temperature-log files with sampled points.",
        },
        {
            "metric": "Unique well codes",
            "value": int(points["well_code"].nunique()),
            "meaning": "G10015 well codes represented by the sampled public curve product.",
        },
        {
            "metric": "Maximum source rows per profile",
            "value": int(source_counts.max()) if source_counts.notna().any() else 0,
            "meaning": "Maximum parsed rows in any source profile before sampling.",
        },
        {
            "metric": "Maximum sampled rows per profile",
            "value": int(sampled_counts.max()) if not sampled_counts.empty else 0,
            "meaning": "Maximum rows retained for any one public profile curve.",
        },
    ]
    return pd.DataFrame(rows)


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


def load_g10015_temperature_profile_points_product(project_root: Path) -> pd.DataFrame:
    path = default_g10015_profile_points_path(project_root)
    if not path.exists():
        return pd.DataFrame(columns=G10015_PROFILE_POINTS_PRODUCT_COLUMNS)
    return pd.read_csv(path)


def load_stability_temperature_model(project_root: Path) -> pd.DataFrame:
    path = default_stability_temperature_model_path(project_root)
    if not path.exists():
        return pd.DataFrame(columns=STABILITY_TEMPERATURE_MODEL_PRODUCT_COLUMNS)
    return pd.read_csv(path)


def load_stability_screen(project_root: Path) -> pd.DataFrame:
    path = default_stability_screen_path(project_root)
    if not path.exists():
        return pd.DataFrame(columns=STABILITY_SCREEN_COLUMNS)
    return pd.read_csv(path)


def _series_or_default(frame: pd.DataFrame, column: str, default: object = pd.NA) -> pd.Series:
    if column in frame.columns:
        return frame[column]
    return pd.Series(default, index=frame.index)


def _numeric_series(frame: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_numeric(_series_or_default(frame, column), errors="coerce")


def _boolean_series(frame: pd.DataFrame, column: str) -> pd.Series:
    values = _series_or_default(frame, column, False)
    if values.dtype == bool:
        return values.fillna(False)
    return values.map(
        lambda value: str(value).strip().lower() in {"true", "1", "yes", "y"}
        if pd.notna(value)
        else False
    )


def _has_text_series(frame: pd.DataFrame, column: str) -> pd.Series:
    values = _series_or_default(frame, column)
    return values.notna() & values.astype(str).str.strip().ne("")


def _temperature_model_feature_frame(model: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "object_id",
        "temperature_at_permafrost_control_c",
        "temperature_at_permafrost_control_method",
        "temperature_at_permafrost_control_status",
        "temperature_at_permafrost_control_extrapolated",
        "temperature_at_permafrost_control_extrapolation_m",
        "temperature_at_depth_basis_c",
        "temperature_at_depth_basis_method",
        "temperature_at_depth_basis_status",
        "temperature_at_depth_basis_extrapolated",
        "temperature_at_depth_basis_extrapolation_m",
    ]
    if model.empty or "object_id" not in model.columns:
        return pd.DataFrame(columns=columns)

    role_prefixes = {
        "nearest_permafrost_control": "temperature_at_permafrost_control",
        "depth_basis": "temperature_at_depth_basis",
    }
    rows: list[dict[str, object]] = []
    for object_id, group in model.groupby("object_id", dropna=False):
        output: dict[str, object] = {"object_id": object_id}
        for role, prefix in role_prefixes.items():
            role_rows = group[group["temperature_model_depth_role"].eq(role)]
            if role_rows.empty:
                output[f"{prefix}_c"] = np.nan
                output[f"{prefix}_method"] = "missing"
                output[f"{prefix}_status"] = "missing"
                output[f"{prefix}_extrapolated"] = False
                output[f"{prefix}_extrapolation_m"] = np.nan
                continue
            row = role_rows.iloc[0]
            output[f"{prefix}_c"] = row.get("temperature_model_c")
            output[f"{prefix}_method"] = row.get("temperature_model_method")
            output[f"{prefix}_status"] = row.get("temperature_model_status")
            output[f"{prefix}_extrapolated"] = bool(
                str(row.get("temperature_extrapolated_below_profile")).lower() == "true"
                or row.get("temperature_extrapolated_below_profile") is True
            )
            output[f"{prefix}_extrapolation_m"] = row.get(
                "temperature_extrapolation_below_profile_m"
            )
        rows.append(output)
    return pd.DataFrame(rows, columns=columns)


def _public_ml_feature_readiness(row: pd.Series) -> str:
    status = str(row.get("stability_result_status", "missing"))
    if not bool(row.get("within_hydrate_assessment_unit")):
        return "context_only_outside_public_hydrate_au"
    if not bool(row.get("depth_available")):
        return "blocked_missing_public_depth"
    if not bool(row.get("temperature_profile_matched")):
        return "blocked_missing_temperature_profile"
    if status == "calculated":
        return "feature_ready_with_calculated_stability_interval"
    if status == "calculated_no_stable_interval":
        return "feature_ready_no_stable_interval_under_baseline"
    if status == "blocked_phase_curve_range_insufficient":
        return "blocked_phase_curve_range_insufficient"
    return f"context_only_{status}"


def _blank_or_block_reason(row: pd.Series) -> str:
    status = str(row.get("stability_result_status", "missing"))
    if status == "calculated":
        return "calculated_baseline_stability_interval"
    if status == "calculated_no_stable_interval":
        return "calculated_no_stable_interval_under_baseline"
    if status == "outside_au_context":
        return "outside_public_usgs_hydrate_assessment_unit"
    if status.startswith("blocked_"):
        return status
    return "context_only_or_unknown"


def build_public_ml_feature_scaffold(project_root: Path) -> pd.DataFrame:
    screen = load_stability_screen(project_root)
    if screen.empty:
        return pd.DataFrame(columns=PUBLIC_ML_FEATURE_SCAFFOLD_COLUMNS)

    base = screen.copy()
    context = load_public_well_stability_context(project_root)
    if not context.empty:
        context_columns = [
            "object_id",
            "current_status",
            "depth_basis_ft",
            "hydrate_assessment_unit_count",
            "well_depth_exceeds_nearest_permafrost_control",
        ]
        available_context = [column for column in context_columns if column in context.columns]
        base = base.merge(
            context[available_context],
            on="object_id",
            how="left",
            suffixes=("", "_context"),
        )

    scaffold = load_stability_input_scaffold(project_root)
    if not scaffold.empty:
        scaffold_columns = [
            "object_id",
            "stability_input_readiness",
            "temperature_profile_count_for_code",
            "temperature_profile_link_method",
            "hydrostatic_pressure_mpa_absolute_at_nearest_permafrost_control",
        ]
        available_scaffold = [column for column in scaffold_columns if column in scaffold.columns]
        base = base.merge(
            scaffold[available_scaffold],
            on="object_id",
            how="left",
            suffixes=("", "_scaffold"),
        )

    temperature_features = _temperature_model_feature_frame(
        load_stability_temperature_model(project_root)
    )
    if not temperature_features.empty:
        base = base.merge(temperature_features, on="object_id", how="left")

    features = pd.DataFrame(index=base.index)
    features["public_ml_feature_scaffold_version"] = PUBLIC_ML_FEATURE_SCAFFOLD_VERSION
    features["public_product_role"] = "public_ml_feature_scaffold_not_training_labels"
    features["ml_row_grain"] = "one_public_well"
    for column in [
        "object_id",
        "permit_number",
        "api_number",
        "well_name",
        "field",
        "pool",
        "lat",
        "lon",
        "current_status",
        "hydrate_assessment_codes",
        "hydrate_assessment_unit_count",
        "depth_source",
        "depth_basis_ft",
        "permafrost_control_code",
        "permafrost_confidence",
        "temperature_profile_code",
        "temperature_profile_file",
        "temperature_profile_count_for_code",
        "temperature_gradient_source",
        "temperature_profile_link_method",
        "temperature_at_permafrost_control_method",
        "temperature_at_permafrost_control_status",
        "temperature_at_depth_basis_method",
        "temperature_at_depth_basis_status",
        "pressure_model_id",
        "phase_curve_id",
        "phase_curve_role",
        "phase_curve_allowed_use",
        "gas_composition_assumption",
        "stability_input_readiness",
        "stability_result_status",
        "stability_confidence",
        "caveat_codes",
    ]:
        features[column] = _series_or_default(base, column)

    if "depth_basis_ft_context" in base.columns:
        features["depth_basis_ft"] = base["depth_basis_ft_context"]

    numeric_columns = [
        "tvd_m",
        "permafrost_base_m",
        "permafrost_control_distance_km",
        "temperature_profile_max_depth_m",
        "temperature_gradient_c_per_100m",
        "temperature_at_permafrost_control_c",
        "temperature_at_permafrost_control_extrapolation_m",
        "temperature_at_depth_basis_c",
        "temperature_at_depth_basis_extrapolation_m",
        "pressure_at_tvd_mpa_absolute",
        "pressure_at_permafrost_control_mpa_absolute",
        "gas_methane_mol_pct",
        "salinity_ppt_assumption",
        "stability_top_m",
        "stability_base_m",
        "stability_thickness_m",
        "well_penetrated_stability_thickness_m",
    ]
    for column in numeric_columns:
        source_column = column
        if column == "pressure_at_permafrost_control_mpa_absolute":
            source_column = "hydrostatic_pressure_mpa_absolute_at_nearest_permafrost_control"
        features[column] = _numeric_series(base, source_column)

    features["within_hydrate_assessment_unit"] = _boolean_series(
        base,
        "within_hydrate_assessment_unit",
    )
    features["well_depth_exceeds_nearest_permafrost_control"] = _boolean_series(
        base,
        "well_depth_exceeds_nearest_permafrost_control",
    )
    features["temperature_at_permafrost_control_extrapolated"] = _boolean_series(
        base,
        "temperature_at_permafrost_control_extrapolated",
    )
    features["temperature_at_depth_basis_extrapolated"] = _boolean_series(
        base,
        "temperature_at_depth_basis_extrapolated",
    )
    features["reaches_stability_zone"] = _boolean_series(base, "reaches_stability_zone")
    features["depth_available"] = features["tvd_m"].notna()
    features["temperature_profile_matched"] = _has_text_series(base, "temperature_profile_file")
    features["well_depth_minus_permafrost_control_m"] = (
        features["tvd_m"] - features["permafrost_base_m"]
    )
    features["stability_interval_calculated"] = features["stability_result_status"].eq(
        "calculated"
    )
    features["no_stable_interval_under_baseline"] = features["stability_result_status"].eq(
        "calculated_no_stable_interval"
    )
    features["blank_or_block_reason"] = features.apply(_blank_or_block_reason, axis=1)
    features["public_ml_feature_readiness"] = features.apply(
        _public_ml_feature_readiness,
        axis=1,
    )
    features["ml_training_readiness"] = "not_training_ready_no_validated_hydrate_labels"
    features["hydrate_occurrence_label_status"] = "not_available_in_public_scaffold"
    features["hydrate_saturation_label_status"] = "not_available_in_public_scaffold"
    features["allowed_ml_use"] = "feature_engineering_and_coverage_readiness_only"
    features["prohibited_ml_use"] = (
        "hydrate_presence_absence_label;hydrate_saturation_label;"
        "validated_model_training;sweet_spot_ranking"
    )
    features["label_guardrail"] = (
        "baseline stability screen may be used as a physics-derived feature, "
        "not as hydrate occurrence or saturation ground truth"
    )

    for column in PUBLIC_ML_FEATURE_SCAFFOLD_COLUMNS:
        if column not in features.columns:
            features[column] = pd.NA
    return features[PUBLIC_ML_FEATURE_SCAFFOLD_COLUMNS]


def public_ml_feature_scaffold_summary_frame(features: pd.DataFrame) -> pd.DataFrame:
    if features.empty:
        return pd.DataFrame(columns=["metric", "value", "meaning"])

    rows = [
        {
            "metric": "Feature scaffold rows",
            "value": int(len(features)),
            "meaning": "One row per public well carried into the ML-readiness scaffold.",
        },
        {
            "metric": "Rows inside public hydrate AU",
            "value": int(features["within_hydrate_assessment_unit"].fillna(False).sum()),
            "meaning": "Rows inside one or more USGS hydrate assessment units.",
        },
        {
            "metric": "Rows with public depth",
            "value": int(features["depth_available"].fillna(False).sum()),
            "meaning": "Rows with a public vertical-depth basis for pressure/depth features.",
        },
        {
            "metric": "Rows with matched temperature profile",
            "value": int(features["temperature_profile_matched"].fillna(False).sum()),
            "meaning": "Rows linked to a public G10015 temperature-profile context.",
        },
        {
            "metric": "Rows with calculated stability interval feature",
            "value": int(features["stability_interval_calculated"].fillna(False).sum()),
            "meaning": "Rows with non-null baseline stability top/base/thickness features.",
        },
        {
            "metric": "Rows with no stable interval under baseline",
            "value": int(features["no_stable_interval_under_baseline"].fillna(False).sum()),
            "meaning": "Rows where inputs were sufficient but the baseline screen found no stable interval.",
        },
        {
            "metric": "Rows with validated hydrate occurrence labels",
            "value": 0,
            "meaning": "No public scaffold row is a validated hydrate-present or hydrate-absent label.",
        },
        {
            "metric": "Rows training-ready for occurrence/saturation ML",
            "value": 0,
            "meaning": "Approved labels/logs are still required before model training.",
        },
    ]
    return pd.DataFrame(rows)


def public_ml_feature_dictionary_frame() -> pd.DataFrame:
    groups = {
        "public_ml_feature_scaffold_version": "product_metadata",
        "public_product_role": "product_metadata",
        "ml_row_grain": "product_metadata",
        "object_id": "well_identity",
        "permit_number": "well_identity",
        "api_number": "well_identity",
        "well_name": "well_identity",
        "field": "well_identity",
        "pool": "well_identity",
        "lat": "well_location",
        "lon": "well_location",
        "current_status": "well_context",
        "hydrate_assessment_codes": "regional_context",
        "hydrate_assessment_unit_count": "regional_context",
        "within_hydrate_assessment_unit": "regional_context",
        "tvd_m": "depth_context",
        "depth_source": "depth_context",
        "depth_basis_ft": "depth_context",
        "depth_available": "depth_context",
        "permafrost_base_m": "permafrost_context",
        "permafrost_control_code": "permafrost_context",
        "permafrost_control_distance_km": "permafrost_context",
        "permafrost_confidence": "permafrost_context",
        "well_depth_exceeds_nearest_permafrost_control": "permafrost_context",
        "well_depth_minus_permafrost_control_m": "permafrost_context",
        "temperature_profile_matched": "temperature_context",
        "temperature_profile_code": "temperature_context",
        "temperature_profile_file": "temperature_context",
        "temperature_profile_count_for_code": "temperature_context",
        "temperature_profile_max_depth_m": "temperature_context",
        "temperature_gradient_c_per_100m": "temperature_context",
        "temperature_gradient_source": "temperature_context",
        "temperature_profile_link_method": "temperature_context",
        "temperature_at_permafrost_control_c": "temperature_model",
        "temperature_at_permafrost_control_method": "temperature_model",
        "temperature_at_permafrost_control_status": "temperature_model",
        "temperature_at_permafrost_control_extrapolated": "temperature_model",
        "temperature_at_permafrost_control_extrapolation_m": "temperature_model",
        "temperature_at_depth_basis_c": "temperature_model",
        "temperature_at_depth_basis_method": "temperature_model",
        "temperature_at_depth_basis_status": "temperature_model",
        "temperature_at_depth_basis_extrapolated": "temperature_model",
        "temperature_at_depth_basis_extrapolation_m": "temperature_model",
        "pressure_model_id": "pressure_phase_context",
        "pressure_at_tvd_mpa_absolute": "pressure_phase_context",
        "pressure_at_permafrost_control_mpa_absolute": "pressure_phase_context",
        "phase_curve_id": "pressure_phase_context",
        "phase_curve_role": "pressure_phase_context",
        "phase_curve_allowed_use": "pressure_phase_context",
        "gas_composition_assumption": "pressure_phase_context",
        "gas_methane_mol_pct": "pressure_phase_context",
        "salinity_ppt_assumption": "pressure_phase_context",
        "stability_input_readiness": "stability_screen",
        "stability_result_status": "stability_screen",
        "stability_confidence": "stability_screen",
        "stability_interval_calculated": "stability_screen",
        "no_stable_interval_under_baseline": "stability_screen",
        "stability_top_m": "stability_screen",
        "stability_base_m": "stability_screen",
        "stability_thickness_m": "stability_screen",
        "well_penetrated_stability_thickness_m": "stability_screen",
        "reaches_stability_zone": "stability_screen",
        "caveat_codes": "stability_screen",
        "blank_or_block_reason": "stability_screen",
        "public_ml_feature_readiness": "ml_readiness",
        "ml_training_readiness": "ml_readiness",
        "hydrate_occurrence_label_status": "label_policy",
        "hydrate_saturation_label_status": "label_policy",
        "allowed_ml_use": "label_policy",
        "prohibited_ml_use": "label_policy",
        "label_guardrail": "label_policy",
    }
    source_products = {
        "product_metadata": "public_ml_feature_scaffold",
        "well_identity": "stability_screen;well_context",
        "well_location": "stability_screen",
        "well_context": "well_context",
        "regional_context": "well_context;stability_screen",
        "depth_context": "well_context;stability_screen",
        "permafrost_context": "GGD223 nearest control via stability_screen",
        "temperature_context": "G10015 inventory/scaffold",
        "temperature_model": "stability_temperature_model",
        "pressure_phase_context": "stability_screen",
        "stability_screen": "stability_screen",
        "ml_readiness": "derived_public_ml_feature_scaffold",
        "label_policy": "project_guardrail",
    }
    rows = []
    for column in PUBLIC_ML_FEATURE_SCAFFOLD_COLUMNS:
        group = groups[column]
        is_label_policy = group == "label_policy"
        is_stability_result = group == "stability_screen"
        rows.append(
            {
                "column_name": column,
                "feature_group": group,
                "source_product": source_products[group],
                "source_column": "derived" if column not in STABILITY_SCREEN_COLUMNS else column,
                "current_status": (
                    "guardrail_not_feature"
                    if is_label_policy
                    else "public_feature_available_with_caveats"
                ),
                "allowed_ml_use": (
                    "policy/audit only"
                    if is_label_policy
                    else "candidate feature or coverage/audit field"
                ),
                "prohibited_use": (
                    "Do not use as a hydrate occurrence, absence, saturation, or producibility label."
                    if is_stability_result or is_label_policy
                    else "Do not use without source/caveat awareness."
                ),
                "upgrade_needed": (
                    "Approved hydrate occurrence/saturation labels and log-depth aligned inputs."
                    if is_label_policy
                    else "Use approved runtime data or improved public controls to strengthen this field."
                ),
                "notes": (
                    "Stability fields are thermodynamic-admissibility features only, not proof."
                    if is_stability_result
                    else "Public-source feature scaffold field."
                ),
            }
        )
    return pd.DataFrame(rows, columns=PUBLIC_ML_FEATURE_DICTIONARY_COLUMNS)


def public_ml_target_registry_frame() -> pd.DataFrame:
    rows = [
        {
            "original_header": "Sgh",
            "canonical_target_family": "hydrate_saturation",
            "target_task": "saturation_regression;occurrence_label_derivation_after_threshold_policy",
            "target_role": "primary_ground_truth_or_calibration_target",
            "source_evidence": "Header screenshots mark Sgh / NMR_SAT as GROUND TRUTH; refined sheets show Sgh tied to depth correspondence.",
            "allowed_use": "Target for hydrate saturation regression; possible source for occurrence labels only after an explicit threshold/uncertainty policy.",
            "prohibited_use": "Do not use as an input feature, normalization feature, ranking feature, or stability-screen predictor.",
            "leakage_policy": "exclude_from_feature_matrix_before_training",
            "current_public_status": "header_evidence_only_no_rows_committed",
            "unit_or_scale_status": "unresolved_fraction_or_percent",
            "future_resolution_needed": "Confirm workbook units, source method, depth alignment, and whether Sgh is supplied, interpreted, NMR-derived, or core-calibrated.",
            "notes": "Preserve original header spelling in deliverables and map to canonical role only as metadata.",
        },
        {
            "original_header": "S_h",
            "canonical_target_family": "hydrate_saturation",
            "target_task": "saturation_regression;occurrence_label_derivation_after_threshold_policy",
            "target_role": "target_or_calibration_reference",
            "source_evidence": "MTE screenshot shows S_h beside measured and derived log fields; science ladder says S_h is a target/calibration/output, not predictor.",
            "allowed_use": "Target or calibration reference for hydrate saturation; compare against predictions during validation.",
            "prohibited_use": "Do not use as an input feature or derive model features from it before splitting.",
            "leakage_policy": "exclude_from_feature_matrix_before_training",
            "current_public_status": "header_evidence_only_no_rows_committed",
            "unit_or_scale_status": "unresolved_fraction_or_percent",
            "future_resolution_needed": "Confirm whether S_h is interpreted, Archie-derived, NMR/core-calibrated, or supplied ground truth.",
            "notes": "Keep distinct from measured inputs even when it appears in the same sheet region.",
        },
        {
            "original_header": "Sh",
            "canonical_target_family": "hydrate_saturation",
            "target_task": "saturation_regression;occurrence_label_derivation_after_threshold_policy",
            "target_role": "target_or_calibration_reference",
            "source_evidence": "IGS screenshot shows Sh and Swr; base file lists Sh under label/target/ground-truth fields.",
            "allowed_use": "Target or calibration reference for hydrate saturation after workbook role confirmation.",
            "prohibited_use": "Do not use as an input feature, predictor, direct feature, or post-review ranking input.",
            "leakage_policy": "exclude_from_feature_matrix_before_training",
            "current_public_status": "header_evidence_only_no_rows_committed",
            "unit_or_scale_status": "unresolved_fraction_or_percent",
            "future_resolution_needed": "Confirm sheet-specific equivalence to Sgh/S_h and fraction 0-1 consistency.",
            "notes": "Header alias should be visible; do not silently rename it away.",
        },
        {
            "original_header": "NMR_SAT",
            "canonical_target_family": "hydrate_saturation",
            "target_task": "saturation_regression;occurrence_label_derivation_after_threshold_policy",
            "target_role": "ground_truth_or_independent_calibration_target",
            "source_evidence": "Header screenshot explicitly marks Sgh / NMR_SAT as GROUND TRUTH; science ladder separates NMRPHI input from NMR_SAT target.",
            "allowed_use": "Ground-truth, calibration, or validation target for saturation where available.",
            "prohibited_use": "Do not use as an input feature; do not confuse with measured NMR porosity/NMRPHI.",
            "leakage_policy": "exclude_from_feature_matrix_before_training",
            "current_public_status": "header_evidence_only_no_rows_committed",
            "unit_or_scale_status": "unresolved_fraction_or_percent",
            "future_resolution_needed": "Confirm NMR processing method, depth alignment, and whether NMR_SAT is the authoritative target for known wells.",
            "notes": "NMRPHI can be an input if measured; NMR_SAT is target-only.",
        },
        {
            "original_header": "Hydrate Saturation",
            "canonical_target_family": "hydrate_saturation",
            "target_task": "saturation_regression;occurrence_label_derivation_after_threshold_policy",
            "target_role": "target_or_reporting_output",
            "source_evidence": "Base file lists Hydrate Saturation under label/target/ground-truth fields.",
            "allowed_use": "Human-readable target/output field for saturation regression and validation reporting.",
            "prohibited_use": "Do not use as an input feature or leakage-bearing helper variable.",
            "leakage_policy": "exclude_from_feature_matrix_before_training",
            "current_public_status": "header_evidence_only_no_rows_committed",
            "unit_or_scale_status": "unresolved_fraction_or_percent",
            "future_resolution_needed": "Confirm relationship to Sgh/S_h/Sh and whether this is supplied or derived.",
            "notes": "This is the plain-language alias; preserve exact workbook header where present.",
        },
        {
            "original_header": "Swr",
            "canonical_target_family": "irreducible_or_residual_water_saturation",
            "target_task": "calibration_reference;water_saturation_constraint",
            "target_role": "target_or_calibration_reference_not_predictor",
            "source_evidence": "Base file lists Swr under label/target/ground-truth fields; MTE/IGS screenshots show S_wr/Swr near saturation fields.",
            "allowed_use": "Calibration/reference target for water saturation or hydrate-saturation equations after source role is confirmed.",
            "prohibited_use": "Do not use as an input feature when predicting hydrate saturation if it is target-derived or post-processed.",
            "leakage_policy": "exclude_until_workbook_formula_confirms_nonleakage_role",
            "current_public_status": "header_evidence_only_no_rows_committed",
            "unit_or_scale_status": "unresolved_fraction_or_percent",
            "future_resolution_needed": "Confirm whether Swr/S_wr is measured, assumed, interpreted, or calculated from target-bearing fields.",
            "notes": "Treat as target/calibration family by default because it is a saturation field.",
        },
        {
            "original_header": "S_wr",
            "canonical_target_family": "irreducible_or_residual_water_saturation",
            "target_task": "calibration_reference;water_saturation_constraint",
            "target_role": "target_or_calibration_reference_not_predictor",
            "source_evidence": "MTE screenshot shows S_wr beside measured and derived fields; unresolved question asks whether S_wr is measured, assumed, or calculated.",
            "allowed_use": "Calibration/reference target after workbook formula review.",
            "prohibited_use": "Do not use as an input feature until proven independent of target outputs and split-safe.",
            "leakage_policy": "exclude_until_workbook_formula_confirms_nonleakage_role",
            "current_public_status": "header_evidence_only_no_rows_committed",
            "unit_or_scale_status": "unresolved_fraction_or_percent",
            "future_resolution_needed": "Confirm formula/provenance and relationship to Swr and hydrate saturation.",
            "notes": "Kept as a separate original header because screenshots preserve this spelling.",
        },
        {
            "original_header": "interpreted phase label",
            "canonical_target_family": "hydrate_occurrence_or_phase_class",
            "target_task": "occurrence_classification",
            "target_role": "classification_target_after_label_policy",
            "source_evidence": "Science ladder says interpreted phase labels are targets, calibration references, or outputs, not predictors.",
            "allowed_use": "Target for occurrence/phase classification after label definitions and uncertainty classes are approved.",
            "prohibited_use": "Do not use final phase labels, manual rankings, or post-review decisions as predictors.",
            "leakage_policy": "exclude_from_feature_matrix_before_training",
            "current_public_status": "not_present_as_rows_in_public_repo",
            "unit_or_scale_status": "categorical_policy_unresolved",
            "future_resolution_needed": "Define hydrate/gas/water/non-reservoir/uncertain class policy and whole-well split handling.",
            "notes": "Occurrence labels may be derived from saturation targets only after threshold and uncertainty policy is approved.",
        },
    ]
    return pd.DataFrame(rows, columns=PUBLIC_ML_TARGET_REGISTRY_COLUMNS)


def public_ml_leakage_guardrails_frame() -> pd.DataFrame:
    target_headers = "Sgh;S_h;Sh;NMR_SAT;Hydrate Saturation;Swr;S_wr;interpreted phase label"
    rows = [
        {
            "guardrail_id": "LG-01",
            "pipeline_stage": "schema_mapping",
            "rule": "Preserve original saturation and label headers, then assign target-only role metadata.",
            "target_headers_covered": target_headers,
            "allowed_inputs": "Measured logs and public context fields only after unit/QC validation.",
            "blocked_inputs": target_headers,
            "reason": "The base file identifies these as label/target/ground-truth or saturation fields.",
            "implementation_status": "documented_public_registry",
        },
        {
            "guardrail_id": "LG-02",
            "pipeline_stage": "feature_engineering",
            "rule": "Do not derive predictor features from hydrate saturation, water saturation, interpreted class, or final ranking fields.",
            "target_headers_covered": target_headers,
            "allowed_inputs": "GR, Rt, RHOB, porosity inputs, Vp, Vs, caliper/QC, public stability context, and source-control metadata.",
            "blocked_inputs": target_headers,
            "reason": "Target-derived predictors would create leakage and inflate model performance.",
            "implementation_status": "planned_runtime_check",
        },
        {
            "guardrail_id": "LG-03",
            "pipeline_stage": "train_validation_split",
            "rule": "Split by whole well before fitting preprocessing, thresholds, scalers, or model weights.",
            "target_headers_covered": target_headers,
            "allowed_inputs": "Training-well features only for fitting transforms.",
            "blocked_inputs": "Validation/test target distributions during transform fitting.",
            "reason": "Neighboring depth rows within the same well are correlated; random row splits can leak target behavior.",
            "implementation_status": "runtime_skeleton_exists",
        },
        {
            "guardrail_id": "LG-04",
            "pipeline_stage": "occurrence_label_derivation",
            "rule": "Occurrence labels may be derived from saturation targets only after an explicit threshold, uncertainty, and class policy is approved.",
            "target_headers_covered": "Sgh;S_h;Sh;NMR_SAT;Hydrate Saturation",
            "allowed_inputs": "Approved target registry and mentor-approved threshold policy.",
            "blocked_inputs": "Ad hoc hydrate-present labels from stability screen, resistivity alone, or manual sweet-spot rank.",
            "reason": "Stability and high resistivity are not direct hydrate labels.",
            "implementation_status": "policy_pending",
        },
        {
            "guardrail_id": "LG-05",
            "pipeline_stage": "public_exports",
            "rule": "Public GitHub/Streamlit exports may show schemas, target roles, counts, and guardrails, but not approved target rows.",
            "target_headers_covered": target_headers,
            "allowed_inputs": "Public-safe summaries and empty/schema-level target registry.",
            "blocked_inputs": "Approved target values, restricted well identifiers, fitted model results, and final metrics.",
            "reason": "Approved well-log/core data belongs only in the authorized runtime environment.",
            "implementation_status": "active_public_boundary",
        },
    ]
    return pd.DataFrame(rows, columns=PUBLIC_ML_LEAKAGE_GUARDRAIL_COLUMNS)


def load_public_ml_feature_scaffold(project_root: Path) -> pd.DataFrame:
    path = default_public_ml_feature_scaffold_path(project_root)
    if not path.exists():
        return pd.DataFrame(columns=PUBLIC_ML_FEATURE_SCAFFOLD_COLUMNS)
    return pd.read_csv(path)


def load_public_ml_feature_scaffold_summary(project_root: Path) -> pd.DataFrame:
    path = default_public_ml_feature_scaffold_summary_path(project_root)
    if not path.exists():
        return pd.DataFrame(columns=["metric", "value", "meaning"])
    return pd.read_csv(path)


def load_public_ml_feature_dictionary(project_root: Path) -> pd.DataFrame:
    path = default_public_ml_feature_dictionary_path(project_root)
    if not path.exists():
        return pd.DataFrame(columns=PUBLIC_ML_FEATURE_DICTIONARY_COLUMNS)
    return pd.read_csv(path)


def load_public_ml_target_registry(project_root: Path) -> pd.DataFrame:
    path = default_public_ml_target_registry_path(project_root)
    if not path.exists():
        return pd.DataFrame(columns=PUBLIC_ML_TARGET_REGISTRY_COLUMNS)
    return pd.read_csv(path)


def load_public_ml_leakage_guardrails(project_root: Path) -> pd.DataFrame:
    path = default_public_ml_leakage_guardrails_path(project_root)
    if not path.exists():
        return pd.DataFrame(columns=PUBLIC_ML_LEAKAGE_GUARDRAIL_COLUMNS)
    return pd.read_csv(path)


def load_approved_schema_coverage_matrix(project_root: Path) -> pd.DataFrame:
    path = default_approved_schema_coverage_matrix_path(project_root)
    if not path.exists():
        return pd.DataFrame(columns=APPROVED_SCHEMA_COVERAGE_MATRIX_COLUMNS)
    return pd.read_csv(path)


def write_public_ml_feature_products(project_root: Path) -> tuple[Path, Path, Path]:
    product_dir = default_stability_products_dir(project_root)
    product_dir.mkdir(parents=True, exist_ok=True)

    scaffold = build_public_ml_feature_scaffold(project_root)
    summary = public_ml_feature_scaffold_summary_frame(scaffold)
    dictionary = public_ml_feature_dictionary_frame()

    scaffold_path = default_public_ml_feature_scaffold_path(project_root)
    summary_path = default_public_ml_feature_scaffold_summary_path(project_root)
    dictionary_path = default_public_ml_feature_dictionary_path(project_root)
    scaffold.to_csv(scaffold_path, index=False)
    summary.to_csv(summary_path, index=False)
    dictionary.to_csv(dictionary_path, index=False)
    return scaffold_path, summary_path, dictionary_path


def write_public_ml_target_registry_products(project_root: Path) -> tuple[Path, Path]:
    product_dir = default_stability_products_dir(project_root)
    product_dir.mkdir(parents=True, exist_ok=True)

    registry = public_ml_target_registry_frame()
    guardrails = public_ml_leakage_guardrails_frame()
    registry_path = default_public_ml_target_registry_path(project_root)
    guardrails_path = default_public_ml_leakage_guardrails_path(project_root)
    registry.to_csv(registry_path, index=False)
    guardrails.to_csv(guardrails_path, index=False)
    return registry_path, guardrails_path


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


def _base_screen_row(row: pd.Series) -> dict[str, object]:
    tvd_m = pd.to_numeric(row.get("depth_basis_m"), errors="coerce")
    return {
        "screen_run_id": STABILITY_SCREEN_RUN_ID,
        "screen_version": STABILITY_SCREEN_VERSION,
        "object_id": row.get("object_id"),
        "permit_number": row.get("permit_number"),
        "api_number": row.get("api_number"),
        "well_name": row.get("well_name"),
        "field": row.get("field"),
        "pool": row.get("pool"),
        "lat": row.get("wellhead_latitude"),
        "lon": row.get("wellhead_longitude"),
        "tvd_m": tvd_m,
        "depth_source": row.get("depth_basis"),
        "depth_basis_ft": np.nan,
        "depth_reference_note": "Public DNR depth field; TrueVertic preferred and DrillerTot fallback is caveated.",
        "hydrate_assessment_codes": row.get("hydrate_assessment_codes"),
        "within_hydrate_assessment_unit": row.get("within_hydrate_assessment_unit"),
        "permafrost_base_m": row.get("nearest_permafrost_depth_m"),
        "permafrost_source": "GGD223 nearest point control",
        "permafrost_control_code": row.get("nearest_ggd223_code"),
        "permafrost_control_distance_km": row.get("nearest_ggd223_distance_km"),
        "permafrost_confidence": "permafrost_point_control_only",
        "temperature_model_id": TEMPERATURE_MODEL_ID,
        "temperature_source": row.get("temperature_profile_link_method"),
        "temperature_profile_code": row.get("nearest_temperature_profile_code"),
        "temperature_profile_file": row.get("nearest_temperature_profile_file"),
        "temperature_profile_max_depth_m": row.get("temperature_profile_max_depth_m"),
        "temperature_gradient_c_per_100m": row.get("rough_geothermal_gradient_c_per_100m"),
        "temperature_gradient_source": "deepest_window_g10015_inventory",
        "temperature_extrapolated_below_profile": False,
        "temperature_extrapolation_below_profile_m": 0.0,
        "temperature_model_confidence": "blocked_missing_inputs",
        "pressure_model_id": "hydrostatic_freshwater_surface_absolute_v1",
        "pressure_source": "hydrostatic_assumption",
        "pore_fluid_density_kg_m3": 1000.0,
        "gravity_m_s2": 9.80665,
        "surface_pressure_mpa": SURFACE_PRESSURE_MPA,
        "pressure_gradient_mpa_per_m": HYDROSTATIC_PRESSURE_MPA_PER_M,
        "pressure_at_tvd_mpa_absolute": hydrostatic_pressure_mpa_absolute(tvd_m),
        "phase_curve_id": PHASE_CURVE_ID,
        "phase_curve_role": PHASE_CURVE_ROLE,
        "phase_curve_allowed_use": PHASE_CURVE_ALLOWED_USE,
        "phase_curve_source": "USGS SIR 2008-5175 Figure 1A digitized methane 5 ppt lookup",
        "gas_composition_assumption": PHASE_CURVE_GAS_COMPOSITION_ASSUMPTION,
        "gas_methane_mol_pct": PHASE_CURVE_GAS_METHANE_MOL_PCT,
        "gas_ethane_mol_pct": PHASE_CURVE_GAS_ETHANE_MOL_PCT,
        "gas_propane_mol_pct": PHASE_CURVE_GAS_PROPANE_MOL_PCT,
        "gas_butane_plus_mol_pct": PHASE_CURVE_GAS_BUTANE_PLUS_MOL_PCT,
        "salinity_ppt_assumption": PHASE_CURVE_SALINITY_PPT,
        "phase_curve_status": "not_applied",
        "stable_depth_grid_step_m": np.nan,
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
        "stability_result_status": "blocked_missing_inputs",
        "stability_confidence": "blocked_missing_inputs",
        "caveat_codes": "hydrostatic_pressure_assumed;phase_curve_methane_5ppt;permafrost_point_control_only;om222_not_digitized;not_hydrate_proof",
        "stability_notes": "Blocked until required public pressure-temperature inputs pass the calculation gates.",
    }


def _blocked_screen_row(row: pd.Series, status: str, notes: str) -> dict[str, object]:
    output = _base_screen_row(row)
    output["stability_result_status"] = status
    if status == "outside_au_context":
        output["stability_confidence"] = "outside_public_au_context"
        output["caveat_codes"] = f"{output['caveat_codes']};outside_usgs_hydrate_au"
    elif "temperature" in status:
        output["caveat_codes"] = f"{output['caveat_codes']};temperature_profile_missing"
    output["stability_notes"] = notes
    return output


def build_stability_screen(
    project_root: Path,
    source_root: Path | None = None,
    grid_step_m: object = DEFAULT_STABILITY_DEPTH_GRID_STEP_M,
) -> pd.DataFrame:
    scaffold = load_stability_input_scaffold(project_root)
    if scaffold.empty:
        return pd.DataFrame(columns=STABILITY_SCREEN_COLUMNS)

    phase_curve = load_methane_phase_curve(project_root)
    if phase_curve.empty:
        rows = [
            _blocked_screen_row(
                row,
                "blocked_missing_phase_curve",
                "Blocked because the baseline methane phase-curve lookup is missing.",
            )
            for _, row in scaffold.iterrows()
        ]
        return pd.DataFrame(rows, columns=STABILITY_SCREEN_COLUMNS)

    active_source = Path(source_root) if source_root is not None else active_stability_source_path(project_root)
    profile_cache: dict[str, pd.DataFrame] = {}
    curve_depth_start_m = phase_curve_min_depth_m(phase_curve)
    curve_depth_limit_m = phase_curve_max_depth_m(phase_curve)
    rows: list[dict[str, object]] = []
    for _, row in scaffold.iterrows():
        if not bool(row.get("within_hydrate_assessment_unit")):
            rows.append(
                _blocked_screen_row(
                    row,
                    "outside_au_context",
                    "Outside current public USGS hydrate assessment unit context.",
                )
            )
            continue

        depth_m = pd.to_numeric(row.get("depth_basis_m"), errors="coerce")
        if not np.isfinite(depth_m) or depth_m <= 0:
            rows.append(
                _blocked_screen_row(
                    row,
                    "blocked_missing_depth",
                    "Blocked because no usable public vertical-depth basis is available.",
                )
            )
            continue

        if row.get("stability_input_readiness") != "ready_for_phase_curve_inputs":
            rows.append(
                _blocked_screen_row(
                    row,
                    "blocked_missing_temperature_profile",
                    "Blocked because the well lacks a matched G10015 temperature profile.",
                )
            )
            continue

        if np.isfinite(curve_depth_start_m) and depth_m < curve_depth_start_m:
            blocked = _blocked_screen_row(
                row,
                "blocked_phase_curve_range_insufficient",
                "Blocked because the public well depth is shallower than the cited phase-curve lookup range.",
            )
            blocked["phase_curve_status"] = "blocked_phase_curve_range_insufficient"
            rows.append(blocked)
            continue

        profile_points = _profile_points_from_source(
            active_source,
            row.get("nearest_temperature_profile_file"),
            profile_cache,
        )
        if profile_points.empty:
            rows.append(
                _blocked_screen_row(
                    row,
                    "blocked_missing_temperature_profile_rows",
                    "Blocked because the matched raw G10015 profile rows are unavailable in this runtime.",
                )
            )
            continue

        gradient = pd.to_numeric(row.get("rough_geothermal_gradient_c_per_100m"), errors="coerce")
        if not np.isfinite(gradient):
            gradient = None
        range_truncated = np.isfinite(curve_depth_limit_m) and depth_m > curve_depth_limit_m
        model_depth_limit_m = min(depth_m, curve_depth_limit_m) if range_truncated else depth_m
        condition_grid = stability_condition_grid_from_profile(
            profile_points,
            phase_curve,
            depth_limit_m=model_depth_limit_m,
            gradient_c_per_100m=gradient,
            step_m=grid_step_m,
            start_depth_m=curve_depth_start_m,
        )
        interval = stability_interval_from_condition_grid(
            condition_grid,
            depth_limit_m=model_depth_limit_m,
            step_m=grid_step_m,
        )

        if range_truncated and not (
            interval["stability_result_status"] == "calculated"
            and interval["base_boundary_method"] == "interpolated_crossing"
        ):
            blocked = _blocked_screen_row(
                row,
                "blocked_phase_curve_range_insufficient",
                "Blocked because the modeled interval does not close within the cited phase-curve lookup range.",
            )
            blocked["phase_curve_status"] = "blocked_phase_curve_range_insufficient"
            rows.append(blocked)
            continue

        output = _base_screen_row(row)
        output.update(interval.to_dict())
        output["phase_curve_status"] = "applied"
        temperature_status = "calculated"
        if interval["stability_result_status"].startswith("blocked"):
            temperature_status = str(condition_grid["temperature_model_status"].iloc[0])
        label_input = {
            **output,
            "depth_basis": row.get("depth_basis"),
            "phase_curve_status": output["phase_curve_status"],
            "phase_curve_allowed_use": PHASE_CURVE_ALLOWED_USE,
            "temperature_model_status": temperature_status,
            "stability_result_status": output["stability_result_status"],
            "temperature_control_distance_km": row.get("nearest_ggd223_distance_km"),
            "within_hydrate_assessment_unit": row.get("within_hydrate_assessment_unit"),
        }
        confidence = stability_source_control_label(label_input)
        output["temperature_model_confidence"] = confidence
        output["stability_confidence"] = confidence
        output["caveat_codes"] = (
            f"{output['caveat_codes']};permafrost_point_control_only;om222_not_digitized"
        )
        if row.get("depth_basis") == "DrillerTot":
            output["caveat_codes"] = f"{output['caveat_codes']};driller_total_depth_fallback"
        if output["stability_result_status"] == "calculated":
            output["stability_notes"] = (
                "Baseline public methane 5 ppt stability-admissibility screen only; "
                "not hydrate proof or saturation."
            )
        elif output["stability_result_status"] == "calculated_no_stable_interval":
            output["stability_notes"] = (
                "Inputs were sufficient for the baseline public screen, but no stable "
                "interval was found in the modeled depth range."
            )
        else:
            output["stability_notes"] = (
                "Blocked because the pressure-temperature grid did not pass all calculation gates."
            )
        rows.append(output)

    return pd.DataFrame(rows, columns=STABILITY_SCREEN_COLUMNS)


def stability_screen_summary_frame(screen: pd.DataFrame) -> pd.DataFrame:
    if screen.empty:
        return pd.DataFrame(columns=["metric", "value", "meaning"])

    calculated = screen["stability_result_status"].eq("calculated")
    rows = [
        {
            "metric": "Screen rows",
            "value": int(len(screen)),
            "meaning": "One row per public scaffold well for the baseline methane 5 ppt run.",
        },
        {
            "metric": "Calculated stability intervals",
            "value": int(calculated.sum()),
            "meaning": "Rows with non-null baseline top/base/thickness after all gates passed.",
        },
        {
            "metric": "No stable interval found",
            "value": int(screen["stability_result_status"].eq("calculated_no_stable_interval").sum()),
            "meaning": "Rows where inputs were sufficient but the modeled interval was not stable.",
        },
        {
            "metric": "Blocked rows",
            "value": int((~screen["stability_result_status"].isin(["calculated", "calculated_no_stable_interval"])).sum()),
            "meaning": "Rows left null because at least one source or calculation gate did not pass.",
        },
        {
            "metric": "Not hydrate proof",
            "value": int(len(screen)),
            "meaning": "Every row remains a stability-admissibility screen, not occurrence or saturation evidence.",
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


def write_g10015_temperature_profile_points_product(
    project_root: Path,
    source_root: Path | None = None,
    max_points_per_profile: int = 160,
) -> tuple[Path, Path] | tuple[None, None]:
    active_source = Path(source_root) if source_root is not None else active_stability_source_path(project_root)
    profile_dir = active_source / G10015_RELATIVE_PATH
    if not profile_dir.exists() or not any(profile_dir.glob("*.txt")):
        return None, None

    points = build_g10015_temperature_profile_points_product(
        active_source,
        max_points_per_profile=max_points_per_profile,
    )
    if points.empty:
        return None, None

    product_dir = default_stability_products_dir(project_root)
    product_dir.mkdir(parents=True, exist_ok=True)
    points_summary = g10015_temperature_profile_points_summary_frame(points)
    points_path = default_g10015_profile_points_path(project_root)
    points_summary_path = default_g10015_profile_points_summary_path(project_root)
    points.to_csv(points_path, index=False)
    points_summary.to_csv(points_summary_path, index=False)
    return points_path, points_summary_path


def write_stability_screen_product(
    project_root: Path,
    source_root: Path | None = None,
) -> tuple[Path, Path] | tuple[None, None]:
    active_source = Path(source_root) if source_root is not None else active_stability_source_path(project_root)
    profile_dir = active_source / G10015_RELATIVE_PATH
    if not profile_dir.exists() or not any(profile_dir.glob("*.txt")):
        return None, None

    screen = build_stability_screen(project_root, active_source)
    if screen.empty:
        return None, None

    product_dir = default_stability_products_dir(project_root)
    product_dir.mkdir(parents=True, exist_ok=True)
    screen_summary = stability_screen_summary_frame(screen)
    screen_path = default_stability_screen_path(project_root)
    screen_summary_path = default_stability_screen_summary_path(project_root)
    screen.to_csv(screen_path, index=False)
    screen_summary.to_csv(screen_summary_path, index=False)
    return screen_path, screen_summary_path


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
