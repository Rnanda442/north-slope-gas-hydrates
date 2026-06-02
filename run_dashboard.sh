#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

VENV_DIR="${DASHBOARD_VENV:-.venv-dashboard}"
PYTHON="${VENV_DIR}/bin/python"

if [[ ! -x "${PYTHON}" ]]; then
  echo "Dashboard environment is missing."
  echo "Run: bash setup_dashboard.sh"
  exit 1
fi

"${PYTHON}" -m streamlit run dashboard/app.py \
  --server.address 0.0.0.0 \
  --server.port "${PORT:-8501}" \
  --server.headless true
