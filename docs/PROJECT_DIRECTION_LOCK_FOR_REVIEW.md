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

Current slide authority:

- `docs/project_blueprints/CURRENT_GMAIL_VISUAL_REVISION_9_SLIDE_North_Slope_Gas_Hydrate_Slides_2026-06-11.pptx`
- Source: Gmail message `19eba86da8752830`, subject `New pressy`, sent
  2026-06-12 01:30 CDT.
- Use this deck first for slide review and revision. Older tracked decks and
  builder outputs are context unless the user requests a scripted rebuild.

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

these scientific proofs are not held down by evidence and are not proofs, we need actual proof of this. and ranges and numbers and reasoning.

## ML Commitments

- Use complete-well or compartment holdouts, not random depth-row validation as
  the final standard. yes 
- Fit normalization, imputation, feature selection, and calibration on training
  wells only. it should be for all the data but your not getting acess to the data cus its clasified, what we are dooing is building what i need to bring bakc into the doe virtual desktop and im giving you the bare minimum for the builds and the paper and stuff, the results and everything will be done later by me personally cuz i cant share the data, but in the meantime i have the equations, the headers to the ecells seets where thedata we are getting is stored and ive normalized them except for the depth. Like the screenshots contain thhe project overview too so that should help withh readjustments hhere.
- Keep target-derived fields out of predictors.
im not sure what means i think we the excells we will get will have the target areas but we also need to know from the equations and hhow gas hydrates are constrained the areas where hydrates are valid. all those variables count for now in the training i think and the targeet variables in the test is what we are testing for yes.
- Use baselines for comparison before advanced models. i meann i dont think we are running any models here itself unless we create 71 csvs of fake data to test on. tat would be crazy.
- Do not report project model metrics until approved-data validation exists. im not sure what this means
- Use Chong et al. (2022) as the direct gas-hydrate/well-log ML anchor. yes this paper is essential for making the diagrams and visuals and explaining the pipeline ml structure 
- Use Singh et al. (2021) and Chong et al. (2024) as comparative ML method yes thhis one too
  support, not North Slope field truth.



## Data Boundary

Public repository and public Drive deliverables may include:

- Public GIS context. yea on open science lab my virtual desktop storing all that data
- Public USGS/DOE/NETL source references.
- Synthetic examples.
- Empty runtime schemas/adapters. 
- Source-backed diagrams and planning documents.

Public repository and public Drive deliverables must not include:

- Approved or restricted LAS/CSV/core rows. yea im just giving header data at the moment i dont plan to give any actual information out. so i wanna be able to either make a fake group of data sets with duplicate header formats and reasonable numbers to test. i think the main thing will be explaining the exact ranges for eachh paramter and whhy. and not just ranges but changes and what they represetnt in the north slope first. this should be done first. 
- Named restricted well identifiers. yea itll just be like dataset 1 dataset2 dataset 3 i have the real names and we will mapp them to the 3d structural explorer when we can but not right now.
- Populated runtime configs. not sure hwaat the rest means
- Trained models.
- Runtime logs or derived sensitive outputs.
- Personal visual assets unless the user explicitly approves public tracking.

## Open Decisions For User Review

Edit these directly:

1. Is the one-sentence project goal correct? the project overview screenshots is the exact overview of the project.
2. Should the deck stay exactly nine slides? yes the deck has to stay nine slides 
3. Should slide 1 include personal/about-me visuals in the repo, or only in
   Drive/local copies? the about me has to be there thhe new sldie deck we have you havnt seenn it yer but it starts with "gmail" its in google slides and just pushed into the repo is good structure jjust bad specifics and format and syntax that we will fix.
4. Resolved 2026-06-12: the Gmail visual revision PPTX is tracked in Git as the 
   current slide authority. Builders, source manifests, and public-safe exported
   panels remain tracked as provenance/rebuild support. yep
5. Is the work order correct: Word first, slides second, website third? yep
6. Should the website remain mostly app/runtime skeleton for now? yea everythhig should be skeletons thhat i can bring into doe anaconda environment from emailing it from my personal account to my doe account and opening it in anaconda and then like uploading the real data for it to run. 
7. Are the primary outputs correct: occurrence, saturation, uncertainty, and
   review/sweet-spot screening? yes 
8. Are any sources, equations, or ML claims missing before the next build? not sure but l diragram and pipeline needs to be fixed. 

## What Is Still Not Ready

- Full Excel workbook and formulas are not yet recovered in this official
  folder.  i sent an email with the screenshot and they should stored i nthe giithub push for access for both the laptop(this one) and PC
- Authoritative hydrate-saturation target is not confirmed. yea we need to use the equations and the sources for hydrates to first constrain  hydrates quanitatively. based on real sccience, and try to account for all the ecternal facters that could affect the parameters, and then we need to check hhow our logics line up withh the data since we do have gas hydrate saturaturation and the target variables for the datasets. 
- Phase labels and uncertain-label conventions are not confirmed.  yea they are not we need to build them with our paramter logiccs too
- Known-label, validation, locked-test, and prediction well lists are not
  confirmed. no i only have access to 3/71 datasets right now so i cant really give you that stuff. i do hhave the welll names for the 3 data sets and i would be able to give you that. 
- Approved-data model metrics do not exist yet.  yea we need to build those
- Public-safe policy for slide-1 personal visual assets needs user decision. i made te first slide for the newest slide version so slide one is ready. the rest of te slides are not.

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
