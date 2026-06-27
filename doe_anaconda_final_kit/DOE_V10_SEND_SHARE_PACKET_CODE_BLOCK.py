# Optional V10 Outlook share-packet email helper.
# Paste this into a new final V10 notebook code cell after the export cell.
# Default behavior opens an Outlook draft; it does not send automatically.

from pathlib import Path
import subprocess

PERSONAL_REVIEW_EMAIL = "nandarohan442@gmail.com"
SEND_NOW = False  # Change to True only if approved to auto-send outside DOE.

output_dir = Path.home() / "Downloads" / "outputs_runtime" / "ml_master"
packet_path = Path(globals().get("SHARE_PACKET_ZIP", output_dir / "share_packet_v10_chong_dphi_lock.zip"))
if not packet_path.exists():
    candidates = sorted(output_dir.glob("share_packet_v10_chong_dphi_lock*.zip"), key=lambda p: p.stat().st_mtime, reverse=True)
    if candidates:
        packet_path = candidates[0]

if not packet_path.exists():
    raise FileNotFoundError(f"Share packet not found: {packet_path}. Rerun the V10 export cell first.")

run_id = globals().get("RUN_ID", "latest")
subject = f"North Slope ML V10 share packet {run_id}"
body = """Attached is the compact V10 share packet from the North Slope gas hydrate ML pipeline.

This packet is intended to contain row-free summary outputs for review. Please confirm the data-transfer boundary before forwarding or using outside the DOE environment.
"""

def ps_single_quote(value) -> str:
    return str(value).replace("'", "''")

def ps_single_line(value) -> str:
    return ps_single_quote(value).replace("\r\n", "`n").replace("\n", "`n")

send_now_ps = "$true" if SEND_NOW else "$false"
script_path = output_dir / "send_share_packet_outlook_v10.ps1"
script_text = f"""$packet = '{ps_single_quote(packet_path)}'
$to = '{ps_single_quote(PERSONAL_REVIEW_EMAIL)}'
$subject = '{ps_single_quote(subject)}'
$body = '{ps_single_line(body)}'
$sendNow = {send_now_ps}

if (-not (Test-Path -LiteralPath $packet)) {{
    throw "Share packet not found: $packet"
}}

$outlook = New-Object -ComObject Outlook.Application
$mail = $outlook.CreateItem(0)
$mail.To = $to
$mail.Subject = $subject
$mail.Body = $body
$mail.Attachments.Add($packet) | Out-Null

if ($sendNow) {{
    $mail.Send()
    Write-Host "Sent share packet to $to"
}} else {{
    $mail.Display()
    Write-Host "Opened Outlook draft for $to with attachment: $packet"
}}
"""
script_path.write_text(script_text, encoding="utf-8")

subprocess.run([
    "powershell",
    "-NoProfile",
    "-ExecutionPolicy", "Bypass",
    "-File", str(script_path),
], check=True)

print(f"Share packet: {packet_path}")
print(f"Outlook helper script: {script_path}")
print("Opened draft" if not SEND_NOW else "Sent email")
