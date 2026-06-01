"""
Central configuration — all parameters live here, nowhere else.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Trading pair
# ---------------------------------------------------------------------------
SYMBOL: str = "BTC/USDT"
TIMEFRAME_DAILY: str = "1d"

# ---------------------------------------------------------------------------
# SMA filter
# ---------------------------------------------------------------------------
SMA_PERIOD: int = 120                   # days
SMA_BUFFER_PCT: float = 0.01            # +/-1 % threshold for entry/exit confirmation

CONFIRMATION_CANDLES_ENTRY: int = 2     # min consecutive daily closes ABOVE SMA to go long
CONFIRMATION_CANDLES_EXIT: int = 2      # min consecutive daily closes BELOW SMA to exit

# ---------------------------------------------------------------------------
# Dynamic stop-loss  (recalculated daily)
# ---------------------------------------------------------------------------
STOP_LOSS_SMA_FACTOR: float = 0.99     # stop_loss_price = SMA_120 * 0.99

# ---------------------------------------------------------------------------
# Grid parameters
# ---------------------------------------------------------------------------
GRID_SPACING_PCT: float = 0.003         # 0.3 % distance between grid levels
MAX_GRID_COUNT: int = 200               # hard cap on active orders

# LOWER_PRICE = SMA_120 * STOP_LOSS_SMA_FACTOR  (set once at bot start)
# UPPER_PRICE = current_price * UPPER_PRICE_MULTIPLIER  (theoretical ceiling)
UPPER_PRICE_MULTIPLIER: float = 10.0

# ---------------------------------------------------------------------------
# Capital & risk
# ---------------------------------------------------------------------------
CAPITAL_INVESTED: float = 0.80          # 80 % of allocated capital deployed
CAPITAL_RESERVE: float = 0.20           # 20 % kept as margin buffer
MAX_LEVERAGE: int = 3                   # hard ceiling — never exceeded

# ---------------------------------------------------------------------------
# Data fetching
# ---------------------------------------------------------------------------
OHLCV_LIMIT: int = 500                  # candles to fetch per request
DATA_CACHE_FILE: str = "data/btc_ohlcv.csv"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_LEVEL: str = "INFO"
LOG_FILE: str = "logs/bot.log"
