from __future__ import annotations

import argparse
import csv
import html
import json
import re
import shutil
import textwrap
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

import pandas as pd
import plotly.graph_objects as go


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATE_STAMP = "2026_06_18"
DATE_HUMAN = "2026-06-18"
FORCE_FIGURE_EXPORT = False

EXPECTED_DATASETS = (
    "curated_dataset1.xlsx",
    "curated_dataset2.xlsx",
    "curated_dataset3.xlsx",
)
OPTIONAL_CONTEXT_FILES = ("wellnametodataset.txt",)

SOURCE_SCREENSHOT_PACKAGE_DIR = Path("docs") / "evidence" / "source_screenshot_share_2026_06_18"
EMAIL_SCREENSHOT_PACKAGE_DIR = SOURCE_SCREENSHOT_PACKAGE_DIR / "email_screenshots_2026_06_12"
SLIDE02_SOURCE_PACKAGE_DIR = SOURCE_SCREENSHOT_PACKAGE_DIR / "slide02_source_bundle_2026_06_17"

EMAIL_SCREENSHOT_EVIDENCE_FILES = (
    "contact_sheet.png",
    "README.md",
    "screenshot_2026-06-05_131418.png",
    "screenshot_2026-06-05_131426.png",
    "screenshot_2026-06-08_111056.png",
    "screenshot_2026-06-08_111108.png",
    "screenshot_2026-06-08_111117.png",
    "screenshot_2026-06-08_111124.png",
    "screenshot_2026-06-09_150342.png",
    "screenshot_2026-06-09_150348.png",
    "screenshot_2026-06-09_152213.png",
    "screenshot_2026-06-09_152220.png",
)

SLIDE02_SOURCE_EVIDENCE_FILES = (
    "README.md",
    "slide02_selected_01_usgs_hydrate_context_page3.png",
    "slide02_selected_02_usgs_hydrate_stability_curve_crop.png",
    "slide02_selected_03_project_digitized_methane_5ppt_curve.csv",
    "slide02_selected_04_project_website_regional_map_reference.png",
)

TOKENS = {
    "surface": "#FCFCFD",
    "panel": "#FFFFFF",
    "ink": "#1F2430",
    "muted": "#6F768A",
    "grid": "#E6E8F0",
    "axis": "#D7DBE7",
    "blue_xlight": "#EAF1FE",
    "blue_light": "#CEDFFE",
    "blue_base": "#A3BEFA",
    "blue_mid": "#5477C4",
    "blue_dark": "#2E4780",
    "gold_xlight": "#FFF4C2",
    "gold_base": "#FFE15B",
    "gold_dark": "#736422",
    "orange_xlight": "#FFEDDE",
    "orange_base": "#F0986E",
    "orange_dark": "#804126",
    "olive_xlight": "#D8ECBD",
    "olive_base": "#A3D576",
    "olive_dark": "#386411",
    "pink_xlight": "#FCDAD6",
    "pink_base": "#F390CA",
    "pink_dark": "#8A3A6F",
    "neutral_xlight": "#F4F5F7",
    "neutral_light": "#E2E5EA",
    "neutral_mid": "#7A828F",
    "neutral_dark": "#464C55",
}

TARGET_HINTS = (
    "sgh",
    "s_h",
    "sh",
    "nmr_sat",
    "hydrate saturation",
    "swr",
    "s_wr",
    "phase",
    "occurrence",
    "label",
)

SKIP_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".venv",
    ".venv-dashboard",
    ".codex_runtime",
    "node_modules",
    "AppData",
    "models_runtime",
    "logs_runtime",
}


@dataclass(frozen=True)
class OutputRecord:
    filename: str
    source_script: str
    input_data_used: str
    safe_for_github: str
    intended_use: str
    sensitivity_limitation: str


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(PROJECT_ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return str(path)


def safe_read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def output_dirs(project_root: Path) -> dict[str, Path]:
    dirs = {
        "figures": project_root / "outputs_runtime" / "figures",
        "tables": project_root / "outputs_runtime" / "tables",
        "slides": project_root / "outputs_runtime" / "slide_exports",
        "paper": project_root / "outputs_runtime" / "paper_exports",
    }
    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)
    return dirs


def candidate_search_roots(project_root: Path, data_dir: Path | None) -> list[Path]:
    roots: list[Path] = []
    if data_dir is not None:
        roots.append(data_dir)
    home = Path.home()
    documents = home / "Documents"
    roots.extend(
        [
            project_root,
            home / "Downloads" / "Northslopedatasets06052026",
            home / "Downloads",
            home / "Desktop",
            home / "OneDrive",
            documents / "ai-powerpoint-workflow-portfolio",
            documents / "north-slope-gas-hydrates-v55",
            documents / "north-slope-gas-hydrates-paper-20260617",
            documents / "north-slope-gas-hydrates-source-intake-20260617",
            documents / "north-slope-gas-hydrates-slide2-20260617",
        ]
    )
    unique: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        try:
            key = str(root.resolve()).lower()
        except OSError:
            key = str(root).lower()
        if key not in seen and root.exists():
            unique.append(root)
            seen.add(key)
    return unique


def iter_files_limited(root: Path, max_files: int = 250_000):
    stack = [root]
    seen_files = 0
    while stack:
        current = stack.pop()
        try:
            entries = list(current.iterdir())
        except (OSError, PermissionError):
            continue
        for entry in entries:
            if entry.is_dir():
                if entry.name in SKIP_DIR_NAMES:
                    continue
                stack.append(entry)
            elif entry.is_file():
                seen_files += 1
                if seen_files > max_files:
                    return
                yield entry


def find_by_name(names: tuple[str, ...], roots: list[Path]) -> dict[str, list[Path]]:
    wanted = {name.lower(): name for name in names}
    matches: dict[str, list[Path]] = {name: [] for name in names}
    for root in roots:
        for path in iter_files_limited(root):
            key = path.name.lower()
            if key in wanted:
                matches[wanted[key]].append(path)
    return matches


def find_by_patterns(patterns: tuple[str, ...], roots: list[Path]) -> dict[str, list[Path]]:
    compiled = [(pattern, re.compile(fnmatch_to_regex(pattern), re.IGNORECASE)) for pattern in patterns]
    matches: dict[str, list[Path]] = {pattern: [] for pattern in patterns}
    for root in roots:
        for path in iter_files_limited(root):
            for pattern, regex in compiled:
                if regex.fullmatch(path.name):
                    matches[pattern].append(path)
    return matches


def fnmatch_to_regex(pattern: str) -> str:
    escaped = ""
    for character in pattern:
        if character == "*":
            escaped += ".*"
        elif character == "?":
            escaped += "."
        else:
            escaped += re.escape(character)
    return escaped


def col_to_num(col: str) -> int:
    result = 0
    for character in col.upper():
        if "A" <= character <= "Z":
            result = result * 26 + (ord(character) - ord("A") + 1)
    return result


def parse_excel_dimension(ref_value: str) -> tuple[int | None, int | None]:
    if not ref_value:
        return None, None
    last_ref = ref_value.split(":")[-1]
    match = re.match(r"([A-Z]+)([0-9]+)", last_ref, flags=re.IGNORECASE)
    if not match:
        return None, None
    return int(match.group(2)), col_to_num(match.group(1))


def workbook_sheet_paths(zf: zipfile.ZipFile) -> dict[str, str]:
    workbook = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    ns = {
        "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
        "rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
        "pkg": "http://schemas.openxmlformats.org/package/2006/relationships",
    }
    rel_lookup = {
        rel.attrib["Id"]: rel.attrib["Target"].lstrip("/")
        for rel in rels.findall("pkg:Relationship", ns)
    }
    paths: dict[str, str] = {}
    for sheet in workbook.findall("main:sheets/main:sheet", ns):
        name = sheet.attrib.get("name", "Sheet")
        rid = sheet.attrib.get(f"{{{ns['rel']}}}id", "")
        target = rel_lookup.get(rid, "")
        if target and not target.startswith("xl/"):
            target = f"xl/{target}"
        if target:
            paths[name] = target
    return paths


def sheet_dimensions(zf: zipfile.ZipFile, sheet_path: str) -> tuple[int | None, int | None, list[str]]:
    root = ET.fromstring(zf.read(sheet_path))
    ns = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    dimension = root.find("main:dimension", ns)
    rows = columns = None
    if dimension is not None:
        rows, columns = parse_excel_dimension(dimension.attrib.get("ref", ""))

    header_values: list[str] = []
    shared_strings = load_shared_strings(zf)
    sheet_data = root.find("main:sheetData", ns)
    if sheet_data is not None:
        first_row = sheet_data.find("main:row", ns)
        if first_row is not None:
            max_col = 0
            max_row = 0
            for row in sheet_data.findall("main:row", ns):
                try:
                    max_row = max(max_row, int(row.attrib.get("r", "0")))
                except ValueError:
                    pass
                for cell in row.findall("main:c", ns):
                    ref_value = cell.attrib.get("r", "")
                    match = re.match(r"([A-Z]+)([0-9]+)", ref_value, flags=re.IGNORECASE)
                    if match:
                        max_col = max(max_col, col_to_num(match.group(1)))
            rows = rows or max_row or None
            columns = columns or max_col or None
            for cell in first_row.findall("main:c", ns):
                header_values.append(read_cell_text(cell, shared_strings, ns))
    return rows, columns, [value for value in header_values if value]


def load_shared_strings(zf: zipfile.ZipFile) -> list[str]:
    try:
        payload = zf.read("xl/sharedStrings.xml")
    except KeyError:
        return []
    root = ET.fromstring(payload)
    ns = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    values: list[str] = []
    for item in root.findall("main:si", ns):
        chunks = [node.text or "" for node in item.findall(".//main:t", ns)]
        values.append("".join(chunks))
    return values


def read_cell_text(cell: ET.Element, shared_strings: list[str], ns: dict[str, str]) -> str:
    value_node = cell.find("main:v", ns)
    if value_node is None or value_node.text is None:
        inline = cell.find("main:is/main:t", ns)
        return inline.text or "" if inline is not None else ""
    raw = value_node.text
    if cell.attrib.get("t") == "s":
        try:
            return shared_strings[int(raw)]
        except (ValueError, IndexError):
            return ""
    return raw


def inspect_xlsx_metadata(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        with zipfile.ZipFile(path) as zf:
            for sheet_name, sheet_path in workbook_sheet_paths(zf).items():
                row_count, column_count, headers = sheet_dimensions(zf, sheet_path)
                rows.append(
                    {
                        "workbook": path.name,
                        "located_path": str(path),
                        "sheet_name": sheet_name,
                        "row_count_estimate": row_count,
                        "column_count_estimate": column_count,
                        "target_like_header_count": sum(
                            1 for header in headers if any(hint in header.lower() for hint in TARGET_HINTS)
                        ),
                        "status": "metadata_read_no_row_values",
                    }
                )
    except (zipfile.BadZipFile, KeyError, ET.ParseError, OSError) as exc:
        rows.append(
            {
                "workbook": path.name,
                "located_path": str(path),
                "sheet_name": "",
                "row_count_estimate": None,
                "column_count_estimate": None,
                "target_like_header_count": None,
                "status": f"metadata_read_failed:{type(exc).__name__}",
            }
        )
    return rows


def discover_dataset_inventory(project_root: Path, data_dir: Path | None) -> tuple[pd.DataFrame, dict[str, list[Path]]]:
    roots = candidate_search_roots(project_root, data_dir)
    matches = find_by_name((*EXPECTED_DATASETS, *OPTIONAL_CONTEXT_FILES), roots)
    rows: list[dict[str, Any]] = []
    for workbook in EXPECTED_DATASETS:
        paths = matches.get(workbook, [])
        if paths:
            rows.extend(inspect_xlsx_metadata(paths[0]))
        else:
            rows.append(
                {
                    "workbook": workbook,
                    "located_path": "",
                    "sheet_name": "",
                    "row_count_estimate": None,
                    "column_count_estimate": None,
                    "target_like_header_count": None,
                    "status": "missing_by_exact_filename_search",
                }
            )
    for context_file in OPTIONAL_CONTEXT_FILES:
        paths = matches.get(context_file, [])
        rows.append(
            {
                "workbook": context_file,
                "located_path": str(paths[0]) if paths else "",
                "sheet_name": "context_file_not_read",
                "row_count_estimate": None,
                "column_count_estimate": None,
                "target_like_header_count": None,
                "status": "located_not_read" if paths else "missing_by_exact_filename_search",
            }
        )
    return pd.DataFrame(rows), matches


def locate_source_bundle(project_root: Path) -> pd.DataFrame:
    roots = candidate_search_roots(project_root, None)
    patterns = (
        "*north_slope_stability_sources*",
        "source_screenshot_share_2026_06_18.zip",
        "contact_sheet.png",
        "screenshot_2026-06-09_150342.png",
        "screenshot_2026-06-09_150348.png",
        "*source_library*.zip",
        "*North_Slope_Curated_Source_Library*",
    )
    matches = find_by_patterns(patterns, roots)
    rows: list[dict[str, Any]] = []

    explicit_sources = (
        {
            "search_pattern": "source_screenshot_share_2026_06_18 extracted package",
            "base_path": project_root / SOURCE_SCREENSHOT_PACKAGE_DIR,
            "required_files": ("README.md",),
            "evidence_type": "packaged screenshot/source handoff",
            "support_note": "Downloaded from Gmail and extracted into repo evidence area.",
        },
        {
            "search_pattern": "email_screenshots_2026_06_12 package evidence",
            "base_path": project_root / EMAIL_SCREENSHOT_PACKAGE_DIR,
            "required_files": EMAIL_SCREENSHOT_EVIDENCE_FILES,
            "evidence_type": "header equation and project-goal screenshots",
            "support_note": "Screenshot evidence for visible headers, target-only labels, equations, and project objectives.",
        },
        {
            "search_pattern": "slide02_source_bundle_2026_06_17 package evidence",
            "base_path": project_root / SLIDE02_SOURCE_PACKAGE_DIR,
            "required_files": SLIDE02_SOURCE_EVIDENCE_FILES,
            "evidence_type": "Slide 2 source-backed visual bundle",
            "support_note": "Source-backed hydrate context, stability curve, digitized methane 5 ppt curve, and website map reference.",
        },
    )
    for source in explicit_sources:
        base_path = source["base_path"]
        required_files = source["required_files"]
        found_files = [base_path / filename for filename in required_files if (base_path / filename).exists()]
        rows.append(
            {
                "search_pattern": source["search_pattern"],
                "matches_found": len(found_files),
                "preferred_path": str(base_path) if base_path.exists() else "",
                "status": "source_screenshot_supported" if len(found_files) == len(required_files) else "missing",
                "evidence_type": source["evidence_type"],
                "support_note": source["support_note"],
            }
        )

    for pattern, paths in matches.items():
        preferred = sorted(paths, key=lambda path: (0 if project_root in path.parents else 1, len(str(path))))
        rows.append(
            {
                "search_pattern": pattern,
                "matches_found": len(paths),
                "preferred_path": str(preferred[0]) if preferred else "",
                "status": "located" if preferred else "missing",
                "evidence_type": "filesystem search",
                "support_note": "Generic local search result.",
            }
        )
    return pd.DataFrame(rows)


def apply_layout(fig: go.Figure, title: str, subtitle: str, width: int = 1500, height: int = 900) -> go.Figure:
    fig.update_layout(
        width=width,
        height=height,
        paper_bgcolor=TOKENS["surface"],
        plot_bgcolor=TOKENS["panel"],
        margin=dict(l=70, r=50, t=120, b=70),
        font=dict(family="Aptos, Segoe UI, Arial, sans-serif", color=TOKENS["ink"], size=18),
        title=dict(
            text=f"<b>{html.escape(title)}</b><br><span style='font-size:16px;color:{TOKENS['muted']}'>{html.escape(subtitle)}</span>",
            x=0.055,
            y=0.975,
            xanchor="left",
            yanchor="top",
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_xaxes(showline=True, linewidth=1, linecolor=TOKENS["axis"], gridcolor=TOKENS["grid"])
    fig.update_yaxes(showline=True, linewidth=1, linecolor=TOKENS["axis"], gridcolor=TOKENS["grid"])
    return fig


def export_figure(
    fig: go.Figure,
    stem: str,
    dirs: dict[str, Path],
    records: list[OutputRecord],
    *,
    input_data_used: str,
    safe_for_github: str,
    intended_use: str,
    sensitivity_limitation: str,
    paper: bool = True,
    slides: bool = True,
) -> list[Path]:
    paths: list[Path] = []
    for ext in ("png", "svg", "pdf"):
        path = dirs["figures"] / f"{stem}.{ext}"
        if FORCE_FIGURE_EXPORT or not path.exists():
            fig.write_image(str(path), scale=2)
        paths.append(path)
        records.append(
            OutputRecord(
                filename=rel(path),
                source_script=rel(Path(__file__)),
                input_data_used=input_data_used,
                safe_for_github=safe_for_github,
                intended_use=intended_use,
                sensitivity_limitation=sensitivity_limitation,
            )
        )
        if slides and ext == "png":
            slide_path = dirs["slides"] / path.name
            shutil.copyfile(path, slide_path)
            records.append(
                OutputRecord(
                    filename=rel(slide_path),
                    source_script=rel(Path(__file__)),
                    input_data_used=input_data_used,
                    safe_for_github=safe_for_github,
                    intended_use="slides",
                    sensitivity_limitation=sensitivity_limitation,
                )
            )
        if paper:
            paper_path = dirs["paper"] / path.name
            shutil.copyfile(path, paper_path)
            records.append(
                OutputRecord(
                    filename=rel(paper_path),
                    source_script=rel(Path(__file__)),
                    input_data_used=input_data_used,
                    safe_for_github=safe_for_github,
                    intended_use="paper",
                    sensitivity_limitation=sensitivity_limitation,
                )
            )
    return paths


def write_table(
    frame: pd.DataFrame,
    stem: str,
    dirs: dict[str, Path],
    records: list[OutputRecord],
    *,
    input_data_used: str,
    safe_for_github: str,
    intended_use: str,
    sensitivity_limitation: str,
) -> Path:
    path = dirs["tables"] / f"{stem}.csv"
    frame.to_csv(path, index=False)
    records.append(
        OutputRecord(
            filename=rel(path),
            source_script=rel(Path(__file__)),
            input_data_used=input_data_used,
            safe_for_github=safe_for_github,
            intended_use=intended_use,
            sensitivity_limitation=sensitivity_limitation,
        )
    )
    return path


def export_table_visual(
    frame: pd.DataFrame,
    stem: str,
    dirs: dict[str, Path],
    records: list[OutputRecord],
    *,
    title: str,
    subtitle: str,
    input_data_used: str,
    safe_for_github: str,
    intended_use: str,
    sensitivity_limitation: str,
    max_rows: int = 12,
    row_height: int = 42,
) -> None:
    visual = frame.head(max_rows).fillna("").copy()
    cell_values = [visual[column].astype(str).tolist() for column in visual.columns]
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=[f"<b>{html.escape(str(column))}</b>" for column in visual.columns],
                    fill_color=TOKENS["blue_dark"],
                    font=dict(color="white", size=15),
                    align="left",
                    height=34,
                ),
                cells=dict(
                    values=cell_values,
                    fill_color=[
                        [TOKENS["panel"] if idx % 2 == 0 else TOKENS["neutral_xlight"] for idx in range(len(visual))]
                    ],
                    align="left",
                    font=dict(color=TOKENS["ink"], size=13),
                    height=row_height,
                ),
            )
        ]
    )
    apply_layout(fig, title, subtitle, width=1800, height=max(760, 230 + (row_height + 12) * len(visual)))
    export_figure(
        fig,
        stem,
        dirs,
        records,
        input_data_used=input_data_used,
        safe_for_github=safe_for_github,
        intended_use=intended_use,
        sensitivity_limitation=sensitivity_limitation,
    )


def build_dataset_inventory_figure(inventory: pd.DataFrame) -> go.Figure:
    located = inventory.loc[inventory["status"].astype(str).str.contains("metadata_read|located", regex=True)]
    workbook_rows = inventory[inventory["workbook"].isin(EXPECTED_DATASETS)].copy()
    missing_count = int(workbook_rows["status"].astype(str).str.contains("missing").sum())
    if workbook_rows["status"].astype(str).str.contains("metadata_read").any():
        plot_df = workbook_rows.copy()
        plot_df["sheet_label"] = plot_df["workbook"].astype(str) + "<br>" + plot_df["sheet_name"].astype(str)
        fig = go.Figure()
        fig.add_bar(
            x=plot_df["sheet_label"],
            y=pd.to_numeric(plot_df["row_count_estimate"], errors="coerce").fillna(0),
            name="Rows",
            marker=dict(color=TOKENS["blue_base"], line=dict(color=TOKENS["blue_dark"], width=1)),
        )
        fig.add_bar(
            x=plot_df["sheet_label"],
            y=pd.to_numeric(plot_df["column_count_estimate"], errors="coerce").fillna(0),
            name="Columns",
            marker=dict(color=TOKENS["gold_base"], line=dict(color=TOKENS["gold_dark"], width=1)),
            yaxis="y2",
        )
        fig.update_layout(
            barmode="group",
            yaxis=dict(title="Estimated rows"),
            yaxis2=dict(title="Estimated columns", overlaying="y", side="right", showgrid=False),
        )
    else:
        fig = go.Figure()
        labels = ["Expected workbooks", "Located workbooks", "Missing workbooks", "Context files located"]
        values = [
            len(EXPECTED_DATASETS),
            int(
                workbook_rows["status"]
                .astype(str)
                .str.contains("metadata_read", regex=False)
                .sum()
            ),
            missing_count,
            int(inventory["status"].astype(str).eq("located_not_read").sum()),
        ]
        colors = [TOKENS["blue_base"], TOKENS["olive_base"], TOKENS["orange_base"], TOKENS["gold_base"]]
        fig.add_bar(
            x=labels,
            y=values,
            marker=dict(color=colors, line=dict(color=TOKENS["neutral_dark"], width=1)),
            text=values,
            textposition="outside",
        )
        fig.update_yaxes(title="File count", range=[0, max(values + [1]) + 1])
    return apply_layout(
        fig,
        "Dataset inventory status",
        "Workbook/sheet metadata only. No approved data rows, well identifiers, or row-level values are displayed.",
    )


def schema_coverage_summary(field_roles: pd.DataFrame, schema_matrix: pd.DataFrame) -> pd.DataFrame:
    role_map = {
        "predictor": "Measured log fields",
        "derived_feature": "Derived physics features",
        "target_only": "Target-only saturation fields",
        "calibration_reference": "Target-only saturation fields",
        "QC": "QC/alignment fields",
        "context": "QC/alignment fields",
        "unresolved": "Unresolved fields",
    }
    if not field_roles.empty and "role" in field_roles:
        summary = (
            field_roles.assign(coverage_group=field_roles["role"].map(role_map).fillna("Unresolved fields"))
            .groupby("coverage_group", dropna=False)
            .agg(field_count=("original_header", "count"), examples=("original_header", lambda values: "; ".join(map(str, values.head(5)))))
            .reset_index()
        )
    else:
        summary = pd.DataFrame(columns=["coverage_group", "field_count", "examples"])
    for group in [
        "Measured log fields",
        "Derived physics features",
        "Target-only saturation fields",
        "QC/alignment fields",
        "Unresolved fields",
    ]:
        if group not in set(summary["coverage_group"]):
            summary.loc[len(summary)] = [group, 0, ""]
    order = {
        "Measured log fields": 0,
        "Derived physics features": 1,
        "Target-only saturation fields": 2,
        "QC/alignment fields": 3,
        "Unresolved fields": 4,
    }
    return summary.assign(order=summary["coverage_group"].map(order)).sort_values("order").drop(columns="order")


def build_schema_coverage_figure(summary: pd.DataFrame) -> go.Figure:
    colors = {
        "Measured log fields": TOKENS["blue_base"],
        "Derived physics features": TOKENS["gold_base"],
        "Target-only saturation fields": TOKENS["pink_base"],
        "QC/alignment fields": TOKENS["olive_base"],
        "Unresolved fields": TOKENS["orange_base"],
    }
    fig = go.Figure(
        go.Bar(
            x=summary["field_count"],
            y=summary["coverage_group"],
            orientation="h",
            marker=dict(
                color=[colors.get(group, TOKENS["neutral_light"]) for group in summary["coverage_group"]],
                line=dict(color=TOKENS["neutral_dark"], width=1),
            ),
            text=summary["field_count"],
            textposition="outside",
            hovertext=summary["examples"],
        )
    )
    fig.update_yaxes(autorange="reversed", title="")
    fig.update_xaxes(title="Header/field count")
    return apply_layout(
        fig,
        "Schema coverage by field role",
        "Counts are from public-safe header/role metadata, not approved workbook rows.",
        width=1500,
        height=820,
    )


def workflow_table() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "stage": "Dataset intake",
                "runtime action": "Locate three curated workbooks by filename and keep them in ignored runtime folders.",
                "public-safe output": "Workbook and sheet counts only.",
                "guardrail": "No raw rows or restricted identifiers.",
            },
            {
                "stage": "Header preservation",
                "runtime action": "Preserve workbook, sheet, original header, unit, and source role before aliasing.",
                "public-safe output": "Header/role inventory.",
                "guardrail": "Original names stay visible; no row values leave runtime.",
            },
            {
                "stage": "Schema discovery",
                "runtime action": "Classify measured logs, derived features, QC/alignment, targets, and unresolved columns.",
                "public-safe output": "Schema coverage chart and field-role table.",
                "guardrail": "Unresolved mnemonics fail closed.",
            },
            {
                "stage": "Leakage screening",
                "runtime action": "Build X_allowed after excluding saturation, phase, occurrence, and target-derived columns.",
                "public-safe output": "Leakage-control summary.",
                "guardrail": "Saturation and occurrence labels never enter predictors.",
            },
            {
                "stage": "Train/test/external scoring",
                "runtime action": "Train on dataset 1 or approved target workbook; score dataset 2/3 as external workbooks.",
                "public-safe output": "Summary-level metric status if approved.",
                "guardrail": "Training-fit metrics are not final science claims.",
            },
            {
                "stage": "Model tracker summary",
                "runtime action": "Read run_summary/train_metrics/features/exclusions only; skip prediction files.",
                "public-safe output": "Target cards and blocker summary.",
                "guardrail": "No row-level predictions or fitted model files.",
            },
        ]
    )


def build_workflow_figure() -> go.Figure:
    stages = workflow_table()
    fig = go.Figure()
    positions = [
        (0.18, 0.68),
        (0.50, 0.68),
        (0.82, 0.68),
        (0.18, 0.39),
        (0.50, 0.39),
        (0.82, 0.39),
    ]
    colors = [TOKENS["blue_base"], TOKENS["gold_base"], TOKENS["olive_base"], TOKENS["pink_base"], TOKENS["orange_base"], TOKENS["blue_light"]]
    for idx, row in stages.iterrows():
        x, y = positions[idx]
        fig.add_shape(
            type="rect",
            x0=x - 0.135,
            x1=x + 0.135,
            y0=y - 0.095,
            y1=y + 0.095,
            xref="paper",
            yref="paper",
            fillcolor=colors[idx],
            line=dict(color=TOKENS["neutral_dark"], width=1.2),
        )
        stage = "<br>".join(textwrap.wrap(str(row["stage"]), width=22, break_long_words=False))
        guardrail = "<br>".join(textwrap.wrap(str(row["guardrail"]), width=34, break_long_words=False))
        text = f"<b>{idx + 1}. {stage}</b><br><span style='font-size:12px'>{guardrail}</span>"
        fig.add_annotation(x=x, y=y, xref="paper", yref="paper", text=text, showarrow=False, align="center", font=dict(size=14))
        if idx < len(stages) - 1:
            x2, y2 = positions[idx + 1]
            if y == y2:
                line_start = x + 0.145
                line_end = x2 - 0.145
                line_y0 = y
                line_y1 = y2
                arrow_x = line_end
                arrow_y = y2
                arrow_text = ">"
            else:
                line_start = x
                line_end = x2
                line_y0 = y - 0.105
                line_y1 = y2 + 0.105
                arrow_x = x2
                arrow_y = y2 + 0.105
                arrow_text = "v"
            fig.add_shape(
                type="line",
                x0=line_start,
                x1=line_end,
                y0=line_y0,
                y1=line_y1,
                xref="paper",
                yref="paper",
                line=dict(color=TOKENS["neutral_dark"], width=1.4),
            )
            fig.add_annotation(
                x=arrow_x,
                y=arrow_y,
                xref="paper",
                yref="paper",
                showarrow=False,
                text=arrow_text,
                font=dict(size=18, color=TOKENS["neutral_dark"]),
            )
    fig.add_annotation(
        x=0.5,
        y=0.13,
        xref="paper",
        yref="paper",
        text="<b>Runtime-only rail:</b> approved rows, well identifiers, row-level predictions, fitted scalers, and trained models stay ignored/local.",
        showarrow=False,
        font=dict(size=18, color=TOKENS["ink"]),
        bgcolor=TOKENS["neutral_xlight"],
        bordercolor=TOKENS["axis"],
        borderwidth=1,
        borderpad=10,
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return apply_layout(
        fig,
        "Three-dataset ML workflow",
        "From curated workbook intake to row-free model tracker summaries.",
        width=1800,
        height=900,
    )


def equation_summary_table() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "equation name": "Hydrostatic pressure",
                "input measurements": "depth_m; pore-pressure gradient",
                "derived feature": "pressure_mpa",
                "ML role": "stability/context gate",
                "limitation": "baseline assumption; not hydrate proof",
            },
            {
                "equation name": "Temperature gradient model",
                "input measurements": "surface/shallow temperature; geothermal gradient; depth_m",
                "derived feature": "temperature_c",
                "ML role": "stability/context gate",
                "limitation": "requires source-control confidence; local gradients can vary",
            },
            {
                "equation name": "Methane 5 ppt phase lookup",
                "input measurements": "pressure_mpa; temperature_c; digitized USGS phase curve",
                "derived feature": "stability_admissibility",
                "ML role": "context, mask, caveat",
                "limitation": "admissible is not occurrence or saturation",
            },
            {
                "equation name": "Density porosity",
                "input measurements": "RHOB/Rho_b; matrix and fluid density assumptions",
                "derived feature": "density_porosity_vv",
                "ML role": "reservoir-quality feature",
                "limitation": "unit and mineral assumptions must be confirmed",
            },
            {
                "equation name": "Vp from sonic slowness",
                "input measurements": "DT or direct Vp",
                "derived feature": "vp_km_s",
                "ML role": "elastic input and impedance source",
                "limitation": "do not mix direct velocity and slowness-derived velocity silently",
            },
            {
                "equation name": "Vs from shear slowness",
                "input measurements": "DTS or direct Vs",
                "derived feature": "vs_km_s",
                "ML role": "rigidity input and gas/hydrate mimic control",
                "limitation": "missing Vs may block elastic feature family",
            },
            {
                "equation name": "Vp/Vs ratio",
                "input measurements": "Vp; Vs",
                "derived feature": "vp_vs_ratio",
                "ML role": "crossplot and nonlinear feature",
                "limitation": "overlaps among hydrate, gas, water, shale, ice, and lithology",
            },
            {
                "equation name": "Acoustic impedance",
                "input measurements": "rho_b; Vp",
                "derived feature": "acoustic_impedance",
                "ML role": "stiffness/contrast feature",
                "limitation": "inherits density, velocity, and unit errors",
            },
            {
                "equation name": "Elastic moduli and lambda/mu-rho",
                "input measurements": "rho_b; Vp; Vs",
                "derived feature": "G; K; E; nu; lambda-rho; mu-rho",
                "ML role": "derived physics feature block",
                "limitation": "calculate only after unit and QC gates pass",
            },
            {
                "equation name": "Archie-style saturation baseline",
                "input measurements": "Rt; phi; Rw; a; m; n; shale correction",
                "derived feature": "Sw or Sh baseline",
                "ML role": "physics baseline or validation reference",
                "limitation": "target-like when used as saturation label; keep out of X_allowed",
            },
        ]
    )


def leakage_table(field_roles: pd.DataFrame) -> pd.DataFrame:
    allowed = field_roles[field_roles["role"].isin(["predictor", "derived_feature", "QC", "context"])] if not field_roles.empty else pd.DataFrame()
    blocked = field_roles[field_roles["role"].isin(["target_only", "calibration_reference", "unresolved"])] if not field_roles.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            {
                "rail": "Allowed predictors",
                "field_count": len(allowed),
                "examples": "; ".join(allowed["original_header"].astype(str).head(10)) if not allowed.empty else "",
                "rule": "Measured logs, derived physics features, QC, and context only after unit/QC review.",
            },
            {
                "rail": "Excluded target-like columns",
                "field_count": len(blocked),
                "examples": "; ".join(blocked["original_header"].astype(str).head(10)) if not blocked.empty else "",
                "rule": "Saturation, phase, occurrence, calibration/reference, and unresolved headers bypass X_allowed.",
            },
            {
                "rail": "Target-only saturation fields",
                "field_count": int(field_roles["original_header"].astype(str).str.contains("Sgh|S_h|^Sh$|NMR_SAT|Hydrate Saturation|Swr|S_wr", regex=True).sum())
                if not field_roles.empty
                else 0,
                "examples": "Sgh; S_h; Sh; NMR_SAT; Hydrate Saturation; Swr; S_wr",
                "rule": "Y-only for training labels, calibration, validation, or residual review after target authority.",
            },
        ]
    )


def build_leakage_figure(leakage: pd.DataFrame) -> go.Figure:
    values = {row["rail"]: int(row["field_count"]) for _, row in leakage.iterrows()}
    plot_df = pd.DataFrame(
        [
            {
                "rail": "Allowed predictors",
                "field_count": values.get("Allowed predictors", 0),
                "rule": "Eligible for X_allowed after unit/QC review",
                "color": TOKENS["blue_base"],
            },
            {
                "rail": "Excluded target-like columns",
                "field_count": values.get("Excluded target-like columns", 0),
                "rule": "Blocked from predictors pending target authority review",
                "color": TOKENS["orange_base"],
            },
            {
                "rail": "Target-only saturation fields",
                "field_count": values.get("Target-only saturation fields", 0),
                "rule": "Y-only labels, calibration, validation, or residual review",
                "color": TOKENS["pink_base"],
            },
        ]
    )
    fig = go.Figure(
        go.Bar(
            x=plot_df["field_count"],
            y=plot_df["rail"],
            orientation="h",
            marker=dict(color=plot_df["color"], line=dict(color=TOKENS["neutral_dark"], width=1)),
            text=plot_df["field_count"],
            textposition="outside",
            hovertext=plot_df["rule"],
        )
    )
    for idx, row in plot_df.iterrows():
        fig.add_annotation(
            x=0.02,
            y=row["rail"],
            xref="paper",
            yref="y",
            showarrow=False,
            xanchor="left",
            align="left",
            text=row["rule"],
            font=dict(size=14, color=TOKENS["muted"]),
            yshift=-28,
        )
    fig.add_annotation(
        x=0.5,
        y=-0.2,
        xref="paper",
        yref="paper",
        showarrow=False,
        text="Guardrail: saturation, occurrence, calibration/reference, unresolved, and target-derived fields do not enter predictor matrices.",
        font=dict(size=16, color=TOKENS["muted"]),
    )
    fig.update_yaxes(autorange="reversed", title="")
    fig.update_xaxes(title="Header/field count")
    return apply_layout(
        fig,
        "Target leakage control",
        "Saturation and interpreted-label columns are Y-only; allowed predictors remain separate.",
        width=1500,
        height=820,
    )


def model_run_summary(project_root: Path) -> pd.DataFrame:
    output_root = project_root / "outputs_runtime"
    run_rows: list[dict[str, Any]] = []
    if output_root.exists():
        for run_dir in output_root.iterdir():
            if not run_dir.is_dir():
                continue
            run_summary = run_dir / "run_summary.csv"
            train_metrics = run_dir / "train_metrics.csv"
            feature_columns = run_dir / "feature_columns.csv"
            feature_by_target = run_dir / "feature_columns_by_target.csv"
            exclusions = run_dir / "excluded_feature_columns_by_target.csv"
            if not any(path.exists() for path in [run_summary, train_metrics, feature_columns, feature_by_target, exclusions]):
                continue
            summary = safe_read_csv(run_summary)
            train = safe_read_csv(train_metrics)
            features = safe_read_csv(feature_by_target if feature_by_target.exists() else feature_columns)
            excluded = safe_read_csv(exclusions)
            run_rows.append(
                {
                    "run_name": run_dir.name,
                    "target_runs": len(summary) if not summary.empty else len(train),
                    "feature_rows": len(features),
                    "excluded_feature_rows": len(excluded),
                    "metric_scope": "training_fit_only_or_summary",
                    "validation_status": "external_metrics_present" if (run_dir / "test_metrics.csv").exists() else "not_detected",
                    "final_claim_ready": False,
                    "sensitivity": "summary files only; prediction files deliberately ignored",
                }
            )
    if run_rows:
        return pd.DataFrame(run_rows)
    return pd.DataFrame(
        [
            {
                "run_name": "No local runtime model summaries detected",
                "target_runs": 0,
                "feature_rows": 0,
                "excluded_feature_rows": 0,
                "metric_scope": "not_available",
                "validation_status": "no outputs_runtime model tracker folder",
                "final_claim_ready": False,
                "sensitivity": "No row-level predictions or model metrics were read.",
            }
        ]
    )


def build_model_tracker_figure(model_summary: pd.DataFrame, dataset_inventory: pd.DataFrame) -> go.Figure:
    workbook_located = int(dataset_inventory["status"].astype(str).str.contains("metadata_read", regex=False).sum())
    run_count = int((model_summary["target_runs"] > 0).sum()) if "target_runs" in model_summary else 0
    values = [workbook_located, run_count, int(model_summary["target_runs"].sum()), 0]
    labels = ["Curated workbooks located", "Run folders with targets", "Summary target runs", "Public row-level outputs"]
    colors = [TOKENS["blue_base"], TOKENS["gold_base"], TOKENS["olive_base"], TOKENS["orange_base"]]
    fig = go.Figure(
        go.Bar(
            x=labels,
            y=values,
            marker=dict(color=colors, line=dict(color=TOKENS["neutral_dark"], width=1)),
            text=values,
            textposition="outside",
        )
    )
    fig.update_yaxes(title="Count", range=[0, max(values + [1]) + 1])
    fig.add_annotation(
        x=0.5,
        y=-0.20,
        xref="paper",
        yref="paper",
        showarrow=False,
        text="First-pass workflow/audit status only. Final DOE-calibrated claims require target authority, whole-well validation, and release review.",
        font=dict(size=16, color=TOKENS["muted"]),
    )
    return apply_layout(
        fig,
        "Model run tracker summary",
        "Summary-level runtime status; no prediction files, fitted models, well identifiers, or approved rows are exported.",
        width=1500,
        height=820,
    )


def source_support_table(project_root: Path, source_discovery: pd.DataFrame) -> pd.DataFrame:
    manifest = safe_read_csv(project_root / "references" / "hydrate-ml-physics-sources" / "2026-06-13" / "source_manifest.csv")
    rows: list[dict[str, Any]] = []
    if not manifest.empty:
        for _, row in manifest.head(16).iterrows():
            rows.append(
                {
                    "source": row.get("title", ""),
                    "status": row.get("status", ""),
                    "supports": row.get("deliverable_role", ""),
                    "limitation": row.get("notes", ""),
                }
            )
    package_rows = source_discovery[source_discovery["status"].eq("source_screenshot_supported")]
    for _, source_row in package_rows.iterrows():
        rows.append(
            {
                "source": source_row.get("search_pattern", "Local screenshot/source package"),
                "status": "source_screenshot_supported",
                "supports": source_row.get("support_note", "Screenshot evidence layer"),
                "limitation": "Screenshot evidence supports header, equation, and source-visual provenance only; no raw rows, well identifiers, or sensitive values are transcribed.",
            }
        )
    located_rows = source_discovery[source_discovery["status"].eq("located")]
    if not located_rows.empty:
        rows.append(
            {
                "source": "Additional local source search matches",
                "status": "located_metadata_only",
                "supports": "Supplemental filesystem evidence for source bundle discovery",
                "limitation": "Discovery metadata only; cite formal papers/reports rather than local paths or screenshots in manuscripts.",
            }
        )
    return pd.DataFrame(rows)


def limitations_table(dataset_inventory: pd.DataFrame, source_discovery: pd.DataFrame, model_summary: pd.DataFrame) -> pd.DataFrame:
    missing_workbooks = dataset_inventory[
        dataset_inventory["workbook"].isin(EXPECTED_DATASETS)
        & dataset_inventory["status"].astype(str).str.contains("missing")
    ]["workbook"].tolist()
    source_missing = source_discovery[source_discovery["status"].eq("missing")]["search_pattern"].tolist()
    screenshot_supported = bool(source_discovery["status"].eq("source_screenshot_supported").any())
    no_runs = bool(model_summary["target_runs"].sum() == 0) if "target_runs" in model_summary else True
    rows = [
        {
            "gap": "Curated workbook availability",
            "status": "blocked" if missing_workbooks else "available",
            "impact": "Dataset inventory and model summaries use located workbook metadata only when files are found.",
            "next action": "Place curated_dataset1/2/3.xlsx in the approved runtime folder and rerun the generator.",
        },
        {
            "gap": "Context file availability",
            "status": "available" if dataset_inventory["workbook"].eq("wellnametodataset.txt").any() and not dataset_inventory.loc[dataset_inventory["workbook"].eq("wellnametodataset.txt"), "status"].astype(str).str.contains("missing").any() else "not located",
            "impact": "Well-name mapping was not read; no identifiers are exposed.",
            "next action": "Use only anonymized/sanitized grouping summaries if needed.",
        },
        {
            "gap": "Source/screenshot bundle",
            "status": "source-screenshot-supported" if screenshot_supported else ("partial" if source_missing else "located"),
            "impact": "The emailed source screenshot package is integrated as a screenshot evidence layer; raw workbook files and some full source roots remain separate.",
            "next action": "Use the screenshot package for header/equation/source-visual provenance and cite formal papers/reports for manuscript claims.",
        },
        {
            "gap": "Model run tracker outputs",
            "status": "not detected" if no_runs else "summary detected",
            "impact": "No runtime metrics are claimed unless run_summary/train_metrics files exist.",
            "next action": "Rerun the DOE runtime pipeline, then export only public-safe summary files.",
        },
        {
            "gap": "Scientific claim level",
            "status": "methods/readiness only",
            "impact": "Figures support slide/paper methods and audit narrative, not final occurrence/saturation claims.",
            "next action": "Lock target authority, split policy, validation plan, and release review before claims.",
        },
    ]
    return pd.DataFrame(rows)


def write_manifest(records: list[OutputRecord], manifest_path: Path) -> None:
    lines = [
        f"# Visual Export Manifest {DATE_HUMAN}",
        "",
        "Generated by `01_pipeline/generate_slide_paper_visuals_2026_06_18.py`.",
        "",
        "Boundary: exported visuals are row-free summaries, diagrams, or public-safe tables. Runtime outputs remain under ignored `outputs_runtime/` unless separately reviewed for publication.",
        "",
        "| filename | source script | input data used | safe for GitHub | use | sensitivity limitation |",
        "|---|---|---|---|---|---|",
    ]
    for record in records:
        lines.append(
            "| "
            + " | ".join(
                html.escape(str(value)).replace("|", "\\|")
                for value in (
                    record.filename,
                    record.source_script,
                    record.input_data_used,
                    record.safe_for_github,
                    record.intended_use,
                    record.sensitivity_limitation,
                )
            )
            + " |"
        )
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest_csv(records: list[OutputRecord], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "filename",
                "source_script",
                "input_data_used",
                "safe_for_github",
                "intended_use",
                "sensitivity_limitation",
            ],
        )
        writer.writeheader()
        for record in records:
            writer.writerow(record.__dict__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate public-safe slide and paper visuals.")
    parser.add_argument("--data-dir", type=Path, help="Optional approved runtime data folder to search first.")
    parser.add_argument("--force-figures", action="store_true", help="Regenerate figure files even when outputs already exist.")
    args = parser.parse_args()
    global FORCE_FIGURE_EXPORT
    FORCE_FIGURE_EXPORT = args.force_figures

    dirs = output_dirs(PROJECT_ROOT)
    records: list[OutputRecord] = []

    field_roles = safe_read_csv(PROJECT_ROOT / "data" / "public_ml_products" / "approved_data_field_role_table_2026-06-15.csv")
    schema_matrix = safe_read_csv(PROJECT_ROOT / "data" / "public_ml_products" / "approved_schema_coverage_matrix_2026-06-15.csv")

    dataset_inventory, _dataset_matches = discover_dataset_inventory(PROJECT_ROOT, args.data_dir)
    source_discovery = locate_source_bundle(PROJECT_ROOT)
    schema_summary = schema_coverage_summary(field_roles, schema_matrix)
    equations = equation_summary_table()
    workflow = workflow_table()
    leakage = leakage_table(field_roles)
    model_summary = model_run_summary(PROJECT_ROOT)
    sources = source_support_table(PROJECT_ROOT, source_discovery)
    limitations = limitations_table(dataset_inventory, source_discovery, model_summary)

    write_table(
        dataset_inventory,
        f"dataset_inventory_summary_{DATE_STAMP}",
        dirs,
        records,
        input_data_used="Exact filename search for curated_dataset1/2/3.xlsx and wellnametodataset.txt; XLSX structure metadata only if located.",
        safe_for_github="conditional_review_required",
        intended_use="both",
        sensitivity_limitation="Workbook row values and well-name mapping are not read or exported.",
    )
    write_table(schema_summary, f"schema_coverage_summary_{DATE_STAMP}", dirs, records, input_data_used="data/public_ml_products/approved_data_field_role_table_2026-06-15.csv", safe_for_github="yes_public_safe", intended_use="both", sensitivity_limitation="Header/role metadata only.")
    write_table(equations, f"equation_summary_table_{DATE_STAMP}", dirs, records, input_data_used="SCIENCE_TO_ML_LOGIC_LADDER and ML_PIPELINE_BASELINE_SOURCE_LEDGER equation lists.", safe_for_github="yes_public_safe", intended_use="paper", sensitivity_limitation="Method table only; equations require unit confirmation before runtime calculations.")
    write_table(workflow, f"three_dataset_workflow_table_{DATE_STAMP}", dirs, records, input_data_used="DOE three-dataset runbook and approved-data intake docs.", safe_for_github="yes_public_safe", intended_use="paper", sensitivity_limitation="Workflow table only; no model outputs.")
    write_table(leakage, f"target_leakage_control_table_{DATE_STAMP}", dirs, records, input_data_used="Field-role table and leakage guardrail docs.", safe_for_github="yes_public_safe", intended_use="both", sensitivity_limitation="Header groups only; no target rows.")
    write_table(model_summary, f"model_run_tracker_public_safe_summary_{DATE_STAMP}", dirs, records, input_data_used="outputs_runtime run_summary/train_metrics/features summaries if present; prediction files ignored.", safe_for_github="conditional_review_required", intended_use="both", sensitivity_limitation="Summary-level only; no row-level predictions, models, or identifiers.")
    write_table(sources, f"source_support_table_{DATE_STAMP}", dirs, records, input_data_used="references/hydrate-ml-physics-sources/2026-06-13/source_manifest.csv and source/screenshot search.", safe_for_github="yes_public_safe", intended_use="paper", sensitivity_limitation="Source roles and limitations only; no copied article text.")
    write_table(limitations, f"limitations_gaps_table_{DATE_STAMP}", dirs, records, input_data_used="Dataset/source/model discovery status and project guardrails.", safe_for_github="yes_public_safe", intended_use="paper", sensitivity_limitation="Status and gaps only.")

    export_figure(
        build_dataset_inventory_figure(dataset_inventory),
        f"dataset_inventory_visual_{DATE_STAMP}",
        dirs,
        records,
        input_data_used="Exact filename search and XLSX workbook/sheet dimensions if files are located.",
        safe_for_github="conditional_review_required",
        intended_use="both",
        sensitivity_limitation="No raw workbook rows, well identifiers, row-level predictions, or sensitive values shown.",
    )
    export_figure(
        build_schema_coverage_figure(schema_summary),
        f"schema_coverage_visual_{DATE_STAMP}",
        dirs,
        records,
        input_data_used="Public-safe field-role table.",
        safe_for_github="yes_public_safe",
        intended_use="both",
        sensitivity_limitation="Header/role counts only.",
    )
    export_figure(
        build_workflow_figure(),
        f"three_dataset_ml_workflow_diagram_{DATE_STAMP}",
        dirs,
        records,
        input_data_used="DOE three-dataset runbook and approved-data intake docs.",
        safe_for_github="yes_public_safe",
        intended_use="both",
        sensitivity_limitation="Workflow logic only; not a model result.",
    )
    export_table_visual(
        equations,
        f"equation_to_ml_feature_map_{DATE_STAMP}",
        dirs,
        records,
        title="Equation-to-ML feature map",
        subtitle="Equation inputs, derived features, ML role, and limitations for the paper and slide methods.",
        input_data_used="Science-to-ML logic ladder and ML pipeline source ledger.",
        safe_for_github="yes_public_safe",
        intended_use="both",
        sensitivity_limitation="Method summary only; no runtime calculations or approved values.",
        max_rows=10,
    )
    export_figure(
        build_leakage_figure(leakage),
        f"target_leakage_control_visual_{DATE_STAMP}",
        dirs,
        records,
        input_data_used="Field-role table and target registry/leakage guardrails.",
        safe_for_github="yes_public_safe",
        intended_use="both",
        sensitivity_limitation="Header group counts only; targets remain Y-only.",
    )
    export_figure(
        build_model_tracker_figure(model_summary, dataset_inventory),
        f"model_run_tracker_summary_visual_{DATE_STAMP}",
        dirs,
        records,
        input_data_used="outputs_runtime summary files if present; otherwise local runtime discovery status.",
        safe_for_github="conditional_review_required",
        intended_use="both",
        sensitivity_limitation="First-pass workflow/audit status only; no final DOE-calibrated science claims.",
    )
    export_table_visual(
        sources,
        f"source_support_table_visual_{DATE_STAMP}",
        dirs,
        records,
        title="Source support table",
        subtitle="Source roles for slide and paper methods; source-paper metrics are not project results.",
        input_data_used="Hydrate ML/physics source manifest and screenshot/source discovery.",
        safe_for_github="yes_public_safe",
        intended_use="paper",
        sensitivity_limitation="Paraphrased source roles only; no restricted data.",
        max_rows=12,
        row_height=88,
    )
    manifest_csv = dirs["tables"] / f"visual_export_manifest_rows_{DATE_STAMP}.csv"
    write_manifest_csv(records, manifest_csv)
    records.append(
        OutputRecord(
            filename=rel(manifest_csv),
            source_script=rel(Path(__file__)),
            input_data_used="Generated export record list.",
            safe_for_github="yes_public_safe",
            intended_use="both",
            sensitivity_limitation="Lists filenames and input classes only.",
        )
    )
    docs_manifest = PROJECT_ROOT / "docs" / f"VISUAL_EXPORT_MANIFEST_{DATE_HUMAN}.md"
    write_manifest(records, docs_manifest)

    run_status = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "figures_dir": rel(dirs["figures"]),
        "tables_dir": rel(dirs["tables"]),
        "slide_exports_dir": rel(dirs["slides"]),
        "paper_exports_dir": rel(dirs["paper"]),
        "manifest": rel(docs_manifest),
        "dataset_workbooks_located": int(dataset_inventory["status"].astype(str).str.contains("metadata_read", regex=False).sum()),
        "model_summary_target_runs": int(model_summary["target_runs"].sum()) if "target_runs" in model_summary else 0,
        "guardrail": "No raw DOE rows, well identifiers, row-level predictions, or sensitive approved-data values were exported.",
    }
    status_path = dirs["tables"] / f"visual_export_run_status_{DATE_STAMP}.json"
    status_path.write_text(json.dumps(run_status, indent=2), encoding="utf-8")
    print(json.dumps(run_status, indent=2))


if __name__ == "__main__":
    main()
