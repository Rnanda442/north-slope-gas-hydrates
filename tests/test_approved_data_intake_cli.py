from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = PROJECT_ROOT / "01_pipeline" / "validate_approved_data_headers.py"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI_SCRIPT), *args],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_cli_accepts_inline_headers_and_creates_json_csv(tmp_path: Path):
    result = run_cli(
        "--headers",
        "DEPTH,GR,RHOB,Rt,Sh",
        "--source-label",
        "inline_public_safe",
        "--output-dir",
        str(tmp_path),
        "--output-prefix",
        "inline_audit",
    )

    assert "ready_for_schema_design: True" in result.stdout
    csv_path = tmp_path / "inline_audit.csv"
    json_path = tmp_path / "inline_audit.json"
    assert csv_path.exists()
    assert json_path.exists()
    report = load_json(json_path)
    assert report["source_label"] == "inline_public_safe"
    assert report["ready_for_schema_design"] is True
    assert report["ready_for_training"] is False
    assert "Sh" in report["target_only_headers"]


def test_cli_reads_header_list_csv(tmp_path: Path):
    header_list = tmp_path / "headers.csv"
    header_list.write_text("header\nDEPTH\nGR\nRHOB\nRt\nCAL1\n", encoding="utf-8")

    run_cli(
        "--headers-csv",
        str(header_list),
        "--output-dir",
        str(tmp_path),
        "--output-prefix",
        "header_list_audit",
    )

    report = load_json(tmp_path / "header_list_audit.json")
    assert report["input_mode"] == "headers_csv"
    assert report["recognized_header_count"] == 5
    assert report["qc_headers"] == ["CAL1"]


def test_cli_source_csv_reads_headers_only_and_never_outputs_row_values(tmp_path: Path):
    source_csv = tmp_path / "private_well_rows_secret.csv"
    source_csv.write_text(
        "DEPTH,GR,RHOB,Rt,Sh\n12345,SECRET_VALUE_123,2.1,50,0.8\n",
        encoding="utf-8",
    )

    run_cli(
        "--source-csv",
        str(source_csv),
        "--header-only",
        "--output-dir",
        str(tmp_path),
        "--output-prefix",
        "source_header_only",
    )

    csv_text = (tmp_path / "source_header_only.csv").read_text(encoding="utf-8")
    json_text = (tmp_path / "source_header_only.json").read_text(encoding="utf-8")
    assert "SECRET_VALUE_123" not in csv_text
    assert "SECRET_VALUE_123" not in json_text
    assert "12345" not in csv_text
    assert "12345" not in json_text
    report = load_json(tmp_path / "source_header_only.json")
    assert report["input_mode"] == "source_csv_header_only"
    assert report["no_row_values_read"] is True


def test_cli_target_only_fields_in_x_allowed_emit_leakage_flags(tmp_path: Path):
    run_cli(
        "--headers",
        "DEPTH,GR,RHOB,Rt,Sh",
        "--x-allowed",
        "DEPTH,GR,Sh",
        "--output-dir",
        str(tmp_path),
        "--output-prefix",
        "leakage_audit",
    )

    report = load_json(tmp_path / "leakage_audit.json")
    assert "target_only_in_x_allowed:Sh" in report["leakage_flags"]
    assert report["ready_for_training"] is False


def test_cli_sanitizes_private_source_paths_by_default(tmp_path: Path):
    private_dir = tmp_path / "private user folder"
    private_dir.mkdir()
    source_csv = private_dir / "restricted_named_well_private.csv"
    source_csv.write_text("DEPTH,GR,RHOB,Rt\n1,PRIVATE_ROW_VALUE,2.1,40\n", encoding="utf-8")

    run_cli(
        "--source-csv",
        str(source_csv),
        "--header-only",
        "--output-dir",
        str(tmp_path),
        "--output-prefix",
        "sanitized_source",
    )

    json_text = (tmp_path / "sanitized_source.json").read_text(encoding="utf-8")
    assert str(source_csv) not in json_text
    assert "restricted_named_well_private" not in json_text
    assert "PRIVATE_ROW_VALUE" not in json_text
    report = load_json(tmp_path / "sanitized_source.json")
    assert report["source_label"] == "source_csv_header_only"


def test_committed_demo_report_says_training_is_false():
    demo_json = (
        PROJECT_ROOT
        / "data"
        / "public_ml_products"
        / "intake_readiness_reports"
        / "demo_header_audit_2026-06-15.json"
    )

    report = load_json(demo_json)
    assert report["source_label"] == "demo_public_safe"
    assert report["ready_for_schema_design"] is True
    assert report["ready_for_training"] is False
    assert report["no_row_values_read"] is True
