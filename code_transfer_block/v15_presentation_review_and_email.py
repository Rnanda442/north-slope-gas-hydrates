"""
DOE/Jupyter helper for V15 presentation review and email handoff.

Run this after the V15 notebook export cell prints "DONE - files written".

It creates a compact review folder and zip packet from row-free V15 outputs:
- run summary text for Codex / presentation review
- checkpoint progress and top WLC tables
- V15 core-aware auxiliary metrics and target-comparison previews
- figure manifest, paper figures PDF, clean summary workbook, and readme
- Outlook draft with the review packet attached

It intentionally does NOT package row-level prediction CSVs or fitted models.

Run from the repository root on the DOE desktop:

    python code_transfer_block\\v15_presentation_review_and_email.py

Optional environment variables:

    PERSONAL_REVIEW_EMAIL  recipient for the Outlook draft
    V15_OUTPUT_DIR         defaults to ~/Downloads/outputs_runtime/ml_master
    V15_RUN_SLUG           defaults to v15_core_aware_multitask_ann
    V15_NO_EMAIL           set to 1 to skip Outlook
"""

from __future__ import annotations

import csv
import json
import os
import shutil
import subprocess
import textwrap
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional, Union


RUN_SLUG = os.environ.get("V15_RUN_SLUG", "v15_core_aware_multitask_ann")
OUTPUT_DIR = Path(
    os.environ.get(
        "V15_OUTPUT_DIR",
        Path.home() / "Downloads" / "outputs_runtime" / "ml_master",
    )
)
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
REVIEW_DIR = OUTPUT_DIR / f"v15_presentation_review_{RUN_SLUG}_{TIMESTAMP}"

ROW_LEVEL_OR_MODEL_TOKENS = (
    "prediction",
    "predictions",
    "selected_models",
    ".joblib",
    "row_reliability",
)

try:
    import pandas as pd
except Exception:  # pragma: no cover - DOE fallback path
    pd = None


def newest(pattern: str) -> Optional[Path]:
    candidates = [p for p in OUTPUT_DIR.glob(pattern) if p.is_file()]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def newest_dir(pattern: str) -> Optional[Path]:
    candidates = [p for p in OUTPUT_DIR.glob(pattern) if p.is_dir()]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def is_safe_review_file(path: Path) -> bool:
    lower = path.name.lower()
    return not any(token in lower for token in ROW_LEVEL_OR_MODEL_TOKENS)


def ps_quote(value: Union[str, Path]) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def file_row(path: Optional[Path], label: str) -> dict:
    if path is None:
        return {
            "label": label,
            "path": "",
            "exists": False,
            "size_bytes": "",
            "modified": "",
        }
    exists = path.exists()
    stat = path.stat() if exists else None
    return {
        "label": label,
        "path": str(path),
        "exists": exists,
        "size_bytes": stat.st_size if stat else "",
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds") if stat else "",
    }


def write_rows_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_preview(path: Optional[Path], max_rows: int = 20):
    if path is None or not path.exists() or pd is None:
        return None
    try:
        return pd.read_csv(path).head(max_rows)
    except Exception:
        return None


def sort_preview(df, preferred_desc: Iterable[str] = (), preferred_asc: Iterable[str] = ()):
    if df is None or pd is None or df.empty:
        return df
    for col in preferred_desc:
        if col in df.columns:
            return df.sort_values(col, ascending=False)
    for col in preferred_asc:
        if col in df.columns:
            return df.sort_values(col, ascending=True)
    return df


def checkpoint_progress(checkpoint_dir: Optional[Path]) -> tuple[list[dict], list[dict]]:
    progress_rows: list[dict] = []
    top_rows: list[dict] = []
    if checkpoint_dir is None or not checkpoint_dir.exists():
        return progress_rows, top_rows

    for metrics_path in sorted(checkpoint_dir.glob("*__metrics.csv")):
        parts = metrics_path.stem.split("__")
        split_name = parts[0] if parts else ""
        wlc_name = parts[1] if len(parts) > 2 else metrics_path.stem.replace("__metrics", "")
        rows = 0
        columns: list[str] = []
        try:
            with metrics_path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                columns = reader.fieldnames or []
                rows = sum(1 for _ in reader)
        except Exception:
            pass
        progress_rows.append(
            {
                "split_name": split_name,
                "wlc_name": wlc_name,
                "metric_rows": rows,
                "file": str(metrics_path),
                "columns": "; ".join(columns[:12]),
            }
        )

    if pd is None:
        return progress_rows, top_rows

    summaries = []
    for summary_path in sorted(checkpoint_dir.glob("*__summary.csv")):
        try:
            df = pd.read_csv(summary_path)
        except Exception:
            continue
        if df.empty:
            continue
        if "split_name" not in df.columns:
            stem_parts = summary_path.stem.split("__")
            df["split_name"] = stem_parts[0] if stem_parts else ""
        if "wlc_name" not in df.columns and "wlc" not in df.columns:
            stem_parts = summary_path.stem.split("__")
            df["wlc_name"] = stem_parts[1] if len(stem_parts) > 2 else summary_path.stem
        summaries.append(df)
    if summaries:
        combined = pd.concat(summaries, ignore_index=True, sort=False)
        score_desc = next((c for c in ["r2_mean", "r2", "score_mean"] if c in combined.columns), None)
        score_asc = next((c for c in ["rmse_mean", "mae_mean", "loss_mean"] if c in combined.columns), None)
        if score_desc:
            combined = combined.sort_values(["split_name", score_desc], ascending=[True, False])
        elif score_asc:
            combined = combined.sort_values(["split_name", score_asc], ascending=[True, True])
        for split_name, group in combined.groupby("split_name", dropna=False):
            row = group.iloc[0].to_dict()
            row["split_name"] = split_name
            top_rows.append({k: row[k] for k in row.keys() if k in row and not str(k).startswith("Unnamed")})
    return progress_rows, top_rows


def copy_if_present(source: Optional[Path], dest_dir: Path) -> Optional[Path]:
    if source is None or not source.exists() or not is_safe_review_file(source):
        return None
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / source.name
    shutil.copy2(source, dest)
    return dest


def copy_figures_from_manifest(figure_manifest: Optional[Path], dest_dir: Path) -> list[Path]:
    copied: list[Path] = []
    if figure_manifest is None or not figure_manifest.exists() or pd is None:
        return copied
    try:
        df = pd.read_csv(figure_manifest)
    except Exception:
        return copied
    possible_cols = [c for c in df.columns if c.lower() in {"path", "file", "filepath", "figure_path", "figure_file"}]
    if not possible_cols:
        return copied
    col = possible_cols[0]
    for value in df[col].dropna().astype(str).tolist():
        candidate = Path(value)
        if not candidate.is_absolute():
            candidate = OUTPUT_DIR / candidate
        if candidate.exists() and candidate.is_file() and candidate.suffix.lower() in {".png", ".jpg", ".jpeg", ".pdf"}:
            dest = copy_if_present(candidate, dest_dir)
            if dest:
                copied.append(dest)
    return copied


def write_excel(tables: dict[str, object], xlsx_path: Path) -> Optional[Path]:
    if pd is None:
        return None
    try:
        with pd.ExcelWriter(xlsx_path) as writer:
            for name, table in tables.items():
                if table is None:
                    continue
                df = table if hasattr(table, "to_excel") else pd.DataFrame(table)
                if df.empty:
                    continue
                safe_name = name[:31]
                df.to_excel(writer, sheet_name=safe_name, index=False)
        return xlsx_path
    except Exception:
        return None


def write_summary_text(
    path: Path,
    files: dict[str, Optional[Path]],
    checkpoint_dir: Optional[Path],
    progress_rows: list[dict],
    top_rows: list[dict],
    copied_files: list[Path],
) -> None:
    run_manifest = {}
    manifest_path = files.get("run_manifest")
    if manifest_path and manifest_path.exists():
        try:
            run_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            run_manifest = {}

    lines = [
        "V15 Core-Aware Multitask ANN Presentation Review",
        "=" * 56,
        f"Created: {datetime.now().isoformat(timespec='seconds')}",
        f"Output folder: {OUTPUT_DIR}",
        f"Run slug: {RUN_SLUG}",
        f"Review folder: {REVIEW_DIR}",
        "",
        "What to use for the presentation:",
        "- paper_figures PDF: compact figure deck generated by the notebook",
        "- clean_summary workbook: row-free summary tables",
        "- v15_review_tables workbook/CSVs: run progress, WLC summary, core-aware metrics",
        "- figure manifest: tells which V15/core-proxy figures exist and what each means",
        "",
        "Important boundary:",
        "This review packet intentionally excludes row-level prediction CSVs and fitted model files.",
        "",
        "Run manifest highlights:",
    ]
    for key in ["code_version", "run_id", "output_dir", "model_dir", "input_dir"]:
        if key in run_manifest:
            lines.append(f"- {key}: {run_manifest[key]}")
    if not run_manifest:
        lines.append("- run_manifest JSON was not readable or not present.")

    lines += [
        "",
        "Key files found:",
    ]
    for label, source in files.items():
        if source and source.exists():
            lines.append(f"- {label}: {source.name}")
        else:
            lines.append(f"- {label}: MISSING")

    lines += [
        "",
        "Chong ANN checkpoint status:",
        f"- checkpoint folder: {checkpoint_dir if checkpoint_dir else 'MISSING'}",
        f"- WLC metric files found: {len(progress_rows)}",
        f"- top WLC rows extracted: {len(top_rows)}",
    ]
    if progress_rows:
        metric_counts = [int(r.get("metric_rows", 0) or 0) for r in progress_rows]
        lines.append(f"- metric rows per WLC: min={min(metric_counts)}, max={max(metric_counts)}")

    lines += [
        "",
        "Files copied into the review folder:",
    ]
    for copied in copied_files:
        lines.append(f"- {copied.name}")

    lines += [
        "",
        "For Codex review, send or upload:",
        f"- {REVIEW_DIR / ('v15_review_packet_' + RUN_SLUG + '_' + TIMESTAMP + '.zip')}",
        f"- {path}",
        "",
        "If the Outlook draft does not appear, check Outlook Drafts and Alt+Tab.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def open_outlook_draft(attachments: list[Path]) -> None:
    if os.environ.get("V15_NO_EMAIL", "").strip() == "1":
        print("V15_NO_EMAIL=1, skipping Outlook draft.")
        return

    recipient = os.environ.get("PERSONAL_REVIEW_EMAIL", "").strip()
    if not recipient:
        recipient = input("Personal review email for Outlook draft: ").strip()
    if not recipient:
        print("No recipient provided; review packet was created but email draft was skipped.")
        return

    attachment_array = ", ".join(ps_quote(p) for p in attachments if p.exists())
    script_path = REVIEW_DIR / f"open_outlook_draft_{RUN_SLUG}_{TIMESTAMP}.ps1"
    script_text = f"""$ErrorActionPreference = "Stop"
$to = {ps_quote(recipient)}
$attachments = @({attachment_array})
$outlook = New-Object -ComObject Outlook.Application
$mail = $outlook.CreateItem(0)
$mail.To = $to
$mail.Subject = "North Slope ML V15 presentation review packet"
$mail.Body = @"
Attached is the compact V15 presentation-review packet.

It includes row-free summaries, checkpoint progress, top WLC/core-aware review tables, the clean summary workbook, and the paper figures PDF when present.

Please review before sending outside the DOE environment.
"@
foreach ($packetPath in $attachments) {{
    if (Test-Path -LiteralPath $packetPath) {{
        $mail.Attachments.Add($packetPath) | Out-Null
    }}
}}
$mail.Save()
$mail.Display()
try {{ $mail.GetInspector.Activate() }} catch {{}}
Write-Host "Saved and opened Outlook draft for $to"
Write-Host "Attached files:"
$attachments | ForEach-Object {{ Write-Host " - $_" }}
"""
    script_path.write_text(script_text, encoding="utf-8")
    subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(script_path),
        ],
        check=True,
    )


def main() -> None:
    if not OUTPUT_DIR.exists():
        raise FileNotFoundError(
            f"V15 output folder not found: {OUTPUT_DIR}. "
            "Set V15_OUTPUT_DIR or run the V15 notebook export cell first."
        )

    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    tables_dir = REVIEW_DIR / "tables"
    figures_dir = REVIEW_DIR / "figures"

    files = {
        "share_packet_zip": newest(f"share_packet_{RUN_SLUG}.zip") or newest("share_packet_*.zip"),
        "paper_figures_pdf": newest(f"paper_figures_{RUN_SLUG}.pdf") or newest("paper_figures_*.pdf"),
        "clean_summary_xlsx": newest(f"clean_summary_{RUN_SLUG}.xlsx") or newest("clean_summary_*.xlsx"),
        "share_packet_readme": newest(f"share_packet_readme_{RUN_SLUG}.txt") or newest("share_packet_readme_*.txt"),
        "run_manifest": newest(f"run_manifest_{RUN_SLUG}.json") or newest("run_manifest_*.json"),
        "active_well_policy": newest(f"active_well_policy_{RUN_SLUG}.csv") or newest("active_well_policy_*.csv"),
        "header_contract_summary": newest(f"header_contract_summary_{RUN_SLUG}.csv") or newest("header_contract_summary_*.csv"),
        "density_porosity_policy": newest(f"density_porosity_policy_summary_{RUN_SLUG}.csv") or newest("density_porosity_policy_summary_*.csv"),
        "feature_policy_summary": newest(f"feature_policy_summary_{RUN_SLUG}.csv") or newest("feature_policy_summary_*.csv"),
        "chong_core_feature_presence": newest(f"chong_core_feature_presence_by_well_{RUN_SLUG}.csv") or newest("chong_core_feature_presence_by_well_*.csv"),
        "v15_core_aux_metrics": newest(f"v15_core_auxiliary_model_metrics_{RUN_SLUG}.csv") or newest("v15_core_auxiliary_model_metrics_*.csv"),
        "v15_target_comparison": newest(f"v15_core_aware_target_comparison_{RUN_SLUG}.csv") or newest("v15_core_aware_target_comparison_*.csv"),
        "v15_figure_manifest": newest(f"v15_core_aware_figure_manifest_{RUN_SLUG}.csv") or newest("v15_core_aware_figure_manifest_*.csv"),
    }

    checkpoint_dir = newest_dir(f"chong_ann_checkpoints_{RUN_SLUG}_*")
    progress_rows, top_rows = checkpoint_progress(checkpoint_dir)

    available_rows = [file_row(path, label) for label, path in files.items()]
    write_rows_csv(tables_dir / "available_files.csv", available_rows)
    write_rows_csv(tables_dir / "chong_ann_checkpoint_progress.csv", progress_rows)
    write_rows_csv(tables_dir / "top_wlc_by_split.csv", top_rows)

    copied_files: list[Path] = []
    for label in [
        "paper_figures_pdf",
        "clean_summary_xlsx",
        "share_packet_readme",
        "run_manifest",
        "active_well_policy",
        "header_contract_summary",
        "density_porosity_policy",
        "feature_policy_summary",
        "chong_core_feature_presence",
        "v15_core_aux_metrics",
        "v15_target_comparison",
        "v15_figure_manifest",
    ]:
        copied = copy_if_present(files.get(label), REVIEW_DIR)
        if copied:
            copied_files.append(copied)

    copied_figures = copy_figures_from_manifest(files.get("v15_figure_manifest"), figures_dir)
    copied_files.extend(copied_figures)

    tables = {
        "available_files": available_rows,
        "checkpoint_progress": progress_rows,
        "top_wlc_by_split": top_rows,
        "core_aux_metrics": sort_preview(
            read_csv_preview(files.get("v15_core_aux_metrics"), 30),
            preferred_desc=["r2_mean", "r2", "score_mean"],
            preferred_asc=["rmse_mean", "mae_mean"],
        ),
        "target_comparison": read_csv_preview(files.get("v15_target_comparison"), 40),
        "figure_manifest": read_csv_preview(files.get("v15_figure_manifest"), 80),
        "feature_policy": read_csv_preview(files.get("feature_policy_summary"), 80),
        "density_porosity": read_csv_preview(files.get("density_porosity_policy"), 80),
        "core_feature_presence": read_csv_preview(files.get("chong_core_feature_presence"), 80),
    }
    review_xlsx = write_excel(tables, REVIEW_DIR / f"v15_review_tables_{RUN_SLUG}_{TIMESTAMP}.xlsx")
    if review_xlsx:
        copied_files.append(review_xlsx)
    else:
        for name, table in tables.items():
            if table is None:
                continue
            if pd is not None and hasattr(table, "to_csv"):
                table.to_csv(tables_dir / f"{name}.csv", index=False)

    summary_txt = REVIEW_DIR / f"v15_review_summary_{RUN_SLUG}_{TIMESTAMP}.txt"
    write_summary_text(summary_txt, files, checkpoint_dir, progress_rows, top_rows, copied_files)
    copied_files.append(summary_txt)

    packet_zip = REVIEW_DIR / f"v15_review_packet_{RUN_SLUG}_{TIMESTAMP}.zip"
    with zipfile.ZipFile(packet_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(REVIEW_DIR.rglob("*")):
            if path.is_file() and path != packet_zip and is_safe_review_file(path):
                zf.write(path, arcname=str(path.relative_to(REVIEW_DIR)))

    email_attachments = [packet_zip, summary_txt]
    for key in ["paper_figures_pdf", "clean_summary_xlsx"]:
        copied = REVIEW_DIR / files[key].name if files.get(key) else None
        if copied and copied.exists():
            email_attachments.append(copied)

    print("\nV15 PRESENTATION REVIEW PACKET CREATED")
    print("=" * 44)
    print("Review folder:", REVIEW_DIR)
    print("Review packet zip:", packet_zip)
    print("Summary for Codex:", summary_txt)
    if review_xlsx:
        print("Review tables workbook:", review_xlsx)
    print("Checkpoint WLC metric files:", len(progress_rows))
    print("Top WLC rows:", len(top_rows))
    print("\nSEND THESE TO CODEX / USE FOR PRESENTATION REVIEW:")
    for item in email_attachments:
        print(" -", item)

    open_outlook_draft(email_attachments)


if __name__ == "__main__":
    main()
