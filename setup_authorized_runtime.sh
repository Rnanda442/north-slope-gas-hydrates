#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

mkdir -p \
  data_runtime/approved_inputs \
  data_runtime/core_calibration \
  data_runtime/reference_only \
  outputs_runtime/qc_reports \
  outputs_runtime/interval_tables \
  outputs_runtime/figures \
  outputs_runtime/presentation_exports \
  models_runtime \
  logs_runtime \
  configs_local

if [[ ! -f configs_local/runtime_config.yaml ]]; then
  cp wireline_ml/configs/runtime_config.example.yaml configs_local/runtime_config.yaml
fi

if [[ ! -f configs_local/curve_aliases.yaml ]]; then
  cp wireline_ml/configs/curve_aliases.example.yaml configs_local/curve_aliases.yaml
fi

cat <<'EOF'
Authorized local runtime folders are ready.

Keep approved well logs, core data, identifiers, derived outputs, models, and
local configuration files inside these ignored folders only:
  data_runtime/
  outputs_runtime/
  models_runtime/
  logs_runtime/
  configs_local/

Before every commit, run:
  git status --short
EOF
