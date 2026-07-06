# COPY THIS WHOLE FILE INTO ONE NEW CELL AFTER THE V15 NOTEBOOK FINISHES.
#
# It rebuilds a local folder named "Code output" with the V15 files needed for
# Codex/presentation review. If Google Drive for Desktop exposes a synced
# "Code output" folder, it replaces that synced folder too.
#
# By default, it excludes row-level prediction CSVs, row-reliability tables,
# old share-packet ZIPs, and fitted model files. Those files are listed in
# excluded_private_outputs_manifest.csv so you can see what was left out.

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
DRIVE_FOLDER_NAME = str(globals().get("DRIVE_FOLDER_NAME", os.environ.get("V15_DRIVE_FOLDER_NAME", "Code output")))
CODE_OUTPUT_DIR = Path(
    globals().get(
        "CODE_OUTPUT_DIR",
        os.environ.get("V15_CODE_OUTPUT_DIR", OUTPUT_DIR / DRIVE_FOLDER_NAME),
    )
).expanduser()

# Keep this False unless an approved policy says row-level outputs may leave the
# DOE runtime. The generated manifest still records excluded files by name/size.
INCLUDE_PRIVATE_ROW_OUTPUTS = str(
    globals().get("INCLUDE_PRIVATE_ROW_OUTPUTS", os.environ.get("V15_INCLUDE_PRIVATE_ROW_OUTPUTS", "0"))
).strip().lower() in {"1", "true", "yes", "y"}

MIRROR_TO_GOOGLE_DRIVE_DESKTOP = str(
    globals().get("MIRROR_TO_GOOGLE_DRIVE_DESKTOP", os.environ.get("V15_MIRROR_TO_GOOGLE_DRIVE_DESKTOP", "1"))
).strip().lower() not in {"0", "false", "no", "n"}

PRIVATE_TOKENS = (
    "prediction",
    "predictions",
    "row_reliability",
    "selected_models",
)
MODEL_SUFFIXES = {".joblib", ".pkl", ".pickle", ".pt", ".pth", ".onnx"}


def newest(pattern):
    candidates = [p for p in OUTPUT_DIR.glob(pattern) if p.is_file()]
    return max(candidates, key=lambda p: p.stat().st_mtime) if candidates else None


def newest_dir(pattern):
    candidates = [p for p in OUTPUT_DIR.glob(pattern) if p.is_dir()]
    return max(candidates, key=lambda p: p.stat().st_mtime) if candidates else None


def rel_to_output(path):
    try:
        return str(path.relative_to(OUTPUT_DIR))
    except Exception:
        return str(path)


def ps_quote(value):
    return "'" + str(value).replace("'", "''") + "'"


def path_size(path):
    if not path.exists():
        return 0
    if path.is_file():
        return path.stat().st_size
    total = 0
    for child in path.rglob("*"):
        if child.is_file():
            try:
                total += child.stat().st_size
            except OSError:
                pass
    return total


def write_csv(path, rows, fieldnames=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    if fieldnames is None:
        seen = []
        for row in rows:
            for key in row.keys():
                if key not in seen:
                    seen.append(key)
        fieldnames = seen
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path, limit=None):
    if not path or not path.exists():
        return []
    try:
        with path.open("r", newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
    except Exception:
        return []
    return rows[:limit] if limit else rows


def private_reason(path):
    name = path.name.lower()
    suffix = path.suffix.lower()
    if path == CODE_OUTPUT_DIR or name == DRIVE_FOLDER_NAME.lower():
        return "generated Code output folder"
    if name.startswith("code_output_") and suffix == ".zip":
        return "generated Code output ZIP"
    if name.startswith("share_packet_") and suffix == ".zip":
        return "old share-packet ZIP skipped; fresh Code output ZIP is created"
    if suffix in MODEL_SUFFIXES:
        return "fitted model or model-binary file"
    for token in PRIVATE_TOKENS:
        if token in name:
            return "row-level prediction/reliability output"
    return ""


def should_copy(path):
    reason = private_reason(path)
    return INCLUDE_PRIVATE_ROW_OUTPUTS or not reason


def safe_replace_dir(path):
    path = path.resolve()
    if str(path) in {"", str(path.anchor)}:
        raise ValueError(f"Refusing to replace unsafe directory: {path}")
    path.mkdir(parents=True, exist_ok=True)
    for child in list(path.iterdir()):
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def copy_file(src, dest, copied_rows):
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    copied_rows.append(
        {
            "source": str(src),
            "destination": str(dest),
            "relative_source": rel_to_output(src),
            "size_bytes": src.stat().st_size,
        }
    )


def copy_tree_filtered(src_dir, dest_dir, copied_rows, excluded_rows):
    for src in sorted(src_dir.rglob("*")):
        if not src.is_file():
            continue
        reason = private_reason(src)
        if reason and not INCLUDE_PRIVATE_ROW_OUTPUTS:
            excluded_rows.append(
                {
                    "path": str(src),
                    "relative_path": rel_to_output(src),
                    "size_bytes": src.stat().st_size,
                    "reason": reason,
                }
            )
            continue
        dest = dest_dir / src.relative_to(src_dir)
        copy_file(src, dest, copied_rows)


def find_checkpoint_dir():
    if globals().get("CHONG_ANN_CHECKPOINT_DIR"):
        candidate = Path(globals()["CHONG_ANN_CHECKPOINT_DIR"]).expanduser()
        if candidate.exists():
            return candidate
    return newest_dir(f"chong_ann_checkpoints_{RUN_SLUG}_*")


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
                "file_path": str(metrics_path),
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

            def as_float(value):
                try:
                    return float(value)
                except Exception:
                    return None

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


def copy_figures_from_manifest(manifest_path, dest_dir, copied_rows, excluded_rows):
    rows = read_csv_rows(manifest_path)
    if not rows:
        return
    path_columns = [
        col
        for col in rows[0].keys()
        if col.lower() in {"path", "file", "filepath", "figure_path", "figure_file"}
    ]
    for row in rows:
        for col in path_columns:
            raw = (row.get(col) or "").strip()
            if not raw:
                continue
            candidate = Path(raw)
            if not candidate.is_absolute():
                candidate = OUTPUT_DIR / candidate
            if not candidate.exists() or not candidate.is_file():
                continue
            reason = private_reason(candidate)
            if reason and not INCLUDE_PRIVATE_ROW_OUTPUTS:
                excluded_rows.append(
                    {
                        "path": str(candidate),
                        "relative_path": rel_to_output(candidate),
                        "size_bytes": candidate.stat().st_size,
                        "reason": reason,
                    }
                )
                continue
            copy_file(candidate, dest_dir / candidate.name, copied_rows)


def file_status_row(label, path):
    if not path or not path.exists():
        return {
            "label": label,
            "exists": False,
            "path": "",
            "relative_path": "",
            "size_bytes": "",
            "modified": "",
        }
    stat = path.stat()
    return {
        "label": label,
        "exists": True,
        "path": str(path),
        "relative_path": rel_to_output(path),
        "size_bytes": stat.st_size if path.is_file() else path_size(path),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
    }


def find_drive_desktop_code_output():
    explicit = str(
        globals().get(
            "DRIVE_SYNC_CODE_OUTPUT_DIR",
            os.environ.get("V15_DRIVE_SYNC_CODE_OUTPUT_DIR", ""),
        )
    ).strip()
    if explicit:
        return Path(explicit).expanduser()

    candidates = [
        Path.home() / "Google Drive" / "My Drive" / DRIVE_FOLDER_NAME,
        Path.home() / "My Drive" / DRIVE_FOLDER_NAME,
    ]
    if os.name == "nt":
        for letter in "DEFGHIJKLMNOPQRSTUVWXYZ":
            candidates.append(Path(f"{letter}:\\My Drive") / DRIVE_FOLDER_NAME)
            candidates.append(Path(f"{letter}:\\Google Drive\\My Drive") / DRIVE_FOLDER_NAME)

    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            return candidate
    return None


def mirror_to_drive_desktop(source_dir):
    if not MIRROR_TO_GOOGLE_DRIVE_DESKTOP:
        return ""
    target = find_drive_desktop_code_output()
    if not target:
        return ""
    if target.name.lower() != DRIVE_FOLDER_NAME.lower():
        raise ValueError(f"Refusing to replace a Drive folder not named {DRIVE_FOLDER_NAME!r}: {target}")
    safe_replace_dir(target)
    for child in source_dir.iterdir():
        dest = target / child.name
        if child.is_dir():
            shutil.copytree(child, dest)
        else:
            shutil.copy2(child, dest)
    return str(target)


def zip_folder(source_dir, zip_path):
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                zf.write(path, arcname=str(Path(DRIVE_FOLDER_NAME) / path.relative_to(source_dir)))


def write_start_here(path, files, checkpoint_dir, progress_rows, top_wlc_rows, excluded_rows, drive_mirror_path, zip_path):
    run_manifest = {}
    manifest_path = files.get("run_manifest")
    if manifest_path and manifest_path.exists():
        try:
            run_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            run_manifest = {}

    metric_counts = [int(r.get("metric_rows", 0) or 0) for r in progress_rows]
    lines = [
        "V15 CODE OUTPUT FOLDER - START HERE",
        "=" * 38,
        f"Created: {datetime.now().isoformat(timespec='seconds')}",
        f"Run slug: {RUN_SLUG}",
        f"Notebook output folder: {OUTPUT_DIR}",
        f"Local Code output folder: {CODE_OUTPUT_DIR}",
        f"Code output ZIP: {zip_path}",
        f"Google Drive Desktop mirror: {drive_mirror_path or 'not detected'}",
        "",
        "Best files for Codex/presentation review:",
        "- 01_review_ready_files/paper_figures_*.pdf",
        "- 01_review_ready_files/clean_summary_*.xlsx",
        "- 02_generated_review_tables/chong_ann_checkpoint_progress.csv",
        "- 02_generated_review_tables/top_wlc_by_split.csv",
        "- 02_generated_review_tables/available_files_manifest.csv",
        "- 02_generated_review_tables/excluded_private_outputs_manifest.csv",
        "- 04_runtime_output_folders/chong_ann_checkpoints_* when present",
        "",
        "What this folder intentionally does:",
        "- replaces/rebuilds the local Code output folder each time this cell runs",
        "- includes figures, summary workbooks, manifests, policy tables, WLC summaries, and checkpoint tables",
        "- excludes row-level predictions and fitted model files by default",
        "",
        "Run manifest highlights:",
    ]
    if run_manifest:
        for key in ["code_version", "run_id", "output_dir", "model_dir", "input_dir"]:
            if key in run_manifest:
                lines.append(f"- {key}: {run_manifest[key]}")
    else:
        lines.append("- run_manifest JSON was missing or unreadable")

    lines += [
        "",
        "ANN checkpoint status:",
        f"- checkpoint folder: {checkpoint_dir if checkpoint_dir else 'MISSING'}",
        f"- WLC metric files found: {len(progress_rows)}",
        f"- top WLC rows extracted: {len(top_wlc_rows)}",
    ]
    if metric_counts:
        lines.append(f"- metric rows per WLC: min={min(metric_counts)}, max={max(metric_counts)}")

    lines += [
        "",
        "Key file status:",
    ]
    for label, source in files.items():
        lines.append(f"- {label}: {'FOUND' if source and source.exists() else 'MISSING'} {source or ''}")

    lines += [
        "",
        f"Private/excluded output count: {len(excluded_rows)}",
        "See 02_generated_review_tables/excluded_private_outputs_manifest.csv for details.",
        "",
        "If Google Drive Desktop was not detected, upload the Code output ZIP or the local Code output folder to your Drive folder named Code output.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def open_outlook_draft(attachments):
    if os.environ.get("V15_NO_EMAIL", "").strip() == "1":
        print("V15_NO_EMAIL=1, skipping Outlook draft.")
        return None

    recipient = str(globals().get("PERSONAL_REVIEW_EMAIL", os.environ.get("PERSONAL_REVIEW_EMAIL", ""))).strip()
    if not recipient:
        recipient = input("Gmail/Drive email for Outlook draft, or press Enter to skip: ").strip()
    if not recipient:
        print("No email entered, so Outlook draft was skipped.")
        return None

    script_path = CODE_OUTPUT_DIR / f"open_outlook_draft_{RUN_SLUG}_{TIMESTAMP}.ps1"
    attachment_array = ", ".join(ps_quote(p) for p in attachments if p and Path(p).exists())
    script_path.write_text(
        f'''$ErrorActionPreference = "Stop"
$to = {ps_quote(recipient)}
$attachments = @({attachment_array})
$outlook = New-Object -ComObject Outlook.Application
$mail = $outlook.CreateItem(0)
$mail.To = $to
$mail.Subject = "North Slope ML V15 Code output packet"
$mail.Body = @"
Attached is the V15 Code output packet for review.

It includes the review ZIP, start-here summary, figure PDF, clean summary workbook, checkpoint progress, WLC tables, and V15 review manifests. Row-level prediction outputs are excluded unless explicitly enabled in the notebook cell.

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
        if os.environ.get("V15_WAIT_FOR_OUTLOOK", "").strip() == "1":
            subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script_path)],
                check=True,
            )
        else:
            subprocess.Popen(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        print("Outlook draft helper launched:", script_path)
    except Exception as exc:
        print("Could not launch Outlook draft helper:", exc)
        print("The Code output folder and ZIP were still created.")
    return script_path


if not OUTPUT_DIR.exists():
    raise FileNotFoundError(f"V15 output folder not found: {OUTPUT_DIR}")

safe_replace_dir(CODE_OUTPUT_DIR)

review_ready_dir = CODE_OUTPUT_DIR / "01_review_ready_files"
tables_dir = CODE_OUTPUT_DIR / "02_generated_review_tables"
figures_dir = CODE_OUTPUT_DIR / "03_figures_from_manifest"
output_files_dir = CODE_OUTPUT_DIR / "04_runtime_output_files"
output_folders_dir = CODE_OUTPUT_DIR / "05_runtime_output_folders"

files = {
    "paper_figures_pdf": newest(f"paper_figures_{RUN_SLUG}.pdf") or newest("paper_figures_*.pdf"),
    "clean_summary_xlsx": newest(f"clean_summary_{RUN_SLUG}.xlsx") or newest("clean_summary_*.xlsx"),
    "model_results_xlsx": newest(f"model_results_{RUN_SLUG}.xlsx") or newest("model_results_*.xlsx"),
    "chong_ann_results_xlsx": newest(f"chong_ann_results_{RUN_SLUG}.xlsx") or newest("chong_ann_results_*.xlsx"),
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
    "v15_multitask_metrics": newest(f"v15_core_aware_multitask_metrics_{RUN_SLUG}.csv") or newest("v15_core_aware_multitask_metrics_*.csv"),
}

checkpoint_dir = find_checkpoint_dir()
progress_rows, top_wlc_rows = checkpoint_review(checkpoint_dir)

copied_rows = []
excluded_rows = []
copied_sources = set()

for label, source in files.items():
    if not source or not source.exists():
        continue
    reason = private_reason(source)
    if reason and not INCLUDE_PRIVATE_ROW_OUTPUTS:
        excluded_rows.append(
            {
                "path": str(source),
                "relative_path": rel_to_output(source),
                "size_bytes": source.stat().st_size,
                "reason": reason,
            }
        )
        continue
    copy_file(source, review_ready_dir / source.name, copied_rows)
    copied_sources.add(str(source.resolve()))

available_rows = [file_status_row(label, path) for label, path in files.items()]
write_csv(tables_dir / "available_files_manifest.csv", available_rows)
write_csv(tables_dir / "chong_ann_checkpoint_progress.csv", progress_rows)
write_csv(tables_dir / "top_wlc_by_split.csv", top_wlc_rows)

for name, source in [
    ("core_aux_metrics_preview.csv", files["v15_core_aux_metrics"]),
    ("target_comparison_preview.csv", files["v15_target_comparison"]),
    ("figure_manifest_preview.csv", files["v15_figure_manifest"]),
    ("feature_policy_preview.csv", files["feature_policy_summary"]),
    ("density_porosity_policy_preview.csv", files["density_porosity_policy"]),
    ("chong_ann_wlc_summary_preview.csv", files["chong_ann_wlc_summary"]),
    ("chong_ann_realization_metrics_preview.csv", files["chong_ann_realization_metrics"]),
]:
    rows = read_csv_rows(source, limit=200)
    if rows:
        write_csv(tables_dir / name, rows)

copy_figures_from_manifest(files["v15_figure_manifest"], figures_dir, copied_rows, excluded_rows)

for src in sorted(OUTPUT_DIR.iterdir()):
    try:
        resolved = str(src.resolve())
    except Exception:
        resolved = str(src)
    if resolved in copied_sources:
        continue
    if src == CODE_OUTPUT_DIR or src.name == DRIVE_FOLDER_NAME:
        continue
    if src.name.startswith("v15_presentation_review_"):
        continue
    if src.name.startswith("Code_output_") and src.suffix.lower() == ".zip":
        continue

    reason = private_reason(src)
    if reason and not INCLUDE_PRIVATE_ROW_OUTPUTS:
        excluded_rows.append(
            {
                "path": str(src),
                "relative_path": rel_to_output(src),
                "size_bytes": path_size(src),
                "reason": reason,
            }
        )
        continue

    if src.is_file():
        copy_file(src, output_files_dir / src.name, copied_rows)
    elif src.is_dir() and (RUN_SLUG in src.name or src.name.startswith("chong_ann_checkpoints_") or src.name.startswith("v15_core_aware_figures_")):
        copy_tree_filtered(src, output_folders_dir / src.name, copied_rows, excluded_rows)

write_csv(tables_dir / "copied_files_manifest.csv", copied_rows)
write_csv(tables_dir / "excluded_private_outputs_manifest.csv", excluded_rows)

code_output_zip = OUTPUT_DIR / f"Code_output_{RUN_SLUG}_{TIMESTAMP}.zip"
start_here_txt = CODE_OUTPUT_DIR / "00_START_HERE.txt"

write_start_here(
    start_here_txt,
    files,
    checkpoint_dir,
    progress_rows,
    top_wlc_rows,
    excluded_rows,
    "",
    code_output_zip,
)
drive_mirror_path = mirror_to_drive_desktop(CODE_OUTPUT_DIR)
write_start_here(
    start_here_txt,
    files,
    checkpoint_dir,
    progress_rows,
    top_wlc_rows,
    excluded_rows,
    drive_mirror_path,
    code_output_zip,
)
if drive_mirror_path:
    shutil.copy2(start_here_txt, Path(drive_mirror_path) / start_here_txt.name)
zip_folder(CODE_OUTPUT_DIR, code_output_zip)
shutil.copy2(code_output_zip, CODE_OUTPUT_DIR / code_output_zip.name)
if drive_mirror_path:
    shutil.copy2(code_output_zip, Path(drive_mirror_path) / code_output_zip.name)

email_attachments = [code_output_zip, start_here_txt]
for key in ["paper_figures_pdf", "clean_summary_xlsx"]:
    src = files[key]
    if src and (review_ready_dir / src.name).exists():
        email_attachments.append(review_ready_dir / src.name)
open_outlook_draft(email_attachments)

print("\nV15 CODE OUTPUT FOLDER READY")
print("=" * 35)
print("Local Code output folder:", CODE_OUTPUT_DIR)
print("Code output ZIP:", code_output_zip)
print("Google Drive Desktop mirror:", drive_mirror_path or "not detected")
print("Copied file count:", len(copied_rows))
print("Excluded private/output file count:", len(excluded_rows))
print("Checkpoint WLC metric files:", len(progress_rows))
print("Top WLC rows:", len(top_wlc_rows))
print("\nUPLOAD/REPLACE IN GOOGLE DRIVE:")
print(" - Upload this ZIP or folder to Drive folder named 'Code output':", code_output_zip)
print(" - If Google Drive Desktop mirror is not detected, replace the Drive folder manually in the browser.")
print("\nBEST FILES FOR CODEX REVIEW:")
print(" -", start_here_txt)
print(" -", tables_dir / "available_files_manifest.csv")
print(" -", tables_dir / "chong_ann_checkpoint_progress.csv")
print(" -", tables_dir / "top_wlc_by_split.csv")
print(" -", tables_dir / "excluded_private_outputs_manifest.csv")

V15_CODE_OUTPUT_DIR = CODE_OUTPUT_DIR
V15_CODE_OUTPUT_ZIP = code_output_zip
V15_CODE_OUTPUT_START_HERE = start_here_txt
