import pytest

from src.pricing import (
    parse_price,
    format_currency,
    apply_discount,
    add_tax,
    bulk_total,
)
from src.order_io import load_order

@pytest.fixture
def sample_prices():
    return [1.25, 2.50, 3.75]

@pytest.mark.parametrize(
    "raw, expected",
    [
        ("$1,231.50", 1231.50),
        ("12.5", 12.50),
        ("0.99", 0.99),
        ("  $8.00  ", 8.00),
    ],
)
def test_parse_price_valid(raw, expected):
    result = parse_price(raw)
    assert result == pytest.approx(expected)

@pytest.mark.parametrize(
    "raw",
    ["", "abc", "12,34,56", "$12,34,56", None],
)
def test_parse_price_invalid_raises(raw):
    with pytest.raises(ValueError):
        parse_price(raw)

@pytest.mark.parametrize(
    "amount, expected",
    [
        (0, "$0.00"),
        (1, "$1.00"),
        (1.2, "$1.20"),
        (1234.567, "$1234.57"),
    ],
)
def test_format_currency(amount, expected):
    assert format_currency(amount) == expected

@pytest.mark.parametrize(
    "price, percent, expected",
    [
        (100.0, 0, 100.0),
        (100.0, 10, 90.0),
        (200.0, 25, 150.0),
    ],
)
def test_apply_discount_normal(price, percent, expected):
    result = apply_discount(price, percent)
    assert result == pytest.approx(expected)

def test_apply_discount_negative_raises():
    with pytest.raises(ValueError):
        apply_discount(100.0, -5)

@pytest.mark.parametrize(
    "price, rate, expected",
    [
        (100.0, 0.10, 110.0),
        (50.0, 0.075, 53.75),
    ],
)
def test_add_tax_valid(price, rate, expected):
    result = add_tax(price, rate)
    assert result == pytest.approx(expected)

def test_add_tax_negative_rate_raises():
    with pytest.raises(ValueError):
        add_tax(100.0, -0.1)

def test_bulk_total_uses_discount_and_tax(sample_prices):
    subtotal = sum(sample_prices)
    discount_percent = 10
    tax_rate = 0.07
    after_discount = subtotal * (1 - discount_percent / 100)
    expected = after_discount * (1 + tax_rate)
    result = bulk_total(sample_prices, discount_percent, tax_rate)
    assert result == pytest.approx(expected)

def test_bulk_total_empty_list_zero():
    assert bulk_total([]) == 0.0

def test_load_order_parses_and_skips_blank(tmp_path):
    order_file = tmp_path / "order.csv"
    order_file.write_text(
        "widget,$10.00\n"
        "\n"
        "gizmo,5.50\n",
        encoding="utf-8",
    )
    items = load_order(order_file)
    assert items == [("widget", 10.0), ("gizmo", 5.5)]

def test_load_order_malformed_line_raises(tmp_path):
    order_file = tmp_path / "bad.csv"
    order_file.write_text("just-one-field\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_order(order_file)
