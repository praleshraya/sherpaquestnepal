"""Import the supplied product workbook into a portable catalog JSON file."""
import json
import re
from hashlib import sha256
from io import BytesIO
from pathlib import Path

import openpyxl
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path('/Users/praleshrayamajhi/Downloads/SHERPA QUEST PRODUCT (2).xlsx')
OUT = ROOT / 'data' / 'products.json'
MEDIA = ROOT / 'assets' / 'products'

def clean(value):
    return re.sub(r'\s+', ' ', str(value or '')).strip()

def add(products, name, category, description='', image='', options='', brand=''):
    name = clean(name)
    if not name:
        return
    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    image = clean(image)
    products.append({
        'id': slug,
        'name': name,
        'category': category,
        'brand': brand or name.split()[0].upper(),
        'description': clean(description),
        'options': clean(options),
        'sourceImage': image,
        'image': f'assets/products/{slug}.jpg' if image else '',
    })

book = openpyxl.load_workbook(SOURCE, data_only=True)
products = []
sheet = book['HELMET AND LUGGAGE']
current = None
category = 'Helmets'
for row in sheet.values:
    name = clean(row[0] if len(row) > 0 else '')
    link = clean(row[1] if len(row) > 1 else '')
    if name == 'RHINOWALK LUGGAGE AND BAGS':
        category = 'Luggage & bags'
        continue
    if not link.startswith('http'):
        if current and not name and len(row) > 2 and row[2]:
            current['description'] += ' ' + clean(row[2])
        continue
    add(products, name, category, row[2] if len(row)>2 else '', link,
        ' | '.join(clean(v) for v in row[3:5] if v), 'ILM' if category == 'Helmets' else 'RHINOWALK')
    current = products[-1]

for row in book['RIDING GEARS'].values:
    if row and row[0] and len(row)>4 and clean(row[4]).startswith('http'):
        add(products, row[0], 'Riding jackets', row[2], row[4], row[1],
            'FEHER' if 'FEHER' in clean(row[0]).upper() else 'ILM')
for row in book['RAINSUIT'].values:
    if row and row[0] and len(row)>3 and clean(row[3]).startswith('http'):
        add(products, row[0], 'Rainwear', row[2], row[3], row[1],
            'FEHER' if 'FEHER' in clean(row[0]).upper() else 'ILM')

gloves = [row for row in book['GLOVES'].values if row and row[0]]
for row in gloves:
    add(products, row[0], 'Gloves', row[2] if len(row)>2 else '', '',
        row[1] if len(row)>1 else '', 'ILM' if 'ILM' in clean(row[0]).upper() else 'ALIEN MONSTER')

for row in book['BOOTS'].values:
    if row and row[0] and len(row)>3 and clean(row[3]).startswith('http'):
        add(products, row[0], 'Boots', row[2], row[3], row[1],
            'ILM' if 'ILM' in clean(row[0]).upper() else 'ARCX')
for row in book['INTERCOM'].values:
    if row and row[0] and len(row)>2 and clean(row[2]).startswith('http'):
        add(products, row[0], 'Intercom', row[1], row[2], '', clean(row[0]).split()[0].upper())

by_id = {product['id']: product for product in products}

def save_embedded(image, product, variant, sequence):
    raw = image._data()
    digest = sha256(raw).hexdigest()
    seen = product.setdefault('_seenImages', set())
    if digest in seen:
        return
    seen.add(digest)
    folder = MEDIA / product['id']
    folder.mkdir(parents=True, exist_ok=True)
    variant_slug = re.sub(r'[^a-z0-9]+', '-', variant.lower()).strip('-')[:55]
    destination = folder / f'{variant_slug}-{sequence:02d}.jpg'
    source = Image.open(BytesIO(raw))
    source.thumbnail((1200, 1200))
    if source.mode in ('RGBA', 'LA') or 'transparency' in source.info:
        rgba = source.convert('RGBA')
        photo = Image.new('RGB', rgba.size, 'white')
        photo.paste(rgba, mask=rgba.getchannel('A'))
    else:
        photo = source.convert('RGB')
    photo.save(destination, 'JPEG', quality=88, optimize=True)
    product.setdefault('gallery', []).append({
        'src': destination.relative_to(ROOT).as_posix(),
        'variant': variant,
    })

# The new workbook places helmet variant photos on a dedicated image sheet.
helmet_sheet = book['IMAGE OF HELMET']
variant_groups = [
    (1, 'ilm-ws-902-dual-sports-helmet', 'Matte black'),
    (60, 'ilm-ws-902-dual-sports-helmet', 'Blue white'),
    (89, 'ilm-902l-modular-helmet', 'Gloss black'),
    (151, 'ilm-902l-modular-helmet', 'Red grey'),
    (227, 'ilm-mf-568-full-face-helmet', 'Red blue'),
    (273, 'ilm-129-helmet', 'Gloss white'),
    (327, 'ilm-129-helmet', 'Matte black'),
    (377, 'ilm-mf-509-full-face', 'Gloss white'),
    (409, 'ilm-mf-509-full-face', 'Gloss black'),
    (458, 'ilm-mf-567-cobra-camelion-helmet', 'Cobra camelion'),
    (506, 'ilm-z-501-helmet', 'Armor red'),
    (571, 'ilm-606v-dual-sports-helmets', 'Black'),
    (609, 'ilm-mf-510-helmet', 'Sky grey'),
]
for image in helmet_sheet._images:
    row = image.anchor._from.row + 1
    match = next(((start, product_id, variant) for start, product_id, variant in reversed(variant_groups) if row >= start), None)
    if match and match[1] in by_id:
        product = by_id[match[1]]
        sequence = 1 + sum(item['variant'] == match[2] for item in product.get('gallery', []))
        save_embedded(image, product, match[2], sequence)

# Glove photos are anchored to the same row as their product name.
glove_sheet = book['GLOVES']
glove_products = [product for product in products if product['category'] == 'Gloves']
for image in glove_sheet._images:
    row = image.anchor._from.row
    index = row - 1
    if 0 <= index < len(glove_products):
        product = glove_products[index]
        sequence = len(product.get('gallery', [])) + 1
        save_embedded(image, product, 'Product view', sequence)
for product in glove_products:
    if product.get('gallery'):
        product['image'] = product['gallery'][0]['src']

brand_names = ('rhinowalk', 'arcx', 'feher', 'mjw', 'osah-drypak', 'alien-monster', 'rhinowalk-alt')
brand_folder = ROOT / 'assets' / 'brands'
brand_folder.mkdir(parents=True, exist_ok=True)
for image, name in zip(book['BRAND LOGOS']._images, brand_names):
    raw = image._data()
    extension = Image.open(BytesIO(raw)).format.lower().replace('jpeg', 'jpg')
    (brand_folder / f'{name}.{extension}').write_bytes(raw)

for product in products:
    product.pop('_seenImages', None)
OUT.parent.mkdir(exist_ok=True)
MEDIA.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(products, ensure_ascii=False, indent=2))
print(f'Imported {len(products)} products with {sum(len(p.get("gallery", [])) for p in products)} embedded images to {OUT}')
