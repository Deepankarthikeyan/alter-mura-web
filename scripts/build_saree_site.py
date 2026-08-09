import re
import urllib.request
from pathlib import Path
from PIL import Image, ImageEnhance, ImageDraw

from saree_catalog import BANNER_SOURCES, HERO_SLIDES, SAREE_CATALOG

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "assets/img"
EXAMPLES = IMG / "examples"
POOL = IMG / "_pool"

PRODUCT_SIZE = (600, 800)
PRODUCT_DETAIL_SIZE = (900, 1100)
BANNER_SIZE = (1600, 620)
HERO_SIZE = (1040, 800)
HERO_BG = (236, 236, 236)
COLLECTION_SIZE = (600, 760)
POST_SIZE = (900, 600)

NON_SAREE_PHRASES = [
    "Warm casual sweater",
    "Style Handbag",
    "MuRa@23 - silk saree",
    "MuRa@23 - catton shirt",
    "MuRa@23 - cotton shirt",
    "knitted sweater",
    "How to choose a dress for a special occasion?",
    "How to choose a dress for&nbsp;a special occasion?",
    "Women's fashion: how not to dress in 2020",
    "How to dress to be on a good account at work?",
    "How to dress fashionably with only a limited amount?",
    "How to dress for women with children working from home?",
    "How to dress so as not to look fat?",
    "How to choose the perfect dress for&nbsp;a special occasion?",
]

SAREE_BLOG_TITLES = [
    "How to choose a saree for a special occasion?",
    "How to style your saree for festivals in 2026",
    "Women's fashion: elegant saree draping tips",
    "Best saree fabrics for every season",
    "How to pick the perfect bridal saree",
    "Saree care tips for silk and cotton weaves",
    "How to drape a saree for office wear",
]


def download(url: str, dest: Path) -> Image.Image:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        dest.write_bytes(resp.read())
    im = Image.open(dest).convert("RGB")
    if im.width < 400 or im.height < 400:
        raise ValueError(f"Image too small: {url}")
    return im


def brighten(im: Image.Image, factor: float = 1.15) -> Image.Image:
    im = ImageEnhance.Brightness(im).enhance(factor)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    return im


def cover_crop(im: Image.Image, size: tuple[int, int], anchor: str = "center") -> Image.Image:
    tw, th = size
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale), int(sh * scale)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    if anchor == "top":
        top = max(0, (nh - th) // 5)
    elif anchor == "right":
        left = max(0, nw - tw)
        top = max(0, (nh - th) // 4)
    return im.crop((left, top, left + tw, top + th))


def save_jpg(im: Image.Image, path: Path, quality: int = 82) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, "JPEG", quality=quality, optimize=True, progressive=True)


def build_product_images() -> dict[str, Image.Image]:
    catalog_images: dict[str, Image.Image] = {}
    for item in SAREE_CATALOG:
        src = POOL / item["file"]
        im = download(item["url"], src)
        im = brighten(im, 1.12)
        cropped = cover_crop(im, PRODUCT_SIZE, anchor="top")
        catalog_images[item["file"]] = cropped
        save_jpg(cropped, EXAMPLES / item["file"])
        print(f"product {item['file']} -> {item['name']}")
    return catalog_images


def compose_hero_slide(source: Image.Image, fade_ratio: float = 0.58) -> Image.Image:
    """Place saree on the right over a light grey studio-style background for readable hero text."""
    w, h = HERO_SIZE
    photo = brighten(source.convert("RGB"), 1.12)
    photo = cover_crop(photo, HERO_SIZE, anchor="right")

    canvas = Image.new("RGB", HERO_SIZE, HERO_BG)
    canvas.paste(photo, (0, 0))

    overlay = Image.new("RGBA", HERO_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    fade_end = int(w * fade_ratio)
    for x in range(fade_end):
        t = 1 - (x / max(fade_end - 1, 1))
        alpha = int(255 * (t**0.75))
        draw.line([(x, 0), (x, h)], fill=(*HERO_BG, alpha))

    return Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")


def build_hero_slides(catalog_images: dict[str, Image.Image]) -> None:
    for slide in HERO_SLIDES:
        source = Image.open(POOL / slide["catalog_file"]).convert("RGB")
        hero = compose_hero_slide(source)
        save_jpg(hero, IMG / slide["file"])
        print(f"hero {slide['file']} -> {slide['name']}")


def build_banners(catalog_images: dict[str, Image.Image]) -> None:
    banner_pool: list[Image.Image] = []
    for i, url in enumerate(BANNER_SOURCES):
        src = POOL / f"banner_{i + 1}.jpg"
        try:
            banner_pool.append(brighten(download(url, src), 1.18))
        except Exception as exc:
            print("banner download fail", url, exc)

    if not banner_pool:
        banner_pool = list(catalog_images.values())

    hero_files = {s["file"] for s in HERO_SLIDES}
    banner_files = [
        "banner-about.jpg", "banner-blog.jpg", "banner-cart.jpg", "banner-checkout.jpg",
        "banner-collections.jpg", "banner-contacts.jpg", "banner-faq.jpg", "banner-login.jpg",
        "banner-newsletter.jpg", "banner-profile.jpg", "banner-shop.jpg", "banner-wishlist.jpg",
        "banner-404.jpg", "login-bg.jpg", "404-bg.jpg", "deal-of-the-week.jpg",
        "sale-image_1.jpg", "sale-image_2.jpg", "sale-image_3.jpg",
    ]
    collection_files = [f"collections-image_{i}.jpg" for i in range(1, 6)]

    for i, name in enumerate(banner_files):
        if name in hero_files:
            continue
        src = banner_pool[i % len(banner_pool)]
        if name.startswith("sale-image") or name == "deal-of-the-week.jpg":
            im = brighten(cover_crop(src, (1200, 760), anchor="top"), 1.08)
        else:
            im = brighten(cover_crop(src, BANNER_SIZE, anchor="top"), 1.08)
        save_jpg(im, IMG / name)

    for i, name in enumerate(collection_files):
        item = SAREE_CATALOG[i % len(SAREE_CATALOG)]
        im = catalog_images[item["file"]]
        save_jpg(cover_crop(im, COLLECTION_SIZE, anchor="top"), IMG / name)


def build_supporting_images(catalog_images: dict[str, Image.Image]) -> None:
    files = {
        "post-content-image.jpg": (1100, 650),
        "post-main-image.jpg": (1100, 650),
    }
    for i in range(1, 13):
        files[f"post-image_{i}.jpg"] = POST_SIZE

    for idx, (fname, size) in enumerate(files.items()):
        item = SAREE_CATALOG[idx % len(SAREE_CATALOG)]
        im = cover_crop(catalog_images[item["file"]].copy(), size, anchor="top")
        save_jpg(brighten(im, 1.05), EXAMPLES / fname)

    for i in range(1, 5):
        save_jpg(catalog_images[SAREE_CATALOG[i - 1]["file"]], EXAMPLES / f"wishlist-image_{i}.jpg")
        save_jpg(catalog_images[SAREE_CATALOG[i]["file"]], EXAMPLES / f"order-image_{i}.jpg")
        save_jpg(catalog_images[SAREE_CATALOG[i + 1]["file"]], EXAMPLES / f"review-image_{i}.jpg")

    save_jpg(catalog_images[SAREE_CATALOG[0]["file"]], EXAMPLES / "author-photo.jpg")
    save_jpg(catalog_images[SAREE_CATALOG[0]["file"]], EXAMPLES / "product-image.jpg", quality=85)


def sync_product_names() -> None:
    all_names = [item["name"] for item in SAREE_CATALOG]

    for path in ROOT.glob("*.html"):
        text = path.read_text()

        for phrase, replacement in zip(NON_SAREE_PHRASES, SAREE_BLOG_TITLES + SAREE_BLOG_TITLES):
            text = text.replace(phrase, replacement)

        for item in SAREE_CATALOG:
            fname = item["file"]
            pname = item["name"]
            text = re.sub(
                rf'(data-lazy="assets/img/examples/{re.escape(fname)}"[^>]*>\s*</a>\s*<div class="short-item__top">.*?<a class="short-item__link" href="[^"]*">)[^<]+(</a>)',
                rf'\1{pname}\2',
                text,
                flags=re.DOTALL,
            )
            text = re.sub(
                rf'(src="assets/img/examples/{re.escape(fname)}"[^>]*>\s*</a>\s*<div class="short-item__top">.*?<a class="short-item__link" href="[^"]*">)[^<]+(</a>)',
                rf'\1{pname}\2',
                text,
                flags=re.DOTALL,
            )

        idx = 0

        def next_name():
            nonlocal idx
            name = all_names[idx % len(all_names)]
            idx += 1
            return name

        for cls in ("wishlist__link", "reviewed__link", "side-cart__link", "order-table__link"):
            parts = text.split(f'class="{cls}"')
            if len(parts) == 1:
                continue
            rebuilt = [parts[0]]
            for chunk in parts[1:]:
                chunk = re.sub(r'^([^>]*>)[^<]+(</a>)', rf'\1{next_name()}\2', chunk, count=1)
                rebuilt.append(f'class="{cls}"' + chunk)
            text = "".join(rebuilt)
            idx = 0

        path.write_text(text)
        print("synced", path.name)


def sync_hero_slides() -> None:
    index = ROOT / "index.html"
    text = index.read_text()
    slides = re.findall(r'(<div class="main-slider__item js-slide[^>]*>.*?</div>\s*</div>\s*</div>\s*</div>)', text, flags=re.DOTALL)
    if len(slides) < len(HERO_SLIDES):
        print("warning: could not parse all hero slides")
        return

    new_slides = []
    for slide_html, meta in zip(slides, HERO_SLIDES):
        slide_html = re.sub(
            r'data-bg="assets/img/[^"]+"',
            f'data-bg="assets/img/{meta["file"]}"',
            slide_html,
            count=1,
        )
        new_slides.append(slide_html)

    for old, new in zip(slides, new_slides):
        text = text.replace(old, new, 1)
    index.write_text(text)
    print("synced index hero slides")


def main() -> None:
    catalog_images = build_product_images()
    build_hero_slides(catalog_images)
    build_banners(catalog_images)
    build_supporting_images(catalog_images)
    sync_product_names()
    sync_hero_slides()
    print("Done: saree catalog built and optimized.")


if __name__ == "__main__":
    main()
