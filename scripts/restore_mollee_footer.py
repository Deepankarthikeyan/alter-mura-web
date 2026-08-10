"""Restore Mollee footer logo column and useful-links structure on all pages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIRST_COL = (ROOT / "scripts" / "mollee_footer_first_col.html").read_text()

FIRST_COL_RE = re.compile(
    r'<div class="footer__col">\s*'
    r'<a class="footer-logo logo" href="[^"]+">\s*'
    r'<img class="logo__image" src="assets/img/logo\.png" alt="MuRa@23">\s*'
    r'</a>\s*'
    r'(?:<span class="footer-description">.*?</span>\s*)?'
    r'(?:<div class="footer-line"></div>\s*)?'
    r'(?:<div class="socials">.*?</div>\s*)?'
    r'</div>',
    re.DOTALL,
)

USEFUL_LINKS = """                                <div class="footer-nav__col">
                                    <span class="footer-title">Useful links</span>
                                    <ul class="footer-nav__list">
                                        <li class="footer-nav__item">
                                            <a class="footer-nav__link" href="{hash}">Privacy Policy</a>
                                        </li>
                                        <li class="footer-nav__item">
                                            <a class="footer-nav__link" href="{hash}">Terms of use</a>
                                        </li>
                                        <li class="footer-nav__item">
                                            <a class="footer-nav__link" href="{hash}">Support</a>
                                        </li>
                                        <li class="footer-nav__item">
                                            <a class="footer-nav__link" href="{hash}">Shipping details</a>
                                        </li>
                                        <li class="footer-nav__item">
                                            <a class="footer-nav__link" href="faq.html">FAQs</a>
                                        </li>
                                    </ul>
                                </div>"""

CONTACT_COL_RE = re.compile(
    r'<div class="footer-nav__col">\s*'
    r'<span class="footer-title">Contact</span>\s*'
    r'<ul class="footer-nav__list">.*?</ul>\s*'
    r'</div>',
    re.DOTALL,
)


def restore_file(path: Path) -> None:
    text = path.read_text()
    page_hash = f"{path.name}#"
    first_col = FIRST_COL.replace("{hash}", page_hash)
    useful_links = USEFUL_LINKS.replace("{hash}", page_hash)

    new_text, count1 = FIRST_COL_RE.subn(first_col, text, count=1)
    new_text, count2 = CONTACT_COL_RE.subn(useful_links, new_text, count=1)

    if count1 != 1:
        print(f"skip {path.name}: footer logo column not found")
        return
    if count2 != 1:
        print(f"warn {path.name}: contact column not replaced")

    path.write_text(new_text)
    print(f"restored {path.name}")


def main() -> None:
    for path in sorted(ROOT.glob("*.html")):
        if path.name.startswith("mollee"):
            continue
        restore_file(path)
    print("Done: Mollee footer structure restored.")


if __name__ == "__main__":
    main()
