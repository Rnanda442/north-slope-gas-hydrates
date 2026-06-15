from __future__ import annotations

import argparse
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dashboard.stability_products import (
    g10015_temperature_profile_points_summary_frame,
    load_g10015_temperature_inventory,
    load_g10015_temperature_profile_points_product,
    load_public_ml_feature_scaffold,
    load_public_well_stability_context,
    load_stability_input_scaffold,
    load_stability_screen,
    load_stability_temperature_model,
    public_ml_feature_scaffold_summary_frame,
    stability_context_summary_frame,
    stability_screen_summary_frame,
    stability_input_scaffold_summary_frame,
    stability_temperature_model_summary_frame,
    temperature_inventory_summary_frame,
    write_g10015_temperature_profile_points_product,
    write_public_stability_products,
    write_public_ml_feature_products,
    write_stability_screen_product,
    write_stability_temperature_model_product,
)
from dashboard.stability_sources import (
    active_stability_source_path,
    default_stability_bundle_path,
    default_stability_snapshot_path,
    stability_bundle_metrics,
)


def project_root_from_script() -> Path:
    return PROJECT_ROOT


def print_frame(title: str, frame) -> None:
    print(f"\n## {title}")
    if frame.empty:
        print("(empty)")
        return
    print(frame.to_string(index=False))


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build public-safe North Slope stability products from the full "
            "OpenScienceLab source bundle when present, or from the committed "
            "public snapshot fallback."
        )
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        default=None,
        help=(
            "Optional source bundle path. Defaults to "
            "data/source_library/north_slope_stability_sources_2026-06-13 if "
            "present, otherwise the committed public snapshot."
        ),
    )
    args = parser.parse_args()

    project_root = project_root_from_script()
    source_root = args.source_root or active_stability_source_path(project_root)

    print(f"Project root: {project_root}")
    print(f"Active source root: {source_root}")
    print(f"Default full bundle: {default_stability_bundle_path(project_root)}")
    print(f"Default public snapshot: {default_stability_snapshot_path(project_root)}")
    print(f"Source metrics: {stability_bundle_metrics(source_root)}")

    outputs = write_public_stability_products(project_root, source_root)
    profile_points_outputs = write_g10015_temperature_profile_points_product(project_root, source_root)
    temperature_model_outputs = write_stability_temperature_model_product(project_root, source_root)
    stability_screen_outputs = write_stability_screen_product(project_root, source_root)
    ml_feature_outputs = write_public_ml_feature_products(project_root)
    print("\n## Written outputs")
    for output in (
        outputs
        + profile_points_outputs
        + temperature_model_outputs
        + stability_screen_outputs
        + ml_feature_outputs
    ):
        if output is not None:
            print(output)

    well_context = load_public_well_stability_context(project_root)
    temperature_inventory = load_g10015_temperature_inventory(project_root)
    profile_points = load_g10015_temperature_profile_points_product(project_root)
    scaffold = load_stability_input_scaffold(project_root)
    temperature_model = load_stability_temperature_model(project_root)
    stability_screen = load_stability_screen(project_root)
    ml_feature_scaffold = load_public_ml_feature_scaffold(project_root)

    print_frame("Well Context Summary", stability_context_summary_frame(well_context))
    print_frame("G10015 Temperature Inventory Summary", temperature_inventory_summary_frame(temperature_inventory))
    print_frame(
        "G10015 Sampled Temperature Profile Points Summary",
        g10015_temperature_profile_points_summary_frame(profile_points),
    )
    print_frame("Stability Input Scaffold Summary", stability_input_scaffold_summary_frame(scaffold))
    print_frame("Stability Temperature Model Summary", stability_temperature_model_summary_frame(temperature_model))
    print_frame("Stability Screen Summary", stability_screen_summary_frame(stability_screen))
    print_frame("Public ML Feature Scaffold Summary", public_ml_feature_scaffold_summary_frame(ml_feature_scaffold))

    print(
        "\nDone. Review changed files under data/public_stability_products/ and "
        "commit only derived public outputs, code, docs, and tests."
    )


if __name__ == "__main__":
    main()
