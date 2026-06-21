from __future__ import annotations

from pathlib import Path
import subprocess
import sys

from dashboard.source_intake_inventory import (
    FOUND_SOURCE_STATUS,
    MISSING_STATUS,
    build_source_intake_inventory,
    match_registry_entry,
    source_intake_summary,
    write_source_intake_outputs,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = PROJECT_ROOT / "01_pipeline" / "build_source_intake_inventory.py"


def test_inventory_matches_known_sources_from_filenames(tmp_path: Path):
    source_drop = tmp_path / "source_drop"
    source_drop.mkdir()
    (source_drop / "collet2019.pdf").write_bytes(b"%PDF-1.4 placeholder")
    (source_drop / "falahat.pdf").write_bytes(b"%PDF-1.4 placeholder")

    inventory = build_source_intake_inventory(
        [source_drop],
        project_root=tmp_path,
        read_pdf_text=False,
    )
    found = inventory[inventory["source_status"].eq(FOUND_SOURCE_STATUS)]

    assert {"SRC_NEW_002", "SRC_NEW_005"}.issubset(set(found["source_id"]))
    assert "SRC_NEW_001" in set(
        inventory[inventory["source_status"].eq(MISSING_STATUS)]["source_id"]
    )
    assert found["safe_path"].str.contains(str(tmp_path), regex=False).sum() == 0


def test_match_registry_entry_uses_doi_text_when_filename_is_unhelpful():
    entry, confidence, score = match_registry_entry(
        "download.pdf",
        "Alaska North Slope LWD article DOI 10.1021/acs.energyfuels.5c06115",
    )

    assert entry is not None
    assert entry.source_id == "SRC_DRIVE_004"
    assert confidence == "high_doi_or_exact_title"
    assert score >= 120


def test_external_paths_are_redacted_by_default(tmp_path: Path):
    project_root = tmp_path / "repo"
    project_root.mkdir()
    external = tmp_path / "external_drive_drop"
    external.mkdir()
    (external / "sign2019.pdf").write_bytes(b"%PDF-1.4 placeholder")

    inventory = build_source_intake_inventory(
        [external],
        project_root=project_root,
        read_pdf_text=False,
    )
    row = inventory[inventory["source_id"].eq("SRC_NEW_004")].iloc[0]

    assert row["source_status"] == FOUND_SOURCE_STATUS
    assert row["safe_path"] == "[external-source]/sign2019.pdf"
    assert str(external) not in row["safe_path"]


def test_write_source_intake_outputs_creates_public_safe_reports(tmp_path: Path):
    source_drop = tmp_path / "source_drop"
    output_dir = tmp_path / "reports"
    source_drop.mkdir()
    (source_drop / "acs.energyfuels.5c06115.pdf").write_bytes(b"%PDF-1.4 placeholder")
    (source_drop / "csv_methane_5ppt_phase_curve_slide_inset.png").write_bytes(b"png")

    inventory = build_source_intake_inventory(
        [source_drop],
        project_root=tmp_path,
        read_pdf_text=False,
    )
    written = write_source_intake_outputs(
        inventory,
        output_dir=output_dir,
        date_tag="2026-06-18",
    )
    report_text = written["report"].read_text(encoding="utf-8")
    gaps_text = written["gaps"].read_text(encoding="utf-8")
    summary = source_intake_summary(inventory)

    assert written["csv"].exists()
    assert "SRC_DRIVE_004" in report_text
    assert "Excel/CSV-derived stability curve" in report_text
    assert "Do not copy raw PDFs" in report_text
    assert "SRC_NEW_001" in gaps_text
    assert "SRC_STABILITY_001" in summary["stability_source_ids"]


def test_source_intake_cli_writes_reports(tmp_path: Path):
    source_drop = tmp_path / "source_drop"
    output_dir = tmp_path / "output"
    source_drop.mkdir()
    (source_drop / "acs.energyfuels.5c05321.pdf").write_bytes(b"%PDF-1.4 placeholder")

    result = subprocess.run(
        [
            sys.executable,
            str(CLI_SCRIPT),
            "--source-dir",
            str(source_drop),
            "--output-dir",
            str(output_dir),
            "--date-tag",
            "2026-06-18",
            "--no-pdf-text",
        ],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Source intake inventory complete." in result.stdout
    assert "found_local: 1" in result.stdout
    assert (output_dir / "source_inventory_2026-06-18.csv").exists()
    assert (output_dir / "DRIVE_GMAIL_SOURCE_HANDOFF_2026-06-18.md").exists()
