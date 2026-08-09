# Curated saree-only catalog — all images from https://unsplash.com
UNSPLASH = "https://images.unsplash.com/photo-{id}?w=1600&q=85&auto=format&fit=crop"


def u(photo_id: str, crop: str = "") -> str:
    url = UNSPLASH.format(id=photo_id)
    return f"{url}&crop={crop}" if crop else url


SAREE_CATALOG = [
    {
        "id": 1,
        "name": "Kanjivaram Silk Saree",
        "url": u("1717835943315-b818e90cb2a1", "center"),
        "file": "product-item_1.jpg",
    },
    {
        "id": 2,
        "name": "Banarasi Silk Saree",
        "url": u("1742677143629-b9784beab2e1", "top"),
        "file": "product-item_2.jpg",
    },
    {
        "id": 3,
        "name": "Cotton Handloom Saree",
        "url": u("1706685481823-b8f1a1c11fca", "top"),
        "file": "product-item_3.jpg",
    },
    {
        "id": 4,
        "name": "Designer Party Saree",
        "url": u("1692992193981-d3d92fabd9cb", "top"),
        "file": "product-item_4.jpg",
    },
    {
        "id": 5,
        "name": "Bridal Silk Saree",
        "url": u("1774437792342-20a785ba0694", "center"),
        "file": "product-item_5.jpg",
    },
    {
        "id": 6,
        "name": "Paithani Silk Saree",
        "url": u("1756483492198-8ca91227489b", "top"),
        "file": "product-item_6.jpg",
    },
    {
        "id": 7,
        "name": "Chanderi Cotton Saree",
        "url": u("1684961415565-80383f48c0c2", "top"),
        "file": "product-item_7.jpg",
    },
    {
        "id": 8,
        "name": "Bandhani Festive Saree",
        "url": u("1678705730064-a7ecbab4b3fb", "center"),
        "file": "product-item_8.jpg",
    },
    {
        "id": 9,
        "name": "Mysore Silk Saree",
        "url": u("1758985402638-6028bae83b98", "center"),
        "file": "product-item_9.jpg",
    },
    {
        "id": 10,
        "name": "Georgette Party Saree",
        "url": u("1771507056578-f9675a2a8f8a", "top"),
        "file": "product-item_10.jpg",
    },
    {
        "id": 11,
        "name": "Tussar Silk Saree",
        "url": u("1749317776467-6dcf2bfbd26b", "center"),
        "file": "product-item_11.jpg",
    },
    {
        "id": 12,
        "name": "Patola Silk Saree",
        "url": u("1769275061356-a038b498c4a7", "center"),
        "file": "product-item_12.jpg",
    },
]

HERO_SLIDES = [
    {
        "file": "first-screen-image.jpg",
        "catalog_file": "product-item_10.jpg",
        "name": "Georgette Party Saree",
    },
    {
        "file": "deal-of-the-week-inner.jpg",
        "catalog_file": "product-item_5.jpg",
        "name": "Bridal Silk Saree",
    },
    {
        "file": "slider-banner.jpg",
        "catalog_file": "product-item_12.jpg",
        "name": "Patola Silk Saree",
    },
]

DEAL_OF_WEEK = {
    "file": "deal-of-the-week.jpg",
    # Outdoor smile + light sky — matches Mollee deal layout for readable left-side text
    "url": u("1761125135252-e7eb993e0145", "top"),
    "name": "Festive Silk Saree",
}

# Dark moody images for season-sale blocks (black card + white text layout)
SEASON_SALE = {
    "collections-image_2.jpg": {
        "url": u("1742038106824-ae078f37b633", "center"),
        "name": "Evening Green Saree",
        "size": (600, 760),
        "anchor": "center",
    },
    "sale-image_1.jpg": {
        "url": u("1756483492198-8ca91227489b", "center"),
        "name": "Paithani Silk Saree",
        "size": (1200, 760),
        "anchor": "center",
    },
    "sale-image_2.jpg": {
        "url": u("1774437792342-20a785ba0694", "center"),
        "name": "Bridal Silk Saree",
        "size": (1200, 760),
        "anchor": "center",
    },
    "sale-image_3.jpg": {
        "url": u("1524504388940-b1c1722653e1", "center"),
        "name": "Classic Silk Saree",
        "size": (1200, 760),
        "anchor": "center",
    },
}

# Page banners cropped to show saree fabric, not face close-ups
PAGE_BANNERS = {
    "banner-contacts.jpg": {
        "url": u("1572470176170-98fa8abcb741", "center"),
        "name": "Silk Saree Drape",
        "anchor": "saree",
    },
    "banner-blog.jpg": {
        "url": u("1692992193981-d3d92fabd9cb", "center"),
        "name": "Designer Party Saree",
        "anchor": "saree",
    },
}

BANNER_SOURCES = [
    u("1742677143629-b9784beab2e1", "top"),
    u("1771507056578-f9675a2a8f8a", "top"),
    u("1769275061356-a038b498c4a7", "center"),
    u("1758985402638-6028bae83b98", "center"),
    u("1692992193981-d3d92fabd9cb", "top"),
    u("1749317776467-6dcf2bfbd26b", "center"),
]

SAREE_NAMES = [item["name"] for item in SAREE_CATALOG]
