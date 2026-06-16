from __future__ import annotations

from pathlib import Path

import pandas as pd


SOURCE_VISUAL_INVENTORY_FILE_NAME = "source_visual_inventory_2026-06-16.csv"

SOURCE_VISUAL_INVENTORY_COLUMNS = [
    "visual_id",
    "artifact",
    "path",
    "slide_or_site_use",
    "visual_type",
    "source_status",
    "provenance",
    "allowed_use",
    "qa_status",
    "replacement_needed",
    "guardrail",
]

PASS_QA_STATUSES = {
    "pass_public_safe",
    "pass_source_backed",
    "pass_project_generated",
    "review_caption_only",
}

REVIEW_REPLACEMENT_VALUES = {"yes", "review"}


def default_public_ml_products_dir(project_root: Path) -> Path:
    return project_root / "data" / "public_ml_products"


def default_source_visual_inventory_path(project_root: Path) -> Path:
    return default_public_ml_products_dir(project_root) / SOURCE_VISUAL_INVENTORY_FILE_NAME


def load_source_visual_inventory(project_root: Path) -> pd.DataFrame:
    path = default_source_visual_inventory_path(project_root)
    if not path.exists():
        return pd.DataFrame(columns=SOURCE_VISUAL_INVENTORY_COLUMNS)

    inventory = pd.read_csv(path)
    for column in SOURCE_VISUAL_INVENTORY_COLUMNS:
        if column not in inventory.columns:
            inventory[column] = ""

    return inventory[SOURCE_VISUAL_INVENTORY_COLUMNS].copy()


def _is_local_inventory_path(path_value: object) -> bool:
    text = str(path_value).strip()
    return bool(text) and not text.startswith(("http://", "https://"))


def missing_local_visual_paths(inventory: pd.DataFrame, project_root: Path) -> list[str]:
    missing: list[str] = []
    if inventory.empty or "path" not in inventory.columns:
        return missing

    for _, row in inventory.iterrows():
        path_text = str(row["path"]).strip()
        if not _is_local_inventory_path(path_text):
            continue
        if not (project_root / path_text).exists():
            missing.append(path_text)
    return missing


def validate_source_visual_inventory(inventory: pd.DataFrame, project_root: Path) -> dict[str, object]:
    missing_columns = [
        column for column in SOURCE_VISUAL_INVENTORY_COLUMNS if column not in inventory.columns
    ]
    missing_paths = missing_local_visual_paths(inventory, project_root)

    if inventory.empty:
        uncited_or_ai_looking_rows: list[str] = []
        replacement_review_rows: list[str] = []
        invalid_qa_status_rows: list[str] = []
    else:
        source_status = inventory["source_status"].fillna("").str.lower()
        qa_status = inventory["qa_status"].fillna("").str.lower()
        replacement = inventory["replacement_needed"].fillna("").str.lower()

        uncited_mask = source_status.str.contains("uncited|ai-looking|ai_generated", regex=True)
        replacement_mask = replacement.isin(REVIEW_REPLACEMENT_VALUES)
        invalid_qa_mask = ~qa_status.isin(PASS_QA_STATUSES)

        uncited_or_ai_looking_rows = inventory.loc[uncited_mask, "visual_id"].astype(str).tolist()
        replacement_review_rows = inventory.loc[replacement_mask, "visual_id"].astype(str).tolist()
        invalid_qa_status_rows = inventory.loc[invalid_qa_mask, "visual_id"].astype(str).tolist()

    return {
        "valid": not missing_columns
        and not missing_paths
        and not uncited_or_ai_looking_rows
        and not invalid_qa_status_rows,
        "missing_columns": missing_columns,
        "missing_local_paths": missing_paths,
        "uncited_or_ai_looking_rows": uncited_or_ai_looking_rows,
        "replacement_review_rows": replacement_review_rows,
        "invalid_qa_status_rows": invalid_qa_status_rows,
    }


def source_visual_inventory_summary_frame(
    inventory: pd.DataFrame,
    project_root: Path,
) -> pd.DataFrame:
    validation = validate_source_visual_inventory(inventory, project_root)

    if inventory.empty:
        return pd.DataFrame(
            [
                {
                    "metric": "Visual inventory rows",
                    "value": 0,
                    "meaning": "No source-visual inventory product is available yet.",
                }
            ]
        )

    source_backed = inventory["source_status"].fillna("").str.contains(
        "source_backed|project_generated|public_safe", case=False, regex=True
    )
    project_generated = inventory["source_status"].fillna("").str.contains(
        "project_generated", case=False, regex=False
    )
    website_captures = inventory["visual_type"].fillna("").str.contains(
        "website_capture", case=False, regex=False
    )

    rows = [
        {
            "metric": "Visual inventory rows",
            "value": int(len(inventory)),
            "meaning": "Slide, website, and appendix visuals tracked with provenance and guardrails.",
        },
        {
            "metric": "Source-backed or public-safe rows",
            "value": int(source_backed.sum()),
            "meaning": "Rows explicitly tied to project-generated panels, website captures, or cited source-backed visuals.",
        },
        {
            "metric": "Project-generated visuals",
            "value": int(project_generated.sum()),
            "meaning": "Rows generated from the website, parameter registry, workflow builder, or public scaffold.",
        },
        {
            "metric": "Website capture visuals",
            "value": int(website_captures.sum()),
            "meaning": "Rows that reuse current Streamlit screenshots rather than detached illustrations.",
        },
        {
            "metric": "Replacement needed/review rows",
            "value": int(len(validation["replacement_review_rows"])),
            "meaning": "Visuals needing source-caption review or replacement before final mentor delivery.",
        },
        {
            "metric": "Inventory validation",
            "value": "pass" if validation["valid"] else "review",
            "meaning": "Checks required columns, local image paths, uncited/AI-looking flags, and QA status values.",
        },
    ]
    return pd.DataFrame(rows)
