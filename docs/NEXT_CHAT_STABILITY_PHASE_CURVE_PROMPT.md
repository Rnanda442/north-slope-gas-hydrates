# Next Chat Prompt - Stability Phase Curve Step

Use this prompt to start the next Codex chat.

```text
We are working in the GitHub repo `Rnanda442/north-slope-gas-hydrates`.
Start by reading `docs/NORTH_SLOPE_PROJECT_BASE.md`, `PROJECT_CONTEXT.md`,
and `docs/source_library_index/stability_source_bundle_2026_06_13.md`.

Current state:
- OpenScienceLab is the heavy-data workbench.
- GitHub/Streamlit is the public delivery surface.
- Raw source files stay out of Git under `data/source_library/`.
- Derived public outputs live under `data/public_stability_products/`.
- Latest complete OSL-derived product commit:
  `aedd734 Rebuild stability products with complete G10015 profiles`.
- Full source bundle status after the missing G10015 upload:
  `7/7` source categories, `43` GGD223 controls, `184` G10015 profiles,
  `3` hydrate AUs.
- Current public stability products:
  `north_slope_well_stability_context_2026-06-14.csv`
  `g10015_temperature_profile_inventory_2026-06-14.csv`
  `stability_input_scaffold_2026-06-14.csv`
- Current scaffold summary:
  `8,084` wells, `483` temperature-profile matches, `374` rows ready for
  phase-curve inputs, `7,113` rows needing temperature profile match, and
  `0` final stability results.
- The local website is viewed at:
  `http://localhost:8517/?page=Explore%20North%20Slope`
  in `Explore North Slope -> Structural Explorer`.

Important guardrail:
Do not call the current scaffold hydrate proof, saturation, or final stability.
It is only an input scaffold. Final `stability_top_m`,
`stability_base_m`, and `stability_thickness_m` should remain uncalculated
until pressure, temperature, and hydrate phase-curve assumptions are locked and
cited.

Next task:
Build the next source-backed stability calculation plan. First decide and
document:
1. pressure assumption and equation, probably hydrostatic pressure with units;
2. temperature model approach using G10015 profiles and GGD223/permafrost context;
3. methane hydrate phase curve source or lookup table;
4. what confidence labels and caveats the public website should show;
5. exact output schema for a future `stability_screen_*.csv`.

Do the reasoning and source mapping before calculating final top/base/thickness.
If web research is needed, use primary/public sources and cite them.
```
