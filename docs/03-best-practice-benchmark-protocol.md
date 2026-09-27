# 03 — Best-Practice Benchmark Protocol (for PhD audit)

Adopted from: Arbi 2019 reproducible backtester, Lopez de Prado AFML Ch7/12 (CPCV/DSR/PBO), Harvey et al. multiple-testing, QuantJourney-BT, Keystone, WenhuangL PIT framework, Concretum 2026 intraday momentum.

## 1. Research contract (write BEFORE touching data)
- Hypothesis, universe, holding (intraday only, no overnight), costs, success gate (e.g. net Sharpe>0 after 30/50bps + DSR>0.95), kill log location.

## 2. Data hygiene
- Point-in-time universe (no current S&P/Nasdaq roster backfilled). Include delists (LEH -78%, GM -96%).
- Corporate actions adjusted with as-filed revision dates, not retroactive.
- Minute bars + daily float + news timestamps; record feed (SIP vs IEX) + delay (15-min suffices only if strategy uses it).

## 3. No-lookahead gates
- shift() audit: signal at t uses ≤t-1. RVOL at 10am uses volume-to-10am, NOT full-day.
- Stop/exit sequencing: no vectorized stop that peeks intrabar high/low.
- Universe-membership, price-forward, stop-sequencing = filtration breaches (MDPI 2026 taxonomy).

## 4. Execution realism (this repo stresses 3 arms)
- Base: spread from TAQ/Corwin-Schultz + commission + 5c slippage.
- Adverse: 30bps + 50bps one-way (Keystone/WenhuangL standard).
- Capacity: ≤1% ADV, Almgren-Chriss impact; D1 low-liq ceiling ~$300k (Palmason).
- No perfect fills; partials/rejects in fast markets; SSR/LULD halts respected.

## 5. Validation (no single backtest passes)
- In-sample plateau (not peak) → purged walk-forward with embargo → locked OOS touched ONCE.
- Trial registry counts EVERY trial; DSR penalizes full history; PBO via CSCV.
- M_eff via eigenvalue (if λ1≈N, you have ~1 bet, not N).
- Report gross AND net, pre- AND post-tax if needed, with identical rank basis.

## 6. Sim → live parity (Cameron + Tradecovex 2026)
- Sim with real constraints (daily loss, trailing DD, brackets). 30-100 logged trades, expectancy in R.
- Expect live 20-40% worse. Micro-live 30-50 trades to calibrate cortisol gap.
- Shadow replay: same-day sim vs live candidate agreement ≥95% over ≥5 sessions or FAIL.

## 7. Journal schema (minimum)
date,symbol,setup,entry,stop,target,exit,result_R,rules_followed,emotion_1-5,lesson. Weekly review: win%, avgW_R, avgL_R, expectancy, rule-break rate, revenge sequences, size drift.

## 8. Kill criteria (examples from this repo)
- Expectancy_R ≤0 after 100 trades → kill.
- DSR <0.95 or PBO >0.5 → kill.
- Net Sharpe collapses at 50bps → capacity story only, not scalable edge.
- 6 within-pond pickers die OOS (Palmason) → report pond, not picker.

## Reproduce this repo
`pytest -q && python -m dtb.benchmark` → `results/benchmark.json` with sha256_16. Any code/data/universe/cost change = new hash + new trial count.
