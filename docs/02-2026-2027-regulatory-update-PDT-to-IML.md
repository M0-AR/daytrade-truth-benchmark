# 02 — 2026-2027 Regulatory Update: PDT → Intraday Margin (IML)

> Book Ch2/6 assumes PDT: 4+ day trades/5d = pattern, $25k minimum. **Do not trade on this in 2026+.**

## What changed (verified 2026-09-27, 3 sources agree)

- **FINRA Regulatory Notice 26-10 (2026-04-20):** replaces day-trading margin requirements *in their entirety*, incl. PDT designation + $25k.
- **SEC Release 34-105226 (2026-04-14, File SR-FINRA-2025-017):** accelerated approval, amends Rule 4210: new (a)(17)-(19), (d)(2), (g)(1)(J)(K); deletes (f)(8)(B),(b),(f)(10),(g)(13).
- **FINRA Investor Insight “Understanding New Intraday Margin” + Unscripted podcast 2026-09-01:** plain-English confirmation.
- Jina-reader fetch of FINRA page 2026-09-26 succeeded (agent-reach path).

Effective **2026-06-04**, phase-in to **2027-10-20**. Brokers may block in real time or bill end-of-day during transition — call your broker.

## New mechanics

- No trade counting, no $25k gate. $2k minimum for leverage still applies.
- **IML-reducing transaction** = any trade reducing withdrawable cash under maintenance (e.g. buy, short sale).
- **Intraday Margin Deficit** = max intraday shortfall of equity vs 25% maintenance (30% shorts, 0DTE now margined).
- Must satisfy **as promptly as possible**; outstanding max 15 biz days; net deposits/increased IML can cover multiple deficits.
- **90-day freeze** if *practice* of non-payment + deficit unsatisfied by T+5: no new shorts/debits except closes. De minimis: ≤ min(5% equity, $1k) or extraordinary circumstances ≠ practice.
- Firms may **pre-block** offending orders (never incur deficit) or end-of-day call.

## Why (FINRA rationale)

- 2001 rules assumed high commissions ($50k breakeven study); zero-commission world broke $25k logic.
- Real-time risk tech now possible; old day-vs-overnight asymmetry (buy AM sell PM ≠ buy PM sell AM) illogical.
- 0DTE invisible under old rule → now covered.

## What stays

- Rule 2130 (account approval) + 2270 (day-trade risk disclosure) still enforce; FINRA: “frequent trading remains high-risk, not for everyone.”
- Maintenance 25% long all day (firms may require more).

## Action for Cameron readers

1. Replace “fund to $25k to unlock” with “fund to survive 10-loss streak at 1% + maintenance all day.”
2. Replace offshore $500 PDT-dodge with “small cash account can day-trade, but leverage = IML deficit risk.”
3. Keep broker brake (#9) — now set IML auto-block, not PDT flag.
4. Thesis impact: lower entry barrier → more entrants → base rates unchanged (Brazil had no PDT and still 97% lose).

Sources: finra.org/rules-guidance/notices/26-10, sec.gov/files/rules/sro/finra/2026/34-105226.pdf, finra.org/investors/insights/intraday-margin-requirements, govinfo FR 91(74) 2026-04-17, ACA 2026-05-06 summary.
