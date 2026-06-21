# Package Exclude Rules

This transfer package is code only.

Excluded from this package and from GitHub:

- approved workbook rows and raw workbook files;
- LAS/DLIS/log-source files and private source packages;
- row-level predictions and runtime scoring tables;
- trained models, fitted scalers, serialized pipelines, and notebooks
  with embedded private outputs;
- credentialed PDFs, private screenshots, secrets, and local config
  files;
- runtime manifests containing private absolute paths or identifiers.

Public-safe derived summaries can be proposed for review only after a
separate row-free/sensitive-token audit.
