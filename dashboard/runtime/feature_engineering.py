from __future__ import annotations

import numpy as np
import pandas as pd

from dashboard.runtime.schemas import CHONG_ML_FEATURE_COLUMNS


def add_standard_features(logs: pd.DataFrame) -> pd.DataFrame:
    features = logs.copy()
    if "gr_api" in features:
        features["vshale"] = np.clip((features["gr_api"] - 30) / (105 - 30), 0, 1)
    if "rhob_g_cc" in features and "density_porosity_vv" not in features:
        features["density_porosity_vv"] = np.clip((2.65 - features["rhob_g_cc"]) / (2.65 - 1.03), 0, 0.7)
    if "dt_us_ft" in features and "vp_km_s" not in features:
        features["vp_km_s"] = 304.8 / features["dt_us_ft"]
    if "dts_us_ft" in features and "vs_km_s" not in features:
        features["vs_km_s"] = 304.8 / features["dts_us_ft"]
    if {"vp_km_s", "vs_km_s"}.issubset(features.columns):
        features["vp_vs_ratio"] = features["vp_km_s"] / features["vs_km_s"]
    if {"rhob_g_cc", "vs_km_s"}.issubset(features.columns):
        features["shear_modulus_gpa"] = features["rhob_g_cc"] * features["vs_km_s"] ** 2
        features["mu_rho"] = features["shear_modulus_gpa"]
    if {"rhob_g_cc", "vp_km_s", "vs_km_s"}.issubset(features.columns):
        features["bulk_modulus_gpa"] = features["rhob_g_cc"] * (
            features["vp_km_s"] ** 2 - (4.0 / 3.0) * features["vs_km_s"] ** 2
        )
        features["lambda_rho"] = features["rhob_g_cc"] * (
            features["vp_km_s"] ** 2 - 2 * features["vs_km_s"] ** 2
        )
    if {"density_porosity_vv", "nmr_porosity_vv"}.issubset(features.columns):
        features["nmr_density_separation_vv"] = features["density_porosity_vv"] - features["nmr_porosity_vv"]
        features["nmr_density_hydrate_proxy"] = np.clip(
            features["nmr_density_separation_vv"] / features["density_porosity_vv"].clip(0.01),
            0,
            1,
        )
    if {"density_porosity_vv", "rt_ohm_m"}.issubset(features.columns):
        features["archie_hydrate_proxy"] = np.clip(
            1 - ((0.12 / ((features["density_porosity_vv"].clip(0.04) ** 2) * features["rt_ohm_m"])) ** 0.5),
            0,
            1,
        )
    if "depth_m" in features:
        features["ghsz_context"] = np.where(
            features["depth_m"].between(470, 1080),
            "stable working screen",
            "outside working screen",
        )
    if "caliper_in" in features:
        caliper = pd.to_numeric(features["caliper_in"], errors="coerce")
        if "well_alias" in features:
            washout_threshold = caliper.groupby(features["well_alias"]).transform(
                lambda values: values.quantile(0.95)
            )
        else:
            washout_threshold = pd.Series(caliper.quantile(0.95), index=features.index)
        features["caliper_washout_flag"] = caliper.ge(washout_threshold) & caliper.notna()

    available_ml_features = [
        column for column in CHONG_ML_FEATURE_COLUMNS if column in features.columns
    ]
    if available_ml_features:
        features["chong_ml_available_feature_count"] = features[available_ml_features].notna().sum(axis=1)
        features["chong_ml_complete_case_flag"] = features[available_ml_features].notna().all(axis=1)
        if "caliper_washout_flag" in features:
            features["chong_ml_complete_case_flag"] &= ~features["caliper_washout_flag"]
    return features
