"""Real market data loader — verified Sep 2026.

Findings (this session, live-tested):
- Stooq CSV `stooq.com/q/d/l/` now returns JS-verification wall (openresty + __verify
  SHA-256 PoW) to plain curl Sep 2026. Prior assumption "curl works with UA" is FALSE.
  Root: Stooq requires API key via CAPTCHA as of early 2026 + per-key quota
  (api-evangelist/stooq, yfuka86 collector). Bulk ZIP at stooq.com/db/h/ still listed.
- Yahoo query1/query2 raw curl: 429 Too Many Requests on this IP within 3 rapid hits.
  Backoff 5s/10s/15s still 429 (IP-throttled). Verified fallback: `yfinance` (handles
  cookies/crumb) succeeds with 4s pacing. Single-IP hammering = classic failure mode
  (logiover 2026-07-09, Alphanume 2026-06-06).
- Yahoo caveats (must disclose in PhD): adjClose rounding to 2dp corrupts long-run
  returns; missing dividends/splits (FORD 1999, EPD double-split 2014); delists absent
  → survivorship bias +1-3pp/yr retail, +17pp Class I (MDPI 2026); intraday 1m only
  recent 7-60d; quotes delayed ~15m (Alpaca free = IEX only + 15m SIP delay).
- HF Data Library: free 1-min 1391 tickers CC-BY, but IEX-only since Mar 2022 (2-3%
  consolidated vol) + fixed snapshot universe → pre-2022 survivorship. Good for
  microstructure demo, not for low-float edge proof.
- Cost ladder (QuanterLab 2026-05-01): large 5-10bps, mid/ETF 10-20, small 20-50,
  micro 50-200+ round-trip. Always stress 5/15/30bps.

This module: yfinance with pacing + disk cache + audit. No key needed.
"""
from __future__ import annotations
import os, time, glob
import pandas as pd

CACHE = os.path.join(os.path.dirname(__file__), "../../data")
CACHE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))

EXPECTED_COLS = ["AdjClose", "Close", "High", "Low", "Open", "Volume"]


def load_cached(symbol: str) -> pd.DataFrame | None:
    p = os.path.join(CACHE, f"{symbol}_daily.csv")
    if not os.path.exists(p):
        return None
    df = pd.read_csv(p, parse_dates=["Date"])
    return df.sort_values("Date").reset_index(drop=True)


def fetch_yfinance(symbol: str, start="2024-01-01", end="2026-09-27", sleep_s=4) -> pd.DataFrame:
    """Fetch via yfinance with pacing. Raises on failure (caller backs off)."""
    import yfinance as yf
    df = yf.download(symbol, start=start, end=end, interval="1d",
                     progress=False, auto_adjust=False)
    if df is None or len(df) == 0:
        raise RuntimeError(f"{symbol}: empty yfinance result (rate-limit or delisted?)")
    # flatten MultiIndex (Price, Ticker) -> single
    if hasattr(df.columns, "levels"):
        try:
            # columns like ('Adj Close', 'SPY') etc.
            df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        except Exception:
            pass
    rename = {"Adj Close": "AdjClose", "adjclose": "AdjClose"}
    df = df.rename(columns=rename)
    df = df.reset_index()
    # ensure Date col
    if "Date" not in df.columns:
        df = df.rename(columns={df.columns[0]: "Date"})
    keep = [c for c in ["Date"] + EXPECTED_COLS if c in df.columns]
    df = df[keep]
    time.sleep(sleep_s)
    return df


def audit(df: pd.DataFrame, symbol: str) -> dict:
    d = df.copy()
    d["prevClose"] = d["Close"].shift(1)
    d["gapPct"] = (d["Open"] - d["prevClose"]) / d["prevClose"] * 100
    d["chgPct"] = (d["Close"] - d["prevClose"]) / d["prevClose"] * 100
    d["avg20Vol"] = d["Volume"].rolling(20).mean()
    d["RVOL"] = d["Volume"] / d["avg20Vol"]
    return {
        "symbol": symbol,
        "bars": len(d),
        "from": str(d["Date"].min()),
        "to": str(d["Date"].max()),
        "plus10": int((d["chgPct"] >= 10).sum()),
        "minus10": int((d["chgPct"] <= -10).sum()),
        "maxRVOL": round(float(d["RVOL"].max()), 2),
        "maxChg": round(float(d["chgPct"].max()), 2),
        "missing_vol_zero": int((d["Volume"] == 0).sum()),
        "nulls": int(d[EXPECTED_COLS].isnull().sum().sum()),
    }


def load_universe(symbols: list[str]) -> dict[str, pd.DataFrame]:
    out = {}
    for s in symbols:
        df = load_cached(s)
        if df is None:
            df = fetch_yfinance(s)
            os.makedirs(CACHE, exist_ok=True)
            df.to_csv(os.path.join(CACHE, f"{s}_daily.csv"), index=False)
        out[s] = df
    return out
