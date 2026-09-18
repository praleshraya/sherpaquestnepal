"""Build one portable HTML page per workbook product."""
import html
import json
import re
from pathlib import Path
from urllib.parse import quote
from product_content import story, feature_rows, feature_points, options_for, color_preview, SWATCHES

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / 'index.html').read_text()
PRODUCTS = json.loads((ROOT / 'data/products.json').read_text())
OUT = ROOT / 'products'
OUT.mkdir(exist_ok=True)

header = INDEX[INDEX.index('<div class="announcement">'):INDEX.index('</header>') + len('</header>')]
footer = INDEX[INDEX.index('<footer class="footer">'):INDEX.index('</footer>') + len('</footer>')]
contact = (ROOT / 'partials/contact.html').read_text()
header = header.replace('src="assets/', 'src="../assets/').replace('href="#', 'href="../index.html#')
footer = footer.replace('src="assets/', 'src="../assets/').replace('href="#', 'href="../index.html#')
header = header.replace('href="about.html"', 'href="../about.html"')
footer = footer.replace('href="about.html"', 'href="../about.html"')
header = header.replace('href="brands.html"', 'href="../brands.html"')
footer = footer.replace('href="brands.html"', 'href="../brands.html"')
header = header.replace('href="riders.html"', 'href="../riders.html"')
footer = footer.replace('href="riders.html"', 'href="../riders.html"')
header = header.replace('href="../index.html#contact-us"', 'href="#contact-us"')

def esc(value):
    return html.escape(str(value or ''), quote=True)

def gallery_color(product, image, colors):
    variant = next((item['variant'] for item in product.get('gallery', []) if item['src'] == image), '')
    normalized = re.sub(r'[^a-z0-9]', '', variant.lower())
    for color in colors:
        if normalized and normalized == re.sub(r'[^a-z0-9]', '', color.lower()):
            return color
    if normalized == 'black' and 'Matte Black' in colors and len(colors) == 1:
        return 'Matte Black'
    return colors[0] if len(colors) == 1 else ''

def card(product):
    alternate = next((item['src'] for item in product.get('gallery', []) if item['src'] != product['image']), None)
    return f'''<a class="related-card" href="{esc(product['id'])}.html">
      <span class="related-image"><img class="related-primary" src="../{esc(product['image'])}" alt="{esc(product['name'])}" loading="lazy">{f'<img class="related-hover" src="../{esc(alternate)}" alt="" loading="lazy">' if alternate else ''}</span>
      <small>{esc(product['brand'] if product['brand'] != 'UNBRANDED' else 'RIDER ESSENTIALS')}</small><strong>{esc(product['name'])}</strong>
   </a>'''

for product in PRODUCTS:
    brand_label = product['brand'] if product['brand'] != 'UNBRANDED' else 'RIDER ESSENTIALS'
    related = [item for item in PRODUCTS if item['category'] == product['category'] and item['id'] != product['id']][:4]
    category_url = '../index.html?category=' + quote(product['category']) + '#products'
    inquiry = 'https://wa.me/9779744464587?text=' + quote("Hello Sherpa Quest Nepal, I'd like to ask about " + product['name'] + '.')
    sizes, colors = options_for(product)
    primary_color = gallery_color(product, product['image'], colors)
    size_buttons = ''.join(f'<button type="button" class="size-option" data-option-size="{esc(size)}" aria-pressed="false">{esc(size)}</button>' for size in sizes)
    color_buttons = ''
    for color in colors:
        preview = color_preview(product, color)
        swatch = SWATCHES.get(color, '#d3cdd0')
        selected = color == primary_color or bool(preview and preview == product['image'])
        preview_attr = f' data-preview-src="../{esc(preview)}"' if preview else ''
        photo_note = 'Photo available' if preview else 'Photo on request'
        color_buttons += f'<button type="button" class="color-option{ " active" if selected else "" }" data-option-color="{esc(color)}"{preview_attr} aria-pressed="{str(selected).lower()}"><span class="color-dot" style="background:{esc(swatch)}"></span><span class="color-label">{esc(color)}<small>{photo_note}</small></span></button>'
    options = f'''<div class="detail-options"><span>CHOOSE YOUR OPTIONS</span>{f'<div class="option-block"><strong>Size</strong><div class="size-options">{size_buttons}</div></div>' if sizes else ''}{f'<div class="option-block"><strong>Color</strong><div class="color-options">{color_buttons}</div><p class="color-image-status" id="color-image-status" aria-live="polite">Select a color to see its photo when available.</p></div>' if colors else ''}<p class="option-help">Listed options are subject to availability. Confirm fit and stock with Sherpa Quest Nepal.</p></div>''' if sizes or colors else ''
    facts = feature_rows(product)
    rows = ''.join(f'<tr><th scope="row">{esc(label)}</th><td>{esc(value)}</td></tr>' for label, value in facts)
    product_story = esc(story(product))
    highlights = ''.join(f'<li>{esc(value)}</li>' for value in feature_points(product))
    accordions = f'''<div class="product-accordions"><details open><summary>Product Details</summary><p>{product_story}</p></details><details><summary>Features</summary><ul>{highlights}</ul></details><details><summary>Specifications</summary><div class="spec-table"><table><tbody>{rows}</tbody></table></div></details></div>'''
    gallery = [{'src': product['image'], 'variant': 'Main view'}]
    gallery += [item for item in product.get('gallery', []) if item['src'] != product['image']]
    grouped = {}
    for index, item in enumerate(gallery):
        picture_color = gallery_color(product, item['src'], colors)
        group_name = picture_color or 'Other views'
        grouped.setdefault(group_name, []).append((index, item, picture_color))
    gallery_controls = ''
    if len(gallery) > 1:
        groups_html = ''
        for group_name, pictures in grouped.items():
            buttons = ''.join(f'<button type="button" class="product-thumb{ " active" if index == 0 else "" }" data-gallery-src="../{esc(item["src"])}" data-gallery-alt="{esc(product["name"])} — {esc(item["variant"])}" data-gallery-color="{esc(picture_color)}" aria-label="Show {esc(item["variant"])} image {index + 1}" aria-pressed="{str(index == 0).lower()}"><img src="../{esc(item["src"])}" alt="" loading="lazy"></button>' for index, item, picture_color in pictures)
            title = f'<strong>{esc(group_name)}</strong>' if colors and len(grouped) > 1 else ''
            groups_html += f'<div class="gallery-color-group" data-gallery-group="{esc(group_name)}">{title}<div class="product-thumbs" aria-label="{esc(group_name)} product images">{buttons}</div></div>'
        gallery_controls = f'<div class="gallery-groups">{groups_html}</div>'
    gallery_arrows = '<button type="button" class="gallery-arrow gallery-prev" aria-label="Previous product image">‹</button><button type="button" class="gallery-arrow gallery-next" aria-label="Next product image">›</button>' if len(gallery) > 1 else ''
    related_section = f'''<section class="related shell"><div class="section-head"><div><p class="eyebrow">KEEP EXPLORING</p><h2>RELATED <em>GEAR</em></h2></div></div><div class="related-grid">{''.join(card(item) for item in related)}</div></section>''' if related else ''
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0b0b0d"><meta name="description" content="Explore {esc(product['name'])} at Sherpa Quest Nepal. Ask about options and availability.">
<title>{esc(product['name'])} | Sherpa Quest Nepal</title>
<link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800;900&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../styles.css?v=3"><link rel="stylesheet" href="../product.css?v=3"><link rel="stylesheet" href="../theme.css?v=4"><script defer src="../navigation.js?v=5"></script><script defer src="../product-gallery.js?v=2"></script><script defer src="../floating-promo.js"></script><script defer src="../contact-form.js"></script></head>
<body data-root="../"><a class="skip" href="#main">Skip to content</a>{header}
<main id="main"><div class="product-page shell"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span>/</span><a href="{category_url}">{esc(product['category'])}</a><span>/</span><span>{esc(product['name'])}</span></nav>
<div class="product-layout"><div class="product-gallery"><div class="product-main-image" aria-label="Swipe to browse product images"><img id="product-main-image" src="../{esc(product['image'])}" data-primary-src="../{esc(product['image'])}" alt="{esc(product['name'])}">{gallery_arrows}</div>{gallery_controls}</div>
<div class="product-info"><p class="eyebrow"><a href="../index.html?brand={quote(product['brand'])}#products">{esc(brand_label)}</a> / {esc(product['category'])}</p><h1>{esc(product['name'])}</h1>
<p class="availability">Ask for price &amp; availability</p>{options}
<p class="product-summary">Choose a listed option, then message us for the latest stock and a fit check.</p>
<a class="button detail-whatsapp" id="product-inquiry" data-product-name="{esc(product['name'])}" href="{inquiry}" target="_blank" rel="noopener">ASK ABOUT THIS PRODUCT</a>
<a class="detail-call" href="tel:+9779744464587">Or call +977 974-4464587</a>
<div class="detail-service"><span>PRODUCT INQUIRIES</span><strong>We can help with sizes, fit and availability.</strong></div>{accordions}</div></div></div>{related_section}</main>
{contact}{footer}<a class="floating-chat" href="https://wa.me/9779744464587" target="_blank" rel="noopener" aria-label="Chat with Sherpa Quest Nepal on WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 11.6a8.5 8.5 0 0 1-12.4 7.5L3 20.5l1.4-5A8.5 8.5 0 1 1 20.5 11.6Z"/><path d="M8.7 8.2c-.4 0-.9.7-.8 1.4.1 1.4 2 4 4.3 5.2 1.5.8 2.7.7 3.3.1l.6-.8-2.1-1-1 .9a7.6 7.6 0 0 1-3-3.1l.8-.9-.9-1.9Z"/></svg><span>CHAT WITH US</span></a>
</body></html>'''
    (OUT / (product['id'] + '.html')).write_text(page)

print(f'Built {len(PRODUCTS)} product pages in {OUT}')
