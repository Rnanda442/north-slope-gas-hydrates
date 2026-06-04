from __future__ import annotations

from io import StringIO

import pandas as pd
import plotly.graph_objects as go


def csv_bytes(frame: pd.DataFrame) -> bytes:
    buffer = StringIO()
    frame.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")


def figure_html_bytes(figure: go.Figure) -> bytes:
    return figure.to_html(include_plotlyjs="cdn", full_html=True).encode("utf-8")
