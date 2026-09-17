"""Prefer light catalog imagery and the supplied transparent glove photos.

Run after importing the workbook, then rebuild product pages.
Original source files stay in assets/products for reference.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
catalog_path = ROOT / 'data/products.json'
products = json.loads(catalog_path.read_text())

preferred = {
    'ilm-606v-dual-sports-helmets': 'black-01.jpg',
    'ilm-ws-902-dual-sports-helmet': 'blue-white-01.jpg',
    'ilm-902l-modular-helmet': 'gloss-black-01.jpg',
    'ilm-mf-509-full-face': 'gloss-white-01.jpg',
    'ilm-mf-567-cobra-camelion-helmet': 'cobra-camelion-01.jpg',
    'ilm-z-501-helmet': 'armor-red-01.jpg',
    'ilm-mf-510-helmet': 'sky-grey-01.jpg',
    'alien-monter-howl-classic-glove': 'product-view-02.jpg',
}
dark_views = {
    'ilm-ws-902-dual-sports-helmet': {'matte-black-02.jpg', 'matte-black-03.jpg'},
    'ilm-902l-modular-helmet': {'gloss-black-05.jpg', 'gloss-black-06.jpg', 'gloss-black-08.jpg', 'red-grey-09.jpg', 'red-grey-10.jpg'},
    'ilm-mf-509-full-face': {'gloss-white-05.jpg'},
    'ilm-mf-510-helmet': {'sky-grey-10.jpg', 'sky-grey-11.jpg', 'sky-grey-12.jpg'},
    'alien-monter-howl-classic-glove': {'product-view-01.jpg'},
}

for product in products:
    product_id = product['id']
    if product_id == 'alien-monster-preadator-evolution':
        folder = f'assets/products/{product_id}'
        product['image'] = f'{folder}/sand-gloves.png'
        product['gallery'] = [
            {'src': f'{folder}/sand-gloves.png', 'variant': 'White'},
            {'src': f'{folder}/olive-gloves.png', 'variant': 'Green'},
        ]
        continue
    product['gallery'] = [
        view for view in product.get('gallery', [])
        if Path(view['src']).name not in dark_views.get(product_id, set())
    ]
    if product_id in preferred:
        product['image'] = f'assets/products/{product_id}/{preferred[product_id]}'

catalog_path.write_text(json.dumps(products, indent=2, ensure_ascii=False) + '\n')
print('Updated featured product imagery and removed dark gallery views from the catalog.')
