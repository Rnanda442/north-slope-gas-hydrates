from __future__ import annotations

import math
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


W, H = 1920, 1080
OUT_W, OUT_H = 1600, 900

NAVY = (9, 34, 49)
DEEP = (4, 21, 33)
TEAL = (22, 125, 141)
ICE = (103, 208, 223)
GREEN = (37, 165, 138)
AMBER = (219, 165, 72)
RED = (204, 75, 74)
INK = (18, 52, 71)
MUTED = (86, 105, 115)
LIGHT = (244, 248, 249)
PANEL = (231, 240, 242)
WHITE = (255, 255, 255)
BLUE = (63, 138, 201)
PURPLE = (128, 139, 214)
SAND = (224, 195, 137)
SHALE = (110, 120, 128)
DARK_PANEL = (11, 39, 54)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = ["arialbd.ttf" if bold else "arial.ttf", "segoeuib.ttf" if bold else "segoeui.ttf"]
    for name in names:
        for root in (Path("C:/Windows/Fonts"), Path("/usr/share/fonts/truetype/dejavu")):
            path = root / name
            if path.exists():
                return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def draw_text(
    d: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    size: int,
    fill: tuple[int, int, int] = INK,
    bold: bool = False,
    width: int | None = None,
    anchor: str | None = None,
    align: str = "left",
    spacing: int = 6,
) -> None:
    f = font(size, bold)
    if width is None:
        d.text(xy, text, font=f, fill=fill, anchor=anchor)
        return
    lines: list[str] = []
    for raw in text.splitlines():
        if not raw:
            lines.append("")
            continue
        current = ""
        for word in raw.split():
            test = f"{current} {word}".strip()
            if d.textlength(test, font=f) <= width or not current:
                current = test
            else:
                lines.append(current)
                current = word
        lines.append(current)
    y = xy[1]
    for line in lines:
        if align == "center":
            x = xy[0] + width // 2
            d.text((x, y), line, font=f, fill=fill, anchor="ma")
        else:
            d.text((xy[0], y), line, font=f, fill=fill)
        y += size + spacing


def card(d: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill=WHITE, outline=(201, 220, 225), radius=22, width=2) -> None:
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(d: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], fill=TEAL, width=4) -> None:
    d.line([start, end], fill=fill, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    length = 17
    pts = [
        end,
        (int(end[0] - length * math.cos(angle - 0.45)), int(end[1] - length * math.sin(angle - 0.45))),
        (int(end[0] - length * math.cos(angle + 0.45)), int(end[1] - length * math.sin(angle + 0.45))),
    ]
    d.polygon(pts, fill=fill)


def fit_image(path: Path, box: tuple[int, int, int, int], cover: bool = False) -> Image.Image | None:
    if not path.exists():
        return None
    img = Image.open(path).convert("RGB")
    bw, bh = box[2] - box[0], box[3] - box[1]
    scale = max(bw / img.width, bh / img.height) if cover else min(bw / img.width, bh / img.height)
    nw, nh = max(1, int(img.width * scale)), max(1, int(img.height * scale))
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    if cover:
        left = max(0, (nw - bw) // 2)
        top = max(0, (nh - bh) // 2)
        img = img.crop((left, top, left + bw, top + bh))
    return img


def paste_image(base: Image.Image, path: Path, box: tuple[int, int, int, int], cover: bool = False, bg=WHITE) -> None:
    d = ImageDraw.Draw(base)
    img = fit_image(path, box, cover)
    if img is None:
        card(d, box, fill=(248, 241, 241), outline=RED)
        draw_text(d, (box[0] + 18, box[1] + 20), f"Missing asset:\n{path.name}", 24, RED, True, box[2] - box[0] - 36)
        return
    card(d, box, fill=bg, outline=(201, 220, 225), radius=20)
    x = box[0] + (box[2] - box[0] - img.width) // 2
    y = box[1] + (box[3] - box[1] - img.height) // 2
    base.paste(img, (x, y))
    d.rounded_rectangle(box, radius=20, outline=(201, 220, 225), width=2)


def new_slide(title: str, subtitle: str = "", dark: bool = False) -> Image.Image:
    bg = DEEP if dark else WHITE
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, H), fill=bg)
    d.rectangle((0, 0, 18, H), fill=TEAL if not dark else ICE)
    draw_text(d, (72, 50), title, 52, WHITE if dark else NAVY, True)
    if subtitle:
        draw_text(d, (76, 120), subtitle, 22, (188, 228, 235) if dark else MUTED, width=1500)
    return img


def footer(img: Image.Image, text: str, dark: bool = False) -> None:
    d = ImageDraw.Draw(img)
    y = H - 58
    line = (71, 93, 105) if dark else (182, 199, 204)
    d.line((64, y - 10, W - 64, y - 10), fill=line, width=2)
    draw_text(d, (72, y), text, 15, (164, 187, 196) if dark else MUTED, width=1700)


def save(img: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.resize((OUT_W, OUT_H), Image.Resampling.LANCZOS).save(path, quality=94)


def molecule(d: ImageDraw.ImageDraw, cx: int, cy: int, r: int) -> None:
    pts = []
    for i in range(8):
        a = math.pi * 2 * i / 8 + 0.2
        pts.append((int(cx + math.cos(a) * r), int(cy + math.sin(a) * r)))
    d.line(pts + [pts[0]], fill=ICE, width=5)
    for p in pts:
        d.ellipse((p[0] - 12, p[1] - 12, p[0] + 12, p[1] + 12), fill=(216, 244, 248), outline=WHITE, width=2)
    d.ellipse((cx - 38, cy - 38, cx + 38, cy + 38), fill=AMBER, outline=WHITE, width=4)
    draw_text(d, (cx, cy - 15), "CH4", 24, WHITE, True, anchor="ma")


def mini_logs(d: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, labels: list[tuple[str, list[float], tuple[int, int, int]]]) -> None:
    for idx, (label, vals, color) in enumerate(labels):
        lx = x + idx * (w + 18)
        d.rounded_rectangle((lx, y, lx + w, y + h), radius=12, fill=(250, 253, 253), outline=(199, 218, 224), width=2)
        d.line((lx + w // 2, y + 20, lx + w // 2, y + h - 20), fill=(218, 231, 235), width=2)
        pts = []
        for j, val in enumerate(vals):
            py = y + 32 + int(j * (h - 64) / max(1, len(vals) - 1))
            px = lx + 18 + int(max(0, min(1, val)) * (w - 36))
            pts.append((px, py))
        d.line(pts, fill=color, width=4, joint="curve")
        draw_text(d, (lx + 12, y + 8), label, 15, color, True)


def gauge(d: ImageDraw.ImageDraw, box: tuple[int, int, int, int], lo: float, hi: float, color: tuple[int, int, int]) -> None:
    x1, y1, x2, y2 = box
    d.rounded_rectangle(box, radius=8, fill=(229, 238, 241), outline=None)
    sx = x1 + int(lo * (x2 - x1))
    ex = x1 + int(hi * (x2 - x1))
    d.rounded_rectangle((sx, y1, ex, y2), radius=8, fill=color, outline=None)
    draw_text(d, (x1, y2 + 5), "0", 13, MUTED)
    draw_text(d, (x2 - 10, y2 + 5), "1", 13, MUTED)


def slide_01(root: Path, out: Path) -> None:
    assets = root / "references" / "presentation-revision-2026-06-11" / "gmail-2026-06-11"
    profile = root / "docs" / "project_blueprints" / "presentation_assets" / "rohan_profile_photo.jpg"
    img = new_slide("Gas Hydrate Occurrence and Saturation Prediction", "Alaska North Slope permafrost reservoirs using physics-constrained AI/ML")
    d = ImageDraw.Draw(img)
    draw_text(d, (78, 188), "Goal: combine approved well logs, NMR, core context, and public GIS without exposing runtime-only data.", 24, MUTED, width=820)
    for i, label in enumerate(["source-backed", "9 slides", "runtime-safe"]):
        colors = [TEAL, (217, 232, 236), (232, 221, 189)]
        fills = [WHITE, NAVY, NAVY]
        x = 78 + i * 210
        d.rounded_rectangle((x, 275, x + 178, 320), radius=12, fill=colors[i])
        draw_text(d, (x + 89, 286), label, 16, fills[i], True, anchor="ma")
    draw_text(d, (80, 380), "About me", 28, NAVY, True)
    paste_image(img, assets / "gmail_inline_07.png", (78, 430, 520, 870), cover=True)
    paste_image(img, assets / "gmail_inline_06.png", (555, 430, 820, 700), cover=True)
    paste_image(img, assets / "gmail_inline_05.png", (555, 725, 820, 870), cover=True)
    for label, y in [("drawing", 892), ("music", 722), ("World Cup", 892)]:
        draw_text(d, (label == "drawing" and 245 or 675, y), label, 18, MUTED, True, anchor="ma")
    for i, label in enumerate(["gym", "running", "swimming"]):
        x = 870 + i * 155
        d.rounded_rectangle((x, 764, x + 130, 820), radius=16, fill=PANEL)
        draw_text(d, (x + 65, 780), label, 18, NAVY, True, anchor="ma")
    paste_image(img, profile, (1180, 160, 1760, 900), cover=True)
    footer(img, "Personal images from 2026-06-11 Gmail instruction; public deck only.")
    save(img, out)


def slide_02(root: Path, out: Path) -> None:
    rev = root / "references" / "presentation-revision-2026-06-11" / "images"
    geo = root / "raw_data" / "geology" / "CNS_AUs" / "CNS_AUs.jpg"
    img = new_slide(
        "Methane Gas Hydrate: Water-Cage Crystal",
        "Source-backed visual definition first; North Slope context second.",
    )
    d = ImageDraw.Draw(img)

    def chem_width(text: str, size: int, bold: bool = False) -> int:
        total = 0
        for ch in text:
            if ch == ".":
                total += int(size * 0.42)
                continue
            f = font(max(10, int(size * 0.58)), bold) if ch.isdigit() else font(size, bold)
            total += int(d.textlength(ch, font=f))
        return total

    def chem_text(x: int, y: int, text: str, size: int, fill, bold: bool = False, anchor: str | None = None) -> None:
        if anchor == "ma":
            x -= chem_width(text, size, bold) // 2
        cursor = x
        for ch in text:
            if ch == ".":
                r = max(3, int(size * 0.11))
                cx = cursor + int(size * 0.22)
                cy = y + int(size * 0.52)
                d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill)
                cursor += int(size * 0.42)
                continue
            is_sub = ch.isdigit()
            f = font(max(10, int(size * 0.58)), bold) if is_sub else font(size, bold)
            yy = y + int(size * 0.45) if is_sub else y
            d.text((cursor, yy), ch, font=f, fill=fill)
            cursor += int(d.textlength(ch, font=f))

    # Source-backed SEM field as the primary visual anchor.
    sem_box = (70, 190, 820, 830)
    sem = fit_image(rev / "usgs_gas_hydrate_crystals_sem_public_domain.jpg", sem_box, cover=True)
    if sem is not None:
        img.paste(sem, sem_box[:2])
        overlay = Image.new("RGBA", (sem_box[2] - sem_box[0], sem_box[3] - sem_box[1]), (7, 30, 43, 0))
        od = ImageDraw.Draw(overlay)
        od.rectangle((0, 0, overlay.width, 190), fill=(7, 30, 43, 150))
        od.rectangle((0, overlay.height - 170, overlay.width, overlay.height), fill=(7, 30, 43, 165))
        img.paste(overlay.convert("RGB"), sem_box[:2], overlay)
    else:
        d.rectangle(sem_box, fill=PANEL)
    d.rectangle(sem_box, outline=(183, 202, 208), width=2)
    draw_text(d, (98, 220), "USGS SEM: gas hydrate crystals", 29, WHITE, True, width=650)
    draw_text(d, (100, 712), "What it is", 19, ICE, True)
    draw_text(
        d,
        (100, 744),
        "Ice-like crystalline solid: gas molecules held inside water cages.",
        23,
        WHITE,
        True,
        width=640,
    )

    # Processing-style clathrate symbol over the SEM field.
    cage_cx, cage_cy = 570, 505
    for radius, alpha_color in [(150, (232, 252, 255)), (106, (207, 242, 248))]:
        pts = []
        for i in range(12):
            a = math.pi * 2 * i / 12 + math.pi / 12
            pts.append((int(cage_cx + math.cos(a) * radius), int(cage_cy + math.sin(a) * radius)))
        d.line(pts + [pts[0]], fill=ICE, width=5)
        for px, py in pts:
            d.ellipse((px - 11, py - 11, px + 11, py + 11), fill=alpha_color, outline=WHITE, width=2)
    for angle in [0.0, math.pi * 2 / 3, math.pi * 4 / 3]:
        px = int(cage_cx + math.cos(angle) * 88)
        py = int(cage_cy + math.sin(angle) * 88)
        d.line((cage_cx, cage_cy, px, py), fill=(194, 236, 242), width=3)
    d.ellipse((cage_cx - 58, cage_cy - 58, cage_cx + 58, cage_cy + 58), fill=AMBER, outline=WHITE, width=5)
    chem_text(cage_cx, cage_cy - 22, "CH4", 39, WHITE, True, anchor="ma")
    chem_text(425, 690, "CH4 + nH2O -> CH4.nH2O", 28, WHITE, True)

    # Definition stream: source statements as code-like visual nodes, not cards.
    d.line((875, 225, 875, 820), fill=(205, 224, 229), width=3)
    for y, label, source, color in [
        (240, "water cages", "USGS FAQ", ICE),
        (360, "methane guest", "USGS primer", AMBER),
        (480, "clathrate solid", "NETL primer", TEAL),
    ]:
        d.ellipse((855, y - 14, 895, y + 26), fill=color, outline=WHITE, width=3)
        draw_text(d, (920, y - 18), label, 24, NAVY, True)
        draw_text(d, (922, y + 22), source, 17, MUTED, True)
    draw_text(d, (890, 610), "Definition anchor", 18, MUTED, True)
    chem_text(890, 646, "CH4 + nH2O", 25, NAVY, True)
    chem_text(890, 688, "-> CH4.nH2O", 25, NAVY, True)
    draw_text(d, (890, 750), "methane hydrate", 18, TEAL, True)

    # P-T / GHSZ diagram with correct symbols.
    plot = (1195, 205, 1765, 565)
    draw_text(d, (1195, 178), "P-T stability gate", 28, NAVY, True)
    d.line((plot[0], plot[3], plot[2], plot[3]), fill=MUTED, width=4)
    d.line((plot[0], plot[3], plot[0], plot[1]), fill=MUTED, width=4)
    arrow(d, (plot[0], plot[3]), (plot[2] + 28, plot[3]), MUTED, 4)
    arrow(d, (plot[0], plot[3]), (plot[0], plot[1] - 28), MUTED, 4)
    draw_text(d, (plot[2] + 44, plot[3] - 12), "T", 27, MUTED, True)
    draw_text(d, (plot[0] - 18, plot[1] - 62), "P", 27, MUTED, True)
    stable = [(plot[0], plot[3]), (plot[0], plot[1] + 35), (plot[0] + 205, plot[1] + 48), (plot[0] + 365, plot[1] + 150), (plot[0] + 468, plot[3])]
    d.polygon(stable, fill=(207, 239, 244))
    boundary = [(plot[0] + 34, plot[3] - 36), (plot[0] + 132, plot[3] - 130), (plot[0] + 245, plot[3] - 205), (plot[0] + 375, plot[3] - 245), (plot[2] - 10, plot[3] - 280)]
    d.line(boundary, fill=TEAL, width=7)
    geothermal = [(plot[0] + 85, plot[3] - 4), (plot[0] + 240, plot[3] - 105), (plot[0] + 398, plot[3] - 222), (plot[2] - 45, plot[3] - 285)]
    d.line(geothermal, fill=RED, width=5)
    draw_text(d, (plot[0] + 165, plot[1] + 105), "GHSZ", 32, TEAL, True)
    draw_text(d, (plot[0] + 126, plot[1] + 145), "gas hydrate stability zone", 17, TEAL, True)
    draw_text(d, (plot[0] + 368, plot[3] - 184), "geotherm", 18, RED, True)
    draw_text(d, (plot[0] + 338, plot[3] + 18), "too warm / unstable", 16, MUTED)
    draw_text(d, (1210, 607), "Stability is necessary, not proof.", 24, RED, True, width=525)
    draw_text(d, (1210, 648), "P-T screens possible hydrate; logs/core still confirm occurrence.", 19, INK, width=545)

    # North Slope context as a low-profile strip instead of a competing slide.
    d.line((1195, 725, 1765, 725), fill=(200, 219, 224), width=2)
    paste_image(img, geo, (1195, 765, 1365, 935), cover=True, bg=WHITE)
    structural = fit_image(rev / "project_streamlit_structural_explorer_v2.png", (1390, 765, 1765, 935), cover=True)
    if structural is not None:
        img.paste(structural, (1390, 765))
        d.rectangle((1390, 765, 1765, 935), outline=(201, 220, 225), width=2)
    draw_text(d, (1195, 695), "North Slope context after definition", 20, NAVY, True)
    for i, (color, label) in enumerate([(GREEN, "reservoir sand"), (PURPLE, "source interval"), (SHALE, "basement relief"), (TEAL, "runtime logs decide")]):
        x = 1195 + i * 175
        d.rounded_rectangle((x, 955, x + 24, 978), radius=5, fill=color)
        draw_text(d, (x + 32, 952), label, 15, MUTED, True)

    footer(
        img,
        "Sources: USGS FAQ 'What are gas hydrates?'; USGS Gas Hydrates Primer; NETL Methane Hydrate Primer; USGS OF 96-272 P-T boundary; USGS SEM image; project Streamlit assets.",
    )
    save(img, out)


PARAMS = [
    ("GR", "Gamma ray", "natural radioactivity", "clean sand screen", (0.10, 0.38), AMBER),
    ("Rt", "Deep resistivity", "electrical resistance", "hydrate support only with other logs", (0.45, 0.90), RED),
    ("RHOB", "Bulk density", "mass per volume", "density porosity and elastic input", (0.35, 0.72), GREEN),
    ("\u03c6_D", "Density porosity", "pore-volume estimate", "reservoir capacity", (0.30, 0.70), GREEN),
    ("\u03c6_NMR", "NMR porosity", "mobile-fluid pore signal", "preferred saturation support", (0.22, 0.58), BLUE),
    ("Vp | Vs", "Sonic velocity", "P and S wave speed", "stiffness and gas separation", (0.45, 0.82), PURPLE),
    ("AI", "Acoustic impedance", "\u03c1_b x Vp", "layer contrast and stiffness", (0.42, 0.78), TEAL),
    ("CAL", "Caliper/DCAL", "borehole diameter", "QC gate for bad hole", (0.00, 0.18), RED),
    ("P-T", "Pressure-temp", "stability context", "necessary, not proof", (0.40, 0.74), NAVY),
]


def slide_03(root: Path, out: Path) -> None:
    img = new_slide("Science-to-ML Parameter Ladder", "The model follows geoscience logic before it sees feature weights.")
    d = ImageDraw.Draw(img)
    tiers = [
        ("1", "Stability context", "Can hydrate exist here?", "depth | pressure | temperature | permafrost | overburden", "mask or context feature", TEAL),
        ("2", "Reservoir quality", "Can the rock host pore-filling hydrate?", "GR | porosity | density | lithology | caliper QC | core quality", "sand/reservoir gate", GREEN),
        ("3", "Hydrate response", "Do logs behave like hydrate-bearing sediment?", "Rt | Vp | Vs | Vp/Vs | AI | lambda-rho | mu-rho | NMR/core targets", "model evidence block", AMBER),
    ]
    for i, (num, title, question, params, role, color) in enumerate(tiers):
        y = 190 + i * 225
        card(d, (92, y, 1768, y + 166), fill=WHITE, outline=(198, 218, 224), radius=24)
        d.ellipse((124, y + 39, 212, y + 127), fill=color, outline=WHITE, width=4)
        draw_text(d, (168, y + 62), num, 34, WHITE, True, anchor="ma")
        draw_text(d, (248, y + 26), title, 32, NAVY, True)
        draw_text(d, (248, y + 78), question, 22, INK, True, width=520)
        draw_text(d, (880, y + 32), params, 24, color, True, width=720)
        d.rounded_rectangle((1330, y + 98, 1718, y + 136), radius=12, fill=(235, 247, 249), outline=(188, 215, 221), width=2)
        draw_text(d, (1524, y + 106), role, 18, NAVY, True, anchor="ma")
        if i < len(tiers) - 1:
            arrow(d, (930, y + 172), (930, y + 216), fill=TEAL, width=5)

    draw_text(d, (105, 870), "Repeated grammar", 24, NAVY, True)
    draw_text(
        d,
        (105, 910),
        "parameter -> physical reason -> hydrate signal -> false positives -> ML role",
        25,
        TEAL,
        True,
        width=940,
    )
    card(d, (1210, 850, 1765, 966), fill=(249, 244, 244), outline=RED)
    draw_text(d, (1240, 875), "Target leakage lock", 23, RED, True)
    draw_text(d, (1240, 914), "S_h, Sgh, NMR_SAT, phase labels, and final rankings score models; they do not enter predictors.", 17, INK, width=470)
    footer(img, "Sources: SCIENCE_TO_ML_LOGIC_LADDER; ML_PIPELINE_BASELINE_SOURCE_LEDGER; WELL_LOG_REQUIREMENTS_MAP; Chong et al. 2022.")
    save(img, out)


def slide_04(root: Path, out: Path) -> None:
    img = new_slide("ML Architecture: Raw Headers to Validated Outputs", "A leakage-safe pipeline that turns source-backed physics into two model heads.", dark=True)
    d = ImageDraw.Draw(img)
    stages = [
        ("Raw headers", "preserve mnemonics\nunits and roles", TEAL),
        ("Unit map", "feet/meters\ng/cc or kg/m3\nvelocity/slowness", BLUE),
        ("Depth align", "logs, NMR,\ncore, labels", GREEN),
        ("QC gates", "caliper status\nmissingness\noutliers", RED),
        ("Features", "Rt log\nVp/Vs, AI\nlambda-rho\nmu-rho", AMBER),
        ("Context", "stability\nsand gate\noverburden", PURPLE),
        ("Leakage lock", "S_h/Sgh/NMR_SAT\nlabels only", RED),
        ("Well split", "train-only prep\ncomplete-well holdout", BLUE),
    ]
    x = 72
    y = 200
    box_w = 210
    for i, (title, body, color) in enumerate(stages):
        bx = x + i * 225
        card(d, (bx, y, bx + box_w, y + 128), fill=(18, 56, 70), outline=(76, 121, 136), radius=18)
        d.rounded_rectangle((bx, y, bx + box_w, y + 12), radius=6, fill=color)
        draw_text(d, (bx + 18, y + 28), title, 23, ICE if color != RED else WHITE, True, width=170)
        draw_text(d, (bx + 18, y + 70), body, 16, (210, 231, 236), width=170)
        if i < len(stages) - 1:
            arrow(d, (bx + box_w + 6, y + 64), (bx + 222, y + 64), fill=(118, 153, 164), width=4)

    branch_y = 520
    card(d, (180, branch_y, 690, branch_y + 190), fill=(17, 58, 64), outline=(75, 129, 137))
    draw_text(d, (220, branch_y + 30), "Occurrence classifier", 31, ICE, True)
    draw_text(d, (220, branch_y + 84), "hydrate-supportive | no hydrate | mimic risk | expert review", 21, WHITE, width=410)
    draw_text(d, (220, branch_y + 138), "Output: probability + reason flags", 20, AMBER, True)

    card(d, (760, branch_y, 1270, branch_y + 190), fill=(17, 58, 64), outline=(75, 129, 137))
    draw_text(d, (800, branch_y + 30), "Saturation regressor", 31, ICE, True)
    draw_text(d, (800, branch_y + 84), "continuous S_h/Sgh estimate where context and labels allow", 21, WHITE, width=410)
    draw_text(d, (800, branch_y + 138), "Output: saturation + uncertainty", 20, AMBER, True)

    card(d, (1340, branch_y, 1760, branch_y + 190), fill=(34, 54, 69), outline=(91, 125, 137))
    draw_text(d, (1374, branch_y + 30), "Validation", 31, ICE, True)
    draw_text(d, (1374, branch_y + 84), "complete wells, calibration, residuals, QC/mimic review", 21, WHITE, width=335)
    draw_text(d, (1374, branch_y + 138), "No fake metrics", 20, RED, True)
    arrow(d, (950, 328), (435, branch_y), fill=(118, 153, 164), width=4)
    arrow(d, (950, 328), (1015, branch_y), fill=(118, 153, 164), width=4)
    arrow(d, (1270, branch_y + 150), (1340, branch_y + 150), fill=(118, 153, 164), width=4)

    d.rounded_rectangle((245, 850, 1675, 904), radius=14, fill=RED)
    draw_text(d, (960, 862), "Guardrail: the model learns from measured and derived features; target-derived columns stay below the leakage barrier.", 24, WHITE, True, anchor="ma")
    footer(img, "Sources: ML_PIPELINE_BASELINE_SOURCE_LEDGER; Chong et al. 2022; Chong et al. 2024; WELL_LOG_REQUIREMENTS_MAP; runtime skeleton.", dark=True)
    save(img, out)


def slide_05(root: Path, out: Path) -> None:
    img = new_slide("Parameter Movements: Hydrate and Its Mimics", "The useful signal is how a hydrate pocket changes the local log response inside its setting.")
    d = ImageDraw.Draw(img)
    panels = [
        ("Hydrate in clean sand", "Rt up + Vp/Vs support + Vs/mu-rho up", TEAL, [("Rt", [0.34, 0.72, 0.86, 0.80, 0.38], RED), ("Vs", [0.42, 0.62, 0.76, 0.70, 0.45], PURPLE), ("NMR", [0.62, 0.35, 0.25, 0.32, 0.58], BLUE)]),
        ("Water sand", "low GR + porosity, but Rt and stiffness moderate", GREEN, [("GR", [0.25, 0.22, 0.26, 0.18, 0.24], AMBER), ("phi", [0.58, 0.62, 0.60, 0.66, 0.61], GREEN), ("Rt", [0.25, 0.30, 0.28, 0.32, 0.27], RED)]),
        ("Free gas", "Rt can rise while Vp softens and Vs does not stiffen", RED, [("Rt", [0.40, 0.68, 0.76, 0.65, 0.42], RED), ("Vp", [0.62, 0.28, 0.24, 0.32, 0.58], BLUE), ("Vs", [0.48, 0.50, 0.52, 0.49, 0.51], PURPLE)]),
        ("Ice / frozen sediment", "Rt very high and velocities high; needs depth/P-T context", PURPLE, [("Rt", [0.52, 0.86, 0.92, 0.84, 0.60], RED), ("Vp", [0.58, 0.76, 0.82, 0.78, 0.62], BLUE), ("Vs", [0.55, 0.74, 0.80, 0.77, 0.60], PURPLE)]),
        ("Tight / cemented rock", "resistive and stiff but pore volume is low", SHALE, [("Rt", [0.45, 0.78, 0.82, 0.75, 0.48], RED), ("Vp", [0.55, 0.80, 0.84, 0.78, 0.57], BLUE), ("phi", [0.42, 0.20, 0.16, 0.22, 0.40], GREEN)]),
        ("Shale / bad hole", "high GR or washout can corrupt the feature table", AMBER, [("GR", [0.70, 0.78, 0.82, 0.74, 0.76], AMBER), ("CAL", [0.25, 0.30, 0.90, 0.88, 0.32], RED), ("RHOB", [0.54, 0.50, 0.22, 0.24, 0.48], GREEN)]),
    ]
    for i, (title, subtitle, color, curves) in enumerate(panels):
        row, col = divmod(i, 3)
        x = 80 + col * 600
        y = 170 + row * 330
        card(d, (x, y, x + 520, y + 260), fill=WHITE)
        draw_text(d, (x + 24, y + 24), title, 26, color, True)
        draw_text(d, (x + 24, y + 62), subtitle, 17, MUTED, width=450)
        d.rounded_rectangle((x + 24, y + 102, x + 474, y + 124), radius=10, fill=(229, 238, 241))
        d.rounded_rectangle((x + 150, y + 102, x + 375, y + 124), radius=10, fill=(198, 231, 221))
        draw_text(d, (x + 24, y + 132), "normalized range 0-1", 14, MUTED)
        mini_logs(d, x + 28, y + 158, 132, 82, curves)
    draw_text(d, (960, 875), "Guardrail: classify hydrate-supportive, mimic risk, poor quality, or out-of-domain. Do not declare hydrate from one curve.", 23, NAVY, True, anchor="ma")
    footer(img, "Sources: ML_PIPELINE_BASELINE_SOURCE_LEDGER; SCIENCE_TO_ML_LOGIC_LADDER; Lee and Collett 2011; Haines et al. 2022; Aung et al. 2026.")
    save(img, out)


def slide_06(root: Path, out: Path) -> None:
    img = new_slide("Feature Equations and Screening Envelopes", "Derived features help separate rigidity, gas response, and false positives.")
    d = ImageDraw.Draw(img)
    card(d, (85, 178, 655, 755), fill=WHITE)
    draw_text(d, (120, 208), "Unit-safe equations", 30, NAVY, True)
    eqs = [
        ("Vp", "1 / DT"),
        ("Vs", "1 / DTS"),
        ("AI", "rho * Vp"),
        ("G or mu", "rho * Vs^2"),
        ("K", "rho * (Vp^2 - 4/3 Vs^2)"),
        ("E", "9KG / (3K + G)"),
        ("nu", "(3K - 2G) / 2(3K + G)"),
        ("lambda-rho", "(K - 2/3G) * rho"),
        ("mu-rho", "G * rho"),
    ]
    for i, (lhs, rhs) in enumerate(eqs):
        y = 268 + i * 48
        d.rounded_rectangle((122, y, 282, y + 34), radius=9, fill=(234, 247, 249), outline=(184, 218, 224), width=2)
        draw_text(d, (202, y + 7), lhs, 18, TEAL if i < 5 else PURPLE, True, anchor="ma")
        draw_text(d, (310, y + 6), rhs, 18, INK, True, width=295)

    card(d, (720, 178, 1245, 755), fill=WHITE)
    draw_text(d, (755, 208), "Hydrate screening envelopes", 30, NAVY, True)
    ranges = [
        ("Rt", "10-100+ ohm-m", RED),
        ("Vp", "2.5-4.0 km/s", BLUE),
        ("Vs", "1.0-2.5 km/s", PURPLE),
        ("Vp/Vs", "1.6-2.4 broad", TEAL),
        ("mu-rho", "10-55 GPa*g/cc", GREEN),
        ("lambda-rho", "12-55 GPa*g/cc", AMBER),
        ("phi", "0.20-0.35", GREEN),
    ]
    for i, (name, rng, color) in enumerate(ranges):
        y = 280 + i * 60
        draw_text(d, (765, y), name, 22, color, True)
        d.rounded_rectangle((930, y + 4, 1185, y + 26), radius=8, fill=(229, 238, 241), outline=None)
        d.rounded_rectangle((980, y + 4, 1135, y + 26), radius=8, fill=color, outline=None)
        draw_text(d, (765, y + 30), rng, 15, MUTED, width=380)

    card(d, (1315, 178, 1815, 755), fill=WHITE)
    draw_text(d, (1350, 208), "How ML uses them", 30, NAVY, True)
    uses = [
        ("Rigidity", "Vs, G, and mu-rho separate hydrate-like frame stiffening from free gas."),
        ("Mimics", "Ice, cement, carbonate, tight rock, and compaction can also be stiff."),
        ("Crossplots", "Broad ranges screen; tighter Vp/Vs 1.4-1.6 is only a hypothesis."),
        ("Provenance", "Derived features cannot be cleaner than their source curves."),
    ]
    for i, (title, body) in enumerate(uses):
        y = 286 + i * 100
        draw_text(d, (1350, y), title, 22, TEAL if i != 1 else RED, True)
        draw_text(d, (1350, y + 32), body, 17, INK, width=395)

    d.rounded_rectangle((210, 850, 1710, 908), radius=16, fill=(249, 244, 244), outline=AMBER, width=3)
    draw_text(d, (960, 864), "Ranges guide QC and crossplots. Final cutoffs must be calibrated against approved Sgh/NMR/core labels.", 24, NAVY, True, anchor="ma")
    footer(img, "Sources: SCIENCE_TO_ML_LOGIC_LADDER; ML_PIPELINE_BASELINE_SOURCE_LEDGER; Cook and Waite 2018; Haines et al. 2022.")
    save(img, out)


def slide_07(root: Path, out: Path) -> None:
    rev = root / "references" / "presentation-revision-2026-06-11" / "images"
    geo = root / "raw_data" / "geology" / "CNS_AUs" / "CNS_AUs.jpg"
    img = new_slide("3D Map and Well Context", "Regional maps explain setting; approved runtime logs still make the hydrate call.")
    d = ImageDraw.Draw(img)
    paste_image(img, geo, (80, 180, 510, 650), cover=True)
    draw_text(d, (105, 670), "2D North Slope public context", 22, NAVY, True, width=380)
    paste_image(img, rev / "project_streamlit_structural_explorer_v2.png", (560, 180, 1250, 650), cover=True)
    draw_text(d, (590, 670), "Current Streamlit structural explorer", 22, NAVY, True, width=620)
    card(d, (1300, 180, 1800, 650), fill=WHITE)
    draw_text(d, (1330, 210), "Legend logic", 30, NAVY, True)
    items = [
        (TEAL, "Public wells and boundaries", "orient the regional question"),
        (PURPLE, "Shublik/source interval", "gas charge and migration context"),
        (AMBER, "Basement/structural relief", "controls pathways and traps"),
        (GREEN, "Reservoir sands", "where logs test pore-scale evidence"),
        (RED, "Runtime boundary", "approved logs stay outside public slides"),
    ]
    for i, (color, label, body) in enumerate(items):
        y = 275 + i * 67
        d.rounded_rectangle((1335, y, 1380, y + 32), radius=8, fill=color)
        draw_text(d, (1400, y - 2), label, 20, color, True)
        draw_text(d, (1400, y + 24), body, 16, MUTED, width=330)
    arrow(d, (275, 760), (820, 760), fill=TEAL, width=5)
    arrow(d, (820, 760), (1480, 760), fill=TEAL, width=5)
    for x, label in [(180, "public map"), (690, "structural context"), (1330, "runtime log review")]:
        d.rounded_rectangle((x, 790, x + 300, 850), radius=16, fill=PANEL)
        draw_text(d, (x + 150, 807), label, 22, NAVY, True, anchor="ma")
    footer(img, "Sources: project Streamlit structural explorer; public CNS assessment-unit image; project source files and runtime boundary docs.")
    save(img, out)


def slide_08(root: Path, out: Path) -> None:
    assets = root / "docs" / "project_blueprints" / "presentation_assets"
    img = new_slide("Results Plan: Separate the Outputs", "The deliverable should show decision evidence, not fake accuracy metrics.")
    d = ImageDraw.Draw(img)
    paste_image(img, assets / "synthetic_well_log_panel.png", (70, 180, 650, 540), cover=True)
    draw_text(d, (110, 570), "Planned approved-data log panel", 22, NAVY, True)
    paste_image(img, assets / "sweet_spot_ranking.png", (90, 650, 650, 850), cover=True)
    outputs = [
        ("Occurrence probability", "classifier output; not saturation or proof", TEAL),
        ("Saturation estimate", "continuous S_h/Sgh where labels and context support it", GREEN),
        ("Uncertainty", "model confidence plus feature and target confidence", BLUE),
        ("QC status", "caliper, missingness, depth match, outliers", RED),
        ("Mimic flags", "gas, ice, tight rock, shale, bad hole, missing feature", AMBER),
        ("Producibility context", "NMR/core/permeability review; not occurrence label", PURPLE),
    ]
    for i, (title, body, color) in enumerate(outputs):
        x = 760 + (i % 2) * 505
        y = 180 + (i // 2) * 178
        card(d, (x, y, x + 455, y + 128), fill=WHITE)
        d.rounded_rectangle((x + 24, y + 36, x + 82, y + 94), radius=16, fill=(235, 247, 249), outline=(186, 219, 225), width=2)
        draw_text(d, (x + 53, y + 50), str(i + 1), 24, color, True, anchor="ma")
        draw_text(d, (x + 110, y + 26), title, 24, color, True)
        draw_text(d, (x + 110, y + 64), body, 17, INK, width=300)

    card(d, (760, 720, 1720, 870), fill=(249, 244, 244), outline=AMBER)
    draw_text(d, (800, 746), "Discussion lens", 25, NAVY, True)
    draw_text(
        d,
        (800, 790),
        "For every interval: what evidence agreed, what looked like a mimic, which QC checks passed, and what data remain unresolved?",
        18,
        INK,
        width=850,
    )
    footer(img, "Sources: ML_PIPELINE_BASELINE_SOURCE_LEDGER; runtime skeleton; Chong et al. 2024; Yoneda et al. 2026; public/synthetic scaffold figures.")
    save(img, out)


def slide_09(root: Path, out: Path) -> None:
    img = new_slide("Conclusion", "The workflow is defensible because the science controls the ML, not the other way around.")
    d = ImageDraw.Draw(img)
    center = (960, 465)
    d.ellipse((700, 245, 1220, 690), fill=(231, 243, 245), outline=(158, 205, 212), width=4)
    draw_text(d, (960, 344), "Science-to-ML ladder", 38, NAVY, True, anchor="ma")
    draw_text(d, (735, 412), "existence context -> host rock -> hydrate response -> leakage-safe model -> review output", 22, MUTED, width=450, align="center")
    nodes = [
        ((185, 245), "Science", "hydrate system defined before parameters", TEAL),
        ((1375, 245), "ML", "separate classifier and saturation regressor", GREEN),
        ((185, 655), "Guardrails", "mimics, bad hole, and target leakage stay visible", AMBER),
        ((1375, 655), "Next", "recover workbook, targets, and approved validation", RED),
    ]
    for (x, y), title, body, color in nodes:
        card(d, (x, y, x + 360, y + 145), fill=WHITE)
        d.ellipse((x + 22, y + 38, x + 80, y + 96), fill=(235, 247, 249), outline=(186, 219, 225), width=2)
        draw_text(d, (x + 51, y + 51), title[0], 24, color, True, anchor="ma")
        draw_text(d, (x + 105, y + 32), title, 25, color, True)
        draw_text(d, (x + 105, y + 70), body, 18, INK, width=220)
        arrow(d, (x + (360 if x < center[0] else 0), y + 68), (center[0] + (-240 if x < center[0] else 240), center[1]), fill=(148, 171, 180), width=4)
    d.ellipse((700, 245, 1220, 690), fill=(231, 243, 245), outline=(158, 205, 212), width=4)
    draw_text(d, (960, 344), "Science-to-ML ladder", 38, NAVY, True, anchor="ma")
    draw_text(d, (735, 412), "existence context -> host rock -> hydrate response -> leakage-safe model -> review output", 22, MUTED, width=450, align="center")
    card(d, (205, 785, 1715, 875), fill=(249, 244, 244), outline=TEAL)
    draw_text(d, (245, 807), "Final message: predict occurrence and saturation only when source role, physical response, target provenance, validation, and uncertainty all stay traceable.", 22, NAVY, True, width=1420, align="center")
    footer(img, "Sources: USGS/DOE/NETL; Chong et al. 2022; Aung et al. 2026; Yoneda et al. 2026; ML pipeline baseline source ledger.")
    save(img, out)


def _slide_02_final(root: Path, out: Path) -> None:
    rev = root / "references" / "presentation-revision-2026-06-11" / "images"
    geo = root / "raw_data" / "geology" / "CNS_AUs" / "CNS_AUs.jpg"
    img = new_slide(
        "What Are Methane Hydrates?",
        "Methane trapped in water cages; North Slope hydrate is a pressure-temperature, reservoir, and log-evidence problem.",
    )
    d = ImageDraw.Draw(img)

    # Source visual plus a clean clathrate sketch.
    sem_box = (72, 180, 675, 695)
    sem = fit_image(rev / "usgs_gas_hydrate_crystals_sem_public_domain.jpg", sem_box, cover=True)
    if sem:
        img.paste(sem, sem_box[:2])
        overlay = Image.new("RGBA", (sem_box[2] - sem_box[0], sem_box[3] - sem_box[1]), (7, 30, 43, 0))
        od = ImageDraw.Draw(overlay)
        od.rectangle((0, 0, overlay.width, 130), fill=(7, 30, 43, 155))
        od.rectangle((0, overlay.height - 120, overlay.width, overlay.height), fill=(7, 30, 43, 170))
        img.paste(overlay.convert("RGB"), sem_box[:2], overlay)
    else:
        d.rectangle(sem_box, fill=PANEL)
    d.rectangle(sem_box, outline=(183, 202, 208), width=2)
    draw_text(d, (100, 210), "Actual hydrate crystals", 29, WHITE, True)
    draw_text(d, (100, 620), "Ice-like solid: CH4 held inside H2O cages", 24, WHITE, True, width=520)

    cx, cy = 470, 425
    for radius, color in [(138, ICE), (93, (190, 235, 242))]:
        pts = []
        for i in range(12):
            a = math.pi * 2 * i / 12 + math.pi / 12
            pts.append((int(cx + math.cos(a) * radius), int(cy + math.sin(a) * radius)))
        d.line(pts + [pts[0]], fill=color, width=5)
        for px, py in pts:
            d.ellipse((px - 10, py - 10, px + 10, py + 10), fill=(230, 252, 255), outline=WHITE, width=2)
    d.ellipse((cx - 55, cy - 55, cx + 55, cy + 55), fill=AMBER, outline=WHITE, width=5)
    draw_text(d, (cx, cy - 18), "CH4", 42, WHITE, True, anchor="ma")
    draw_text(d, (710, 198), "Definition", 25, NAVY, True)
    definition = [
        ("water lattice", "H2O molecules form cage-like crystals", ICE),
        ("methane guest", "CH4 occupies the cage", AMBER),
        ("hydrate solid", "stable only under the right P-T conditions", TEAL),
    ]
    for i, (label, body, color) in enumerate(definition):
        y = 250 + i * 98
        d.ellipse((718, y, 762, y + 44), fill=color, outline=WHITE, width=3)
        draw_text(d, (788, y - 2), label, 23, NAVY, True)
        draw_text(d, (788, y + 35), body, 17, INK, width=390)
    draw_text(d, (718, 575), "Conceptual reaction", 17, MUTED, True)
    draw_text(d, (718, 615), "CH4 + nH2O -> CH4·nH2O", 30, TEAL, True)

    # Stability diagram with the current North Slope public-screen assumptions.
    plot = (1160, 188, 1778, 565)
    draw_text(d, (1160, 158), "Stability diagram", 28, NAVY, True)
    d.line((plot[0], plot[3], plot[2], plot[3]), fill=MUTED, width=4)
    d.line((plot[0], plot[3], plot[0], plot[1]), fill=MUTED, width=4)
    arrow(d, (plot[0], plot[3]), (plot[2] + 28, plot[3]), MUTED, 4)
    arrow(d, (plot[0], plot[3]), (plot[0], plot[1] - 28), MUTED, 4)
    draw_text(d, (plot[2] + 40, plot[3] - 10), "T", 26, MUTED, True)
    draw_text(d, (plot[0] - 18, plot[1] - 62), "P", 26, MUTED, True)
    stable = [
        (plot[0], plot[3]),
        (plot[0], plot[1] + 48),
        (plot[0] + 260, plot[1] + 60),
        (plot[0] + 444, plot[1] + 145),
        (plot[0] + 540, plot[3]),
    ]
    d.polygon(stable, fill=(207, 239, 244))
    boundary = [
        (plot[0] + 35, plot[3] - 45),
        (plot[0] + 150, plot[3] - 145),
        (plot[0] + 285, plot[3] - 225),
        (plot[0] + 440, plot[3] - 270),
        (plot[2] - 12, plot[3] - 300),
    ]
    d.line(boundary, fill=TEAL, width=7)
    geotherm = [
        (plot[0] + 110, plot[3] - 5),
        (plot[0] + 275, plot[3] - 110),
        (plot[0] + 445, plot[3] - 235),
        (plot[2] - 38, plot[3] - 315),
    ]
    d.line(geotherm, fill=RED, width=5)
    draw_text(d, (plot[0] + 212, plot[1] + 112), "GHSZ", 34, TEAL, True)
    draw_text(d, (plot[0] + 165, plot[1] + 152), "gas hydrate stability zone", 17, TEAL, True)
    draw_text(d, (plot[0] + 410, plot[3] - 205), "geotherm", 18, RED, True)
    draw_text(d, (plot[0] + 352, plot[3] + 22), "too warm / unstable", 16, MUTED)

    assumptions = [
        ("100% CH4 + 5 ppt", "public baseline phase curve"),
        ("hydrostatic P", "first-pass pressure model"),
        ("G10015 + GGD223", "temperature and permafrost controls"),
        ("stability only", "necessary, not proof"),
    ]
    for i, (title, body) in enumerate(assumptions):
        x = 1160 + (i % 2) * 310
        y = 610 + (i // 2) * 86
        card(d, (x, y, x + 280, y + 62), fill=(247, 252, 253), outline=(198, 218, 224), radius=15)
        draw_text(d, (x + 18, y + 11), title, 18, TEAL if i != 3 else RED, True)
        draw_text(d, (x + 18, y + 37), body, 14, INK, width=238)

    # North Slope context strip: target habit and map context.
    paste_image(img, geo, (720, 755, 925, 960), cover=True, bg=WHITE)
    structural = fit_image(rev / "project_streamlit_structural_explorer_v2.png", (955, 755, 1245, 960), cover=True)
    if structural:
        img.paste(structural, (955, 755))
        d.rectangle((955, 755, 1245, 960), outline=(201, 220, 225), width=2)
    card(d, (1280, 755, 1780, 960), fill=(249, 244, 244), outline=AMBER, radius=20)
    draw_text(d, (1312, 782), "North Slope project assumption", 22, NAVY, True)
    draw_text(
        d,
        (1312, 822),
        "Main target is pore-filling methane hydrate in sand-rich permafrost reservoirs. Logs/core define occurrence and saturation; maps only frame the setting.",
        18,
        INK,
        width=425,
    )
    footer(img, "Sources: USGS gas hydrate FAQ and SEM image; NETL methane hydrate primer; USGS SIR 2008-5175 phase-curve method; project stability calculation plan.")
    save(img, out)


def _slide_03_final(root: Path, out: Path) -> None:
    img = new_slide(
        "Parameters: Well-Log Scaffold",
        "Symbols are shown with plain names, roles, and caveats so the final deck reads like science, not a spreadsheet.",
    )
    d = ImageDraw.Draw(img)
    columns = [
        (
            "1. Stability context",
            "Can hydrate exist here?",
            TEAL,
            [
                ("z", "Depth", "P-T position", "datum and units"),
                ("P", "Pressure", "phase input", "hydrostatic assumption"),
                ("T", "Temperature", "phase input", "profile extrapolation"),
                ("PF", "Permafrost", "thermal seal context", "point controls"),
            ],
        ),
        (
            "2. Reservoir quality",
            "Can the rock host it?",
            GREEN,
            [
                ("GR", "Gamma ray", "clean-sand gate", "radioactive minerals"),
                ("φD", "Density porosity", "pore volume", "mineral mix, washout"),
                ("ρb", "Bulk density", "porosity and AI", "shale, compaction"),
                ("CAL", "Caliper", "bad-hole QC", "not hydrate evidence"),
            ],
        ),
        (
            "3. Hydrate response",
            "Do logs agree?",
            AMBER,
            [
                ("Rt", "Deep resistivity", "electrical support", "gas, ice, tight rock"),
                ("Vp", "P-wave velocity", "stiffness support", "cement, lithology"),
                ("Vs", "S-wave velocity", "rigidity support", "missing shear sonic"),
                ("φNMR", "NMR porosity", "mobile-fluid check", "processing settings"),
            ],
        ),
    ]
    for c, (title, question, color, rows) in enumerate(columns):
        x = 80 + c * 600
        card(d, (x, 172, x + 540, 760), fill=WHITE, outline=(195, 216, 223), radius=24)
        d.rounded_rectangle((x, 172, x + 540, 224), radius=20, fill=color)
        draw_text(d, (x + 28, 187), title, 24, WHITE, True)
        draw_text(d, (x + 28, 246), question, 22, NAVY, True, width=470)
        for i, (sym, name, role, caveat) in enumerate(rows):
            y = 300 + i * 102
            d.rounded_rectangle((x + 28, y, x + 128, y + 74), radius=18, fill=(235, 247, 249), outline=(184, 218, 224), width=2)
            draw_text(d, (x + 78, y + 20), sym, 27, color, True, anchor="ma")
            draw_text(d, (x + 154, y + 2), name, 21, NAVY, True)
            draw_text(d, (x + 154, y + 32), role, 16, INK, width=210)
            draw_text(d, (x + 365, y + 32), caveat, 15, RED if "not" in caveat or "gas" in caveat else MUTED, width=140)
            if i < len(rows) - 1:
                d.line((x + 78, y + 75, x + 78, y + 92), fill=(202, 222, 227), width=3)

    # Derived and target fields sit below the tiered scaffold.
    card(d, (80, 805, 1145, 938), fill=(247, 252, 253), outline=(198, 218, 224), radius=22)
    draw_text(d, (112, 830), "Derived physics features", 23, NAVY, True)
    derived = [("Vp/Vs", "gas and stiffness separation"), ("AI", "ρbVp impedance"), ("μρ", "rigidity"), ("λρ", "incompressibility")]
    for i, (sym, body) in enumerate(derived):
        x = 112 + i * 250
        d.rounded_rectangle((x, 878, x + 210, 916), radius=12, fill=PANEL)
        draw_text(d, (x + 14, 887), sym, 18, TEAL if i < 2 else PURPLE, True)
        draw_text(d, (x + 84, 890), body, 13, INK, width=112)
    card(d, (1190, 805, 1785, 938), fill=(249, 244, 244), outline=RED, radius=22)
    draw_text(d, (1222, 830), "Locked target fields", 23, RED, True)
    draw_text(
        d,
        (1222, 874),
        "Sh, Sgh, NMR saturation, hydrate saturation, phase labels, and final rankings are labels or outputs. Keep them out of predictors.",
        17,
        INK,
        width=520,
    )
    footer(img, "Sources: well-log requirements map; science-to-ML ladder; ML baseline source ledger; Chong et al. 2022.")
    save(img, out)


def _slide_04_final(root: Path, out: Path) -> None:
    flow = root / "docs" / "project_blueprints" / "presentation_assets" / "full_workflow_diagram_2026_06_15" / "full_project_ml_workflow_flowchart.png"
    img = new_slide(
        "ML Methodology: Full Project Workflow",
        "The new diagram belongs here: approved inputs, stability context, feature engineering, leakage barrier, occurrence, saturation, and validation.",
        dark=False,
    )
    d = ImageDraw.Draw(img)
    paste_image(img, flow, (58, 156, 1862, 916), cover=False, bg=WHITE)
    card(d, (155, 930, 1765, 1000), fill=(249, 244, 244), outline=AMBER, radius=18)
    draw_text(
        d,
        (190, 951),
        "Key point: stability and maps are context. Occurrence is a classified label; saturation is a continuous target; both wait for approved labels and whole-well validation.",
        22,
        NAVY,
        True,
        width=1540,
        align="center",
    )
    footer(img, "Sources: full project ML workflow diagram; approved-data schema architecture plan; ML citation packet; public/runtime boundary docs.")
    save(img, out)


def _slide_05_final(root: Path, out: Path) -> None:
    img = new_slide(
        "Why These Parameters Matter",
        "Each parameter has a physical reason, a hydrate-supportive signal, a mimic, and an ML role.",
    )
    d = ImageDraw.Draw(img)
    rows = [
        ("Stability", "z, P, T, permafrost", "tests whether hydrate can exist", "not proof by itself", "context, mask, reason flag", TEAL),
        ("Sand host", "GR, φ, ρb, core lithology", "low shale + pore volume can host hydrate", "clean water sand, thin beds, shale mix", "reservoir-quality gate", GREEN),
        ("Electrical", "Rt", "hydrate replaces conductive water, so Rt can rise", "gas, ice, tight rock, salinity, invasion", "log-transform input plus mimic flag", RED),
        ("Elastic", "Vp, Vs, AI, μρ, λρ", "hydrate stiffens the sediment frame", "cement, carbonate, compaction, ice", "derived feature block", PURPLE),
        ("NMR and core", "φNMR, Sh, Sgh, core", "independent saturation and calibration support", "sparse core, processing settings, depth mismatch", "labels and validation overlays", BLUE),
        ("Quality control", "CAL, missingness, outliers", "protects density, sonic, NMR, and Rt", "bad hole can fake curve changes", "exclude, downweight, or flag", AMBER),
    ]
    headers = [("Family", 95), ("Symbols", 360), ("Why it helps", 640), ("What can fool it", 1020), ("ML use", 1390)]
    for label, x in headers:
        draw_text(d, (x, 174), label, 21, NAVY, True)
    d.line((82, 214, 1810, 214), fill=(187, 209, 216), width=3)
    for i, (family, symbols, why, mimic, role, color) in enumerate(rows):
        y = 238 + i * 105
        card(d, (75, y, 1815, y + 82), fill=WHITE, outline=(201, 220, 225), radius=20)
        d.rounded_rectangle((75, y, 92, y + 82), radius=8, fill=color)
        draw_text(d, (105, y + 18), family, 22, color, True, width=220)
        draw_text(d, (360, y + 18), symbols, 22, NAVY, True, width=240)
        draw_text(d, (640, y + 13), why, 18, INK, width=320)
        draw_text(d, (1020, y + 13), mimic, 18, RED if i in [0, 2, 3, 5] else MUTED, width=315)
        draw_text(d, (1390, y + 13), role, 18, TEAL, True, width=340)

    mini_y = 885
    d.rounded_rectangle((240, mini_y, 1680, mini_y + 70), radius=18, fill=(235, 247, 249), outline=(184, 218, 224), width=2)
    draw_text(
        d,
        (960, mini_y + 18),
        "Final presentation point: the model should learn agreement across families, not a single cutoff such as high Rt or low GR.",
        22,
        NAVY,
        True,
        anchor="ma",
    )
    footer(img, "Sources: science-to-ML ladder; ML baseline source ledger; Lee and Collett 2011; Haines et al. 2022; Chong et al. 2022.")
    save(img, out)


def _slide_06_final(root: Path, out: Path) -> None:
    img = new_slide(
        "Geomechanical Feature Sketch",
        "Rock physics explains why hydrate-supportive stiffness must be checked against gas, ice, cement, lithology, stress, and borehole quality.",
    )
    d = ImageDraw.Draw(img)

    # Grain-pack / hydrate sketch.
    card(d, (78, 175, 700, 760), fill=WHITE, outline=(201, 220, 225), radius=24)
    draw_text(d, (112, 205), "Pore-scale idea", 27, NAVY, True)
    rock_box = (140, 292, 610, 622)
    d.rounded_rectangle(rock_box, radius=36, fill=(228, 232, 221), outline=(145, 164, 151), width=3)
    for i in range(45):
        px = rock_box[0] + 34 + (i % 9) * 48 + (10 if (i // 9) % 2 else 0)
        py = rock_box[1] + 32 + (i // 9) * 58
        fill = SAND if i % 3 else (235, 241, 242)
        d.ellipse((px - 20, py - 15, px + 20, py + 15), fill=fill, outline=(160, 150, 119), width=1)
    for px, py in [(245, 390), (335, 445), (425, 390), (500, 502)]:
        d.ellipse((px - 26, py - 26, px + 26, py + 26), fill=(212, 243, 247), outline=TEAL, width=3)
        draw_text(d, (px, py - 11), "H", 22, TEAL, True, anchor="ma")
    arrow(d, (92, 400), (150, 400), BLUE, 5)
    arrow(d, (612, 400), (675, 400), BLUE, 5)
    draw_text(d, (96, 362), "Vp", 22, BLUE, True)
    draw_text(d, (625, 362), "Vs", 22, PURPLE, True)
    d.line((188, 270, 562, 270), fill=AMBER, width=5)
    arrow(d, (376, 240), (376, 282), AMBER, 5)
    draw_text(d, (250, 225), "overburden and compaction shift baselines", 17, MUTED, width=340)
    draw_text(d, (126, 655), "Hydrate can cement or bridge pores, raising shear rigidity. Gas may raise Rt but does not stiffen the frame the same way.", 19, INK, width=520)

    # Equations.
    card(d, (755, 175, 1215, 760), fill=WHITE, outline=(201, 220, 225), radius=24)
    draw_text(d, (790, 205), "Unit-safe features", 27, NAVY, True)
    eqs = [
        ("AI", "ρb × Vp"),
        ("G = μ", "ρb × Vs²"),
        ("K", "ρb × (Vp² − 4Vs²/3)"),
        ("ν", "(3K − 2G) / 2(3K + G)"),
        ("λρ", "(K − 2G/3) × ρb"),
        ("μρ", "G × ρb"),
    ]
    for i, (lhs, rhs) in enumerate(eqs):
        y = 270 + i * 70
        d.rounded_rectangle((790, y, 910, y + 42), radius=12, fill=(235, 247, 249), outline=(184, 218, 224), width=2)
        draw_text(d, (850, y + 9), lhs, 19, TEAL if i < 3 else PURPLE, True, anchor="ma")
        draw_text(d, (940, y + 8), rhs, 19, INK, True, width=230)
    draw_text(d, (790, 705), "Derived features inherit errors from density, sonic units, depth alignment, and QC.", 18, RED, True, width=360)

    # Crossplot sketch.
    card(d, (1270, 175, 1818, 760), fill=WHITE, outline=(201, 220, 225), radius=24)
    draw_text(d, (1305, 205), "Interpretation crossplot", 27, NAVY, True)
    px1, py1, px2, py2 = 1340, 640, 1750, 305
    d.line((px1, py1, 1765, py1), fill=MUTED, width=3)
    d.line((px1, py1, px1, 285), fill=MUTED, width=3)
    arrow(d, (px1, py1), (1775, py1), MUTED, 3)
    arrow(d, (px1, py1), (px1, 275), MUTED, 3)
    draw_text(d, (1698, 655), "λρ", 20, MUTED, True)
    draw_text(d, (1305, 278), "μρ", 20, MUTED, True)
    clusters = [
        ("water sand", 1460, 540, GREEN),
        ("gas sand", 1530, 595, RED),
        ("hydrate sand", 1625, 430, TEAL),
        ("ice/cement", 1710, 345, PURPLE),
        ("shale", 1430, 370, AMBER),
    ]
    for label, cx, cy, color in clusters:
        for j in range(7):
            dx = ((j % 3) - 1) * 14
            dy = ((j // 3) - 1) * 12
            d.ellipse((cx + dx - 6, cy + dy - 6, cx + dx + 6, cy + dy + 6), fill=color, outline=WHITE, width=1)
        draw_text(d, (cx - 45, cy - 45), label, 15, color, True, width=120)
    draw_text(d, (1310, 700), "Hydrate-supportive zone requires sand, P-T context, Rt support, and QC.", 17, INK, width=430)

    checks = [
        ("hydrate support", TEAL),
        ("free gas risk", RED),
        ("ice/cement risk", PURPLE),
        ("shale risk", AMBER),
        ("bad-hole QC", RED),
    ]
    for i, (label, color) in enumerate(checks):
        x = 215 + i * 300
        d.rounded_rectangle((x, 838, x + 250, 890), radius=15, fill=color)
        draw_text(d, (x + 125, 853), label, 18, WHITE, True, anchor="ma")
    footer(img, "Sources: runtime feature engineering; science-to-ML ladder; Cook and Waite 2018; Haines et al. 2022; ML baseline ledger.")
    save(img, out)


def _slide_07_final(root: Path, out: Path) -> None:
    rev = root / "references" / "presentation-revision-2026-06-11" / "images"
    geo = root / "raw_data" / "geology" / "CNS_AUs" / "CNS_AUs.jpg"
    img = new_slide(
        "Map Stack: Website Now and Runtime Later",
        "The 3D view should show every map surface as context, then point forward to approved-runtime occurrence and saturation maps.",
    )
    d = ImageDraw.Draw(img)

    panels = [
        ((78, 178, 650, 505), "Current 3D structural explorer", rev / "project_streamlit_structural_explorer_v2.png", TEAL),
        ((690, 178, 1180, 505), "Public AU and regional map", geo, GREEN),
    ]
    for box, title, path, color in panels:
        paste_image(img, path, box, cover=True, bg=WHITE)
        d.rounded_rectangle((box[0], box[1], box[2], box[1] + 44), radius=16, fill=(7, 30, 43))
        draw_text(d, (box[0] + 18, box[1] + 12), title, 18, WHITE, True, width=box[2] - box[0] - 35)

    # Guarded stability map sketch.
    stab = (1220, 178, 1818, 505)
    card(d, stab, fill=WHITE, outline=(201, 220, 225), radius=22)
    draw_text(d, (1248, 205), "Guarded stability screen", 22, NAVY, True)
    coast = [(1265, 330), (1340, 270), (1430, 280), (1515, 245), (1640, 290), (1770, 278)]
    d.line(coast, fill=(112, 161, 178), width=5)
    for i in range(90):
        x = 1270 + (i * 47) % 500
        y = 325 + ((i * 71) % 110)
        color = (210, 224, 230)
        if i % 23 == 0:
            color = TEAL
        elif i % 29 == 0:
            color = GREEN
        elif i % 17 == 0:
            color = RED
        d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=color)
    counts = [("22", "calculated", TEAL), ("8", "no stable interval", GREEN), ("8,054", "blocked", RED)]
    for i, (num, label, color) in enumerate(counts):
        x = 1255 + i * 175
        d.rounded_rectangle((x, 445, x + 155, 485), radius=12, fill=(235, 247, 249), outline=color, width=2)
        draw_text(d, (x + 18, 454), num, 17, color, True)
        draw_text(d, (x + 65, 456), label, 12, INK, width=85)

    # Lower panels: audit plot, current/future map inventory, future runtime.
    audit = (78, 565, 650, 895)
    card(d, audit, fill=WHITE, outline=(201, 220, 225), radius=22)
    draw_text(d, (105, 592), "Selected-well P-T audit", 22, NAVY, True)
    ax = (140, 828, 570, 635)
    d.line((ax[0], ax[1], ax[2], ax[1]), fill=MUTED, width=3)
    d.line((ax[0], ax[1], ax[0], ax[3]), fill=MUTED, width=3)
    d.line([(155, 800), (250, 735), (355, 690), (500, 665)], fill=TEAL, width=5)
    d.line([(200, 830), (315, 760), (438, 695), (545, 620)], fill=RED, width=4)
    draw_text(d, (330, 664), "phase curve", 15, TEAL, True)
    draw_text(d, (435, 725), "modeled T", 15, RED, True)
    draw_text(d, (105, 850), "Shows assumption audit, not occurrence proof.", 17, RED, True, width=500)

    inventory = (690, 565, 1180, 895)
    card(d, inventory, fill=WHITE, outline=(201, 220, 225), radius=22)
    draw_text(d, (720, 592), "Website maps to carry forward", 22, NAVY, True)
    map_rows = [
        ("Now", "3D structural surfaces", TEAL),
        ("Now", "public wells + hydrate AUs", GREEN),
        ("Now", "stability status map", AMBER),
        ("Now", "temperature-phase audit", BLUE),
        ("Future", "approved occurrence map", RED),
        ("Future", "approved saturation/uncertainty map", PURPLE),
    ]
    for i, (status, label, color) in enumerate(map_rows):
        y = 640 + i * 39
        d.rounded_rectangle((720, y, 800, y + 26), radius=9, fill=color)
        draw_text(d, (760, y + 6), status, 11, WHITE, True, anchor="ma")
        draw_text(d, (820, y + 3), label, 17, INK, width=310)

    future = (1220, 565, 1818, 895)
    card(d, future, fill=(247, 252, 253), outline=(201, 220, 225), radius=22)
    draw_text(d, (1248, 592), "Future approved-runtime 3D maps", 22, NAVY, True)
    # Draw an abstract 3D surface with vertical prediction tracks.
    surface = [(1280, 770), (1400, 690), (1610, 710), (1760, 780), (1640, 835), (1435, 820)]
    d.polygon(surface, fill=(213, 235, 226), outline=TEAL)
    for x, y, color, label in [(1380, 735, TEAL, "Pocc"), (1515, 725, GREEN, "Sh"), (1640, 760, AMBER, "unc")]:
        d.line((x, y - 90, x, y + 75), fill=color, width=5)
        d.ellipse((x - 12, y - 98, x + 12, y - 74), fill=color)
        draw_text(d, (x - 22, y - 125), label, 15, color, True)
    draw_text(d, (1248, 835), "Only after approved logs, labels, and validation; public version shows reviewed summaries.", 17, INK, width=510)

    footer(img, "Sources: current Streamlit structural explorer; public CNS/AU map; guarded stability-screen products; planned approved-runtime outputs.")
    save(img, out)


def _slide_08_final(root: Path, out: Path) -> None:
    img = new_slide(
        "Results and Discussion: What Gets Measured",
        "The final results section must separate source-backed labels, model outputs, uncertainty, and scientific interpretation.",
    )
    d = ImageDraw.Draw(img)

    # Occurrence measurement answer, compact and explicit.
    card(d, (75, 178, 1815, 382), fill=(247, 252, 253), outline=(184, 218, 224), radius=24)
    draw_text(d, (110, 205), "How occurrence is measured in the sources", 28, NAVY, True)
    occurrence_points = [
        ("Chong 2024", "categorical classes from interpreted RAB resistivity images, resistivity, and Vp: pore-filling, fracture-filling, or none"),
        ("Chong 2022 / Singh 2021", "main label is continuous Sh/Sgh from NMR-density or Archie-style saturation; occurrence is inferred only after a label policy"),
        ("Our project", "use approved phase labels, mentor-reviewed intervals, or an approved Sh threshold; never use stability as the occurrence label"),
    ]
    for i, (source, body) in enumerate(occurrence_points):
        x = 112 + i * 560
        d.rounded_rectangle((x, 260, x + 520, 352), radius=16, fill=WHITE, outline=(201, 220, 225), width=2)
        draw_text(d, (x + 18, 274), source, 17, TEAL if i != 2 else RED, True, width=470)
        draw_text(d, (x + 18, 302), body, 14, INK, width=470)

    outputs = [
        ("Occurrence probability", "classifier output after approved labels", TEAL),
        ("Saturation estimate", "continuous Sh/Sgh regression target", GREEN),
        ("Uncertainty", "model + feature + target confidence", BLUE),
        ("QC and mimic flags", "bad hole, shale, gas, ice, tight rock", RED),
        ("Validation figures", "calibration, residuals, held-out wells", PURPLE),
        ("Discussion", "why evidence agreed or disagreed", AMBER),
    ]
    for i, (title, body, color) in enumerate(outputs):
        x = 90 + (i % 3) * 600
        y = 432 + (i // 3) * 170
        card(d, (x, y, x + 520, y + 125), fill=WHITE, outline=(201, 220, 225), radius=20)
        d.ellipse((x + 25, y + 32, x + 85, y + 92), fill=(235, 247, 249), outline=color, width=3)
        draw_text(d, (x + 55, y + 48), str(i + 1), 22, color, True, anchor="ma")
        draw_text(d, (x + 112, y + 28), title, 23, color, True)
        draw_text(d, (x + 112, y + 66), body, 17, INK, width=350)

    card(d, (275, 820, 1645, 918), fill=(249, 244, 244), outline=AMBER, radius=22)
    draw_text(d, (315, 846), "Discussion rule", 23, NAVY, True)
    draw_text(
        d,
        (535, 846),
        "For every interval: what evidence supported hydrate, what looked like a mimic, which QC checks passed, and what approved label or residual proves the model is behaving.",
        19,
        INK,
        width=1040,
    )
    footer(img, "Sources: Chong et al. 2024 occurrence workflow; Chong et al. 2022 and Singh et al. 2021 saturation targets; ML baseline ledger.")
    save(img, out)


def _slide_09_final(root: Path, out: Path) -> None:
    img = new_slide(
        "Conclusion",
        "The final project is an explainable workflow for hydrate occurrence, saturation, and review-ready uncertainty.",
    )
    d = ImageDraw.Draw(img)

    center = (960, 450)
    d.ellipse((650, 245, 1270, 655), fill=(231, 243, 245), outline=(158, 205, 212), width=4)
    draw_text(d, (960, 332), "Final message", 40, NAVY, True, anchor="ma")
    draw_text(
        d,
        (725, 400),
        "Predict occurrence and saturation only when source role, physics response, target provenance, validation, and uncertainty stay traceable.",
        23,
        INK,
        True,
        width=470,
        align="center",
    )

    nodes = [
        ((110, 205), "Science value", "defines the North Slope hydrate system before parameters", TEAL),
        ((1350, 205), "ML value", "separate occurrence classifier and saturation regressor", GREEN),
        ((110, 635), "Delivery value", "website is a public skeleton and map/workflow surface", AMBER),
        ((1350, 635), "Next tasks", "recover workbook formulas, labels, splits, and approved figures", RED),
    ]
    for (x, y), title, body, color in nodes:
        card(d, (x, y, x + 430, y + 150), fill=WHITE, outline=(201, 220, 225), radius=22)
        d.rounded_rectangle((x + 28, y + 42, x + 92, y + 106), radius=18, fill=(235, 247, 249), outline=color, width=3)
        draw_text(d, (x + 60, y + 58), title[0], 25, color, True, anchor="ma")
        draw_text(d, (x + 118, y + 35), title, 26, color, True)
        draw_text(d, (x + 118, y + 76), body, 18, INK, width=260)
        arrow(d, (x + (430 if x < 900 else 0), y + 75), (center[0] + (-305 if x < 900 else 305), center[1]), fill=(148, 171, 180), width=4)

    checklist = [
        ("Now", "public source maps, stability screen, schema coverage, leakage barrier"),
        ("Next", "approved occurrence labels and Sh target policy"),
        ("Final", "whole-well validation, calibrated outputs, reviewed public-safe summaries"),
    ]
    for i, (phase, body) in enumerate(checklist):
        x = 265 + i * 465
        d.rounded_rectangle((x, 825, x + 405, 910), radius=20, fill=(247, 252, 253), outline=(184, 218, 224), width=2)
        draw_text(d, (x + 24, 848), phase, 23, TEAL if i == 0 else (AMBER if i == 1 else GREEN), True)
        draw_text(d, (x + 112, 844), body, 16, INK, width=260)

    footer(img, "Sources: project direction lock; full workflow diagram; approved-data schema plan; USGS/DOE/NETL source stack; ML citation packet.")
    save(img, out)


def _write_contact_sheet(outputs: list[Path], out_dir: Path) -> None:
    thumbs: list[Image.Image] = []
    for path in outputs:
        with Image.open(path).convert("RGB") as src:
            thumbs.append(src.resize((480, 270), Image.Resampling.LANCZOS))
    sheet = Image.new("RGB", (3 * 520, 3 * 330), WHITE)
    d = ImageDraw.Draw(sheet)
    for i, thumb in enumerate(thumbs):
        x = (i % 3) * 520 + 20
        y = (i // 3) * 330 + 42
        d.text((x, y - 28), path_label(outputs[i]), fill=INK, font=font(18, True))
        sheet.paste(thumb, (x, y))
        d.rectangle((x, y, x + 480, y + 270), outline=(190, 210, 216), width=2)
    sheet.save(out_dir / "processing_panel_contact_sheet.jpg", quality=92)


def path_label(path: Path) -> str:
    return path.stem.replace("_", " ")


# Final deck prompt execution, 2026-06-15.
# These definitions intentionally override earlier draft builders while keeping
# the original nine-slide Gmail topic sequence used by build_assets().

def paste_full_slide_plate(base: Image.Image, path: Path) -> bool:
    d = ImageDraw.Draw(base)
    plate = fit_image(path, (0, 0, W, H), cover=False)
    if plate is None:
        card(d, (80, 180, W - 80, H - 120), fill=(248, 241, 241), outline=RED)
        draw_text(d, (120, 230), f"Missing whole-slide plate:\n{path.name}", 34, RED, True, width=1500)
        return False
    x = (W - plate.width) // 2
    y = (H - plate.height) // 2
    base.paste(plate, (x, y))
    return True


def _draw_unit_track(
    d: ImageDraw.ImageDraw,
    x: int,
    y: int,
    w: int,
    label: str,
    unit: str,
    color: tuple[int, int, int],
    active: bool = True,
) -> None:
    d.rounded_rectangle((x, y, x + w, y + 68), radius=16, fill=(248, 252, 253), outline=(205, 223, 228), width=2)
    draw_text(d, (x + 14, y + 10), label, 17, color if active else MUTED, True, width=w - 28)
    draw_text(d, (x + 14, y + 35), unit, 13, MUTED, width=w - 225)
    if active:
        bar_left = x + w - 190
        bar_right = x + w - 52
        d.rounded_rectangle((bar_left, y + 42, bar_right, y + 54), radius=6, fill=(225, 236, 240))
        d.rounded_rectangle((bar_left, y + 42, bar_right - 26, y + 54), radius=6, fill=color)
        draw_text(d, (x + w - 56, y + 36), "0-1", 12, MUTED, True)


def _slide_02_final(root: Path, out: Path) -> None:
    rev = root / "references" / "presentation-revision-2026-06-11" / "images"
    geo = root / "raw_data" / "geology" / "CNS_AUs" / "CNS_AUs.jpg"
    img = new_slide(
        "Introduction: What And Why Gas Hydrates",
        "Methane hydrate is CH4 held inside H2O cages; North Slope hydrate prediction needs more than stability.",
    )
    d = ImageDraw.Draw(img)

    # Light, legible hydrate definition panel replaces the dark SEM-dominant draft.
    card(d, (70, 178, 720, 775), fill=(248, 253, 254), outline=(185, 220, 226), radius=24)
    draw_text(d, (98, 210), "Methane-in-water-cage visual", 28, NAVY, True)
    for r, alpha in [(225, (234, 249, 251)), (180, (223, 245, 248)), (135, (211, 238, 243))]:
        d.ellipse((395 - r, 500 - r, 395 + r, 500 + r), outline=alpha, width=3)
    molecule(d, 395, 500, 180)
    draw_text(d, (115, 705), "CH4 guest molecule + H2O lattice cage", 23, INK, True, width=540)
    draw_text(d, (115, 735), "A crystal habit that can occupy pore space in sand-rich permafrost reservoirs.", 18, MUTED, width=540)

    card(d, (755, 178, 1185, 470), fill=WHITE, outline=(198, 220, 225), radius=22)
    draw_text(d, (782, 210), "Small source image only", 24, NAVY, True)
    paste_image(img, rev / "usgs_gas_hydrate_crystals_sem_public_domain.jpg", (782, 252, 1148, 425), cover=True)
    draw_text(d, (790, 436), "SEM/sample image supports the definition; it is not the slide's main visual.", 14, MUTED, width=350)

    card(d, (1225, 178, 1815, 520), fill=(246, 252, 253), outline=(184, 218, 224), radius=22)
    draw_text(d, (1252, 210), "Pressure-temperature gate", 25, NAVY, True)
    gx1, gy1, gx2, gy2 = 1280, 285, 1770, 455
    d.line((gx1, gy2, gx2, gy2), fill=MUTED, width=3)
    d.line((gx1, gy2, gx1, gy1), fill=MUTED, width=3)
    d.polygon([(1320, 430), (1510, 365), (1725, 365), (1770, 455), (1320, 455)], fill=(214, 242, 247), outline=TEAL)
    d.line((1305, 445, 1750, 300), fill=BLUE, width=4)
    d.line((1305, 300, 1780, 430), fill=RED, width=4)
    draw_text(d, (1370, 355), "GHSZ", 31, TEAL, True)
    draw_text(d, (1690, 460), "T", 18, MUTED, True)
    draw_text(d, (1253, 286), "P", 18, MUTED, True)
    draw_text(d, (1252, 475), "Stability is necessary context, not occurrence proof.", 17, RED, True, width=515)

    card(d, (755, 510, 1185, 775), fill=WHITE, outline=(198, 220, 225), radius=22)
    draw_text(d, (782, 540), "North Slope context", 24, NAVY, True)
    paste_image(img, geo, (790, 585, 1148, 720), cover=True)
    draw_text(d, (790, 732), "Public regional maps guide review; approved well evidence trains labels later.", 14, MUTED, width=350)

    concepts = [
        ("Occurrence", "Is hydrate present by approved target evidence?", BLUE),
        ("Saturation", "How much hydrate is present where labels exist?", GREEN),
        ("Reservoir quality", "Can the rock host pore-filling hydrate?", AMBER),
        ("Production", "Does the system have gas charge, migration, and deliverability?", PURPLE),
    ]
    for i, (label, body, color) in enumerate(concepts):
        y = 550 + i * 70
        card(d, (1225, y, 1815, y + 58), fill=WHITE, outline=(205, 223, 228), radius=16)
        d.rectangle((1225, y, 1235, y + 58), fill=color)
        draw_text(d, (1258, y + 10), label, 18, color, True)
        draw_text(d, (1455, y + 9), body, 14, INK, width=320)

    d.rounded_rectangle((110, 825, 1810, 925), radius=22, fill=(250, 247, 236), outline=(222, 199, 141), width=2)
    draw_text(
        d,
        (145, 850),
        "Slide correction: define hydrate with a clean cage visual, then separate stability, occurrence, saturation, reservoir quality, and production.",
        23,
        NAVY,
        True,
        width=1600,
    )
    footer(img, "Sources: USGS hydrate imagery; project source ledger; public North Slope context layers. No approved well rows or model results shown.")
    save(img, out)


def _slide_03_final(root: Path, out: Path) -> None:
    img = new_slide(
        "Parameters And Well-Log Scaffold",
        "Original headers stay visible; canonical aliases and 0-1 scaling are metadata after split, not a replacement for source units.",
    )
    d = ImageDraw.Draw(img)

    card(d, (70, 175, 615, 845), fill=(248, 253, 254), outline=(184, 218, 224), radius=24)
    draw_text(d, (102, 208), "Visible source headers", 30, NAVY, True)
    header_tracks = [
        ("DEPTH / DEPT / Depth_ft / True Depth", "ft or m; alignment axis, not normalized", BLUE, False),
        ("Rho_b / RHOB / Density_gpcc", "g/cc or kg/m3; convert before equations", TEAL, True),
        ("Phi_porosity / phi_den / DPHI", "fraction or percent; confirm source", GREEN, True),
        ("NMRPHI / phi_nmr", "measured porosity input where available", PURPLE, True),
        ("Rt / RES / AO90", "ohm-m; mnemonic confirmation required", AMBER, True),
        ("GR", "API; lithology / clean-sand proxy", TEAL, True),
        ("Vp / VELP and Vs / VS1", "velocity or slowness-derived; unit gate", BLUE, True),
        ("caliper / CAL1 / differential caliper", "coverage-first QC, not assumed filtering", AMBER, True),
    ]
    for i, (label, unit, color, active) in enumerate(header_tracks):
        _draw_unit_track(d, 102, 260 + i * 68, 475, label, unit, color, active)

    card(d, (665, 175, 1235, 845), fill=WHITE, outline=(198, 220, 225), radius=24)
    draw_text(d, (697, 208), "Sticky variable fingerprint", 30, NAVY, True)
    fingerprint = [
        ("1", "source sheet/file", "MTE, IGS, MTE_refined, IGS_refined"),
        ("2", "original header", "preserve exact spelling first"),
        ("3", "unit above values", "ft/m, g/cc, API, ohm-m, m/s"),
        ("4", "role", "measured, derived, QC, context, target, unresolved"),
        ("5", "normalized name", "runtime alias after provenance is kept"),
        ("6", "X permission", "allowed only after unit/QC/leakage checks"),
        ("7", "leakage risk", "Y-only fields bypass X_allowed"),
        ("8", "runtime note", "mentor/workbook question if unresolved"),
    ]
    for i, (num, label, body) in enumerate(fingerprint):
        y = 270 + i * 63
        d.ellipse((704, y, 742, y + 38), fill=TEAL if i < 6 else RED, outline=None)
        draw_text(d, (723, y + 8), num, 17, WHITE, True, anchor="ma")
        draw_text(d, (760, y - 2), label, 20, INK, True)
        draw_text(d, (760, y + 25), body, 15, MUTED, width=415)

    card(d, (1285, 175, 1815, 845), fill=(250, 253, 253), outline=(198, 220, 225), radius=24)
    draw_text(d, (1317, 208), "Role split before modeling", 30, NAVY, True)
    role_rows = [
        ("X_allowed", "measured logs + valid derived features + QC/context flags", GREEN),
        ("Unit gate", "all numeric predictors scaled 0-1 after whole-well split", TEAL),
        ("Depth", "kept as depth/alignment/context axis unless approved", BLUE),
        ("Caliper", "gather coverage first; missing QC becomes a flag", AMBER),
        ("Y-only rail", "Sgh, S_h, Sh, NMR_SAT, Hydrate Saturation, Swr, S_wr, phase/occurrence labels", RED),
    ]
    for i, (label, body, color) in enumerate(role_rows):
        y = 280 + i * 98
        d.rounded_rectangle((1320, y, 1780, y + 72), radius=18, fill=WHITE, outline=(205, 223, 228), width=2)
        d.rectangle((1320, y, 1330, y + 72), fill=color)
        draw_text(d, (1352, y + 10), label, 20, color, True)
        draw_text(d, (1495, y + 10), body, 14, INK, width=260)

    d.rounded_rectangle((180, 890, 1700, 958), radius=18, fill=(241, 249, 252), outline=(184, 218, 224), width=2)
    draw_text(d, (220, 910), "Current coverage: about 3 of 71 datasets are visible, enough for schema/architecture readiness but not final training or metrics.", 22, NAVY, True, width=1460)
    footer(img, "Sources: WELL_LOG_REQUIREMENTS_MAP; approved-data schema coverage plan; intake spec; first model experiment plan.")
    save(img, out)


def _slide_04_final(root: Path, out: Path) -> None:
    plate = root / "docs" / "project_blueprints" / "presentation_assets" / "full_workflow_diagram_2026_06_15" / "slide_04_expanded_architecture_map.png"
    img = Image.new("RGB", (W, H), WHITE)
    if not paste_full_slide_plate(img, plate):
        footer(img, "Missing V5.2 expanded architecture plate.")
    save(img, out)


def _slide_05_final(root: Path, out: Path) -> None:
    img = new_slide(
        "Why Parameters And Model Choices Matter",
        "No single log proves hydrate; each family needs a physical reason, mimic check, QC status, and model role.",
    )
    d = ImageDraw.Draw(img)
    card(d, (70, 170, 1850, 790), fill=WHITE, outline=(198, 220, 225), radius=22)

    cols = [112, 285, 555, 900, 1265, 1630]
    headers = ["Family", "Examples", "What it measures", "Hydrate support", "Mimics / masks", "ML role"]
    widths = [170, 245, 320, 335, 340, 190]
    for x, head, w in zip(cols, headers, widths, strict=True):
        draw_text(d, (x, 205), head, 18, NAVY, True, width=w)
    d.line((90, 240, 1828, 240), fill=(194, 215, 220), width=3)

    rows = [
        ("Lithology", "GR, shale proxy", "sand vs shale tendency", "clean sand can host pore-filling hydrate", "radioactive minerals, laminated shale", "reservoir gate"),
        ("Porosity", "RHOB, DPHI, NMRPHI", "pore volume and fluid response", "porous sand gives storage capacity", "shale, washout, gas effect, unit errors", "input + cross-check"),
        ("Electrical", "Rt, RES, AO90", "formation conductivity", "hydrate can raise resistivity in clean sand", "free gas, ice, tight rock, salinity", "log transform"),
        ("Elastic", "Vp, Vs, Vp/Vs", "frame stiffness and ratios", "hydrate stiffens sediment frame", "cement, carbonate, ice, stress", "derived features"),
        ("Impedance", "rho_b * Vp", "density-velocity contrast", "supports elastic separation", "compaction, lithology, bad density", "crossplot feature"),
        ("NMR/core", "NMRPHI, core, labels", "calibration and target evidence", "supports labels or residual review", "sparse sampling, depth mismatch", "Y/review only"),
        ("QC", "caliper, diff caliper", "borehole trust", "protects density, sonic, Rt", "missing bit size/sign convention", "coverage-first flag"),
    ]
    for i, row in enumerate(rows):
        y = 265 + i * 70
        fill = (249, 253, 253) if i % 2 == 0 else WHITE
        d.rounded_rectangle((90, y - 8, 1828, y + 54), radius=14, fill=fill, outline=(218, 231, 235), width=1)
        accent = [TEAL, GREEN, RED, PURPLE, BLUE, AMBER, SHALE][i]
        d.rectangle((90, y - 8, 98, y + 54), fill=accent)
        for x, text, w in zip(cols, row, widths, strict=True):
            draw_text(d, (x, y + 4), text, 14 if x > 500 else 15, INK if x != cols[0] else accent, x == cols[0], width=w, spacing=3)

    ladder = [
        ("1", "transparent baselines", "majority/logistic/linear checks"),
        ("2", "tree or boosting", "tabular nonlinear baseline"),
        ("3", "ANN/Keras", "Chong-style ML anchor after leakage controls"),
    ]
    for i, (num, title, body) in enumerate(ladder):
        x = 150 + i * 550
        d.rounded_rectangle((x, 835, x + 455, 928), radius=22, fill=(247, 252, 253), outline=(184, 218, 224), width=2)
        d.ellipse((x + 22, 858, x + 70, 906), fill=[TEAL, AMBER, PURPLE][i])
        draw_text(d, (x + 46, 872), num, 20, WHITE, True, anchor="ma")
        draw_text(d, (x + 90, 852), title, 22, NAVY, True, width=320)
        draw_text(d, (x + 90, 884), body, 15, MUTED, width=330)
        if i < 2:
            arrow(d, (x + 470, 882), (x + 535, 882), fill=TEAL, width=4)

    footer(img, "Sources: science-to-ML ladder; ML pipeline ledger; Chong et al. hydrate ML source anchor. Method architecture only, no model metrics.")
    save(img, out)


def _slide_06_final(root: Path, out: Path) -> None:
    img = new_slide(
        "Geomechanics, Equations, And Unit Gate",
        "Equation features enter X_allowed only after source, unit, QC, and leakage checks pass.",
    )
    d = ImageDraw.Draw(img)

    card(d, (70, 170, 525, 905), fill=(248, 253, 254), outline=(184, 218, 224), radius=24)
    draw_text(d, (105, 205), "Unit gate", 30, NAVY, True)
    gates = [
        ("Headers", "preserve original name and unit"),
        ("Depth", "convert ft/m; keep alignment axis"),
        ("Density", "g/cc or kg/m3 before elastic math"),
        ("Velocity", "Vp/Vs direct or DT/DTS conversion"),
        ("Porosity", "fraction vs percent recorded"),
        ("Caliper", "coverage first, threshold later"),
        ("Targets", "Sgh/S_h/Sh/NMR_SAT are Y-only"),
    ]
    for i, (label, body) in enumerate(gates):
        y = 275 + i * 82
        d.rounded_rectangle((105, y, 490, y + 58), radius=16, fill=WHITE, outline=(205, 223, 228), width=2)
        draw_text(d, (125, y + 9), label, 18, TEAL if i < 6 else RED, True, width=110)
        draw_text(d, (245, y + 9), body, 14, INK, width=220)

    equations = [
        ("GR proxy", "GR -> shale volume or clean-sand flag", TEAL),
        ("Density porosity", "phi_D = (rho_ma - rho_b)/(rho_ma - rho_f)", GREEN),
        ("Resistivity", "logRt = log(Rt); Archie only if Rw/a/m/n approved", AMBER),
        ("Vp/Vs", "VpVs = Vp / Vs", PURPLE),
        ("Acoustic impedance", "AI = rho_b * Vp", BLUE),
        ("Shear modulus", "G = rho_b * Vs^2", PURPLE),
        ("Bulk modulus", "K = rho_b * (Vp^2 - 4/3 * Vs^2)", BLUE),
        ("Elastic ratios", "E = 9KG/(3K+G); nu = (3K-2G)/(2(3K+G))", GREEN),
        ("Lambda/mu", "lambda = K - 2G/3; mu = G", PURPLE),
        ("lambda-rho", "lambda-rho and mu-rho after unit consistency", BLUE),
        ("NMR-density gap", "phi_NMR - phi_D as reviewed separation feature", AMBER),
        ("Caliper QC", "CAL, bit size, and differential caliper create QC flags", SHALE),
    ]
    for i, (title, body, color) in enumerate(equations):
        col = i % 3
        row = i // 3
        x = 585 + col * 410
        y = 185 + row * 170
        d.rounded_rectangle((x, y, x + 370, y + 125), radius=20, fill=WHITE, outline=(205, 223, 228), width=2)
        d.rectangle((x, y, x + 10, y + 125), fill=color)
        draw_text(d, (x + 28, y + 18), title, 21, color, True, width=310)
        draw_text(d, (x + 28, y + 55), body, 15, INK, width=310, spacing=4)

    d.rounded_rectangle((595, 880, 1790, 948), radius=18, fill=(250, 247, 236), outline=(222, 199, 141), width=2)
    draw_text(
        d,
        (625, 900),
        "Active feature rule: measured inputs and derived equations can feed ML only after units, source provenance, QC, and target-leakage checks pass.",
        21,
        NAVY,
        True,
        width=1130,
    )
    footer(img, "Sources: WELL_LOG_REQUIREMENTS_MAP; science-to-ML ladder; ML baseline source ledger. Formula chips are architecture, not calculated results.")
    save(img, out)


def _slide_08_final(root: Path, out: Path) -> None:
    plate = root / "docs" / "project_blueprints" / "presentation_assets" / "full_workflow_diagram_2026_06_15" / "slide_07_ml_runtime_detail.png"
    img = Image.new("RGB", (W, H), WHITE)
    if not paste_full_slide_plate(img, plate):
        footer(img, "Missing V5.2 ML runtime detail plate.")
    save(img, out)


def _slide_09_final(root: Path, out: Path) -> None:
    img = new_slide(
        "Conclusion And Next Steps",
        "Current contribution: public-safe ML/schema readiness outside the stability screen, with no final training or metrics claimed.",
    )
    d = ImageDraw.Draw(img)

    card(d, (90, 175, 1015, 760), fill=(248, 253, 254), outline=(184, 218, 224), radius=24)
    draw_text(d, (125, 210), "Completed outside stability", 32, NAVY, True)
    completed = [
        ("schema coverage matrix", "public-safe header-level inventory for available and expected fields"),
        ("field-role table", "measured inputs, derived features, QC, context, calibration, target-only, unresolved"),
        ("intake spec + validator", "variable fingerprint and header-audit readiness checks"),
        ("target leakage barrier", "Sgh/S_h/Sh/NMR_SAT and phase labels bypass X_allowed"),
        ("first model experiment plan", "occurrence classification and saturation regression remain linked but separate"),
        ("whole-well validation design", "split before train-only scaling, imputation, feature selection, and model fitting"),
    ]
    for i, (title, body) in enumerate(completed):
        y = 280 + i * 72
        d.ellipse((125, y, 158, y + 33), fill=GREEN)
        draw_text(d, (141, y + 7), "OK", 11, WHITE, True, anchor="ma")
        draw_text(d, (178, y - 2), title, 20, INK, True, width=310)
        draw_text(d, (500, y - 2), body, 16, MUTED, width=420)

    card(d, (1060, 175, 1815, 760), fill=WHITE, outline=(198, 220, 225), radius=24)
    draw_text(d, (1095, 210), "Blue runtime confirmations", 32, BLUE, True)
    questions = [
        "Target priority when Sgh, S_h, Sh, and NMR_SAT coexist",
        "Fraction-vs-percent convention for saturation labels",
        "Occurrence-label provenance: source classes, thresholds, or reviewed intervals",
        "Train / validation / locked-test well assignment after full recovery",
        "Caliper coverage sufficiency before washout filtering",
        "Missing-log adapter policy for Vp, RHOB, or other absent curves",
    ]
    for i, q in enumerate(questions):
        y = 285 + i * 70
        d.rounded_rectangle((1098, y, 1775, y + 48), radius=16, fill=(239, 248, 255), outline=(153, 197, 232), width=2)
        draw_text(d, (1120, y + 11), q, 16, INK, True, width=625)

    d.rounded_rectangle((165, 815, 1755, 925), radius=24, fill=(250, 247, 236), outline=(222, 199, 141), width=2)
    draw_text(
        d,
        (205, 842),
        "Mentor message: the project is ready to load approved headers through a leakage-safe ML architecture; real occurrence and saturation training waits for approved rows, target authority, units, split policy, and review.",
        24,
        NAVY,
        True,
        width=1500,
    )
    footer(img, "Sources: approved-data intake spec; first model experiment plan; V5.2 workflow package. No fake results, predictions, or metrics.")
    save(img, out)


def build_assets(root: Path) -> list[Path]:
    out_dir = root / "docs" / "project_blueprints" / "presentation_assets" / "processing_revisions_2026_06_11"
    outputs = [
        out_dir / "slide_01_about_me.png",
        out_dir / "slide_02_hydrate_intro.png",
        out_dir / "slide_03_parameter_scaffold.png",
        out_dir / "slide_04_ml_architecture.png",
        out_dir / "slide_05_parameter_behavior.png",
        out_dir / "slide_06_geomechanics.png",
        out_dir / "slide_07_map_context.png",
        out_dir / "slide_08_results_plan.png",
        out_dir / "slide_09_conclusion.png",
    ]
    builders = [
        slide_01,
        _slide_02_final,
        _slide_03_final,
        _slide_04_final,
        _slide_05_final,
        _slide_06_final,
        _slide_07_final,
        _slide_08_final,
        _slide_09_final,
    ]
    for builder, output in zip(builders, outputs, strict=True):
        builder(root, output)
    _write_contact_sheet(outputs, out_dir)
    return outputs


if __name__ == "__main__":
    build_assets(Path(__file__).resolve().parents[2])
