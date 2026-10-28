"""US Equity Game — Step 2: historical data and anonymous chart."""
import streamlit as st

from charts.candlestick import make_chart
from data.market_data import load_history, choose_start, VISIBLE_CANDLES

st.set_page_config(page_title="US Equity Game", page_icon="📈", layout="wide")
st.title("📈 US Equity Game")
st.caption("Predict price movements without seeing dates or price labels.")

left, right = st.columns(2)
with left:
    ticker = st.text_input("Stock symbol", value="NVDA").strip().upper()
with right:
    interval = st.selectbox("Candlestick interval", ["1m", "5m", "15m", "1h", "1d", "1wk", "1mo"], index=1)

if not ticker:
    st.info("Enter a stock symbol to load a chart.")
    st.stop()

selection = (ticker, interval)
if st.session_state.get("selection") != selection:
    st.session_state.selection = selection
    st.session_state.pop("window_end", None)

try:
    with st.spinner("Loading historical candles..."):
        history = load_history(ticker, interval)
    if len(history) < VISIBLE_CANDLES + 1:
        st.warning(f"Only {len(history)} candles are available for {ticker} at {interval}. At least {VISIBLE_CANDLES + 1} are required for a playable chart. Try another interval or ticker.")
        st.stop()
    if "window_end" not in st.session_state:
        st.session_state.window_end = choose_start(history)
except Exception as exc:
    st.error(f"Unable to load market data: {exc}")
    st.stop()

st.subheader(f"{ticker} · {interval} · {VISIBLE_CANDLES} candles")
window_end = st.session_state.window_end
window = history.iloc[window_end - VISIBLE_CANDLES:window_end]
st.plotly_chart(make_chart(window), use_container_width=True, config={"displayModeBar": False, "scrollZoom": False})

if st.button("New random chart"):
    st.session_state.window_end = choose_start(history)
    st.rerun()

st.divider()
st.info("Step 2 preview: Betting and candle reveal are coming in Step 3.")
first, second, third = st.columns(3)
first.metric("Starting Bankroll", "$1,000.00")
second.metric("Total P&L", "$0.00")
third.metric("Rounds Played", "0")
