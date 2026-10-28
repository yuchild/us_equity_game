"""Historical OHLCV retrieval and game-window selection."""
from __future__ import annotations

import pandas as pd
import streamlit as st
import yfinance as yf

INTERVAL_PERIODS = {
    "1m": "5d", "5m": "1mo", "15m": "1mo", "1h": "6mo",
    "1d": "5y", "1wk": "10y", "1mo": "max",
}
VISIBLE_CANDLES = 60
RESERVED_CANDLES = 30


@st.cache_data(ttl=900, show_spinner=False)
def load_history(ticker: str, interval: str) -> pd.DataFrame:
    """Return normalized historical OHLCV candles, oldest first."""
    symbol = ticker.strip().upper()
    if not symbol or interval not in INTERVAL_PERIODS:
        raise ValueError("Enter a ticker and choose a supported interval.")

    history = yf.download(
        tickers=symbol,
        period=INTERVAL_PERIODS[interval],
        interval=interval,
        auto_adjust=True,
        progress=False,
        threads=False,
    )
    if history.empty:
        raise ValueError(f"No historical data returned for {symbol} ({interval}).")

    # Recent yfinance versions may return a two-level column index.
    if isinstance(history.columns, pd.MultiIndex):
        history.columns = history.columns.get_level_values(0)

    required = ["Open", "High", "Low", "Close"]
    if not set(required).issubset(history.columns):
        raise ValueError("Yahoo Finance did not return complete OHLC data.")

    history = history.dropna(subset=required).sort_index()
    history = history.loc[~history.index.duplicated(keep="last")]
    if history.empty:
        raise ValueError("No usable candles were returned.")
    return history


def choose_start(history: pd.DataFrame, visible: int = VISIBLE_CANDLES,
                 reserve: int = RESERVED_CANDLES) -> int:
    """Choose a random end-exclusive window, reserving future candles."""
    import secrets

    if len(history) < visible + 1:
        raise ValueError(f"Only {len(history)} candles available; at least {visible + 1} required to play.")
    available_reserve = min(reserve, len(history) - visible)
    # End-exclusive index for the initial displayed window.
    maximum_end = len(history) - available_reserve
    return visible + secrets.randbelow(maximum_end - visible + 1)
