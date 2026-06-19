from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import textwrap
from datetime import datetime, timezone
from zipfile import ZIP_DEFLATED, ZipFile


PACKAGE_NAME = "doe_jupyter_code_package_2026_06_19"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_PUBLIC = PROJECT_ROOT / "outputs_public"
PACKAGE_ROOT = OUTPUTS_PUBLIC / PACKAGE_NAME
ZIP_PATH = OUTPUTS_PUBLIC / f"{PACKAGE_NAME}.zip"

EXPECTED_DATASET_FILENAMES = (
    "curated_dataset1.xlsx",
    "curated_dataset2.xlsx",
    "curated_dataset3.xlsx",
    "wellnametodataset.txt",
)

COPIED_FILES = (
    "01_pipeline/inspect_three_dataset_headers.py",
    "01_pipeline/run_three_dataset_ml_pipeline.py",
    "01_pipeline/export_model_run_review_assets.py",
    "01_pipeline/generate_doe_equation_derived_visuals.py",
    "01_pipeline/generate_slide_paper_visuals_2026_06_18.py",
    "code_transfer_block/inspect_three_dataset_headers_standalone.py",
    "code_transfer_block/multi_saturation_target_workflow.py",
    "dashboard/__init__.py",
    "dashboard/approved_data_intake.py",
    "dashboard/source_visual_inventory.py",
    "dashboard/parameter_evidence.py",
    "docs/opensciencelab_runtime_layout.md",
    "docs/DOE_THREE_DATASET_ML_PIPELINE_RUNBOOK_2026-06-16.md",
    "docs/DOE_RUNTIME_PRESENTATION_AND_MODEL_TRACKING_PLAN_2026-06-16.md",
    "docs/ANACONDA_DEPENDENCY_REQUEST_2026-06-16.md",
)

FORBIDDEN_SUFFIXES = {
    ".xlsx",
    ".xls",
    ".xlsb",
    ".las",
    ".dlis",
    ".csv",
    ".tsv",
    ".parquet",
    ".feather",
    ".pkl",
    ".pickle",
    ".joblib",
    ".sav",
    ".h5",
    ".hdf5",
    ".keras",
    ".onnx",
    ".pt",
    ".pth",
    ".env",
}


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def package_rel(path: Path) -> str:
    return path.relative_to(PACKAGE_ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(body).strip() + "\n", encoding="utf-8")


def copied_file_list() -> list[str]:
    runtime_files = sorted(path.as_posix() for path in Path("dashboard/runtime").glob("*.py"))
    return sorted({*COPIED_FILES, *runtime_files})


def copy_public_safe_sources() -> list[str]:
    copied: list[str] = []
    for relative in copied_file_list():
        source = PROJECT_ROOT / relative
        if not source.exists():
            raise FileNotFoundError(f"Required package source is missing: {relative}")
        destination = PACKAGE_ROOT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        copied.append(package_rel(destination))
    return copied


def write_readme() -> str:
    path = PACKAGE_ROOT / "README_DOE_JUPYTER_CODE_PACKAGE_2026_06_19.md"
    write_text(
        path,
        f"""
        # DOE Jupyter Code Package 2026-06-19

        This package is a GitHub-safe code transfer bundle for running the
        North Slope three-workbook ML workflow on the DOE desktop or another
        approved runtime machine. It contains code, docs, wrappers, and package
        manifests only. It does not contain approved workbook rows, LAS files,
        private well identifiers, runtime predictions, fitted models, fitted
        scalers, credentialed PDFs, or private configs.

        ## Expected Local Data Files

        Place the real approved files in a local folder outside GitHub, such as
        a DOE-approved data directory:

        - `curated_dataset1.xlsx`
        - `curated_dataset2.xlsx`
        - `curated_dataset3.xlsx`
        - `wellnametodataset.txt` optional, if approved and available

        Do not copy those files into this package folder unless the folder is
        outside the Git worktree. Never commit them.

        ## Quick Start In Anaconda Prompt

        ```powershell
        conda activate north_slope_hydrates
        cd <unzipped package folder>
        python verify_package.py
        python verify_package.py --data-dir "<approved data folder>"
        python run_header_scan.py --data-dir "<approved data folder>"
        python run_three_dataset_baseline.py --data-dir "<approved data folder>" --target auto --model baseline
        python run_three_dataset_baseline.py --data-dir "<approved data folder>" --target auto --model mlp
        python run_model_run_review_assets.py --project-root . --output-dir outputs_runtime/model_run_review_assets_current
        ```

        The wrapper scripts forward arguments to the original repo entry
        points while preserving the package-root import layout.

        ## Jupyter-Friendly Use

        In a notebook cell, use shell commands from the package root:

        ```python
        !python verify_package.py --data-dir r"<approved data folder>"
        !python run_header_scan.py --data-dir r"<approved data folder>"
        !python run_three_dataset_baseline.py --data-dir r"<approved data folder>" --target auto --model baseline
        ```

        If the header scan finds a verified target column, rerun with the exact
        target:

        ```python
        !python run_three_dataset_baseline.py --data-dir r"<approved data folder>" --target "EXACT_TARGET_COLUMN" --model baseline
        ```

        ## Runtime Output Boundary

        Runtime outputs belong under ignored local folders:

        - `outputs_runtime/`
        - `models_runtime/`
        - `logs_runtime/`
        - `configs_local/`

        Do not push raw data, row-level predictions, trained model files,
        fitted scalers, private runtime manifests, or private well identifiers
        to GitHub. Public-safe summaries must be reviewed before publication.

        ## Included Code Areas

        - Three-workbook header inspection and ML runners under `01_pipeline/`
        - Multi-saturation workflow under `code_transfer_block/`
        - Runtime helpers under `dashboard/runtime/`
        - Approved-data intake and row-free source/model helpers under `dashboard/`
        - DOE runtime/runbook docs under `docs/`

        See `PACKAGE_MANIFEST.json` for the exact file list and checksums.
        """,
    )
    return package_rel(path)


def write_env_example() -> str:
    path = PACKAGE_ROOT / ".env.example"
    write_text(
        path,
        """
        DOE_DATA_DIR=
        DOE_OUTPUT_ROOT=
        DOE_MODEL_ROOT=
        DOE_RUN_LABEL=
        DOE_TARGET_COLUMN=
        """,
    )
    return package_rel(path)


def write_package_gitignore() -> str:
    path = PACKAGE_ROOT / ".gitignore"
    write_text(
        path,
        """
        data_runtime/
        outputs_runtime/
        models_runtime/
        logs_runtime/
        configs_local/
        *.xlsx
        *.xls
        *.xlsb
        *.las
        *.dlis
        *.csv
        *.tsv
        *.parquet
        *.feather
        *.pkl
        *.pickle
        *.joblib
        *.sav
        *.h5
        *.hdf5
        *.keras
        *.onnx
        *.pt
        *.pth
        .env
        __pycache__/
        *.pyc
        """,
    )
    return package_rel(path)


def write_exclude_rules() -> str:
    path = PACKAGE_ROOT / "PACKAGE_EXCLUDE_RULES.md"
    write_text(
        path,
        """
        # Package Exclude Rules

        This transfer package is code only.

        Excluded from this package and from GitHub:

        - approved workbook rows and raw workbook files;
        - LAS/DLIS/log-source files and private source packages;
        - row-level predictions and runtime scoring tables;
        - trained models, fitted scalers, serialized pipelines, and notebooks
          with embedded private outputs;
        - credentialed PDFs, private screenshots, secrets, and local config
          files;
        - runtime manifests containing private absolute paths or identifiers.

        Public-safe derived summaries can be proposed for review only after a
        separate row-free/sensitive-token audit.
        """,
    )
    return package_rel(path)


def write_wrapper(path: Path, target_script: str, description: str) -> str:
    write_text(
        path,
        f'''
        """{description}"""

        from __future__ import annotations

        from pathlib import Path
        import runpy
        import sys


        PACKAGE_ROOT = Path(__file__).resolve().parent
        TARGET_SCRIPT = PACKAGE_ROOT / {target_script!r}


        def main() -> None:
            if str(PACKAGE_ROOT) not in sys.path:
                sys.path.insert(0, str(PACKAGE_ROOT))
            sys.argv[0] = str(TARGET_SCRIPT)
            runpy.run_path(str(TARGET_SCRIPT), run_name="__main__")


        if __name__ == "__main__":
            main()
        ''',
    )
    return package_rel(path)


def write_wrappers() -> list[str]:
    return [
        write_wrapper(
            PACKAGE_ROOT / "run_header_scan.py",
            "01_pipeline/inspect_three_dataset_headers.py",
            "Jupyter-friendly wrapper for three-workbook header inspection.",
        ),
        write_wrapper(
            PACKAGE_ROOT / "run_three_dataset_baseline.py",
            "01_pipeline/run_three_dataset_ml_pipeline.py",
            "Jupyter-friendly wrapper for the three-workbook baseline/MLP workflow.",
        ),
        write_wrapper(
            PACKAGE_ROOT / "run_model_run_review_assets.py",
            "01_pipeline/export_model_run_review_assets.py",
            "Jupyter-friendly wrapper for row-free model-run review exports.",
        ),
        write_wrapper(
            PACKAGE_ROOT / "run_multi_saturation.py",
            "code_transfer_block/multi_saturation_target_workflow.py",
            "Jupyter-friendly wrapper for the standalone multi-saturation workflow.",
        ),
    ]


def write_verify_script() -> str:
    path = PACKAGE_ROOT / "verify_package.py"
    required_files_literal = repr(
        [
            "01_pipeline/inspect_three_dataset_headers.py",
            "01_pipeline/run_three_dataset_ml_pipeline.py",
            "01_pipeline/export_model_run_review_assets.py",
            "code_transfer_block/multi_saturation_target_workflow.py",
            "dashboard/runtime/three_dataset_pipeline.py",
            "dashboard/runtime/model_run_tracker.py",
            "dashboard/approved_data_intake.py",
            "PACKAGE_MANIFEST.json",
        ]
    )
    expected_files_literal = repr(list(EXPECTED_DATASET_FILENAMES))
    forbidden_suffixes_literal = repr(sorted(FORBIDDEN_SUFFIXES))
    write_text(
        path,
        f'''
        from __future__ import annotations

        import argparse
        import importlib
        import json
        from pathlib import Path
        import py_compile
        import sys


        REQUIRED_FILES = {required_files_literal}
        EXPECTED_DATASET_FILENAMES = {expected_files_literal}
        FORBIDDEN_SUFFIXES = set({forbidden_suffixes_literal})


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
                    compile_errors.append({{"file": path.relative_to(package_root).as_posix(), "error": str(error)}})

            if str(package_root) not in sys.path:
                sys.path.insert(0, str(package_root))
            import_results = {{}}
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
                    import_results[module_name] = f"failed: {{error}}"

            dataset_status = {{}}
            if args.data_dir:
                data_dir = args.data_dir.resolve()
                dataset_status = {{
                    name: "present" if (data_dir / name).exists() else "missing"
                    for name in EXPECTED_DATASET_FILENAMES
                }}
            else:
                dataset_status = {{name: "not checked; pass --data-dir to verify filename presence" for name in EXPECTED_DATASET_FILENAMES}}

            summary = {{
                "package_root": str(package_root),
                "required_files_missing": missing,
                "forbidden_files_present": forbidden,
                "py_compile_errors": compile_errors,
                "import_results": import_results,
                "expected_dataset_filenames": dataset_status,
                "status": "ok" if not missing and not forbidden and not compile_errors and all(value == "ok" for value in import_results.values()) else "needs_review",
                "note": "This verifier checks structure, imports, and filenames only; it does not read approved workbook rows.",
            }}
            print(json.dumps(summary, indent=2, sort_keys=True))
            if summary["status"] != "ok":
                raise SystemExit(1)


        if __name__ == "__main__":
            main()
        ''',
    )
    return package_rel(path)


def file_manifest() -> list[dict[str, object]]:
    rows = []
    for path in sorted(PACKAGE_ROOT.rglob("*")):
        if not path.is_file():
            continue
        rows.append(
            {
                "path": package_rel(path),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    return rows


def write_manifest(generated_files: list[str], copied_files: list[str]) -> str:
    manifest_path = PACKAGE_ROOT / "PACKAGE_MANIFEST.json"
    manifest = {
        "package_name": PACKAGE_NAME,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_repo": "Rnanda442/north-slope-gas-hydrates",
        "package_scope": "GitHub-safe code/docs/wrappers only; no data rows or runtime outputs.",
        "expected_dataset_filenames": list(EXPECTED_DATASET_FILENAMES),
        "copied_files": copied_files,
        "generated_files": sorted(generated_files),
        "excluded_suffixes": sorted(FORBIDDEN_SUFFIXES),
        "files": [],
    }
    write_text(manifest_path, json.dumps(manifest, indent=2, sort_keys=True))
    manifest["files"] = file_manifest()
    write_text(manifest_path, json.dumps(manifest, indent=2, sort_keys=True))
    return package_rel(manifest_path)


def verify_no_forbidden_files() -> None:
    forbidden = [
        path
        for path in PACKAGE_ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in FORBIDDEN_SUFFIXES and path.name != ".env.example"
    ]
    if forbidden:
        formatted = "\n".join(package_rel(path) for path in forbidden)
        raise RuntimeError(f"Forbidden file types were included:\n{formatted}")


def write_zip() -> None:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with ZipFile(ZIP_PATH, "w", compression=ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE_ROOT.rglob("*")):
            if path.is_file():
                archive.write(path, f"{PACKAGE_NAME}/{package_rel(path)}")


def main() -> None:
    outputs_public = OUTPUTS_PUBLIC.resolve()
    package_root = PACKAGE_ROOT.resolve()
    if outputs_public not in package_root.parents:
        raise RuntimeError(f"Refusing to rebuild package outside outputs_public: {package_root}")
    if PACKAGE_ROOT.exists():
        shutil.rmtree(PACKAGE_ROOT)
    PACKAGE_ROOT.mkdir(parents=True, exist_ok=True)

    copied = copy_public_safe_sources()
    generated = [
        write_readme(),
        write_env_example(),
        write_package_gitignore(),
        write_exclude_rules(),
        write_verify_script(),
        *write_wrappers(),
    ]
    generated.append(write_manifest(generated, copied))
    verify_no_forbidden_files()
    write_zip()
    print(
        json.dumps(
            {
                "package": rel(PACKAGE_ROOT),
                "zip": rel(ZIP_PATH),
                "copied_file_count": len(copied),
                "generated_file_count": len(generated),
                "zip_bytes": ZIP_PATH.stat().st_size,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
