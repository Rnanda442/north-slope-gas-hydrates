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
  VS Code/Jupyter cell after the V15 notebook finishes. It builds the same
  row-free review packet and opens a saved Outlook draft without manually
  opening a terminal.
- `anaconda_commands.txt` - short command list for the DOE prompt.

## Guardrail

Do not paste approved workbook rows, prediction rows, fitted model files, or
runtime outputs back into GitHub. Bring back only row-free summaries after
review.
