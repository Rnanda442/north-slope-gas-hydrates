from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path
import py_compile
import sys


REQUIRED_FILES = ['01_pipeline/inspect_three_dataset_headers.py', '01_pipeline/run_three_dataset_ml_pipeline.py', '01_pipeline/export_model_run_review_assets.py', 'code_transfer_block/multi_saturation_target_workflow.py', 'dashboard/runtime/three_dataset_pipeline.py', 'dashboard/runtime/model_run_tracker.py', 'dashboard/approved_data_intake.py', 'PACKAGE_MANIFEST.json']
EXPECTED_DATASET_FILENAMES = ['curated_dataset1.xlsx', 'curated_dataset2.xlsx', 'curated_dataset3.xlsx', 'wellnametodataset.txt']
FORBIDDEN_SUFFIXES = set(['.csv', '.dlis', '.env', '.feather', '.h5', '.hdf5', '.joblib', '.keras', '.las', '.onnx', '.parquet', '.pickle', '.pkl', '.pt', '.pth', '.sav', '.tsv', '.xls', '.xlsb', '.xlsx'])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify the DOE Jupyter code package without reading workbook rows.")
    parser.add_argument("--package-root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--data-dir", type=Path, help="Optional approved local data folder to check by filename only.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    package_root = args.package_root.resolve()
    missing = [name for name in REQUIRED_FILES if not (package_root / name).exists()]
    forbidden = [
        path.relative_to(package_root).as_posix()
        for path in package_root.rglob("*")
        if path.is_file() and path.suffix.lower() in FORBIDDEN_SUFFIXES and path.name != ".env.example"
    ]

    compile_errors = []
    for path in sorted(package_root.rglob("*.py")):
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as error:
            compile_errors.append({"file": path.relative_to(package_root).as_posix(), "error": str(error)})

    if str(package_root) not in sys.path:
        sys.path.insert(0, str(package_root))
    import_results = {}
    for module_name in [
        "dashboard.approved_data_intake",
        "dashboard.runtime.three_dataset_pipeline",
        "dashboard.runtime.model_run_tracker",
        "dashboard.source_visual_inventory",
        "dashboard.parameter_evidence",
    ]:
        try:
            importlib.import_module(module_name)
            import_results[module_name] = "ok"
        except Exception as error:
            import_results[module_name] = f"failed: {error}"

    dataset_status = {}
    if args.data_dir:
        data_dir = args.data_dir.resolve()
        dataset_status = {
            name: "present" if (data_dir / name).exists() else "missing"
            for name in EXPECTED_DATASET_FILENAMES
        }
    else:
        dataset_status = {name: "not checked; pass --data-dir to verify filename presence" for name in EXPECTED_DATASET_FILENAMES}

    summary = {
        "package_root": str(package_root),
        "required_files_missing": missing,
        "forbidden_files_present": forbidden,
        "py_compile_errors": compile_errors,
        "import_results": import_results,
        "expected_dataset_filenames": dataset_status,
        "status": "ok" if not missing and not forbidden and not compile_errors and all(value == "ok" for value in import_results.values()) else "needs_review",
        "note": "This verifier checks structure, imports, and filenames only; it does not read approved workbook rows.",
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    if summary["status"] != "ok":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
