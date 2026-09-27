from dtb.data_real import load_cached, audit
from dtb.guardrails import TradeIntent, check_halts_ssr_iml


def test_real_csvs_present_and_sane():
    for s in ["SPY", "GME", "AMC"]:
        df = load_cached(s)
        assert df is not None and len(df) > 600, s
        assert set(["Open", "High", "Low", "Close", "Volume"]).issubset(df.columns)


def test_real_volatility_pond():
    # Verified Sep 2026 on Yahoo daily 2024-01-02..2026-09-25 (686 bars):
    # SPY +10% days == 1, GME == 17, AMC == 19. Large caps rarely trigger Cameron filter.
    assert audit(load_cached("SPY"), "SPY")["plus10"] <= 2
    assert audit(load_cached("GME"), "GME")["plus10"] >= 10
    assert audit(load_cached("AMC"), "AMC")["plus10"] >= 10


def test_ssr_gate_blocks():
    ok, m = check_halts_ssr_iml(TradeIntent("X", 5, 6, 4.5, 100, is_short=True, prev_day_chg=-0.12))
    assert not ok and "SSR" in m


def test_iml_gate_halts():
    ok, m = check_halts_ssr_iml(TradeIntent("X", 5, 6, 4.5, 100, intraday_deficit=True))
    assert not ok and "IML" in m
