# Sherpa Quest Nepal storefront

This is a static storefront prototype inspired by the layout pattern of [Autonity](https://autonity.in/), with original Sherpa Quest branding and imagery. It is designed to become a WordPress theme or WooCommerce storefront later. No WordPress installation is needed to review it locally.

## Preview

Run `python3 -m http.server 4173` from this folder and open `http://localhost:4173/`. A local server is needed because the catalog is loaded from `data/products.json`.

## Content and assets

- `index.html`, `styles.css`, and `script.js` contain the site structure, styling, and catalog interactions.
- `carousel.css` and `carousel.js` provide two responsive, keyboard accessible homepage carousels with arrows, dots, autoplay, and pause on hover or focus. The first links each featured product to its own page; the helmet carousel links to the filtered helmet collection.
- `assets/banners/` contains three bright original scenic backgrounds for the featured carousel. Product cutouts come from the local catalog images. The promotional cards below the first carousel link to helmet, jacket, and luggage collections.
- `navigation.js` powers the shared sticky header and image-tile dropdown menus.
- `products/` contains one standalone HTML page for each product, with its own URL, details, inquiry link, and related gear. Run `python3 scripts/build_product_pages.py` after changing the catalog or shared header to refresh these pages.
- `about.html` is the standalone About Us page. Run `python3 scripts/build_about_page.py` after changing the shared header or footer.
- `product.css` styles individual product pages.
- `data/products.json` contains 55 products imported from `SHERPA QUEST PRODUCT (2).xlsx`. It retains product names, categories, descriptions, available options, brand, original source-image URL, and available image galleries.
- `assets/products/` contains local copies of the workbook-linked images. The supplied transparent Alien Monster glove photos are stored in its product folder. The catalog uses light-background variants and excludes dark-background gallery views; source files remain in the asset folders for reference.
- `assets/brands/` contains the embedded brand logos from the updated workbook; matching logos appear in the homepage brand strip.
- `assets/sherpa-hero.png` is original artwork created for this site.
- `assets/sherpa-quest-logo.png` is the logo supplied by Sherpa Quest Nepal.
- `scripts/import_workbook.py` rebuilds the catalog and extracts embedded photos from the updated workbook path. `scripts/download_product_images.py` saves externally linked product images locally. After reimporting, run `python3 scripts/curate_product_images.py` and then `python3 scripts/build_product_pages.py` to restore the selected light imagery and product pages.

The workbook contains no product prices, inventory levels, checkout rules, or delivery policies, so the storefront uses product inquiries instead of a cart or checkout. Confirm product claims, stock, and variants before publishing commercially.

The logo, search and action row stays sticky while the desktop menu row fades away on scroll. On narrow screens the menu row collapses to a hamburger control. Dropdown tile labels lead to filtered catalog views; their plus links open the pictured product page. The Instagram button alternates between Follow and a static follower snapshot; refresh that number periodically.

The black, white and red palette is defined in `theme.css`. Product page stories, feature rows, sizes, color labels and photo mappings live in `scripts/product_content.py`; running `python3 scripts/build_product_pages.py` regenerates all product pages after a content change. Color choices switch to a matching local photo when one is available, and the inquiry message includes the selected size and color.

Product pages now show the short story, feature highlights and specifications in collapsible sections beside the gallery. Catalog cards and related cards show a second local photo on hover when available. The Brands navigation opens `brands.html`, and brand tiles lead to a filtered product grid. The floating, muted video promotion uses `floating_ad_promotion_video.mov`; visitors can close it for the current browser session. Regenerate the auxiliary pages with `python3 scripts/build_about_page.py` and `python3 scripts/build_brands_page.py` after changing shared navigation or brand tiles.

The homepage places assurance cards, a curated New Arrivals row, and Shop by Luggage tiles directly after the main carousel. The product and brand counts in the assurance panel are calculated from `data/products.json` in `script.js`. Arrival tiles use selected existing catalog products; confirm which items are truly new before publishing.

## WordPress migration

Use this folder as the design source. The HTML sections map to WordPress template parts: header, hero, categories, product loop, brands, contact, and footer. CSS is plain and framework independent. Import `data/products.json` into WooCommerce products or a product custom post type, then upload images from `assets/products/` into the WordPress media library. Replace the JavaScript catalog render with WordPress queries while keeping the same class names and styles. Configure prices, inventory, payments, shipping, and policies in WordPress when those details are available.
