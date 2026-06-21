# Four-Well Core, Lithology, NMR, And Location Source Hunt

Date: 2026-06-19

Scope: Prompt 14 source hunt for the current four-well / three-workbook ML
direction. This report uses repository-visible source indexes, public source
pages already saved in the repo, project handoff notes, and local source-folder
manifests. It does not inspect or export workbook rows.

## Search Summary

Searches covered:

- repo docs, data, references, dashboard code, and tests for `MTE`, `Mount
  Elbert`, `IGS`, `Ignik Sikumi`, `MLK`, `ETG`, `Eileen`, `Hydrate-01`,
  `HYDRATE 02`, `NMR`, `pressure core`, `permeability`, `lithology`, and
  `hydrate saturation`;
- `C:\Users\gargi\Downloads`, `C:\Users\gargi\OneDrive`, and project worktrees
  for source manifests, PDFs, DOCX source notes, and workbook-like files;
- exact filename search for `curated_dataset1.xlsx`, `curated_dataset2.xlsx`,
  `curated_dataset3.xlsx`, and `wellnametodataset.txt`.

Result:

- Strong formal source support exists for Mount Elbert / Well-MTE as a public
  North Slope gas-hydrate test-well context.
- Project metadata supports IGS as Ignik Sikumi / Well-IGS, but the strongest
  formal source still needs to be paired with the exact workbook/header mapping.
- Hydrate-01 and HYDRATE 02 are strong source-backed ANS calibration/context
  examples, but this pass did not prove they are active rows/cases in the three
  current workbooks.
- `MLK` and `ETG` remain unresolved as workbook aliases or well identifiers.
  `ETG` may mean Eileen Gas Hydrate Trend context, not a well, until header
  metadata proves otherwise.
- Exact curated workbook filenames were not found on this machine, so workbook
  membership remains a DOE desktop task.

## Source-Evidence Table

| verified well name | alias | source title | local/Drive path | page/figure/table | location/field/trend | lithology evidence | core/NMR/pressure-core evidence | saturation evidence | public-safe use | Drive/OSL-only restriction | remaining gap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Mount Elbert Gas Hydrate Stratigraphic Test Well | MTE; Well-MTE; Mt. Elbert | Lee and Collett 2011, "In-situ gas hydrate saturation estimated from various well logs at the Mount Elbert Gas Hydrate Stratigraphic Test Well, Alaska North Slope" | `references/hydrate-ml-physics-sources/2026-06-13/lee_collett_2011_mount_elbert_usgs_page.html`; `docs/source_library_index/source_manifest.csv` also lists `permafrost-mtelbert (1).pdf` in the local source library | USGS source page metadata and abstract; formal full PDF still useful for figure/page extraction | Milne Point / Eileen Gas Hydrate Trend style ANS context from the source page and project notes | Source page states cores and reservoir properties were acquired; project docs use this as cored/logged ANS case context | Source page states NMR, P-wave, S-wave, electrical resistivity, pore-water salinity, and cores were used | Source page supports NMR/velocity/resistivity saturation comparison; source values must stay citation context, not project results | Use as Slide 3 / Word anchor for complementary log and core calibration logic | Do not copy source figures or workbook rows without rights/data review | Confirm whether `curated_dataset1/2/3.xlsx` actually includes MTE and whether `MTE_refined` is a processing view or separate sheet/case |
| Ignik Sikumi Test Well | IGS; Well-IGS | Project source map and intake spec identify Well-IGS as Ignik Sikumi; Singh/NETL source is cited by project builder as MTE/IGS context | `docs/APPROVED_DATA_INTAKE_SPEC_2026-06-15.md`; `data/public_ml_products/approved_data_field_role_table_2026-06-15.csv`; `docs/source_map_for_slides.md`; `references/hydrate-ml-physics-sources/2026-06-13/singh_seol_myshakin_2021_prediction_gas_hydrate_saturation_ml_optimal_well_logs_osti.pdf` | `docs/source_map_for_slides.md` points to Mt. Elbert and Ignik Sikumi well-log figures in the Singh source; formal page/figure should be rechecked before slide use | Eileen Gas Hydrate Trend / Prudhoe Bay public context appears in project docs and public stability products | Not verified in this pass beyond project metadata and source-map pointers | Not verified in this pass beyond source-map pointer and workbook-header notes | Header-only project products show `Sh`, `Swr`, and saturation-family fields for IGS; no row values inspected | Use as a named candidate only after header-only DOE confirmation; use public map context cautiously | Do not expose workbook rows, private workbook paths, or row-level saturation values | Need exact source page/figure and DOE header mapping to confirm active workbook membership and evidence families |
| Hydrate-01 Stratigraphic Test Well | Hydrate-01 | Haines et al. 2022, "Gas hydrate saturation estimates, gas hydrate occurrence, and reservoir characteristics based on well log data from the Hydrate-01 Stratigraphic Test Well, Alaska North Slope" | `references/presentation-revision-2026-06-11/source_manifest.csv`; `references/hydrate-ml-physics-sources/2026-06-13/source_manifest.csv` notes user PDF still needed | USGS publication page in manifest; full PDF still needed for figure/page extraction | Alaska North Slope hydrate test-well context | Source title and project docs support reservoir-characteristics framing | Manifest/project notes support sonic, resistivity, and NMR comparison; full PDF needed for detailed figure extraction | Project docs cite high-saturation source context; do not reuse source values as project outputs | Use as Word/Slide 3 source anchor for log-response and NMR/core calibration discussion | Full article/PDF and figures should stay Drive/source-library until rights and size are reviewed | Confirm whether Hydrate-01 maps to active four-workbook scope or is only supporting source context |
| HYDRATE 02 Geo Data Well | Hydrate-02; HYDRATE 02 | Yoneda et al. 2026, "Permeability Evaluation of Hydrate Reservoirs Based on NMR T2 Relaxation Time from Both Log and Laboratory Data, Alaska North Slope HYDRATE 02 Geo Data Well" | `references/hydrate-ml-physics-sources/2026-06-13/google_drive_uploaded_sources_2026_06_13.md`; Drive PDF recorded there | Drive source PDF recorded; exact figures/tables not extracted in this pass | Alaska North Slope production-test / geo-data well context | Strong source candidate for reservoir/seal and lithology/permeability framing; Phillips/Waite/Yoneda/Haines 2026 lithology paper is still missing | Direct source role is NMR T2 from log and laboratory data, pressure-core/permeability/producibility calibration | Use for permeability and producibility framing, not occurrence labels | Use as Slide 3/Word anchor for NMR/core calibration strip and why permeability is not occurrence | Full PDF remains Drive-only; do not commit source figures or row-level values | Need exact page/table extraction and decision on whether HYDRATE 02 is one of the four active cases |
| Eileen Gas Hydrate Trend | ETG?; Eileen trend | Zyrianova, Collett, and Boswell 2024, "Characterization of the Structural-Stratigraphic and Reservoir Controls on the Occurrence of Gas Hydrates in the Eileen Gas Hydrate Trend, Alaska North Slope" | `references/hydrate-ml-physics-sources/2026-06-13/source_manifest.csv` lists URL and blocked download status | Public page/URL only; PDF not retrieved locally | Eileen Gas Hydrate Trend regional reservoir/structural context | Source role is reservoir and structural-stratigraphic controls | Not a direct workbook/core evidence source in this pass | Not a direct saturation target source in this pass | Use as regional context and map/cross-section source lead | Full PDF should remain source-library/Drive until retrieved and reviewed | Determine whether `ETG` is a trend abbreviation only or a workbook alias/case name |
| MLK | MLK | No formal source located in this pass | No source path verified | Not applicable | Unresolved | Unresolved | Unresolved | Unresolved | Do not use on slides as a verified well name yet | Header-only workbook mapping may reveal it, but this machine did not have the curated workbooks | Need exact header/sheet/source evidence |

## Source Leads To Recover Or Verify Next

| source lead | why it matters | next action |
|---|---|---|
| `curated_dataset1.xlsx`, `curated_dataset2.xlsx`, `curated_dataset3.xlsx`, `wellnametodataset.txt` | Required to prove the actual four active wells/cases and workbook membership | Run Prompt 15 on the DOE desktop where these files exist |
| Singh et al. 2021 / OSTI PDF | Project source map says it includes Mt. Elbert and Ignik Sikumi well-log figures | Reopen source and record exact pages/figures before Slide 3 |
| Collett, Boswell, and Zyrianova 2022 ANS terrestrial hydrate systems chapter | Project companion cites this as Mount Elbert, Ignik Sikumi, Hydrate-01 context | Retrieve/source-review exact chapter pages if it will support well-name claims |
| Haines et al. 2022 Hydrate-01 full article | Needed for exact sonic/resistivity/NMR and reservoir-characteristics figures | User/Drive/source-library PDF needed |
| Phillips/Waite/Yoneda/Haines et al. 2026 lithological-control paper | Likely strongest lithology/pressure-core source for HYDRATE 02 | User/Drive/source-library PDF needed |
| Aung et al. 2026 LWD source | Strongest current ANS logging/QC source | Extract exact log-suite and QC statements from Drive PDF before Slide 3 |

## Slide Implications

- Slide 3 should not label four specific active wells until Prompt 15 confirms
  workbook metadata.
- Use Mount Elbert as the clearest public example for multi-log saturation
  comparison with NMR, P/S velocity, resistivity, and core/reservoir context.
- Use HYDRATE 02 / Yoneda 2026 as the clearest NMR T2, pressure-core, and
  permeability calibration anchor.
- Treat Ignik Sikumi as a likely IGS public case-study context but still
  unresolved for exact workbook membership.
- Treat `MLK` and `ETG` as unresolved labels. If `ETG` appears on a slide, it
  should say Eileen Gas Hydrate Trend unless header metadata proves it is a
  well/case alias.

## Bottom Line

The source stack can support a strong four-well/case evidence framework, but
this pass does not prove the exact four active workbook wells. The next required
step is a DOE desktop header-only mapping of the three curated workbooks.
