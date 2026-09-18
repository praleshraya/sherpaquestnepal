"""Build a browsable brand grid from the storefront's shared layout."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
index = (ROOT / 'index.html').read_text()
header = index[index.index('<div class="announcement">'):index.index('</header>') + len('</header>')]
footer = index[index.index('<footer class="footer">'):index.index('</footer>') + len('</footer>')]
for anchor in ('top', 'brands', 'contact', 'categories', 'products'):
    header = header.replace(f'href="#{anchor}"', f'href="index.html#{anchor}"')
    footer = footer.replace(f'href="#{anchor}"', f'href="index.html#{anchor}"')
section = index[index.index('<section class="brands"'):index.index('</section>', index.index('<section class="brands"')) + len('</section>')]
section = section.replace('class="brands"', 'class="brands brands-page"', 1)
section = section.replace('<a class="text-link" href="brands.html">VIEW ALL BRANDS</a>', '')

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0b0b0d"><meta name="description" content="Explore the motorcycle gear brands carried by Sherpa Quest Nepal.">
<title>Our Brands | Sherpa Quest Nepal</title><link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800;900&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css?v=3"><link rel="stylesheet" href="theme.css?v=2"><script defer src="navigation.js?v=3"></script><script defer src="floating-promo.js"></script></head>
<body><a class="skip" href="#main">Skip to content</a>{header}
<main id="main">{section}</main>{footer}
<a class="floating-chat" href="https://wa.me/9779744464587" target="_blank" rel="noopener" aria-label="Chat with Sherpa Quest Nepal on WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 11.6a8.5 8.5 0 0 1-12.4 7.5L3 20.5l1.4-5A8.5 8.5 0 1 1 20.5 11.6Z"/><path d="M8.7 8.2c-.4 0-.9.7-.8 1.4.1 1.4 2 4 4.3 5.2 1.5.8 2.7.7 3.3.1l.6-.8-2.1-1-1 .9a7.6 7.6 0 0 1-3-3.1l.8-.9-.9-1.9Z"/></svg><span>CHAT WITH US</span></a>
</body></html>'''
(ROOT / 'brands.html').write_text(page)
print('Built brands.html')
