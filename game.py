"""Pure game calculations; no Streamlit dependency."""
from dataclasses import dataclass

STARTING_BANKROLL = 10000.0

@dataclass(frozen=True)
class Result:
    entry: float
    exit: float
    direction: str
    wager: float
    candles: int
    price_return: float
    profit: float


def settle(entry: float, exit: float, direction: str, wager: float, candles: int) -> Result:
    if entry <= 0 or exit <= 0:
        raise ValueError("Prices must be positive.")
    if direction not in ("Up", "Down") or candles not in (1, 3, 5):
        raise ValueError("Invalid direction or candle count.")
    if wager <= 0:
        raise ValueError("Wager must be positive.")
    change = exit / entry - 1
    profit = wager * change * (1 if direction == "Up" else -1)
    return Result(entry, exit, direction, wager, candles, change, profit)
