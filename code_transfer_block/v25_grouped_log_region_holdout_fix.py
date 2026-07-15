# V25 full replacement code block for the failed report-review cell
#
# Copy this whole file into the V25 notebook cell under:
#
#     4. V25 Core-Aware Auxiliary Learning And Final 3-to-1 Report Review
#
# It replaces the entire failed cell, not just the small helper section.
# It keeps the original V25 report-review logic and fixes the grouped-log
# comparison crash caused by duplicate task_type insertion.

# =============================================================================
# ML models - V25 final 3-to-1 transfer workflow
# =============================================================================

# V10 keeps the V9 validation/modeling design and adds explicit source-policy audits:
# 1) train on three active wells by default,
# 2) select model/feature set using only the three-well training pool,
# 3) evaluate on the held-out well as the external transfer well,
# 4) report combined transfer metrics and per-transfer-well metrics,
# 5) keep normalized-input protection and target-leakage blocking.

MEASURED_FEATURES = [
    "gr_api",
    "rhob_g_cc",
    "density_porosity_vv",
    "neutron_porosity_vv",
    "rt_ohm_m",
    "vp_m_s",
    "vs_m_s",
]
SAFE_TRANSFORM_FEATURES = [
    "log10_rt",
    "clean_sand_score",
]
PROXY_EQUATION_FEATURES = [
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
]
CONTEXT_FEATURES = [
    "pressure_hydrostatic_mpa",
]
DENSITY_POROSITY_FAMILY_FEATURES = [
    "density_porosity_vv",
    "phi_density_calc",
    "phi_effective_for_equations",
]

if INCLUDE_NMR_POROSITY_AS_FEATURE:
    MEASURED_FEATURES.append("nmr_porosity_vv")

# Direct target-derived fields and review outputs are deliberately excluded from X_allowed.
BLOCKED_FEATURES = {
    "hydrate_saturation_reference",
    "water_saturation_reference",
    "sh_nmr_density_calc",
    "sw_archie_calc",
    "sh_archie_calc",
    "occurrence_probability_screen",
    "hydrate_occurrence_screen",
    "hydrate_occurrence_label",
    "occurrence_label_status",
    "qc_status",
    "well_alias",
    "well_name",
    "site",
    "source_workbook",
    "source_sheet",
    "source_layout",
    "source_header_contract",
    "source_hydrate_header",
    "source_water_header",
    "phi_effective_source",
    "lat",
    "lon",
}

TARGETED_RIDGE_ALPHAS = [float(x.strip()) for x in os.environ.get("TARGETED_RIDGE_ALPHAS", "10").split(",") if x.strip()]

def ridge_model_name(alpha: float) -> str:
    return "ridge_a" + str(alpha).replace(".", "p").rstrip("0").rstrip("p")

REGRESSION_MODELS = {"mean_baseline": DummyRegressor(strategy="mean")}
for _ridge_alpha in TARGETED_RIDGE_ALPHAS:
    REGRESSION_MODELS[ridge_model_name(_ridge_alpha)] = Ridge(alpha=float(_ridge_alpha), random_state=RANDOM_SEED)
if V25_ENABLE_RESEARCH_MODELS:
    REGRESSION_MODELS.update({
        "gradient_boosting_shallow": GradientBoostingRegressor(n_estimators=90, learning_rate=0.04, max_depth=2, random_state=RANDOM_SEED),
        "gradient_boosting_huber": GradientBoostingRegressor(n_estimators=100, learning_rate=0.04, max_depth=2, loss="huber", random_state=RANDOM_SEED),
    })
if ENABLE_RANDOM_FOREST_REGRESSION:
    REGRESSION_MODELS["random_forest_shallow"] = RandomForestRegressor(n_estimators=80, max_depth=4, min_samples_leaf=5, random_state=RANDOM_SEED, n_jobs=1)

TARGETED_LOGISTIC_C_VALUES = [float(x.strip()) for x in os.environ.get("TARGETED_LOGISTIC_C_VALUES", "1").split(",") if x.strip()]

def logistic_model_name(c_value: float) -> str:
    return "logistic_balanced_c" + str(c_value).replace(".", "p").rstrip("0").rstrip("p")

CLASSIFICATION_MODELS = {"majority_baseline": DummyClassifier(strategy="most_frequent")}
for _logistic_c in TARGETED_LOGISTIC_C_VALUES:
    _name = "logistic_balanced" if abs(float(_logistic_c) - 1.0) < 1e-12 else logistic_model_name(_logistic_c)
    CLASSIFICATION_MODELS[_name] = LogisticRegression(max_iter=3000, C=float(_logistic_c), class_weight="balanced", random_state=RANDOM_SEED)
if V25_ENABLE_RESEARCH_MODELS:
    CLASSIFICATION_MODELS["gradient_boosting_cls"] = GradientBoostingClassifier(n_estimators=90, learning_rate=0.04, max_depth=2, random_state=RANDOM_SEED)
if ENABLE_RANDOM_FOREST_CLASSIFICATION:
    CLASSIFICATION_MODELS["random_forest_cls"] = RandomForestClassifier(n_estimators=90, max_depth=4, min_samples_leaf=4, class_weight="balanced", random_state=RANDOM_SEED, n_jobs=1)


def unique_preserve_order(values: list[str]) -> list[str]:
    out = []
    seen = set()
    for v in values:
        if v not in seen:
            out.append(v)
            seen.add(v)
    return out


def wells_label(wells: list[str] | str) -> str:
    if isinstance(wells, str):
        return wells
    return "+".join(wells)


def candidate_feature_sets() -> dict[str, list[str]]:
    feature_sets = {
        "measured_only": MEASURED_FEATURES,
        "safe_normalized": MEASURED_FEATURES + SAFE_TRANSFORM_FEATURES,
    }
    if EVALUATE_PROXY_FEATURE_SET_FOR_REVIEW:
        proxy_cols = MEASURED_FEATURES + SAFE_TRANSFORM_FEATURES + PROXY_EQUATION_FEATURES
        if ALLOW_PRESSURE_CONTEXT_IN_PRIMARY_MODEL:
            proxy_cols = proxy_cols + CONTEXT_FEATURES
        feature_sets["equation_proxy_review"] = proxy_cols
    if ALLOW_PRESSURE_CONTEXT_IN_PRIMARY_MODEL:
        feature_sets["safe_plus_pressure_context"] = MEASURED_FEATURES + SAFE_TRANSFORM_FEATURES + CONTEXT_FEATURES
    if EVALUATE_WIDE_FEATURE_SET_TRIALS:
        wide_cols = MEASURED_FEATURES + SAFE_TRANSFORM_FEATURES + PROXY_EQUATION_FEATURES
        if ALLOW_PRESSURE_CONTEXT_IN_PRIMARY_MODEL:
            wide_cols = wide_cols + CONTEXT_FEATURES
        feature_sets["all_allowed_inputs_review"] = wide_cols
        feature_sets["all_allowed_except_density_porosity_review"] = [c for c in wide_cols if c not in DENSITY_POROSITY_FAMILY_FEATURES]
    return {k: unique_preserve_order(v) for k, v in feature_sets.items()}


PRIMARY_ALLOWED_FEATURE_SETS = {"measured_only", "safe_normalized"}
if ALLOW_PROXY_EQUATION_FEATURES_IN_PRIMARY_MODEL:
    PRIMARY_ALLOWED_FEATURE_SETS.add("equation_proxy_review")
if ALLOW_PRESSURE_CONTEXT_IN_PRIMARY_MODEL:
    PRIMARY_ALLOWED_FEATURE_SETS.add("safe_plus_pressure_context")
if EVALUATE_WIDE_FEATURE_SET_TRIALS and WIDE_FEATURE_SET_SELECTION_ELIGIBLE and ALLOW_PROXY_EQUATION_FEATURES_IN_PRIMARY_MODEL:
    PRIMARY_ALLOWED_FEATURE_SETS.update({"all_allowed_inputs_review", "all_allowed_except_density_porosity_review"})


def available_feature_sets(train_df: pd.DataFrame) -> tuple[dict[str, list[str]], pd.DataFrame]:
    rows = []
    out: dict[str, list[str]] = {}
    for set_name, cols in candidate_feature_sets().items():
        candidates = [c for c in cols if c in train_df.columns and c not in BLOCKED_FEATURES]
        if not candidates:
            out[set_name] = []
            rows.append({"feature_set": set_name, "feature": "none", "coverage": np.nan, "selected": False, "primary_eligible": set_name in PRIMARY_ALLOWED_FEATURE_SETS})
            continue
        coverage = train_df[candidates].notna().mean().sort_values(ascending=False)
        selected = coverage[coverage >= MIN_TRAIN_FEATURE_COVERAGE].index.tolist()
        out[set_name] = selected
        for feature, cov in coverage.items():
            rows.append({
                "feature_set": set_name,
                "feature": feature,
                "coverage": float(cov),
                "selected": feature in selected,
                "primary_eligible": set_name in PRIMARY_ALLOWED_FEATURE_SETS,
                "normalized_input_mode": NORMALIZED_INPUT_MODE,
            })
    return out, pd.DataFrame(rows)


def row_completeness_mask(df: pd.DataFrame, feature_cols: list[str]) -> pd.Series:
    if not feature_cols:
        return pd.Series(False, index=df.index)
    return df[feature_cols].notna().mean(axis=1) >= MIN_ROW_FEATURE_FRACTION


def target_rows(df: pd.DataFrame, target_col: str, wells: list[str], feature_cols: list[str] | None = None) -> pd.DataFrame:
    sub = df[df["well_alias"].isin(wells)].copy()
    sub = sub[sub[target_col].notna()].copy()
    if feature_cols:
        sub = sub[row_completeness_mask(sub, feature_cols)].copy()
    return sub


def equal_well_weights(df: pd.DataFrame) -> np.ndarray:
    counts = df["well_alias"].value_counts().to_dict()
    w = df["well_alias"].map(lambda x: 1.0 / max(counts.get(x, 1), 1)).astype(float).to_numpy()
    return w / np.nanmean(w)


def regression_sample_weights(df: pd.DataFrame, target_col: str) -> np.ndarray:
    w = equal_well_weights(df)
    if APPLY_TARGET_BIN_WEIGHTS and target_col in df.columns:
        y = pd.to_numeric(df[target_col], errors="coerce").clip(0, 1)
        bins = pd.cut(y, bins=SATURATION_BIN_EDGES, labels=False, include_lowest=True)
        counts = bins.value_counts(dropna=True).to_dict()
        used_bins = max(len(counts), 1)
        bweights = bins.map(lambda b: len(y) / (used_bins * counts.get(b, 1)) if pd.notna(b) else 1.0).astype(float).to_numpy()
        bweights = np.clip(bweights, 0.35, 4.0)
        w = w * bweights
    return w / np.nanmean(w)


def classification_sample_weights(df: pd.DataFrame, target_col: str) -> np.ndarray:
    w = equal_well_weights(df)
    y = df[target_col].astype(int)
    counts = y.value_counts().to_dict()
    class_w = y.map(lambda c: len(y) / (2.0 * max(counts.get(c, 1), 1))).astype(float).to_numpy()
    w = w * class_w
    return w / np.nanmean(w)


def fit_pipeline(model, X, y, sample_weight=None) -> Pipeline:
    pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", MinMaxScaler()),
        ("model", clone(model)),
    ])
    if sample_weight is not None:
        try:
            pipe.fit(X, y, model__sample_weight=sample_weight)
        except Exception:
            pipe.fit(X, y)
    else:
        pipe.fit(X, y)
    return pipe


def metric_dict(y_true, y_pred) -> dict[str, float]:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return {
        "n": int(np.isfinite(y_true).sum()),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(math.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)) if len(y_true) > 1 else np.nan,
        "bias": float(np.nanmean(y_pred - y_true)),
        "prediction_min": float(np.nanmin(y_pred)),
        "prediction_max": float(np.nanmax(y_pred)),
    }


def classifier_probability(pipe: Pipeline, X: pd.DataFrame) -> np.ndarray:
    model = pipe.named_steps["model"]
    if hasattr(pipe, "predict_proba"):
        proba = pipe.predict_proba(X)
        classes = list(getattr(model, "classes_", []))
        if 1 in classes:
            return proba[:, classes.index(1)]
        return proba[:, -1]
    pred = pipe.predict(X)
    return np.asarray(pred, dtype=float)


def classification_metric_dict(y_true, proba, pred_label) -> dict[str, float]:
    y_true = np.asarray(y_true, dtype=int)
    proba = np.asarray(proba, dtype=float)
    pred_label = np.asarray(pred_label, dtype=int)
    out = {
        "n": int(len(y_true)),
        "accuracy": float(accuracy_score(y_true, pred_label)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, pred_label)),
        "precision": float(precision_score(y_true, pred_label, zero_division=0)),
        "recall": float(recall_score(y_true, pred_label, zero_division=0)),
        "f1": float(f1_score(y_true, pred_label, zero_division=0)),
        "brier": float(brier_score_loss(y_true, np.clip(proba, 0, 1))) if len(np.unique(y_true)) == 2 else np.nan,
        "positive_rate_reference": float(np.mean(y_true == 1)),
        "positive_rate_predicted": float(np.mean(pred_label == 1)),
        "probability_min": float(np.nanmin(proba)),
        "probability_max": float(np.nanmax(proba)),
    }
    out["roc_auc"] = float(roc_auc_score(y_true, proba)) if len(np.unique(y_true)) == 2 else np.nan
    return out


def make_depth_block_groups(train: pd.DataFrame, n_splits: int = DEPTH_BLOCK_CV_N_SPLITS) -> tuple[np.ndarray, str, int]:
    """Create CV groups without using external transfer wells.

    If multiple wells are in the train set, use well groups. If one well is in the
    train set, split the training well into contiguous depth blocks.
    """
    well_groups = train["well_alias"].astype(str).to_numpy()
    unique_wells = np.unique(well_groups)
    if len(unique_wells) >= 2:
        return well_groups, "well_group_cv_inside_train", len(unique_wells)

    depth = pd.to_numeric(train.get("depth_m"), errors="coerce")
    if depth.notna().sum() < 20:
        # Fallback to row-order blocks if depth is missing, still using only training rows.
        order = pd.Series(np.arange(len(train)), index=train.index)
    else:
        order = depth.rank(method="first")
    q = min(int(n_splits), max(2, len(train) // 40))
    q = max(2, q)
    try:
        groups = pd.qcut(order, q=q, labels=False, duplicates="drop")
    except Exception:
        groups = pd.Series(np.arange(len(train)) % q, index=train.index)
    groups = pd.Series(groups, index=train.index).astype("Int64").fillna(0).astype(int).to_numpy()
    n_groups = len(np.unique(groups))
    return groups, "single_train_well_depth_block_cv", n_groups


def saturation_detection_metric_dict(y_true, y_pred, threshold: float = OCCURRENCE_POSITIVE_SH_THRESHOLD) -> dict[str, float]:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    mask = np.isfinite(y_true) & np.isfinite(y_pred)
    y_true = y_true[mask]
    y_pred = y_pred[mask]
    if len(y_true) == 0:
        return {
            "saturation_detection_threshold": float(threshold),
            "saturation_detection_n": 0,
            "saturation_precision": np.nan,
            "saturation_recall": np.nan,
            "saturation_f1": np.nan,
            "saturation_accuracy": np.nan,
            "saturation_true_positive": 0,
            "saturation_false_positive": 0,
            "saturation_false_negative": 0,
            "saturation_true_negative": 0,
            "saturation_positive_rate_reference": np.nan,
            "saturation_positive_rate_predicted": np.nan,
        }
    true_label = (y_true >= threshold).astype(int)
    pred_label = (y_pred >= threshold).astype(int)
    tp = int(((true_label == 1) & (pred_label == 1)).sum())
    fp = int(((true_label == 0) & (pred_label == 1)).sum())
    fn = int(((true_label == 1) & (pred_label == 0)).sum())
    tn = int(((true_label == 0) & (pred_label == 0)).sum())
    return {
        "saturation_detection_threshold": float(threshold),
        "saturation_detection_n": int(len(y_true)),
        "saturation_precision": float(precision_score(true_label, pred_label, zero_division=0)),
        "saturation_recall": float(recall_score(true_label, pred_label, zero_division=0)),
        "saturation_f1": float(f1_score(true_label, pred_label, zero_division=0)),
        "saturation_accuracy": float(accuracy_score(true_label, pred_label)),
        "saturation_true_positive": tp,
        "saturation_false_positive": fp,
        "saturation_false_negative": fn,
        "saturation_true_negative": tn,
        "saturation_positive_rate_reference": float(np.mean(true_label == 1)),
        "saturation_positive_rate_predicted": float(np.mean(pred_label == 1)),
    }


def saturation_bin_metrics(pred_df: pd.DataFrame, target: str, model: str, feature_set: str, validation_scope: str = "combined_transfer") -> pd.DataFrame:
    if pred_df.empty:
        return pd.DataFrame()
    tmp = pred_df.copy()
    tmp["reference_bin"] = pd.cut(tmp["reference"].clip(0, 1), bins=SATURATION_BIN_EDGES, labels=SATURATION_BIN_LABELS, include_lowest=True)
    rows = []
    for bin_name, sub in tmp.groupby("reference_bin", dropna=False):
        if len(sub) == 0:
            continue
        m = metric_dict(sub["reference"], sub["prediction"])
        m.update({
            "target": target,
            "model": model,
            "feature_set": feature_set,
            "validation_scope": validation_scope,
            "reference_bin": str(bin_name),
            "reference_mean": float(sub["reference"].mean()),
            "prediction_mean": float(sub["prediction"].mean()),
        })
        rows.append(m)
    tmp2 = tmp[tmp["reference"].notna() & tmp["prediction"].notna()].copy()
    if len(tmp2):
        for threshold in SATURATION_DETECTION_THRESHOLDS:
            detect = saturation_detection_metric_dict(tmp2["reference"], tmp2["prediction"], threshold=threshold)
            rows.append({
                "target": target,
                "model": model,
                "feature_set": feature_set,
                "validation_scope": validation_scope,
                "reference_bin": f"threshold_Sh_ge_{threshold:.2f}",
                "n": int(len(tmp2)),
                "mae": np.nan,
                "rmse": np.nan,
                "r2": np.nan,
                "bias": np.nan,
                "prediction_min": np.nan,
                "prediction_max": np.nan,
                "reference_mean": detect["saturation_positive_rate_reference"],
                "prediction_mean": detect["saturation_positive_rate_predicted"],
                "occurrence_accuracy_from_regression": detect["saturation_accuracy"],
                "occurrence_precision_from_regression": detect["saturation_precision"],
                "occurrence_recall_from_regression": detect["saturation_recall"],
                "occurrence_f1_from_regression": detect["saturation_f1"],
                "true_positive": detect["saturation_true_positive"],
                "false_positive": detect["saturation_false_positive"],
                "false_negative": detect["saturation_false_negative"],
                "true_negative": detect["saturation_true_negative"],
                "saturation_detection_threshold": detect["saturation_detection_threshold"],
            })
    return pd.DataFrame(rows)


def evaluate_regression_model(pipe: Pipeline, valid: pd.DataFrame, features: list[str], target_col: str) -> tuple[dict[str, float], pd.DataFrame]:
    X_valid = valid[features]
    y_valid = valid[target_col].astype(float)
    pred_raw = pipe.predict(X_valid)
    pred = np.clip(pred_raw, 0.0, 1.0)
    m = metric_dict(y_valid, pred)
    tmp_cols = [
        "well_alias", "well_name", "site", "depth_m", "depth_ft", target_col,
        "hydrate_occurrence_screen", "occurrence_probability_screen", "hydrate_occurrence_label",
        "occurrence_label_status", "qc_status", "sh_nmr_density_calc", "sh_archie_calc",
        "sw_archie_calc", "rw_est_ohm_m",
    ]
    tmp_cols = [c for c in tmp_cols if c in valid.columns]
    pred_df = valid[tmp_cols].copy().rename(columns={target_col: "reference"})
    pred_df["prediction"] = pred
    pred_df["prediction_raw"] = pred_raw
    pred_df["residual"] = pred_df["prediction"] - pred_df["reference"]
    return m, pred_df


def per_well_regression_metrics(pred_df: pd.DataFrame, base: dict[str, Any]) -> pd.DataFrame:
    rows = []
    if pred_df.empty:
        return pd.DataFrame(rows)
    for well, sub in pred_df.groupby("well_alias", dropna=False):
        if len(sub) < 2:
            continue
        m = metric_dict(sub["reference"], sub["prediction"])
        row = dict(base)
        row.update(m)
        if base.get("target") == "hydrate_saturation":
            row.update(saturation_detection_metric_dict(sub["reference"], sub["prediction"], threshold=OCCURRENCE_POSITIVE_SH_THRESHOLD))
        row["validation_scope"] = "per_transfer_well"
        row["validation_well"] = well
        row["validation_rows"] = len(sub)
        rows.append(row)
    return pd.DataFrame(rows)


def group_cv_regression(df: pd.DataFrame, target_name: str, target_col: str, train_wells: list[str]) -> tuple[pd.DataFrame, dict[str, list[str]], pd.DataFrame]:
    train0 = df[df["well_alias"].isin(train_wells) & df[target_col].notna()].copy()
    feature_sets, feature_catalog = available_feature_sets(train0)
    rows = []
    for feature_set_name, features in feature_sets.items():
        if not features:
            continue
        train = target_rows(df, target_col, train_wells, features)
        groups, cv_mode, n_groups = make_depth_block_groups(train)
        for model_name, model in REGRESSION_MODELS.items():
            fold_rows = []
            if len(train) < 20 or n_groups < 2:
                rows.append({
                    "target": target_name,
                    "task_type": "regression",
                    "feature_set": feature_set_name,
                    "model": model_name,
                    "cv_status": "not_enough_groups_or_rows",
                    "cv_mode": cv_mode,
                    "cv_folds": 0,
                    "cv_rmse_mean": np.nan,
                    "cv_mae_mean": np.nan,
                    "cv_r2_mean": np.nan,
                    "primary_eligible": feature_set_name in PRIMARY_ALLOWED_FEATURE_SETS,
                })
                continue
            cv = GroupKFold(n_splits=n_groups)
            for fold_i, (tr_idx, va_idx) in enumerate(cv.split(train[features], train[target_col], groups=groups), start=1):
                tr = train.iloc[tr_idx].copy()
                va = train.iloc[va_idx].copy()
                if len(tr) < 10 or len(va) < 5:
                    continue
                weights = regression_sample_weights(tr, target_col)
                try:
                    pipe = fit_pipeline(model, tr[features], tr[target_col].astype(float), sample_weight=weights)
                    m, _ = evaluate_regression_model(pipe, va, features, target_col)
                    m.update({"fold": fold_i, "heldout_train_block": str(np.unique(groups[va_idx]).tolist()), "cv_mode": cv_mode})
                    fold_rows.append(m)
                except Exception as exc:
                    fold_rows.append({"fold": fold_i, "rmse": np.nan, "mae": np.nan, "r2": np.nan, "cv_mode": cv_mode, "note": str(exc)})
            fold_df = pd.DataFrame(fold_rows)
            rows.append({
                "target": target_name,
                "task_type": "regression",
                "feature_set": feature_set_name,
                "model": model_name,
                "cv_status": "ok" if fold_df.get("rmse", pd.Series(dtype=float)).notna().any() else "failed",
                "cv_mode": cv_mode,
                "cv_folds": int(fold_df.get("rmse", pd.Series(dtype=float)).notna().sum()),
                "cv_rmse_mean": float(fold_df["rmse"].mean()) if "rmse" in fold_df else np.nan,
                "cv_rmse_std": float(fold_df["rmse"].std()) if "rmse" in fold_df else np.nan,
                "cv_mae_mean": float(fold_df["mae"].mean()) if "mae" in fold_df else np.nan,
                "cv_r2_mean": float(fold_df["r2"].mean()) if "r2" in fold_df else np.nan,
                "primary_eligible": feature_set_name in PRIMARY_ALLOWED_FEATURE_SETS,
                "feature_count": len(features),
                "train_rows_cv_pool": len(train),
                "train_wells": wells_label(train_wells),
            })
    return pd.DataFrame(rows), feature_sets, feature_catalog


def select_regression_candidate(cv_df: pd.DataFrame) -> pd.Series:
    eligible = cv_df[
        cv_df["primary_eligible"].fillna(False)
        & cv_df["cv_rmse_mean"].notna()
        & ~cv_df["model"].str.contains("baseline", case=False, na=False)
    ].copy()
    if eligible.empty:
        eligible = cv_df[cv_df["cv_rmse_mean"].notna()].copy()
    if eligible.empty:
        raise ValueError("No regression candidate produced valid training-only CV metrics")
    locked = eligible[eligible["model"].eq("ridge_a10") & eligible["feature_set"].eq("safe_normalized")].copy()
    if len(locked):
        return locked.sort_values(["cv_rmse_mean", "cv_mae_mean", "feature_count"], ascending=[True, True, True]).iloc[0]
    return eligible.sort_values(["cv_rmse_mean", "cv_mae_mean", "feature_count"], ascending=[True, True, True]).iloc[0]


def run_regression_target(df: pd.DataFrame, target_name: str, target_col: str, train_wells: list[str], validation_wells: list[str], diagnostic_only: bool = False) -> dict[str, Any]:
    cv_df, feature_sets, feature_catalog = group_cv_regression(df, target_name, target_col, train_wells)
    if diagnostic_only:
        valid_cv = cv_df[cv_df["cv_rmse_mean"].notna()].copy()
        if valid_cv.empty:
            selected = pd.Series({"feature_set": "safe_normalized", "model": "ridge_a1", "cv_rmse_mean": np.nan, "cv_mae_mean": np.nan, "cv_r2_mean": np.nan, "primary_eligible": True})
        else:
            selected = select_regression_candidate(cv_df)
    else:
        selected = select_regression_candidate(cv_df)

    selected_feature_set = str(selected["feature_set"])
    selected_model_name = str(selected["model"])
    features = feature_sets.get(selected_feature_set) or available_feature_sets(df[df["well_alias"].isin(train_wells)].copy())[0].get(selected_feature_set, [])
    if not features:
        raise ValueError(f"No selected features for {target_name}/{selected_feature_set}")

    train = target_rows(df, target_col, train_wells, features)
    valid = target_rows(df, target_col, validation_wells, features)
    if len(train) < 20:
        raise ValueError(f"Not enough training rows for {target_name}: {len(train)}")
    if len(valid) < 5:
        raise ValueError(f"Not enough validation rows for {target_name} on {wells_label(validation_wells)}: {len(valid)}")

    selected_model = REGRESSION_MODELS[selected_model_name]
    selected_pipe = fit_pipeline(selected_model, train[features], train[target_col].astype(float), sample_weight=regression_sample_weights(train, target_col))
    transfer_m, transfer_pred = evaluate_regression_model(selected_pipe, valid, features, target_col)
    base = {
        "target": target_name,
        "target_column": target_col,
        "task_type": "regression",
        "model": selected_model_name,
        "feature_set": selected_feature_set,
        "selection_stage": "external_transfer_after_training_well_depth_block_cv" if not diagnostic_only else "diagnostic_external_transfer_after_training_well_cv",
        "train_wells": wells_label(train_wells),
        "validation_well": wells_label(validation_wells),
        "validation_wells": wells_label(validation_wells),
        "validation_scope": "combined_transfer_wells",
        "feature_count": len(features),
        "train_rows": len(train),
        "validation_rows": len(valid),
        "cv_rmse_mean_for_selection": selected.get("cv_rmse_mean", np.nan),
        "cv_mae_mean_for_selection": selected.get("cv_mae_mean", np.nan),
        "cv_mode_for_selection": selected.get("cv_mode", TRAINING_SELECTION_MODE),
        "diagnostic_only": bool(diagnostic_only),
    }
    transfer_m.update(base)
    if target_name == "hydrate_saturation":
        transfer_m.update(saturation_detection_metric_dict(valid[target_col], transfer_pred["prediction"], threshold=OCCURRENCE_POSITIVE_SH_THRESHOLD))
    transfer_pred["target"] = target_name
    transfer_pred["model"] = selected_model_name
    transfer_pred["feature_set"] = selected_feature_set
    transfer_pred["validation_scope"] = "combined_transfer_wells"

    per_well_metrics = per_well_regression_metrics(transfer_pred, base)

    # Evaluate all candidates on transfer wells for transparency, but do not use transfer metrics for selection.
    transfer_rows = [transfer_m]
    all_candidate_predictions = [transfer_pred]
    for feature_set_name, feature_cols in feature_sets.items():
        if not feature_cols:
            continue
        tr = target_rows(df, target_col, train_wells, feature_cols)
        va = target_rows(df, target_col, validation_wells, feature_cols)
        if len(tr) < 20 or len(va) < 5:
            continue
        for model_name, model in REGRESSION_MODELS.items():
            if model_name == selected_model_name and feature_set_name == selected_feature_set:
                continue
            try:
                pipe = fit_pipeline(model, tr[feature_cols], tr[target_col].astype(float), sample_weight=regression_sample_weights(tr, target_col))
                m, p = evaluate_regression_model(pipe, va, feature_cols, target_col)
                m.update({
                    "target": target_name,
                    "target_column": target_col,
                    "task_type": "regression",
                    "model": model_name,
                    "feature_set": feature_set_name,
                    "selection_stage": "external_transfer_transparency_only_not_used_for_selection",
                    "train_wells": wells_label(train_wells),
                    "validation_well": wells_label(validation_wells),
                    "validation_wells": wells_label(validation_wells),
                    "validation_scope": "combined_transfer_wells",
                    "feature_count": len(feature_cols),
                    "train_rows": len(tr),
                    "validation_rows": len(va),
                    "cv_rmse_mean_for_selection": cv_df.loc[(cv_df["model"] == model_name) & (cv_df["feature_set"] == feature_set_name), "cv_rmse_mean"].min() if len(cv_df) else np.nan,
                    "cv_mae_mean_for_selection": cv_df.loc[(cv_df["model"] == model_name) & (cv_df["feature_set"] == feature_set_name), "cv_mae_mean"].min() if len(cv_df) else np.nan,
                    "cv_mode_for_selection": TRAINING_SELECTION_MODE,
                    "diagnostic_only": bool(diagnostic_only),
                })
                if target_name == "hydrate_saturation":
                    m.update(saturation_detection_metric_dict(va[target_col], p["prediction"], threshold=OCCURRENCE_POSITIVE_SH_THRESHOLD))
                p["target"] = target_name
                p["model"] = model_name
                p["feature_set"] = feature_set_name
                p["validation_scope"] = "combined_transfer_wells"
                transfer_rows.append(m)
                all_candidate_predictions.append(p)
            except Exception:
                continue

    transfer_metrics = pd.DataFrame(transfer_rows).sort_values(["selection_stage", "rmse", "mae"]).reset_index(drop=True)
    all_preds = pd.concat(all_candidate_predictions, ignore_index=True)
    bin_metrics = saturation_bin_metrics(transfer_pred, target_name, selected_model_name, selected_feature_set)

    # Final refit remains on the single calibration well for the deployed transfer model.
    final_train = train.copy()
    final_pipe = fit_pipeline(selected_model, final_train[features], final_train[target_col].astype(float), sample_weight=regression_sample_weights(final_train, target_col))

    try:
        perm = permutation_importance(selected_pipe, valid[features], valid[target_col].astype(float), n_repeats=8, random_state=RANDOM_SEED, scoring="neg_root_mean_squared_error")
        imp = pd.DataFrame({
            "target": target_name,
            "model": selected_model_name,
            "feature_set": selected_feature_set,
            "feature": features,
            "importance_mean": perm.importances_mean,
            "importance_std": perm.importances_std,
            "importance_scoring": "neg_root_mean_squared_error",
            "importance_caveat": "computed on external transfer wells for review; not used for model selection",
        }).sort_values("importance_mean", ascending=False)
    except Exception as exc:
        imp = pd.DataFrame({"target": [target_name], "model": [selected_model_name], "feature_set": [selected_feature_set], "feature": ["importance_failed"], "importance_mean": [np.nan], "importance_std": [np.nan], "note": [str(exc)]})

    return {
        "task_type": "regression",
        "target": target_name,
        "target_col": target_col,
        "train_wells": train_wells,
        "validation_wells": validation_wells,
        "validation_well": wells_label(validation_wells),
        "features": features,
        "feature_set": selected_feature_set,
        "cv_metrics": cv_df,
        "feature_catalog": feature_catalog,
        "metrics": transfer_metrics,
        "selected_blind_metrics": pd.DataFrame([transfer_m]),
        "transfer_metrics_by_well": per_well_metrics,
        "predictions": all_preds,
        "selected_predictions": transfer_pred,
        "bin_metrics": bin_metrics,
        "feature_importance": imp,
        "selected_model_name": selected_model_name,
        "selected_validation_pipeline": selected_pipe,
        "final_pipeline": final_pipe,
        "final_train_rows": len(final_train),
        "final_train_wells": train_wells,
        "diagnostic_only": bool(diagnostic_only),
    }


def group_cv_classification(df: pd.DataFrame, target_col: str, train_wells: list[str]) -> tuple[pd.DataFrame, dict[str, list[str]], pd.DataFrame]:
    train0 = df[df["well_alias"].isin(train_wells) & df[target_col].notna()].copy()
    feature_sets, feature_catalog = available_feature_sets(train0)
    rows = []
    for feature_set_name, features in feature_sets.items():
        if not features:
            continue
        train = target_rows(df, target_col, train_wells, features)
        groups, cv_mode, n_groups = make_depth_block_groups(train)
        for model_name, model in CLASSIFICATION_MODELS.items():
            fold_rows = []
            if len(train) < 20 or n_groups < 2 or train[target_col].nunique(dropna=True) < 2:
                rows.append({
                    "target": "hydrate_occurrence",
                    "task_type": "classification",
                    "feature_set": feature_set_name,
                    "model": model_name,
                    "cv_status": "not_enough_groups_rows_or_classes",
                    "cv_mode": cv_mode,
                    "cv_folds": 0,
                    "cv_f1_mean": np.nan,
                    "cv_balanced_accuracy_mean": np.nan,
                    "cv_roc_auc_mean": np.nan,
                    "primary_eligible": feature_set_name in PRIMARY_ALLOWED_FEATURE_SETS,
                    "train_wells": wells_label(train_wells),
                })
                continue
            cv = GroupKFold(n_splits=n_groups)
            for fold_i, (tr_idx, va_idx) in enumerate(cv.split(train[features], train[target_col], groups=groups), start=1):
                tr = train.iloc[tr_idx].copy()
                va = train.iloc[va_idx].copy()
                if len(tr) < 10 or len(va) < 5 or tr[target_col].nunique(dropna=True) < 2:
                    continue
                try:
                    pipe = fit_pipeline(model, tr[features], tr[target_col].astype(int), sample_weight=classification_sample_weights(tr, target_col))
                    proba = classifier_probability(pipe, va[features])
                    pred_label = (proba >= OCCURRENCE_CLASSIFICATION_THRESHOLD).astype(int)
                    m = classification_metric_dict(va[target_col].astype(int), proba, pred_label)
                    m.update({"fold": fold_i, "heldout_train_block": str(np.unique(groups[va_idx]).tolist()), "cv_mode": cv_mode})
                    fold_rows.append(m)
                except Exception as exc:
                    fold_rows.append({"fold": fold_i, "f1": np.nan, "balanced_accuracy": np.nan, "roc_auc": np.nan, "cv_mode": cv_mode, "note": str(exc)})
            fold_df = pd.DataFrame(fold_rows)
            rows.append({
                "target": "hydrate_occurrence",
                "task_type": "classification",
                "feature_set": feature_set_name,
                "model": model_name,
                "cv_status": "ok" if fold_df.get("f1", pd.Series(dtype=float)).notna().any() else "failed",
                "cv_mode": cv_mode,
                "cv_folds": int(fold_df.get("f1", pd.Series(dtype=float)).notna().sum()),
                "cv_f1_mean": float(fold_df["f1"].mean()) if "f1" in fold_df else np.nan,
                "cv_balanced_accuracy_mean": float(fold_df["balanced_accuracy"].mean()) if "balanced_accuracy" in fold_df else np.nan,
                "cv_roc_auc_mean": float(fold_df["roc_auc"].mean()) if "roc_auc" in fold_df else np.nan,
                "primary_eligible": feature_set_name in PRIMARY_ALLOWED_FEATURE_SETS,
                "feature_count": len(features),
                "train_rows_cv_pool": len(train),
                "train_wells": wells_label(train_wells),
            })
    return pd.DataFrame(rows), feature_sets, feature_catalog


def select_classification_candidate(cv_df: pd.DataFrame) -> pd.Series:
    eligible = cv_df[
        cv_df["primary_eligible"].fillna(False)
        & (~cv_df["model"].str.contains("baseline", case=False, na=False))
        & (cv_df[["cv_f1_mean", "cv_balanced_accuracy_mean", "cv_roc_auc_mean"]].notna().any(axis=1))
    ].copy()
    if eligible.empty:
        eligible = cv_df[(~cv_df["model"].str.contains("baseline", case=False, na=False))].copy()
    if eligible.empty:
        eligible = cv_df.copy()
    eligible["selection_score"] = eligible["cv_roc_auc_mean"].fillna(eligible["cv_f1_mean"]).fillna(eligible["cv_balanced_accuracy_mean"])
    locked = eligible[eligible["model"].eq("logistic_balanced") & eligible["feature_set"].eq("safe_normalized")].copy()
    if len(locked):
        return locked.sort_values(["selection_score", "cv_f1_mean", "cv_balanced_accuracy_mean", "feature_count"], ascending=[False, False, False, True], na_position="last").iloc[0]
    if eligible["selection_score"].notna().any():
        return eligible.sort_values(["selection_score", "cv_f1_mean", "cv_balanced_accuracy_mean", "feature_count"], ascending=[False, False, False, True]).iloc[0]
    return pd.Series({"feature_set": "safe_normalized", "model": "logistic_balanced", "selection_score": np.nan, "cv_mode": TRAINING_SELECTION_MODE})


def per_well_classification_metrics(pred_df: pd.DataFrame, base: dict[str, Any]) -> pd.DataFrame:
    rows = []
    if pred_df.empty:
        return pd.DataFrame(rows)
    for well, sub in pred_df.groupby("well_alias", dropna=False):
        if len(sub) < 2:
            continue
        m = classification_metric_dict(sub["reference"].astype(int), sub["occurrence_probability_ml"], sub["predicted_label"].astype(int))
        row = dict(base)
        row.update(m)
        row["validation_scope"] = "per_transfer_well"
        row["validation_well"] = well
        row["validation_rows"] = len(sub)
        rows.append(row)
    return pd.DataFrame(rows)


def run_occurrence_classifier(df: pd.DataFrame, train_wells: list[str], validation_wells: list[str]) -> dict[str, Any]:
    target_name = "hydrate_occurrence"
    target_col = "hydrate_occurrence_label"
    cv_df, feature_sets, feature_catalog = group_cv_classification(df, target_col, train_wells)
    selected = select_classification_candidate(cv_df)
    selected_feature_set = str(selected["feature_set"])
    selected_model_name = str(selected["model"])
    features = feature_sets.get(selected_feature_set) or available_feature_sets(df[df["well_alias"].isin(train_wells)].copy())[0].get(selected_feature_set, [])
    if not features:
        raise ValueError(f"No selected occurrence features for {selected_feature_set}")

    train = target_rows(df, target_col, train_wells, features)
    valid = target_rows(df, target_col, validation_wells, features)
    if len(train) < 20:
        raise ValueError(f"Not enough occurrence training rows: {len(train)}")
    if len(valid) < 5:
        raise ValueError(f"Not enough occurrence validation rows on {wells_label(validation_wells)}: {len(valid)}")
    if train[target_col].nunique(dropna=True) < 2:
        raise ValueError("Occurrence classifier needs both positive and negative labels in training wells")

    model = CLASSIFICATION_MODELS[selected_model_name]
    selected_pipe = fit_pipeline(model, train[features], train[target_col].astype(int), sample_weight=classification_sample_weights(train, target_col))
    proba = classifier_probability(selected_pipe, valid[features])
    pred_label = (proba >= OCCURRENCE_CLASSIFICATION_THRESHOLD).astype(int)
    transfer_m = classification_metric_dict(valid[target_col].astype(int), proba, pred_label)
    base = {
        "target": target_name,
        "target_column": target_col,
        "task_type": "classification",
        "model": selected_model_name,
        "feature_set": selected_feature_set,
        "selection_stage": "external_transfer_after_training_well_depth_block_cv",
        "train_wells": wells_label(train_wells),
        "validation_well": wells_label(validation_wells),
        "validation_wells": wells_label(validation_wells),
        "validation_scope": "combined_transfer_wells",
        "feature_count": len(features),
        "train_rows": len(train),
        "validation_rows": len(valid),
        "positive_threshold_sh": OCCURRENCE_POSITIVE_SH_THRESHOLD,
        "negative_threshold_sh": OCCURRENCE_NEGATIVE_SH_THRESHOLD,
        "classification_threshold": OCCURRENCE_CLASSIFICATION_THRESHOLD,
        "cv_f1_mean_for_selection": selected.get("cv_f1_mean", np.nan),
        "cv_balanced_accuracy_mean_for_selection": selected.get("cv_balanced_accuracy_mean", np.nan),
        "cv_roc_auc_mean_for_selection": selected.get("cv_roc_auc_mean", np.nan),
        "cv_mode_for_selection": selected.get("cv_mode", TRAINING_SELECTION_MODE),
        "diagnostic_only": False,
    }
    transfer_m.update(base)

    tmp_cols = [
        "well_alias", "well_name", "site", "depth_m", "depth_ft", "hydrate_saturation_reference",
        "hydrate_occurrence_label", "occurrence_label_status", "hydrate_occurrence_screen",
        "occurrence_probability_screen", "qc_status", "sh_nmr_density_calc", "sh_archie_calc",
        "sw_archie_calc", "rw_est_ohm_m",
    ]
    tmp_cols = [c for c in tmp_cols if c in valid.columns]
    transfer_pred = valid[tmp_cols].copy()
    transfer_pred["target"] = target_name
    transfer_pred["model"] = selected_model_name
    transfer_pred["feature_set"] = selected_feature_set
    transfer_pred["validation_scope"] = "combined_transfer_wells"
    transfer_pred["reference"] = valid[target_col].astype(int).to_numpy()
    transfer_pred["occurrence_probability_ml"] = np.clip(proba, 0.0, 1.0)
    transfer_pred["predicted_label"] = pred_label
    transfer_pred["label_residual"] = transfer_pred["predicted_label"] - transfer_pred["reference"]

    per_well_metrics = per_well_classification_metrics(transfer_pred, base)

    transfer_rows = [transfer_m]
    all_pred_tables = [transfer_pred]
    for feature_set_name, feature_cols in feature_sets.items():
        if not feature_cols:
            continue
        tr = target_rows(df, target_col, train_wells, feature_cols)
        va = target_rows(df, target_col, validation_wells, feature_cols)
        if len(tr) < 20 or len(va) < 5 or tr[target_col].nunique(dropna=True) < 2:
            continue
        for model_name, mmodel in CLASSIFICATION_MODELS.items():
            if model_name == selected_model_name and feature_set_name == selected_feature_set:
                continue
            try:
                pipe = fit_pipeline(mmodel, tr[feature_cols], tr[target_col].astype(int), sample_weight=classification_sample_weights(tr, target_col))
                p = classifier_probability(pipe, va[feature_cols])
                lab = (p >= OCCURRENCE_CLASSIFICATION_THRESHOLD).astype(int)
                m = classification_metric_dict(va[target_col].astype(int), p, lab)
                m.update({
                    "target": target_name,
                    "target_column": target_col,
                    "task_type": "classification",
                    "model": model_name,
                    "feature_set": feature_set_name,
                    "selection_stage": "external_transfer_transparency_only_not_used_for_selection",
                    "train_wells": wells_label(train_wells),
                    "validation_well": wells_label(validation_wells),
                    "validation_wells": wells_label(validation_wells),
                    "validation_scope": "combined_transfer_wells",
                    "feature_count": len(feature_cols),
                    "train_rows": len(tr),
                    "validation_rows": len(va),
                    "positive_threshold_sh": OCCURRENCE_POSITIVE_SH_THRESHOLD,
                    "negative_threshold_sh": OCCURRENCE_NEGATIVE_SH_THRESHOLD,
                    "classification_threshold": OCCURRENCE_CLASSIFICATION_THRESHOLD,
                    "cv_mode_for_selection": TRAINING_SELECTION_MODE,
                    "diagnostic_only": False,
                })
                tab = va[tmp_cols].copy()
                tab["target"] = target_name
                tab["model"] = model_name
                tab["feature_set"] = feature_set_name
                tab["validation_scope"] = "combined_transfer_wells"
                tab["reference"] = va[target_col].astype(int).to_numpy()
                tab["occurrence_probability_ml"] = np.clip(p, 0.0, 1.0)
                tab["predicted_label"] = lab
                tab["label_residual"] = tab["predicted_label"] - tab["reference"]
                transfer_rows.append(m)
                all_pred_tables.append(tab)
            except Exception:
                continue

    metrics = pd.DataFrame(transfer_rows).sort_values(["selection_stage", "f1", "balanced_accuracy"], ascending=[True, False, False]).reset_index(drop=True)
    predictions = pd.concat(all_pred_tables, ignore_index=True)

    final_train = train.copy()
    final_pipe = fit_pipeline(model, final_train[features], final_train[target_col].astype(int), sample_weight=classification_sample_weights(final_train, target_col))

    try:
        scoring = "roc_auc" if valid[target_col].nunique() == 2 else "accuracy"
        perm = permutation_importance(selected_pipe, valid[features], valid[target_col].astype(int), n_repeats=8, random_state=RANDOM_SEED, scoring=scoring)
        imp = pd.DataFrame({
            "target": target_name,
            "model": selected_model_name,
            "feature_set": selected_feature_set,
            "feature": features,
            "importance_mean": perm.importances_mean,
            "importance_std": perm.importances_std,
            "importance_scoring": scoring,
            "importance_caveat": "computed on external transfer wells for review; not used for model selection",
        }).sort_values("importance_mean", ascending=False)
    except Exception as exc:
        imp = pd.DataFrame({"target": [target_name], "model": [selected_model_name], "feature_set": [selected_feature_set], "feature": ["importance_failed"], "importance_mean": [np.nan], "importance_std": [np.nan], "note": [str(exc)]})

    return {
        "task_type": "classification",
        "target": target_name,
        "target_col": target_col,
        "train_wells": train_wells,
        "validation_wells": validation_wells,
        "validation_well": wells_label(validation_wells),
        "features": features,
        "feature_set": selected_feature_set,
        "cv_metrics": cv_df,
        "feature_catalog": feature_catalog,
        "metrics": metrics,
        "selected_blind_metrics": pd.DataFrame([transfer_m]),
        "transfer_metrics_by_well": per_well_metrics,
        "predictions": predictions,
        "selected_predictions": transfer_pred,
        "feature_importance": imp,
        "selected_model_name": selected_model_name,
        "selected_validation_pipeline": selected_pipe,
        "final_pipeline": final_pipe,
        "final_train_rows": len(final_train),
        "final_train_wells": train_wells,
        "diagnostic_only": False,
    }

# Run V25 primary 3-to-1 transfer outputs.
results = []
results.append(run_regression_target(features_df, "hydrate_saturation", "hydrate_saturation_reference", HYDRATE_TRAIN_WELLS, HYDRATE_VALIDATION_WELLS, diagnostic_only=False))

water_skip_rows = []
if WATER_MODEL_MODE == "skip":
    water_skip_rows.append({
        "target": "water_saturation",
        "status": "skipped_by_v25_default",
        "reason": "V25 final report focuses on hydrate saturation and occurrence; water remains opt-in diagnostic only.",
        "train_wells": wells_label(WATER_TRAIN_WELLS),
        "validation_wells": wells_label(WATER_VALIDATION_WELLS),
    })
else:
    try:
        results.append(run_regression_target(features_df, "water_saturation", "water_saturation_reference", WATER_TRAIN_WELLS, WATER_VALIDATION_WELLS, diagnostic_only=(WATER_MODEL_MODE == "diagnostic_only")))
    except Exception as exc:
        water_skip_rows.append({
            "target": "water_saturation",
            "status": "skipped_runtime_exception",
            "reason": f"{type(exc).__name__}: {exc}",
            "train_wells": wells_label(WATER_TRAIN_WELLS),
            "validation_wells": wells_label(WATER_VALIDATION_WELLS),
        })
water_diagnostic_status_df = pd.DataFrame(water_skip_rows)
occurrence_result = run_occurrence_classifier(features_df, OCCURRENCE_TRAIN_WELLS, OCCURRENCE_VALIDATION_WELLS)

# Consolidated tables.
metrics_df = pd.concat([r["metrics"] for r in results], ignore_index=True)
predictions_df = pd.concat([r["predictions"] for r in results], ignore_index=True)
selected_regression_metrics_df = pd.concat([r["selected_blind_metrics"] for r in results], ignore_index=True)
cv_metrics_df = pd.concat([*[r["cv_metrics"] for r in results], occurrence_result["cv_metrics"]], ignore_index=True)
feature_set_catalog_df = pd.concat([*[r["feature_catalog"] for r in results], occurrence_result["feature_catalog"]], ignore_index=True).drop_duplicates().reset_index(drop=True)
bin_metrics_df = pd.concat([r["bin_metrics"] for r in results if len(r.get("bin_metrics", pd.DataFrame()))], ignore_index=True) if any(len(r.get("bin_metrics", pd.DataFrame())) for r in results) else pd.DataFrame()
occurrence_metrics_df = occurrence_result["metrics"]
occurrence_predictions_df = occurrence_result["predictions"]
feature_importance_df = pd.concat([*[r["feature_importance"] for r in results], occurrence_result["feature_importance"]], ignore_index=True)
transfer_metrics_by_well_df = pd.concat([*[r.get("transfer_metrics_by_well", pd.DataFrame()) for r in results], occurrence_result.get("transfer_metrics_by_well", pd.DataFrame())], ignore_index=True, sort=False)
saturation_detection_source_df = pd.concat([metrics_df, transfer_metrics_by_well_df], ignore_index=True, sort=False)
saturation_detection_metrics_df = saturation_detection_source_df[
    saturation_detection_source_df.get("target", pd.Series(dtype=str)).astype(str).eq("hydrate_saturation")
    & saturation_detection_source_df.get("saturation_detection_threshold", pd.Series(index=saturation_detection_source_df.index, dtype=float)).notna()
].copy() if len(saturation_detection_source_df) else pd.DataFrame()

selected_rows = []
for r in results:
    best = r["selected_blind_metrics"].iloc[0].to_dict()
    selected_rows.append({
        "target": r["target"],
        "task_type": r["task_type"],
        "selected_model": r["selected_model_name"],
        "feature_set": r["feature_set"],
        "validation_well": r["validation_well"],
        "validation_wells": r["validation_well"],
        "train_wells": "+".join(r["train_wells"]),
        "final_train_wells": "+".join(r["final_train_wells"]),
        "features_used": ", ".join(r["features"]),
        "feature_count": len(r["features"]),
        "final_train_rows": r["final_train_rows"],
        "validation_rmse": best.get("rmse", np.nan),
        "validation_mae": best.get("mae", np.nan),
        "validation_r2": best.get("r2", np.nan),
        "validation_saturation_detection_threshold": best.get("saturation_detection_threshold", np.nan),
        "validation_saturation_precision": best.get("saturation_precision", np.nan),
        "validation_saturation_recall": best.get("saturation_recall", np.nan),
        "validation_saturation_f1": best.get("saturation_f1", np.nan),
        "validation_saturation_accuracy": best.get("saturation_accuracy", np.nan),
        "validation_accuracy": np.nan,
        "validation_f1": np.nan,
        "validation_roc_auc": np.nan,
        "diagnostic_only": r.get("diagnostic_only", False),
        "note": "Diagnostic-only water transfer; not a primary claim" if r["target"] == "water_saturation" else "V25 primary 3-to-1 transfer: trained on three active wells, selected inside the training pool, then tested on the held-out well",
    })

best_occ = occurrence_result["selected_blind_metrics"].iloc[0].to_dict()
selected_rows.append({
    "target": occurrence_result["target"],
    "task_type": occurrence_result["task_type"],
    "selected_model": occurrence_result["selected_model_name"],
    "feature_set": occurrence_result["feature_set"],
    "validation_well": occurrence_result["validation_well"],
    "validation_wells": occurrence_result["validation_well"],
    "train_wells": "+".join(occurrence_result["train_wells"]),
    "final_train_wells": "+".join(occurrence_result["final_train_wells"]),
    "features_used": ", ".join(occurrence_result["features"]),
    "feature_count": len(occurrence_result["features"]),
    "final_train_rows": occurrence_result["final_train_rows"],
    "validation_rmse": np.nan,
    "validation_mae": np.nan,
    "validation_r2": np.nan,
    "validation_saturation_detection_threshold": np.nan,
    "validation_saturation_precision": np.nan,
    "validation_saturation_recall": np.nan,
    "validation_saturation_f1": np.nan,
    "validation_saturation_accuracy": np.nan,
    "validation_accuracy": best_occ.get("accuracy", np.nan),
    "validation_f1": best_occ.get("f1", np.nan),
    "validation_roc_auc": best_occ.get("roc_auc", np.nan),
    "diagnostic_only": False,
    "note": f"V25 occurrence label demo: positive Sh >= {OCCURRENCE_POSITIVE_SH_THRESHOLD:.2f}, negative Sh <= {OCCURRENCE_NEGATIVE_SH_THRESHOLD:.2f}; trained on three active wells and tested on the held-out well",
})
selected_summary_df = pd.DataFrame(selected_rows)




# V25 final report table: leave-one-well-out 3-to-1 folds.
def v25_fold_label(train_wells: list[str], heldout_well: str) -> str:
    return f"train_{''.join(train_wells)}__test_{heldout_well}"


def v25_annotate_frame(frame: pd.DataFrame, *, heldout_well: str, train_wells: list[str], fold_id: str, table_role: str) -> pd.DataFrame:
    if frame is None or frame.empty:
        return pd.DataFrame()
    out = frame.copy()
    out.insert(0, "v25_table_role", table_role)
    out.insert(1, "v25_eval_mode", "leave_one_well_out_3_to_1")
    out.insert(2, "v25_fold_id", fold_id)
    out.insert(3, "v25_heldout_well", heldout_well)
    out.insert(4, "v25_train_wells", wells_label(train_wells))
    out.insert(5, "v25_train_well_count", len(train_wells))
    out.insert(6, "v25_test_well_count", 1)
    return out


def v25_build_leave_one_out_3to1_tables() -> dict[str, pd.DataFrame]:
    hydrate_selected, hydrate_all, hydrate_by_well, hydrate_bins = [], [], [], []
    occurrence_selected, occurrence_all, occurrence_by_well = [], [], []
    failures = []
    for heldout_well in ACTIVE_PROJECT_WELLS:
        train_wells = [well for well in ACTIVE_PROJECT_WELLS if well != heldout_well]
        fold_id = v25_fold_label(train_wells, heldout_well)
        try:
            hyd = run_regression_target(
                features_df,
                "hydrate_saturation",
                "hydrate_saturation_reference",
                train_wells,
                [heldout_well],
                diagnostic_only=False,
            )
            hydrate_selected.append(v25_annotate_frame(hyd["selected_blind_metrics"], heldout_well=heldout_well, train_wells=train_wells, fold_id=fold_id, table_role="selected_hydrate_saturation"))
            hydrate_all.append(v25_annotate_frame(hyd["metrics"], heldout_well=heldout_well, train_wells=train_wells, fold_id=fold_id, table_role="all_hydrate_saturation_candidates"))
            hydrate_by_well.append(v25_annotate_frame(hyd.get("transfer_metrics_by_well", pd.DataFrame()), heldout_well=heldout_well, train_wells=train_wells, fold_id=fold_id, table_role="hydrate_saturation_by_heldout_well"))
            hydrate_bins.append(v25_annotate_frame(hyd.get("bin_metrics", pd.DataFrame()), heldout_well=heldout_well, train_wells=train_wells, fold_id=fold_id, table_role="hydrate_saturation_bin_bias"))
        except Exception as exc:
            failures.append({
                "v25_fold_id": fold_id,
                "v25_heldout_well": heldout_well,
                "v25_train_wells": wells_label(train_wells),
                "task": "hydrate_saturation",
                "status": "failed",
                "error_type": type(exc).__name__,
                "error": str(exc),
            })
        try:
            occ = run_occurrence_classifier(features_df, train_wells, [heldout_well])
            occurrence_selected.append(v25_annotate_frame(occ["selected_blind_metrics"], heldout_well=heldout_well, train_wells=train_wells, fold_id=fold_id, table_role="selected_hydrate_occurrence"))
            occurrence_all.append(v25_annotate_frame(occ["metrics"], heldout_well=heldout_well, train_wells=train_wells, fold_id=fold_id, table_role="all_hydrate_occurrence_candidates"))
            occurrence_by_well.append(v25_annotate_frame(occ.get("transfer_metrics_by_well", pd.DataFrame()), heldout_well=heldout_well, train_wells=train_wells, fold_id=fold_id, table_role="occurrence_by_heldout_well"))
        except Exception as exc:
            failures.append({
                "v25_fold_id": fold_id,
                "v25_heldout_well": heldout_well,
                "v25_train_wells": wells_label(train_wells),
                "task": "hydrate_occurrence",
                "status": "failed",
                "error_type": type(exc).__name__,
                "error": str(exc),
            })
    return {
        "v25_loo_hydrate_selected_df": pd.concat(hydrate_selected, ignore_index=True, sort=False) if hydrate_selected else pd.DataFrame(),
        "v25_loo_hydrate_all_metrics_df": pd.concat(hydrate_all, ignore_index=True, sort=False) if hydrate_all else pd.DataFrame(),
        "v25_loo_hydrate_by_well_df": pd.concat(hydrate_by_well, ignore_index=True, sort=False) if hydrate_by_well else pd.DataFrame(),
        "v25_loo_hydrate_bins_df": pd.concat(hydrate_bins, ignore_index=True, sort=False) if hydrate_bins else pd.DataFrame(),
        "v25_loo_occurrence_selected_df": pd.concat(occurrence_selected, ignore_index=True, sort=False) if occurrence_selected else pd.DataFrame(),
        "v25_loo_occurrence_all_metrics_df": pd.concat(occurrence_all, ignore_index=True, sort=False) if occurrence_all else pd.DataFrame(),
        "v25_loo_occurrence_by_well_df": pd.concat(occurrence_by_well, ignore_index=True, sort=False) if occurrence_by_well else pd.DataFrame(),
        "v25_loo_failures_df": pd.DataFrame(failures),
    }


if V25_RUN_LEAVE_ONE_OUT_3TO1:
    _v25_loo_tables = v25_build_leave_one_out_3to1_tables()
else:
    _v25_loo_tables = {
        "v25_loo_hydrate_selected_df": pd.DataFrame(),
        "v25_loo_hydrate_all_metrics_df": pd.DataFrame(),
        "v25_loo_hydrate_by_well_df": pd.DataFrame(),
        "v25_loo_hydrate_bins_df": pd.DataFrame(),
        "v25_loo_occurrence_selected_df": pd.DataFrame(),
        "v25_loo_occurrence_all_metrics_df": pd.DataFrame(),
        "v25_loo_occurrence_by_well_df": pd.DataFrame(),
        "v25_loo_failures_df": pd.DataFrame([{"status": "skipped", "reason": "V25_RUN_LEAVE_ONE_OUT_3TO1=0"}]),
    }
globals().update(_v25_loo_tables)


def v25_build_loo_aggregate_summary() -> pd.DataFrame:
    rows = []
    hyd = v25_loo_hydrate_selected_df.copy() if isinstance(globals().get("v25_loo_hydrate_selected_df"), pd.DataFrame) else pd.DataFrame()
    if len(hyd):
        for (model, feature_set), group in hyd.groupby(["model", "feature_set"], dropna=False):
            rows.append({
                "task": "hydrate_saturation",
                "model": model,
                "feature_set": feature_set,
                "folds": int(group["v25_fold_id"].nunique()),
                "mean_rmse": float(pd.to_numeric(group.get("rmse"), errors="coerce").mean()),
                "mean_mae": float(pd.to_numeric(group.get("mae"), errors="coerce").mean()),
                "mean_r2": float(pd.to_numeric(group.get("r2"), errors="coerce").mean()),
                "mean_bias": float(pd.to_numeric(group.get("bias"), errors="coerce").mean()) if "bias" in group else np.nan,
                "heldout_wells": "+".join(group["v25_heldout_well"].astype(str).tolist()),
                "claim_note": "Leave-one-well-out 3-to-1 development review; not blind new-well validation because V15-V20 informed candidate design.",
            })
    occ = v25_loo_occurrence_selected_df.copy() if isinstance(globals().get("v25_loo_occurrence_selected_df"), pd.DataFrame) else pd.DataFrame()
    if len(occ):
        for (model, feature_set), group in occ.groupby(["model", "feature_set"], dropna=False):
            rows.append({
                "task": "hydrate_occurrence",
                "model": model,
                "feature_set": feature_set,
                "folds": int(group["v25_fold_id"].nunique()),
                "mean_accuracy": float(pd.to_numeric(group.get("accuracy"), errors="coerce").mean()),
                "mean_balanced_accuracy": float(pd.to_numeric(group.get("balanced_accuracy"), errors="coerce").mean()) if "balanced_accuracy" in group else np.nan,
                "mean_precision": float(pd.to_numeric(group.get("precision"), errors="coerce").mean()) if "precision" in group else np.nan,
                "mean_recall": float(pd.to_numeric(group.get("recall"), errors="coerce").mean()) if "recall" in group else np.nan,
                "mean_f1": float(pd.to_numeric(group.get("f1"), errors="coerce").mean()),
                "mean_roc_auc": float(pd.to_numeric(group.get("roc_auc"), errors="coerce").mean()) if "roc_auc" in group else np.nan,
                "heldout_wells": "+".join(group["v25_heldout_well"].astype(str).tolist()),
                "claim_note": "Occurrence labels are derived from saturation thresholds; report precision and recall separately.",
            })
    return pd.DataFrame(rows)


v25_loo_aggregate_summary_df = v25_build_loo_aggregate_summary()

V25_REGION_HOLDOUT_LABELS = {
    "WellA": "Canada/Mallik WellA holdout",
    "WellC": "Alaska North Slope WellC holdout",
}


def v25_feature_group_role(feature_set: Any) -> str:
    name = str(feature_set)
    if name == "safe_normalized":
        return "baseline_safe_logs"
    if name == "all_allowed_except_density_porosity_review":
        return "grouped_logs_without_density_porosity_family"
    if name == "all_allowed_inputs_review":
        return "all_allowed_logs_and_safe_equations"
    if name == "equation_proxy_review":
        return "equation_proxy_package"
    if name == "measured_only":
        return "measured_log_only_baseline"
    return "other_candidate_feature_set"


def v25_pick_best_grouped_log_rows(
    frame: pd.DataFrame,
    *,
    task: str,
    task_type: str,
) -> pd.DataFrame:
    if frame is None or frame.empty:
        return pd.DataFrame()
    required = {"v25_heldout_well", "v25_train_wells", "feature_set"}
    if not required.issubset(frame.columns):
        return pd.DataFrame()

    work = frame.copy()
    work = work[work["v25_heldout_well"].astype(str).isin(V25_REGION_HOLDOUT_WELLS)].copy()
    work = work[work["feature_set"].astype(str).isin(V25_GROUPED_LOG_FEATURE_SETS)].copy()
    if work.empty:
        return pd.DataFrame()

    numeric_columns = [
        "rmse",
        "mae",
        "r2",
        "bias",
        "saturation_precision",
        "saturation_recall",
        "saturation_f1",
        "saturation_accuracy",
        "accuracy",
        "balanced_accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
        "validation_rows",
        "train_rows",
        "feature_count",
    ]
    for column in numeric_columns:
        if column in work.columns:
            work[column] = pd.to_numeric(work[column], errors="coerce")

    rows: list[pd.Series] = []
    for (_heldout_well, _feature_set), group in work.groupby(
        ["v25_heldout_well", "feature_set"],
        dropna=False,
    ):
        group = group.copy()
        if task_type == "regression":
            sort_cols = [c for c in ["rmse", "mae", "r2"] if c in group.columns]
            ascending = [c in {"rmse", "mae"} for c in sort_cols]
        else:
            sort_cols = [
                c
                for c in ["f1", "balanced_accuracy", "accuracy", "roc_auc"]
                if c in group.columns
            ]
            ascending = [False] * len(sort_cols)
        if sort_cols:
            group = group.sort_values(sort_cols, ascending=ascending, na_position="last")
        rows.append(group.iloc[0])

    if not rows:
        return pd.DataFrame()

    out = pd.DataFrame(rows).reset_index(drop=True)
    out = out.loc[:, ~out.columns.duplicated()].copy()

    out["v25_region_question"] = (
        "WellA Canada/Mallik holdout vs WellC Alaska holdout grouped-log comparison"
    )
    out["task"] = task
    out["task_type"] = task_type
    out["v25_region_holdout_label"] = (
        out["v25_heldout_well"]
        .map(V25_REGION_HOLDOUT_LABELS)
        .fillna(out["v25_heldout_well"].astype(str))
    )
    out["v25_feature_group_role"] = out["feature_set"].map(v25_feature_group_role)
    out["v25_selection_guardrail"] = (
        "External held-out metrics are summarized after train-pool CV selection; "
        "this table is diagnostic evidence, not a held-out-row winner selection rule."
    )
    out["v25_claim_boundary"] = (
        "Known-four-well development comparison; not blind new-well validation "
        "or gas-origin proof by itself."
    )

    metric_cols = [
        "rmse",
        "mae",
        "r2",
        "bias",
        "saturation_precision",
        "saturation_recall",
        "saturation_f1",
        "saturation_accuracy",
        "accuracy",
        "balanced_accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
    ]
    out["baseline_feature_set"] = "safe_normalized"

    for (_heldout_well, _task_group), idxs in out.groupby(
        ["v25_heldout_well", "task_type"],
        dropna=False,
    ).groups.items():
        idxs = list(idxs)
        subset = out.loc[idxs]
        baseline_rows = subset[subset["feature_set"].astype(str).eq("safe_normalized")]
        if baseline_rows.empty:
            baseline_rows = subset.head(1)
            out.loc[idxs, "baseline_feature_set"] = str(
                baseline_rows.iloc[0].get("feature_set", "")
            )
        baseline = baseline_rows.iloc[0]
        for column in metric_cols:
            if column not in out.columns:
                continue
            base_value = pd.to_numeric(
                pd.Series([baseline.get(column, np.nan)]),
                errors="coerce",
            ).iloc[0]
            out.loc[idxs, f"baseline_{column}"] = base_value
            out.loc[idxs, f"delta_{column}_vs_baseline"] = (
                pd.to_numeric(out.loc[idxs, column], errors="coerce") - base_value
            )

    if "delta_rmse_vs_baseline" in out.columns:
        out["rmse_improvement_vs_baseline"] = -out["delta_rmse_vs_baseline"]

    ordered_first = [
        "v25_region_question",
        "task",
        "task_type",
        "v25_region_holdout_label",
        "v25_heldout_well",
        "v25_train_wells",
        "feature_set",
        "v25_feature_group_role",
        "model",
        "validation_scope",
        "selection_stage",
        "feature_count",
        "train_rows",
        "validation_rows",
        "baseline_feature_set",
    ]
    ordered: list[str] = []

    def add_ordered_column(column: str) -> None:
        if column in out.columns and column not in ordered:
            ordered.append(column)

    for column in ordered_first:
        add_ordered_column(column)
    for column in out.columns:
        if (
            column in metric_cols
            or column.startswith("baseline_")
            or column.startswith("delta_")
            or column.endswith("_improvement_vs_baseline")
        ):
            add_ordered_column(column)
    for column in ["v25_selection_guardrail", "v25_claim_boundary"]:
        add_ordered_column(column)
    for column in out.columns:
        add_ordered_column(column)

    return out[ordered].reset_index(drop=True)


def v25_build_region_holdout_grouped_log_comparison() -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    hydrate_all = globals().get("v25_loo_hydrate_all_metrics_df", pd.DataFrame())
    occurrence_all = globals().get("v25_loo_occurrence_all_metrics_df", pd.DataFrame())

    hydrate = v25_pick_best_grouped_log_rows(
        hydrate_all,
        task="hydrate_saturation",
        task_type="regression",
    )
    if not hydrate.empty:
        frames.append(hydrate)

    occurrence = v25_pick_best_grouped_log_rows(
        occurrence_all,
        task="hydrate_occurrence",
        task_type="classification",
    )
    if not occurrence.empty:
        frames.append(occurrence)

    if not frames:
        return pd.DataFrame(
            [
                {
                    "v25_region_question": (
                        "WellA Canada/Mallik holdout vs WellC Alaska holdout "
                        "grouped-log comparison"
                    ),
                    "status": "no_rows_available",
                    "reason": (
                        "Leave-one-well-out candidate metrics were empty or "
                        "V25_REGION_HOLDOUT_WELLS/V25_GROUPED_LOG_FEATURE_SETS "
                        "did not match available rows."
                    ),
                    "requested_holdout_wells": "+".join(V25_REGION_HOLDOUT_WELLS),
                    "requested_feature_sets": "+".join(V25_GROUPED_LOG_FEATURE_SETS),
                    "v25_selection_guardrail": (
                        "No external heldout metrics were used for model selection."
                    ),
                }
            ]
        )

    return pd.concat(frames, ignore_index=True, sort=False)


v25_region_holdout_grouped_log_df = v25_build_region_holdout_grouped_log_comparison()


def build_model_selection_audit() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    combined_metrics = pd.concat([metrics_df, occurrence_metrics_df], ignore_index=True, sort=False)
    selected_lookup = selected_summary_df.copy()
    for _, selected in selected_lookup.iterrows():
        target = selected.get("target", "")
        task_type = selected.get("task_type", "")
        train_wells = [part for part in str(selected.get("train_wells", "")).split("+") if part]
        train_well_count = len(set(train_wells))
        target_metrics = combined_metrics[combined_metrics.get("target", pd.Series(dtype=str)).astype(str).eq(str(target))].copy()
        if "diagnostic_only" in target_metrics.columns:
            target_metrics = target_metrics[target_metrics["diagnostic_only"].astype(str).str.lower().isin(["false", "0", "nan"])]
        if task_type == "classification":
            rank_cols = ["f1", "balanced_accuracy", "roc_auc"]
            available = [col for col in rank_cols if col in target_metrics.columns]
            best_external = target_metrics.sort_values(available, ascending=[False] * len(available), na_position="last").head(1) if available else pd.DataFrame()
            selected_metric = selected.get("validation_f1", np.nan)
            best_metric = best_external[available[0]].iloc[0] if len(best_external) and available else np.nan
            metric_name = available[0] if available else "f1"
        else:
            best_external = target_metrics.sort_values(["rmse", "mae"], ascending=[True, True], na_position="last").head(1) if {"rmse", "mae"}.issubset(target_metrics.columns) else pd.DataFrame()
            selected_metric = selected.get("validation_rmse", np.nan)
            best_metric = best_external["rmse"].iloc[0] if len(best_external) and "rmse" in best_external else np.nan
            metric_name = "rmse"
        if len(best_external):
            best_row = best_external.iloc[0]
            best_model = best_row.get("model", "")
            best_feature_set = best_row.get("feature_set", "")
            best_stage = best_row.get("selection_stage", "")
        else:
            best_model = ""
            best_feature_set = ""
            best_stage = ""
        selected_pair = f"{selected.get('selected_model', '')}/{selected.get('feature_set', '')}"
        best_pair = f"{best_model}/{best_feature_set}" if best_model or best_feature_set else ""
        if train_well_count >= 2:
            selection_status = "transfer_aware_group_cv_inside_training_pool"
            next_action = "Keep final validation wells locked out of model selection; review per-heldout-train-well metrics before claims."
        else:
            selection_status = "depth_block_cv_only_single_training_well"
            next_action = "For transfer-aware selection, set at least two scientifically approved training wells, e.g. HYDRATE_TRAIN_WELLS=WellA,WellB,WellD with WellC held out for the V25 comparison."
        cv_modes = target_metrics["cv_mode_for_selection"].dropna() if len(target_metrics) and "cv_mode_for_selection" in target_metrics else pd.Series(dtype=object)
        rows.append({
            "target": target,
            "task_type": task_type,
            "train_wells": selected.get("train_wells", ""),
            "validation_wells": selected.get("validation_wells", selected.get("validation_well", "")),
            "train_well_count": train_well_count,
            "model_selection_strategy": MODEL_SELECTION_STRATEGY,
            "selection_status": selection_status,
            "cv_mode_for_selection": cv_modes.iloc[0] if len(cv_modes) else TRAINING_SELECTION_MODE,
            "selected_model_feature_set": selected_pair,
            "selected_validation_metric_name": metric_name,
            "selected_validation_metric": selected_metric,
            "best_external_transfer_model_feature_set": best_pair,
            "best_external_transfer_metric": best_metric,
            "best_external_transfer_stage": best_stage,
            "external_transfer_used_for_selection": False,
            "selection_reason": "Selected by training-pool CV only; external transfer candidates are transparency diagnostics.",
            "next_action": next_action,
        })
    return pd.DataFrame(rows)


model_selection_audit_df = build_model_selection_audit()

# Correctness/readiness checks to make the model reviewable before adding stability/producibility.
correctness_checks_df = pd.DataFrame([
    {
        "check": "validation_design",
        "status": f"hydrate train {'+'.join(HYDRATE_TRAIN_WELLS)} -> test {'+'.join(HYDRATE_VALIDATION_WELLS)}",
        "meaning": "V25 transfer design: three training wells choose models by training-pool CV; the held-out well stays external until final scoring. Leave-one-out 3-to-1 folds are exported separately.",
    },
    {
        "check": "training_selection_mode",
        "status": TRAINING_SELECTION_MODE,
        "meaning": "Model/feature-set selection happens inside the training pool. V25 multiwell training uses whole-well GroupKFold; depth-block CV is retained only as a fallback for manual reduced-well smoke tests. External transfer results are not used for selection.",
    },
    {
        "check": "normalized_input_mode",
        "status": "active" if NORMALIZED_INPUT_MODE else "inactive",
        "meaning": "All non-depth curves are treated as normalized. Physical equations are proxy/review features unless raw units are supplied.",
    },
    {
        "check": "primary_feature_policy",
        "status": PRIMARY_FEATURE_POLICY,
        "meaning": "Primary model selection is limited to measured/safe-normalized feature sets; proxy equation features are review-only by default.",
    },
    {
        "check": "wide_feature_set_trials",
        "status": "selection_eligible" if WIDE_FEATURE_SET_SELECTION_ELIGIBLE else "transparency_only",
        "meaning": "The run tests all allowed inputs and all allowed inputs except the density-porosity family after leakage blocking, coverage filtering, and training-pool CV.",
    },
    {
        "check": "target_leakage_block",
        "status": "active",
        "meaning": "S_h/S_wr, Archie Sh/Sw, NMR-density Sh, rule screens, labels, and model outputs are blocked from X predictors.",
    },
    {
        "check": "saturation_precision_recall",
        "status": ",".join(f"Sh>={x:.2f}" for x in SATURATION_DETECTION_THRESHOLDS),
        "meaning": "Precision/recall for saturation are reported only after thresholding continuous saturation predictions into hydrate-detected versus not-detected intervals.",
    },
    {
        "check": "target_bin_weights",
        "status": "active" if APPLY_TARGET_BIN_WEIGHTS else "inactive",
        "meaning": "High-saturation and rare target bins receive weighting so the model is not optimized only for low-saturation rows.",
    },
    {
        "check": "water_model_status",
        "status": WATER_MODEL_MODE,
        "meaning": "Water saturation is not treated as a primary accuracy claim because external water-target coverage is limited.",
    },
])

print("Selected models:")
display(selected_summary_df)
print("Training-well depth-block CV selection metrics:")
display(cv_metrics_df.sort_values(["target", "task_type", "primary_eligible"], ascending=[True, True, False]).head(30))
print("External transfer regression metrics:")
display(metrics_df.sort_values(["target", "selection_stage", "rmse"]).head(30))
print("Per-transfer-well metrics:")
display(transfer_metrics_by_well_df.head(30))
print("Hydrate saturation threshold detection metrics:")
display(saturation_detection_metrics_df.head(30))
print("Occurrence classifier external transfer metrics:")
display(occurrence_metrics_df.head(20))
print("Correctness checks:")
display(correctness_checks_df)
print("V25 grouped-log region holdout comparison:")
display(v25_region_holdout_grouped_log_df)
