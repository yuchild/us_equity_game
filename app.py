import streamlit as st

st.set_page_config(
    page_title="US Equity Game",
    page_icon="📈",
    layout="wide",
)

st.title("📈 US Equity Game")
st.caption("Test your ability to predict stock price movements.")

col1, col2 = st.columns(2)

with col1:
    ticker = st.text_input(
        "Stock symbol",
        value="NVDA",
    ).strip().upper()

with col2:
    interval = st.selectbox(
        "Candlestick interval",
        options=["1m", "5m", "15m", "1h", "1d", "1wk", "1mo"],
        index=1,
    )

st.subheader("Stock Chart")
st.info("Historical candlestick chart coming in Step 2.")

st.divider()

col3, col4, col5 = st.columns(3)

with col3:
    direction = st.radio(
        "Predict direction",
        options=["Up", "Down"],
        horizontal=True,
    )

with col4:
    wager = st.number_input(
        "Wager ($)",
        min_value=1.0,
        value=1000.0,
        step=100.0,
    )

with col5:
    advance = st.selectbox(
        "Advance candles",
        options=[1, 3, 5],
        index=0,
    )

st.button(
    "Reveal Next Candles",
    disabled=True,
    use_container_width=True,
)

st.divider()

col6, col7, col8 = st.columns(3)

col6.metric("Starting Balance", "$1,000.00")
col7.metric("Total P&L", "$0.00")
col8.metric("Rounds Played", "0")

st.button("Reset Game", disabled=True)