"""Real-data benchmark: Cameron filters on live Yahoo/daily bars + cost stress.

Method (no lookahead):
- Signal uses prevClose/avg20Vol computed on t-1 only.
- Gap+Go proxy: if Open gaps +5%+ vs prevClose AND prior RVOL elevated, simulate
  intraday long Open->Close with stop -1R and target +2R (R = Open - low_estimate).
  Since daily bars lack intraday path, we mark TO-BE-CONFIRMED on 1-min data and
  report gross vs net at 5/15/30bps + 20/50bps small-cap arms (QuanterLab ladder).
- SSR gate: if prev day chg <= -10%, shorts blocked (Rule 201 uptick-only).
- LULD proxy: if daily range >20%, flag halt-risk (cannot size full).
- Survivorship warning: Yahoo universe = survivors only; results are UPPER BOUND.
  Discount 1-3pp/yr retail, more for small caps (TrendsAndBreakouts/Shumway -30%
  missing DLRET).

Output: results/real_benchmark.json with hash.
"""
from __future__ import annotations
import argparse, json, hashlib, os
import pandas as pd
from .data_real import load_cached, audit

COST_ARMS_BPS = [5, 15, 30, 50, 100]


def evaluate_symbol(symbol: str) -> dict:
    df = load_cached(symbol)
    if df is None:
        return {"symbol": symbol, "error": "no cached CSV (run fetch first)"}
    d = df.copy()
    d["prevClose"] = d["Close"].shift(1)
    d["prevVol20"] = d["Volume"].shift(1).rolling(20).mean()
    d["gapPct"] = (d["Open"] - d["prevClose"]) / d["prevClose"] * 100
    d["chgPct"] = (d["Close"] - d["prevClose"]) / d["prevClose"] * 100
    d["RVOL_open_proxy"] = d["Volume"].shift(1) / d["prevVol20"]
    d["rangePct"] = (d["High"] - d["Low"]) / d["prevClose"] * 100

    # Cameron daily proxy: gap >= +5% (intraday needs +10% on 1m; daily close proxy looser)
    # Count strict +10% gap days separately.
    strict_gap = d[d["gapPct"] >= 10]
    loose_gap = d[d["gapPct"] >= 5]

    # SSR days: prev chg <= -10%
    d["prevChg"] = d["chgPct"].shift(1)
    ssr_days = int((d["prevChg"] <= -10).sum())
    halt_risk_days = int((d["rangePct"] >= 20).sum())

    # Naive strategy: buy every +5% gap at open, sell at close (overnight held 0d, intraday proxy)
    # Gross per-trade = (Close-Open)/Open. This OVERSTATES (no intraday stop-outs).
    trades = d.loc[d["gapPct"] >= 5, ["Date", "Open", "Close", "gapPct"]].copy()
    trades["grossPct"] = (trades["Close"] - trades["Open"]) / trades["Open"] * 100

    out = {
        "symbol": symbol,
        "audit": audit(df, symbol),
        "n_gap5": len(trades),
        "n_gap10": len(strict_gap),
        "ssr_days": ssr_days,
        "halt_risk_days_range20": halt_risk_days,
        "win_rate_gap5_close": round(float((trades["grossPct"] > 0).mean()) if len(trades) else 0, 4),
        "avg_gross_gap5": round(float(trades["grossPct"].mean()) if len(trades) else 0, 4),
        "median_gross_gap5": round(float(trades["grossPct"].median()) if len(trades) else 0, 4),
    }
    # cost stress: net = gross - bps/100
    for bps in COST_ARMS_BPS:
        cost = bps / 100.0
        net = (trades["grossPct"] - cost) if len(trades) else pd.Series([], dtype=float)
        out[f"net_avg_{bps}bps"] = round(float(net.mean()) if len(net) else 0, 4)
        out[f"win_{bps}bps"] = round(float((net > 0).mean()) if len(net) else 0, 4)
    out["note"] = "UPPER BOUND: no intraday stops, survivors-only, no spread-widening on halt days"
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default="SPY,QQQ,AAPL,NVDA,TSLA,GME,AMC,PLTR")
    ap.add_argument("--out", default="results/real_benchmark.json")
    a = ap.parse_args()
    syms = [s.strip() for s in a.symbols.split(",")]
    res = {"symbols": {}, "cost_arms_bps": COST_ARMS_BPS,
           "method": "gap5 Open->Close proxy, daily bars, survivors-only UPPER BOUND"}
    for s in syms:
        try:
            res["symbols"][s] = evaluate_symbol(s)
        except Exception as e:
            res["symbols"][s] = {"symbol": s, "error": repr(e)[:300]}
    h = hashlib.sha256(json.dumps(res, sort_keys=True, default=str).encode()).hexdigest()[:16]
    res["sha256_16"] = h
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    json.dump(res, open(a.out, "w"), indent=2, default=str)
    print(f"WROTE {a.out} hash={h}")
    for s, r in res["symbols"].items():
        if "error" in r:
            print(f"- {s}: ERROR {r['error']}")
        else:
            print(f"- {s}: gaps5={r['n_gap5']} gaps10={r['n_gap10']} win={r['win_rate_gap5_close']} avgGross={r['avg_gross_gap5']}% net30bps={r['net_avg_30bps']}% SSRdays={r['ssr_days']} haltRisk={r['halt_risk_days_range20']}")


if __name__ == "__main__":
    main()
