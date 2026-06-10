"""Public and synthetic visual-story constants for the Streamlit website."""

from __future__ import annotations


MISSION_OUTCOMES = [
    {
        "label": "Detect",
        "detail": "Find hydrate-supportive intervals.",
        "color": "#67d0df",
    },
    {
        "label": "Quantify",
        "detail": "Estimate saturation with uncertainty.",
        "color": "#25b99a",
    },
    {
        "label": "Rank",
        "detail": "Separate sweet spots from producibility.",
        "color": "#d8a24a",
    },
]


HEADER_DERIVED_SYNTHETIC_NOTE = (
    "Header-derived synthetic records only: the user supplied Excel header/schema "
    "references, not real well-log rows. Values are generated placeholders for "
    "layout, validation, and visual QA."
)


EVIDENCE_STACK = [
    {"label": "Regional context", "detail": "assessment, structure, public GIS", "color": "#67d0df"},
    {"label": "Stability + reservoir", "detail": "admissible zone and sand quality", "color": "#25b99a"},
    {"label": "Logs + core", "detail": "GR, Rt, density, Vp, Vs, NMR, core labels", "color": "#d8a24a"},
    {"label": "Decision", "detail": "phase, saturation, uncertainty, rank", "color": "#8ea7ff"},
]


SOURCE_ANCHORS = [
    {
        "claim": "ML inputs and saturation target design",
        "source": "Chong et al. (2022)",
        "use": "Density, porosity, resistivity, GR, Vp, Vs; NMR-density saturation reference; ANN baseline.",
    },
    {
        "claim": "NMR, sonic, and resistivity comparison",
        "source": "Lee and Collett (2011); Haines et al. (2022)",
        "use": "Cross-check saturation evidence and keep shale/tool effects visible.",
    },
    {
        "claim": "Good sand can remain no-hydrate",
        "source": "Zyrianova et al. (2024); USGS assessment sources",
        "use": "Compartmentalization, partial fill, water contacts, and charge/structure limits.",
    },
    {
        "claim": "Reservoir quality is separate from hydrate presence",
        "source": "Helmold and LePain (2023)",
        "use": "Texture, burial, porosity, permeability, and reservoir screening.",
    },
    {
        "claim": "Public maps constrain, not classify",
        "source": "USGS/Collett regional assessment sources",
        "use": "Regional petroleum-system framing without interval-scale hydrate labels.",
    },
]


PIPELINE_STAGES = [
    {"label": "Logs + core", "status": "runtime", "color": "#67d0df"},
    {"label": "QC", "status": "ready / partial / blocked", "color": "#d8a24a"},
    {"label": "Physics", "status": "derived features", "color": "#25b99a"},
    {"label": "ML", "status": "held-out wells", "color": "#8ea7ff"},
    {"label": "Review", "status": "uncertainty + reasons", "color": "#f2f5f6"},
    {"label": "Deliver", "status": "Word + slides", "color": "#f2f5f6"},
]


LAYER_SUMMARY = [
    {"label": "Assessment units", "value": 6, "color": "#67d0df"},
    {"label": "2D seismic", "value": 26, "color": "#25b99a"},
    {"label": "3D footprints", "value": 36, "color": "#8ea7ff"},
    {"label": "Public wells", "value": 10250, "color": "#f2f5f6"},
    {"label": "Missing geometry", "value": 356, "color": "#d8a24a"},
]


STRUCTURE_LAYERS = [
    {"label": "Topo", "depth": 0.16, "color": "#6cc36c"},
    {"label": "LCU", "depth": 0.36, "color": "#67a9dc"},
    {"label": "Shublik", "depth": 0.57, "color": "#f6a04d"},
    {"label": "Basement", "depth": 0.79, "color": "#b278c9"},
]


SYNTHETIC_TRACKS = [
    {"label": "GR", "color": "#67d0df", "phase": 0.3},
    {"label": "Rt", "color": "#d8a24a", "phase": 1.1},
    {"label": "RHOB", "color": "#25b99a", "phase": 2.0},
    {"label": "Vp", "color": "#8ea7ff", "phase": 2.8},
    {"label": "Vs", "color": "#f2f5f6", "phase": 3.5},
    {"label": "NMR", "color": "#d889b7", "phase": 4.0},
]


EVIDENCE_DOMAINS = [
    {"label": "Reservoir", "value": 0.78, "color": "#25b99a"},
    {"label": "Hydrate", "value": 0.71, "color": "#67d0df"},
    {"label": "Saturation", "value": 0.55, "color": "#8ea7ff"},
    {"label": "Flow", "value": 0.62, "color": "#f2f5f6"},
    {"label": "QC", "value": 0.86, "color": "#25b99a"},
    {"label": "Stability", "value": 0.69, "color": "#d8a24a"},
]


TARGET_BOUNDARY = [
    {"label": "Measured logs", "lane": "input", "color": "#67d0df"},
    {"label": "Derived physics", "lane": "feature", "color": "#25b99a"},
    {"label": "Targets", "lane": "target", "color": "#d8a24a"},
    {"label": "No leakage", "lane": "guardrail", "color": "#d66a6a"},
]


COHORT_SPLIT = [
    {"label": "Known wells", "count": 14, "color": "#67d0df"},
    {"label": "Train", "count": 8, "color": "#25b99a"},
    {"label": "Validate", "count": 3, "color": "#d8a24a"},
    {"label": "Locked test", "count": 3, "color": "#d66a6a"},
    {"label": "Prediction", "count": 57, "color": "#8ea7ff"},
]


BUILT_NEXT = {
    "built": [
        "Regional atlas",
        "Synthetic log scaffold",
        "Runtime readiness",
        "Physics features",
        "Grouped validation plan",
    ],
    "next": [
        "Workbook mapping",
        "Core-log calibration",
        "Model training",
        "Held-out results",
        "Final deliverables",
    ],
}


BLOCKERS = [
    {"label": "Excel workbook", "affects": "requirements", "severity": "waiting"},
    {"label": "Target fields", "affects": "labels", "severity": "waiting"},
    {"label": "Source library", "affects": "provenance", "severity": "partial"},
]


DELIVERABLES = [
    {"label": "Website figures", "status": "built from public/synthetic visuals"},
    {"label": "Word draft", "status": "align after verified workflow"},
    {"label": "PowerPoint", "status": "replace placeholders with results"},
    {"label": "Approved outputs", "status": "authorized runtime only"},
]
