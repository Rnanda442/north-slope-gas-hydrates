from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Iterable, Sequence

import pandas as pd


SOURCE_INTAKE_COLUMNS = [
    "source_id",
    "source_status",
    "match_confidence",
    "canonical_title",
    "short_citation",
    "doi_or_link",
    "source_kind",
    "project_role",
    "slide_3_use",
    "stability_use",
    "file_name",
    "extension",
    "bytes",
    "safe_path",
    "detected_title_snippet",
    "known_drive_or_gmail_location",
    "github_push_status",
    "next_action",
    "guardrail",
]

DEFAULT_SOURCE_EXTENSIONS = {
    ".csv",
    ".docx",
    ".gif",
    ".htm",
    ".html",
    ".jpeg",
    ".jpg",
    ".md",
    ".pdf",
    ".png",
    ".txt",
    ".webp",
    ".xlsx",
}

PUBLIC_GUARDRAIL = (
    "Public-safe source inventory only. Do not copy raw PDFs, private Drive/Gmail "
    "exports, approved well-log/core rows, trained models, predictions, or "
    "credentials into GitHub."
)

FOUND_SOURCE_STATUS = "found_local_source_file"
FOUND_REFERENCE_STATUS = "found_local_reference_note"
MISSING_STATUS = "expected_missing_or_drive_only"
UNMATCHED_STATUS = "found_local_unmatched_review"


@dataclass(frozen=True)
class SourceRegistryEntry:
    source_id: str
    canonical_title: str
    short_citation: str
    doi_or_link: str
    source_kind: str
    project_role: str
    slide_3_use: str
    stability_use: str
    known_drive_or_gmail_location: str
    github_push_status: str
    next_action: str
    expected_files: tuple[str, ...]
    match_terms: tuple[str, ...]


SOURCE_REGISTRY: tuple[SourceRegistryEntry, ...] = (
    SourceRegistryEntry(
        source_id="SRC_NEW_001",
        canonical_title=(
            "Automated Well-Log Processing and Lithology Classification by "
            "Identifying Optimal Features Through Unsupervised and Supervised "
            "Machine-Learning Algorithms"
        ),
        short_citation="Singh, Seol, and Myshakin (2020)",
        doi_or_link="10.2118/202477-PA",
        source_kind="well_log_processing_ml",
        project_role=(
            "Feature selection, lithology classification, and preprocessing "
            "logic for hydrate-reservoir log interpretation."
        ),
        slide_3_use=(
            "Supports the clean-reservoir/lithology gate before hydrate-response "
            "signals are interpreted."
        ),
        stability_use="none",
        known_drive_or_gmail_location="missing_from_current_gmail_drive_check",
        github_push_status="manifest_only_until_pdf_license_review",
        next_action="Download PDF if access is available; verify title and DOI before citing.",
        expected_files=("202477", "automated_well_log_processing", "lithology_classification"),
        match_terms=(
            "10.2118/202477-PA",
            "202477",
            "automated well-log processing",
            "lithology classification",
            "identifying optimal features",
        ),
    ),
    SourceRegistryEntry(
        source_id="SRC_NEW_002",
        canonical_title=(
            "India National Gas Hydrate Program Expedition 02 Summary of "
            "Scientific Results: Gas hydrate systems along the eastern "
            "continental margin of India"
        ),
        short_citation="Collett et al. (2019)",
        doi_or_link="10.1016/j.marpetgeo.2019.05.023",
        source_kind="gas_hydrate_field_program",
        project_role=(
            "Comparative logging/coring hydrate system source; useful for how "
            "hydrate intervals are integrated with cores and logs."
        ),
        slide_3_use=(
            "Use as a comparative coring/logging context source, not as direct "
            "Alaska evidence."
        ),
        stability_use="none",
        known_drive_or_gmail_location=(
            "Drive root file collet2019.pdf; "
            "https://drive.google.com/file/d/1kMr-KBqpB4RS-9soUT60PwD918ZvcUtF/view"
        ),
        github_push_status="manifest_only_large_pdf_drive_only",
        next_action="Keep raw PDF in Drive; extract source notes and any allowed figure references.",
        expected_files=("collet2019.pdf", "collett2019.pdf", "nghp02", "nghp-02"),
        match_terms=(
            "10.1016/j.marpetgeo.2019.05.023",
            "collet2019",
            "collett",
            "india national gas hydrate program",
            "nghp-02",
        ),
    ),
    SourceRegistryEntry(
        source_id="SRC_NEW_003",
        canonical_title=(
            "Predicting shear wave velocity from conventional well logs with "
            "deep and hybrid machine learning algorithms"
        ),
        short_citation="Rajabi et al. (2023)",
        doi_or_link="10.1007/s13202-022-01531-z",
        source_kind="missing_shear_velocity_ml",
        project_role=(
            "Supports missing Vs handling and derived elastic/geomechanical "
            "feature caveats."
        ),
        slide_3_use=(
            "Use for the derived Vs / mu-rho caveat when shear logs are absent "
            "and must be estimated."
        ),
        stability_use="none",
        known_drive_or_gmail_location="missing_from_current_gmail_drive_check",
        github_push_status="manifest_only_until_pdf_license_review",
        next_action="Download PDF if available; verify whether it is open for reuse.",
        expected_files=("rajabi", "s13202-022-01531-z", "shear_wave_velocity"),
        match_terms=(
            "10.1007/s13202-022-01531-z",
            "predicting shear wave velocity",
            "conventional well logs",
            "deep and hybrid machine learning",
            "rajabi",
        ),
    ),
    SourceRegistryEntry(
        source_id="SRC_NEW_004",
        canonical_title=(
            "A comprehensive review on the geomechanical properties of gas "
            "hydrate bearing sediments"
        ),
        short_citation="Lijith, Malagar, and Singh (2019)",
        doi_or_link="10.1016/j.marpetgeo.2019.03.024",
        source_kind="hydrate_geomechanics_review",
        project_role=(
            "Geomechanical property context for stiffness, strength, and hydrate "
            "bearing sediment behavior."
        ),
        slide_3_use=(
            "Use to explain why hydrate-bearing intervals can shift acoustic "
            "and elastic responses, while still needing log/core confirmation."
        ),
        stability_use="none",
        known_drive_or_gmail_location="Gmail draft/thread new paps attachment sign2019.pdf",
        github_push_status="manifest_only_gmail_attachment_verify_first",
        next_action="Open sign2019.pdf locally and verify title/DOI before using.",
        expected_files=("sign2019.pdf", "lijith", "malagar", "geomechanical"),
        match_terms=(
            "10.1016/j.marpetgeo.2019.03.024",
            "comprehensive review",
            "geomechanical properties",
            "gas hydrate bearing sediments",
            "lijith",
            "malagar",
        ),
    ),
    SourceRegistryEntry(
        source_id="SRC_NEW_005",
        canonical_title="A new rock physics model to estimate shear velocity log",
        short_citation="Dalvand and Falahat (2021)",
        doi_or_link="10.1016/j.petrol.2020.107697",
        source_kind="rock_physics_shear_velocity",
        project_role=(
            "Rock-physics support for estimated shear velocity provenance and "
            "limitations."
        ),
        slide_3_use=(
            "Use for the visual note that Vs-derived signals are model-derived "
            "unless measured shear is available."
        ),
        stability_use="none",
        known_drive_or_gmail_location="Gmail draft/thread new paps attachment falahat.pdf",
        github_push_status="manifest_only_gmail_attachment_verify_first",
        next_action="Open falahat.pdf locally and verify title/DOI before using.",
        expected_files=("falahat.pdf", "dalvand", "shear_velocity_log"),
        match_terms=(
            "10.1016/j.petrol.2020.107697",
            "new rock physics model",
            "estimate shear velocity log",
            "dalvand",
            "falahat",
        ),
    ),
    SourceRegistryEntry(
        source_id="SRC_NEW_006",
        canonical_title=(
            "Supplementary materials for machine-learning assessment of methane "
            "hydrate occurrence and saturation offshore India"
        ),
        short_citation="Chong et al. (2024 supplement)",
        doi_or_link="10.1190/int-2023-0056.1",
        source_kind="hydrate_ml_supplement",
        project_role=(
            "Supplemental workflow, preprocessing, or figure details for the "
            "offshore India occurrence/saturation ML article."
        ),
        slide_3_use=(
            "Use only if the supplement contains clear log-response or feature "
            "workflow figures."
        ),
        stability_use="none",
        known_drive_or_gmail_location="missing_supplement",
        github_push_status="manifest_only_until_supplement_license_review",
        next_action="Find supplement and record whether figures are usable.",
        expected_files=("supplement", "supplementary", "int-2023-0056"),
        match_terms=(
            "supplementary",
            "supplemental",
            "10.1190/int-2023-0056.1",
            "offshore india",
            "chong",
            "methane hydrate occurrence and saturation",
        ),
    ),
    SourceRegistryEntry(
        source_id="SRC_EXISTING_001",
        canonical_title=(
            "Application of machine learning to characterize gas hydrate "
            "reservoirs in Mackenzie Delta (Canada) and on the Alaska north "
            "slope (USA)"
        ),
        short_citation="Chong, Singh, Creason, Seol, and Myshakin (2022)",
        doi_or_link="10.1007/s10596-022-10151-9",
        source_kind="direct_ans_hydrate_ml",
        project_role=(
            "Direct Mackenzie Delta / Alaska North Slope hydrate ML comparison "
            "source."
        ),
        slide_3_use=(
            "Key ANS example for connecting log response patterns to ML-ready "
            "features."
        ),
        stability_use="context_only",
        known_drive_or_gmail_location="references/ml-sources/2026-06-11",
        github_push_status="already_local_public_source_review_existing",
        next_action="Use for ANS-specific signal and feature logic after rereading figures/tables.",
        expected_files=("s10596-022-10151-9.pdf",),
        match_terms=(
            "10.1007/s10596-022-10151-9",
            "s10596-022-10151-9",
            "mackenzie delta",
            "alaska north slope",
            "application of machine learning to characterize gas hydrate reservoirs",
        ),
    ),
    SourceRegistryEntry(
        source_id="SRC_EXISTING_002",
        canonical_title=(
            "Prediction of gas hydrate saturation using machine learning and "
            "optimal set of well-logs"
        ),
        short_citation="Singh, Seol, and Myshakin (2021)",
        doi_or_link="10.1007/s10596-020-10004-3",
        source_kind="hydrate_saturation_ml",
        project_role=(
            "Optimal well-log feature family and saturation target source."
        ),
        slide_3_use=(
            "Supports resistivity/acoustic/porosity feature families, but target "
            "saturation remains Y-only."
        ),
        stability_use="none",
        known_drive_or_gmail_location="references/hydrate-ml-physics-sources/2026-06-13",
        github_push_status="already_local_public_source_review_existing",
        next_action="Use for feature-family wording and leakage-safe target separation.",
        expected_files=("singh_seol_myshakin_2021", "optimal_well_logs"),
        match_terms=(
            "10.1007/s10596-020-10004-3",
            "prediction of gas hydrate saturation",
            "optimal set of well-logs",
            "singh",
            "seol",
            "myshakin",
        ),
    ),
    SourceRegistryEntry(
        source_id="SRC_EXISTING_003",
        canonical_title=(
            "Machine-learning application to assess occurrence and saturations "
            "of methane hydrate in marine deposits offshore India"
        ),
        short_citation="Chong, Collett, Creason, Seol, and Myshakin (2024)",
        doi_or_link="10.1190/int-2023-0056.1",
        source_kind="hydrate_occurrence_saturation_ml",
        project_role=(
            "Occurrence classification plus saturation regression architecture "
            "comparison source."
        ),
        slide_3_use=(
            "Use for the two-stage occurrence/saturation logic, not as direct "
            "ANS evidence."
        ),
        stability_use="none",
        known_drive_or_gmail_location="references/hydrate-ml-physics-sources/2026-06-13",
        github_push_status="already_local_public_source_review_existing",
        next_action="Use with clear regional caveat: offshore India comparison source.",
        expected_files=("chong_collett_creason_seol_myshakin_2024",),
        match_terms=(
            "10.1190/int-2023-0056.1",
            "offshore india",
            "machine-learning application",
            "occurrence and saturations",
            "methane hydrate in marine deposits",
        ),
    ),
    SourceRegistryEntry(
        source_id="SRC_DRIVE_001",
        canonical_title=(
            "Estimating Compressional Velocity and Bulk Density Logs in Marine "
            "Gas Hydrates Using Machine Learning"
        ),
        short_citation="Naim, Cook, and Moortgat (2023)",
        doi_or_link="10.3390/en16237709",
        source_kind="missing_vp_density_ml",
        project_role=(
            "Missing Vp and RHOB prediction source for incomplete log suites."
        ),
        slide_3_use=(
            "Use for explaining missing-log adapters and uncertainty when Vp or "
            "bulk density is absent."
        ),
        stability_use="none",
        known_drive_or_gmail_location="Drive root file Estimating_Compressional_Velocity_and_Bulk_Density.pdf",
        github_push_status="manifest_only_until_pdf_license_review",
        next_action="Move into Drive source folder; record license before extracting figures.",
        expected_files=("Estimating_Compressional_Velocity_and_Bulk_Density.pdf",),
        match_terms=(
            "10.3390/en16237709",
            "estimating compressional velocity",
            "bulk density logs",
            "marine gas hydrates",
            "naim",
            "moortgat",
        ),
    ),
    SourceRegistryEntry(
        source_id="SRC_DRIVE_002",
        canonical_title=(
            "Permeability Evaluation of Hydrate Reservoirs Based on NMR T2 "
            "Relaxation Time from Both Log and Laboratory Data, Alaska North "
            "Slope HYDRATE 02 Geo Data Well"
        ),
        short_citation="Yoneda et al. (2026)",
        doi_or_link="10.1021/acs.energyfuels.5c05321",
        source_kind="direct_ans_nmr_core",
        project_role=(
            "Direct ANS NMR/core/permeability calibration source for HYDRATE 02."
        ),
        slide_3_use=(
            "Key source for showing NMR/core confirmation alongside log signals."
        ),
        stability_use="none",
        known_drive_or_gmail_location="Drive root file acs.energyfuels.5c05321.pdf",
        github_push_status="manifest_only_until_pdf_license_review",
        next_action="Move into Drive source folder; extract only allowed citation notes/figures.",
        expected_files=("acs.energyfuels.5c05321.pdf", "5c05321"),
        match_terms=(
            "10.1021/acs.energyfuels.5c05321",
            "5c05321",
            "nmr t2 relaxation",
            "hydrate 02 geo data well",
            "alaska north slope",
            "yoneda",
        ),
    ),
    SourceRegistryEntry(
        source_id="SRC_DRIVE_003",
        canonical_title=(
            "A comparative study of machine learning methods for gas hydrate "
            "identification"
        ),
        short_citation="Tian et al. (2023)",
        doi_or_link="10.1016/j.geoen.2023.211564",
        source_kind="comparative_hydrate_identification_ml",
        project_role=(
            "Comparative hydrate identification source using seismic/log "
            "feature families such as Vp/Vs."
        ),
        slide_3_use=(
            "Use for comparative ML identification logic and Vp/Vs cue caveats."
        ),
        stability_use="none",
        known_drive_or_gmail_location="Drive root file main.pdf",
        github_push_status="manifest_only_filename_main_requires_verify",
        next_action="Rename main.pdf after verifying title/DOI; avoid relying on filename alone.",
        expected_files=("main.pdf", "geoen.2023.211564"),
        match_terms=(
            "10.1016/j.geoen.2023.211564",
            "comparative study",
            "machine learning methods",
            "gas hydrate identification",
            "tian",
        ),
    ),
    SourceRegistryEntry(
        source_id="SRC_DRIVE_004",
        canonical_title=(
            "Alaska North Slope Extended-Duration Gas Hydrate Production Test "
            "Site Logging-While-Drilling Data Acquisition"
        ),
        short_citation="Aung et al. (2026)",
        doi_or_link="10.1021/acs.energyfuels.5c06115",
        source_kind="direct_ans_lwd_acquisition",
        project_role=(
            "Direct ANS LWD acquisition source for GR, resistivity, sonic, NMR, "
            "caliper/QC, and completion selection context."
        ),
        slide_3_use=(
            "Primary slide 3 source for the visual hydrate-signal bundle: clean "
            "GR interval, resistivity right-shift, sonic/elastic right-shift, "
            "NMR/core support, and QC."
        ),
        stability_use="context_only",
        known_drive_or_gmail_location="Drive root file acs.energyfuels.5c06115.pdf",
        github_push_status="manifest_only_until_pdf_license_review",
        next_action="Move into Drive source folder; prioritize figures/tables for slide 3 signal planning.",
        expected_files=("acs.energyfuels.5c06115.pdf", "5c06115"),
        match_terms=(
            "10.1021/acs.energyfuels.5c06115",
            "5c06115",
            "logging-while-drilling data acquisition",
            "extended-duration gas hydrate production test",
            "alaska north slope",
            "aung",
        ),
    ),
    SourceRegistryEntry(
        source_id="SRC_DRIVE_005",
        canonical_title=(
            "Research on the Estimate of Gas Hydrate Saturation Based on LSTM "
            "Recurrent Neural Network"
        ),
        short_citation="Li and Liu (2020)",
        doi_or_link="10.3390/en13246536",
        source_kind="sequence_saturation_ml",
        project_role=(
            "Comparative sequence-model source for saturation estimation from "
            "well logs."
        ),
        slide_3_use=(
            "Optional comparison source for sequence-model saturation; do not "
            "use as visual proof of ANS hydrate."
        ),
        stability_use="none",
        known_drive_or_gmail_location="Drive root file energies-13-06536-v2.pdf",
        github_push_status="manifest_only_until_pdf_license_review",
        next_action="Move into Drive source folder; record whether article is CC BY/open.",
        expected_files=("energies-13-06536-v2.pdf", "en13246536"),
        match_terms=(
            "10.3390/en13246536",
            "lstm recurrent neural network",
            "estimate of gas hydrate saturation",
            "li and liu",
            "energies",
        ),
    ),
    SourceRegistryEntry(
        source_id="SRC_STABILITY_001",
        canonical_title=(
            "Excel/CSV-derived stability curve screenshot and methane 5 ppt "
            "hydrate CSV products"
        ),
        short_citation="Project-derived stability visual package (2026)",
        doi_or_link="docs/source_library_index/stability_source_bundle_2026_06_13.md",
        source_kind="project_generated_stability_visual",
        project_role=(
            "Public-safe stability-context curve derived from the project source "
            "bundle and Excel/CSV products."
        ),
        slide_3_use=(
            "Use only as a small stability-context gate if slide 3 needs it; the "
            "core slide 3 story should stay focused on log/coring signals."
        ),
        stability_use=(
            "Only approved stability visual family for stability slides: use the "
            "Excel/CSV-derived screenshots, not generic stock curves."
        ),
        known_drive_or_gmail_location="docs/evidence/slide02_source_bundle_2026_06_17",
        github_push_status="public_safe_project_generated_products_ok",
        next_action="Use existing processed screenshots/CSV; do not substitute unrelated stability images.",
        expected_files=(
            "csv_methane_5ppt_phase_curve_slide_inset.png",
            "chat_selected_hydrate_stability_curve_crop.png",
            "phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1.csv",
            "slide02_selected_02_usgs_hydrate_stability_curve_crop.png",
            "slide02_selected_03_project_digitized_methane_5ppt_curve.csv",
        ),
        match_terms=(
            "csv_methane_5ppt_phase_curve_slide_inset",
            "chat_selected_hydrate_stability_curve_crop",
            "phase_curve_methane_5ppt_sir2008_csmhyd_digitized_v1",
            "slide02_selected_02_usgs_hydrate_stability_curve_crop",
            "slide02_selected_03_project_digitized_methane_5ppt_curve",
            "methane_5ppt",
            "stability_curve",
        ),
    ),
)


def default_source_library_index_dir(project_root: Path) -> Path:
    return project_root / "docs" / "source_library_index"


def normalize_text(value: object) -> str:
    text = str(value or "").lower()
    text = re.sub(r"[^a-z0-9./_-]+", " ", text)
    return " ".join(text.split())


def compact_text(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value or "").lower())


def safe_path_for_inventory(
    path: Path,
    *,
    project_root: Path,
    include_external_paths: bool = False,
) -> str:
    path = path.resolve()
    project_root = project_root.resolve()
    try:
        return path.relative_to(project_root).as_posix()
    except ValueError:
        if include_external_paths:
            return str(path)
        return f"[external-source]/{path.name}"


def iter_source_files(
    source_dirs: Sequence[Path],
    *,
    extensions: Iterable[str] = DEFAULT_SOURCE_EXTENSIONS,
) -> list[Path]:
    normalized_extensions = {
        ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in extensions
    }
    files: list[Path] = []
    for source_dir in source_dirs:
        if not source_dir.exists():
            continue
        if source_dir.is_file():
            if source_dir.suffix.lower() in normalized_extensions:
                files.append(source_dir)
            continue
        for path in source_dir.rglob("*"):
            if path.is_file() and path.suffix.lower() in normalized_extensions:
                files.append(path)
    return sorted(files, key=lambda value: str(value).lower())


def extract_pdf_text(path: Path, *, max_pages: int = 2, max_chars: int = 6000) -> str:
    readers = (_extract_pdf_text_with_pypdf, _extract_pdf_text_with_pdfplumber)
    for reader in readers:
        try:
            text = reader(path, max_pages=max_pages, max_chars=max_chars)
        except Exception:
            text = ""
        if text.strip():
            return text[:max_chars]
    return ""


def _extract_pdf_text_with_pypdf(path: Path, *, max_pages: int, max_chars: int) -> str:
    try:
        from pypdf import PdfReader
    except Exception:
        return ""

    reader = PdfReader(str(path))
    parts: list[str] = []
    for page in reader.pages[:max_pages]:
        parts.append(page.extract_text() or "")
        if sum(len(part) for part in parts) >= max_chars:
            break
    return "\n".join(parts)[:max_chars]


def _extract_pdf_text_with_pdfplumber(path: Path, *, max_pages: int, max_chars: int) -> str:
    try:
        import pdfplumber
    except Exception:
        return ""

    parts: list[str] = []
    with pdfplumber.open(str(path)) as pdf:
        for page in pdf.pages[:max_pages]:
            parts.append(page.extract_text() or "")
            if sum(len(part) for part in parts) >= max_chars:
                break
    return "\n".join(parts)[:max_chars]


def extract_source_text(path: Path, *, read_pdf_text: bool = True) -> str:
    if path.suffix.lower() == ".pdf" and read_pdf_text:
        return extract_pdf_text(path)
    if path.suffix.lower() in {".md", ".txt", ".html", ".htm"}:
        try:
            return path.read_text(encoding="utf-8", errors="ignore")[:6000]
        except Exception:
            return ""
    return ""


def title_snippet(text: str, *, max_chars: int = 220) -> str:
    cleaned = " ".join(str(text or "").split())
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[: max_chars - 3].rstrip() + "..."


def match_registry_entry(
    file_name: str,
    extracted_text: str = "",
    *,
    registry: Sequence[SourceRegistryEntry] = SOURCE_REGISTRY,
) -> tuple[SourceRegistryEntry | None, str, int]:
    name_norm = normalize_text(file_name)
    name_compact = compact_text(file_name)
    blob_norm = normalize_text(f"{file_name} {extracted_text}")
    blob_compact = compact_text(f"{file_name} {extracted_text}")

    best_entry: SourceRegistryEntry | None = None
    best_score = 0
    best_confidence = "unmatched"

    for entry in registry:
        score = 0
        doi = entry.doi_or_link
        if doi and doi.startswith("10.") and compact_text(doi) in blob_compact:
            score += 120
        for expected_file in entry.expected_files:
            expected_norm = normalize_text(expected_file)
            expected_compact = compact_text(expected_file)
            if expected_norm and expected_norm == name_norm:
                score += 80
            elif expected_compact and expected_compact in name_compact:
                score += 45
            elif expected_compact and expected_compact in blob_compact:
                score += 20
        for term in entry.match_terms:
            term_norm = normalize_text(term)
            term_compact = compact_text(term)
            if term_compact and term_compact in name_compact:
                score += 24
            elif term_norm and term_norm in blob_norm:
                score += 10
            elif term_compact and term_compact in blob_compact:
                score += 8

        if score > best_score:
            best_entry = entry
            best_score = score
            if score >= 120:
                best_confidence = "high_doi_or_exact_title"
            elif score >= 70:
                best_confidence = "high_filename_or_title"
            elif score >= 35:
                best_confidence = "medium_filename_terms"
            elif score >= 18:
                best_confidence = "review_filename_terms"
            else:
                best_confidence = "unmatched"

    if best_score < 18:
        return None, "unmatched", best_score
    return best_entry, best_confidence, best_score


def _entry_row(
    entry: SourceRegistryEntry,
    *,
    source_status: str,
    match_confidence: str,
    file_path: Path | None,
    project_root: Path,
    detected_text: str = "",
    include_external_paths: bool = False,
) -> dict[str, object]:
    if file_path is None:
        file_name = ""
        extension = ""
        size = ""
        safe_path = ""
    else:
        file_name = file_path.name
        extension = file_path.suffix.lower()
        try:
            size = file_path.stat().st_size
        except OSError:
            size = ""
        safe_path = safe_path_for_inventory(
            file_path,
            project_root=project_root,
            include_external_paths=include_external_paths,
        )

    return {
        "source_id": entry.source_id,
        "source_status": source_status,
        "match_confidence": match_confidence,
        "canonical_title": entry.canonical_title,
        "short_citation": entry.short_citation,
        "doi_or_link": entry.doi_or_link,
        "source_kind": entry.source_kind,
        "project_role": entry.project_role,
        "slide_3_use": entry.slide_3_use,
        "stability_use": entry.stability_use,
        "file_name": file_name,
        "extension": extension,
        "bytes": size,
        "safe_path": safe_path,
        "detected_title_snippet": title_snippet(detected_text),
        "known_drive_or_gmail_location": entry.known_drive_or_gmail_location,
        "github_push_status": entry.github_push_status,
        "next_action": entry.next_action,
        "guardrail": PUBLIC_GUARDRAIL,
    }


def _unknown_row(
    *,
    unknown_number: int,
    file_path: Path,
    project_root: Path,
    detected_text: str,
    include_external_paths: bool,
) -> dict[str, object]:
    try:
        size = file_path.stat().st_size
    except OSError:
        size = ""
    return {
        "source_id": f"SRC_UNMATCHED_{unknown_number:03d}",
        "source_status": UNMATCHED_STATUS,
        "match_confidence": "unmatched",
        "canonical_title": "",
        "short_citation": "",
        "doi_or_link": "",
        "source_kind": "unmatched_local_source_file",
        "project_role": "Review manually before using in Word, deck, website, or model notes.",
        "slide_3_use": "unknown_until_reviewed",
        "stability_use": "unknown_until_reviewed",
        "file_name": file_path.name,
        "extension": file_path.suffix.lower(),
        "bytes": size,
        "safe_path": safe_path_for_inventory(
            file_path,
            project_root=project_root,
            include_external_paths=include_external_paths,
        ),
        "detected_title_snippet": title_snippet(detected_text),
        "known_drive_or_gmail_location": "",
        "github_push_status": "do_not_push_raw_until_reviewed",
        "next_action": "Identify citation, DOI/link, license, and project role before reuse.",
        "guardrail": PUBLIC_GUARDRAIL,
    }


def matched_file_status(entry: SourceRegistryEntry, file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    if entry.source_id == "SRC_STABILITY_001":
        if suffix in {".csv", ".gif", ".jpeg", ".jpg", ".png", ".webp"}:
            return FOUND_SOURCE_STATUS
        return FOUND_REFERENCE_STATUS
    if suffix == ".pdf":
        return FOUND_SOURCE_STATUS
    return FOUND_REFERENCE_STATUS


def build_source_intake_inventory(
    source_dirs: Sequence[Path],
    *,
    project_root: Path,
    registry: Sequence[SourceRegistryEntry] = SOURCE_REGISTRY,
    read_pdf_text: bool = True,
    include_external_paths: bool = False,
    extensions: Iterable[str] = DEFAULT_SOURCE_EXTENSIONS,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    matched_source_ids: set[str] = set()
    unknown_number = 1

    for file_path in iter_source_files(source_dirs, extensions=extensions):
        detected_text = extract_source_text(file_path, read_pdf_text=read_pdf_text)
        entry, confidence, _score = match_registry_entry(
            file_path.name,
            detected_text,
            registry=registry,
        )
        if entry is None:
            rows.append(
                _unknown_row(
                    unknown_number=unknown_number,
                    file_path=file_path,
                    project_root=project_root,
                    detected_text=detected_text,
                    include_external_paths=include_external_paths,
                )
            )
            unknown_number += 1
            continue
        source_status = matched_file_status(entry, file_path)
        if source_status == FOUND_SOURCE_STATUS:
            matched_source_ids.add(entry.source_id)
        rows.append(
            _entry_row(
                entry,
                source_status=source_status,
                match_confidence=confidence,
                file_path=file_path,
                project_root=project_root,
                detected_text=detected_text,
                include_external_paths=include_external_paths,
            )
        )

    for entry in registry:
        if entry.source_id in matched_source_ids:
            continue
        rows.append(
            _entry_row(
                entry,
                source_status=MISSING_STATUS,
                match_confidence="not_found_in_scanned_dirs",
                file_path=None,
                project_root=project_root,
            )
        )

    frame = pd.DataFrame(rows)
    for column in SOURCE_INTAKE_COLUMNS:
        if column not in frame.columns:
            frame[column] = ""
    return frame[SOURCE_INTAKE_COLUMNS].sort_values(
        by=["source_status", "source_id", "file_name"],
        ascending=[True, True, True],
        ignore_index=True,
    )


def _join_values(values: Iterable[object]) -> str:
    cleaned = [str(value).strip() for value in values if str(value).strip()]
    return "; ".join(cleaned)


def source_intake_summary(inventory: pd.DataFrame) -> dict[str, object]:
    found = inventory[inventory["source_status"].eq(FOUND_SOURCE_STATUS)]
    reference_notes = inventory[inventory["source_status"].eq(FOUND_REFERENCE_STATUS)]
    missing = inventory[inventory["source_status"].eq(MISSING_STATUS)]
    unmatched = inventory[inventory["source_status"].eq(UNMATCHED_STATUS)]
    slide3_sources = inventory[
        inventory["slide_3_use"].fillna("").str.contains("slide 3|signal|log|core|nmr|resistivity|sonic|Vs", case=False, regex=True)
        & inventory["source_id"].ne("SRC_STABILITY_001")
    ]
    stability_sources = inventory[
        inventory["stability_use"].fillna("").str.contains("stability|curve|context", case=False, regex=True)
    ]
    return {
        "rows": int(len(inventory)),
        "found_local": int(len(found)),
        "found_local_reference_note": int(len(reference_notes)),
        "expected_missing_or_drive_only": int(len(missing)),
        "found_local_unmatched_review": int(len(unmatched)),
        "slide3_source_ids": sorted(set(slide3_sources["source_id"].astype(str))),
        "stability_source_ids": sorted(set(stability_sources["source_id"].astype(str))),
        "missing_source_ids": sorted(set(missing["source_id"].astype(str))),
        "unmatched_files": sorted(unmatched["file_name"].astype(str).tolist()),
    }


def _best_rows_for_source_ids(inventory: pd.DataFrame, source_ids: Sequence[str]) -> pd.DataFrame:
    status_rank = {
        FOUND_SOURCE_STATUS: 0,
        FOUND_REFERENCE_STATUS: 1,
        MISSING_STATUS: 2,
        UNMATCHED_STATUS: 3,
    }
    rows: list[pd.Series] = []
    for source_id in source_ids:
        subset = inventory[inventory["source_id"].eq(source_id)].copy()
        if subset.empty:
            continue
        subset["_rank"] = subset["source_status"].map(status_rank).fillna(99)
        rows.append(subset.sort_values(["_rank", "file_name"]).iloc[0].drop(labels=["_rank"]))
    if not rows:
        return pd.DataFrame(columns=inventory.columns)
    return pd.DataFrame(rows).reset_index(drop=True)


def markdown_source_intake_report(
    inventory: pd.DataFrame,
    *,
    generated_at_utc: str | None = None,
) -> str:
    generated_at_utc = generated_at_utc or datetime.now(timezone.utc).isoformat(timespec="seconds")
    summary = source_intake_summary(inventory)
    found = inventory[inventory["source_status"].eq(FOUND_SOURCE_STATUS)]
    reference_notes = inventory[inventory["source_status"].eq(FOUND_REFERENCE_STATUS)]
    direct_slide3 = _best_rows_for_source_ids(
        inventory,
        ["SRC_DRIVE_004", "SRC_DRIVE_002", "SRC_EXISTING_001"],
    )
    stability = _best_rows_for_source_ids(inventory, ["SRC_STABILITY_001"])
    missing = inventory[inventory["source_status"].eq(MISSING_STATUS)]

    lines = [
        "# Source Organization Report",
        "",
        f"Generated UTC: `{generated_at_utc}`",
        "",
        "## Scope",
        "",
        "This report inventories public/source-planning files only. It records source status, use, and next actions without copying raw PDFs or approved-data rows into GitHub.",
        "",
        "## Counts",
        "",
        f"- Inventory rows: `{summary['rows']}`",
        f"- Found local source files/assets: `{summary['found_local']}`",
        f"- Found local reference notes/pages: `{summary['found_local_reference_note']}`",
        f"- Expected missing or Drive/Gmail-only sources: `{summary['expected_missing_or_drive_only']}`",
        f"- Unmatched local files needing review: `{summary['found_local_unmatched_review']}`",
        "",
        "## Slide 3 Priority Sources",
        "",
    ]
    for _, row in direct_slide3.iterrows():
        lines.append(
            f"- `{row['source_id']}` - {row['short_citation']}: {row['slide_3_use']} "
            f"Status: `{row['source_status']}`."
        )
    if direct_slide3.empty:
        lines.append("- No direct slide 3 priority source rows were generated.")

    lines.extend(["", "## Stability Visual Rule", ""])
    if not stability.empty:
        for _, row in stability.iterrows():
            lines.append(
                f"- `{row['source_id']}` - {row['canonical_title']}: "
                f"{row['stability_use']} Status: `{row['source_status']}`."
            )
    else:
        lines.append(
            "- Use only the project Excel/CSV-derived stability curve screenshots for stability visuals."
        )

    lines.extend(["", "## Found Local Source Files And Assets", ""])
    if found.empty:
        lines.append("- No matching local source files or source assets found in scanned folders.")
    else:
        for _, row in found.iterrows():
            lines.append(
                f"- `{row['source_id']}` `{row['file_name']}` -> `{row['safe_path']}` "
                f"({row['match_confidence']})"
            )

    lines.extend(["", "## Found Reference Notes Or Pages", ""])
    if reference_notes.empty:
        lines.append("- No matching reference notes or pages found.")
    else:
        for _, row in reference_notes.iterrows():
            lines.append(
                f"- `{row['source_id']}` `{row['file_name']}` -> `{row['safe_path']}` "
                f"({row['match_confidence']}); this does not satisfy the PDF/source-file check."
            )

    lines.extend(["", "## Missing Or Drive/Gmail-Only Sources", ""])
    for _, row in missing.iterrows():
        lines.append(
            f"- `{row['source_id']}` - {row['short_citation']}: {row['known_drive_or_gmail_location']}. "
            f"Next: {row['next_action']}"
        )

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            f"- {PUBLIC_GUARDRAIL}",
            "- Slide 3 should show signal movement and cross-checks, not just parameter ranges.",
            "- Stability products are context/admissibility visuals only, not hydrate proof.",
        ]
    )
    return "\n".join(lines)


def markdown_source_gaps_report(inventory: pd.DataFrame) -> str:
    missing = inventory[inventory["source_status"].eq(MISSING_STATUS)]
    unmatched = inventory[inventory["source_status"].eq(UNMATCHED_STATUS)]
    lines = [
        "# Source Gaps And Downloads",
        "",
        "## Download / Verify Queue",
        "",
    ]
    for _, row in missing.iterrows():
        lines.append(
            f"- `{row['source_id']}` - {row['short_citation']}: {row['next_action']} "
            f"Known location/status: {row['known_drive_or_gmail_location']}"
        )
    if missing.empty:
        lines.append("- No expected sources are missing from the scanned folders.")

    lines.extend(["", "## Unmatched Local Files", ""])
    if unmatched.empty:
        lines.append("- No unmatched local files found.")
    else:
        for _, row in unmatched.iterrows():
            lines.append(
                f"- `{row['file_name']}` at `{row['safe_path']}`: identify citation and push status before use."
            )

    lines.extend(
        [
            "",
            "## GitHub Rule",
            "",
            "- Commit this report, CSV inventories, notes, prompts, and public-safe derived screenshots.",
            "- Keep raw PDFs in Drive/local source folders unless redistribution rights and file size are reviewed.",
        ]
    )
    return "\n".join(lines)


def markdown_drive_gmail_handoff(inventory: pd.DataFrame) -> str:
    summary = source_intake_summary(inventory)
    lines = [
        "# Drive/Gmail Source Handoff",
        "",
        "## Known Intake Locations",
        "",
        "- Gmail thread/draft subject: `new paps`",
        "- Gmail message id: `19ed80c3c8baedbe`",
        "- Gmail attachments to verify: `sign2019.pdf`, `falahat.pdf`",
        "- Drive upload: `collet2019.pdf`",
        "- Drive URL: <https://drive.google.com/file/d/1kMr-KBqpB4RS-9soUT60PwD918ZvcUtF/view>",
        "",
        "## PC Command Template",
        "",
        "```powershell",
        "python 01_pipeline\\build_source_intake_inventory.py `",
        "  --source-dir \"C:\\path\\to\\Drive\\North Slope Gas Hydrates\\source_intake_2026-06-17\\01_raw_pdfs\" `",
        "  --source-dir \"C:\\path\\to\\Drive\\North Slope Gas Hydrates\\source_intake_2026-06-17\\02_source_screenshots\" `",
        "  --source-dir \"docs\\evidence\\slide02_source_bundle_2026_06_17\" `",
        "  --output-dir \"docs\\source_library_index\" `",
        "  --date-tag 2026-06-18",
        "```",
        "",
        "## Current Inventory Snapshot",
        "",
        f"- Found local source files/assets: `{summary['found_local']}`",
        f"- Found local reference notes/pages: `{summary['found_local_reference_note']}`",
        f"- Missing or Drive/Gmail-only source rows: `{summary['expected_missing_or_drive_only']}`",
        f"- Unmatched local source files: `{summary['found_local_unmatched_review']}`",
        f"- Slide 3 source ids in registry: `{_join_values(summary['slide3_source_ids'])}`",
        f"- Stability source ids in registry: `{_join_values(summary['stability_source_ids'])}`",
        "",
        "## Required PC Output Back To GitHub",
        "",
        "- Updated source inventory CSV and Markdown reports.",
        "- Source notes that summarize log/coring signals and figure candidates.",
        "- Public-safe crops/screenshots only when license/use has been recorded.",
        "- No raw PDFs, private Gmail exports, approved data rows, credentials, or model outputs.",
    ]
    return "\n".join(lines)


def write_source_intake_outputs(
    inventory: pd.DataFrame,
    *,
    output_dir: Path,
    date_tag: str,
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    date_slug = re.sub(r"[^0-9A-Za-z_-]+", "_", date_tag).strip("_") or "latest"
    csv_path = output_dir / f"source_inventory_{date_slug}.csv"
    report_path = output_dir / f"SOURCE_ORGANIZATION_REPORT_{date_slug}.md"
    gaps_path = output_dir / f"SOURCE_GAPS_AND_DOWNLOADS_{date_slug}.md"
    handoff_path = output_dir / f"DRIVE_GMAIL_SOURCE_HANDOFF_{date_slug}.md"

    inventory.to_csv(csv_path, index=False)
    report_path.write_text(markdown_source_intake_report(inventory), encoding="utf-8")
    gaps_path.write_text(markdown_source_gaps_report(inventory), encoding="utf-8")
    handoff_path.write_text(markdown_drive_gmail_handoff(inventory), encoding="utf-8")

    return {
        "csv": csv_path,
        "report": report_path,
        "gaps": gaps_path,
        "handoff": handoff_path,
    }
