import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = (ROOT / "scripts" / "mollee_header_block.html").read_text()

BLOCK_RE = re.compile(
    r"<!-- BEGIN HEADER -->.*?<!-- MOBILE NAVIGATION END -->",
    re.DOTALL,
)


def restore_file(path: Path) -> None:
    text = path.read_text()
    if "<header class=\"header\">" not in text:
        return
    page_hash = f"{path.name}#"
    block = TEMPLATE.replace("{hash}", page_hash)
    new_text, count = BLOCK_RE.subn(block, text, count=1)
    if count != 1:
        print(f"skip {path.name}: block not found")
        return
    path.write_text(new_text)
    print(f"restored {path.name}")


def main() -> None:
    for path in sorted(ROOT.glob("*.html")):
        restore_file(path)
    print("Done: Mollee header structure restored.")


if __name__ == "__main__":
    main()
