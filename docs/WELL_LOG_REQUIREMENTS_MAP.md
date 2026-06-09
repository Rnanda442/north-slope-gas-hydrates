# Well-Log Requirements Map

Last updated: 2026-06-09

## Purpose

Translate the recovered Excel header screenshots into explicit requirements for
the synthetic well-log scaffold and future authorized runtime.

The screenshots are layout and schema references only. Their numerical values
were normalized by the user and must not be treated as original well
measurements, scientific calibration values, or model-training records.

## Source References

The header specification was derived from six normalized screenshots attached
to the user's self-sent Gmail message `IMages of well headers no source leakage`
on 2026-06-08.

The screenshots are intentionally not stored in Git or displayed on the public
website. This document is the durable public-safe derivative: it records only
header names, units, schema roles, formatting concepts, and unresolved
questions.

## Header Architecture

The workbook uses four distinct schema roles:

1. **Measured or supplied curves**: depth, density, neutron/NMR porosity,
   gamma ray, caliper, resistivity, and supplied velocities.
2. **Derived features**: density porosity, velocity ratio, impedance, and
   potentially saturation-related features.
3. **QC and alignment fields**: differential caliper, outlier-removal flags,
   unit-specific depth vectors, and depth correspondence at ML-data spacing.
4. **Targets or interpretation outputs**: hydrate saturation, `Sgh`, `S_h`,
   `NMR_SAT`, and irreducible-water saturation `S_wr` or `Swr`.

These roles must remain explicit in code and exports. A target column must never
silently become an input feature.

## Canonical Header Map

| Visible header or label | Meaning shown or inferred | Visible unit | Proposed canonical field | Schema role | Requirement or caution |
|---|---|---|---|---|---|
| `DEPTH`, `DEPT`, `Depth_ft`, `Depth, ft`, `True Depth` | Sample depth | ft or m depending on sheet | `depth_value` plus `depth_unit`; standardized output `depth_m` | Index / measured | Do not alias feet directly to `depth_m`; convert with recorded source unit |
| `Rho_b`, `RHOB`, `Density_gcpcc` | Bulk density | kg/m3 or g/cc depending on sheet | `rhob_g_cc` | Measured input | Unit-aware conversion is required; preserve original unit |
| `Phi_porosity`, `DPHI`, `phi_den` | Density-derived porosity | Screenshot unit is inconsistent in one header | `density_porosity_vv` | Derived or supplied feature | Confirm whether supplied or calculated; porosity should be dimensionless fraction or percent |
| `NPHI`, `phi_neut` | Neutron porosity | not shown | `neutron_porosity_vv` | Measured input | Record fraction-versus-percent convention |
| `NMRPHI`, `phi_nmr` | NMR porosity | not shown | `nmr_porosity_vv` | Measured input where available | User confirmed NMR is available; preserve whether the field is an input curve or target-derived value |
| `GR` | Gamma ray | API | `gr_api` | Measured input | Existing runtime field |
| `caliper`, `CAL1` | Caliper | screenshot suggests inches for `CAL1`; not universal | `caliper_in` | Measured/QC input | Preserve source unit and convert if necessary |
| `Differential Caliper` | Borehole deviation from expected gauge | mm shown | `differential_caliper` | QC feature | Define reference diameter and sign convention |
| `RES`, `Deep formation resistivity`, `A090`, `AF90` | Deep resistivity or tool-specific resistivity channel | Ohm.m | `rt_ohm_m` with source mnemonic retained | Measured input | `A090` and `AF90` require tool/mnemonic confirmation before canonical mapping |
| `Vp`, `VP`, `VELP` | Compressional-wave velocity | m/s | `vp_m_s` | Measured or supplied input | Do not confuse with sonic slowness `DT`; support direct velocity and calculated velocity |
| `Vs`, `VS`, `VS1` | Shear-wave velocity | m/s | `vs_m_s` | Measured or supplied input | Do not confuse with `DTS`; support direct velocity and calculated velocity |
| `Ratio Vp/Vs` | Compressional-to-shear velocity ratio | dimensionless | `vp_vs_ratio` | Derived feature | Calculate from canonical velocities when both are available |
| `Impedance` | Acoustic impedance, labeled `Rho_b * Vp` | kg/m2*s as shown | `acoustic_impedance` | Derived feature | Confirm desired unit expression and density conversion before calculation |
| `Sgh`, `S_h`, `Hydrate Saturation`, `NMR_SAT` | Gas-hydrate saturation target or interpretation | fraction not explicitly shown | `hydrate_saturation_vv` | Target / interpretation | Required regression target for known wells; confirm whether the authoritative target is supplied, NMR-derived, core-calibrated, or interpreted, and never use it as an input |
| `S_wr`, `Swr` | Irreducible-water saturation | fraction not explicitly shown | `irreducible_water_saturation_vv` | Target, calibration, or derived field | Confirm formula and whether it is measured, assumed, or calculated |
| `depths_unitD`, `depths_unitC`, `Unit D`, `Unit C` | Unit-specific depth vectors | ft shown in refined sheets | `source_depth_*` | Alignment/QC | Preserve unit identifier and original sampling |
| `Depth correspondence at ML data` | Resampled or matched depth | not consistently displayed | `aligned_depth` plus unit | Alignment/QC | Record interpolation or nearest-depth method and offset |

## Visible Workbook Organization

### Main ML Header Block

The header layout uses stacked rows:

1. role label such as `ML INPUT`, `OUTLIER REMOVAL`, or `GROUND TRUTH`;
2. short mnemonic;
3. unit;
4. plain-language description.

The scaffold should preserve this four-level concept even if the website uses
cards or tooltips instead of merged Excel cells.

### Source Sheets

Visible tabs include:

- `MTE`
- `IGS`
- `MTE_refined`
- `IGS_refined`

The unrefined sheets contain compact curve tables. The refined sheets appear to
contain unit-specific depth/saturation pairs and depth correspondence at the
machine-learning sampling interval.

## Scaffold Requirements

| ID | Requirement | Target area | Acceptance criterion |
|---|---|---|---|
| H1 | Preserve original mnemonic, description, unit, and schema role for every imported column | Runtime schemas/loaders | A mapping report shows source and canonical metadata |
| H2 | Support depth in feet or meters with explicit conversion to canonical meters | Runtime loaders/validation | Feet are never silently interpreted as meters |
| H3 | Support density in g/cc or kg/m3 with explicit conversion | Runtime loaders/validation | Equivalent density values standardize consistently |
| H4 | Support direct `Vp`/`Vs` inputs as well as `DT`/`DTS`-derived velocities | Schemas/feature engineering | Provenance identifies supplied versus calculated velocity |
| H5 | Separate measured inputs, derived features, QC fields, alignment fields, and targets | Schemas/exports/UI | Target leakage checks fail when target fields enter the feature set |
| H6 | Preserve source resistivity mnemonics while mapping confirmed deep-resistivity channels | Loaders/config | Unconfirmed `A090`/`AF90` mappings remain review items |
| H7 | Report source sampling, aligned depth, matching method, and offset | Alignment/core calibration | Refined outputs retain traceable source-to-ML depth correspondence |
| H8 | Display the four-level header meaning in the synthetic scaffold | Streamlit well-log engine | Users can see role, mnemonic, unit, and description |
| H9 | Treat normalized screenshot values as non-scientific layout examples only | Tests/docs/public site | No screenshot values are ingested into calculations or training |
| H10 | Add representative synthetic cases for unit conversion, aliases, alignment, and target leakage | Tests | Each requirement has at least one focused test |
| H11 | Fit normalization and imputation on training wells only | Modeling pipeline | Validation, locked-test, and prediction wells never influence fitted preprocessing |

## Proposed Track Groups

The future well-log panel should organize tracks by scientific function:

1. Depth and alignment
2. Borehole QC: caliper and differential caliper
3. Lithology: gamma ray
4. Porosity: density, density porosity, neutron porosity, NMR porosity
5. Electrical response: deep resistivity
6. Elastic response: `Vp`, `Vs`, `Vp/Vs`, acoustic impedance
7. Interpretation and calibration: hydrate saturation and irreducible-water
   saturation
8. Uncertainty and readiness flags

Measured and derived curves should use visibly different styling.
Ground-truth or calibration tracks should be visually isolated from ML inputs.

## Unresolved Questions

1. Does `A090` or `AF90` represent the selected deep-resistivity curve, and
   which tool family produced it?
2. Is `Phi_porosity` supplied directly or calculated from bulk density?
3. What is the correct unit for the `Phi_porosity` header that currently shows
   `kg/m3`?
4. Are `Vp` and `Vs` original supplied velocities or calculations from sonic
   slowness?
5. Is `S_wr` measured, assumed, or calculated?
6. Which sheets correspond to which source units or wells?
7. What interpolation or matching rule created `Depth correspondence at ML data`?
8. Are hydrate saturation fields fractions from 0 to 1 or percentages from 0
   to 100?
9. Which field provides the authoritative saturation target, and is it supplied,
   NMR-derived, core-calibrated, or interpreted, for the approximately 20%
   known-well cohort?
10. Which exact phase classes and uncertain-label convention are supplied for
    the known wells?
11. Are outcomes for the approximately 80% prediction wells available later
    for blind evaluation?

These questions should be resolved from the workbook, formulas, or supporting
documentation before changing scientific calculations.
