from pathlib import Path
from typing import List, Tuple

from .pricing import parse_price, format_currency, bulk_total

Item = Tuple[str, float]

def load_order(path: Path) -> List[Item]:
    items = []
    text = Path(path).read_text(encoding="utf-8")
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        parts = stripped.split(",")
        if len(parts) != 2:
            raise ValueError
        name, raw_price = parts[0].strip(), parts[1].strip()
        price_value = parse_price(raw_price)
        items.append((name, price_value))
    return items

def write_receipt(path: Path, items: List[Item], discount_percent: float, tax_rate: float) -> None:
    lines = []
    lines.append("RECEIPT")
    lines.append("-------")
    for name, price in items:
        lines.append(f"{name}: {format_currency(price)}")
    lines.append("")
    prices = [p for _, p in items]
    subtotal = sum(prices)
    total = bulk_total(prices, discount_percent, tax_rate)
    lines.append(f"SUBTOTAL: {format_currency(subtotal)}")
    lines.append(f"DISCOUNT: {discount_percent:.0f}%")
    lines.append(f"TAX RATE: {tax_rate * 100:.0f}%")
    lines.append(f"TOTAL: {format_currency(total)}")
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
