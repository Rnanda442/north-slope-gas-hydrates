from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
ASSET_DIR = (
    ROOT
    / "docs"
    / "project_blueprints"
    / "presentation_assets"
    / "editable_visual_match_2026_06_19"
)
REFERENCE_DIR = ASSET_DIR / "reference_drive_panels"
CROP_DIR = ASSET_DIR / "cropped_reference_assets"
RENDER_DIR = ASSET_DIR / "rendered_slides"
DRIVE_THUMBNAIL_DIR = ASSET_DIR / "drive_import_thumbnails"
CONTACT_SHEET = ASSET_DIR / "editable_visual_match_contact_sheet_2026_06_19.png"
REFERENCE_CONTACT_SHEET = ASSET_DIR / "reference_drive_contact_sheet_2026_06_19.png"
DRIVE_CONTACT_SHEET = ASSET_DIR / "drive_import_contact_sheet_2026_06_19.png"
WEBSITE_MAP_DIR = (
    ROOT
    / "docs"
    / "project_blueprints"
    / "presentation_assets"
    / "website_well_maps_2026_06_18"
)


LIGHT = (248, 250, 252)
GRID = (203, 213, 225)
NAVY = (15, 23, 42)


def build_slide07_unified_map_only_panel() -> Path:
    source = WEBSITE_MAP_DIR / "unified_north_slope_well_stability_context_map_2026_06_18.png"
    if not source.exists():
        raise FileNotFoundError(source)

    image = Image.open(source).convert("RGB")
    # Crop out the baked title/sidebar so Slide 7 can use editable PowerPoint
    # labels and callouts around the GIS map image.
    left = int(image.width * 0.035)
    top = int(image.height * 0.145)
    right = int(image.width * 0.735)
    bottom = int(image.height * 0.785)
    crop = image.crop((left, top, right, bottom))

    panel_w, panel_h = 1500, 820
    canvas = Image.new("RGB", (panel_w, panel_h), (255, 255, 255))
    ratio = min(panel_w / crop.width, panel_h / crop.height)
    resized = crop.resize((int(crop.width * ratio), int(crop.height * ratio)), Image.LANCZOS)
    x = (panel_w - resized.width) // 2
    y = (panel_h - resized.height) // 2
    canvas.paste(resized, (x, y))
    output = CROP_DIR / "slide07_unified_map_only_panel.png"
    canvas.save(output)
    return output


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
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


def crop_reference_assets() -> list[Path]:
    CROP_DIR.mkdir(parents=True, exist_ok=True)
    crops: list[tuple[str, str, tuple[int, int, int, int]]] = [
        ("slide_01_personal_about_me_v5_5_reference.png", "slide01_drawing.png", (66, 359, 434, 727)),
        ("slide_01_personal_about_me_v5_5_reference.png", "slide01_rap_caviar.png", (463, 359, 684, 584)),
        ("slide_01_personal_about_me_v5_5_reference.png", "slide01_world_cup.png", (463, 604, 684, 728)),
        ("slide_01_personal_about_me_v5_5_reference.png", "slide01_photo.png", (984, 133, 1468, 751)),
        ("slide_02_source_context_v5_5_reference.png", "slide02_hydrate_structure_panel.png", (84, 274, 586, 604)),
        ("slide_02_source_context_v5_5_reference.png", "slide02_north_slope_map_panel.png", (632, 238, 1233, 640)),
        ("slide_02_source_context_v5_5_reference.png", "slide02_stability_curve_panel.png", (1273, 244, 1518, 496)),
        ("slide_04_full_complex_project_workflow_v5_5_reference.png", "slide04_architecture_body.png", (0, 92, 1600, 842)),
        ("slide_07_complex_ml_runtime_architecture_v5_5_reference.png", "slide07_runtime_body.png", (0, 92, 1600, 842)),
    ]
    outputs: list[Path] = []
    for source_name, output_name, box in crops:
        source = REFERENCE_DIR / source_name
        if not source.exists():
            raise FileNotFoundError(source)
        image = Image.open(source).convert("RGB")
        output = CROP_DIR / output_name
        image.crop(box).save(output)
        outputs.append(output)
    outputs.append(build_slide07_unified_map_only_panel())
    return outputs


def build_contact_sheet(
    input_dir: Path,
    pattern: str,
    output: Path,
    label_prefix: str,
) -> Path:
    paths = sorted(input_dir.glob(pattern))
    if not paths:
        raise FileNotFoundError(f"No images found in {input_dir} matching {pattern}")

    thumbs: list[Image.Image] = []
    thumb_w = 560
    for path in paths:
        img = Image.open(path).convert("RGB")
        ratio = thumb_w / img.width
        thumbs.append(img.resize((thumb_w, int(img.height * ratio)), Image.LANCZOS))

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
        draw.text((x, y), f"{label_prefix} {index + 1}", fill=NAVY, font=label_font)
        sheet.paste(thumb, (x, y + label_h))
        draw.rectangle((x, y + label_h, x + thumb.width, y + label_h + thumb.height), outline=GRID, width=2)

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--crop", action="store_true")
    parser.add_argument("--contact-sheet", action="store_true")
    parser.add_argument("--reference-contact-sheet", action="store_true")
    parser.add_argument("--drive-contact-sheet", action="store_true")
    args = parser.parse_args()

    ran = False
    if args.crop:
        for path in crop_reference_assets():
            print(path)
        ran = True
    if args.contact_sheet:
        print(build_contact_sheet(RENDER_DIR, "slide_??_editable_visual_match.png", CONTACT_SHEET, "Slide"))
        ran = True
    if args.reference_contact_sheet:
        print(build_contact_sheet(REFERENCE_DIR, "slide_??_*.png", REFERENCE_CONTACT_SHEET, "Reference Slide"))
        ran = True
    if args.drive_contact_sheet:
        print(
            build_contact_sheet(
                DRIVE_THUMBNAIL_DIR,
                "slide_??_drive_visual_match.png",
                DRIVE_CONTACT_SHEET,
                "Drive Slide",
            )
        )
        ran = True
    if not ran:
        for path in crop_reference_assets():
            print(path)


if __name__ == "__main__":
    main()
