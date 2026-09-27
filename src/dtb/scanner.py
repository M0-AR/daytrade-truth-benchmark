"""Gap / momentum scanner — Cameron #1 + 2026 practitioner consensus.

Filters (ALL must pass for A+):
 float <= 20M (allow to 50M with WARN), price $2-$20,
 day change >= +10%, RVOL >= 2.0, news==True.
 RVOL = today_vol / avg30_vol (time-of-day naive; intraday use time-adjusted).
 Float rotation = cumvol / float_shares (DayTradingToolkit 2026-05-13).
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Candle:
    symbol: str
    price: float
    prev_close: float
    today_vol: int
    avg30_vol: int
    float_shares: int
    has_news: bool
    spread_cents: float = 5.0


def pct_change(c: Candle) -> float:
    return (c.price - c.prev_close) / c.prev_close if c.prev_close else 0


def rvol(c: Candle) -> float:
    return c.today_vol / c.avg30_vol if c.avg30_vol else 0


def float_rotation(c: Candle) -> float:
    return c.today_vol / c.float_shares if c.float_shares else 0


def grade(c: Candle) -> dict:
    chg = pct_change(c)
    rv = rvol(c)
    rot = float_rotation(c)
    float_m = c.float_shares / 1e6
    checks = {
        "chg>=10%": chg >= 0.10,
        "rvol>=2": rv >= 2.0,
        "price 2-20": 2.0 <= c.price <= 20.0,
        "news": c.has_news,
        "float<=20M": float_m <= 20,
        "float<=50M": float_m <= 50,
        "spread_ok": c.spread_cents <= 15,
        "rotation>=1": rot >= 1.0,
    }
    a_plus = all([checks["chg>=10%"], checks["rvol>=2"], checks["price 2-20"],
                  checks["news"], checks["float<=50M"]])
    grade_s = "A+" if (a_plus and checks["float<=20M"]) else ("B" if a_plus else "SKIP")
    return {"symbol": c.symbol, "chg": round(chg, 4), "rvol": round(rv, 2),
            "floatM": round(float_m, 2), "rotation": round(rot, 3),
            "spread_c": c.spread_cents, "checks": checks, "grade": grade_s}


def scan(candles: list[Candle]) -> list[dict]:
    ranked = sorted([grade(c) for c in candles],
                    key=lambda g: (g["grade"] != "A+", -g["rvol"], -g["chg"]))
    return ranked
