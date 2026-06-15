# Google Drive Uploaded Source PDFs

Recorded: 2026-06-13

## Purpose

The user uploaded five additional papers to Google Drive for use as project
sources. This file records the Drive source PDFs, their inferred citation
identity from connector text extraction, and their permitted use in the
North Slope Gas Hydrates project.

These Drive PDFs should be treated as source-library references. They should
not be confused with approved runtime well-log rows, core rows, restricted well
identifiers, trained models, populated configs, or project results.

## Drive Source PDFs

| Paper | Drive file | Project role | Guardrail |
|---|---|---|---|
| Aung, T.T., Naito, K., Tano, K., Tamaki, M., and Boswell, R., 2026, *Alaska North Slope Extended-Duration Gas Hydrate Production Test Site Logging-While-Drilling Data Acquisition*, Energy & Fuels, https://doi.org/10.1021/acs.energyfuels.5c06115 | `acs.energyfuels.5c06115.pdf`, `https://drive.google.com/file/d/13A_vps7WV84Mkhox2qvQV83GXUCGrp6-/view?usp=drivesdk` | Direct ANS LWD acquisition, QC, log suite, resistivity selection, sonic/NMR limitations, and completion-selection support | Use for current ANS logging workflow and QC logic; do not cite quick-look saturation values as this project's results |
| Yoneda, J., Hiruta, A., Oshima, M., Jin, Y., Ohtsuki, S., Arima, Y., Nakatsuka, Y., and Okinaka, N., 2026, *Permeability Evaluation of Hydrate Reservoirs Based on NMR T2 Relaxation Time from Both Log and Laboratory Data, Alaska North Slope HYDRATE 02 Geo Data Well*, Energy & Fuels, https://doi.org/10.1021/acs.energyfuels.5c05321 | `acs.energyfuels.5c05321.pdf`, `https://drive.google.com/file/d/1EYHhsdagBU32BRzE7ogZ5mxpPdjh-oIM/view?usp=drivesdk` | Direct ANS NMR, pressure-core, permeability, reservoir/seal, and producibility-calibration source | Use for NMR/core calibration and permeability/producibility framing; do not turn permeability into a hydrate occurrence label |
| Tian, D., Yang, S., Gong, Y., Geng, M., Li, Y., and Hu, G., 2023, *A Comparative Study of Machine Learning Methods for Gas Hydrate Identification*, Geoenergy Science and Engineering, v. 223, 211564, https://doi.org/10.1016/j.geoen.2023.211564 | `main.pdf`, `https://drive.google.com/file/d/17U0jJGUHsfALWfBX4AUBUBDXO50JB5S3/view?usp=drivesdk` | Comparative ML hydrate/non-hydrate classification source using `V_p` and `V_s` and multiple supervised algorithms | Use for method comparison and classification framing only; not ANS calibration or field truth |
| Li, C., and Liu, X., 2020, *Research on the Estimate of Gas Hydrate Saturation Based on LSTM Recurrent Neural Network*, Energies, v. 13, 6536, https://doi.org/10.3390/en13246536 | `energies-13-06536-v2.pdf`, `https://drive.google.com/file/d/1iCpzTKBPbs8q8OJaYMsNEVovaDhzP5m3/view?usp=drivesdk` | Comparative sequence/deep-learning source for saturation prediction from resistivity and acoustic velocity logs | Use to justify depth-sequence-aware models as optional future candidates; not primary ANS evidence |
| Naim, F., Cook, A.E., and Moortgat, J., 2023, *Estimating Compressional Velocity and Bulk Density Logs in Marine Gas Hydrates Using Machine Learning*, Energies, v. 16, 7709, https://doi.org/10.3390/en16237709 | `Estimating_Compressional_Velocity_and_Bulk_Density.pdf`, `https://drive.google.com/file/d/1946CbSu_kuR8rG1_6uyHx6sr2mpEh2Ll/view?usp=drivesdk` | Comparative missing-log and feature-completeness source for predicting `V_p` or bulk density from other logs | Use only for missing-curve imputation/model-adapter rationale; marine source, not ANS hydrate occurrence evidence |

## Source Implications

The five uploads strengthen three parts of the project:

- **Direct ANS workflow support:** Aung et al. (2026) and Yoneda et al.
  (2026) support the current LWD/NMR/core workflow, QC decisions, and
  reservoir/producibility framing.
- **Comparative ML method support:** Tian et al. (2023), Li and Liu (2020),
  and Naim et al. (2023) support classification, sequence models, and
  missing-log prediction as method options.
- **Guardrail support:** the sources reinforce the need to keep hydrate
  occurrence, saturation, permeability/producibility, and data-quality flags as
  separate concepts.

## Retrieval Notes

- The files were identified through Google Drive recent-file metadata and
  connector text extraction on 2026-06-13.
- The PDFs remain in Google Drive rather than being copied into the public Git
  repository.
- If a later deliverable uses exact figures, tables, or detailed excerpts from
  these PDFs, cite the paper and verify the relevant passage again from the
  Drive source.

