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


def load_model_matrix(path: Path, target_col: str) -> pd.DataFrame:
    df = read_table(path)
    required = {"well_alias", target_col}
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"model matrix missing required columns: {missing}")
    out = df.copy()
    out[target_col] = normalize_fraction(out[target_col])
    out = out[out[target_col].notna()].copy()
    out["well_alias"] = out["well_alias"].astype(str)
    return out


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


def run_ann_loo(
    model_matrix: Path,
    output_dir: Path,
    target_col: str,
    heldout_wells: list[str],
    cfg: AnnConfig,
    min_feature_count: int,
    compute_derived: bool,
    save_private_predictions: bool,
    occurrence_threshold: float,
) -> dict[str, object]:
    load_ml_globals()
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_dir = output_dir / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)

    df = load_model_matrix(model_matrix, target_col)
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
                "mean_r2_across_realizations": float(fold_metric_df["r2"].mean()),
                "median_r2_across_realizations": float(fold_metric_df["r2"].median()),
                "max_r2_across_realizations": float(fold_metric_df["r2"].max()),
                "reference_prior_r2_mean_if_available": reference.get("r2_mean", ""),
                "reference_prior_rmse_mean_if_available": reference.get("rmse_mean", ""),
                "reference_source": reference.get("source", ""),
                "figure_path": str(figure_path),
            }
        )

    metrics_df = pd.DataFrame(metric_rows)
    selected_df = pd.DataFrame(selected_rows)
    metrics_path = output_dir / "ann_loo_metrics_by_realization.csv"
    selected_path = output_dir / "ann_loo_fold_summary.csv"
    weights_path = output_dir / "ann_loo_wlc_feature_weights.csv"
    metrics_df.to_csv(metrics_path, index=False)
    selected_df.to_csv(selected_path, index=False)
    feature_weights.to_csv(weights_path, index=False)

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
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    manifest = {
        "code_version": CODE_VERSION,
        "created": datetime.now().isoformat(timespec="seconds"),
        "model_matrix": str(model_matrix),
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
            "wlc_feature_weights": str(weights_path),
            "private_selected_predictions": predictions_path,
            "figure_dir": str(figure_dir),
            "contact_sheet": str(contact_sheet_path),
            "readme": str(note),
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
        "heldout_wells": parse_wells(args.heldout_wells),
        "default_wlc": args.wlc,
        "default_wlc_features": WLC_FEATURES[args.wlc],
        "ann_config": asdict(cfg),
        "known_reference_metrics": REFERENCE_FINAL_ANN_METRICS,
        "default_output_dir": str(runtime_output_dir()),
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
    parser.add_argument("--occurrence-threshold", type=float, default=float(os.environ.get("ANN_LOO_OCCURRENCE_THRESHOLD", DEFAULT_OCCURRENCE_THRESHOLD)))
    parser.add_argument("--print-plan", action="store_true")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.print_plan:
        print_plan(args)
        if not args.model_matrix_csv:
            return

    if not args.model_matrix_csv:
        raise SystemExit("Provide --model-matrix-csv or set ANN_LOO_MODEL_MATRIX. Use --print-plan to view the scaffold without private data.")

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
    output_dir = Path(args.output_dir) if args.output_dir else runtime_output_dir()
    manifest = run_ann_loo(
        model_matrix=Path(args.model_matrix_csv),
        output_dir=output_dir,
        target_col=args.target_column,
        heldout_wells=parse_wells(args.heldout_wells),
        cfg=cfg,
        min_feature_count=args.min_feature_count,
        compute_derived=not args.no_compute_derived,
        save_private_predictions=not args.no_private_predictions,
        occurrence_threshold=args.occurrence_threshold,
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
