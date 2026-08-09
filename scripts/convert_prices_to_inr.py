"""Convert all USD prices in HTML files to Indian Rupees."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USD_TO_INR = 83


def format_inr(amount: float) -> str:
    rupees = round(amount)
    return f"₹{rupees:,}"


def convert_prices(text: str) -> str:
    return re.sub(
        r"\$(\d+(?:\.\d{1,2})?)",
        lambda m: format_inr(float(m.group(1)) * USD_TO_INR),
        text,
    )


def main() -> None:
    for path in sorted(ROOT.glob("*.html")):
        original = path.read_text()
        updated = convert_prices(original)
        if updated != original:
            path.write_text(updated)
            print(f"updated {path.name}")


if __name__ == "__main__":
    main()
