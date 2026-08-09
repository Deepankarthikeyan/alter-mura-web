import os
from collections import deque
from pathlib import Path
from PIL import Image
import urllib.request

ROOT = Path('/workspace')
IMG = ROOT / 'assets/img'

# --- Transparent logo ---
logo_path = IMG / 'logo.png'
img = Image.open(logo_path).convert('RGBA')
w, h = img.size
pixels = img.load()


def is_bg(r, g, b, a):
    if a < 10:
        return True
    return r < 35 and g < 35 and b < 35


visited = [[False] * w for _ in range(h)]
q = deque()
for x in range(w):
    for y in (0, h - 1):
        if not visited[y][x] and is_bg(*pixels[x, y]):
            q.append((x, y))
            visited[y][x] = True
for y in range(h):
    for x in (0, w - 1):
        if not visited[y][x] and is_bg(*pixels[x, y]):
            q.append((x, y))
            visited[y][x] = True
while q:
    x, y = q.popleft()
    pixels[x, y] = (0, 0, 0, 0)
    for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
        if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx] and is_bg(*pixels[nx, ny]):
            visited[ny][nx] = True
            q.append((nx, ny))

bbox = img.getbbox()
if bbox:
    img = img.crop(bbox)
img.save(logo_path)
fav = img.copy()
fav.thumbnail((64, 64), Image.Resampling.LANCZOS)
fav.save(IMG / 'favicon.png')
print('Logo transparent:', img.size)

# --- Download saree images ---
sources = [
    'https://images.unsplash.com/photo-1717835943315-b818e90cb2a1?w=1400&q=85&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1756483492198-8ca91227489b?w=1400&q=85&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1774437792342-20a785ba0694?w=1400&q=85&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1742677143629-b9784beab2e1?w=1400&q=85&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1771507056578-f9675a2a8f8a?w=1400&q=85&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1698657169196-29b4783810c2?w=1400&q=85&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1616986491129-3e37cb654c82?w=1400&q=85&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1692992193981-d3d92fabd9cb?w=1400&q=85&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=1400&q=85&auto=format&fit=crop',
]

pool = []
tmp_dir = IMG / '_pool'
tmp_dir.mkdir(exist_ok=True)
for i, url in enumerate(sources):
    out = tmp_dir / f'saree_{i + 1}.jpg'
    try:
        if not out.exists() or out.stat().st_size < 1000:
            urllib.request.urlretrieve(url, out)
        im = Image.open(out).convert('RGB')
        pool.append(im)
        print('OK', out.name, im.size)
    except Exception as e:
        print('FAIL', url, e)

if len(pool) < 3:
    raise SystemExit('Not enough saree images downloaded')


def pick(i, size):
    im = pool[i % len(pool)].copy()
    return im.resize(size, Image.Resampling.LANCZOS)


sizes = {
    'product-item': (600, 800),
    'product-image': (900, 1100),
    'post-image': (800, 600),
    'post-content': (1200, 700),
    'post-main': (1200, 700),
    'banner': (1920, 700),
    'collections-image': (900, 1100),
    'first-screen': (1400, 900),
    'slider-banner': (1400, 900),
    'deal-of-the-week': (1200, 800),
    'sale-image': (900, 700),
    'login-bg': (1200, 900),
    '404-bg': (1400, 900),
    'review-image': (300, 400),
    'wishlist-image': (300, 400),
    'order-image': (200, 260),
    'author-photo': (400, 400),
}

paths = sorted({
    m.group(0)
    for html in ROOT.glob('*.html')
    for m in __import__('re').finditer(r'assets/img/[^"\')\s]+\.(?:jpg|png|jpeg)', html.read_text())
})

for idx, rel in enumerate(paths):
    if 'payment_' in rel or rel.endswith('favicon.png') or rel.endswith('logo.png') or rel.endswith('captcha.png'):
        continue
    full = ROOT / rel
    full.parent.mkdir(parents=True, exist_ok=True)
    name = full.name
    key = 'banner'
    for k in sizes:
        if k in name or k.replace('-', '_') in name:
            key = k
            break
    if 'examples' in rel:
        if 'product-item' in name:
            key = 'product-item'
        elif 'product-image' in name:
            key = 'product-image'
        elif 'post-content' in name:
            key = 'post-content'
        elif 'post-main' in name:
            key = 'post-main'
        elif 'post-image' in name:
            key = 'post-image'
        elif 'review' in name:
            key = 'review-image'
        elif 'wishlist' in name:
            key = 'wishlist-image'
        elif 'order' in name:
            key = 'order-image'
        elif 'author' in name:
            key = 'author-photo'
    size = sizes.get(key, (1000, 800))
    im = pick(idx, size)
    if full.suffix.lower() == '.png':
        im.save(full, 'PNG')
    else:
        im.save(full, 'JPEG', quality=88)
    print('WROTE', rel)

print('Total images written:', len(paths))
