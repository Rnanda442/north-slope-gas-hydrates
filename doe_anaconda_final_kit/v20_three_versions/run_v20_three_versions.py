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


CODE_VERSION = "V20_three_fixed_versions"
DEFAULT_TARGET = "hydrate_saturation_reference"
DEFAULT_TRAIN_WELLS = ["WellC"]
DEFAULT_TRANSFER_WELLS = ["WellA", "WellB", "WellD"]
DEFAULT_OCCURRENCE_THRESHOLD = 0.05
DEFAULT_CLASS_PROBABILITY_THRESHOLD = 0.5
DEFAULT_COMBINED_CORE_WORKBOOK_NAME = "actual_core_data_combined.xlsx"
HYDRATE02_TARGET_SHEET = "12_Candidate_Sh_Targets"

MEASURED_FEATURES = [
    "gr_api",
    "rhob_g_cc",
    "density_porosity_vv",
    "neutron_porosity_vv",
    "rt_ohm_m",
    "vp_m_s",
    "vs_m_s",
    "nmr_porosity_vv",
]

SAFE_TRANSFORM_FEATURES = [
    "log10_rt",
    "clean_sand_score",
]

EQUATION_GEOMECH_FEATURES = [
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
    "phi_density_calc",
    "phi_effective_for_equations",
    "vsh_larionov_tertiary",
    "pressure_hydrostatic_mpa",
]

BLOCKED_FEATURES = {
    "hydrate_saturation_reference",
    "water_saturation_reference",
    "sh_nmr_density_calc",
    "sw_archie_calc",
    "sh_archie_calc",
    "hydrate_occurrence_label",
    "occurrence_probability_screen",
    "well_alias",
    "well_name",
    "site",
    "source_workbook",
    "source_sheet",
    "lat",
    "lon",
}

CORE_PRIOR_FEATURE = "hydrate02_core_prior_sh_from_porosity"
POROSITY_SOURCE_PREFERENCE = [
    "density_porosity_vv",
    "neutron_porosity_vv",
    "nmr_porosity_vv",
    "phi_density_calc",
    "phi_effective_for_equations",
]


def load_sklearn_globals() -> None:
    """Import sklearn lazily so --print-plan works on lightweight runtimes."""
    global SimpleImputer
    global LogisticRegression
    global Ridge
    global accuracy_score
    global balanced_accuracy_score
    global confusion_matrix
    global f1_score
    global mean_absolute_error
    global mean_squared_error
    global precision_score
    global r2_score
    global recall_score
    global roc_auc_score
    global MinMaxScaler

    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression, Ridge
    from sklearn.metrics import (
        accuracy_score,
        balanced_accuracy_score,
        confusion_matrix,
        f1_score,
        mean_absolute_error,
        mean_squared_error,
        precision_score,
        r2_score,
        recall_score,
        roc_auc_score,
    )
    from sklearn.preprocessing import MinMaxScaler


@dataclass(frozen=True)
class VariantSpec:
    variant_id: str
    short_name: str
    feature_policy: str
    primary_feature_weight: float
    safe_transform_weight: float
    equation_geomech_weight: float
    core_prior_weight: float
    interpretation: str


def default_variants() -> list[VariantSpec]:
    return [
        VariantSpec(
            variant_id="V20A",
            short_name="baseline_safe",
            feature_policy="safe_normalized",
            primary_feature_weight=1.0,
            safe_transform_weight=1.0,
            equation_geomech_weight=0.0,
            core_prior_weight=0.0,
            interpretation="Lower-bias V19-style Ridge alpha 10 baseline.",
        ),
        VariantSpec(
            variant_id="V20B",
            short_name="equation_dominance",
            feature_policy="safe_plus_equation",
            primary_feature_weight=0.25,
            safe_transform_weight=0.25,
            equation_geomech_weight=1.0,
            core_prior_weight=0.0,
            interpretation="Reversed-weight stress test: equation/geomechanics dominate primary log inputs.",
        ),
        VariantSpec(
            variant_id="V20C",
            short_name="hydrate02_core_prior",
            feature_policy="safe_plus_hydrate02_core_prior",
            primary_feature_weight=1.0,
            safe_transform_weight=1.0,
            equation_geomech_weight=0.0,
            core_prior_weight=0.25,
            interpretation="Frozen HYDRATE-02 core porosity-to-Sh prior as auxiliary feature only.",
        ),
    ]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_core_candidate_csv() -> Path:
    return (
        repo_root()
        / "data_runtime"
        / "core_calibration"
        / "target_saturation_integration_2026_07_12"
        / "03_candidate_target_tables"
        / "hydrate02_table_s1_candidate_sh_targets_2026-07-12.csv"
    )


def default_core_workbook() -> Path:
    doe_downloads_path = (
        Path.home()
        / "Downloads"
        / "Northslopedatasets06052026"
        / DEFAULT_COMBINED_CORE_WORKBOOK_NAME
    )
    if doe_downloads_path.exists():
        return doe_downloads_path
    return (
        repo_root()
        / "data_runtime"
        / "core_calibration"
        / "target_saturation_integration_2026_07_12"
        / "05_integrated_workbook"
        / DEFAULT_COMBINED_CORE_WORKBOOK_NAME
    )


def runtime_output_dir() -> Path:
    return repo_root() / "outputs_runtime" / "v20_three_versions" / datetime.now().strftime("%Y%m%d_%H%M%S")


def normalize_fraction(values: pd.Series) -> pd.Series:
    out = pd.to_numeric(values, errors="coerce")
    finite = out[np.isfinite(out)]
    if not finite.empty and finite.quantile(0.95) > 1.5:
        out = out / 100.0
    return out.clip(0.0, 1.0)


def first_existing_column(df: pd.DataFrame, names: Iterable[str]) -> str | None:
    for name in names:
        if name in df.columns:
            return name
    return None


def parse_wells(raw: str | None, default: list[str]) -> list[str]:
    if not raw:
        return list(default)
    out = [part.strip() for part in raw.replace(";", ",").split(",") if part.strip()]
    return out or list(default)


def feature_family(feature: str) -> str:
    if feature == CORE_PRIOR_FEATURE:
        return "core_prior"
    if feature in MEASURED_FEATURES:
        return "primary"
    if feature in SAFE_TRANSFORM_FEATURES:
        return "safe_transform"
    if feature in EQUATION_GEOMECH_FEATURES:
        return "equation_geomech"
    return "other"


def feature_weight(feature: str, variant: VariantSpec) -> float:
    family = feature_family(feature)
    if family == "primary":
        return variant.primary_feature_weight
    if family == "safe_transform":
        return variant.safe_transform_weight
    if family == "equation_geomech":
        return variant.equation_geomech_weight
    if family == "core_prior":
        return variant.core_prior_weight
    return 0.0


def candidate_features(df: pd.DataFrame, variant: VariantSpec) -> list[str]:
    features: list[str] = []
    if variant.feature_policy in {"safe_normalized", "safe_plus_equation", "safe_plus_hydrate02_core_prior"}:
        features.extend(MEASURED_FEATURES)
        features.extend(SAFE_TRANSFORM_FEATURES)
    if variant.feature_policy == "safe_plus_equation":
        features.extend(EQUATION_GEOMECH_FEATURES)
    if variant.feature_policy == "safe_plus_hydrate02_core_prior":
        features.append(CORE_PRIOR_FEATURE)
    clean = []
    seen = set()
    for feature in features:
        if feature in seen or feature in BLOCKED_FEATURES or feature not in df.columns:
            continue
        weight = feature_weight(feature, variant)
        if weight <= 0:
            continue
        clean.append(feature)
        seen.add(feature)
    return clean


def load_core_candidate_rows(core_workbook: Path, core_csv: Path) -> tuple[pd.DataFrame | None, dict[str, object]]:
    audit: dict[str, object] = {
        "core_workbook": str(core_workbook),
        "core_csv": str(core_csv),
        "source_kind": "",
        "source_sheet": "",
        "status": "not_used",
        "row_count": 0,
        "positive_sh_rows": 0,
        "r2_train_tiny_core_only": "",
        "slope_on_phi_fraction": "",
        "intercept": "",
    }
    if core_workbook.exists():
        try:
            core = pd.read_excel(core_workbook, sheet_name=HYDRATE02_TARGET_SHEET)
            audit.update(
                {
                    "source_kind": "combined_core_workbook",
                    "source_sheet": HYDRATE02_TARGET_SHEET,
                }
            )
            return core, audit
        except Exception as exc:
            audit["workbook_read_error"] = f"{type(exc).__name__}: {exc}"
    if core_csv.exists():
        core = pd.read_csv(core_csv)
        audit["source_kind"] = "fallback_candidate_csv"
        return core, audit
    audit["status"] = "missing_combined_core_workbook_and_candidate_csv"
    return None, audit


def fit_core_prior(core_workbook: Path, core_csv: Path) -> tuple[Ridge | None, dict[str, object]]:
    core, audit = load_core_candidate_rows(core_workbook, core_csv)
    if core is None:
        return None, audit
    required = {"porosity_phi_iw_pct", "hydrate_saturation_sh_iw_fraction"}
    if not required.issubset(core.columns):
        audit["status"] = "missing_required_core_columns"
        return None, audit
    phi = normalize_fraction(core["porosity_phi_iw_pct"])
    sh = normalize_fraction(core["hydrate_saturation_sh_iw_fraction"])
    mask = phi.notna() & sh.notna()
    if int(mask.sum()) < 4:
        audit["status"] = "too_few_core_rows"
        return None, audit
    model = Ridge(alpha=1.0)
    x = phi[mask].to_numpy().reshape(-1, 1)
    y = sh[mask].to_numpy()
    model.fit(x, y)
    pred = np.clip(model.predict(x), 0.0, 1.0)
    audit.update(
        {
            "status": "fit_from_hydrate02_table_s1",
            "row_count": int(mask.sum()),
            "positive_sh_rows": int((sh[mask] > 0).sum()),
            "r2_train_tiny_core_only": float(r2_score(y, pred)) if len(np.unique(y)) > 1 else "",
            "slope_on_phi_fraction": float(model.coef_[0]),
            "intercept": float(model.intercept_),
            "warning": "Tiny external core prior only; not four-well validation truth.",
        }
    )
    return model, audit


def add_core_prior_feature(df: pd.DataFrame, core_model: Ridge | None) -> pd.DataFrame:
    out = df.copy()
    out[CORE_PRIOR_FEATURE] = np.nan
    if core_model is None:
        return out
    porosity_col = first_existing_column(out, POROSITY_SOURCE_PREFERENCE)
    if porosity_col is None:
        return out
    phi = normalize_fraction(out[porosity_col])
    mask = phi.notna()
    if mask.any():
        out.loc[mask, CORE_PRIOR_FEATURE] = np.clip(core_model.predict(phi[mask].to_numpy().reshape(-1, 1)), 0.0, 1.0)
    return out


def make_design(
    train_df: pd.DataFrame,
    eval_df: pd.DataFrame,
    features: list[str],
    variant: VariantSpec,
) -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    imputer = SimpleImputer(strategy="median")
    scaler = MinMaxScaler()
    x_train_raw = train_df[features].apply(pd.to_numeric, errors="coerce")
    x_eval_raw = eval_df[features].apply(pd.to_numeric, errors="coerce")
    x_train = imputer.fit_transform(x_train_raw)
    x_eval = imputer.transform(x_eval_raw)
    x_train = scaler.fit_transform(x_train)
    x_eval = scaler.transform(x_eval)
    weights = np.array([feature_weight(feature, variant) for feature in features], dtype=float)
    x_train = x_train * weights
    x_eval = x_eval * weights
    meta = {
        "features": features,
        "feature_count": len(features),
        "feature_weights": dict(zip(features, weights.tolist())),
        "dropped_missing_features": [],
    }
    return x_train, x_eval, meta


def saturation_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float | int]:
    return {
        "n": int(len(y_true)),
        "rmse": float(math.sqrt(mean_squared_error(y_true, y_pred))) if len(y_true) else np.nan,
        "mae": float(mean_absolute_error(y_true, y_pred)) if len(y_true) else np.nan,
        "r2": float(r2_score(y_true, y_pred)) if len(y_true) > 1 else np.nan,
        "bias": float(np.mean(y_pred - y_true)) if len(y_true) else np.nan,
    }


def occurrence_metrics(y_label: np.ndarray, score: np.ndarray, probability_threshold: float) -> dict[str, float | int]:
    y_pred = (score >= probability_threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_label, y_pred, labels=[0, 1]).ravel()
    result: dict[str, float | int] = {
        "n": int(len(y_label)),
        "accuracy": float(accuracy_score(y_label, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_label, y_pred)),
        "precision": float(precision_score(y_label, y_pred, zero_division=0)),
        "recall": float(recall_score(y_label, y_pred, zero_division=0)),
        "f1": float(f1_score(y_label, y_pred, zero_division=0)),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }
    if len(np.unique(y_label)) > 1:
        result["roc_auc"] = float(roc_auc_score(y_label, score))
    else:
        result["roc_auc"] = np.nan
    return result


def bin_metrics(df: pd.DataFrame, y_col: str, pred_col: str) -> pd.DataFrame:
    bins = [-0.001, 0.0, 0.01, 0.05, 0.2, 0.5, 1.000001]
    labels = ["zero", "zero_to_0p01", "0p01_to_0p05", "0p05_to_0p2", "0p2_to_0p5", "0p5_to_1"]
    temp = df.copy()
    temp["saturation_bin"] = pd.cut(temp[y_col], bins=bins, labels=labels, include_lowest=True)
    rows = []
    for (well, bin_name), group in temp.groupby(["well_alias", "saturation_bin"], observed=False):
        valid = group[[y_col, pred_col]].dropna()
        if valid.empty:
            continue
        rows.append(
            {
                "well_alias": well,
                "saturation_bin": str(bin_name),
                **saturation_metrics(valid[y_col].to_numpy(), valid[pred_col].to_numpy()),
            }
        )
    return pd.DataFrame(rows)


def load_model_matrix(path: Path, target_col: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Model matrix not found: {path}")
    df = pd.read_csv(path)
    required = {"well_alias", target_col}
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"Model matrix missing required columns: {missing}")
    df = df.copy()
    df[target_col] = normalize_fraction(df[target_col])
    return df[df[target_col].notna()].copy()


def run_variants(
    model_matrix: Path,
    core_workbook: Path,
    core_candidate_csv: Path,
    output_dir: Path,
    target_col: str,
    train_wells: list[str],
    transfer_wells: list[str],
    occurrence_threshold: float,
    class_probability_threshold: float,
    write_predictions: bool,
) -> dict[str, object]:
    load_sklearn_globals()
    output_dir.mkdir(parents=True, exist_ok=True)
    df = load_model_matrix(model_matrix, target_col)
    core_model, core_audit = fit_core_prior(core_workbook, core_candidate_csv)
    df = add_core_prior_feature(df, core_model)

    train_df = df[df["well_alias"].isin(train_wells)].copy()
    transfer_df = df[df["well_alias"].isin(transfer_wells)].copy()
    if train_df.empty:
        raise ValueError(f"No training rows found for train_wells={train_wells}")
    if transfer_df.empty:
        raise ValueError(f"No transfer rows found for transfer_wells={transfer_wells}")

    sat_rows = []
    occ_rows = []
    bin_frames = []
    pred_frames = []
    feature_rows = []

    for variant in default_variants():
        features = candidate_features(df, variant)
        if not features:
            sat_rows.append(
                {
                    "variant_id": variant.variant_id,
                    "short_name": variant.short_name,
                    "scope": "combined_transfer",
                    "status": "skipped_no_features",
                    "n": 0,
                    "rmse": np.nan,
                    "mae": np.nan,
                    "r2": np.nan,
                    "bias": np.nan,
                }
            )
            continue

        x_train, x_transfer, design_meta = make_design(train_df, transfer_df, features, variant)
        y_train = train_df[target_col].to_numpy(dtype=float)
        y_transfer = transfer_df[target_col].to_numpy(dtype=float)
        y_train_occ = (y_train >= occurrence_threshold).astype(int)
        y_transfer_occ = (y_transfer >= occurrence_threshold).astype(int)

        reg = Ridge(alpha=10.0)
        reg.fit(x_train, y_train)
        pred = np.clip(reg.predict(x_transfer), 0.0, 1.0)

        combined = saturation_metrics(y_transfer, pred)
        sat_rows.append(
            {
                "variant_id": variant.variant_id,
                "short_name": variant.short_name,
                "scope": "combined_transfer",
                "status": "ok",
                **combined,
            }
        )
        eval_out = transfer_df[["well_alias", target_col]].copy()
        eval_out["prediction"] = pred
        eval_out["variant_id"] = variant.variant_id
        eval_out["short_name"] = variant.short_name
        for well, group in eval_out.groupby("well_alias"):
            sat_rows.append(
                {
                    "variant_id": variant.variant_id,
                    "short_name": variant.short_name,
                    "scope": f"transfer_well:{well}",
                    "status": "ok",
                    **saturation_metrics(group[target_col].to_numpy(), group["prediction"].to_numpy()),
                }
            )

        bins = bin_metrics(eval_out, target_col, "prediction")
        if not bins.empty:
            bins.insert(0, "short_name", variant.short_name)
            bins.insert(0, "variant_id", variant.variant_id)
            bin_frames.append(bins)

        if len(np.unique(y_train_occ)) > 1:
            cls = LogisticRegression(
                class_weight="balanced",
                max_iter=2000,
                random_state=42,
                solver="liblinear",
            )
            cls.fit(x_train, y_train_occ)
            occ_score = cls.predict_proba(x_transfer)[:, 1]
            eval_out["occurrence_probability"] = occ_score
            occ_combined = occurrence_metrics(y_transfer_occ, occ_score, class_probability_threshold)
            occ_rows.append(
                {
                    "variant_id": variant.variant_id,
                    "short_name": variant.short_name,
                    "scope": "combined_transfer",
                    "label_threshold": occurrence_threshold,
                    "probability_threshold": class_probability_threshold,
                    "status": "ok",
                    **occ_combined,
                }
            )
            for well, group in eval_out.groupby("well_alias"):
                occ_rows.append(
                    {
                        "variant_id": variant.variant_id,
                        "short_name": variant.short_name,
                        "scope": f"transfer_well:{well}",
                        "label_threshold": occurrence_threshold,
                        "probability_threshold": class_probability_threshold,
                        "status": "ok",
                        **occurrence_metrics(
                            (group[target_col].to_numpy() >= occurrence_threshold).astype(int),
                            group["occurrence_probability"].to_numpy(),
                            class_probability_threshold,
                        ),
                    }
                )
        else:
            occ_rows.append(
                {
                    "variant_id": variant.variant_id,
                    "short_name": variant.short_name,
                    "scope": "combined_transfer",
                    "label_threshold": occurrence_threshold,
                    "probability_threshold": class_probability_threshold,
                    "status": "skipped_training_has_one_class",
                    "n": int(len(y_transfer_occ)),
                }
            )

        for feature in features:
            feature_rows.append(
                {
                    "variant_id": variant.variant_id,
                    "short_name": variant.short_name,
                    "feature": feature,
                    "family": feature_family(feature),
                    "weight": design_meta["feature_weights"][feature],
                }
            )
        if write_predictions:
            pred_frames.append(eval_out)

    sat_df = pd.DataFrame(sat_rows)
    occ_df = pd.DataFrame(occ_rows)
    bin_df = pd.concat(bin_frames, ignore_index=True) if bin_frames else pd.DataFrame()
    feature_df = pd.DataFrame(feature_rows)
    core_audit_df = pd.DataFrame([core_audit])

    sat_path = output_dir / "v20_saturation_metrics.csv"
    occ_path = output_dir / "v20_occurrence_metrics.csv"
    bin_path = output_dir / "v20_saturation_bin_metrics.csv"
    feature_path = output_dir / "v20_feature_weights.csv"
    core_path = output_dir / "v20_hydrate02_core_prior_audit.csv"
    sat_df.to_csv(sat_path, index=False)
    occ_df.to_csv(occ_path, index=False)
    bin_df.to_csv(bin_path, index=False)
    feature_df.to_csv(feature_path, index=False)
    core_audit_df.to_csv(core_path, index=False)

    predictions_path = ""
    if write_predictions and pred_frames:
        predictions_path = str(output_dir / "v20_private_transfer_predictions.csv")
        pd.concat(pred_frames, ignore_index=True).to_csv(predictions_path, index=False)

    manifest = {
        "code_version": CODE_VERSION,
        "created": datetime.now().isoformat(timespec="seconds"),
        "model_matrix_csv": str(model_matrix),
        "core_workbook": str(core_workbook),
        "core_candidate_csv_fallback": str(core_candidate_csv),
        "target_column": target_col,
        "train_wells": train_wells,
        "transfer_wells": transfer_wells,
        "occurrence_threshold": occurrence_threshold,
        "class_probability_threshold": class_probability_threshold,
        "variants": [asdict(v) for v in default_variants()],
        "outputs": {
            "saturation_metrics": str(sat_path),
            "occurrence_metrics": str(occ_path),
            "saturation_bin_metrics": str(bin_path),
            "feature_weights": str(feature_path),
            "core_prior_audit": str(core_path),
            "private_predictions": predictions_path,
        },
        "boundary_note": "Outputs are runtime/private by default. Do not commit row-level predictions or approved workbook rows.",
    }
    manifest_path = output_dir / "v20_run_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def print_plan() -> None:
    plan = {
        "code_version": CODE_VERSION,
        "train_wells": DEFAULT_TRAIN_WELLS,
        "transfer_wells": DEFAULT_TRANSFER_WELLS,
        "target_column": DEFAULT_TARGET,
        "occurrence_threshold": DEFAULT_OCCURRENCE_THRESHOLD,
        "class_probability_threshold": DEFAULT_CLASS_PROBABILITY_THRESHOLD,
        "variants": [asdict(v) for v in default_variants()],
        "core_workbook_default": str(default_core_workbook()),
        "core_candidate_csv_fallback": str(default_core_candidate_csv()),
    }
    print(json.dumps(plan, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the three fixed V20 hydrate ML comparison variants.")
    parser.add_argument("--model-matrix-csv", default=os.environ.get("V20_MODEL_MATRIX_CSV", ""))
    parser.add_argument("--core-workbook", default=os.environ.get("V20_CORE_WORKBOOK_XLSX", str(default_core_workbook())))
    parser.add_argument("--core-candidate-csv", default=os.environ.get("V20_CORE_CANDIDATE_CSV", str(default_core_candidate_csv())))
    parser.add_argument("--output-dir", default=os.environ.get("V20_OUTPUT_DIR", ""))
    parser.add_argument("--target-column", default=os.environ.get("V20_TARGET_COLUMN", DEFAULT_TARGET))
    parser.add_argument("--train-wells", default=os.environ.get("V20_TRAIN_WELLS", ",".join(DEFAULT_TRAIN_WELLS)))
    parser.add_argument("--transfer-wells", default=os.environ.get("V20_TRANSFER_WELLS", ",".join(DEFAULT_TRANSFER_WELLS)))
    parser.add_argument("--occurrence-threshold", type=float, default=float(os.environ.get("V20_OCCURRENCE_THRESHOLD", DEFAULT_OCCURRENCE_THRESHOLD)))
    parser.add_argument("--class-probability-threshold", type=float, default=float(os.environ.get("V20_CLASS_PROBABILITY_THRESHOLD", DEFAULT_CLASS_PROBABILITY_THRESHOLD)))
    parser.add_argument("--write-predictions", action="store_true", help="Write row-level transfer predictions to the runtime output folder.")
    parser.add_argument("--print-plan", action="store_true", help="Print the fixed V20 plan and exit without reading private data.")
    args = parser.parse_args()

    if args.print_plan:
        print_plan()
        if not args.model_matrix_csv:
            return

    if not args.model_matrix_csv:
        raise SystemExit("Provide --model-matrix-csv or set V20_MODEL_MATRIX_CSV. Use --print-plan to view the scaffold without private data.")

    output_dir = Path(args.output_dir) if args.output_dir else runtime_output_dir()
    manifest = run_variants(
        model_matrix=Path(args.model_matrix_csv),
        core_workbook=Path(args.core_workbook),
        core_candidate_csv=Path(args.core_candidate_csv),
        output_dir=output_dir,
        target_col=args.target_column,
        train_wells=parse_wells(args.train_wells, DEFAULT_TRAIN_WELLS),
        transfer_wells=parse_wells(args.transfer_wells, DEFAULT_TRANSFER_WELLS),
        occurrence_threshold=args.occurrence_threshold,
        class_probability_threshold=args.class_probability_threshold,
        write_predictions=args.write_predictions,
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
