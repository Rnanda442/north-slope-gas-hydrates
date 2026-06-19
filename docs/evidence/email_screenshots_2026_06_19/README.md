# Email Screenshot Header Manifest

Date indexed: 2026-06-19

Source email: self-email titled `screenshots`, sent/received 2026-06-19 00:35 America/Chicago. Body text says the attachments are screenshots for the four dataset headers, temperature gradient, and equations.

Raw attachment storage: `data/source_library/email_screenshot_headers_2026_06_19/`

The raw PNGs are intentionally kept in the ignored source-library folder because several screenshots show row-level workbook values or copyrighted source-paper text. GitHub carries this manifest and header-only summaries only.

## Screenshot Inventory

| screenshot file | what it is | visible workbook/sheet or source | GitHub-safe use | raw PNG handling |
|---|---|---|---|---|
| `Screenshot 2026-06-05 131418.png` | Header-only Excel row for log-feature roles | Unnamed workbook header strip | Header names and role labels only: `DEPTH`, `Rho_b`, `Phi_porosity`, `Differential Caliper`, `Deep formation resistivity`, `GR`, `Vs`, `Vp`, `Ratio Vp/Vs`, likely `Impedance`. | Local/ignored copy only. |
| `Screenshot 2026-06-05 131426.png` | Header-only continuation of the same feature/target strip | Unnamed workbook header strip | Confirms `Impedance` and target/calibration field `Sgh`/`NMR_SAT`; target-only, not predictor input. | Local/ignored copy only. |
| `Screenshot 2026-06-08 111056.png` | Excel sheet with headers and row values | Active sheet `MTE`; visible tabs `MTE`, `IGS`, `MTE_refined`, `IGS_refined` | Header-only mapping: `Depth_ft`, `Density_gpcc`, `phi_den`, `phi_nmr`, `S_h`, `S_wr`, `GR`, `phi_neut`, `CAL1`, `AO90`, `VELP`, `VS1`, `depths_unitD`, `depths_unitC`. `S_h` and `S_wr` are target/calibration fields. | Raw image stays local/ignored because it shows row-level values. |
| `Screenshot 2026-06-08 111108.png` | Excel sheet with headers and row values | Active sheet `IGS`; visible tabs `MTE`, `IGS`, `MTE_refined`, `IGS_refined` | Header-only mapping: `DEPT`, `RHOB`, `NPHI`, `DPHI`, `NMRPHI`, `GR`, `caliper`, `RES`, `VP`, `VS`, `Sh`, `Swr`. `Sh` and `Swr` are target/calibration fields. | Raw image stays local/ignored because it shows row-level values. |
| `Screenshot 2026-06-08 111117.png` | Refined target/alignment table with row values | Active sheet `MTE_refined` | Header-only mapping: `Unit D`, `Depth, ft`, `Sgh`, `Depth correspondence at ML data`, `Unit C`, `Depth, ft`, `Sgh`, `Depth correspondence at ML data`. This is a refined/processed MTE sheet, not a separate well by screenshot evidence. | Raw image stays local/ignored because it shows row-level values. |
| `Screenshot 2026-06-08 111124.png` | Refined target/alignment table with row values | Active sheet `IGS_refined` | Header-only mapping: `Depth (ft)`, `Hydrate Saturation`, `Sgh`. This is a refined/processed IGS sheet, not a separate well by screenshot evidence. | Raw image stays local/ignored because it shows row-level values. |
| `Screenshot 2026-06-09 150342.png` | Source-paper/equation screenshot | Geomechanical-equation source text | Public-safe inventory only: dynamic Young's modulus, dynamic Poisson's ratio, brittleness, mu-rho/shear impedance, lambda-rho equation families. | Raw image stays local/ignored because it is a source-paper screenshot. |
| `Screenshot 2026-06-16 151227.png` | Methane/hydrate dissociation-curve spreadsheet | Temperature/pressure curve table | Header-only/source inventory: methane temperature and hydrate pressure curve columns for CO2 mass-fraction scenarios. | Raw image stays local/ignored because it shows table values. |
| `Screenshot 2026-06-16 151236.png` | Continuation of methane/hydrate dissociation-curve spreadsheet | Temperature/pressure curve table | Same source/equation inventory group as `151227`; no new public header mapping. | Raw image stays local/ignored because it shows table values. |
| `Screenshot 2026-06-16 151241.png` | Continuation of methane/hydrate dissociation-curve spreadsheet | Temperature/pressure curve table | Same source/equation inventory group as `151227`; no new public header mapping. | Raw image stays local/ignored because it shows table values. |

## Workbook/Sheet Conclusions From Screenshots

| visible sheet | classification | suspected alias | evidence | target/calibration fields | predictor/header families |
|---|---|---|---|---|---|
| `MTE` | Actual workbook well sheet | Mount Elbert / Well-MTE | Active Excel tab in `Screenshot 2026-06-08 111056.png`. | `S_h`, `S_wr` | depth, density/RHOB, density porosity, NMR porosity, gamma ray, neutron porosity, caliper, resistivity, Vp, Vs, unit-depth helpers |
| `IGS` | Actual workbook well sheet | Ignik Sikumi / Well-IGS | Active Excel tab in `Screenshot 2026-06-08 111108.png`. | `Sh`, `Swr` | depth, RHOB, neutron porosity, density porosity, NMR porosity, gamma ray, caliper, resistivity, Vp, Vs |
| `MTE_refined` | Refined/processed MTE sheet | MTE processed target/depth-alignment sheet | Active Excel tab in `Screenshot 2026-06-08 111117.png`. | `Sgh` | unit/depth correspondence only; not an independent predictor sheet |
| `IGS_refined` | Refined/processed IGS sheet | IGS processed target/depth-alignment sheet | Active Excel tab in `Screenshot 2026-06-08 111124.png`. | `Hydrate Saturation`, `Sgh` | depth correspondence only; not an independent predictor sheet |

Screenshot-only conclusion: the latest email verifies two actual workbook well sheets (`MTE`, `IGS`) plus two refined/processed sheets (`MTE_refined`, `IGS_refined`). It does not by itself verify four independent workbook wells. Hydrate-01 and HYDRATE 02 are currently public source-case and well-location anchors unless separate header evidence confirms active workbook membership.

`MLK` and `ETG` were not visible in this latest screenshot set. Existing project docs treat `ETG` as Eileen Gas Hydrate Trend context unless future workbook/header evidence proves it is a well/case alias.

## Modeling Boundary

Target/calibration columns must not be listed as predictor inputs. Fields such as `S_h`, `Sh`, `Sgh`, `Hydrate Saturation`, `NMR_SAT`, `S_wr`, and `Swr` belong to label, calibration, validation, target, or post-model comparison workflows only.
