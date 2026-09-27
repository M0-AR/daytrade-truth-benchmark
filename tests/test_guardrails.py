from dtb.guardrails import TradeIntent, DayState, full_gate

def test_good_passes():
    i = TradeIntent("AAA", 5.20, 6.20, 4.70, 500, 12, 0.13, 4.0, True, True)
    ok, _ = full_gate(i, DayState(50, 200, 200, 0), 25000, 250)
    assert ok

def test_bad_price_rejected():
    i = TradeIntent("BBB", 35.0, 36.0, 33.0, 100, 200, 0.16, 4.0, True, True)
    ok, msgs = full_gate(i, DayState(0, 200, 200, 0), 25000, 250)
    assert not ok
    assert any("price" in m.lower() or "R:R" in m for m in msgs)

def test_daily_halt():
    i = TradeIntent("AAA", 5.20, 6.20, 4.70, 100, 12, 0.13, 4.0, True, True)
    ok, msgs = full_gate(i, DayState(-250, 200, 200, 1), 25000, 250)
    assert not ok
