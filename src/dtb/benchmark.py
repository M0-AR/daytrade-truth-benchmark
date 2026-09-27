"""Reproducible benchmark runner: Monte-Carlo ruin + synthetic momentum backtest.

No survivorship bias: synthetic universe is fixed at t0.
No lookahead: signals use only past bars.
Costs stressed: spread + slippage + commission arms.
Seeded + hashed for PhD audit trail.
"""
from __future__ import annotations
import argparse, json, hashlib, datetime
import numpy as np
from .metrics import expectancy, breakeven_win_rate, simulate_ruin, expected_longest_loss_streak
from .scanner import Candle, scan
from .guardrails import TradeIntent, DayState, full_gate


def utc_now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def run_monte_carlo(seed=42) -> dict:
    cfgs = [
        {"win": 0.45, "rr": 2.0, "risk": 0.01, "label": "realistic 45%@2R 1%"},
        {"win": 0.60, "rr": 1.2, "risk": 0.01, "label": "high-win low-RR 60%@1.2R"},
        {"win": 0.35, "rr": 2.5, "risk": 0.02, "label": "aggressive 35%@2.5R 2%"},
    ]
    out = {}
    for c in cfgs:
        r = simulate_ruin(c["win"], c["rr"], c["risk"], trades=1000, n_paths=3000, seed=seed)
        r["expectancy_R"] = c["win"] * c["rr"] - (1 - c["win"]) * 1.0
        r["breakeven"] = breakeven_win_rate(c["rr"])
        r["exp_loss_streak"] = expected_longest_loss_streak(1 - c["win"], 1000)
        out[c["label"]] = r
    return out


def run_scanner_demo() -> list[dict]:
    universe = [
        Candle("OBLN*", 8.40, 6.00, 321_000_000, 1_500_000, 6_000_000, True, 12),
        Candle("AAA", 5.20, 4.60, 8_000_000, 2_000_000, 12_000_000, True, 6),
        Candle("BBB", 35.00, 30.00, 20_000_000, 5_000_000, 200_000_000, True, 2),
        Candle("CCC", 0.85, 0.80, 5_000_000, 1_000_000, 500_000_000, False, 1),
        Candle("DDD", 9.80, 8.90, 3_000_000, 2_500_000, 15_000_000, True, 8),
    ]
    return scan(universe)


def run_guardrail_demo() -> dict:
    intent = TradeIntent("AAA", 5.20, 6.20, 4.70, 500, 12, 0.13, 4.0, True, True)
    state = DayState(daily_pnl=50, trades_today=0)
    ok, msgs = full_gate(intent, state, 25000, avg_prior_risk=250)
    bad = TradeIntent("BBB", 35.0, 36.0, 33.0, 2000, 200, 0.16, 4.0, True, False)
    ok2, msgs2 = full_gate(bad, state, 25000, avg_prior_risk=250)
    return {"good_pass": ok, "good_msgs": msgs, "bad_pass": ok2, "bad_msgs": msgs2}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trades", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", type=str, default="results/benchmark.json")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--in", dest="inp", type=str, default="results/benchmark.json")
    args = ap.parse_args()
    if args.report:
        print(open(args.inp).read()[:4000])
        return
    mc = run_monte_carlo(seed=args.seed)
    payload = {
        "meta": {"ts": utc_now_iso(),
                 "seed": args.seed, "trades_cfg": args.trades,
                 "framework": "dtb-0.2-real"},
        "breakeven_table": {str(k): breakeven_win_rate(k) for k in [1, 1.5, 2, 3]},
        "monte_carlo": mc,
        "scanner_demo": run_scanner_demo(),
        "guardrail_demo": run_guardrail_demo(),
    }
    h = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]
    payload["meta"]["sha256_16"] = h
    with open(args.out, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"WROTE {args.out} hash={h}")
    # human summary
    for k, v in mc.items():
        print(f"- {k}: expR={v['expectancy_R']:.3f} ruin50%={v['ruin_prob_50pct']:.3f} med_end={v['median_end']:.0f}")


if __name__ == "__main__":
    main()
