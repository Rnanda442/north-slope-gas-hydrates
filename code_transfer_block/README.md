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
- `anaconda_commands.txt` - short command list for the DOE prompt.

## Guardrail

Do not paste approved workbook rows, prediction rows, fitted model files, or
runtime outputs back into GitHub. Bring back only row-free summaries after
review.
