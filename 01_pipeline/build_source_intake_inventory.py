from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dashboard.source_intake_inventory import (  # noqa: E402
    DEFAULT_SOURCE_EXTENSIONS,
    build_source_intake_inventory,
    default_source_library_index_dir,
    source_intake_summary,
    write_source_intake_outputs,
)


DEFAULT_SOURCE_DIRS = [
    PROJECT_ROOT / "references",
    PROJECT_ROOT
    / "docs"
    / "evidence"
    / "slide02_source_bundle_2026_06_17",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a public-safe source intake inventory from local PDF/screenshot/source "
            "folders without copying raw PDFs into GitHub."
        )
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        action="append",
        dest="source_dirs",
        help=(
            "Folder or file to scan. Repeat for Drive exports, Gmail attachment "
            "folders, screenshots, and project-generated stability visuals. Defaults "
            "to the repo's references folder and current stability visual package."
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=default_source_library_index_dir(PROJECT_ROOT),
        help="Folder for CSV and Markdown reports.",
    )
    parser.add_argument(
        "--date-tag",
        default=date.today().isoformat(),
        help="Date tag for output filenames, e.g. 2026-06-18.",
    )
    parser.add_argument(
        "--no-pdf-text",
        action="store_true",
        help="Skip first-page PDF text extraction and identify sources from filenames only.",
    )
    parser.add_argument(
        "--include-external-paths",
        action="store_true",
        help=(
            "Write full paths for source files outside the repo. Use only for private "
            "local reports; leave off before pushing to GitHub."
        ),
    )
    parser.add_argument(
        "--extension",
        action="append",
        dest="extensions",
        help="Optional extension filter. Repeat as needed, e.g. --extension .pdf --extension .png.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_dirs = args.source_dirs or DEFAULT_SOURCE_DIRS
    extensions = args.extensions or sorted(DEFAULT_SOURCE_EXTENSIONS)

    inventory = build_source_intake_inventory(
        source_dirs,
        project_root=PROJECT_ROOT,
        read_pdf_text=not args.no_pdf_text,
        include_external_paths=args.include_external_paths,
        extensions=extensions,
    )
    written = write_source_intake_outputs(
        inventory,
        output_dir=args.output_dir,
        date_tag=args.date_tag,
    )
    summary = source_intake_summary(inventory)

    print("Source intake inventory complete.")
    for label, path in written.items():
        print(f"{label}: {path}")
    print(f"found_local: {summary['found_local']}")
    print(f"expected_missing_or_drive_only: {summary['expected_missing_or_drive_only']}")
    print(f"found_local_unmatched_review: {summary['found_local_unmatched_review']}")


if __name__ == "__main__":
    main()
