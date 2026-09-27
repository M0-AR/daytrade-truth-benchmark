# 04 — PhD Paper Outline (testable, not hagiography)

**Working title:** *Intraday Momentum in Low-Float U.S. Equities: Gross Edge, Net Frictions, and the Reproducibility Gap — Re-examining Retail Day-Trading Claims Post-FINRA 2026*

## Research questions
1. Does Cameron-style filter (+10%, RVOL≥2, $2-20, ≤20M float, news) predict same-day continuation net of costs?
2. What share of gross is consumed by spread/impact/SSR-halt?
3. Does IML reform change entry/survival vs PDT era?
4. Can journaled discipline (daily halt, 1-trade start) be distinguished from luck via DSR/PBO?

## Hypotheses (falsifiable)
- H1 (pond): Filtered universe shows + intraday drift 10:15→13:15 ET gross (replicate Palmason +0.139%/d t≈4).
- H2 (costs): Net ≤0 below $480M mcap after TAQ spreads (clawRxiv).
- H3 (picker): No within-pond selector survives locked OOS + DSR>0.95 (expect KILL — publish it).
- H4 (risk): 2:1 + 1% rule lowers ruin vs unbalanced (Monte-Carlo in `dtb.metrics`).
- H5 (sim gap): Live underperforms sim 20-40% controlling for rules.
- H6 (halt): SSR/LULD exposure explains fat left tail of low-float runners.
- H7 (regulation): IML lowers capital gate but not 2-yr survival (diff-in-diff around 2026-06-04).

## Methods
- PIT universe 2016-2027 NYSE/NASDAQ common, delists incl., float from filings.
- Fixed window 10:15→13:15, equal-weight 4-10/day, long-only, no leverage (baseline).
- Three cost arms: base / 30bps / 50bps + Corwin-Schultz spread + volume cap.
- CPCV + embargo, DSR(N=all trials), PBO, M_eff.
- Sim/live shadow parity (≥5 sessions, ≥95% agreement).
- Ethics: no mirror-trading advice; disclose FTC + base rates; IRB if human subjects (journal diaries).

## Contributions
1. First post-IML replication of low-float momentum with full cost stress.
2. Filtration taxonomy applied to retail scanner (Class I/II/III audit).
3. Open compendium: code+hash+kill log (this repo) — reviewers can re-run `docker compose up benchmark`.

## Chapter map
1. Lit (Barber/Chague/Jordan + Amihud + microstructure) 2. Institutional change (PDT→IML) 3. Data/PIT 4. Strategy formalization (scanner+guardrails as code) 5. Results (gross vs net) 6. Behavioral (journal/rehab) 7. Conclusion: pond real, picker unproven, costs are the thesis.

## Data needed (no scraping of broker PII)
CRSP/TAQ or SIP minute + float + RavenPack/news + FINRA IML notices + own sim journals (anonymized).
