# North Slope Gas Hydrate Dashboard

This repository contains the unclassified Alaska North Slope geospatial workspace
and a URL-accessible Streamlit regional atlas. The application organizes the
existing public-source GIS assets, exported Plotly scenes, and manuscript-backed
research framework. A future wireline module will be added as a configurable
runtime extension for approved environments.

## OpenScienceLab Setup

Pull the latest changes:

```bash
cd ~/north-slope-gas-hydrates
git pull
```

Install the dashboard dependency once:

```bash
python -m pip install -r requirements-dashboard.txt
```

Launch the dashboard:

```bash
bash run_dashboard.sh
```

The process listens on port `8501`. In a JupyterHub environment with
`jupyter-server-proxy`, open:

```text
https://<your-opensciencelab-host>/<your-user-prefix>/proxy/8501/
```

If the proxy URL is unclear, run:

```bash
jupyter server list
```

Use the displayed base URL and append `proxy/8501/`.

## Atlas Views

- `Welcome`: project purpose, public-data boundary, and atlas entry points
- `Regional Atlas`: assessment units, seismic coverage, and public well inventory
- `Structural Explorer`: generated North Slope 3D structural scenes
- `Data Library`: curated layer metadata and a filterable repository inventory
- `Research Framework`: manuscript-backed interpretation chain and decision rules
- `Future Well-Log Engine`: runtime-only blueprint for approved well-log analysis

## Current Data Layout

- `raw_data/`: public-source shapefiles, XYZ grids, and rasters
- `03_data_final/core_layers/`: cleaned core geospatial Parquet layers
- `03_data_final/feature_layers/`: feature-enriched Parquet layers
- `03_data_final/gis_ready_surfaces/`: depth-grid surfaces prepared for GIS use
- `03_data_final/master_layers/`: consolidated 2D and 3D analysis tables
- `05_exports/html/`: generated interactive Plotly scenes and notebook exports

## Data Boundary

Do not commit classified, controlled, restricted, or credential-bearing material.
The future well-log module must accept data at runtime from the approved
environment rather than embedding DOE data in this repository.
