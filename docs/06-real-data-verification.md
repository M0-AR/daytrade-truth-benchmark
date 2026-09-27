# 06 — Real-Data Verification (live market data, Sep 2026)

Tested on **real Yahoo Finance daily OHLCV 2024-01-02 → 2026-09-25 (686 bars)** via `yfinance`
with 4s pacing + disk cache in `data/*_daily.csv`. No API key. All numbers below are
re-runnable: `python -m dtb.benchmark_real --out results/real_benchmark.json`.

## 1. What broke vs assumptions (fixed)

| Assumption (v0.1) | Live test result Sep 2026 | Fix |
|---|---|---|
| Stooq curl with UA works | **FALSE.** `stooq.com/q/d/l/` returns JS `__verify` SHA-256 PoW wall (openresty). Needs CAPTCHA API key since early 2026 + quota. | Loader uses `yfinance`; Stooq documented as bulk-ZIP fallback only |
| Yahoo raw curl works | **PARTLY FALSE.** `query1` instant 429; `query2` worked once then 429 on 3 rapid hits; 5/10/15s backoff still 429 (IP-throttled). | `yfinance` (cookie/crumb) + 4s pacing succeeds; raw curl removed |
| `datetime.utcnow()` fine | DeprecationWarning | `now(timezone.utc)` (fixed) |
| Monte-Carlo terminal $$$ is the story | Misleading compounding (25k→736k median). Hides CAGR/DD/costs. | Report expectancy_R + ruin + streak; real bench adds cost arms |
| Scanner RVOL naive is enough | Time-of-day naive overstates morning RVOL; misses float rotation | Docs + `rotation` + spread gate; intraday confirmation required |
| Guardrails complete | Missing SSR/LULD/IML | `check_halts_ssr_iml()` added + tested |

## 2. Real-data audit (Yahoo, survivors-only UPPER BOUND)

| Symbol | bars | +10% days | -10% days | maxRVOL | maxChg |
|---|---|---|---|---|---|
| SPY | 686 | 1 | 0 | 3.0 | +10.5% |
| QQQ | 686 | 1 | 0 | 3.0 | +12.0% |
| AAPL | 686 | 1 | 0 | 5.2 | +15.3% |
| NVDA | 686 | 3 | 2 | 3.5 | +18.7% |
| TSLA | 686 | 7 | 6 | 2.7 | +22.7% |
| PLTR | 686 | 10 | 8 | 6.3 | +30.8% |
| GME | 686 | 17 | 17 | 8.6 | +74.4% |
| AMC | 686 | 19 | 12 | 10.9 | +78.4% |

**Reading:** Cameron filter (+10%, RVOL≥2, $2-20, news, low float) almost never fires on
SPY/QQQ/AAPL (1/686). Pond is meme/small-cap (GME/AMC/PLTR). This matches Amihud
illiquidity + Barber retail-crowding (same-day pop → multi-day reversal). Large-cap
momentum needs different thresholds (practitioner $10-50 core).

## 3. Naive Gap+Go proxy (Open→Close on ≥+5% gaps, NO intraday stops)

Live result 2026-09-27 (`results/real_benchmark.json` hash `900e12dab9e280d7`):

| Symbol | n_gap5 | win% gross | avg gross | net@30bps | SSR days | halt-risk (range≥20%) |
|---|---|---|---|---|---|---|
| SPY | 0 | — | — | — | 0 | 0 |
| QQQ | 0 | — | — | — | 0 | 0 |
| AAPL | 3 | 0.0% | -2.02% | -2.32% | 0 | 0 |
| NVDA | 8 | 50.0% | -0.82% | -1.12% | 2 | 0 |
| TSLA | 13 | 38.5% | -0.75% | -1.05% | 6 | 1 |
| GME | 9 | 22.2% | -6.32% | -6.62% | 17 | 14 |
| AMC | 10 | 60.0% | +2.19% | +1.89% | 12 | 10 |
| PLTR | 15 | 60.0% | +0.69% | +0.39% | 8 | 2 |

Expected shape (verified pattern): gross near 0 to slightly negative on large caps,
positive-but-fragile on meme names, collapsing at 30-50bps. This is the **gross-vs-net**
thesis (clawRxiv <$480M erased; QuanterLab small 20-50bps, micro 50-200bps).
Daily proxy OVERSTATES (no stop-outs, no spread widening on halt days) — hence UPPER BOUND.

## 4. Data-quality caveats (must cite in PhD)

- Yahoo: adjClose 2dp rounding, missing dividends/splits, delists absent, restated
  fundamentals, 1m only 7-60d recent, delayed ~15m. Alphanume: “fine to learn, poor to risk.”
- Survivorship: discount 1-3pp/yr retail; Shumway missing DLRET ≈ -30% for performance delists;
  Class I +17pp if violated (MDPI 2026). Our universe has zero dead tickers by construction.
- Free intraday: HF Library 1-min 1391 tickers CC-BY but IEX-only post-Mar-2022 (2-3% vol);
  Alpaca free = IEX + 15m SIP delay, 200/min; Plus $99 SIP.
- Costs: stress 5/15/30/50/100bps every run. Edge < 2× round-trip cost = unlikely to survive.

## 5. How to reproduce / extend

```bash
pip install -r requirements.txt
pytest -q  # incl. tests/test_real.py (SPY≤2, GME/AMC≥10 +10% days)
python -m dtb.benchmark_real --out results/real_benchmark.json
docker compose up --build benchmark
```

Next for paper: add Norgate/CRSP PIT + delist returns, 1-min confirmation of exits,
news timestamps, purge/embargo WFA, DSR/PBO with full trial registry.
