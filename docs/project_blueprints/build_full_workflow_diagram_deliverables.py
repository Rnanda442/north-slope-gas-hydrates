from __future__ import annotations

import csv
import hashlib
import math
from io import BytesIO
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.shared import Inches, Pt
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation


ROOT = Path(__file__).resolve().parents[2]
BLUEPRINT_DIR = ROOT / "docs" / "project_blueprints"
ASSET_DIR = BLUEPRINT_DIR / "presentation_assets" / "full_workflow_diagram_2026_06_15"
SOURCE_DECK = BLUEPRINT_DIR / "CURRENT_GMAIL_VISUAL_REVISION_9_SLIDE_North_Slope_Gas_Hydrate_Slides_2026-06-11.pptx"
OUT_DECK = BLUEPRINT_DIR / "FULL_WORKFLOW_ML_DIAGRAM_9_SLIDE_North_Slope_Gas_Hydrate_Slides_2026-06-15.pptx"
OUT_DOCX = BLUEPRINT_DIR / "North_Slope_Gas_Hydrate_Full_ML_Workflow_Diagram_2026-06-15.docx"
OUT_CONTACT_SHEET = ASSET_DIR / "full_workflow_deck_contact_sheet.png"
PUBLIC_PRODUCTS = ROOT / "data" / "public_stability_products"

W, H = 1600, 900
EXPANDED_W, EXPANDED_H = 3000, 1688
NAVY = (11, 35, 48)
DEEP = (5, 19, 27)
TEAL = (18, 124, 139)
ICE = (82, 185, 214)
ICE_LIGHT = (223, 244, 248)
GREEN = (37, 154, 113)
GREEN_LIGHT = (224, 246, 236)
AMBER = (219, 159, 52)
AMBER_LIGHT = (250, 239, 211)
RED = (200, 62, 65)
RED_LIGHT = (252, 229, 230)
BLUE = (55, 133, 203)
BLUE_LIGHT = (228, 241, 253)
PURPLE = (111, 105, 190)
PURPLE_LIGHT = (236, 234, 250)
MUTED = (82, 103, 112)
LIGHT = (244, 249, 250)
LINE = (181, 210, 217)
WHITE = (255, 255, 255)
LOCKED_SLIDE_HASHES: dict[int, str] = {}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "arialbd.ttf" if bold else "arial.ttf",
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "calibrib.ttf" if bold else "calibri.ttf",
    ]
    roots = [Path("C:/Windows/Fonts"), Path("/usr/share/fonts/truetype/dejavu")]
    for name in candidates:
        for root in roots:
            path = root / name
            if path.exists():
                return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, size: int, width: int, bold: bool = False) -> list[str]:
    f = font(size, bold)
    lines: list[str] = []
    for raw in text.splitlines():
        if not raw:
            lines.append("")
            continue
        current = ""
        for word in raw.split():
            test = f"{current} {word}".strip()
            if draw.textlength(test, font=f) <= width or not current:
                current = test
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    value: str,
    size: int,
    fill: tuple[int, int, int] = NAVY,
    bold: bool = False,
    width: int | None = None,
    align: str = "left",
    gap: int = 5,
) -> int:
    f = font(size, bold)
    if width is None:
        draw.text(xy, value, font=f, fill=fill)
        return xy[1] + size + gap
    y = xy[1]
    for line in wrap_lines(draw, value, size, width, bold):
        if align == "center":
            x = xy[0] + width // 2 - int(draw.textlength(line, font=f) // 2)
        elif align == "right":
            x = xy[0] + width - int(draw.textlength(line, font=f))
        else:
            x = xy[0]
        draw.text((x, y), line, font=f, fill=fill)
        y += size + gap
    return y


def card(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    fill: tuple[int, int, int] = WHITE,
    outline: tuple[int, int, int] = LINE,
    radius: int = 18,
    width: int = 2,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    fill: tuple[int, int, int] = TEAL,
    width: int = 4,
    label: str | None = None,
    label_offset: tuple[int, int] = (0, 0),
) -> None:
    draw.line((start, end), fill=fill, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    length = 15
    points = [
        end,
        (int(end[0] - length * math.cos(angle - 0.45)), int(end[1] - length * math.sin(angle - 0.45))),
        (int(end[0] - length * math.cos(angle + 0.45)), int(end[1] - length * math.sin(angle + 0.45))),
    ]
    draw.polygon(points, fill=fill)
    if label:
        mx = (start[0] + end[0]) // 2 + label_offset[0]
        my = (start[1] + end[1]) // 2 + label_offset[1]
        f = font(12, True)
        pad = 5
        w = int(draw.textlength(label, font=f)) + pad * 2
        card(draw, (mx - w // 2, my - 14, mx + w // 2, my + 12), fill=WHITE, outline=fill, radius=9, width=1)
        draw.text((mx - w // 2 + pad, my - 10), label, font=f, fill=fill)


def pill(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    label: str,
    fill: tuple[int, int, int],
    text_fill: tuple[int, int, int] = NAVY,
) -> None:
    card(draw, box, fill=fill, outline=fill, radius=14, width=1)
    f = font(13, True)
    x = box[0] + (box[2] - box[0]) // 2 - int(draw.textlength(label, font=f) // 2)
    y = box[1] + (box[3] - box[1] - 13) // 2 - 2
    draw.text((x, y), label, font=f, fill=text_fill)


def node(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    heading: str,
    lines: list[str],
    fill: tuple[int, int, int],
    accent: tuple[int, int, int],
    tag: str | None = None,
) -> None:
    card(draw, box, fill=fill, outline=accent, radius=18, width=2)
    draw.rounded_rectangle((box[0], box[1], box[0] + 10, box[3]), radius=10, fill=accent)
    text(draw, (box[0] + 24, box[1] + 15), heading, 18, accent, True, width=box[2] - box[0] - 42)
    y = box[1] + 48
    for item in lines:
        y = text(draw, (box[0] + 26, y), item, 13, NAVY, width=box[2] - box[0] - 45, gap=4)
    if tag:
        pill(draw, (box[0] + 24, box[3] - 34, box[2] - 24, box[3] - 10), tag, WHITE, accent)


def canvas(dark: bool = False) -> Image.Image:
    img = Image.new("RGB", (W, H), DEEP if dark else WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 18, H), fill=ICE if dark else TEAL)
    return img


def title(draw: ImageDraw.ImageDraw, heading: str, subheading: str, dark: bool = False) -> None:
    text(draw, (58, 38), heading, 38, WHITE if dark else NAVY, True)
    text(draw, (61, 88), subheading, 17, (196, 229, 235) if dark else MUTED, width=1340)


def footer(draw: ImageDraw.ImageDraw, value: str, dark: bool = False) -> None:
    y = H - 50
    draw.line((54, y - 8, W - 54, y - 8), fill=(73, 96, 105) if dark else LINE, width=2)
    text(draw, (58, y), value, 12, (168, 195, 204) if dark else MUTED, width=1420)


def read_summary(name: str) -> dict[str, str]:
    path = PUBLIC_PRODUCTS / name
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as fh:
        return {row["metric"]: row["value"] for row in csv.DictReader(fh)}


def fmt_count(summary: dict[str, str], key: str, fallback: str) -> str:
    value = summary.get(key, fallback)
    try:
        number = float(value)
    except ValueError:
        return value
    if number.is_integer():
        return f"{int(number):,}"
    return f"{number:,.1f}"


def summaries() -> dict[str, str]:
    well = read_summary("north_slope_well_stability_context_summary_2026-06-14.csv")
    temp = read_summary("g10015_temperature_profile_summary_2026-06-14.csv")
    model = read_summary("stability_temperature_model_summary_2026-06-14.csv")
    screen = read_summary("stability_screen_summary_2026-06-14_methane_5ppt_v1.csv")
    return {
        "wells": fmt_count(well, "Arctic Slope public wells", "8,084"),
        "profiles": fmt_count(temp, "G10015 profiles", "184"),
        "codes": fmt_count(temp, "Unique well codes", "24"),
        "temp_rows": fmt_count(model, "Temperature model rows", "16,168"),
        "temp_calculated": fmt_count(model, "Calculated key depths", "919"),
        "temp_extrapolated": fmt_count(model, "Extrapolated key depths", "387"),
        "temp_blocked": fmt_count(model, "Blocked key depths", "15,249"),
        "screen_rows": fmt_count(screen, "Screen rows", "8,084"),
        "screen_calculated": fmt_count(screen, "Calculated stability intervals", "22"),
        "screen_no_interval": fmt_count(screen, "No stable interval found", "8"),
        "screen_blocked": fmt_count(screen, "Blocked rows", "8,054"),
    }


def save(img: Image.Image, name: str) -> Path:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    path = ASSET_DIR / name
    img.save(path, quality=94)
    return path


def full_workflow_panel() -> Path:
    values = summaries()
    img = Image.new("RGB", (EXPANDED_W, EXPANDED_H), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 30, EXPANDED_H), fill=TEAL)
    draw.rectangle((0, 0, EXPANDED_W, 150), fill=(246, 251, 252))
    draw.line((70, 150, EXPANDED_W - 70, 150), fill=LINE, width=3)
    text(draw, (78, 42), "Equation-Driven North Slope Gas Hydrate ML Workflow", 46, NAVY, True)
    text(
        draw,
        (80, 98),
        "Expanded roadmap from source headers and stability constraints to leakage-safe occurrence classification, saturation regression, validation, and review exports.",
        22,
        MUTED,
        width=2450,
    )

    def big_pill(box: tuple[int, int, int, int], label: str, fill, accent) -> None:
        card(draw, box, fill=fill, outline=accent, radius=20, width=2)
        f = font(19, True)
        x = box[0] + (box[2] - box[0]) // 2 - int(draw.textlength(label, font=f) // 2)
        draw.text((x, box[1] + 11), label, font=f, fill=accent)

    def section(box: tuple[int, int, int, int], label: str, accent) -> None:
        card(draw, box, fill=(249, 252, 252), outline=(214, 230, 234), radius=28, width=2)
        draw.rectangle((box[0] + 22, box[1] + 25, box[0] + 33, box[1] + 62), fill=accent)
        text(draw, (box[0] + 50, box[1] + 24), label, 24, accent, True)

    def detailed_node(
        box: tuple[int, int, int, int],
        heading: str,
        rows: list[str],
        fill,
        accent,
        tag: str | None = None,
        size: int = 21,
    ) -> None:
        card(draw, box, fill=fill, outline=accent, radius=22, width=3)
        draw.rounded_rectangle((box[0], box[1], box[0] + 14, box[3]), radius=12, fill=accent)
        y = text(draw, (box[0] + 34, box[1] + 22), heading, 24, accent, True, width=box[2] - box[0] - 60)
        y += 6
        for row in rows:
            draw.ellipse((box[0] + 36, y + 8, box[0] + 47, y + 19), fill=accent)
            y = text(draw, (box[0] + 58, y), row, size, NAVY, width=box[2] - box[0] - 85, gap=8)
        if tag:
            big_pill((box[0] + 34, box[3] - 50, box[2] - 34, box[3] - 12), tag, WHITE, accent)

    def formula_box(
        box: tuple[int, int, int, int],
        heading: str,
        formulas: list[str],
        note: str,
        accent,
    ) -> None:
        card(draw, box, fill=WHITE, outline=accent, radius=18, width=2)
        text(draw, (box[0] + 22, box[1] + 16), heading, 22, accent, True, width=box[2] - box[0] - 44)
        y = box[1] + 55
        for formula in formulas:
            card(draw, (box[0] + 22, y, box[2] - 22, y + 43), fill=(247, 251, 252), outline=(224, 235, 238), radius=9, width=1)
            text(draw, (box[0] + 38, y + 10), formula, 19, NAVY, True, width=box[2] - box[0] - 76, gap=3)
            y += 51
        text(draw, (box[0] + 24, y + 2), note, 17, MUTED, width=box[2] - box[0] - 48, gap=5)

    def arrow_big(
        start: tuple[int, int],
        end: tuple[int, int],
        fill=TEAL,
        width: int = 5,
        label: str | None = None,
        label_offset: tuple[int, int] = (0, 0),
    ) -> None:
        draw.line((start, end), fill=fill, width=width)
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        length = 22
        points = [
            end,
            (int(end[0] - length * math.cos(angle - 0.45)), int(end[1] - length * math.sin(angle - 0.45))),
            (int(end[0] - length * math.cos(angle + 0.45)), int(end[1] - length * math.sin(angle + 0.45))),
        ]
        draw.polygon(points, fill=fill)
        if label:
            mx = (start[0] + end[0]) // 2 + label_offset[0]
            my = (start[1] + end[1]) // 2 + label_offset[1]
            f = font(18, True)
            pad = 11
            w = int(draw.textlength(label, font=f)) + pad * 2
            card(draw, (mx - w // 2, my - 20, mx + w // 2, my + 19), fill=WHITE, outline=fill, radius=12, width=2)
            draw.text((mx - w // 2 + pad, my - 12), label, font=f, fill=fill)

    def dashed_arrow(
        start: tuple[int, int],
        end: tuple[int, int],
        fill=RED,
        width: int = 5,
        label: str | None = None,
        label_offset: tuple[int, int] = (0, 0),
    ) -> None:
        x1, y1 = start
        x2, y2 = end
        dx, dy = x2 - x1, y2 - y1
        length = math.hypot(dx, dy)
        if length == 0:
            return
        ux, uy = dx / length, dy / length
        dash, gap = 24, 14
        distance = 0.0
        while distance < length - 28:
            sx = int(x1 + ux * distance)
            sy = int(y1 + uy * distance)
            ex = int(x1 + ux * min(distance + dash, length - 28))
            ey = int(y1 + uy * min(distance + dash, length - 28))
            draw.line((sx, sy, ex, ey), fill=fill, width=width)
            distance += dash + gap
        arrow_big((int(x1 + ux * max(length - 42, 0)), int(y1 + uy * max(length - 42, 0))), end, fill, width, label, label_offset)

    # Main section backgrounds.
    section((70, 178, 710, 1500), "1. Source and schema controls", TEAL)
    section((750, 178, 1515, 1500), "2. Stability and physics features", BLUE)
    section((1555, 178, 2165, 1500), "3. Leakage-safe ML runtime", PURPLE)
    section((2205, 178, 2930, 1500), "4. Validation and reviewed outputs", GREEN)

    detailed_node(
        (105, 245, 680, 455),
        "Source intake",
        [
            "Public scaffold: DNR wells, GGD223 controls, G10015 temperature profiles, USGS hydrate AUs.",
            "Approved runtime later: LAS/CSV logs, core, NMR, workbook labels.",
            "Keep original headers, units, well names, depth basis, and provenance before aliasing.",
        ],
        ICE_LIGHT,
        TEAL,
        "schema before modeling",
        size=18,
    )
    detailed_node(
        (105, 500, 680, 730),
        "Unit, depth, and QC gates",
        [
            "DEPTH/DEPT/True Depth -> one depth axis with original values retained.",
            "RHOB, GR, Rt, Vp, Vs, NMRPHI, phi_D, caliper and missingness flags.",
            "Bad-hole, outlier, unit, and alignment failures are flagged before features.",
        ],
        WHITE,
        GREEN,
        "fail closed",
        size=18,
    )
    detailed_node(
        (105, 775, 680, 1010),
        "Current data reality",
        [
            f"{values['wells']} public scaffold wells; {values['profiles']} G10015 profiles across {values['codes']} codes.",
            f"{values['temp_calculated']} calculated and {values['temp_extrapolated']} extrapolated temperature key depths.",
            f"{values['screen_calculated']} baseline stability-admissibility intervals; {values['screen_blocked']} blocked screen rows.",
        ],
        BLUE_LIGHT,
        BLUE,
        "screening context only",
        size=19,
    )
    detailed_node(
        (105, 1055, 680, 1425),
        "Guardrails that shape the ML design",
        [
            "No public diagram is hydrate proof, final stability, saturation, model accuracy, or sweet-spot ranking.",
            "Stability becomes an admissibility/context field, confidence label, mask, or caveat.",
            "Target-like columns such as Sgh, S_h, Sh, NMR_SAT, Hydrate Saturation, Swr, and phase labels cannot become predictors.",
            "Final validation must hold out whole wells or compartments, not random neighboring depth rows.",
        ],
        RED_LIGHT,
        RED,
        "prevents overclaiming",
        size=18,
    )

    formula_box(
        (790, 245, 1475, 590),
        "Pressure-temperature stability branch",
        [
            "P_abs(MPa) = P_surface + (rho_w * g * z_m) / 1,000,000",
            "T_model(z) = interp(profile); extrapolate only inside guardrail",
            "stable_candidate = T_model(z) <= T_eq(P_abs, CH4, 5 ppt)",
        ],
        "Top/base/thickness are written only when depth, pressure, temperature, phase-curve range, AU context, and source-control gates pass.",
        BLUE,
    )
    detailed_node(
        (790, 640, 1115, 900),
        "Measured log families",
        [
            "Lithology/reservoir: GR, RHOB, phi_D, NMRPHI.",
            "Fluids/hydrate response: Rt and resistivity family.",
            "Mechanical/elastic response: Vp, Vs, impedance, Vp/Vs.",
            "QC context: caliper, washout, missingness, depth mismatch.",
        ],
        WHITE,
        TEAL,
        size=18,
    )
    formula_box(
        (1150, 640, 1475, 900),
        "Derived physics features",
        [
            "Vsh = (GR - GR_clean) / (GR_shale - GR_clean)",
            "phi_D = (rho_ma - RHOB) / (rho_ma - rho_f)",
            "Vp = 304.8 / DT;  Vs = 304.8 / DTS",
            "AI = RHOB * Vp",
        ],
        "Use only after units and curve meanings are confirmed.",
        GREEN,
    )
    formula_box(
        (790, 955, 1475, 1188),
        "Elastic and saturation baseline checks",
        [
            "mu_rho = RHOB * Vs^2",
            "lambda_rho = RHOB * (Vp^2 - 2 * Vs^2)",
            "Sh_NMRD = max(0, (phi_D - phi_NMR) / phi_D)",
        ],
        "Archie/NMR-density saturation estimates are baselines or validation checks unless the mentor approves a target definition.",
        AMBER,
    )
    detailed_node(
        (790, 1232, 1475, 1425),
        "Feature matrix contract",
        [
            "X_allowed = measured logs + derived physics + QC flags + stability context.",
            "Every feature row keeps source, unit, depth, QC, confidence, and role metadata.",
            "Rows blocked by source controls remain blank rather than silently inferred.",
        ],
        GREEN_LIGHT,
        GREEN,
        "predictors only",
        size=18,
    )

    detailed_node(
        (1590, 245, 2130, 455),
        "Target registry",
        [
            "Y_occurrence: interval/phase/core-supported hydrate class when approved.",
            "Y_saturation: Sgh / S_h / Sh / NMR_SAT / Hydrate Saturation after source mapping.",
            "Targets can supervise, calibrate, or validate. They do not enter X_allowed.",
        ],
        RED_LIGHT,
        RED,
        "labels only",
        size=18,
    )
    detailed_node(
        (1590, 500, 2130, 735),
        "Whole-well split first",
        [
            "Partition by well, field, or compartment before imputation, scaling, selection, or tuning.",
            "Debugging row splits can exist, but final claims need unseen wells/compartments.",
            "Keep train/validation/test provenance in every exported row.",
        ],
        ICE_LIGHT,
        BLUE,
        "no depth-neighbor leakage",
        size=18,
    )
    detailed_node(
        (1590, 780, 2130, 1025),
        "Train-only preprocessing",
        [
            "Fit imputation, min-max/standard scaling, feature selection, PCA, and thresholds on training wells only.",
            "Apply frozen transforms to validation, locked test, and prediction wells.",
            "Start with simple baselines before tree/ANN/Keras candidates.",
        ],
        PURPLE_LIGHT,
        PURPLE,
        "reproducible runtime",
        size=18,
    )
    formula_box(
        (1590, 1070, 2130, 1425),
        "Model heads and learning targets",
        [
            "X_allowed -> P(hydrate occurrence)",
            "X_allowed -> Sh_pred",
            "loss = classifier_loss + regressor_loss + calibration review",
            "candidate models = baseline, tree/boosting, ANN/Keras",
        ],
        "Occurrence and saturation stay linked scientifically, but they are evaluated as separate outputs with separate residual/error review.",
        PURPLE,
    )

    formula_box(
        (2240, 245, 2895, 455),
        "Occurrence classifier output",
        [
            "P_hydrate(z) = model_occurrence(X_allowed)",
            "class = calibrated threshold(P_hydrate)",
        ],
        "Report probability, calibration, confusion matrix, false-positive review, mimic flags, and confidence.",
        BLUE,
    )
    formula_box(
        (2240, 500, 2895, 735),
        "Saturation regression output",
        [
            "Sh_pred(z) = model_saturation(X_allowed)",
            "residual = Sh_target - Sh_pred",
        ],
        "Compare against approved NMR/core/interpreted saturation targets by well, depth, reservoir, and QC state.",
        GREEN,
    )
    detailed_node(
        (2240, 780, 2895, 1088),
        "Validation and error review",
        [
            "Held-out wells/compartments: accuracy, recall/precision, calibration, R2/RMSE/MAE where valid.",
            "Residual review by depth, lithology, permafrost/stability context, caliper, missing curves, and source confidence.",
            "Mimic checks: shale, ice, cementation, gas, washout, tool response, pressure-temperature assumption.",
            "Document where the model is out-of-domain rather than forcing a prediction.",
        ],
        AMBER_LIGHT,
        AMBER,
        size=18,
    )
    detailed_node(
        (2240, 1135, 2895, 1425),
        "Reviewed export package",
        [
            "Per-depth outputs: P_hydrate, Sh_pred, uncertainty, QC, mimic, reason flags.",
            "Per-well summaries: interval candidates, source confidence, validation status, blocked reasons.",
            "Maps/plots/tables become public-safe only after review removes restricted rows and unsupported claims.",
        ],
        GREEN_LIGHT,
        GREEN,
        "future approved-data result",
        size=18,
    )

    # Flow arrows.
    arrow_big((680, 350), (790, 350), TEAL, label="source rows")
    arrow_big((680, 615), (790, 770), GREEN, label="validated inputs", label_offset=(-10, -20))
    arrow_big((680, 890), (790, 1328), BLUE, label="current context", label_offset=(-20, -26))
    arrow_big((1115, 770), (1150, 770), TEAL)
    arrow_big((1132, 900), (1132, 955), GREEN, label="derive", label_offset=(66, 0))
    arrow_big((1132, 1188), (1132, 1232), GREEN)
    arrow_big((1475, 1328), (1590, 616), GREEN, label="X_allowed", label_offset=(16, -130))
    dashed_arrow((1800, 455), (1800, 500), RED, label="target map")
    dashed_arrow((1590, 350), (1475, 1328), RED, label="bypass feature matrix", label_offset=(-120, 175))
    arrow_big((1860, 735), (1860, 780), PURPLE)
    arrow_big((1860, 1025), (1860, 1070), PURPLE)
    arrow_big((2130, 1238), (2240, 350), PURPLE, label="classification head", label_offset=(68, -190))
    arrow_big((2130, 1298), (2240, 615), PURPLE, label="regression head", label_offset=(60, 80))
    arrow_big((2565, 455), (2565, 500), BLUE)
    arrow_big((2565, 735), (2565, 780), GREEN)
    arrow_big((2565, 1088), (2565, 1135), AMBER)

    # Status strip.
    card(draw, (70, 1520, 2930, 1626), fill=(245, 249, 250), outline=LINE, radius=22, width=2)
    big_pill((105, 1545, 270, 1595), "complete", GREEN_LIGHT, GREEN)
    text(draw, (295, 1543), "source boundary, 5 ppt methane phase lookup, hydrostatic pressure, temperature model, schema roles, leakage guardrails", 19, NAVY, width=820)
    big_pill((1160, 1545, 1345, 1595), "calculated", BLUE_LIGHT, BLUE)
    text(draw, (1372, 1543), f"{values['temp_calculated']} temp key depths; {values['screen_calculated']} baseline admissibility intervals; {values['screen_no_interval']} no-interval rows", 19, NAVY, width=640)
    big_pill((2140, 1545, 2295, 1595), "future", AMBER_LIGHT, AMBER)
    text(draw, (2322, 1543), "approved logs/core/NMR execution, trained models, saturation predictions, final proof, and sweet-spot ranking", 19, NAVY, width=560)
    text(
        draw,
        (80, 1640),
        "Guardrail: stability is necessary but not sufficient. The ML pipeline predicts occurrence and saturation only after approved labels, leakage-safe preprocessing, and held-out-well validation.",
        17,
        MUTED,
        width=2800,
    )

    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    expanded_path = ASSET_DIR / "full_project_ml_workflow_flowchart_expanded.png"
    img.save(expanded_path, quality=94)
    slide_img = img.resize((W, H), Image.Resampling.LANCZOS)
    return save(slide_img, "full_project_ml_workflow_flowchart.png")


def overview_slide_panel() -> Path:
    # Reuse the full workflow image as the main slide panel.
    return full_workflow_panel()


def flow_slide(
    filename: str,
    heading: str,
    subheading: str,
    steps: list[tuple[str, list[str], tuple[int, int, int], tuple[int, int, int]]],
    guardrail: str,
    footer_text: str,
) -> Path:
    img = canvas(False)
    draw = ImageDraw.Draw(img)
    title(draw, heading, subheading)
    start_x = 70
    y = 210
    box_w = 260
    gap = 35
    previous: tuple[int, int, int, int] | None = None
    for idx, (step_heading, lines, fill, accent) in enumerate(steps):
        x = start_x + idx * (box_w + gap)
        box = (x, y, x + box_w, y + 250)
        node(draw, box, step_heading, lines, fill, accent)
        if previous:
            arrow(draw, (previous[2] + 8, y + 125), (box[0] - 8, y + 125), accent)
        previous = box
    card(draw, (74, 595, 1528, 736), fill=LIGHT, outline=LINE, radius=18)
    text(draw, (108, 623), "Guardrail", 20, RED, True)
    text(draw, (250, 618), guardrail, 26, NAVY, True, width=1170)
    footer(draw, footer_text)
    return save(img, filename)


def slide_04_inputs_boundary() -> Path:
    return flow_slide(
        "slide_04_inputs_boundary_zoom.png",
        "The Inputs Split Into Public Context And Approved Runtime Data",
        "The diagram separates what can be shown publicly from what must stay inside OSL or the approved environment.",
        [
            ("Public sources", ["DNR wells", "GGD223 / G10015", "USGS AU + phase curve", "source documents"], ICE_LIGHT, TEAL),
            ("Public products", ["compact CSV summaries", "screen status counts", "website visuals", "mentor slides"], BLUE_LIGHT, BLUE),
            ("Approved inputs", ["LAS / CSV logs", "core and NMR", "workbook labels", "runtime only"], GREEN_LIGHT, GREEN),
            ("Boundary review", ["no approved rows", "no restricted IDs", "no trained models", "summaries only"], RED_LIGHT, RED),
            ("Deliverables", ["Word explanation", "9-slide deck", "Streamlit scaffold", "public-safe exports"], WHITE, TEAL),
        ],
        "The public side explains the method. The approved side runs the real log/core analysis.",
        "Use this as the slide-deck explanation for why GitHub/Streamlit and OSL both exist.",
    )


def slide_05_stability_branch() -> Path:
    return flow_slide(
        "slide_05_stability_branch_zoom.png",
        "Stability Connects Into ML As Context, Not As Proof",
        "The pressure-temperature screen is a guarded branch that feeds context, masks, confidence, and caveats.",
        [
            ("Depth basis", ["TrueVertic preferred", "DrillerTot fallback", "public depth caveat"], WHITE, TEAL),
            ("Pressure", ["hydrostatic assumption", "absolute pressure", "not measured pressure"], ICE_LIGHT, BLUE),
            ("Temperature", ["G10015 profile", "GGD223 control", "interpolate / extrapolate", "block missing"], BLUE_LIGHT, BLUE),
            ("Phase curve", ["100% methane", "5 ppt salinity", "SIR 2008 digitized", "scenario capable"], AMBER_LIGHT, AMBER),
            ("Stability status", ["calculated interval", "no stable interval", "blocked", "not hydrate proof"], RED_LIGHT, RED),
        ],
        "A stable interval can only say hydrate is admissible under assumptions; logs/core decide occurrence and saturation later.",
        "Current guarded run: 8,084 screen rows, 22 calculated admissibility intervals, 8 no-stable-interval rows, 8,054 blocked rows.",
    )


def slide_06_features() -> Path:
    return flow_slide(
        "slide_06_features_zoom.png",
        "Well Logs Become Feature Blocks Only After QC And Units",
        "The ML table is built from measured curves, derived physics features, and context flags with source provenance.",
        [
            ("Headers", ["DEPTH / RHOB / GR", "Rt / Vp / Vs", "NMRPHI where measured", "source mnemonics kept"], WHITE, TEAL),
            ("Normalize", ["feet vs meters", "g/cc vs kg/m3", "velocity/slowness", "raw values retained"], ICE_LIGHT, BLUE),
            ("QC + alignment", ["caliper / washout", "missingness", "outliers", "core-log offsets"], AMBER_LIGHT, AMBER),
            ("Derived features", ["AI = rho * Vp", "Vp/Vs", "G, K, E, nu", "lambda-rho / mu-rho"], GREEN_LIGHT, GREEN),
            ("Context flags", ["stability admissibility", "reservoir quality", "mimic risk", "source confidence"], BLUE_LIGHT, BLUE),
        ],
        "High resistivity, low GR, high velocity, or stability context cannot become standalone hydrate labels.",
        "This follows the science-to-ML ladder: stability context -> reservoir quality -> hydrate response.",
    )


def slide_07_leakage_modeling() -> Path:
    return flow_slide(
        "slide_07_leakage_modeling_zoom.png",
        "The Leakage Barrier Controls What The Model Is Allowed To Learn",
        "Targets supervise or validate the model; they do not enter the feature table as predictors.",
        [
            ("Target registry", ["S_h / Sgh", "NMR_SAT", "phase labels", "core calibration"], RED_LIGHT, RED),
            ("Allowed inputs", ["measured logs", "derived features", "QC/context flags", "source confidence"], GREEN_LIGHT, GREEN),
            ("Split first", ["complete wells", "compartments", "train / validation / test", "no random-row final claim"], ICE_LIGHT, BLUE),
            ("Train controls", ["train-only scaling", "train-only imputation", "baseline first", "tree/ANN after gates"], PURPLE_LIGHT, PURPLE),
            ("Two heads", ["occurrence classifier", "saturation regressor", "linked but separate", "calibrated outputs"], WHITE, TEAL),
        ],
        "The answer columns cannot leak into the input side, even if they are useful for calibration or validation.",
        "ML source anchors: Chong et al. 2022, Singh et al. 2021, Chong et al. 2024; project results wait for approved validation.",
    )


def slide_08_outputs_validation() -> Path:
    return flow_slide(
        "slide_08_outputs_validation_zoom.png",
        "The Final Product Is A Reviewed Output Package, Not One Score",
        "The approved runtime should export interpretable outputs and only public-safe reductions after review.",
        [
            ("Occurrence", ["probability track", "calibration check", "balanced metrics", "well holdouts"], BLUE_LIGHT, BLUE),
            ("Saturation", ["continuous S_h estimate", "target overlay where allowed", "residual review", "uncertainty"], GREEN_LIGHT, GREEN),
            ("Reason flags", ["supporting features", "mimic risks", "QC warnings", "out-of-domain"], AMBER_LIGHT, AMBER),
            ("Validation", ["NMR/core comparison", "well/compartment split", "depth/reservoir residuals", "no fake metrics"], PURPLE_LIGHT, PURPLE),
            ("Exports", ["plots and tables", "GIS links", "manuscript figures", "public-safe summary"], WHITE, TEAL),
        ],
        "Do not present public stability status, screenshots, or comparative-source metrics as this project's validated ML results.",
        "Outputs remain approved-runtime products until the public-safe boundary review decides what can be shown.",
    )


def slide_09_status_decisions() -> Path:
    values = summaries()
    img = canvas(False)
    draw = ImageDraw.Draw(img)
    title(draw, "What The Diagram Says About Where We Are Now", "The project has a defensible workflow map; it does not yet have approved-data hydrate predictions.")

    columns = [
        (
            "Complete",
            [
                "public / OSL boundary",
                "public scaffold and status products",
                "methane 5 ppt phase lookup",
                "hydrostatic pressure logic",
                "temperature-model logic",
                "guarded stability-screen writer",
            ],
            GREEN_LIGHT,
            GREEN,
        ),
        (
            "Calculated",
            [
                f"{values['temp_rows']} temperature key-depth rows",
                f"{values['temp_calculated']} calculated key depths",
                f"{values['temp_extrapolated']} extrapolated key depths",
                f"{values['screen_calculated']} baseline admissibility intervals",
                f"{values['screen_no_interval']} sufficient-input no-interval rows",
            ],
            BLUE_LIGHT,
            BLUE,
        ),
        (
            "Blocked / future",
            [
                f"{values['temp_blocked']} blocked temperature key depths",
                f"{values['screen_blocked']} blocked screen rows",
                "approved logs/core/NMR execution",
                "occurrence labels and saturation targets",
                "trained ML metrics and sweet-spot ranking",
            ],
            RED_LIGHT,
            RED,
        ),
    ]
    x = 72
    for heading, rows, fill, accent in columns:
        card(draw, (x, 170, x + 455, 620), fill=fill, outline=accent, radius=22, width=2)
        text(draw, (x + 28, 198), heading, 28, accent, True)
        y = 258
        for row in rows:
            draw.ellipse((x + 28, y + 5, x + 40, y + 17), fill=accent)
            y = text(draw, (x + 54, y), row, 19, NAVY, width=360, gap=12)
        x += 505

    card(draw, (72, 675, 1530, 790), fill=LIGHT, outline=LINE, radius=18)
    text(draw, (105, 704), "Next decisions", 20, AMBER, True)
    text(
        draw,
        (280, 698),
        "baseline phase curve, mixed-gas sensitivity, confidence thresholds, OM-222 digitization, approved validation fields, and whether final ML always shows occurrence classification plus saturation regression as linked outputs.",
        22,
        NAVY,
        True,
        width=1160,
    )
    footer(draw, "Blocked means the workflow is refusing to overclaim without required inputs; it does not mean no hydrate.")
    return save(img, "slide_09_status_and_next_decisions.png")


def preserve_source_slide_panel(slide_number: int, name: str) -> Path:
    if not SOURCE_DECK.exists():
        raise FileNotFoundError(SOURCE_DECK)
    prs = Presentation(SOURCE_DECK)
    slide = prs.slides[slide_number - 1]
    pictures = [shape for shape in slide.shapes if shape.shape_type == 13]
    if len(pictures) != 1:
        raise ValueError(f"Source slide {slide_number} should have exactly one raster panel, found {len(pictures)}")
    blob = pictures[0].image.blob
    with Image.open(BytesIO(blob)) as image:
        if image.size != (W, H):
            raise ValueError(f"Source slide {slide_number} image size is {image.size}, expected {(W, H)}")
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    path = ASSET_DIR / name
    path.write_bytes(blob)
    LOCKED_SLIDE_HASHES[slide_number] = hashlib.sha256(blob).hexdigest()
    return path


def build_panels() -> list[Path]:
    return [
        preserve_source_slide_panel(1, "slide_01_locked_from_current_gmail_deck.png"),
        preserve_source_slide_panel(2, "slide_02_locked_from_current_gmail_deck.png"),
        overview_slide_panel(),
        slide_04_inputs_boundary(),
        slide_05_stability_branch(),
        slide_06_features(),
        slide_07_leakage_modeling(),
        slide_08_outputs_validation(),
        slide_09_status_decisions(),
    ]


def clear_slide(slide) -> None:
    for shape in list(slide.shapes):
        element = shape._element  # noqa: SLF001 - python-pptx has no public remove API.
        element.getparent().remove(element)


def rebuild_deck(panel_paths: list[Path]) -> Path:
    prs = Presentation(SOURCE_DECK)
    if len(prs.slides) != 9:
        raise ValueError(f"Expected 9 slides in {SOURCE_DECK}, found {len(prs.slides)}")
    if len(panel_paths) != 9:
        raise ValueError(f"Expected 9 panels, found {len(panel_paths)}")
    for slide, panel in zip(prs.slides, panel_paths, strict=True):
        clear_slide(slide)
        slide.shapes.add_picture(str(panel), 0, 0, width=prs.slide_width, height=prs.slide_height)
    prs.save(OUT_DECK)
    return OUT_DECK


def verify_deck(path: Path) -> None:
    prs = Presentation(path)
    if len(prs.slides) != 9:
        raise ValueError(f"Expected 9 slides, found {len(prs.slides)}")
    for idx, slide in enumerate(prs.slides, start=1):
        pictures = [shape for shape in slide.shapes if shape.shape_type == 13]
        if len(pictures) != 1:
            raise ValueError(f"Slide {idx} should have exactly one raster panel, found {len(pictures)}")
        blob = pictures[0].image.blob
        with Image.open(BytesIO(blob)) as image:
            if image.size != (W, H):
                raise ValueError(f"Slide {idx} image size is {image.size}, expected {(W, H)}")
        if idx in LOCKED_SLIDE_HASHES and hashlib.sha256(blob).hexdigest() != LOCKED_SLIDE_HASHES[idx]:
            raise ValueError(f"Slide {idx} no longer matches the locked source panel")


def build_contact_sheet(panel_paths: list[Path]) -> Path:
    thumb_w, thumb_h = 480, 270
    margin = 34
    label_h = 34
    gap = 26
    sheet_w = margin * 2 + thumb_w * 3 + gap * 2
    sheet_h = margin * 2 + (thumb_h + label_h) * 3 + gap * 2
    img = Image.new("RGB", (sheet_w, sheet_h), WHITE)
    draw = ImageDraw.Draw(img)
    for idx, path in enumerate(panel_paths, start=1):
        row = (idx - 1) // 3
        col = (idx - 1) % 3
        x = margin + col * (thumb_w + gap)
        y = margin + row * (thumb_h + label_h + gap)
        panel = Image.open(path).convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        card(draw, (x - 4, y - 4, x + thumb_w + 4, y + thumb_h + label_h), fill=(248, 251, 252), outline=LINE, radius=14, width=2)
        img.paste(panel, (x, y))
        draw.rectangle((x, y, x + thumb_w, y + thumb_h), outline=(160, 190, 198), width=2)
        text(draw, (x + 14, y + thumb_h + 9), f"Slide {idx}", 18, NAVY, True, width=thumb_w - 28)
    OUT_CONTACT_SHEET.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT_CONTACT_SHEET, quality=94)
    return OUT_CONTACT_SHEET


def apply_doc_style(document: Document) -> None:
    normal = document.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(10.5)
    for style_name, size in [("Title", 22), ("Heading 1", 16), ("Heading 2", 13)]:
        style = document.styles[style_name]
        style.font.name = "Arial"
        style.font.size = Pt(size)
        style.font.bold = True


def build_word_companion(diagram_path: Path) -> Path:
    document = Document()
    apply_doc_style(document)
    section = document.sections[0]
    section.orientation = WD_ORIENT.LANDSCAPE
    section.page_width, section.page_height = section.page_height, section.page_width
    section.top_margin = Inches(0.55)
    section.bottom_margin = Inches(0.55)
    section.left_margin = Inches(0.55)
    section.right_margin = Inches(0.55)

    props = document.core_properties
    props.title = "North Slope Gas Hydrate Full ML Workflow Diagram"
    props.subject = "Diagram-first explanation of the public, OSL, stability, and ML workflow"
    props.author = "North Slope Gas Hydrates project"

    document.add_heading("North Slope Gas Hydrate Full ML Workflow Diagram", level=0)
    document.add_paragraph(
        "This companion page explains the one-map workflow requested for the slide refresh. "
        "The figure connects source and schema controls, OpenScienceLab and approved-runtime inputs, "
        "the guarded pressure-temperature stability branch, well-log physics equations, the leakage "
        "barrier, occurrence classification, saturation regression, validation, and reviewed exports."
    )
    document.add_picture(str(diagram_path), width=Inches(9.9))

    document.add_heading("How To Read The Diagram", level=1)
    for item in [
        "The left lane is source and schema control: public-source context, current status counts, original headers, unit checks, depth basis, and QC gates.",
        "The center and right lanes are the OSL and approved-runtime path: raw source rebuilds, approved logs/core/NMR later, pressure-temperature stability context, feature engineering, modeling, and validation.",
        "The equation blocks show how pressure, temperature, phase-boundary lookup, lithology, porosity, velocity, elastic, and saturation-baseline calculations become context fields, features, or validation checks.",
        "The stability branch feeds context, masks, confidence labels, and caveats into the ML workflow. It does not become hydrate proof or a saturation label.",
        "The leakage barrier keeps S_h, Sgh, NMR_SAT, phase labels, and final ranks out of predictor features unless a field is proven to be an independent measured input.",
        "The final ML design keeps occurrence classification and saturation regression linked but separate.",
    ]:
        document.add_paragraph(item, style="List Bullet")

    document.add_heading("Current Status Shown In The Figure", level=1)
    values = summaries()
    status_table = document.add_table(rows=1, cols=3)
    status_table.style = "Table Grid"
    headers = ["Complete", "Calculated", "Blocked / Future"]
    for i, header in enumerate(headers):
        run = status_table.rows[0].cells[i].paragraphs[0].add_run(header)
        run.bold = True
    row = status_table.add_row().cells
    row[0].text = "Public/OSL boundary; phase curve; pressure model; temperature-model logic; source-control labels; guarded writer."
    row[1].text = (
        f"{values['temp_calculated']} temperature key depths, "
        f"{values['temp_extrapolated']} extrapolated key depths, and "
        f"{values['screen_calculated']} baseline stability-admissibility intervals."
    )
    row[2].text = (
        f"{values['temp_blocked']} temperature key-depth rows, "
        f"{values['screen_blocked']} screen rows, approved logs/core/NMR, "
        "trained ML metrics, saturation outputs, hydrate proof, and sweet-spot ranking."
    )

    document.add_heading("Required Guardrail Language", level=1)
    document.add_paragraph(
        "This is a workflow and admissibility-screen diagram. It does not claim final hydrate stability, "
        "hydrate proof, hydrate saturation, validated ML performance, producibility, or sweet spots."
    )

    OUT_DOCX.parent.mkdir(parents=True, exist_ok=True)
    document.save(OUT_DOCX)
    return OUT_DOCX


def main() -> None:
    panels = build_panels()
    deck = rebuild_deck(panels)
    verify_deck(deck)
    contact_sheet = build_contact_sheet(panels)
    docx = build_word_companion(panels[2])
    print(f"Wrote {panels[2]}")
    print(f"Wrote {contact_sheet}")
    print(f"Wrote {deck}")
    print(f"Wrote {docx}")
    print(f"Wrote panels to {ASSET_DIR}")


if __name__ == "__main__":
    main()
