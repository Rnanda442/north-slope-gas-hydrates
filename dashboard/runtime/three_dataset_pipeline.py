from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any

import numpy as np
import pandas as pd

from dashboard.runtime.feature_engineering import add_standard_features
from dashboard.runtime.loaders import standardize_curve_columns
from dashboard.runtime.schemas import default_curve_aliases, target_only_column_aliases
from dashboard.runtime.validation import readiness_frame, validate_log_table


DEFAULT_TRAIN_FILE = "curated_dataset1.xlsx"
DEFAULT_TEST_FILES = ("curated_dataset2.xlsx", "curated_dataset3.xlsx")
IDENTIFIER_AND_CONTEXT_COLUMNS = {
    "well_alias",
    "depth_m",
    "source_dataset",
    "dataset_file",
    "source_sheet",
    "split",
    "row_index",
}
CLASSIFICATION_NAME_HINTS = ("occurrence", "class", "label", "phase", "hydratepresent")
REGRESSION_NAME_HINTS = ("saturation", "sat", "sgh", "shyd", "nmr_sat")


@dataclass(frozen=True)
class WorkbookDataset:
    label: str
    split: str
    path: Path
    sheet_name: str
    frame: pd.DataFrame


@dataclass(frozen=True)
class TargetSpec:
    column: str | None
    task: str
    family: str
    reason: str

    @property
    def is_available(self) -> bool:
        return self.column is not None and self.task in {"regression", "classification"}


def normalize_header_name(column: object) -> str:
    return "".join(character for character in str(column).lower() if character.isalnum())


def sanitize_label(label: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9_.-]+", "_", label.strip()).strip("._-")
    return sanitized[:100] or "dataset"


def target_alias_lookup() -> dict[str, tuple[str, str]]:
    lookup: dict[str, tuple[str, str]] = {}
    for family, aliases in target_only_column_aliases().items():
        for alias in aliases:
            lookup[normalize_header_name(alias)] = (family, alias)
    return lookup


def target_like_column(column: object) -> bool:
    normalized = normalize_header_name(column)
    if normalized in target_alias_lookup():
        return True
    if normalized in {"class", "label", "target", "y", "occurrence", "phase", "hydratepresent"}:
        return True
    has_hydrate = "hydrate" in normalized or "sgh" in normalized or normalized.startswith("sh")
    has_target_word = any(part in normalized for part in ("sat", "saturation", "occur", "class", "label", "phase"))
    return has_hydrate and has_target_word


def canonical_name_for_header(header: object) -> str | None:
    normalized = normalize_header_name(header)
    for canonical, aliases in default_curve_aliases().items():
        if normalized == normalize_header_name(canonical):
            return canonical
        for alias in aliases:
            if normalized == normalize_header_name(alias):
                return canonical
    return None


def header_role_hint(header: object) -> str:
    normalized = normalize_header_name(header)
    target_lookup = target_alias_lookup().get(normalized)
    if target_lookup is not None:
        return f"target_only_{target_lookup[0]}"
    if target_like_column(header):
        return "possible_target_review"
    canonical = canonical_name_for_header(header)
    if canonical in {"well_alias", "depth_m"}:
        return "identifier_or_depth_axis"
    if canonical is not None:
        return "candidate_feature_or_context"
    return "unmapped_review"


def read_first_nonempty_excel_sheet(path: Path, sheet_name: str | None = None) -> tuple[pd.DataFrame, str]:
    if not path.exists():
        raise FileNotFoundError(f"Workbook does not exist: {path}")
    with pd.ExcelFile(path) as excel:
        excel_sheet_names = list(excel.sheet_names)
    sheet_names = [sheet_name] if sheet_name else excel_sheet_names
    for candidate in sheet_names:
        if candidate not in excel_sheet_names:
            raise ValueError(f"Sheet {candidate!r} is not present in {path.name}.")
        frame = pd.read_excel(path, sheet_name=candidate)
        if not frame.empty and len(frame.columns):
            return frame, str(candidate)
    first_sheet = str(excel_sheet_names[0])
    return pd.read_excel(path, sheet_name=first_sheet), first_sheet


def scan_workbook_headers(path: Path, *, sample_rows: int = 25) -> tuple[pd.DataFrame, pd.DataFrame]:
    if not path.exists():
        raise FileNotFoundError(f"Workbook does not exist: {path}")
    with pd.ExcelFile(path) as excel:
        sheet_names = list(excel.sheet_names)
    sheet_rows: list[dict[str, Any]] = []
    column_rows: list[dict[str, Any]] = []
    for sheet_name in sheet_names:
        sample = pd.read_excel(path, sheet_name=sheet_name, nrows=sample_rows)
        full_header = pd.read_excel(path, sheet_name=sheet_name, nrows=0)
        sheet_rows.append(
            {
                "workbook": path.name,
                "sheet_name": str(sheet_name),
                "sampled_rows": int(len(sample)),
                "column_count": int(len(full_header.columns)),
                "has_target_like_header": bool(any(target_like_column(column) for column in full_header.columns)),
            }
        )
        for position, column in enumerate(full_header.columns, start=1):
            values = sample[column] if column in sample else pd.Series(dtype=object)
            numeric = pd.to_numeric(values, errors="coerce")
            role_hint = header_role_hint(column)
            column_rows.append(
                {
                    "workbook": path.name,
                    "sheet_name": str(sheet_name),
                    "column_position": position,
                    "original_header": str(column),
                    "normalized_header": normalize_header_name(column),
                    "canonical_header": canonical_name_for_header(column) or "",
                    "role_hint": role_hint,
                    "non_null_sample_rows": int(values.notna().sum()),
                    "numeric_sample_rows": int(numeric.notna().sum()),
                    "unique_sample_values": int(values.dropna().nunique()),
                    "suggested_target_task": (
                        "classification"
                        if role_hint.endswith("phase_or_occurrence_label")
                        or role_hint == "possible_target_review"
                        and any(hint in normalize_header_name(column) for hint in CLASSIFICATION_NAME_HINTS)
                        else "regression"
                        if "saturation" in role_hint or "sat" in normalize_header_name(column)
                        else ""
                    ),
                }
            )
    return pd.DataFrame(sheet_rows), pd.DataFrame(column_rows)


def scan_three_dataset_headers(
    data_dir: Path,
    *,
    files: tuple[str, ...] = (DEFAULT_TRAIN_FILE, *DEFAULT_TEST_FILES),
    sample_rows: int = 25,
    output_root: Path = Path("outputs_runtime"),
    run_label: str | None = None,
) -> dict[str, Any]:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    label = sanitize_label(run_label or f"three_dataset_header_scan_{timestamp}")
    run_dir = Path(output_root) / label
    run_dir.mkdir(parents=True, exist_ok=True)

    sheet_frames: list[pd.DataFrame] = []
    column_frames: list[pd.DataFrame] = []
    missing_files: list[str] = []
    for file_name in files:
        path = Path(data_dir).expanduser() / file_name
        if not path.exists():
            missing_files.append(str(path))
            continue
        sheets, columns = scan_workbook_headers(path, sample_rows=sample_rows)
        sheet_frames.append(sheets)
        column_frames.append(columns)

    sheet_inventory = pd.concat(sheet_frames, ignore_index=True) if sheet_frames else pd.DataFrame()
    column_inventory = pd.concat(column_frames, ignore_index=True) if column_frames else pd.DataFrame()
    target_hints = (
        column_inventory[column_inventory["role_hint"].str.contains("target", case=False, na=False)].copy()
        if not column_inventory.empty
        else pd.DataFrame()
    )

    sheet_path = run_dir / "workbook_sheet_inventory.csv"
    column_path = run_dir / "workbook_column_inventory.csv"
    target_path = run_dir / "target_header_hints.csv"
    sheet_inventory.to_csv(sheet_path, index=False)
    column_inventory.to_csv(column_path, index=False)
    target_hints.to_csv(target_path, index=False)

    suggestions: list[str] = []
    if not target_hints.empty:
        first = target_hints.iloc[0]
        task = first.get("suggested_target_task") or "regression"
        suggestions.append(
            "python 01_pipeline\\run_three_dataset_ml_pipeline.py "
            f"--data-dir \"{Path(data_dir).expanduser()}\" "
            f"--target \"{first['original_header']}\" --target-task {task}"
        )
    suggestions_path = run_dir / "suggested_commands.txt"
    suggestions_path.write_text("\n".join(suggestions) + ("\n" if suggestions else ""), encoding="utf-8")

    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_dir_name": Path(data_dir).expanduser().name,
        "missing_files": missing_files,
        "sheet_inventory": str(sheet_path),
        "column_inventory": str(column_path),
        "target_header_hints": str(target_path),
        "suggested_commands": str(suggestions_path),
        "target_hint_count": int(len(target_hints)),
        "guardrail": "Header/sample scan is approved-runtime local only; do not commit workbook rows or sensitive identifiers.",
    }
    write_json(run_dir / "header_scan_manifest.json", manifest)
    return {"run_dir": str(run_dir), **manifest}


def load_workbook_dataset(path: Path, *, label: str, split: str, sheet_name: str | None = None) -> WorkbookDataset:
    raw, used_sheet = read_first_nonempty_excel_sheet(path, sheet_name=sheet_name)
    standardized = standardize_curve_columns(raw)
    standardized["source_dataset"] = label
    standardized["dataset_file"] = path.name
    standardized["source_sheet"] = used_sheet
    standardized["split"] = split
    standardized["row_index"] = np.arange(len(standardized))
    if "well_alias" not in standardized.columns:
        standardized["well_alias"] = label
    return WorkbookDataset(label=label, split=split, path=path, sheet_name=used_sheet, frame=standardized)


def load_three_dataset_workbooks(
    data_dir: Path,
    *,
    train_file: str = DEFAULT_TRAIN_FILE,
    test_files: tuple[str, ...] = DEFAULT_TEST_FILES,
    sheet_name: str | None = None,
) -> list[WorkbookDataset]:
    data_dir = Path(data_dir).expanduser()
    datasets = [
        load_workbook_dataset(
            data_dir / train_file,
            label=Path(train_file).stem,
            split="train",
            sheet_name=sheet_name,
        )
    ]
    for test_file in test_files:
        datasets.append(
            load_workbook_dataset(
                data_dir / test_file,
                label=Path(test_file).stem,
                split="test",
                sheet_name=sheet_name,
            )
        )
    return datasets


def detect_target_candidates(frame: pd.DataFrame) -> pd.DataFrame:
    lookup = target_alias_lookup()
    rows: list[dict[str, Any]] = []
    for column in frame.columns:
        normalized = normalize_header_name(column)
        family_alias = lookup.get(normalized)
        family = family_alias[0] if family_alias else ""
        if family or target_like_column(column):
            values = frame[column]
            numeric = pd.to_numeric(values, errors="coerce")
            non_null = int(values.notna().sum())
            numeric_non_null = int(numeric.notna().sum())
            if family == "phase_or_occurrence_label" or any(hint in normalized for hint in CLASSIFICATION_NAME_HINTS):
                task_hint = "classification"
            elif numeric_non_null > 0:
                task_hint = "regression"
            else:
                task_hint = "classification"
            rows.append(
                {
                    "column": str(column),
                    "normalized_column": normalized,
                    "target_family": family or "target_like_unregistered",
                    "task_hint": task_hint,
                    "non_null_rows": non_null,
                    "numeric_non_null_rows": numeric_non_null,
                    "unique_non_null_values": int(values.dropna().nunique()),
                }
            )
    return pd.DataFrame(
        rows,
        columns=[
            "column",
            "normalized_column",
            "target_family",
            "task_hint",
            "non_null_rows",
            "numeric_non_null_rows",
            "unique_non_null_values",
        ],
    )


def find_column_by_request(frame: pd.DataFrame, requested: str) -> str | None:
    if requested in frame.columns:
        return requested
    requested_normalized = normalize_header_name(requested)
    for column in frame.columns:
        if normalize_header_name(column) == requested_normalized:
            return str(column)
    return None


def infer_task_for_column(frame: pd.DataFrame, column: str, requested_task: str) -> str:
    if requested_task != "auto":
        return requested_task
    normalized = normalize_header_name(column)
    if any(hint in normalized for hint in CLASSIFICATION_NAME_HINTS):
        return "classification"
    if any(hint in normalized for hint in REGRESSION_NAME_HINTS):
        return "regression"
    numeric = pd.to_numeric(frame[column], errors="coerce")
    if numeric.notna().sum() >= max(3, int(frame[column].notna().sum() * 0.8)):
        return "regression"
    return "classification"


def choose_target(
    train_frame: pd.DataFrame,
    *,
    requested_target: str = "auto",
    requested_task: str = "auto",
) -> tuple[TargetSpec, pd.DataFrame]:
    candidates = detect_target_candidates(train_frame)
    selected_column: str | None = None
    reason = ""
    if requested_target != "auto":
        selected_column = find_column_by_request(train_frame, requested_target)
        if selected_column is None:
            raise ValueError(f"Requested target {requested_target!r} was not found in the training workbook.")
        reason = "target requested by CLI"
    elif not candidates.empty:
        candidate_order = candidates.copy()
        candidate_order["priority"] = candidate_order["target_family"].map(
            {
                "hydrate_saturation": 0,
                "phase_or_occurrence_label": 1,
                "target_like_unregistered": 2,
                "irreducible_or_residual_water_saturation": 3,
            }
        ).fillna(9)
        candidate_order = candidate_order.sort_values(
            ["priority", "non_null_rows", "unique_non_null_values"],
            ascending=[True, False, False],
        )
        selected_column = str(candidate_order.iloc[0]["column"])
        reason = "first usable target-like column by project priority"

    if selected_column is None:
        spec = TargetSpec(
            column=None,
            task="readiness_only",
            family="none_detected",
            reason="no target-like saturation, occurrence, or phase column detected in training workbook",
        )
        return spec, candidates

    task = infer_task_for_column(train_frame, selected_column, requested_task)
    target_lookup = target_alias_lookup().get(normalize_header_name(selected_column))
    family = target_lookup[0] if target_lookup else "target_like_unregistered"
    selected = candidates.copy()
    if selected.empty:
        selected = pd.DataFrame(
            [
                {
                    "column": selected_column,
                    "normalized_column": normalize_header_name(selected_column),
                    "target_family": family,
                    "task_hint": task,
                    "non_null_rows": int(train_frame[selected_column].notna().sum()),
                    "numeric_non_null_rows": int(pd.to_numeric(train_frame[selected_column], errors="coerce").notna().sum()),
                    "unique_non_null_values": int(train_frame[selected_column].dropna().nunique()),
                }
            ]
        )
    selected["selected"] = selected["column"].astype(str).eq(selected_column)
    return TargetSpec(column=selected_column, task=task, family=family, reason=reason), selected


def feature_side_frame(frame: pd.DataFrame, target_columns: set[str]) -> pd.DataFrame:
    drop_columns = [
        column
        for column in frame.columns
        if str(column) in target_columns or target_like_column(column)
    ]
    return frame.drop(columns=drop_columns, errors="ignore")


def make_feature_matrix(frame: pd.DataFrame, *, target_columns: set[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    features = add_standard_features(frame)
    excluded = set(target_columns)
    rows: list[dict[str, Any]] = []
    selected_columns: list[str] = []
    for column in features.columns:
        column_name = str(column)
        if column_name in excluded or column_name in IDENTIFIER_AND_CONTEXT_COLUMNS or target_like_column(column_name):
            continue
        if pd.api.types.is_bool_dtype(features[column]):
            values = features[column].astype(int)
        else:
            values = pd.to_numeric(features[column], errors="coerce")
        if values.notna().sum() == 0:
            continue
        features[column_name] = values
        selected_columns.append(column_name)
        rows.append(
            {
                "feature_column": column_name,
                "non_null_rows": int(values.notna().sum()),
                "coverage_fraction": round(float(values.notna().mean()), 4),
                "minimum": float(values.min(skipna=True)),
                "maximum": float(values.max(skipna=True)),
                "role": "numeric_model_input",
                "normalized_by_pipeline": True,
            }
        )
    return features[selected_columns].copy(), pd.DataFrame(rows)


def dataset_inventory_frame(datasets: list[WorkbookDataset]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for dataset in datasets:
        frame = dataset.frame
        depth = pd.to_numeric(frame.get("depth_m"), errors="coerce") if "depth_m" in frame else pd.Series(dtype=float)
        rows.append(
            {
                "source_dataset": dataset.label,
                "split": dataset.split,
                "file_name": dataset.path.name,
                "sheet_name": dataset.sheet_name,
                "rows": len(frame),
                "columns": len(frame.columns),
                "wells": int(frame["well_alias"].nunique()) if "well_alias" in frame else 0,
                "depth_min_m": float(depth.min(skipna=True)) if depth.notna().any() else None,
                "depth_max_m": float(depth.max(skipna=True)) if depth.notna().any() else None,
            }
        )
    return pd.DataFrame(rows)


def schema_readiness_for_datasets(datasets: list[WorkbookDataset], target_columns: set[str]) -> pd.DataFrame:
    rows: list[pd.DataFrame] = []
    for dataset in datasets:
        report = validate_log_table(feature_side_frame(dataset.frame, target_columns))
        frame = readiness_frame(report)
        if frame.empty:
            frame = pd.DataFrame([{"Severity": "info", "Column": "table", "Message": "Feature-side log table passed current checks."}])
        frame.insert(0, "source_dataset", dataset.label)
        frame.insert(1, "split", dataset.split)
        frame.insert(2, "status", report.status)
        frame.insert(3, "rows", report.rows)
        frame.insert(4, "wells", report.wells)
        rows.append(frame)
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def build_model_pipeline(task: str, model_kind: str, random_state: int) -> Any:
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    from sklearn.impute import SimpleImputer
    from sklearn.neural_network import MLPClassifier, MLPRegressor
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import MinMaxScaler

    if model_kind == "mlp":
        if task == "classification":
            model = MLPClassifier(hidden_layer_sizes=(32, 16), max_iter=600, random_state=random_state)
        else:
            model = MLPRegressor(hidden_layer_sizes=(32, 16), max_iter=600, random_state=random_state)
    elif task == "classification":
        model = RandomForestClassifier(
            n_estimators=250,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=random_state,
        )
    else:
        model = RandomForestRegressor(
            n_estimators=250,
            min_samples_leaf=2,
            random_state=random_state,
        )
    return Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("minmax_scaler", MinMaxScaler()),
            ("model", model),
        ]
    )


def evaluate_predictions(y_true: pd.Series, y_pred: np.ndarray, *, task: str) -> dict[str, Any]:
    if task == "classification":
        from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score

        return {
            "rows_scored": int(len(y_true)),
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
            "f1_macro": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        }
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    y_numeric = pd.to_numeric(y_true, errors="coerce")
    pred_numeric = pd.to_numeric(pd.Series(y_pred), errors="coerce")
    rmse = float(np.sqrt(mean_squared_error(y_numeric, pred_numeric)))
    return {
        "rows_scored": int(len(y_numeric)),
        "mae": float(mean_absolute_error(y_numeric, pred_numeric)),
        "rmse": rmse,
        "r2": float(r2_score(y_numeric, pred_numeric)) if len(y_numeric) >= 2 else None,
    }


def prepare_supervised_table(
    frame: pd.DataFrame,
    *,
    target: TargetSpec,
    feature_columns: list[str],
    target_columns: set[str],
) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    if target.column is None:
        raise ValueError("Cannot prepare a supervised table without a target column.")
    X_all, _ = make_feature_matrix(frame, target_columns=target_columns)
    for column in feature_columns:
        if column not in X_all.columns:
            X_all[column] = np.nan
    X = X_all[feature_columns].copy()
    y_raw = frame[target.column]
    if target.task == "regression":
        y = pd.to_numeric(y_raw, errors="coerce")
    else:
        y = y_raw.astype("string")
    mask = y.notna() & X.notna().any(axis=1)
    return X.loc[mask].reset_index(drop=True), y.loc[mask].reset_index(drop=True), frame.loc[mask].reset_index(drop=True)


def prediction_frame(
    source_frame: pd.DataFrame,
    *,
    y_true: pd.Series | None,
    y_pred: np.ndarray,
    task: str,
    model: Any,
    X: pd.DataFrame,
    target_column: str,
) -> pd.DataFrame:
    output = pd.DataFrame(
        {
            "source_dataset": source_frame.get("source_dataset", pd.Series([""] * len(source_frame))).astype(str),
            "dataset_file": source_frame.get("dataset_file", pd.Series([""] * len(source_frame))).astype(str),
            "well_alias": source_frame.get("well_alias", pd.Series([""] * len(source_frame))).astype(str),
            "row_index": source_frame.get("row_index", pd.Series(range(len(source_frame)))),
        }
    )
    if "depth_m" in source_frame:
        output["depth_m"] = source_frame["depth_m"]
    output["target_column"] = target_column
    if y_true is not None:
        output["y_true"] = y_true.to_numpy()
    output["y_pred"] = y_pred
    if task == "classification" and hasattr(model, "predict_proba"):
        try:
            probabilities = model.predict_proba(X)
            output["y_pred_probability_max"] = probabilities.max(axis=1)
        except Exception:
            pass
    return output


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str), encoding="utf-8")


def run_three_dataset_pipeline(
    *,
    data_dir: Path,
    train_file: str = DEFAULT_TRAIN_FILE,
    test_files: tuple[str, ...] = DEFAULT_TEST_FILES,
    sheet_name: str | None = None,
    requested_target: str = "auto",
    requested_task: str = "auto",
    model_kind: str = "baseline",
    output_root: Path = Path("outputs_runtime"),
    model_root: Path = Path("models_runtime"),
    random_state: int = 42,
    run_label: str | None = None,
) -> dict[str, Any]:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    label = sanitize_label(run_label or f"three_dataset_ml_run_{timestamp}")
    run_dir = Path(output_root) / label
    model_dir = Path(model_root) / label
    run_dir.mkdir(parents=True, exist_ok=True)
    model_dir.mkdir(parents=True, exist_ok=True)

    datasets = load_three_dataset_workbooks(
        data_dir,
        train_file=train_file,
        test_files=tuple(test_files),
        sheet_name=sheet_name,
    )
    train_dataset = datasets[0]
    target, target_candidates = choose_target(
        train_dataset.frame,
        requested_target=requested_target,
        requested_task=requested_task,
    )
    target_columns = {str(column) for column in target_candidates.get("column", pd.Series(dtype=str)).astype(str)}
    if target.column:
        target_columns.add(target.column)

    inventory = dataset_inventory_frame(datasets)
    schema_readiness = schema_readiness_for_datasets(datasets, target_columns)
    feature_matrix, feature_inventory = make_feature_matrix(train_dataset.frame, target_columns=target_columns)

    written: dict[str, str] = {}
    inventory_path = run_dir / "dataset_inventory.csv"
    readiness_path = run_dir / "schema_readiness.csv"
    target_path = run_dir / "target_detection.csv"
    feature_path = run_dir / "feature_columns.csv"
    inventory.to_csv(inventory_path, index=False)
    schema_readiness.to_csv(readiness_path, index=False)
    target_candidates.to_csv(target_path, index=False)
    feature_inventory.to_csv(feature_path, index=False)
    written.update(
        {
            "dataset_inventory": str(inventory_path),
            "schema_readiness": str(readiness_path),
            "target_detection": str(target_path),
            "feature_columns": str(feature_path),
        }
    )

    train_metrics_rows: list[dict[str, Any]] = []
    test_metrics_rows: list[dict[str, Any]] = []
    model_path: Path | None = None
    feature_columns = feature_matrix.columns.astype(str).tolist()
    status = "readiness_only"
    blocked_reason = ""

    if not target.is_available:
        blocked_reason = target.reason
    elif not feature_columns:
        blocked_reason = "no numeric non-target feature columns detected after leakage and context exclusions"
    else:
        X_train, y_train, train_rows = prepare_supervised_table(
            train_dataset.frame,
            target=target,
            feature_columns=feature_columns,
            target_columns=target_columns,
        )
        if len(X_train) < 3:
            blocked_reason = "fewer than three target-bearing training rows after preprocessing"
        elif target.task == "classification" and y_train.nunique() < 2:
            blocked_reason = "classification target has fewer than two classes in the training workbook"
        else:
            model = build_model_pipeline(target.task, model_kind, random_state)
            model.fit(X_train, y_train)
            train_pred = model.predict(X_train)
            train_metrics = evaluate_predictions(y_train, train_pred, task=target.task)
            train_metrics.update(
                {
                    "dataset": train_dataset.label,
                    "split": "train",
                    "task": target.task,
                    "target_column": target.column,
                    "model_kind": model_kind,
                    "feature_count": len(feature_columns),
                }
            )
            train_metrics_rows.append(train_metrics)
            train_prediction_path = run_dir / f"predictions_{sanitize_label(train_dataset.label)}.csv"
            prediction_frame(
                train_rows,
                y_true=y_train,
                y_pred=train_pred,
                task=target.task,
                model=model,
                X=X_train,
                target_column=target.column or "",
            ).to_csv(train_prediction_path, index=False)
            written["train_predictions"] = str(train_prediction_path)

            for dataset in datasets[1:]:
                if target.column not in dataset.frame.columns:
                    test_metrics_rows.append(
                        {
                            "dataset": dataset.label,
                            "split": "test",
                            "task": target.task,
                            "target_column": target.column,
                            "model_kind": model_kind,
                            "feature_count": len(feature_columns),
                            "rows_scored": 0,
                            "status": "blocked",
                            "blocked_reason": "target column not present in test workbook",
                        }
                    )
                    continue
                X_test, y_test, test_rows = prepare_supervised_table(
                    dataset.frame,
                    target=target,
                    feature_columns=feature_columns,
                    target_columns=target_columns,
                )
                if X_test.empty:
                    test_metrics_rows.append(
                        {
                            "dataset": dataset.label,
                            "split": "test",
                            "task": target.task,
                            "target_column": target.column,
                            "model_kind": model_kind,
                            "feature_count": len(feature_columns),
                            "rows_scored": 0,
                            "status": "blocked",
                            "blocked_reason": "no test rows have both target and at least one feature",
                        }
                    )
                    continue
                test_pred = model.predict(X_test)
                metrics = evaluate_predictions(y_test, test_pred, task=target.task)
                metrics.update(
                    {
                        "dataset": dataset.label,
                        "split": "test",
                        "task": target.task,
                        "target_column": target.column,
                        "model_kind": model_kind,
                        "feature_count": len(feature_columns),
                        "status": "scored",
                        "blocked_reason": "",
                    }
                )
                test_metrics_rows.append(metrics)
                prediction_path = run_dir / f"predictions_{sanitize_label(dataset.label)}.csv"
                prediction_frame(
                    test_rows,
                    y_true=y_test,
                    y_pred=test_pred,
                    task=target.task,
                    model=model,
                    X=X_test,
                    target_column=target.column or "",
                ).to_csv(prediction_path, index=False)
                written[f"predictions_{dataset.label}"] = str(prediction_path)

            from joblib import dump

            model_path = model_dir / "model.joblib"
            dump(
                {
                    "model": model,
                    "feature_columns": feature_columns,
                    "target": asdict(target),
                    "model_kind": model_kind,
                },
                model_path,
            )
            written["model"] = str(model_path)
            status = "trained"

    train_metrics_path = run_dir / "train_metrics.csv"
    test_metrics_path = run_dir / "test_metrics.csv"
    pd.DataFrame(train_metrics_rows).to_csv(train_metrics_path, index=False)
    pd.DataFrame(test_metrics_rows).to_csv(test_metrics_path, index=False)
    written["train_metrics"] = str(train_metrics_path)
    written["test_metrics"] = str(test_metrics_path)

    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": status,
        "blocked_reason": blocked_reason,
        "data_dir_name": Path(data_dir).expanduser().name,
        "train_file": train_file,
        "test_files": list(test_files),
        "target": asdict(target),
        "model_kind": model_kind,
        "feature_count": len(feature_columns),
        "feature_columns": feature_columns,
        "outputs": written,
        "guardrail": (
            "Approved workbook rows, predictions, fitted scalers, and trained models stay in ignored runtime folders "
            "unless reviewed and summarized separately."
        ),
    }
    manifest_path = run_dir / "run_manifest.json"
    write_json(manifest_path, manifest)
    written["run_manifest"] = str(manifest_path)
    return {
        "status": status,
        "blocked_reason": blocked_reason,
        "run_dir": str(run_dir),
        "model_dir": str(model_dir),
        "model_path": str(model_path) if model_path else None,
        "target": asdict(target),
        "feature_count": len(feature_columns),
        "outputs": written,
    }
