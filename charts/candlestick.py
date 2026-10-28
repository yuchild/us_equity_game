"""Price and aligned volume chart, with optional end-game axis reveal."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def make_chart(candles: pd.DataFrame, reveal: bool = False) -> go.Figure:
    positions = list(range(len(candles)))
    up = candles['Close'] >= candles['Open']
    colors = ['#22c55e' if rising else '#ef4444' for rising in up]
    figure = make_subplots(rows=2, cols=1, shared_xaxes=True,
                           row_heights=[0.79, 0.21], vertical_spacing=0.025)
    figure.add_trace(go.Candlestick(
        x=positions, open=candles['Open'], high=candles['High'],
        low=candles['Low'], close=candles['Close'],
        increasing_line_color='#22c55e', increasing_fillcolor='#22c55e',
        decreasing_line_color='#ef4444', decreasing_fillcolor='#ef4444',
        hoverinfo='skip' if not reveal else 'all', name='Price',
    ), row=1, col=1)
    volume = candles['Volume'] if 'Volume' in candles else pd.Series(0, index=candles.index)
    figure.add_trace(go.Bar(
        x=positions, y=volume, marker_color=colors, name='Volume',
        hoverinfo='skip' if not reveal else 'y',
    ), row=2, col=1)
    figure.update_layout(
        template='plotly_dark', paper_bgcolor='#000000', plot_bgcolor='#000000',
        height=850, margin=dict(l=12, r=20, t=16, b=28),
        showlegend=False, hovermode='x' if reveal else False,
        dragmode=False, bargap=0.12,
    )
    labels = [pd.Timestamp(ts).strftime('%Y-%m-%d %H:%M') for ts in candles.index]
    tick_positions = list(range(0, len(positions), max(1, len(positions)//6)))
    figure.update_xaxes(visible=reveal, fixedrange=True, rangeslider_visible=False,
                        tickmode='array', tickvals=tick_positions,
                        ticktext=[labels[i] for i in tick_positions], tickangle=-25,
                        row=2, col=1)
    figure.update_xaxes(visible=False, fixedrange=True, rangeslider_visible=False,
                        row=1, col=1)
    figure.update_yaxes(visible=reveal, fixedrange=True, title_text='Price (USD)' if reveal else None,
                        row=1, col=1)
    figure.update_yaxes(visible=reveal, fixedrange=True, title_text='Volume' if reveal else None,
                        row=2, col=1)
    if reveal:
        figure.update_traces(selector=dict(type='candlestick'),
                             customdata=labels,
                             hovertemplate=None)
        figure.update_layout(hovermode='closest')
    return figure
