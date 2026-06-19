# Copy this entire file into one Jupyter Notebook cell in the DOE environment.
# It uses only pandas/pathlib and does not depend on project imports or __file__.

from datetime import datetime
from pathlib import Path

import pandas as pd


DATA_DIR = Path(r"C:\Users\rohan.nanda\Downloads\Northslopedatasets06052026")
OUTPUT_ROOT = Path.cwd() / "outputs_runtime" / (
    "notebook_header_scan_" + datetime.now().strftime("%Y%m%d_%H%M%S")
)
WORKBOOKS = (
    "curated_dataset1.xlsx",
    "curated_dataset2.xlsx",
    "curated_dataset3.xlsx",
)
SAMPLE_ROWS = 25

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


try:
    display
except NameError:

    def display(value):
        if hasattr(value, "to_string"):
            print(value.to_string(index=False))
        else:
            print(value)


def normalize_header(value):
    return "".join(character for character in str(value).lower() if character.isalnum() or character == "_")


def role_hint(header):
    normalized = normalize_header(header)
    if any(word in normalized for word in TARGET_WORDS):
        return "possible_target"
    if any(word in normalized for word in FEATURE_WORDS):
        return "possible_feature_or_context"
    return "review"


OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

sheet_rows = []
column_rows = []
missing_files = []

for workbook_name in WORKBOOKS:
    path = DATA_DIR / workbook_name
    if not path.exists():
        missing_files.append(str(path))
        continue

    print("\n===", path.name, "===")
    with pd.ExcelFile(path) as excel:
        sheet_names = list(excel.sheet_names)
    print("Sheets:", sheet_names)

    for sheet_name in sheet_names:
        frame = pd.read_excel(path, sheet_name=sheet_name, nrows=SAMPLE_ROWS)
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
target_hints = column_inventory[column_inventory["role_hint"].eq("possible_target")].copy()

sheet_inventory.to_csv(OUTPUT_ROOT / "workbook_sheet_inventory.csv", index=False)
column_inventory.to_csv(OUTPUT_ROOT / "workbook_column_inventory.csv", index=False)
target_hints.to_csv(OUTPUT_ROOT / "target_header_hints.csv", index=False)

suggested_commands = []
if not target_hints.empty:
    first_hint = target_hints.iloc[0]
    first_target = first_hint["original_header"]
    train_workbook = first_hint["workbook"]
    test_workbooks = [name for name in WORKBOOKS if name != train_workbook]
    task = "classification" if "class" in normalize_header(first_target) or "label" in normalize_header(first_target) else "regression"
    split_args = f"--train {train_workbook} --test {' '.join(test_workbooks)} " if train_workbook != WORKBOOKS[0] else ""
    suggested_commands.append(
        'python 01_pipeline\\run_three_dataset_ml_pipeline.py --data-dir '
        f'"{DATA_DIR}" {split_args}--target "{first_target}" --target-task {task}'
    )

(OUTPUT_ROOT / "suggested_commands.txt").write_text("\n".join(suggested_commands), encoding="utf-8")

print("\nSaved outputs to:")
print(OUTPUT_ROOT)

if missing_files:
    print("\nMissing workbook paths:")
    for missing in missing_files:
        print(missing)

print("\nPossible target headers:")
if target_hints.empty:
    print("No target-like headers found by name. Open workbook_column_inventory.csv and inspect manually.")
else:
    display(target_hints[["workbook", "sheet_name", "original_header", "numeric_sample_rows", "unique_sample_values"]])
    print("\nSuggested command:")
    for command in suggested_commands:
        print(command)
