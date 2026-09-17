"""Save the workbook's linked product photos as local JPEGs."""
import io
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / 'data/products.json').read_text())

def save(product):
    if not product['sourceImage']:
        return product['name'], 'embedded'
    dest = ROOT / product['image']
    if dest.exists():
        return product['name'], 'exists'
    req = urllib.request.Request(product['sourceImage'], headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            raw = response.read()
        image = Image.open(io.BytesIO(raw)).convert('RGB')
        image.thumbnail((1000, 1000))
        image.save(dest, 'JPEG', quality=85, optimize=True)
        return product['name'], 'saved'
    except Exception as error:
        return product['name'], f'failed: {error}'

with ThreadPoolExecutor(max_workers=8) as pool:
    for result in as_completed([pool.submit(save, p) for p in catalog]):
        print(*result.result(), sep=' | ')
