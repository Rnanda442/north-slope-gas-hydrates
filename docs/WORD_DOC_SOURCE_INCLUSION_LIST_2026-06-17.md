# Word Doc Source Inclusion List - 2026-06-17

Purpose: source-backed checklist for the next North Slope gas hydrate Word document pass. This note is public-safe and contains no approved runtime rows, row-level predictions, fitted model output, or restricted well-log data.

## GitHub Rebase Check

- Local working folder checked: `C:\Users\Writwik\Documents\north-slope-gas-hydrates`
- Local branch: `main`
- Local HEAD before rebase/pull: `b23cb2a`
- Remote `origin/main` after fetch: `3ce22d7`
- Newer remote branch found: `origin/codex-v55-deck-20260617` at `635f1e8`
- Action taken: fetched all remotes and reviewed newer commits.
- Action not taken: no in-place rebase or pull was performed because the local checkout already has many uncommitted edits and untracked deliverables. Rebase should be done only after those changes are saved, stashed, committed, or moved to a clean worktree.

Remote changes to account for in the next Word/document pass:

- DOE three-dataset runtime pipeline and header inspection work.
- Model run tracker and mentor review dashboard work.
- Saturation feature matrix cleanup and target-leakage policy work.
- V5.5 Slide 2 source-visual rebuild.
- V5.5 Slide 3 signal-response deck branch update.

## Sources Checked From Gmail And Drive

| Source | Found in | Use in Word doc | Guardrail |
|---|---|---|---|
| Lijith, Malagar, and Singh, 2019, "A comprehensive review on the geomechanical properties of gas hydrate bearing sediments" | Gmail draft `new paps`, attachment `sign2019.pdf` | Add a geomechanics and producibility subsection: hydrate morphology, stiffness, strength, permeability reduction, dissociation risk, and why geomechanics matters after occurrence/saturation screening. | Use as general GHBS geomechanics support, not as North Slope project validation. Do not turn its saturation-strength ranges into project thresholds. |
| Dalvand and Falahat, 2021, "A new rock physics model to estimate shear velocity log" | Gmail draft `new paps`, attachment `falahat.pdf` | Add a measured-vs-estimated Vs subsection and an equation appendix note for elastic/rock-physics features. Explain why Vs is useful but must be provenance-tagged if estimated. | Do not use their case-study coefficients as North Slope equations. Missing-log adapters require mentor approval and validation. |
| `ML_Project_Reference_and_CreditScoreV4_Case_Notes.docx` | Gmail `ML sources` | Add a methodology-control box: baseline first, train-only preprocessing, leakage-safe split, data quality dimensions, drift/monitoring, and validation discipline. | Treat as project methodology guidance only, not as a research-paper citation. |
| Source screenshot share package | `docs/evidence/source_screenshot_share_2026_06_18/`, downloaded from Gmail message `19edbe9531662f2f` | Use as the packaged screenshot evidence layer for headers, target-only labels, equations, project objectives, and Slide 2 source visuals. | Screenshot files are evidence and planning inputs only, not formal manuscript sources. Do not transcribe row values or expose sensitive approved-data values. |
| Equation screenshots from June 9 | `docs/evidence/source_screenshot_share_2026_06_18/email_screenshots_2026_06_12/` | Use only to verify the equation list and variable explanations before regenerating the Word doc. | Screenshot filenames should not appear as formal manuscript sources. Cite the real paper/report sources behind the equations. |
| Current Word draft `North_Slope_Gas_Hydrate_Source_Backed_Research_Overview_2026-06-17.docx` | Gmail `New word doc update` | Use as the current six-page Word baseline. It already has the science-to-ML ladder, evidence hierarchy, parameter framework, target registry, model ladder, validation plan, and mentor decisions. | It still needs deeper equation detail and the new emailed papers integrated explicitly. |
| V5.5 Slide 3 Signal Response Update companion | Google Drive: <https://docs.google.com/document/d/1w_Ca7nYorJQpdq9IxbziKH57XXU8ELougIiQNN4lUc8> | Pull in the signal-response stack logic: stability/BGHS context, GR, caliper QC, porosity/RHOB, Rt, Vp, Vs/mu-rho, NMR/core, hydrate-compatible intervals, gas mimic intervals, and bad-hole intervals. | Keep as deck/document planning support. Use the cited papers and public source products as scientific sources. |
| North Slope Gas Hydrate Reservoir Characterization Research Overview 2026-06-15 | Google Drive: <https://docs.google.com/document/d/1J_6YWE18nfHqmEkifl-AFFgDXcOgglkwIfAtL4Fcaw4> | Use as a source-backed synthesis for parameter families, feature roles, model ladder, and references. | It is a project synthesis document, not independent scientific evidence. |
| Aung, Naito, Tano, Tamaki, and Boswell, 2026, ANS LWD data acquisition | Found through Drive synthesis text; DOI `10.1021/acs.energyfuels.5c06115` | Add a direct Alaska North Slope LWD section: STW/GDW/PTW-1/PTW-2 context, B1/D1 sands, GR/resistivity/density/neutron/sonic/NMR tool families, QC, NMR caveats, and completion-interval logic. | Do not treat source quick-look values or source intervals as this project's results. |
| Yoneda et al., 2026, HYDRATE 02 NMR T2 and permeability | Found through Drive synthesis text; DOI `10.1021/acs.energyfuels.5c05321` | Add NMR/permeability support: T2 distributions, bound/free fluid concepts, hydraulic-radius permeability model, hydrate reducing permeability, post-dissociation permeability context. | Permeability is producibility/context, not occurrence truth. Avoid source-paper model errors or results as project metrics. |
| Naim, Cook, and Moortgat, 2023, missing Vp/RHOB ML | Drive PDF/result, DOI `10.3390/en16237709` | Add an optional missing-log adapter subsection: predicting Vp or RHOB can be done in literature when logs are missing, but measured logs remain preferred. | Use only as background for possible adapters. Do not claim North Slope transferability without mentor approval and validation. |
| Tian et al., 2023, comparative hydrate identification ML | Drive synthesis/source text, DOI `10.1016/j.geoen.2023.211564` | Add model-ladder support for occurrence classification using velocity-sensitive features and tree/SVM/KNN/boosting comparisons. | Do not copy their ODP Hydrate Ridge metrics as project performance or North Slope calibration. |
| Li and Liu, 2020, LSTM saturation estimate | Drive synthesis/source text, DOI `10.3390/en13246536` | Mention sequence/depth-aware models as a future path if continuous labeled intervals support them. | Keep optional. Do not make LSTM the first model before leakage, split, and target authority are settled. |
| Chong et al., 2022 | Existing project ML source, DOI `10.1007/s10596-022-10151-9` | Keep as the direct permafrost-associated hydrate ML anchor for ANS/Mallik-style well-log ML workflow and ANN-style saturation modeling. | Do not copy its reported metrics as project metrics. |
| Chong et al., 2024 / USGS | Existing project source, <https://pubs.usgs.gov/publication/70250169> | Use to support separate occurrence and saturation model heads and ANN/Keras architecture language. | Method support only until approved North Slope runtime validation exists. |
| Singh, Seol, and Myshakin, 2021 | Existing project source, DOI `10.1007/s10596-020-10004-3` | Use to support feature-set thinking for saturation prediction from selected well logs. | Do not treat selected source features as final project features until approved headers and units are verified. |
| Lee and Collett, 2011 | Existing project source, USGS/public source page | Use for Mount Elbert saturation-from-well-logs context and Archie/log interpretation background. | Source method support, not project result. |
| Haines et al., 2022 | Existing project source, DOI `10.1021/acs.energyfuels.1c04100` | Use for Hydrate-01 gas hydrate occurrence, saturation estimates, reservoir characteristics, and calibration context. | Do not expose or imply restricted row-level project data. |
| Zyrianova, Collett, and Boswell, 2024 | Existing project source, <https://www.mdpi.com/2077-1312/12/3/472> | Use for Eileen Gas Hydrate Trend structural, stratigraphic, and reservoir controls. | Use as geologic context, not direct ML labels. |
| Collett et al., 2019 USGS North Slope assessment | Existing project source, DOI `10.3133/fs20193037` | Use for regional North Slope gas hydrate resource/context framing. | Regional context only, not project prediction validation. |

## Specific Things To Add Or Strengthen In The Word Doc

1. Add a short "What changed from the source review" paragraph near the front.
   - Mention that new emailed papers expand geomechanics and Vs/missing-log treatment.
   - Mention that newer GitHub commits add DOE three-dataset runtime, target-leakage cleanup, model tracking, and V5.5 source-backed visual logic.

2. Add a stronger "Direct Alaska North Slope source base" subsection.
   - Put Aung 2026, Yoneda 2026, Haines 2022, Lee and Collett 2011, Zyrianova 2024, and Collett/USGS sources in one table.
   - Explain what each source supports: logs, NMR/core, reservoir quality, stability/context, structural setting, or occurrence/saturation calibration.
   - Make clear that source examples are method anchors, not this project's trained results.

3. Add a "Geomechanics and producibility context" subsection.
   - Use Lijith et al. 2019 to explain hydrate-bearing sediment strength, stiffness, morphology, and dissociation risk.
   - Explain pore-filling, load-bearing, and cementing hydrate habits.
   - Explain that strength/stiffness/permeability are not occurrence labels, but they matter for reservoir interpretation and future production risk.

4. Add a "Measured vs estimated elastic variables" subsection.
   - Define measured inputs: Vp, Vs, RHOB, porosity, GR, Rt where present.
   - Define derived features: Vp/Vs, acoustic impedance, shear modulus, bulk modulus, Poisson's ratio, lambda-rho, mu-rho.
   - Use Dalvand and Falahat 2021 to support Vs estimation as a possible rock-physics/machine-learning problem.
   - State that estimated Vs or RHOB must carry a provenance flag and cannot be mixed silently with measured curves.

5. Add a "Missing-log adapter policy" subsection.
   - Use Naim et al. 2023 to show that Vp/RHOB prediction has literature support.
   - State that adapters are optional and validation-required.
   - Add a decision table: measured curve available, missing but estimable, missing and blocked.

6. Expand the equation appendix.
   - Pressure/depth equation and temperature-gradient equation for stability context.
   - Phase-boundary lookup logic for methane 5 ppt baseline.
   - Archie-style saturation as a physics baseline or calibration reference, not a leakage predictor when it defines target saturation.
   - Elastic equations: acoustic impedance, Vp/Vs, shear modulus, bulk modulus, Poisson's ratio, lambda-rho, mu-rho.
   - Rock-physics/Vs estimation equations only as optional adapter background.
   - NMR permeability concepts from Yoneda 2026, especially T2 distribution and hydraulic-radius model logic, with caveats.

7. Add a "Three-dataset approved-runtime draft" section if not already regenerated from the newest GitHub work.
   - Explain that the three curated Excel datasets are a controlled runtime package.
   - Explain header preservation, schema discovery, target-only saturation fields, leakage controls, train-only preprocessing, and external-score logic.
   - Keep target fields as Y-only: `Sgh`, `S_h`, `Sh`, `NMR_SAT`, `Hydrate Saturation`, `Swr`, `S_wr`, occurrence labels, and phase labels.
   - State that saturation values are expected as fractions on a 0-1 scale, with sheet-level runtime verification still required.

8. Add a visual/table for variable fingerprints.
   - Original header.
   - Unit as seen or inferred.
   - Canonical alias.
   - Role: measured input, derived feature, QC/context, alignment, target-only, calibration/reference, output, unresolved.
   - Feature-matrix permission.
   - Leakage risk.
   - Missingness/QC handling.
   - Source support.

9. Add a signal-response explanation.
   - Use the V5.5 slide 3 logic in prose: hydrate-compatible interpretation requires co-moving evidence, not one curve.
   - Clean sand plus high Rt plus stiffness/velocity response plus NMR/core support plus stability admissibility is stronger evidence.
   - High Rt alone is weak because free gas, ice, tight/cemented rock, salinity, invasion, and washout can mimic hydrate.

10. Add a "What we can claim now" and "What we cannot claim yet" box.
   - Can claim: source-backed workflow, public/approved boundary, schema readiness, target-leakage barrier, stability as context, DOE runtime path, and model architecture readiness.
   - Cannot claim: final hydrate occurrence predictions, final saturation estimates, final model performance, final stability top/base/thickness, or public release of approved runtime rows.

## Tables And Figures The Word Doc Should Include

- Evidence hierarchy table: direct ANS sources, direct permafrost ML, comparative hydrate ML, project synthesis.
- Direct ANS log/source table: GR, resistivity, density/neutron, sonic, NMR, caliper/QC, core.
- Variable fingerprint table.
- Target-only leakage table.
- Three-dataset runtime flow diagram.
- Equation-to-feature table.
- Signal-response stack diagram or simplified track-style figure.
- Missing-log adapter decision table.
- Public vs approved runtime boundary figure.
- Mentor decision table.

## Mentor-Facing Decisions Still To Keep Visible

- Which saturation target is authoritative when multiple labels exist in one sheet?
- Confirm every saturation target is stored as a fraction from 0 to 1.
- Which fields define occurrence: saturation threshold, interpreted phase labels, source occurrence calls, or mentor-reviewed intervals?
- Which wells become training, validation, locked-test, and prediction wells?
- Are MTE/IGS refined sheets confirmed as processing stages of the same source wells by workbook metadata?
- Are missing-log adapters allowed for Vp, Vs, RHOB, or other critical features?
- What caliper/washout policy is valid once bit size, units, and caliper coverage are verified?

## Guardrails For The Next Word Pass

- Do not cite internal source maps, prompts, screenshots, artifact indexes, or chat notes as scientific references.
- Do not expose approved data rows, row-level predictions, fitted models, populated runtime configs, or restricted identifiers.
- Do not treat public stability intervals as hydrate proof, occurrence labels, saturation, or final top/base/thickness.
- Do not copy source-paper metrics into project results.
- Do not use source-paper quick-look saturation values as this project's result.
- Do not let saturation-like columns enter the feature matrix.
- Do not silently mix measured logs and estimated adapter outputs.
- Keep the current claim as methods/readiness until approved data, target authority, and validation splits are locked.
