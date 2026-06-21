from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Iterable

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dashboard.runtime.model_run_tracker import TRAINING_FIT_WARNING, load_local_model_run_tracker


SAFE_RUN_COMPARISON_COLUMNS = [
    "run_name",
    "run_types",
    "trained_target_runs",
    "target_columns",
    "unique_feature_columns",
    "feature_families",
    "excluded_columns_audited",
    "validation_statuses",
    "has_external_or_whole_workbook_validation",
    "stability_join_status",
    "final_claim_ready",
    "final_claim_needed",
]
TRAINING_METRIC_COLUMNS = ["mean_train_r2"]


def timestamp_label() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def default_output_dir(project_root: Path) -> Path:
    return project_root / "outputs_runtime" / f"model_run_review_assets_{timestamp_label()}"


def safe_columns(frame: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=list(columns))
    selected = frame[[column for column in columns if column in frame.columns]].copy()
    for column in columns:
        if column not in selected.columns:
            selected[column] = pd.NA
    return selected[list(columns)]


def feature_family_counts(features: pd.DataFrame) -> pd.DataFrame:
    columns = ["run_name", "feature_family", "feature_count"]
    if features.empty or not {"run_name", "feature_family"}.issubset(features.columns):
        return pd.DataFrame(columns=columns)
    grouped = (
        features.assign(feature_family=features["feature_family"].fillna("unknown"))
        .groupby(["run_name", "feature_family"], dropna=False)
        .size()
        .reset_index(name="feature_count")
        .sort_values(["run_name", "feature_family"])
    )
    return grouped[columns]


def exclusion_reason_counts(exclusions: pd.DataFrame) -> pd.DataFrame:
    columns = ["run_name", "reason", "excluded_column_count"]
    if exclusions.empty or not {"run_name", "reason"}.issubset(exclusions.columns):
        return pd.DataFrame(columns=columns)
    scoped = exclusions.copy()
    if "decision" in scoped.columns:
        scoped = scoped[scoped["decision"].astype(str).str.lower().eq("excluded")]
    grouped = (
        scoped.assign(reason=scoped["reason"].fillna("unspecified"))
        .groupby(["run_name", "reason"], dropna=False)
        .size()
        .reset_index(name="excluded_column_count")
        .sort_values(["run_name", "reason"])
    )
    return grouped[columns]


def validation_status_counts(public_summary: pd.DataFrame) -> pd.DataFrame:
    columns = ["validation_status", "target_run_count"]
    if public_summary.empty or "validation_status" not in public_summary.columns:
        return pd.DataFrame(columns=columns)
    return (
        public_summary.assign(validation_status=public_summary["validation_status"].fillna("unknown"))
        .groupby("validation_status", dropna=False)
        .size()
        .reset_index(name="target_run_count")
        .sort_values("validation_status")
    )


def _font(size: int):
    try:
        from PIL import ImageFont

        return ImageFont.truetype("arial.ttf", size=size)
    except Exception:
        from PIL import ImageFont

        return ImageFont.load_default()


def _short_text(value: object, limit: int = 44) -> str:
    text = str(value)
    if len(text) <= limit:
        return text
    return f"{text[: limit - 3]}..."


def write_bar_chart_png(
    frame: pd.DataFrame,
    *,
    label_column: str,
    value_column: str,
    title: str,
    subtitle: str,
    output_path: Path,
) -> bool:
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.with_suffix(".txt").write_text(
            f"{title}\n{subtitle}\nPillow is unavailable, so no PNG was rendered.\n",
            encoding="utf-8",
        )
        return False

    rows = []
    if not frame.empty and {label_column, value_column}.issubset(frame.columns):
        scoped = frame[[label_column, value_column]].copy()
        scoped[value_column] = pd.to_numeric(scoped[value_column], errors="coerce").fillna(0)
        rows = [(str(row[label_column]), float(row[value_column])) for _, row in scoped.iterrows()]

    width = 1400
    height = max(520, 185 + max(len(rows), 1) * 58)
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    title_font = _font(34)
    subtitle_font = _font(20)
    label_font = _font(18)
    value_font = _font(18)

    draw.rectangle((0, 0, width, 86), fill=(28, 45, 57))
    draw.text((42, 24), title, fill="white", font=title_font)
    draw.text((42, 104), subtitle, fill=(75, 89, 99), font=subtitle_font)

    if not rows:
        draw.rounded_rectangle((42, 190, width - 42, 330), radius=18, fill=(244, 247, 249), outline=(205, 214, 220))
        draw.text((78, 245), "No local runtime summary rows were found.", fill=(55, 66, 74), font=label_font)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path)
        return True

    max_value = max(value for _, value in rows) or 1.0
    label_x = 44
    bar_x = 420
    bar_width = width - bar_x - 155
    y = 170
    palette = [(43, 111, 138), (84, 141, 120), (183, 117, 78), (115, 92, 145), (92, 118, 169)]

    for index, (label, value) in enumerate(rows):
        color = palette[index % len(palette)]
        bar_len = int(bar_width * (value / max_value))
        draw.text((label_x, y + 6), _short_text(label), fill=(41, 50, 56), font=label_font)
        draw.rounded_rectangle((bar_x, y, bar_x + bar_width, y + 28), radius=8, fill=(235, 240, 243))
        draw.rounded_rectangle((bar_x, y, bar_x + max(bar_len, 4), y + 28), radius=8, fill=color)
        draw.text((bar_x + bar_width + 20, y + 3), f"{value:g}", fill=(41, 50, 56), font=value_font)
        y += 58

    draw.text(
        (42, height - 46),
        "Public-safe review asset: derived from local summary tables only; no approved rows, row-level predictions, or model binaries.",
        fill=(97, 106, 112),
        font=subtitle_font,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    return True


def write_markdown_brief(
    output_path: Path,
    *,
    public_summary: pd.DataFrame,
    run_comparison: pd.DataFrame,
    feature_counts: pd.DataFrame,
    validation_counts: pd.DataFrame,
) -> None:
    run_count = int(run_comparison["run_name"].nunique()) if "run_name" in run_comparison else 0
    target_count = int(len(public_summary))
    validation_lines = (
        [f"- {row['validation_status']}: {row['target_run_count']}" for _, row in validation_counts.iterrows()]
        if not validation_counts.empty
        else ["- No validation status rows found."]
    )
    feature_lines = (
        [
            f"- {row['feature_family']}: {row['feature_count']}"
            for _, row in feature_counts.groupby("feature_family", dropna=False)["feature_count"]
            .sum()
            .reset_index()
            .iterrows()
        ]
        if not feature_counts.empty
        else ["- No feature-family rows found."]
    )
    output_path.write_text(
        "\n".join(
            [
                "# Model Run Review Asset Brief",
                "",
                f"Generated UTC: `{datetime.now(timezone.utc).isoformat(timespec='seconds')}`",
                "",
                "## Scope",
                "",
                "This folder is a public-safe review export derived from ignored local runtime summaries. It does not include approved workbook rows, row-level predictions, fitted model binaries, secrets, or private runtime manifests.",
                "",
                "## Current Local Summary",
                "",
                f"- Runtime folders summarized: `{run_count}`",
                f"- Target/run cards summarized: `{target_count}`",
                f"- Metric warning: {TRAINING_FIT_WARNING}",
                "- Stability use: context, admissibility, mask, confidence, or caveat only; not hydrate proof, occurrence, or saturation.",
                "- Final claims: blocked until mentor-approved targets, whole-well/geographic validation, calibration review, and public-release approval.",
                "",
                "## Validation Status Counts",
                "",
                *validation_lines,
                "",
                "## Feature Family Counts",
                "",
                *feature_lines,
                "",
                "## Intended Use",
                "",
                "- Word companion: use the CSV tables for source-backed method/status tables.",
                "- Slide deck: use the PNGs as row-free runtime-review visuals.",
                "- Website: use the same tracker logic locally; do not publish these outputs unless reviewed.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def export_model_run_review_assets(
    project_root: Path,
    *,
    output_dir: Path | None = None,
    max_runs: int = 12,
    include_training_fit_metrics: bool = False,
) -> dict[str, object]:
    project_root = Path(project_root).resolve()
    output_dir = Path(output_dir or default_output_dir(project_root)).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    tracker = load_local_model_run_tracker(project_root, max_runs=max_runs)
    public_summary = tracker["public_safe_summary"]
    run_comparison = tracker["run_comparison"].copy()
    comparison_columns = list(SAFE_RUN_COMPARISON_COLUMNS)
    if include_training_fit_metrics:
        comparison_columns.extend(TRAINING_METRIC_COLUMNS)
    safe_run_comparison = safe_columns(run_comparison, comparison_columns)
    if include_training_fit_metrics:
        safe_run_comparison["training_metric_warning"] = TRAINING_FIT_WARNING

    feature_counts = feature_family_counts(tracker["features"])
    exclusion_counts = exclusion_reason_counts(tracker["exclusions"])
    validation_counts = validation_status_counts(public_summary)

    written: dict[str, str] = {}
    tables = {
        "public_safe_model_run_summary": public_summary,
        "public_safe_run_comparison": safe_run_comparison,
        "feature_family_counts": feature_counts,
        "exclusion_reason_counts": exclusion_counts,
        "validation_status_counts": validation_counts,
    }
    for name, frame in tables.items():
        path = output_dir / f"{name}.csv"
        frame.to_csv(path, index=False)
        written[name] = str(path)

    write_markdown_brief(
        output_dir / "model_run_review_brief.md",
        public_summary=public_summary,
        run_comparison=safe_run_comparison,
        feature_counts=feature_counts,
        validation_counts=validation_counts,
    )
    written["markdown_brief"] = str(output_dir / "model_run_review_brief.md")

    aggregate_feature_counts = (
        feature_counts.groupby("feature_family", dropna=False)["feature_count"].sum().reset_index()
        if not feature_counts.empty
        else pd.DataFrame(columns=["feature_family", "feature_count"])
    )
    write_bar_chart_png(
        aggregate_feature_counts,
        label_column="feature_family",
        value_column="feature_count",
        title="Feature Families In Local Runtime Runs",
        subtitle="Counts are schema/model-audit summaries, not row-level approved data.",
        output_path=output_dir / "feature_family_coverage.png",
    )
    write_bar_chart_png(
        validation_counts,
        label_column="validation_status",
        value_column="target_run_count",
        title="Validation Status Of Local Target Runs",
        subtitle="Training-fit rows are separated from external or whole-workbook validation.",
        output_path=output_dir / "validation_status_summary.png",
    )
    written["feature_family_coverage_png"] = str(output_dir / "feature_family_coverage.png")
    written["validation_status_summary_png"] = str(output_dir / "validation_status_summary.png")

    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "max_runs": max_runs,
        "runtime_folder_count": int(len(tracker["runs"])),
        "target_run_count": int(len(public_summary)),
        "include_training_fit_metrics": include_training_fit_metrics,
        "training_metric_warning": TRAINING_FIT_WARNING,
        "public_safe_scope": "summary tables and derived figures only",
        "not_exported": [
            "approved workbook rows",
            "row-level predictions",
            "trained model binaries",
            "private runtime manifests",
            "secrets",
        ],
        "written": written,
    }
    manifest_path = output_dir / "asset_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    written["asset_manifest"] = str(manifest_path)
    return {"output_dir": str(output_dir), **manifest}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export Word/slide-ready, row-free model-run review tables and figures from ignored runtime summaries."
    )
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--max-runs", type=int, default=12)
    parser.add_argument(
        "--include-training-fit-metrics",
        action="store_true",
        help="Include training-fit metric summaries in the local ignored export. They are not final performance claims.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = export_model_run_review_assets(
        args.project_root,
        output_dir=args.output_dir,
        max_runs=args.max_runs,
        include_training_fit_metrics=args.include_training_fit_metrics,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    print()
    print("Review assets written. Keep this folder local/ignored unless a public-safe release is approved.")


if __name__ == "__main__":
    main()
