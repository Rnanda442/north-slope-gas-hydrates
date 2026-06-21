# Header-Only Four-Well Workbook Mapping Done / Needed Handoff

## Prompts Worked On

- Prompt 15: Header-only four-well workbook mapping.
- This consolidated handoff combines the local exact-filename search with the public-safe visible-header mapping from committed screenshot manifests, source-summary tables, and header registries.
- It does not claim that the live DOE Excel workbook metadata has been re-read on this laptop.

## Evidence Boundary

- No approved workbook rows, cell values, row-level predictions, trained models, fitted scalers, raw screenshots, or private local workbook paths are committed here.
- The user reported a new self-email with screenshots for the four dataset headers, temperature gradient, and equations. Those screenshots are approved review material for Drive/OSL, but the raw images are excluded from GitHub.
- This report uses GitHub-safe committed evidence:
  - `docs/evidence/email_screenshots_2026_06_12/README.md`
  - `data/public_ml_products/approved_data_field_role_table_2026-06-15.csv`
  - `data/public_ml_products/approved_schema_coverage_matrix_2026-06-15.csv`
  - `dashboard/well_log_engine.py`
  - `docs/deliverable_status_inventory.md`

## Done

- Searched local `Documents`, `Downloads`, and `OneDrive` folders for the expected approved-runtime filenames:
  - `curated_dataset1.xlsx`
  - `curated_dataset2.xlsx`
  - `curated_dataset3.xlsx`
  - `wellnametodataset.txt`
- Confirmed this laptop does not have the expected curated workbook filenames available by exact-name search.
- Searched the repo for workbook mapping references, MTE/IGS/refined sheet metadata, and existing header-only plans.
- Confirmed a source-backed visible-header grouping for the current ML/log scaffold.
- Confirmed target-like and calibration-like fields that must stay out of predictors.
- Preserved `MTE`, `IGS`, `MTE_refined`, `IGS_refined`, `MLK`, and `ETG` as provenance questions unless a source explicitly verifies their role.
- Clarified that visible screenshot/header evidence is enough for slide scaffolding and public-safe data contracts, but not enough to call the actual workbook-to-well mapping final.

## Visible Header Mapping

| visible group | visible headers | current role | public-safe use | blocked or prohibited use | confidence | remaining question |
| --- | --- | --- | --- | --- | --- | --- |
| Depth and alignment | `DEPTH`, `DEPT`, `True Depth`, `Depth_ft`, `Depth (ft)`, `depths_unitD`, `depths_unitC`, `Depth correspondence at ML data` | index / QC / alignment | Show as depth-alignment and interval-registration metadata. | Do not expose row-level depths or create false precision around matching method. | high for header presence; medium for exact alignment meaning | What interpolation, unit conversion, or matching rule produced the refined depth correspondence? |
| Borehole quality | `caliper`, `CAL1`, `differential caliper` | measured QC | Use as bad-hole / washout QC context in the log scaffold. | Do not treat as hydrate evidence. | high | What reference hole size and units apply per workbook? |
| Lithology | `GR` | measured input / lithology cue | Use as clean-sand versus shale-rich context. | Do not use as proof of hydrate occurrence. | high | Confirm API units and local shale/sand calibration by well. |
| Density and porosity | `Rho_b`, `RHOB`, `Density_gpcc`, `Phi_porosity`, `phi_den`, `DPHI`, `NPHI`, `phi_neut`, `NMRPHI`, `phi_nmr` | measured or derived input family | Show density, neutron, density-porosity, and NMR-porosity as input-capable when independently measured. | Do not confuse `NMRPHI` / `phi_nmr` with `NMR_SAT`. | high for header presence; medium for unit convention | Confirm fraction versus percent for porosity fields by workbook. |
| Electrical response | `Rt`, `RES`, `Deep formation resistivity`, `AO90`, `AF90` | measured input or unresolved mnemonic | Use `Rt`/`RES` as resistivity input/context when units and tool channel are confirmed. | Keep `AO90` and `AF90` blocked until the tool mnemonic is verified. | high for header presence; medium for mnemonic role | Is the screenshot/header spelling `AO90` or `A090`, and what tool channel does it represent? |
| Elastic response | `Vp`, `VP`, `VELP`, `Vs`, `VS`, `VS1` | measured or supplied velocity family | Use for sonic/elastic context and derived attributes when units are standardized. | Do not infer hydrate from velocity alone. | high for header presence; medium for unit convention | Confirm whether velocities are measured, supplied, or calculated in each workbook. |
| Derived elastic attributes | `Ratio Vp/Vs`, `Impedance` | derived feature family | Use as explainable derived attributes in Slide 3 / equation slides. | Do not present derived features as cleaner than their density/velocity inputs. | high for header presence | Should stored ratio/impedance be trusted or recalculated from canonical `Vp`, `Vs`, and density? |
| Saturation / labels | `Sgh`, `S_h`, `Sh`, `Hydrate Saturation`, `NMR_SAT` | target-only / calibration / validation | Use only as supervised target, calibration, validation, or post-prediction review labels. | Never put these in `X_allowed` predictors, feature normalization, ranking inputs, or slide language implying proof by stability/log response alone. | high | Which saturation field is authoritative when multiple labels coexist? |
| Irreducible water / calibration | `Swr`, `S_wr` | calibration-reference unless proven otherwise | Mention only as calibration/reference context after source review. | Do not use as predictor until role is source-verified. | medium | Are these independent measured values, derived labels, or interpretation outputs? |

## Workbook / Case Identity Status

| name or label | evidence status | safe current wording | unresolved issue |
| --- | --- | --- | --- |
| `MTE` / `Well-MTE` | Public-safe notes support use as Mount Elbert / MTE context. | Use as a verified public-safe case label only where the cited notes support it. | Confirm exact approved workbook membership. |
| `IGS` / `Well-IGS` | Public-safe notes support use as Ignik Sikumi / IGS context. | Use as a verified public-safe case label only where the cited notes support it. | Confirm exact approved workbook membership. |
| `MTE_refined` | Visible as a refined/alignment sheet or stage in committed screenshot notes. | Treat as a refined processing/alignment view unless workbook metadata proves it is a separate well/case. | Is it a sheet, workbook, stage, or separate case? |
| `IGS_refined` | Visible as a refined/alignment sheet or stage in committed screenshot notes. | Treat as a refined processing/alignment view unless workbook metadata proves it is a separate well/case. | Is it a sheet, workbook, stage, or separate case? |
| `MLK` | Mentioned by the user as a suspected name; not verified in the committed header evidence inspected here. | Keep unresolved. | Does `MLK` appear in any header screenshot, workbook tab, source document, or well-name mapping file? |
| `ETG` | Mentioned by the user as a suspected name; public notes also warn it may be confused with Eileen Gas Hydrate Trend. | Keep unresolved unless a workbook/source explicitly uses it as a well/case name. | Is `ETG` a well/case alias, trend name, or shorthand? |
| `curated_dataset1.xlsx`, `curated_dataset2.xlsx`, `curated_dataset3.xlsx` | Runtime/runbook filenames; tests use synthetic fixture assumptions only. | Use as workbook placeholders until the DOE/PC header-only scan confirms actual membership. | Which sheets/cases/wells are inside each real workbook? |

## Still Needed

- Run Prompt 15 on the machine that has the real approved workbooks, inspecting only workbook metadata, sheet names, visible headers, named ranges, and safe workbook properties.
- Export only workbook metadata: sheet names, headers, named ranges, safe workbook properties, target-like headers, feature-like headers, and depth/alignment columns.
- Confirm whether the current active scope is four distinct wells, two named wells plus refined views, or three workbooks with four working cases.
- Confirm whether `MTE_refined`, `IGS_refined`, `MLK`, `ETG`, or other labels are wells, sheets, aliases, processing stages, or unresolved.
- Confirm the authoritative saturation target among `Sgh`, `S_h`, `Sh`, `Hydrate Saturation`, and `NMR_SAT`.
- Confirm units for porosity, velocities, resistivity, density, and saturation without exporting row values.

## Files / Assets

- Added this handoff report:
  - `docs/delegated_work/2026-06-19/header_only_four_well_workbook_mapping_done_needed.md`
- No raw screenshot, workbook, source PDF, or data-row asset was added.

## Branch / Commit

- Source branches:
  - `codex/prompts-14-17-20260619`
  - `codex/prompt15-visible-header-mapping-20260619`
- Final integration commit is recorded in the unified slide workspace branch.

## Slides Affected

- Slide 3: log signal, lithology, core/calibration evidence scaffold.
- Slide 4: ML architecture leakage guardrails and feature/target separation.
- Slide 5: equation/derived-attribute cards.
- Slide 6/7: evidence review and stability/context language.
- Slide 8: DOE export placeholders.
- Later final deck rebuild: editable labels should use these header groups and target-only guardrails.

## Main Codex Next Steps

- Use this report as the public-safe Prompt 15A header contract for slide scaffolding.
- Do not wait on raw rows to rebuild editable slide structure.
- Do not treat local Downloads workbook-like files as the active three curated DOE workbooks without user confirmation.
- Before final well naming or DOE-calibrated model claims, import the PC/DOE header-only workbook metadata output and update the identity/status table.
