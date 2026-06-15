# Hydrate ML and Physics Source Intake

Created: 2026-06-13

## Purpose

This folder collects public-source papers and source pages for the
science-to-ML logic ladder, hydrate signal interpretation, well-log QC, and
future Word/PowerPoint revision. It contains only public/open or official
source-page material. It does not contain approved runtime well-log rows, core
rows, restricted well identifiers, trained models, populated configs, or
sensitive derived outputs.

## Local Files Retrieved

| File | Status | Use |
|---|---|---|
| `singh_seol_myshakin_2021_prediction_gas_hydrate_saturation_ml_optimal_well_logs_osti.pdf` | Downloaded from OSTI | Comparative ML saturation source; explains limitations of resistivity/acoustic methods and use of routine logs against NMR-derived saturation |
| `chong_collett_creason_seol_myshakin_2024_occurrence_saturation_methane_hydrate_offshore_india_osti.pdf` | Downloaded from OSTI | Comparative ML source for separate occurrence classification and saturation regression, including pore-filling, fracture-filling, and no-hydrate labels |
| `chong_collett_creason_seol_myshakin_2024_usgs_page.html` | Official USGS publication page saved | Citation/source-page backup for Chong et al. 2024 |
| `cook_waite_2018_archie_saturation_exponent_usgs_page.html` | Official USGS publication page saved | Resistivity/Archie calibration source-page backup |
| `lee_collett_2011_mount_elbert_usgs_page.html` | Official USGS publication page saved | Mount Elbert ANS well-log source-page backup |

Already present elsewhere in the repo:

| File | Existing location | Use |
|---|---|---|
| `s10596-022-10151-9.pdf` | `references/ml-sources/2026-06-11/` | Direct permafrost hydrate ML anchor: ANS/Mallik, NMR-derived `Sgh`, caliper/washout screening, six well-log features, ANN workflow |

## Google Drive Source PDFs

On 2026-06-13, the user uploaded five additional papers to Google Drive. They
are recorded in `google_drive_uploaded_sources_2026_06_13.md` and should be
treated as source-library references without copying the PDFs into public Git.

The uploads cover:

- Aung et al. (2026), ANS extended-duration production-test LWD acquisition;
- Yoneda et al. (2026), ANS HYDRATE 02 NMR T2 permeability from log and core
  data;
- Tian et al. (2023), comparative hydrate/non-hydrate ML classification;
- Li and Liu (2020), comparative LSTM saturation prediction from well logs;
- Naim, Cook, and Moortgat (2023), comparative missing `V_p` and bulk-density
  log prediction.

## Not Downloaded

The following official or publisher URLs did not provide a downloadable PDF in
this session or returned a 403/access page. They remain usable as citations and
source leads, but the full PDFs should be supplied by the user or retrieved
through legitimate institutional/open-access routes if needed.

| Paper | Why not local yet |
|---|---|
| Lee and Collett (2011), Mount Elbert in-situ hydrate saturation | Official USGS page was saved; publisher PDF was not downloaded from a verified open source |
| Haines et al. (2022), Hydrate-01 saturation estimates | ACS/USGS access blocked direct retrieval in this session |
| Cook and Waite (2018), Archie saturation exponent | Official USGS page was saved; Wiley PDF endpoint returned an access page, not a PDF |
| Zyrianova, Collett, and Boswell (2024), Eileen Trend controls | MDPI blocked direct download from the local command-line session, though the public page was verified by web lookup |
| Li and Liu (2020), LSTM hydrate saturation | Drive PDF now recorded in `google_drive_uploaded_sources_2026_06_13.md`; not copied into Git |
| Naim, Cook, and Moortgat (2023), ML prediction of `V_p` and density logs | Drive PDF now recorded in `google_drive_uploaded_sources_2026_06_13.md`; not copied into Git |
| Tian et al. (2023), comparative ML hydrate identification | Drive PDF now recorded in `google_drive_uploaded_sources_2026_06_13.md`; not copied into Git |
| Xiao et al. (2026), Qilian Mountain permafrost ML comparison | Publisher full text not retrieved; useful permafrost comparison if user can provide |
| Zhu et al. (2023), hydrate morphology identification with ML | OUP PDF endpoint returned an access page, not a PDF |
| Aung et al. (2026), ANS extended-duration production test LWD acquisition | Drive PDF now recorded in `google_drive_uploaded_sources_2026_06_13.md`; not copied into Git |
| Phillips/Waite/Yoneda/Haines et al. (2026), HYDRATE 02 lithological control | Newly published/issue source; full text not retrieved |
| Haines (2026), pressure core and LWD physical property linkage | Newly published/issue source; full text not retrieved |

## Practical Use

For the next Word/PPT pass:

- Use Chong et al. (2022), Singh et al. (2021), and Chong et al. (2024) as the
  main ML-method stack.
- Use Lee and Collett (2011), Haines et al. (2022), Cook and Waite (2018), and
  Zyrianova et al. (2024) as the main hydrate-physics and North Slope
  interpretation stack once full text is available or source-page statements
  are sufficient.
- Treat marine and non-ANS papers as comparative method support, not North
  Slope field truth.
- Do not cite source-reported model metrics as this project's results.
