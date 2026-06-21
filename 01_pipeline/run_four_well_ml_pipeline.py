from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dashboard.runtime.four_well_runtime import (
    DEFAULT_CORE_FILE,
    DEFAULT_LOG_FILE,
    DEFAULT_SPLIT_FILE,
    run_four_well_runtime_pipeline,
)


def default_data_dir() -> Path:
    return PROJECT_ROOT / "approved_runtime" / "four_well"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the four-well North Slope hydrate ML runtime package. "
            "Put approved DOE/local CSV rows in an ignored data directory, then use this runner "
            "to join public four-well identity, public stability context, optional core samples, "
            "and approved saturation or occurrence targets."
        )
    )
    parser.add_argument("--data-dir", type=Path, default=default_data_dir())
    parser.add_argument("--logs", default=DEFAULT_LOG_FILE, help="Combined four-well log CSV inside --data-dir.")
    parser.add_argument(
        "--core",
        default=DEFAULT_CORE_FILE,
        help="Optional core or pressure-core sample CSV inside --data-dir. Use --core '' to skip.",
    )
    parser.add_argument(
        "--split",
        default=DEFAULT_SPLIT_FILE,
        help="Split-registry CSV inside --data-dir. Falls back to public template if omitted or absent.",
    )
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
    parser.add_argument("--run-label", help="Optional folder name for this run.")
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--max-core-offset-m", type=float, default=3.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    core_file = args.core if args.core else None
    split_file = args.split if args.split else None
    result = run_four_well_runtime_pipeline(
        project_root=PROJECT_ROOT,
        data_dir=args.data_dir,
        logs_file=args.logs,
        core_file=core_file,
        split_file=split_file,
        requested_target=args.target,
        requested_task=args.target_task,
        model_kind=args.model,
        output_root=args.output_root,
        model_root=args.model_root,
        run_label=args.run_label,
        random_state=args.random_state,
        max_core_offset_m=args.max_core_offset_m,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    print()
    if result["status"] == "trained":
        print("Run complete. Review metrics, predictions, and core overlays inside the ignored runtime output folder.")
    else:
        print("Readiness outputs were written, but model training did not run.")
        print(f"Blocked reason: {result['blocked_reason']}")


if __name__ == "__main__":
    main()
