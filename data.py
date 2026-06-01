"""
Fetches and caches daily BTC/USDT OHLCV data (UTC close) via ccxt.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

import ccxt
import pandas as pd

import config

logger = logging.getLogger(__name__)


def _make_exchange() -> ccxt.Exchange:
    """Return an unauthenticated exchange instance for public market data."""
    exchange = ccxt.binance({"enableRateLimit": True})
    return exchange


def fetch_ohlcv(
    symbol: str = config.SYMBOL,
    timeframe: str = config.TIMEFRAME_DAILY,
    limit: int = config.OHLCV_LIMIT,
    retries: int = 3,
    retry_delay: float = 2.0,
) -> pd.DataFrame:
    """
    Fetch daily OHLCV candles from the exchange.

    Returns a DataFrame with columns:
        timestamp (UTC, datetime64), open, high, low, close, volume
    Indexed by timestamp.
    """
    exchange = _make_exchange()

    for attempt in range(1, retries + 1):
        try:
            logger.info("Fetching %d %s candles for %s (attempt %d)", limit, timeframe, symbol, attempt)
            raw: list[list] = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            break
        except (ccxt.NetworkError, ccxt.ExchangeError) as exc:
            logger.warning("Fetch attempt %d failed: %s", attempt, exc)
            if attempt == retries:
                raise
            time.sleep(retry_delay)

    df = pd.DataFrame(raw, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    df.set_index("timestamp", inplace=True)
    df = df.astype(float)

    logger.info("Fetched %d candles; latest close: %s @ %.2f", len(df), df.index[-1], df["close"].iloc[-1])
    return df


def load_ohlcv(
    cache_path: str = config.DATA_CACHE_FILE,
    refresh: bool = False,
) -> pd.DataFrame:
    """
    Return OHLCV data, using a local CSV cache when available.

    Args:
        cache_path: Path to the CSV cache file.
        refresh:    Force a live fetch even if the cache exists.
    """
    path = Path(cache_path)

    if path.exists() and not refresh:
        logger.info("Loading OHLCV from cache: %s", path)
        df = pd.read_csv(path, index_col="timestamp", parse_dates=True)
        df.index = pd.DatetimeIndex(df.index, tz="UTC")
        return df

    path.parent.mkdir(parents=True, exist_ok=True)
    df = fetch_ohlcv()
    df.to_csv(path)
    logger.info("OHLCV cached to %s", path)
    return df
