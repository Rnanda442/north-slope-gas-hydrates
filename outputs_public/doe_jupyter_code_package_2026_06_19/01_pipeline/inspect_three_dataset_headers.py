from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dashboard.runtime.three_dataset_pipeline import (
    DEFAULT_TEST_FILES,
    DEFAULT_TRAIN_FILE,
    scan_three_dataset_headers,
)


def default_data_dir() -> Path:
    return Path.home() / "Downloads" / "Northslopedatasets06052026"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect the three approved Excel workbooks and print sheet/header/target hints."
    )
    parser.add_argument("--data-dir", type=Path, default=default_data_dir())
    parser.add_argument("--files", nargs="+", default=[DEFAULT_TRAIN_FILE, *DEFAULT_TEST_FILES])
    parser.add_argument("--sample-rows", type=int, default=25)
    parser.add_argument("--output-root", type=Path, default=PROJECT_ROOT / "outputs_runtime")
    parser.add_argument("--run-label")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = scan_three_dataset_headers(
        args.data_dir,
        files=tuple(args.files),
        sample_rows=args.sample_rows,
        output_root=args.output_root,
        run_label=args.run_label,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    print()
    print("Open these CSVs if the terminal output is too cramped:")
    print(result["column_inventory"])
    print(result["target_header_hints"])
    print()
    if result["target_hint_count"]:
        print("Possible target headers were found. Check target_header_hints.csv, then rerun the ML pipeline with the suggested command.")
    else:
        print("No target-like headers were found by name. Open workbook_column_inventory.csv and pick the target column manually if one exists.")


if __name__ == "__main__":
    main()
