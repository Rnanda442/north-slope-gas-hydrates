# Format and Style Rules

Created: 2026-06-12

## Global Rules

- Treat the Word document as the detailed source-backed explanation.
- Treat the PowerPoint as visual communication for a DOE/internship audience.
- Keep public deliverables source-backed and public-safe.
- Do not show approved runtime data, restricted well identifiers, trained model
  results, populated local configs, or derived sensitive outputs.
- Use the website only as an app/runtime skeleton or source of reusable visuals,
  not as the main deliverable topic.

## Word Document Rules

- Fill the abstract and introduction with complete paragraphs.
- The introduction should explain what gas hydrates are, why the North Slope
  matters, why logs/core are needed, and why ML is useful but must be
  physically constrained.
- Avoid numbered topic lists in the introduction.
- Later sections can remain scaffolded until real approved data and final
  outputs exist.
- Add a source-coverage section that separates:
  - primary North Slope science;
  - direct gas-hydrate ML;
  - comparative ML methods;
  - project synthesis and equation notes;
  - general ML methodology notes.
- Parameter sections should use one repeated grammar:
  `measures`, `hydrate use`, `false positives`, `ML role`, `source basis`.
- The Word doc should explain why each model and validation choice is made.
- Results should be described as planned output types until approved-data
  validation exists.

## Slide Deck Rules

- Keep exactly 9 slides unless the user explicitly changes the count.
- Prefer larger visuals and fewer words.
- Use code-rendered/Processing-style visuals, diagrams, icons, charts, and
  source-backed imagery.
- Avoid generic PowerPoint clip-art, logo walls, and crowded text tables.
- Put a compact source footer or source chip on each technical slide.
- Use the same parameter icon/symbol system across slides 3-6.
- Use correct symbols:
  - `R_t` for deep resistivity;
  - `GR` for gamma ray;
  - `CAL` or `DCAL` for caliper/washout;
  - `V_p` and `V_s` for sonic velocities;
  - `rho_b` for bulk density;
  - `phi`, `phi_D`, `phi_nmr`, and `phi_core` for porosity forms;
  - `S_h` or `Sgh` for hydrate saturation;
  - `AI = rho_b * V_p` for acoustic impedance;
  - `V_p/V_s`, `mu-rho`, and `lambda-rho` for derived elastic features.
- If an equation-derived or target-derived field is shown, make it clear
  whether it is an input, derived feature, calibration target, or locked output.
- Use short visual labels, not full paragraph explanations on slides.

## Science Language Rules

- Separate these concepts:
  - occurrence;
  - saturation;
  - reservoir quality;
  - producibility;
  - uncertainty.
- Stability is an admissibility screen, not positive proof of hydrate.
- High resistivity is supportive only when clean sand, porosity, elastic, NMR,
  core, and QC evidence agree.
- Low gamma ray supports clean reservoir sand, not hydrate by itself.
- Caliper is a data-quality gate, not hydrate evidence.
- Core data calibrates and validates interpretations; sparse core should not be
  treated as continuous truth.
- Public map context screens where interpretation is plausible; direct logs and
  core decide interval-scale evidence.

## ML Rules

- Keep target fields locked out of model inputs:
  - hydrate saturation labels;
  - phase labels;
  - final rankings;
  - future known/prediction outcomes.
- Avoid random-row validation as the final standard. Use complete-well or
  compartment holdouts.
- Fit preprocessing only on training wells:
  - normalization;
  - imputation;
  - feature selection;
  - learned weights;
  - calibration.
- Depth is the alignment and context axis. It should not be normalized in the
  same way as privacy-controlled multivariable log features.
- Use baseline models for comparison, then advanced models only after leakage,
  validation, and calibration controls are explicit.
- Do not show model metrics as project results until approved-data validation
  has actually happened.
- Use Chong et al. (2022) as the direct gas-hydrate/well-log ML anchor.
- Use Singh et al. (2021) and Chong et al. (2024) as comparative ML support
  only after citation details are added to the Word reference list.

## Visual Architecture Rules

Slide 4 should show a real architecture, not a decorative pipeline.

Required flow:

```text
Approved logs and core context
-> parameter symbol chips
-> unit and alias mapping
-> QC gates by parameter
-> depth alignment
-> feature engineering and equations
-> target registry and leakage barrier
-> train-only preprocessing
-> complete-well split
-> baseline and advanced model ladder
-> occurrence, saturation, uncertainty, and review outputs
```

Each major connection should communicate a reason:

- parameter to QC gate: trust and usability;
- parameter to equation: derived physical feature;
- parameter to target registry: target-leakage protection;
- preprocessing to split: no future/validation leakage;
- model outputs to review: scientific interpretation, not automatic truth.

## Slide-Specific Rules

| Slide | Required rule |
|---|---|
| 1 | About me and title, not technical overload |
| 2 | Define methane hydrate with source-backed visual, P-T stability, North Slope context |
| 3 | Parameter icons/symbols, larger visuals, less text |
| 4 | Detailed ML architecture with meaningful connections |
| 5 | Parameter behavior in clean sand, shale, gas, hydrate, bad hole, and false positives |
| 6 | Equation/symbol cleanup and geomechanics feature meaning |
| 7 | Map as screening/context, not proof |
| 8 | Planned results and error review, no fake metrics |
| 9 | Source-backed conclusion and next data tasks |
