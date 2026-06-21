from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np
import pandas as pd


REPO_MARKERS = (
    "PROJECT_CONTEXT.md",
    "data/public_stability_products/stability_screen_2026-06-14_methane_5ppt_v1.csv",
)
DEFAULT_CASE_ROLES = ("workbook_header_anchor", "public_source_case")


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if all((candidate / marker).exists() for marker in REPO_MARKERS):
            return candidate
    raise FileNotFoundError("Could not find the north-slope-gas-hydrates repo root.")


def default_output_dir(repo_root: Path) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return repo_root / "outputs_runtime" / f"spatial_stability_join_{stamp}"


def normalize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    output = frame.copy()
    output.columns = [str(column).strip() for column in output.columns]
    return output


def first_present(columns: list[str], candidates: tuple[str, ...]) -> str | None:
    normalized = {column.lower(): column for column in columns}
    for candidate in candidates:
        if candidate.lower() in normalized:
            return normalized[candidate.lower()]
    return None


def require_lat_lon(frame: pd.DataFrame, *, label: str) -> tuple[str, str]:
    columns = list(frame.columns)
    lat_col = first_present(columns, ("wellhead_latitude", "latitude", "lat", "case_lat"))
    lon_col = first_present(columns, ("wellhead_longitude", "longitude", "lon", "case_lon"))
    if lat_col is None or lon_col is None:
        raise ValueError(f"{label} needs latitude/longitude columns.")
    return lat_col, lon_col


def case_label(row: pd.Series) -> str:
    for column in ("map_label", "well_case", "verified_public_well_name", "well_name", "api_number"):
        value = row.get(column)
        if pd.notna(value) and str(value).strip():
            return str(value).strip()
    return "case_well"


def select_case_wells(case_wells: pd.DataFrame, case_roles: tuple[str, ...]) -> pd.DataFrame:
    wells = normalize_columns(case_wells)
    if "case_role" in wells.columns and case_roles:
        wells = wells[wells["case_role"].astype(str).isin(case_roles)].copy()
    lat_col, lon_col = require_lat_lon(wells, label="case wells")
    wells["case_lat"] = pd.to_numeric(wells[lat_col], errors="coerce")
    wells["case_lon"] = pd.to_numeric(wells[lon_col], errors="coerce")
    wells = wells.dropna(subset=["case_lat", "case_lon"]).copy()
    wells["case_label"] = wells.apply(case_label, axis=1)
    return wells.reset_index(drop=True)


def load_stability_screen(path: Path) -> pd.DataFrame:
    screen = normalize_columns(pd.read_csv(path))
    required = {"lat", "lon", "stability_result_status"}
    missing = sorted(required - set(screen.columns))
    if missing:
        raise ValueError(f"stability screen missing required columns: {missing}")
    screen["lat"] = pd.to_numeric(screen["lat"], errors="coerce")
    screen["lon"] = pd.to_numeric(screen["lon"], errors="coerce")
    return screen.dropna(subset=["lat", "lon"]).reset_index(drop=True)


def haversine_km(lat1: float, lon1: float, lat2: np.ndarray, lon2: np.ndarray) -> np.ndarray:
    earth_radius_km = 6371.0088
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2.astype(float))
    dphi = np.radians(lat2.astype(float) - lat1)
    dlambda = np.radians(lon2.astype(float) - lon1)
    a = np.sin(dphi / 2.0) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2.0) ** 2
    return 2.0 * earth_radius_km * np.arcsin(np.sqrt(a))


def comparable_api(value: Any) -> str:
    if pd.isna(value):
        return ""
    digits = "".join(character for character in str(value) if character.isdigit())
    return digits.lstrip("0") or digits


def choose_context_row(case: pd.Series, screen: pd.DataFrame, distances: np.ndarray) -> tuple[pd.Series, str, float]:
    case_api = comparable_api(case.get("api_number"))
    if case_api and "api_number" in screen.columns:
        api_values = screen["api_number"].map(comparable_api)
        matches = screen[api_values.eq(case_api)]
        if not matches.empty:
            match_index = int(matches.index[0])
            return screen.loc[match_index], "api_match", float(distances[match_index])
    nearest_index = int(np.nanargmin(distances))
    return screen.loc[nearest_index], "nearest_screen_point", float(distances[nearest_index])


def compact_status(row: pd.Series) -> dict[str, Any]:
    fields = [
        "well_name",
        "api_number",
        "field",
        "pool",
        "lat",
        "lon",
        "within_hydrate_assessment_unit",
        "hydrate_assessment_codes",
        "stability_result_status",
        "stability_confidence",
        "stability_top_m",
        "stability_base_m",
        "stability_thickness_m",
        "well_penetrated_stability_thickness_m",
        "permafrost_control_code",
        "permafrost_control_distance_km",
        "temperature_profile_code",
        "temperature_gradient_c_per_100m",
        "temperature_gradient_source",
        "phase_curve_id",
        "gas_composition_assumption",
        "salinity_ppt_assumption",
        "caveat_codes",
        "stability_notes",
    ]
    return {f"screen_{field}": row.get(field, "") for field in fields}


def spatial_join_case_wells(
    case_wells: pd.DataFrame,
    stability_screen: pd.DataFrame,
    *,
    case_roles: tuple[str, ...] = DEFAULT_CASE_ROLES,
    nearby_count: int = 5,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    cases = select_case_wells(case_wells, case_roles)
    screen = stability_screen.reset_index(drop=True)
    screen_lats = screen["lat"].to_numpy(dtype=float)
    screen_lons = screen["lon"].to_numpy(dtype=float)
    context_rows: list[dict[str, Any]] = []
    nearby_rows: list[dict[str, Any]] = []

    for _, case in cases.iterrows():
        distances = haversine_km(float(case["case_lat"]), float(case["case_lon"]), screen_lats, screen_lons)
        selected, method, selected_distance = choose_context_row(case, screen, distances)
        base = {
            "case_label": case["case_label"],
            "case_role": case.get("case_role", ""),
            "well_case": case.get("well_case", ""),
            "verified_public_well_name": case.get("verified_public_well_name", ""),
            "case_api_number": case.get("api_number", ""),
            "case_lat": float(case["case_lat"]),
            "case_lon": float(case["case_lon"]),
            "stability_join_method": method,
            "stability_join_distance_km": round(selected_distance, 4),
            "stability_context_guardrail": "P-T admissibility context only; not hydrate proof, occurrence, saturation, or producibility.",
        }
        base.update(compact_status(selected))
        context_rows.append(base)

        order = np.argsort(distances)[:nearby_count]
        for rank, index in enumerate(order, start=1):
            row = screen.loc[int(index)]
            nearby_rows.append(
                {
                    "case_label": case["case_label"],
                    "nearby_rank": rank,
                    "distance_km": round(float(distances[int(index)]), 4),
                    **compact_status(row),
                }
            )

    return pd.DataFrame(context_rows), pd.DataFrame(nearby_rows)


def write_plotly_map(context: pd.DataFrame, nearby: pd.DataFrame, output_html: Path) -> dict[str, Any]:
    try:
        import plotly.graph_objects as go
    except ImportError:
        return {"html": "", "png": "", "status": "plotly_not_installed"}

    fig = go.Figure()
    if not nearby.empty:
        fig.add_trace(
            go.Scattergeo(
                lon=nearby["screen_lon"],
                lat=nearby["screen_lat"],
                text=nearby["case_label"] + "<br>" + nearby["screen_stability_result_status"].astype(str),
                mode="markers",
                marker=dict(size=6, color="#94a3b8", opacity=0.45),
                name="nearby stability-screen points",
            )
        )
    if not context.empty:
        fig.add_trace(
            go.Scattergeo(
                lon=context["screen_lon"],
                lat=context["screen_lat"],
                text=context["case_label"] + "<br>" + context["screen_stability_result_status"].astype(str),
                mode="markers",
                marker=dict(size=13, color="#2563eb", line=dict(color="white", width=1.5)),
                name="selected stability context row",
            )
        )
        fig.add_trace(
            go.Scattergeo(
                lon=context["case_lon"],
                lat=context["case_lat"],
                text=context["case_label"],
                mode="markers+text",
                textposition="top center",
                marker=dict(size=16, color="#dc2626", symbol="star", line=dict(color="white", width=1.5)),
                name="case wells",
            )
        )
        for _, row in context.iterrows():
            fig.add_trace(
                go.Scattergeo(
                    lon=[row["case_lon"], row["screen_lon"]],
                    lat=[row["case_lat"], row["screen_lat"]],
                    mode="lines",
                    line=dict(color="#64748b", width=1),
                    showlegend=False,
                    hoverinfo="skip",
                )
            )

    fig.update_layout(
        title=(
            "DOE local case-well stability context join<br>"
            "<sup>Stability is P-T admissibility context only, not hydrate proof or target truth.</sup>"
        ),
        geo=dict(
            projection_type="mercator",
            lonaxis=dict(range=[-151.0, -148.8]),
            lataxis=dict(range=[70.1, 70.55]),
            showland=True,
            landcolor="#f8fafc",
            showocean=True,
            oceancolor="#dbeafe",
            showcountries=False,
            showcoastlines=True,
            coastlinecolor="#64748b",
        ),
        legend=dict(orientation="h", y=0.02),
        margin=dict(l=20, r=20, t=80, b=20),
        width=1200,
        height=760,
    )
    output_html.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_html), include_plotlyjs="cdn", full_html=True)
    output_png = output_html.with_suffix(".png")
    png_status = "not_written"
    try:
        fig.write_image(str(output_png), scale=2)
        png_status = "written"
    except Exception as exc:  # kaleido may be unavailable in DOE.
        png_status = f"not_written:{type(exc).__name__}"
    return {"html": str(output_html), "png": str(output_png) if output_png.exists() else "", "status": png_status}


def read_optional_temperature_gradient(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {"status": "not_supplied", "path": "", "rows": 0, "columns": []}
    if not path.exists():
        return {"status": "missing", "path": str(path), "rows": 0, "columns": []}
    frame = pd.read_csv(path, nrows=50)
    return {
        "status": "located_sampled_first_50_rows",
        "path": str(path),
        "rows_sampled": int(len(frame)),
        "columns": [str(column) for column in frame.columns],
        "guardrail": "Local temperature-gradient source sampled for schema only in this manifest.",
    }


def run(
    repo_root: Path,
    *,
    case_wells_csv: Path,
    stability_screen_csv: Path,
    output_dir: Path,
    temperature_gradient_csv: Path | None = None,
    case_roles: tuple[str, ...] = DEFAULT_CASE_ROLES,
    nearby_count: int = 5,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    case_wells = pd.read_csv(case_wells_csv)
    stability_screen = load_stability_screen(stability_screen_csv)
    context, nearby = spatial_join_case_wells(
        case_wells,
        stability_screen,
        case_roles=case_roles,
        nearby_count=nearby_count,
    )
    context_path = output_dir / "case_well_stability_context.csv"
    nearby_path = output_dir / "nearby_stability_screen_points.csv"
    context.to_csv(context_path, index=False)
    nearby.to_csv(nearby_path, index=False)
    map_status = write_plotly_map(context, nearby, output_dir / "case_well_stability_context_map.html")
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "case_wells_csv": str(case_wells_csv),
        "stability_screen_csv": str(stability_screen_csv),
        "case_roles": list(case_roles),
        "case_well_count": int(len(context)),
        "nearby_count_per_case": nearby_count,
        "temperature_gradient_csv": read_optional_temperature_gradient(temperature_gradient_csv),
        "outputs": {
            "case_well_stability_context": str(context_path),
            "nearby_stability_screen_points": str(nearby_path),
            "map": map_status,
        },
        "guardrails": [
            "Stability is P-T admissibility context only.",
            "Stability is not an occurrence label, saturation label, hydrate proof, or producibility result.",
            "Nearby stability points may be used for post-model overlay or ablation-tested context features only.",
            "Keep outputs_runtime local/ignored until public-safe review.",
        ],
    }
    manifest_path = output_dir / "spatial_stability_join_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return manifest


def parse_args() -> argparse.Namespace:
    repo_root = find_repo_root(Path.cwd().resolve())
    parser = argparse.ArgumentParser(
        description="Join DOE/local case wells to public stability-screen context points and write local maps."
    )
    parser.add_argument("--repo-root", type=Path, default=repo_root)
    parser.add_argument(
        "--case-wells-csv",
        type=Path,
        default=repo_root / "data/public_ml_products/four_well_case_location_index_2026-06-19.csv",
    )
    parser.add_argument(
        "--stability-screen-csv",
        type=Path,
        default=repo_root / "data/public_stability_products/stability_screen_2026-06-14_methane_5ppt_v1.csv",
    )
    parser.add_argument("--temperature-gradient-csv", type=Path)
    parser.add_argument("--output-dir", type=Path, default=default_output_dir(repo_root))
    parser.add_argument("--case-roles", nargs="+", default=list(DEFAULT_CASE_ROLES))
    parser.add_argument("--nearby-count", type=int, default=5)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    result = run(
        repo_root,
        case_wells_csv=args.case_wells_csv,
        stability_screen_csv=args.stability_screen_csv,
        output_dir=args.output_dir,
        temperature_gradient_csv=args.temperature_gradient_csv,
        case_roles=tuple(args.case_roles),
        nearby_count=args.nearby_count,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    print()
    print("Spatial stability join complete. Keep outputs_runtime local/ignored unless reviewed.")


if __name__ == "__main__":
    main()

