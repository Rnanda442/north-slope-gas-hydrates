# Project Direction Lock For Review

Created: 2026-06-12

Status: review draft. The user should revise this file before the next major
Word, PowerPoint, or website edit if the goal, audience, order, or visual
direction is wrong.

## Purpose

This file exists to prevent the project from drifting between chats, laptops,
the Word document, the slide deck, and the website. It states the working vision
and the order of work before the next round of deliverable changes.

## One-Sentence Project Goal

Build a source-backed North Slope gas-hydrate workflow that uses approved
well-log and core inputs to predict hydrate occurrence and saturation, while
keeping public materials synthetic, traceable, visually clear, and protected
from target leakage.

## Audience

Primary audience:

- DOE / internship reviewers.
- Technical but mixed-background readers.
- People who may understand energy/geoscience better than machine learning.

Communication style:

- Scientific and government-ready.
- Visual-first, but not decorative.
- Clear enough for a non-specialist to understand what `R_t`, `GR`, `V_p`,
  `V_s`, `AI`, `S_h`, and QC gates mean.
- Honest about what is planned versus what has already been validated.

## Current Priority Order

1. Confirm this direction file.
2. Update the Word document first.
3. Rebuild the nine-slide PowerPoint from the Word/source plan.
4. Update the website only where it supports the app/runtime skeleton or
   mirrors the finalized public-safe workflow.

Reason:

The Word document should lock the science, sources, parameter meanings,
methodology, and validation logic. The slides should then simplify that into
large source-backed visuals. The website should not drive the science or deck
story during this pass.

## Deliverable Roles

| Deliverable | Role | Current rule |
|---|---|---|
| Word document | Main source-backed explanation of the project | Methods and source logic first; no fake results |
| PowerPoint | Visual explanation for presentation | Exactly nine slides unless the user changes this |
| Website | Public atlas plus app/runtime skeleton | Secondary for now; no public real data |
| Runtime skeleton | Future approved-data execution path | Can define schemas, QC, features, validation, and outputs |
| Source package | Evidence and visual provenance | Every claim should trace to a source tier |

## Word Document Direction

The Word document should read like a research plan and methods document, not
like speaker notes for the slides.

Required shape:

- Filled abstract.
- Filled introduction.
- Source/evidence tier section.
- Parameter section using a repeated grammar:
  `measures`, `hydrate use`, `false positives`, `ML role`, `source basis`.
- Methodology section:
  approved logs/core -> schema/unit mapping -> depth alignment -> QC gates ->
  feature equations -> target registry -> train-only preprocessing ->
  complete-well validation -> outputs.
- ML framework:
  direct permafrost ML anchor, comparative ML methods, baseline/advanced model
  ladder, leakage controls, calibration, and monitoring.
- Results/discussion plan:
  planned figures and review outputs only, not made-up metrics.

## Nine-Slide PowerPoint Direction

The deck should be visual and source-backed. The current deck is raster-panel
based, so edits should go through the builders and generated panels rather than
manual native slide text-box edits.

Required slide roles:

| Slide | Role |
|---|---|
| 1 | Title and about me |
| 2 | What methane hydrate is and why North Slope matters |
| 3 | Parameter and well-log scaffold |
| 4 | Detailed ML architecture |
| 5 | Why parameter behavior matters |
| 6 | Geomechanics and equations |
| 7 | Map/context and screening logic |
| 8 | Results/discussion plan and error review |
| 9 | Conclusion and next approved-data tasks |

Slide visual rules:

- Use larger visuals and fewer words.
- Use Processing/code-rendered visuals where practical.
- Use correct symbols and plain names together.
- Reuse parameter icons across slides 3-6.
- Keep `S_h`, `Sgh`, `NMR_SAT`, phase labels, and final rankings locked as
  labels/outputs, not model inputs.
- Do not show fake model metrics.

## Website Direction

The website should not be the main workstream until the Word and deck direction
are stable.

Allowed website work in this phase:

- Keep the app running.
- Keep the public/synthetic data boundary visible.
- Show runtime skeleton readiness.
- Mirror finalized workflow diagrams after the Word/PPT direction is approved.
- Use public-safe generated visuals.

Avoid for now:

- Large navigation redesigns.
- New public claims not already backed by the Word/source plan.
- Any real approved-data loading in the public app.

## Scientific Commitments

These rules should stay consistent across the Word document, slides, website,
and runtime skeleton:

- Gas-hydrate stability is necessary but not proof.
- Occurrence, saturation, reservoir quality, producibility, and uncertainty are
  separate concepts.
- High resistivity alone is not a hydrate label.
- Low gamma ray supports clean sand/reservoir context, not hydrate proof.
- Caliper is a QC gate, not hydrate evidence.
- Core calibrates and validates where available; sparse core is not continuous
  truth.
- GIS/map context is screening context; logs and core decide interval evidence.

## ML Commitments

- Use complete-well or compartment holdouts, not random depth-row validation as
  the final standard.
- Fit normalization, imputation, feature selection, and calibration on training
  wells only.
- Keep target-derived fields out of predictors.
- Use baselines for comparison before advanced models.
- Do not report project model metrics until approved-data validation exists.
- Use Chong et al. (2022) as the direct gas-hydrate/well-log ML anchor.
- Use Singh et al. (2021) and Chong et al. (2024) as comparative ML method
  support, not North Slope field truth.

## Data Boundary

Public repository and public Drive deliverables may include:

- Public GIS context.
- Public USGS/DOE/NETL source references.
- Synthetic examples.
- Empty runtime schemas/adapters.
- Source-backed diagrams and planning documents.

Public repository and public Drive deliverables must not include:

- Approved or restricted LAS/CSV/core rows.
- Named restricted well identifiers.
- Populated runtime configs.
- Trained models.
- Runtime logs or derived sensitive outputs.
- Personal visual assets unless the user explicitly approves public tracking.

## Open Decisions For User Review

Edit these directly:

1. Is the one-sentence project goal correct?
2. Should the deck stay exactly nine slides?
3. Should slide 1 include personal/about-me visuals in the repo, or only in
   Drive/local copies?
4. Should the current PPTX be tracked in Git, or should Git track only builders,
   source manifests, and public-safe exported panels?
5. Is the work order correct: Word first, slides second, website third?
6. Should the website remain mostly app/runtime skeleton for now?
7. Are the primary outputs correct: occurrence, saturation, uncertainty, and
   review/sweet-spot screening?
8. Are any sources, equations, or ML claims missing before the next build?

## What Is Still Not Ready

- Full Excel workbook and formulas are not yet recovered in this official
  folder.
- Authoritative hydrate-saturation target is not confirmed.
- Phase labels and uncertain-label conventions are not confirmed.
- Known-label, validation, locked-test, and prediction well lists are not
  confirmed.
- Approved-data model metrics do not exist yet.
- Public-safe policy for slide-1 personal visual assets needs user decision.

## Acceptance Criteria Before Next Major Edit

Proceed to Word/PPT changes only when:

- This direction file has been reviewed or accepted.
- Source roles are clear.
- Data-boundary rules are accepted.
- The slide count and slide roles are accepted.
- The Word-first, slide-second, website-third order is accepted or revised.

## Current Working Recommendation

Do the next work in this order:

1. User reviews and edits this file.
2. Update the Word builder and DOCX.
3. Rebuild the slide panels and PPTX.
4. Upload/replace Drive deliverables only after local verification.
5. Update website/app skeleton only for consistency with the final approved
   Word/PPT direction.
