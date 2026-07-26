# Source Gaps and Downloads - 2026-06-17

This note tracks source gaps after the Gmail/Drive intake pass. It is a GitHub-safe checklist only; it does not contain raw PDFs or restricted source material.

## Missing or Still Needed

| Source ID | Source | DOI or locator | Status | Why it matters | Next action |
| --- | --- | --- | --- | --- | --- |
| `SRC_NEW_001` | Singh, Seol, and Myshakin 2020, automated well-log processing and lithology classification | `10.2118/202477-PA` | Missing from this intake | Supports lithology-aware feature selection, well-log processing, and non-ML-audience explanation of why GR/resistivity/sonic families are grouped before modeling. | Locate PDF or formal source page; add to Drive `01_raw_pdfs` or `99_do_not_push_restricted_or_unclear` depending on license. |
| `SRC_NEW_003` | Rajabi et al. 2023, predicting shear wave velocity from conventional logs | `10.1007/s13202-022-01531-z` | Missing from this intake | Supports Vs imputation caveats and shows that missing sonic/shear logs require explicit validation before derived elastic features are trusted. | Locate PDF or source page; add metadata to source inventory once found. |
| `SRC_NEW_006` | Chong et al. 2024 offshore India supplementary materials | USGS publication page and supplement, if available | Not obtained in this intake | Could support model architecture, features, and occurrence/saturation output framing without claiming our own final results. | Search USGS page and publisher supplement; keep supplement Drive-only until license and size are checked. |
| `SCREENSHOT_GAP_001` | Source-title screenshots from `C:\Users\gargi\OneDrive\Pictures\Screenshots` | Local screenshot folder | Not available on this machine | Needed to connect phone/email source evidence to canonical source inventory. | Copy from the laptop or synced OneDrive into Drive `02_source_screenshots`. |
| `DOC_GAP_001` | `docs/SOURCE_ACCESS_MAP_2026-06-17.md` | Repo file | Not found in this checkout | Requested orientation/source-access context. | Recover from the authoritative repo/branch if it exists, or recreate from current handoff docs. |
| `DOC_GAP_002` | `docs/NEW_SOURCE_SCREENSHOT_INTAKE_2026-06-17.md` | Repo file | Not found in this checkout | Requested screenshot-intake status note. | Recover if available; otherwise use this note and the handoff file as the replacement source-intake record. |
| `DOC_GAP_003` | `docs/SOURCE_INTAKE_UPDATE_2026-06-17.md` | Repo file | Not found in this checkout | Requested source-intake update note. | Recover if available; otherwise use `SOURCE_ORGANIZATION_REPORT_2026-06-17.md`. |
| `PATH_GAP_001` | Requested repo path `C:\Users\gargi\Documents\AI powerpoint\north-slope-gas-hydrates` | Local path | Not available on this machine | User-provided primary path for the project on another PC/laptop. | Use the available Writwik checkout for this commit; compare with Gargi machine later if needed. |

## Sources Organized This Pass

These were located and placed in Drive:

- Lijith, Malagar, and Singh 2019 geomechanics review from Gmail attachment `sign2019.pdf`.
- Dalvand and Falahat 2021 shear velocity model from Gmail attachment `falahat.pdf`.
- Collett, Boswell, Waite et al. 2019 NGHP-02 scientific results from Drive file `collet2019.pdf`.
- Naim, Cook, and Moortgat 2023 Vp/RHOB prediction from Drive loose PDF.
- Yoneda et al. 2026 Alaska North Slope HYDRATE 02 NMR/permeability from Drive loose PDF.
- Tian et al. 2023 comparative ML hydrate identification from Drive loose PDF.
- Aung et al. 2026 Alaska North Slope LWD acquisition from Drive loose PDF.
- Li and Liu 2020 LSTM hydrate saturation from Drive loose PDF.

## GitHub Push Rules

- Raw PDFs stay Drive-only unless the user explicitly approves a license/size/public-safety exception.
- PDFs with unclear license, private provenance, or possible restrictions belong in Drive `99_do_not_push_restricted_or_unclear`.
- GitHub should contain manifests, notes, prompts, public-safe figures, and generated summaries only.
- The source inventory should be updated whenever a missing source is found or a canonical Drive copy changes.

## Highest Priority Next Downloads

1. Singh, Seol, and Myshakin 2020, `10.2118/202477-PA`.
2. Rajabi et al. 2023, `10.1007/s13202-022-01531-z`.
3. Chong et al. 2024 supplementary materials, if publicly obtainable.
4. Source-title screenshots from the Gargi OneDrive screenshot folder.
