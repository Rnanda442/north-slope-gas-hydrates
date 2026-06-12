# Source Registry For Next Word and PowerPoint Pass

Created: 2026-06-12

This registry organizes the source pool by use. It points to source locations
instead of duplicating source PDFs/images into this directory.

## Source-Use Rule

Every public scientific claim should trace to a verified public or
project-classified source. Public slides and documents must not expose approved
well-log rows, core rows, restricted well identifiers, trained model outputs,
populated runtime settings, or sensitive derived outputs.

Use sources by evidence tier:

| Tier | Valid use | Do not use for |
|---|---|---|
| Primary North Slope science | North Slope hydrate occurrence, reservoir, log response, stability, resource context | Generic ML validation claims outside its scope |
| Direct gas-hydrate ML | Permafrost/well-log ML feature and workflow analogy | This project's future model metrics |
| Comparative ML | Model-choice support and validation framing | North Slope field truth |
| Project synthesis | Organizing equations, visual plans, and implementation requirements | Independent scientific confirmation |
| General ML notes | Leakage, validation, baseline, monitoring, and calibration language | Hydrate science evidence |
| Visual/public assets | Slide visuals and icons | Hidden data inference or quantitative claims |

## Email and User Instruction Provenance

| Source | Location | Use |
|---|---|---|
| Project constraint Q&A | Gmail message `19ea87193e412a0d` | Deliverable priority, audience, public/runtime boundary, ML goals |
| Word/PPT structure email | Gmail message `19eae3dbcf315575` | Nine-slide structure and Word formatting rules |
| New changes and instructions | Gmail message `19eb2f4c157c062b` | Website deprioritization, parameter visuals, ML architecture rules |
| ML sources email | Gmail message `19eb8291ad5c05c9` | ML source attachments and integration instruction |
| PowerPoint visual feedback | Gmail message `19eb912268782bbc` | Processing visuals, slide 2 redesign, parameter/architecture issues |

## Direct ML Sources

| Source | Location | Role |
|---|---|---|
| Chong et al. (2022), local PDF `s10596-022-10151-9.pdf` | `references/ml-sources/2026-06-11/` | Direct gas-hydrate ANN/well-log workflow anchor for permafrost-associated settings, feature families, NMR-density saturation target concept, QC/outlier screening, normalization, validation language |
| `ML_Project_Reference_and_CreditScoreV4_Case_Notes.docx` | `references/ml-sources/2026-06-11/` | General ML controls: baseline-first modeling, leakage-safe preprocessing, train-only transforms, validation design, data quality, calibration, monitoring |

## Comparative ML Sources To Add Or Cite

These sources should support ML method design only. They should not replace
North Slope calibration or be presented as North Slope field evidence.

Ready-to-cite strings, allowed deliverable language, and guardrails are recorded
in `docs/ML_CITATION_PACKET_FOR_DELIVERABLES.md`.

| Source | Current status | Use |
|---|---|---|
| Singh et al. (2021), `Prediction of gas hydrate saturation using machine learning and optimal set of well-logs`, DOI `10.1007/s10596-020-10004-3` | Verified in `docs/ML_CITATION_PACKET_FOR_DELIVERABLES.md` | Comparative ML saturation prediction and feature-set rationale |
| Chong et al. (2024), `Machine learning application to assess occurrence and saturations of methane hydrate in marine deposits offshore India`, DOI `10.1190/int-2023-0056.1` | Verified in `docs/ML_CITATION_PACKET_FOR_DELIVERABLES.md` | Comparative occurrence plus saturation prediction and balanced-accuracy framing |

## Primary North Slope Hydrate Science

Primary source matrix:
`docs/SWEET_SPOT_SOURCE_MATRIX.md`

Use these for hydrate occurrence, regional context, reservoir quality, log
response, and North Slope interpretation:

| Source | Main deliverable use |
|---|---|
| Chong et al. (2022) | Direct permafrost ML/well-log workflow analogue |
| USGS Alaska Gas Hydrate Assessment Team (2014) | Petroleum-system assessment, accumulations, faults, water contacts |
| Collett et al. (2019) | North Slope assessment-unit and resource framing |
| Collett, Boswell, and Zyrianova (2022) | Mount Elbert, Ignik Sikumi, and Hydrate-01 synthesis |
| Collett et al. (2011) | Permafrost-associated occurrence and development context |
| Lee and Collett (2011) | Mount Elbert NMR, sonic, resistivity, and saturation comparison |
| Haines et al. (2022) | Hydrate-01 sonic/resistivity/NMR saturation comparison |
| Zyrianova et al. (2024) | Eileen-trend compartmentalization, partial fill, water contacts |
| Lewis and Collett (2013) | Brookian well-log correlation and hydrate occurrence |
| Helmold and LePain (2023) | Nanushuk reservoir quality, depositional texture, burial controls |

## Slide 2 Gas Hydrate Definition and Context Sources

Source manifest:
`references/presentation-revision-2026-06-11/source_manifest.csv`

| ID | Source | URL or path | Slide/doc use |
|---|---|---|---|
| S02 | USGS gas hydrate crystals image | `https://www.usgs.gov/media/images/gas-hydrate-crystals` | SEM/photo texture for gas hydrate visual |
| S06 | USGS gas hydrate FAQ | `https://www.usgs.gov/faqs/what-are-gas-hydrates` | Plain-language definition |
| S07 | USGS gas hydrates primer | `https://www.usgs.gov/centers/whcmsc/science/gas-hydrates-primer` | Formation and occurrence context |
| S08 | USGS FS 2019-3037 | `https://pubs.usgs.gov/publication/fs20193037` | North Slope resource/context |
| S09 | DOE Alaska North Slope gas hydrates page | `https://www.energy.gov/hgeo/articles/alaska-north-slope-gas-hydrates-site-visit` | DOE/site visit/context |
| S10 | NETL North Slope gas hydrate reservoir characterization | `https://netl.doe.gov/node/6846` | Project and reservoir-characterization context |
| S22 | USGS phase-boundary open-file chapter | `https://pubs.usgs.gov/of/1996/of96-272/ch04.html` | Pressure-temperature stability sketch |
| S23 | NETL methane hydrate primer | `https://www.netl.doe.gov/sites/default/files/netl-file/2017-Methane-Hydrate-Primer%5B1%5D.pdf` | Hydrate stability and energy/security context |
| S24 | Central North Slope assessment-unit map | `raw_data/geology/CNS_AUs/CNS_AUs.jpg` | 2D North Slope context |

## Parameter and Well-Log Sources

| Source | Location | Use |
|---|---|---|
| USGS gamma log image | `https://www.usgs.gov/media/images/geophysical-logs-gamma-logs` | `GR` lithology/reservoir-gate visual |
| USGS caliper log image | `https://www.usgs.gov/media/images/geophysical-logs-caliper` | `CAL` bad-hole/QC visual |
| USGS fluid-resistivity image | `https://www.usgs.gov/media/images/geophysical-logs-fluid-resistivity-log` | `R_t` resistivity visual |
| USGS Hydrate-01 saturation estimates page | `https://www.usgs.gov/publications/gas-hydrate-saturation-estimates-gas-hydrate-occurrence-and-reservoir-characteristics` | Sonic, resistivity, NMR saturation and reservoir-quality logic |
| USGS NMR logging publication page | `https://pubs.usgs.gov/publication/70245367` | NMR porosity/pore-fluid wording |
| USGS selected borehole geophysical logging methods | `https://water.usgs.gov/ogw/bgas/logging_table.html` | Caliper/resistivity measured-property wording |
| ODP sonic tools chapter | `https://www-odp.tamu.edu/publications/149_IR/chap_02/c2_10.htm` | `V_p`, `V_s`, and acoustic tools wording |
| Runtime feature engineering | `dashboard/runtime/feature_engineering.py` | Implemented equation names and feature roles |
| Well-log requirements map | `docs/WELL_LOG_REQUIREMENTS_MAP.md` | Symbols, roles, target-leakage boundary |
| Parameter/effect tree | `docs/project_blueprints/ml_parameter_effect_tree.csv` | Icon families, caveats, model roles |

## Parameter Families To Carry Through Slides And Word

| Parameter family | Preferred symbols | Plain-language name | Role |
|---|---|---|---|
| Deep resistivity | `R_t`, `RES`, `A090`, `AF90` | Deep formation resistivity | Strong input feature, never standalone hydrate proof |
| NMR porosity/saturation support | `NMRPHI`, `phi_nmr`, `NMR_SAT` | NMR-visible pore fluid and derived saturation support | Input when measured, target/calibration only when derived |
| Compressional velocity | `V_p` | Compressional-wave velocity | Elastic input and source for derived stiffness features |
| Shear velocity | `V_s` | Shear-wave velocity | Elastic input, helps separate hydrate/free-gas behavior |
| Density/density porosity | `rho_b`, `RHOB`, `phi_D` | Bulk density and density porosity | Porosity and elastic equation input |
| Gamma ray | `GR` | Natural gamma radiation/lithology | Reservoir/lithology gate, not hydrate proof |
| Caliper | `CAL`, `DCAL` | Borehole diameter and washout | QC gate, not hydrate evidence |
| Derived elastic features | `V_p/V_s`, `AI`, `mu-rho`, `lambda-rho` | Elastic ratios and impedances | Derived features that inherit input errors |
| Core context | `phi_core`, `k`, lithology | Core porosity, permeability, and lithology | Calibration and validation |
| Depth/stability/overburden | `DEPTH`, `P`, `T`, overburden | Alignment and stability context | Context axis, not normalized like other curves |

## Internal App And Runtime Sources

These are allowed to guide the Word/PPT method explanation, but the website is
not the focus of this pass.

| Source | Use |
|---|---|
| `docs/runtime_skeleton_brief.md` | Approved-data skeleton, validation, target separation, app/runtime boundary |
| `dashboard/runtime/schemas.py` | Canonical fields, target provenance, validation types |
| `dashboard/runtime/loaders.py` | CSV/LAS adapter and curve-alias standardization |
| `dashboard/runtime/validation.py` | Readiness checks and complete-well split planning |
| `dashboard/runtime/feature_engineering.py` | Equations and reusable feature transforms |
| `dashboard/runtime/modeling.py` | Current rule-based placeholder and future ML adapter pattern |

## Visual Asset Sources

| Source group | Location | Use |
|---|---|---|
| Presentation visual package | `references/presentation-revision-2026-06-11/` | Source manifest, image assets, icon registry, slide instruction sheets |
| Generated slide panels | `docs/project_blueprints/presentation_assets/processing_revisions_2026_06_11/` | Current slide raster panels |
| Current structural explorer reference | `docs/project_blueprints/presentation_assets/streamlit_3d_context_v2.png` | Supporting slide 2/7 app-context visual only |
| Profile photo | `docs/project_blueprints/presentation_assets/rohan_profile_photo.jpg` | Slide 1 |
