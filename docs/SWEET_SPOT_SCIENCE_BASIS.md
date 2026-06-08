# Synthetic Sweet-Spot Science Basis

Last updated: 2026-06-08

## Purpose

Document the research logic used to make the public synthetic well-log scaffold
more intuitive and scientifically aligned.

This is not a calibrated North Slope classification model. It separates:

- source-supported directional relationships;
- synthetic working thresholds used to demonstrate software behavior;
- questions that require the full workbook, approved data, and local
  calibration.

## Source Architecture

The repository source-library index contains 28 candidate artifacts across six
groups: public field reports, Alaska geology and reservoir references, wireline
equations and ranges, geomechanics/productivity/ML synthesis, manuscript
synthesis, and map/public-data support.

Ten directly relevant primary public references are currently exposed on the
website. They cover North Slope assessment, scientific drilling, permafrost
occurrence, well-log interpretation, reservoir architecture, stratigraphic
correlation, reservoir quality, and machine-learning saturation prediction.

Connected Google Drive documents reviewed during one synthesis pass on
2026-06-08:

- `Geomechanical relationship with Wireline Logging AN`
- `new query with all stuff`
- `PDF notes reorganized`
- `pdf notes`

Repository sources also used:

- the classification-methods manuscript draft;
- the research-paper draft;
- the public science references already listed in
  `dashboard/well_log_engine.py`.

Those four Drive documents are a review subset, not the project's total source
base. They and the project manuscripts guide the logic but do not replace
verification against primary publications before final scientific claims or
calibrated thresholds are published.

See `docs/SWEET_SPOT_SOURCE_MATRIX.md` for the evidence tiers, primary-source
roles, indexed-library coverage, and treatment rules.

## Supported Directional Relationships

### Stability

Pressure-temperature stability is an admissibility condition, not proof of
hydrate. Stable intervals may remain empty because gas supply, migration, or
reservoir capacity is absent.

### Reservoir

Sand-prone, porous, connected intervals are better candidates for pore-filling
and potentially producible hydrate than clay-rich intervals. A good reservoir
can still contain no hydrate.

### Electrical

Hydrate can increase resistivity by replacing conductive pore water. High
resistivity is non-unique and may also reflect gas, low porosity, ice,
carbonate, lithology, or water-property assumptions.

### Elastic

Hydrate generally stiffens sediment, supporting increases in both compressional
and shear velocity. Free gas commonly lowers compressional velocity while shear
velocity is less affected. Stress and competent lithology remain competing
explanations.

### Porosity and NMR

NMR may show reduced mobile-fluid response where hydrate occupies pore space.
NMR-density separation is useful when depth alignment and tool quality are
defensible. Density alone is a weak hydrate discriminator because the
hydrate-water density contrast is small.

### Saturation

Electrical and NMR-density saturation estimates require local parameters,
depth matching, lithology correction, and uncertainty reporting. They should
agree with independent phase evidence rather than create a label alone.

### Producibility

Maximum saturation is not automatically the best production target. Hydrate can
reduce permeability by blocking pore throats. Moderate occupancy in a connected,
permeable sand may outrank a high-saturation interval with poor pressure
communication.

## Public Synthetic Logic

The website demonstrates the following sequence:

1. QC gate
2. Stability gate
3. Reservoir-quality gate
4. Electrical and elastic phase-evidence gate
5. Competing-explanation review
6. Saturation-proxy review
7. Producibility review

Each interval reports passed and blocking evidence domains. The public scaffold
uses synthetic thresholds solely to exercise this workflow.

## Calibration Work Still Required

Before scientific use:

1. confirm workbook formulas, units, and source mnemonics;
2. establish per-well or per-formation baselines rather than universal values;
3. calibrate Archie parameters and water resistivity;
4. quantify NMR-density depth alignment and shale effects;
5. correct velocity trends for burial, stress, lithology, and acquisition;
6. calibrate permeability and producibility against core and pressure data;
7. validate classification by held-out wells;
8. test failure cases such as good sand with no hydrate, gas, ice, shale,
   carbonate, and bad-hole response.

## Implementation Rule

Code may encode source-supported relationships and synthetic demonstration
thresholds. It must label those thresholds as synthetic and must not present
them as universal North Slope sweet-spot criteria.
