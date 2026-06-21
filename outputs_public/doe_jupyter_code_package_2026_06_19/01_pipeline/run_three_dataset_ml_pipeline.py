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
    run_three_dataset_pipeline,
)


def default_data_dir() -> Path:
    return Path.home() / "Downloads" / "Northslopedatasets06052026"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the local approved-runtime three-workbook ML pipeline. "
            "Default split: curated_dataset1.xlsx trains; curated_dataset2/3.xlsx are external tests."
        )
    )
    parser.add_argument("--data-dir", type=Path, default=default_data_dir())
    parser.add_argument("--train", default=DEFAULT_TRAIN_FILE)
    parser.add_argument("--test", nargs="+", default=list(DEFAULT_TEST_FILES))
    parser.add_argument("--sheet", help="Optional sheet name. By default the first non-empty sheet is used.")
    parser.add_argument("--target", default="auto", help="Target column name, or auto.")
    parser.add_argument(
        "--target-task",
        choices=["auto", "regression", "classification"],
        default="auto",
        help="Use regression for saturation targets and classification for occurrence/phase targets.",
    )
    parser.add_argument(
        "--model",
        choices=["baseline", "mlp"],
        default="baseline",
        help="baseline uses random forests; mlp uses a small sklearn neural-network prototype.",
    )
    parser.add_argument("--output-root", type=Path, default=PROJECT_ROOT / "outputs_runtime")
    parser.add_argument("--model-root", type=Path, default=PROJECT_ROOT / "models_runtime")
    parser.add_argument("--run-label", help="Optional folder name for this run under outputs_runtime/models_runtime.")
    parser.add_argument("--random-state", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_three_dataset_pipeline(
        data_dir=args.data_dir,
        train_file=args.train,
        test_files=tuple(args.test),
        sheet_name=args.sheet,
        requested_target=args.target,
        requested_task=args.target_task,
        model_kind=args.model,
        output_root=args.output_root,
        model_root=args.model_root,
        random_state=args.random_state,
        run_label=args.run_label,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    print()
    if result["status"] == "trained":
        print("Run complete. Review metrics and predictions inside the ignored runtime output folder.")
    else:
        print("Readiness outputs were written, but model training did not run.")
        print(f"Blocked reason: {result['blocked_reason']}")


if __name__ == "__main__":
    main()
