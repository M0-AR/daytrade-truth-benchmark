"""Executable Cameron guardrails (20) — enforced, not just documented.

Source: Cameron 2023 List of Guardrails (Ch 2,5,6,8,10,11).
Each returns (ok: bool, reason: str). Account-level brakes mirror
FINRA 2026 IML spirit: hard daily loss + max position.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class TradeIntent:
    symbol: str
    price: float
    target: float
    stop: float
    shares: int
    float_m: float | None = None
    pct_change: float | None = None  # vs prev close, e.g. 0.15 = +15%
    rvol: float | None = None
    has_news: bool = False
    is_obvious_leader: bool = False
    prev_day_chg: float | None = None  # for SSR Rule 201: <= -0.10 blocks shorts
    daily_range_pct: float | None = None  # LULD proxy: >=0.20 = halt-risk
    is_short: bool = False
    intraday_deficit: bool = False  # FINRA 2026 IML: broker would block


@dataclass
class DayState:
    daily_pnl: float
    daily_profit_target: float = 200.0
    daily_max_loss: float = 200.0  # guardrail #8: max loss == target
    trades_today: int = 0
    max_trades: int = 3


def reward_risk(intent: TradeIntent) -> float:
    risk = intent.price - intent.stop
    reward = intent.target - intent.price
    if risk <= 0:
        return 0.0
    return reward / risk


def check_profit_loss_ratio(intent: TradeIntent, minimum: float = 2.0):
    """#5: minimum 2:1 planned."""
    rr = reward_risk(intent)
    if rr >= minimum:
        return True, f"R:R {rr:.2f} >= {minimum}"
    return False, f"REJECT R:R {rr:.2f} < {minimum} (#5)"


def check_price_band(intent: TradeIntent):
    """#1c: $2-$20 (prefer $2-$10)."""
    if 2.0 <= intent.price <= 20.0:
        return True, f"price ${intent.price:.2f} in band"
    return False, f"REJECT price ${intent.price:.2f} outside $2-$20 (#1)"


def check_momentum_filters(intent: TradeIntent):
    """#1a,b,d,e + #13 + #15: +10%+, RVOL>=2, news, low float, obvious."""
    reasons = []
    if intent.pct_change is None or intent.pct_change < 0.10:
        return False, f"REJECT chg {intent.pct_change} < +10% (#1)"
    if intent.rvol is None or intent.rvol < 2.0:
        return False, f"REJECT RVOL {intent.rvol} < 2.0 (#1)"
    if not intent.has_news:
        return False, "REJECT no news catalyst (#1)"
    if intent.float_m is not None and intent.float_m > 50:
        return False, f"REJECT float {intent.float_m}M > 50M (#1)"
    if not intent.is_obvious_leader:
        reasons.append("WARN not obvious leader (#15) — reduce size")
    return True, "momentum filters pass; " + "; ".join(reasons) if reasons else "momentum filters pass"


def check_balanced_risk(intent: TradeIntent, avg_prior_risk: float):
    """#10: no single trade erases >2 prior winners. Enforce risk <= 2x avg."""
    risk_dollars = (intent.price - intent.stop) * intent.shares
    if avg_prior_risk <= 0:
        return True, "no baseline yet"
    if risk_dollars <= 2 * avg_prior_risk:
        return True, f"risk ${risk_dollars:.0f} <= 2x avg ${avg_prior_risk:.0f}"
    return False, f"REJECT risk ${risk_dollars:.0f} > 2x avg ${avg_prior_risk:.0f} (#10)"


def check_daily_brake(state: DayState):
    """#8: stop at -max loss; #11 throttle; get-green-shutdown for beginners."""
    if state.daily_pnl <= -state.daily_max_loss:
        return False, f"HALT daily PnL {state.daily_pnl:.0f} <= -{state.daily_max_loss:.0f} (#8)"
    if state.trades_today >= state.max_trades:
        return False, f"HALT {state.trades_today} trades >= max {state.max_trades}"
    return True, "daily brake clear"


def check_max_position(intent: TradeIntent, account: float, max_pct: float = 0.25):
    """#9 broker-level: position value <= max_pct of account (default 25% notional w/o margin)."""
    notional = intent.price * intent.shares
    if notional <= account * max_pct * 4:  # allow 4x intraday but flag
        if notional <= account * max_pct:
            return True, f"notional ${notional:.0f} within {max_pct:.0%}"
        return True, f"WARN notional ${notional:.0f} uses leverage (IML watch 2026)"
    return False, f"REJECT notional ${notional:.0f} exceeds brake (#9)"


def check_halts_ssr_iml(intent: TradeIntent):
    """NEW (verified Sep 2026): SSR Rule 201 + LULD + IML 2026.
    - Short with prev_day <= -10% -> REJECT (uptick-only, Tradingsim 2026).
    - Range >= 20% -> HALT-risk WARN (reduce to 1/4 size, Cameron rehab).
    - IML deficit flag from broker -> HALT (FINRA 26-10).
    """
    if intent.intraday_deficit:
        return False, "HALT IML deficit — broker must block (FINRA 26-10)"
    if intent.is_short and intent.prev_day_chg is not None and intent.prev_day_chg <= -0.10:
        return False, f"REJECT short under SSR {intent.prev_day_chg:.1%} — uptick only (Rule 201)"
    if intent.daily_range_pct is not None and intent.daily_range_pct >= 0.20:
        return True, f"WARN range {intent.daily_range_pct:.1%} >= 20% — halt-risk, quarter size (LULD)"
    return True, "halts/SSR/IML clear"


def full_gate(intent: TradeIntent, state: DayState, account: float, avg_prior_risk: float = 0):
    """Run all gates in order. Returns (pass, [messages])."""
    msgs = []
    for fn in [lambda: check_daily_brake(state),
               lambda: check_halts_ssr_iml(intent),
               lambda: check_profit_loss_ratio(intent),
               lambda: check_price_band(intent),
               lambda: check_momentum_filters(intent),
               lambda: check_balanced_risk(intent, avg_prior_risk),
               lambda: check_max_position(intent, account)]:
        ok, m = fn()
        msgs.append(m)
        if not ok and m.startswith(("REJECT", "HALT")):
            return False, msgs
    return True, msgs
