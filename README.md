# US Equity Game — Step 3

A Streamlit historical candlestick prediction game, for educational use only.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Test

```bash
python -m unittest test_game.py
```

## Rules

- Begin with $1,000, no real money involved.
- The chart shows 60 candles, with dates and price labels hidden.
- Choose Up or Down, wager no more than your current bankroll, and reveal 1, 3, or 5 candles.
- Profit = wager × (exit close / entry close − 1), multiplied by +1 for Up or −1 for Down.
- Wagers are independent long/short exposures; no leverage, fees, spreads, or interest are modeled.
- The chart rolls forward 1/3/5 candles after each round.
- End Game freezes the score; Reset starts a fresh random game with NVDA/5m and $1,000.
- Yahoo Finance data availability varies. Only completed historical candles are used where available; data are not guaranteed accurate.

## Future enhancements

Ticker autocomplete, explicit new-game controls, improved market-session handling, additional scoring rules, deployment.

## Step 4 additions
- Sidebar contains stock, interval, wager, direction, reveal, end, and reset controls.
- Volume bars share the candlestick x-axis and use the same green/red direction colors.
- Dates, prices, volume scale, and hover remain hidden until **End game**.
- End game reveals the axes and price hover details; Reset game returns to NVDA/5m.
