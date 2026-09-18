"""Build a riding gallery page with the storefront's shared header and footer."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
index = (ROOT / 'index.html').read_text()
header = index[index.index('<div class="announcement">'):index.index('</header>') + len('</header>')]
footer = index[index.index('<footer class="footer">'):index.index('</footer>') + len('</footer>')]
contact = (ROOT / 'partials/contact.html').read_text()
for anchor in ('top', 'brands', 'contact', 'contact-us', 'categories', 'products'):
    header = header.replace(f'href="#{anchor}"', f'href="index.html#{anchor}"')
    footer = footer.replace(f'href="#{anchor}"', f'href="index.html#{anchor}"')
header = header.replace('href="index.html#contact-us"', 'href="#contact-us"')

cards = [
    ('assets/banners/high-pass-road.webp', 'A motorcycle parked beside a mountain road', 'THE HIGH PASS', 'Long roads, wider horizons.', 'index.html?category=Luggage%20%26%20bags#products'),
    ('assets/products/ilm-ws-902-dual-sports-helmet/matte-black-06.jpg', 'Helmeted rider with an adventure motorcycle in the mountains', 'MOUNTAIN MILES', 'Adventure gear in its element.', 'products/ilm-ws-902-dual-sports-helmet.html'),
    ('assets/banners/green-valley-road.webp', 'Motorcyclist riding on a valley road', 'THE VALLEY ROUTE', 'The journey is part of the destination.', 'index.html#products'),
    ('assets/products/ilm-ws-902-dual-sports-helmet/matte-black-05.jpg', 'Helmeted rider standing beside a motorcycle', 'TRAIL READY', 'Built for the routes beyond the city.', 'products/ilm-ws-902-dual-sports-helmet.html'),
    ('assets/products/ilm-ws-902-dual-sports-helmet/matte-black-08.jpg', 'Close view of a rider wearing a motorcycle helmet', 'RIDER FOCUS', 'Every detail matters on the road.', 'products/ilm-ws-902-dual-sports-helmet.html'),
    ('assets/banners/golden-ridge-road.webp', 'Open mountain road in Nepal', 'WHAT LIES AHEAD', 'Find your next line through the hills.', 'index.html#products'),
]
gallery = ''.join(f'''<a class="rider-card" href="{url}"><img src="{image}" alt="{alt}" loading="lazy"><span class="rider-card-shade"></span><span class="rider-card-copy"><small>RIDE INSPIRATION</small><strong>{title}</strong><span>{caption}</span></span></a>''' for image, alt, title, caption, url in cards)

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0b0b0d"><meta name="description" content="Explore riding inspiration, routes and gear with Sherpa Quest Nepal.">
<title>From Our Riders | Sherpa Quest Nepal</title><link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800;900&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css?v=3"><link rel="stylesheet" href="theme.css?v=4"><link rel="stylesheet" href="riders.css?v=1"><script defer src="navigation.js?v=5"></script><script defer src="floating-promo.js"></script><script defer src="contact-form.js"></script></head>
<body><a class="skip" href="#main">Skip to content</a>{header}
<main id="main"><section class="riders-hero"><div class="shell"><p class="eyebrow light">SHERPA QUEST NEPAL / ROAD STORIES</p><h1>FROM OUR<br><em>RIDERS.</em></h1><p>Riding inspiration for the journeys ahead. Explore the places and gear that keep us moving.</p></div></section>
<section class="riders-gallery shell" aria-label="Riding inspiration gallery"><div class="section-head"><div><p class="eyebrow">THE ROAD IS CALLING</p><h2>MOMENTS FROM <em>THE RIDE</em></h2></div></div><div class="rider-grid">{gallery}</div></section>
<section class="riders-share"><div class="shell riders-share-inner"><div><p class="eyebrow light">JOIN THE JOURNEY</p><h2>SHARE YOUR<br><em>NEXT RIDE.</em></h2><p>Tag Sherpa Quest Nepal on Instagram to show us where your gear takes you.</p></div><a href="https://www.instagram.com/sherpaquest4adventure/" target="_blank" rel="noopener noreferrer">VISIT OUR INSTAGRAM</a></div></section></main>{contact}{footer}
<a class="floating-chat" href="https://wa.me/9779744464587" target="_blank" rel="noopener" aria-label="Chat with Sherpa Quest Nepal on WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 11.6a8.5 8.5 0 0 1-12.4 7.5L3 20.5l1.4-5A8.5 8.5 0 1 1 20.5 11.6Z"/><path d="M8.7 8.2c-.4 0-.9.7-.8 1.4.1 1.4 2 4 4.3 5.2 1.5.8 2.7.7 3.3.1l.6-.8-2.1-1-1 .9a7.6 7.6 0 0 1-3-3.1l.8-.9-.9-1.9Z"/></svg><span>CHAT WITH US</span></a>
</body></html>'''
(ROOT / 'riders.html').write_text(page)
print('Built riders.html')
