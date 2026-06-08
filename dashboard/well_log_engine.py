from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dashboard.runtime.exports import csv_bytes, figure_html_bytes
from dashboard.runtime.loaders import load_runtime_data as load_configured_runtime_data
from dashboard.runtime.schemas import RuntimeConfig, default_curve_aliases


SYNTHETIC_LABEL = "SYNTHETIC DEMONSTRATION DATA"

HEADER_SCHEMA_BLUEPRINT = [
    {
        "Track group": "Depth and alignment",
        "Visible headers": "DEPTH, DEPT, Depth_ft, Depth, ft",
        "Canonical field": "depth_m",
        "Role": "Index / measured",
        "Unit handling": "Accept ft or m; convert explicitly to m",
    },
    {
        "Track group": "Borehole QC",
        "Visible headers": "caliper, CAL1, Differential Caliper",
        "Canonical field": "caliper_in, differential_caliper",
        "Role": "Measured / QC",
        "Unit handling": "Preserve source unit and reference diameter",
    },
    {
        "Track group": "Lithology",
        "Visible headers": "GR",
        "Canonical field": "gr_api",
        "Role": "Measured input",
        "Unit handling": "API",
    },
    {
        "Track group": "Porosity",
        "Visible headers": "Rho_b, RHOB, Density_gcpcc, DPHI, NPHI, NMRPHI",
        "Canonical field": "rhob_g_cc and porosity channels",
        "Role": "Measured / derived",
        "Unit handling": "Convert density; confirm fraction versus percent",
    },
    {
        "Track group": "Electrical response",
        "Visible headers": "RES, A090, AF90, Deep formation resistivity",
        "Canonical field": "rt_ohm_m",
        "Role": "Measured input",
        "Unit handling": "Ohm.m; confirm tool mnemonic",
    },
    {
        "Track group": "Elastic response",
        "Visible headers": "Vp, VP, VELP, Vs, VS, VS1",
        "Canonical field": "vp_m_s, vs_m_s",
        "Role": "Measured or supplied",
        "Unit handling": "m/s; keep supplied-versus-calculated provenance",
    },
    {
        "Track group": "Elastic response",
        "Visible headers": "Ratio Vp/Vs, Impedance",
        "Canonical field": "vp_vs_ratio, acoustic_impedance",
        "Role": "Derived feature",
        "Unit handling": "Calculate from canonical density and velocity",
    },
    {
        "Track group": "Interpretation / calibration",
        "Visible headers": "Sgh, S_h, Hydrate Saturation, NMR_SAT, S_wr, Swr",
        "Canonical field": "hydrate_saturation_vv, irreducible_water_saturation_vv",
        "Role": "Target / interpretation",
        "Unit handling": "Confirm fraction versus percent; exclude from ML inputs",
    },
]

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
    "shear_modulus_gpa": ("Shear modulus", "GPa"),
    "bulk_modulus_gpa": ("Bulk modulus", "GPa"),
    "poisson_ratio": ("Poisson ratio", "ratio"),
    "youngs_modulus_gpa": ("Young's modulus", "GPa"),
    "lambda_rho": ("lambda-rho", "GPa g/cc"),
    "mu_rho": ("mu-rho", "GPa g/cc"),
    "vshale": ("Shale volume proxy", "fraction"),
    "nmr_porosity_vv": ("NMR porosity", "v/v"),
    "nmr_density_separation_vv": ("NMR-density separation", "v/v"),
    "caliper_in": ("Caliper", "in"),
    "temperature_c": ("Temperature", "deg C"),
    "pressure_mpa": ("Pressure", "MPa"),
    "vertical_stress_mpa": ("Vertical stress", "MPa"),
    "effective_stress_mpa": ("Effective stress", "MPa"),
    "permeability_retention_proxy": ("Permeability retention proxy", "fraction"),
    "reservoir_quality_score": ("Reservoir quality score", "0-1"),
    "hydrate_evidence_score": ("Hydrate evidence score", "0-1"),
    "archie_hydrate_proxy": ("Archie hydrate proxy", "fraction"),
    "nmr_density_hydrate_proxy": ("NMR-density hydrate proxy", "fraction"),
}

SCREENING_BANDS = {
    "gr_api": (25, 65, "Cleaner reservoir-sand tendency; validate with porosity and facies."),
    "rt_ohm_m": (10, 100, "Hydrate-supportive Rt tendency only when sonic/NMR/QC agree."),
    "density_porosity_vv": (0.20, 0.35, "Reservoir capacity window; capacity is not occupancy."),
    "vp_km_s": (2.5, 4.0, "Hydrate/ice/competent-sand stiffening tendency; compare Vs and lithology."),
    "vs_km_s": (1.0, 2.5, "Rigidity-supportive tendency that helps separate hydrate from free gas."),
    "mu_rho": (10, 55, "Rigidity increase; review ice-bearing sediment and competent lithology."),
    "lambda_rho": (12, 55, "Compressibility-sensitive crossplot lane; not a standalone classifier."),
    "nmr_density_separation_vv": (0.06, 0.22, "Mobile-fluid deficit proxy; depth-match and NMR QC required."),
    "archie_hydrate_proxy": (0.35, 0.80, "Supplementary saturation lane; salinity and clay uncertainty remain."),
    "nmr_density_hydrate_proxy": (0.35, 0.80, "Preferred saturation proxy where NMR exists; calibrate to core."),
    "effective_stress_mpa": (3, 18, "Stress context for compaction and mechanical risk, not hydrate proof."),
    "permeability_retention_proxy": (0.20, 0.75, "Production-review lane; high saturation may reduce flow."),
    "reservoir_quality_score": (0.55, 1.0, "Good rock screen before phase classification."),
    "hydrate_evidence_score": (0.55, 1.0, "Multi-log evidence score; requires admissibility and QC review."),
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

EQUATION_LIBRARY = [
    {
        "Equation group": "Lithology / reservoir quality",
        "Equation": "Vsh = clip((GR - GR_clean) / (GR_shale - GR_clean), 0, 1)",
        "Inputs": "GR plus local clean-sand and shale anchors",
        "Feature produced": "Shale volume proxy",
        "Why it matters": "Screens clean reservoir sand before any hydrate phase call.",
        "Classification use": "Hydrate evidence is downgraded in shale-rich intervals unless core/facies evidence supports it.",
        "Source anchor": "Manuscript Section 8; hydrate_property_ranges_full_suite; Nanushuk reservoir-quality source",
    },
    {
        "Equation group": "Density porosity",
        "Equation": "phi_D = (rho_ma - RHOB) / (rho_ma - rho_f)",
        "Inputs": "RHOB, matrix density, fluid density",
        "Feature produced": "Storage-capacity porosity",
        "Why it matters": "Separates reservoir capacity from hydrate occupancy.",
        "Classification use": "Good porosity raises reservoir-quality score but does not create a hydrate label.",
        "Source anchor": "Manuscript Table 12.A6; hydrate_wireline_equation_map",
    },
    {
        "Equation group": "Sonic velocity",
        "Equation": "Vp = 304.8 / DT; Vs = 304.8 / DTS",
        "Inputs": "DT and DTS in us/ft",
        "Feature produced": "Compressional and shear velocity",
        "Why it matters": "Hydrate tends to stiffen the frame; gas tends to soften sonic response.",
        "Classification use": "Hydrate-supportive Rt requires elastic support to avoid gas/low-porosity false positives.",
        "Source anchor": "Lee and Collett (2011); Haines et al. (2022); manuscript Section 7",
    },
    {
        "Equation group": "Elastic moduli",
        "Equation": "G = rho * Vs^2; K = rho * (Vp^2 - 4Vs^2/3)",
        "Inputs": "RHOB, Vp, Vs",
        "Feature produced": "Shear modulus and bulk modulus",
        "Why it matters": "Quantifies rigidity and incompressibility from logs.",
        "Classification use": "Higher shear modulus supports hydrate/ice/competent-rock review; low stiffness with high Rt flags gas or ambiguity.",
        "Source anchor": "lambda_density_pt_overburden_ranges; manuscript Table 12.A7",
    },
    {
        "Equation group": "Lambda-rho / mu-rho",
        "Equation": "lambda-rho = rho * (Vp^2 - 2Vs^2); mu-rho = rho * Vs^2",
        "Inputs": "RHOB, Vp, Vs",
        "Feature produced": "Fluid-sensitive and rigidity-sensitive crossplot terms",
        "Why it matters": "Separates gas-softened response from hydrate/ice/rigid-framework response better than Rt alone.",
        "Classification use": "Used as a crossplot lane; overlap with shale, ice, and carbonates remains explicit.",
        "Source anchor": "lambda_density_pt_overburden_ranges; hydrate_property_ranges_full_suite",
    },
    {
        "Equation group": "Poisson / Young's modulus",
        "Equation": "nu = (Vp^2 - 2Vs^2) / (2(Vp^2 - Vs^2)); E = 2G(1 + nu)",
        "Inputs": "Vp, Vs, shear modulus",
        "Feature produced": "Mechanical behavior features",
        "Why it matters": "Adds geomechanical context for compaction and production-risk discussion.",
        "Classification use": "Not a hydrate detector; supports rock-type and producibility interpretation.",
        "Source anchor": "Geomechanical relationship with Wireline Logging AN; geomechanics/productivity notes",
    },
    {
        "Equation group": "Pressure-temperature admissibility",
        "Equation": "T(z) = T0 + GT*z; Pp(z) = rho_w*g*z",
        "Inputs": "Depth, thermal gradient, water density",
        "Feature produced": "Working GHSZ screen",
        "Why it matters": "Hydrate can only exist where pressure-temperature conditions are admissible.",
        "Classification use": "Outside/marginal stability prevents automatic hydrate promotion even if logs look interesting.",
        "Source anchor": "USGS Hydrate-01 and Mount Elbert publications; manuscript Section 6",
    },
    {
        "Equation group": "Overburden / effective stress",
        "Equation": "sigma_v = integral(rho_b*g dz); sigma_eff = sigma_v - alpha*Pp",
        "Inputs": "Depth, density/overburden gradient, pore pressure, Biot coefficient",
        "Feature produced": "Vertical and effective stress",
        "Why it matters": "Stress affects compaction, velocity, porosity, and mechanical risk.",
        "Classification use": "Velocity/stiffness anomalies are reviewed against stress and rock type before hydrate labeling.",
        "Source anchor": "north_slope_overburden_framework; geomechanics/productivity notes",
    },
    {
        "Equation group": "Saturation proxy",
        "Equation": "Sh_Archie = 1 - (a*Rw / (phi^m * Rt))^(1/n)",
        "Inputs": "Rt, porosity, water resistivity, Archie parameters",
        "Feature produced": "Electrical hydrate proxy",
        "Why it matters": "Hydrate reduces connected brine pathways and can increase Rt.",
        "Classification use": "Supplementary only; clay, salinity, gas, low porosity, and ice must be reviewed.",
        "Source anchor": "Lee and Collett (2011); hydrate_wireline_equation_map",
    },
    {
        "Equation group": "NMR-density saturation proxy",
        "Equation": "Sh_NMRD = (phi_D - phi_NMR) / phi_D",
        "Inputs": "Density porosity and NMR porosity",
        "Feature produced": "Preferred hydrate proxy where NMR exists",
        "Why it matters": "NMR-density separation can represent pore volume not seen as mobile water.",
        "Classification use": "Preferred saturation proxy, but depth matching, shale effects, and tool QC remain visible.",
        "Source anchor": "Lee and Collett (2011); Haines et al. (2022)",
    },
    {
        "Equation group": "Permeability / producibility risk",
        "Equation": "k_rel_proxy = (1 - Sh)^n",
        "Inputs": "Hydrate saturation proxy and exponent n",
        "Feature produced": "Permeability retention proxy",
        "Why it matters": "High saturation may increase resource density while reducing flow capacity.",
        "Classification use": "Separates hydrate occurrence/saturation from production sweet-spot ranking.",
        "Source anchor": "Hydrate_Full_Expanded_Document; geomechanics/productivity notes",
    },
]

CLASSIFICATION_WORKFLOW = [
    {
        "Stage": "1. QC gate",
        "Question": "Are borehole conditions and curve coverage good enough?",
        "Primary variables": "Caliper, missing DTS/NMR, curve depth alignment",
        "Pass logic": "Bad-hole intervals remain review-only until density/sonic reliability is defensible.",
    },
    {
        "Stage": "2. Stability gate",
        "Question": "Can hydrate physically exist at this depth?",
        "Primary variables": "Temperature, pressure, depth, local gradient",
        "Pass logic": "Inside working GHSZ permits evaluation; it does not prove hydrate.",
    },
    {
        "Stage": "3. Rock-quality gate",
        "Question": "Is there enough clean, connected reservoir volume?",
        "Primary variables": "GR/Vsh, density porosity, rock type, facies",
        "Pass logic": "Clean porous sand is a candidate host; shale/coal/carbonate require separate handling.",
    },
    {
        "Stage": "4. Phase-evidence gate",
        "Question": "Do electrical, sonic, density, and NMR responses agree?",
        "Primary variables": "Rt, Vp, Vs, lambda-rho, mu-rho, NMR-density proxy",
        "Pass logic": "Hydrate is promoted only when high Rt is supported by stiffness and saturation evidence.",
    },
    {
        "Stage": "5. Competing-explanation gate",
        "Question": "Could the same signal be gas, ice, shale, coal, carbonate, or stress?",
        "Primary variables": "Vp/Vs, mu-rho, Vsh, effective stress, permafrost/depth context",
        "Pass logic": "Ambiguous intervals stay in expert review rather than being forced into hydrate/non-hydrate.",
    },
    {
        "Stage": "6. Producibility ranking",
        "Question": "If hydrate is present, is it likely to flow/respond well?",
        "Primary variables": "Porosity, permeability proxy, saturation proxy, stress, continuity",
        "Pass logic": "Moderate saturation with retained flow can outrank maximum saturation for production review.",
    },
]

ROCKTYPE_CONTEXT_GUIDE = [
    {
        "Rock / interval type": "Clean sand",
        "Why it helps": "Provides pore volume and likely permeability for hydrate occupancy.",
        "False-positive risk": "Can be water-bearing with no charge or hydrate occupancy.",
        "Dashboard response": "Eligible for reservoir-quality score and phase-evidence review.",
    },
    {
        "Rock / interval type": "Shaly or bentonitic sand",
        "Why it helps": "May host thin or mixed hydrate-bearing layers.",
        "False-positive risk": "Clay conductivity, bound water, and radioactive minerals distort GR/Rt/porosity transforms.",
        "Dashboard response": "Downgrade confidence and require NMR/core/facies support.",
    },
    {
        "Rock / interval type": "Ice-bearing sediment / permafrost",
        "Why it helps": "Can be stiff and resistive in hydrate stability settings.",
        "False-positive risk": "Ice can overlap hydrate in Vs, mu-rho, and resistivity behavior.",
        "Dashboard response": "Require depth/permafrost and P-T context before hydrate promotion.",
    },
    {
        "Rock / interval type": "Free-gas sand",
        "Why it helps": "Can share high resistivity with hydrate-bearing intervals.",
        "False-positive risk": "Gas often lowers Vp and weakens lambda-rho compared with hydrate.",
        "Dashboard response": "High Rt plus low Vp/elastic weakness routes to gas-supportive or expert-review lanes.",
    },
    {
        "Rock / interval type": "Coal/lignite or carbonate/competent rock",
        "Why it helps": "Important regional lithologies and mechanical end members.",
        "False-positive risk": "Can create high/low density, high resistivity, or high stiffness unrelated to hydrate.",
        "Dashboard response": "Treat as competing lithology until local log/core evidence resolves it.",
    },
]


def load_runtime_data(config: RuntimeConfig | None = None) -> pd.DataFrame:
    return load_configured_runtime_data(config, generate_synthetic_logs)


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
    shear_modulus = rhob * vs**2
    bulk_modulus = rhob * (vp**2 - (4.0 / 3.0) * vs**2)
    poisson = (vp**2 - 2 * vs**2) / (2 * (vp**2 - vs**2))
    youngs_modulus = 2 * shear_modulus * (1 + poisson)
    lambda_rho = rhob * (vp**2 - 2 * vs**2)
    mu_rho = shear_modulus
    vshale = np.clip((gr - 30) / (105 - 30), 0, 1)
    nmr = porosity - np.where(hydrate, 0.12, np.where(ambiguous, 0.055, 0.012))
    nmr += rng.normal(0, 0.012, depth.size)
    if not nmr_available:
        nmr[:] = np.nan
    separation = porosity - nmr
    archie = np.clip(1 - ((0.12 / ((porosity.clip(0.04) ** 2) * rt)) ** 0.5), 0, 1)
    nmr_proxy = np.clip(separation / porosity, 0, 1)
    saturation_for_flow = np.where(np.isnan(nmr_proxy), archie, nmr_proxy)
    permeability_retention = np.clip((1 - saturation_for_flow) ** 3, 0, 1)
    vertical_stress = depth * 0.0226
    effective_stress = vertical_stress - (0.85 * pressure)
    reservoir_quality_score = np.clip(
        0.45 * ((65 - gr) / 45)
        + 0.40 * ((porosity - 0.12) / 0.22)
        + 0.15 * (1 - vshale),
        0,
        1,
    )
    hydrate_evidence_score = np.clip(
        0.30 * ((np.log10(rt.clip(0.1)) - np.log10(5)) / (np.log10(80) - np.log10(5)))
        + 0.25 * ((vp - 2.4) / 1.4)
        + 0.20 * ((vs - 1.0) / 1.2)
        + 0.15 * ((mu_rho - 5) / 25)
        + 0.10 * saturation_for_flow,
        0,
        1,
    )
    rock_type = np.select(
        [
            vshale >= 0.65,
            (vshale < 0.35) & (porosity >= 0.22),
            (vshale < 0.55) & (porosity >= 0.18),
            (rhob < 1.85) | ((gr < 45) & (rt > 20) & (vp < 2.35)),
        ],
        ["shale-rich / non-reservoir", "clean reservoir sand", "shaly reservoir sand", "coal/gas-risk review"],
        default="mixed lithology review",
    )
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
            "shear_modulus_gpa": shear_modulus,
            "bulk_modulus_gpa": bulk_modulus,
            "poisson_ratio": poisson,
            "youngs_modulus_gpa": youngs_modulus,
            "lambda_rho": lambda_rho,
            "mu_rho": mu_rho,
            "vshale": vshale,
            "rock_type_screen": rock_type,
            "nmr_porosity_vv": nmr,
            "nmr_density_separation_vv": separation,
            "caliper_in": caliper,
            "borehole_qc": qc,
            "temperature_c": temperature,
            "pressure_mpa": pressure,
            "vertical_stress_mpa": vertical_stress,
            "effective_stress_mpa": effective_stress,
            "ghsz_context": stability,
            "core_calibration_placeholder": "synthetic placeholder only",
            "archie_hydrate_proxy": archie,
            "nmr_density_hydrate_proxy": nmr_proxy,
            "permeability_retention_proxy": permeability_retention,
            "reservoir_quality_score": reservoir_quality_score,
            "hydrate_evidence_score": hydrate_evidence_score,
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
            reservoir = (
                median["gr_api"] < 65
                and median["density_porosity_vv"] >= 0.20
                and median["reservoir_quality_score"] >= 0.45
            )
            qc_review = (interval["borehole_qc"] != "PASS").any()
            nmr_available = interval["nmr_porosity_vv"].notna().mean() >= 0.5
            elastic_support = median["vp_km_s"] >= 2.9 and median["mu_rho"] >= 6.0 and median["hydrate_evidence_score"] >= 0.50
            high_rt = median["rt_ohm_m"] >= 10
            gas_like = median["vp_km_s"] < 2.35 and high_rt
            common_rock_type = interval["rock_type_screen"].mode().iloc[0]
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
            if common_rock_type not in {"clean reservoir sand", "shaly reservoir sand"}:
                flags.append(f"competing lithology: {common_rock_type}")
            if median["effective_stress_mpa"] > 14:
                flags.append("higher effective-stress context")
            if phase.startswith("hydrate") and median["permeability_retention_proxy"] < 0.20:
                flags.append("low permeability-retention proxy")
            rows.append(
                {
                    "Data label": SYNTHETIC_LABEL,
                    "Well alias": alias,
                    "Top depth (m)": int(top),
                    "Base depth (m)": int(top + interval_m),
                    "Stability admissibility": "admissible working screen" if stable else "outside / uncertain",
                    "Reservoir quality": "reservoir-grade screen" if reservoir else "non-reservoir / marginal",
                    "Dominant rock-type screen": common_rock_type,
                    "Phase-classification evidence": phase,
                    "Reservoir-quality score": round(float(median["reservoir_quality_score"]), 2),
                    "Hydrate-evidence score": round(float(median["hydrate_evidence_score"]), 2),
                    "Hydrate-saturation proxy": round(float(proxy), 2) if pd.notna(proxy) else np.nan,
                    "Proxy source": proxy_source,
                    "Effective stress (MPa)": round(float(median["effective_stress_mpa"]), 1),
                    "Permeability-retention proxy": round(float(median["permeability_retention_proxy"]), 2),
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
    specs = [
        ("gr_api", "GR"),
        ("rt_ohm_m", "Rt"),
        ("density_porosity_vv", "Density phi"),
        ("vp_km_s", "Vp"),
        ("mu_rho", "mu-rho"),
        ("nmr_density_hydrate_proxy", "NMR Sh proxy"),
    ]
    figure = make_subplots(rows=1, cols=len(specs), shared_yaxes=True, horizontal_spacing=0.035)
    for index, (column, label) in enumerate(specs, start=1):
        figure.add_trace(go.Scatter(x=well[column], y=well["depth_m"], name=label, mode="lines"), row=1, col=index)
        figure.update_xaxes(title_text=label, row=1, col=index)
    phase_styles = {
        "hydrate sand": ("rgba(22, 125, 141, 0.16)", "hydrate-supportive"),
        "gas sand": ("rgba(217, 119, 61, 0.14)", "gas-risk"),
        "ambiguous / expert review": ("rgba(120, 120, 120, 0.12)", "expert review"),
        "good sand, no hydrate": ("rgba(76, 175, 80, 0.10)", "good sand/no hydrate"),
    }
    for phase, (color, label) in phase_styles.items():
        mask = well["synthetic_phase_reference"].eq(phase)
        if not mask.any():
            continue
        block_ids = (mask.ne(mask.shift(fill_value=False))).cumsum()
        for _, block in well[mask].groupby(block_ids[mask]):
            top = float(block["depth_m"].min())
            base = float(block["depth_m"].max())
            figure.add_hrect(y0=top, y1=base, fillcolor=color, line_width=0, row="all", col="all")
            figure.add_annotation(
                xref="x domain",
                yref="y",
                x=0.02,
                y=(top + base) / 2,
                text=label,
                showarrow=True,
                arrowhead=2,
                ax=52,
                ay=0,
                bgcolor="rgba(255,255,255,0.86)",
                bordercolor="#123447",
                borderwidth=1,
                font={"size": 10},
            )
    figure.update_yaxes(title_text="Depth (m)", autorange="reversed", row=1, col=1)
    figure.update_layout(
        title=f"{SYNTHETIC_LABEL} | {well_alias} well-log panel with interpretation callouts",
        height=680,
        showlegend=False,
    )
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
