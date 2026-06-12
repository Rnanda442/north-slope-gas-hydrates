# Deliverable Revision Base

Created: 2026-06-12

## Purpose

This directory is the working base for the next North Slope gas-hydrate Word
document and nine-slide PowerPoint pass. It consolidates the user instructions,
past email format rules, current deliverable audit, source pool, visual rules,
and slide-to-document alignment before any new deliverable rebuild.

The website is out of scope for this pass except where the app/runtime skeleton
or reusable code-rendered visuals help explain the research workflow.

## Active Deliverables

| Deliverable | Current local file | Current role |
|---|---|---|
| PowerPoint | `docs/project_blueprints/CURRENT_GMAIL_VISUAL_REVISION_9_SLIDE_North_Slope_Gas_Hydrate_Slides_2026-06-11.pptx` | Current nine-slide Gmail visual revision deck |
| Word document | `docs/project_blueprints/North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview.docx` | Current research overview document |
| Slide builder | `docs/project_blueprints/build_ml_revamp_powerpoint.py` | Rebuilds the deck from generated slide panels |
| Slide visual builder | `docs/project_blueprints/build_processing_slide_assets.py` | Builds Processing-style raster visuals |
| Word builder | `docs/project_blueprints/build_research_overview_deliverables.py` | Rebuilds the Word document |

Current Drive slide deck reference:
`https://docs.google.com/presentation/d/1irTOw1wSGSMkQmUrHp33XPKykfgHNjbQANKyDkbv3H4/edit`

Current Gmail slide source:
Gmail message `19eba86da8752830`, subject `New pressy`, sent 2026-06-12
01:30 CDT. The attached file was copied into this repo as
`docs/project_blueprints/CURRENT_GMAIL_VISUAL_REVISION_9_SLIDE_North_Slope_Gas_Hydrate_Slides_2026-06-11.pptx`.

## Files In This Base

| File | Use |
|---|---|
| `01_email_instruction_digest.md` | User/email instructions converted into build requirements |
| `02_current_deliverable_audit.md` | Current PPTX/DOCX state and implementation implications |
| `03_source_registry.md` | Source pool organized by role and deliverable use |
| `04_format_and_style_rules.md` | Word, slide, science, ML, and data-boundary rules |
| `05_slide_word_alignment_matrix.md` | Slide-by-slide plan tied to matching Word sections |
| `06_next_execution_checklist.md` | Ordered checklist for the next rebuild |

## Non-Negotiables

- Keep the presentation at exactly nine slides unless the user explicitly
  changes the slide count.
- Use code-rendered/Processing-style visuals for slide graphics instead of
  building the deck around PowerPoint shapes or generic logos.
- Use correct parameter symbols and pair each symbol with a plain-language name.
- Explain parameters through visuals: measured property, hydrate interpretation,
  false positives, and ML role.
- Treat the Word document as the detailed source-backed explanation. Treat the
  slides as visual communication.
- Do not insert approved well-log rows, core rows, restricted well identifiers,
  trained model outputs, populated runtime settings, or sensitive derived
  outputs into public deliverables.

## Current Working Assumption

The next pass should update the Word document first, because it carries the
detailed source logic and methods explanation. The PowerPoint should then be
rebuilt from the Word plan so the slide visuals, terminology, source roles, and
validation language stay synchronized.
