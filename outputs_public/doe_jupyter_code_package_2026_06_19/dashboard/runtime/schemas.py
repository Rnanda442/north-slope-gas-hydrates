from __future__ import annotations

from dataclasses import dataclass, field


SYNTHETIC_INPUT_MODE = "synthetic"
APPROVED_INPUT_MODE = "approved_local_runtime"

REQUIRED_LOG_COLUMNS = (
    "well_alias",
    "depth_m",
    "gr_api",
    "rt_ohm_m",
    "rhob_g_cc",
)

OPTIONAL_LOG_COLUMNS = (
    "density_porosity_vv",
    "neutron_porosity_vv",
    "dt_us_ft",
    "dts_us_ft",
    "vp_km_s",
    "vs_km_s",
    "vp_m_s",
    "vs_m_s",
    "nmr_porosity_vv",
    "caliper_in",
    "temperature_c",
    "pressure_mpa",
)

REQUIRED_CORE_COLUMNS = (
    "well_alias",
    "sample_depth_m",
)

OPTIONAL_CORE_COLUMNS = (
    "porosity_vv",
    "permeability_md",
    "hydrate_saturation_vv",
    "lithology",
    "core_quality",
)

CHONG_ML_FEATURE_COLUMNS = (
    "rhob_g_cc",
    "density_porosity_vv",
    "rt_ohm_m",
    "gr_api",
    "vp_km_s",
    "vs_km_s",
)

TARGET_LABEL_CONTRACT = (
    {
        "Target": "Hydrate saturation regression",
        "Preferred source": "Supplied or core-calibrated hydrate saturation from known wells",
        "Alternatives": "Documented multi-method interpreted saturation; NMR-density saturation where available",
        "Do not use as inputs": "Any saturation target, interpreted class, or target-derived column",
        "Status before workbook": "Required; exact source unconfirmed",
    },
    {
        "Target": "Phase classification",
        "Preferred source": "Known-well interval labels for hydrate / gas / water / non-reservoir",
        "Alternatives": "Core-supported interval interpretation",
        "Do not use as inputs": "Final phase labels or manual sweet-spot rankings",
        "Status before workbook": "Required; exact label column unconfirmed",
    },
    {
        "Target": "Sweet-spot ranking",
        "Preferred source": "Separate decision target combining occurrence confidence and reservoir quality",
        "Alternatives": "Expert-review priority with explicit reasons",
        "Do not use as inputs": "Final ranking, producibility outcome, or post-review decision",
        "Status before workbook": "Planning only",
    },
)

PROJECT_COHORT_ASSUMPTIONS = {
    "Estimated total wells": 71,
    "Known development fraction": 0.20,
    "Prediction fraction": 0.80,
    "Expected NMR": "Yes",
    "Primary outputs": "Phase classification and continuous hydrate saturation",
    "Feature strategy": "Normalized multivariable logs and physics-derived features; transformations fit on training wells only and weights learned or calibrated, not assumed",
}

TARGET_ONLY_COLUMN_ALIASES = {
    "hydrate_saturation": (
        "Sgh",
        "S_h",
        "Sh",
        "NMR_SAT",
        "Hydrate Saturation",
        "hydrate_saturation_vv",
    ),
    "irreducible_or_residual_water_saturation": (
        "Swr",
        "S_wr",
        "irreducible_water_saturation_vv",
    ),
    "phase_or_occurrence_label": (
        "interpreted phase label",
        "phase_label",
        "hydrate_phase",
        "hydrate_occurrence_label",
        "runtime_phase_label",
    ),
}


@dataclass(frozen=True)
class RuntimeConfig:
    input_mode: str = SYNTHETIC_INPUT_MODE
    approved_csv_paths: tuple[str, ...] = ()
    approved_las_paths: tuple[str, ...] = ()
    core_csv_paths: tuple[str, ...] = ()
    output_root: str = "outputs_runtime"
    model_root: str = "models_runtime"
    curve_aliases: dict[str, tuple[str, ...]] = field(default_factory=dict)


def default_curve_aliases() -> dict[str, tuple[str, ...]]:
    return {
        "well_alias": ("well_alias", "WELL", "WELL_NAME", "Well Name", "UWI", "API"),
        "depth_m": ("depth_m", "DEPTH_M", "DEPTH", "MD", "MD_M", "TVD", "TVD_M"),
        "gr_api": ("gr_api", "GR", "GAMMA", "GAMMA_RAY", "Gamma Ray"),
        "rt_ohm_m": ("rt_ohm_m", "RT", "ILD", "RDEP", "RES", "RES_DEEP", "Deep formation resistivity"),
        "rhob_g_cc": ("rhob_g_cc", "RHOB", "DEN", "DENSITY", "Rho_b", "Density_gcpcc", "Density_gpcc"),
        "density_porosity_vv": ("density_porosity_vv", "DPHI", "PHID", "DEN_POR", "Phi_porosity", "phi_den"),
        "neutron_porosity_vv": ("neutron_porosity_vv", "NPHI", "TNPH", "NEUTRON_POR", "phi_neut"),
        "dt_us_ft": ("dt_us_ft", "DT", "DTC", "AC"),
        "dts_us_ft": ("dts_us_ft", "DTS", "DTSM"),
        "vp_km_s": ("vp_km_s", "VP_KM_S"),
        "vs_km_s": ("vs_km_s", "VS_KM_S"),
        "vp_m_s": ("vp_m_s", "Vp", "VP", "VELP", "VP_M_S"),
        "vs_m_s": ("vs_m_s", "Vs", "VS", "VS1", "VELS", "VS_M_S"),
        "nmr_porosity_vv": ("nmr_porosity_vv", "NMRPHI", "TCMR", "CMRP", "phi_nmr"),
        "caliper_in": ("caliper_in", "CALI", "CALIPER", "caliper", "CAL1"),
        "temperature_c": ("temperature_c", "TEMP", "TEMPERATURE_C"),
        "pressure_mpa": ("pressure_mpa", "PRESSURE", "PRESSURE_MPA", "PP_MPA"),
    }


def target_only_column_aliases() -> dict[str, tuple[str, ...]]:
    return TARGET_ONLY_COLUMN_ALIASES


@dataclass(frozen=True)
class ValidationIssue:
    severity: str
    column: str
    message: str


@dataclass(frozen=True)
class RuntimeReadinessReport:
    status: str
    rows: int
    wells: int
    issues: tuple[ValidationIssue, ...]

    @property
    def is_ready(self) -> bool:
        return self.status == "ready"
