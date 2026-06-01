#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
python -m streamlit run dashboard/app.py \
  --server.address 0.0.0.0 \
  --server.port "${PORT:-8501}" \
  --server.headless true
