# Gmail Recovery Summary — 2026-06-25

This file records the Gmail/self-sent project attachment recovery pass for the North Slope gas-hydrate project.

## Result

- Repo-intake staging package created locally: `gmail_repo_intake_2026-06-25/`
- Local-only source-library package created locally: `data/source_library/gmail_recovered_2026-06-25/`
- Full local manifest created: `gmail_recovery_manifest_2026-06-25.md`
- Full inventory CSV created: `gmail_recovery_inventory_2026-06-25.csv`

## Counts from the recovery pass

- Repo-staged manifest files: 3
- Repo-staged project docs/decks: 3
- Staged reference screenshots/images: 11
- Local-only source-library files: 48
- Gmail-listed unresolved items needing follow-up: 25
- Total manifest rows: 90

## Repo-facing files staged locally

These were staged in the repo-intake package for review/copy into the repository:

- `docs/source_library_index/gmail_recovery_inventory_2026-06-25.csv`
- `docs/source_library_index/gmail_recovery_manifest_2026-06-25.md`
- `docs/source_library_index/source_manifest_uploaded_2026-06-25.csv`
- `docs/project_blueprints/gmail_recovered_2026-06-25/Codex_Website_Brand_Design_Workflow.docx`
- `docs/project_blueprints/gmail_recovered_2026-06-25/ML_Project_Reference_and_CreditScoreV4_Case_Notes.docx`
- `docs/project_blueprints/gmail_recovered_2026-06-25/V5.5 Slide 3 Signal Response QC-Cleaned North Slope Gas Hydrate ML Workflow Slides 2026-06-17 (1).pptx`
- `references/gmail_recovered_2026-06-25/screenshots/` containing 11 staged screenshot/reference images

## Local-only source files recovered

Raw/source material was intentionally kept under the ignored `data/source_library/` boundary. This includes the extracted curated source-library bundle plus four direct Gmail source papers:

- `data/source_library/gmail_recovered_2026-06-25/extra_source_papers/An_Empirical_Comparison_of_Machine_Learn.pdf`
- `data/source_library/gmail_recovered_2026-06-25/extra_source_papers/falahat.pdf`
- `data/source_library/gmail_recovered_2026-06-25/extra_source_papers/s10596-022-10151-9.pdf`
- `data/source_library/gmail_recovered_2026-06-25/extra_source_papers/sign2019.pdf`
- `data/source_library/gmail_recovered_2026-06-25/source_library/` extracted from `North_Slope_Curated_Source_Library_UNCLASSIFIED.zip`

Do not commit raw PDFs or source bundles from `data/source_library/` unless the project data-boundary decision is changed deliberately.

## Unresolved Gmail-listed items

The full manifest lists 25 unresolved names. Main examples include older/final manuscript or deck names, source screenshot ZIPs, the reference-management ZIP, and several paper attachments from the `Paper text and sources` thread. These were not physically recovered in this pass or had stale attachment IDs.

## Copy/commit guidance

1. Copy `gmail_repo_intake_2026-06-25/` into the repository root only after reviewing screenshots and binary docs/decks.
2. Copy `data/source_library/gmail_recovered_2026-06-25/` only into the local ignored source-library area.
3. Run `git status --short` before committing.
4. Commit text manifests and public-safe reviewed assets only.
