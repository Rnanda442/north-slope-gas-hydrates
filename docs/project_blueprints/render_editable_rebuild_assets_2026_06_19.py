from __future__ import annotations

import argparse
import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
ASSET_DIR = (
    ROOT
    / "docs"
    / "project_blueprints"
    / "presentation_assets"
    / "editable_rebuild_2026_06_19"
)
PT_CSV = (
    ROOT
    / "data"
    / "public_stability_products"
    / "phase_curve_methane_5ppt_screenshot_recovered_2026-06-18.csv"
)
PT_PNG = ASSET_DIR / "slide_02_pt_diagram_from_recovered_csv_2026_06_19.png"
CONTACT_SHEET = ASSET_DIR / "editable_rebuild_contact_sheet_2026_06_19.png"
DRIVE_CONTACT_SHEET = ASSET_DIR / "drive_import_contact_sheet_2026_06_19.png"


NAVY = (15, 23, 42)
SLATE = (71, 85, 105)
TEAL = (15, 118, 110)
AMBER = (180, 83, 9)
BLUE = (29, 78, 216)
LIGHT = (248, 250, 252)
GRID = (203, 213, 225)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def read_phase_curve() -> list[dict[str, float]]:
    if not PT_CSV.exists():
        raise FileNotFoundError(f"Missing P-T CSV: {PT_CSV}")
    rows: list[dict[str, float]] = []
    with PT_CSV.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            try:
                rows.append(
                    {
                        "temperature_c": float(row["equilibrium_temperature_c"]),
                        "pressure_mpa": float(row["pressure_mpa_absolute"]),
                        "depth_m": float(row["source_depth_m"]),
                    }
                )
            except (KeyError, TypeError, ValueError):
                continue
    if len(rows) < 3:
        raise ValueError("Recovered P-T CSV did not contain enough numeric points.")
    return sorted(rows, key=lambda item: item["pressure_mpa"])


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    width: int,
    fill: tuple[int, int, int],
    text_font: ImageFont.ImageFont,
    line_gap: int = 4,
) -> int:
    x, y = xy
    words = text.split()
    line = ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=text_font)[2] <= width:
            line = candidate
        else:
            draw.text((x, y), line, fill=fill, font=text_font)
            y += text_font.size + line_gap if hasattr(text_font, "size") else 18
            line = word
    if line:
        draw.text((x, y), line, fill=fill, font=text_font)
        y += text_font.size + line_gap if hasattr(text_font, "size") else 18
    return y


def render_pt_diagram() -> Path:
    rows = read_phase_curve()
    ASSET_DIR.mkdir(parents=True, exist_ok=True)

    width, height = 1800, 1180
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), fill=LIGHT)

    title_font = font(58, True)
    label_font = font(34, True)
    tick_font = font(27)
    small_font = font(25)
    callout_font = font(29, True)

    left, top, right, bottom = 170, 150, 1320, 930
    x_min, x_max = -12.0, 16.0
    y_min, y_max = 0.0, 22.0

    def x_pos(temp: float) -> float:
        return left + (temp - x_min) / (x_max - x_min) * (right - left)

    def y_pos(pressure: float) -> float:
        return bottom - (pressure - y_min) / (y_max - y_min) * (bottom - top)

    draw.text((92, 50), "Methane + 5 ppt P-T diagram", fill=NAVY, font=title_font)
    draw.text(
        (96, 112),
        "CSV-derived phase boundary; stability context only, not hydrate proof",
        fill=SLATE,
        font=small_font,
    )

    draw.rectangle((left, top, right, bottom), fill=(255, 255, 255), outline=NAVY, width=3)
    for t in range(-10, 17, 5):
        x = x_pos(t)
        draw.line((x, top, x, bottom), fill=GRID, width=2)
        draw.text((x - 18, bottom + 20), f"{t}", fill=SLATE, font=tick_font)
    for p in range(0, 23, 5):
        y = y_pos(p)
        draw.line((left, y, right, y), fill=GRID, width=2)
        draw.text((left - 62, y - 14), f"{p}", fill=SLATE, font=tick_font)

    points = [(x_pos(row["temperature_c"]), y_pos(row["pressure_mpa"])) for row in rows]
    for p1, p2 in zip(points[:-1], points[1:]):
        draw.line((*p1, *p2), fill=TEAL, width=8)
    for x, y in points[:: max(1, len(points) // 12)]:
        draw.ellipse((x - 8, y - 8, x + 8, y + 8), fill=(13, 148, 136), outline="white", width=2)

    draw.text(((left + right) // 2 - 170, bottom + 72), "Temperature (C)", fill=NAVY, font=label_font)
    draw.text((42, (top + bottom) // 2 - 30), "Pressure (MPa)", fill=NAVY, font=label_font)

    # Depth reference ticks on right side.
    draw.line((right + 50, top, right + 50, bottom), fill=SLATE, width=3)
    for depth in [250, 750, 1250, 1750, 2250]:
        pressure = 0.101325 + depth * 0.00980665
        if y_min <= pressure <= y_max:
            y = y_pos(pressure)
            draw.line((right + 40, y, right + 65, y), fill=SLATE, width=3)
            draw.text((right + 78, y - 15), f"{depth} m", fill=SLATE, font=tick_font)
    draw.text((right + 36, bottom + 72), "Depth guide", fill=NAVY, font=small_font)

    callout = (1368, 210, 1708, 560)
    draw.rounded_rectangle(callout, radius=24, fill=(236, 253, 245), outline=TEAL, width=3)
    draw.text((1398, 238), "How to read this", fill=TEAL, font=callout_font)
    draw_wrapped(
        draw,
        (1398, 300),
        "Higher pressure and lower temperature move conditions toward methane hydrate stability.",
        260,
        NAVY,
        small_font,
    )
    draw_wrapped(
        draw,
        (1398, 448),
        "Use with geology, logs, and core evidence; never as a standalone occurrence claim.",
        260,
        SLATE,
        small_font,
    )

    source_box = (92, 1000, 1708, 1105)
    draw.rounded_rectangle(source_box, radius=18, fill=(255, 251, 235), outline=(245, 158, 11), width=2)
    draw_wrapped(
        draw,
        (120, 1024),
        "Source: data/public_stability_products/phase_curve_methane_5ppt_screenshot_recovered_2026-06-18.csv, digitized from Lee et al. 2008 USGS SIR 2008-5175 Fig. 1A.",
        1530,
        (120, 53, 15),
        small_font,
    )

    image.save(PT_PNG)
    return PT_PNG


def build_contact_sheet() -> Path:
    slide_paths = sorted((ASSET_DIR / "rendered_slides").glob("slide_??_editable_rebuild.png"))
    if not slide_paths:
        raise FileNotFoundError(f"No exported slide PNGs found in {ASSET_DIR}")
    thumbs: list[Image.Image] = []
    thumb_w = 560
    for path in slide_paths:
        img = Image.open(path).convert("RGB")
        ratio = thumb_w / img.width
        thumb = img.resize((thumb_w, int(img.height * ratio)), Image.LANCZOS)
        thumbs.append(thumb)

    cols = 3
    pad = 32
    label_h = 38
    thumb_h = max(thumb.height for thumb in thumbs)
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new(
        "RGB",
        (cols * thumb_w + (cols + 1) * pad, rows * (thumb_h + label_h) + (rows + 1) * pad),
        LIGHT,
    )
    draw = ImageDraw.Draw(sheet)
    label_font = font(25, True)
    for index, thumb in enumerate(thumbs):
        col = index % cols
        row = index // cols
        x = pad + col * (thumb_w + pad)
        y = pad + row * (thumb_h + label_h + pad)
        draw.text((x, y), f"Slide {index + 1}", fill=NAVY, font=label_font)
        sheet.paste(thumb, (x, y + label_h))
        draw.rectangle((x, y + label_h, x + thumb.width, y + label_h + thumb.height), outline=GRID, width=2)

    sheet.save(CONTACT_SHEET)
    return CONTACT_SHEET


def build_drive_import_contact_sheet() -> Path:
    thumb_dir = ASSET_DIR / "drive_import_thumbnails"
    slide_paths = sorted(thumb_dir.glob("slide_??_drive_import.png"))
    if not slide_paths:
        raise FileNotFoundError(f"No Drive import thumbnails found in {thumb_dir}")

    thumbs: list[Image.Image] = []
    thumb_w = 560
    for path in slide_paths:
        img = Image.open(path).convert("RGB")
        ratio = thumb_w / img.width
        thumb = img.resize((thumb_w, int(img.height * ratio)), Image.LANCZOS)
        thumbs.append(thumb)

    cols = 3
    pad = 32
    label_h = 38
    thumb_h = max(thumb.height for thumb in thumbs)
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new(
        "RGB",
        (cols * thumb_w + (cols + 1) * pad, rows * (thumb_h + label_h) + (rows + 1) * pad),
        LIGHT,
    )
    draw = ImageDraw.Draw(sheet)
    label_font = font(25, True)
    for index, thumb in enumerate(thumbs):
        col = index % cols
        row = index // cols
        x = pad + col * (thumb_w + pad)
        y = pad + row * (thumb_h + label_h + pad)
        draw.text((x, y), f"Drive Slide {index + 1}", fill=NAVY, font=label_font)
        sheet.paste(thumb, (x, y + label_h))
        draw.rectangle((x, y + label_h, x + thumb.width, y + label_h + thumb.height), outline=GRID, width=2)

    sheet.save(DRIVE_CONTACT_SHEET)
    return DRIVE_CONTACT_SHEET


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pt", action="store_true", help="Render the P-T diagram only.")
    parser.add_argument("--contact-sheet", action="store_true", help="Build the contact sheet from exported slides.")
    parser.add_argument(
        "--drive-contact-sheet",
        action="store_true",
        help="Build the contact sheet from downloaded Drive import thumbnails.",
    )
    args = parser.parse_args()

    if args.pt:
        print(render_pt_diagram())
    if args.contact_sheet:
        print(build_contact_sheet())
    if args.drive_contact_sheet:
        print(build_drive_import_contact_sheet())
    if not args.pt and not args.contact_sheet and not args.drive_contact_sheet:
        print(render_pt_diagram())
        try:
            print(build_contact_sheet())
        except FileNotFoundError:
            pass
        try:
            print(build_drive_import_contact_sheet())
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    main()
