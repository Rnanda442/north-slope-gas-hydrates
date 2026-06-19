# Public Basemap Landmark Bundle

This folder is the tracked website-runtime target for the interactive North
Slope 2D well map landmark layers.

Generate the public-safe derived bundle on the OSL/PC machine with:

```powershell
python 01_pipeline\export_public_basemap_landmarks_2026_06_19.py
```

The exporter reads public GIS layers staged under
`data/source_library/basemap_landmarks_2026_06_18/` and writes simplified
GeoJSON layers plus `manifest.json` here.

Guardrails:
- Public geospatial context only.
- No approved DOE rows, private workbooks, well-log attachments, row-level
  predictions, trained models, or fitted scalers.
- Website use is orientation/context only, not hydrate occurrence, saturation,
  producibility, or ML-result evidence.
