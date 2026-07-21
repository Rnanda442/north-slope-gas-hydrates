#!/usr/bin/env python3
"""Run ANN leave-one-well-out hydrate saturation scatters.

This GitHub-facing runner contains code only. It expects a private local model
matrix at runtime and writes row-level predictions only to an ignored runtime
output folder. Do not commit the model matrix or prediction CSVs.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


CODE_VERSION = "V26_ann_loo_scatter_plots"
DEFAULT_TARGET = "hydrate_saturation_reference"
DEFAULT_HELDOUT_WELLS = ["WellA", "WellB", "WellC", "WellD"]
DEFAULT_OCCURRENCE_THRESHOLD = 0.05
DEFAULT_WLC = "EQ_full_except_density_porosity_no_target_leakage"
SATURATION_BIN_EDGES = [-0.001, 0.01, 0.05, 0.20, 0.50, 1.000001]
SATURATION_BIN_LABELS = ["zero_trace", "trace_occurrence", "low", "moderate", "high"]
SATURATION_BIN_DISPLAY = {
    "zero_trace": "zero / trace",
    "trace_occurrence": "trace / occurrence",
    "low": "low",
    "moderate": "moderate",
    "high": "high",
}

WELL_METADATA = {
    "WellA": {"region": "Canada", "origin": "thermogenic", "color": "#6D5BD0"},
    "WellB": {"region": "Canada", "origin": "thermogenic", "color": "#3E7CB1"},
    "WellC": {"region": "Alaska", "origin": "thermogenic", "color": "#008C89"},
    "WellD": {"region": "Alaska", "origin": "mixed", "color": "#F56522"},
}

WLC_FEATURES = {
    "rho+phi+Rt": [
        "rhob_g_cc",
        "density_porosity_vv",
        "rt_ohm_m",
    ],
    "phi+Rt+Vp": [
        "density_porosity_vv",
        "rt_ohm_m",
        "vp_m_s",
    ],
    "GR+Rt+Vp": [
        "gr_api",
        "rt_ohm_m",
        "vp_m_s",
    ],
    "safe_normalized": [
        "gr_api",
        "rhob_g_cc",
        "density_porosity_vv",
        "neutron_porosity_vv",
        "rt_ohm_m",
        "vp_m_s",
        "vs_m_s",
        "log10_rt",
        "clean_sand_score",
    ],
    "EQ_full_except_density_porosity_no_target_leakage": [
        "rhob_g_cc",
        "gr_api",
        "rt_ohm_m",
        "vp_m_s",
        "vs_m_s",
        "log10_rt",
        "clean_sand_score",
        "vsh_larionov_tertiary",
        "vp_vs_ratio",
        "acoustic_impedance",
        "shear_impedance",
        "shear_modulus_gpa",
        "bulk_modulus_gpa",
        "youngs_modulus_gpa",
        "youngs_modulus_mpsi",
        "poisson_ratio",
        "lambda_rho",
        "mu_rho",
        "lr_term",
        "mr_term",
        "brittleness_youngs_pct",
        "brittleness_poisson_pct",
        "brittleness_total_pct",
    ],
}

REFERENCE_FINAL_ANN_METRICS = {
    "WellA": {
        "source": "V22 chong_wlc_summary",
        "wlc": "EQ_full_except_density_porosity_no_target_leakage",
        "r2_mean": 0.916840,
        "r2_std": 0.023614,
        "r2_min": 0.826746,
        "r2_max": 0.947180,
        "rmse_mean": 0.081088,
    },
    "WellC": {
        "source": "V25 chong_wlc_summary",
        "wlc": "EQ_full_except_density_porosity_no_target_leakage",
        "r2_mean": 0.763274,
        "r2_std": 0.027225,
        "r2_min": 0.668869,
        "r2_max": 0.800274,
        "rmse_mean": 0.130877,
    },
}

BLOCKED_COLUMNS = {
    DEFAULT_TARGET,
    "water_saturation_reference",
    "hydrate_occurrence_label",
    "occurrence_probability_screen",
    "sh_nmr_density_calc",
    "sw_archie_calc",
    "sh_archie_calc",
    "prediction",
    "reference",
    "residual",
    "well_alias",
    "well_name",
    "site",
    "source_workbook",
    "source_sheet",
    "lat",
    "lon",
}


def load_ml_globals() -> None:
    """Import heavy ML/plotting packages only when a real run is requested."""
    global SimpleImputer
    global MLPRegressor
    global mean_absolute_error
    global mean_squared_error
    global r2_score
    global MinMaxScaler
    global Pipeline
    global plt

    try:
        from sklearn.impute import SimpleImputer
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        from sklearn.neural_network import MLPRegressor
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import MinMaxScaler

        import matplotlib.pyplot as plt
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Missing ANN runner dependency. In the Anaconda/Python environment, install: "
            "pip install scikit-learn matplotlib pandas numpy pillow"
        ) from exc


@dataclass(frozen=True)
class AnnConfig:
    wlc_name: str
    hidden_layer_sizes: tuple[int, ...]
    activation: str
    solver: str
    learning_rate_init: float
    alpha: float
    batch_size: int | str
    max_iter: int
    early_stopping: bool
    validation_fraction: float
    n_iter_no_change: int
    seed_base: int
    seed_step: int
    realizations: int
    scatter_selection: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def runtime_output_dir() -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return repo_root() / "outputs_runtime" / "ann_loo_scatter_plots" / stamp


def parse_wells(raw: str | None) -> list[str]:
    if not raw:
        return list(DEFAULT_HELDOUT_WELLS)
    wells = [part.strip() for part in raw.replace(";", ",").split(",") if part.strip()]
    return wells or list(DEFAULT_HELDOUT_WELLS)


def parse_hidden_layers(raw: str) -> tuple[int, ...]:
    values = [int(part.strip()) for part in raw.replace(";", ",").split(",") if part.strip()]
    if not values:
        raise ValueError("hidden layer list cannot be empty")
    return tuple(values)


def normalize_fraction(values: pd.Series) -> pd.Series:
    out = pd.to_numeric(values, errors="coerce")
    finite = out[np.isfinite(out)]
    if not finite.empty and finite.quantile(0.95) > 1.5:
        out = out / 100.0
    return out.clip(0.0, 1.0)


def read_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"model matrix not found: {path}")
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if suffix == ".parquet":
        return pd.read_parquet(path)
    raise ValueError(f"unsupported model matrix file type: {path.suffix}")


def prepare_model_matrix(df: pd.DataFrame, target_col: str, source_label: str) -> pd.DataFrame:
    required = {"well_alias", target_col}
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"{source_label} missing required columns: {missing}")
    out = df.copy()
    out[target_col] = normalize_fraction(out[target_col])
    out = out[out[target_col].notna()].copy()
    if out.empty:
        raise ValueError(f"{source_label} has no non-null {target_col} rows")
    out["well_alias"] = out["well_alias"].astype(str)
    return out


def load_model_matrix(path: Path, target_col: str) -> pd.DataFrame:
    return prepare_model_matrix(read_table(path), target_col, f"model matrix {path}")


NOTEBOOK_MODEL_MATRIX_CANDIDATES = (
    "features_df",
    "model_matrix_df",
    "model_matrix",
    "model_df",
    "training_df",
    "ml_df",
    "active_df",
    "df",
)


def find_model_matrix_dataframe_in_namespace(
    namespace: dict[str, object],
    target_col: str,
    wlc_name: str,
    min_feature_count: int,
    compute_derived: bool,
) -> tuple[pd.DataFrame | None, str]:
    ordered_names = [name for name in NOTEBOOK_MODEL_MATRIX_CANDIDATES if name in namespace]
    ordered_names.extend(name for name in namespace if name not in ordered_names)

    candidates: list[tuple[tuple[int, int, int, int], str, pd.DataFrame]] = []
    seen_ids: set[int] = set()
    for name in ordered_names:
        value = namespace.get(name)
        if id(value) in seen_ids or not isinstance(value, pd.DataFrame):
            continue
        seen_ids.add(id(value))
        try:
            prepared = prepare_model_matrix(value, target_col, f"notebook dataframe {name!r}")
            feature_frame = add_derived_features(prepared) if compute_derived else prepared
            features, _ = selected_features(feature_frame, wlc_name, min_feature_count)
        except Exception:
            continue
        wells = sorted(prepared["well_alias"].dropna().astype(str).unique().tolist())
        preferred_rank = len(NOTEBOOK_MODEL_MATRIX_CANDIDATES)
        if name in NOTEBOOK_MODEL_MATRIX_CANDIDATES:
            preferred_rank = NOTEBOOK_MODEL_MATRIX_CANDIDATES.index(name)
        score = (-preferred_rank, len(features), len(wells), len(prepared))
        label = f"notebook dataframe `{name}`"
        candidates.append((score, label, value.copy()))

    if not candidates:
        return None, ""
    _, label, frame = max(candidates, key=lambda item: item[0])
    return frame, label


def find_notebook_model_matrix(
    target_col: str,
    wlc_name: str,
    min_feature_count: int,
    compute_derived: bool,
) -> tuple[pd.DataFrame | None, str]:
    try:
        ipython = get_ipython()  # type: ignore[name-defined]
    except NameError:
        return None, ""
    namespace = getattr(ipython, "user_ns", {}) or {}
    return find_model_matrix_dataframe_in_namespace(namespace, target_col, wlc_name, min_feature_count, compute_derived)


def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """Fill simple derived columns only when source columns exist."""
    out = df.copy()

    if "log10_rt" not in out.columns and "rt_ohm_m" in out.columns:
        rt = pd.to_numeric(out["rt_ohm_m"], errors="coerce")
        out["log10_rt"] = np.where(rt > 0, np.log10(rt), np.nan)

    if "vp_vs_ratio" not in out.columns and {"vp_m_s", "vs_m_s"}.issubset(out.columns):
        vp = pd.to_numeric(out["vp_m_s"], errors="coerce")
        vs = pd.to_numeric(out["vs_m_s"], errors="coerce")
        out["vp_vs_ratio"] = np.where(vs > 0, vp / vs, np.nan)

    if {"rhob_g_cc", "vp_m_s"}.issubset(out.columns):
        rho = pd.to_numeric(out["rhob_g_cc"], errors="coerce") * 1000.0
        vp = pd.to_numeric(out["vp_m_s"], errors="coerce")
        if "acoustic_impedance" not in out.columns:
            out["acoustic_impedance"] = rho * vp

    if {"rhob_g_cc", "vs_m_s"}.issubset(out.columns):
        rho = pd.to_numeric(out["rhob_g_cc"], errors="coerce") * 1000.0
        vs = pd.to_numeric(out["vs_m_s"], errors="coerce")
        if "shear_impedance" not in out.columns:
            out["shear_impedance"] = rho * vs
        if "shear_modulus_gpa" not in out.columns:
            out["shear_modulus_gpa"] = rho * (vs**2) / 1e9
        if "mu_rho" not in out.columns:
            out["mu_rho"] = rho * (vs**2)

    if {"rhob_g_cc", "vp_m_s", "vs_m_s"}.issubset(out.columns):
        rho = pd.to_numeric(out["rhob_g_cc"], errors="coerce") * 1000.0
        vp = pd.to_numeric(out["vp_m_s"], errors="coerce")
        vs = pd.to_numeric(out["vs_m_s"], errors="coerce")
        if "bulk_modulus_gpa" not in out.columns:
            out["bulk_modulus_gpa"] = rho * ((vp**2) - (4.0 / 3.0) * (vs**2)) / 1e9
        if "lambda_rho" not in out.columns:
            out["lambda_rho"] = rho * ((vp**2) - 2.0 * (vs**2))

    if "poisson_ratio" not in out.columns and "vp_vs_ratio" in out.columns:
        ratio = pd.to_numeric(out["vp_vs_ratio"], errors="coerce")
        denom = 2.0 * ((ratio**2) - 1.0)
        out["poisson_ratio"] = np.where(np.abs(denom) > 1e-12, ((ratio**2) - 2.0) / denom, np.nan)

    if "youngs_modulus_gpa" not in out.columns and {"shear_modulus_gpa", "poisson_ratio"}.issubset(out.columns):
        shear = pd.to_numeric(out["shear_modulus_gpa"], errors="coerce")
        pr = pd.to_numeric(out["poisson_ratio"], errors="coerce")
        out["youngs_modulus_gpa"] = 2.0 * shear * (1.0 + pr)

    if "youngs_modulus_mpsi" not in out.columns and "youngs_modulus_gpa" in out.columns:
        out["youngs_modulus_mpsi"] = pd.to_numeric(out["youngs_modulus_gpa"], errors="coerce") * 0.145038

    return out


def selected_features(df: pd.DataFrame, wlc_name: str, min_feature_count: int) -> tuple[list[str], list[str]]:
    if wlc_name not in WLC_FEATURES:
        raise ValueError(f"unknown WLC '{wlc_name}'. Choices: {', '.join(WLC_FEATURES)}")
    candidates = WLC_FEATURES[wlc_name]
    available = [feature for feature in candidates if feature in df.columns and feature not in BLOCKED_COLUMNS]
    missing = [feature for feature in candidates if feature not in available]
    if len(available) < min_feature_count:
        raise ValueError(
            f"WLC '{wlc_name}' has only {len(available)} available features; "
            f"need at least {min_feature_count}. Missing: {missing}"
        )
    return available, missing


def r2_safe(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    if len(y_true) < 2:
        return float("nan")
    return float(r2_score(y_true, y_pred))


def regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float | int]:
    return {
        "n": int(len(y_true)),
        "r2": r2_safe(y_true, y_pred),
        "rmse": float(math.sqrt(mean_squared_error(y_true, y_pred))),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "bias": float(np.mean(y_pred - y_true)),
        "reference_mean": float(np.mean(y_true)),
        "prediction_mean": float(np.mean(y_pred)),
    }


def occurrence_from_regression(y_true: np.ndarray, y_pred: np.ndarray, threshold: float) -> dict[str, float | int]:
    ref = y_true >= threshold
    pred = y_pred >= threshold
    tp = int(np.sum(ref & pred))
    tn = int(np.sum(~ref & ~pred))
    fp = int(np.sum(~ref & pred))
    fn = int(np.sum(ref & ~pred))
    recall = tp / (tp + fn) if (tp + fn) else float("nan")
    specificity = tn / (tn + fp) if (tn + fp) else float("nan")
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    accuracy = (tp + tn) / len(ref) if len(ref) else float("nan")
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    balanced = (recall + specificity) / 2.0 if np.isfinite(recall) and np.isfinite(specificity) else float("nan")
    return {
        "occurrence_accuracy": float(accuracy),
        "occurrence_balanced_accuracy": float(balanced),
        "occurrence_precision": float(precision),
        "occurrence_recall": float(recall),
        "occurrence_f1": float(f1),
        "occurrence_true_positive": tp,
        "occurrence_false_positive": fp,
        "occurrence_false_negative": fn,
        "occurrence_true_negative": tn,
        "occurrence_positive_rate_reference": float(np.mean(ref)),
        "occurrence_positive_rate_predicted": float(np.mean(pred)),
    }


def saturation_bin_bias(
    pred_df: pd.DataFrame,
    target_col: str,
    heldout_well: str,
    train_wells: str,
    wlc_name: str,
    realization: int,
    selection_strategy: str,
) -> pd.DataFrame:
    if pred_df.empty:
        return pd.DataFrame()
    temp = pred_df.copy()
    temp["reference"] = normalize_fraction(temp[target_col])
    temp["prediction"] = normalize_fraction(temp["prediction"])
    temp = temp[temp["reference"].notna() & temp["prediction"].notna()].copy()
    if temp.empty:
        return pd.DataFrame()
    temp["saturation_bin"] = pd.cut(
        temp["reference"],
        bins=SATURATION_BIN_EDGES,
        labels=SATURATION_BIN_LABELS,
        include_lowest=True,
    )
    rows = []
    for bin_name, group in temp.groupby("saturation_bin", observed=False):
        valid = group[["reference", "prediction"]].dropna()
        if valid.empty:
            continue
        residual = valid["prediction"].to_numpy(dtype=float) - valid["reference"].to_numpy(dtype=float)
        rows.append(
            {
                "heldout_well": heldout_well,
                "train_wells": train_wells,
                "wlc_name": wlc_name,
                "selected_realization": realization,
                "selected_strategy": selection_strategy,
                "saturation_bin": str(bin_name),
                "saturation_bin_label": SATURATION_BIN_DISPLAY.get(str(bin_name), str(bin_name)),
                "n": int(len(valid)),
                "bias": float(np.mean(residual)),
                "bias_pp": float(np.mean(residual) * 100.0),
                "mae_pp": float(np.mean(np.abs(residual)) * 100.0),
                "rmse_pp": float(math.sqrt(np.mean(residual**2)) * 100.0),
                "reference_mean_pp": float(valid["reference"].mean() * 100.0),
                "prediction_mean_pp": float(valid["prediction"].mean() * 100.0),
            }
        )
    return pd.DataFrame(rows)


def well_short_label(well: str) -> str:
    return well.replace("Well", "") if well.startswith("Well") else well


def bias_direction(value: object) -> str:
    if pd.isna(value):
        return "no rows"
    bias = float(value)
    if bias > 0.5:
        return "overpredict"
    if bias < -0.5:
        return "underpredict"
    return "near zero"


def build_slide8_bias_long(bin_bias_df: pd.DataFrame, selected_df: pd.DataFrame, heldout_wells: list[str]) -> pd.DataFrame:
    """Create one slide-ready row per held-out well and saturation bin.

    The workbook intentionally contains aggregate bin statistics only. It does
    not include row-level private predictions or the private model matrix.
    """
    selected_lookup = {}
    if not selected_df.empty:
        selected_lookup = {str(row["heldout_well"]): row for _, row in selected_df.iterrows()}

    rows: list[dict[str, object]] = []
    for heldout in heldout_wells:
        meta = WELL_METADATA.get(heldout, {})
        selected = selected_lookup.get(heldout, {})
        for order, bin_name in enumerate(SATURATION_BIN_LABELS, start=1):
            match = pd.DataFrame()
            if not bin_bias_df.empty:
                match = bin_bias_df[
                    bin_bias_df["heldout_well"].astype(str).eq(heldout)
                    & bin_bias_df["saturation_bin"].astype(str).eq(bin_name)
                ]
            if match.empty:
                values = {
                    "n": 0,
                    "bias": pd.NA,
                    "bias_pp": pd.NA,
                    "mae_pp": pd.NA,
                    "rmse_pp": pd.NA,
                    "reference_mean_pp": pd.NA,
                    "prediction_mean_pp": pd.NA,
                    "data_status": "no_rows_in_bin",
                }
            else:
                source = match.iloc[0]
                values = {
                    "n": int(source.get("n", 0)),
                    "bias": source.get("bias", pd.NA),
                    "bias_pp": source.get("bias_pp", pd.NA),
                    "mae_pp": source.get("mae_pp", pd.NA),
                    "rmse_pp": source.get("rmse_pp", pd.NA),
                    "reference_mean_pp": source.get("reference_mean_pp", pd.NA),
                    "prediction_mean_pp": source.get("prediction_mean_pp", pd.NA),
                    "data_status": "ok",
                }

            rows.append(
                {
                    "heldout_well": heldout,
                    "well_label": well_short_label(heldout),
                    "region": meta.get("region", ""),
                    "origin": meta.get("origin", ""),
                    "plot_color": meta.get("color", ""),
                    "train_wells": selected.get("train_wells", ""),
                    "wlc_name": selected.get("wlc_name", ""),
                    "selected_realization": selected.get("selected_realization", ""),
                    "selected_strategy": selected.get("selected_strategy", ""),
                    "saturation_bin_order": order,
                    "saturation_bin": bin_name,
                    "saturation_bin_label": SATURATION_BIN_DISPLAY.get(bin_name, bin_name),
                    **values,
                }
            )

    out = pd.DataFrame(rows)
    if not out.empty:
        out["bias_direction"] = out["bias_pp"].map(bias_direction)
        out["slide8_label"] = out.apply(
            lambda row: "" if pd.isna(row["bias_pp"]) else f"{float(row['bias_pp']):+.1f}",
            axis=1,
        )
    return out


def build_slide8_bias_wide(slide8_long: pd.DataFrame, heldout_wells: list[str]) -> pd.DataFrame:
    if slide8_long.empty:
        return pd.DataFrame()
    base_cols = ["saturation_bin_order", "saturation_bin", "saturation_bin_label"]
    base = slide8_long[base_cols].drop_duplicates().sort_values("saturation_bin_order").reset_index(drop=True)
    for heldout in heldout_wells:
        cut = slide8_long[slide8_long["heldout_well"].eq(heldout)].copy()
        label = well_short_label(heldout)
        keep = base_cols + ["bias_pp", "n", "data_status", "slide8_label"]
        cut = cut[keep].rename(
            columns={
                "bias_pp": f"{label}_bias_pp",
                "n": f"{label}_n",
                "data_status": f"{label}_data_status",
                "slide8_label": f"{label}_slide8_label",
            }
        )
        base = base.merge(cut, on=base_cols, how="left")
    return base


def format_excel_workbook(writer: pd.ExcelWriter) -> None:
    workbook = writer.book
    for worksheet in writer.sheets.values():
        worksheet.freeze_panes = "A2"
        worksheet.sheet_view.showGridLines = False
        for column_cells in worksheet.columns:
            values = [str(cell.value) if cell.value is not None else "" for cell in column_cells]
            width = min(max(max((len(value) for value in values), default=0) + 2, 10), 42)
            worksheet.column_dimensions[column_cells[0].column_letter].width = width
    for sheet_name in ["slide8_bias_long", "slide8_bias_wide"]:
        if sheet_name in writer.sheets:
            ws = writer.sheets[sheet_name]
            for cell in ws[1]:
                cell.font = cell.font.copy(bold=True)
    if "README" in writer.sheets:
        ws = writer.sheets["README"]
        ws.column_dimensions["A"].width = 28
        ws.column_dimensions["B"].width = 92
        for cell in ws[1]:
            cell.font = cell.font.copy(bold=True)
    workbook.active = workbook.sheetnames.index("slide8_bias_long") if "slide8_bias_long" in workbook.sheetnames else 0


def write_slide8_excel_workbook(
    output_dir: Path,
    selected_df: pd.DataFrame,
    bin_bias_df: pd.DataFrame,
    heldout_wells: list[str],
    cfg: AnnConfig,
    target_col: str,
    occurrence_threshold: float,
) -> tuple[Path, pd.DataFrame, pd.DataFrame]:
    workbook_path = output_dir / "ann_loo_slide8_saturation_bin_bias.xlsx"
    slide8_long = build_slide8_bias_long(bin_bias_df, selected_df, heldout_wells)
    slide8_wide = build_slide8_bias_wide(slide8_long, heldout_wells)
    readme = pd.DataFrame(
        [
            {"field": "purpose", "value": "Slide 8 source workbook: ANN prediction minus reference by saturation bin for every held-out well."},
            {"field": "data_boundary", "value": "Aggregate bin statistics only; no row-level predictions, private model matrix, or trained model bundle."},
            {"field": "bias_definition", "value": "bias_pp = mean(ANN prediction - reference hydrate saturation) in percentage points."},
            {"field": "bin_source", "value": "Rows are binned by reference hydrate saturation."},
            {"field": "well_scope", "value": ", ".join(heldout_wells)},
            {"field": "wlc_name", "value": cfg.wlc_name},
            {"field": "target_column", "value": target_col},
            {"field": "occurrence_threshold", "value": occurrence_threshold},
            {"field": "missing_bin_rule", "value": "If a well has no rows in a bin, n=0 and bias fields stay blank."},
            {"field": "recommended_slide_sheet", "value": "Use slide8_bias_wide for plotting and slide8_bias_long for audit labels."},
        ]
    )
    try:
        with pd.ExcelWriter(workbook_path, engine="openpyxl") as writer:
            slide8_long.to_excel(writer, sheet_name="slide8_bias_long", index=False)
            slide8_wide.to_excel(writer, sheet_name="slide8_bias_wide", index=False)
            selected_df.to_excel(writer, sheet_name="fold_summary", index=False)
            readme.to_excel(writer, sheet_name="README", index=False)
            format_excel_workbook(writer)
    except ModuleNotFoundError as exc:
        raise SystemExit("Missing Excel dependency. Install with: pip install openpyxl") from exc
    return workbook_path, slide8_long, slide8_wide


def copy_slide8_workbook(workbook_path: Path, copy_dir: Path | None, copy_to_downloads: bool) -> list[Path]:
    targets: list[Path] = []
    if copy_dir is not None:
        targets.append(copy_dir)
    if copy_to_downloads:
        targets.append(Path.home() / "Downloads")

    copied: list[Path] = []
    seen: set[Path] = set()
    for target_dir in targets:
        resolved = target_dir.expanduser().resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        resolved.mkdir(parents=True, exist_ok=True)
        dest = resolved / workbook_path.name
        shutil.copy2(workbook_path, dest)
        copied.append(dest)
    return copied


def make_ann(seed: int, cfg: AnnConfig) -> Pipeline:
    ann = MLPRegressor(
        hidden_layer_sizes=cfg.hidden_layer_sizes,
        activation=cfg.activation,
        solver=cfg.solver,
        learning_rate_init=cfg.learning_rate_init,
        alpha=cfg.alpha,
        batch_size=cfg.batch_size,
        max_iter=cfg.max_iter,
        early_stopping=cfg.early_stopping,
        validation_fraction=cfg.validation_fraction,
        n_iter_no_change=cfg.n_iter_no_change,
        random_state=seed,
    )
    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", MinMaxScaler()),
            ("ann", ann),
        ]
    )


def choose_realization(metrics: pd.DataFrame, strategy: str) -> int:
    if metrics.empty:
        raise ValueError("cannot choose from empty realization metrics")
    if strategy == "best_r2":
        row = metrics.sort_values(["r2", "rmse"], ascending=[False, True]).iloc[0]
    elif strategy == "median_r2":
        temp = metrics.copy()
        median = temp["r2"].median()
        temp["distance_to_median_r2"] = (temp["r2"] - median).abs()
        row = temp.sort_values(["distance_to_median_r2", "rmse"], ascending=[True, True]).iloc[0]
    elif strategy == "first":
        row = metrics.sort_values("realization").iloc[0]
    else:
        raise ValueError("scatter_selection must be one of: best_r2, median_r2, first")
    return int(row["realization"])


def plot_scatter(
    pred_df: pd.DataFrame,
    heldout_well: str,
    cfg: AnnConfig,
    selected_row: pd.Series,
    output_path: Path,
    target_col: str,
) -> None:
    meta = WELL_METADATA.get(heldout_well, {})
    color = str(meta.get("color", "#008C89"))
    region = str(meta.get("region", ""))
    origin = str(meta.get("origin", ""))
    reference = pred_df[target_col].to_numpy() * 100.0
    prediction = pred_df["prediction"].to_numpy() * 100.0

    fig, ax = plt.subplots(figsize=(7.2, 5.4), dpi=180)
    ax.scatter(reference, prediction, s=13, alpha=0.46, c=color, edgecolors="none")
    ax.plot([0, 100], [0, 100], linestyle="--", linewidth=1.2, color="#102536")
    ax.set_xlim(-3, 103)
    ax.set_ylim(-3, 103)
    ax.set_xlabel("Reference hydrate saturation (%)", fontsize=11)
    ax.set_ylabel("ANN prediction (%)", fontsize=11)
    ax.grid(True, color="#D8E5EA", linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)
    title = f"Held-out {heldout_well}: ANN predicted vs reference"
    subtitle = f"{region} {origin} | WLC: {cfg.wlc_name}"
    ax.set_title(title + "\n" + subtitle, fontsize=12, fontweight="bold", color="#102536", pad=10)
    text = (
        f"R2 {selected_row['r2']:.3f}\n"
        f"RMSE {selected_row['rmse'] * 100:.1f} pp\n"
        f"n {int(selected_row['n']):,}"
    )
    ax.text(
        0.05,
        0.95,
        text,
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=10,
        color="#102536",
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "#CBD6DC", "alpha": 0.92},
    )
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def plot_contact_sheet(image_paths: list[Path], output_path: Path) -> None:
    if not image_paths:
        return
    from PIL import Image

    images = [Image.open(path).convert("RGB") for path in image_paths]
    thumb_w, thumb_h = 720, 540
    thumbs = []
    for image in images:
        image.thumbnail((thumb_w, thumb_h))
        canvas = Image.new("RGB", (thumb_w, thumb_h), "white")
        left = (thumb_w - image.width) // 2
        top = (thumb_h - image.height) // 2
        canvas.paste(image, (left, top))
        thumbs.append(canvas)
    cols = 2
    rows = int(math.ceil(len(thumbs) / cols))
    sheet = Image.new("RGB", (cols * thumb_w, rows * thumb_h), "white")
    for idx, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((idx % cols) * thumb_w, (idx // cols) * thumb_h))
    sheet.save(output_path)


def ps_quote(path: Path) -> str:
    return "'" + str(path).replace("'", "''") + "'"


def copy_existing(src: Path, dest_dir: Path, copied_paths: list[Path], subdir: str | None = None) -> Path | None:
    if not src.exists():
        return None
    target_dir = dest_dir / subdir if subdir else dest_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    dest = target_dir / src.name
    shutil.copy2(src, dest)
    copied_paths.append(dest)
    return dest


def write_email_packet(
    output_dir: Path,
    cfg: AnnConfig,
    model_matrix_label: str,
    heldout_wells: list[str],
    features: list[str],
    selected_df: pd.DataFrame,
    metrics_path: Path,
    selected_path: Path,
    bin_bias_path: Path,
    slide8_workbook_path: Path,
    weights_path: Path,
    contact_sheet_path: Path,
    figure_paths: list[Path],
    note_path: Path,
    open_outlook_draft: bool,
) -> dict[str, object]:
    review_dir = output_dir / "ann_loo_email_packet"
    review_dir.mkdir(parents=True, exist_ok=True)

    copied_paths: list[Path] = []
    review_metrics_path = copy_existing(metrics_path, review_dir, copied_paths)
    review_summary_path = copy_existing(selected_path, review_dir, copied_paths)
    review_bin_bias_path = copy_existing(bin_bias_path, review_dir, copied_paths)
    review_slide8_workbook_path = copy_existing(slide8_workbook_path, review_dir, copied_paths)
    review_weights_path = copy_existing(weights_path, review_dir, copied_paths)
    review_contact_sheet_path = copy_existing(contact_sheet_path, review_dir, copied_paths)
    copy_existing(note_path, review_dir, copied_paths)
    review_figure_paths = [p for p in (copy_existing(path, review_dir, copied_paths, subdir="figures") for path in figure_paths) if p]

    share_manifest_path = review_dir / "ann_loo_share_manifest.json"
    share_manifest = {
        "code_version": CODE_VERSION,
        "created": datetime.now().isoformat(timespec="seconds"),
        "wlc_name": cfg.wlc_name,
        "heldout_wells": heldout_wells,
        "features_used": features,
        "scatter_selection": cfg.scatter_selection,
        "model_matrix_name_only": model_matrix_label,
        "row_level_predictions_included": False,
        "summary_rows": selected_df.to_dict(orient="records"),
        "boundary_note": "Compact packet for review. It excludes row-level prediction CSVs and the private model matrix.",
    }
    share_manifest_path.write_text(json.dumps(share_manifest, indent=2), encoding="utf-8")
    copied_paths.append(share_manifest_path)

    packet_readme_path = review_dir / "ANN_LOO_EMAIL_PACKET_README.txt"
    packet_readme_path.write_text(
        "\n".join(
            [
                f"North Slope Gas Hydrate ML {CODE_VERSION} ANN scatter packet",
                f"Created: {datetime.now().isoformat(timespec='seconds')}",
                f"WLC: {cfg.wlc_name}",
                f"Held-out wells: {' + '.join(heldout_wells)}",
                "",
                "This packet is the compact handoff output for ANN-only held-out-well scatter plots.",
                "It excludes the private model matrix and row-level prediction CSVs.",
                "",
                "Use first:",
                "- ann_loo_scatter_contact_sheet.png for the four scatter plots in one image.",
                "- ann_loo_fold_summary.csv for the selected R2/RMSE values.",
                "- ann_loo_selected_saturation_bin_bias.csv for ANN bias by saturation bin.",
                "- ann_loo_slide8_saturation_bin_bias.xlsx for slide-ready A-D bin-bias tables.",
                "- figures/ for individual held-out-well scatter PNGs.",
                "",
                "Wording note:",
                "- WLC feature weights are input-feature weights, not neural-network hidden-layer weights.",
                "- If best_r2 is used, call the plot a best-realization visual, not an unbiased model-selection claim.",
                "",
                "Review before sending outside the DOE environment.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    copied_paths.append(packet_readme_path)

    share_packet_zip = review_dir / f"share_packet_{CODE_VERSION}.zip"
    packet_files = [path for path in copied_paths if path.exists() and path != share_packet_zip]
    with zipfile.ZipFile(share_packet_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in packet_files:
            zf.write(path, arcname=str(path.relative_to(review_dir)))

    outlook_script_path = review_dir / f"open_outlook_draft_{CODE_VERSION}.ps1"
    attachments = [
        share_packet_zip,
        review_slide8_workbook_path,
        review_contact_sheet_path,
        review_summary_path,
        packet_readme_path,
    ]
    attachment_array = ", ".join(ps_quote(path) for path in attachments if path and path.exists())
    outlook_script_path.write_text(
        f'''$ErrorActionPreference = "Stop"
$to = $env:PERSONAL_REVIEW_EMAIL
$attachments = @({attachment_array})
$outlook = New-Object -ComObject Outlook.Application
$mail = $outlook.CreateItem(0)
if ($to) {{ $mail.To = $to }}
$mail.Subject = "North Slope ML {CODE_VERSION} ANN scatter packet"
$mail.Body = @"
Attached is the compact ANN leave-one-well-out scatter packet.

Review folder:
{review_dir}

This packet is intended for review only. Please check the data boundary before sending outside the DOE environment.
"@
foreach ($packetPath in $attachments) {{
    if (Test-Path -LiteralPath $packetPath) {{
        $mail.Attachments.Add($packetPath) | Out-Null
    }}
}}
$mail.Save()
$mail.Display()
try {{ $mail.GetInspector.Activate() }} catch {{}}
Write-Host "Saved and opened Outlook draft."
Write-Host "Review folder: {review_dir}"
Write-Host "Attachments:"
$attachments | ForEach-Object {{ Write-Host " - $_" }}
''',
        encoding="utf-8",
    )

    audit_path = review_dir / "ann_loo_email_packet_audit.csv"
    required_artifacts = [
        ("share_packet_zip", share_packet_zip),
        ("contact_sheet_png", review_contact_sheet_path),
        ("fold_summary_csv", review_summary_path),
        ("selected_saturation_bin_bias_csv", review_bin_bias_path),
        ("slide8_saturation_bin_bias_xlsx", review_slide8_workbook_path),
        ("metrics_by_realization_csv", review_metrics_path),
        ("wlc_feature_weights_csv", review_weights_path),
        ("packet_readme", packet_readme_path),
        ("share_manifest_json", share_manifest_path),
        ("outlook_draft_helper", outlook_script_path),
    ]
    audit_df = pd.DataFrame(
        [
            {
                "artifact": name,
                "path": str(path) if path else "",
                "exists": bool(path and path.exists()),
                "size_bytes": path.stat().st_size if path and path.exists() and path.is_file() else None,
            }
            for name, path in required_artifacts
        ]
    )
    audit_df.to_csv(audit_path, index=False)
    with zipfile.ZipFile(share_packet_zip, "a", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(audit_path, arcname=audit_path.name)

    outlook_status = f"automatic Outlook draft skipped; run {outlook_script_path} manually"
    if open_outlook_draft and os.name == "nt":
        try:
            completed = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(outlook_script_path),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=90,
            )
            outlook_status = f"PowerShell exit code {completed.returncode}"
            if completed.stdout.strip():
                print("ANN LOO Outlook helper stdout:")
                print(completed.stdout.strip())
            if completed.stderr.strip():
                print("ANN LOO Outlook helper stderr:")
                print(completed.stderr.strip())
        except Exception as exc:
            outlook_status = f"automatic Outlook draft failed: {exc}"
            print("ANN LOO Outlook draft helper did not run automatically:", exc)

    return {
        "email_packet_dir": str(review_dir),
        "share_packet_zip": str(share_packet_zip),
        "packet_readme": str(packet_readme_path),
        "packet_audit_csv": str(audit_path),
        "outlook_draft_script": str(outlook_script_path),
        "outlook_draft_status": outlook_status,
        "review_contact_sheet": str(review_contact_sheet_path) if review_contact_sheet_path else "",
        "review_fold_summary": str(review_summary_path) if review_summary_path else "",
        "review_slide8_workbook": str(review_slide8_workbook_path) if review_slide8_workbook_path else "",
        "review_figures": [str(path) for path in review_figure_paths],
    }


def run_ann_loo(
    model_matrix: Path | None,
    output_dir: Path,
    target_col: str,
    heldout_wells: list[str],
    cfg: AnnConfig,
    min_feature_count: int,
    compute_derived: bool,
    save_private_predictions: bool,
    occurrence_threshold: float,
    create_email_packet: bool,
    open_outlook_draft: bool,
    slide8_excel_copy_dir: Path | None,
    copy_slide8_excel_to_downloads: bool,
    model_matrix_df: pd.DataFrame | None = None,
    model_matrix_source: str = "",
) -> dict[str, object]:
    load_ml_globals()
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_dir = output_dir / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)

    if model_matrix_df is not None:
        model_matrix_input_mode = "notebook_dataframe"
        model_matrix_label = model_matrix_source or "notebook dataframe"
        df = prepare_model_matrix(model_matrix_df, target_col, model_matrix_label)
    elif model_matrix is not None:
        model_matrix_input_mode = "file"
        model_matrix_label = model_matrix.name
        df = load_model_matrix(model_matrix, target_col)
    else:
        raise ValueError("Provide a model-matrix path or notebook dataframe.")

    if compute_derived:
        df = add_derived_features(df)

    features, missing_features = selected_features(df, cfg.wlc_name, min_feature_count)
    all_wells = sorted(df["well_alias"].dropna().unique())
    unknown = sorted(set(heldout_wells).difference(all_wells))
    if unknown:
        raise ValueError(f"heldout wells not found in model matrix: {unknown}; available wells: {all_wells}")

    feature_weights = pd.DataFrame(
        {
            "wlc_name": cfg.wlc_name,
            "feature": features,
            "weight_used_before_scaling": 1.0,
            "weight_note": "Selected WLC input feature; not a neural-network hidden-layer weight.",
        }
    )

    metric_rows: list[dict[str, object]] = []
    selected_rows: list[dict[str, object]] = []
    bin_bias_rows: list[dict[str, object]] = []
    prediction_frames: list[pd.DataFrame] = []
    figure_paths: list[Path] = []

    for heldout in heldout_wells:
        train_wells = [well for well in all_wells if well != heldout and well in heldout_wells]
        train_df = df[df["well_alias"].isin(train_wells)].copy()
        test_df = df[df["well_alias"].eq(heldout)].copy()
        if train_df.empty or test_df.empty:
            raise ValueError(f"empty train/test split for heldout {heldout}")

        x_train = train_df[features].apply(pd.to_numeric, errors="coerce")
        y_train = train_df[target_col].to_numpy(dtype=float)
        x_test = test_df[features].apply(pd.to_numeric, errors="coerce")
        y_test = test_df[target_col].to_numpy(dtype=float)

        fold_predictions: list[pd.DataFrame] = []
        fold_metrics: list[dict[str, object]] = []
        for realization in range(1, cfg.realizations + 1):
            seed = cfg.seed_base + (realization - 1) * cfg.seed_step
            model = make_ann(seed, cfg)
            model.fit(x_train, y_train)
            pred = np.clip(model.predict(x_test), 0.0, 1.0)
            metrics = regression_metrics(y_test, pred)
            metrics.update(occurrence_from_regression(y_test, pred, occurrence_threshold))
            row = {
                "heldout_well": heldout,
                "train_wells": "+".join(train_wells),
                "wlc_name": cfg.wlc_name,
                "realization": realization,
                "seed": seed,
                "selected_for_scatter": False,
                **metrics,
            }
            fold_metrics.append(row)

            pred_df = test_df[["well_alias", target_col]].copy()
            for optional in ["well_name", "site", "depth_m", "depth_ft"]:
                if optional in test_df.columns:
                    pred_df[optional] = test_df[optional].values
            pred_df["prediction"] = pred
            pred_df["realization"] = realization
            pred_df["seed"] = seed
            pred_df["heldout_well"] = heldout
            pred_df["train_wells"] = "+".join(train_wells)
            pred_df["wlc_name"] = cfg.wlc_name
            fold_predictions.append(pred_df)

        fold_metric_df = pd.DataFrame(fold_metrics)
        selected_realization = choose_realization(fold_metric_df, cfg.scatter_selection)
        fold_metric_df.loc[fold_metric_df["realization"].eq(selected_realization), "selected_for_scatter"] = True
        metric_rows.extend(fold_metric_df.to_dict(orient="records"))

        selected_metric = fold_metric_df[fold_metric_df["realization"].eq(selected_realization)].iloc[0]
        selected_prediction = [p for p in fold_predictions if int(p["realization"].iloc[0]) == selected_realization][0]
        if save_private_predictions:
            prediction_frames.append(selected_prediction)
        bin_bias_rows.extend(
            saturation_bin_bias(
                selected_prediction,
                target_col=target_col,
                heldout_well=heldout,
                train_wells="+".join(train_wells),
                wlc_name=cfg.wlc_name,
                realization=selected_realization,
                selection_strategy=cfg.scatter_selection,
            ).to_dict(orient="records")
        )

        figure_path = figure_dir / f"ann_loo_scatter_{heldout.lower()}_{cfg.wlc_name}.png"
        plot_scatter(selected_prediction, heldout, cfg, selected_metric, figure_path, target_col)
        figure_paths.append(figure_path)

        reference = REFERENCE_FINAL_ANN_METRICS.get(heldout, {})
        selected_rows.append(
            {
                "heldout_well": heldout,
                "train_wells": "+".join(train_wells),
                "wlc_name": cfg.wlc_name,
                "selected_realization": selected_realization,
                "selected_strategy": cfg.scatter_selection,
                "selected_r2": float(selected_metric["r2"]),
                "selected_rmse": float(selected_metric["rmse"]),
                "selected_occurrence_balanced_accuracy": float(selected_metric["occurrence_balanced_accuracy"]),
                "selected_occurrence_accuracy": float(selected_metric["occurrence_accuracy"]),
                "selected_occurrence_precision": float(selected_metric["occurrence_precision"]),
                "selected_occurrence_recall": float(selected_metric["occurrence_recall"]),
                "selected_occurrence_f1": float(selected_metric["occurrence_f1"]),
                "selected_occurrence_reference_positive_rate": float(selected_metric["occurrence_positive_rate_reference"]),
                "selected_occurrence_predicted_positive_rate": float(selected_metric["occurrence_positive_rate_predicted"]),
                "selected_occurrence_true_positive": int(selected_metric["occurrence_true_positive"]),
                "selected_occurrence_false_positive": int(selected_metric["occurrence_false_positive"]),
                "selected_occurrence_false_negative": int(selected_metric["occurrence_false_negative"]),
                "selected_occurrence_true_negative": int(selected_metric["occurrence_true_negative"]),
                "mean_r2_across_realizations": float(fold_metric_df["r2"].mean()),
                "median_r2_across_realizations": float(fold_metric_df["r2"].median()),
                "max_r2_across_realizations": float(fold_metric_df["r2"].max()),
                "mean_occurrence_balanced_accuracy_across_realizations": float(
                    fold_metric_df["occurrence_balanced_accuracy"].mean()
                ),
                "reference_prior_r2_mean_if_available": reference.get("r2_mean", ""),
                "reference_prior_rmse_mean_if_available": reference.get("rmse_mean", ""),
                "reference_source": reference.get("source", ""),
                "figure_path": str(figure_path),
            }
        )

    metrics_df = pd.DataFrame(metric_rows)
    selected_df = pd.DataFrame(selected_rows)
    bin_bias_df = pd.DataFrame(bin_bias_rows)
    metrics_path = output_dir / "ann_loo_metrics_by_realization.csv"
    selected_path = output_dir / "ann_loo_fold_summary.csv"
    bin_bias_path = output_dir / "ann_loo_selected_saturation_bin_bias.csv"
    weights_path = output_dir / "ann_loo_wlc_feature_weights.csv"
    metrics_df.to_csv(metrics_path, index=False)
    selected_df.to_csv(selected_path, index=False)
    bin_bias_df.to_csv(bin_bias_path, index=False)
    feature_weights.to_csv(weights_path, index=False)
    slide8_workbook_path, slide8_long_df, slide8_wide_df = write_slide8_excel_workbook(
        output_dir=output_dir,
        selected_df=selected_df,
        bin_bias_df=bin_bias_df,
        heldout_wells=heldout_wells,
        cfg=cfg,
        target_col=target_col,
        occurrence_threshold=occurrence_threshold,
    )
    slide8_copied_paths = copy_slide8_workbook(
        slide8_workbook_path,
        copy_dir=slide8_excel_copy_dir,
        copy_to_downloads=copy_slide8_excel_to_downloads,
    )

    predictions_path = ""
    if save_private_predictions and prediction_frames:
        predictions_path = str(output_dir / "ann_loo_selected_predictions_private.csv")
        pd.concat(prediction_frames, ignore_index=True).to_csv(predictions_path, index=False)

    contact_sheet_path = output_dir / "ann_loo_scatter_contact_sheet.png"
    plot_contact_sheet(figure_paths, contact_sheet_path)

    note = output_dir / "ann_loo_readme.md"
    note.write_text(
        "\n".join(
            [
                "# ANN LOO Scatter Output",
                "",
                f"Code version: `{CODE_VERSION}`",
                f"WLC: `{cfg.wlc_name}`",
                f"Scatter selection: `{cfg.scatter_selection}`",
                "",
                "Use these figures as ANN-only held-out-well scatter visuals.",
                "Do not commit row-level prediction CSVs or private model matrices.",
                "",
                "Important wording:",
                "- WLC feature weights are input-selection weights, not neural hidden-layer weights.",
                "- If `best_r2` selection is used, the figure is a best-realization visualization, not an unbiased model-selection claim.",
                f"- Slide 8 workbook: `{slide8_workbook_path.name}` contains A-D bin-bias tables.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    email_outputs: dict[str, object] = {}
    if create_email_packet:
        email_outputs = write_email_packet(
            output_dir=output_dir,
            cfg=cfg,
            model_matrix_label=model_matrix_label,
            heldout_wells=heldout_wells,
            features=features,
            selected_df=selected_df,
            metrics_path=metrics_path,
            selected_path=selected_path,
            bin_bias_path=bin_bias_path,
            slide8_workbook_path=slide8_workbook_path,
            weights_path=weights_path,
            contact_sheet_path=contact_sheet_path,
            figure_paths=figure_paths,
            note_path=note,
            open_outlook_draft=open_outlook_draft,
        )

    manifest = {
        "code_version": CODE_VERSION,
        "created": datetime.now().isoformat(timespec="seconds"),
        "model_matrix": str(model_matrix) if model_matrix is not None else model_matrix_label,
        "model_matrix_input_mode": model_matrix_input_mode,
        "target_column": target_col,
        "heldout_wells": heldout_wells,
        "available_wells": all_wells,
        "ann_config": asdict(cfg),
        "features_used": features,
        "features_missing_from_wlc": missing_features,
        "reference_final_ann_metrics": REFERENCE_FINAL_ANN_METRICS,
        "outputs": {
            "metrics_by_realization": str(metrics_path),
            "fold_summary": str(selected_path),
            "selected_saturation_bin_bias": str(bin_bias_path),
            "slide8_saturation_bin_bias_workbook": str(slide8_workbook_path),
            "slide8_saturation_bin_bias_workbook_copies": [str(path) for path in slide8_copied_paths],
            "slide8_bias_long_rows": int(len(slide8_long_df)),
            "slide8_bias_wide_rows": int(len(slide8_wide_df)),
            "wlc_feature_weights": str(weights_path),
            "private_selected_predictions": predictions_path,
            "figure_dir": str(figure_dir),
            "contact_sheet": str(contact_sheet_path),
            "readme": str(note),
            **email_outputs,
        },
        "boundary_note": "Runtime outputs may contain private row-level predictions. Keep them out of GitHub unless separately reviewed.",
    }
    manifest_path = output_dir / "ann_loo_run_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def print_plan(args: argparse.Namespace) -> None:
    cfg = AnnConfig(
        wlc_name=args.wlc,
        hidden_layer_sizes=parse_hidden_layers(args.hidden_layers),
        activation=args.activation,
        solver=args.solver,
        learning_rate_init=args.learning_rate_init,
        alpha=args.alpha,
        batch_size=args.batch_size if args.batch_size == "auto" else int(args.batch_size),
        max_iter=args.max_iter,
        early_stopping=args.early_stopping,
        validation_fraction=args.validation_fraction,
        n_iter_no_change=args.n_iter_no_change,
        seed_base=args.seed_base,
        seed_step=args.seed_step,
        realizations=args.realizations,
        scatter_selection=args.scatter_selection,
    )
    plan = {
        "code_version": CODE_VERSION,
        "required_private_input": ["well_alias", args.target_column],
        "notebook_input_fallback": "If --model-matrix-csv is omitted in Jupyter, the runner looks for a usable `features_df` dataframe.",
        "heldout_wells": parse_wells(args.heldout_wells),
        "default_wlc": args.wlc,
        "default_wlc_features": WLC_FEATURES[args.wlc],
        "ann_config": asdict(cfg),
        "known_reference_metrics": REFERENCE_FINAL_ANN_METRICS,
        "default_output_dir": str(runtime_output_dir()),
        "email_packet": {
            "created_by_default": True,
            "contents": [
                "share_packet_V26_ann_loo_scatter_plots.zip",
                "ann_loo_scatter_contact_sheet.png",
                "ann_loo_fold_summary.csv",
                "ann_loo_selected_saturation_bin_bias.csv",
                "ann_loo_slide8_saturation_bin_bias.xlsx",
                "individual scatter PNGs",
                "Outlook draft helper PowerShell script",
            ],
            "automatic_outlook_draft_default": os.name == "nt",
        },
        "slide8_excel": {
            "created_by_default": True,
            "output_name": "ann_loo_slide8_saturation_bin_bias.xlsx",
            "sheets": ["slide8_bias_long", "slide8_bias_wide", "fold_summary", "README"],
            "copy_to_downloads_flag": "--copy-slide8-excel-to-downloads",
            "copy_to_custom_dir_flag": "--slide8-excel-copy-dir",
        },
        "boundary_note": "Code can go to GitHub. Private model matrices and row-level predictions should not.",
    }
    print(json.dumps(plan, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run ANN-only leave-one-well-out scatter plots for North Slope hydrate saturation.")
    parser.add_argument("--model-matrix-csv", default=os.environ.get("ANN_LOO_MODEL_MATRIX", ""))
    parser.add_argument("--output-dir", default=os.environ.get("ANN_LOO_OUTPUT_DIR", ""))
    parser.add_argument("--target-column", default=os.environ.get("ANN_LOO_TARGET_COLUMN", DEFAULT_TARGET))
    parser.add_argument("--heldout-wells", default=os.environ.get("ANN_LOO_HELDOUT_WELLS", ",".join(DEFAULT_HELDOUT_WELLS)))
    parser.add_argument("--wlc", default=os.environ.get("ANN_LOO_WLC", DEFAULT_WLC), choices=sorted(WLC_FEATURES))
    parser.add_argument("--hidden-layers", default=os.environ.get("ANN_LOO_HIDDEN_LAYERS", "40,40"))
    parser.add_argument("--activation", default=os.environ.get("ANN_LOO_ACTIVATION", "relu"))
    parser.add_argument("--solver", default=os.environ.get("ANN_LOO_SOLVER", "adam"))
    parser.add_argument("--learning-rate-init", type=float, default=float(os.environ.get("ANN_LOO_LEARNING_RATE", "0.001")))
    parser.add_argument("--alpha", type=float, default=float(os.environ.get("ANN_LOO_ALPHA", "0.0001")))
    parser.add_argument("--batch-size", default=os.environ.get("ANN_LOO_BATCH_SIZE", "100"))
    parser.add_argument("--max-iter", type=int, default=int(os.environ.get("ANN_LOO_MAX_ITER", "500")))
    parser.add_argument("--early-stopping", action="store_true", help="Use sklearn MLP early stopping inside the training wells only.")
    parser.add_argument("--validation-fraction", type=float, default=float(os.environ.get("ANN_LOO_VALIDATION_FRACTION", "0.15")))
    parser.add_argument("--n-iter-no-change", type=int, default=int(os.environ.get("ANN_LOO_N_ITER_NO_CHANGE", "30")))
    parser.add_argument("--realizations", type=int, default=int(os.environ.get("ANN_LOO_REALIZATIONS", "100")))
    parser.add_argument("--seed-base", type=int, default=int(os.environ.get("ANN_LOO_SEED_BASE", "4659")))
    parser.add_argument("--seed-step", type=int, default=int(os.environ.get("ANN_LOO_SEED_STEP", "37")))
    parser.add_argument(
        "--scatter-selection",
        default=os.environ.get("ANN_LOO_SCATTER_SELECTION", "best_r2"),
        choices=["best_r2", "median_r2", "first"],
        help="Which realization to use for each scatter plot.",
    )
    parser.add_argument("--min-feature-count", type=int, default=int(os.environ.get("ANN_LOO_MIN_FEATURE_COUNT", "3")))
    parser.add_argument("--no-compute-derived", action="store_true", help="Do not add simple derived features such as log10_rt or impedance.")
    parser.add_argument("--no-private-predictions", action="store_true", help="Skip row-level selected prediction CSV output.")
    parser.add_argument("--no-email-packet", action="store_true", help="Skip compact ZIP packet and Outlook draft helper output.")
    parser.add_argument("--no-open-outlook-draft", action="store_true", help="Create the packet/helper but do not automatically open Outlook.")
    parser.add_argument(
        "--slide8-excel-copy-dir",
        default=os.environ.get("ANN_LOO_SLIDE8_EXCEL_COPY_DIR", ""),
        help="Optional folder to receive a copy of ann_loo_slide8_saturation_bin_bias.xlsx, such as a Google Drive sync folder.",
    )
    parser.add_argument(
        "--copy-slide8-excel-to-downloads",
        action="store_true",
        default=os.environ.get("ANN_LOO_COPY_SLIDE8_EXCEL_TO_DOWNLOADS", "").strip().lower() in {"1", "true", "yes"},
        help="Also copy ann_loo_slide8_saturation_bin_bias.xlsx to ~/Downloads.",
    )
    parser.add_argument("--occurrence-threshold", type=float, default=float(os.environ.get("ANN_LOO_OCCURRENCE_THRESHOLD", DEFAULT_OCCURRENCE_THRESHOLD)))
    parser.add_argument("--print-plan", action="store_true")
    return parser


def is_jupyter_kernel_arg(arg: str) -> bool:
    return arg in {"-f", "--f"} or arg.startswith("-f=") or arg.startswith("--f=")


def parse_args_notebook_safe(parser: argparse.ArgumentParser) -> argparse.Namespace:
    """Parse CLI args while tolerating Jupyter's injected kernel-file arg.

    Running this helper from a notebook can add an argument such as
    ``--f=C:\\...\\kernel-*.json`` to ``sys.argv``. That argument belongs to
    ipykernel, not this runner. We ignore only that Jupyter argument and still
    fail on real unknown runner flags so typos do not pass silently.
    """
    args, unknown = parser.parse_known_args()
    unexpected: list[str] = []
    skip_next = False
    for arg in unknown:
        if skip_next:
            skip_next = False
            continue
        if arg in {"-f", "--f"}:
            skip_next = True
            continue
        if is_jupyter_kernel_arg(arg):
            continue
        unexpected.append(arg)
    if unexpected:
        parser.error("unrecognized arguments: " + " ".join(unexpected))
    return args


def main() -> None:
    parser = build_parser()
    args = parse_args_notebook_safe(parser)

    if args.print_plan:
        print_plan(args)
        if not args.model_matrix_csv:
            return

    model_matrix_path = Path(args.model_matrix_csv) if args.model_matrix_csv else None
    model_matrix_df: pd.DataFrame | None = None
    model_matrix_source = ""
    if model_matrix_path is None:
        model_matrix_df, model_matrix_source = find_notebook_model_matrix(
            target_col=args.target_column,
            wlc_name=args.wlc,
            min_feature_count=args.min_feature_count,
            compute_derived=not args.no_compute_derived,
        )
        if model_matrix_df is None:
            raise SystemExit(
                "Provide --model-matrix-csv, set ANN_LOO_MODEL_MATRIX, or run this after the V26 "
                "notebook cell that defines a usable `features_df` dataframe. If using %run, use "
                "`%run -i ./run_ann_loo_scatter_plots.py --copy-slide8-excel-to-downloads`."
            )
        print(f"Using {model_matrix_source} as the ANN LOO model matrix.")

    cfg = AnnConfig(
        wlc_name=args.wlc,
        hidden_layer_sizes=parse_hidden_layers(args.hidden_layers),
        activation=args.activation,
        solver=args.solver,
        learning_rate_init=args.learning_rate_init,
        alpha=args.alpha,
        batch_size=args.batch_size if args.batch_size == "auto" else int(args.batch_size),
        max_iter=args.max_iter,
        early_stopping=args.early_stopping,
        validation_fraction=args.validation_fraction,
        n_iter_no_change=args.n_iter_no_change,
        seed_base=args.seed_base,
        seed_step=args.seed_step,
        realizations=args.realizations,
        scatter_selection=args.scatter_selection,
    )
    env_open_outlook = os.environ.get("ANN_LOO_OPEN_OUTLOOK_DRAFT", "1").strip().lower() not in {"0", "false", "no"}
    output_dir = Path(args.output_dir) if args.output_dir else runtime_output_dir()
    slide8_excel_copy_dir = Path(args.slide8_excel_copy_dir) if args.slide8_excel_copy_dir else None
    manifest = run_ann_loo(
        model_matrix=model_matrix_path,
        output_dir=output_dir,
        target_col=args.target_column,
        heldout_wells=parse_wells(args.heldout_wells),
        cfg=cfg,
        min_feature_count=args.min_feature_count,
        compute_derived=not args.no_compute_derived,
        save_private_predictions=not args.no_private_predictions,
        occurrence_threshold=args.occurrence_threshold,
        create_email_packet=not args.no_email_packet,
        open_outlook_draft=env_open_outlook and not args.no_open_outlook_draft,
        slide8_excel_copy_dir=slide8_excel_copy_dir,
        copy_slide8_excel_to_downloads=args.copy_slide8_excel_to_downloads,
        model_matrix_df=model_matrix_df,
        model_matrix_source=model_matrix_source,
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
