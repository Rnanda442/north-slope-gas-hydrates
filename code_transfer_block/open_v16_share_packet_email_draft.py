"""
DOE/Jupyter helper: copy the latest V16 outputs into a new review folder and
open a saved Outlook draft.

Use this after the V16 notebook export cell has printed "DONE - files written".
It does not send email. It creates a fresh folder like:

    ~/Downloads/Northslopedatasets06052026/V16_output_review_<run_id_or_time>/

Then it copies row-free review artifacts there and opens an Outlook draft with
the compact share packet attached.

Paste this whole file into a Jupyter cell, or run from Anaconda Prompt:

    python code_transfer_block\\open_v16_share_packet_email_draft.py

Optional environment variables:

    PERSONAL_REVIEW_EMAIL   recipient for the draft
    V16_OUTPUT_DIR          defaults to ~/Downloads/outputs_runtime/ml_master
    V16_RUN_SLUG            defaults to v16_core_aware_final_focus_ann
    V16_REVIEW_ROOT         defaults to ~/Downloads/Northslopedatasets06052026
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


RUN_SLUG = os.environ.get("V16_RUN_SLUG", "v16_core_aware_final_focus_ann")
OUTPUT_DIR = Path(
    os.environ.get(
        "V16_OUTPUT_DIR",
        Path.home() / "Downloads" / "outputs_runtime" / "ml_master",
    )
)
REVIEW_ROOT = Path(
    os.environ.get(
        "V16_REVIEW_ROOT",
        Path.home() / "Downloads" / "Northslopedatasets06052026",
    )
)


def newest(pattern: str) -> Path | None:
    candidates = [p for p in OUTPUT_DIR.glob(pattern) if p.is_file()]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def ps_quote(value: str | Path) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def read_manifest(path: Path | None) -> dict:
    if not path or not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def unique_review_dir(run_id: str) -> Path:
    label = run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
    base = REVIEW_ROOT / f"V16_output_review_{label}"
    if not base.exists():
        return base
    for i in range(2, 100):
        candidate = REVIEW_ROOT / f"V16_output_review_{label}_{i}"
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Could not create a unique review folder under {REVIEW_ROOT}")


def copy_if_present(path: Path | None, destination: Path, copied: list[Path]) -> None:
    if not path or not path.exists() or not path.is_file():
        return
    out = destination / path.name
    shutil.copy2(path, out)
    copied.append(out)


def manifest_path(value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(value)
    return path if path.exists() else None


def main() -> None:
    if not OUTPUT_DIR.exists():
        raise FileNotFoundError(f"V16 output folder not found: {OUTPUT_DIR}")

    share_zip = newest(f"share_packet_{RUN_SLUG}.zip") or newest("share_packet_v16*.zip")
    manifest_json = newest(f"run_manifest_{RUN_SLUG}.json") or newest("run_manifest_v16*.json")
    manifest = read_manifest(manifest_json)
    run_id = str(manifest.get("run_id") or "")
    review_dir = unique_review_dir(run_id)
    review_dir.mkdir(parents=True, exist_ok=False)

    copied: list[Path] = []
    core_files = [
        share_zip,
        manifest_json,
        newest(f"clean_summary_{RUN_SLUG}.xlsx"),
        newest(f"share_packet_readme_{RUN_SLUG}.txt"),
        newest(f"paper_figures_{RUN_SLUG}.pdf"),
        newest(f"draft_share_packet_email_{RUN_SLUG}.ps1"),
    ]
    for item in core_files:
        copy_if_present(item, review_dir, copied)

    manifest_keys_to_copy = [
        "active_well_policy_csv",
        "header_contract_summary_csv",
        "density_porosity_policy_csv",
        "chong_core_feature_presence_csv",
        "feature_policy_summary_csv",
        "model_selection_audit_csv",
        "stability_join_audit_csv",
        "saturation_detection_metrics_csv",
        "chong_ann_wlc_summary_csv",
        "chong_ann_realization_metrics_csv",
        "core_target_fill_audit_csv",
        "pass7_core_context_match_summary_csv",
        "pass7_core_context_measurement_profile_csv",
        "pass7_core_proxy_score_csv",
        "pass7_core_proxy_figure_manifest_csv",
        "v15_core_auxiliary_model_metrics_csv",
        "v15_core_aware_target_comparison_csv",
        "v15_core_aware_multitask_metrics_csv",
        "v15_core_aware_figure_manifest_csv",
        "v15_core_usage_audit_csv",
    ]
    for key in manifest_keys_to_copy:
        copy_if_present(manifest_path(manifest.get(key)), review_dir, copied)

    local_readme = review_dir / "V16_REVIEW_FOLDER_README.txt"
    local_readme.write_text(
        "\n".join(
            [
                "V16 North Slope Gas Hydrate ML review folder",
                f"Created: {datetime.now().isoformat(timespec='seconds')}",
                f"Run slug: {RUN_SLUG}",
                f"Run ID: {run_id or 'not found in manifest'}",
                f"Source output folder: {OUTPUT_DIR}",
                "",
                "Boundary:",
                "This folder is for local DOE/runtime review. Do not move row-level predictions,",
                "approved rows, fitted models, runtime logs, or private identifiers into GitHub.",
                "",
                "Copied artifacts:",
                *[f"- {p.name}" for p in copied],
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    copied.append(local_readme)

    if share_zip is None:
        raise FileNotFoundError(
            f"No V16 share packet found in {OUTPUT_DIR}. "
            "Run the V16 notebook final export cell first."
        )

    recipient = os.environ.get("PERSONAL_REVIEW_EMAIL", "").strip()
    if not recipient:
        recipient = input("Personal review email for Outlook draft: ").strip()
    if not recipient:
        raise SystemExit("No recipient provided; set PERSONAL_REVIEW_EMAIL or enter it when prompted.")

    attachments = []
    for name in [
        f"share_packet_{RUN_SLUG}.zip",
        f"clean_summary_{RUN_SLUG}.xlsx",
        f"paper_figures_{RUN_SLUG}.pdf",
        "V16_REVIEW_FOLDER_README.txt",
    ]:
        item = review_dir / name
        if item.exists():
            attachments.append(item)

    attachment_array = ", ".join(ps_quote(p) for p in attachments)
    script_path = review_dir / f"open_outlook_draft_{RUN_SLUG}.ps1"
    script_text = f"""$ErrorActionPreference = "Stop"
$to = {ps_quote(recipient)}
$attachments = @({attachment_array})
$outlook = New-Object -ComObject Outlook.Application
$mail = $outlook.CreateItem(0)
$mail.To = $to
$mail.Subject = "North Slope ML V16 review packet"
$mail.Body = @"
Attached is the compact V16 review packet. The copied review folder is:

{review_dir}

This packet is intended for review only. Please check the data boundary before
sending outside the DOE environment.
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
Write-Host "Review folder: {review_dir}"
Write-Host "Attached files:"
$attachments | ForEach-Object {{ Write-Host " - $_" }}
"""
    script_path.write_text(script_text, encoding="utf-8")

    print("Created V16 review folder:", review_dir)
    print("Copied files:")
    for item in copied:
        print(" -", item)
    print("Running Outlook draft helper:", script_path)
    print("Attachments:")
    for attachment in attachments:
        print(" -", attachment)

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


if __name__ == "__main__":
    main()
