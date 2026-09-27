from dtb.metrics import expectancy, breakeven_win_rate, position_size, kelly_fraction, expected_longest_loss_streak

def test_breakeven_2R_is_one_third():
    assert abs(breakeven_win_rate(2.0) - 1/3) < 1e-9

def test_breakeven_table_monotone():
    assert breakeven_win_rate(1) == 0.5
    assert breakeven_win_rate(3) == 0.25

def test_expectancy_example():
    # 60% x $200 - 40% x $120 = $72 (DayTradingToolkit example)
    assert abs(expectancy(0.6, 200, 120) - 72) < 1e-9

def test_cameron_90pct_trap():
    # 9x +$100 then 1x -$1000 = -$100 despite 90% win
    assert 9*100 - 1000 == -100

def test_position_size_1pct():
    assert position_size(25000, 0.01, 0.50) == 500
    assert position_size(25000, 0.01, 1.00) == 250

def test_kelly_bounds():
    f = kelly_fraction(0.55, 1.5)
    assert abs(f - 0.25) < 1e-9

def test_loss_streak_formula():
    s = expected_longest_loss_streak(0.4, 1000)
    assert 7 < s < 9
