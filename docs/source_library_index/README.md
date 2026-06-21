# Source Library Index

This folder contains a lightweight index of the public/source-planning materials
organized for the Alaska North Slope gas hydrate project.

## Files

- `source_manifest.csv` lists the organized source files by category, source
  path, copied-library path, file size, and modification time.
- `source_index.md` summarizes the organized source groups and gives orientation
  snippets for later citation work.
- `source_inventory_2026-06-17.csv`,
  `SOURCE_ORGANIZATION_REPORT_2026-06-17.md`,
  `SOURCE_GAPS_AND_DOWNLOADS_2026-06-17.md`, and
  `DRIVE_GMAIL_SOURCE_HANDOFF_2026-06-17.md` are the current Gmail/Drive source
  intake authority from the PC organization pass. They record the Drive folder,
  verified Gmail attachments, organized raw-PDF names, missing papers, and the
  rule that raw PDFs remain Drive-only until license and size are reviewed.
- `../../01_pipeline/build_source_intake_inventory.py` can regenerate the same
  public-safe source inventory/report naming convention from local Drive/Gmail
  folders. Use it for future source drops instead of creating parallel
  timestamped formats.
- `stability_source_bundle_2026_06_13.md` documents the OpenScienceLab stability
  source bundle behind the current public stability products. Pair it with
  `../STABILITY_CALCULATION_PLAN.md` before implementing the temperature model
  and stability intersection step.
- `source_index.md` also includes `permafrost-mtelbert (1).pdf`, the Collett
  et al. (2011) Alaska North Slope occurrence paper now used to justify
  mixed-gas phase-curve sensitivity planning.

## How the Sources Are Used

The current project direction is not a general gas hydrate overview. The source
library is being used to support a future approved-data workflow:

1. measured wireline/core variables,
2. derived equations and physics features,
3. staged hydrate classification gates,
4. machine-learning features and validation,
5. results, uncertainty, and producibility discussion.

The broad manuscript remains useful as a synthesis/source accumulation, while
the paper-sources-only equation-focused Word document is now the main research
paper working copy:

```text
docs/project_blueprints/North_Slope_Gas_Hydrate_Equation_Focused_Research_Overview_Paper_Sources_Only_2026-06-17.docx
```

The next source pass should use the organized Drive source folder and this
index. The Drive PDFs, screenshots, local paths, and Gmail attachment files are
internal evidence/navigation aids; only reviewed manifests, notes, and
public-safe derived visuals belong in GitHub.

## What Is Not Included

The full source-library PDFs and DOCX files are not copied into this Git folder.
Several are large, and at least one exceeds GitHub's 100 MB file limit. Keep the
full source library locally or in an approved cloud/workspace storage location.

## Boundary

This index is for public-source planning only. Do not add classified,
restricted, credentialed, or approved-environment-only well-log data here.
