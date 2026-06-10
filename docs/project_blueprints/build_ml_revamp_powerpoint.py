from __future__ import annotations

import csv
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[2]
BLUEPRINT_DIR = ROOT / "docs" / "project_blueprints"
BASE_PPTX = BLUEPRINT_DIR / "Drive_base_CURRENT_June_10_North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview_Slides.pptx"
OUT_PPTX = BLUEPRINT_DIR / "North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview.pptx"
PARAMETER_CSV = BLUEPRINT_DIR / "ml_parameter_effect_tree.csv"


NAVY = RGBColor(9, 34, 49)
DEEP = RGBColor(4, 21, 33)
TEAL = RGBColor(22, 125, 141)
ICE = RGBColor(103, 208, 223)
GREEN = RGBColor(37, 185, 154)
AMBER = RGBColor(216, 162, 74)
RED = RGBColor(207, 83, 83)
INK = RGBColor(18, 52, 71)
MUTED = RGBColor(86, 105, 115)
LIGHT = RGBColor(244, 248, 249)
WHITE = RGBColor(255, 255, 255)
SAND = RGBColor(246, 239, 226)
PURPLE = RGBColor(142, 167, 255)


def clear_deck(prs: Presentation) -> None:
    slide_ids = prs.slides._sldIdLst  # noqa: SLF001 - python-pptx has no public delete API.
    for slide_id in list(slide_ids):
        r_id = slide_id.rId
        prs.part.drop_rel(r_id)
        slide_ids.remove(slide_id)


def blank_slide(prs: Presentation):
    return prs.slides.add_slide(prs.slide_layouts[6])


def fill_background(slide, color: RGBColor = WHITE) -> None:
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = color


def set_shape_fill(shape, color: RGBColor, transparency: int = 0) -> None:
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.fill.transparency = transparency


def set_line(shape, color: RGBColor, width: float = 1.0, transparency: int = 0) -> None:
    shape.line.color.rgb = color
    shape.line.width = Pt(width)
    shape.line.transparency = transparency


def textbox(slide, x, y, w, h, text, size=14, color=INK, bold=False, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.margin_left = Inches(0.05)
    tf.margin_right = Inches(0.05)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    tf.vertical_anchor = MSO_ANCHOR.TOP
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = "Aptos"
    return box


def title(slide, heading, subtitle=None, dark=False) -> None:
    color = WHITE if dark else INK
    sub_color = RGBColor(190, 220, 226) if dark else MUTED
    textbox(slide, 0.55, 0.28, 12.1, 0.48, heading, 25, color, True)
    if subtitle:
        textbox(slide, 0.58, 0.78, 11.7, 0.32, subtitle, 10.5, sub_color)


def footer(slide, text, dark=False) -> None:
    color = RGBColor(170, 202, 208) if dark else MUTED
    textbox(slide, 0.55, 7.08, 12.2, 0.22, text, 7.2, color)


def rect(slide, x, y, w, h, fill, line=TEAL, radius=True, transparency=0):
    shape_type = MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE if radius else MSO_AUTO_SHAPE_TYPE.RECTANGLE
    shape = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
    set_shape_fill(shape, fill, transparency)
    set_line(shape, line, 1.1)
    return shape


def label_box(slide, x, y, w, h, head, body, fill=LIGHT, line=TEAL, head_color=INK, body_color=MUTED, dark=False):
    rect(slide, x, y, w, h, fill, line)
    textbox(slide, x + 0.12, y + 0.1, w - 0.24, 0.22, head, 10.5, head_color if not dark else WHITE, True)
    textbox(slide, x + 0.12, y + 0.38, w - 0.24, h - 0.44, body, 8.4, body_color if not dark else RGBColor(205, 230, 234))


def connector(slide, x1, y1, x2, y2, color=TEAL, width=1.5, arrow=True):
    conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    conn.line.color.rgb = color
    conn.line.width = Pt(width)
    if arrow:
        conn.line.end_arrowhead = True
    return conn


def pill(slide, x, y, w, h, text, fill, color=WHITE, size=9.5, line=None):
    shape = rect(slide, x, y, w, h, fill, line or fill)
    shape.text_frame.clear()
    p = shape.text_frame.paragraphs[0]
    p.text = text
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(size)
    p.font.bold = True
    p.font.color.rgb = color
    return shape


def read_parameters() -> list[dict[str, str]]:
    with PARAMETER_CSV.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def slide_title(prs, params):
    slide = blank_slide(prs)
    fill_background(slide, WHITE)
    title(slide, "Gas Hydrate Occurrence and Saturation Prediction", "North Slope well-log and core evidence with physics-constrained ML")
    label_box(slide, 0.65, 1.45, 3.4, 1.35, "Rohan Nanda", "Lead Geologist\nM.S. Geosciences, University of Texas at Dallas", SAND, AMBER)
    label_box(slide, 0.65, 3.1, 3.4, 1.15, "About me", "I like drawing, swimming, and running.", LIGHT, TEAL)
    rect(slide, 4.55, 1.32, 7.9, 3.9, LIGHT, TEAL)
    textbox(slide, 4.85, 1.65, 7.2, 0.45, "Revamp focus", 18, INK, True)
    textbox(
        slide,
        4.85,
        2.18,
        7.0,
        1.4,
        "Explain each well-log parameter visually, show what can mask hydrate signals, then map the ML architecture from inputs to predicted sweet spots.",
        17,
        INK,
        True,
    )
    pill(slide, 4.85, 4.05, 2.0, 0.45, "parameters", TEAL)
    pill(slide, 7.1, 4.05, 2.0, 0.45, "masking", AMBER)
    pill(slide, 9.35, 4.05, 2.0, 0.45, "ML branches", PURPLE)
    textbox(slide, 0.7, 5.75, 11.5, 0.45, "Public-safe deck: no classified well data, no real approved rows, no trained models.", 14, RED, True, PP_ALIGN.CENTER)
    footer(slide, "Source base: Drive deck exported 2026-06-10; Chong et al. 2022; Excel header map; local equation documents.")


def slide_problem(prs):
    slide = blank_slide(prs)
    fill_background(slide, WHITE)
    title(slide, "What This Deck Must Explain", "The audience needs to understand why a parameter matters before seeing an ML architecture.")
    stages = [
        ("Parameter", "What property does it measure?"),
        ("Signal line", "Which side is hydrate-supportive?"),
        ("Masking effect", "What else can create the same response?"),
        ("ML decision", "How is it used without target leakage?"),
    ]
    x = 0.75
    for i, (head, body) in enumerate(stages):
        label_box(slide, x + i * 3.05, 1.55, 2.55, 1.2, head, body, LIGHT, [TEAL, GREEN, AMBER, PURPLE][i])
        if i < len(stages) - 1:
            connector(slide, x + i * 3.05 + 2.58, 2.15, x + (i + 1) * 3.05 - 0.12, 2.15, TEAL)
    textbox(slide, 1.05, 3.55, 11.15, 0.45, "The deck should be visual first: icons, signal bars, branch logic, and architecture maps instead of lists of variables.", 17, INK, True, PP_ALIGN.CENTER)
    label_box(slide, 1.1, 4.55, 3.35, 1.25, "Depth", "Retain as depth/alignment context; do not normalize like other values.", SAND, AMBER)
    label_box(slide, 4.95, 4.55, 3.35, 1.25, "Other curves", "Normalize or standardize values for privacy and ML training.", LIGHT, TEAL)
    label_box(slide, 8.8, 4.55, 3.35, 1.25, "Targets", "Use for labels/calibration only; never as predictors.", LIGHT, RED)
    footer(slide, "Planning weights and graphics are conceptual until approved well data and targets are available.")


def icon(slide, x, y, label, color):
    c = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL, Inches(x), Inches(y), Inches(0.38), Inches(0.38))
    set_shape_fill(c, color)
    set_line(c, color)
    textbox(slide, x - 0.04, y + 0.08, 0.46, 0.18, label, 7.2, WHITE, True, PP_ALIGN.CENTER)


def slide_parameter_grid(prs, params):
    slide = blank_slide(prs)
    fill_background(slide, WHITE)
    title(slide, "Parameter Signal Grid", "Each curve has a hydrate-supportive direction, but every strong signal has masks.")
    textbox(slide, 0.72, 1.05, 2.1, 0.22, "ambiguous / masked", 8.3, RED, True)
    textbox(slide, 10.15, 1.05, 2.1, 0.22, "hydrate-supportive", 8.3, TEAL, True, PP_ALIGN.RIGHT)

    coords = []
    for col in range(2):
        for row in range(5):
            coords.append((0.65 + col * 6.15, 1.38 + row * 1.02))

    abbrev = {
        "Deep resistivity": "Rt",
        "NMR porosity / NMR saturation support": "NMR",
        "Vp / compressional velocity": "Vp",
        "Vs / shear velocity": "Vs",
        "Density and density porosity": "rho",
        "Gamma ray / lithology": "GR",
        "Caliper / differential caliper": "Cal",
        "Vp/Vs ratio and acoustic impedance": "AI",
        "Core porosity / permeability / lithology": "Core",
        "Depth / pressure-temperature / overburden": "Depth",
    }

    for (x, y), row in zip(coords, params):
        weight = float(row["planned_importance_percent"])
        rect(slide, x, y, 5.72, 0.82, LIGHT, RGBColor(214, 225, 229))
        icon(slide, x + 0.12, y + 0.18, abbrev.get(row["parameter"], "?")[:5], TEAL)
        textbox(slide, x + 0.6, y + 0.11, 2.75, 0.2, row["parameter"], 8.2, INK, True)
        textbox(slide, x + 3.55, y + 0.11, 0.55, 0.2, f"{weight:.0f}%", 8.5, AMBER, True, PP_ALIGN.RIGHT)
        # Signal line: left gray/red ambiguity, right teal hydrate-supportive side.
        connector(slide, x + 0.65, y + 0.48, x + 4.95, y + 0.48, RGBColor(177, 184, 189), 1.4, False)
        connector(slide, x + 2.7, y + 0.48, x + 4.95, y + 0.48, TEAL, 3.0, False)
        pill(slide, x + 4.93, y + 0.38, 0.24, 0.2, "", TEAL, line=TEAL)
        mask = row["major_masks_or_false_positives"].split(";")[0].strip()
        textbox(slide, x + 0.6, y + 0.58, 4.9, 0.16, f"mask: {mask}", 6.5, MUTED)
    footer(slide, "Weights are planning priors for visual emphasis, not trained feature importance.")


def slide_parameter_trees(prs, params):
    slide = blank_slide(prs)
    fill_background(slide, WHITE)
    title(slide, "Parameter Effect Trees", "Read each parameter as evidence plus masking conditions, not as a one-step hydrate label.")
    selected = [
        params[0],
        params[1],
        params[2],
        params[4],
    ]
    x_positions = [0.55, 3.78, 7.01, 10.24]
    colors = [TEAL, GREEN, PURPLE, AMBER]
    for x, row, color in zip(x_positions, selected, colors):
        rect(slide, x, 1.32, 2.55, 4.95, LIGHT, color)
        textbox(slide, x + 0.14, 1.5, 2.2, 0.4, row["parameter"], 11, INK, True, PP_ALIGN.CENTER)
        pill(slide, x + 0.6, 2.12, 1.35, 0.32, "measure", color)
        textbox(slide, x + 0.22, 2.56, 2.12, 0.42, row["primary_hydrate_effect"], 7.4, INK)
        connector(slide, x + 1.28, 3.08, x + 1.28, 3.55, color)
        pill(slide, x + 0.52, 3.58, 1.5, 0.32, "can mask", RED)
        masks = "; ".join(row["major_masks_or_false_positives"].split(";")[:3])
        textbox(slide, x + 0.22, 4.0, 2.1, 0.48, masks, 7.2, MUTED)
        connector(slide, x + 1.28, 4.58, x + 1.28, 5.0, color)
        pill(slide, x + 0.42, 5.03, 1.7, 0.32, "ML use", NAVY)
        textbox(slide, x + 0.22, 5.42, 2.12, 0.46, row["model_role"], 7.0, INK)
    footer(slide, "The detailed matrix is stored in docs/project_blueprints/ml_parameter_effect_tree.csv.")


def slide_architecture_overview(prs):
    slide = blank_slide(prs)
    fill_background(slide, DEEP)
    title(slide, "ML Architecture Overview", "Hybrid architecture: MLOps flow plus hydrate-specific evidence logic.", dark=True)
    boxes = [
        ("Input parameters", "GR, Rt, RHOB, NMR,\nVp, Vs, caliper, core", ICE),
        ("Normalize + QC", "Depth retained;\nother values standardized", GREEN),
        ("Feature equations", "Vsh, porosity, Vp/Vs,\nAI, lambda-rho, mu-rho", AMBER),
        ("Model branches", "phase classification +\nSgh regression", PURPLE),
        ("Predicted sweet spots", "rank, uncertainty,\nmasking explanation", WHITE),
    ]
    y = 2.05
    for i, (head, body, color) in enumerate(boxes):
        x = 0.58 + i * 2.48
        rect(slide, x, y, 2.05, 1.36, RGBColor(13, 57, 70), color)
        textbox(slide, x + 0.15, y + 0.18, 1.75, 0.25, head, 10.2, color, True, PP_ALIGN.CENTER)
        textbox(slide, x + 0.18, y + 0.58, 1.68, 0.5, body, 8.0, WHITE, False, PP_ALIGN.CENTER)
        if i < len(boxes) - 1:
            connector(slide, x + 2.08, y + 0.68, x + 2.38, y + 0.68, color)
    # Supporting stores like the reference image.
    label_box(slide, 1.05, 4.45, 2.45, 0.72, "Source library", "public papers + equation docs", RGBColor(10, 72, 78), TEAL, dark=True)
    label_box(slide, 3.9, 4.45, 2.45, 0.72, "Feature store", "derived physics features", RGBColor(10, 72, 78), GREEN, dark=True)
    label_box(slide, 6.75, 4.45, 2.45, 0.72, "Target registry", "labels locked away", RGBColor(10, 72, 78), RED, dark=True)
    label_box(slide, 9.6, 4.45, 2.45, 0.72, "Monitoring", "held-out wells + drift", RGBColor(10, 72, 78), PURPLE, dark=True)
    connector(slide, 2.28, 4.44, 2.28, 3.55, TEAL)
    connector(slide, 5.12, 4.44, 5.12, 3.55, GREEN)
    connector(slide, 7.98, 4.44, 7.98, 3.55, RED)
    connector(slide, 10.82, 4.44, 10.82, 3.55, PURPLE)
    footer(slide, "Architecture adapted from the Drive reference image, but constrained to the North Slope well-log workflow.", dark=True)


def slide_detailed_architecture(prs):
    slide = blank_slide(prs)
    fill_background(slide, DEEP)
    title(slide, "Detailed ML Decision Map", "The model receives physical features; labels and final rankings stay outside the feature table.", dark=True)
    # Left input families
    families = [
        ("Lithology", "GR + core lithology"),
        ("Electrical", "Rt / deep resistivity"),
        ("Porosity", "RHOB, DPHI, NMR"),
        ("Elastic", "Vp, Vs, Vp/Vs"),
        ("QC", "caliper, missingness"),
    ]
    for i, (head, body) in enumerate(families):
        label_box(slide, 0.55, 1.25 + i * 0.75, 2.05, 0.52, head, body, RGBColor(12, 61, 74), ICE, dark=True)
        connector(slide, 2.6, 1.51 + i * 0.75, 3.22, 3.0, ICE, 0.9)
    label_box(slide, 3.25, 2.32, 2.35, 1.35, "QC + normalization", "Depth stays depth.\nOther values are standardized.\nBad-hole rows are flagged.", RGBColor(12, 61, 74), GREEN, dark=True)
    label_box(slide, 6.0, 2.32, 2.25, 1.35, "Feature equations", "Vsh, porosity,\nAI, Vp/Vs,\nlambda-rho, mu-rho", RGBColor(12, 61, 74), AMBER, dark=True)
    connector(slide, 5.62, 3.0, 5.98, 3.0, GREEN)
    # Leakage barrier
    connector(slide, 8.55, 1.2, 8.55, 5.85, RED, 2.5, False)
    textbox(slide, 8.68, 1.2, 1.1, 0.55, "target leakage barrier", 8.0, RED, True)
    label_box(slide, 8.78, 4.8, 2.0, 0.85, "Locked targets", "Sgh, S_h, NMR_SAT,\nphase labels, final ranks", RGBColor(75, 28, 33), RED, dark=True)
    # Branches
    connector(slide, 8.28, 2.75, 9.25, 2.15, PURPLE)
    connector(slide, 8.28, 3.25, 9.25, 3.8, PURPLE)
    label_box(slide, 9.3, 1.55, 2.95, 0.92, "Classification branch", "hydrate / gas / water / non-reservoir + uncertainty", RGBColor(12, 61, 74), PURPLE, dark=True)
    label_box(slide, 9.3, 3.25, 2.95, 0.92, "Saturation regression", "continuous Sgh from calibrated known-well targets", RGBColor(12, 61, 74), PURPLE, dark=True)
    label_box(slide, 9.3, 5.05, 2.95, 0.62, "Output", "predicted sweet spots with reasons", RGBColor(12, 61, 74), GREEN, dark=True)
    connector(slide, 10.78, 2.48, 10.78, 5.02, PURPLE)
    connector(slide, 10.78, 4.17, 10.78, 5.02, PURPLE)
    footer(slide, "Parallel branches follow the project plan: classification and saturation regression share features but keep separate outputs.", dark=True)


def slide_leakage_normalization(prs):
    slide = blank_slide(prs)
    fill_background(slide, WHITE)
    title(slide, "Normalization and Leakage Rules", "Privacy and model validity both depend on keeping roles explicit.")
    label_box(slide, 0.75, 1.35, 3.3, 1.45, "Depth", "Keep as depth/alignment context. Do not hide its meaning by treating it like a generic normalized curve.", SAND, AMBER)
    label_box(slide, 4.95, 1.35, 3.3, 1.45, "Input curves", "Normalize or standardize RHOB, Rt, GR, NMR, Vp, Vs, caliper, and derived features after train-well fitting.", LIGHT, TEAL)
    label_box(slide, 9.15, 1.35, 3.3, 1.45, "Targets", "Sgh, S_h, NMR_SAT, phase labels, and final rankings supervise or evaluate only.", LIGHT, RED)
    connector(slide, 2.4, 3.1, 2.4, 4.1, AMBER)
    connector(slide, 6.6, 3.1, 6.6, 4.1, TEAL)
    connector(slide, 10.8, 3.1, 10.8, 4.1, RED)
    pill(slide, 1.1, 4.25, 2.6, 0.55, "alignment axis", AMBER, INK)
    pill(slide, 5.05, 4.25, 3.1, 0.55, "training-well transforms", TEAL)
    pill(slide, 9.55, 4.25, 2.55, 0.55, "locked labels", RED)
    textbox(slide, 1.0, 5.58, 11.2, 0.55, "Any fitted preprocessing, imputation, feature selection, or learned weighting must be fit on training wells only, then applied unchanged to validation, test, and prediction wells.", 15, INK, True, PP_ALIGN.CENTER)
    footer(slide, "Rule source: Excel header map, runtime validation plan, and user revamp instruction.")


def slide_parallel_models(prs):
    slide = blank_slide(prs)
    fill_background(slide, WHITE)
    title(slide, "Classification and Saturation Are Parallel", "The ML papers motivate shared features, but the outputs answer different questions.")
    label_box(slide, 0.75, 1.55, 2.7, 1.0, "Shared feature table", "Normalized logs + equations + QC flags", LIGHT, TEAL)
    connector(slide, 3.45, 2.05, 4.6, 1.55, TEAL)
    connector(slide, 3.45, 2.05, 4.6, 3.15, TEAL)
    label_box(slide, 4.65, 1.0, 3.2, 1.15, "Phase classification", "Predict hydrate, gas, water, non-reservoir, or uncertain.", LIGHT, PURPLE)
    label_box(slide, 4.65, 2.72, 3.2, 1.15, "Saturation regression", "Predict continuous hydrate saturation where calibrated targets exist.", LIGHT, PURPLE)
    connector(slide, 7.85, 1.58, 9.05, 2.35, PURPLE)
    connector(slide, 7.85, 3.3, 9.05, 2.75, PURPLE)
    label_box(slide, 9.1, 1.85, 3.2, 1.35, "Sweet-spot review", "Combine occurrence confidence, saturation, reservoir quality, flow risk, and uncertainty.", SAND, AMBER)
    textbox(slide, 0.95, 5.1, 11.45, 0.4, "A high saturation estimate is not automatically the best sweet spot; producibility and uncertainty remain separate.", 16, RED, True, PP_ALIGN.CENTER)
    footer(slide, "Chong et al. supports ML saturation experiments; this project also needs separate phase classification and review ranking.")


def slide_masking_failure_modes(prs):
    slide = blank_slide(prs)
    fill_background(slide, WHITE)
    title(slide, "Masking Conditions the Model Must Respect", "These are not edge cases; they are why the model must be physics-constrained.")
    modes = [
        ("Gas", "high Rt + low Vp can mimic hydrate unless Vs/NMR/core disagree", RED),
        ("Ice", "stiff and resistive, but permafrost context changes interpretation", ICE),
        ("Shale", "GR, bound water, and clay effects distort porosity and NMR", AMBER),
        ("Carbonate/cement", "high velocity and resistivity without hydrate occupancy", PURPLE),
        ("Overburden", "compaction raises density and velocities across baselines", GREEN),
        ("Bad hole", "washout can corrupt density, neutron, sonic, and resistivity", RED),
    ]
    for i, (head, body, color) in enumerate(modes):
        x = 0.75 + (i % 3) * 4.15
        y = 1.45 + (i // 3) * 2.0
        label_box(slide, x, y, 3.45, 1.35, head, body, LIGHT, color)
    textbox(slide, 0.85, 5.95, 11.3, 0.42, "Each parameter tree should show both the hydrate-supportive direction and the major false-positive path.", 15, INK, True, PP_ALIGN.CENTER)
    footer(slide, "Primary controls: Lee and Collett 2011; Haines et al. 2022; Zyrianova et al. 2024; local equation/range docs.")


def slide_overburden(prs):
    slide = blank_slide(prs)
    fill_background(slide, WHITE)
    title(slide, "Overburden Map Role", "Future OpenScienceLab shapefiles should explain changing baselines, not classify hydrate by themselves.")
    # Stylized North Slope section
    rect(slide, 0.85, 1.25, 7.3, 4.6, SAND, AMBER, radius=False)
    for i, (label, color) in enumerate([
        ("surface / permafrost", ICE),
        ("Sagwon and younger load", RGBColor(180, 210, 165)),
        ("Brookian reservoir section", AMBER),
        ("deeper structural context", RGBColor(170, 145, 190)),
    ]):
        y = 1.42 + i * 0.86
        shape = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, Inches(1.12), Inches(y), Inches(6.75), Inches(0.62))
        set_shape_fill(shape, color, 10)
        set_line(shape, color)
        textbox(slide, 1.28, y + 0.18, 6.4, 0.18, label, 9.0, INK, True)
    connector(slide, 4.45, 1.25, 4.45, 5.75, RED, 2.0, False)
    textbox(slide, 4.55, 5.35, 2.1, 0.25, "burial pressure shifts density / velocity baselines", 8.4, RED, True)
    label_box(slide, 8.65, 1.35, 3.55, 0.92, "Why it matters", "Density, Vp, Vs, and impedance all change with compaction and stress.", LIGHT, TEAL)
    label_box(slide, 8.65, 2.65, 3.55, 0.92, "What shapefiles add", "Structural position, stratigraphic load, and map-based context.", LIGHT, GREEN)
    label_box(slide, 8.65, 3.95, 3.55, 0.92, "What it cannot do", "It cannot replace logs, core, or calibrated labels.", LIGHT, RED)
    footer(slide, "Overburden visual is a placeholder until the OpenScienceLab shapefiles are gathered.")


def slide_sweet_spots(prs):
    slide = blank_slide(prs)
    fill_background(slide, WHITE)
    title(slide, "Predicted Sweet Spots Are Review Outputs", "The final output should explain why an interval is worth review, not just assign a score.")
    parts = [
        ("Occurrence", "Is hydrate likely present?", TEAL),
        ("Saturation", "How much pore space may be occupied?", PURPLE),
        ("Reservoir", "Is there connected sand and pore volume?", GREEN),
        ("Flow risk", "Could permeability remain useful?", AMBER),
        ("Uncertainty", "What masks or missing data remain?", RED),
    ]
    for i, (head, body, color) in enumerate(parts):
        x = 0.75 + i * 2.45
        label_box(slide, x, 1.45, 2.05, 1.28, head, body, LIGHT, color)
        if i < len(parts) - 1:
            connector(slide, x + 2.06, 2.08, x + 2.35, 2.08, color)
    rect(slide, 2.15, 4.0, 9.0, 1.35, SAND, AMBER)
    textbox(slide, 2.42, 4.25, 8.45, 0.36, "Predicted sweet spot = multi-log hydrate evidence + reservoir quality + calibrated saturation + manageable uncertainty", 15, INK, True, PP_ALIGN.CENTER)
    textbox(slide, 2.42, 4.78, 8.45, 0.22, "Public deck shows the architecture; approved runtime later supplies real metrics and figures.", 10.5, MUTED, False, PP_ALIGN.CENTER)
    footer(slide, "Sweet-spot rankings remain review outputs and cannot be used as model inputs.")


def slide_conclusion(prs):
    slide = blank_slide(prs)
    fill_background(slide, WHITE)
    title(slide, "Final Project Message", "A defensible ML workflow is built from physical evidence, not isolated curve responses.")
    label_box(slide, 0.9, 1.45, 3.3, 1.25, "Scientific value", "Separates occurrence, saturation, reservoir quality, uncertainty, and producibility.", LIGHT, TEAL)
    label_box(slide, 5.0, 1.45, 3.3, 1.25, "ML value", "Uses physics-backed features, parallel model branches, and whole-well validation.", LIGHT, PURPLE)
    label_box(slide, 9.1, 1.45, 3.3, 1.25, "Energy value", "Supports future North Slope gas-hydrate resource characterization.", LIGHT, AMBER)
    textbox(slide, 1.05, 3.6, 11.2, 0.75, "Next work: gather approved workbook/formulas and overburden shapefiles, then replace conceptual graphics with verified runtime figures.", 19, INK, True, PP_ALIGN.CENTER)
    footer(slide, "Sources: USGS/DOE/NETL; Chong et al. 2022; Lee and Collett 2011; Haines et al. 2022; project header/equation docs.")


def build() -> None:
    params = read_parameters()
    if BASE_PPTX.exists():
        prs = Presentation(str(BASE_PPTX))
        clear_deck(prs)
    else:
        prs = Presentation()
        clear_deck(prs)
    prs.slide_width = Inches(13.333333)
    prs.slide_height = Inches(7.5)

    slide_title(prs, params)
    slide_problem(prs)
    slide_parameter_grid(prs, params)
    slide_parameter_trees(prs, params)
    slide_architecture_overview(prs)
    slide_detailed_architecture(prs)
    slide_leakage_normalization(prs)
    slide_parallel_models(prs)
    slide_masking_failure_modes(prs)
    slide_overburden(prs)
    slide_sweet_spots(prs)
    slide_conclusion(prs)

    prs.save(OUT_PPTX)
    print(OUT_PPTX)


if __name__ == "__main__":
    build()
