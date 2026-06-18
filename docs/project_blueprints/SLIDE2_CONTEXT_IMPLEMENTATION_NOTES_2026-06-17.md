# Slide 2 Context Implementation Notes - 2026-06-17

## Original Spine To Preserve

Slide 2 should explain what gas hydrates are and why the Alaska North Slope matters. It should not become a workflow, registry, schema, or model-results slide.

## Accepted Slide 2 Baseline

The 2026-06-17 three-column layout is the accepted Slide 2 direction:

1. What gas hydrate is.
2. Why the North Slope matters.
3. Why pressure-temperature stability is a gate.

The visual hierarchy should stay this way unless the user or mentor explicitly changes the slide spine.

## Implemented In The Current Draft

1. Replace the Processing-style regional image with a real public geology GIS-layer preview.
   - Slide asset: `docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_11_dggs_umiat_gubik_geology_layer_slide_map.png`
   - Handoff preview asset: `docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_10_dggs_umiat_gubik_geology_layer_preview.png`
   - Source: Herriott et al. 2018, Alaska DGGS RI 2018-6, Geologic map of the Umiat-Gubik area, central North Slope, Alaska, DOI `10.14509/30099`.
   - Shows: geologic map units, contacts/faults, geologic lines, and fold axes.
   - OSL handoff: upload the public DGGS shapefile package before wiring the same layer into the website.
   - Guardrail: context only; not hydrate occurrence or saturation evidence.
   - Provenance retained: the earlier website-mirrored geoscience orientation map remains at `docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_08_north_slope_geoscience_orientation_map.png` as a fallback, and the earlier Structure Explorer 2D wells/seismic export remains at `docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_05_structure_explorer_2d_wells_seismic.png`.

2. Add source-package hydrate structure evidence.
   - Asset: `docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_09_world_atlas_fig1_1_full_structure_types_si_highlighted.png`
   - Purpose: show Structure I, Structure II, and Structure H with Structure I circled.
   - Slide meaning: Structure I / methane-dominant hydrate is the current equation/stability baseline.
   - Caption style: cite as `World Atlas Fig. 1.1 after Warrier et al. 2016; sI highlighted`, not as an internal source-package filename.
   - Caution: the source figure needs rights/caption review before public release.

3. Add the North Slope subsurface geology cross section.
   - Asset: `docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_06_usgs_arctic_alaska_cross_section_fig2_crop.png`
   - Purpose: visually explain that North Slope hydrate work sits inside a real basin/structural framework.
   - Guardrail: geologic context only; not hydrate proof.

4. Keep the pressure-temperature diagram.
   - Asset: `docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_02_usgs_hydrate_stability_curve_crop.png`
   - Purpose: explain why stability is a physics gate.
   - Guardrail: admissible under assumptions, not occurrence or saturation proof.

5. Keep the bottom logic simple.
   - North Slope methane hydrate needs integrated geology, stability, well-log, and core evidence.
   - No hydrate proof, occurrence prediction, saturation prediction, or model results are claimed on this slide.

## Remaining Choices

- Decide whether the World Atlas Structure I/II/H figure can be used in public GitHub/Drive deliverables, or replace it with a public-domain/redrawn-after-source version.
- Upload the DGGS RI 2018-6 shapefile package to OpenScienceLab and wire a website geology-layer view from that approved OSL location.
- If the mentor wants less density, keep the cross section and DGGS geology map, then move the full Structure I/II/H source figure to speaker notes or the companion doc.
- If the structure figure stays, keep Structure I circled and label Structure II/H as gas-composition sensitivity, not the current baseline.
