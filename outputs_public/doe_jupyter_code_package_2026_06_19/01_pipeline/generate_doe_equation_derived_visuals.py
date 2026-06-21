"""Create slide-ready equation-derived visuals from DOE/private well data.

This script is GitHub-safe because it stores only code. It does not bundle or
require private DOE data. Run it on the DOE desktop, then email/share the output
PNGs back to the presentation machine.

The visuals deliberately avoid well-log depth tracks. They summarize equation
outputs and source coverage so the slide answers:

    Are we using equations, or log-line movement?

Answer:
    The logs move in depth, but the equations convert those measurements into
    physical quantities. The project can use both: raw/normalized measurements
    and equation-derived quantities. This script visualizes the equation-derived
    side without exposing raw depth-track curves.

Example:
    python 01_pipeline/generate_doe_equation_derived_visuals.py \
      --input "D:/DOE/private_logs/features.csv" \
      --out-dir "D:/DOE/equation_slide_outputs"

Optional constants can be adjusted on the command line:
    --rho-ma 2.65 --rho-f 1.03 --archie-rw 0.5 --archie-a 1 --archie-m 2 --archie-n 2
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PHASE_CURVE = (
    REPO_ROOT
    / "data"
    / "public_stability_products"
    / "phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1.csv"
)


ALIASES: dict[str, list[str]] = {
    "depth_m": ["depth_m", "depth", "dept", "depm", "md_m", "tvd_m", "true_depth_m"],
    "depth_ft": ["depth_ft", "dept_ft", "md_ft", "tvd_ft", "true_depth_ft"],
    "well": ["well", "well_name", "well_alias", "well_id", "runtime_well_id", "api_number"],
    "rhob": ["rhob", "rho_b", "density_gpcc", "density_gcc", "bulk_density", "bulk_density_gcc"],
    "rt": ["rt", "res", "deep_resistivity", "resistivity", "resd", "rdeep", "ild", "ao90", "af90"],
    "density_porosity": ["density_porosity", "density_porosity_vv", "phi_d", "dphi", "phi_den", "phi_porosity"],
    "porosity": ["porosity", "phi", "phit", "nphi", "neutron_porosity", "nmrphi", "nmr_porosity"],
    "dtp": ["dtp", "dt", "delta_tp", "dt_us_ft", "sonic", "compressional_slowness"],
    "dts": ["dts", "delta_ts", "dts_us_ft", "shear_sonic", "shear_slowness"],
    "vp": ["vp", "velp", "vp_km_s", "vp_m_s", "compressional_velocity"],
    "vs": ["vs", "vs1", "vs_km_s", "vs_m_s", "shear_velocity"],
    "temperature_c": ["temperature_c", "temp_c", "t_c", "temperature", "t_model", "tz"],
    "pressure_mpa": ["pressure_mpa", "p_mpa", "p_abs_mpa", "pressure"],
}


@dataclass(frozen=True)
class Constants:
    rho_ma: float = 2.65
    rho_f: float = 1.03
    archie_a: float = 1.0
    archie_rw: float = 0.5
    archie_m: float = 2.0
    archie_n: float = 2.0
    hydrostatic_gradient_mpa_m: float = 0.00980665


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    name = "arialbd.ttf" if bold else "arial.ttf"
    candidates = [
        Path("C:/Windows/Fonts") / name,
        Path("C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/calibri.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


F_TITLE = font(27, True)
F_HEAD = font(18, True)
F_BODY = font(14)
F_SMALL = font(11)
F_TINY = font(9)


def canonical_name(value: str) -> str:
    return (
        str(value)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace("(", "")
        .replace(")", "")
        .replace(".", "")
    )


def find_column(columns: Iterable[str], role: str) -> str | None:
    canon_to_original = {canonical_name(column): column for column in columns}
    for alias in ALIASES[role]:
        key = canonical_name(alias)
        if key in canon_to_original:
            return canon_to_original[key]
    return None


def read_table(path: Path, sheet: str | None = None) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xlsm"}:
        return pd.read_excel(path, sheet_name=sheet or 0)
    if suffix == ".parquet":
        return pd.read_parquet(path)
    raise ValueError(f"Unsupported input extension: {path.suffix}")


def numeric_series(df: pd.DataFrame, role: str) -> tuple[pd.Series | None, str | None]:
    column = find_column(df.columns, role)
    if column is None:
        return None, None
    return pd.to_numeric(df[column], errors="coerce"), column


def as_fraction(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    median = values.dropna().median() if values.notna().any() else np.nan
    if pd.notna(median) and median > 1.5:
        return values / 100.0
    return values


def density_to_gcc(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    median = values.dropna().median() if values.notna().any() else np.nan
    if pd.notna(median) and median > 20:
        return values / 1000.0
    return values


def velocity_to_km_s(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    median = values.dropna().median() if values.notna().any() else np.nan
    if pd.isna(median):
        return values
    if median > 200:
        return values / 1000.0
    return values


def slowness_us_ft_to_km_s(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    return 304.8 / values.replace(0, np.nan)


def load_phase_curve(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        return None
    phase = pd.read_csv(path)
    required = {"pressure_mpa_absolute", "equilibrium_temperature_c"}
    if not required.issubset(phase.columns):
        return None
    return phase.sort_values("pressure_mpa_absolute")


def interpolate_teq(pressure_mpa: pd.Series, phase_curve: pd.DataFrame | None) -> pd.Series:
    if phase_curve is None:
        return pd.Series(np.nan, index=pressure_mpa.index)
    valid = pressure_mpa.dropna()
    if valid.empty:
        return pd.Series(np.nan, index=pressure_mpa.index)
    pressures = phase_curve["pressure_mpa_absolute"].to_numpy(dtype=float)
    temps = phase_curve["equilibrium_temperature_c"].to_numpy(dtype=float)
    values = np.interp(pressure_mpa.to_numpy(dtype=float), pressures, temps, left=np.nan, right=np.nan)
    return pd.Series(values, index=pressure_mpa.index)


def derive_equation_features(df: pd.DataFrame, constants: Constants, phase_curve: pd.DataFrame | None) -> tuple[pd.DataFrame, dict[str, str]]:
    out = pd.DataFrame(index=df.index)
    source_columns: dict[str, str] = {}

    well_col = find_column(df.columns, "well")
    out["well_id"] = df[well_col].astype(str) if well_col else "unknown_well"
    if well_col:
        source_columns["well_id"] = well_col

    depth_m, depth_col = numeric_series(df, "depth_m")
    if depth_m is None:
        depth_ft, depth_ft_col = numeric_series(df, "depth_ft")
        if depth_ft is not None:
            depth_m = depth_ft * 0.3048
            source_columns["depth_m"] = depth_ft_col or "depth_ft"
    else:
        source_columns["depth_m"] = depth_col or "depth_m"
    if depth_m is not None:
        out["depth_m"] = depth_m

    rhob, rhob_col = numeric_series(df, "rhob")
    if rhob is not None:
        out["rho_b_gcc"] = density_to_gcc(rhob)
        source_columns["rho_b_gcc"] = rhob_col or "rhob"

    rt, rt_col = numeric_series(df, "rt")
    if rt is not None:
        out["rt_ohm_m"] = rt.where(rt > 0)
        source_columns["rt_ohm_m"] = rt_col or "rt"

    supplied_phi, supplied_phi_col = numeric_series(df, "density_porosity")
    if supplied_phi is not None:
        out["phi_input"] = as_fraction(supplied_phi)
        source_columns["phi_input"] = supplied_phi_col or "density_porosity"
    elif "rho_b_gcc" in out:
        out["phi_input"] = ((constants.rho_ma - out["rho_b_gcc"]) / (constants.rho_ma - constants.rho_f)).clip(-0.05, 0.7)
        source_columns["phi_input"] = "computed_from_rho_b"
    else:
        porosity, porosity_col = numeric_series(df, "porosity")
        if porosity is not None:
            out["phi_input"] = as_fraction(porosity)
            source_columns["phi_input"] = porosity_col or "porosity"

    if {"phi_input", "rt_ohm_m"}.issubset(out.columns):
        phi = out["phi_input"].clip(0.01, 0.8)
        sw = ((constants.archie_a * constants.archie_rw) / ((phi**constants.archie_m) * out["rt_ohm_m"])) ** (1 / constants.archie_n)
        out["sw_archie"] = sw.clip(0, 1.5)
        out["sh_archie"] = (1 - out["sw_archie"]).clip(0, 1)

    vp, vp_col = numeric_series(df, "vp")
    if vp is not None:
        out["vp_km_s"] = velocity_to_km_s(vp)
        source_columns["vp_km_s"] = vp_col or "vp"
    else:
        dtp, dtp_col = numeric_series(df, "dtp")
        if dtp is not None:
            out["vp_km_s"] = slowness_us_ft_to_km_s(dtp)
            source_columns["vp_km_s"] = dtp_col or "dtp"

    vs, vs_col = numeric_series(df, "vs")
    if vs is not None:
        out["vs_km_s"] = velocity_to_km_s(vs)
        source_columns["vs_km_s"] = vs_col or "vs"
    else:
        dts, dts_col = numeric_series(df, "dts")
        if dts is not None:
            out["vs_km_s"] = slowness_us_ft_to_km_s(dts)
            source_columns["vs_km_s"] = dts_col or "dts"

    if {"vp_km_s", "vs_km_s"}.issubset(out.columns):
        out["vp_vs_ratio"] = out["vp_km_s"] / out["vs_km_s"].replace(0, np.nan)
    if {"rho_b_gcc", "vp_km_s"}.issubset(out.columns):
        out["ai_rhob_vp"] = out["rho_b_gcc"] * out["vp_km_s"]
    if {"rho_b_gcc", "vs_km_s"}.issubset(out.columns):
        out["si_rhob_vs"] = out["rho_b_gcc"] * out["vs_km_s"]
        out["mu_rho"] = (out["rho_b_gcc"] ** 2) * (out["vs_km_s"] ** 2)
    if {"rho_b_gcc", "vp_km_s", "vs_km_s"}.issubset(out.columns):
        out["lambda_rho"] = (out["rho_b_gcc"] ** 2) * ((out["vp_km_s"] ** 2) - 2 * (out["vs_km_s"] ** 2))

    pressure, pressure_col = numeric_series(df, "pressure_mpa")
    if pressure is not None:
        out["pressure_mpa"] = pressure
        source_columns["pressure_mpa"] = pressure_col or "pressure_mpa"
    elif "depth_m" in out:
        out["pressure_mpa"] = constants.hydrostatic_gradient_mpa_m * out["depth_m"]
        source_columns["pressure_mpa"] = "computed_from_depth_m"

    temp, temp_col = numeric_series(df, "temperature_c")
    if temp is not None:
        out["temperature_c"] = temp
        source_columns["temperature_c"] = temp_col or "temperature_c"

    if {"pressure_mpa", "temperature_c"}.issubset(out.columns):
        out["teq_c"] = interpolate_teq(out["pressure_mpa"], phase_curve)
        out["stability_margin_c"] = out["teq_c"] - out["temperature_c"]
        out["stable_pt_flag"] = out["stability_margin_c"] >= 0

    return out, source_columns


def safe_quantile(series: pd.Series, q: float) -> float | None:
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return None
    return float(values.quantile(q))


def build_symbol_readiness(derived: pd.DataFrame, source_columns: dict[str, str], constants: Constants) -> pd.DataFrame:
    specs = [
        ("rho_b", "density log", "rho_b_gcc", "well log input"),
        ("Rt", "deep resistivity", "rt_ohm_m", "well log input"),
        ("φD / φ", "porosity input/output", "phi_input", "derived or supplied"),
        ("Sw", "water saturation", "sw_archie", "derived output"),
        ("Sh", "hydrate saturation proxy", "sh_archie", "derived output"),
        ("Vp", "P-wave velocity", "vp_km_s", "well log or derived"),
        ("Vs", "S-wave velocity", "vs_km_s", "well log or derived"),
        ("AI", "acoustic impedance", "ai_rhob_vp", "derived output"),
        ("mu-rho", "shear stiffness", "mu_rho", "derived output"),
        ("lambda-rho", "compressional stiffness", "lambda_rho", "derived output"),
        ("T(z)", "temperature", "temperature_c", "temperature input/model"),
        ("P(z)", "pressure", "pressure_mpa", "pressure/depth input"),
        ("Teq", "phase boundary", "teq_c", "public phase curve"),
        ("stable?", "P-T admissibility", "stable_pt_flag", "derived context"),
    ]
    rows = []
    total = len(derived)
    for symbol, meaning, column, source_type in specs:
        present = column in derived
        usable = int(derived[column].notna().sum()) if present else 0
        rows.append(
            {
                "symbol": symbol,
                "meaning": meaning,
                "column": column,
                "source_type": source_type,
                "source_column_or_assumption": source_columns.get(column, "computed/constant" if present else "missing"),
                "usable_rows": usable,
                "usable_pct": round((usable / total * 100), 1) if total else 0,
                "status": "usable" if usable > 0 else "missing",
            }
        )
    for symbol, meaning, value in [
        ("rho_ma", "matrix density assumption", constants.rho_ma),
        ("rho_f", "fluid density assumption", constants.rho_f),
        ("Rw", "water resistivity assumption", constants.archie_rw),
        ("a,m,n", "Archie constants", f"{constants.archie_a}, {constants.archie_m}, {constants.archie_n}"),
    ]:
        rows.append(
            {
                "symbol": symbol,
                "meaning": meaning,
                "column": "constant",
                "source_type": "core/lab/literature assumption",
                "source_column_or_assumption": value,
                "usable_rows": total,
                "usable_pct": 100.0 if total else 0,
                "status": "assumption",
            }
        )
    return pd.DataFrame(rows)


def draw_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, fill: str, fnt: ImageFont.ImageFont) -> None:
    draw.text(xy, value, fill=fill, font=fnt)


def scale(value: float, src_min: float, src_max: float, dst_min: float, dst_max: float) -> float:
    if not np.isfinite(value) or src_min == src_max:
        return (dst_min + dst_max) / 2
    return dst_min + (value - src_min) * (dst_max - dst_min) / (src_max - src_min)


def values_for_plot(df: pd.DataFrame, column: str) -> pd.Series:
    if column not in df:
        return pd.Series(dtype=float)
    return pd.to_numeric(df[column], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()


def draw_histogram(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], values: pd.Series, title: str, color: str) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=12, fill="#ffffff", outline="#c7dde4", width=2)
    draw_text(draw, (x0 + 14, y0 + 12), title, "#0d2430", F_HEAD)
    values = pd.to_numeric(values, errors="coerce").dropna()
    plot = (x0 + 30, y0 + 56, x1 - 22, y1 - 36)
    px0, py0, px1, py1 = plot
    draw.rectangle(plot, fill="#fbfdfe", outline="#edf3f5")
    if values.empty:
        draw_text(draw, (x0 + 28, y0 + 86), "not available from input columns", "#d23b40", F_BODY)
        return
    clipped = values.clip(values.quantile(0.01), values.quantile(0.99))
    counts, edges = np.histogram(clipped, bins=min(22, max(6, int(math.sqrt(len(clipped))))))
    max_count = max(int(counts.max()), 1)
    for i, count in enumerate(counts):
        bx0 = scale(i, 0, len(counts), px0, px1)
        bx1 = scale(i + 0.85, 0, len(counts), px0, px1)
        by0 = scale(count, 0, max_count, py1, py0)
        draw.rectangle((bx0, by0, bx1, py1), fill=color)
    median = float(values.median())
    q10 = float(values.quantile(0.10))
    q90 = float(values.quantile(0.90))
    draw_text(draw, (x0 + 14, y1 - 24), f"n={len(values):,}   P10={q10:.2g}   median={median:.2g}   P90={q90:.2g}", "#496473", F_SMALL)


def draw_histogram_grid(derived: pd.DataFrame, out_path: Path) -> None:
    img = Image.new("RGB", (1400, 860), "#f8fbfc")
    draw = ImageDraw.Draw(img)
    draw_text(draw, (44, 30), "Equation-derived quantities from DOE data", "#0d2430", F_TITLE)
    draw_text(draw, (46, 64), "No well-log tracks shown: these are distributions after applying the equations.", "#496473", F_BODY)
    panels = [
        ("phi_input", "φD / φ porosity input", "#256fd8"),
        ("sh_archie", "Sh from Archie check", "#d23b40"),
        ("mu_rho", "μρ shear stiffness", "#15946a"),
        ("lambda_rho", "λρ compressional stiffness", "#6a5bd2"),
    ]
    boxes = [(44, 112, 680, 390), (720, 112, 1356, 390), (44, 430, 680, 708), (720, 430, 1356, 708)]
    for (column, title, color), box in zip(panels, boxes):
        draw_histogram(draw, box, values_for_plot(derived, column), title, color)
    draw_text(draw, (46, 804), "Use on slide: show that equations produce physical variables, not just visual line movement.", "#0e5261", F_BODY)
    img.save(out_path)


def draw_scatter(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], x: pd.Series, y: pd.Series, title: str, xlabel: str, ylabel: str, color: str) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=12, fill="#ffffff", outline="#c7dde4", width=2)
    draw_text(draw, (x0 + 14, y0 + 12), title, "#0d2430", F_HEAD)
    data = pd.concat([x.rename("x"), y.rename("y")], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
    plot = (x0 + 54, y0 + 58, x1 - 28, y1 - 48)
    px0, py0, px1, py1 = plot
    draw.rectangle(plot, fill="#fbfdfe", outline="#edf3f5")
    draw_text(draw, (px0, y1 - 34), xlabel, "#496473", F_TINY)
    draw_text(draw, (x0 + 10, py0 - 16), ylabel, "#496473", F_TINY)
    if data.empty:
        draw_text(draw, (x0 + 28, y0 + 86), "not available from input columns", "#d23b40", F_BODY)
        return
    sample = data.sample(min(len(data), 1800), random_state=17)
    xmin, xmax = sample["x"].quantile([0.01, 0.99])
    ymin, ymax = sample["y"].quantile([0.01, 0.99])
    for _, row in sample.iterrows():
        sx = scale(row["x"], xmin, xmax, px0, px1)
        sy = scale(row["y"], ymin, ymax, py1, py0)
        draw.ellipse((sx - 2, sy - 2, sx + 2, sy + 2), fill=color)
    draw_text(draw, (x0 + 14, y1 - 24), f"n={len(data):,}; sampled points={len(sample):,}", "#496473", F_SMALL)


def draw_crossplot_grid(derived: pd.DataFrame, out_path: Path) -> None:
    img = Image.new("RGB", (1400, 860), "#f8fbfc")
    draw = ImageDraw.Draw(img)
    draw_text(draw, (44, 30), "Equation outputs compared without depth tracks", "#0d2430", F_TITLE)
    draw_text(draw, (46, 64), "These visuals show relationships between derived quantities, not raw well-log line shapes.", "#496473", F_BODY)
    boxes = [(44, 112, 680, 390), (720, 112, 1356, 390), (44, 430, 680, 708), (720, 430, 1356, 708)]
    plot_specs = [
        ("phi_input", "sh_archie", "Porosity vs Archie Sh", "φD / φ", "Sh", "#d23b40"),
        ("vp_km_s", "mu_rho", "Velocity vs shear stiffness", "Vp", "μρ", "#15946a"),
        ("lambda_rho", "mu_rho", "Elastic crossplot", "λρ", "μρ", "#6a5bd2"),
        ("temperature_c", "teq_c", "Temperature vs stability boundary", "T(z)", "Teq", "#d99012"),
    ]
    for box, (xcol, ycol, title, xlabel, ylabel, color) in zip(boxes, plot_specs):
        draw_scatter(draw, box, values_for_plot(derived, xcol), values_for_plot(derived, ycol), title, xlabel, ylabel, color)
    draw_text(draw, (46, 804), "Use on slide: show the project uses data relationships after physics transforms, not hand-reading one curve.", "#0e5261", F_BODY)
    img.save(out_path)


def draw_readiness_matrix(readiness: pd.DataFrame, out_path: Path) -> None:
    img = Image.new("RGB", (1400, 860), "#f8fbfc")
    draw = ImageDraw.Draw(img)
    draw_text(draw, (44, 30), "Equation symbol readiness from DOE input table", "#0d2430", F_TITLE)
    draw_text(draw, (46, 64), "Shows which symbols are measured logs, assumptions/core constants, or derived equation outputs.", "#496473", F_BODY)
    groups = [
        ("well log / measured", readiness[readiness["source_type"].str.contains("well log|temperature|pressure", case=False, regex=True)]),
        ("core/lab/literature assumptions", readiness[readiness["source_type"].str.contains("assumption|phase", case=False, regex=True)]),
        ("equation-derived outputs", readiness[readiness["source_type"].str.contains("derived", case=False, regex=True)]),
    ]
    x_positions = [44, 493, 942]
    colors = ["#256fd8", "#d99012", "#15946a"]
    for (title, group), x0, color in zip(groups, x_positions, colors):
        draw.rounded_rectangle((x0, 112, x0 + 414, 720), radius=12, fill="#ffffff", outline=color, width=2)
        draw_text(draw, (x0 + 18, 130), title, color, F_HEAD)
        y = 170
        for _, row in group.head(12).iterrows():
            pct = float(row["usable_pct"])
            status_color = "#15946a" if row["status"] in {"usable", "assumption"} and pct > 0 else "#d23b40"
            draw_text(draw, (x0 + 18, y), str(row["symbol"]), "#0d2430", F_BODY)
            draw_text(draw, (x0 + 86, y), str(row["meaning"])[:30], "#496473", F_SMALL)
            bar_x = x0 + 260
            draw.rectangle((bar_x, y + 4, bar_x + 118, y + 14), outline="#d9e9ee", fill="#edf7f8")
            draw.rectangle((bar_x, y + 4, bar_x + int(118 * min(pct, 100) / 100), y + 14), fill=status_color)
            draw_text(draw, (bar_x + 124, y - 1), f"{pct:.0f}%", "#496473", F_TINY)
            y += 39
    draw_text(draw, (46, 804), "Use on slide: color/highlight equation symbols by source type instead of writing every definition in tiny font.", "#0e5261", F_BODY)
    img.save(out_path)


def write_summary(derived: pd.DataFrame, readiness: pd.DataFrame, out_dir: Path, source_columns: dict[str, str]) -> None:
    metrics = {}
    for column in [
        "phi_input",
        "sh_archie",
        "vp_km_s",
        "vs_km_s",
        "mu_rho",
        "lambda_rho",
        "stability_margin_c",
    ]:
        if column not in derived:
            continue
        metrics[column] = {
            "usable_rows": int(derived[column].notna().sum()),
            "p10": safe_quantile(derived[column], 0.10),
            "median": safe_quantile(derived[column], 0.50),
            "p90": safe_quantile(derived[column], 0.90),
        }
    summary = {
        "row_count": int(len(derived)),
        "well_count": int(derived["well_id"].nunique()) if "well_id" in derived else 0,
        "source_columns": source_columns,
        "metrics": metrics,
        "slide_guidance": [
            "Do not use well-log depth tracks on the equation slide.",
            "Use equation_derived_distributions.png to show what equations produce.",
            "Use equation_output_crossplots.png to show relationships among equation outputs.",
            "Use equation_symbol_readiness.png to color-code symbols by data source.",
        ],
    }
    (out_dir / "equation_visual_manifest.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    readiness.to_csv(out_dir / "equation_symbol_readiness.csv", index=False)


def run(input_path: Path, out_dir: Path, constants: Constants, sheet: str | None = None, phase_curve_path: Path = DEFAULT_PHASE_CURVE) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    raw = read_table(input_path, sheet=sheet)
    phase_curve = load_phase_curve(phase_curve_path)
    derived, source_columns = derive_equation_features(raw, constants, phase_curve)
    readiness = build_symbol_readiness(derived, source_columns, constants)

    outputs = {
        "distributions": out_dir / "equation_derived_distributions.png",
        "crossplots": out_dir / "equation_output_crossplots.png",
        "readiness": out_dir / "equation_symbol_readiness.png",
        "manifest": out_dir / "equation_visual_manifest.json",
        "readiness_csv": out_dir / "equation_symbol_readiness.csv",
    }
    draw_histogram_grid(derived, outputs["distributions"])
    draw_crossplot_grid(derived, outputs["crossplots"])
    draw_readiness_matrix(readiness, outputs["readiness"])
    write_summary(derived, readiness, out_dir, source_columns)
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Private DOE CSV/XLSX/parquet table with log/core/equation inputs.")
    parser.add_argument("--sheet", default=None, help="Excel sheet name or index; default is first sheet.")
    parser.add_argument("--out-dir", required=True, type=Path, help="Output folder for slide-ready PNGs and manifests.")
    parser.add_argument("--phase-curve", default=DEFAULT_PHASE_CURVE, type=Path, help="Phase boundary CSV for Teq(P), defaults to repo public methane 5 ppt curve.")
    parser.add_argument("--rho-ma", default=2.65, type=float, help="Matrix density assumption in g/cc.")
    parser.add_argument("--rho-f", default=1.03, type=float, help="Fluid density assumption in g/cc.")
    parser.add_argument("--archie-a", default=1.0, type=float, help="Archie tortuosity constant.")
    parser.add_argument("--archie-rw", default=0.5, type=float, help="Formation water resistivity assumption in ohm m.")
    parser.add_argument("--archie-m", default=2.0, type=float, help="Archie cementation exponent.")
    parser.add_argument("--archie-n", default=2.0, type=float, help="Archie saturation exponent.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    constants = Constants(
        rho_ma=args.rho_ma,
        rho_f=args.rho_f,
        archie_a=args.archie_a,
        archie_rw=args.archie_rw,
        archie_m=args.archie_m,
        archie_n=args.archie_n,
    )
    outputs = run(args.input, args.out_dir, constants, sheet=args.sheet, phase_curve_path=args.phase_curve)
    for label, path in outputs.items():
        print(f"{label}: {path}")


if __name__ == "__main__":
    main()
