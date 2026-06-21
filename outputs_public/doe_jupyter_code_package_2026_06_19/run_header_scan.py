"""Jupyter-friendly wrapper for three-workbook header inspection."""

from __future__ import annotations

from pathlib import Path
import runpy
import sys


PACKAGE_ROOT = Path(__file__).resolve().parent
TARGET_SCRIPT = PACKAGE_ROOT / '01_pipeline/inspect_three_dataset_headers.py'


def main() -> None:
    if str(PACKAGE_ROOT) not in sys.path:
        sys.path.insert(0, str(PACKAGE_ROOT))
    sys.argv[0] = str(TARGET_SCRIPT)
    runpy.run_path(str(TARGET_SCRIPT), run_name="__main__")


if __name__ == "__main__":
    main()
