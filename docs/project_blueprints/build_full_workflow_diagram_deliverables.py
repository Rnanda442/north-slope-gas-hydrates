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
PUBLIC_PRODUCTS = ROOT / "data" / "public_stability_products"

W, H = 1600, 900
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
    img = canvas(False)
    draw = ImageDraw.Draw(img)
    title(
        draw,
        "Full ML Workflow: Inputs, Stability, Features, Models, Outputs",
        "One map connects the public scaffold, OSL workbench, stability-admissibility screen, and later approved-data occurrence plus saturation ML.",
    )

    # Background zones.
    card(draw, (52, 122, 386, 722), fill=(238, 249, 250), outline=TEAL, radius=24, width=2)
    card(draw, (410, 122, 1548, 722), fill=(248, 251, 251), outline=LINE, radius=24, width=2)
    draw.line((398, 135, 398, 708), fill=RED, width=4)
    text(draw, (72, 138), "Public delivery surface", 19, TEAL, True)
    text(draw, (428, 138), "OpenScienceLab / approved-runtime build path", 19, GREEN, True)
    pill(draw, (310, 740, 486, 770), "data boundary", RED_LIGHT, RED)
    text(draw, (505, 742), "Only reviewed public-safe summaries, diagrams, and derived status products move back to GitHub/Streamlit/Word/slides.", 14, MUTED, width=870)

    node(
        draw,
        (72, 170, 366, 328),
        "Public/source inputs",
        [
            "Alaska DNR wells and public depths",
            "GGD223 permafrost controls",
            "G10015 temperature profiles",
            "USGS hydrate AUs and phase sources",
        ],
        ICE_LIGHT,
        TEAL,
    )
    node(
        draw,
        (72, 356, 366, 530),
        "Current public status",
        [
            f"{values['wells']} public scaffold wells",
            f"{values['profiles']} G10015 profiles / {values['codes']} codes",
            f"{values['screen_calculated']} calculated admissibility intervals",
            f"{values['screen_blocked']} blocked screen rows",
        ],
        WHITE,
        BLUE,
        "not hydrate proof",
    )
    node(
        draw,
        (72, 560, 366, 692),
        "Public communication",
        [
            "GitHub and Streamlit",
            "Word document and slide deck",
            "source-backed diagrams and caveats",
        ],
        WHITE,
        TEAL,
    )

    node(
        draw,
        (432, 170, 728, 328),
        "Stability inputs",
        [
            "depth basis -> hydrostatic pressure",
            "G10015/GGD223 temperature model",
            "100% methane + 5 ppt phase curve",
            "source-control confidence",
        ],
        ICE_LIGHT,
        BLUE,
    )
    node(
        draw,
        (772, 170, 1068, 328),
        "Stability branch",
        [
            "T_model <= T_eq(P_abs)",
            "top/base/thickness only when gates pass",
            "blocked when source coverage is insufficient",
        ],
        BLUE_LIGHT,
        BLUE,
        "admissibility only",
    )
    node(
        draw,
        (432, 366, 728, 524),
        "Approved inputs later",
        [
            "LAS / CSV well logs",
            "core, NMR, workbook labels",
            "original headers, units, mnemonics",
            "approved environment only",
        ],
        GREEN_LIGHT,
        GREEN,
    )
    node(
        draw,
        (772, 366, 1068, 524),
        "Preprocess and features",
        [
            "unit normalization and depth alignment",
            "caliper/QC/missingness review",
            "GR, RHOB, phi, Rt, Vp, Vs",
            "AI, Vp/Vs, G, K, lambda-rho, mu-rho",
        ],
        WHITE,
        GREEN,
    )
    node(
        draw,
        (772, 558, 1068, 692),
        "Leakage barrier",
        [
            "S_h / Sgh / NMR_SAT / phase labels",
            "target, calibration, or validation only",
            "excluded from predictor features",
        ],
        RED_LIGHT,
        RED,
    )
    node(
        draw,
        (1112, 260, 1330, 470),
        "Modeling path",
        [
            "complete-well or compartment split",
            "train-only preprocessing",
            "physics and simple baselines",
            "tree / ANN after controls pass",
        ],
        PURPLE_LIGHT,
        PURPLE,
    )
    node(
        draw,
        (1360, 190, 1530, 326),
        "Occurrence",
        ["classifier", "probability", "calibration"],
        BLUE_LIGHT,
        BLUE,
    )
    node(
        draw,
        (1360, 362, 1530, 498),
        "Saturation",
        ["regressor", "S_h estimate", "residual review"],
        GREEN_LIGHT,
        GREEN,
    )
    node(
        draw,
        (1112, 558, 1530, 692),
        "Validated outputs",
        [
            "probability, saturation, uncertainty",
            "QC status, mimic flags, reason flags",
            "tables, plots, GIS links, manuscript exports after review",
        ],
        AMBER_LIGHT,
        AMBER,
        "future approved-data result",
    )

    # Flow arrows.
    arrow(draw, (366, 245), (432, 245), TEAL, label="source context")
    arrow(draw, (728, 245), (772, 245), BLUE)
    arrow(draw, (1068, 252), (1112, 342), BLUE, label="context feature", label_offset=(-20, -18))
    arrow(draw, (366, 442), (432, 442), GREEN, label="OSL rebuild")
    arrow(draw, (218, 530), (218, 560), TEAL, width=3)
    arrow(draw, (728, 442), (772, 442), GREEN)
    arrow(draw, (920, 524), (920, 558), GREEN)
    arrow(draw, (1068, 625), (1112, 400), RED, label="features only")
    arrow(draw, (1330, 342), (1360, 258), PURPLE)
    arrow(draw, (1330, 400), (1360, 430), PURPLE)
    arrow(draw, (1445, 326), (1265, 558), BLUE)
    arrow(draw, (1445, 498), (1315, 558), GREEN)

    # Status and legend strip.
    card(draw, (72, 786, 1530, 836), fill=LIGHT, outline=LINE, radius=16)
    pill(draw, (94, 798, 204, 826), "complete", GREEN_LIGHT, GREEN)
    text(draw, (218, 801), "boundary, phase curve, pressure model, temperature logic, guarded writer", 13, NAVY, width=450)
    pill(draw, (690, 798, 808, 826), "calculated", BLUE_LIGHT, BLUE)
    text(draw, (822, 801), f"{values['temp_calculated']} temp key depths; {values['screen_calculated']} baseline admissibility intervals", 13, NAVY, width=370)
    pill(draw, (1225, 798, 1324, 826), "blocked", RED_LIGHT, RED)
    text(draw, (1338, 801), "approved ML outputs, proof, saturation, and sweet spots", 13, NAVY, width=175)
    footer(draw, "Guardrail: stability is necessary but not sufficient; occurrence and saturation wait for approved labels, core/NMR calibration, and grouped validation.")
    return save(img, "full_project_ml_workflow_flowchart.png")


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
        "The figure connects public source inputs, OpenScienceLab and approved-runtime inputs, "
        "the guarded pressure-temperature stability branch, feature engineering, the leakage "
        "barrier, occurrence classification, saturation regression, validation, and public-safe exports."
    )
    document.add_picture(str(diagram_path), width=Inches(9.9))

    document.add_heading("How To Read The Diagram", level=1)
    for item in [
        "The left lane is the public delivery surface: public sources, public stability products, GitHub, Streamlit, Word, and slides.",
        "The center and right lanes are the OSL and approved-runtime path: raw source rebuilds, approved logs/core/NMR later, preprocessing, feature engineering, modeling, and validation.",
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
    docx = build_word_companion(panels[2])
    print(f"Wrote {panels[2]}")
    print(f"Wrote {deck}")
    print(f"Wrote {docx}")
    print(f"Wrote panels to {ASSET_DIR}")


if __name__ == "__main__":
    main()
