from src.pricing import apply_discount

def test_apply_discount_regression_percent_handling():
    result = apply_discount(100.0, 10)
    assert result == 90.0
