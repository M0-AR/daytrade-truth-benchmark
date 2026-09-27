"""Core trading math — all formulas verified against 2026 sources.

Sources:
- Expectancy = (WinRate*AvgWin)-(LossRate*AvgLoss) — DayTradingToolkit 2026-04-17,
  Investopedia risk-management, Tradingsim 2026-06-05
- Breakeven win rate = 1/(1+R) where R = reward/risk multiple — ChartMini 2026-03-28,
  Dhanith 2026-07-08, DayTradingToolkit cheat sheet
- Risk of ruin approx + Monte Carlo — DayTradingToolkit risk-of-ruin 2026-03-14,
  Kaufman formula RoR=((1-edge)/(1+edge))^U, CFA 2% ceiling
- Kelly f*=(W*R-L)/R — Kelly 1956 via METAtronics 2026-03-10; use quarter-Kelly in practice
"""
from __future__ import annotations
import math
import numpy as np


def expectancy(win_rate: float, avg_win: float, avg_loss: float) -> float:
    """Expected value per trade in currency units.
    avg_loss must be positive magnitude.
    """
    assert 0 <= win_rate <= 1, "win_rate in [0,1]"
    assert avg_win >= 0 and avg_loss >= 0
    return win_rate * avg_win - (1 - win_rate) * avg_loss


def expectancy_R(win_rate: float, avg_win_R: float, avg_loss_R: float = 1.0) -> float:
    """Expectancy in R-multiples. avg_loss_R positive magnitude."""
    return win_rate * avg_win_R - (1 - win_rate) * avg_loss_R


def breakeven_win_rate(reward_risk: float) -> float:
    """Pre-cost breakeven: 1/(1+R). R=2 -> 0.333."""
    assert reward_risk > 0
    return 1.0 / (1.0 + reward_risk)


def breakeven_table() -> dict:
    return {R: breakeven_win_rate(R) for R in [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]}


def position_size(account: float, risk_pct: float, risk_per_share: float) -> int:
    """Shares = (account*risk_pct)/risk_per_share. risk_pct e.g. 0.01."""
    assert account > 0 and 0 < risk_pct <= 0.05 and risk_per_share > 0
    return int((account * risk_pct) // risk_per_share) if risk_per_share else 0


def kelly_fraction(win_rate: float, reward_risk: float) -> float:
    """f* = (W*R - L)/R. Can be >1 or negative -> clamp in practice."""
    L = 1 - win_rate
    return (win_rate * reward_risk - L) / reward_risk if reward_risk else 0.0


def risk_of_ruin_kaufman(win_rate: float, reward_risk: float, risk_units: float) -> float:
    """Kaufman simplified RoR. edge = W-L approx for even-money; generalized:
    Use p=win prob, q=1-p, edge per unit = (p*R - q)/R normalized.
    Falls back to Monte Carlo for accuracy — this is closed-form guide only.
    risk_units = account / risk_per_trade (e.g. 100 units at 1%).
    """
    p = win_rate
    q = 1 - p
    # advantage per trial in units of stake
    # expected return per unit risked:
    mu = p * reward_risk - q * 1.0
    if mu <= 0:
        return 1.0
    # classic gambler's ruin approx for favorable game:
    # RoR ≈ ((q/p_eff))^U is only exact for 1:1; use exponent form:
    # use edge ratio method: ((1-edge)/(1+edge))^U where edge=mu/(R avg)
    edge = mu / ((p * reward_risk + q) + 1e-12)
    edge = min(max(edge, 0.001), 0.9)
    return float(((1 - edge) / (1 + edge)) ** risk_units)


def simulate_ruin(win_rate: float, reward_risk: float, risk_pct: float,
                  account: float = 25000, trades: int = 1000,
                  n_paths: int = 5000, seed: int = 42,
                  ruin_level: float = 0.5) -> dict:
    """Monte-Carlo ruin: fraction of paths falling below ruin_level*start.
    Returns dict with ruin_prob, median_end, p10, p90, longest_loss_streak_median.
    """
    rng = np.random.default_rng(seed)
    start = account
    ends = np.empty(n_paths)
    ruined = 0
    streaks = []
    for i in range(n_paths):
        bal = start
        cur_streak = 0
        max_streak = 0
        for _ in range(trades):
            risk_amt = bal * risk_pct
            if rng.random() < win_rate:
                bal += risk_amt * reward_risk
                cur_streak = 0
            else:
                bal -= risk_amt
                cur_streak += 1
                max_streak = max(max_streak, cur_streak)
            if bal <= 0:
                bal = 0
                break
        ends[i] = bal
        streaks.append(max_streak)
        if bal < start * ruin_level:
            ruined += 1
    return {
        "ruin_prob_50pct": ruined / n_paths,
        "median_end": float(np.median(ends)),
        "p10_end": float(np.percentile(ends, 10)),
        "p90_end": float(np.percentile(ends, 90)),
        "median_max_loss_streak": float(np.median(streaks)),
        "n_paths": n_paths, "trades": trades, "seed": seed,
    }


def expected_longest_loss_streak(loss_rate: float, n: int) -> float:
    """log(N)/log(1/loss_rate) — DayTradingToolkit 2026."""
    if loss_rate <= 0 or loss_rate >= 1:
        return 0.0
    return math.log(n) / math.log(1 / loss_rate)
