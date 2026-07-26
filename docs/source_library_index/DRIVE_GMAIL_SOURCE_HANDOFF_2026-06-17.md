# Drive and Gmail Source Handoff - 2026-06-17

## Drive Folder Tree

Root:

- `North Slope Gas Hydrates`
- URL: https://drive.google.com/drive/folders/1OE2NhaxdtP6pxRJh-BoRV_I8jxyeEl0Y

Intake:

- `source_intake_2026-06-17`
- URL: https://drive.google.com/drive/folders/1J6LzcDIUGM3TgZ34MA4_FezkvEb0S-Wp

Subfolders:

- `00_inbox_from_phone` - Gmail attachments and phone-uploaded intake items.
- `01_raw_pdfs` - Canonically named raw source PDFs. Drive-only by default.
- `02_source_screenshots` - Source-title screenshots and visual provenance captures.
- `03_extracted_figures` - Future extracted/redrawn figure working area after license review.
- `04_source_notes` - Future source reading notes.
- `05_public_safe_project_updates` - Public-safe manifests, prompts, and summaries suitable for repo mirroring.
- `99_do_not_push_restricted_or_unclear` - Holding area for uncertain, restricted, or license-unclear material.

## Gmail Thread

- Subject: `new paps`
- Message ID: `19ed80c3c8baedbe`
- Status: draft
- Action taken: attachments saved to Drive; draft was not sent.

Attachments:

| Gmail attachment | Size | Verified source | Drive destination |
| --- | ---: | --- | --- |
| `sign2019.pdf` | 2,458,966 bytes | Lijith, Malagar, and Singh 2019, "A comprehensive review on the geomechanical properties of gas hydrate bearing sediments," DOI `10.1016/j.marpetgeo.2019.03.024` | https://drive.google.com/file/d/1WdqEPRLpKkb80TicUnUZpS_ouVv9aN5U/view?usp=drivesdk |
| `falahat.pdf` | 7,395,386 bytes | Dalvand and Falahat 2021, "A new rock physics model to estimate shear velocity log," DOI `10.1016/j.petrol.2020.107697` | https://drive.google.com/file/d/1eEThqNAYYt4BU5PsNnVHkBGgE92zjgAh/view?usp=drivesdk |

## Drive Raw PDF Copy Map

| Original Drive/root file | Canonical file | Intake folder | URL |
| --- | --- | --- | --- |
| `collet2019.pdf` | `collett_boswell_waite_etal_2019_nghp02_scientific_results_india_marpetgeo.pdf` | `01_raw_pdfs` | https://drive.google.com/file/d/1I9fhphoECaD01hCHcZpuaQXx1lhkgymh/view?usp=drivesdk |
| `Estimating_Compressional_Velocity_and_Bulk_Density.pdf` | `naim_cook_moortgat_2023_vp_rhob_prediction_marine_hydrates_energies.pdf` | `01_raw_pdfs` | https://drive.google.com/file/d/11VQWqSuNjjei_gyTFsr3XkllBqoft-T4/view?usp=drivesdk |
| `acs.energyfuels.5c05321.pdf` | `yoneda_etal_2026_ans_hydrate02_nmr_permeability_energyfuels.pdf` | `01_raw_pdfs` | https://drive.google.com/file/d/13_PITIHxLh2jUNvwzhymHUYb_UJyei_0/view?usp=drivesdk |
| `main.pdf` | `tian_etal_2023_comparative_ml_hydrate_identification_geoenergy.pdf` | `01_raw_pdfs` | https://drive.google.com/file/d/1esAJBUaOXeUYmjYMqeioDM07HaCIEdd9/view?usp=drivesdk |
| `acs.energyfuels.5c06115.pdf` | `aung_etal_2026_ans_lwd_data_acquisition_energyfuels.pdf` | `01_raw_pdfs` | https://drive.google.com/file/d/1Sov0JhDwTVN90RmIJ5rIm8ZODg6j7nnM/view?usp=drivesdk |
| `energies-13-06536-v2.pdf` | `li_liu_2020_lstm_hydrate_saturation_energies.pdf` | `01_raw_pdfs` | https://drive.google.com/file/d/1PsyuuV4FGB0QvwH2nljJEQg_9XpEnjVc/view?usp=drivesdk |

## Screenshot Handoff

Expected local screenshot folder:

- `C:\Users\gargi\OneDrive\Pictures\Screenshots`

This folder was not available on the current machine. The Drive folder `02_source_screenshots` is ready for later upload from the laptop or synced OneDrive.

## Public-Safe Repo Files

The GitHub-safe intake record is:

- `docs/source_library_index/source_inventory_2026-06-17.csv`
- `docs/source_library_index/SOURCE_ORGANIZATION_REPORT_2026-06-17.md`
- `docs/source_library_index/SOURCE_GAPS_AND_DOWNLOADS_2026-06-17.md`
- `docs/source_library_index/DRIVE_GMAIL_SOURCE_HANDOFF_2026-06-17.md`

## Operating Rules

- Do not send the Gmail draft unless the user explicitly asks.
- Do not push raw PDFs to GitHub unless license, file size, and public-safe status are explicitly approved.
- Keep unclear source material in `99_do_not_push_restricted_or_unclear`.
- Use `01_raw_pdfs` as the canonical Drive PDF location.
- Use GitHub for source manifests, source maps, prompts, public-safe notes, and derived assets only.
- Do not expose approved well-log rows, restricted screenshots, row-level predictions, fitted models, populated runtime configs, or sensitive DOE outputs.

## Next Handoff Actions

1. Add the missing source-title screenshots to `02_source_screenshots`.
2. Locate Singh, Seol, and Myshakin 2020 and Rajabi et al. 2023.
3. Check for Chong et al. 2024 supplementary files.
4. Add short source notes in `04_source_notes` after reading each PDF.
5. Extract or redraw figures only after checking license and citation requirements.
