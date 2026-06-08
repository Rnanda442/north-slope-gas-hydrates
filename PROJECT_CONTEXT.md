# North Slope Gas Hydrates Project Context

Last updated: 2026-06-08

## Purpose

This file is the living project memory for people and agents working in this
repository. Read it before starting work and update it after meaningful changes.
The detailed architecture, workstream status, dependencies, and next activities
live in `docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md`.

## Project Goal

Build a scientifically defensible North Slope gas-hydrate research workflow that
connects public regional GIS context with an authorized, runtime-only well-log
and core-analysis system. The immediate goal is to finish the well-log
scaffolding using the user's Excel-based design as a visual and functional
reference.

The intended analysis chain is:

```text
regional geology and stability context
-> approved LAS/CSV/core inputs
-> schema mapping and quality control
-> standardized well-log and core tables
-> manuscript-backed feature engineering
-> core-log calibration
-> interval screening and classification
-> uncertainty-aware plots, tables, GIS links, and manuscript exports
```

## Current Focus

Use the recovered normalized Excel header screenshots to define the canonical
well-log schema, unit conversions, curve roles, track groups, and target-leakage
guardrails. Continue recovering the workbook and formulas before changing
scientific calculations.

## Current State

- The public Streamlit regional atlas is implemented.
- The website includes a mobile-responsive `Project Roadmap` page sourced from
  `docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md`.
- The synthetic well-log planning page and reusable calculation layer are
  implemented in `dashboard/well_log_engine.py`.
- The authorized runtime skeleton is implemented in `dashboard/runtime/`.
- Tests exist in `tests/test_well_log_engine.py` and
  `tests/test_runtime_skeleton.py`.
- The full project test suite passed on 2026-06-08: 13 tests passed.
- Public GIS layers, notebooks, structural surfaces, and Plotly exports are
  present.
- Two working Word drafts are present in `docs/project_blueprints/`.
- The public source-library index is present in `docs/source_library_index/`.
- Six normalized Excel header screenshots are stored in
  `references/well-log-spreadsheet/` and mapped in
  `docs/WELL_LOG_REQUIREMENTS_MAP.md`.
- The user's full Excel workbook and PowerPoint have not yet been recovered into
  this official folder.
- The missing PowerPoint was last confirmed in the source laptop's `Downloads`
  folder as `Alaska_North_Slope_Wireline_ML_Presentation_Scaffold_outline.pptx`.
- The June 6 source migration targeted a local fake-Drive folder and did not
  upload the source library: 211 of 212 files were missing and 1 was blocked.
- Several supporting research documents were found on the connected Google
  Drive, but the connected account does not currently expose the named North
  Slope PowerPoint or source-library folder. See
  `docs/source_recovery_status.md`.
- The working tree was recovered on 2026-06-07 from a prior Codex session
  archive.
- This official folder is connected to
  `https://github.com/Rnanda442/north-slope-gas-hydrates.git`; local `main` and
  `origin/main` were synchronized on 2026-06-08.

## Website

Primary entry point: `streamlit_app.py`

Main application: `dashboard/app.py`

Hosted deployment:
`https://north-slope-gas-hydrates-vj67xkke9ksfzveon8ldt2.streamlit.app/`

As checked on 2026-06-08, the deployment is public and anonymous visitors can
open it without Streamlit sign-in.

Current public views:

- Welcome
- Regional Atlas
- Structural Explorer
- Data Library
- Research Framework
- Future Well-Log Engine

The hosted website must remain a public-source atlas and synthetic demonstration.
It must not load or expose authorized well-log or core data.

## Scientific Rules

1. Gas-hydrate stability is necessary but not sufficient for hydrate presence.
2. Hydrate occurrence, saturation, reservoir quality, and producibility are
   separate outputs.
3. High resistivity alone is not a defensible hydrate label.
4. Classification should use multiple logs plus geological context.
5. Core calibration adjusts confidence and should not silently overwrite logs.
6. Future model validation must split by well, not by random depth rows.
7. GIS context constrains and visualizes interpretation; it does not replace
   direct log or core evidence.

## Authoritative Project Files

- `README.md`: repository and website orientation
- `docs/project_inventory.md`: current asset inventory and engineering stages
- `docs/runtime_skeleton_brief.md`: runtime package design and scientific rules
- `docs/opensciencelab_runtime_layout.md`: authorized-data folder boundary
- `docs/data_dictionary.md`: public atlas layer definitions
- `docs/project_blueprints/Alaska_North_Slope_Wireline_ML_Classification_Methods_Draft.docx`:
  primary working methods direction
- `docs/project_blueprints/Alaska_North_Slope_Wireline_ML_Research_Paper_Draft.docx`:
  broader manuscript and source synthesis
- `docs/source_library_index/source_index.md`: source orientation
- `docs/source_library_index/source_manifest.csv`: source inventory
- `docs/source_recovery_status.md`: Drive search results, original paths, and
  recovery checklist
- `docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md`: authoritative architecture,
  priorities, workstream status, blockers, and next-work sequence
- `docs/PROJECT_IMPROVEMENT_STRATEGY.md`: principles and phased improvement
  strategy for keeping product changes aligned with the scientific goal
- `docs/WELL_LOG_REQUIREMENTS_MAP.md`: screenshot-derived header schema,
  scaffold requirements, track groups, and unresolved questions

## Source Intake

Place public or synthetic design references in `references/` using descriptive
names. Spreadsheet screenshots belong in `references/well-log-spreadsheet/`.

For each screenshot or workbook, record:

- original filename and date
- sheet or screen represented
- visible columns, units, formulas, and chart tracks
- whether values are public, synthetic, or restricted
- intended dashboard or runtime behavior
- unresolved questions

Restricted or approved-environment-only data must not be copied into this
repository. Record only a non-sensitive description and keep the actual file in
the authorized runtime environment.

## Next Actions

The current ordered plan is maintained in
`docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md`.

## Update Protocol

Keep this file concise and factual. Maintain detailed status, dependencies,
blockers, and next activities in the architecture/activity map.

## Decision Log

- 2026-06-07: This folder was designated the official project folder.
- 2026-06-07: `PROJECT_CONTEXT.md` is the canonical living project memory.
- 2026-06-07: The classification-methods Word draft is the primary manuscript
  direction; the broader research-paper draft is supporting context.
- 2026-06-07: The public website remains synthetic/public-source only, while
  approved well-log and core inputs remain runtime-only.

## Change Log

- 2026-06-07: Recovered the project working tree from the June 6 Codex archive.
- 2026-06-07: Added agent instructions, project context, and source-intake
  guidance.
- 2026-06-07: Verified the recovered well-log and runtime scaffold with 8 passing
  tests.
- 2026-06-07: Searched the connected Google Drive and documented that the June 6
  migration was a failed local test rather than a real Drive upload.
- 2026-06-08: Added the project architecture and activity map as the
  authoritative next-work tracker.
- 2026-06-08: Published the architecture/activity map inside Streamlit and added
  responsive phone-width styling.
- 2026-06-08: Recorded the hosted Streamlit URL and found that its initial
  sharing state required sign-in.
- 2026-06-08: Verified the official folder's Git remote and history are
  synchronized, and improved the roadmap's phone-width workstream view.
- 2026-06-08: Changed the hosted Streamlit deployment to public access and
  verified that an anonymous request reaches the app without an access-denied
  response.
- 2026-06-08: Established a phased improvement strategy centered on guided
  scientific communication, requirements traceability, runtime readiness, and
  decision-quality outputs.
- 2026-06-08: Recovered six normalized Excel header screenshots and created the
  initial well-log requirements map without using the displayed values.
