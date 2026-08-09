"""Restore Mollee template copy/structure while keeping MuRa@23 branding and saree products."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = [
    ("meet New <br>Saree week", "meet New <br>Fashion week"),
    ("<span class=\"collection__category\">silk sarees</span>", "<span class=\"collection__category\">accessories</span>"),
    ("<b>new</b> silk sarees", "<b>new</b> accessories"),
    ("<span class=\"collection__category\">wedding sarees</span>", "<span class=\"collection__category\">sweters</span>"),
    ("<b>bridal</b> collection", "<b>men</b> collection"),
    ("<span class=\"collection__category\">cotton sarees</span>", "<span class=\"collection__category\">dresses</span>"),
    ("<b>festive</b> collection", "<b>women</b> collection"),
    ("Celebrate timeless <br>saree elegance", "Stay warm <br>and trendy"),
    (
        "Handpicked silk and cotton sarees crafted for every special occasion",
        "Non aliqua reprehenderit reprehenderit culpa laboris nulla minim anim velit",
    ),
    (
        "Explore our latest festive saree collection with exclusive offers",
        "Non aliqua reprehenderit reprehenderit culpa laboris nulla",
    ),
    (
        "Curators of exquisite handwoven sarees — silk, cotton, bridal, and festive collections from across India.",
        "Official representative of the world-famous clothing brand MuRa@23 in India and the world.",
    ),
    ("Elegant Silk <br>Collection", "Fashion for <br>this summer"),
    ("New Bridal <br>Collection", "new Autumn <br>arrivals 2020"),
    ("Graceful Cotton <br>Saree Collection", "Trendy look <br>for every day"),
    ('href="index.html#products-2">Silk</a>', 'href="index.html#products-2">Men</a>'),
    ('href="index.html#products-3">Cotton</a>', 'href="index.html#products-3">Women</a>'),
    ('href="index.html#products-4">Bridal</a>', 'href="index.html#products-4">Accessories</a>'),
    ('href="index.html#products-5">Wedding</a>', 'href="index.html#products-5">New arrivals</a>'),
]


def main() -> None:
    for path in ROOT.glob("*.html"):
        text = path.read_text()
        original = text
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text)
            print(f"updated {path.name}")


if __name__ == "__main__":
    main()
