from __future__ import annotations

import argparse
from datetime import datetime
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


KEY_REPO_MARKERS = (
    "PROJECT_CONTEXT.md",
    "01_pipeline/run_three_dataset_ml_pipeline.py",
    "code_transfer_block/multi_saturation_target_workflow.py",
)

DEFAULT_WORKBOOKS = (
    "curated_dataset1.xlsx",
    "curated_dataset2.xlsx",
    "curated_dataset3.xlsx",
)


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if all((candidate / marker).exists() for marker in KEY_REPO_MARKERS):
            return candidate
    raise FileNotFoundError(
        "Could not find repo root. Run this from inside the north-slope-gas-hydrates repo "
        "or pass --repo-root."
    )


def timestamp_label() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def read_config(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def as_path(value: str | None, default: Path) -> Path:
    if value:
        return Path(value).expanduser()
    return default


def run_command(command: list[str], *, cwd: Path, required: bool = True) -> dict[str, Any]:
    print("\n$", " ".join(str(part) for part in command))
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if completed.stdout:
        print(completed.stdout)
    if completed.stderr:
        print(completed.stderr, file=sys.stderr)
    if required and completed.returncode != 0:
        raise subprocess.CalledProcessError(completed.returncode, command, completed.stdout, completed.stderr)
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout[-1200:] if completed.stdout else "",
        "stderr_tail": completed.stderr[-1200:] if completed.stderr else "",
    }


def compile_checks(repo_root: Path) -> list[dict[str, Any]]:
    scripts = [
        "01_pipeline/inspect_three_dataset_headers.py",
        "01_pipeline/run_three_dataset_ml_pipeline.py",
        "01_pipeline/export_model_run_review_assets.py",
        "01_pipeline/generate_slide_paper_visuals_2026_06_18.py",
        "01_pipeline/generate_doe_equation_derived_visuals.py",
        "code_transfer_block/multi_saturation_target_workflow.py",
        "doe_jupyter_runtime_pack/run_public_safe_ml_graph_exports.py",
    ]
    results = []
    for script in scripts:
        results.append(run_command([sys.executable, "-m", "py_compile", script], cwd=repo_root))
    return results


def module_available(module_name: str) -> bool:
    return importlib.util.find_spec(module_name) is not None


def skipped_command(label: str, reason: str) -> dict[str, Any]:
    print(f"\nSkipping {label}: {reason}")
    return {
        "command": [f"skipped:{label}"],
        "returncode": None,
        "stdout_tail": "",
        "stderr_tail": reason,
    }


def validate_workbooks(data_dir: Path, workbooks: list[str]) -> list[dict[str, str]]:
    rows = []
    for workbook in workbooks:
        path = data_dir / workbook
        rows.append(
            {
                "workbook": workbook,
                "path": str(path),
                "status": "found" if path.exists() else "missing",
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run DOE-local ML graph and audit exports without committing approved data."
    )
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--data-dir", type=Path, help="Folder containing curated_dataset1/2/3.xlsx.")
    parser.add_argument("--output-root", type=Path, help="Ignored runtime output root.")
    parser.add_argument("--run-single-target-pipeline", action="store_true")
    parser.add_argument("--skip-slide-paper-visuals", action="store_true")
    parser.add_argument("--skip-spatial-stability-join", action="store_true")
    parser.add_argument("--equation-input", type=Path, help="Optional approved local CSV/XLSX/parquet table.")
    parser.add_argument("--equation-sheet", help="Optional Excel sheet for equation input.")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve() if args.repo_root else find_repo_root(Path.cwd().resolve())
    config = read_config(args.config)

    data_dir = as_path(
        str(args.data_dir) if args.data_dir else config.get("data_dir"),
        Path.home() / "Downloads" / "Northslopedatasets06052026",
    )
    workbooks = list(config.get("workbooks") or DEFAULT_WORKBOOKS)
    train_workbook = str(config.get("train_workbook", DEFAULT_WORKBOOKS[0]))
    test_workbooks = list(config.get("test_workbooks") or [name for name in workbooks if name != train_workbook])
    target = str(config.get("target", "auto"))
    target_task = str(config.get("target_task", "auto"))
    model = str(config.get("model", "baseline"))
    include_training_fit = bool(config.get("include_training_fit_metrics", False))
    run_single_target = bool(config.get("run_single_target_pipeline", False)) or args.run_single_target_pipeline
    run_slide_paper_visuals = bool(config.get("run_slide_paper_visuals", True)) and not args.skip_slide_paper_visuals
    run_spatial_join = bool(config.get("run_spatial_stability_join", True)) and not args.skip_spatial_stability_join
    case_wells_csv = Path(config.get("case_wells_csv", "data/public_ml_products/four_well_case_location_index_2026-06-19.csv"))
    if not case_wells_csv.is_absolute():
        case_wells_csv = repo_root / case_wells_csv
    case_roles = [str(role) for role in config.get("case_roles", ["workbook_header_anchor", "public_source_case"])]
    nearby_count = int(config.get("nearby_stability_points_per_case", 5))
    temperature_gradient_csv = None
    if config.get("temperature_gradient_csv"):
        temperature_gradient_csv = Path(config["temperature_gradient_csv"]).expanduser()
    equation_input = args.equation_input or (Path(config["equation_input"]) if config.get("equation_input") else None)
    equation_sheet = args.equation_sheet if args.equation_sheet is not None else config.get("equation_sheet")

    output_root = as_path(
        str(args.output_root) if args.output_root else None,
        repo_root / "outputs_runtime" / f"doe_jupyter_pack_{timestamp_label()}",
    )
    output_root.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, Any] = {
        "repo_root": str(repo_root),
        "data_dir": str(data_dir),
        "output_root": str(output_root),
        "guardrail": "Local runtime export only; do not push approved rows, predictions, models, or populated configs.",
        "workbooks": validate_workbooks(data_dir, workbooks),
        "python_package_checks": {
            "sklearn": module_available("sklearn"),
            "plotly": module_available("plotly"),
            "PIL": module_available("PIL"),
            "pandas": module_available("pandas"),
        },
        "commands": [],
    }

    manifest["commands"].extend(compile_checks(repo_root))

    header_output = output_root / "header_scan"
    manifest["commands"].append(
        run_command(
            [
                sys.executable,
                "01_pipeline/inspect_three_dataset_headers.py",
                "--data-dir",
                str(data_dir),
                "--files",
                *workbooks,
                "--output-root",
                str(output_root),
                "--run-label",
                header_output.name,
            ],
            cwd=repo_root,
        )
    )

    if module_available("sklearn"):
        multi_output = output_root / "multi_saturation"
        manifest["commands"].append(
            run_command(
                [
                    sys.executable,
                    "code_transfer_block/multi_saturation_target_workflow.py",
                    "--data-dir",
                    str(data_dir),
                    "--workbooks",
                    *workbooks,
                    "--output-dir",
                    str(multi_output),
                ],
                cwd=repo_root,
                required=False,
            )
        )
    else:
        manifest["commands"].append(
            skipped_command("multi_saturation", "scikit-learn is not installed in this Python environment.")
        )

    if run_single_target and module_available("sklearn"):
        single_output = output_root / "single_target_pipeline"
        model_output = output_root / "single_target_models"
        command = [
            sys.executable,
            "01_pipeline/run_three_dataset_ml_pipeline.py",
            "--data-dir",
            str(data_dir),
            "--train",
            train_workbook,
            "--test",
            *test_workbooks,
            "--target",
            target,
            "--target-task",
            target_task,
            "--model",
            model,
            "--output-root",
            str(single_output),
            "--model-root",
            str(model_output),
            "--run-label",
            str(config.get("run_label", "doe_jupyter_pack")),
        ]
        manifest["commands"].append(run_command(command, cwd=repo_root, required=False))
    elif run_single_target:
        manifest["commands"].append(
            skipped_command("single_target_pipeline", "scikit-learn is not installed in this Python environment.")
        )

    if run_spatial_join:
        spatial_output = output_root / "spatial_stability_join"
        spatial_command = [
            sys.executable,
            "doe_jupyter_runtime_pack/run_spatial_stability_join.py",
            "--repo-root",
            str(repo_root),
            "--case-wells-csv",
            str(case_wells_csv),
            "--output-dir",
            str(spatial_output),
            "--case-roles",
            *case_roles,
            "--nearby-count",
            str(nearby_count),
        ]
        if temperature_gradient_csv is not None:
            spatial_command.extend(["--temperature-gradient-csv", str(temperature_gradient_csv)])
        manifest["commands"].append(run_command(spatial_command, cwd=repo_root, required=False))

    review_output = output_root / "model_run_review_assets"
    review_command = [
        sys.executable,
        "01_pipeline/export_model_run_review_assets.py",
        "--project-root",
        str(repo_root),
        "--output-dir",
        str(review_output),
    ]
    if include_training_fit:
        review_command.append("--include-training-fit-metrics")
    manifest["commands"].append(run_command(review_command, cwd=repo_root, required=False))

    if run_slide_paper_visuals:
        manifest["commands"].append(
            run_command(
                [
                    sys.executable,
                    "01_pipeline/generate_slide_paper_visuals_2026_06_18.py",
                    "--data-dir",
                    str(data_dir),
                ],
                cwd=repo_root,
                required=False,
            )
        )

    if equation_input:
        equation_output = output_root / "equation_visuals"
        equation_command = [
            sys.executable,
            "01_pipeline/generate_doe_equation_derived_visuals.py",
            "--input",
            str(equation_input),
            "--out-dir",
            str(equation_output),
        ]
        if equation_sheet:
            equation_command.extend(["--sheet", str(equation_sheet)])
        manifest["commands"].append(run_command(equation_command, cwd=repo_root, required=False))

    manifest_path = output_root / "doe_jupyter_pack_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    print("\nDOE Jupyter runtime pack complete.")
    print(f"Manifest: {manifest_path}")
    print("Keep outputs_runtime local/ignored unless a public-safe release is reviewed and approved.")


if __name__ == "__main__":
    main()
