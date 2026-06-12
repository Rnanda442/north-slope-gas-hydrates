# Email and User Instruction Digest

Created: 2026-06-12

This digest converts the relevant Gmail/user instructions into concrete
requirements for the next Word and PowerPoint pass.

## 2026-06-08 - Project Constraint Q&A

Gmail message id: `19ea87193e412a0d`

Key requirements:

- The main deliverable is a strong ML workflow and skeleton before approved data
  arrives.
- The audience is internship/DOE oriented and includes people who may not be ML
  specialists.
- The public-facing explanation should be visual, scientific, and modern.
- The expected approved inputs include LAS, CSV, Excel-style well-log headers,
  depth/location/log parameters, overburden context, and core data.
- The project should support detection, saturation, and sweet-spot screening.
- The ML framing should be physics constrained and should not depend on one
  simple threshold.
- Baselines are useful, but the project can use stronger models after the data
  and validation plan are confirmed.
- The website is lower priority than the Word document and PowerPoint. For this
  pass, the website only matters as an app/runtime skeleton and visual source.
- The deck should be about nine slides, visually dense, scientific, and
  government-ready.
- The Word document should explain the choices, method, and reasoning in more
  detail than the slides.

## 2026-06-09 - Word and PowerPoint Structure

Gmail message id: `19eae3dbcf315575`

Key requirements:

- The Word document needs a filled abstract and introduction.
- The introduction should be at least a page and should use planned-out
  sentences rather than topic-numbered fragments.
- Later Word sections can remain structured as an outline until real data and
  final outputs exist.
- The Word document should avoid bare bullet-heavy writing where full paragraphs
  are needed.
- Small Processing sketches or relevant source-backed visuals can support the
  document.
- The PowerPoint must remain a nine-slide deck:
  - Slide 1: about me, title, photo, drawing, and physical activities.
  - Slide 2: introduction to gas hydrates, what they are, and why they matter.
  - Slide 3: parameters and well-log scaffold.
  - Slide 4: ML methodology and architecture.
  - Slide 5: why the parameters and model choices matter.
  - Slide 6: geomechanics/equations/format cleanup.
  - Slides 7-8: map, discussion, results, and review logic.
  - Slide 9: conclusion.

## 2026-06-10 - New Changes and Instructions

Gmail message id: `19eb2f4c157c062b`

Key requirements:

- Set the website aside. The main goal is the slides and Word document.
- Use the ML paper and the ML Word notes as source material.
- Use Excel header/equation screenshots only as schema and formula references,
  not as public data rows.
- Visually describe each parameter and the property it measures.
- Build a node/edge style ML architecture where every parameter has a clear
  source, unit, QC rule, and model role.
- Inputs come from approved well-log headers and core context.
- Depth should not be normalized the same way as the other privacy-controlled
  features. Depth is the alignment/context axis.
- Other numerical fields should use train-only normalization or preprocessing
  once approved runtime data exists.
- Create reusable parameter symbols and icons that can carry through the deck.
- The audience should understand symbols such as `V_p`, `V_s`, `AI`, `GR`, and
  `R_t` without needing to know petrophysics already.
- Plan the visuals and source logic before implementing the next deck.

## 2026-06-11 - ML Sources

Gmail message id: `19eb8291ad5c05c9`

Local source folder:
`references/ml-sources/2026-06-11/`

Attached files:

- `s10596-022-10151-9.pdf`
- `ML_Project_Reference_and_CreditScoreV4_Case_Notes.docx`

Key requirements:

- Read and integrate the ML source specifics into the topics instead of using
  generic ML language.
- Use the paper as the direct gas-hydrate/well-log ML anchor.
- Use the ML notes for validation, leakage prevention, data-quality, baseline,
  calibration, and monitoring language.
- Do not treat the ML notes as hydrate science evidence.

## 2026-06-11 - PowerPoint Visual Feedback

Gmail message id: `19eb912268782bbc`

Key requirements:

- Use Processing/code-rendered visuals. Avoid generic PowerPoint visuals.
- Slide 2 needs source-backed gas-hydrate visuals, not the old structural
  explorer screenshot as the main image.
- Slide 2 should use USGS gas-hydrate definition/source context, a
  pressure-temperature stability diagram, DOE/NETL context, a 2D Alaska/North
  Slope map, and the newer structural explorer only as supporting context.
- Slide 2 should explain the structural legend and make methane hydrate the
  target explicit.
- Slide 3 has too many parameters and too much text. It needs larger visuals,
  correct symbols, and parameter-specific imagery or icons.
- Slide 4 ML architecture needs clearer line meaning. Approved logs should feed
  parameter icon chips, each parameter should connect to its own QC/unit/source
  gates, and the gates should flow into feature engineering, target registry,
  validation, models, and outputs.
- Slide 5 needs visuals showing behavior in clean sand, shale, gas, hydrate,
  bad hole, and other false-positive cases.
- Slide 6 needs better formatting and correct equation/symbol handling.
- All slides need the right sources, clearer visual hierarchy, and stronger ML
  pipeline detail.

## Current User Direction

Latest working direction:

- Work on the slides and Word document again.
- First make a clear plan based on goals and sources.
- Make sure the ML source coverage is complete enough to explain the pipeline
  and science.
- Look at the slides, the Word document, and the format necessities from past
  emails.
- Forget the website for now except for apps/runtime skeletons and visuals that
  support the deliverables.
- Put the source rules, format rules, and working plan in a directory that can
  guide future execution.
