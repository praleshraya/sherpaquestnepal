"""Build the About Us page using the storefront's shared header and footer."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
index = (ROOT / 'index.html').read_text()
header = index[index.index('<div class="announcement">'):index.index('</header>') + len('</header>')]
footer = index[index.index('<footer class="footer">'):index.index('</footer>') + len('</footer>')]
for anchor in ('top', 'brands', 'contact', 'categories', 'products'):
    header = header.replace(f'href="#{anchor}"', f'href="index.html#{anchor}"')
    footer = footer.replace(f'href="#{anchor}"', f'href="index.html#{anchor}"')

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#215c48"><meta name="description" content="Get to know Sherpa Quest Nepal, a Nepal-based destination for motorcycle riding gear, helmets, luggage and off-road accessories.">
<title>About Us | Sherpa Quest Nepal</title><link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800;900&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="about.css"><script defer src="navigation.js"></script></head>
<body><a class="skip" href="#main">Skip to content</a>{header}
<main id="main">
  <section class="about-hero"><img src="assets/sherpa-hero.png" alt="Motorcyclist riding through a mountain landscape in Nepal"><div class="about-hero-shade"></div><div class="shell about-hero-copy"><p class="eyebrow light">SHERPA QUEST NEPAL</p><h1>GEAR FOR THE<br><em>JOURNEY.</em></h1><p>Riding gear, touring essentials and off-road accessories for the roads ahead.</p></div></section>
  <section class="about-story shell"><div><p class="eyebrow">ABOUT US</p><h2>BUILT AROUND<br><em>THE RIDE.</em></h2></div><div class="about-story-copy"><p>Sherpa Quest Nepal brings together motorcycle gear and accessories for riders exploring Nepal and beyond. Our catalog covers helmets, jackets, gloves, boots, rainwear, intercoms, and luggage for everyday trips and longer journeys.</p><p>We make it easy to explore product details and ask about fit, options and availability before choosing gear for your next ride.</p></div></section>
  <section class="about-categories"><div class="shell"><p class="eyebrow">WHAT YOU WILL FIND</p><h2>READY FOR YOUR<br><em>NEXT ROUTE.</em></h2><div class="about-category-grid"><a href="index.html?category=Helmets#products">HELMETS <span>↗</span></a><a href="index.html?category=Riding%20jackets#products">RIDING JACKETS <span>↗</span></a><a href="index.html?category=Gloves#products">GLOVES <span>↗</span></a><a href="index.html?category=Boots#products">BOOTS <span>↗</span></a><a href="index.html?category=Luggage%20%26%20bags#products">LUGGAGE &amp; BAGPACKS <span>↗</span></a><a href="index.html?category=Rainwear#products">RAINWEAR <span>↗</span></a></div></div></section>
  <section class="about-connection shell"><div><p class="eyebrow">RIDE WITH US</p><h2>LET'S FIND<br><em>YOUR GEAR.</em></h2><p>Have a question about a product, size, or availability? Get in touch with Sherpa Quest Nepal.</p></div><div class="about-contact-links"><a href="tel:+9779744464587"><small>CALL US</small><strong>+977 974-4464587</strong><span>↗</span></a><a href="mailto:sherpaquestoffroad@gmail.com"><small>EMAIL US</small><strong>sherpaquestoffroad@gmail.com</strong><span>↗</span></a><a href="https://wa.me/9779744464587" target="_blank" rel="noopener"><small>MESSAGE US</small><strong>WhatsApp Sherpa Quest Nepal</strong><span>↗</span></a></div></section>
</main>{footer}
<a class="floating-chat" href="https://wa.me/9779744464587" target="_blank" rel="noopener" aria-label="Chat with Sherpa Quest Nepal on WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 11.6a8.5 8.5 0 0 1-12.4 7.5L3 20.5l1.4-5A8.5 8.5 0 1 1 20.5 11.6Z"/><path d="M8.7 8.2c-.4 0-.9.7-.8 1.4.1 1.4 2 4 4.3 5.2 1.5.8 2.7.7 3.3.1l.6-.8-2.1-1-1 .9a7.6 7.6 0 0 1-3-3.1l.8-.9-.9-1.9Z"/></svg><span>CHAT WITH US</span></a>
</body></html>'''
(ROOT / 'about.html').write_text(page)
print('Built about.html')
