# Detailed PowerPoint Change Prompt

Revise the current nine-slide North Slope Gas Hydrate ML deck, focusing on
slides 1 through 6. Preserve slides 7 through 9 unless spacing or source
footers need minor alignment. Keep the total deck at exactly nine slides.

Use the source package in:

`references/presentation-revision-2026-06-11/`

Use these local assets:

- `images/project_streamlit_structural_explorer_v2.png`
- `images/usgs_gas_hydrate_crystals_sem_public_domain.jpg`
- `images/usgs_gamma_logs_public_domain.png`
- `images/usgs_caliper_logs_public_domain.png`
- `images/usgs_fluid_resistivity_logs_public_domain.jpg`

Follow these public-safety rules:

- Do not use approved well-log rows, restricted identifiers, real runtime
  outputs, trained model metrics, populated runtime configs, or sensitive
  derived results.
- Treat the current well-log panels and Streamlit assets as public/synthetic or
  public regional context only.
- Keep `S_h`, `Sgh`, `NMR_SAT`, phase labels, and final rankings locked as
  targets/calibration/output fields, never as model inputs.

## Global Visual System

Use a clean scientific deck style with large visuals, fewer words, and
consistent icons. Each icon must show both the symbol and the plain-language
parameter name. Use the icon registry in `icon_registry.csv` throughout slides
3 through 6.

Recommended symbols:

- `GR`: Gamma ray
- `Rt`: Deep resistivity
- `RHOB`: Bulk density
- `phi_D`: Density porosity
- `phi_NMR`: NMR porosity
- `Vp`: Compressional velocity
- `Vs`: Shear velocity
- `Vp/Vs`: Velocity ratio
- `AI`: Acoustic impedance
- `mu-rho`: Shear stiffness feature
- `lambda-rho`: Compressional stiffness feature
- `CAL/DCAL`: Caliper / differential caliper
- `z / P-T`: Depth and pressure-temperature context
- `Core`: Core calibration
- `S_h locked`: Hydrate saturation target, not input

Use concise footers with source anchors. Avoid long source paragraphs.

## Slide 1: Gas Hydrate Occurrence and Saturation Prediction

Rebuild the title slide with a personal but professional `About me` strip.

Required content:

- Main title: `Gas Hydrate Occurrence and Saturation Prediction`.
- Subtitle: `Permafrost sediments on the Alaska North Slope using physics-constrained AI/ML`.
- Profile photo remains prominent.
- About me text: `About me: drawing | gym | running | swimming`.
- Add four small icons for drawing, gym, running, and swimming.
- Keep a small public-data boundary footer.

Visual direction:

- Left: title, subtitle, one sentence project goal, about-me icon strip.
- Right: profile photo.
- Do not add a crowded biography paragraph.

## Slide 2: Introduction: What and Why Gas Hydrates

Replace the older structural explorer image with the newer Streamlit visual:

`images/project_streamlit_structural_explorer_v2.png`

Add a clear gas hydrate visual. Use the USGS hydrate-crystal image as a texture
or visual anchor, and create a simple custom methane hydrate cage diagram if
space allows.

Required point visuals:

- `What`: methane trapped in ice-like water cages.
- `Where`: Arctic permafrost and North Slope regional context.
- `Why`: large assessed resource and energy/science value.
- `Goal`: predict occurrence and saturation separately from reservoir quality,
  gas charge, migration, and producibility.

Source anchors:

- USGS gas hydrate FAQ and primer.
- USGS North Slope assessment fact sheet.
- DOE Alaska North Slope gas hydrates site visit.
- NETL North Slope gas hydrate reservoir characterization page.

## Slide 3: Parameters: Well-Log Scaffold

Redesign this slide so it is visual-first and not packed with text.

Layout:

- Use 6 to 8 large parameter-family tiles.
- Each tile has a symbol badge, plain name, icon or mini-scene, and two short
  lines:
  - `Measures: ...`
  - `Caveat: ...`
- Do not put long measurement, hydrate-use, caveat, and ML-role paragraphs in
  each tile.

Required tiles:

- Lithology: `GR`, Gamma ray.
- Electrical: `Rt`, Deep resistivity.
- Density/porosity: `RHOB`, `phi_D`.
- NMR/fluid: `phi_NMR` and locked target badge for `S_h` or `NMR_SAT`.
- Elastic: `Vp`, `Vs`, `Vp/Vs`, `AI`.
- Borehole QC: `CAL/DCAL`.
- Context/calibration: `z / P-T`, `Core`.

Visual references:

- USGS gamma-log image for `GR`.
- USGS caliper-log image for `CAL/DCAL`.
- USGS fluid-resistivity-log image for electrical response.
- Custom generated/source-backed icons for the rest.

Footer:

`Sources: WELL_LOG_REQUIREMENTS_MAP; parameter matrix; USGS borehole-log references; Haines et al. 2022; NETL ML source.`

## Slide 4: ML Methodology: Architecture

Rebuild the architecture as a detailed connected pipeline.

Architecture content:

1. `Approved logs` input stack with icons:
   `GR`, `Rt`, `RHOB`, `phi_D`, `phi_NMR`, `Vp`, `Vs`, `CAL/DCAL`, `Core`, `z`.
2. Individual QC gate boxes, each with its own line:
   - `Unit and tool provenance`
   - `Depth alignment`
   - `Caliper / washout`
   - `Missingness / outliers`
   - `Lithology / reservoir gate`
   - `Target-leakage barrier`
3. Feature-equation boxes:
   - `Vsh` from `GR`
   - `phi_D` from `RHOB`
   - `Delta_NMR-D = phi_D - phi_NMR`
   - `Vp/Vs = Vp / Vs`
   - `AI = rho_b * Vp`
   - `mu-rho = rho_b * Vs^2`
   - `lambda-rho = rho_b * (Vp^2 - 2Vs^2)`
4. ML workflow boxes:
   - train-only imputation/scaling
   - complete-well split
   - rule/logit/Ridge baseline
   - tree/boosting models
   - Keras ANN saturation test
   - classification branch
   - saturation-regression branch
   - uncertainty/review flags
   - sweet-spot prediction output

Target-leakage visual:

- Draw a red locked rail under the feature flow.
- Put `S_h`, `Sgh`, `NMR_SAT`, phase labels, and final rankings below it.
- Add one short note: `Labels supervise or score models; they do not become predictors.`

## Slide 5: ML Methodology: Why These Parameters

Replace abstract parameter rectangles with behavior visuals.

Use six panels:

- `Clean sand`: low `GR`, usable porosity, possible reservoir.
- `Hydrate in sand`: high `Rt`, NMR-density separation, stiffer elastic
  response, clean reservoir gate.
- `Shale`: high `GR`, bound water, poor reservoir quality.
- `Free gas`: high `Rt` possible, `Vp` drops relative to `Vs`.
- `Ice/cement/carbonate`: stiff and resistive mimic.
- `Bad hole`: `CAL/DCAL` washout corrupts density, NMR/neutron, sonic, and
  resistivity.

Each panel should show a mini log curve, small rock/pore visual, or crossplot
region. Keep only a title and one short caveat line in each panel.

Footer:

`Sources: parameter matrix; Haines et al. 2022; NETL ML source; USGS gamma/caliper/resistivity references.`

## Slide 6: Geomechanical Feature Sketch

Make the slide a large rock-physics visual rather than many small text boxes.

Layout:

- Left: input icons `RHOB`, `Vp`, `Vs`, `GR`, `Rt`, `phi_NMR`, `CAL/DCAL`.
- Center: large rock block with P-wave and S-wave icons moving through it.
- Right: equation stack:
  - `AI = rho_b * Vp`
  - `Vp/Vs = Vp / Vs`
  - `mu-rho = rho_b * Vs^2`
  - `lambda-rho = rho_b * (Vp^2 - 2Vs^2)`
- Bottom: behavior comparison strip:
  `hydrate-supportive`, `free gas`, `shale`, `ice/cement/carbonate`,
  `overburden`, `bad hole`.

Main takeaway:

`High resistivity or high velocity is evidence to review, not a hydrate label by itself.`

Footer:

`Sources: runtime feature engineering; ODP sonic-tools reference; Haines et al. 2022; parameter matrix.`

## Asset Generation Prompts

Use these only for custom visuals if the deck builder needs bitmap assets.

### Gas Hydrate Cage

Create a clean scientific illustration of methane hydrate in a sand pore. Show
a blue water-molecule cage around one central methane molecule, embedded in
tan sediment grains, with subtle pressure and cold-temperature cues. No text
inside the image. White or transparent background. Style: polished scientific
vector rendered as a high-resolution bitmap, 16:9 crop, suitable for a
PowerPoint science deck.

### Well-Log Parameter Icon Set

Create a consistent set of simple scientific icons on transparent backgrounds:
gamma ray `GR`, deep resistivity `Rt`, bulk density `RHOB`, density porosity
`phi_D`, NMR porosity `phi_NMR`, compressional velocity `Vp`, shear velocity
`Vs`, velocity ratio `Vp/Vs`, acoustic impedance `AI`, caliper `CAL/DCAL`,
depth and pressure-temperature `z / P-T`, core calibration, and locked hydrate
saturation target `S_h`. Use one stroke style, muted teal/blue/amber/green/red
palette, no commercial tool branding, no real well data.

### Parameter Behavior Panels

Create six small source-backed concept panels showing simplified log behavior:
clean sand, hydrate-bearing sand, shale, free gas, ice/cement/carbonate mimic,
and bad-hole washout. Use synthetic curves only, no real well identifiers or
values. Each panel should contain one mini log track, one pore/rock icon, and a
single short label.
