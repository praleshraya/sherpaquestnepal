"""Build one portable HTML page per workbook product."""
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / 'index.html').read_text()
PRODUCTS = json.loads((ROOT / 'data/products.json').read_text())
OUT = ROOT / 'products'
OUT.mkdir(exist_ok=True)

header = INDEX[INDEX.index('<div class="announcement">'):INDEX.index('</header>') + len('</header>')]
footer = INDEX[INDEX.index('<footer class="footer">'):INDEX.index('</footer>') + len('</footer>')]
header = header.replace('src="assets/', 'src="../assets/').replace('href="#', 'href="../index.html#')
footer = footer.replace('src="assets/', 'src="../assets/').replace('href="#', 'href="../index.html#')
header = header.replace('href="about.html"', 'href="../about.html"')
footer = footer.replace('href="about.html"', 'href="../about.html"')

def esc(value):
    return html.escape(str(value or ''), quote=True)

def card(product):
    return f'''<a class="related-card" href="{esc(product['id'])}.html">
      <span class="related-image"><img src="../{esc(product['image'])}" alt="{esc(product['name'])}" loading="lazy"></span>
      <small>{esc(product['brand'])}</small><strong>{esc(product['name'])}</strong>
    </a>'''

for product in PRODUCTS:
    related = [item for item in PRODUCTS if item['category'] == product['category'] and item['id'] != product['id']][:4]
    category_url = '../index.html?category=' + quote(product['category']) + '#products'
    inquiry = 'https://wa.me/9779744464587?text=' + quote("Hello Sherpa Quest Nepal, I'd like to ask about " + product['name'] + '.')
    description = esc(product['description'] or 'Contact Sherpa Quest Nepal for product details and availability.')
    options = f'<div class="detail-options"><span>AVAILABLE OPTIONS</span><p>{esc(product["options"])}</p></div>' if product['options'] else ''
    gallery = [{'src': product['image'], 'variant': 'Main view'}]
    gallery += [item for item in product.get('gallery', []) if item['src'] != product['image']]
    gallery_controls = f'''<div class="product-thumbs" aria-label="Product images">{''.join(f'<button type="button" class="product-thumb{ " active" if index == 0 else "" }" data-gallery-src="../{esc(item["src"])}" data-gallery-alt="{esc(product["name"])} — {esc(item["variant"])}" aria-label="Show {esc(item["variant"])} image {index + 1}" aria-pressed="{str(index == 0).lower()}"><img src="../{esc(item["src"])}" alt="" loading="lazy"></button>' for index, item in enumerate(gallery))}</div>''' if len(gallery) > 1 else ''
    related_section = f'''<section class="related shell"><div class="section-head"><div><p class="eyebrow">KEEP EXPLORING</p><h2>RELATED <em>GEAR</em></h2></div></div><div class="related-grid">{''.join(card(item) for item in related)}</div></section>''' if related else ''
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#215c48"><meta name="description" content="Explore {esc(product['name'])} at Sherpa Quest Nepal. Ask about options and availability.">
<title>{esc(product['name'])} | Sherpa Quest Nepal</title>
<link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800;900&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../styles.css"><link rel="stylesheet" href="../product.css"><script defer src="../navigation.js"></script><script defer src="../product-gallery.js"></script></head>
<body data-root="../"><a class="skip" href="#main">Skip to content</a>{header}
<main id="main"><div class="product-page shell"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span>/</span><a href="{category_url}">{esc(product['category'])}</a><span>/</span><span>{esc(product['name'])}</span></nav>
<div class="product-layout"><div class="product-gallery"><div class="product-main-image"><img id="product-main-image" src="../{esc(product['image'])}" alt="{esc(product['name'])}"></div>{gallery_controls}</div>
<div class="product-info"><p class="eyebrow">{esc(product['brand'])} / {esc(product['category'])}</p><h1>{esc(product['name'])}</h1>
<p class="availability">Ask for price &amp; availability</p>{options}
<p class="product-summary">Explore this item and confirm the right options for your ride with Sherpa Quest Nepal.</p>
<a class="button detail-whatsapp" href="{inquiry}" target="_blank" rel="noopener">ASK ABOUT THIS PRODUCT <span>↗</span></a>
<a class="detail-call" href="tel:+9779744464587">Or call +977 974-4464587</a>
<div class="detail-service"><span>PRODUCT INQUIRIES</span><strong>We can help with sizes, fit and availability.</strong></div></div></div>
<section class="product-description"><p class="eyebrow">PRODUCT INFORMATION</p><h2>PRODUCT <em>DETAILS</em></h2><p>{description}</p></section></div>{related_section}</main>
{footer}<a class="floating-chat" href="https://wa.me/9779744464587" target="_blank" rel="noopener" aria-label="Chat with Sherpa Quest Nepal on WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 11.6a8.5 8.5 0 0 1-12.4 7.5L3 20.5l1.4-5A8.5 8.5 0 1 1 20.5 11.6Z"/><path d="M8.7 8.2c-.4 0-.9.7-.8 1.4.1 1.4 2 4 4.3 5.2 1.5.8 2.7.7 3.3.1l.6-.8-2.1-1-1 .9a7.6 7.6 0 0 1-3-3.1l.8-.9-.9-1.9Z"/></svg><span>CHAT WITH US</span></a>
</body></html>'''
    (OUT / (product['id'] + '.html')).write_text(page)

print(f'Built {len(PRODUCTS)} product pages in {OUT}')
