#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

VENV_DIR="${DASHBOARD_VENV:-.venv-dashboard}"

if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
  python -m venv "${VENV_DIR}"
fi

"${VENV_DIR}/bin/python" -m pip install --upgrade pip
"${VENV_DIR}/bin/python" -m pip install -r requirements-dashboard.txt

echo
echo "Dashboard environment is ready."
echo "Launch with: bash run_dashboard.sh"
