# Code Transfer Block

This folder is for short, copyable code blocks that can be moved into the DOE
Anaconda/Jupyter environment without re-downloading the full repository.

Use this folder when chat copy/paste is awkward or when DOE needs one small
script at a time.

## Current Blocks

- `notebook_header_scan_cell.py` - copy the whole file into one Jupyter cell.
  It scans the three curated Excel workbooks, prints likely target headers, and
  writes local CSV summaries.
- `inspect_three_dataset_headers_standalone.py` - run from Anaconda Prompt as a
  standalone script. It does not import project modules.
- `multi_saturation_target_workflow.py` - standalone first-pass runtime that
  treats every saturation-like column as a separate Y-only regression target,
  then predicts unlabeled feature sheets where possible.
- `v15_presentation_review_and_email.py` - after the V15 notebook finishes,
  builds a compact row-free presentation review packet from the V15 outputs,
  prints the files Codex needs to review how well the run worked, and opens a
  saved Outlook draft with the packet attached.
- `v15_after_notebook_copy_this_cell.py` - copy the entire file into one new
  VS Code/Jupyter cell after the V15 notebook finishes. It rebuilds a local
  `Code output` folder with the V15 review files, figures, summaries,
  manifests, WLC/checkpoint tables, and a fresh ZIP for Drive upload. If Google
  Drive for Desktop exposes a synced `Code output` folder, it mirrors the
  rebuilt folder there too. If `rclone` is installed and configured with a
  Google Drive remote named `gdrive`, it automatically syncs/replaces
  `gdrive:Code output`. Row-level predictions and fitted models are excluded
  by default and listed in an excluded-files manifest.
- `anaconda_commands.txt` - short command list for the DOE prompt.

## Guardrail

Do not paste approved workbook rows, prediction rows, fitted model files, or
runtime outputs back into GitHub. Bring back only row-free summaries after
review.
