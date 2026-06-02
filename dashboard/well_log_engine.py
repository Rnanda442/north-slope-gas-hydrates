from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
from typing import Iterable

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


SYNTHETIC_LABEL = "SYNTHETIC DEMONSTRATION DATA"

VARIABLES = {
    "gr_api": ("GR", "API"),
    "rt_ohm_m": ("Resistivity Rt", "ohm m"),
    "rhob_g_cc": ("RHOB", "g/cc"),
    "density_porosity_vv": ("Density porosity", "v/v"),
    "dt_us_ft": ("DT", "us/ft"),
    "vp_km_s": ("Vp", "km/s"),
    "dts_us_ft": ("DTS", "us/ft"),
    "vs_km_s": ("Vs", "km/s"),
    "vp_vs_ratio": ("Vp/Vs", "ratio"),
    "lambda_rho": ("lambda-rho", "GPa g/cc"),
    "mu_rho": ("mu-rho", "GPa g/cc"),
    "nmr_porosity_vv": ("NMR porosity", "v/v"),
    "nmr_density_separation_vv": ("NMR-density separation", "v/v"),
    "caliper_in": ("Caliper", "in"),
    "temperature_c": ("Temperature", "deg C"),
    "pressure_mpa": ("Pressure", "MPa"),
    "archie_hydrate_proxy": ("Archie hydrate proxy", "fraction"),
    "nmr_density_hydrate_proxy": ("NMR-density hydrate proxy", "fraction"),
}

RANGE_GUIDE = [
    {
        "Variable": "GR",
        "Unit": "API",
        "Working tendency or screening range": "Lower GR supports a cleaner sand screen; use local clean/shale anchors.",
        "Why it may support interpretation": "GR helps distinguish reservoir-grade sand from shale-rich intervals before phase interpretation.",
        "Competing explanations": "Bentonitic shale, radioactive sand, coal, and local facies variation.",
        "Required supporting evidence": "RHOB/porosity, borehole QC, depositional context, and multi-log phase evidence.",
        "Uncertainty warning": "Use as a lithology filter, never as a hydrate indicator.",
        "Manuscript source": "Section 8; Tables 8.A7, 8.A10, A.1",
    },
    {
        "Variable": "Rt",
        "Unit": "ohm m",
        "Working tendency or screening range": "Hydrate sand working anchor about 10-100+; water sand about 1-5.",
        "Why it may support interpretation": "Pore-filling hydrate can reduce conductive water connectivity and increase resistivity.",
        "Competing explanations": "Gas, low porosity, clay effects, carbonate, coal/lignite, and ice-bearing sediment.",
        "Required supporting evidence": "Sonic, density/porosity, lithology, NMR where available, and P-T context.",
        "Uncertainty warning": "High Rt alone is evidence, not a hydrate label. Archie is a supplementary cross-check.",
        "Manuscript source": "Sections 8, 13; Tables 8.A6, 13.A2, A.1",
    },
    {
        "Variable": "RHOB",
        "Unit": "g/cc",
        "Working tendency or screening range": "Hydrate sand working anchor about 2.00-2.30; water sand about 2.10-2.40.",
        "Why it may support interpretation": "Density supports porosity and storage-capacity estimation and can show modest hydrate-related reduction.",
        "Competing explanations": "Gas, ice-bearing sediment, coal/lignite, washout, and lithology changes.",
        "Required supporting evidence": "Caliper/borehole QC, GR, sonic, porosity consistency, and local matrix assumptions.",
        "Uncertainty warning": "Bad-hole density response must be flagged before interpretation.",
        "Manuscript source": "Section 8; Tables 8.A7, 8.A12, A.1",
    },
    {
        "Variable": "Porosity",
        "Unit": "fraction",
        "Working tendency or screening range": "Hydrate sand working anchor about 0.20-0.35; interpret capacity separately from occupancy.",
        "Why it may support interpretation": "Porosity describes storage capacity and supports density/NMR saturation transforms.",
        "Competing explanations": "Shale correction, matrix choice, gas effect, washout, and thin-bed averaging.",
        "Required supporting evidence": "GR, RHOB QC, NMR where available, and local calibration.",
        "Uncertainty warning": "Good reservoir sand can contain no hydrate.",
        "Manuscript source": "Sections 3, 8; Tables 8.A7, A.1",
    },
    {
        "Variable": "Vp",
        "Unit": "km/s",
        "Working tendency or screening range": "Hydrate sand working anchor about 2.5-4.0; gas sand about 1.5-2.5.",
        "Why it may support interpretation": "Hydrate frame stiffening can increase compressional velocity; gas tends to soften the response.",
        "Competing explanations": "Stress, cementation, ice-bearing sediment, carbonate, and competent clastics.",
        "Required supporting evidence": "Vs, RHOB, GR/lithology, stress context, and P-T screen.",
        "Uncertainty warning": "Velocity anomalies require stress and lithology review.",
        "Manuscript source": "Section 7; Tables 7.A1, 7.A7, A.1",
    },
    {
        "Variable": "Vs",
        "Unit": "km/s",
        "Working tendency or screening range": "Hydrate sand working anchor about 1.0-2.5; gas sand about 0.3-1.0.",
        "Why it may support interpretation": "Shear response helps identify rigidity increase and separate hydrate from gas-related compressibility.",
        "Competing explanations": "Stress, ice-bearing sediment, competent lithology, and missing or unreliable DTS.",
        "Required supporting evidence": "Vp, density, GR/lithology, tool QC, and depth context.",
        "Uncertainty warning": "Treat missing DTS as an explicit routing state.",
        "Manuscript source": "Section 7; Tables 7.A1, 12.A7, A.1",
    },
    {
        "Variable": "Vp/Vs",
        "Unit": "ratio",
        "Working tendency or screening range": "Hydrate sand working anchor about 1.6-2.4; use only as a crossplot tendency.",
        "Why it may support interpretation": "The ratio combines compressional and shear behavior for phase discrimination.",
        "Competing explanations": "Stress, lithology, ice-bearing sediment, and tool mismatch.",
        "Required supporting evidence": "Vp, Vs, RHOB, GR/lithology, and QC.",
        "Uncertainty warning": "Do not convert an overlapping ratio range into a universal threshold.",
        "Manuscript source": "Section 7; Tables 7.A2, A.2, A.3",
    },
    {
        "Variable": "lambda-rho",
        "Unit": "GPa g/cc",
        "Working tendency or screening range": "Hydrate sand working anchor about 12-55 in Table A.2; end-member crossplots require local calibration.",
        "Why it may support interpretation": "Lambda-rho helps characterize compressibility and fluid-sensitive elastic behavior.",
        "Competing explanations": "Gas, shale, carbonates, stress, and mixed intervals.",
        "Required supporting evidence": "mu-rho, Vp/Vs, GR, RHOB, and local core/log review.",
        "Uncertainty warning": "Appendix end-member tables overlap; use a multi-attribute view.",
        "Manuscript source": "Section 7.3; Tables 7.A2, A.2, A.3",
    },
    {
        "Variable": "mu-rho",
        "Unit": "GPa g/cc",
        "Working tendency or screening range": "Hydrate sand working anchor about 10-55; gas sand about 1-10.",
        "Why it may support interpretation": "Rigidity increase is a useful hydrate-supportive tendency when shear data are reliable.",
        "Competing explanations": "Ice-bearing sediment, shale, carbonates, competent sand, and stress.",
        "Required supporting evidence": "lambda-rho, Vp/Vs, GR/lithology, depth relative to permafrost, and P-T context.",
        "Uncertainty warning": "Ice-bearing sediment can overlap hydrate.",
        "Manuscript source": "Section 7.3; Tables 7.A2, A.2, A.3",
    },
    {
        "Variable": "NMR-density separation",
        "Unit": "fraction",
        "Working tendency or screening range": "Positive density-minus-NMR porosity separation supports a mobile-fluid-deficit screen.",
        "Why it may support interpretation": "The manuscript prefers NMR-density saturation where NMR exists.",
        "Competing explanations": "Tool quality, depth mismatch, shale response, and matrix assumptions.",
        "Required supporting evidence": "Density QC, local depth alignment, GR/lithology, and core calibration.",
        "Uncertainty warning": "NMR coverage is optional; absence must remain visible.",
        "Manuscript source": "Section 8; Tables 8.A4, 8.A7, 12.A6",
    },
    {
        "Variable": "Temperature",
        "Unit": "deg C",
        "Working tendency or screening range": "Use local T(z); North Slope example anchor starts near -10 deg C with 2.0-4.0 deg C/100 m gradients.",
        "Why it may support interpretation": "Temperature is required for probabilistic stability admissibility.",
        "Competing explanations": "Local thermal anomalies, uncertain gradient, and non-equilibrium behavior.",
        "Required supporting evidence": "Pressure, depth reference, permafrost depth, and local thermal calibration.",
        "Uncertainty warning": "GHSZ is necessary but not sufficient.",
        "Manuscript source": "Section 6; Tables 6.A1, A.4",
    },
    {
        "Variable": "Pressure",
        "Unit": "MPa",
        "Working tendency or screening range": "Use local P(z); first-pass hydrostatic anchor about 9.795 kPa/m.",
        "Why it may support interpretation": "Pressure combines with temperature to define stability admissibility.",
        "Competing explanations": "Pressure anomalies, compositional effects, local stress, and uncertain depth reference.",
        "Required supporting evidence": "Temperature, depth reference, local pressure observations, and uncertainty bounds.",
        "Uncertainty warning": "P-T screening is probabilistic, not an absolute classifier.",
        "Manuscript source": "Section 6; Tables 6.A1, A.4",
    },
    {
        "Variable": "GHSZ context",
        "Unit": "categorical",
        "Working tendency or screening range": "Stable / marginal / outside working screen.",
        "Why it may support interpretation": "The screen defines where hydrate can physically exist.",
        "Competing explanations": "Stable but uncharged sand, leakage, bypass, local anomalies, and partial fill.",
        "Required supporting evidence": "Direct logs, reservoir quality, charge/localization context, and core calibration.",
        "Uncertainty warning": "Stability is necessary but not sufficient.",
        "Manuscript source": "Sections 3, 6, 13; Tables 6.A1, 13.A1",
    },
]

SWEET_SPOT_GUIDE = [
    {
        "Planning band": "Admissibility only",
        "Synthetic saturation-proxy range": "Any",
        "Use": "Confirm that the interval is inside a probabilistic GHSZ screen.",
        "Scientific anchor": "GHSZ is necessary but not sufficient.",
        "Required confirmation": "Reservoir quality, multi-log phase evidence, and local calibration.",
    },
    {
        "Planning band": "Occupancy / expert review",
        "Synthetic saturation-proxy range": "< 0.35",
        "Use": "Preserve low-to-moderate occupancy, thin-bed averaging, and ambiguous responses for review.",
        "Scientific anchor": "The manuscript warns that thin strong hydrate beds can average into modest apparent saturation.",
        "Required confirmation": "Vertical-resolution review, NMR where available, sonic, Rt, and core depth match.",
    },
    {
        "Planning band": "Candidate sweet-spot review lane",
        "Synthetic saturation-proxy range": "0.35-0.60",
        "Use": "Flag a moderate-saturation interval for production-oriented review when reservoir quality and QC remain favorable.",
        "Scientific anchor": "Manuscript load-bearing transition about 0.35-0.45; retained permeability can matter more than maximum saturation.",
        "Required confirmation": "Connected pore volume, permeability retention, pressure communication, core calibration, and geomechanics.",
    },
    {
        "Planning band": "High-saturation hydrate-supportive lane",
        "Synthetic saturation-proxy range": "0.60-0.80",
        "Use": "Flag strong hydrate-supportive evidence while retaining a separate flow-risk review.",
        "Scientific anchor": "Public Mount Elbert study: hydrate intervals averaged about 0.50-0.54 and reached about 0.75.",
        "Required confirmation": "NMR-density preferred, sonic and Rt agreement, reservoir continuity, and producibility review.",
    },
    {
        "Planning band": "Very-high-saturation resource lane",
        "Synthetic saturation-proxy range": "> 0.80",
        "Use": "Flag high resource density and detectability, not an automatic best production target.",
        "Scientific anchor": "Public Hydrate-01 study: target reservoir sands reached approximately 0.90 saturation.",
        "Required confirmation": "Permeability-collapse risk, pressure communication, mechanical response, and local core calibration.",
    },
]

PUBLIC_SCIENCE_REFERENCES = [
    {
        "Reference": "Lee and Collett (2011), Mount Elbert",
        "Public URL": "https://pubs.usgs.gov/publication/70036903",
        "Dashboard use": "NMR, sonic, and electrical-resistivity saturation agreement; clay effects must be considered for resistivity interpretation.",
    },
    {
        "Reference": "Haines et al. (2022), Hydrate-01",
        "Public URL": "https://pubs.usgs.gov/publication/70249535",
        "Dashboard use": "Sonic saturation estimates compare with resistivity and NMR; target sands reached approximately 90% pore-space hydrate occupancy.",
    },
    {
        "Reference": "Zyrianova et al. (2024), Eileen trend",
        "Public URL": "https://pubs.usgs.gov/publication/70252109",
        "Dashboard use": "Fault-block segmentation, partial fill, and down-dip water contacts support good-sand/no-hydrate and compartment-aware outcomes.",
    },
]


@dataclass(frozen=True)
class RuntimeConfig:
    input_mode: str = "synthetic"
    approved_csv_paths: tuple[str, ...] = ()
    approved_las_paths: tuple[str, ...] = ()
    curve_aliases: dict[str, tuple[str, ...]] | None = None


def default_curve_aliases() -> dict[str, tuple[str, ...]]:
    return {
        "depth_m": ("DEPTH", "MD", "TVD"),
        "gr_api": ("GR",),
        "rt_ohm_m": ("RT", "ILD", "RDEP"),
        "rhob_g_cc": ("RHOB",),
        "dt_us_ft": ("DT", "DTC"),
        "dts_us_ft": ("DTS",),
        "nmr_porosity_vv": ("NMRPHI", "TCMR"),
        "caliper_in": ("CALI",),
    }


def load_runtime_data(config: RuntimeConfig | None = None) -> pd.DataFrame:
    config = config or RuntimeConfig(curve_aliases=default_curve_aliases())
    if config.input_mode != "synthetic":
        raise NotImplementedError(
            "Approved LAS/CSV loading is intentionally a local-runtime adapter. "
            "Point this configuration layer at authorized files inside the approved environment."
        )
    return generate_synthetic_logs()


def _well_frame(alias: str, offset: float, nmr_available: bool) -> pd.DataFrame:
    rng = np.random.default_rng(sum(ord(char) for char in alias))
    depth = np.arange(350.0, 1150.1, 5.0)
    phase = np.full(depth.shape, "non-reservoir", dtype=object)
    reservoir = ((depth >= 520 + offset) & (depth <= 640 + offset)) | (
        (depth >= 780 + offset) & (depth <= 920 + offset)
    )
    phase[reservoir] = "water sand"
    if alias == "SYNTH-WELL-01":
        phase[(depth >= 555) & (depth <= 620)] = "hydrate sand"
        phase[(depth >= 835) & (depth <= 875)] = "gas sand"
    elif alias == "SYNTH-WELL-02":
        phase[(depth >= 585) & (depth <= 645)] = "good sand, no hydrate"
        phase[(depth >= 820) & (depth <= 900)] = "hydrate sand"
    else:
        phase[(depth >= 610) & (depth <= 675)] = "ambiguous / expert review"
        phase[(depth >= 850) & (depth <= 910)] = "hydrate sand"

    clean_sand = phase != "non-reservoir"
    hydrate = phase == "hydrate sand"
    gas = phase == "gas sand"
    ambiguous = phase == "ambiguous / expert review"
    gr = np.where(clean_sand, 42, 102) + rng.normal(0, 7, depth.size)
    gr = np.where(ambiguous, 62 + rng.normal(0, 9, depth.size), gr)
    porosity = np.where(clean_sand, 0.30, 0.14) + rng.normal(0, 0.018, depth.size)
    rt = np.where(clean_sand, 3.2, 2.0) * np.exp(rng.normal(0, 0.22, depth.size))
    rt = np.where(hydrate, 48 * np.exp(rng.normal(0, 0.28, depth.size)), rt)
    rt = np.where(gas, 34 * np.exp(rng.normal(0, 0.26, depth.size)), rt)
    rt = np.where(ambiguous, 28 * np.exp(rng.normal(0, 0.38, depth.size)), rt)
    rhob = np.where(clean_sand, 2.18, 2.48) + rng.normal(0, 0.035, depth.size)
    rhob = np.where(gas, rhob - 0.18, rhob)
    vp = np.where(clean_sand, 2.65, 3.05) + rng.normal(0, 0.12, depth.size)
    vp = np.where(hydrate, vp + 0.68, vp)
    vp = np.where(gas, vp - 0.65, vp)
    vp = np.where(ambiguous, vp + 0.25, vp)
    vs = np.where(clean_sand, 1.33, 1.48) + rng.normal(0, 0.09, depth.size)
    vs = np.where(hydrate, vs + 0.56, vs)
    vs = np.where(gas, vs - 0.42, vs)
    vs = np.where(ambiguous, vs + 0.22, vs)
    caliper = 8.5 + rng.normal(0, 0.20, depth.size)
    washout = ((depth >= 705 + offset) & (depth <= 735 + offset)) | (
        (alias == "SYNTH-WELL-03") & (depth >= 630) & (depth <= 655)
    )
    caliper = np.where(washout, caliper + 1.7, caliper)
    temperature = -10 + depth * 0.032
    pressure = depth * 0.009795
    dt = 304.8 / vp
    dts = 304.8 / vs
    vp_vs = vp / vs
    lambda_rho = rhob * (vp**2 - 2 * vs**2)
    mu_rho = rhob * vs**2
    nmr = porosity - np.where(hydrate, 0.12, np.where(ambiguous, 0.055, 0.012))
    nmr += rng.normal(0, 0.012, depth.size)
    if not nmr_available:
        nmr[:] = np.nan
    separation = porosity - nmr
    archie = np.clip(1 - ((0.12 / ((porosity.clip(0.04) ** 2) * rt)) ** 0.5), 0, 1)
    nmr_proxy = np.clip(separation / porosity, 0, 1)
    qc = np.where(caliper > 9.5, "REVIEW: borehole washout", "PASS")
    stability = np.where((depth >= 470) & (depth <= 1080), "stable working screen", "outside working screen")
    return pd.DataFrame(
        {
            "well_alias": alias,
            "location_alias": alias.replace("WELL", "LOCATION"),
            "depth_m": depth,
            "gr_api": gr,
            "rt_ohm_m": rt,
            "rhob_g_cc": rhob,
            "density_porosity_vv": porosity,
            "dt_us_ft": dt,
            "vp_km_s": vp,
            "dts_us_ft": dts,
            "vs_km_s": vs,
            "vp_vs_ratio": vp_vs,
            "lambda_rho": lambda_rho,
            "mu_rho": mu_rho,
            "nmr_porosity_vv": nmr,
            "nmr_density_separation_vv": separation,
            "caliper_in": caliper,
            "borehole_qc": qc,
            "temperature_c": temperature,
            "pressure_mpa": pressure,
            "ghsz_context": stability,
            "core_calibration_placeholder": "synthetic placeholder only",
            "archie_hydrate_proxy": archie,
            "nmr_density_hydrate_proxy": nmr_proxy,
            "synthetic_phase_reference": phase,
            "data_boundary": SYNTHETIC_LABEL,
        }
    )


def generate_synthetic_logs() -> pd.DataFrame:
    return pd.concat(
        [
            _well_frame("SYNTH-WELL-01", 0, True),
            _well_frame("SYNTH-WELL-02", 25, True),
            _well_frame("SYNTH-WELL-03", 50, False),
        ],
        ignore_index=True,
    )


def variable_range_summary(
    logs: pd.DataFrame,
    variables: Iterable[str] | None = None,
    well_alias: str | None = None,
    depth_interval: tuple[float, float] | None = None,
) -> pd.DataFrame:
    subset = logs.copy()
    if well_alias:
        subset = subset[subset["well_alias"] == well_alias]
    if depth_interval:
        subset = subset[subset["depth_m"].between(*depth_interval)]
    variables = list(variables or VARIABLES)
    rows = []
    for variable in variables:
        label, unit = VARIABLES[variable]
        values = subset[variable]
        non_null = values.dropna()
        rows.append(
            {
                "Data label": SYNTHETIC_LABEL,
                "Variable": label,
                "Column": variable,
                "Unit": unit,
                "Minimum": non_null.min() if not non_null.empty else np.nan,
                "P10": non_null.quantile(0.10) if not non_null.empty else np.nan,
                "Median": non_null.median() if not non_null.empty else np.nan,
                "P90": non_null.quantile(0.90) if not non_null.empty else np.nan,
                "Maximum": non_null.max() if not non_null.empty else np.nan,
                "Missingness %": round(values.isna().mean() * 100, 1),
                "QC status": "REVIEW" if values.isna().any() or (subset["borehole_qc"] != "PASS").any() else "PASS",
            }
        )
    return pd.DataFrame(rows)


def screen_intervals(logs: pd.DataFrame, interval_m: int = 40) -> pd.DataFrame:
    rows = []
    for alias, well in logs.groupby("well_alias"):
        well = well.copy()
        well["interval_top_m"] = (well["depth_m"] // interval_m) * interval_m
        for top, interval in well.groupby("interval_top_m"):
            median = interval.median(numeric_only=True)
            stable = (interval["ghsz_context"] == "stable working screen").mean() >= 0.5
            reservoir = median["gr_api"] < 65 and median["density_porosity_vv"] >= 0.20
            qc_review = (interval["borehole_qc"] != "PASS").any()
            nmr_available = interval["nmr_porosity_vv"].notna().mean() >= 0.5
            elastic_support = median["vp_km_s"] >= 2.9 and median["mu_rho"] >= 6.0
            high_rt = median["rt_ohm_m"] >= 10
            gas_like = median["vp_km_s"] < 2.35 and high_rt
            if reservoir and stable and high_rt and elastic_support and not qc_review:
                phase = "hydrate-supportive multi-log response"
            elif reservoir and gas_like:
                phase = "gas-supportive response"
            elif reservoir and not high_rt:
                phase = "good sand, no hydrate"
            elif reservoir:
                phase = "ambiguous / expert review"
            else:
                phase = "non-reservoir / review"
            proxy = (
                median["nmr_density_hydrate_proxy"]
                if nmr_available
                else median["archie_hydrate_proxy"]
            )
            proxy_source = "NMR-density preferred" if nmr_available else "Archie supplementary cross-check"
            core_confidence = "placeholder: not calibrated" if not qc_review else "placeholder: QC-limited"
            producibility = "separate review"
            sweet_spot_lane = "not promoted"
            if phase.startswith("hydrate") and proxy < 0.60 and median["density_porosity_vv"] >= 0.24:
                producibility = "moderate-priority synthetic screen"
                sweet_spot_lane = "candidate sweet-spot review lane"
            elif phase.startswith("hydrate"):
                producibility = "flow-risk review: saturation is not producibility"
                sweet_spot_lane = "high-saturation resource lane; flow-risk review"
            flags = []
            if not stable:
                flags.append("outside working GHSZ screen")
            if qc_review:
                flags.append("borehole QC review")
            if not nmr_available:
                flags.append("NMR unavailable")
            if high_rt and not elastic_support:
                flags.append("high Rt without full elastic support")
            rows.append(
                {
                    "Data label": SYNTHETIC_LABEL,
                    "Well alias": alias,
                    "Top depth (m)": int(top),
                    "Base depth (m)": int(top + interval_m),
                    "Stability admissibility": "admissible working screen" if stable else "outside / uncertain",
                    "Reservoir quality": "reservoir-grade screen" if reservoir else "non-reservoir / marginal",
                    "Phase-classification evidence": phase,
                    "Hydrate-saturation proxy": round(float(proxy), 2) if pd.notna(proxy) else np.nan,
                    "Proxy source": proxy_source,
                    "Core-calibration confidence": core_confidence,
                    "Producibility screen": producibility,
                    "Synthetic sweet-spot review lane": sweet_spot_lane,
                    "Uncertainty flags": "; ".join(flags) if flags else "none in synthetic screen",
                }
            )
    return pd.DataFrame(rows)


def synthetic_core_placeholders() -> pd.DataFrame:
    return pd.DataFrame(
        [
            [SYNTHETIC_LABEL, "SYNTH-WELL-01", 590.0, "+/- 1.5 m", "illustrative good", "hydrate sand", 0.29, 0.48, "none", 0.85],
            [SYNTHETIC_LABEL, "SYNTH-WELL-02", 615.0, "+/- 2.0 m", "illustrative fair", "water-bearing sand", 0.31, 0.05, "minor expansion", 0.60],
            [SYNTHETIC_LABEL, "SYNTH-WELL-03", 875.0, "+/- 3.0 m", "illustrative review", "hydrate-supportive", 0.27, 0.42, "depth-match review", 0.45],
        ],
        columns=[
            "Data label",
            "Well alias",
            "Sample depth (m)",
            "Depth-match uncertainty window",
            "Pressure-core quality",
            "Interpreted phase",
            "Porosity",
            "Saturation reference",
            "Disturbance flag",
            "Confidence weight",
        ],
    )


def nearby_log_calibration(logs: pd.DataFrame, core: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, sample in core.iterrows():
        well = logs[logs["well_alias"] == sample["Well alias"]].copy()
        nearest = well.iloc[(well["depth_m"] - sample["Sample depth (m)"]).abs().argmin()]
        rows.append(
            {
                **sample.to_dict(),
                "Nearest log depth (m)": nearest["depth_m"],
                "Depth offset (m)": round(float(nearest["depth_m"] - sample["Sample depth (m)"]), 2),
                "Nearest GR (API)": round(float(nearest["gr_api"]), 1),
                "Nearest Rt (ohm m)": round(float(nearest["rt_ohm_m"]), 1),
                "Nearest Vp (km/s)": round(float(nearest["vp_km_s"]), 2),
                "Nearest borehole QC": nearest["borehole_qc"],
            }
        )
    return pd.DataFrame(rows)


def well_log_panel(logs: pd.DataFrame, well_alias: str) -> go.Figure:
    well = logs[logs["well_alias"] == well_alias]
    specs = [("gr_api", "GR"), ("rt_ohm_m", "Rt"), ("density_porosity_vv", "Density phi"), ("vp_km_s", "Vp"), ("nmr_density_hydrate_proxy", "NMR Sh proxy")]
    figure = make_subplots(rows=1, cols=len(specs), shared_yaxes=True, horizontal_spacing=0.035)
    for index, (column, label) in enumerate(specs, start=1):
        figure.add_trace(go.Scatter(x=well[column], y=well["depth_m"], name=label, mode="lines"), row=1, col=index)
        figure.update_xaxes(title_text=label, row=1, col=index)
    figure.update_yaxes(title_text="Depth (m)", autorange="reversed", row=1, col=1)
    figure.update_layout(title=f"{SYNTHETIC_LABEL} | {well_alias} well-log panel", height=640, showlegend=False)
    return figure


def cross_well_range_figure(summary: pd.DataFrame, variable_label: str) -> go.Figure:
    selected = summary[summary["Variable"] == variable_label]
    figure = go.Figure()
    figure.add_trace(go.Bar(x=selected["Well alias"], y=selected["Median"], name="Median"))
    figure.add_trace(go.Scatter(x=selected["Well alias"], y=selected["Minimum"], mode="markers", name="Minimum"))
    figure.add_trace(go.Scatter(x=selected["Well alias"], y=selected["Maximum"], mode="markers", name="Maximum"))
    figure.update_layout(title=f"{SYNTHETIC_LABEL} | Cross-well {variable_label} comparison", height=430, barmode="group")
    return figure


def model_placeholder_figures() -> tuple[go.Figure, go.Figure]:
    matrix = go.Figure(
        data=go.Heatmap(
            z=[[18, 3, 2], [4, 15, 3], [2, 4, 16]],
            x=["hydrate", "water", "review"],
            y=["hydrate", "water", "review"],
            colorscale="Blues",
            showscale=False,
            text=[[18, 3, 2], [4, 15, 3], [2, 4, 16]],
            texttemplate="%{text}",
        )
    )
    matrix.update_layout(title=f"{SYNTHETIC_LABEL} | Placeholder confusion matrix", height=380)
    calibration = go.Figure()
    calibration.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Ideal"))
    calibration.add_trace(go.Scatter(x=[0.1, 0.3, 0.5, 0.7, 0.9], y=[0.08, 0.27, 0.52, 0.66, 0.84], mode="lines+markers", name="Synthetic placeholder"))
    calibration.update_layout(
        title=f"{SYNTHETIC_LABEL} | Placeholder model-calibration panel",
        xaxis_title="Predicted probability",
        yaxis_title="Observed frequency",
        height=380,
    )
    return matrix, calibration


def csv_bytes(frame: pd.DataFrame) -> bytes:
    buffer = StringIO()
    frame.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")


def figure_html_bytes(figure: go.Figure) -> bytes:
    return figure.to_html(include_plotlyjs="cdn", full_html=True).encode("utf-8")
