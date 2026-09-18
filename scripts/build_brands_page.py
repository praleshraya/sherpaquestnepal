"""Build a browsable brand grid from the storefront's shared layout."""
from pathlib import Path
from urllib.parse import quote
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
index = (ROOT / 'index.html').read_text()
header = index[index.index('<div class="announcement">'):index.index('</header>') + len('</header>')]
footer = index[index.index('<footer class="footer">'):index.index('</footer>') + len('</footer>')]
contact = (ROOT / 'partials/contact.html').read_text()
for anchor in ('top', 'brands', 'contact', 'contact-us', 'categories', 'products'):
    header = header.replace(f'href="#{anchor}"', f'href="index.html#{anchor}"')
    footer = footer.replace(f'href="#{anchor}"', f'href="index.html#{anchor}"')
header = header.replace('href="index.html#contact-us"', 'href="#contact-us"')
section = index[index.index('<section class="brands"'):index.index('</section>', index.index('<section class="brands"')) + len('</section>')]
section = section.replace('class="brands"', 'class="brands brands-page"', 1)
section = section.replace('<a class="text-link" href="brands.html">VIEW ALL BRANDS</a>', '')
products = json.loads((ROOT / 'data/products.json').read_text())
brands = sorted({item['brand'] for item in products if item['brand'] != 'UNBRANDED'}, key=lambda brand: (brand not in ('ILM', 'RHINOWALK', 'ALIEN MONSTER'), brand))
logos = {'RHINOWALK':'rhinowalk.png','ALIEN MONSTER':'alien-monster.jpg','FEHER':'feher.jpg','ARCX':'arcx.jpg','MJW':'mjw.jpg','OSAH':'osah-drypak.jpg'}
cards = []
for brand in brands:
    mark = f'<img src="assets/brands/{logos[brand]}" alt="">' if brand in logos and (ROOT / 'assets/brands' / logos[brand]).exists() else escape(brand)
    cards.append(f'<a class="brand-tile" href="index.html?brand={quote(brand)}#products"><span class="brand-mark">{mark}</span><strong>{escape(brand)}</strong></a>')
start = section.index('<div class="brand-grid featured-brands">')
end = section.index('</div></div></section>', start)
section = section[:start] + '<div class="brand-grid">' + ''.join(cards) + section[end:]

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0b0b0d"><meta name="description" content="Explore the motorcycle gear brands carried by Sherpa Quest Nepal.">
<title>Our Brands | Sherpa Quest Nepal</title><link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800;900&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css?v=3"><link rel="stylesheet" href="theme.css?v=4"><script defer src="navigation.js?v=5"></script><script defer src="floating-promo.js"></script><script defer src="contact-form.js"></script></head>
<body><a class="skip" href="#main">Skip to content</a>{header}
<main id="main">{section}</main>{contact}{footer}
<a class="floating-chat" href="https://wa.me/9779744464587" target="_blank" rel="noopener" aria-label="Chat with Sherpa Quest Nepal on WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 11.6a8.5 8.5 0 0 1-12.4 7.5L3 20.5l1.4-5A8.5 8.5 0 1 1 20.5 11.6Z"/><path d="M8.7 8.2c-.4 0-.9.7-.8 1.4.1 1.4 2 4 4.3 5.2 1.5.8 2.7.7 3.3.1l.6-.8-2.1-1-1 .9a7.6 7.6 0 0 1-3-3.1l.8-.9-.9-1.9Z"/></svg><span>CHAT WITH US</span></a>
</body></html>'''
(ROOT / 'brands.html').write_text(page)
print('Built brands.html')
