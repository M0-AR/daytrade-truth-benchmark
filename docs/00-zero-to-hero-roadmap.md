# 00 — Zero-to-Hero Roadmap (verified)

Goal: take a reader from “never traded” to “can run a reproducible benchmark + sim with audit trail” without risking real money prematurely.

## Phase 0 — Decide if you should start (Day 0)
- Read Cameron Ch 1-4 myths. Verify base rates: <1% predictably profitable (Barber et al. 2014), 97% Brazil persisters lose (Chague 2020), 70% US sample lose (Jordan & Diltz 2003). Source vote: 3 academic AGREE.
- Capital check: book used $25k PDT minimum. **2026 update:** PDT gone (FINRA 26-10). You still need $2k for leverage + maintenance 25% all day. Do NOT start if you need rent money (Cameron #16, Tradecovex 2026).
- Gear: laptop + 2 monitors, Windows or E*Trade/Ameritrade Mac, sim with Level 2 + hotkeys + export (Cameron Ch5).

## Phase 1 — Foundations (Weeks 1-4)
- Market basics: IPO/float/market-cap/bid-ask/spread/margin/long-short (Cameron Ch6 glossary verified vs Investopedia 2026).
- Candlesticks: doji/bottoming-topping-tail/hammer/long-body (Cameron Ch9). Add volume + VWAP + 9/20EMA. Practice: print A+ charts, label.
- Math: breakeven=1/(1+R), expectancy, 1% rule, position_size=(acct*risk)/risk_per_share. Run `pytest tests/test_metrics.py`.

## Phase 2 — One strategy, one plan (Weeks 5-8)
- Pick ONE: gap-and-go small-cap momentum (price $2-20, +10%+, RVOL≥2, float≤20M, news, obvious leader). All six must co-occur (Prodigy 2026, EasySwing 2026 AGREE).
- Write trading plan: max risk/trade (25% of daily target), profit target/trade, daily target=max loss ($200 starter), max 1-3 trades, 7:30-11:30 ET only, stop conditions.
- Code it: `src/dtb/scanner.py` + `guardrails.py`. If gate says SKIP/HALT, you skip.

## Phase 3 — Sim with constraints (Months 3-5, 30-100 trades)
- Sim balance = real planned capital (not $100k fantasy). Enforce daily loss halt, journal every trade: date/symbol/setup/entry/stop/target/exit/R/rules?/emotion.
- Expect live = sim minus 20-40% (Alpaca 3-5x paper>live; Tradie 2026). If sim expectancy ≤0 after 50 trades, fix strategy, not size.
- Pass gate: 5-6 green weeks + survived 1 drawdown + recovery (Cameron #20, Martin 8-month sim case).

## Phase 4 — Micro-live bridge (Months 6-8)
- Tiny real size (100 shares or micro). Goal is emotional calibration (cortisol, revenge, size-drift), not profit. Keep sim running in parallel for ideas.
- Trader Rehab on drawdown: halve size + halve daily loss + 1 trade/day x5 (Cameron Ch8).

## Phase 5 — Scale slowly (Months 9-24)
- 100→200→300 shares every 2-3 green weeks. Then 1→2 trades/day. Throttle hot/cold (Cameron #11). Top-10 days = ~20% year — do not cap winners by “get green shutdown” forever; that rule is training wheels.
- Monthly audit: expectancy, R-multiple distribution, DSR, slippage calibration.

## Exit criteria (do NOT go live if…)
- No written plan, <50 rule-clean sim trades, no daily-loss halt, negative expectancy, or trading phone-app/Uber stoplight (Cameron Ch7).

Time to consistency (verified): ~24mo median survivors; 12-18mo full-time+mentor; 40% quit month 1, 80% by yr2, 93% by yr5 (Barber et al. + TrailingStopLoss 2026 synthesis).
