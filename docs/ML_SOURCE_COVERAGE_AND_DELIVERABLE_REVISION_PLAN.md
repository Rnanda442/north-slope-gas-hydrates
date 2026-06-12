# ML Source Coverage and Deliverable Revision Plan

Created: 2026-06-12

## Purpose

Before the next PowerPoint or Word edit, use this plan to keep every ML and
hydrate-science claim traceable. The goal is to make the deck and Word document
look polished while also making the science defensible.

The revision should not add approved well-log rows, core rows, restricted well
identifiers, trained model outputs, populated runtime settings, or sensitive
derived results to the public repository or public Drive deck.

## Current Coverage Verdict

The current source base is strong for gas-hydrate system science, North Slope
context, well-log interpretation, and public/runtime data-boundary rules.

The current source base is adequate but not complete for ML. Chong et al. (2022)
is the direct permafrost/North Slope ANN saturation anchor. To make the ML
pipeline feel fully covered in the Word document and the slide deck, the next
pass should add a small comparative ML tier:

- Singh et al. (2021) for neural-network/SGD saturation prediction from optimal
  well-log sets.
- Chong et al. (2024), the USGS/Interpretation offshore India ML paper, for
  occurrence plus saturation prediction and balanced-accuracy framing.
- The local ML Project Reference Notes for general ML controls only:
  baseline-first modeling, leakage-safe preprocessing, validation design,
  calibration, drift/data-quality checks, and monitoring language.

These comparative sources should support method design, not North Slope field
truth. North Slope occurrence, reservoir, and saturation claims should still be
anchored to North Slope sources such as Lee and Collett (2011), Haines et al.
(2022), Collett et al. (2019), and Zyrianova et al. (2024).

## Claim-to-Source Matrix

| Claim area | Primary source support | Deliverable use | Guardrail |
|---|---|---|---|
| What gas hydrate is | USGS gas hydrate FAQ/primer; NETL methane hydrate primer | Slide 2 and Word introduction | Keep methane hydrate target explicit; do not generalize to every hydrate gas |
| North Slope resource context | USGS FS 2019-3037; DOE/NETL North Slope hydrate pages | Slide 2, conclusion, Word introduction | Resource scale does not prove interval occurrence |
| Stability window | USGS OF 96-272 and North Slope assessment/stability sources | Slide 2 and methods framing | Stability is necessary, not proof |
| Petroleum-system controls | USGS SIR 2008-5175; Zyrianova et al. (2024); source matrix | Slide 7, Word discussion | Map context guides screening; logs/core decide occurrence |
| Reservoir quality controls | Zyrianova et al. (2024); Helmold and LePain (2023); local overburden docs | Slides 5-7, Word discussion | Reservoir quality, saturation, and producibility stay separate |
| Well-log hydrate response | Lee and Collett (2011); Haines et al. (2022); USGS well-log characterization | Slides 3, 5, 6; Word parameters/methods | High resistivity or high velocity alone is not a hydrate label |
| Feature equations | `docs/WELL_LOG_REQUIREMENTS_MAP.md`; `dashboard/runtime/feature_engineering.py`; local equation/range docs | Slides 3-6 and Word methodology | Formula variables must be named; target fields stay out of inputs |
| Direct permafrost ML analogy | Chong et al. (2022) PDF in `references/ml-sources/2026-06-11/` | Slide 4, Slide 5, Word ML framework | Use as an analogue; do not copy its metrics as this project's results |
| Comparative ML methods | Singh et al. (2021); Chong et al. (2024) USGS/Interpretation offshore India ML page | Word ML literature paragraph; slide notes or compact source callout | Comparative/marine sources support model choice only, not North Slope calibration |
| General ML controls | `ML_Project_Reference_and_CreditScoreV4_Case_Notes.docx` | Word validation/error section; slide 4 and 8 language | Treat as methodology notes, not hydrate science evidence |
| Data boundary and leakage | Project context, runtime skeleton, requirements map, ML notes | Every slide and Word methods section | No approved data or answer columns enter public visuals |

## Source Status

### Already Local and Usable

- `references/ml-sources/2026-06-11/s10596-022-10151-9.pdf`
  - Direct ML anchor for gas-hydrate saturation prediction in permafrost
    settings, including Alaska North Slope and Mallik.
- `references/ml-sources/2026-06-11/ML_Project_Reference_and_CreditScoreV4_Case_Notes.docx`
  - General ML workflow controls: baseline-first modeling, leakage-safe
    preprocessing, validation design, data-quality checks, calibration, and
    monitoring.
- `docs/source_library_index/source_index.md`
  - Indexed project source inventory and extracted orientations.
- `docs/SWEET_SPOT_SOURCE_MATRIX.md`
  - Primary science source tiers and source-use rules.
- `docs/WELL_LOG_REQUIREMENTS_MAP.md`
  - Header roles, target-leakage rules, unresolved target questions, and
    synthetic-data boundary.
- `docs/project_blueprints/ml_parameter_effect_tree.csv`
  - Parameter family, physical meaning, caveat, and ML role matrix.
- `docs/ML_VISUAL_ARCHITECTURE_PLAN.md`
  - Knowledge-graph, decision-tree, leakage-barrier, and whole-well validation
    visual contracts.

### Add or Cite in the Next Source Pass

These do not need to dominate the deck, but they should be recorded in the Word
references and source matrix before claiming that the ML method is fully
covered:

- Singh et al. (2021), `Prediction of gas hydrate saturation using machine
  learning and optimal set of well-logs`, DOI `10.1007/s10596-020-10004-3`.
- Chong et al. (2024), `Machine learning application to assess occurrence and
  saturations of methane hydrate in marine deposits offshore India`.
- USGS well-log characterization page for the resistivity/acoustic logging
  interpretation basis.

## Word Document Revision Plan

The Word document should read like a methods-and-source-backed research plan,
not like speaker notes for the slides.

1. Abstract
   - Keep the project objective crisp: predict occurrence and saturation from
     approved North Slope logs/core while keeping public visuals synthetic.
   - Do not claim model results yet.

2. Introduction
   - Use USGS/DOE/NETL for hydrate definition, North Slope resource context, and
     why reservoir characterization matters.
   - Add one sentence that the North Slope is a system problem: stability,
     reservoir sand, charge, structure, log response, and calibration must
     overlap.

3. Source Coverage and Evidence Base
   - Add a short subsection that separates primary North Slope science,
     comparative ML papers, project synthesis docs, and general ML methodology
     notes.
   - This prevents a reviewer from thinking all sources have the same evidence
     weight.

4. Parameters
   - Rebuild around the parameter families from
     `ml_parameter_effect_tree.csv`.
   - For every family, use the same grammar:
     `measures`, `hydrate use`, `caveats`, `ML role`, `source basis`.

5. Methodology
   - Show the flow:
     approved data intake -> schema/unit mapping -> depth alignment -> QC gates
     -> feature engineering -> target registry -> train-only preprocessing ->
     model ladder -> validation -> outputs.
   - Define all symbols used in equations.

6. ML Framework
   - Place Chong et al. as the direct permafrost ANN analogue.
   - Add Singh et al. and Chong et al. (2024) as comparative ML support.
   - Explain why the project will still use complete-well validation and
     leakage-safe preprocessing rather than assuming random row splits are
     enough.

7. Error and Validation
   - Make this section stronger than a typical student project:
     target leakage, row leakage, bad-hole intervals, unit conversion, missing
     NMR/Vs, gas/ice/cement/shale mimics, calibration, residuals by well, and
     drift or out-of-distribution review.

8. Results and Discussion Plan
   - Leave real results blank until approved data exist.
   - Define exactly what final figures will be: well-log panel, saturation
     curve, classification confusion matrix, regression residual plot,
     calibration plot, and geologic review map.

9. References
   - Use primary public sources for science claims.
   - Keep user-supplied synthesis and ML notes clearly labeled as project
     planning or methodology notes.

## PowerPoint Revision Plan

Keep exactly nine slides unless the user explicitly approves a new slide count.
The current Drive deck is visually revised; the next pass should focus on
source discipline and ML clarity.

| Slide | Role | Required source-backed improvement |
|---|---|---|
| 1 | Title/about me | Keep concise; do not add technical burden |
| 2 | Gas hydrate definition | Already redrawn; keep SEM-first visual and source-backed P-T/stability message |
| 3 | Parameters | Make each symbol/icon trace to a source family; use short labels and consistent grammar |
| 4 | ML architecture | Make the pipeline explicit: approved logs -> QC gates -> equations -> feature table -> target registry -> split -> model ladder -> outputs |
| 5 | Why parameters | Tie each behavior panel to a physical reason and a false-positive condition |
| 6 | Geomechanics | Define `AI`, `Vp/Vs`, `mu-rho`, `lambda-rho`, and what each can and cannot prove |
| 7 | Map context | Say the map is screening/context; do not imply hydrate confirmation from public GIS |
| 8 | Results/discussion | Show future output slots and error-review flags, not fake model results |
| 9 | Conclusion | End with source-backed workflow value and next data tasks: workbook, targets, approved validation |

## Required Visual/Language Rules

- Use `occurrence`, `saturation`, `reservoir quality`, `uncertainty`, and
  `producibility` as separate concepts.
- Use `S_h`, `Sgh`, `NMR_SAT`, phase labels, and final rankings as locked
  labels/outputs, not input features.
- Never show random-row validation as the final standard. Use complete-well or
  compartment holdouts.
- Never show actual model metrics until approved-data validation has happened.
- Keep source footers short on slides; put detailed citations in the Word doc
  and source plan.
- Comparative ML sources can justify algorithm choices, but North Slope
  occurrence and reservoir claims need North Slope sources.

## Execution Order For The Next Pass

1. Finalize the source matrix in this document and add any missing comparative
   ML source citations to the Word references.
2. Update the Word builder first because it is the detailed source-backed
   methods document.
3. Update the PowerPoint builder second, using the Word plan as the authority.
4. Regenerate local DOCX/PPTX.
5. Verify the PPTX has exactly nine slides and inspect any changed slide images.
6. Upload or replace the Drive files only after local verification.
7. Verify Google-rendered thumbnails for all changed slides.
8. Run tests if code/builders changed; at minimum run `git diff --check` after
   documentation-only edits.

## Open Questions Before Results Claims

These must remain visible as blockers, not hidden assumptions:

1. Which field is the authoritative hydrate-saturation target?
2. Is saturation supplied, NMR-derived, core-calibrated, interpreted, or a
   combination?
3. Are saturation values fractions or percentages?
4. Which phase labels and uncertain-label conventions are supplied?
5. Which wells are known-label development wells, validation wells, locked-test
   wells, and prediction wells?
6. Are outcomes for prediction wells available later for blind evaluation?
7. What exact unit and alias mappings are used in the full workbook formulas?
8. Which intervals are excluded for bad-hole, missing curve, depth mismatch,
   or outlier reasons?
