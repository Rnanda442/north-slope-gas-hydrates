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
    img = new_slide("Parameters: Well-Log Scaffold", "Each symbol shows what is measured, the normalized model range, and why it enters the pipeline.")
    d = ImageDraw.Draw(img)
    for idx, (sym, name, measures, role, rng, color) in enumerate(PARAMS):
        row, col = divmod(idx, 3)
        x = 80 + col * 600
        y = 170 + row * 230
        card(d, (x, y, x + 520, y + 175), fill=WHITE)
        d.rounded_rectangle((x + 22, y + 25, x + 118, y + 120), radius=20, fill=(235, 247, 249), outline=(186, 219, 225), width=2)
        draw_text(d, (x + 70, y + 55), sym, 27, color, True, anchor="ma")
        draw_text(d, (x + 145, y + 26), name, 24, NAVY, True)
        draw_text(d, (x + 145, y + 65), f"Measures: {measures}", 18, INK, width=335)
        draw_text(d, (x + 145, y + 112), f"ML use: {role}", 17, MUTED, width=335)
        gauge(d, (x + 145, y + 145, x + 475, y + 160), rng[0], rng[1], color)
    card(d, (1120, 855, 1780, 975), fill=(249, 244, 244), outline=RED)
    draw_text(d, (1150, 875), "Locked target fields", 25, RED, True)
    draw_text(d, (1150, 915), "S_h, Sgh, NMR_SAT, phase labels, and final rankings supervise or score models. They stay out of the input table to prevent target leakage.", 18, INK, width=570)
    footer(img, "Sources: WELL_LOG_REQUIREMENTS_MAP; dashboard/well_log_engine.py; dashboard/runtime/feature_engineering.py; Lee & Collett 2011; Haines et al. 2022.")
    save(img, out)


def slide_04(root: Path, out: Path) -> None:
    img = new_slide("ML Methodology: Architecture", "Every parameter passes shared gates before equations, features, split policy, models, and review outputs.", dark=True)
    d = ImageDraw.Draw(img)
    x0 = 70
    draw_text(d, (x0, 180), "Log inputs", 26, ICE, True)
    inputs = ["GR", "Rt", "RHOB", "\u03c6_NMR", "Vp", "Vs", "CAL", "Core"]
    for i, sym in enumerate(inputs):
        y = 230 + i * 66
        d.rounded_rectangle((x0, y, x0 + 125, y + 45), radius=10, fill=(20, 73, 88), outline=ICE, width=2)
        draw_text(d, (x0 + 62, y + 10), sym, 22, WHITE, True, anchor="ma")
        d.line((x0 + 125, y + 22, 225, y + 22), fill=(118, 153, 164), width=3)
    d.line((225, 252, 225, 635), fill=(118, 153, 164), width=5)
    draw_text(d, (238, 635), "all curves pass the shared gate stack", 15, (191, 218, 224), width=180)
    gates = [
        ("1", "Units + source", "all curves carry source mnemonic and unit", TEAL),
        ("2", "Depth alignment", "same interval before features are calculated", BLUE),
        ("3", "Borehole QC", "caliper/missing/outlier flags gate reliability", RED),
        ("4", "Reservoir/stability screen", "sand + P-T admissibility before hydrate review", GREEN),
        ("5", "Leakage lock", "targets never become predictors", AMBER),
    ]
    gx = 285
    for i, (num, title, body, color) in enumerate(gates):
        y = 190 + i * 115
        card(d, (gx, y, gx + 350, y + 84), fill=(18, 56, 70), outline=(76, 121, 136))
        d.ellipse((gx + 18, y + 22, gx + 58, y + 62), fill=color)
        draw_text(d, (gx + 38, y + 31), num, 20, WHITE, True, anchor="ma")
        draw_text(d, (gx + 75, y + 16), title, 22, ICE, True)
        draw_text(d, (gx + 75, y + 47), body, 15, (210, 231, 236), width=245)
        arrow(d, (225, y + 42), (gx, y + 42), fill=(118, 153, 164), width=3)
    eqx = 720
    card(d, (eqx, 190, eqx + 360, 580), fill=(17, 58, 64), outline=(75, 129, 137))
    draw_text(d, (eqx + 30, 215), "Feature equations", 27, ICE, True)
    eqs = [
        ("Vsh", "(GR-GRclean)/(GRshale-GRclean)"),
        ("\u03c6_D", "(\u03c1ma-RHOB)/(\u03c1ma-\u03c1f)"),
        ("Vp, Vs", "304.8 / DT, 304.8 / DTS"),
        ("AI", "RHOB x Vp"),
        ("\u03bb\u03c1, \u03bc\u03c1", "RHOB(Vp^2-2Vs^2), RHOB x Vs^2"),
        ("S_h proxy", "(\u03c6_D-\u03c6_NMR)/\u03c6_D"),
    ]
    for i, (lhs, rhs) in enumerate(eqs):
        y = 270 + i * 45
        draw_text(d, (eqx + 35, y), lhs, 21, WHITE, True)
        draw_text(d, (eqx + 145, y), rhs, 17, (191, 218, 224), width=190)
    arrow(d, (gx + 350, 442), (eqx, 380), fill=(118, 153, 164), width=4)
    stages = [
        ("Feature table", "measured + derived; train-fit scaling"),
        ("Split policy", "held-out wells; no random depth rows"),
        ("Model ladder", "rules -> Logit/Ridge -> RF/GBM -> Keras ANN"),
        ("Outputs", "phase, S_h, probability, reason codes"),
    ]
    sx = 1160
    for i, (title, body) in enumerate(stages):
        y = 185 + i * 140
        card(d, (sx, y, sx + 420, y + 95), fill=(22, 56, 69), outline=(74, 122, 136))
        draw_text(d, (sx + 24, y + 20), title, 25, ICE if i < 3 else AMBER, True)
        draw_text(d, (sx + 24, y + 55), body, 17, WHITE, width=360)
        if i:
            arrow(d, (sx + 210, y - 44), (sx + 210, y), fill=(118, 153, 164), width=4)
    arrow(d, (eqx + 360, 380), (sx, 230), fill=(118, 153, 164), width=4)
    d.rounded_rectangle((350, 895, 1550, 930), radius=12, fill=RED)
    draw_text(d, (950, 940), "Target leakage barrier: S_h, Sgh, NMR_SAT and final labels score/supervise models only.", 23, ICE, True, anchor="ma")
    footer(img, "Sources: Classification Methods Draft; dashboard/runtime/feature_engineering.py; WELL_LOG_REQUIREMENTS_MAP; Chong et al. 2022.", dark=True)
    save(img, out)


def slide_05(root: Path, out: Path) -> None:
    img = new_slide("ML Methodology: Why These Parameters", "Normalized behavior panels show the range the model reviews and why each pattern is not a label by itself.")
    d = ImageDraw.Draw(img)
    panels = [
        ("Clean sand", "low GR + usable porosity, but no hydrate proof", GREEN, [("GR", [0.25, 0.22, 0.26, 0.18], AMBER), ("phi", [0.55, 0.62, 0.60, 0.66], GREEN), ("Rt", [0.25, 0.30, 0.28, 0.32], RED)]),
        ("Hydrate in sand", "Rt high + NMR-density gap + stiffness", TEAL, [("Rt", [0.38, 0.78, 0.88, 0.76], RED), ("NMR", [0.62, 0.30, 0.25, 0.34], BLUE), ("Vp", [0.45, 0.70, 0.78, 0.72], PURPLE)]),
        ("Shale", "high GR and bound water can mimic porosity", AMBER, [("GR", [0.72, 0.78, 0.82, 0.74], AMBER), ("phi", [0.58, 0.52, 0.55, 0.53], GREEN), ("Rt", [0.30, 0.34, 0.29, 0.36], RED)]),
        ("Free gas", "Rt may rise while Vp softens", RED, [("Rt", [0.40, 0.68, 0.76, 0.65], RED), ("Vp", [0.62, 0.28, 0.24, 0.32], BLUE), ("Vs", [0.48, 0.50, 0.52, 0.49], PURPLE)]),
        ("Ice/cement", "stiff and resistive, but not necessarily hydrate", PURPLE, [("Rt", [0.45, 0.80, 0.84, 0.78], RED), ("Vp", [0.52, 0.78, 0.82, 0.76], BLUE), ("GR", [0.30, 0.27, 0.25, 0.28], AMBER)]),
        ("Bad hole", "washout corrupts density, sonic, NMR, Rt", RED, [("CAL", [0.20, 0.30, 0.92, 0.86], RED), ("RHOB", [0.54, 0.50, 0.22, 0.24], GREEN), ("Vp", [0.55, 0.53, 0.30, 0.34], BLUE)]),
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
    draw_text(d, (960, 990), "Rule: the model learns evidence patterns after lithology, P-T context, borehole QC, and competing explanations are checked.", 23, NAVY, True, anchor="ma")
    footer(img, "Sources: parameter matrix; Haines et al. 2022; Lee & Collett 2011; dashboard/well_log_engine.py normalized ranges.")
    save(img, out)


def slide_06(root: Path, out: Path) -> None:
    img = new_slide("Geomechanical Feature Sketch", "Use source-backed equations to test stiffness, stress, and gas-versus-hydrate ambiguity.")
    d = ImageDraw.Draw(img)
    card(d, (90, 180, 620, 740), fill=WHITE)
    draw_text(d, (120, 205), "Inputs", 30, NAVY, True)
    inputs = [("RHOB", "bulk density"), ("Vp", "P-wave velocity"), ("Vs", "S-wave velocity"), ("Rt", "electrical support"), ("GR", "lithology"), ("CAL", "borehole QC")]
    for i, (sym, label) in enumerate(inputs):
        y = 265 + i * 70
        d.rounded_rectangle((125, y, 220, y + 46), radius=12, fill=(234, 247, 249), outline=(184, 218, 224), width=2)
        draw_text(d, (172, y + 11), sym, 22, TEAL if i < 3 else AMBER, True, anchor="ma")
        draw_text(d, (245, y + 12), label, 20, INK, width=280)
    rock = [(770, 245), (1065, 245), (1190, 430), (1065, 615), (770, 615), (645, 430)]
    d.polygon(rock, fill=(218, 226, 219), outline=(135, 158, 150))
    for i in range(34):
        px = 720 + (i % 7) * 60
        py = 310 + (i // 7) * 50
        d.ellipse((px, py, px + 23, py + 15), fill=(187, 211, 215), outline=(155, 181, 186))
    for y, color, label in [(350, BLUE, "P wave"), (505, PURPLE, "S wave")]:
        d.line((585, y, 725, y), fill=color, width=6)
        arrow(d, (725, y), (790, y), fill=color, width=5)
        draw_text(d, (585, y - 32), label, 18, color, True)
    card(d, (1250, 175, 1800, 710), fill=WHITE)
    draw_text(d, (1280, 205), "Equations used", 30, NAVY, True)
    eqs = [
        "Vp = 304.8 / DT",
        "Vs = 304.8 / DTS",
        "AI = RHOB x Vp",
        "\u03bc\u03c1 = RHOB x Vs^2",
        "\u03bb\u03c1 = RHOB x (Vp^2 - 2Vs^2)",
        "G = RHOB x Vs^2",
        "K = RHOB x (Vp^2 - 4Vs^2/3)",
        "\u03bd = (Vp^2 - 2Vs^2) / [2(Vp^2 - Vs^2)]",
        "\u03c3_eff = \u03c3_v - \u03b1Pp",
    ]
    for i, eq in enumerate(eqs):
        draw_text(d, (1290, 260 + i * 45), eq, 20, INK, True if i < 5 else False, width=470)
    checks = [
        ("hydrate-supportive", GREEN),
        ("free gas", RED),
        ("ice/cement", PURPLE),
        ("stress context", BLUE),
        ("bad hole", RED),
    ]
    for i, (label, color) in enumerate(checks):
        x = 190 + i * 320
        d.rounded_rectangle((x, 820, x + 250, 875), radius=14, fill=color)
        draw_text(d, (x + 125, 836), label, 18, WHITE, True, anchor="ma")
    footer(img, "Sources: dashboard/well_log_engine.py equation groups; dashboard/runtime/feature_engineering.py; WELL_LOG_REQUIREMENTS_MAP; manuscript equation/range docs.")
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
    img = new_slide("Results and Discussion Plan", "Final results need figures that explain evidence agreement, uncertainty, and review flags.")
    d = ImageDraw.Draw(img)
    paste_image(img, assets / "synthetic_well_log_panel.png", (80, 180, 680, 565), cover=True)
    paste_image(img, assets / "sweet_spot_ranking.png", (120, 610, 660, 820), cover=True)
    outputs = [
        ("Gate table", "QC, stability, reservoir, phase evidence", TEAL),
        ("Model figures", "confusion, calibration, residuals", BLUE),
        ("Interval output", "class probability + S_h", GREEN),
        ("Review flags", "bad hole, shale, gas, out-of-distribution", RED),
        ("Discussion lens", "why an interval passed, failed, or stayed expert review", AMBER),
    ]
    for i, (title, body, color) in enumerate(outputs):
        x = 780 + (i % 2) * 470
        y = 185 + (i // 2) * 190
        w = 420 if i < 4 else 890
        card(d, (x, y, x + w, y + 130), fill=WHITE)
        d.rounded_rectangle((x + 22, y + 35, x + 78, y + 91), radius=14, fill=(235, 247, 249), outline=(186, 219, 225), width=2)
        draw_text(d, (x + 50, y + 49), str(i + 1), 24, color, True, anchor="ma")
        draw_text(d, (x + 100, y + 28), title, 24, color, True)
        draw_text(d, (x + 100, y + 65), body, 18, INK, width=w - 130)
        if i in (0, 1, 2, 3):
            arrow(d, (x + w // 2, y + 130), (x + w // 2, y + 170), fill=(136, 163, 174), width=3)
    footer(img, "Sources: Classification Methods Draft; Chong et al. 2022; dashboard/well_log_engine.py; public/synthetic project figures.")
    save(img, out)


def slide_09(root: Path, out: Path) -> None:
    img = new_slide("Conclusion", "The workflow is strongest when occurrence, saturation, uncertainty, and producibility stay separated.")
    d = ImageDraw.Draw(img)
    center = (960, 465)
    d.ellipse((720, 245, 1200, 685), fill=(231, 243, 245), outline=(158, 205, 212), width=4)
    draw_text(d, (960, 365), "Explainable hydrate prediction", 38, NAVY, True, anchor="ma")
    draw_text(d, (960, 430), "public context + approved logs + equations + validation", 22, MUTED, width=430, align="center")
    nodes = [
        ((210, 260), "Science", "separate occurrence and saturation", TEAL),
        ((1365, 260), "ML", "transparent features and reason codes", GREEN),
        ((210, 650), "Energy", "rank sweet spots, not labels only", AMBER),
        ((1365, 650), "Next", "confirm workbook labels and runtime figures", RED),
    ]
    for (x, y), title, body, color in nodes:
        card(d, (x, y, x + 360, y + 135), fill=WHITE)
        d.ellipse((x + 22, y + 38, x + 80, y + 96), fill=(235, 247, 249), outline=(186, 219, 225), width=2)
        draw_text(d, (x + 51, y + 51), title[0], 24, color, True, anchor="ma")
        draw_text(d, (x + 105, y + 32), title, 25, color, True)
        draw_text(d, (x + 105, y + 69), body, 18, INK, width=220)
        arrow(d, (x + (360 if x < center[0] else 0), y + 68), (center[0] + (-240 if x < center[0] else 240), center[1]), fill=(148, 171, 180), width=4)
    draw_text(d, (960, 820), "Final message: predict hydrate occurrence and saturation only when source, target provenance, validation, and uncertainty all stay traceable.", 27, NAVY, True, anchor="ma")
    footer(img, "Sources: USGS/DOE/NETL; Chong et al. 2022; Haines et al. 2022; WELL_LOG_REQUIREMENTS_MAP; runtime equation docs.")
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
