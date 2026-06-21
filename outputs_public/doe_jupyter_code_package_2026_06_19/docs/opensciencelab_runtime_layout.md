# OpenScienceLab Authorized Runtime Layout

## Boundary Rule

The Git repository is a public-source planning scaffold. Approved well logs,
core data, identifiers, derived outputs, models, and populated local
configuration files must remain inside the authorized OpenScienceLab
environment. Do not commit, upload, paste into chat, or send them to Streamlit
Community Cloud.

## First-Time Setup

```bash
cd ~/north-slope-gas-hydrates
git pull origin main
bash setup_dashboard.sh
bash setup_authorized_runtime.sh
```

## Folder Layout

```text
north-slope-gas-hydrates/
  data_runtime/                 # ignored: approved inputs only
    approved_inputs/            # LAS/CSV files
    core_calibration/           # approved core-calibration tables
    reference_only/             # local supporting files
  outputs_runtime/              # ignored: derived local outputs
    qc_reports/
    interval_tables/
    figures/
    presentation_exports/
  models_runtime/               # ignored: fitted models and serialized artifacts
  logs_runtime/                 # ignored: local execution logs
  configs_local/                # ignored: populated local mappings and paths
  data/source_library/          # ignored/local: uploaded public source bundle
  wireline_ml/configs/          # tracked: public example templates only
```

## Working Rule

Run `git status --short` before every commit or push. Only reusable code,
documentation, empty-folder setup logic, and synthetic examples belong in Git.

## Stability Source Bundle

The 2026-06-13 public-source bundle for the Structural Explorer should be
uploaded into OpenScienceLab and extracted to:

```text
data/source_library/north_slope_stability_sources_2026-06-13/
```

The local laptop upload zip is:

```text
C:\Users\gargi\Downloads\north_slope_stability_sources_2026-06-13_UPLOAD_TO_OPENSCIENCE.zip
```

See `docs/source_library_index/stability_source_bundle_2026_06_13.md` for the
file inventory and setup order. Do not commit the unzipped source files unless
the project later chooses a small, license-safe subset for public vendoring.

