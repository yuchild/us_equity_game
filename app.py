"""US Equity Game — Step 3: bankroll, wagering, and candle reveal."""
import streamlit as st

from charts.candlestick import make_chart
from data.market_data import load_history, choose_start, VISIBLE_CANDLES
from game import STARTING_BANKROLL, settle

st.set_page_config(page_title="US Equity Game", page_icon="📈", layout="wide")
st.title("📈 US Equity Game")
st.caption("Historical market prediction game · No real-money trading")


def new_game(history, selection):
    st.session_state.game_selection = selection
    st.session_state.cursor = choose_start(history)
    st.session_state.initial_cursor = st.session_state.cursor
    st.session_state.bankroll = STARTING_BANKROLL
    st.session_state.rounds = []
    st.session_state.ended = False
    st.session_state.last_result = None


if st.session_state.pop("reset_defaults", False):
    st.session_state["ticker_widget"] = "NVDA"
    st.session_state["interval_widget"] = "5m"

left, right = st.columns(2)
with left:
    ticker = st.text_input("Stock symbol", "NVDA", key="ticker_widget").strip().upper()
with right:
    interval = st.selectbox("Candlestick interval", ["1m", "5m", "15m", "1h", "1d", "1wk", "1mo"], index=1, key="interval_widget")

if not ticker:
    st.info("Enter a stock ticker to begin.")
    st.stop()

try:
    with st.spinner("Loading historical candles..."):
        history = load_history(ticker, interval)
except Exception as exc:
    st.error(f"Could not load {ticker}: {exc}")
    st.stop()

if len(history) < VISIBLE_CANDLES + 1:
    st.warning(f"{ticker} has only {len(history)} candles for {interval}; at least {VISIBLE_CANDLES + 1} are needed. Try a different interval or ticker.")
    st.stop()

selection = (ticker, interval)
if st.session_state.get("game_selection") != selection:
    new_game(history, selection)

cursor = st.session_state.cursor
# Display a rolling 60-candle window, advancing only after a wager.
window = history.iloc[cursor - VISIBLE_CANDLES:cursor]
st.subheader(f"{ticker} · {interval} · 60 candles")
st.plotly_chart(make_chart(window), use_container_width=True, config={"displayModeBar": False, "scrollZoom": False})

balance = st.session_state.bankroll
pnl = balance - STARTING_BANKROLL
m1, m2, m3 = st.columns(3)
m1.metric("Bankroll", f"${balance:,.2f}")
m2.metric("Total P&L", f"${pnl:+,.2f}")
m3.metric("Rounds Played", len(st.session_state.rounds))

if st.session_state.last_result is not None:
    result = st.session_state.last_result
    st.success(f"Last round: {result.direction} · {result.candles} candle(s) · {result.profit:+,.2f} USD ({result.price_return:+.2%} stock move)") if result.profit >= 0 else st.error(f"Last round: {result.direction} · {result.candles} candle(s) · {result.profit:+,.2f} USD ({result.price_return:+.2%} stock move)")

remaining = len(history) - cursor
if st.session_state.ended:
    st.info(f"Game ended. Final P&L: ${pnl:+,.2f} across {len(st.session_state.rounds)} rounds.")
elif balance <= 0:
    st.warning("Your bankroll is exhausted. End the game or reset.")
elif remaining == 0:
    st.info("No more historical candles are available. End the game or reset.")
else:
    st.write("### Place your next wager")
    with st.form("wager_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            direction = st.radio("Direction", ["Up", "Down"], horizontal=True)
        with c2:
            wager = st.number_input("Wager ($)", min_value=0.01, max_value=float(round(balance, 2)), value=float(min(1000.0, round(balance, 2))), step=10.0, format="%.2f")
        with c3:
            advance = st.selectbox("Reveal candles", [1, 3, 5], index=0)
        submitted = st.form_submit_button("Place wager and reveal", use_container_width=True, disabled=remaining < advance)
    if remaining < 5:
        st.caption(f"Only {remaining} future candle(s) remain. Choose a valid reveal length.")
    if submitted:
        if wager > round(balance, 2) or wager <= 0 or advance > remaining:
            st.error("Invalid wager or insufficient future candles.")
        else:
            # Entry is the most recently displayed close; exit is the last newly revealed close.
            entry = float(history.iloc[cursor - 1]["Close"])
            exit_price = float(history.iloc[cursor + advance - 1]["Close"])
            result = settle(entry, exit_price, direction, wager, advance)
            st.session_state.bankroll = max(0.0, balance + result.profit)
            st.session_state.cursor += advance
            st.session_state.rounds.append(result)
            st.session_state.last_result = result
            st.rerun()

if st.session_state.rounds:
    with st.expander("Round history"):
        rows = [{"Round": i + 1, "Direction": r.direction, "Wager ($)": round(r.wager, 2), "Candles": r.candles, "Stock move (%)": round(100 * r.price_return, 3), "P&L ($)": round(r.profit, 2)} for i, r in enumerate(st.session_state.rounds)]
        st.dataframe(rows, use_container_width=True, hide_index=True)

c1, c2 = st.columns(2)
with c1:
    if st.button("End game", disabled=st.session_state.ended, use_container_width=True):
        st.session_state.ended = True
        st.rerun()
with c2:
    if st.button("Reset game", use_container_width=True):
        # Reset all gameplay and restore the original NVDA / 5m defaults.
        for key in ("game_selection", "cursor", "initial_cursor", "bankroll", "rounds", "ended", "last_result"):
            st.session_state.pop(key, None)
        st.session_state["reset_defaults"] = True
        st.rerun()
