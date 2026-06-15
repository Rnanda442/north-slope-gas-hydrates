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
    builders = [slide_01, slide_02, slide_03, slide_04, slide_05, slide_06, slide_07, slide_08, slide_09]
    for builder, output in zip(builders, outputs, strict=True):
        builder(root, output)
    return outputs


if __name__ == "__main__":
    build_assets(Path(__file__).resolve().parents[2])
