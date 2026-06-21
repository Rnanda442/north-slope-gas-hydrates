from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def build_log_panel(logs: pd.DataFrame, well_alias: str, columns: tuple[str, ...]) -> go.Figure:
    well = logs[logs["well_alias"] == well_alias]
    figure = make_subplots(rows=1, cols=len(columns), shared_yaxes=True, horizontal_spacing=0.035)
    for index, column in enumerate(columns, start=1):
        figure.add_trace(go.Scatter(x=well[column], y=well["depth_m"], mode="lines", name=column), row=1, col=index)
        figure.update_xaxes(title_text=column, row=1, col=index)
    figure.update_yaxes(title_text="Depth (m)", autorange="reversed", row=1, col=1)
    figure.update_layout(title=f"{well_alias} runtime well-log panel", height=650, showlegend=False)
    return figure

def build_core_log_crossplot(matches: pd.DataFrame, core_column: str, log_column: str) -> go.Figure:
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=matches[core_column],
            y=matches[log_column],
            mode="markers",
            text=matches["well_alias"],
            name="core-log matches",
        )
    )
    figure.update_layout(
        title=f"Core-log calibration: {core_column} vs {log_column}",
        xaxis_title=core_column,
        yaxis_title=log_column,
        height=430,
    )
    return figure
