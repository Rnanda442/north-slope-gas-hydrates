from __future__ import annotations

import numpy as np
import pandas as pd


def rule_based_interval_labels(features: pd.DataFrame) -> pd.DataFrame:
    labels = features.copy()
    reservoir = (
        labels.get("gr_api", pd.Series(np.inf, index=labels.index)) < 65
    ) & (
        labels.get("density_porosity_vv", pd.Series(0, index=labels.index)) >= 0.20
    )
    high_rt = labels.get("rt_ohm_m", pd.Series(0, index=labels.index)) >= 10
    elastic = labels.get("vp_km_s", pd.Series(0, index=labels.index)) >= 2.9
    stable = labels.get("ghsz_context", pd.Series("", index=labels.index)).eq("stable working screen")
    gas_risk = high_rt & (labels.get("vp_km_s", pd.Series(np.inf, index=labels.index)) < 2.35)
    labels["runtime_phase_label"] = np.select(
        [
            reservoir & stable & high_rt & elastic,
            reservoir & gas_risk,
            reservoir & ~high_rt,
            reservoir,
        ],
        [
            "hydrate-supportive multi-log response",
            "gas-supportive response",
            "good sand, no hydrate",
            "ambiguous / expert review",
        ],
        default="non-reservoir / review",
    )
    return labels


class ModelAdapter:
    """Interface placeholder for approved-environment ML models."""

    def fit(self, features: pd.DataFrame, labels: pd.Series) -> "ModelAdapter":
        raise NotImplementedError("Fit approved models locally after labels are calibrated.")

    def predict(self, features: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError("Load approved models locally from models_runtime.")
