"""Anonymous candlestick chart: no price or date labels."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go


def make_chart(candles: pd.DataFrame) -> go.Figure:
    # Integer positions conceal the underlying dates and market sessions.
    positions = list(range(len(candles)))
    figure = go.Figure(go.Candlestick(
        x=positions,
        open=candles["Open"],
        high=candles["High"],
        low=candles["Low"],
        close=candles["Close"],
        increasing_line_color="#22c55e",
        increasing_fillcolor="#22c55e",
        decreasing_line_color="#ef4444",
        decreasing_fillcolor="#ef4444",
        hoverinfo="skip",
        name="",
    ))
    figure.update_layout(
        template="plotly_dark",
        paper_bgcolor="#000000",
        plot_bgcolor="#000000",
        height=520,
        margin=dict(l=8, r=8, t=12, b=8),
        showlegend=False,
        hovermode=False,
        dragmode=False,
        xaxis=dict(visible=False, fixedrange=True, rangeslider=dict(visible=False)),
        yaxis=dict(visible=False, fixedrange=True),
    )
    return figure
