from streamlit.testing.v1 import AppTest

from dashboard.well_log_engine import (
    generate_synthetic_logs,
    screen_intervals,
    sweet_spot_review_table,
)


def test_sweet_spot_review_table_is_ranked_and_explainable() -> None:
    intervals = screen_intervals(generate_synthetic_logs())
    ranked = sweet_spot_review_table(intervals)

    assert ranked["Synthetic review priority"].is_monotonic_decreasing
    assert "Evidence domains passed" in ranked
    assert "Blocking domains" in ranked
    assert ranked["Synthetic review priority"].between(0, 1).all()


def test_sweet_spot_page_renders() -> None:
    app = AppTest.from_file("streamlit_app.py", default_timeout=30)
    app.query_params["page"] = "North Slope Sweet Spots"
    app.run(timeout=30)

    assert not app.exception
    assert app.title[0].value == "North Slope Gas-Hydrate Sweet Spots"
    assert [metric.label for metric in app.metric[:4]] == [
        "Synthetic intervals",
        "Review-lane candidates",
        "Hydrate-supportive",
        "Good sand, no hydrate",
    ]
    assert len(app.dataframe) >= 1
