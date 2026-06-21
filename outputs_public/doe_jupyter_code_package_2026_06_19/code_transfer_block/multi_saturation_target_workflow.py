from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re

import numpy as np
import pandas as pd


DEFAULT_WORKBOOKS = ("curated_dataset1.xlsx", "curated_dataset2.xlsx", "curated_dataset3.xlsx")
FEATURE_POLICY_VERSION = "clean_feature_matrix_v3_2026_06_16"
IDENTIFIER_COLUMNS = {"well_alias", "depth_m", "source_workbook", "source_sheet", "row_index"}
MAX_MODEL_ABS_VALUE = 1.0e12
SATURATION_EXACT = {
    "sgh",
    "sh",
    "shyd",
    "hydratesat",
    "hydratesaturation",
    "nmrsat",
    "swr",
    "sw",
    "swi",
    "swirr",
}
SATURATION_WORDS = ("sat", "saturation")
NOT_SATURATION_WORDS = ("porosity", "density", "sample", "station", "status")
FEATURE_ALIASES = {
    "well_alias": ("well_alias", "well", "wellname", "well_name", "uwi", "api"),
    "depth_m": ("depth_m", "depth", "depthm", "depthft", "dept", "md", "mdm", "tvd", "tvdm"),
    "gr_api": ("gr_api", "gr", "gamma", "gammaray", "gamma_ray"),
    "rt_ohm_m": ("rt_ohm_m", "rt", "res", "rdep", "resdeep", "ild", "deepresistivity"),
    "rhob_g_cc": ("rhob_g_cc", "rhob", "density", "densitygpcc", "densitygcc", "den", "rho_b", "bulk_density"),
    "density_porosity_vv": ("density_porosity_vv", "dphi", "phid", "phiden", "denpor", "densityporosity"),
    "neutron_porosity_vv": ("neutron_porosity_vv", "nphi", "tnph", "phineut", "neutronporosity"),
    "dt_us_ft": ("dt_us_ft", "dt", "dtc", "ac"),
    "dts_us_ft": ("dts_us_ft", "dts", "dtsm"),
    "vp_km_s": ("vp_km_s", "vpkms"),
    "vs_km_s": ("vs_km_s", "vskms"),
    "vp_m_s": ("vp_m_s", "vp", "velp", "vpmps"),
    "vs_m_s": ("vs_m_s", "vs", "vs1", "vels", "vsmps"),
    "nmr_porosity_vv": ("nmr_porosity_vv", "nmrphi", "phinmr", "tcmr", "cmrp", "nmrporosity"),
    "caliper_in": ("caliper_in", "caliper", "cali", "cal1"),
}
CONTEXT_OR_HELPER_EXACT = {"index", "row", "rowindex", "depth", "depthm", "depthft", "dept", "md", "tvd"}
CONTEXT_OR_HELPER_PARTS = ("depth", "unit", "units")


def normalize_header(value: object) -> str:
    return "".join(character for character in str(value).lower() if character.isalnum())


def sanitize_label(value: object) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(value).strip()).strip("._-")
    return sanitized[:90] or "target"


def clean_numeric_series(values: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(values, errors="coerce")
    numeric = numeric.replace([np.inf, -np.inf], np.nan)
    numeric = numeric.mask(numeric.abs() > MAX_MODEL_ABS_VALUE)
    return numeric


def clean_numeric_frame(frame: pd.DataFrame) -> pd.DataFrame:
    cleaned = frame.copy()
    for column in cleaned.columns:
        cleaned[column] = clean_numeric_series(cleaned[column])
    return cleaned


def is_saturation_header(header: object) -> bool:
    normalized = normalize_header(header)
    if any(word in normalized for word in NOT_SATURATION_WORDS):
        return False
    return normalized in SATURATION_EXACT or any(word in normalized for word in SATURATION_WORDS)


def canonical_feature_name(header: object) -> str | None:
    normalized = normalize_header(header)
    for canonical, aliases in FEATURE_ALIASES.items():
        if normalized == normalize_header(canonical):
            return canonical
        for alias in aliases:
            if normalized == normalize_header(alias):
                return canonical
    return None


def is_context_or_helper_header(header: object) -> bool:
    normalized = normalize_header(header)
    canonical = canonical_feature_name(header)
    return (
        normalized.startswith("unnamed")
        or normalized in CONTEXT_OR_HELPER_EXACT
        or any(part in normalized for part in CONTEXT_OR_HELPER_PARTS)
        or canonical in {"well_alias", "depth_m"}
    )


def feature_exclusion_reason(name: str, saturation_columns: set[str], canonical_columns: set[str]) -> str:
    canonical_name = canonical_feature_name(name)
    is_raw_alias_duplicate = canonical_name is not None and canonical_name != name and canonical_name in canonical_columns
    if name in saturation_columns or is_saturation_header(name):
        return "target_only_saturation"
    if name in IDENTIFIER_COLUMNS:
        return "identifier_or_runtime_context"
    if is_context_or_helper_header(name):
        return "context_depth_unit_or_spreadsheet_helper"
    if is_raw_alias_duplicate:
        return f"raw_alias_duplicate_of_{canonical_name}"
    return ""


def sheet_key(sheet_name: str) -> str:
    normalized = normalize_header(sheet_name)
    if "1" in normalized:
        return "1"
    if "2" in normalized:
        return "2"
    if "3" in normalized:
        return "3"
    return ""


def canonicalize_features(frame: pd.DataFrame) -> pd.DataFrame:
    output = frame.copy()
    normalized_lookup = {normalize_header(column): column for column in output.columns}
    for canonical, aliases in FEATURE_ALIASES.items():
        if canonical in output.columns:
            continue
        for alias in aliases:
            actual = normalized_lookup.get(normalize_header(alias))
            if actual is not None:
                output[canonical] = output[actual]
                break

    for column in output.columns:
        if column == "well_alias":
            output[column] = output[column].astype(str)
            continue
        numeric = clean_numeric_series(output[column])
        if numeric.notna().any():
            output[column] = numeric

    if "rhob_g_cc" in output and "density_porosity_vv" not in output:
        output["density_porosity_vv"] = ((2.65 - clean_numeric_series(output["rhob_g_cc"])) / (2.65 - 1.03)).clip(0, 0.7)
    if "gr_api" in output:
        output["vshale"] = ((clean_numeric_series(output["gr_api"]) - 30) / (105 - 30)).clip(0, 1)
    if "dt_us_ft" in output and "vp_km_s" not in output:
        with np.errstate(divide="ignore", invalid="ignore"):
            output["vp_km_s"] = 304.8 / clean_numeric_series(output["dt_us_ft"])
    if "dts_us_ft" in output and "vs_km_s" not in output:
        with np.errstate(divide="ignore", invalid="ignore"):
            output["vs_km_s"] = 304.8 / clean_numeric_series(output["dts_us_ft"])
    if "vp_m_s" in output and "vp_km_s" not in output:
        output["vp_km_s"] = clean_numeric_series(output["vp_m_s"]) / 1000.0
    if "vs_m_s" in output and "vs_km_s" not in output:
        output["vs_km_s"] = clean_numeric_series(output["vs_m_s"]) / 1000.0
    if {"vp_km_s", "vs_km_s"}.issubset(output.columns):
        with np.errstate(divide="ignore", invalid="ignore"):
            output["vp_vs_ratio"] = clean_numeric_series(output["vp_km_s"]) / clean_numeric_series(output["vs_km_s"])
    if {"density_porosity_vv", "rt_ohm_m"}.issubset(output.columns):
        phi = clean_numeric_series(output["density_porosity_vv"]).clip(0.04)
        rt = clean_numeric_series(output["rt_ohm_m"])
        with np.errstate(divide="ignore", invalid="ignore"):
            output["archie_hydrate_proxy"] = (1 - ((0.12 / ((phi**2) * rt)) ** 0.5)).clip(0, 1)
    return output.replace([np.inf, -np.inf], np.nan)


def feature_table(frame: pd.DataFrame, saturation_columns: set[str]) -> tuple[pd.DataFrame, list[str]]:
    canonical = canonicalize_features(frame)
    canonical_columns = set(str(column) for column in canonical.columns)
    selected: list[str] = []
    feature_values: dict[str, pd.Series] = {}
    for column in canonical.columns:
        name = str(column)
        if feature_exclusion_reason(name, saturation_columns, canonical_columns):
            continue
        values = clean_numeric_series(canonical[column])
        if values.notna().sum() == 0:
            continue
        selected.append(name)
        feature_values[name] = values
    return clean_numeric_frame(pd.DataFrame(feature_values)), selected


def feature_policy_audit(frame: pd.DataFrame, saturation_columns: set[str], target_id: str) -> pd.DataFrame:
    canonical = canonicalize_features(frame)
    canonical_columns = set(str(column) for column in canonical.columns)
    rows: list[dict[str, object]] = []
    for column in canonical.columns:
        name = str(column)
        reason = feature_exclusion_reason(name, saturation_columns, canonical_columns)
        values = clean_numeric_series(canonical[column])
        if not reason and values.notna().sum() == 0:
            reason = "non_numeric_or_empty"
        rows.append(
            {
                "target_id": target_id,
                "feature_policy_version": FEATURE_POLICY_VERSION,
                "column": name,
                "canonical_feature": canonical_feature_name(name) or "",
                "decision": "excluded" if reason else "included",
                "reason": reason,
                "numeric_rows": int(values.notna().sum()),
            }
        )
    return pd.DataFrame(rows)


def read_workbook_sheets(data_dir: Path, workbook_names: tuple[str, ...]) -> list[dict[str, object]]:
    sheets: list[dict[str, object]] = []
    for workbook_name in workbook_names:
        path = data_dir / workbook_name
        if not path.exists():
            continue
        with pd.ExcelFile(path) as excel:
            sheet_names = list(excel.sheet_names)
        for sheet_name in sheet_names:
            frame = pd.read_excel(path, sheet_name=sheet_name)
            frame["source_workbook"] = workbook_name
            frame["source_sheet"] = str(sheet_name)
            frame["row_index"] = np.arange(len(frame))
            sheets.append({"workbook": workbook_name, "sheet": str(sheet_name), "frame": frame})
    return sheets


def saturation_target_inventory(sheets: list[dict[str, object]]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for sheet in sheets:
        frame = sheet["frame"]
        assert isinstance(frame, pd.DataFrame)
        for column in frame.columns:
            if not is_saturation_header(column):
                continue
            values = clean_numeric_series(frame[column])
            rows.append(
                {
                    "workbook": sheet["workbook"],
                    "sheet_name": sheet["sheet"],
                    "target_column": str(column),
                    "numeric_rows": int(values.notna().sum()),
                    "unique_values": int(values.dropna().nunique()),
                    "minimum": float(values.min(skipna=True)) if values.notna().any() else None,
                    "maximum": float(values.max(skipna=True)) if values.notna().any() else None,
                }
            )
    return pd.DataFrame(rows)


def find_feature_source_for_target(
    target_sheet: dict[str, object],
    target_column: str,
    sheets: list[dict[str, object]],
) -> tuple[pd.DataFrame | None, str, str]:
    target_frame = target_sheet["frame"]
    assert isinstance(target_frame, pd.DataFrame)
    saturation_columns = {str(column) for column in target_frame.columns if is_saturation_header(column)}
    same_features, same_feature_columns = feature_table(target_frame, saturation_columns)
    if same_feature_columns:
        return target_frame.copy(), str(target_sheet["workbook"]), "same_sheet"

    target_key = sheet_key(str(target_sheet["sheet"]))
    scored_candidates: list[tuple[int, dict[str, object], list[str]]] = []
    for candidate in sheets:
        candidate_frame = candidate["frame"]
        assert isinstance(candidate_frame, pd.DataFrame)
        candidate_saturation = {str(column) for column in candidate_frame.columns if is_saturation_header(column)}
        candidate_features, candidate_feature_columns = feature_table(candidate_frame, candidate_saturation)
        if not candidate_feature_columns:
            continue
        score = len(candidate_feature_columns)
        if len(candidate_frame) == len(target_frame):
            score += 100
        if target_key and sheet_key(str(candidate["sheet"])) == target_key:
            score += 50
        if target_key and target_key in str(candidate["workbook"]):
            score += 25
        scored_candidates.append((score, candidate, candidate_feature_columns))

    if not scored_candidates:
        return None, "", "blocked_no_feature_source"
    _score, best, _columns = sorted(scored_candidates, key=lambda item: item[0], reverse=True)[0]
    best_frame = best["frame"]
    assert isinstance(best_frame, pd.DataFrame)
    if len(best_frame) != len(target_frame):
        return None, str(best["workbook"]), "blocked_row_count_mismatch"
    aligned = best_frame.reset_index(drop=True).copy()
    aligned[target_column] = target_frame[target_column].reset_index(drop=True)
    return aligned, str(best["workbook"]), "row_order_aligned"


def fit_and_predict_all_saturations(
    data_dir: Path,
    workbook_names: tuple[str, ...] = DEFAULT_WORKBOOKS,
    output_dir: Path | None = None,
    min_training_rows: int = 5,
) -> dict[str, object]:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.impute import SimpleImputer
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import MinMaxScaler

    data_dir = data_dir.expanduser()
    output_dir = output_dir or Path.cwd() / "outputs_runtime" / f"multi_saturation_clean_features_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_dir.mkdir(parents=True, exist_ok=True)

    sheets = read_workbook_sheets(data_dir, workbook_names)
    target_inventory = saturation_target_inventory(sheets)
    target_inventory.to_csv(output_dir / "saturation_target_inventory.csv", index=False)

    sheet_inventory = pd.DataFrame(
        [
            {
                "workbook": sheet["workbook"],
                "sheet_name": sheet["sheet"],
                "rows": len(sheet["frame"]),
                "columns": len(sheet["frame"].columns),
            }
            for sheet in sheets
        ]
    )
    sheet_inventory.to_csv(output_dir / "sheet_inventory.csv", index=False)

    summary_rows: list[dict[str, object]] = []
    feature_rows: list[dict[str, object]] = []
    feature_audit_rows: list[pd.DataFrame] = []
    if target_inventory.empty:
        (output_dir / "run_summary.csv").write_text("status,message\nblocked,no saturation targets found\n", encoding="utf-8")
        return {"status": "blocked", "message": "no saturation targets found", "output_dir": str(output_dir)}

    for _, target in target_inventory.iterrows():
        target_sheet = next(
            sheet for sheet in sheets if sheet["workbook"] == target["workbook"] and sheet["sheet"] == target["sheet_name"]
        )
        target_column = str(target["target_column"])
        training_frame, feature_source, alignment_method = find_feature_source_for_target(target_sheet, target_column, sheets)
        target_id = sanitize_label(f"{target['workbook']}_{target['sheet_name']}_{target_column}")
        if training_frame is None:
            summary_rows.append(
                {
                    "target_id": target_id,
                    "target_column": target_column,
                    "target_workbook": target["workbook"],
                    "target_sheet": target["sheet_name"],
                    "status": "blocked",
                    "alignment_method": alignment_method,
                    "feature_source": feature_source,
                    "training_rows": 0,
                }
            )
            continue

        saturation_columns = {str(column) for column in training_frame.columns if is_saturation_header(column)}
        X_train_all, feature_columns = feature_table(training_frame, saturation_columns)
        feature_audit_rows.append(feature_policy_audit(training_frame, saturation_columns, target_id))
        y = clean_numeric_series(training_frame[target_column])
        mask = y.notna() & X_train_all.notna().any(axis=1)
        X_train = clean_numeric_frame(X_train_all.loc[mask].reset_index(drop=True))
        y_train = y.loc[mask].reset_index(drop=True)
        if len(X_train) < min_training_rows:
            summary_rows.append(
                {
                    "target_id": target_id,
                    "target_column": target_column,
                    "target_workbook": target["workbook"],
                    "target_sheet": target["sheet_name"],
                    "status": "blocked",
                    "alignment_method": alignment_method,
                    "feature_source": feature_source,
                    "training_rows": int(len(X_train)),
                    "blocked_reason": "not enough target-bearing training rows",
                }
            )
            continue

        model = Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("minmax_scaler", MinMaxScaler()),
                ("model", RandomForestRegressor(n_estimators=250, min_samples_leaf=2, random_state=42)),
            ]
        )
        model.fit(X_train[feature_columns], y_train)
        train_pred = model.predict(X_train[feature_columns])
        target_output_dir = output_dir / target_id
        target_output_dir.mkdir(parents=True, exist_ok=True)

        for feature in feature_columns:
            feature_rows.append({"target_id": target_id, "feature_column": feature})

        prediction_files: list[str] = []
        metric_rows: list[dict[str, object]] = []
        for sheet in sheets:
            frame = sheet["frame"]
            assert isinstance(frame, pd.DataFrame)
            sheet_saturation = {str(column) for column in frame.columns if is_saturation_header(column)}
            X_all, _feature_columns = feature_table(frame, sheet_saturation)
            for feature in feature_columns:
                if feature not in X_all:
                    X_all[feature] = np.nan
            X_pred = clean_numeric_frame(X_all[feature_columns])
            row_mask = X_pred.notna().any(axis=1)
            if not row_mask.any():
                continue
            X_pred = X_pred.loc[row_mask].reset_index(drop=True)
            source_rows = frame.loc[row_mask].reset_index(drop=True)
            y_pred = model.predict(X_pred)
            prediction = pd.DataFrame(
                {
                    "target_id": target_id,
                    "target_column": target_column,
                    "source_workbook": sheet["workbook"],
                    "source_sheet": sheet["sheet"],
                    "row_index": source_rows.get("row_index", pd.Series(range(len(source_rows)))),
                    "y_pred": y_pred,
                    "prediction_status": "scored_unlabeled",
                }
            )
            if "well_alias" in source_rows:
                prediction["well_alias"] = source_rows["well_alias"]
            if "depth_m" in canonicalize_features(source_rows):
                prediction["depth_m"] = canonicalize_features(source_rows)["depth_m"]
            if target_column in source_rows:
                y_true = clean_numeric_series(source_rows[target_column])
                valid = y_true.notna()
                prediction.loc[valid, "y_true"] = y_true.loc[valid]
                prediction.loc[valid, "prediction_status"] = "scored_with_target"
                if valid.sum() >= 2:
                    metric_rows.append(
                        {
                            "target_id": target_id,
                            "source_workbook": sheet["workbook"],
                            "source_sheet": sheet["sheet"],
                            "rows_scored": int(valid.sum()),
                            "mae": float(mean_absolute_error(y_true.loc[valid], y_pred[valid])),
                            "rmse": float(np.sqrt(mean_squared_error(y_true.loc[valid], y_pred[valid]))),
                            "r2": float(r2_score(y_true.loc[valid], y_pred[valid])),
                        }
                    )
            workbook_stem = Path(str(sheet["workbook"])).stem
            prediction_path = target_output_dir / f"predictions_{sanitize_label(workbook_stem)}_{sanitize_label(sheet['sheet'])}.csv"
            prediction.to_csv(prediction_path, index=False)
            prediction_files.append(str(prediction_path))

        pd.DataFrame(metric_rows).to_csv(target_output_dir / "metrics_by_sheet.csv", index=False)
        summary_rows.append(
            {
                "target_id": target_id,
                "target_column": target_column,
                "target_workbook": target["workbook"],
                "target_sheet": target["sheet_name"],
                "status": "trained",
                "alignment_method": alignment_method,
                "feature_source": feature_source,
                "training_rows": int(len(X_train)),
                "feature_count": int(len(feature_columns)),
                "train_mae": float(mean_absolute_error(y_train, train_pred)),
                "train_rmse": float(np.sqrt(mean_squared_error(y_train, train_pred))),
                "train_r2": float(r2_score(y_train, train_pred)) if len(y_train) >= 2 else None,
                "prediction_file_count": len(prediction_files),
            }
        )

    run_summary = pd.DataFrame(summary_rows)
    run_summary.to_csv(output_dir / "run_summary.csv", index=False)
    pd.DataFrame(feature_rows).to_csv(output_dir / "feature_columns_by_target.csv", index=False)
    if feature_audit_rows:
        pd.concat(feature_audit_rows, ignore_index=True).to_csv(output_dir / "excluded_feature_columns_by_target.csv", index=False)
    manifest = {
        "status": "complete",
        "output_dir": str(output_dir),
        "feature_policy_version": FEATURE_POLICY_VERSION,
        "target_count": int(len(target_inventory)),
        "trained_target_count": int((run_summary["status"] == "trained").sum()) if not run_summary.empty else 0,
        "guardrail": "All saturation-like columns are treated as target-only Y variables, not model inputs.",
    }
    (output_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train/predict separate regressors for all saturation-like target columns.")
    parser.add_argument("--data-dir", type=Path, default=Path.home() / "Downloads" / "Northslopedatasets06052026")
    parser.add_argument("--workbooks", nargs="+", default=list(DEFAULT_WORKBOOKS))
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--min-training-rows", type=int, default=5)
    args, _unknown = parser.parse_known_args()
    return args


def main() -> None:
    args = parse_args()
    result = fit_and_predict_all_saturations(
        args.data_dir,
        workbook_names=tuple(args.workbooks),
        output_dir=args.output_dir,
        min_training_rows=args.min_training_rows,
    )
    print(json.dumps(result, indent=2))
    print(f"\nFeature policy version: {FEATURE_POLICY_VERSION}")
    print("\nOpen these files in the output folder:")
    print("saturation_target_inventory.csv")
    print("run_summary.csv")
    print("feature_columns_by_target.csv")
    print("excluded_feature_columns_by_target.csv")


if __name__ == "__main__":
    main()
