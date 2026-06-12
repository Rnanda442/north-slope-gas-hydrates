# Current Deliverable Audit

Created: 2026-06-12

## PowerPoint Audit

Local file:
`docs/project_blueprints/CURRENT_GMAIL_VISUAL_REVISION_9_SLIDE_North_Slope_Gas_Hydrate_Slides_2026-06-11.pptx`

Source:

- Gmail message `19eba86da8752830`
- Subject: `New pressy`
- Sent: 2026-06-12 01:30 CDT
- Original local copy: `C:\Users\gargi\Downloads\GMAIL VISUAL REVISION 9-SLIDE North Slope Gas Hydrate Slides 2026-06-11.pptx`

Current structure:

- 9 slides.
- Verified locally as a valid PPTX.
- Treat this Gmail deck as the latest user-approved slide starting point.
- The older tracked `North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview.pptx`
  remains useful as provenance and builder output, but it is not the first deck
  to revise.

Implementation implication:

- Do not plan normal PowerPoint text-box edits as the primary workflow.
- Slide changes should be made in the code-rendered panel assets, then rebuilt
  into the PPTX unless the user specifically requests quick native edits.
- The main slide asset generator is
  `docs/project_blueprints/build_processing_slide_assets.py`.
- The deck assembly builder is
  `docs/project_blueprints/build_ml_revamp_powerpoint.py`.

Current Drive slide deck reference:
`https://docs.google.com/presentation/d/1irTOw1wSGSMkQmUrHp33XPKykfgHNjbQANKyDkbv3H4/edit`

Current risk:

- Because the deck is raster-panel based, visual QA must inspect the generated
  slide images or exported thumbnails. A clean PPTX object tree does not prove
  the slide looks good.

## Word Document Audit

Local file:
`docs/project_blueprints/North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview.docx`

Current structure:

- 173 inspected paragraphs.
- Main early sections include title, subtitle, boundary/source notes, Abstract,
  Introduction, conceptual hydrate-reservoir sketch, approved-data processing
  sketch, website visual workflow, Parameters, and a parameter/masking matrix.

Implementation implication:

- The document already has a useful research-overview scaffold, but it still
  contains a website visual workflow section that should be deprioritized for
  this pass.
- The next revision should emphasize:
  - gas-hydrate science and North Slope context;
  - source coverage and evidence tiers;
  - parameter meanings, symbols, equations, and caveats;
  - approved-data ML pipeline and validation design;
  - output placeholders without fake results.
- The Word builder is
  `docs/project_blueprints/build_research_overview_deliverables.py`.

## Existing Planning Sources Already In Repo

| File | Role for next pass |
|---|---|
| `docs/ML_SOURCE_COVERAGE_AND_DELIVERABLE_REVISION_PLAN.md` | Current source gate for ML and science coverage |
| `docs/NINE_SLIDE_POWERPOINT_REVISION_WORKFLOW.md` | Prior nine-slide deck workflow |
| `docs/ML_PARAMETER_TREE_AND_DECK_REVAMP_PLAN.md` | Parameter and deck visual rationale |
| `docs/ML_VISUAL_ARCHITECTURE_PLAN.md` | Architecture and visual logic |
| `docs/SWEET_SPOT_SOURCE_MATRIX.md` | Source tiers and North Slope evidence matrix |
| `docs/WELL_LOG_REQUIREMENTS_MAP.md` | Header/schema/target-leakage boundary |
| `docs/runtime_skeleton_brief.md` | Runtime/app skeleton and approved-data boundary |
| `docs/project_blueprints/ml_parameter_effect_tree.csv` | Parameter family, caveat, icon, and model-role matrix |
| `references/presentation-revision-2026-06-11/source_manifest.csv` | Visual and text source manifest for the slide revision package |
| `references/ml-sources/2026-06-11/README.md` | ML source intake and role definition |

## Required Verification After Next Rebuild

- Confirm the local PPTX still contains exactly 9 slides.
- Render or inspect changed slide panels at slide size.
- Inspect Google-rendered thumbnails after any Drive upload or replacement.
- Confirm the Word document opens and has the expected section order.
- Run `git diff --check` after edits.
- Run project tests only when code/builders/runtime behavior changed.
