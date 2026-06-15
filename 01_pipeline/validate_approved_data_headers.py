from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from typing import Iterable

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dashboard.approved_data_intake import build_intake_readiness_report, load_field_role_table


DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "public_ml_products" / "intake_readiness_reports"


def split_headers(headers_text: str | None) -> list[str]:
    if not headers_text:
        return []
    return [part.strip() for part in headers_text.split(",") if part.strip()]


def sanitize_label(label: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9_.-]+", "_", label.strip())
    sanitized = sanitized.strip("._-")
    return sanitized[:100] or "header_audit"


def source_label_for_input(
    *,
    input_mode: str,
    source_path: Path | None = None,
    source_label: str | None = None,
    include_source_name: bool = False,
) -> str:
    if source_label:
        return sanitize_label(source_label)
    if include_source_name and source_path is not None:
        return sanitize_label(str(source_path))
    return {
        "inline_headers": "inline_headers",
        "headers_csv": "headers_csv_input",
        "source_csv_header_only": "source_csv_header_only",
    }.get(input_mode, "header_audit")


def read_header_list_csv(path: Path) -> list[str]:
    frame = pd.read_csv(path)
    if frame.empty and len(frame.columns) == 1:
        return [str(frame.columns[0])]
    if "header" in frame.columns:
        values = frame["header"].dropna().astype(str).tolist()
    elif "original_header" in frame.columns:
        values = frame["original_header"].dropna().astype(str).tolist()
    else:
        first_column = frame.columns[0]
        values = frame[first_column].dropna().astype(str).tolist()
    return [value.strip() for value in values if value.strip()]


def read_source_csv_headers(path: Path) -> list[str]:
    return pd.read_csv(path, nrows=0).columns.astype(str).tolist()


def resolve_headers(args: argparse.Namespace) -> tuple[list[str], str, Path | None]:
    input_count = sum(
        bool(value)
        for value in [
            args.headers,
            args.headers_csv,
            args.source_csv,
        ]
    )
    if input_count != 1:
        raise SystemExit("Provide exactly one of --headers, --headers-csv, or --source-csv.")
    if args.source_csv and not args.header_only:
        raise SystemExit("--source-csv requires --header-only so row values are never read.")

    if args.headers:
        return split_headers(args.headers), "inline_headers", None
    if args.headers_csv:
        path = Path(args.headers_csv)
        return read_header_list_csv(path), "headers_csv", path
    path = Path(args.source_csv)
    return read_source_csv_headers(path), "source_csv_header_only", path


def list_value(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, tuple):
        return [str(item) for item in value]
    return [str(value)]


def join_list(value: object) -> str:
    return "; ".join(list_value(value))


def report_to_public_summary(
    report: dict[str, object],
    *,
    source_label: str,
    input_mode: str,
    headers: Iterable[str],
) -> dict[str, object]:
    recognized = report.get("recognized_headers")
    recognized_count = int(len(recognized)) if recognized is not None else 0
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_label": source_label,
        "input_mode": input_mode,
        "header_count": len(list(headers)),
        "recognized_header_count": recognized_count,
        "unknown_headers": list_value(report.get("unknown_headers")),
        "predictor_headers": list_value(report.get("predictor_headers")),
        "derived_feature_headers": list_value(report.get("derived_feature_headers")),
        "qc_headers": list_value(report.get("qc_headers")),
        "context_headers": list_value(report.get("context_headers")),
        "target_only_headers": list_value(report.get("target_only_headers")),
        "unresolved_headers": list_value(report.get("unresolved_headers")),
        "leakage_flags": list_value(report.get("leakage_flags")),
        "missing_required_fields": list_value(report.get("missing_required_fields")),
        "blocked_reasons": list_value(report.get("blocked_reasons")),
        "mentor_questions": list_value(report.get("mentor_questions")),
        "ready_for_schema_design": bool(report.get("ready_for_schema_design", False)),
        "ready_for_training": bool(report.get("ready_for_training", False)),
        "ready_for_public_release": bool(report.get("ready_for_public_release", False)),
        "no_row_values_read": True,
        "guardrail": "Header-only public-safe audit; no approved/private row values read or written.",
    }


def csv_summary_frame(summary: dict[str, object]) -> pd.DataFrame:
    row = {
        key: join_list(value) if isinstance(value, list) else value
        for key, value in summary.items()
    }
    return pd.DataFrame([row])


def markdown_summary(summary: dict[str, object]) -> str:
    blocked = summary["blocked_reasons"] or ["none"]
    mentor = summary["mentor_questions"] or ["none"]
    return "\n".join(
        [
            "# Approved-Data Intake Readiness Report",
            "",
            f"Generated UTC: `{summary['generated_at_utc']}`",
            "",
            "## Public-Safe Scope",
            "",
            "This is a header-only readiness report. It does not include approved well-log rows, private workbook rows, restricted identifiers, occurrence probabilities, saturation predictions, trained metrics, or sensitive outputs.",
            "",
            "## Summary",
            "",
            f"- Source label: `{summary['source_label']}`",
            f"- Input mode: `{summary['input_mode']}`",
            f"- Header count: `{summary['header_count']}`",
            f"- Recognized header count: `{summary['recognized_header_count']}`",
            f"- Ready for schema design: `{summary['ready_for_schema_design']}`",
            f"- Ready for training: `{summary['ready_for_training']}`",
            f"- Ready for public release: `{summary['ready_for_public_release']}`",
            "",
            "## Header Roles",
            "",
            f"- Predictors: {join_list(summary['predictor_headers']) or 'none'}",
            f"- Derived features: {join_list(summary['derived_feature_headers']) or 'none'}",
            f"- QC headers: {join_list(summary['qc_headers']) or 'none'}",
            f"- Context headers: {join_list(summary['context_headers']) or 'none'}",
            f"- Target-only headers: {join_list(summary['target_only_headers']) or 'none'}",
            f"- Unresolved headers: {join_list(summary['unresolved_headers']) or 'none'}",
            f"- Unknown headers: {join_list(summary['unknown_headers']) or 'none'}",
            "",
            "## Blocked Reasons",
            "",
            *[f"- `{reason}`" for reason in blocked],
            "",
            "## Mentor Questions",
            "",
            *[f"- {question}" for question in mentor],
            "",
            "## Guardrails",
            "",
            "- Stability remains methane 5 ppt admissibility/context only, not hydrate proof.",
            "- Occurrence and saturation labels are Y-only target/calibration/validation fields.",
            "- Target-only fields must never enter `X_allowed`.",
        ]
    )


def write_outputs(
    summary: dict[str, object],
    *,
    output_dir: Path,
    output_prefix: str,
    markdown_output: Path | None = None,
    write_markdown: bool = False,
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = sanitize_label(output_prefix)
    csv_path = output_dir / f"{prefix}.csv"
    json_path = output_dir / f"{prefix}.json"
    csv_summary_frame(summary).to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

    written = {"csv": csv_path, "json": json_path}
    if markdown_output is not None or write_markdown:
        md_path = markdown_output or output_dir / f"{prefix}.md"
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(markdown_summary(summary), encoding="utf-8")
        written["markdown"] = md_path
    return written


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a public-safe approved-data header readiness audit without reading row values."
    )
    parser.add_argument("--headers", help="Comma-separated header list, e.g. DEPTH,GR,RHOB,Rt,Sh.")
    parser.add_argument("--headers-csv", type=Path, help="CSV with a header or original_header column.")
    parser.add_argument("--source-csv", type=Path, help="CSV data source. Requires --header-only; only nrows=0 is read.")
    parser.add_argument("--header-only", action="store_true", help="Required with --source-csv to confirm row values are not read.")
    parser.add_argument("--x-allowed", help="Optional comma-separated candidate X_allowed headers.")
    parser.add_argument("--source-label", help="Public-safe source label to record in outputs.")
    parser.add_argument("--include-source-name", action="store_true", help="Record the input source name/path in outputs. Use only for public-safe paths.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--output-prefix", default="header_audit")
    parser.add_argument("--write-markdown", action="store_true")
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--allow-missing-log-adapters", action="store_true")
    parser.add_argument("--approved-rows-available", action="store_true")
    parser.add_argument("--split-policy-confirmed", action="store_true")
    parser.add_argument("--validation-plan-confirmed", action="store_true")
    parser.add_argument("--public-release-review-complete", action="store_true")
    parser.add_argument("--authoritative-saturation-field")
    parser.add_argument("--saturation-unit-convention", choices=["fraction", "percent"])
    parser.add_argument("--occurrence-evidence-source")
    parser.add_argument("--occurrence-confidence")
    parser.add_argument("--occurrence-interval-policy")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    headers, input_mode, source_path = resolve_headers(args)
    field_roles = load_field_role_table(PROJECT_ROOT)

    metadata = {
        "authoritative_saturation_field": args.authoritative_saturation_field,
        "saturation_unit_convention": args.saturation_unit_convention,
        "occurrence_evidence_source": args.occurrence_evidence_source,
        "occurrence_confidence": args.occurrence_confidence,
        "occurrence_interval_policy": args.occurrence_interval_policy,
    }
    metadata = {key: value for key, value in metadata.items() if value}

    options = {
        "metadata": metadata,
        "x_allowed_headers": split_headers(args.x_allowed) if args.x_allowed else None,
        "approved_rows_available": args.approved_rows_available,
        "split_policy_confirmed": args.split_policy_confirmed,
        "validation_plan_confirmed": args.validation_plan_confirmed,
        "public_release_review_complete": args.public_release_review_complete,
        "allow_missing_log_adapters": args.allow_missing_log_adapters,
    }
    report = build_intake_readiness_report(headers, field_roles, options=options)
    source_label = source_label_for_input(
        input_mode=input_mode,
        source_path=source_path,
        source_label=args.source_label,
        include_source_name=args.include_source_name,
    )
    summary = report_to_public_summary(
        report,
        source_label=source_label,
        input_mode=input_mode,
        headers=headers,
    )
    written = write_outputs(
        summary,
        output_dir=args.output_dir,
        output_prefix=args.output_prefix,
        markdown_output=args.markdown_output,
        write_markdown=args.write_markdown,
    )

    print("Header audit complete.")
    for label, path in written.items():
        print(f"{label}: {path}")
    print(f"ready_for_schema_design: {summary['ready_for_schema_design']}")
    print(f"ready_for_training: {summary['ready_for_training']}")


if __name__ == "__main__":
    main()
