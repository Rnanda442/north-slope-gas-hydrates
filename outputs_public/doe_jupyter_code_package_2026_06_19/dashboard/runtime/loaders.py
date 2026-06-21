from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pandas as pd

from dashboard.runtime.schemas import (
    APPROVED_INPUT_MODE,
    RuntimeConfig,
    default_curve_aliases,
)


def normalize_aliases(aliases: dict[str, tuple[str, ...]] | None = None) -> dict[str, tuple[str, ...]]:
    merged = default_curve_aliases()
    if aliases:
        merged.update(aliases)
    return merged


def standardize_curve_columns(
    frame: pd.DataFrame,
    aliases: dict[str, tuple[str, ...]] | None = None,
) -> pd.DataFrame:
    lookup = {column.lower(): column for column in frame.columns}
    rename_map: dict[str, str] = {}
    for canonical, candidates in normalize_aliases(aliases).items():
        for candidate in candidates:
            actual = lookup.get(candidate.lower())
            if actual is not None:
                rename_map[actual] = canonical
                break
    standardized = frame.rename(columns=rename_map).copy()
    for column in standardized.columns:
        if column == "well_alias":
            continue
        numeric = pd.to_numeric(standardized[column], errors="coerce")
        if numeric.notna().any():
            standardized[column] = numeric
    if "well_alias" in standardized:
        standardized["well_alias"] = standardized["well_alias"].astype(str)
    return standardized


def load_csv_logs(paths: tuple[str, ...], aliases: dict[str, tuple[str, ...]] | None = None) -> pd.DataFrame:
    frames = []
    for raw_path in paths:
        path = Path(raw_path)
        frame = pd.read_csv(path)
        standardized = standardize_curve_columns(frame, aliases)
        if "well_alias" not in standardized:
            standardized["well_alias"] = path.stem
        frames.append(standardized)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def load_las_logs(*_: object) -> pd.DataFrame:
    raise NotImplementedError(
        "LAS loading is a local approved-runtime adapter. Add lasio inside the "
        "authorized environment and keep approved files outside Git."
    )


def load_runtime_data(
    config: RuntimeConfig | None,
    synthetic_factory: Callable[[], pd.DataFrame],
) -> pd.DataFrame:
    config = config or RuntimeConfig(curve_aliases=default_curve_aliases())
    if not config.curve_aliases:
        config = RuntimeConfig(
            input_mode=config.input_mode,
            approved_csv_paths=config.approved_csv_paths,
            approved_las_paths=config.approved_las_paths,
            core_csv_paths=config.core_csv_paths,
            output_root=config.output_root,
            model_root=config.model_root,
            curve_aliases=default_curve_aliases(),
        )
    if config.input_mode == "synthetic":
        return synthetic_factory()
    if config.input_mode == APPROVED_INPUT_MODE:
        if config.approved_las_paths:
            return load_las_logs(config.approved_las_paths, config.curve_aliases)
        return load_csv_logs(config.approved_csv_paths, config.curve_aliases)
    raise ValueError(f"Unknown runtime input_mode: {config.input_mode}")
