from __future__ import annotations

import base64
from collections import Counter
from html import escape
import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

from dashboard.approved_data_intake import build_variable_fingerprints, intake_validator_contract_frame
from dashboard.parameter_evidence import (
    default_parameter_evidence_registry_path,
    load_parameter_evidence_registry,
    parameter_evidence_summary_frame,
    validate_parameter_evidence_registry,
)
from dashboard.processing_visuals import render_processing_sketch
from dashboard.source_visual_inventory import (
    default_source_visual_inventory_path,
    load_source_visual_inventory,
    source_visual_inventory_summary_frame,
    validate_source_visual_inventory,
)
from dashboard.runtime.feature_engineering import add_standard_features
from dashboard.runtime.schemas import (
    CHONG_ML_FEATURE_COLUMNS,
    PROJECT_COHORT_ASSUMPTIONS,
    TARGET_LABEL_CONTRACT,
)
from dashboard.stability_sources import (
    active_stability_source_path,
    default_stability_bundle_path,
    default_stability_snapshot_path,
    load_ggd223_permafrost_points,
    load_hydrate_assessment_units,
    stability_bundle_metrics,
    stability_source_kind,
    stability_source_status_frame,
)
from dashboard.stability_products import (
    default_approved_schema_coverage_matrix_path,
    default_g10015_inventory_path,
    default_public_ml_feature_dictionary_path,
    default_public_ml_feature_scaffold_path,
    default_public_ml_leakage_guardrails_path,
    default_public_ml_target_registry_path,
    default_stability_input_scaffold_path,
    default_stability_screen_path,
    default_well_context_path,
    load_approved_schema_coverage_matrix,
    load_g10015_temperature_inventory,
    load_g10015_temperature_profile_points_product,
    load_methane_phase_curve,
    load_public_ml_feature_dictionary,
    load_public_ml_feature_scaffold,
    load_public_ml_feature_scaffold_summary,
    load_public_ml_leakage_guardrails,
    load_public_ml_target_registry,
    load_public_well_stability_context,
    load_stability_input_scaffold,
    load_stability_screen,
    load_stability_temperature_model,
    public_ml_feature_scaffold_summary_frame,
    public_ml_leakage_guardrails_frame,
    public_ml_target_registry_frame,
    stability_input_capability_matrix_frame,
    stability_osl_pull_triggers_frame,
    stability_parameter_readiness_frame,
    stability_context_summary_frame,
    stability_input_scaffold_summary_frame,
    stability_screen_summary_frame,
    stability_website_product_spec_frame,
    temperature_inventory_summary_frame,
)
from dashboard.runtime.validation import (
    curve_coverage_frame,
    grouped_well_split_frame,
    output_readiness_frame,
    project_cohort_plan_frame,
    readiness_frame,
    validate_log_table,
)
from dashboard.well_log_engine import (
    CLASSIFICATION_WORKFLOW,
    EQUATION_LIBRARY,
    HEADER_SCHEMA_BLUEPRINT,
    RANGE_GUIDE,
    PUBLIC_SCIENCE_REFERENCES,
    ROCKTYPE_CONTEXT_GUIDE,
    SCREENING_BANDS,
    SOURCE_LIBRARY_COVERAGE,
    SYNTHETIC_LABEL,
    SWEET_SPOT_GUIDE,
    SWEET_SPOT_EVIDENCE_MODEL,
    VARIABLES,
    cross_well_range_figure,
    csv_bytes,
    figure_html_bytes,
    load_runtime_data,
    model_placeholder_figures,
    nearby_log_calibration,
    screen_intervals,
    sweet_spot_review_table,
    synthetic_core_placeholders,
    variable_range_summary,
    well_log_panel,
)
from dashboard.visual_story_data import (
    BLOCKERS,
    BUILT_NEXT,
    COHORT_SPLIT,
    DELIVERABLES,
    EVIDENCE_DOMAINS,
    EVIDENCE_STACK,
    HEADER_DERIVED_SYNTHETIC_NOTE,
    HYDRATE_DECISION_TREE,
    LAYER_SUMMARY,
    ML_ARCHITECTURE,
    MISSION_OUTCOMES,
    PIPELINE_STAGES,
    SOURCE_ANCHORS,
    STRUCTURE_LAYERS,
    SYNTHETIC_TRACKS,
    TARGET_BOUNDARY,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = PROJECT_ROOT / "05_exports" / "html"
ARCHITECTURE_PATH = PROJECT_ROOT / "docs" / "PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md"
VISION_PATH = PROJECT_ROOT / "docs" / "PROJECT_VISION_GOALS_AND_NEXT_STEPS.md"
FULL_WORKFLOW_ASSET_DIR = (
    PROJECT_ROOT
    / "docs"
    / "project_blueprints"
    / "presentation_assets"
    / "full_workflow_diagram_2026_06_16_v5_3"
)
FULL_WORKFLOW_FLOWCHART = FULL_WORKFLOW_ASSET_DIR / "slide_04_simplified_workflow_v5_3.png"
FULL_WORKFLOW_EXPANDED_FLOWCHART = FULL_WORKFLOW_ASSET_DIR / "full_project_ml_workflow_flowchart_expanded.png"
FULL_WORKFLOW_ML_NETWORK = FULL_WORKFLOW_ASSET_DIR / "ml_pipeline_network_detail_v5.png"
FULL_WORKFLOW_CONTACT_SHEET = FULL_WORKFLOW_ASSET_DIR / "v5_3_workflow_deck_contact_sheet.png"
V5_3_WEBSITE_CAPTURE_DIR = (
    PROJECT_ROOT
    / "docs"
    / "project_blueprints"
    / "presentation_assets"
    / "v5_3_website_captures"
)
FULL_WORKFLOW_DECK = (
    PROJECT_ROOT
    / "docs"
    / "project_blueprints"
    / "V5_3_North_Slope_Gas_Hydrate_ML_Workflow_Slides_2026-06-16.pptx"
)
FULL_WORKFLOW_WORD = (
    PROJECT_ROOT
    / "docs"
    / "project_blueprints"
    / "V5_3_North_Slope_Gas_Hydrate_ML_Workflow_Companion_2026-06-16.docx"
)
FULL_WORKFLOW_DRIVE_SLIDES_URL = "https://docs.google.com/presentation/d/1kP0icjCLpldXZX80eww27IIokG1s3VbM5bSXiGLk8Sw"
FULL_WORKFLOW_DRIVE_DOC_URL = "https://docs.google.com/document/d/1QcF-31U77_MyPHnrBSYFZSswFyIzO8P3pMLBSTIMgMQ"
SOURCE_VISUAL_INVENTORY = default_source_visual_inventory_path(PROJECT_ROOT)
APPROVED_DATA_FIELD_ROLE_TABLE = (
    PROJECT_ROOT
    / "data"
    / "public_ml_products"
    / "approved_data_field_role_table_2026-06-15.csv"
)
APPROVED_DATA_INTAKE_TEMPLATE = (
    PROJECT_ROOT
    / "data"
    / "public_ml_products"
    / "approved_data_intake_template_2026-06-15.csv"
)
APPROVED_DATA_INTAKE_VALIDATION_SCHEMA = (
    PROJECT_ROOT
    / "data"
    / "public_ml_products"
    / "approved_data_intake_validation_schema_2026-06-15.csv"
)
FIRST_MODEL_OUTPUT_SCHEMA = (
    PROJECT_ROOT
    / "data"
    / "public_ml_products"
    / "first_model_output_schema_2026-06-15.csv"
)
APPROVED_DATA_SOURCE_COLUMN_REGISTRY_TEMPLATE = (
    PROJECT_ROOT
    / "data"
    / "public_ml_products"
    / "approved_data_source_column_registry_template_2026-06-15.csv"
)
APPROVED_DATA_WELL_DEPTH_INDEX_TEMPLATE = (
    PROJECT_ROOT
    / "data"
    / "public_ml_products"
    / "approved_data_well_depth_index_template_2026-06-15.csv"
)
APPROVED_DATA_X_ALLOWED_CANDIDATE_TEMPLATE = (
    PROJECT_ROOT
    / "data"
    / "public_ml_products"
    / "approved_data_x_allowed_candidate_template_2026-06-15.csv"
)
APPROVED_DATA_Y_TARGET_REGISTRY_TEMPLATE = (
    PROJECT_ROOT
    / "data"
    / "public_ml_products"
    / "approved_data_y_target_registry_template_2026-06-15.csv"
)
FIRST_MODEL_OUTPUT_SCHEMA_TEMPLATE = (
    PROJECT_ROOT
    / "data"
    / "public_ml_products"
    / "first_model_output_schema_template_2026-06-15.csv"
)
VARIABLE_FINGERPRINT_TEMPLATE = (
    PROJECT_ROOT
    / "data"
    / "public_ml_products"
    / "variable_fingerprint_template_2026-06-15.csv"
)
PUBLIC_PARAMETER_EVIDENCE_REGISTRY = default_parameter_evidence_registry_path(PROJECT_ROOT)
INTAKE_READINESS_REPORT_DIR = PROJECT_ROOT / "data" / "public_ml_products" / "intake_readiness_reports"
DEMO_HEADER_AUDIT_CSV = INTAKE_READINESS_REPORT_DIR / "demo_header_audit_2026-06-15.csv"
DEMO_HEADER_AUDIT_JSON = INTAKE_READINESS_REPORT_DIR / "demo_header_audit_2026-06-15.json"
APPROVED_DATA_INTAKE_READINESS_REPORT = (
    PROJECT_ROOT / "docs" / "APPROVED_DATA_INTAKE_READINESS_REPORT_2026-06-15.md"
)
OSL_HEADER_AUDIT_RUNBOOK = PROJECT_ROOT / "docs" / "OSL_APPROVED_DATA_HEADER_AUDIT_RUNBOOK_2026-06-15.md"
IGNORED_DIRS = {
    ".git",
    ".ipynb_checkpoints",
    "__pycache__",
    ".venv-dashboard",
    "configs_local",
    "data_runtime",
    "logs_runtime",
    "models_runtime",
    "outputs_runtime",
    "source_library",
}

REGIONAL_SCENE = EXPORT_DIR / "north_slope_plotly_advanced.html"
STRUCTURAL_SCENES = {
    "Master structural scene": EXPORT_DIR / "north_slope_master_analysis_scene.html",
    "Full-resolution structural scene": EXPORT_DIR
    / "north_slope_master_analysis_scene_full_no_simplify.html",
}
MASTER_3D = PROJECT_ROOT / "03_data_final" / "master_layers" / "north_slope_master_3d_surfaces.parquet"

STABILITY_SCREEN_STATUS_STYLES = {
    "calculated": {
        "label": "Calculated screen interval",
        "color": "#2563eb",
        "size": 11,
        "opacity": 0.92,
    },
    "calculated_no_stable_interval": {
        "label": "Calculated, no stable interval",
        "color": "#111827",
        "size": 9,
        "opacity": 0.82,
    },
    "blocked_phase_curve_range_insufficient": {
        "label": "Blocked: phase curve range",
        "color": "#d97706",
        "size": 7,
        "opacity": 0.72,
    },
    "blocked_missing_temperature_profile": {
        "label": "Blocked: missing temperature profile",
        "color": "#94a3b8",
        "size": 5,
        "opacity": 0.42,
    },
    "blocked_missing_depth": {
        "label": "Blocked: missing depth",
        "color": "#64748b",
        "size": 6,
        "opacity": 0.55,
    },
    "outside_au_context": {
        "label": "Outside public AU context",
        "color": "#7c3aed",
        "size": 6,
        "opacity": 0.58,
    },
}

STABILITY_SCREEN_CONFIDENCE_COLORS = {
    "high_source_control": "#2563eb",
    "medium_source_control": "#0891b2",
    "low_source_control": "#d97706",
}

BLANK_REASON_DETAILS = {
    "calculated": {
        "label": "Calculated baseline interval",
        "meaning": "All current public gates passed and top/base/thickness were written.",
        "next_step": "Use as screened interval only; compare with logs/core before any hydrate claim.",
    },
    "calculated_no_stable_interval": {
        "label": "No stable interval in modeled range",
        "meaning": "Inputs were available, but the modeled pressure-temperature path did not enter the baseline stability window.",
        "next_step": "Keep as a valid negative screen row; revisit only if temperature or phase assumptions change.",
    },
    "blocked_missing_temperature_profile": {
        "label": "Blank: no matched temperature profile",
        "meaning": "The well did not connect to a direct public G10015 temperature profile under the current baseline crosswalk.",
        "next_step": "Audit name/code/coordinate crosswalks or add a separate proxy-temperature sensitivity screen if approved.",
    },
    "blocked_missing_depth": {
        "label": "Blank: missing usable depth",
        "meaning": "The public well record lacks the depth needed for pressure and interval screening.",
        "next_step": "Recover/validate a public depth field or keep this row as a data gap.",
    },
    "blocked_phase_curve_range_insufficient": {
        "label": "Blank: phase-curve range insufficient",
        "meaning": "A direct temperature profile exists, but the modeled interval does not close inside the cited phase-curve lookup range.",
        "next_step": "Extend the cited lookup/model range or keep the row blocked.",
    },
    "outside_au_context": {
        "label": "Context only: outside public AU",
        "meaning": "The well falls outside the committed USGS hydrate assessment-unit context.",
        "next_step": "Do not use for public hydrate screening unless the spatial context is revised and cited.",
    },
}

TEMPERATURE_PROXY_TIER_DETAILS = {
    "direct_g10015_profile_match": {
        "label": "Direct G10015 profile match",
        "meaning": "Current baseline tier. A public temperature profile is matched to the screen row.",
        "allowed_use": "Allowed in the baseline screen.",
        "color": "#2563eb",
        "size": 9,
        "opacity": 0.9,
    },
    "proxy_candidate_near_g10015_control": {
        "label": "Proxy candidate: within 50 km",
        "meaning": "No direct profile match, but the well is within 50 km of a located G10015 control.",
        "allowed_use": "Sensitivity/planning only until mentor approves proxy assumptions.",
        "color": "#0891b2",
        "size": 7,
        "opacity": 0.72,
    },
    "proxy_candidate_regional_g10015_control": {
        "label": "Proxy candidate: 50-100 km",
        "meaning": "No direct profile match; nearest located G10015 control is regional rather than local.",
        "allowed_use": "Regional sensitivity only; not a baseline stability result.",
        "color": "#d97706",
        "size": 6,
        "opacity": 0.62,
    },
    "distant_from_g10015_controls": {
        "label": "Distant from located G10015 controls",
        "meaning": "No direct profile match and more than 100 km from a located G10015 control.",
        "allowed_use": "Needs another cited temperature source before calculation.",
        "color": "#ef4444",
        "size": 6,
        "opacity": 0.55,
    },
    "missing_well_depth": {
        "label": "Missing well depth",
        "meaning": "Temperature proxying cannot help until the well depth is available.",
        "allowed_use": "Data recovery task.",
        "color": "#64748b",
        "size": 6,
        "opacity": 0.5,
    },
    "outside_public_au_context": {
        "label": "Outside public AU context",
        "meaning": "Outside the committed hydrate assessment-unit context.",
        "allowed_use": "Context only.",
        "color": "#7c3aed",
        "size": 6,
        "opacity": 0.55,
    },
    "temperature_control_location_gap": {
        "label": "Temperature-control location gap",
        "meaning": "The inventory code lacks a committed coordinate crosswalk or the row lacks location.",
        "allowed_use": "Crosswalk/source cleanup task.",
        "color": "#475569",
        "size": 6,
        "opacity": 0.55,
    },
}
MASTER_2D = PROJECT_ROOT / "03_data_final" / "master_layers" / "north_slope_master_2d_layers.parquet"
STRUCTURAL_HORIZONS = ["NStopo", "NSLCU", "NSshublik", "NSbasement"]
CONTEXT_OVERLAYS = [
    "North Slope study-area boundary",
    "Assessment-unit outlines",
    "North Slope public wells",
]
TOPIC5_EVIDENCE_ATLAS_PRIORITY = [
    {
        "Evidence object": "Regional atlas and satellite-style context",
        "Why it moved up": "Sets the public, basin-scale context before any interval receives an ML score.",
        "How AI uses it": "Constrains confidence, flags out-of-context predictions, and supports reviewer triage.",
        "Boundary": "Context feature only; it does not label hydrate intervals.",
    },
    {
        "Evidence object": "Assessment units, structure, 2D/3D seismic footprints",
        "Why it moved up": "Explains where the well-log evidence sits inside the larger North Slope system.",
        "How AI uses it": "Groups wells, preserves holdout logic, and keeps regional comparability visible.",
        "Boundary": "Public-source atlas layer; not a replacement for approved logs or cores.",
    },
    {
        "Evidence object": "Well-log scaffold",
        "Why it moved up": "Removes the blank Topic 5 placeholder and shows the exact panel expected in outputs.",
        "How AI uses it": "Turns GR, Rt, RHOB, NMR, Vp, and Vs into QC'd physics features and review intervals.",
        "Boundary": "Synthetic/header-derived in this hosted site.",
    },
    {
        "Evidence object": "Output visualization pack",
        "Why it moved up": "Connects model results to explainable figures rather than hidden table rows.",
        "How AI uses it": "Displays interval classification, saturation proxy, uncertainty, and calibration behavior.",
        "Boundary": "Export scaffold until authorized runtime data are loaded.",
    },
]

TOPIC5_SCAFFOLD_OUTPUTS = [
    {
        "Output": "Well-log panel",
        "What it shows": "Depth-aligned GR, Rt, RHOB, NMR, Vp, Vs, and highlighted review intervals.",
        "AI contribution": "Screens curve agreement, QC flags, hydrate-supportive intervals, and competing explanations.",
    },
    {
        "Output": "Variable range table",
        "What it shows": "Per-well ranges and medians for model-ready input variables.",
        "AI contribution": "Catches missing curves, out-of-range values, and feature distributions before fitting.",
    },
    {
        "Output": "Cross-well comparison",
        "What it shows": "The same variable compared across the synthetic well cohort.",
        "AI contribution": "Supports whole-well validation and prevents nearby-depth leakage from looking like skill.",
    },
    {
        "Output": "Interval interpretation table",
        "What it shows": "Candidate intervals, evidence domains, blockers, and uncertainty flags.",
        "AI contribution": "Separates hydrate classification, saturation proxy, reservoir quality, and review priority.",
    },
    {
        "Output": "Model diagnostic panels",
        "What it shows": "Placeholder confusion matrix and calibration curve for the future approved-data run.",
        "AI contribution": "Shows where the classifier abstains, fails, or needs calibration before delivery.",
    },
]

TOPIC5_AI_WORKFLOW = [
    {
        "Workflow step": "Prepare inputs",
        "AI role": "Map approved workbook headers into canonical log, QC, target, and derived-feature roles.",
        "Human check": "Confirm units, depth alignment, missing curves, and sensitive-data boundaries.",
    },
    {
        "Workflow step": "Engineer features",
        "AI role": "Compute porosity, Vsh, Vp/Vs, acoustic impedance, lambda-rho, and mu-rho consistently.",
        "Human check": "Review assumptions where tool response, shale, gas, ice, or borehole condition may mimic hydrate.",
    },
    {
        "Workflow step": "Model outcomes",
        "AI role": "Use separate classification, saturation/regression, and uncertainty outputs.",
        "Human check": "Keep saturation fields, phase labels, and sweet-spot ranks out of the feature inputs.",
    },
    {
        "Workflow step": "Explain outputs",
        "AI role": "Attach evidence domains and visualization outputs to every flagged interval.",
        "Human check": "Approve final hydrate calls only after source, core/log, and regional context review.",
    },
]

SURFACE_CATALOG = {
    "NStopo": {
        "Label": "Topographic reference",
        "Description": "Near-surface reference horizon used to orient the structural stack.",
        "Color": "#4daf4a",
    },
    "NSLCU": {
        "Label": "Lower Cretaceous unconformity",
        "Description": "Regional unconformity surface used as a subsurface structural reference.",
        "Color": "#377eb8",
    },
    "NSshublik": {
        "Label": "Shublik surface",
        "Description": "Regional Shublik structural horizon used for deeper framework context.",
        "Color": "#ff7f00",
    },
    "NSbasement": {
        "Label": "Basement surface",
        "Description": "Deep basement structural reference for regional basin geometry.",
        "Color": "#984ea3",
    },
    "NStopo-LCU": {
        "Label": "Topography to LCU interval",
        "Description": "Thickness-style grid between the topographic reference and LCU.",
        "Color": "#66c2a5",
    },
    "NSLCU-Shublik": {
        "Label": "LCU to Shublik interval",
        "Description": "Thickness-style grid between LCU and the Shublik surface.",
        "Color": "#fc8d62",
    },
    "NSshublik-basement": {
        "Label": "Shublik to basement interval",
        "Description": "Thickness-style grid between the Shublik and basement surfaces.",
        "Color": "#8da0cb",
    },
    "NStopo-basement": {
        "Label": "Topography to basement interval",
        "Description": "Full reference interval between topography and basement.",
        "Color": "#e78ac3",
    },
}

PAGES = [
    "Overview",
    "Explore North Slope",
    "Analyze Hydrates",
    "Project Plan",
]

PAGE_ALIASES = {
    "Welcome": "Overview",
    "Project Roadmap": "Project Plan",
    "North Slope Sweet Spots": "Analyze Hydrates",
    "Log Scaffold": "Analyze Hydrates",
    "Future Well-Log Engine": "Analyze Hydrates",
    "Well-Log Engine": "Analyze Hydrates",
    "Well Log Scaffold": "Analyze Hydrates",
    "Regional Atlas": "Explore North Slope",
    "Structural Explorer": "Explore North Slope",
    "Data Library": "Explore North Slope",
    "Research Framework": "Project Plan",
}

LAYER_CATALOG = [
    {
        "Layer": "Well-bottom-hole locations",
        "Role": "Regional well inventory",
        "Records": "10,250",
        "Geometry": "Point",
        "Status": "Cleaned + enriched",
        "Source category": "Public-source GIS",
        "Boundary tag": "PUBLIC-SOURCE ATLAS",
        "Description": "Well-bottom-hole inventory used for regional orientation and map filtering.",
        "Location": "03_data_final/core_layers/clean_well_locations.parquet",
    },
    {
        "Layer": "2D seismic coverage",
        "Role": "Regional line coverage",
        "Records": "26 surveys",
        "Geometry": "Line / MultiLine",
        "Status": "Cleaned + enriched",
        "Source category": "Public-source GIS",
        "Boundary tag": "PUBLIC-SOURCE ATLAS",
        "Description": "Regional 2D line inventory used to show available seismic context.",
        "Location": "03_data_final/core_layers/clean_2d_seismic.parquet",
    },
    {
        "Layer": "3D seismic inventory",
        "Role": "Survey footprint coverage",
        "Records": "36 surveys",
        "Geometry": "Polygon / MultiPolygon",
        "Status": "Cleaned + enriched",
        "Source category": "Public-source GIS",
        "Boundary tag": "PUBLIC-SOURCE ATLAS",
        "Description": "Polygon footprints showing areas with 3D seismic inventory coverage.",
        "Location": "03_data_final/core_layers/clean_3d_seismic.parquet",
    },
    {
        "Layer": "North Slope assessment units",
        "Role": "Regional petroleum-system framework",
        "Records": "6 units",
        "Geometry": "Polygon / MultiPolygon",
        "Status": "Cleaned + enriched",
        "Source category": "Public-source geology",
        "Boundary tag": "PUBLIC-SOURCE ATLAS",
        "Description": "Regional assessment units used as petroleum-system context.",
        "Location": "03_data_final/core_layers/north_slope_assessment_units.parquet",
    },
    {
        "Layer": "North Slope extent",
        "Role": "Study-area boundary",
        "Records": "1 boundary",
        "Geometry": "Polygon",
        "Status": "Cleaned + enriched",
        "Source category": "Project-derived boundary",
        "Boundary tag": "PUBLIC-SOURCE ATLAS",
        "Description": "Study-area outline for North Slope-focused visualization.",
        "Location": "03_data_final/core_layers/north_slope_extent.parquet",
    },
    {
        "Layer": "Structural depth grids",
        "Role": "Subsurface framework",
        "Records": "8 XYZ grids",
        "Geometry": "Grid points + rasters",
        "Status": "Processed",
        "Source category": "Public-source structural grids",
        "Boundary tag": "PUBLIC-SOURCE ATLAS",
        "Description": "Raw XYZ structural references and interval grids used in the 3D explorer.",
        "Location": "raw_data/north_slope_depth_grids/",
    },
    {
        "Layer": "GIS-ready surfaces",
        "Role": "Topography, Shublik, and basement surfaces",
        "Records": "3 surfaces",
        "Geometry": "Point GeoJSON + Parquet",
        "Status": "Dashboard ready",
        "Source category": "Project-derived GIS output",
        "Boundary tag": "PUBLIC-SOURCE ATLAS",
        "Description": "Processed surface points exported for GIS and lightweight inspection.",
        "Location": "03_data_final/gis_ready_surfaces/",
    },
]

FRAMEWORK_STAGES = [
    ("01", "Environment", "Pressure-temperature boundary conditions"),
    ("02", "Tectonics", "Migration pathways, burial history, and traps"),
    ("03", "Deposition", "Reservoir architecture and sand distribution"),
    ("04", "Reservoir", "Porosity, permeability, continuity, and compartmentalization"),
    ("05", "Physics", "Elastic, electrical, and geomechanical response"),
    ("06", "Logs", "Wireline measurements and derived attributes"),
    ("07", "Interpretation", "Failure-aware phase discrimination"),
    ("08", "ML", "Physics-constrained classification and ranking"),
    ("09", "Exploitation", "Separate resource density from producibility"),
]


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --atlas-navy: #123447;
            --atlas-teal: #167d8d;
            --atlas-ice: #edf7f8;
            --atlas-sand: #f4efe6;
            --atlas-orange: #d9773d;
        }
        .stApp {
            background: linear-gradient(180deg, #f8fbfb 0%, #ffffff 36%);
        }
        [data-testid="stSidebar"] {
            background: #123447;
        }
        [data-testid="stSidebar"] * {
            color: #f7fbfc;
        }
        [data-testid="stSidebar"] .stRadio label {
            padding: 0.18rem 0;
        }
        .atlas-kicker {
            color: #167d8d;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.14em;
            text-transform: uppercase;
        }
        .atlas-hero {
            background: linear-gradient(125deg, #123447 0%, #176477 70%, #167d8d 100%);
            border-radius: 8px;
            color: white;
            padding: 2.4rem 2.7rem;
            margin-bottom: 1.1rem;
        }
        .atlas-hero h1 {
            color: white;
            font-size: 2.45rem;
            line-height: 1.08;
            margin: 0.3rem 0 0.75rem;
        }
        .atlas-hero p {
            color: #e8f6f7;
            font-size: 1.05rem;
            max-width: 860px;
        }
        .atlas-card {
            background: white;
            border: 1px solid #d9e7e8;
            border-radius: 8px;
            min-height: 162px;
            padding: 1.1rem 1.2rem;
        }
        .atlas-card h4 {
            color: #123447;
            margin: 0.1rem 0 0.4rem;
        }
        .atlas-step {
            background: #edf7f8;
            border-left: 4px solid #167d8d;
            border-radius: 8px;
            margin: 0.42rem 0;
            padding: 0.66rem 0.85rem;
        }
        .path-card {
            background: #ffffff;
            border: 1px solid #d9e7e8;
            border-radius: 8px;
            min-height: 118px;
            padding: 1rem;
        }
        .path-card h4 {
            color: #123447;
            margin: 0 0 0.35rem;
        }
        .path-card p {
            color: #49636b;
            margin: 0;
        }
        .boundary-badge {
            background: #f4efe6;
            border: 1px solid #e4d8c4;
            border-radius: 8px;
            color: #5d4b2a;
            display: inline-block;
            font-size: 0.86rem;
            font-weight: 700;
            margin: 0.35rem 0 0.75rem;
            padding: 0.36rem 0.62rem;
        }
        .atlas-step strong {
            color: #123447;
        }
        .atlas-boundary {
            background: #f4efe6;
            border: 1px solid #e4d8c4;
            border-radius: 10px;
            padding: 0.8rem 1rem;
        }
        .roadmap-status {
            background: #ffffff;
            border: 1px solid #d9e7e8;
            border-radius: 12px;
            padding: 0.9rem 1rem;
            margin-bottom: 0.7rem;
        }
        .roadmap-status strong {
            color: #123447;
        }
        .roadmap-next {
            background: linear-gradient(135deg, #edf7f8 0%, #ffffff 100%);
            border: 1px solid #bcdcdf;
            border-left: 5px solid #167d8d;
            border-radius: 12px;
            padding: 1rem 1.1rem;
            margin: 0.8rem 0 1rem;
        }
        .roadmap-next strong {
            color: #123447;
        }
        .roadmap-mobile {
            display: none;
        }
        .roadmap-table {
            border-collapse: collapse;
            font-size: 0.88rem;
            width: 100%;
        }
        .roadmap-table th {
            background: #edf7f8;
            color: #123447;
            text-align: left;
        }
        .roadmap-table th,
        .roadmap-table td {
            border: 1px solid #d9e7e8;
            padding: 0.55rem;
            vertical-align: top;
        }
        .roadmap-card {
            background: #ffffff;
            border: 1px solid #d9e7e8;
            border-radius: 12px;
            padding: 0.9rem 1rem;
            margin-bottom: 0.7rem;
        }
        .roadmap-card-title {
            color: #123447;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }
        .roadmap-pill {
            background: #edf7f8;
            border-radius: 999px;
            color: #166674;
            display: inline-block;
            font-size: 0.76rem;
            font-weight: 700;
            margin-bottom: 0.55rem;
            padding: 0.2rem 0.55rem;
        }
        .roadmap-label {
            color: #527078;
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }
        [data-testid="stDataFrame"] {
            overflow-x: auto;
        }
        [data-baseweb="tab-list"] {
            overflow-x: auto;
            scrollbar-width: thin;
        }
        [data-baseweb="tab"] {
            flex: 0 0 auto;
        }
        @media (max-width: 768px) {
            .block-container {
                padding: 1rem 0.8rem 4rem;
                max-width: 100%;
            }
            .atlas-hero {
                border-radius: 12px;
                padding: 1.35rem 1.1rem;
                margin-bottom: 0.8rem;
            }
            .atlas-hero h1 {
                font-size: 1.85rem;
                line-height: 1.12;
            }
            .atlas-hero p {
                font-size: 0.96rem;
            }
            .atlas-card {
                min-height: auto;
                margin-bottom: 0.65rem;
            }
            h1 {
                font-size: 1.85rem !important;
            }
            h2 {
                font-size: 1.45rem !important;
            }
            h3 {
                font-size: 1.2rem !important;
            }
            [data-testid="stHorizontalBlock"] {
                flex-direction: column;
                gap: 0.55rem;
            }
            [data-testid="stHorizontalBlock"] > div {
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 0 !important;
            }
            [data-testid="stMetric"] {
                border-bottom: 1px solid #e3ecec;
                padding-bottom: 0.45rem;
            }
            iframe {
                max-width: 100%;
            }
            .stButton button,
            .stDownloadButton button {
                width: 100%;
            }
            .roadmap-desktop {
                display: none;
            }
            .roadmap-mobile {
                display: block;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def markdown_section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    if marker not in text:
        return ""
    section = text.split(marker, 1)[1]
    return section.split("\n## ", 1)[0].strip()


def markdown_table(section: str) -> pd.DataFrame:
    lines = [line.strip() for line in section.splitlines() if line.strip().startswith("|")]
    if len(lines) < 2:
        return pd.DataFrame()
    headers = [cell.strip() for cell in lines[0].strip("|").split("|")]
    rows = []
    for line in lines[2:]:
        cells = [cell.strip().replace("`", "") for cell in line.strip("|").split("|")]
        if len(cells) == len(headers):
            rows.append(cells)
    return pd.DataFrame(rows, columns=headers)


def architecture_content() -> str:
    if not ARCHITECTURE_PATH.exists():
        return ""
    return ARCHITECTURE_PATH.read_text(encoding="utf-8")


def vision_content() -> str:
    if not VISION_PATH.exists():
        return ""
    return VISION_PATH.read_text(encoding="utf-8")


def roadmap_cards(workstreams: pd.DataFrame) -> str:
    cards = []
    for row in workstreams.to_dict(orient="records"):
        safe = {key: escape(str(value)) for key, value in row.items()}
        cards.append(
            f"""
            <div class="roadmap-card">
              <div class="roadmap-card-title">{safe["ID"]} · {safe["Workstream"]}</div>
              <div class="roadmap-pill">{safe["Status"]}</div>
              <div class="roadmap-label">Next activity</div>
              <div>{safe["Immediate activity"]}</div>
              <div class="roadmap-label" style="margin-top:0.65rem">Dependency</div>
              <div>{safe["Dependency"]}</div>
            </div>
            """
        )
    return '<div class="roadmap-mobile">' + "".join(cards) + "</div>"


def format_bytes(size: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:,.1f} {unit}"
        value /= 1024
    return f"{size:,} B"


@st.cache_data
def project_files() -> list[dict[str, object]]:
    rows = []
    for path in PROJECT_ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(PROJECT_ROOT)
        if any(part in IGNORED_DIRS for part in relative.parts):
            continue
        rows.append(
            {
                "Path": relative.as_posix(),
                "Type": path.suffix.lower() or "(none)",
                "Size": format_bytes(path.stat().st_size),
                "Bytes": path.stat().st_size,
            }
        )
    return sorted(rows, key=lambda row: str(row["Path"]).lower())


@st.cache_data
def read_scene(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


@st.cache_data
def load_structural_surfaces() -> pd.DataFrame:
    return pd.read_parquet(
        MASTER_3D,
        columns=["x_3338", "y_3338", "lon", "lat", "depth_m", "surface_name"],
    )


@st.cache_data
def load_regional_context() -> pd.DataFrame:
    layers = pd.read_parquet(
        MASTER_2D,
        columns=["layer_name", "feature_id", "vertex_order", "lon", "lat", "depth_m", "au_name"],
    )
    return layers[layers["layer_name"].isin(["extent", "assessment_units", "wells"])].copy()


@st.cache_data
def load_north_slope_wells() -> pd.DataFrame:
    context = load_regional_context()
    extent = context[context["layer_name"] == "extent"]
    wells = context[context["layer_name"] == "wells"].copy()
    return wells[
        wells["lon"].between(extent["lon"].min(), extent["lon"].max())
        & wells["lat"].between(extent["lat"].min(), extent["lat"].max())
    ]


def sample_rows(df: pd.DataFrame, max_rows: int) -> pd.DataFrame:
    if len(df) <= max_rows:
        return df
    step = max(1, len(df) // max_rows)
    return df.iloc[::step].head(max_rows)


def grid_surface(surface: pd.DataFrame, max_cells: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    stride = max(1, round((len(surface) / max_cells) ** 0.5))
    index = "y_3338"
    columns = "x_3338"
    lon = surface.pivot(index=index, columns=columns, values="lon").iloc[::stride, ::stride]
    lat = surface.pivot(index=index, columns=columns, values="lat").iloc[::stride, ::stride]
    depth = surface.pivot(index=index, columns=columns, values="depth_m").iloc[::stride, ::stride]
    return lon, lat, depth


def add_context_line(
    figure: go.Figure,
    rows: pd.DataFrame,
    name: str,
    color: str,
    width: int,
    showlegend: bool = True,
) -> None:
    figure.add_trace(
        go.Scatter3d(
            x=rows["lon"],
            y=rows["lat"],
            z=[0] * len(rows),
            mode="lines",
            name=name,
            showlegend=showlegend,
            line={"color": color, "width": width},
            hovertemplate=f"<b>{name}</b><br>Longitude: %{{x:.2f}}<br>Latitude: %{{y:.2f}}<extra></extra>",
        )
    )


def build_geographic_structural_figure(
    selected_surfaces: list[str],
    cells_per_surface: int,
    selected_overlays: list[str],
) -> go.Figure:
    surfaces = load_structural_surfaces()
    figure = go.Figure()

    for surface_name in selected_surfaces:
        surface = surfaces[surfaces["surface_name"] == surface_name]
        lon, lat, depth = grid_surface(surface, cells_per_surface)
        metadata = SURFACE_CATALOG[surface_name]
        figure.add_trace(
            go.Surface(
                x=lon,
                y=lat,
                z=depth,
                name=metadata["Label"],
                colorscale=[[0, metadata["Color"]], [1, metadata["Color"]]],
                opacity=0.72,
                showscale=False,
                showlegend=True,
                hovertemplate=(
                    f"<b>{metadata['Label']}</b><br>"
                    "Longitude: %{x:.2f}<br>"
                    "Latitude: %{y:.2f}<br>"
                    "Depth: %{z:,.0f} m<extra></extra>"
                ),
            )
        )

    context = load_regional_context()
    if "North Slope study-area boundary" in selected_overlays:
        extent = context[context["layer_name"] == "extent"].sort_values("vertex_order")
        add_context_line(figure, extent, "North Slope study-area boundary", "#111111", 8)

    if "Assessment-unit outlines" in selected_overlays:
        assessment_units = context[context["layer_name"] == "assessment_units"]
        for index, (_, rows) in enumerate(assessment_units.groupby("feature_id")):
            rows = rows.sort_values("vertex_order")
            rows = sample_rows(rows, 400)
            add_context_line(
                figure,
                rows,
                "Assessment-unit outlines",
                "#d9773d",
                4,
                showlegend=index == 0,
            )

    if "North Slope public wells" in selected_overlays:
        wells = sample_rows(load_north_slope_wells(), 1800)
        figure.add_trace(
            go.Scatter3d(
                x=wells["lon"],
                y=wells["lat"],
                z=wells["depth_m"],
                mode="markers",
                name="North Slope public wells",
                marker={"size": 2.8, "color": "#111111", "opacity": 0.65},
                hovertemplate=(
                    "<b>North Slope public well</b><br>"
                    "Longitude: %{x:.2f}<br>"
                    "Latitude: %{y:.2f}<extra></extra>"
                ),
            )
        )

    figure.update_layout(
        height=760,
        margin={"l": 0, "r": 0, "t": 40, "b": 0},
        legend={"orientation": "h", "y": 1.02, "x": 0},
        scene={
            "xaxis_title": "Longitude",
            "yaxis_title": "Latitude",
            "zaxis_title": "Depth (m, positive downward)",
            "zaxis": {"autorange": "reversed"},
            "aspectmode": "manual",
            "aspectratio": {"x": 1.8, "y": 1, "z": 0.55},
            "camera": {"eye": {"x": 1.55, "y": -1.75, "z": 1.05}},
        },
    )
    return figure


@st.cache_data
def cached_stability_source_status(bundle_root: str) -> pd.DataFrame:
    return stability_source_status_frame(Path(bundle_root))


@st.cache_data
def cached_stability_bundle_metrics(bundle_root: str) -> dict[str, object]:
    return stability_bundle_metrics(Path(bundle_root))


@st.cache_data
def cached_ggd223_points(bundle_root: str) -> pd.DataFrame:
    points = load_ggd223_permafrost_points(Path(bundle_root))
    return pd.DataFrame(points.drop(columns="geometry", errors="ignore"))


@st.cache_data
def cached_hydrate_assessment_units(bundle_root: str):
    return load_hydrate_assessment_units(Path(bundle_root))


@st.cache_data
def cached_public_well_stability_context(project_root: str) -> pd.DataFrame:
    return load_public_well_stability_context(Path(project_root))


@st.cache_data
def cached_g10015_temperature_inventory(project_root: str) -> pd.DataFrame:
    return load_g10015_temperature_inventory(Path(project_root))


@st.cache_data
def cached_g10015_temperature_profile_points(project_root: str) -> pd.DataFrame:
    return load_g10015_temperature_profile_points_product(Path(project_root))


@st.cache_data
def cached_public_ml_feature_scaffold(project_root: str) -> pd.DataFrame:
    return load_public_ml_feature_scaffold(Path(project_root))


@st.cache_data
def cached_public_ml_feature_scaffold_summary(project_root: str) -> pd.DataFrame:
    return load_public_ml_feature_scaffold_summary(Path(project_root))


@st.cache_data
def cached_public_ml_feature_dictionary(project_root: str) -> pd.DataFrame:
    return load_public_ml_feature_dictionary(Path(project_root))


@st.cache_data
def cached_public_ml_target_registry(project_root: str) -> pd.DataFrame:
    return load_public_ml_target_registry(Path(project_root))


@st.cache_data
def cached_public_ml_leakage_guardrails(project_root: str) -> pd.DataFrame:
    return load_public_ml_leakage_guardrails(Path(project_root))


@st.cache_data
def cached_approved_schema_coverage_matrix(project_root: str) -> pd.DataFrame:
    return load_approved_schema_coverage_matrix(Path(project_root))


@st.cache_data
def cached_approved_data_field_role_table(project_root: str) -> pd.DataFrame:
    path = Path(project_root) / "data" / "public_ml_products" / "approved_data_field_role_table_2026-06-15.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data
def cached_parameter_evidence_registry(project_root: str) -> pd.DataFrame:
    return load_parameter_evidence_registry(Path(project_root))


@st.cache_data
def cached_source_visual_inventory(project_root: str) -> pd.DataFrame:
    return load_source_visual_inventory(Path(project_root))


@st.cache_data
def cached_stability_input_scaffold(project_root: str) -> pd.DataFrame:
    return load_stability_input_scaffold(Path(project_root))


@st.cache_data
def cached_stability_screen(project_root: str) -> pd.DataFrame:
    return load_stability_screen(Path(project_root))


@st.cache_data
def cached_stability_temperature_model(project_root: str) -> pd.DataFrame:
    return load_stability_temperature_model(Path(project_root))


@st.cache_data
def cached_methane_phase_curve(project_root: str) -> pd.DataFrame:
    return load_methane_phase_curve(Path(project_root))


def project_relative_or_absolute(path: Path) -> str:
    try:
        return path.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return str(path)


def png_data_uri(path: Path) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def polygon_parts(geometry):
    if geometry is None or geometry.is_empty:
        return []
    if geometry.geom_type == "Polygon":
        return [geometry]
    if geometry.geom_type == "MultiPolygon":
        return list(geometry.geoms)
    return []


def build_stability_source_figure(
    permafrost_points: pd.DataFrame,
    assessment_units,
) -> go.Figure:
    figure = go.Figure()
    has_traces = False

    if not assessment_units.empty:
        for index, (_, row) in enumerate(assessment_units.iterrows()):
            assessment_name = row.get("ASSESSNAME", "Gas hydrate assessment unit")
            for polygon in polygon_parts(row.geometry):
                x, y = polygon.exterior.xy
                figure.add_trace(
                    go.Scattergeo(
                        lon=list(x),
                        lat=list(y),
                        mode="lines",
                        name="USGS hydrate AUs",
                        legendgroup="USGS hydrate AUs",
                        showlegend=index == 0,
                        line={"color": "#d9773d", "width": 2},
                        hovertemplate=(
                            f"<b>{escape(str(assessment_name))}</b><br>"
                            "USGS gas hydrate assessment unit<extra></extra>"
                        ),
                    )
                )
                has_traces = True

    if not permafrost_points.empty:
        figure.add_trace(
            go.Scattergeo(
                lon=permafrost_points["longitude"],
                lat=permafrost_points["latitude"],
                mode="markers",
                name="GGD223 permafrost controls",
                marker={
                    "size": 9,
                    "color": permafrost_points["permafrost_depth_m"],
                    "colorscale": "Viridis",
                    "line": {"color": "#ffffff", "width": 0.8},
                    "colorbar": {"title": "pf depth m"},
                },
                text=permafrost_points["well_designation"],
                customdata=permafrost_points[["code", "permafrost_depth_m", "elevation_m"]],
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Code: %{customdata[0]}<br>"
                    "Permafrost depth: %{customdata[1]} m<br>"
                    "Elevation: %{customdata[2]} m<br>"
                    "Lon/lat: %{lon:.2f}, %{lat:.2f}<extra></extra>"
                ),
            )
        )
        has_traces = True

    figure.update_layout(
        height=520,
        margin={"l": 0, "r": 0, "t": 10, "b": 0},
        legend={"orientation": "h", "y": 1.03, "x": 0},
        geo={
            "scope": "north america",
            "projection_type": "albers usa",
            "showland": True,
            "landcolor": "#f2f5f6",
            "showocean": True,
            "oceancolor": "#e9f2f3",
            "showlakes": True,
            "lakecolor": "#e9f2f3",
            "subunitcolor": "#d4dde0",
            "countrycolor": "#d4dde0",
            "fitbounds": "locations" if has_traces else False,
        },
    )
    return figure


def render_scene(path: Path, height: int = 830) -> None:
    if not path.exists():
        st.warning(f"Scene has not been generated yet: {path.relative_to(PROJECT_ROOT)}")
        return
    st.caption(f"{path.relative_to(PROJECT_ROOT).as_posix()} | {format_bytes(path.stat().st_size)}")
    components.html(read_scene(path), height=height, scrolling=True)


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown("## North Slope Atlas")
        st.caption("Public-source regional workspace")
        st.markdown("---")
        requested_page = st.query_params.get("page", PAGES[0])
        requested_page = PAGE_ALIASES.get(requested_page, requested_page)
        if requested_page not in PAGES:
            requested_page = PAGES[0]
        page = st.radio(
            "Navigate",
            PAGES,
            index=PAGES.index(requested_page),
            label_visibility="collapsed",
        )
        if st.query_params.get("page") != page:
            st.query_params["page"] = page
        st.markdown("---")
        st.caption("Current milestone")
        st.markdown("**Regional atlas foundation**")
        st.progress(0.45)
        st.caption("Public GIS now. Runtime-only approved well logs later.")
    return page


def render_metric_row(files: list[dict[str, object]]) -> None:
    extensions = Counter(str(row["Type"]) for row in files)
    total_size = sum(int(row["Bytes"]) for row in files)
    cols = st.columns(4)
    cols[0].metric("Public well locations", "10,250")
    cols[1].metric("Seismic inventories", "62 total", "26 2D / 36 3D")
    cols[2].metric("Structural XYZ grids", "8")
    cols[3].metric("Workspace footprint", format_bytes(total_size))
    st.caption(
        f"{len(files):,} repository files | {extensions['.parquet']:,} Parquet layers | "
        f"{extensions['.html']:,} interactive HTML exports"
    )


def render_welcome(files: list[dict[str, object]]) -> None:
    st.markdown(
        """
        <div class="atlas-hero">
          <div class="atlas-kicker" style="color:#aee8ed">Alaska North Slope</div>
          <h1>Gas Hydrate Regional Atlas</h1>
          <p>
            A public-source regional context workspace for understanding the
            geology, wells, seismic coverage, and structural surfaces that will
            support future physics-constrained hydrate interpretation.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_metric_row(files)

    st.markdown("### Start Here")
    cols = st.columns(4)
    cards = [
        (
            "Explore the regional context",
            "Use the Regional Atlas to compare assessment units, seismic coverage, "
            "and well locations across the North Slope.",
        ),
        (
            "Inspect subsurface structure",
            "Open the Structural Explorer to review generated 3D surfaces and "
            "their relationship to the public well inventory.",
        ),
        (
            "Connect the manuscript",
            "Use the Research Framework to keep maps, measurements, future ML, "
            "and producibility logic tied to one scientific chain.",
        ),
        (
            "Open the log scaffold",
            "Use the Log Scaffold to inspect synthetic well-log tracks, runtime "
            "readiness, target controls, and presentation exports.",
        ),
    ]
    for col, (title, text) in zip(cols, cards):
        col.markdown(
            f'<div class="atlas-card"><h4>{title}</h4><p>{text}</p></div>',
            unsafe_allow_html=True,
        )
    st.markdown("[Open Log Scaffold](?page=Log%20Scaffold)")

    st.markdown("### What This Atlas Is For")
    st.write(
        "This release organizes the public regional foundation before restricted "
        "well logs arrive. It makes your existing notebook work legible, reusable, "
        "and presentation-ready while preserving a clean boundary around the "
        "future DOE runtime workflow."
    )
    st.markdown(
        """
        <div class="atlas-boundary">
          <strong>Data boundary:</strong> classified, controlled, or restricted
          material is not part of this repository. The future well-log engine will
          load approved data at runtime inside the authorized environment.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_outcome_cards() -> None:
    cols = st.columns(3)
    for col, outcome in zip(cols, MISSION_OUTCOMES):
        col.markdown(
            f"""
            <div class="path-card">
              <h4 style="border-left:4px solid {outcome['color']};padding-left:0.55rem">
                {escape(outcome['label'])}
              </h4>
              <p>{escape(outcome['detail'])}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_path_cards() -> None:
    cards = [
        ("Explore the North Slope", "Map layers, wells, seismic, and structure.", "Explore North Slope"),
        ("Review Hydrate Decisions", "Logs, evidence, readiness, and uncertainty.", "Analyze Hydrates"),
        ("See What Happens Next", "Built pieces, blockers, and deliverables.", "Project Plan"),
    ]
    cols = st.columns(3)
    for col, (title, text, page) in zip(cols, cards):
        col.markdown(
            f"""
            <a href="?page={page.replace(' ', '%20')}" style="text-decoration:none">
              <div class="path-card">
                <h4>{escape(title)}</h4>
                <p>{escape(text)}</p>
              </div>
            </a>
            """,
            unsafe_allow_html=True,
        )


def render_source_anchors() -> None:
    st.markdown("#### Evidence Anchors")
    for anchor in SOURCE_ANCHORS:
        st.markdown(f"**{anchor['claim']}**")
        st.caption(anchor["source"])
        st.write(anchor["use"])
    st.caption(
        "Project synthesis documents organize the workflow; public claims should trace back to verified primary sources."
    )


def render_overview(files: list[dict[str, object]]) -> None:
    render_processing_sketch(
        "system_flow",
        {"tracks": SYNTHETIC_TRACKS},
        "Constraining North Slope Gas Hydrates",
        "Regional context, synthetic well evidence, and interval decisions in one public-safe view.",
        height=430,
    )
    st.markdown(
        '<span class="boundary-badge">Public-source site. Approved logs stay runtime-only.</span>',
        unsafe_allow_html=True,
    )
    render_outcome_cards()
    render_processing_sketch(
        "pipeline",
        {"stages": PIPELINE_STAGES, "heading": "Data to Decision"},
        "Data-to-Decision Pipeline",
        "Files move through QC, physics, whole-well ML validation, expert review, and deliverables.",
        height=340,
    )
    render_processing_sketch(
        "evidence_stack",
        {"stack": EVIDENCE_STACK, "tracks": SYNTHETIC_TRACKS},
        "Subsurface Evidence Stack",
        "Regional context narrows confidence; logs, core, and labels determine interval decisions.",
        height=430,
    )
    render_path_cards()
    with st.expander("Repository context and data boundary"):
        render_metric_row(files)
        st.markdown(
            """
            The hosted website is a public-source atlas and synthetic planning
            scaffold. Restricted logs, core data, named identifiers, trained
            models, populated runtime configs, and derived sensitive outputs
            belong only in the authorized runtime environment.
            """
        )


def render_project_roadmap() -> None:
    content = architecture_content()
    vision = vision_content()
    st.markdown('<div class="atlas-kicker">Living project plan</div>', unsafe_allow_html=True)
    st.title("Project Vision, Goals & Next Steps")
    st.write(
        "The current scientific objective, deliverable priorities, ML direction, "
        "workstreams, blockers, and ordered next actions. This page reads the "
        "tracked project documents directly so the website and repository stay aligned."
    )

    if not content or not vision:
        st.error("The vision or architecture tracker is not available in this deployment.")
        return

    st.markdown("### Project Vision")
    st.markdown(markdown_section(vision, "Project Vision"))
    st.markdown("### Primary Goal")
    st.markdown(markdown_section(vision, "Primary Goal"))

    goal_cols = st.columns(3)
    goal_cols[0].metric("Primary outputs", "Detection + saturation")
    goal_cols[1].metric("Presentation target", "~8 visual slides")
    goal_cols[2].metric("Validation unit", "Held-out wells")

    with st.expander("Deliverables, inputs, and ML direction", expanded=True):
        st.markdown("#### Deliverable Priority")
        st.markdown(markdown_section(vision, "Deliverable Priority"))
        st.markdown("#### Expected Approved Inputs")
        st.markdown(markdown_section(vision, "Expected Approved Inputs"))
        st.markdown("#### ML Direction")
        st.markdown(markdown_section(vision, "ML Direction"))

    workstreams = markdown_table(markdown_section(content, "Workstream Activity Map"))
    components = markdown_table(markdown_section(content, "Component Map"))
    blockers = markdown_table(markdown_section(content, "Blockers and Risks"))

    if not workstreams.empty:
        statuses = workstreams["Status"].astype(str)
        cols = st.columns(4)
        cols[0].metric("Workstreams", len(workstreams))
        active = int(
            statuses.str.startswith("In progress").sum()
            + statuses.str.startswith("Partial").sum()
        )
        cols[1].metric("Active", active)
        waiting = int(
            statuses.str.startswith("Waiting").sum()
            + statuses.str.startswith("Blocked").sum()
        )
        cols[2].metric("Waiting / blocked", waiting)
        cols[3].metric("Complete", int(statuses.str.startswith("Complete").sum()))

    st.markdown("### How the System Connects")
    st.markdown(
        """
        <div class="roadmap-status">
          <strong>Public path</strong><br>
          Regional GIS &rarr; processed layers &rarr; Streamlit atlas &rarr;
          public research communication
        </div>
        <div class="roadmap-status">
          <strong>Scientific path</strong><br>
          Sources and manuscript &rarr; equations and interpretation rules &rarr;
          well-log requirements &rarr; tested classification workflow
        </div>
        <div class="roadmap-status">
          <strong>Authorized path</strong><br>
          Approved logs and core data &rarr; validation &rarr; feature engineering
          &rarr; interval screening &rarr; uncertainty-aware results
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Current Priority")
    st.markdown(
        """
        <div class="roadmap-next">
          <strong>Next project move</strong><br>
          Recover the full Excel workbook, confirm the target labels and units,
          and convert the recovered presentation into the requested concise,
          visual deliverable. Build grouped-well evaluation before model tuning.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(markdown_section(content, "Current Priority"))

    st.markdown("### Workstream Status")
    if workstreams.empty:
        st.info("No workstream table is currently defined.")
    else:
        st.markdown(roadmap_cards(workstreams), unsafe_allow_html=True)
        desktop_table = workstreams.to_html(
            index=False,
            border=0,
            classes=["roadmap-table"],
            escape=True,
        )
        st.markdown(
            f'<div class="roadmap-desktop">{desktop_table}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("### Component Status")
    if not components.empty:
        st.dataframe(components, use_container_width=True, hide_index=True)

    st.markdown("### Blockers and Risks")
    if not blockers.empty:
        st.dataframe(blockers, use_container_width=True, hide_index=True)

    st.markdown("### Near-Term Sequence")
    st.markdown(markdown_section(content, "Near-Term Sequence"))

    st.markdown("### Immediate Next Steps")
    st.markdown(markdown_section(vision, "Immediate Next Steps"))

    with st.expander("Decisions still needed"):
        st.markdown(markdown_section(vision, "Decisions Still Needed"))

    with st.expander("Project boundaries and key decisions"):
        st.markdown("#### Data Boundary")
        st.markdown(markdown_section(content, "Data Boundary"))
        st.markdown("#### Key Decisions")
        st.markdown(markdown_section(content, "Key Decisions"))

    st.caption(
        "Sources: docs/PROJECT_VISION_GOALS_AND_NEXT_STEPS.md and "
        "docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md | "
        "Update the tracked document after important milestones or priority changes."
    )


def render_sweet_spot_page() -> None:
    st.markdown('<div class="atlas-kicker">Synthetic decision workspace</div>', unsafe_allow_html=True)
    st.title("North Slope Gas-Hydrate Sweet Spots")
    st.write(
        "A focused, research-aligned review of synthetic intervals using the full "
        "well-log, reservoir, pressure-temperature, and geomechanical scaffold. "
        "This page demonstrates how future approved data will be evaluated."
    )
    st.warning(
        f"{SYNTHETIC_LABEL}. Review priorities are workflow-triage aids, not hydrate "
        "probabilities, reserves, or calibrated North Slope thresholds."
    )

    logs = load_runtime_data()
    intervals = screen_intervals(logs)
    ranked = sweet_spot_review_table(intervals)
    candidates = intervals[
        intervals["Synthetic sweet-spot review lane"].str.contains(
            "candidate sweet-spot",
            na=False,
        )
    ]

    metric_cols = st.columns(4)
    metric_cols[0].metric("Synthetic intervals", len(intervals))
    metric_cols[1].metric("Review-lane candidates", len(candidates))
    metric_cols[2].metric(
        "Hydrate-supportive",
        int(intervals["Phase-classification evidence"].str.startswith("hydrate").sum()),
    )
    metric_cols[3].metric(
        "Good sand, no hydrate",
        int((intervals["Phase-classification evidence"] == "good sand, no hydrate").sum()),
    )

    st.markdown("### Ranked Review Queue")
    st.caption(
        "Priority balances reservoir quality, multi-log hydrate evidence, retained "
        "flow capacity, moderate-occupancy preference, QC, stability, and stress context."
    )
    st.dataframe(ranked, use_container_width=True, hide_index=True)

    interval_labels = {
        f'{row["Well alias"]} | {row["Top depth (m)"]}-{row["Base depth (m)"]} m': index
        for index, row in intervals.iterrows()
    }
    selected_label = st.selectbox(
        "Inspect a synthetic interval",
        list(interval_labels),
        index=0,
    )
    selected = intervals.loc[interval_labels[selected_label]]

    st.markdown("### Selected Interval Decision")
    decision_cols = st.columns(4)
    decision_cols[0].metric("Review priority", f'{selected["Synthetic review priority"]:.2f}')
    decision_cols[1].metric("Reservoir quality", f'{selected["Reservoir-quality score"]:.2f}')
    decision_cols[2].metric("Hydrate evidence", f'{selected["Hydrate-evidence score"]:.2f}')
    decision_cols[3].metric(
        "Flow retention",
        f'{selected["Permeability-retention proxy"]:.2f}',
    )
    st.info(str(selected["Interpretation summary"]))
    st.write(
        f'**Review lane:** {selected["Synthetic sweet-spot review lane"]}  \n'
        f'**Passed evidence:** {selected["Evidence domains passed"]}  \n'
        f'**Blocking domains:** {selected["Blocking domains"]}  \n'
        f'**Uncertainty:** {selected["Uncertainty flags"]}'
    )

    evidence_values = {
        "Reservoir": selected["Reservoir-quality score"],
        "Hydrate evidence": selected["Hydrate-evidence score"],
        "Saturation proxy": selected["Hydrate-saturation proxy"],
        "Flow retention": selected["Permeability-retention proxy"],
        "QC": 0 if "borehole QC review" in selected["Uncertainty flags"] else 1,
        "Stability": 0 if selected["Stability admissibility"] == "outside / uncertain" else 1,
    }
    evidence_figure = go.Figure(
        go.Bar(
            x=list(evidence_values.values()),
            y=list(evidence_values),
            orientation="h",
            marker_color=["#167d8d", "#d9773d", "#4c78a8", "#59a14f", "#8f6bb3", "#76b7b2"],
            text=[f"{value:.2f}" for value in evidence_values.values()],
            textposition="auto",
        )
    )
    evidence_figure.update_layout(
        title="Evidence Profile",
        xaxis={"range": [0, 1], "title": "Synthetic normalized support"},
        yaxis={"autorange": "reversed"},
        height=390,
        margin={"l": 0, "r": 0, "t": 45, "b": 0},
    )
    st.plotly_chart(evidence_figure, use_container_width=True)

    tabs = st.tabs(
        [
            "Input Variables",
            "Geomechanics",
            "Competing Explanations",
            "Science and Sources",
        ]
    )
    with tabs[0]:
        input_rows = [
            ("GR", selected["GR median (API)"], "API", "Lithology and clean-sand screen"),
            ("Rt", selected["Rt median (ohm m)"], "ohm m", "Electrical hydrate evidence; non-unique"),
            ("RHOB", selected["RHOB median (g/cc)"], "g/cc", "Density and porosity constraint"),
            ("Density porosity", selected["Density porosity median"], "v/v", "Reservoir capacity"),
            ("NMR porosity", selected["NMR porosity median"], "v/v", "Mobile-fluid response where available"),
            ("Vp", selected["Vp median (km/s)"], "km/s", "Compressional stiffness and gas discrimination"),
            ("Vs", selected["Vs median (km/s)"], "km/s", "Rigidity and hydrate-versus-gas support"),
            ("Vp/Vs", selected["Vp/Vs median"], "ratio", "Elastic phase context"),
            ("Hydrate saturation proxy", selected["Hydrate-saturation proxy"], "fraction", selected["Proxy source"]),
        ]
        st.dataframe(
            pd.DataFrame(input_rows, columns=["Variable", "Interval median", "Unit", "Decision role"]),
            use_container_width=True,
            hide_index=True,
        )
    with tabs[1]:
        geomechanics = pd.DataFrame(
            [
                ("Shear modulus", selected["Shear modulus (GPa)"], "GPa", "Rigidity"),
                ("Bulk modulus", selected["Bulk modulus (GPa)"], "GPa", "Compressibility"),
                ("Young's modulus", selected["Young's modulus (GPa)"], "GPa", "Stiffness"),
                ("Poisson ratio", selected["Poisson ratio"], "ratio", "Elastic behavior"),
                ("Lambda-rho", selected["Lambda-rho"], "GPa g/cc", "Fluid/compressibility context"),
                ("Mu-rho", selected["Mu-rho"], "GPa g/cc", "Rigidity context"),
                ("Vertical stress", selected["Vertical stress (MPa)"], "MPa", "Overburden"),
                ("Effective stress", selected["Effective stress (MPa)"], "MPa", "Compaction and flow risk"),
            ],
            columns=["Property", "Synthetic interval median", "Unit", "Interpretation role"],
        )
        st.dataframe(geomechanics, use_container_width=True, hide_index=True)
        st.caption(
            "High stiffness can support hydrate interpretation, but burial, effective "
            "stress, ice, cementation, and competent lithology can mimic the response."
        )
    with tabs[2]:
        st.dataframe(
            pd.DataFrame(ROCKTYPE_CONTEXT_GUIDE),
            use_container_width=True,
            hide_index=True,
        )
        st.error(
            "High resistivity plus low Vp remains gas-supportive. High stiffness "
            "without reservoir and pore-fluid agreement remains a lithology/stress review."
        )
    with tabs[3]:
        source_metrics = st.columns(3)
        source_metrics[0].metric("Primary public references", len(PUBLIC_SCIENCE_REFERENCES))
        source_metrics[1].metric(
            "Indexed project artifacts",
            sum(row["Indexed artifacts"] for row in SOURCE_LIBRARY_COVERAGE),
        )
        source_metrics[2].metric("Source groups", len(SOURCE_LIBRARY_COVERAGE))
        st.caption(
            "The four connected-Drive documents were one synthesis subset. "
            "They are not the project's total source base."
        )
        st.dataframe(
            pd.DataFrame(SWEET_SPOT_EVIDENCE_MODEL),
            use_container_width=True,
            hide_index=True,
        )
        st.subheader("Source Library Coverage")
        st.dataframe(
            pd.DataFrame(SOURCE_LIBRARY_COVERAGE),
            use_container_width=True,
            hide_index=True,
        )
        st.subheader("Verified Primary Public References")
        st.dataframe(
            pd.DataFrame(PUBLIC_SCIENCE_REFERENCES),
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            "Project manuscripts, equation maps, and Drive synthesis documents organize "
            "the workflow but are not counted as independent confirmation. Final "
            "thresholds require source-by-source verification and authorized-data calibration."
        )


def render_regional_atlas() -> None:
    st.markdown('<div class="atlas-kicker">Regional context</div>', unsafe_allow_html=True)
    st.title("Regional Atlas")
    st.write(
        "This interactive map is the existing regional visualization from the "
        "notebook workflow. It brings together the North Slope extent, assessment "
        "units, 2D seismic lines, 3D seismic footprints, and well locations."
    )
    cols = st.columns(3)
    cols[0].metric("Assessment units", "6")
    cols[1].metric("2D seismic surveys", "26")
    cols[2].metric("3D seismic footprints", "36")
    st.info(
        "Use the Plotly controls inside the map to zoom and inspect layers. "
        "The well-color selector switches the active well comparison."
    )
    render_scene(REGIONAL_SCENE, height=870)


def render_stability_source_bundle() -> None:
    full_bundle_root = default_stability_bundle_path(PROJECT_ROOT)
    snapshot_root = default_stability_snapshot_path(PROJECT_ROOT)
    source_root = active_stability_source_path(PROJECT_ROOT)
    source_label = project_relative_or_absolute(source_root)
    status = cached_stability_source_status(str(source_root))
    metrics = cached_stability_bundle_metrics(str(source_root))
    source_kind = stability_source_kind(source_root)

    st.markdown("### Public Stability Source Bundle")
    st.caption(f"Active stability source: `{source_label}`")
    st.warning(
        "This is a stability admissibility screen. It can show where hydrate could "
        "be thermodynamically plausible, but it is not hydrate proof and not a "
        "saturation prediction."
    )

    cols = st.columns(4)
    cols[0].metric(
        "Source items",
        f'{metrics["Ready source items"]}/{metrics["Total source items"]}',
        metrics["Bundle"],
    )
    cols[1].metric("GGD223 controls", f'{metrics["GGD223 controls"]:,}')
    cols[2].metric("Hydrate AUs", f'{metrics["Hydrate AUs"]:,}')
    cols[3].metric("Source G10015 files", f'{metrics["G10015 profiles"]:,}')

    if not source_root.exists():
        st.info(
            "No full source bundle or committed public snapshot was found. The "
            "full OpenScienceLab source-bundle path is "
            f"`{project_relative_or_absolute(full_bundle_root)}` and the public "
            "snapshot fallback path is "
            f"`{project_relative_or_absolute(snapshot_root)}`."
        )
        st.dataframe(status, use_container_width=True, hide_index=True)
        return

    missing = status[status["Status"] != "Ready"]
    if source_kind == "Public snapshot":
        st.success(
            "Using the committed public snapshot: GGD223 permafrost-depth controls "
            "and USGS hydrate assessment units are available without the large "
            "local source bundle."
        )
        st.caption(
            "Upload the full source bundle in OpenScienceLab when you need the "
            "G10015 temperature-profile files, the OM-222 source plate, and the "
            "full Alaska DNR well package."
        )
    elif missing.empty:
        st.success("All tracked source-bundle items are present.")
    else:
        st.warning(
            "Some source-bundle items are still missing. The available layers will "
            "load, but the stability workflow is incomplete."
        )
    st.dataframe(status, use_container_width=True, hide_index=True)

    permafrost_points = cached_ggd223_points(str(source_root))
    assessment_units = cached_hydrate_assessment_units(str(source_root))
    if permafrost_points.empty and assessment_units.empty:
        st.info("No mappable stability-source layers were found yet.")
        render_public_well_stability_context_product()
        return

    st.plotly_chart(
        build_stability_source_figure(permafrost_points, assessment_units),
        use_container_width=True,
    )

    if not permafrost_points.empty:
        depth_min = int(permafrost_points["permafrost_depth_m"].min())
        depth_max = int(permafrost_points["permafrost_depth_m"].max())
        st.caption(
            f"GGD223 permafrost-depth controls range from {depth_min:,} to "
            f"{depth_max:,} m in `stnlist.dat`. Use these as point controls and "
            "OM-222 as the mapped plate until permafrost-base contours are digitized."
        )
        preview = permafrost_points.sort_values("permafrost_depth_m", ascending=False).head(12)
        st.dataframe(
            preview[
                [
                    "well_designation",
                    "code",
                    "latitude",
                    "longitude",
                    "elevation_m",
                    "permafrost_depth_m",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

    render_public_well_stability_context_product()


def render_public_well_stability_context_product() -> None:
    context_path = default_well_context_path(PROJECT_ROOT)
    context = cached_public_well_stability_context(str(PROJECT_ROOT))
    if context.empty:
        st.info(
            "No public well stability-context product has been generated yet. "
            f"Expected path: `{project_relative_or_absolute(context_path)}`."
        )
        return

    st.markdown("#### Public Well Stability Context Product")
    st.caption(
        "Derived from public DNR well locations/depths, nearest GGD223 "
        "permafrost-depth controls, and USGS hydrate assessment-unit membership. "
        "This is screening context, not hydrate proof."
    )
    summary = stability_context_summary_frame(context)
    candidate_count = int((context["stability_context_flag"] == "public_context_candidate").sum())
    au_count = int(context["within_hydrate_assessment_unit"].sum())
    depth_count = int(pd.to_numeric(context["depth_basis_m"], errors="coerce").notna().sum())

    cols = st.columns(4)
    cols[0].metric("Arctic Slope wells", f"{len(context):,}")
    cols[1].metric("Inside hydrate AU", f"{au_count:,}")
    cols[2].metric("Depth available", f"{depth_count:,}")
    cols[3].metric("Context candidates", f"{candidate_count:,}")
    st.dataframe(summary, use_container_width=True, hide_index=True)

    candidate_preview = context[
        context["stability_context_flag"] == "public_context_candidate"
    ].copy()
    preview_source = candidate_preview if not candidate_preview.empty else context
    preview = preview_source.sort_values(["nearest_ggd223_distance_km", "well_name"]).head(14)
    st.dataframe(
        preview[
            [
                "well_name",
                "field",
                "depth_basis",
                "depth_basis_ft",
                "hydrate_assessment_codes",
                "nearest_ggd223_code",
                "nearest_permafrost_depth_m",
                "nearest_ggd223_distance_km",
                "stability_context_flag",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )
    st.download_button(
        "Download public well context CSV",
        context.to_csv(index=False).encode("utf-8"),
        file_name=context_path.name,
        mime="text/csv",
        use_container_width=True,
    )

    render_g10015_temperature_inventory_product()


def render_g10015_temperature_inventory_product() -> None:
    inventory_path = default_g10015_inventory_path(PROJECT_ROOT)
    inventory = cached_g10015_temperature_inventory(str(PROJECT_ROOT))
    if inventory.empty:
        st.info(
            "No G10015 temperature-profile inventory has been generated yet. "
            f"Expected path: `{project_relative_or_absolute(inventory_path)}`."
        )
        return

    st.markdown("#### G10015 Temperature Profile Inventory")
    st.caption(
        "Compact inventory of public processed borehole temperature logs. "
        "The gradient value is a rough deepest-window context estimate, not a "
        "calibrated geothermal model."
    )
    max_depth = float(pd.to_numeric(inventory["max_depth_m"], errors="coerce").max())
    gradient_count = int(
        pd.to_numeric(
            inventory["deepest_window_gradient_c_per_100m"],
            errors="coerce",
        ).notna().sum()
    )
    cols = st.columns(4)
    cols[0].metric("G10015 profiles", f"{len(inventory):,}")
    cols[1].metric("Well codes", f"{inventory['well_code'].nunique():,}")
    cols[2].metric("Deepest log", f"{max_depth:,.1f} m")
    cols[3].metric("Gradient estimates", f"{gradient_count:,}")
    st.dataframe(
        temperature_inventory_summary_frame(inventory),
        use_container_width=True,
        hide_index=True,
    )
    preview = inventory.sort_values(["well_code", "max_depth_m"], ascending=[True, False]).head(14)
    st.dataframe(
        preview[
            [
                "file_name",
                "well_code",
                "well_name",
                "log_date",
                "sample_count",
                "max_depth_m",
                "deepest_temperature_c",
                "deepest_window_gradient_c_per_100m",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )
    st.download_button(
        "Download G10015 inventory CSV",
        inventory.to_csv(index=False).encode("utf-8"),
        file_name=inventory_path.name,
        mime="text/csv",
        use_container_width=True,
    )
    render_stability_input_scaffold_product()
    render_guarded_stability_screen_product()
    render_stability_parameter_readiness()


def render_stability_input_scaffold_product() -> None:
    scaffold_path = default_stability_input_scaffold_path(PROJECT_ROOT)
    scaffold = cached_stability_input_scaffold(str(PROJECT_ROOT))
    if scaffold.empty:
        st.info(
            "No stability input scaffold has been generated yet. "
            f"Expected path: `{project_relative_or_absolute(scaffold_path)}`."
        )
        return

    st.markdown("#### Stability Input Scaffold")
    st.caption(
        "One-row-per-public-well input table for the next stability calculation. "
        "It lines up public depth, nearest permafrost control, G10015 temperature "
        "context where available, and a provisional hydrostatic pressure estimate. "
        "Top/base/thickness are intentionally not calculated here."
    )
    summary = stability_input_scaffold_summary_frame(scaffold)
    matched = int(scaffold["nearest_temperature_profile_code"].notna().sum())
    ready = int((scaffold["stability_input_readiness"] == "ready_for_phase_curve_inputs").sum())
    cols = st.columns(4)
    cols[0].metric("Scaffold wells", f"{len(scaffold):,}")
    cols[1].metric("Temperature matched", f"{matched:,}")
    cols[2].metric("Next-step ready", f"{ready:,}")
    cols[3].metric("Final results", "0")
    st.dataframe(summary, use_container_width=True, hide_index=True)

    preview_source = scaffold[
        scaffold["stability_input_readiness"] == "ready_for_phase_curve_inputs"
    ].copy()
    if preview_source.empty:
        preview_source = scaffold
    preview = preview_source.sort_values(["nearest_ggd223_distance_km", "well_name"]).head(14)
    preview_columns = [
        "well_name",
        "depth_basis_m",
        "nearest_ggd223_code",
        "nearest_permafrost_depth_m",
        "nearest_temperature_profile_code",
        "rough_geothermal_gradient_c_per_100m",
        "hydrostatic_pressure_mpa_at_depth_basis",
        "hydrostatic_pressure_mpa_absolute_at_depth_basis",
        "phase_curve_status",
        "planned_phase_curve_id",
        "planned_phase_curve_role",
        "planned_gas_composition_assumption",
        "stability_input_readiness",
    ]
    st.dataframe(
        preview[[column for column in preview_columns if column in preview.columns]],
        use_container_width=True,
        hide_index=True,
    )
    st.download_button(
        "Download stability input scaffold CSV",
        scaffold.to_csv(index=False).encode("utf-8"),
        file_name=scaffold_path.name,
        mime="text/csv",
        use_container_width=True,
    )


def build_stability_screen_map(screen: pd.DataFrame) -> go.Figure:
    map_frame = screen.copy()
    map_frame["lat"] = pd.to_numeric(map_frame.get("lat"), errors="coerce")
    map_frame["lon"] = pd.to_numeric(map_frame.get("lon"), errors="coerce")
    map_frame["stability_top_m"] = pd.to_numeric(
        map_frame.get("stability_top_m"), errors="coerce"
    )
    map_frame["stability_base_m"] = pd.to_numeric(
        map_frame.get("stability_base_m"), errors="coerce"
    )
    map_frame["stability_thickness_m"] = pd.to_numeric(
        map_frame.get("stability_thickness_m"), errors="coerce"
    )
    map_frame["tvd_m"] = pd.to_numeric(map_frame.get("tvd_m"), errors="coerce")
    map_frame = map_frame.dropna(subset=["lat", "lon"])

    figure = go.Figure()
    if map_frame.empty:
        figure.update_layout(
            height=520,
            margin={"l": 0, "r": 0, "t": 24, "b": 0},
            annotations=[
                {
                    "text": "No latitude/longitude values available for the screen.",
                    "xref": "paper",
                    "yref": "paper",
                    "x": 0.5,
                    "y": 0.5,
                    "showarrow": False,
                }
            ],
        )
        return figure

    center_lat = float(map_frame["lat"].median())
    center_lon = float(map_frame["lon"].median())
    statuses = list(STABILITY_SCREEN_STATUS_STYLES)
    extra_statuses = [
        status
        for status in sorted(map_frame["stability_result_status"].dropna().unique())
        if status not in STABILITY_SCREEN_STATUS_STYLES
    ]
    for status in statuses + extra_statuses:
        style = STABILITY_SCREEN_STATUS_STYLES.get(
            status,
            {
                "label": status,
                "color": "#475569",
                "size": 6,
                "opacity": 0.55,
            },
        )
        subset = map_frame[map_frame["stability_result_status"].eq(status)].copy()
        if subset.empty:
            continue
        hover_text = (
            "<b>"
            + subset["well_name"].fillna("Unnamed well").astype(str)
            + "</b><br>Status: "
            + subset["stability_result_status"].fillna("missing").astype(str)
            + "<br>Confidence: "
            + subset["stability_confidence"].fillna("missing").astype(str)
            + "<br>TVD: "
            + subset["tvd_m"].round(1).astype(str)
            + " m<br>Top/Base: "
            + subset["stability_top_m"].round(1).astype(str)
            + " / "
            + subset["stability_base_m"].round(1).astype(str)
            + " m<br>Thickness: "
            + subset["stability_thickness_m"].round(1).astype(str)
            + " m"
        )
        figure.add_trace(
            go.Scattermapbox(
                lat=subset["lat"],
                lon=subset["lon"],
                mode="markers",
                name=style["label"],
                marker={
                    "size": style["size"],
                    "color": style["color"],
                    "opacity": style["opacity"],
                },
                text=hover_text,
                hovertemplate="%{text}<extra></extra>",
            )
        )

    figure.update_layout(
        height=560,
        margin={"l": 0, "r": 0, "t": 30, "b": 0},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.01,
            "xanchor": "left",
            "x": 0,
        },
        mapbox={
            "style": "open-street-map",
            "center": {"lat": center_lat, "lon": center_lon},
            "zoom": 4.0,
        },
    )
    return figure


def build_stability_interval_depth_figure(screen: pd.DataFrame) -> go.Figure:
    intervals = screen[screen["stability_result_status"].eq("calculated")].copy()
    for column in ["stability_top_m", "stability_base_m", "stability_thickness_m"]:
        intervals[column] = pd.to_numeric(intervals[column], errors="coerce")
    intervals = intervals.dropna(
        subset=["well_name", "stability_top_m", "stability_base_m", "stability_thickness_m"]
    )

    figure = go.Figure()
    if intervals.empty:
        figure.update_layout(
            height=420,
            margin={"l": 0, "r": 0, "t": 24, "b": 0},
            annotations=[
                {
                    "text": "No calculated intervals are available in this screen run.",
                    "xref": "paper",
                    "yref": "paper",
                    "x": 0.5,
                    "y": 0.5,
                    "showarrow": False,
                }
            ],
        )
        return figure

    intervals = intervals.sort_values(
        ["stability_top_m", "stability_base_m", "well_name"],
        ascending=[True, True, True],
    ).head(30)
    y_labels = [
        f"{row.well_name} ({str(row.stability_confidence).replace('_source_control', '')})"
        for row in intervals.itertuples()
    ]
    colors = [
        STABILITY_SCREEN_CONFIDENCE_COLORS.get(confidence, "#64748b")
        for confidence in intervals["stability_confidence"]
    ]
    figure.add_trace(
        go.Bar(
            x=intervals["stability_thickness_m"],
            y=y_labels,
            base=intervals["stability_top_m"],
            orientation="h",
            marker={"color": colors, "line": {"color": "white", "width": 0.5}},
            customdata=intervals[
                [
                    "stability_top_m",
                    "stability_base_m",
                    "stability_thickness_m",
                    "temperature_profile_code",
                    "caveat_codes",
                ]
            ],
            hovertemplate=(
                "<b>%{y}</b><br>Top: %{customdata[0]:.1f} m"
                "<br>Base: %{customdata[1]:.1f} m"
                "<br>Thickness: %{customdata[2]:.1f} m"
                "<br>Temperature profile: %{customdata[3]}"
                "<br>Caveats: %{customdata[4]}<extra></extra>"
            ),
            name="Calculated interval",
        )
    )
    figure.update_layout(
        height=max(420, 28 * len(intervals) + 120),
        margin={"l": 220, "r": 24, "t": 24, "b": 48},
        xaxis_title="Depth interval in meters (top to base)",
        yaxis_title="",
        bargap=0.32,
        showlegend=False,
    )
    figure.update_xaxes(rangemode="tozero")
    return figure


def build_selected_well_phase_audit_figure(
    screen_row: pd.Series,
    temperature_model: pd.DataFrame,
    phase_curve: pd.DataFrame,
    profile_points: pd.DataFrame | None = None,
) -> go.Figure:
    figure = go.Figure()
    well_name = str(screen_row.get("well_name", "Selected well"))
    object_id = screen_row.get("object_id")

    curve = phase_curve.copy()
    curve["source_depth_m"] = pd.to_numeric(curve.get("source_depth_m"), errors="coerce")
    curve["equilibrium_temperature_c"] = pd.to_numeric(
        curve.get("equilibrium_temperature_c"),
        errors="coerce",
    )
    curve = curve.dropna(subset=["source_depth_m", "equilibrium_temperature_c"]).sort_values(
        "source_depth_m"
    )
    if not curve.empty:
        figure.add_trace(
            go.Scatter(
                x=curve["equilibrium_temperature_c"],
                y=curve["source_depth_m"],
                mode="lines",
                name="Methane 5 ppt phase boundary",
                line={"color": "#111827", "width": 3},
                hovertemplate=(
                    "Phase boundary<br>Depth: %{y:.1f} m"
                    "<br>Equilibrium T: %{x:.2f} C<extra></extra>"
                ),
            )
        )

    selected_profile_file = screen_row.get("temperature_profile_file")
    selected_profile_code = screen_row.get("temperature_profile_code")
    sampled_profile = pd.DataFrame()
    if profile_points is not None and not profile_points.empty:
        profile_frame = profile_points.copy()
        if pd.notna(selected_profile_file) and "file_name" in profile_frame.columns:
            sampled_profile = profile_frame[profile_frame["file_name"].eq(selected_profile_file)]
        if (
            sampled_profile.empty
            and pd.notna(selected_profile_code)
            and "well_code" in profile_frame.columns
        ):
            sampled_profile = profile_frame[profile_frame["well_code"].eq(selected_profile_code)]
        sampled_profile["depth_m"] = pd.to_numeric(
            sampled_profile.get("depth_m"),
            errors="coerce",
        )
        sampled_profile["temperature_c"] = pd.to_numeric(
            sampled_profile.get("temperature_c"),
            errors="coerce",
        )
        sampled_profile = sampled_profile.dropna(
            subset=["depth_m", "temperature_c"],
        ).sort_values("depth_m")
    if not sampled_profile.empty:
        figure.add_trace(
            go.Scatter(
                x=sampled_profile["temperature_c"],
                y=sampled_profile["depth_m"],
                mode="lines",
                name="Sampled measured G10015 profile",
                line={"color": "#16a34a", "width": 3},
                customdata=sampled_profile[["file_name", "sample_method"]],
                hovertemplate=(
                    "Sampled measured profile<br>Depth: %{y:.1f} m"
                    "<br>Temperature: %{x:.2f} C"
                    "<br>File: %{customdata[0]}"
                    "<br>Sampling: %{customdata[1]}<extra></extra>"
                ),
            )
        )

    model = temperature_model.copy()
    if "object_id" in model.columns and pd.notna(object_id):
        model = model[model["object_id"].eq(object_id)]
    else:
        model = model[model["well_name"].eq(well_name)]
    model["depth_m"] = pd.to_numeric(model.get("depth_m"), errors="coerce")
    model["temperature_model_c"] = pd.to_numeric(
        model.get("temperature_model_c"),
        errors="coerce",
    )
    model = model.dropna(subset=["depth_m", "temperature_model_c"]).sort_values("depth_m")
    if not model.empty:
        figure.add_trace(
            go.Scatter(
                x=model["temperature_model_c"],
                y=model["depth_m"],
                mode="lines+markers",
                name="OSL modeled temperature key depths",
                line={"color": "#2563eb", "width": 3},
                marker={"size": 9},
                customdata=model[
                    [
                        "temperature_model_depth_role",
                        "temperature_model_method",
                        "temperature_model_status",
                    ]
                ],
                hovertemplate=(
                    "Temperature model<br>Depth: %{y:.1f} m"
                    "<br>Temperature: %{x:.2f} C"
                    "<br>Role: %{customdata[0]}"
                    "<br>Method: %{customdata[1]}"
                    "<br>Status: %{customdata[2]}<extra></extra>"
                ),
            )
        )

    screen_points = []
    for label, depth_col, temp_col in [
        ("Screen top", "stability_top_m", "stability_top_temperature_c"),
        ("Screen base", "stability_base_m", "stability_base_temperature_c"),
    ]:
        depth = pd.to_numeric(pd.Series([screen_row.get(depth_col)]), errors="coerce").iloc[0]
        temp = pd.to_numeric(pd.Series([screen_row.get(temp_col)]), errors="coerce").iloc[0]
        if pd.notna(depth) and pd.notna(temp):
            screen_points.append({"label": label, "depth_m": depth, "temperature_c": temp})
    if screen_points:
        points = pd.DataFrame(screen_points)
        figure.add_trace(
            go.Scatter(
                x=points["temperature_c"],
                y=points["depth_m"],
                mode="markers+text",
                name="Screen top/base",
                marker={
                    "size": 13,
                    "color": "#f97316",
                    "line": {"color": "white", "width": 1},
                },
                text=points["label"],
                textposition="middle right",
                hovertemplate=(
                    "%{text}<br>Depth: %{y:.1f} m"
                    "<br>Temperature: %{x:.2f} C<extra></extra>"
                ),
            )
        )

    reference_depths = [
        ("Permafrost control", screen_row.get("permafrost_base_m"), "#0f766e"),
        ("Well TVD", screen_row.get("tvd_m"), "#64748b"),
    ]
    plotted_depths = []
    for label, value, color in reference_depths:
        depth = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
        if pd.isna(depth):
            continue
        plotted_depths.append(depth)
        figure.add_hline(
            y=float(depth),
            line={"color": color, "width": 1.5, "dash": "dot"},
            annotation_text=label,
            annotation_position="right",
        )

    if curve.empty and model.empty and sampled_profile.empty and not screen_points:
        figure.update_layout(
            annotations=[
                {
                    "text": "No phase/temperature audit points are available for this well.",
                    "xref": "paper",
                    "yref": "paper",
                    "x": 0.5,
                    "y": 0.5,
                    "showarrow": False,
                }
            ]
        )

    max_depth_candidates = []
    for frame, depth_column in [
        (curve, "source_depth_m"),
        (sampled_profile, "depth_m"),
        (model, "depth_m"),
    ]:
        if not frame.empty:
            max_depth_candidates.append(float(frame[depth_column].max()))
    max_depth_candidates.extend(float(depth) for depth in plotted_depths if pd.notna(depth))
    if screen_points:
        max_depth_candidates.append(float(pd.DataFrame(screen_points)["depth_m"].max()))
    max_depth = max(max_depth_candidates) if max_depth_candidates else 1000.0

    figure.update_layout(
        height=560,
        margin={"l": 70, "r": 32, "t": 40, "b": 56},
        title=f"{well_name} temperature-phase audit",
        xaxis_title="Temperature (C)",
        yaxis_title="Depth (m)",
        legend={"orientation": "h", "y": 1.08, "x": 0},
    )
    figure.update_yaxes(autorange="reversed", range=[max_depth * 1.03, 0])
    return figure


def stability_blank_reason_summary_frame(screen: pd.DataFrame) -> pd.DataFrame:
    if screen.empty or "stability_result_status" not in screen.columns:
        return pd.DataFrame(columns=["reason", "rows", "share_pct", "meaning", "next_step"])

    status_counts = screen["stability_result_status"].fillna("missing").value_counts()
    ordered_statuses = [
        "blocked_missing_temperature_profile",
        "blocked_missing_depth",
        "blocked_phase_curve_range_insufficient",
        "outside_au_context",
        "calculated_no_stable_interval",
        "calculated",
    ]
    ordered_statuses += [
        status for status in status_counts.index.tolist() if status not in ordered_statuses
    ]
    rows = []
    total = max(len(screen), 1)
    for status in ordered_statuses:
        count = int(status_counts.get(status, 0))
        if count == 0:
            continue
        detail = BLANK_REASON_DETAILS.get(
            status,
            {
                "label": status,
                "meaning": "Status not yet documented in the diagnostic legend.",
                "next_step": "Review before using in public interpretation.",
            },
        )
        rows.append(
            {
                "reason": detail["label"],
                "status_code": status,
                "rows": count,
                "share_pct": round(100 * count / total, 2),
                "meaning": detail["meaning"],
                "next_step": detail["next_step"],
            }
        )
    return pd.DataFrame(rows)


def build_blank_reason_bar_figure(summary: pd.DataFrame) -> go.Figure:
    figure = go.Figure()
    if summary.empty:
        return figure
    colors = [
        STABILITY_SCREEN_STATUS_STYLES.get(code, {"color": "#475569"})["color"]
        for code in summary["status_code"]
    ]
    figure.add_trace(
        go.Bar(
            x=summary["rows"],
            y=summary["reason"],
            orientation="h",
            marker={"color": colors},
            customdata=summary[["share_pct", "next_step"]],
            hovertemplate=(
                "<b>%{y}</b><br>Rows: %{x:,}"
                "<br>Share: %{customdata[0]:.2f}%"
                "<br>Next: %{customdata[1]}<extra></extra>"
            ),
        )
    )
    figure.update_layout(
        height=max(360, 46 * len(summary) + 80),
        margin={"l": 260, "r": 24, "t": 24, "b": 40},
        xaxis_title="Rows",
        yaxis_title="",
        showlegend=False,
    )
    return figure


def g10015_temperature_control_crosswalk_frame(
    inventory: pd.DataFrame,
    ggd223_points: pd.DataFrame,
) -> pd.DataFrame:
    if inventory.empty:
        return pd.DataFrame(
            columns=[
                "well_code",
                "profile_files",
                "profile_well_names",
                "max_profile_depth_m",
                "ggd223_code",
                "ggd223_well_designation",
                "latitude",
                "longitude",
                "coordinate_status",
                "crosswalk_method",
            ]
        )

    profile_summary = (
        inventory.assign(
            max_depth_m=pd.to_numeric(inventory.get("max_depth_m"), errors="coerce"),
        )
        .groupby("well_code", dropna=False)
        .agg(
            profile_files=("file_name", "nunique"),
            profile_well_names=(
                "well_name",
                lambda values: "; ".join(
                    sorted({str(value) for value in values.dropna() if str(value).strip()})[:4]
                ),
            ),
            max_profile_depth_m=("max_depth_m", "max"),
        )
        .reset_index()
    )

    controls = ggd223_points.copy()
    for column in ["code", "well_designation"]:
        if column in controls.columns:
            controls[column] = controls[column].astype(str)
    control_codes = controls["code"].dropna().astype(str) if "code" in controls else pd.Series()
    rows = []
    for profile in profile_summary.itertuples(index=False):
        code = str(profile.well_code)
        match = controls[controls["code"].eq(code)] if "code" in controls else pd.DataFrame()
        crosswalk_method = "exact_ggd223_code"
        if match.empty and not control_codes.empty:
            prefix_codes = control_codes[control_codes.str.startswith(code)]
            if len(prefix_codes) == 1:
                match = controls[controls["code"].eq(prefix_codes.iloc[0])]
                crosswalk_method = "unique_prefix_ggd223_code"

        if match.empty:
            rows.append(
                {
                    **profile._asdict(),
                    "ggd223_code": pd.NA,
                    "ggd223_well_designation": pd.NA,
                    "latitude": np.nan,
                    "longitude": np.nan,
                    "coordinate_status": "missing_committed_coordinate_crosswalk",
                    "crosswalk_method": "needs_g10015_location_source_or_alias",
                }
            )
            continue

        control = match.iloc[0]
        rows.append(
            {
                **profile._asdict(),
                "ggd223_code": control.get("code"),
                "ggd223_well_designation": control.get("well_designation"),
                "latitude": pd.to_numeric(
                    pd.Series([control.get("latitude")]), errors="coerce"
                ).iloc[0],
                "longitude": pd.to_numeric(
                    pd.Series([control.get("longitude")]), errors="coerce"
                ).iloc[0],
                "coordinate_status": "located_from_committed_ggd223_control",
                "crosswalk_method": crosswalk_method,
            }
        )
    return pd.DataFrame(rows)


def temperature_proxy_candidate_audit_frame(
    screen: pd.DataFrame,
    control_crosswalk: pd.DataFrame,
) -> pd.DataFrame:
    if screen.empty:
        return pd.DataFrame()

    audit = screen.copy()
    audit["lat"] = pd.to_numeric(audit.get("lat"), errors="coerce")
    audit["lon"] = pd.to_numeric(audit.get("lon"), errors="coerce")
    audit["tvd_m"] = pd.to_numeric(audit.get("tvd_m"), errors="coerce")
    audit["nearest_g10015_control_code"] = pd.NA
    audit["nearest_g10015_control_distance_km"] = np.nan
    audit["nearest_g10015_control_crosswalk_method"] = pd.NA

    located_controls = control_crosswalk.dropna(subset=["latitude", "longitude"]).copy()
    if not located_controls.empty:
        valid_rows = audit["lat"].notna() & audit["lon"].notna()
        if valid_rows.any():
            well_lat = np.radians(
                audit.loc[valid_rows, "lat"].to_numpy(dtype="float64")
            )[:, None]
            well_lon = np.radians(
                audit.loc[valid_rows, "lon"].to_numpy(dtype="float64")
            )[:, None]
            control_lat = np.radians(
                located_controls["latitude"].to_numpy(dtype="float64")
            )[None, :]
            control_lon = np.radians(
                located_controls["longitude"].to_numpy(dtype="float64")
            )[None, :]
            delta_lat = control_lat - well_lat
            delta_lon = control_lon - well_lon
            haversine = (
                np.sin(delta_lat / 2) ** 2
                + np.cos(well_lat) * np.cos(control_lat) * np.sin(delta_lon / 2) ** 2
            )
            distances = 6371.0088 * 2 * np.arctan2(
                np.sqrt(haversine), np.sqrt(1 - haversine)
            )
            nearest_index = np.argmin(distances, axis=1)
            nearest_controls = located_controls.iloc[nearest_index].reset_index(drop=True)
            audit.loc[valid_rows, "nearest_g10015_control_code"] = nearest_controls[
                "well_code"
            ].to_numpy()
            audit.loc[valid_rows, "nearest_g10015_control_distance_km"] = distances[
                np.arange(distances.shape[0]), nearest_index
            ]
            audit.loc[valid_rows, "nearest_g10015_control_crosswalk_method"] = nearest_controls[
                "crosswalk_method"
            ].to_numpy()

    has_direct_profile = audit["temperature_profile_code"].notna()
    inside_au = audit["within_hydrate_assessment_unit"].eq(True)
    has_depth = audit["tvd_m"].notna()
    distance = audit["nearest_g10015_control_distance_km"]

    audit["temperature_proxy_tier"] = "temperature_control_location_gap"
    audit.loc[~inside_au, "temperature_proxy_tier"] = "outside_public_au_context"
    audit.loc[inside_au & ~has_depth, "temperature_proxy_tier"] = "missing_well_depth"
    audit.loc[
        inside_au & has_depth & ~has_direct_profile & distance.gt(100),
        "temperature_proxy_tier",
    ] = "distant_from_g10015_controls"
    audit.loc[
        inside_au
        & has_depth
        & ~has_direct_profile
        & distance.gt(50)
        & distance.le(100),
        "temperature_proxy_tier",
    ] = "proxy_candidate_regional_g10015_control"
    audit.loc[
        inside_au & has_depth & ~has_direct_profile & distance.le(50),
        "temperature_proxy_tier",
    ] = "proxy_candidate_near_g10015_control"
    audit.loc[has_direct_profile, "temperature_proxy_tier"] = "direct_g10015_profile_match"

    audit["temperature_proxy_tier_label"] = audit["temperature_proxy_tier"].map(
        lambda tier: TEMPERATURE_PROXY_TIER_DETAILS.get(tier, {"label": tier})["label"]
    )
    return audit


def temperature_proxy_tier_summary_frame(audit: pd.DataFrame) -> pd.DataFrame:
    if audit.empty:
        return pd.DataFrame(columns=["tier", "rows", "share_pct", "meaning", "allowed_use"])

    counts = audit["temperature_proxy_tier"].value_counts()
    ordered_tiers = [
        "direct_g10015_profile_match",
        "proxy_candidate_near_g10015_control",
        "proxy_candidate_regional_g10015_control",
        "distant_from_g10015_controls",
        "missing_well_depth",
        "outside_public_au_context",
        "temperature_control_location_gap",
    ]
    rows = []
    total = max(len(audit), 1)
    for tier in ordered_tiers + [tier for tier in counts.index if tier not in ordered_tiers]:
        count = int(counts.get(tier, 0))
        if count == 0:
            continue
        details = TEMPERATURE_PROXY_TIER_DETAILS.get(
            tier,
            {
                "label": tier,
                "meaning": "Tier not documented yet.",
                "allowed_use": "Review before using.",
            },
        )
        rows.append(
            {
                "tier": details["label"],
                "tier_code": tier,
                "rows": count,
                "share_pct": round(100 * count / total, 2),
                "meaning": details["meaning"],
                "allowed_use": details["allowed_use"],
            }
        )
    return pd.DataFrame(rows)


def build_temperature_proxy_map(audit: pd.DataFrame) -> go.Figure:
    map_frame = audit.dropna(subset=["lat", "lon"]).copy()
    figure = go.Figure()
    if map_frame.empty:
        return figure

    center_lat = float(map_frame["lat"].median())
    center_lon = float(map_frame["lon"].median())
    ordered_tiers = list(TEMPERATURE_PROXY_TIER_DETAILS)
    for tier in ordered_tiers:
        subset = map_frame[map_frame["temperature_proxy_tier"].eq(tier)]
        if subset.empty:
            continue
        details = TEMPERATURE_PROXY_TIER_DETAILS[tier]
        hover_text = (
            "<b>"
            + subset["well_name"].fillna("Unnamed well").astype(str)
            + "</b><br>Tier: "
            + subset["temperature_proxy_tier_label"].astype(str)
            + "<br>Nearest G10015 control: "
            + subset["nearest_g10015_control_code"].fillna("missing").astype(str)
            + "<br>Nearest distance: "
            + subset["nearest_g10015_control_distance_km"].round(1).astype(str)
            + " km<br>Screen status: "
            + subset["stability_result_status"].fillna("missing").astype(str)
        )
        figure.add_trace(
            go.Scattermapbox(
                lat=subset["lat"],
                lon=subset["lon"],
                mode="markers",
                name=details["label"],
                marker={
                    "size": details["size"],
                    "color": details["color"],
                    "opacity": details["opacity"],
                },
                text=hover_text,
                hovertemplate="%{text}<extra></extra>",
            )
        )

    figure.update_layout(
        height=560,
        margin={"l": 0, "r": 0, "t": 30, "b": 0},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.01,
            "xanchor": "left",
            "x": 0,
        },
        mapbox={
            "style": "open-street-map",
            "center": {"lat": center_lat, "lon": center_lon},
            "zoom": 4.0,
        },
    )
    return figure


def build_temperature_proxy_distance_figure(audit: pd.DataFrame) -> go.Figure:
    distance_frame = audit[
        audit["temperature_proxy_tier"].isin(
            [
                "proxy_candidate_near_g10015_control",
                "proxy_candidate_regional_g10015_control",
                "distant_from_g10015_controls",
            ]
        )
    ].copy()
    distance_frame = distance_frame.dropna(subset=["nearest_g10015_control_distance_km"])

    figure = go.Figure()
    if distance_frame.empty:
        return figure

    for tier, details in TEMPERATURE_PROXY_TIER_DETAILS.items():
        subset = distance_frame[distance_frame["temperature_proxy_tier"].eq(tier)]
        if subset.empty:
            continue
        figure.add_trace(
            go.Histogram(
                x=subset["nearest_g10015_control_distance_km"],
                name=details["label"],
                marker={"color": details["color"]},
                opacity=0.78,
                xbins={"start": 0, "end": 150, "size": 10},
            )
        )
    figure.update_layout(
        barmode="stack",
        height=360,
        margin={"l": 48, "r": 24, "t": 24, "b": 52},
        xaxis_title="Distance to nearest located G10015 temperature control (km)",
        yaxis_title="Rows",
        legend={"orientation": "h", "y": 1.05, "x": 0},
    )
    return figure


def render_guarded_stability_screen_product() -> None:
    screen_path = default_stability_screen_path(PROJECT_ROOT)
    screen = cached_stability_screen(str(PROJECT_ROOT))

    st.markdown("#### Guarded Baseline Stability Screen")
    if screen.empty:
        st.info(
            "No guarded baseline stability screen has been generated yet. "
            f"Expected path: `{project_relative_or_absolute(screen_path)}`."
        )
        return

    st.caption(
        "Baseline methane 5 ppt stability-admissibility screen. It is not "
        "hydrate proof, saturation evidence, producibility evidence, or a "
        "sweet-spot ranking."
    )
    calculated = screen["stability_result_status"].eq("calculated")
    no_interval = screen["stability_result_status"].eq("calculated_no_stable_interval")
    blocked = ~(calculated | no_interval)
    not_proof = screen["caveat_codes"].fillna("").str.contains("not_hydrate_proof").sum()

    cols = st.columns(5)
    cols[0].metric("Screen rows", f"{len(screen):,}")
    cols[1].metric("Calculated intervals", f"{int(calculated.sum()):,}")
    cols[2].metric("No stable interval", f"{int(no_interval.sum()):,}")
    cols[3].metric("Blocked rows", f"{int(blocked.sum()):,}")
    cols[4].metric("Not hydrate proof", f"{int(not_proof):,}")

    st.dataframe(
        stability_screen_summary_frame(screen),
        use_container_width=True,
        hide_index=True,
    )

    status_counts = (
        screen["stability_result_status"]
        .fillna("missing")
        .value_counts()
        .rename_axis("stability_result_status")
        .reset_index(name="rows")
    )
    confidence_counts = (
        screen["stability_confidence"]
        .fillna("missing")
        .value_counts()
        .rename_axis("stability_confidence")
        .reset_index(name="rows")
    )
    preview_columns = [
        "well_name",
        "tvd_m",
        "permafrost_base_m",
        "temperature_profile_code",
        "stability_result_status",
        "stability_confidence",
        "stability_top_m",
        "stability_base_m",
        "stability_thickness_m",
        "caveat_codes",
        "stability_notes",
    ]
    display_columns = [column for column in preview_columns if column in screen.columns]
    calculated_preview = (
        screen.loc[calculated, display_columns]
        .sort_values(["stability_confidence", "well_name"], ascending=[True, True])
        .head(30)
    )
    blocked_preview = (
        screen.loc[~calculated, display_columns]
        .sort_values(["stability_result_status", "well_name"], ascending=[True, True])
        .head(30)
    )

    source_root = active_stability_source_path(PROJECT_ROOT)
    ggd223_points = cached_ggd223_points(str(source_root))
    inventory = cached_g10015_temperature_inventory(str(PROJECT_ROOT))
    control_crosswalk = g10015_temperature_control_crosswalk_frame(inventory, ggd223_points)
    proxy_audit = temperature_proxy_candidate_audit_frame(screen, control_crosswalk)
    blank_summary = stability_blank_reason_summary_frame(screen)
    proxy_summary = temperature_proxy_tier_summary_frame(proxy_audit)
    temperature_model = cached_stability_temperature_model(str(PROJECT_ROOT))
    phase_curve = cached_methane_phase_curve(str(PROJECT_ROOT))
    sampled_profile_points = cached_g10015_temperature_profile_points(str(PROJECT_ROOT))

    status_tab, blanks_tab, temperature_tab, intervals_tab, tables_tab = st.tabs(
        [
            "Status Map",
            "Why Blanks",
            "Temperature Coverage",
            "Calculated Intervals",
            "Tables & Downloads",
        ]
    )

    with status_tab:
        st.markdown("##### 2D Screen Status Map")
        st.caption(
            "Point colors show calculation status only. Blue means the baseline "
            "screen could calculate an interval for that well; it does not mean "
            "hydrate was detected."
        )
        st.plotly_chart(
            build_stability_screen_map(screen),
            use_container_width=True,
            config={"displayModeBar": True, "responsive": True},
        )
        left, right = st.columns(2)
        left.dataframe(status_counts, use_container_width=True, hide_index=True)
        right.dataframe(confidence_counts, use_container_width=True, hide_index=True)

    with blanks_tab:
        st.markdown("##### Why So Many Rows Are Blank")
        st.caption(
            "Blank means the row failed at least one public-source gate. It is "
            "a data/readiness result, not a failed file transfer."
        )
        st.plotly_chart(
            build_blank_reason_bar_figure(blank_summary),
            use_container_width=True,
            config={"displayModeBar": True, "responsive": True},
        )
        st.dataframe(blank_summary, use_container_width=True, hide_index=True)
        st.info(
            "The largest blank group is the missing-temperature-profile gate. "
            "That reflects sparse direct G10015 coverage and current crosswalk "
            "rules; it should be audited before any proxy-temperature screen is run."
        )

    with temperature_tab:
        located_controls = int(
            control_crosswalk["coordinate_status"]
            .eq("located_from_committed_ggd223_control")
            .sum()
        )
        direct_profile_rows = int(
            proxy_audit["temperature_proxy_tier"].eq("direct_g10015_profile_match").sum()
        )
        near_proxy_rows = int(
            proxy_audit["temperature_proxy_tier"]
            .eq("proxy_candidate_near_g10015_control")
            .sum()
        )
        regional_proxy_rows = int(
            proxy_audit["temperature_proxy_tier"]
            .eq("proxy_candidate_regional_g10015_control")
            .sum()
        )
        metric_cols = st.columns(4)
        metric_cols[0].metric("G10015 codes located", f"{located_controls}/24")
        metric_cols[1].metric("Direct profile rows", f"{direct_profile_rows:,}")
        metric_cols[2].metric("Near proxy candidates", f"{near_proxy_rows:,}")
        metric_cols[3].metric("Regional candidates", f"{regional_proxy_rows:,}")
        st.caption(
            "Proxy tiers are planning labels only. They do not fill blank "
            "top/base/thickness values and are not part of the baseline screen."
        )
        st.plotly_chart(
            build_temperature_proxy_map(proxy_audit),
            use_container_width=True,
            config={"displayModeBar": True, "responsive": True},
        )
        st.dataframe(proxy_summary, use_container_width=True, hide_index=True)
        st.plotly_chart(
            build_temperature_proxy_distance_figure(proxy_audit),
            use_container_width=True,
            config={"displayModeBar": True, "responsive": True},
        )
        st.markdown("##### G10015/GGD223 Crosswalk Audit")
        st.caption(
            "Most G10015 codes can be located through committed GGD223 controls. "
            "A few code/location gaps should be resolved from G10015 location "
            "metadata before broad proxy screening."
        )
        st.dataframe(control_crosswalk, use_container_width=True, hide_index=True)
        st.markdown(
            """
Source anchors: [NSIDC G10015](https://nsidc.org/data/g10015/versions/1),
[NSIDC GGD223](https://nsidc.org/data/ggd223/versions/1), and
[USGS SIR 2008-5175](https://pubs.usgs.gov/sir/2008/5175/pdf/SIR08-5175_508.pdf).
"""
        )

    with intervals_tab:
        st.markdown("##### Selected Well Temperature/Phase Audit")
        st.caption(
            "This plot uses committed public products: the methane 5 ppt phase "
            "boundary, sampled measured G10015 profile points when exported, "
            "OSL modeled temperature at key depths, and screen top/base "
            "markers where available."
        )
        if sampled_profile_points.empty:
            st.info(
                "The sampled measured G10015 profile export is not committed yet. "
                "Run the public stability rebuild in OSL to add full curve traces."
            )
        selection_source = screen.copy()
        selection_source["selection_priority"] = selection_source[
            "stability_result_status"
        ].map(
            {
                "calculated": 0,
                "calculated_no_stable_interval": 1,
                "blocked_phase_curve_range_insufficient": 2,
                "blocked_missing_temperature_profile": 3,
                "blocked_missing_depth": 4,
                "outside_au_context": 5,
            }
        ).fillna(9)
        selection_source = selection_source.sort_values(
            ["selection_priority", "well_name", "object_id"]
        )
        selection_options = [
            (
                f"{row.well_name} | {row.stability_result_status} | "
                f"object {row.object_id}"
            )
            for row in selection_source.itertuples()
        ]
        selected_label = st.selectbox(
            "Selected well audit plot",
            selection_options,
            index=0,
        )
        selected_index = selection_options.index(selected_label)
        selected_row = selection_source.iloc[selected_index]
        st.plotly_chart(
            build_selected_well_phase_audit_figure(
                selected_row,
                temperature_model,
                phase_curve,
                sampled_profile_points,
            ),
            use_container_width=True,
            config={"displayModeBar": True, "responsive": True},
        )
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "well_name": selected_row.get("well_name"),
                        "screen_status": selected_row.get("stability_result_status"),
                        "temperature_profile": selected_row.get("temperature_profile_code"),
                        "temperature_source": selected_row.get("temperature_source"),
                        "top_m": selected_row.get("stability_top_m"),
                        "base_m": selected_row.get("stability_base_m"),
                        "thickness_m": selected_row.get("stability_thickness_m"),
                        "caveats": selected_row.get("caveat_codes"),
                    }
                ]
            ),
            use_container_width=True,
            hide_index=True,
        )
        st.markdown("##### Calculated Interval Depth View")
        st.caption(
            "The 22 calculated rows are plotted as top-to-base screen intervals. "
            "These are baseline admissibility intervals, not confirmed hydrate zones."
        )
        st.plotly_chart(
            build_stability_interval_depth_figure(screen),
            use_container_width=True,
            config={"displayModeBar": True, "responsive": True},
        )
        st.markdown("##### Calculated Interval Rows")
        if calculated_preview.empty:
            st.info("No rows passed every screen gate in this run.")
        else:
            st.dataframe(calculated_preview, use_container_width=True, hide_index=True)

    with tables_tab:
        st.markdown("##### Blocked Or No-Interval Sample")
        st.dataframe(blocked_preview, use_container_width=True, hide_index=True)
        audit_columns = [
            "well_name",
            "lat",
            "lon",
            "tvd_m",
            "stability_result_status",
            "temperature_proxy_tier_label",
            "temperature_profile_code",
            "nearest_g10015_control_code",
            "nearest_g10015_control_distance_km",
            "stability_confidence",
            "caveat_codes",
        ]
        st.markdown("##### Downloadable Diagnostic Audit")
        st.dataframe(
            proxy_audit[[column for column in audit_columns if column in proxy_audit.columns]]
            .head(60),
            use_container_width=True,
            hide_index=True,
        )
        st.download_button(
            "Download guarded stability screen CSV",
            screen.to_csv(index=False).encode("utf-8"),
            file_name=screen_path.name,
            mime="text/csv",
            use_container_width=True,
        )
        st.download_button(
            "Download blank/proxy diagnostic CSV",
            proxy_audit.to_csv(index=False).encode("utf-8"),
            file_name="stability_blank_proxy_diagnostic_2026-06-14.csv",
            mime="text/csv",
            use_container_width=True,
        )


def render_stability_parameter_readiness() -> None:
    st.markdown("#### Stability Pipeline Readiness")
    st.caption(
        "Current input status before calculating stability top, base, and thickness. "
        "Rows marked context or planned should not be treated as final model features yet."
    )
    st.dataframe(
        stability_parameter_readiness_frame(),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown("#### Input Capability Matrix")
    st.caption(
        "What the public inputs can support now, what remains scenario-only, "
        "and what must wait for approved runtime data."
    )
    st.dataframe(
        stability_input_capability_matrix_frame(),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown("#### OpenScienceLab Pull Triggers")
    st.caption(
        "When the public repo is enough, and when the heavy source bundle in "
        "OpenScienceLab is required."
    )
    st.dataframe(
        stability_osl_pull_triggers_frame(),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown("#### Final Website Product Shape")
    st.caption(
        "Target website sections for the guarded baseline stability workflow, "
        "with the claims each section must avoid."
    )
    st.dataframe(
        stability_website_product_spec_frame(),
        use_container_width=True,
        hide_index=True,
    )


def render_structural_explorer() -> None:
    st.markdown('<div class="atlas-kicker">Subsurface context</div>', unsafe_allow_html=True)
    st.title("Structural Explorer")
    st.write(
        "Compare regional structural horizons as lightweight surface planes. The "
        "horizontal axes use longitude and latitude, while optional context overlays "
        "connect the subsurface model to the North Slope study area."
    )
    cols = st.columns([2, 1])
    selected_surfaces = cols[0].multiselect(
        "Visible structural horizons",
        STRUCTURAL_HORIZONS,
        default=["NStopo", "NSLCU", "NSshublik", "NSbasement"],
        format_func=lambda name: f"{name} - {SURFACE_CATALOG[name]['Label']}",
    )
    cells_per_surface = cols[1].select_slider(
        "Surface detail",
        options=[1500, 3000, 6000, 12000],
        value=3000,
        format_func=lambda cells: f"Up to {cells:,} cells / horizon",
    )
    selected_overlays = st.multiselect(
        "Regional context overlays",
        CONTEXT_OVERLAYS,
        default=["North Slope study-area boundary", "Assessment-unit outlines"],
    )

    if selected_surfaces:
        st.caption(
            f"Rendering up to {cells_per_surface * len(selected_surfaces):,} surface cells. "
            "Interval-thickness grids remain documented in the Data Library but are "
            "not drawn as structural planes."
        )
        st.plotly_chart(
            build_geographic_structural_figure(
                selected_surfaces,
                cells_per_surface,
                selected_overlays,
            ),
            use_container_width=True,
        )
    else:
        st.info("Select at least one structural layer to draw the 3D view.")

    render_stability_source_bundle()

    st.markdown("### Structural Layer Labels")
    surface_rows = [
        {
            "Code": code,
            "Plain-language label": metadata["Label"],
            "Meaning": metadata["Description"],
            "Boundary tag": "PUBLIC-SOURCE ATLAS",
        }
        for code, metadata in SURFACE_CATALOG.items()
    ]
    st.dataframe(surface_rows, use_container_width=True, hide_index=True)

    show_heavy_scene = st.checkbox(
        "Show original heavy HTML scene fallback",
        value=False,
        key="show_heavy_structural_scene",
    )
    if show_heavy_scene:
        st.warning(
            "These notebook exports are preserved for completeness. They can lag "
            "because they embed much larger point collections."
        )
        label = st.selectbox("Original structural scene", list(STRUCTURAL_SCENES))
        if st.button("Load original heavy scene"):
            render_scene(STRUCTURAL_SCENES[label], height=870)


def render_data_library(files: list[dict[str, object]]) -> None:
    st.markdown('<div class="atlas-kicker">Public-source inventory</div>', unsafe_allow_html=True)
    st.title("Data Library")
    st.write(
        "The curated layer catalog explains the analytical role of the main data "
        "products. The repository browser below provides the full file-level view."
    )
    st.dataframe(LAYER_CATALOG, use_container_width=True, hide_index=True)
    st.caption(
        "Boundary tags label the public atlas data products. Future approved "
        "restricted inputs must remain outside this hosted repository."
    )

    st.markdown("### Repository Browser")
    extensions = sorted({str(row["Type"]) for row in files})
    cols = st.columns([1, 1])
    selected = cols[0].multiselect("File types", extensions, default=extensions)
    query = cols[1].text_input("Path contains", placeholder="Example: gis_ready_surfaces")
    filtered = [
        row
        for row in files
        if str(row["Type"]) in selected and query.lower() in str(row["Path"]).lower()
    ]
    st.dataframe(
        [{key: row[key] for key in ("Path", "Type", "Size")} for row in filtered],
        use_container_width=True,
        hide_index=True,
    )
    st.caption(f"Showing {len(filtered):,} of {len(files):,} repository files")

    st.markdown("### Known Quality Notes")
    st.warning(
        "The public well inventory contains 10,250 records. Of these, 9,894 have "
        "point geometry and 356 currently lack usable geometry. The atlas should "
        "preserve that distinction rather than silently treating all records as mappable."
    )


def render_framework() -> None:
    st.markdown('<div class="atlas-kicker">Manuscript blueprint</div>', unsafe_allow_html=True)
    st.title("Research Framework")
    st.write(
        "The manuscript is the scientific backbone of the application. It treats "
        "gas hydrate as a coupled petroleum-system and rock-physics outcome rather "
        "than a single-map or single-log anomaly."
    )
    for number, title, description in FRAMEWORK_STAGES:
        st.markdown(
            f'<div class="atlas-step"><strong>{number} · {title}</strong><br>{description}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("### Decision Rules To Preserve")
    st.markdown(
        """
        1. The gas hydrate stability zone defines where hydrate **can** exist, not where it must exist.
        2. Reservoir capacity, hydrate occupancy, saturation, and recoverability are separate outcomes.
        3. High resistivity alone is not a defensible hydrate label.
        4. Regional geology should constrain interval interpretation, not replace log-derived evidence.
        5. Producibility requires retained permeability, connected pore volume, pressure communication, and mechanical stability.
        """
    )


def render_future_engine() -> None:
    st.markdown('<div class="atlas-kicker">Synthetic planning scaffold</div>', unsafe_allow_html=True)
    st.title("Log Scaffold")
    st.caption("Formerly listed as Future Well-Log Engine.")
    st.write(
        "This presentation-ready scaffold previews the outputs planned for the later "
        "runtime-only analysis module. It contains synthetic example records only."
    )
    st.warning(
        f"{SYNTHETIC_LABEL}. PUBLIC-SOURCE PLANNING SCAFFOLD. Do not upload approved "
        "well logs, core data, identifiers, populated sensitive outputs, derived "
        "sensitive results, or credentials to this hosted dashboard."
    )

    cols = st.columns(3)
    blocks = [
        (
            "Expected inputs",
            "<code>DEPTH</code>, <code>GR</code>, <code>RHOB</code>, "
            "<code>DT</code>, <code>DTS</code>, <code>Rt</code>, porosity "
            "channels, and NMR where available.",
        ),
        (
            "Derived features",
            "Shale volume, porosity, saturation proxies, <code>Vp</code>, "
            "<code>Vs</code>, <code>Vp/Vs</code>, elastic moduli, stress, "
            "permeability-risk proxy, and QA flags.",
        ),
        (
            "Outputs",
            "Admissibility, reservoir quality, phase evidence, saturation proxy, core confidence, uncertainty, and separate producibility screening.",
        ),
    ]
    for col, (title, text) in zip(cols, blocks):
        col.markdown(
            f'<div class="atlas-card"><h4>{title}</h4><p>{text}</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown("### Scientific Rules Kept Visible")
    st.markdown(
        """
        1. GHSZ is necessary but not sufficient.
        2. High Rt is evidence, not a hydrate label.
        3. Good reservoir sand can contain no hydrate.
        4. Geology and seismic context constrain confidence; they do not replace direct log evidence.
        5. NMR-density saturation is preferred where NMR exists; Archie is a supplementary cross-check with uncertainty flags.
        6. Hydrate occurrence, saturation, and producibility remain separate outputs.
        7. Validation must split by well, not randomly by depth sample.
        8. Maximum hydrate saturation is not automatically the best production target.
        """
    )

    logs = load_runtime_data()
    intervals = screen_intervals(logs)
    core = synthetic_core_placeholders()
    calibrated_core = nearby_log_calibration(logs, core)

    tabs = st.tabs(
        [
            "Runtime Readiness & ML Plan",
            "ML Visual Architecture",
            "Variable Range Explorer",
            "Header & Track Blueprint",
            "Sweet-Spot Evidence Model",
            "Equation-to-Decision Map",
            "Hydrate Interpretation Range Guide",
            "Interval Screening Scaffold",
            "Core Calibration Scaffold",
            "Presentation Outputs",
        ]
    )
    with tabs[0]:
        render_runtime_readiness(logs)
    with tabs[1]:
        render_ml_visual_architecture()
    with tabs[2]:
        render_variable_range_explorer(logs)
    with tabs[3]:
        render_header_blueprint()
    with tabs[4]:
        render_sweet_spot_evidence_model(intervals)
    with tabs[5]:
        render_equation_decision_map()
    with tabs[6]:
        render_range_guide()
    with tabs[7]:
        render_interval_screen(intervals)
    with tabs[8]:
        render_core_calibration(calibrated_core)
    with tabs[9]:
        render_presentation_outputs(logs, intervals, calibrated_core)

    st.markdown("### Planned Runtime Analysis Sequence")
    sequence = [
        ("1", "Stability admissibility", "Screen pressure-temperature context without using it as a positive label."),
        ("2", "Reservoir screening", "Identify clean reservoir intervals and preserve good-sand/no-hydrate outcomes."),
        ("3", "Phase classification", "Use multi-log evidence to distinguish hydrate, gas, water, and uncertainty."),
        ("4", "Charge and structure", "Apply regional context as a constraint on interval-scale evidence."),
        ("5", "Producibility ranking", "Separate detectability and saturation from pressure communication and flow risk."),
    ]
    for number, title, description in sequence:
        st.markdown(f"**{number}. {title}**  \n{description}")

    st.info(
        "Transfer point: the reusable calculation layer is isolated behind a runtime "
        "configuration adapter. Authorized LAS/CSV loading should be added and run "
        "locally inside the approved DOE environment."
    )


def render_runtime_readiness(logs: pd.DataFrame) -> None:
    st.subheader("Runtime Readiness & ML Plan")
    st.caption(
        f"{SYNTHETIC_LABEL} | Header-derived synthetic records generated from "
        "Excel schema references, project answers, and Chong et al. (2022)."
    )
    features = add_standard_features(logs)
    report = validate_log_table(logs)
    coverage = curve_coverage_frame(logs)
    outputs = output_readiness_frame(features)
    splits = grouped_well_split_frame(logs)

    ready_outputs = int((outputs["Status"] == "Ready").sum())
    partial_outputs = int((outputs["Status"] == "Partial").sum())
    blocked_outputs = int((outputs["Status"] == "Blocked").sum())
    metrics = st.columns(4)
    metrics[0].metric("Input status", report.status.title())
    metrics[1].metric("Ready outputs", ready_outputs)
    metrics[2].metric("Partial outputs", partial_outputs)
    metrics[3].metric("Blocked outputs", blocked_outputs)

    st.markdown("#### Curve Coverage and Routing")
    st.dataframe(coverage, use_container_width=True, hide_index=True)

    st.markdown("#### Output Readiness")
    st.dataframe(outputs, use_container_width=True, hide_index=True)
    st.info(
        "NMR-density saturation is preferred when NMR exists. Missing NMR does "
        "not block the full workflow: electrical saturation remains a flagged "
        "cross-check, and the model can test other log combinations."
    )

    st.markdown("#### Complete-Well Evaluation Split")
    st.dataframe(splits, use_container_width=True, hide_index=True)
    st.error(
        "Do not randomly split neighboring depth rows across train and test. "
        "The final model must demonstrate performance on wells excluded from training."
    )

    st.markdown("#### Planned 71-Well Cohort Design")
    cohort_plan = project_cohort_plan_frame(
        total_wells=PROJECT_COHORT_ASSUMPTIONS["Estimated total wells"],
        known_fraction=PROJECT_COHORT_ASSUMPTIONS["Known development fraction"],
    )
    st.dataframe(cohort_plan, use_container_width=True, hide_index=True)
    st.caption(
        "Working estimate: 14 known wells support model development and 57 wells "
        "form the prediction cohort. Final counts depend on label completeness and "
        "whether all wells contain compatible curves."
    )
    st.warning(
        "The 20% known-well cohort cannot be used entirely for fitting. Whole wells "
        "inside that cohort must remain unseen for validation and a locked test."
    )
    st.caption(
        "Normalization ranges, imputers, feature selection, and any learned variable "
        "weights must be fitted on training wells only, then applied unchanged to "
        "validation, locked-test, and prediction wells."
    )

    st.markdown("#### Supervised Target Contract")
    st.dataframe(pd.DataFrame(TARGET_LABEL_CONTRACT), use_container_width=True, hide_index=True)
    st.info(
        "Current assumption: NMR and the screenshot-listed fields are available. "
        "Saturation training must still identify the authoritative target as supplied, "
        "NMR-derived, core-calibrated, or documented interpreted saturation. The same "
        "normalized log families may support both outputs, but classification and "
        "saturation remain separate models or model heads."
    )

    st.markdown("#### Attached-Paper Feature Contract")
    st.write(
        "The source paper tests density, porosity, resistivity, gamma ray, Vp, "
        "and Vs. The runtime keeps each feature physically interpretable and "
        "records missing-curve routes instead of silently inventing measurements."
    )
    st.code("\n".join(CHONG_ML_FEATURE_COLUMNS), language="text")

    issues = readiness_frame(report)
    if issues.empty:
        st.success("No blocking synthetic input issues were detected.")
    else:
        st.markdown("#### Input Issues")
        st.dataframe(issues, use_container_width=True, hide_index=True)


def render_ml_visual_architecture() -> None:
    st.subheader("Topic 5: ML Evidence and Well-Log Scaffold")
    st.caption(
        "Updated Topic 5 brings the evidence atlas and satellite-style regional "
        "variables forward, then connects them to the well-log scaffold, ML model "
        "branches, and output visualizations."
    )
    st.info(
        "Topic 5 now uses the newer well-log ML scaffold direction: regional atlas "
        "context first, synthetic/header-derived logs second, and explainable model "
        "outputs last. The hosted app still avoids approved logs, core rows, and "
        "sensitive derived outputs."
    )

    metrics = st.columns(3)
    metrics[0].metric("Scaffold sync", "2026-06-02")
    metrics[1].metric("Evidence update", "2026-06-09")
    metrics[2].metric("Validation unit", "Whole wells")

    st.markdown("#### Evidence Atlas Priority")
    st.dataframe(
        pd.DataFrame(TOPIC5_EVIDENCE_ATLAS_PRIORITY),
        use_container_width=True,
        hide_index=True,
    )

    render_processing_sketch(
        "ml_architecture",
        ML_ARCHITECTURE,
        "Header-to-Model Knowledge Graph",
        "Concrete headers, regional context, and equations stay attached to every model output.",
        height=430,
    )
    st.warning(
        "Target fields such as hydrate saturation, NMR-derived saturation, phase "
        "labels, and sweet-spot rankings are labels or review outputs. They cannot "
        "be fitted as input features."
    )
    render_processing_sketch(
        "decision_tree",
        {"nodes": HYDRATE_DECISION_TREE},
        "Hydrate Interpretation Decision Tree",
        "The model should preserve no-hydrate, gas, bad-hole, and uncertainty branches.",
        height=430,
    )

    cols = st.columns(2)
    with cols[0]:
        st.markdown("#### Visual Contract")
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Visual": "Evidence atlas context",
                        "Source basis": "Public North Slope atlas, assessment units, structural layers, and well inventory",
                        "Reader takeaway": "Regional and satellite-style variables influence confidence and triage before interval scoring.",
                    },
                    {
                        "Visual": "Knowledge graph",
                        "Source basis": "Excel header roles; Chong feature set; equation library",
                        "Reader takeaway": "Inputs, features, labels, and outputs are separate.",
                    },
                    {
                        "Visual": "Well-log scaffold",
                        "Source basis": "Synthetic/header-derived GR, Rt, RHOB, NMR, Vp, Vs tracks",
                        "Reader takeaway": "The once-blank scaffold now shows the output panel and downloadable evidence tables.",
                    },
                    {
                        "Visual": "Decision tree",
                        "Source basis": "Sweet-spot science basis; interpretation rules",
                        "Reader takeaway": "Hydrate is assigned only after staged evidence survives.",
                    },
                    {
                        "Visual": "Whole-well split",
                        "Source basis": "Runtime validation plan",
                        "Reader takeaway": "Models are tested on unseen wells, not adjacent rows.",
                    },
                ]
            ),
            use_container_width=True,
            hide_index=True,
        )
    with cols[1]:
        st.markdown("#### Concrete Feature Families")
        st.dataframe(
            pd.DataFrame(
                [
                    {"Family": "Regional context", "Fields": "assessment unit, structural position, public well context, atlas layer flags", "Use": "Confidence, grouping, and review triage"},
                    {"Family": "Measured", "Fields": "GR, Rt, RHOB, NMR, Vp, Vs, caliper", "Use": "Model inputs after QC"},
                    {"Family": "Derived", "Fields": "Vsh, density porosity, Vp/Vs, acoustic impedance, lambda-rho, mu-rho", "Use": "Physics-backed features"},
                    {"Family": "Targets", "Fields": "Sgh, S_h, NMR_SAT, phase class, sweet-spot rank", "Use": "Supervision or review only"},
                ]
            ),
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("#### Embedded Well-Log Scaffold Outputs")
    st.dataframe(
        pd.DataFrame(TOPIC5_SCAFFOLD_OUTPUTS),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("#### How AI Helps This Workflow")
    st.dataframe(
        pd.DataFrame(TOPIC5_AI_WORKFLOW),
        use_container_width=True,
        hide_index=True,
    )

def render_variable_range_explorer(logs: pd.DataFrame) -> None:
    st.subheader("Variable Range Explorer")
    st.caption(f"{SYNTHETIC_LABEL} | Summary statistics are descriptive planning outputs, not universal thresholds.")
    wells = sorted(logs["well_alias"].unique())
    cols = st.columns([1, 1, 2])
    well = cols[0].selectbox("Synthetic location / well alias", wells)
    variable = cols[1].selectbox("Variable", list(VARIABLES), format_func=lambda name: VARIABLES[name][0])
    depth_min, depth_max = logs["depth_m"].min(), logs["depth_m"].max()
    depth_range = cols[2].slider("Depth interval (m)", float(depth_min), float(depth_max), (float(depth_min), float(depth_max)), step=5.0)
    subset = logs[(logs["well_alias"] == well) & logs["depth_m"].between(*depth_range)]
    label, unit = VARIABLES[variable]
    figure = go.Figure(go.Scatter(x=subset[variable], y=subset["depth_m"], mode="lines", name=label))
    figure.update_layout(title=f"{SYNTHETIC_LABEL} | {well} | {label}", xaxis_title=f"{label} ({unit})", yaxis_title="Depth (m)", height=530)
    figure.update_yaxes(autorange="reversed")
    if variable in SCREENING_BANDS:
        x0, x1, note = SCREENING_BANDS[variable]
        figure.add_vrect(
            x0=x0,
            x1=x1,
            fillcolor="rgba(22, 125, 141, 0.15)",
            line_width=0,
            annotation_text="working review band",
            annotation_position="top left",
        )
        figure.add_annotation(
            x=x1,
            y=float(subset["depth_m"].quantile(0.25)),
            text=note,
            showarrow=True,
            arrowhead=2,
            ax=70,
            ay=-45,
            bgcolor="rgba(255,255,255,0.92)",
            bordercolor="#167d8d",
            borderwidth=1,
            font={"size": 11},
        )
    st.plotly_chart(figure, use_container_width=True)
    summary = variable_range_summary(logs, [variable], well, depth_range)
    st.dataframe(summary, use_container_width=True, hide_index=True)
    st.download_button("Download variable-range table (CSV)", csv_bytes(summary), "synthetic_variable_range_table.csv", "text/csv", key="range_explorer_table")

    st.markdown("#### Cross-Well Comparison")
    cross_well = pd.concat(
        [
            variable_range_summary(logs, [variable], alias, depth_range).assign(**{"Well alias": alias})
            for alias in wells
        ],
        ignore_index=True,
    )
    st.plotly_chart(cross_well_range_figure(cross_well, label), use_container_width=True)
    st.dataframe(cross_well, use_container_width=True, hide_index=True)


def render_header_blueprint() -> None:
    st.subheader("Header & Track Blueprint")
    st.caption(
        "Derived from three Excel header/schema references. Names, units, roles, "
        "and layout guide the scaffold; no user-supplied data rows or reference "
        "values are used."
    )
    st.warning(
        "Measured inputs, derived features, QC/alignment fields, and targets remain "
        "separate. Hydrate saturation and water-saturation fields are not ML inputs."
    )
    st.dataframe(
        pd.DataFrame(HEADER_SCHEMA_BLUEPRINT),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown(
        """
        **Planned track order:** depth and alignment; borehole QC; lithology;
        porosity; electrical response; elastic response; interpretation and
        calibration; uncertainty and readiness.

        Unit-aware loading is required before these headers can drive scientific
        calculations. In particular, depth appears in feet and meters, while bulk
        density appears in both `g/cc` and `kg/m3` conventions.
        """
    )


def render_sweet_spot_evidence_model(intervals: pd.DataFrame) -> None:
    st.subheader("Synthetic Sweet-Spot Evidence Model")
    st.caption(
        "Research-backed directional logic applied to synthetic data. The working "
        "thresholds are demonstrative and require local calibration before scientific use."
    )
    st.error(
        "A sweet spot is not the row with the largest hydrate-saturation proxy. "
        "It is an interval where hydrate evidence, reservoir quality, retained flow "
        "capacity, QC, and uncertainty remain jointly defensible."
    )
    st.dataframe(
        pd.DataFrame(SWEET_SPOT_EVIDENCE_MODEL),
        use_container_width=True,
        hide_index=True,
    )

    candidates = intervals[
        intervals["Synthetic sweet-spot review lane"].str.contains(
            "candidate sweet-spot",
            na=False,
        )
    ]
    st.markdown("#### Explainable Synthetic Candidates")
    if candidates.empty:
        st.info("No synthetic intervals currently satisfy the complete review lane.")
        return
    st.dataframe(
        candidates[
            [
                "Well alias",
                "Top depth (m)",
                "Base depth (m)",
                "Phase-classification evidence",
                "Hydrate-saturation proxy",
                "Permeability-retention proxy",
                "Evidence domains passed",
                "Blocking domains",
                "Interpretation summary",
                "Uncertainty flags",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


def render_equation_decision_map() -> None:
    st.subheader("Equation-to-Decision Map")
    st.caption(
        "This is the scaffold direction for the real-data project: measured logs become derived "
        "features, derived features feed staged physics gates, and only then does ML classify intervals."
    )
    st.info(
        "The key design choice: every future model feature must keep its physical meaning attached. "
        "That prevents the dashboard from saying 'hydrate' just because one curve looks interesting."
    )
    st.markdown("#### Derived Equation Library")
    st.dataframe(pd.DataFrame(EQUATION_LIBRARY), use_container_width=True, hide_index=True)

    st.markdown("#### Classification Workflow")
    st.dataframe(pd.DataFrame(CLASSIFICATION_WORKFLOW), use_container_width=True, hide_index=True)

    st.markdown("#### Rock-Type and Overburden Context")
    st.write(
        "Rock type and stress change the meaning of the same log value. A high-resistivity, "
        "high-stiffness interval in clean sand means something different than the same response "
        "in ice-bearing sediment, coal, carbonate, or a washed-out borehole."
    )
    st.dataframe(pd.DataFrame(ROCKTYPE_CONTEXT_GUIDE), use_container_width=True, hide_index=True)


def render_range_guide() -> None:
    st.subheader("Hydrate Interpretation Range Guide")
    st.caption(
        "Manuscript-backed working tendencies for planning. These ranges overlap competing "
        "end members and must not be treated as universal thresholds."
    )
    st.error("High resistivity alone is not a hydrate label. Stability is necessary but not sufficient.")
    st.dataframe(pd.DataFrame(RANGE_GUIDE), use_container_width=True, hide_index=True)
    st.markdown("#### Synthetic Sweet-Spot Planning Guide")
    st.write(
        "These saturation-proxy bands are presentation and expert-review lanes. "
        "They are not universal thresholds and they do not replace locally calibrated "
        "multi-log interpretation inside the authorized environment."
    )
    st.dataframe(pd.DataFrame(SWEET_SPOT_GUIDE), use_container_width=True, hide_index=True)
    st.markdown("#### Public Science Anchors")
    st.dataframe(pd.DataFrame(PUBLIC_SCIENCE_REFERENCES), use_container_width=True, hide_index=True)


def render_interval_screen(intervals: pd.DataFrame) -> None:
    st.subheader("Interval Screening Scaffold")
    st.caption(f"{SYNTHETIC_LABEL} | Separate staged outputs preserve good-sand/no-hydrate and expert-review outcomes.")
    well = st.selectbox("Synthetic interval-screen well alias", sorted(intervals["Well alias"].unique()))
    selected = intervals[intervals["Well alias"] == well]
    st.dataframe(selected, use_container_width=True, hide_index=True)
    st.download_button("Download interval-interpretation table (CSV)", csv_bytes(selected), "synthetic_interval_interpretation.csv", "text/csv", key="interval_screen_table")


def render_core_calibration(calibrated_core: pd.DataFrame) -> None:
    st.subheader("Core Calibration Scaffold")
    st.caption(
        f"{SYNTHETIC_LABEL} | Future approved pressure-core observations remain local. "
        "The placeholder table shows depth-match uncertainty and nearby-log linkage."
    )
    st.dataframe(calibrated_core, use_container_width=True, hide_index=True)
    st.download_button("Download core-to-log calibration table (CSV)", csv_bytes(calibrated_core), "synthetic_core_to_log_calibration.csv", "text/csv", key="core_calibration_table")


def render_presentation_outputs(logs: pd.DataFrame, intervals: pd.DataFrame, calibrated_core: pd.DataFrame) -> None:
    st.subheader("Presentation Outputs")
    st.caption(
        f"{SYNTHETIC_LABEL} | Topic 5 embedded well-log scaffold synced to the newer "
        "ML evidence direction."
    )
    st.info(
        "This is the embedded well-log scaffold for Topic 5: it shows the interval-level "
        "log panel, variable range table, cross-well comparison, uncertainty summary, "
        "and model diagnostics used to explain how AI helped produce and review outputs."
    )
    st.markdown("#### Output Visualization Map")
    st.dataframe(
        pd.DataFrame(TOPIC5_SCAFFOLD_OUTPUTS),
        use_container_width=True,
        hide_index=True,
    )
    well = st.selectbox("Presentation-output synthetic well", sorted(logs["well_alias"].unique()))
    panel = well_log_panel(logs, well)
    st.plotly_chart(panel, use_container_width=True)
    st.download_button("Download well-log panel (HTML)", figure_html_bytes(panel), "synthetic_well_log_panel.html", "text/html", key="presentation_well_panel")

    range_table = variable_range_summary(logs, well_alias=well)
    st.dataframe(range_table, use_container_width=True, hide_index=True)
    st.download_button("Download variable-range table (CSV)", csv_bytes(range_table), "synthetic_variable_range_table.csv", "text/csv", key="presentation_range_table")

    interval_table = intervals[intervals["Well alias"] == well]
    st.download_button("Download interval-interpretation table (CSV)", csv_bytes(interval_table), "synthetic_interval_interpretation.csv", "text/csv", key="presentation_interval_table")

    cross_well = pd.concat(
        [
            variable_range_summary(logs, ["rt_ohm_m"], alias).assign(**{"Well alias": alias})
            for alias in sorted(logs["well_alias"].unique())
        ],
        ignore_index=True,
    )
    cross_well_figure = cross_well_range_figure(cross_well, "Resistivity Rt")
    st.plotly_chart(cross_well_figure, use_container_width=True)
    st.download_button("Download cross-well comparison (HTML)", figure_html_bytes(cross_well_figure), "synthetic_cross_well_comparison.html", "text/html", key="presentation_cross_well")
    st.download_button("Download core-to-log table (CSV)", csv_bytes(calibrated_core), "synthetic_core_to_log_calibration.csv", "text/csv", key="presentation_core_table")

    uncertainty = intervals[["Data label", "Well alias", "Top depth (m)", "Base depth (m)", "Uncertainty flags"]]
    st.download_button("Download uncertainty summary (CSV)", csv_bytes(uncertainty), "synthetic_uncertainty_summary.csv", "text/csv", key="presentation_uncertainty")

    confusion, calibration = model_placeholder_figures()
    cols = st.columns(2)
    cols[0].plotly_chart(confusion, use_container_width=True)
    cols[1].plotly_chart(calibration, use_container_width=True)
    cols[0].download_button("Download placeholder confusion matrix (HTML)", figure_html_bytes(confusion), "synthetic_placeholder_confusion_matrix.html", "text/html", key="presentation_confusion")
    cols[1].download_button("Download placeholder calibration panel (HTML)", figure_html_bytes(calibration), "synthetic_placeholder_calibration_panel.html", "text/html", key="presentation_calibration")


def render_project_plan() -> None:
    content = architecture_content()
    vision = vision_content()
    st.markdown('<div class="atlas-kicker">Project execution</div>', unsafe_allow_html=True)
    st.title("Project Plan")
    st.write("Built public pieces are ready; approved-data steps activate only inside the runtime boundary.")
    render_processing_sketch(
        "built_next",
        BUILT_NEXT,
        "Built Now / Activate Next",
        "A visual split between current public/synthetic assets and approved-data-dependent work.",
        height=390,
    )
    col1, col2 = st.columns(2)
    with col1:
        render_processing_sketch(
            "blocks",
            {"heading": "Blockers", "rows": BLOCKERS},
            "Current Blockers",
            "Open dependencies affect workbook mapping, labels, and source provenance.",
            height=280,
        )
    with col2:
        render_processing_sketch(
            "blocks",
            {"heading": "Deliverables", "rows": DELIVERABLES},
            "Deliverable Path",
            "Website visuals feed Word and PowerPoint; approved outputs remain runtime-only.",
            height=280,
        )

    if not content or not vision:
        st.error("The vision or architecture tracker is not available in this deployment.")
        return

    st.markdown("### Next Three Actions")
    next_actions = [
        "Recover the full Excel workbook and remaining public sources.",
        "Confirm saturation targets, NMR role, phase labels, and whole-well splits.",
        "Implement workbook-derived rules and replace placeholders with validated results.",
    ]
    for action in next_actions:
        st.markdown(f'<div class="atlas-step">{escape(action)}</div>', unsafe_allow_html=True)

    workstreams = markdown_table(markdown_section(content, "Workstream Activity Map"))
    blockers = markdown_table(markdown_section(content, "Blockers and Risks"))
    if not workstreams.empty:
        statuses = workstreams["Status"].astype(str)
        cols = st.columns(4)
        cols[0].metric("Workstreams", len(workstreams))
        cols[1].metric(
            "Active",
            int(statuses.str.startswith("In progress").sum() + statuses.str.startswith("Partial").sum()),
        )
        cols[2].metric(
            "Waiting / blocked",
            int(statuses.str.startswith("Waiting").sum() + statuses.str.startswith("Blocked").sum()),
        )
        cols[3].metric("Complete", int(statuses.str.startswith("Complete").sum()))

    with st.expander("Detailed tracker"):
        st.markdown("#### Project Vision")
        st.markdown(markdown_section(vision, "Project Vision"))
        st.markdown("#### Current Priority")
        st.markdown(markdown_section(content, "Current Priority"))
        if not workstreams.empty:
            st.markdown("#### Workstream Status")
            st.markdown('<div class="roadmap-desktop">', unsafe_allow_html=True)
            st.dataframe(workstreams, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown(roadmap_cards(workstreams), unsafe_allow_html=True)
        if not blockers.empty:
            st.markdown("#### Blockers and Risks")
            st.dataframe(blockers, use_container_width=True, hide_index=True)
        st.markdown("#### Near-Term Sequence")
        st.markdown(markdown_section(content, "Near-Term Sequence"))


def render_explore_north_slope(files: list[dict[str, object]]) -> None:
    st.markdown('<div class="atlas-kicker">Public regional context</div>', unsafe_allow_html=True)
    st.title("Explore North Slope")
    st.write("Public GIS and structural layers constrain interpretation; they do not classify hydrate by themselves.")
    tabs = st.tabs(["Regional Map", "3D Structure", "Data & Sources"])
    with tabs[0]:
        render_processing_sketch(
            "layer_map",
            {"layers": LAYER_SUMMARY},
            "Regional Layer Overview",
            "Assessment units, seismic coverage, public wells, and missing geometry stay visible before the full map.",
            height=360,
        )
        with st.expander("Full interactive regional map", expanded=True):
            render_regional_atlas()
    with tabs[1]:
        render_processing_sketch(
            "structure_stack",
            {"layers": STRUCTURE_LAYERS},
            "Structural Stack Preview",
            "A lightweight public-horizon sketch leads into the precise Plotly structural explorer.",
            height=360,
        )
        with st.expander("Full 3D structural explorer", expanded=True):
            render_structural_explorer()
    with tabs[2]:
        render_processing_sketch(
            "blocks",
            {
                "heading": "Source Boundary",
                "rows": [
                    {"label": "Public GIS", "status": "hosted"},
                    {"label": "Synthetic logs", "status": "demo only"},
                    {"label": "Approved logs", "status": "runtime only", "severity": "waiting"},
                    {"label": "Core data", "status": "runtime only", "severity": "waiting"},
                    {"label": "Sensitive outputs", "status": "do not publish", "severity": "waiting"},
                    {"label": "Figures", "status": "public/synthetic export"},
                ],
            },
            "Public / Runtime Boundary",
            "Source categories are separated before users reach file tables.",
            height=300,
        )
        with st.expander("Layer catalog and repository browser", expanded=True):
            render_data_library(files)


def render_interval_review(logs: pd.DataFrame, intervals: pd.DataFrame) -> None:
    ranked = sweet_spot_review_table(intervals)
    candidates = intervals[
        intervals["Synthetic sweet-spot review lane"].str.contains("candidate sweet-spot", na=False)
    ]
    cols = st.columns(4)
    cols[0].metric("Synthetic intervals", len(intervals))
    cols[1].metric("Review-lane candidates", len(candidates))
    cols[2].metric(
        "Hydrate-supportive",
        int(intervals["Phase-classification evidence"].str.startswith("hydrate").sum()),
    )
    cols[3].metric(
        "Good sand, no hydrate",
        int((intervals["Phase-classification evidence"] == "good sand, no hydrate").sum()),
    )
    interval_labels = {
        f'{row["Well alias"]} | {row["Top depth (m)"]}-{row["Base depth (m)"]} m': index
        for index, row in intervals.iterrows()
    }
    selected_label = st.selectbox("Synthetic interval", list(interval_labels), index=0)
    selected = intervals.loc[interval_labels[selected_label]]
    st.info(str(selected["Interpretation summary"]))
    evidence_values = {
        "Reservoir": selected["Reservoir-quality score"],
        "Hydrate evidence": selected["Hydrate-evidence score"],
        "Saturation proxy": selected["Hydrate-saturation proxy"],
        "Flow retention": selected["Permeability-retention proxy"],
        "QC": 0 if "borehole QC review" in selected["Uncertainty flags"] else 1,
        "Stability": 0 if selected["Stability admissibility"] == "outside / uncertain" else 1,
    }
    figure = go.Figure(
        go.Bar(
            x=list(evidence_values.values()),
            y=list(evidence_values),
            orientation="h",
            marker_color=["#167d8d", "#d9773d", "#4c78a8", "#59a14f", "#8f6bb3", "#76b7b2"],
            text=[f"{value:.2f}" for value in evidence_values.values()],
            textposition="auto",
        )
    )
    figure.update_layout(
        title="Selected Interval Evidence",
        xaxis={"range": [0, 1], "title": "Synthetic normalized support"},
        yaxis={"autorange": "reversed"},
        height=340,
        margin={"l": 0, "r": 0, "t": 45, "b": 0},
    )
    st.plotly_chart(figure, use_container_width=True)
    with st.expander("Ranked review queue and interval details"):
        st.dataframe(ranked, use_container_width=True, hide_index=True)
        input_rows = [
            ("GR", selected["GR median (API)"], "API", "Lithology and clean-sand screen"),
            ("Rt", selected["Rt median (ohm m)"], "ohm m", "Electrical hydrate evidence; non-unique"),
            ("RHOB", selected["RHOB median (g/cc)"], "g/cc", "Density and porosity constraint"),
            ("NMR porosity", selected["NMR porosity median"], "v/v", "Mobile-fluid response where available"),
            ("Vp/Vs", selected["Vp/Vs median"], "ratio", "Elastic phase context"),
            ("Hydrate saturation proxy", selected["Hydrate-saturation proxy"], "fraction", selected["Proxy source"]),
        ]
        st.dataframe(
            pd.DataFrame(input_rows, columns=["Variable", "Interval median", "Unit", "Decision role"]),
            use_container_width=True,
            hide_index=True,
        )


def render_public_ml_readiness() -> None:
    st.subheader("Public ML Readiness")
    features = cached_public_ml_feature_scaffold(str(PROJECT_ROOT))
    summary = cached_public_ml_feature_scaffold_summary(str(PROJECT_ROOT))
    dictionary = cached_public_ml_feature_dictionary(str(PROJECT_ROOT))

    if features.empty:
        st.info("The public ML feature scaffold has not been generated yet.")
        return

    if summary.empty:
        summary = public_ml_feature_scaffold_summary_frame(features)

    metric_lookup = dict(zip(summary["metric"], summary["value"], strict=False))
    cols = st.columns(4)
    cols[0].metric("Feature rows", f"{int(metric_lookup.get('Feature scaffold rows', 0)):,}")
    cols[1].metric(
        "Temperature matched",
        f"{int(metric_lookup.get('Rows with matched temperature profile', 0)):,}",
    )
    cols[2].metric(
        "Stability interval features",
        f"{int(metric_lookup.get('Rows with calculated stability interval feature', 0)):,}",
    )
    cols[3].metric(
        "Validated ML labels",
        f"{int(metric_lookup.get('Rows with validated hydrate occurrence labels', 0)):,}",
    )

    st.warning(
        "This is a public feature and coverage scaffold. It is not a hydrate-present label, "
        "hydrate-absent label, saturation target, producibility result, or sweet-spot ranking."
    )

    readiness_counts = (
        features["public_ml_feature_readiness"]
        .fillna("unknown")
        .value_counts()
        .rename_axis("readiness")
        .reset_index(name="rows")
    )
    figure = go.Figure(
        go.Bar(
            x=readiness_counts["rows"],
            y=readiness_counts["readiness"],
            orientation="h",
            marker={"color": "#2563eb"},
            hovertemplate="%{y}<br>Rows: %{x:,}<extra></extra>",
        )
    )
    figure.update_layout(
        title="Public Feature Readiness",
        xaxis_title="Rows",
        yaxis_title="",
        height=360,
        margin={"l": 20, "r": 20, "t": 50, "b": 20},
    )
    st.plotly_chart(figure, use_container_width=True)

    st.markdown("##### Feature Scaffold Preview")
    preview_columns = [
        "well_name",
        "public_ml_feature_readiness",
        "stability_result_status",
        "stability_confidence",
        "temperature_profile_matched",
        "stability_top_m",
        "stability_base_m",
        "stability_thickness_m",
        "blank_or_block_reason",
    ]
    st.dataframe(
        features[[column for column in preview_columns if column in features.columns]].head(500),
        use_container_width=True,
        hide_index=True,
    )

    with st.expander("Feature dictionary and label policy", expanded=True):
        st.dataframe(summary, use_container_width=True, hide_index=True)
        st.dataframe(dictionary, use_container_width=True, hide_index=True)

    cols = st.columns(3)
    cols[0].download_button(
        "Download ML feature scaffold CSV",
        csv_bytes(features),
        default_public_ml_feature_scaffold_path(PROJECT_ROOT).name,
        "text/csv",
        key="download_public_ml_feature_scaffold",
    )
    cols[1].download_button(
        "Download feature dictionary CSV",
        csv_bytes(dictionary),
        default_public_ml_feature_dictionary_path(PROJECT_ROOT).name,
        "text/csv",
        key="download_public_ml_feature_dictionary",
    )
    cols[2].download_button(
        "Download ML summary CSV",
        csv_bytes(summary),
        "public_ml_feature_scaffold_summary_2026-06-15.csv",
        "text/csv",
        key="download_public_ml_feature_summary",
    )


PARAMETER_TIER_COLORS = {
    "Stability context": "#2f80d0",
    "Reservoir quality": "#1f9f73",
    "Hydrate response": "#127c8b",
    "QC and review": "#d79a2b",
    "Targets and validation": "#c84242",
}


def build_parameter_evidence_bar_figure(registry: pd.DataFrame) -> go.Figure:
    if registry.empty:
        return go.Figure()

    plot_frame = registry.iloc[::-1].copy()
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=plot_frame["parameter_family"],
            x=[1.0] * len(plot_frame),
            orientation="h",
            marker_color="#eef5f7",
            marker_line_color="#bad3da",
            marker_line_width=1,
            hoverinfo="skip",
            showlegend=False,
            name="Normalized axis",
        )
    )
    for _, row in plot_frame.iterrows():
        tier = str(row["tier"])
        color = PARAMETER_TIER_COLORS.get(tier, "#526770")
        start = float(row["hydrate_window_norm_start"])
        end = float(row["hydrate_window_norm_end"])
        if end <= start:
            fig.add_trace(
                go.Scatter(
                    x=[0.5],
                    y=[row["parameter_family"]],
                    mode="markers+text",
                    marker={"size": 11, "color": color, "symbol": "x"},
                    text=["Y-only"],
                    textposition="middle right",
                    hovertext=row["public_guardrail"],
                    hoverinfo="text",
                    showlegend=False,
                )
            )
            continue

        fig.add_trace(
            go.Bar(
                y=[row["parameter_family"]],
                x=[end - start],
                base=[start],
                orientation="h",
                marker_color=color,
                marker_line_color=color,
                marker_line_width=1,
                text=[row["hydrate_direction_label"]],
                textposition="inside",
                insidetextanchor="middle",
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    + f"Tier: {tier}<br>"
                    + f"Hydrate-compatible: {escape(str(row['working_screening_envelope']))}<br>"
                    + f"Mimics/masks: {escape(str(row['false_positives_or_masks']))}<br>"
                    + f"Guardrail: {escape(str(row['public_guardrail']))}<extra></extra>"
                ),
                showlegend=False,
                name=str(row["hydrate_direction_label"]),
            )
        )
        fig.add_annotation(
            x=start,
            y=row["parameter_family"],
            text=str(row["low_axis_label"]),
            showarrow=False,
            xanchor="right",
            yshift=20,
            font={"size": 10, "color": "#526770"},
        )
        fig.add_annotation(
            x=end,
            y=row["parameter_family"],
            text=str(row["high_axis_label"]),
            showarrow=False,
            xanchor="left",
            yshift=20,
            font={"size": 10, "color": "#526770"},
        )

    fig.update_layout(
        title={"text": ""},
        height=max(470, 42 * len(plot_frame) + 160),
        margin={"l": 210, "r": 35, "t": 35, "b": 45},
        xaxis={
            "range": [0, 1],
            "tickmode": "array",
            "tickvals": [0, 0.5, 1],
            "ticktext": ["low / outside", "middle", "high / inside"],
            "title": "Normalized evidence axis for presentation only",
            "showgrid": False,
            "zeroline": False,
        },
        yaxis={"title": None, "automargin": True},
        barmode="overlay",
        bargap=0.35,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={"family": "Arial, sans-serif", "color": "#0b2330"},
    )
    return fig


def render_parameter_evidence_board() -> None:
    registry = cached_parameter_evidence_registry(str(PROJECT_ROOT))
    if registry.empty:
        st.info("The public parameter evidence registry has not been created yet.")
        return

    validation = validate_parameter_evidence_registry(registry)
    st.markdown("##### Parameter Evidence Board")
    st.caption(
        "Public-safe, source-backed screening logic for the slide parameter bars. "
        "Numeric envelopes are working ranges, not final DOE thresholds; directional rows stay directional."
    )
    st.dataframe(parameter_evidence_summary_frame(registry), use_container_width=True, hide_index=True)
    if not validation["valid"]:
        st.warning(f"Registry needs review: {validation}")

    st.plotly_chart(
        build_parameter_evidence_bar_figure(registry),
        use_container_width=True,
        key="schema_parameter_evidence_bar_figure",
    )

    display_columns = [
        "tier",
        "parameter_family",
        "hydrate_direction_label",
        "opposing_or_mimic_label",
        "working_screening_envelope",
        "ml_role",
        "public_guardrail",
    ]
    st.dataframe(registry[display_columns], use_container_width=True, hide_index=True)
    st.download_button(
        "Download parameter evidence registry CSV",
        csv_bytes(registry),
        PUBLIC_PARAMETER_EVIDENCE_REGISTRY.name,
        "text/csv",
        key="download_public_parameter_evidence_registry",
    )


def render_full_workflow_map_panel() -> None:
    st.markdown("##### Full Workflow Map")
    st.caption(
        "One public-safe map connecting the public scaffold, OSL workbench, stability context, "
        "approved-data schema controls, leakage barrier, future model heads, validation, and exports."
    )
    st.caption(
        "The canvas below is the Processing-style interactive overview; the static exports/downloads are detailed V5.3 diagrams generated by the reproducible Python builder."
    )
    detailed_workflow_payload = {
        "cards": [
            {
                "title": "1. Source schema",
                "badge": "public + OSL",
                "color": "#67d0df",
                "lines": [
                    "DNR wells, GGD223, G10015, USGS AUs",
                    "approved LAS/CSV/core/NMR later",
                    "original headers preserved first",
                ],
                "equations": [
                    "source header -> canonical alias",
                    "sheet/file -> provenance row",
                    "role -> feature / target / QC",
                ],
                "note": "About 3/71 approved-data datasets visible now.",
            },
            {
                "title": "2. Unit and QC gates",
                "badge": "fail closed",
                "color": "#25b99a",
                "lines": [
                    "depth, density, sonic, porosity, caliper",
                    "missingness and bad-hole flags",
                    "train-only transforms later",
                ],
                "equations": [
                    "depth_ft -> depth_m",
                    "RHOB kg/m3 -> g/cc",
                    "caliper -> washout flag",
                ],
                "note": "Unresolved units stay out of final modeling.",
            },
            {
                "title": "3. Stability equations",
                "badge": "context",
                "color": "#d8a24a",
                "lines": [
                    "hydrostatic absolute pressure",
                    "G10015 temperature model",
                    "methane 5 ppt phase lookup",
                ],
                "equations": [
                    "Pabs = 0.101 + rho_w*g*z",
                    "Tmodel = interp/extrap G10015",
                    "stable if Tmodel <= Teq(Pabs)",
                ],
                "note": "Admissibility only, not occurrence.",
            },
            {
                "title": "4. Physics features",
                "badge": "inputs",
                "color": "#8ea7ff",
                "lines": [
                    "reservoir, resistivity, sonic, NMR",
                    "elastic crossplots and saturation proxies",
                    "mimic risks remain visible",
                ],
                "equations": [
                    "Vsh=(GR-GRc)/(GRs-GRc)",
                    "phiD=(rho_ma-RHOB)/(rho_ma-rho_f)",
                    "Vp=304.8/DT; Vs=304.8/DTS",
                ],
                "note": "lambda-rho, mu-rho, Archie, NMR-density feed review.",
            },
            {
                "title": "5. Target-only rail",
                "badge": "labels",
                "color": "#d66a6a",
                "lines": [
                    "Sgh, S_h, Sh, NMR_SAT",
                    "Hydrate Saturation, Swr, S_wr",
                    "phase labels and manual calls",
                ],
                "equations": [
                    "NMR_SAT -> target/check only",
                    "Archie Sh -> baseline/check only",
                    "targets bypass feature matrix",
                ],
                "note": "Runtime validation now blocks leakage.",
            },
            {
                "title": "6. Model heads",
                "badge": "future",
                "color": "#8ea7ff",
                "lines": [
                    "whole-well train/validation/test split",
                    "physics/simple baseline first",
                    "tree or ANN after controls pass",
                ],
                "equations": [
                    "features -> occurrence P(hydrate)",
                    "features -> saturation Sh",
                    "preprocessing fit on train wells",
                ],
                "note": "No final model metrics until approved labels exist.",
            },
            {
                "title": "7. Validation and exports",
                "badge": "review",
                "color": "#25b99a",
                "lines": [
                    "calibration and residual plots",
                    "QC, mimic, reason, uncertainty flags",
                    "public-safe summaries only",
                ],
                "equations": [
                    "compare vs Sgh/NMR/core targets",
                    "review by well/depth/QC/lithology",
                    "export maps/tables after review",
                ],
                "note": "Outputs are predictions, not proof.",
            },
        ],
        "sources": [
            {"label": "SIR 2008-5175 P-T", "color": "#d8a24a"},
            {"label": "Chong 2022 ML", "color": "#8ea7ff"},
            {"label": "Lee/Collett/Haines logs", "color": "#67d0df"},
            {"label": "Target registry", "color": "#d66a6a"},
            {"label": "ML source ledger", "color": "#25b99a"},
        ],
    }
    render_processing_sketch(
        "detailed_ml_workflow",
        detailed_workflow_payload,
        "Equation-Driven Workflow Map",
        "Equations and source gates are wired into the ML path before any occurrence or saturation model is trained.",
        height=760,
    )

    equation_gate_groups = [
        "Lithology / reservoir quality",
        "Density porosity",
        "Sonic velocity",
        "Elastic moduli",
        "Lambda-rho / mu-rho",
        "Pressure-temperature admissibility",
        "Overburden / effective stress",
        "Saturation proxy",
        "NMR-density saturation proxy",
        "Permeability / producibility risk",
    ]
    equation_gates = pd.DataFrame(EQUATION_LIBRARY)
    equation_gates = equation_gates[
        equation_gates["Equation group"].isin(equation_gate_groups)
    ][
        [
            "Equation group",
            "Equation",
            "Inputs",
            "Feature produced",
            "Classification use",
            "Source anchor",
        ]
    ]
    with st.expander("Equation gates behind the workflow map", expanded=True):
        st.dataframe(equation_gates, use_container_width=True, hide_index=True)
        st.caption(
            "These equations produce candidate features, context fields, baselines, or validation checks. "
            "They do not create hydrate proof, saturation labels, or public model metrics by themselves."
        )

    with st.expander("Static export preview and downloads", expanded=False):
        workflow_preview_path = (
            FULL_WORKFLOW_EXPANDED_FLOWCHART
            if FULL_WORKFLOW_EXPANDED_FLOWCHART.exists()
            else FULL_WORKFLOW_FLOWCHART
        )
        if workflow_preview_path.exists():
            st.markdown(
                (
                    f'<img src="{png_data_uri(workflow_preview_path)}" '
                    'alt="Full ML workflow map" '
                    'style="width: 100%; height: auto; border: 1px solid #c7d2da; border-radius: 8px;" />'
                ),
                unsafe_allow_html=True,
            )
            st.caption(
                f"{project_relative_or_absolute(workflow_preview_path)} | "
                "workflow/status guide only, not hydrate proof or trained-model output"
            )
        else:
            st.info(f"Workflow map not found yet: {project_relative_or_absolute(workflow_preview_path)}")

    with st.expander("ML architecture detail: features, QC, neural network, and outputs", expanded=True):
        if FULL_WORKFLOW_ML_NETWORK.exists():
            st.markdown(
                (
                    f'<img src="{png_data_uri(FULL_WORKFLOW_ML_NETWORK)}" '
                    'alt="ML model architecture detail" '
                    'style="width: 100%; height: auto; border: 1px solid #c7d2da; border-radius: 8px;" />'
                ),
                unsafe_allow_html=True,
            )
            st.caption(
                f"{project_relative_or_absolute(FULL_WORKFLOW_ML_NETWORK)} | "
                "architecture guide only; no trained model, labels, or performance metrics yet"
            )
        else:
            st.info(f"ML architecture detail not found yet: {project_relative_or_absolute(FULL_WORKFLOW_ML_NETWORK)}")

    cols = st.columns(4)
    cols[0].metric("Public scaffold wells", "8,084")
    cols[1].metric("Calculated admissibility intervals", "22")
    cols[2].metric("Approved-data subset", "~3 / 71")
    cols[3].metric("Model outputs", "Future")

    st.info(
        "Use the V5.3 deck and companion as the mentor-facing roadmap: stability is a context/admissibility branch, "
        "target fields bypass the feature matrix, and occurrence plus saturation outputs wait for "
        "approved labels and whole-well validation."
    )

    download_specs = [
        (
            "Download expanded workflow PNG",
            FULL_WORKFLOW_EXPANDED_FLOWCHART
            if FULL_WORKFLOW_EXPANDED_FLOWCHART.exists()
            else FULL_WORKFLOW_FLOWCHART,
            "image/png",
            "download_full_workflow_png",
        ),
        (
            "Download ML architecture PNG",
            FULL_WORKFLOW_ML_NETWORK,
            "image/png",
            "download_ml_network_png",
        ),
        (
            "Download slide contact sheet",
            FULL_WORKFLOW_CONTACT_SHEET,
            "image/png",
            "download_full_workflow_contact_sheet",
        ),
        (
            "Download workflow PPTX",
            FULL_WORKFLOW_DECK,
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "download_full_workflow_pptx",
        ),
        (
            "Download workflow DOCX",
            FULL_WORKFLOW_WORD,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "download_full_workflow_docx",
        ),
    ]
    download_columns = st.columns(5)
    for column, (label, path, mime, key) in zip(download_columns, download_specs):
        if path.exists():
            column.download_button(
                label,
                path.read_bytes(),
                path.name,
                mime,
                key=key,
            )
        else:
            column.button(label, disabled=True, key=f"{key}_missing")


def render_presentation_export_image_card(
    title: str,
    path: Path,
    caption: str,
    key: str,
) -> None:
    st.markdown(f"##### {title}")
    if path.exists():
        st.markdown(
            (
                f'<img src="{png_data_uri(path)}" '
                f'alt="{escape(title)}" '
                'style="width: 100%; height: auto; border: 1px solid #c7d2da; border-radius: 8px;" />'
            ),
            unsafe_allow_html=True,
        )
        st.caption(f"{caption} | {project_relative_or_absolute(path)}")
        st.download_button(
            f"Download {title}",
            path.read_bytes(),
            path.name,
            "image/png",
            key=f"download_export_{key}",
        )
    else:
        st.info(f"Export image not found yet: {project_relative_or_absolute(path)}")


def render_presentation_exports() -> None:
    st.subheader("Presentation Exports")
    st.caption(
        "Slide-ready, public-safe panels for the current V5.3 deck and Word companion. "
        "These previews reuse current website captures, generated V5.3 panels, and source-backed visuals; "
        "they do not include approved rows, trained-model outputs, occurrence predictions, or saturation predictions."
    )

    inventory = cached_source_visual_inventory(str(PROJECT_ROOT))
    validation = validate_source_visual_inventory(inventory, PROJECT_ROOT)

    cols = st.columns(4)
    cols[0].metric("Tracked visuals", f"{len(inventory):,}")
    cols[1].metric("Missing local files", f"{len(validation['missing_local_paths']):,}")
    cols[2].metric("Uncited/AI-looking flags", f"{len(validation['uncited_or_ai_looking_rows']):,}")
    cols[3].metric("QA status", "pass" if validation["valid"] else "review")

    if validation["valid"]:
        st.success(
            "Current source-visual inventory passes required-column, local-path, uncited/AI-looking, and QA-status checks."
        )
    else:
        st.warning(f"Source-visual inventory needs review: {validation}")

    export_specs = [
        (
            "North Slope Map",
            V5_3_WEBSITE_CAPTURE_DIR / "02_explore_regional_map.png",
            "Current website regional-map capture for slide context",
            "north_slope_map",
        ),
        (
            "Parameter Ranges",
            FULL_WORKFLOW_ASSET_DIR / "slide_03_parameter_ranges_v5_3.png",
            "Slide-scale bars for parameter direction and working ranges",
            "parameter_ranges",
        ),
        (
            "Parameter Evidence",
            FULL_WORKFLOW_ASSET_DIR / "slide_05_parameter_evidence_visuals_v5_3.png",
            "Normalized evidence visual for hydrate-compatible log behavior",
            "parameter_evidence",
        ),
        (
            "Stability Schematic",
            FULL_WORKFLOW_ASSET_DIR / "slide_06_stability_physics_v5_3.png",
            "Pressure-temperature admissibility method; not hydrate proof",
            "stability_schematic",
        ),
        (
            "Simplified Workflow",
            FULL_WORKFLOW_ASSET_DIR / "slide_04_simplified_workflow_v5_3.png",
            "Non-ML audience explanation of the public/OSL workflow",
            "simplified_workflow",
        ),
        (
            "Validation Outputs",
            FULL_WORKFLOW_ASSET_DIR / "slide_08_validation_uncertainty_outputs_v5_3.png",
            "Planned validation and uncertainty outputs with no fake results",
            "validation_outputs",
        ),
        (
            "Expanded Architecture",
            FULL_WORKFLOW_EXPANDED_FLOWCHART,
            "Detailed project architecture appendix plate",
            "expanded_architecture",
        ),
        (
            "ML Runtime Detail",
            FULL_WORKFLOW_ML_NETWORK,
            "Detailed ML runtime, target rail, validation, and output plate",
            "ml_runtime_detail",
        ),
    ]

    st.markdown("##### Slide-ready panels")
    for index in range(0, len(export_specs), 2):
        columns = st.columns(2)
        for column, spec in zip(columns, export_specs[index : index + 2]):
            with column:
                render_presentation_export_image_card(*spec)

    with st.expander("Live parameter evidence bars", expanded=False):
        registry = cached_parameter_evidence_registry(str(PROJECT_ROOT))
        if registry.empty:
            st.info("The public parameter evidence registry has not been created yet.")
        else:
            live_parameter_figure = build_parameter_evidence_bar_figure(registry)
            st.plotly_chart(
                live_parameter_figure,
                use_container_width=True,
                key="presentation_parameter_evidence_bar_figure",
            )
            st.download_button(
                "Download live parameter bars HTML",
                figure_html_bytes(live_parameter_figure),
                "public_parameter_evidence_bars_2026-06-16.html",
                "text/html",
                key="download_live_parameter_bars_html",
            )

    st.markdown("##### Visual provenance QA")
    st.dataframe(
        source_visual_inventory_summary_frame(inventory, PROJECT_ROOT),
        use_container_width=True,
        hide_index=True,
    )
    display_columns = [
        "visual_id",
        "slide_or_site_use",
        "source_status",
        "qa_status",
        "replacement_needed",
        "guardrail",
    ]
    if not inventory.empty:
        st.dataframe(inventory[display_columns], use_container_width=True, hide_index=True)
        st.download_button(
            "Download source visual inventory CSV",
            csv_bytes(inventory),
            SOURCE_VISUAL_INVENTORY.name,
            "text/csv",
            key="download_source_visual_inventory",
        )


def render_schema_coverage_architecture() -> None:
    st.subheader("Schema Coverage & Architecture")
    matrix = cached_approved_schema_coverage_matrix(str(PROJECT_ROOT))
    field_roles = cached_approved_data_field_role_table(str(PROJECT_ROOT))

    if matrix.empty:
        st.info("The approved-data schema coverage matrix has not been generated yet.")
        return

    render_full_workflow_map_panel()

    target_like = matrix["role"].isin(["target_only", "calibration_reference"])
    required_like = matrix["required_for_model"].fillna("").str.contains(
        "required|target",
        case=False,
        regex=True,
    )
    available_like = matrix["available_in_current_subset"].fillna("").str.startswith("yes")

    cols = st.columns(4)
    cols[0].metric("Available datasets", "~3 / 71")
    cols[1].metric("Schema rows", f"{len(matrix):,}")
    cols[2].metric("Target/calibration rows", f"{int(target_like.sum()):,}")
    cols[3].metric("Model training", "Not started")

    st.warning(
        "This is schema-level coverage only. It preserves original headers and "
        "roles, separates target-only saturation fields, and does not include "
        "approved well-log rows, trained models, predictions, or performance metrics."
    )

    render_parameter_evidence_board()

    st.markdown("##### Latest V5.3 deck and companion roles")
    latest_roles = [
        {
            "Artifact": "V5.3 slide deck",
            "Role": "Mentor-readable presentation with source-backed hydrate/North Slope context, parameter-range visuals, simplified workflow, stability context, beginner ML architecture, validation outputs, and intact appendix architecture plates.",
            "Local file": project_relative_or_absolute(FULL_WORKFLOW_DECK),
            "Drive link": FULL_WORKFLOW_DRIVE_SLIDES_URL or "pending Drive import",
        },
        {
            "Artifact": "V5.3 Word companion",
            "Role": "Research/source-backed explanation of the same workflow, including project purpose, public/OSL boundary, parameter evidence, stability method, ML workflow, website outputs, and mentor decisions.",
            "Local file": project_relative_or_absolute(FULL_WORKFLOW_WORD),
            "Drive link": FULL_WORKFLOW_DRIVE_DOC_URL or "pending Drive import",
        },
    ]
    st.dataframe(pd.DataFrame(latest_roles), use_container_width=True, hide_index=True)
    if FULL_WORKFLOW_DRIVE_SLIDES_URL or FULL_WORKFLOW_DRIVE_DOC_URL:
        link_parts = []
        if FULL_WORKFLOW_DRIVE_SLIDES_URL:
            link_parts.append(f"[Open V5.3 Google Slides]({FULL_WORKFLOW_DRIVE_SLIDES_URL})")
        if FULL_WORKFLOW_DRIVE_DOC_URL:
            link_parts.append(f"[Open V5.3 Google Doc]({FULL_WORKFLOW_DRIVE_DOC_URL})")
        st.markdown(" | ".join(link_parts))

    st.markdown("##### Current public counts")
    current_counts = pd.DataFrame(
        [
            {
                "Item": "Public scaffold wells",
                "Count": "8,084",
                "Use": "public regional scaffold, not approved ML rows",
            },
            {
                "Item": "GGD223 permafrost controls",
                "Count": "43",
                "Use": "public permafrost context",
            },
            {
                "Item": "G10015 temperature profiles",
                "Count": "184",
                "Use": "public temperature-profile context",
            },
            {
                "Item": "USGS hydrate assessment units",
                "Count": "3",
                "Use": "regional context only",
            },
            {
                "Item": "Temperature-profile matches",
                "Count": "483",
                "Use": "future context/mask/confidence candidates",
            },
            {
                "Item": "Methane 5 ppt admissibility intervals",
                "Count": "22",
                "Use": "stability context only, not hydrate proof",
            },
            {
                "Item": "No-stable-interval rows",
                "Count": "8",
                "Use": "screen outcome under current gates",
            },
            {
                "Item": "Blocked stability-screen rows",
                "Count": "8,054",
                "Use": "blocked by current source/calculation gates",
            },
            {
                "Item": "Approved datasets visible for schema design",
                "Count": "~3 / 71",
                "Use": "headers/schema only, not public row data",
            },
        ]
    )
    st.dataframe(current_counts, use_container_width=True, hide_index=True)

    st.markdown("##### Readiness contract")
    readiness_contract = pd.DataFrame(
        [
            {
                "Area": "Public now",
                "Allowed display": "diagrams, counts, schemas, caveats, blocked reasons, synthetic examples",
                "Not allowed": "approved rows, trained metrics, occurrence probabilities, saturation predictions",
            },
            {
                "Area": "OSL / approved runtime later",
                "Allowed display": "approved LAS/CSV/core/NMR rows, target mapping, fitting, validation, reviewed outputs",
                "Not allowed": "public release before boundary review",
            },
            {
                "Area": "Stability",
                "Allowed display": "methane 5 ppt admissibility context, masks, confidence, caveats",
                "Not allowed": "hydrate proof, occurrence label, saturation target, sweet-spot rank",
            },
            {
                "Area": "X_allowed",
                "Allowed display": "measured logs, valid derived features, QC fields, approved context",
                "Not allowed": "Sgh, S_h, Sh, NMR_SAT, Hydrate Saturation, Swr, phase labels",
            },
            {
                "Area": "Y-only labels",
                "Allowed display": "target authority, calibration, validation overlays after approval",
                "Not allowed": "predictor columns or feature selection inputs",
            },
        ]
    )
    st.dataframe(readiness_contract, use_container_width=True, hide_index=True)

    st.markdown("##### Blocked reasons and mentor decisions")
    blocked_decisions = pd.DataFrame(
        [
            {
                "Blocked item": "Official phase curve policy",
                "Current handling": "methane 5 ppt baseline only",
                "Decision needed": "baseline only or labeled scenarios",
            },
            {
                "Blocked item": "Occurrence and saturation labels",
                "Current handling": "target-only headers visible, zero public target rows",
                "Decision needed": "official target authority and unit convention",
            },
            {
                "Blocked item": "Validation split",
                "Current handling": "whole-well/compartment/geographic options documented",
                "Decision needed": "final split policy before preprocessing",
            },
            {
                "Blocked item": "Missing G10015 coverage",
                "Current handling": "rows remain blocked unless policy changes",
                "Decision needed": "blocked, proxy tier, or scenario-only gradient",
            },
            {
                "Blocked item": "Public website outputs",
                "Current handling": "public-safe diagrams, counts, schemas, caveats, readiness",
                "Decision needed": "which views are acceptable before validation",
            },
        ]
    )
    st.dataframe(blocked_decisions, use_container_width=True, hide_index=True)

    st.markdown("##### Intake Validator Contract")
    st.caption(
        "Header-level validator only. It checks column roles, leakage, target "
        "authority, unit policy, split readiness, and blocked reasons without "
        "loading approved row values."
    )
    required_column_families = pd.DataFrame(
        [
            {
                "Required family": "Depth basis",
                "Accepted examples": "DEPTH, DEPT, Depth_ft, True Depth, depth_m",
                "Blocked reason": "missing_required_field:depth_basis",
            },
            {
                "Required family": "Reservoir or lithology curve",
                "Accepted examples": "GR, RHOB/Rho_b, density or porosity family",
                "Blocked reason": "missing_required_field:lithology_or_reservoir_curve",
            },
            {
                "Required family": "Hydrate-response curve family",
                "Accepted examples": "Rt/RES, NMRPHI, Vp, Vs, impedance",
                "Blocked reason": "missing_required_field:hydrate_response_curve_family",
            },
            {
                "Required family": "Target registry",
                "Accepted examples": "Y-only occurrence and saturation labels with authority metadata",
                "Blocked reason": "no_approved_target_authority_for_training",
            },
            {
                "Required family": "Split group",
                "Accepted examples": "whole-well, compartment, or geographic/geologic holdout",
                "Blocked reason": "whole_well_split_required_before_train_only_preprocessing",
            },
        ]
    )
    st.dataframe(required_column_families, use_container_width=True, hide_index=True)
    st.dataframe(intake_validator_contract_frame(), use_container_width=True, hide_index=True)

    st.markdown("##### Variable Fingerprint And Intake Validator")
    st.caption(
        "Every header gets a public-safe fingerprint before it can enter the "
        "approved runtime: original name, unit, normalized name, role, feature "
        "permission, leakage risk, and unresolved mentor question."
    )
    st.markdown(
        """
- **X_allowed rule:** measured logs, derived features, QC fields, and approved context only.
- **Y-only target rule:** `Sgh`, `S_h`, `Sh`, `NMR_SAT`, Hydrate Saturation, `Swr`, phase labels, and occurrence labels never enter `X_allowed`.
- **Caliper coverage first:** use caliper washout QC only when `caliper`, `CAL1`, or differential caliper coverage exists; otherwise carry a missing-QC flag.
- **Missing-log adapter:** optional and validation-required for missing `Vp` or `RHOB`; default is blocked until mentor approval.
- **Occurrence/saturation tasks:** occurrence classification and saturation regression are linked but separate tasks.
"""
    )
    fingerprint_fields = pd.DataFrame(
        [
            {
                "Fingerprint field": "original_header",
                "Purpose": "Preserve the exact source header or mnemonic.",
            },
            {
                "Fingerprint field": "unit",
                "Purpose": "Keep units visible beside the source header and normalized name.",
            },
            {
                "Fingerprint field": "normalized",
                "Purpose": "Records whether a canonical project name exists.",
            },
            {
                "Fingerprint field": "role",
                "Purpose": "measured input, derived feature, QC, context, target, calibration, or unresolved.",
            },
            {
                "Fingerprint field": "allowed_in_feature_matrix",
                "Purpose": "True only for approved predictor, derived, QC, or context fields.",
            },
            {
                "Fingerprint field": "leakage_risk",
                "Purpose": "Flags target-only, calibration, unresolved, or depth-as-predictor risk.",
            },
            {
                "Fingerprint field": "unresolved_mentor_question",
                "Purpose": "Keeps blue/open questions visible before training.",
            },
        ]
    )
    st.dataframe(fingerprint_fields, use_container_width=True, hide_index=True)

    if not field_roles.empty:
        fingerprints = build_variable_fingerprints(field_roles)
        field_role_counts = (
            fingerprints["role"]
            .fillna("unresolved")
            .value_counts()
            .rename_axis("role")
            .reset_index(name="field_role_rows")
        )
        st.dataframe(field_role_counts, use_container_width=True, hide_index=True)
        st.dataframe(
            fingerprints[
                [
                    "original_header",
                    "unit",
                    "normalized_name",
                    "role",
                    "allowed_in_feature_matrix",
                    "leakage_risk",
                    "unresolved_mentor_question",
                ]
            ].head(30),
            use_container_width=True,
            hide_index=True,
        )

    validator_decisions = pd.DataFrame(
        [
            {
                "Decision box": "X_allowed rule",
                "Current rule": "Measured logs, derived features, QC fields, and approved context may enter X_allowed after fingerprint and unit checks.",
                "Open point": "Depth stays the alignment/context axis unless mentor approves predictor use.",
            },
            {
                "Decision box": "Y-only target rule",
                "Current rule": "Sgh, S_h, Sh, NMR_SAT, Hydrate Saturation, Swr, phase labels, and occurrence labels never enter X_allowed.",
                "Open point": "Mentor must choose official target authority and unit convention.",
            },
            {
                "Decision box": "Caliper coverage first",
                "Current rule": "Use caliper/CAL1/differential caliper for washout QC when coverage exists.",
                "Open point": "If coverage is not enough, create a missing-QC flag instead of filtering rows.",
            },
            {
                "Decision box": "Missing-log adapter",
                "Current rule": "Default is blocked unless explicitly approved.",
                "Open point": "Vp/RHOB adapter models are optional and validation-required for North Slope use.",
            },
            {
                "Decision box": "Occurrence evidence",
                "Current rule": "Occurrence is target/validation evidence from core, pressure-core, NMR/core-derived saturation, validated log interpretation, or documented seismic indicators.",
                "Open point": "Stability does not measure occurrence.",
            },
            {
                "Decision box": "Saturation task",
                "Current rule": "Saturation regression is linked to but separate from occurrence classification.",
                "Open point": "Choose authoritative saturation field and fraction/percent convention.",
            },
        ]
    )
    st.dataframe(validator_decisions, use_container_width=True, hide_index=True)

    template_specs = [
        (
            "Approved-data intake template",
            APPROVED_DATA_INTAKE_TEMPLATE,
            "source registry, well-depth index, X_allowed, and Y target tables",
            "download_approved_data_intake_template",
        ),
        (
            "Intake validation schema",
            APPROVED_DATA_INTAKE_VALIDATION_SCHEMA,
            "validator checks, pass rules, blocked reasons, and guardrails",
            "download_approved_data_intake_validation_schema",
        ),
        (
            "First model output schema",
            FIRST_MODEL_OUTPUT_SCHEMA,
            "future occurrence, saturation, uncertainty, reason flag, and release fields",
            "download_first_model_output_schema",
        ),
        (
            "Source column registry template",
            APPROVED_DATA_SOURCE_COLUMN_REGISTRY_TEMPLATE,
            "header-level source registry with role, unit, dtype, and caveat columns",
            "download_approved_data_source_column_registry_template",
        ),
        (
            "Well-depth index template",
            APPROVED_DATA_WELL_DEPTH_INDEX_TEMPLATE,
            "runtime well/depth alignment, split group, and release-status columns",
            "download_approved_data_well_depth_index_template",
        ),
        (
            "X_allowed candidate template",
            APPROVED_DATA_X_ALLOWED_CANDIDATE_TEMPLATE,
            "predictor, derived-feature, QC, and context placeholders with no Y-only columns",
            "download_approved_data_x_allowed_candidate_template",
        ),
        (
            "Y target registry template",
            APPROVED_DATA_Y_TARGET_REGISTRY_TEMPLATE,
            "occurrence and saturation target authority, source evidence, and caveat columns",
            "download_approved_data_y_target_registry_template",
        ),
        (
            "First model output template",
            FIRST_MODEL_OUTPUT_SCHEMA_TEMPLATE,
            "future occurrence, saturation, uncertainty, reason flag, and release fields",
            "download_first_model_output_schema_template",
        ),
        (
            "Variable fingerprint template",
            VARIABLE_FINGERPRINT_TEMPLATE,
            "per-variable role, unit, leakage, feature-permission, and mentor-question fields",
            "download_variable_fingerprint_template",
        ),
    ]
    st.markdown("##### Public-safe runtime templates")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Template": label,
                    "Purpose": purpose,
                    "Path": project_relative_or_absolute(path),
                    "Status": "available" if path.exists() else "missing",
                }
                for label, path, purpose, _ in template_specs
            ]
        ),
        use_container_width=True,
        hide_index=True,
    )
    for offset in range(0, len(template_specs), 3):
        for column, (label, path, _purpose, key) in zip(st.columns(3), template_specs[offset : offset + 3]):
            if path.exists():
                column.download_button(
                    f"Download {label}",
                    path.read_bytes(),
                    path.name,
                    "text/csv",
                    key=key,
                )
            else:
                column.button(f"Download {label}", disabled=True, key=f"{key}_missing")

    st.markdown("##### Header Audit / OSL Handoff")
    st.caption(
        "The CLI runner audits headers only. It can be used in OSL against "
        "approved workbook/LAS/CSV/core/NMR sources without printing or writing "
        "row values."
    )
    st.code(
        "python 01_pipeline/validate_approved_data_headers.py "
        "--source-csv path/to/approved_or_runtime_file.csv --header-only "
        "--source-label osl_header_audit_public_safe "
        "--output-prefix osl_header_audit_2026-06-15",
        language="bash",
    )

    handoff_contract = pd.DataFrame(
        [
            {
                "Area": "CLI exists",
                "Public-safe use": "`01_pipeline/validate_approved_data_headers.py` reads inline headers, header-list CSVs, or CSV headers with `nrows=0`.",
                "Must stay out": "approved row values and private workbook rows",
            },
            {
                "Area": "Validates",
                "Public-safe use": "recognized/unknown headers, roles, X_allowed leakage, missing required fields, blocked reasons, mentor questions",
                "Must stay out": "trained model metrics, occurrence probabilities, saturation predictions",
            },
            {
                "Area": "Safe to copy back",
                "Public-safe use": "CSV/JSON/Markdown readiness summaries, header lists, units, row counts, depth ranges, coverage counts",
                "Must stay out": "restricted identifiers unless anonymized and approved",
            },
            {
                "Area": "OSL-only",
                "Public-safe use": "keep approved LAS/CSV/core/NMR rows and populated runtime configs in authorized storage",
                "Must stay out": "raw target values and row-level predictions",
            },
        ]
    )
    st.dataframe(handoff_contract, use_container_width=True, hide_index=True)

    demo_summary = {}
    if DEMO_HEADER_AUDIT_JSON.exists():
        demo_summary = json.loads(DEMO_HEADER_AUDIT_JSON.read_text(encoding="utf-8"))
    if demo_summary:
        st.markdown(
            f"Demo report summary: source `{demo_summary.get('source_label', '')}`, "
            f"recognized headers `{demo_summary.get('recognized_header_count', '')}`, "
            f"ready_for_schema_design `{demo_summary.get('ready_for_schema_design', False)}`, "
            f"ready_for_training `{demo_summary.get('ready_for_training', False)}`."
        )
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Demo field": "source_label",
                        "Value": demo_summary.get("source_label", ""),
                    },
                    {
                        "Demo field": "recognized_header_count",
                        "Value": demo_summary.get("recognized_header_count", ""),
                    },
                    {
                        "Demo field": "ready_for_schema_design",
                        "Value": demo_summary.get("ready_for_schema_design", False),
                    },
                    {
                        "Demo field": "ready_for_training",
                        "Value": demo_summary.get("ready_for_training", False),
                    },
                    {
                        "Demo field": "blocked_reasons",
                        "Value": "; ".join(demo_summary.get("blocked_reasons", [])),
                    },
                ]
            ),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Demo header audit report has not been generated yet.")

    audit_downloads = [
        ("Demo CSV report", DEMO_HEADER_AUDIT_CSV, "text/csv", "download_demo_header_audit_csv"),
        ("Demo JSON report", DEMO_HEADER_AUDIT_JSON, "application/json", "download_demo_header_audit_json"),
        (
            "Readiness report Markdown",
            APPROVED_DATA_INTAKE_READINESS_REPORT,
            "text/markdown",
            "download_approved_data_intake_readiness_report",
        ),
        (
            "OSL header-audit runbook",
            OSL_HEADER_AUDIT_RUNBOOK,
            "text/markdown",
            "download_osl_header_audit_runbook",
        ),
    ]
    for offset in range(0, len(audit_downloads), 2):
        for column, (label, path, mime, key) in zip(st.columns(2), audit_downloads[offset : offset + 2]):
            if path.exists():
                column.download_button(
                    f"Download {label}",
                    path.read_bytes(),
                    path.name,
                    mime,
                    key=key,
                )
            else:
                column.button(f"Download {label}", disabled=True, key=f"{key}_missing")

    role_counts = (
        matrix["role"]
        .fillna("unresolved")
        .value_counts()
        .rename_axis("role")
        .reset_index(name="headers")
    )
    role_figure = go.Figure(
        go.Bar(
            x=role_counts["headers"],
            y=role_counts["role"],
            orientation="h",
            marker={"color": "#0f766e"},
            hovertemplate="%{y}<br>Headers: %{x}<extra></extra>",
        )
    )
    role_figure.update_layout(
        title="Header Roles In The Public-Safe Schema Matrix",
        xaxis_title="Header rows",
        yaxis_title="",
        height=340,
        margin={"l": 20, "r": 20, "t": 50, "b": 20},
    )
    st.plotly_chart(role_figure, use_container_width=True)

    architecture = pd.DataFrame(
        [
            {
                "Stage": "Available subset and screenshots",
                "Feature path": "Use visible headers to design schema and architecture.",
                "Target path": "No approved target rows are exposed.",
            },
            {
                "Stage": "Schema preservation",
                "Feature path": "Keep original sheet/file names and headers, then add canonical aliases as metadata.",
                "Target path": "Keep original saturation and phase-label headers visible.",
            },
            {
                "Stage": "Role classification",
                "Feature path": "Measured inputs, derived features, QC fields, context features, and unresolved fields are separated.",
                "Target path": "`Sgh`, `S_h`, `Sh`, `NMR_SAT`, hydrate-saturation fields, `Swr`, `S_wr`, and phase labels are target/calibration only.",
            },
            {
                "Stage": "Unit and QC layer",
                "Feature path": "Normalize depth, density, velocity/slowness, porosity, resistivity, and caliper status.",
                "Target path": "Confirm target units as fraction or percent before labels are used.",
            },
            {
                "Stage": "Leakage barrier",
                "Feature path": "Build feature matrix only from approved measured, derived, QC, and optional context fields.",
                "Target path": "Bypass feature matrix and go only to training labels or validation overlays.",
            },
            {
                "Stage": "Model and validation",
                "Feature path": "Use whole-well split, baselines, tree/boosting, and ANN/Keras only after approved coverage expands.",
                "Target path": "Validate saturation regression and later occurrence classification by held-out wells.",
            },
        ]
    )
    st.markdown("##### Architecture path")
    st.dataframe(architecture, use_container_width=True, hide_index=True)

    st.markdown("##### Schema matrix preview")
    preview_columns = [
        "sheet_or_dataset_name",
        "original_header",
        "canonical_alias",
        "role",
        "feature_family",
        "required_for_model",
        "available_in_current_subset",
        "leakage_risk",
        "unresolved_question",
    ]
    st.dataframe(
        matrix[[column for column in preview_columns if column in matrix.columns]],
        use_container_width=True,
        hide_index=True,
    )

    if not field_roles.empty:
        st.markdown("##### Approved-data field role table")
        role_preview_columns = [
            "original_header",
            "normalized_name",
            "source_dataset",
            "role",
            "unit",
            "expected_dtype",
            "required_for_model",
            "public_safe_to_show",
            "caveats",
        ]
        st.dataframe(
            field_roles[[column for column in role_preview_columns if column in field_roles.columns]],
            use_container_width=True,
            hide_index=True,
        )

    with st.expander("Coverage checks", expanded=False):
        st.dataframe(role_counts, use_container_width=True, hide_index=True)
        st.write(
            f"Required or target-like schema rows currently visible: {int((required_like & available_like).sum()):,}. "
            "This supports architecture design, not final training or metrics."
        )

    st.download_button(
        "Download schema coverage matrix CSV",
        csv_bytes(matrix),
        default_approved_schema_coverage_matrix_path(PROJECT_ROOT).name,
        "text/csv",
        key="download_approved_schema_coverage_matrix",
    )
    if not field_roles.empty:
        st.download_button(
            "Download approved-data field role table CSV",
            csv_bytes(field_roles),
            APPROVED_DATA_FIELD_ROLE_TABLE.name,
            "text/csv",
            key="download_approved_data_field_role_table",
        )


def render_public_ml_target_registry() -> None:
    st.subheader("Target Registry & Leakage Guardrail")
    registry = cached_public_ml_target_registry(str(PROJECT_ROOT))
    guardrails = cached_public_ml_leakage_guardrails(str(PROJECT_ROOT))

    if registry.empty:
        registry = public_ml_target_registry_frame()
    if guardrails.empty:
        guardrails = public_ml_leakage_guardrails_frame()

    target_headers = registry["original_header"].tolist()
    cols = st.columns(4)
    cols[0].metric("Target headers", f"{len(target_headers):,}")
    cols[1].metric(
        "Hydrate saturation targets",
        f"{int(registry['canonical_target_family'].eq('hydrate_saturation').sum()):,}",
    )
    cols[2].metric("Leakage rules", f"{len(guardrails):,}")
    cols[3].metric("Public target rows", "0")

    st.warning(
        "The saturation family is already treated as target-only: "
        "`Sgh`, `S_h`, `Sh`, `NMR_SAT`, `Hydrate Saturation`, `Swr`, and `S_wr` "
        "must stay out of the input feature matrix unless a workbook formula proves a non-leaking role."
    )

    st.markdown("##### Target-only header registry")
    st.dataframe(registry, use_container_width=True, hide_index=True)

    st.markdown("##### Leakage guardrails")
    st.dataframe(guardrails, use_container_width=True, hide_index=True)

    cols = st.columns(2)
    cols[0].download_button(
        "Download target registry CSV",
        csv_bytes(registry),
        default_public_ml_target_registry_path(PROJECT_ROOT).name,
        "text/csv",
        key="download_public_ml_target_registry",
    )
    cols[1].download_button(
        "Download leakage guardrails CSV",
        csv_bytes(guardrails),
        default_public_ml_leakage_guardrails_path(PROJECT_ROOT).name,
        "text/csv",
        key="download_public_ml_leakage_guardrails",
    )


def render_analyze_hydrates() -> None:
    st.markdown('<div class="atlas-kicker">Synthetic decision workspace</div>', unsafe_allow_html=True)
    st.title("Analyze Hydrates")
    st.write(
        "Public stability features show current coverage; synthetic logs show the future workflow shape. "
        "Approved well and core data stay outside the public site."
    )
    logs = load_runtime_data()
    intervals = screen_intervals(logs)
    core = synthetic_core_placeholders()
    calibrated_core = nearby_log_calibration(logs, core)
    render_processing_sketch(
        "well_evidence",
        {"tracks": SYNTHETIC_TRACKS, "domains": EVIDENCE_DOMAINS},
        "Well-Log Evidence Board",
        "Depth tracks, highlighted intervals, evidence domains, and QC are visible before the tables.",
        height=430,
    )
    st.warning(
        f"{SYNTHETIC_LABEL}. {HEADER_DERIVED_SYNTHETIC_NOTE} Do not upload approved logs, core data, identifiers, or derived sensitive outputs."
    )
    tabs = st.tabs(
        [
            "Public ML Readiness",
            "Schema Coverage & Architecture",
            "Target Registry & Leakage",
            "Interval Review",
            "Runtime Readiness",
            "Presentation Exports",
            "Methods & Evidence",
        ]
    )
    with tabs[0]:
        render_public_ml_readiness()
    with tabs[1]:
        render_schema_coverage_architecture()
    with tabs[2]:
        render_public_ml_target_registry()
    with tabs[3]:
        render_interval_review(logs, intervals)
    with tabs[4]:
        col1, col2 = st.columns(2)
        with col1:
            render_processing_sketch(
                "target_boundary",
                {"items": TARGET_BOUNDARY},
                "Target Leakage Guardrail",
                "Measured inputs, derived features, and target fields stay separated.",
                height=280,
            )
        with col2:
            render_processing_sketch(
                "cohort_split",
                {"split": COHORT_SPLIT},
                "Whole-Well Split Plan",
                "Validation is by well, not neighboring depth rows.",
                height=280,
            )
        render_runtime_readiness(logs)
    with tabs[5]:
        render_presentation_exports()
    with tabs[6]:
        render_ml_visual_architecture()
        render_source_anchors()
        with st.expander("Header and track blueprint", expanded=True):
            render_header_blueprint()
        with st.expander("Sweet-spot evidence model"):
            render_sweet_spot_evidence_model(intervals)
        with st.expander("Equation-to-decision map"):
            render_equation_decision_map()
        with st.expander("Range guide and public science anchors"):
            render_range_guide()
        with st.expander("Interval, core, and presentation exports"):
            render_interval_screen(intervals)
            render_core_calibration(calibrated_core)
            render_presentation_outputs(logs, intervals, calibrated_core)


def main() -> None:
    st.set_page_config(
        page_title="North Slope Gas Hydrate Atlas",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="auto",
    )
    apply_styles()
    files = project_files()
    page = render_sidebar()

    if page == "Overview":
        render_overview(files)
    elif page == "Explore North Slope":
        render_explore_north_slope(files)
    elif page == "Analyze Hydrates":
        render_analyze_hydrates()
    elif page == "Project Plan":
        render_project_plan()
    else:
        render_framework()

    st.divider()
    st.caption(
        "North Slope Gas Hydrate Regional Atlas | Public-source foundation | "
        "Run inside OpenScienceLab"
    )


if __name__ == "__main__":
    main()
