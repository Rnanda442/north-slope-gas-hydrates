# Slide Update Attachment Editability Audit 2026-06-18

## Scope

Source email searched in Gmail:

- Subject: `slide updates for the newest deck`
- Message id: `19edd022306af325`
- Attachment:
  `V5.5 Slide 3 Signal Response QC-Cleaned North Slope Gas Hydrate ML Workflow Slides 2026-06-17 (1).pptx`

The attachment was downloaded only into ignored runtime audit storage:

- `outputs_runtime/attachment_audit_temp/V5.5_email_slide_updates_2026-06-18_INVALID_8slides_audit_candidate.pptx`

It was not promoted to a reference deck because it contains eight slides, not
the required nine. It should not be committed as a raw attachment unless the
user explicitly approves that later.

## Structural Finding

The PPTX is a valid PowerPoint file, but not a valid nine-slide deck.

- Slide count: 8
- Slide size: widescreen 16:9
- Slides 1-4 and 6-8 are single full-slide PNG screenshots at 1600 x 900 px.
- Slide 5 is the only slide made from editable PowerPoint shapes/text.
- No private approved rows, row-level predictions, fitted models, or final
  hydrate claims were observed in the extracted slide images/text.

## Slide 2 Source-Package Comparison

Local source-backed Slide 2 package checked:

- `docs/project_blueprints/presentation_assets/slide2_usgs_remake_2026_06_16/`

Important note: this folder exists locally, but `git ls-files` did not show it
as tracked in the current Git index. Treat it as a local source-update package
until the branch state is cleaned up.

What the package provides:

- USGS SIR 2008-5175 P-T figure pages and clean P-T crop.
- USGS SIR 2012-5147 Arctic Alaska page images and clean cross-section crop.
- A source-backed 1600 x 900 remake named
  `slide_02_usgs_stability_geology_remake_2026_06_16.png`.

Comparison to the email attachment:

- The attachment Slide 2 is a full-slide screenshot, not editable.
- The attachment uses the useful high-level structure of hydrate definition,
  North Slope context, and P-T diagram, but all labels and callouts are baked
  into one raster image.
- The local Slide 2 source package has cleaner source-backed P-T and geology
  assets, but the final rebuild should use the newer corrected GIS-layer map
  and should rebuild text/arrows/callouts as editable PowerPoint objects.
- The final Slide 2 should not keep small source/citation text on the main
  slide. Detailed citations belong in Word, speaker notes, or end material.

## Slide-By-Slide Audit

### Slide 1 - Cover / Personal Opener

- Slide role: cover and brief personal/project opener.
- Editable now: nothing. The slide is one full-slide PNG.
- Flat/raster-only rebuild needed: all title text, subtitle, "About me" area,
  hobby labels, image frames, and layout.
- Assets to preserve: project title intent and simple three-chip status row
  if still wanted. Personal photo should be removed and replaced manually later
  by the user.
- Text that stays on slide: concise project title and one public-safe guardrail
  sentence.
- Text/citations that move to Word/end material: none needed on the cover.
- Needed source/data figure before rebuilding: optional professional user photo
  supplied by the user; otherwise use a neutral North Slope map/structure visual.

### Slide 2 - Gas Hydrates And Why The North Slope Matters

- Slide role: explain what gas hydrates are and why the North Slope is the
  project setting.
- Editable now: nothing. The slide is one full-slide PNG.
- Flat/raster-only rebuild needed: title, section numbers, hydrate structure
  labels, P-T diagram labels, map/cross-section captions, callouts, and footer.
- Assets to preserve: hydrate structure source figure if the original source is
  confirmed; USGS/DOE P-T diagram concept; Arctic Alaska cross-section; North
  Slope map concept.
- Text that stays on slide: big high-level phrases only, such as `methane in
  water cages`, `cold + pressure`, `stability window`, `North Slope setting`,
  and `not proof`.
- Text/citations that move to Word/end material: source lines, detailed
  explanation of structures II/H, gas-composition sensitivity text, figure
  provenance, and stability caveat detail.
- Needed source/data figure before rebuilding: corrected combined GIS-layer
  North Slope map; original hydrate structure source image with Structure I
  circled cleanly; source-backed explanation for Structure I/II/H; thermogenic
  versus biogenic methane source support; source-backed energy/resource
  potential statement for Alaska/North Slope; preferably an east-west or
  anticline-relevant cross-section if available.

### Slide 3 - Hydrate Signal Response / Well-Log Scaffold

- Slide role: show how log signals move together across depth before equations
  and ML.
- Editable now: nothing. The slide is one full-slide PNG.
- Flat/raster-only rebuild needed: well-log curves, interval highlights,
  callouts, decoder boxes, strip labels, bottom equation chips, and arrows.
- Assets to preserve: idea of depth-aligned log tracks, hydrate-support versus
  mimic intervals, and the target-only rail.
- Text that stays on slide: short labels only: `clean sand`, `resistive`,
  `stiff`, `Vs matters`, `mimic`, `QC`, `target only`.
- Text/citations that move to Word/end material: long decoder explanations,
  formal caveats, and detailed source provenance.
- Needed source/data figure before rebuilding: a simplified but more
  well-log-like curve stack; a lithology/rock-type side strip for clean
  sandstone, shale, and possible hydrate-bearing sand; visual explanation of
  why Vs is useful because shear response is not carried by fluids; North Slope
  shallow hydrate-zone lithology source around the target depth range if
  available.

### Slide 4 - Full Complex Project Workflow

- Slide role: full project workflow from public context through approved
  runtime ML and public-safe outputs.
- Editable now: nothing. The slide is one full-slide PNG.
- Flat/raster-only rebuild needed: all workflow boxes, connectors, labels,
  legends, and inset panels.
- Assets to preserve: complete end-to-end logic and separation of public
  context, approved runtime, feature matrix, target-only labels, validation,
  and outputs.
- Text that stays on slide: simplified lane labels and a small number of
  audience-facing workflow stages.
- Text/citations that move to Word/end material: implementation details, file
  names, registry names, detailed counts, and long caveats.
- Needed source/data figure before rebuilding: none required for the diagram,
  but the rebuild needs a two-minute script and a combined-box plan so the
  complex diagram can be audience-readable.

### Slide 5 - Equation Slide

- Slide role: equation/physics layer connecting measured logs to derived
  features and stability context.
- Editable now: yes. It contains 136 auto-shapes, 4 lines, and 117 text shapes.
- Flat/raster-only rebuild needed: not raster-only, but it is too fragmented
  and crowded. It should be rebuilt/simplified rather than merely edited.
- Assets to preserve: density porosity equation, Archie saturation equation,
  sonic velocity terms, elastic terms, and stability-context equation.
- Text that stays on slide: equation names, readable formulas using actual
  fraction formatting, and one phrase per equation explaining the physical
  meaning.
- Text/citations that move to Word/end material: "why use it" paragraphs,
  source registry statements, public map provenance, and long equation
  interpretation.
- Needed source/data figure before rebuilding: no map should remain on this
  slide. Use small icons or mini-sketches for density, resistivity, sonic/elastic
  stiffness, and P-T stability if needed.

### Slide 6 - Complex ML Runtime Architecture

- Slide role: show the leakage-safe ML runtime architecture and ANN/baseline
  structure.
- Editable now: nothing. The slide is one full-slide PNG.
- Flat/raster-only rebuild needed: all model boxes, arrows, target rail,
  feature matrix, neural-network graphic, and output boxes.
- Assets to preserve: leakage barrier, target-only rail, baseline-before-ANN
  ladder, whole-well split, occurrence/saturation outputs, and ANN/Keras anchor.
- Text that stays on slide: high-level labels only: `X inputs`, `Y-only
  targets`, `split by well`, `baseline`, `ANN`, `occurrence`, `saturation`,
  `review`.
- Text/citations that move to Word/end material: detailed method notes, source
  names, implementation terms, and long caveats.
- Needed source/data figure before rebuilding: editable neural-network
  schematic, feature-family icons, and possibly a small target-leakage lock icon.

### Slide 7 - Stability-To-ML Overlay

- Slide role: currently tries to explain stability screen use in ML.
- Editable now: nothing. The slide is one full-slide PNG.
- Flat/raster-only rebuild needed: all boxes, arrows, counts, and labels.
- Assets to preserve: stability guardrail and public counts if still current.
- Text that stays on slide: `stability is context`, `not proof`, `screening
  support`, and concise count labels if verified.
- Text/citations that move to Word/end material: block/use-policy details,
  caveat lists, and review-layer mechanics.
- Needed source/data figure before rebuilding: the corrected GIS-layer public
  stability map should move here. It should not be presented as an ML overlay
  or prediction map.

### Slide 8 - Current Status / What Is Next

- Slide role: status, non-claims, and next-step summary.
- Editable now: nothing. The slide is one full-slide PNG.
- Flat/raster-only rebuild needed: all text columns, icons, labels, and footer.
- Assets to preserve: three-column logic: `what done`, `what not claimed`,
  `what next`.
- Text that stays on slide: only major public-safe bullets and mentor-facing
  next steps.
- Text/citations that move to Word/end material: detailed source/provenance
  line and implementation-specific wording.
- Needed source/data figure before rebuilding: current public count snapshot
  and model-run tracker summary only if they are public-safe and verified.

### Slide 9 - Missing

- Slide role: results/discussion or final mentor-decision slide.
- Editable now: not present in the attachment.
- Flat/raster-only rebuild needed: create from scratch as editable objects.
- Assets to preserve: none from the attachment.
- Text that stays on slide: likely `review path`, `mentor decisions`, `what
  becomes publishable`, and `what remains blocked`.
- Text/citations that move to Word/end material: detailed source list and
  method caveats.
- Needed source/data figure before rebuilding: public-safe result/discussion
  plan, not fake predictions; optional map/status thumbnails after review.

## Rebuild Priority

1. Rebuild the deck as actual editable PowerPoint objects, not full-slide
   screenshots.
2. Promote the corrected GIS-layer stability map to Slide 7, not Slide 5.
3. Rebuild Slide 2 from source assets rather than the raster screenshot.
4. Rebuild Slide 3 with more realistic well-log tracks, a lithology strip, and
   a clear Vs explanation.
5. Simplify Slide 4 and Slide 6 into audience-facing editable diagrams while
   keeping the complex full versions as appendix/source-of-truth material.
6. Rebuild Slide 5 as a clean equation board with real fraction formatting and
   no map.
7. Create a real Slide 9.
