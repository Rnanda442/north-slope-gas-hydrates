#!/usr/bin/env python3
"""V27 audience Q&A diagnostics for the North Slope gas hydrate workflow.

This GitHub-facing runner contains code only. It expects the private model
matrix and optional V26 output tables at runtime, then writes aggregate review
outputs to ignored `outputs_runtime/`. Do not commit private matrices,
row-level predictions, or populated review packets.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


CODE_VERSION = "V27_qna_diagnostics"
DEFAULT_TARGET = "hydrate_saturation_reference"
DEFAULT_THRESHOLDS = [0.01, 0.03, 0.05, 0.10]

WELL_PATTERNS = {
    "WellA": ["mallik 2l 38", "mallik 2l-38", "2l 38", "2l-38"],
    "WellB": ["mallik 5l 38", "mallik 5l-38", "5l 38", "5l-38"],
    "WellC": ["mount elbert", "mt elbert", "elbert"],
    "WellD": ["ignik sikumi", "iġnik sikumi", "sikumi", "ignik"],
}

QUESTION_TOPICS = [
    ("Q1", "stability_zone", "Can we locate stable hydrate intervals for each ML well?"),
    ("Q2", "caliper_qc", "Can caliper/QC masks be implemented and tested?"),
    ("Q3", "geologic_ambiguity", "Can ambiguity be exposed instead of hidden?"),
    ("Q4", "model_learning", "Which log families carry the prediction?"),
    ("Q5", "leakage_overfit", "Are target leakage and memorization guarded?"),
    ("Q6", "metric_choice", "Do regression/classification metrics answer different questions?"),
    ("Q7", "occurrence_threshold", "How sensitive is occurrence to the saturation cutoff?"),
    ("Q8", "saturation_vs_occurrence", "Why can saturation transfer while occurrence fails?"),
    ("Q9", "well_d", "What specifically fails in Well D?"),
    ("Q10", "well_c", "Is Well C a bias case or a failure?"),
    ("Q11", "nmr_boundary", "Is NMR kept on the target/review side?"),
    ("Q12", "proxy_limits", "Where do hydrate proxy signals disagree?"),
    ("Q13", "feature_importance", "Which variables matter most by well?"),
    ("Q14", "new_reservoir_screening", "Can this screen new reservoirs?"),
]

TARGET_LIKE_PATTERNS = [
    "hydrate_saturation",
    "occurrence",
    "nmr",
    "archie",
    "prediction",
    "residual",
    "reference",
]

FEATURE_FAMILIES = {
    "resistivity_fluid": ["rt", "resist"],
    "elastic_stiffness": ["vp", "vs", "impedance", "modulus", "lambda", "mu", "brittleness"],
    "lithology_reservoir": ["gr", "gamma", "sand", "vsh", "shale"],
    "density_porosity": ["rhob", "density", "porosity", "phi"],
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def runtime_output_dir() -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return repo_root() / "outputs_runtime" / "qna_diagnostics_v27" / stamp


def default_public_stability_csv() -> Path:
    return repo_root() / "data" / "public_stability_products" / "stability_screen_2026-06-14_methane_5ppt_v1.csv"


def default_phase_curve_csv() -> Path:
    return repo_root() / "data" / "public_stability_products" / "phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1.csv"


def normalize_name(value: object) -> str:
    text = str(value or "").lower()
    text = text.replace("ġ", "g")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def read_table(path: Path | None) -> pd.DataFrame | None:
    if path is None or not path.exists():
        return None
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if suffix == ".parquet":
        return pd.read_parquet(path)
    raise ValueError(f"Unsupported table type: {path}")


def optional_path(raw: str | None) -> Path | None:
    if not raw:
        return None
    path = Path(raw).expanduser()
    return path if path.exists() else None


def newest_child(path: Path) -> Path | None:
    if not path.exists():
        return None
    children = [p for p in path.iterdir() if p.is_dir()]
    if not children:
        return None
    return max(children, key=lambda p: p.stat().st_mtime)


def find_v26_output_dir(raw: str | None) -> Path | None:
    explicit = optional_path(raw)
    if explicit:
        return explicit
    return newest_child(repo_root() / "outputs_runtime" / "ann_loo_scatter_plots")


def sidecar(v26_dir: Path | None, explicit: str | None, name: str) -> Path | None:
    path = optional_path(explicit)
    if path:
        return path
    if v26_dir:
        candidate = v26_dir / name
        if candidate.exists():
            return candidate
    return None


def first_column(frame: pd.DataFrame, exact: list[str] | None = None, contains: list[str] | None = None) -> str | None:
    exact = exact or []
    contains = contains or []
    lower = {str(c).lower(): c for c in frame.columns}
    for name in exact:
        if name.lower() in lower:
            return lower[name.lower()]
    for col in frame.columns:
        low = str(col).lower()
        if any(term in low for term in contains):
            return str(col)
    return None


def columns_containing(frame: pd.DataFrame, terms: list[str]) -> list[str]:
    out: list[str] = []
    for col in frame.columns:
        low = str(col).lower()
        if any(term in low for term in terms):
            out.append(str(col))
    return out


def row_counts_by_well(matrix: pd.DataFrame) -> pd.DataFrame:
    if "well_alias" not in matrix.columns:
        return pd.DataFrame()
    return matrix.groupby("well_alias", dropna=False).size().reset_index(name="row_count")


def add_well_row_id(frame: pd.DataFrame, well_col: str = "well_alias") -> pd.DataFrame:
    out = frame.copy()
    out["_well_row_id"] = out.groupby(well_col, dropna=False).cumcount()
    return out


def align_predictions(matrix: pd.DataFrame, predictions: pd.DataFrame | None) -> pd.DataFrame | None:
    if predictions is None or predictions.empty:
        return None
    if "well_alias" not in matrix.columns or "well_alias" not in predictions.columns:
        return None

    matrix_keyed = add_well_row_id(matrix)
    pred_keyed = add_well_row_id(predictions)
    keep_cols = ["well_alias", "_well_row_id"]
    for col in matrix.columns:
        if col not in pred_keyed.columns and col not in keep_cols:
            keep_cols.append(col)
    return pred_keyed.merge(matrix_keyed[keep_cols], on=["well_alias", "_well_row_id"], how="left")


def metric_summary(reference: pd.Series, prediction: pd.Series) -> dict[str, float]:
    ref = pd.to_numeric(reference, errors="coerce")
    pred = pd.to_numeric(prediction, errors="coerce")
    mask = ref.notna() & pred.notna()
    if not mask.any():
        return {"n": 0, "bias_pp": np.nan, "mae_pp": np.nan, "rmse_pp": np.nan}
    err = pred[mask] - ref[mask]
    return {
        "n": int(mask.sum()),
        "bias_pp": float(err.mean() * 100.0),
        "mae_pp": float(err.abs().mean() * 100.0),
        "rmse_pp": float(np.sqrt(np.mean(np.square(err))) * 100.0),
    }


def classification_counts(reference: pd.Series, prediction: pd.Series, threshold: float) -> dict[str, float]:
    ref = pd.to_numeric(reference, errors="coerce")
    pred = pd.to_numeric(prediction, errors="coerce")
    mask = ref.notna() & pred.notna()
    if not mask.any():
        return {"n": 0}
    y_true = ref[mask] >= threshold
    y_pred = pred[mask] >= threshold
    tp = int((y_true & y_pred).sum())
    tn = int((~y_true & ~y_pred).sum())
    fp = int((~y_true & y_pred).sum())
    fn = int((y_true & ~y_pred).sum())
    recall = tp / (tp + fn) if (tp + fn) else np.nan
    specificity = tn / (tn + fp) if (tn + fp) else np.nan
    precision = tp / (tp + fp) if (tp + fp) else np.nan
    balanced_accuracy = np.nanmean([recall, specificity])
    return {
        "n": int(mask.sum()),
        "threshold": threshold,
        "true_positive": tp,
        "false_positive": fp,
        "false_negative": fn,
        "true_negative": tn,
        "balanced_accuracy": float(balanced_accuracy),
        "precision": float(precision) if not np.isnan(precision) else np.nan,
        "recall": float(recall) if not np.isnan(recall) else np.nan,
        "specificity": float(specificity) if not np.isnan(specificity) else np.nan,
        "reference_positive_rate": float(y_true.mean()),
        "predicted_positive_rate": float(y_pred.mean()),
    }


def write_column_inventory(matrix: pd.DataFrame, output_dir: Path) -> Path:
    rows = []
    for col in matrix.columns:
        low = str(col).lower()
        rows.append(
            {
                "column": col,
                "role_hint": role_hint(low),
                "non_null": int(matrix[col].notna().sum()),
                "dtype": str(matrix[col].dtype),
                "example": next((str(v) for v in matrix[col].dropna().head(1)), ""),
            }
        )
    out = output_dir / "qna_v27_column_inventory.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    return out


def role_hint(low: str) -> str:
    if any(term in low for term in TARGET_LIKE_PATTERNS):
        return "target_or_answer_side"
    if "qc" in low or "caliper" in low or low in {"cali", "cali_in"}:
        return "qc_or_borehole_quality"
    if any(term in low for term in ["stability", "stable", "temperature", "pressure", "permafrost"]):
        return "stability_context"
    if any(term in low for term in ["depth", "tvd", "md"]):
        return "depth_context"
    if any(term in low for terms in FEATURE_FAMILIES.values() for term in terms):
        return "candidate_log_feature"
    return "metadata_or_other"


def public_stability_matches(matrix: pd.DataFrame, stability: pd.DataFrame | None) -> pd.DataFrame:
    rows = []
    if stability is None or stability.empty or "well_name" not in stability.columns:
        for well in sorted(matrix.get("well_alias", pd.Series(dtype=str)).dropna().unique()):
            rows.append({"well_alias": well, "public_stability_match_status": "no_public_stability_table"})
        return pd.DataFrame(rows)

    stability = stability.copy()
    stability["_norm_well_name"] = stability["well_name"].map(normalize_name)
    for well in sorted(matrix["well_alias"].dropna().unique()):
        patterns = [normalize_name(p) for p in WELL_PATTERNS.get(str(well), [str(well)])]
        mask = pd.Series(False, index=stability.index)
        for pattern in patterns:
            mask = mask | stability["_norm_well_name"].str.contains(pattern, regex=False, na=False)
        matched = stability.loc[mask].copy()
        if matched.empty:
            rows.append(
                {
                    "well_alias": well,
                    "public_stability_match_status": "no_public_match",
                    "public_stability_claim": "No stability interval can be claimed from the public screen for this ML well.",
                }
            )
            continue
        for _, row in matched.head(5).iterrows():
            rows.append(
                {
                    "well_alias": well,
                    "public_stability_match_status": "matched_public_screen",
                    "public_well_name": row.get("well_name", ""),
                    "stability_result_status": row.get("stability_result_status", ""),
                    "reaches_stability_zone": row.get("reaches_stability_zone", ""),
                    "stability_top_m": row.get("stability_top_m", np.nan),
                    "stability_base_m": row.get("stability_base_m", np.nan),
                    "stability_thickness_m": row.get("stability_thickness_m", np.nan),
                    "stability_confidence": row.get("stability_confidence", ""),
                    "caveat_codes": row.get("caveat_codes", ""),
                    "public_stability_claim": "Context only unless stable interval top/base are populated and depth-aligned.",
                }
            )
    return pd.DataFrame(rows)


def phase_curve_stability(matrix: pd.DataFrame, phase_curve: pd.DataFrame | None) -> pd.Series | None:
    pressure_col = first_column(
        matrix,
        exact=["pressure_mpa_absolute", "pressure_at_tvd_mpa_absolute", "pressure_mpa"],
        contains=["pressure"],
    )
    temp_col = first_column(
        matrix,
        exact=["temperature_c", "temperature_at_depth_basis_c", "temp_c"],
        contains=["temperature"],
    )
    if pressure_col is None or temp_col is None or phase_curve is None or phase_curve.empty:
        return None
    if not {"pressure_mpa_absolute", "equilibrium_temperature_c"}.issubset(phase_curve.columns):
        return None
    curve = phase_curve.dropna(subset=["pressure_mpa_absolute", "equilibrium_temperature_c"]).sort_values("pressure_mpa_absolute")
    if curve.empty:
        return None
    pressure = pd.to_numeric(matrix[pressure_col], errors="coerce")
    temp = pd.to_numeric(matrix[temp_col], errors="coerce")
    pmin = curve["pressure_mpa_absolute"].min()
    pmax = curve["pressure_mpa_absolute"].max()
    inside_range = pressure.between(pmin, pmax)
    eq_temp = pd.Series(np.nan, index=matrix.index, dtype=float)
    eq_temp.loc[inside_range] = np.interp(
        pressure.loc[inside_range],
        curve["pressure_mpa_absolute"],
        curve["equilibrium_temperature_c"],
    )
    return temp <= eq_temp


def write_stability_overlay(
    matrix: pd.DataFrame,
    aligned: pd.DataFrame | None,
    stability: pd.DataFrame | None,
    phase_curve: pd.DataFrame | None,
    output_dir: Path,
) -> Path:
    rows = []
    depth_col = first_column(matrix, exact=["depth_m", "tvd_m"], contains=["depth_m", "tvd_m"])
    top_col = first_column(matrix, exact=["stability_top_m"], contains=["stability_top"])
    base_col = first_column(matrix, exact=["stability_base_m"], contains=["stability_base"])
    direct_flag_col = first_column(matrix, exact=["inside_stability_zone", "reaches_stability_zone"], contains=["stable_zone"])

    work = matrix.copy()
    flag_source = "not_available_in_matrix"
    if depth_col and top_col and base_col:
        depth = pd.to_numeric(work[depth_col], errors="coerce")
        top = pd.to_numeric(work[top_col], errors="coerce")
        base = pd.to_numeric(work[base_col], errors="coerce")
        work["_inside_stability_zone"] = depth.between(top, base)
        flag_source = "depth_between_stability_top_base"
    elif direct_flag_col:
        work["_inside_stability_zone"] = work[direct_flag_col].astype(str).str.lower().isin(["true", "1", "yes", "inside", "stable"])
        flag_source = f"direct_flag:{direct_flag_col}"
    else:
        phase_flag = phase_curve_stability(work, phase_curve)
        if phase_flag is not None:
            work["_inside_stability_zone"] = phase_flag
            flag_source = "pressure_temperature_phase_curve"

    if "_inside_stability_zone" in work.columns:
        for (well, inside), group in work.groupby(["well_alias", "_inside_stability_zone"], dropna=False):
            row = {
                "well_alias": well,
                "flag_source": flag_source,
                "inside_stability_zone": inside,
                "row_count": int(len(group)),
                "mean_reference_saturation_pp": float(pd.to_numeric(group.get(DEFAULT_TARGET), errors="coerce").mean() * 100.0)
                if DEFAULT_TARGET in group.columns
                else np.nan,
            }
            if aligned is not None and "_well_row_id" in aligned.columns:
                keyed = add_well_row_id(work)
                subset_keys = keyed.loc[group.index, ["well_alias", "_well_row_id"]]
                merged = subset_keys.merge(aligned, on=["well_alias", "_well_row_id"], how="left")
                if {"hydrate_saturation_reference", "prediction"}.issubset(merged.columns):
                    row.update(metric_summary(merged["hydrate_saturation_reference"], merged["prediction"]))
            rows.append(row)
    else:
        for well, group in matrix.groupby("well_alias", dropna=False):
            rows.append(
                {
                    "well_alias": well,
                    "flag_source": flag_source,
                    "inside_stability_zone": np.nan,
                    "row_count": int(len(group)),
                    "status": "No interval stability columns or pressure-temperature pair found in model matrix.",
                }
            )

    public_matches = public_stability_matches(matrix, stability)
    out = pd.DataFrame(rows).merge(public_matches, on="well_alias", how="left")
    path = output_dir / "qna_v27_stability_overlay_by_well.csv"
    out.to_csv(path, index=False)
    return path


def write_qc_metrics(matrix: pd.DataFrame, aligned: pd.DataFrame | None, output_dir: Path) -> Path:
    rows = []
    qc_cols = columns_containing(matrix, ["qc", "caliper_status", "borehole_quality"])

    caliper_col = first_column(matrix, exact=["cali", "cali_in", "caliper", "caliper_in"], contains=["caliper", "cali"])
    bit_col = first_column(matrix, exact=["bit_size_in", "hole_size_in", "bs_in"], contains=["bit_size", "hole_size"])
    if caliper_col and caliper_col not in qc_cols:
        work = matrix.copy()
        cali = pd.to_numeric(work[caliper_col], errors="coerce")
        work["_caliper_physical_range_status"] = np.where(cali.between(4.0, 30.0), "physical_range_pass", "physical_range_review")
        qc_cols.append("_caliper_physical_range_status")
        if bit_col:
            bit = pd.to_numeric(work[bit_col], errors="coerce")
            work["_caliper_delta_status"] = np.where((cali - bit).abs() <= 1.5, "caliper_delta_pass", "caliper_delta_review")
            qc_cols.append("_caliper_delta_status")
    else:
        work = matrix.copy()

    if not qc_cols:
        for well, group in matrix.groupby("well_alias", dropna=False):
            rows.append({"well_alias": well, "qc_field": "none_found", "qc_value": "not_available", "row_count": int(len(group))})
    else:
        joined = aligned
        if joined is not None:
            matrix_keyed = add_well_row_id(work)
            add_cols = ["well_alias", "_well_row_id"] + [c for c in qc_cols if c in work.columns]
            joined = joined.drop(columns=[c for c in qc_cols if c in joined.columns], errors="ignore")
            joined = joined.merge(matrix_keyed[add_cols], on=["well_alias", "_well_row_id"], how="left")
        for qc_col in qc_cols:
            if qc_col not in work.columns:
                continue
            grouped = work.groupby(["well_alias", qc_col], dropna=False)
            for (well, value), group in grouped:
                row = {"well_alias": well, "qc_field": qc_col, "qc_value": value, "row_count": int(len(group))}
                if joined is not None and {"hydrate_saturation_reference", "prediction", qc_col}.issubset(joined.columns):
                    sub = joined[(joined["well_alias"] == well) & (joined[qc_col].astype(str) == str(value))]
                    row.update(metric_summary(sub["hydrate_saturation_reference"], sub["prediction"]))
                rows.append(row)

    out = output_dir / "qna_v27_qc_mask_metrics.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    return out


def write_occurrence_thresholds(aligned: pd.DataFrame | None, output_dir: Path) -> Path:
    rows = []
    if aligned is None or not {"hydrate_saturation_reference", "prediction", "heldout_well"}.issubset(aligned.columns):
        rows.append({"status": "selected predictions not available; threshold sensitivity not computed"})
    else:
        for well, group in aligned.groupby("heldout_well", dropna=False):
            for threshold in DEFAULT_THRESHOLDS:
                row = {"heldout_well": well}
                row.update(classification_counts(group["hydrate_saturation_reference"], group["prediction"], threshold))
                rows.append(row)
    out = output_dir / "qna_v27_occurrence_threshold_sensitivity.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    return out


def percentile_score(series: pd.Series, high_is_hydrate: bool = True) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    score = numeric.rank(pct=True)
    if not high_is_hydrate:
        score = 1.0 - score
    return score


def write_ambiguity(aligned: pd.DataFrame | None, matrix: pd.DataFrame, output_dir: Path) -> Path:
    work = aligned.copy() if aligned is not None else add_well_row_id(matrix)
    signals = pd.DataFrame(index=work.index)

    if "log10_rt" in work.columns:
        signals["resistivity_fluid"] = percentile_score(work["log10_rt"], True)
    elif "rt_ohm_m" in work.columns:
        signals["resistivity_fluid"] = percentile_score(work["rt_ohm_m"], True)

    elastic_cols = [c for c in ["vp_m_s", "bulk_modulus_gpa", "acoustic_impedance"] if c in work.columns]
    if elastic_cols:
        signals["elastic_stiffness"] = pd.concat([percentile_score(work[c], True) for c in elastic_cols], axis=1).mean(axis=1)

    lith_scores = []
    if "clean_sand_score" in work.columns:
        lith_scores.append(percentile_score(work["clean_sand_score"], True))
    if "vsh_larionov_tertiary" in work.columns:
        lith_scores.append(percentile_score(work["vsh_larionov_tertiary"], False))
    if "gr_api" in work.columns:
        lith_scores.append(percentile_score(work["gr_api"], False))
    if lith_scores:
        signals["lithology_reservoir"] = pd.concat(lith_scores, axis=1).mean(axis=1)

    porosity_scores = []
    for col in ["density_porosity_vv", "neutron_porosity_vv"]:
        if col in work.columns:
            porosity_scores.append(percentile_score(work[col], True))
    if "rhob_g_cc" in work.columns:
        porosity_scores.append(percentile_score(work["rhob_g_cc"], False))
    if porosity_scores:
        signals["density_porosity"] = pd.concat(porosity_scores, axis=1).mean(axis=1)

    if signals.empty:
        out = output_dir / "qna_v27_ambiguity_by_well.csv"
        pd.DataFrame([{"status": "no supported signal columns available"}]).to_csv(out, index=False)
        return out

    work["_signal_family_count"] = signals.notna().sum(axis=1)
    work["_ambiguity_score"] = signals.max(axis=1) - signals.min(axis=1)
    work["_high_ambiguity"] = work["_ambiguity_score"] >= 0.45

    rows = []
    well_col = "heldout_well" if "heldout_well" in work.columns else "well_alias"
    for well, group in work.groupby(well_col, dropna=False):
        row = {
            "well_alias": well,
            "row_count": int(len(group)),
            "mean_ambiguity_score": float(group["_ambiguity_score"].mean()),
            "high_ambiguity_rate": float(group["_high_ambiguity"].mean()),
            "mean_signal_family_count": float(group["_signal_family_count"].mean()),
        }
        if {"hydrate_saturation_reference", "prediction"}.issubset(group.columns):
            row.update(metric_summary(group["hydrate_saturation_reference"], group["prediction"]))
            counts = classification_counts(group["hydrate_saturation_reference"], group["prediction"], 0.05)
            row.update({f"occurrence_{k}": v for k, v in counts.items() if k != "threshold"})
            high = group[group["_high_ambiguity"]]
            low = group[~group["_high_ambiguity"]]
            if not high.empty:
                row["high_ambiguity_rmse_pp"] = metric_summary(high["hydrate_saturation_reference"], high["prediction"])["rmse_pp"]
            if not low.empty:
                row["low_ambiguity_rmse_pp"] = metric_summary(low["hydrate_saturation_reference"], low["prediction"])["rmse_pp"]
        rows.append(row)

    out = output_dir / "qna_v27_ambiguity_by_well.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    return out


def feature_family(feature: object) -> str:
    low = str(feature).lower()
    tokens = set(re.split(r"[^a-z0-9]+", low))
    if any(term in low for term in ["gamma", "sand", "shale"]) or low.startswith("gr_") or low.startswith("vsh"):
        return "lithology_reservoir"
    if low in {"rt_ohm_m", "log10_rt"} or "resist" in low or "resistivity" in tokens:
        return "resistivity_fluid"
    if (
        low.startswith("vp_")
        or low.startswith("vs_")
        or low == "vp_vs_ratio"
        or any(term in low for term in ["impedance", "modulus", "lambda", "mu", "brittleness"])
    ):
        return "elastic_stiffness"
    if any(term in low for term in ["rhob", "density", "porosity"]) or "phi" in tokens:
        return "density_porosity"
    return "other"


def write_feature_family_summary(importance: pd.DataFrame | None, output_dir: Path) -> Path:
    rows = []
    if importance is None or importance.empty or "feature" not in importance.columns:
        rows.append({"status": "permutation importance table not available"})
    else:
        frame = importance.copy()
        frame["feature_family"] = frame["feature"].map(feature_family)
        value_col = first_column(frame, exact=["importance_rmse_pp"], contains=["importance"])
        group_cols = [c for c in ["heldout_well", "feature_family"] if c in frame.columns]
        if value_col and group_cols:
            summary = (
                frame.groupby(group_cols, dropna=False)
                .agg(total_importance_rmse_pp=(value_col, "sum"), top_feature=("feature", lambda s: "; ".join(s.head(3).astype(str))))
                .reset_index()
            )
            rows = summary.to_dict("records")
        else:
            rows.append({"status": "importance table missing expected columns"})
    out = output_dir / "qna_v27_feature_family_summary.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    return out


def write_readiness_summary(paths: dict[str, Path], matrix: pd.DataFrame, output_dir: Path) -> Path:
    inv = pd.read_csv(paths["column_inventory"])
    role_counts = inv["role_hint"].value_counts().to_dict()
    stability_available = role_counts.get("stability_context", 0) > 0
    qc_available = role_counts.get("qc_or_borehole_quality", 0) > 0

    rows = []
    for qid, topic, question in QUESTION_TOPICS:
        if topic == "stability_zone":
            status = "needs_v27_input_or_join" if not stability_available else "testable_from_matrix"
            answer = "V26 has no active interval stability fields unless the private matrix is upgraded."
        elif topic == "caliper_qc":
            status = "testable_from_v26_flags" if qc_available else "needs_caliper_or_qc_columns"
            answer = "Use qc_status/qc_caliper_status now; raw CALI plus bit size would be stronger."
        elif topic in {"occurrence_threshold", "saturation_vs_occurrence", "well_d"}:
            status = "testable_if_predictions_available"
            answer = "Use selected predictions to compare saturation error and occurrence false positives."
        elif topic == "feature_importance":
            status = "testable_if_importance_available"
            answer = "Use permutation importance grouped into resistivity, elastic, lithology, and porosity families."
        else:
            status = "supported_by_existing_workflow"
            answer = "Use whole-well holdouts, leakage guards, and signal-family diagnostics."
        rows.append(
            {
                "question_id": qid,
                "topic": topic,
                "question": question,
                "current_status": status,
                "short_answer_for_qna": answer,
            }
        )

    out = output_dir / "qna_v27_question_readiness_summary.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    return out


def copy_if_present(path: Path | None, dest: Path, copied: list[Path]) -> None:
    if path and path.exists() and path.is_file():
        out = dest / path.name
        shutil.copy2(path, out)
        copied.append(out)


def ps_quote(value: str | Path) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def write_email_packet(output_dir: Path, paths: dict[str, Path], recipient: str, open_draft: bool) -> dict[str, str]:
    packet_dir = output_dir / "qna_v27_email_packet"
    packet_dir.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for key in [
        "readiness_summary",
        "stability_overlay",
        "qc_metrics",
        "threshold_sensitivity",
        "ambiguity",
        "feature_family_summary",
        "column_inventory",
    ]:
        copy_if_present(paths.get(key), packet_dir, copied)

    summary_md = packet_dir / "QNA_V27_EMAIL_PACKET_README.md"
    summary_md.write_text(
        "\n".join(
            [
                "# North Slope Gas Hydrate ML V27 Q&A diagnostics packet",
                "",
                f"Created: {datetime.now().isoformat(timespec='seconds')}",
                f"Code version: {CODE_VERSION}",
                "",
                "## What this packet answers",
                "",
                "- Stability: whether interval stability is already present in the ML matrix, or whether a new stability join/pressure-temperature input is required.",
                "- Caliper/QC: whether existing QC flags or raw caliper fields can support pass/review masks.",
                "- Ambiguity: whether log-family disagreement lines up with prediction error or false positives.",
                "- Occurrence: how sensitive yes/no hydrate calls are to the saturation threshold.",
                "- Feature families: whether each held-out well is driven more by resistivity, elastic, lithology, or porosity signals.",
                "",
                "## Recommended interpretation",
                "",
                "The high-level Q&A can be sent now. Run V27 before resending a stronger DOE-facing update if you want the stability, QC, and ambiguity answers backed by new tables rather than described as next steps.",
                "",
                "## Data boundary",
                "",
                "This packet is aggregate review material. Keep private model matrices, row-level predictions, fitted models, and raw approved log rows out of GitHub.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    copied.append(summary_md)

    audit = packet_dir / "qna_v27_email_packet_audit.csv"
    pd.DataFrame({"file": [p.name for p in copied], "path": [str(p) for p in copied]}).to_csv(audit, index=False)
    copied.append(audit)

    share_zip = packet_dir / f"share_packet_{CODE_VERSION}.zip"
    with zipfile.ZipFile(share_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for item in copied:
            zf.write(item, arcname=item.name)

    attachments = [share_zip, summary_md]
    attachment_array = ", ".join(ps_quote(path) for path in attachments)
    draft = packet_dir / f"open_outlook_draft_{CODE_VERSION}.ps1"
    to_line = ps_quote(recipient) if recipient else "$env:PERSONAL_REVIEW_EMAIL"
    draft.write_text(
        f"""$ErrorActionPreference = "Stop"
$to = {to_line}
$attachments = @({attachment_array})
$outlook = New-Object -ComObject Outlook.Application
$mail = $outlook.CreateItem(0)
if ($to) {{ $mail.To = $to }}
$mail.Subject = "North Slope ML {CODE_VERSION} Q&A diagnostics packet"
$mail.Body = @"
Attached is the V27 Q&A diagnostics packet.

Review folder:
{packet_dir}

Use this after checking the data boundary. The packet is aggregate review material and should not include private row-level data.
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
Write-Host "Review folder: {packet_dir}"
""",
        encoding="utf-8",
    )

    if open_draft:
        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(draft)],
            check=False,
        )

    return {
        "email_packet_dir": str(packet_dir),
        "share_packet_zip": str(share_zip),
        "packet_readme": str(summary_md),
        "outlook_draft_script": str(draft),
    }


def run(args: argparse.Namespace) -> dict[str, object]:
    model_matrix_path = optional_path(args.model_matrix_csv)
    if model_matrix_path is None:
        raise SystemExit("Provide --model-matrix-csv or set QNA_MODEL_MATRIX / ANN_LOO_MODEL_MATRIX.")
    matrix = read_table(model_matrix_path)
    if matrix is None:
        raise SystemExit(f"Could not read model matrix: {model_matrix_path}")
    if "well_alias" not in matrix.columns:
        raise SystemExit("Model matrix must include a well_alias column.")

    output_dir = Path(args.output_dir) if args.output_dir else runtime_output_dir()
    output_dir.mkdir(parents=True, exist_ok=True)

    v26_dir = find_v26_output_dir(args.v26_output_dir)
    predictions = read_table(sidecar(v26_dir, args.predictions_csv, "ann_loo_selected_predictions_private.csv"))
    fold_summary = read_table(sidecar(v26_dir, args.fold_summary_csv, "ann_loo_fold_summary.csv"))
    bin_bias = read_table(sidecar(v26_dir, args.bin_bias_csv, "ann_loo_selected_saturation_bin_bias.csv"))
    importance = read_table(sidecar(v26_dir, args.importance_csv, "ann_permutation_importance.csv"))
    stability = read_table(optional_path(args.stability_csv) or default_public_stability_csv())
    phase_curve = read_table(optional_path(args.phase_curve_csv) or default_phase_curve_csv())
    aligned = align_predictions(matrix, predictions)

    paths: dict[str, Path] = {}
    paths["column_inventory"] = write_column_inventory(matrix, output_dir)
    paths["stability_overlay"] = write_stability_overlay(matrix, aligned, stability, phase_curve, output_dir)
    paths["qc_metrics"] = write_qc_metrics(matrix, aligned, output_dir)
    paths["threshold_sensitivity"] = write_occurrence_thresholds(aligned, output_dir)
    paths["ambiguity"] = write_ambiguity(aligned, matrix, output_dir)
    paths["feature_family_summary"] = write_feature_family_summary(importance, output_dir)
    paths["readiness_summary"] = write_readiness_summary(paths, matrix, output_dir)

    if fold_summary is not None:
        fold_path = output_dir / "qna_v27_v26_fold_summary_copy.csv"
        fold_summary.to_csv(fold_path, index=False)
        paths["fold_summary_copy"] = fold_path
    if bin_bias is not None:
        bias_path = output_dir / "qna_v27_v26_bin_bias_copy.csv"
        bin_bias.to_csv(bias_path, index=False)
        paths["bin_bias_copy"] = bias_path

    email_outputs: dict[str, str] = {}
    if not args.no_email_packet:
        email_outputs = write_email_packet(
            output_dir=output_dir,
            paths=paths,
            recipient=args.recipient_email or os.environ.get("PERSONAL_REVIEW_EMAIL", ""),
            open_draft=args.open_outlook_draft,
        )

    manifest = {
        "code_version": CODE_VERSION,
        "created": datetime.now().isoformat(timespec="seconds"),
        "model_matrix": str(model_matrix_path),
        "v26_output_dir": str(v26_dir) if v26_dir else "",
        "row_counts_by_well": row_counts_by_well(matrix).to_dict("records"),
        "outputs": {key: str(value) for key, value in paths.items()},
        "email_outputs": email_outputs,
        "data_boundary": "Runtime outputs may include aggregate diagnostics from private data. Do not commit populated outputs_runtime folders.",
    }
    manifest_path = output_dir / "qna_v27_run_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    manifest["manifest"] = str(manifest_path)
    return manifest


def print_plan(args: argparse.Namespace) -> None:
    plan = {
        "code_version": CODE_VERSION,
        "purpose": "Create aggregate Q&A diagnostics from the private V26 model matrix and output tables.",
        "required_input": "--model-matrix-csv or QNA_MODEL_MATRIX / ANN_LOO_MODEL_MATRIX",
        "default_output_dir": str(runtime_output_dir()),
        "optional_inputs": {
            "v26_output_dir": "--v26-output-dir or latest outputs_runtime/ann_loo_scatter_plots",
            "stability_csv": str(default_public_stability_csv()),
            "phase_curve_csv": str(default_phase_curve_csv()),
        },
        "outputs": [
            "qna_v27_question_readiness_summary.csv",
            "qna_v27_stability_overlay_by_well.csv",
            "qna_v27_qc_mask_metrics.csv",
            "qna_v27_occurrence_threshold_sensitivity.csv",
            "qna_v27_ambiguity_by_well.csv",
            "qna_v27_feature_family_summary.csv",
            "qna_v27_email_packet/",
        ],
        "email_packet": "Creates a share ZIP and Outlook draft helper; use --open-outlook-draft to display the draft.",
    }
    print(json.dumps(plan, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create V27 aggregate diagnostics for audience Q&A answers.")
    parser.add_argument("--model-matrix-csv", default=os.environ.get("QNA_MODEL_MATRIX") or os.environ.get("ANN_LOO_MODEL_MATRIX", ""))
    parser.add_argument("--v26-output-dir", default=os.environ.get("QNA_V26_OUTPUT_DIR", ""))
    parser.add_argument("--predictions-csv", default=os.environ.get("QNA_PREDICTIONS_CSV", ""))
    parser.add_argument("--fold-summary-csv", default=os.environ.get("QNA_FOLD_SUMMARY_CSV", ""))
    parser.add_argument("--bin-bias-csv", default=os.environ.get("QNA_BIN_BIAS_CSV", ""))
    parser.add_argument("--importance-csv", default=os.environ.get("QNA_IMPORTANCE_CSV", ""))
    parser.add_argument("--stability-csv", default=os.environ.get("QNA_STABILITY_CSV", ""))
    parser.add_argument("--phase-curve-csv", default=os.environ.get("QNA_PHASE_CURVE_CSV", ""))
    parser.add_argument("--output-dir", default=os.environ.get("QNA_OUTPUT_DIR", ""))
    parser.add_argument("--recipient-email", default=os.environ.get("PERSONAL_REVIEW_EMAIL", ""))
    parser.add_argument("--no-email-packet", action="store_true")
    parser.add_argument("--open-outlook-draft", action="store_true")
    parser.add_argument("--print-plan", action="store_true")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.print_plan:
        print_plan(args)
        return
    manifest = run(args)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
