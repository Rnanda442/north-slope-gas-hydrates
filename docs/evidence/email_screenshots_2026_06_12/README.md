# Email Screenshot Evidence Manifest

Source email: `19ebdbee04125e4e`

Subject: `alaska north slope deliverable base`

Received/sent: 2026-06-12 16:31 CDT

Purpose: keep the Excel header screenshots, data examples, equation screenshots, and project-goal screenshots close to the North Slope app so the well-log scaffold can repeatedly reference the same source material.

## Screenshot Classification

| File | Type | Use |
| --- | --- | --- |
| `contact_sheet.png` | Contact sheet | Quick visual index of all screenshots in this email pull. |
| `screenshot_2026-06-05_131418.png` | Excel header / data contract | Primary header screenshot. Shows `DEPTH`, `Rho_b`, `Phi_porosity`, differential caliper removal, deep formation resistivity, `GR`, `Vs`, `Vp`, `Ratio Vp/Vs`, and impedance as ML inputs or preprocessing fields. |
| `screenshot_2026-06-05_131426.png` | Excel header / target contract | Continuation of the header screenshot. Shows `Vp`, `Ratio Vp/Vs`, `Impedance`, and `Sgh / NMR_SAT` marked as `GROUND TRUTH`. |
| `screenshot_2026-06-08_111056.png` | Excel sample table | MTE-style data view with `Depth_ft`, `Density_gpcc`, `phi_den`, `phi_nmr`, `S_h`, `S_wr`, `GR`, `phi_neut`, `CAL1`, `AO90`, `VELP`, `VS1`, and depth-unit columns. |
| `screenshot_2026-06-08_111108.png` | Excel sample table | IGS-style data view with `DEPT`, `RHOB`, `NPHI`, `DPHI`, `NMRPHI`, `GR`, `caliper`, `RES`, `VP`, `VS`, `Sh`, and `Swr`. |
| `screenshot_2026-06-08_111117.png` | Excel refined target table | `MTE_refined` view showing depth correspondence against ML data and `Sgh` labels. |
| `screenshot_2026-06-08_111124.png` | Excel refined target table | `IGS_refined` view showing `Depth (ft)` and hydrate saturation / `Sgh` label values. |
| `screenshot_2026-06-09_150342.png` | Equation screenshot | Geomechanical equation set for Young's modulus, Poisson's ratio, brittleness terms, mu-rho, lambda-rho, acoustic impedance, and shear impedance. |
| `screenshot_2026-06-09_150348.png` | Equation explanation screenshot | Text explaining brittleness and lambda-rho / mu-rho crossplot logic, and why GR is included as organic-content/lithology context. |
| `screenshot_2026-06-09_152213.png` | Project goal screenshot | Goal/vision screenshot for gas hydrate occurrence and saturation prediction using AI/ML on Alaska North Slope permafrost sediments. |
| `screenshot_2026-06-09_152220.png` | Project objective screenshot | Training/workflow objective screenshot: remove outliers, select depth intervals, process raw well-log data, use Keras, tune ANN, optimize, validate unseen data, and present graphical/tabular results. |

## Header Fields To Carry Forward

Measured and preprocessing fields:

- `DEPTH` / `True Depth` / `Depth_ft`
- `Rho_b` / `RHOB` / `Density_gpcc`
- `Phi_porosity` / `phi_den` / `DPHI`
- `NMRPHI` / `phi_nmr`
- `Differential Caliper` / `caliper` / `CAL1`
- `Deep formation resistivity` / `RES` / `AO90`
- `GR`
- `Vs` / `VS1`
- `Vp` / `VELP`
- `Ratio Vp/Vs`
- `Impedance`

Label or ground-truth fields:

- `Sgh`
- `S_h`
- `Sh`
- `NMR_SAT`
- `Hydrate Saturation`

Rule: label/ground-truth fields can supervise, score, calibrate, or validate models. They should not be engineered back into predictor inputs.

## Equation Set Captured

The equation screenshot includes:

- Young's modulus, `YM`
- Poisson's ratio, `PR`
- brittleness from Young's modulus, `BR_YM`
- brittleness from Poisson's ratio, `BR_PR`
- total brittleness, `BRIT_TOTAL`
- mu-rho / shear impedance term, `MR`
- lambda-rho term, `LR`

These should be placed in the future well-log scaffold as physics-derived features, not as standalone hydrate labels.

