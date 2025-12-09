from typing import Iterable

def parse_price(raw: str) -> float:
    if raw is None:
        raise ValueError
    s = str(raw).strip()
    if not s:
        raise ValueError
    if s.startswith("$"):
        s = s[1:]
    s = s.replace(",", "")
    try:
        value = float(s)
    except:
        raise ValueError
    return value

def format_currency(amount: float) -> str:
    return f"${amount:.2f}"

def apply_discount(price: float, percent: float) -> float:
    if percent < 0:
        raise ValueError
    discount_fraction = percent / 100.0
    return price * (1.0 - discount_fraction)

def add_tax(price: float, rate: float) -> float:
    if rate < 0:
        raise ValueError
    return price * (1.0 + rate)

def bulk_total(prices: Iterable[float], discount_percent: float = 0.0, tax_rate: float = 0.0) -> float:
    subtotal = sum(prices)
    after_discount = apply_discount(subtotal, discount_percent)
    return add_tax(after_discount, tax_rate)
