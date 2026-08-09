# Curated saree-only catalog. Every URL is a verified woman-in-saree photo from Unsplash.
SAREE_CATALOG = [
    {
        "id": 1,
        "name": "Kanjivaram Silk Saree",
        "url": "https://images.unsplash.com/photo-1717835943315-b818e90cb2a1?w=1200&q=80&auto=format&fit=crop",
        "file": "product-item_1.jpg",
    },
    {
        "id": 2,
        "name": "Banarasi Silk Saree",
        "url": "https://images.unsplash.com/photo-1742677143629-b9784beab2e1?w=1200&q=80&auto=format&fit=crop",
        "file": "product-item_2.jpg",
    },
    {
        "id": 3,
        "name": "Cotton Handloom Saree",
        "url": "https://images.unsplash.com/photo-1706685481823-b8f1a1c11fca?w=1200&q=80&auto=format&fit=crop",
        "file": "product-item_3.jpg",
    },
    {
        "id": 4,
        "name": "Designer Party Saree",
        "url": "https://images.unsplash.com/photo-1692992193981-d3d92fabd9cb?w=1200&q=80&auto=format&fit=crop",
        "file": "product-item_4.jpg",
    },
    {
        "id": 5,
        "name": "Bridal Silk Saree",
        "url": "https://images.unsplash.com/photo-1774437792342-20a785ba0694?w=1200&q=80&auto=format&fit=crop",
        "file": "product-item_5.jpg",
    },
    {
        "id": 6,
        "name": "Paithani Silk Saree",
        "url": "https://images.unsplash.com/photo-1756483492198-8ca91227489b?w=1200&q=80&auto=format&fit=crop",
        "file": "product-item_6.jpg",
    },
    {
        "id": 7,
        "name": "Chanderi Cotton Saree",
        "url": "https://images.unsplash.com/photo-1684961415565-80383f48c0c2?w=1200&q=80&auto=format&fit=crop",
        "file": "product-item_7.jpg",
    },
    {
        "id": 8,
        "name": "Bandhani Festive Saree",
        "url": "https://images.unsplash.com/photo-1678705730064-a7ecbab4b3fb?w=1200&q=80&auto=format&fit=crop",
        "file": "product-item_8.jpg",
    },
    {
        "id": 9,
        "name": "Mysore Silk Saree",
        "url": "https://images.unsplash.com/photo-1698657169196-29b4783810c2?w=1200&q=80&auto=format&fit=crop&crop=center",
        "file": "product-item_9.jpg",
    },
    {
        "id": 10,
        "name": "Georgette Party Saree",
        "url": "https://images.unsplash.com/photo-1771507056578-f9675a2a8f8a?w=1200&q=80&auto=format&fit=crop",
        "file": "product-item_10.jpg",
    },
    {
        "id": 11,
        "name": "Tussar Silk Saree",
        "url": "https://images.unsplash.com/photo-1749317776467-6dcf2bfbd26b?w=1200&q=80&auto=format&fit=crop",
        "file": "product-item_11.jpg",
    },
    {
        "id": 12,
        "name": "Patola Silk Saree",
        "url": "https://images.unsplash.com/photo-1771654805161-442c6aab7b55?w=1200&q=80&auto=format&fit=crop",
        "file": "product-item_12.jpg",
    },
]

# Homepage hero slider: light sarees only, matched to slide copy
HERO_SLIDES = [
    {
        "file": "first-screen-image.jpg",
        "catalog_file": "product-item_2.jpg",
        "name": "Banarasi Silk Saree",
        "title": "Discover Elegant <br>Saree Collection",
        "subtitle": "<b>new</b> silk sarees",
    },
    {
        "file": "deal-of-the-week-inner.jpg",
        "catalog_file": "product-item_5.jpg",
        "name": "Bridal Silk Saree",
        "title": "Bridal Silk <br>Saree Collection",
        "subtitle": "<b>wedding</b> specials",
    },
    {
        "file": "slider-banner.jpg",
        "catalog_file": "product-item_4.jpg",
        "name": "Designer Party Saree",
        "title": "Designer Party <br>Saree Styles",
        "subtitle": "<b>festive</b> collection",
    },
]

# Light saree banners for inner pages
BANNER_SOURCES = [
    "https://images.unsplash.com/photo-1742677143629-b9784beab2e1?w=1600&q=80&auto=format&fit=crop&crop=top",
    "https://images.unsplash.com/photo-1684961415565-80383f48c0c2?w=1600&q=80&auto=format&fit=crop&crop=top",
    "https://images.unsplash.com/photo-1692992193981-d3d92fabd9cb?w=1600&q=80&auto=format&fit=crop&crop=top",
    "https://images.unsplash.com/photo-1678705730064-a7ecbab4b3fb?w=1600&q=80&auto=format&fit=crop&crop=top",
    "https://images.unsplash.com/photo-1749317776467-6dcf2bfbd26b?w=1600&q=80&auto=format&fit=crop&crop=top",
]

SAREE_NAMES = [item["name"] for item in SAREE_CATALOG]
