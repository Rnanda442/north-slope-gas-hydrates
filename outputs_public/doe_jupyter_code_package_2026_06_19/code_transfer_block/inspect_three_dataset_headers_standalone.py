from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import pandas as pd


TARGET_WORDS = (
    "sgh",
    "s_h",
    "sh",
    "sat",
    "saturation",
    "hydrate",
    "nmr_sat",
    "class",
    "label",
    "phase",
    "occurrence",
    "target",
)
FEATURE_WORDS = (
    "well",
    "depth",
    "gr",
    "gamma",
    "rt",
    "res",
    "rhob",
    "density",
    "por",
    "phi",
    "vp",
    "vs",
    "dt",
    "dts",
    "nmr",
    "caliper",
)


def normalize_header(value: object) -> str:
    return "".join(character for character in str(value).lower() if character.isalnum() or character == "_")


def role_hint(header: object) -> str:
    normalized = normalize_header(header)
    if any(word in normalized for word in TARGET_WORDS):
        return "possible_target"
    if any(word in normalized for word in FEATURE_WORDS):
        return "possible_feature_or_context"
    return "review"


def scan_workbooks(data_dir: Path, workbook_names: list[str], sample_rows: int, output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sheet_rows: list[dict[str, object]] = []
    column_rows: list[dict[str, object]] = []
    missing_files: list[str] = []

    for workbook_name in workbook_names:
        path = data_dir / workbook_name
        if not path.exists():
            missing_files.append(str(path))
            continue
        print(f"\n=== {path.name} ===")
        with pd.ExcelFile(path) as excel:
            sheet_names = list(excel.sheet_names)
        print("Sheets:", ", ".join(sheet_names))
        for sheet_name in sheet_names:
            frame = pd.read_excel(path, sheet_name=sheet_name, nrows=sample_rows)
            sheet_rows.append(
                {
                    "workbook": path.name,
                    "sheet_name": sheet_name,
                    "sampled_rows": len(frame),
                    "column_count": len(frame.columns),
                    "has_target_like_header": any(role_hint(column) == "possible_target" for column in frame.columns),
                }
            )
            for position, column in enumerate(frame.columns, start=1):
                values = frame[column]
                numeric = pd.to_numeric(values, errors="coerce")
                column_rows.append(
                    {
                        "workbook": path.name,
                        "sheet_name": sheet_name,
                        "column_position": position,
                        "original_header": str(column),
                        "normalized_header": normalize_header(column),
                        "role_hint": role_hint(column),
                        "non_null_sample_rows": int(values.notna().sum()),
                        "numeric_sample_rows": int(numeric.notna().sum()),
                        "unique_sample_values": int(values.dropna().nunique()),
                    }
                )

    sheet_inventory = pd.DataFrame(sheet_rows)
    column_inventory = pd.DataFrame(column_rows)
    target_hints = (
        column_inventory[column_inventory["role_hint"].eq("possible_target")].copy()
        if not column_inventory.empty
        else pd.DataFrame()
    )

    sheet_path = output_dir / "workbook_sheet_inventory.csv"
    column_path = output_dir / "workbook_column_inventory.csv"
    target_path = output_dir / "target_header_hints.csv"
    command_path = output_dir / "suggested_commands.txt"

    sheet_inventory.to_csv(sheet_path, index=False)
    column_inventory.to_csv(column_path, index=False)
    target_hints.to_csv(target_path, index=False)

    suggested_commands: list[str] = []
    if not target_hints.empty:
        first_hint = target_hints.iloc[0]
        first_target = str(first_hint["original_header"])
        train_workbook = str(first_hint["workbook"])
        test_workbooks = [name for name in workbook_names if name != train_workbook]
        normalized = normalize_header(first_target)
        task = "classification" if "class" in normalized or "label" in normalized else "regression"
        split_args = f"--train {train_workbook} --test {' '.join(test_workbooks)} " if train_workbook != workbook_names[0] else ""
        suggested_commands.append(
            'python 01_pipeline\\run_three_dataset_ml_pipeline.py --data-dir '
            f'"{data_dir}" {split_args}--target "{first_target}" --target-task {task}'
        )
    command_path.write_text("\n".join(suggested_commands), encoding="utf-8")

    return {
        "output_dir": str(output_dir),
        "missing_files": missing_files,
        "sheet_inventory": str(sheet_path),
        "column_inventory": str(column_path),
        "target_header_hints": str(target_path),
        "suggested_commands": str(command_path),
        "target_hint_count": int(len(target_hints)),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Standalone DOE workbook header scanner.")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path.home() / "Downloads" / "Northslopedatasets06052026",
    )
    parser.add_argument(
        "--workbooks",
        nargs="+",
        default=["curated_dataset1.xlsx", "curated_dataset2.xlsx", "curated_dataset3.xlsx"],
    )
    parser.add_argument("--sample-rows", type=int, default=25)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.cwd() / "outputs_runtime" / f"standalone_header_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
    )
    args, _unknown = parser.parse_known_args()
    return args


def main() -> None:
    args = parse_args()
    result = scan_workbooks(args.data_dir, args.workbooks, args.sample_rows, args.output_dir)
    print("\nSaved outputs to:")
    print(result["output_dir"])
    if result["missing_files"]:
        print("\nMissing workbook paths:")
        for missing in result["missing_files"]:
            print(missing)
    print("\nTarget hint count:", result["target_hint_count"])
    print("Open:", result["target_header_hints"])
    print("Open:", result["suggested_commands"])


if __name__ == "__main__":
    main()
