# North Slope Workspace Inventory

## Current Repository Scope

The repository is an unclassified Alaska North Slope geospatial workspace built
from public-source material. The initial inventory contains 98 tracked source,
analysis, and export files before the dashboard additions.

## Primary Analysis Assets

- `01_pipeline/GISviz.ipynb`: GIS processing and visualization workflow
- `02_visualization/North Slope Data Layer Map.ipynb`: interactive map workflow
- `Master.ipynb`: consolidated analysis and export workflow
- `Depth_grid_processing.ipynb`: structural depth-grid processing
- `03_data_final/core_layers/`: cleaned map, seismic, well, extent, and assessment-unit layers
- `03_data_final/feature_layers/`: feature-enriched geospatial layers
- `03_data_final/gis_ready_surfaces/`: GIS-ready topographic, Shublik, and basement surfaces
- `03_data_final/master_layers/`: consolidated 2D layers and 3D structural surfaces
- `05_exports/html/`: interactive Plotly scenes and notebook HTML exports

## Public-Source Raw Inputs

- 2D seismic line shapefiles
- 3D seismic inventory shapefiles
- North Slope assessment-unit shapefiles
- Well-bottom-hole location shapefiles
- Eight XYZ structural grids and their raster exports

## Manuscript-Backed Modeling Rules

The supporting manuscript defines a coupled interpretation chain:

```text
environment -> tectonics -> deposition -> reservoir -> physics -> logs -> interpretation -> ML -> exploitation
```

The dashboard and future wireline module should preserve these rules:

1. Gas hydrate stability is necessary but not sufficient for hydrate presence.
2. Hydrate occurrence, hydrate saturation, and hydrate producibility are separate outputs.
3. High resistivity alone is not a defensible hydrate label.
4. Interval-scale interpretation should remain wireline-centered, using geological context as a constraint rather than a replacement for measurement evidence.
5. Future log interpretation should combine lithology, density, sonic, resistivity, porosity, NMR where available, stability context, and geomechanical screening.

## Dashboard Status

The first dashboard release adds:

- Manuscript-backed overview
- Embedded interactive Plotly scene viewer
- Filterable repository data catalog
- Explicit future wireline-module roadmap
- OpenScienceLab launch script and setup instructions

## Next Engineering Stages

1. Run and visually inspect the dashboard inside OpenScienceLab.
2. Confirm the JupyterHub proxy URL for stable browser access.
3. Add a lightweight configuration file for dashboard labels and scene selection.
4. Build LAS/CSV schema mapping and quality-control reports using only approved synthetic or public example logs.
5. Add well-log tracks, interval flags, assumptions, and uncertainty reporting.
