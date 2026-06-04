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
    "dt_us_ft",
    "dts_us_ft",
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
        "well_alias": ("well_alias", "WELL", "WELL_NAME", "UWI", "API"),
        "depth_m": ("depth_m", "DEPTH_M", "DEPTH", "MD", "MD_M", "TVD", "TVD_M"),
        "gr_api": ("gr_api", "GR", "GAMMA", "GAMMA_RAY"),
        "rt_ohm_m": ("rt_ohm_m", "RT", "ILD", "RDEP", "RES_DEEP"),
        "rhob_g_cc": ("rhob_g_cc", "RHOB", "DEN", "DENSITY"),
        "dt_us_ft": ("dt_us_ft", "DT", "DTC", "AC"),
        "dts_us_ft": ("dts_us_ft", "DTS", "DTSM"),
        "nmr_porosity_vv": ("nmr_porosity_vv", "NMRPHI", "TCMR", "CMRP"),
        "caliper_in": ("caliper_in", "CALI", "CALIPER"),
        "temperature_c": ("temperature_c", "TEMP", "TEMPERATURE_C"),
        "pressure_mpa": ("pressure_mpa", "PRESSURE", "PRESSURE_MPA", "PP_MPA"),
    }


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
