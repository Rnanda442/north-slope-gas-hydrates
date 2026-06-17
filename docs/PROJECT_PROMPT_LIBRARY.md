# Project Prompt Library

Last updated: 2026-06-16

Use these prompts as reusable starting points. Each prompt intentionally starts
by reading `docs/AGENT_START_HERE.md`; keep that requirement when copying or
editing.

## Slide Rebuild

```text
We are working in Rnanda442/north-slope-gas-hydrates.

First read docs/AGENT_START_HERE.md, then docs/CURRENT_ARTIFACT_INDEX.md.
Then read docs/FULL_PROJECT_ML_WORKFLOW_DIAGRAM.md,
docs/FINAL_DELIVERABLE_CONSOLIDATION_AND_CLEANUP_PLAN_2026-06-15.md,
docs/FINAL_NINE_SLIDE_GAP_AND_DIAGRAM_REUSE_PLAN_2026-06-15.md,
docs/FINAL_NEW_SLIDE_DECK_CREATION_PROMPT_2026-06-15.md, and
docs/GMAIL_STYLE_V5_2_SLIDE_REMAKE_PROMPT_2026-06-15.md.

Task: rebuild or revise the current V5.3 mentor-facing deck. Keep the nine main
audience topic slides, preserve the complex workflow and ML runtime diagrams as
whole appendix plates when needed, use website/source-backed visuals, and keep
the explanation clear for non-ML/non-hydrate audiences.

Guardrails: do not expose approved/private rows; do not claim hydrate proof,
final stability, final top/base/thickness, trained ML metrics, occurrence
predictions, saturation predictions, or sweet spots. Use blue callouts only for
runtime confirmations that depend on approved workbook recovery.

Before editing, run git status --short and preserve unrelated changes. Prefer
`docs/project_blueprints/build_full_workflow_diagram_deliverables.py`. After
rebuilding, verify the deck exists locally, inspect the slide count and
generated panels/contact sheet, run the requested tests, update
docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md only if a milestone or next
action changed, then report exactly what changed.
```

## Word Companion Rebuild

```text
We are working in Rnanda442/north-slope-gas-hydrates.

First read docs/AGENT_START_HERE.md, then docs/CURRENT_ARTIFACT_INDEX.md.
Then read docs/NORTH_SLOPE_PROJECT_BASE.md,
docs/APPROVED_DATA_SCHEMA_COVERAGE_AND_MODEL_ARCHITECTURE_PLAN.md,
docs/APPROVED_DATA_INTAKE_SPEC_2026-06-15.md,
docs/FIRST_MODEL_EXPERIMENT_PLAN_2026-06-15.md,
docs/STABILITY_CALCULATION_PLAN.md, docs/SCIENCE_TO_ML_LOGIC_LADDER.md, and
docs/ML_PIPELINE_BASELINE_SOURCE_LEDGER.md.

Task: rebuild or revise the V5.3 Word companion so it explains the current
public/OSL boundary, stability-admissibility layer, parameter evidence logic,
approved-data intake contract, leakage-safe ML workflow, occurrence
classification path, saturation regression path, validation plan, and mentor
decisions.

Guardrails: public-safe planning artifact only. Do not include approved rows,
trained metrics, hydrate proof, final stability top/base/thickness, occurrence
predictions, saturation predictions, or sweet-spot claims.

Before editing, run git status --short. Prefer
docs/project_blueprints/build_full_workflow_diagram_deliverables.py. Verify
the DOCX exists locally after rebuild, run the requested tests, update relevant
docs only for meaningful changes, and report the output path.
```

## Website Update

```text
We are working in Rnanda442/north-slope-gas-hydrates.

First read docs/AGENT_START_HERE.md, then docs/CURRENT_ARTIFACT_INDEX.md.
Then inspect dashboard/app.py, streamlit_app.py, the relevant helper module,
and the data products or docs that drive the page being changed.

Task: update the public Streamlit site while keeping the four-section structure:
Overview, Explore North Slope, Analyze Hydrates, and Project Plan. Keep Explore
North Slope focused on Regional Map, 3D Structure, and Data & Sources. Keep
Analyze Hydrates focused on Public ML Readiness, Schema Coverage &
Architecture, Target Registry & Leakage, Interval Review, Runtime Readiness,
Model Run Tracker, Presentation Exports, and Methods & Evidence.

Guardrails: the website is public delivery and skeleton transfer surface only.
It must not load approved rows, private identifiers, trained model artifacts,
approved metrics, occurrence predictions, or saturation predictions.

Before editing, run git status --short. Add or update tests for behavior
changes. For meaningful UI changes, run the app locally and verify with browser
QA if a local target is available. Run python -m pytest and report the tested
count.
```

## OSL Header Audit

```text
We are working in Rnanda442/north-slope-gas-hydrates.

First read docs/AGENT_START_HERE.md, then docs/CURRENT_ARTIFACT_INDEX.md.
Then read docs/OSL_APPROVED_DATA_HEADER_AUDIT_RUNBOOK_2026-06-15.md,
docs/APPROVED_DATA_INTAKE_SPEC_2026-06-15.md, and
data/public_ml_products/README.md.

Task: prepare or run the approved-data header audit in OSL/approved runtime.
Use 01_pipeline/validate_approved_data_headers.py. For CSV inputs, use
--header-only so no row values are read. Write only public-safe readiness
summaries under data/public_ml_products/intake_readiness_reports/.

Guardrails: do not print, copy, commit, or summarize approved row values,
restricted well identifiers, private workbook paths, populated configs, model
outputs, or sensitive derived results. Sanitize source names unless explicitly
approved for public use.

After running, inspect output CSV/JSON locally, verify no row-level values are
present, update docs only if the readiness status or next action changed, run
python -m pytest if code changed, and report output paths plus blocked reasons.
```

## Source Research Pass

```text
We are working in Rnanda442/north-slope-gas-hydrates.

First read docs/AGENT_START_HERE.md, then docs/CURRENT_ARTIFACT_INDEX.md.
Then read docs/source_library_index/README.md,
docs/source_library_index/source_index.md, docs/ML_PIPELINE_BASELINE_SOURCE_LEDGER.md,
and the source package README that matches the topic.

Task: run a source research pass for [topic]. Add only legitimate public,
institutionally available, or user-authorized source records. Place public
source packages under references/<topic>/<YYYY-MM-DD>/ with a README or
source_manifest.csv. Update docs/source_library_index/ only when the source
index changes.

Guardrails: do not commit restricted PDFs, credentialed downloads, approved
data, private rows, or raw heavy bundles. If a paper is inaccessible, record a
needs-PDF or retrieval note rather than fabricating content.

After intake, summarize what was added, what remains missing, how each source
can be used, and what claims it does not support.
```

## Parameter Evidence Update

```text
We are working in Rnanda442/north-slope-gas-hydrates.

First read docs/AGENT_START_HERE.md, then docs/CURRENT_ARTIFACT_INDEX.md.
Then read data/public_ml_products/README.md,
data/public_ml_products/public_parameter_evidence_registry_2026-06-16.csv,
dashboard/parameter_evidence.py, docs/SCIENCE_TO_ML_LOGIC_LADDER.md, and
docs/ML_PIPELINE_BASELINE_SOURCE_LEDGER.md.

Task: update the public parameter evidence board for [new parameter/source].
Keep rows public-safe and distinguish stability, reservoir quality,
hydrate-response logs, QC, and Y-only targets. Mark numeric values as working
screening envelopes unless source and approved-data calibration justify
stronger language.

Guardrails: stability, high resistivity, low GR, velocity/elastic changes, NMR
separation, and target labels are not hydrate proof by themselves. Target
labels stay Y-only and never enter X_allowed.

After editing, run the parameter evidence tests and then python -m pytest.
Update docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md only if this changes a
milestone, blocker, priority, dependency, or next action.
```

## Stability Guardrail Check

```text
We are working in Rnanda442/north-slope-gas-hydrates.

First read docs/AGENT_START_HERE.md, then docs/CURRENT_ARTIFACT_INDEX.md.
Then read docs/STABILITY_CALCULATION_PLAN.md,
data/public_stability_products/README.md,
data/public_stability_products/stability_input_capability_matrix_2026-06-14.csv,
and data/public_stability_products/stability_osl_pull_triggers_2026-06-14.csv.

Task: audit [doc/code/product/page] for stability-language and data-boundary
guardrails. Confirm it says stability-admissibility/context only and does not
claim hydrate proof, final stability, final top/base/thickness, occurrence,
saturation, producibility, or sweet spots.

Guardrails: the methane 5 ppt screen is a public baseline under assumptions.
Mixed gas/composition variants remain scenario candidates unless source-backed
and mentor-approved. Blocked rows stay null with explicit blocked reasons.

After the audit, list exact files and lines reviewed, required fixes, and tests
run. If changes were made, run python -m pytest.
```

## Mentor Status Update

```text
We are working in Rnanda442/north-slope-gas-hydrates.

First read docs/AGENT_START_HERE.md, then docs/CURRENT_ARTIFACT_INDEX.md.
Then read docs/MENTOR_PROJECT_STATUS_PACKAGE_V5_WORKFLOW_2026-06-15.md,
docs/MENTOR_DECISION_REQUESTS_2026-06-15.md,
docs/WEEKDAY_PROGRESS_REPORT_TEMPLATE.md,
docs/APPROVED_DATA_SCHEMA_COVERAGE_AND_MODEL_ARCHITECTURE_PLAN.md, and
docs/STABILITY_CALCULATION_PLAN.md.

Task: draft a concise mentor status update for [date/audience]. Include what is
complete, what is public-safe, what remains OSL/approved-runtime only, what is
blocked by data or mentor decisions, and the next requested decision.

Guardrails: do not report hydrate proof, final stability, final
top/base/thickness, trained ML metrics, occurrence predictions, saturation
predictions, or sweet-spot ranking. Use clear public-safe language and separate
stability-admissibility from occurrence/saturation modeling.

Output the update as Markdown unless a DOCX/PPTX build is explicitly requested.
Update project docs only if the status, blockers, or next action changed.
```
