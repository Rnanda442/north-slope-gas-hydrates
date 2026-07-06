# COPY THIS WHOLE FILE INTO ONE NEW CELL AFTER THE V15 NOTEBOOK FINISHES.
#
# It creates a compact V15 presentation-review packet and opens/saves an
# Outlook draft with that packet attached. It does not require a terminal.
# It does not package row-level prediction CSVs or fitted model files.

import csv
import json
import os
import shutil
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path


RUN_SLUG = str(globals().get("RUN_SLUG", os.environ.get("V15_RUN_SLUG", "v15_core_aware_multitask_ann")))
OUTPUT_DIR = Path(
    globals().get(
        "OUTPUT_DIR",
        os.environ.get(
            "V15_OUTPUT_DIR",
            Path.home() / "Downloads" / "outputs_runtime" / "ml_master",
        ),
    )
).expanduser()
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
REVIEW_DIR = OUTPUT_DIR / f"v15_presentation_review_{RUN_SLUG}_{TIMESTAMP}"
ROW_LEVEL_OR_MODEL_TOKENS = (
    "prediction",
    "predictions",
    "selected_models",
    ".joblib",
    "row_reliability",
)

# This prompt appears inside the notebook cell output area in VS Code/Jupyter.
if os.environ.get("V15_NO_EMAIL", "").strip() == "1":
    PERSONAL_REVIEW_EMAIL = ""
else:
    PERSONAL_REVIEW_EMAIL = os.environ.get("PERSONAL_REVIEW_EMAIL", "").strip()
    if not PERSONAL_REVIEW_EMAIL:
        PERSONAL_REVIEW_EMAIL = input("Personal email for Outlook draft: ").strip()


def newest(pattern):
    candidates = [p for p in OUTPUT_DIR.glob(pattern) if p.is_file()]
    return max(candidates, key=lambda p: p.stat().st_mtime) if candidates else None


def newest_dir(pattern):
    candidates = [p for p in OUTPUT_DIR.glob(pattern) if p.is_dir()]
    return max(candidates, key=lambda p: p.stat().st_mtime) if candidates else None


def ps_quote(value):
    return "'" + str(value).replace("'", "''") + "'"


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path, limit=None):
    if not path or not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    return rows[:limit] if limit else rows


def file_info(label, path):
    if not path or not path.exists():
        return {
            "label": label,
            "exists": False,
            "path": "",
            "size_bytes": "",
            "modified": "",
        }
    stat = path.stat()
    return {
        "label": label,
        "exists": True,
        "path": str(path),
        "size_bytes": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
    }


def safe_copy(path, dest_dir):
    if not path or not path.exists():
        return None
    lower = path.name.lower()
    if lower.endswith(".zip"):
        return None
    if any(token in lower for token in ROW_LEVEL_OR_MODEL_TOKENS):
        return None
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / path.name
    shutil.copy2(path, dest)
    return dest


def copy_figures_from_manifest(manifest_path, dest_dir):
    copied = []
    rows = read_csv_rows(manifest_path)
    if not rows:
        return copied
    path_columns = [
        c
        for c in rows[0].keys()
        if c.lower() in {"path", "file", "filepath", "figure_path", "figure_file"}
    ]
    for row in rows:
        for col in path_columns:
            raw = (row.get(col) or "").strip()
            if not raw:
                continue
            candidate = Path(raw)
            if not candidate.is_absolute():
                candidate = OUTPUT_DIR / candidate
            if candidate.exists() and candidate.suffix.lower() in {".png", ".jpg", ".jpeg", ".pdf"}:
                copied_path = safe_copy(candidate, dest_dir)
                if copied_path:
                    copied.append(copied_path)
    return copied


def checkpoint_review(checkpoint_dir):
    progress = []
    top_rows = []
    if not checkpoint_dir or not checkpoint_dir.exists():
        return progress, top_rows

    for metrics_path in sorted(checkpoint_dir.glob("*__metrics.csv")):
        parts = metrics_path.stem.split("__")
        split_name = parts[0] if parts else ""
        wlc_name = parts[1] if len(parts) > 1 else metrics_path.stem
        rows = read_csv_rows(metrics_path)
        progress.append(
            {
                "split_name": split_name,
                "wlc_name": wlc_name,
                "metric_rows": len(rows),
                "file_name": metrics_path.name,
            }
        )

    summary_by_split = {}
    for summary_path in sorted(checkpoint_dir.glob("*__summary.csv")):
        rows = read_csv_rows(summary_path)
        if not rows:
            continue
        parts = summary_path.stem.split("__")
        inferred_split = parts[0] if parts else ""
        inferred_wlc = parts[1] if len(parts) > 1 else summary_path.stem
        for row in rows:
            row.setdefault("split_name", inferred_split)
            row.setdefault("wlc_name", inferred_wlc)
            split = row.get("split_name", inferred_split)
            current = summary_by_split.get(split)
            if current is None:
                summary_by_split[split] = row
                continue

            def as_float(value, default=None):
                try:
                    return float(value)
                except Exception:
                    return default

            row_r2 = as_float(row.get("r2_mean", row.get("r2")))
            cur_r2 = as_float(current.get("r2_mean", current.get("r2")))
            row_rmse = as_float(row.get("rmse_mean", row.get("rmse")))
            cur_rmse = as_float(current.get("rmse_mean", current.get("rmse")))
            if row_r2 is not None and (cur_r2 is None or row_r2 > cur_r2):
                summary_by_split[split] = row
            elif row_r2 is None and row_rmse is not None and (cur_rmse is None or row_rmse < cur_rmse):
                summary_by_split[split] = row

    for split, row in sorted(summary_by_split.items()):
        compact = {k: v for k, v in row.items() if not k.lower().startswith("unnamed")}
        compact["selected_for_split"] = split
        top_rows.append(compact)
    return progress, top_rows


if not OUTPUT_DIR.exists():
    raise FileNotFoundError(f"V15 output folder not found: {OUTPUT_DIR}")

REVIEW_DIR.mkdir(parents=True, exist_ok=True)
tables_dir = REVIEW_DIR / "tables"

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
    "chong_ann_wlc_summary": newest(f"chong_ann_wlc_summary_{RUN_SLUG}.csv") or newest("chong_ann_wlc_summary_*.csv"),
    "chong_ann_realization_metrics": newest(f"chong_ann_realization_metrics_{RUN_SLUG}.csv") or newest("chong_ann_realization_metrics_*.csv"),
    "v15_core_aux_metrics": newest(f"v15_core_auxiliary_model_metrics_{RUN_SLUG}.csv") or newest("v15_core_auxiliary_model_metrics_*.csv"),
    "v15_target_comparison": newest(f"v15_core_aware_target_comparison_{RUN_SLUG}.csv") or newest("v15_core_aware_target_comparison_*.csv"),
    "v15_figure_manifest": newest(f"v15_core_aware_figure_manifest_{RUN_SLUG}.csv") or newest("v15_core_aware_figure_manifest_*.csv"),
}

checkpoint_dir = None
if globals().get("CHONG_ANN_CHECKPOINT_DIR"):
    possible_checkpoint_dir = Path(globals()["CHONG_ANN_CHECKPOINT_DIR"]).expanduser()
    if possible_checkpoint_dir.exists():
        checkpoint_dir = possible_checkpoint_dir
if checkpoint_dir is None:
    checkpoint_dir = newest_dir(f"chong_ann_checkpoints_{RUN_SLUG}_*")
progress_rows, top_wlc_rows = checkpoint_review(checkpoint_dir)

available_rows = [file_info(label, path) for label, path in files.items()]
write_csv(tables_dir / "available_files.csv", available_rows)
write_csv(tables_dir / "chong_ann_checkpoint_progress.csv", progress_rows)
write_csv(tables_dir / "top_wlc_by_split.csv", top_wlc_rows)

copied = []
for label, path in files.items():
    if label == "share_packet_zip":
        continue
    copied_path = safe_copy(path, REVIEW_DIR)
    if copied_path:
        copied.append(copied_path)

for name, source in [
    ("core_aux_metrics_preview.csv", files["v15_core_aux_metrics"]),
    ("target_comparison_preview.csv", files["v15_target_comparison"]),
    ("figure_manifest_preview.csv", files["v15_figure_manifest"]),
    ("feature_policy_preview.csv", files["feature_policy_summary"]),
    ("density_porosity_policy_preview.csv", files["density_porosity_policy"]),
    ("chong_ann_wlc_summary_preview.csv", files["chong_ann_wlc_summary"]),
    ("chong_ann_realization_metrics_preview.csv", files["chong_ann_realization_metrics"]),
]:
    rows = read_csv_rows(source, limit=120)
    if rows:
        out = tables_dir / name
        write_csv(out, rows)
        copied.append(out)

figures_dir = REVIEW_DIR / "figures"
copied.extend(copy_figures_from_manifest(files["v15_figure_manifest"], figures_dir))

run_manifest = {}
if files["run_manifest"] and files["run_manifest"].exists():
    try:
        run_manifest = json.loads(files["run_manifest"].read_text(encoding="utf-8"))
    except Exception:
        run_manifest = {}

metric_counts = [int(r.get("metric_rows", 0) or 0) for r in progress_rows]
summary_txt = REVIEW_DIR / f"v15_review_summary_{RUN_SLUG}_{TIMESTAMP}.txt"
summary_lines = [
    "V15 PRESENTATION REVIEW SUMMARY",
    "=" * 32,
    f"Created: {datetime.now().isoformat(timespec='seconds')}",
    f"Output folder: {OUTPUT_DIR}",
    f"Review folder: {REVIEW_DIR}",
    f"Run slug: {RUN_SLUG}",
    "",
    "Use these for the presentation/review:",
    "- paper_figures PDF for quick figure review",
    "- clean_summary workbook for row-free summary tables",
    "- top_wlc_by_split.csv for which WLCs ran best by split",
    "- chong_ann_checkpoint_progress.csv for how much of the ANN suite completed",
    "- Chong ANN WLC summary and realization-metric previews when available",
    "- V15 core auxiliary and target comparison preview CSVs",
    "",
    "Run manifest highlights:",
]
if run_manifest:
    for key in ["code_version", "run_id", "output_dir", "model_dir", "input_dir"]:
        if key in run_manifest:
            summary_lines.append(f"- {key}: {run_manifest[key]}")
else:
    summary_lines.append("- run_manifest was missing or unreadable")

summary_lines += [
    "",
    "Key file status:",
]
for row in available_rows:
    summary_lines.append(f"- {row['label']}: {'FOUND' if row['exists'] else 'MISSING'} {row['path']}")

summary_lines += [
    "",
    "ANN checkpoint status:",
    f"- checkpoint folder: {checkpoint_dir if checkpoint_dir else 'MISSING'}",
    f"- WLC metric files found: {len(progress_rows)}",
    f"- top WLC rows extracted: {len(top_wlc_rows)}",
]
if metric_counts:
    summary_lines.append(f"- metric rows per WLC: min={min(metric_counts)}, max={max(metric_counts)}")

summary_lines += [
    "",
    "Boundary note:",
    "This packet intentionally excludes row-level prediction CSVs and fitted model files.",
]
summary_txt.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
copied.append(summary_txt)

packet_zip = REVIEW_DIR / f"v15_review_packet_{RUN_SLUG}_{TIMESTAMP}.zip"
with zipfile.ZipFile(packet_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for path in sorted(REVIEW_DIR.rglob("*")):
        if path.is_file() and path != packet_zip:
            zf.write(path, arcname=str(path.relative_to(REVIEW_DIR)))

email_attachments = [packet_zip, summary_txt]
for label in ["paper_figures_pdf", "clean_summary_xlsx"]:
    src = files[label]
    if src and (REVIEW_DIR / src.name).exists():
        email_attachments.append(REVIEW_DIR / src.name)

if PERSONAL_REVIEW_EMAIL:
    ps1 = REVIEW_DIR / f"open_outlook_draft_{RUN_SLUG}_{TIMESTAMP}.ps1"
    attachment_array = ", ".join(ps_quote(p) for p in email_attachments)
    ps1.write_text(
        f'''$ErrorActionPreference = "Stop"
$to = {ps_quote(PERSONAL_REVIEW_EMAIL)}
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
''',
        encoding="utf-8",
    )
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1)],
            check=True,
        )
    except Exception as exc:
        print("Outlook draft could not be opened automatically:", exc)
        print("The review packet was still created.")
        print("Draft PowerShell helper:", ps1)
else:
    print("No email entered, so Outlook draft was skipped. Review packet was still created.")

print("\nV15 PRESENTATION REVIEW PACKET CREATED")
print("=" * 44)
print("Review folder:", REVIEW_DIR)
print("Review packet zip:", packet_zip)
print("Summary for Codex:", summary_txt)
print("Checkpoint WLC metric files:", len(progress_rows))
print("Top WLC rows:", len(top_wlc_rows))
print("\nSEND THESE TO CODEX / USE FOR PRESENTATION REVIEW:")
for item in email_attachments:
    print(" -", item)

V15_REVIEW_DIR = REVIEW_DIR
V15_REVIEW_PACKET_ZIP = packet_zip
V15_REVIEW_SUMMARY_TXT = summary_txt
