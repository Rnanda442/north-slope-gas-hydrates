from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pandas as pd
import plotly.graph_objects as go
from PIL import Image, ImageChops
from plotly.subplots import make_subplots
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from pptx import Presentation
from pptx.dml.color import RGBColor as PptRGB
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches as PptInches, Pt as PptPt

from dashboard.well_log_engine import (
    generate_synthetic_logs,
    model_placeholder_figures,
    screen_intervals,
    sweet_spot_review_table,
    well_log_panel,
)
OUT_DIR = REPO_ROOT / "docs" / "project_blueprints"
DOCX_OUT = OUT_DIR / "North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview.docx"
PPTX_OUT = OUT_DIR / "North_Slope_Gas_Hydrate_Reservoir_Characterization_Research_Overview.pptx"
ASSET_DIR = OUT_DIR / "presentation_assets"
MASTER_3D = REPO_ROOT / "03_data_final" / "master_layers" / "north_slope_master_3d_surfaces.parquet"
MASTER_2D = REPO_ROOT / "03_data_final" / "master_layers" / "north_slope_master_2d_layers.parquet"

NAVY = "123447"
TEAL = "167D8D"
ICE = "EAF5F6"
SAND = "F4EFE6"
GRAY = "EEF2F4"
INK = "1F2933"
MUTED = "5E6A71"
WHITE = "FFFFFF"


REFERENCES = [
    "Collett, T.S., Lewis, K.A., Zyrianova, M.V., and others. 2019. Assessment of undiscovered gas hydrate resources in the North Slope of Alaska, 2018. USGS Fact Sheet 2019-3037. DOI: 10.3133/fs20193037. https://pubs.usgs.gov/publication/fs20193037",
    "National Energy Technology Laboratory. Alaska North Slope Gas Hydrate Reservoir Characterization. Project summary. https://netl.doe.gov/node/6846",
    "U.S. Department of Energy. 2024. DOE and international partners complete gas hydrates production testing on Alaska North Slope. https://www.energy.gov/hgeo/articles/doe-and-international-partners-complete-gas-hydrates-production-testing-alaska-north",
    "Chong, L.B., Singh, H., Creason, C.G., and others. 2022. Application of machine learning to characterize gas hydrate reservoirs in Mackenzie Delta (Canada) and on the Alaska North Slope (USA). Computational Geosciences, 26, 991-1006. DOI: 10.1007/s10596-022-10151-9. https://link.springer.com/article/10.1007/s10596-022-10151-9",
    "Lee, M.W., and Collett, T.S. 2011. In-situ gas hydrate saturation estimated from various well logs at the Mount Elbert Gas Hydrate Stratigraphic Test Well, Alaska North Slope. Marine and Petroleum Geology, 28, 439-449. https://pubs.usgs.gov/publication/70036903",
    "Haines, S.S., Collett, T.S., Yoneda, J., Shimoda, N., Boswell, R., and Okinaka, N. 2022. Gas hydrate saturation estimates, gas hydrate occurrence, and reservoir characteristics based on well log data from the Hydrate-01 stratigraphic test well, Alaska North Slope. Energy & Fuels, 36, 3040-3050. DOI: 10.1021/acs.energyfuels.1c04100. https://pubs.acs.org/doi/10.1021/acs.energyfuels.1c04100",
    "Zyrianova, M.V., Collett, T.S., and Boswell, R. 2024. Characterization of structural, stratigraphic, and reservoir controls on gas hydrate occurrence in the Eileen Gas Hydrate Trend, Alaska North Slope. https://www.mdpi.com/2077-1312/12/3/472",
]


def export_plotly(figure: go.Figure, path: Path, width=1200, height=720) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.write_image(str(path), width=width, height=height, scale=1.7)
    trim_white_margin(path)
    return path


def trim_white_margin(path: Path, padding: int = 28) -> None:
    image = Image.open(path).convert("RGB")
    background = Image.new("RGB", image.size, (255, 255, 255))
    diff = ImageChops.difference(image, background)
    bbox = diff.getbbox()
    if not bbox:
        image.save(path)
        return
    left = max(0, bbox[0] - padding)
    top = max(0, bbox[1] - padding)
    right = min(image.size[0], bbox[2] + padding)
    bottom = min(image.size[1], bbox[3] + padding)
    image.crop((left, top, right, bottom)).save(path)


def project_asset_path(name: str) -> Path:
    return ASSET_DIR / name


def build_regional_3d_asset() -> Path:
    surfaces = pd.read_parquet(
        MASTER_3D,
        columns=["lon", "lat", "depth_m", "surface_name"],
    )
    wells = pd.read_parquet(
        MASTER_2D,
        columns=["layer_name", "lon", "lat", "depth_m"],
    )
    wells = wells[wells["layer_name"] == "wells"].dropna(subset=["lon", "lat"]).head(450)

    figure = go.Figure()
    colors = {"NStopo": "#3F8E54", "NSLCU": "#2878B5", "NSshublik": "#D9773D", "NSbasement": "#7353A4"}
    for surface_name in ["NStopo", "NSLCU", "NSshublik", "NSbasement"]:
        subset = surfaces[surfaces["surface_name"] == surface_name].dropna()
        if subset.empty:
            continue
        subset = subset.iloc[:: max(1, len(subset) // 1800)]
        figure.add_trace(
            go.Scatter3d(
                x=subset["lon"],
                y=subset["lat"],
                z=-subset["depth_m"],
                mode="markers",
                marker={"size": 2.2, "color": colors[surface_name], "opacity": 0.62},
                name=surface_name,
            )
        )
    figure.add_trace(
        go.Scatter3d(
            x=wells["lon"],
            y=wells["lat"],
            z=[120] * len(wells),
            mode="markers",
            marker={"size": 2.8, "color": "#0B1F2A", "opacity": 0.85},
            name="public wells",
        )
    )
    figure.update_layout(
        title="Public North Slope structural context and well inventory",
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin={"l": 0, "r": 0, "t": 52, "b": 0},
        legend={"orientation": "h", "y": 0.02, "x": 0.02},
        scene={
            "xaxis_title": "Longitude",
            "yaxis_title": "Latitude",
            "zaxis_title": "Relative depth",
            "camera": {"eye": {"x": 1.55, "y": -1.7, "z": 0.85}},
        },
    )
    return export_plotly(figure, project_asset_path("regional_3d_context.png"), 1280, 760)


def build_well_log_asset(logs: pd.DataFrame) -> Path:
    figure = well_log_panel(logs, "SYNTH-WELL-01")
    figure.update_layout(title="Synthetic well-log scaffold: multi-log hydrate interpretation")
    return export_plotly(figure, project_asset_path("synthetic_well_log_panel.png"), 1280, 760)


def build_ml_metrics_asset() -> Path:
    confusion, calibration = model_placeholder_figures()
    figure = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Classification error view", "Saturation calibration view"),
        horizontal_spacing=0.14,
    )
    for trace in confusion.data:
        figure.add_trace(trace, row=1, col=1)
    for trace in calibration.data:
        figure.add_trace(trace, row=1, col=2)
    figure.update_xaxes(title_text="Predicted class", row=1, col=1)
    figure.update_yaxes(title_text="Reference class", row=1, col=1)
    figure.update_xaxes(title_text="Predicted probability", row=1, col=2)
    figure.update_yaxes(title_text="Observed frequency", row=1, col=2)
    figure.update_layout(
        title="Model validation outputs to replace placeholders after approved-data execution",
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin={"l": 58, "r": 30, "t": 70, "b": 52},
    )
    return export_plotly(figure, project_asset_path("model_validation_placeholders.png"), 1280, 640)


def build_sweet_spot_asset(logs: pd.DataFrame) -> Path:
    intervals = screen_intervals(logs)
    ranked = sweet_spot_review_table(intervals).head(8).sort_values("Synthetic review priority")
    figure = go.Figure(
        go.Bar(
            x=ranked["Synthetic review priority"],
            y=ranked["Well alias"] + " " + ranked["Top depth (m)"].astype(str) + "-" + ranked["Base depth (m)"].astype(str) + " m",
            orientation="h",
            marker={"color": ranked["Hydrate-saturation proxy"], "colorscale": "Tealgrn", "showscale": True, "colorbar": {"title": "Sh proxy"}},
            text=ranked["Evidence domains passed"],
            textposition="outside",
        )
    )
    figure.update_layout(
        title="Synthetic sweet-spot ranking scaffold",
        xaxis_title="Review priority score",
        yaxis_title="Synthetic interval",
        margin={"l": 190, "r": 80, "t": 70, "b": 50},
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    return export_plotly(figure, project_asset_path("sweet_spot_ranking.png"), 1280, 640)


def build_visual_assets() -> dict[str, Path]:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    logs = generate_synthetic_logs()
    return {
        "regional_3d": build_regional_3d_asset(),
        "well_log": build_well_log_asset(logs),
        "metrics": build_ml_metrics_asset(),
        "sweet_spot": build_sweet_spot_asset(logs),
    }


def shade_cell(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), fill)
    tc_pr.append(shading)


def set_borders(table, color="B7C9D3") -> None:
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        element = OxmlElement(f"w:{edge}")
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), "4")
        element.set(qn("w:space"), "0")
        element.set(qn("w:color"), color)
        borders.append(element)
    tbl_pr.append(borders)


def write_cell(cell, text: str, *, bold=False, color=INK, size=8.6, align=WD_ALIGN_PARAGRAPH.LEFT) -> None:
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(text)
    run.bold = bold
    run.font.name = "Aptos"
    run.font.size = Pt(size)
    run.font.color.rgb = RGBColor.from_string(color)


def configure_doc(doc: Document) -> None:
    section = doc.sections[0]
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.65)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Aptos"
    normal.font.size = Pt(10.2)
    normal.paragraph_format.space_after = Pt(5)
    for style_name, size, color in [
        ("Heading 1", 15, NAVY),
        ("Heading 2", 12.5, TEAL),
        ("Heading 3", 11, NAVY),
    ]:
        style = styles[style_name]
        style.font.name = "Aptos Display"
        style.font.size = Pt(size)
        style.font.color.rgb = RGBColor.from_string(color)
        style.paragraph_format.space_before = Pt(10)
        style.paragraph_format.space_after = Pt(4)


def add_body(doc: Document, text: str, size=10.2) -> None:
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.1
    for run in p.runs:
        run.font.name = "Aptos"
        run.font.size = Pt(size)
        run.font.color.rgb = RGBColor.from_string(INK)


def add_note(doc: Document, text: str) -> None:
    table = doc.add_table(rows=1, cols=1)
    table.style = "Table Grid"
    set_borders(table, "D2C8B8")
    cell = table.cell(0, 0)
    shade_cell(cell, SAND)
    write_cell(cell, text, bold=True, size=9.2, color=NAVY)
    doc.add_paragraph()


def add_process_sketch(doc: Document, title: str, labels: list[str], fill=SAND) -> None:
    doc.add_heading(title, level=3)
    cols = len(labels) * 2 - 1
    table = doc.add_table(rows=1, cols=cols)
    table.style = "Table Grid"
    set_borders(table, "C5D3D8")
    widths = [1.0 if i % 2 == 0 else 0.25 for i in range(cols)]
    for idx, width in enumerate(widths):
        table.cell(0, idx).width = Inches(width)
    for idx in range(cols):
        cell = table.cell(0, idx)
        if idx % 2 == 0:
            shade_cell(cell, fill if idx in {0, cols - 1} else ICE)
            write_cell(cell, labels[idx // 2], bold=True, size=7.8, color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER)
        else:
            shade_cell(cell, WHITE)
            write_cell(cell, "->", bold=True, size=9.5, color=TEAL, align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_paragraph()


def add_placeholder_section(doc: Document, title: str, sentence: str) -> None:
    doc.add_heading(title, level=1)
    add_body(doc, sentence)


def build_docx() -> None:
    doc = Document()
    configure_doc(doc)

    title = doc.add_paragraph()
    title.paragraph_format.space_after = Pt(2)
    run = title.add_run("Gas Hydrate Occurrence and Saturation Prediction in Permafrost Sediments on the Alaska North Slope Using AI/ML")
    run.bold = True
    run.font.name = "Aptos Display"
    run.font.size = Pt(20)
    run.font.color.rgb = RGBColor.from_string(NAVY)

    subtitle = doc.add_paragraph("Research-paper outline with filled abstract and introduction")
    subtitle.paragraph_format.space_after = Pt(8)
    for run in subtitle.runs:
        run.font.name = "Aptos"
        run.font.size = Pt(10.5)
        run.font.color.rgb = RGBColor.from_string(MUTED)

    add_note(
        doc,
        "Boundary: this public-source planning document contains no restricted well logs, approved-runtime data, named restricted well identifiers, populated model results, credentials, or sensitive derived outputs.",
    )

    doc.add_heading("Abstract", level=1)
    add_body(
        doc,
        "Gas hydrates are solid crystalline compounds in which gas molecules, dominantly methane, are trapped inside cages of water molecules under cold and high-pressure conditions. On the Alaska North Slope, permafrost and shallow subsurface pressure-temperature conditions create a setting where hydrate can accumulate in sand-rich reservoirs and represent a significant natural-gas resource. The United States Geological Survey assessed the North Slope gas hydrate system as containing a mean of approximately 53.8 trillion cubic feet of undiscovered, technically recoverable gas in hydrate accumulations, making the region an important target for energy-resource characterization and long-term energy security planning. This project develops a physics-constrained machine-learning workflow for predicting gas hydrate occurrence and saturation from approved well-log and core-analysis data. The workflow will compile published AI/ML methods, generate a depth-indexed dataset from density, porosity, natural gamma ray, resistivity, acoustic velocity, NMR, and core measurements, train classification and regression models, and calibrate predictions against core and interpreted saturation evidence. The expected outcome is an auditable reservoir characterization framework that separates hydrate occurrence, saturation, reservoir quality, uncertainty, and later producibility screening.",
    )

    doc.add_heading("Introduction", level=1)
    add_body(
        doc,
        "Gas hydrates are ice-like solids that store methane in the pore systems of sediment. They are not conventional gas reservoirs, because the gas is held in a solid water-gas structure rather than existing as a free gas phase. Their formation requires pressure-temperature stability, but stability alone is not enough to produce an accumulation. A reservoir interval must also have pore space, a supply of gas, migration pathways, water, and geologic architecture that allows hydrate to occupy and remain within the sediment. This distinction is central to the Alaska North Slope project. The purpose is not only to ask where hydrate could be stable, but to identify which intervals are most likely to contain hydrate, how much pore volume is occupied, and how reliable that interpretation is."
    )
    add_body(
        doc,
        "The Alaska North Slope is a strong study area because it combines permafrost-associated hydrate stability, documented hydrate-bearing test wells, public regional geologic context, and a history of DOE, NETL, USGS, and industry-supported hydrate research. Mount Elbert, Hydrate-01, and Eileen-trend studies show that hydrate-bearing sands can be investigated using a multi-log interpretation that includes resistivity, density, neutron and NMR porosity, sonic velocity, and core calibration. This project uses that research base to build a practical workflow for approved data. The final scientific question is whether well-log and core measurements can be processed into reliable machine-learning features that predict occurrence and saturation across known and prediction wells."
    )
    add_body(
        doc,
        "Characterizing a gas hydrate reservoir matters because a regional resource estimate does not identify the best intervals for detailed evaluation. Characterization translates resource potential into interval-scale evidence. It asks whether the rock is a reservoir, whether the log response is consistent with hydrate rather than gas, ice, shale, carbonate, coal, or borehole effects, whether NMR or core evidence supports a saturation estimate, and whether the uncertainty is low enough for the result to be used in a technical decision. High resistivity alone is not a hydrate label, and high saturation alone is not a producibility ranking. Occurrence, saturation, reservoir quality, uncertainty, and producibility must remain separate outputs."
    )
    add_body(
        doc,
        "The project will use all available screenshot-listed fields and NMR where present. The expected input families include depth, location, gamma ray, density, density porosity, neutron porosity, NMR porosity, resistivity, caliper, Vp, Vs, Vp/Vs, acoustic impedance, interpreted hydrate saturation fields such as Sgh or S_h, NMR-derived saturation where supplied, core porosity, permeability, lithology, and quality flags. These variables are scientifically useful only when their roles are controlled. Measured curves, derived features, quality-control fields, alignment fields, and supervised targets must be separated so that the model does not accidentally learn from the answer column it is supposed to predict."
    )
    add_process_sketch(
        doc,
        "Conceptual hydrate-reservoir sketch",
        ["stability", "reservoir sand", "gas charge", "multi-log evidence", "saturation", "sweet spot"],
    )
    add_body(
        doc,
        "The machine-learning component will follow a staged workflow rather than immediately relying on a black-box model. Raw well-log data must first be compared, cleaned, depth-aligned, and screened for outliers and borehole-quality problems. Relevant depth intervals will then be selected, processed into a consistent dataset, and transformed into petrophysical and geomechanical features. The project will compare historical AI/ML approaches for gas hydrate occurrence and saturation prediction, then use baseline classification and regression models before testing nonlinear models such as artificial neural networks. Keras-based neural-network workflows are appropriate only after the training labels, curve coverage, and validation design are defensible."
    )
    add_process_sketch(
        doc,
        "Approved-data processing sketch",
        ["raw logs", "QC", "features", "labels", "ML models", "validated outputs"],
        fill=ICE,
    )
    add_body(
        doc,
        "A key methodological control is validation by complete well. Randomly splitting neighboring depth samples can make performance appear stronger than it will be on an unseen well because adjacent samples are highly correlated. The planned workflow will reserve complete wells for validation and testing, report classification and regression error, and compare predicted saturation against core and interpreted reference measurements. The final deliverables will present the work in graphical and tabular form so that conclusions, recommendations, and uncertainty can be reviewed by geoscientists and energy-resource decision makers."
    )

    add_placeholder_section(
        doc,
        "Parameters",
        "This section will define each input variable, unit convention, source mnemonic, derived feature, and target field used in the approved-data workflow, including density, porosity, gamma ray, resistivity, Vp, Vs, NMR, caliper, hydrate saturation, core porosity, core permeability, and lithology.",
    )
    add_process_sketch(
        doc,
        "Parameter-role sketch",
        ["measured logs", "derived physics", "QC flags", "targets", "outputs"],
        fill=SAND,
    )

    add_placeholder_section(
        doc,
        "Methodology",
        "This section will describe data intake, unit standardization, outlier removal, depth matching, feature engineering, core-log calibration, and the workflow used to generate the final machine-learning dataset.",
    )
    add_body(
        doc,
        "The geomechanical feature set will include dynamic Young's modulus, Poisson's ratio, brittleness, lambda-rho, and mu-rho where density, Vp, and Vs are available. These features help place hydrate interpretation in a rock-physics context because stiffness, rigidity, and incompressibility can help distinguish hydrate-supported responses from gas, lithology, or stress effects."
    )

    add_placeholder_section(
        doc,
        "Machine-Learning Framework",
        "This section will compare classification models for hydrate occurrence, regression models for continuous hydrate saturation, and nonlinear ANN methods informed by Chong et al. (2022), while preserving complete-well validation and target-leakage controls.",
    )
    add_process_sketch(
        doc,
        "ML architecture sketch",
        ["features", "classification", "saturation regression", "ANN test", "held-out wells"],
        fill=ICE,
    )

    add_placeholder_section(
        doc,
        "Error and Validation",
        "This section will report classification precision, recall, F1, confusion matrices, regression MAE, RMSE, R2, calibration by saturation band, outlier behavior, missing-curve performance, and validation against unseen wells.",
    )
    add_placeholder_section(
        doc,
        "Discussion",
        "This section will interpret the predicted hydrate intervals, compare model behavior against geologic expectations, discuss false positives and ambiguous intervals, and explain how reservoir quality and uncertainty affect sweet-spot ranking.",
    )
    add_placeholder_section(
        doc,
        "Conclusion",
        "This section will summarize what the workflow demonstrates, what the final approved-data results show, and how the project supports North Slope gas hydrate reservoir characterization for future energy-resource evaluation.",
    )

    doc.add_heading("References", level=1)
    for ref in REFERENCES:
        add_body(doc, ref, size=9)

    doc.save(DOCX_OUT)


def ppt_color(hex_color: str) -> PptRGB:
    return PptRGB(int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))


def add_textbox(slide, x, y, w, h, text, size=18, bold=False, color=INK, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(PptInches(x), PptInches(y), PptInches(w), PptInches(h))
    frame = box.text_frame
    frame.clear()
    frame.margin_left = PptInches(0.05)
    frame.margin_right = PptInches(0.05)
    frame.vertical_anchor = MSO_ANCHOR.TOP
    p = frame.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = "Aptos"
    run.font.size = PptPt(size)
    run.font.bold = bold
    run.font.color.rgb = ppt_color(color)
    return box


def add_title(slide, title, subtitle=None):
    add_textbox(slide, 0.55, 0.24, 12.1, 0.45, title, size=24, bold=True, color=NAVY)
    if subtitle:
        add_textbox(slide, 0.58, 0.76, 11.8, 0.35, subtitle, size=11.5, color=MUTED)


def add_panel(slide, x, y, w, h, fill=ICE, line=TEAL, radius=True):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(shape_type, PptInches(x), PptInches(y), PptInches(w), PptInches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = ppt_color(fill)
    shape.line.color.rgb = ppt_color(line)
    shape.line.width = PptPt(1.1)
    return shape


def add_label(slide, x, y, w, h, label, body="", fill=ICE):
    add_panel(slide, x, y, w, h, fill=fill)
    add_textbox(slide, x + 0.12, y + 0.1, w - 0.24, 0.27, label, size=12.2, bold=True, color=NAVY)
    if body:
        add_textbox(slide, x + 0.12, y + 0.42, w - 0.24, h - 0.48, body, size=8.9, color=INK)


def add_footer(slide, text="Sources: USGS 2019; DOE/NETL; Chong et al. 2022; Lee and Collett 2011; Haines et al. 2022"):
    add_textbox(slide, 0.55, 7.18, 12.1, 0.22, text, size=7.3, color=MUTED)


def add_arrow(slide, x1, y1, x2, y2):
    line = slide.shapes.add_connector(1, PptInches(x1), PptInches(y1), PptInches(x2), PptInches(y2))
    line.line.color.rgb = ppt_color(TEAL)
    line.line.width = PptPt(2)
    return line


def add_bullet_list(slide, x, y, w, h, items, size=11.5):
    box = slide.shapes.add_textbox(PptInches(x), PptInches(y), PptInches(w), PptInches(h))
    frame = box.text_frame
    frame.clear()
    frame.margin_left = PptInches(0.08)
    for idx, item in enumerate(items):
        p = frame.paragraphs[0] if idx == 0 else frame.add_paragraph()
        p.text = item
        p.level = 0
        p.font.name = "Aptos"
        p.font.size = PptPt(size)
        p.font.color.rgb = ppt_color(INK)
    return box


def add_flow(slide, labels: list[str], x=0.8, y=2.0, box_w=1.45, box_h=0.68, gap=0.38):
    for idx, label in enumerate(labels):
        bx = x + idx * (box_w + gap)
        add_label(slide, bx, y, box_w, box_h, label, "", SAND if idx in {0, len(labels) - 1} else ICE)
        if idx < len(labels) - 1:
            add_arrow(slide, bx + box_w + 0.02, y + box_h / 2, bx + box_w + gap - 0.08, y + box_h / 2)


def add_image(slide, path: Path, x, y, w, h):
    return slide.shapes.add_picture(str(path), PptInches(x), PptInches(y), PptInches(w), PptInches(h))


def build_pptx() -> None:
    assets = build_visual_assets()
    prs = Presentation()
    prs.slide_width = PptInches(13.333)
    prs.slide_height = PptInches(7.5)
    blank = prs.slide_layouts[6]

    slide = prs.slides.add_slide(blank)
    add_title(slide, "Gas Hydrate Occurrence and Saturation Prediction", "Permafrost sediments on the Alaska North Slope using AI/ML")
    add_image(slide, assets["regional_3d"], 7.05, 1.08, 5.65, 3.35)
    photo = slide.shapes.add_shape(MSO_SHAPE.OVAL, PptInches(0.78), PptInches(1.42), PptInches(1.85), PptInches(1.85))
    photo.fill.solid()
    photo.fill.fore_color.rgb = ppt_color(GRAY)
    photo.line.color.rgb = ppt_color(TEAL)
    add_textbox(slide, 1.02, 2.1, 1.35, 0.3, "photo", size=16, bold=True, color=MUTED, align=PP_ALIGN.CENTER)
    add_label(slide, 2.95, 1.4, 3.55, 1.2, "Rohan Nanda", "Lead Geologist\nM.S. Geosciences, University of Texas at Dallas", SAND)
    add_label(slide, 0.8, 3.75, 5.7, 1.35, "Project focus", "Use approved well-log, NMR, and core-analysis data to predict gas hydrate occurrence and saturation, then communicate results as reservoir-characterization evidence.")
    add_label(slide, 7.25, 4.72, 5.2, 0.9, "Website asset embedded", "Public North Slope structural scene and well inventory generated from the project atlas.", ICE)
    add_footer(slide, "Deck structure follows project email instructions received 2026-06-09.")

    slide = prs.slides.add_slide(blank)
    add_title(slide, "Introduction: What and Why Gas Hydrates", "A potential natural-gas resource that requires reservoir-scale characterization")
    add_label(slide, 0.8, 1.28, 3.45, 1.25, "Gas hydrate", "Methane is held inside crystalline water cages in sediment pore space.", SAND)
    add_label(slide, 0.8, 2.9, 3.45, 1.25, "North Slope value", "USGS assessed a mean of about 53.8 TCF of technically recoverable gas in North Slope hydrate accumulations.")
    add_label(slide, 0.8, 4.52, 3.45, 1.25, "Characterization goal", "Translate resource potential into interval-scale occurrence, saturation, uncertainty, and sweet-spot evidence.")
    add_flow(slide, ["stability", "reservoir", "gas charge", "logs/core", "saturation"], x=4.9, y=1.35, box_w=1.34)
    add_label(slide, 4.9, 3.05, 6.85, 1.4, "Core message", "Stability is necessary but not proof. The project asks whether well logs, NMR, and core evidence jointly support hydrate occurrence and saturation.")
    add_label(slide, 4.9, 4.92, 6.85, 0.9, "Energy-security framing", "The presentation stays focused on natural-gas resource characterization, not environmental-impact discussion.", SAND)
    add_footer(slide)

    slide = prs.slides.add_slide(blank)
    add_title(slide, "Parameters: Well-Log Scaffold", "Measured curves, derived physics, QC fields, and targets stay separated")
    add_image(slide, assets["well_log"], 5.25, 1.08, 7.45, 4.65)
    for i, (label, body) in enumerate([
        ("Lithology", "GR, core lithology, clean-sand screening"),
        ("Porosity", "Density, neutron, NMR, core porosity"),
        ("Electrical", "Deep resistivity and source mnemonics"),
        ("Elastic", "Vp, Vs, Vp/Vs, impedance, moduli"),
        ("Targets", "Sgh, S_h, NMR_SAT, phase classes"),
        ("QC", "Caliper, outliers, depth match, missing curves"),
    ]):
        add_label(slide, 0.65, 1.12 + i * 0.78, 4.25, 0.62, label, body, SAND if label == "Targets" else ICE)
    add_label(slide, 5.45, 5.88, 6.9, 0.65, "Embedded website scaffold", "Synthetic well-log panel with interpretation callouts from the Future Well-Log Engine.")
    add_footer(slide, "Sources: recovered header screenshots; project Q&A update; Lee and Collett 2011; Haines et al. 2022")

    slide = prs.slides.add_slide(blank)
    add_title(slide, "ML Methodology: Architecture", "Workflow adapted from gas-hydrate ML literature and approved-data constraints")
    add_flow(slide, ["raw logs", "QC", "features", "labels", "models", "validation"], x=0.85, y=1.25, box_w=1.55)
    add_label(slide, 0.95, 2.7, 3.1, 1.35, "Data processing", "Remove outliers, select depth intervals, align logs and core, and standardize units.", SAND)
    add_label(slide, 4.35, 2.7, 3.1, 1.35, "Modeling", "Compare rules, linear baselines, tree models, and Keras/ANN saturation models.")
    add_label(slide, 7.75, 2.7, 3.1, 1.35, "Validation", "Use complete-well holdouts and compare predictions against core and interpreted measurements.")
    add_image(slide, assets["metrics"], 2.0, 4.45, 9.45, 1.65)
    add_footer(slide, "Source anchor: Chong et al. 2022; project runtime requirements map.")

    slide = prs.slides.add_slide(blank)
    add_title(slide, "ML Methodology: Why These Parameters", "Classification and regression need different evidence")
    add_image(slide, assets["sweet_spot"], 6.45, 1.15, 5.95, 3.0)
    add_label(slide, 0.8, 1.28, 5.0, 1.0, "Classification", "Predict hydrate occurrence or phase class using lithology, resistivity, elastic, NMR, and QC context.", SAND)
    add_label(slide, 0.8, 2.62, 5.0, 1.0, "Regression", "Predict continuous hydrate saturation from calibrated logs, NMR-derived or core-calibrated targets, and physics features.")
    add_label(slide, 0.8, 3.96, 5.0, 1.0, "Linear vs nonlinear", "Linear baselines show traceable relationships; nonlinear models test interactions among reservoir, electrical, elastic, and NMR evidence.")
    add_label(slide, 6.65, 4.62, 5.55, 0.92, "Website ranking logic", "The sweet-spot ranking is an explainable scaffold, not a final result until approved data are run.", ICE)
    add_footer(slide)

    slide = prs.slides.add_slide(blank)
    add_title(slide, "Geomechanical Feature Sketch", "Rock-physics parameters help evaluate hydrate-consistent stiffness")
    add_panel(slide, 0.8, 1.1, 11.75, 4.55, fill=WHITE, line=TEAL, radius=False)
    add_textbox(slide, 1.1, 1.35, 4.15, 0.35, "Inputs from the well-log scaffold", 16, True, NAVY)
    add_textbox(slide, 1.1, 1.88, 3.9, 1.0, "rho, Vp, Vs, GR, porosity, NMR", 20, True, TEAL, PP_ALIGN.CENTER)
    add_textbox(slide, 5.1, 1.35, 3.8, 0.35, "Derived rock-physics terms", 16, True, NAVY)
    add_textbox(slide, 5.1, 1.9, 3.8, 1.95, "YM = f(rho, Vp, Vs)\nPR = f(Vp, Vs)\nMR = (Vs * rho)^2\nLR = (Vp * rho)^2 - 2(Vs * rho)^2", 17, True, INK, PP_ALIGN.CENTER)
    add_textbox(slide, 9.15, 1.35, 2.95, 0.35, "Interpretation use", 16, True, NAVY)
    add_textbox(slide, 9.15, 1.92, 2.9, 1.35, "Compare hydrate, gas, water, shale, ice, and stress effects.", 15, True, TEAL, PP_ALIGN.CENTER)
    add_arrow(slide, 4.65, 2.55, 5.0, 2.55)
    add_arrow(slide, 8.95, 2.55, 9.1, 2.55)
    add_label(slide, 1.1, 4.35, 10.85, 0.82, "Purpose", "Integrate mechanical behavior with log response so high resistivity or high velocity is not treated as a hydrate label by itself.", SAND)
    add_footer(slide, "Source anchor: project geomechanics screenshots and local equation-map documents.")

    slide = prs.slides.add_slide(blank)
    add_title(slide, "3D Map and Well Context", "Regional context constrains interpretation but does not replace log evidence")
    add_image(slide, assets["regional_3d"], 0.75, 1.05, 7.35, 4.7)
    add_label(slide, 8.45, 1.35, 3.75, 1.2, "Map use", "Show well positions, structural context, data coverage, and candidate intervals.", SAND)
    add_label(slide, 8.45, 3.05, 3.75, 1.2, "Boundary", "Public deck can show synthetic/public context; approved well identifiers and results stay in the authorized runtime.")
    add_label(slide, 8.45, 4.75, 3.75, 0.8, "OpenScienceLab step", "Ready to replace this with approved-environment map output when you push/run there.", ICE)
    add_footer(slide, "Source anchor: project GIS atlas and future approved-runtime outputs.")

    slide = prs.slides.add_slide(blank)
    add_title(slide, "Results and Discussion Plan", "Website placeholders now show what approved-data outputs will replace")
    add_image(slide, assets["metrics"], 0.78, 1.05, 5.85, 2.8)
    add_image(slide, assets["sweet_spot"], 6.9, 1.05, 5.45, 2.8)
    add_label(slide, 0.9, 4.35, 3.5, 1.0, "Expected figures", "Well-log panel, saturation plot, confusion matrix, calibration plot.", SAND)
    add_label(slide, 4.85, 4.35, 3.5, 1.0, "Discussion", "Explain model behavior, false positives, uncertain intervals, and geologic controls.")
    add_label(slide, 8.8, 4.35, 3.5, 1.0, "Outputs", "Occurrence class, saturation estimate, uncertainty, sweet-spot rank, review flags.")
    add_footer(slide)

    slide = prs.slides.add_slide(blank)
    add_title(slide, "Conclusion", "Final project message")
    add_label(slide, 0.95, 1.35, 3.2, 1.45, "Scientific value", "Hydrate occurrence, saturation, reservoir quality, and producibility are separated.")
    add_label(slide, 4.6, 1.35, 3.2, 1.45, "ML value", "Models are trained on physics-backed features and tested by complete well.")
    add_label(slide, 8.25, 1.35, 3.2, 1.45, "Energy value", "Characterization supports future natural-gas resource evaluation and energy security.")
    add_textbox(slide, 1.2, 4.25, 10.7, 0.7, "The goal is a defensible, explainable workflow for predicting gas hydrate occurrence and saturation from approved North Slope well-log and core data.", 20, True, NAVY, PP_ALIGN.CENTER)
    add_footer(slide)

    prs.save(PPTX_OUT)


def main() -> None:
    build_docx()
    build_pptx()
    print(DOCX_OUT)
    print(PPTX_OUT)


if __name__ == "__main__":
    main()
