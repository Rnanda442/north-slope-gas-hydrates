# North Slope Gas Hydrate Dashboard

[Open the hosted Streamlit atlas](https://north-slope-gas-hydrates-vj67xkke9ksfzveon8ldt2.streamlit.app/)

[Open the Project Architecture and Activity Map](docs/PROJECT_ARCHITECTURE_AND_ACTIVITY_MAP.md)

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

Create the isolated dashboard environment once:

```bash
bash setup_dashboard.sh
```

Launch the dashboard:

```bash
bash run_dashboard.sh
```

The setup script creates `.venv-dashboard` inside the project folder. This avoids
writing into OpenScienceLab's shared `/opt/conda` installation, which may be
read-only.

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

## Stable Hosted Atlas URL

The unclassified regional atlas can also be deployed through Streamlit Community
Cloud. This provides a stable `streamlit.app` HTTPS link that can be opened
directly without keeping an OpenScienceLab terminal running.

Current deployment:

```text
https://north-slope-gas-hydrates-vj67xkke9ksfzveon8ldt2.streamlit.app/
```

The deployment is public and can be opened without Streamlit sign-in.

Deploy from:

```text
https://share.streamlit.io/
```

Choose:

```text
Repository: Rnanda442/north-slope-gas-hydrates
Branch: main
Main file path: streamlit_app.py
```

The hosted deployment is for the public-source regional atlas only. Do not
upload classified, controlled, restricted, or credential-bearing material to
Streamlit Community Cloud.

## Atlas Views

- `Welcome`: project purpose, public-data boundary, and atlas entry points
- `Project Roadmap`: mobile-friendly architecture, workstream status, blockers,
  and next actions read from the tracked project activity map
- `Regional Atlas`: assessment units, seismic coverage, and public well inventory
- `Structural Explorer`: generated North Slope 3D structural scenes
- `Data Library`: curated layer metadata and a filterable repository inventory
- `Research Framework`: manuscript-backed interpretation chain and decision rules
- `Future Well-Log Engine`: synthetic planning scaffold for the later runtime-only
  approved well-log analysis, including variable ranges, interpretation guidance,
  interval screening, core-calibration placeholders, and presentation exports

## Current Data Layout

- `raw_data/`: public-source shapefiles, XYZ grids, and rasters
- `03_data_final/core_layers/`: cleaned core geospatial Parquet layers
- `03_data_final/feature_layers/`: feature-enriched Parquet layers
- `03_data_final/gis_ready_surfaces/`: depth-grid surfaces prepared for GIS use
- `03_data_final/master_layers/`: consolidated 2D and 3D analysis tables
- `05_exports/html/`: generated interactive Plotly scenes and notebook exports
- `docs/data_dictionary.md`: plain-language layer labels and atlas boundary tags

## Data Boundary

Do not commit classified, controlled, restricted, or credential-bearing material.
The future well-log module must accept data at runtime from the approved
environment rather than embedding DOE data in this repository.

## Synthetic Well-Log Planning Scaffold

The public dashboard includes synthetic records with neutral aliases such as
`SYNTH-WELL-01`. These records preview the analysis outputs that should later be
generated locally inside the authorized DOE environment. Every export is labeled
`SYNTHETIC DEMONSTRATION DATA`.

The reusable calculation layer lives in `dashboard/well_log_engine.py`. Its
`RuntimeConfig` boundary is the future transfer point for authorized LAS/CSV
adapters. Do not point hosted Streamlit deployments at approved runtime files.

For an authorized OpenScienceLab working layout, run:

```bash
bash setup_authorized_runtime.sh
```

The created `data_runtime/`, `outputs_runtime/`, `models_runtime/`,
`logs_runtime/`, and `configs_local/` folders are intentionally ignored by Git.
See `docs/opensciencelab_runtime_layout.md`.
