import re
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import urllib.request

ROOT = Path('/workspace')
IMG = ROOT / 'assets/img'
POOL = IMG / '_pool'

# Curated light saree / fabric images only
LIGHT_SOURCES = [
    ('white_saree', 'https://images.unsplash.com/photo-1742677143629-b9784beab2e1?w=1800&q=85&auto=format&fit=crop'),
    ('white_red_saree', 'https://images.unsplash.com/photo-1678705730064-a7ecbab4b3fb?w=1800&q=85&auto=format&fit=crop'),
    ('yellow_white_saree', 'https://images.unsplash.com/photo-1684961415565-80383f48c0c2?w=1800&q=85&auto=format&fit=crop'),
    ('pink_gold_fabric', 'https://images.unsplash.com/photo-1698657169196-29b4783810c2?w=1800&q=85&auto=format&fit=crop'),
    ('cotton_textile', 'https://images.unsplash.com/photo-1616986491129-3e37cb654c82?w=1800&q=85&auto=format&fit=crop'),
    ('soft_color_saree', 'https://images.unsplash.com/photo-1692992193981-d3d92fabd9cb?w=1800&q=85&auto=format&fit=crop'),
    ('pastel_fabrics', 'https://images.unsplash.com/photo-1558171813-4c088753af8f?w=1800&q=85&auto=format&fit=crop'),
    ('light_green_saree', 'https://images.unsplash.com/photo-1756483492198-8ca91227489b?w=1800&q=85&auto=format&fit=crop'),
]

SIZES = {
    'product-item': (600, 800),
    'product-image': (900, 1100),
    'post-image': (900, 650),
    'post-content': (1200, 700),
    'post-main': (1200, 700),
    'banner': (1920, 700),
    'collections-image': (700, 900),
    'first-screen': (1040, 1200),
    'slider-banner': (1040, 1200),
    'deal-of-the-week': (1200, 800),
    'sale-image': (900, 700),
    'login-bg': (1200, 900),
    '404-bg': (1400, 900),
    'review-image': (300, 400),
    'wishlist-image': (300, 400),
    'order-image': (200, 260),
    'author-photo': (400, 400),
}

BANNER_KEYS = {'banner', 'first-screen', 'slider-banner', 'deal-of-the-week', 'sale-image', 'login-bg', '404-bg', 'collections-image'}
TEXT_OVERLAY_KEYS = {'deal-of-the-week', 'sale-image', 'collections-image_2'}


def avg_brightness(im: Image.Image) -> float:
    sample = im.convert('RGB').resize((64, 64), Image.Resampling.BILINEAR)
    pixels = list(sample.getdata())
    return sum((r + g + b) / 3 for r, g, b in pixels) / len(pixels)


def download_pool() -> list[Image.Image]:
    POOL.mkdir(exist_ok=True)
    images: list[Image.Image] = []
    for name, url in LIGHT_SOURCES:
        path = POOL / f'{name}.jpg'
        try:
            urllib.request.urlretrieve(url, path)
            im = Image.open(path).convert('RGB')
            if avg_brightness(im) < 90:
                im = brighten(im, 1.35)
                im.save(path, 'JPEG', quality=90)
            images.append(im)
            print(f'OK {name}: {im.size} brightness={avg_brightness(im):.0f}')
        except Exception as exc:
            print(f'FAIL {name}: {exc}')
    if len(images) < 4:
        raise SystemExit('Not enough light saree images downloaded')
    return images


def brighten(im: Image.Image, factor: float = 1.25) -> Image.Image:
    im = ImageEnhance.Brightness(im).enhance(factor)
    im = ImageEnhance.Contrast(im).enhance(1.05)
    im = ImageEnhance.Color(im).enhance(0.95)
    return im


def cover_crop(im: Image.Image, size: tuple[int, int], focus: str = 'center') -> Image.Image:
    target_w, target_h = size
    src_w, src_h = im.size
    scale = max(target_w / src_w, target_h / src_h)
    resized = im.resize((int(src_w * scale), int(src_h * scale)), Image.Resampling.LANCZOS)
    rw, rh = resized.size
    left = (rw - target_w) // 2
    top = (rh - target_h) // 2
    if focus == 'top':
        top = max(0, (rh - target_h) // 4)
    elif focus == 'right':
        left = max(0, rw - target_w)
        top = max(0, (rh - target_h) // 3)
    return resized.crop((left, top, left + target_w, top + target_h))


def add_light_wash(im: Image.Image, strength: float = 0.28) -> Image.Image:
    overlay = Image.new('RGB', im.size, (255, 255, 255))
    return Image.blend(im, overlay, strength)


def add_soft_gradient_for_text(im: Image.Image) -> Image.Image:
    im = add_light_wash(im, 0.22)
    grad = Image.new('L', im.size, 0)
    draw = ImageDraw.Draw(grad)
    w, h = im.size
    for x in range(w):
        alpha = int(220 * (1 - x / w) ** 1.4)
        draw.line([(x, 0), (x, h)], fill=alpha)
    white = Image.new('RGB', im.size, (255, 255, 255))
    return Image.composite(white, im, grad)


def classify(name: str, rel: str) -> str:
    ordered = sorted(SIZES.keys(), key=len, reverse=True)
    for key in ordered:
        if key in name or key.replace('-', '_') in name:
            return key
    if 'examples' in rel:
        if 'product-item' in name:
            return 'product-item'
        if 'product-image' in name:
            return 'product-image'
        if 'post-content' in name:
            return 'post-content'
        if 'post-main' in name:
            return 'post-main'
        if 'post-image' in name:
            return 'post-image'
        if 'review' in name:
            return 'review-image'
        if 'wishlist' in name:
            return 'wishlist-image'
        if 'order' in name:
            return 'order-image'
        if 'author' in name:
            return 'author-photo'
    return 'banner'


def pick_image(pool: list[Image.Image], idx: int, key: str) -> Image.Image:
    # Prefer brightest images for banners and text-overlay sections
    ranked = sorted(pool, key=avg_brightness, reverse=True)
    if key in BANNER_KEYS:
        return ranked[idx % min(4, len(ranked))]
    if key in {'product-item', 'product-image', 'review-image', 'wishlist-image', 'order-image'}:
        fabric = [im for im in pool if avg_brightness(im) > 120]
        source = fabric if fabric else pool
        return source[idx % len(source)]
    return pool[idx % len(pool)]


def process_image(pool: list[Image.Image], idx: int, key: str, rel: str) -> Image.Image:
    im = pick_image(pool, idx, key).copy()
    size = SIZES.get(key, (1000, 800))
    focus = 'right' if key in {'first-screen', 'slider-banner'} else 'top' if key in BANNER_KEYS else 'center'
    im = cover_crop(im, size, focus=focus)
    im = brighten(im, 1.18 if key in BANNER_KEYS else 1.1)
    if key in BANNER_KEYS or key in {'deal-of-the-week', 'sale-image'}:
        im = add_light_wash(im, 0.18)
    if key in {'deal-of-the-week', 'sale-image'} or 'collections-image_2' in rel:
        im = add_soft_gradient_for_text(im)
    if key in {'product-item', 'product-image', 'review-image', 'wishlist-image'}:
        im = im.filter(ImageFilter.SHARPEN)
    return im


def collect_paths() -> list[str]:
    return sorted({
        m.group(0)
        for html in ROOT.glob('*.html')
        for m in re.finditer(r'assets/img/[^"\')\s]+\.(?:jpg|png|jpeg)', html.read_text())
        if 'payment_' not in m.group(0)
        and not m.group(0).endswith(('favicon.png', 'logo.png', 'captcha.png'))
    })


def main() -> None:
    pool = download_pool()
    paths = collect_paths()
    for idx, rel in enumerate(paths):
        key = classify(Path(rel).name, rel)
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        im = process_image(pool, idx, key, rel)
        if out.suffix.lower() == '.png':
            im.save(out, 'PNG')
        else:
            im.save(out, 'JPEG', quality=90, optimize=True)
        print('WROTE', rel, key, im.size)
    print('Total images written:', len(paths))


if __name__ == '__main__':
    main()
