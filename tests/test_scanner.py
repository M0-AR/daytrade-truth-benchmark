from dtb.scanner import Candle, scan

def test_obln_is_aplus():
    c = Candle("OBLN*", 8.40, 6.00, 321_000_000, 1_500_000, 6_000_000, True, 12)
    top = scan([c])[0]
    assert top["grade"] == "A+"
    assert top["rotation"] > 10

def test_penny_skipped():
    c = Candle("CCC", 0.85, 0.80, 5_000_000, 1_000_000, 500_000_000, False, 1)
    assert scan([c])[0]["grade"] == "SKIP"
