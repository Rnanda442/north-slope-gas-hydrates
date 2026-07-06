"""
DOE/Jupyter helper: open a saved Outlook draft for the latest V15 review packet.

Use this after the V15 notebook export cell has printed "DONE - files written".
It does not contain an email address. It reads PERSONAL_REVIEW_EMAIL if set,
otherwise it asks for the personal review email when run.

Paste into a Jupyter cell or run from Anaconda Prompt:

    python code_transfer_block\open_v15_share_packet_email_draft.py

Optional environment variables:

    PERSONAL_REVIEW_EMAIL  recipient for the draft
    V15_OUTPUT_DIR         output folder; defaults to ~/Downloads/outputs_runtime/ml_master
    V15_RUN_SLUG           defaults to v15_core_aware_multitask_ann
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


RUN_SLUG = os.environ.get("V15_RUN_SLUG", "v15_core_aware_multitask_ann")
OUTPUT_DIR = Path(
    os.environ.get(
        "V15_OUTPUT_DIR",
        Path.home() / "Downloads" / "outputs_runtime" / "ml_master",
    )
)


def newest(pattern: str) -> Path | None:
    candidates = [p for p in OUTPUT_DIR.glob(pattern) if p.is_file()]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def ps_quote(value: str | Path) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def main() -> None:
    if not OUTPUT_DIR.exists():
        raise FileNotFoundError(f"V15 output folder not found: {OUTPUT_DIR}")

    recipient = os.environ.get("PERSONAL_REVIEW_EMAIL", "").strip()
    if not recipient:
        recipient = input("Personal review email for Outlook draft: ").strip()
    if not recipient:
        raise SystemExit("No recipient provided; set PERSONAL_REVIEW_EMAIL or enter it when prompted.")

    share_zip = newest(f"share_packet_{RUN_SLUG}.zip") or newest("share_packet_*.zip")
    figures_pdf = newest(f"paper_figures_{RUN_SLUG}.pdf") or newest("paper_figures_*.pdf")
    clean_summary = newest(f"clean_summary_{RUN_SLUG}.xlsx") or newest("clean_summary_*.xlsx")
    readme = newest(f"share_packet_readme_{RUN_SLUG}.txt") or newest("share_packet_readme_*.txt")

    if share_zip is None:
        raise FileNotFoundError(
            f"No share_packet_*.zip found in {OUTPUT_DIR}. "
            "Run the V15 notebook export cell first."
        )

    attachments = []
    for item in [share_zip, figures_pdf, clean_summary, readme]:
        if item and item.exists() and item not in attachments:
            attachments.append(item)

    attachment_array = ", ".join(ps_quote(p) for p in attachments)
    script_path = OUTPUT_DIR / f"open_outlook_draft_{RUN_SLUG}.ps1"
    script_text = f"""$ErrorActionPreference = "Stop"
$to = {ps_quote(recipient)}
$attachments = @({attachment_array})
$outlook = New-Object -ComObject Outlook.Application
$mail = $outlook.CreateItem(0)
$mail.To = $to
$mail.Subject = "North Slope ML V15 review packet"
$mail.Body = @"
Attached are the compact V15 review packet plus the figures PDF and clean summary workbook when present.

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

    print("Using V15 output folder:", OUTPUT_DIR)
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
