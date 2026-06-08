from dashboard.app import architecture_content, markdown_section, markdown_table
from streamlit.testing.v1 import AppTest


def test_architecture_tracker_contains_required_sections() -> None:
    content = architecture_content()

    assert "## Workstream Activity Map" in content
    assert "## Current Priority" in content
    assert "## Near-Term Sequence" in content


def test_markdown_table_parses_workstreams() -> None:
    content = architecture_content()
    workstreams = markdown_table(markdown_section(content, "Workstream Activity Map"))

    assert not workstreams.empty
    assert list(workstreams.columns) == [
        "ID",
        "Workstream",
        "Status",
        "Immediate activity",
        "Dependency",
        "Completion signal",
    ]
    assert "W1" in workstreams["ID"].tolist()


def test_project_roadmap_page_renders() -> None:
    app = AppTest.from_file("streamlit_app.py", default_timeout=30)
    app.query_params["page"] = "Project Roadmap"
    app.run(timeout=30)

    assert not app.exception
    assert app.title[0].value == "Project Architecture & Activity Map"
    assert [(metric.label, metric.value) for metric in app.metric] == [
        ("Workstreams", "9"),
        ("In progress", "1"),
        ("Ready", "1"),
        ("Waiting / blocked", "4"),
    ]
    assert len(app.dataframe) == 3
