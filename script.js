const CATEGORIES = ['All gear','Helmets','Luggage & bags','Riding jackets','Gloves','Boots','Rainwear','Intercom'];
const categoryImages = {
  'Helmets':'ilm-606v-dual-sports-helmets',
  'Luggage & bags':'rhinowalk-20ltr-tail-bag',
  'Riding jackets':'feher-ventilated-breathable-sj2311-riding-jacket-aeroflow',
  'Gloves':'alien-monster-preadator-evolution',
  'Boots':'arcx-l60612-urban-guard',
  'Intercom':'freedcon-fx',
};
const featuredIds = [
  'ilm-606v-dual-sports-helmets','rhinowalk-20ltr-tail-bag',
  'feher-ventilated-breathable-sj2311-riding-jacket-aeroflow',
  'alien-monster-preadator-evolution','arcx-l60612-urban-guard',
  'ilm-motorcycle-rain-suit-stormshield','freedcon-fx','rhinowalk-28ltr-saddle-bag'
];
const newArrivalIds = [
  'ilm-ws-902-dual-sports-helmet',
  'alien-monster-preadator-evolution',
  'feher-ventilated-breathable-sj2311-riding-jacket-aeroflow',
  'rhinowalk-20ltr-tail-bag'
];
const $ = selector => document.querySelector(selector);
const escapeHtml = value => String(value || '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const image = product => `<img src="${escapeHtml(product.image)}" alt="${escapeHtml(product.name)}" loading="lazy" onerror="this.onerror=null;this.src='assets/placeholder.svg'">`;
let products = [];
let category = 'All gear';
let brand = '';
let keyword = '';
let query = '';
let visible = 8;

function card(product) {
  const url = `products/${encodeURIComponent(product.id)}.html`;
  const alternate = product.gallery?.find(item => item.src !== product.image)?.src;
  const productImages = `<img class="product-primary" src="${escapeHtml(product.image)}" alt="${escapeHtml(product.name)}" loading="lazy" onerror="this.onerror=null;this.src='assets/placeholder.svg'">${alternate ? `<img class="product-hover" src="${escapeHtml(alternate)}" alt="" loading="lazy" onerror="this.remove()">` : ''}`;
  return `<article class="product-card"><a class="product-image${alternate ? ' has-alternate' : ''}" href="${url}" aria-label="View ${escapeHtml(product.name)}"><span class="product-tag">${escapeHtml(product.category.toUpperCase())}</span>${productImages}</a><a class="product-brand" href="index.html?brand=${encodeURIComponent(product.brand)}#products">${escapeHtml(product.brand)}</a><h3><a href="${url}">${escapeHtml(product.name)}</a></h3><a class="product-action" href="${url}">VIEW DETAILS</a></article>`;
}
function renderCategories() {
  const featured = ['Helmets','Luggage & bags','Riding jackets','Gloves','Boots','Intercom'];
  $('#category-grid').innerHTML = featured.map(name => {
    const product = products.find(item => item.id === categoryImages[name]);
    return `<a class="category-card" href="#products" data-category="${escapeHtml(name)}"><div class="category-image">${image(product)}</div><h3>${escapeHtml(name)}</h3></a>`;
  }).join('');
}
function renderNewArrivals() {
  const grid = $('#new-arrivals-grid');
  if (!grid) return;
  grid.innerHTML = newArrivalIds.map(id => products.find(item => item.id === id)).filter(Boolean).map(card).join('');
  const count = $('#assurance-product-count');
  const brands = $('#assurance-brand-count');
  if (count) count.textContent = String(products.length);
  if (brands) brands.textContent = String(new Set(products.map(product => product.brand)).size);
}
function renderFilters() {
  $('#filters').innerHTML = CATEGORIES.map(name => `<button class="filter${name === category ? ' active' : ''}" type="button" data-filter="${escapeHtml(name)}" aria-pressed="${name === category}">${escapeHtml(name)}</button>`).join('');
}
function renderProducts() {
  const matches = products.filter(product =>
    (category === 'All gear' || product.category === category) &&
    (!brand || product.brand.toLowerCase() === brand.toLowerCase()) &&
    (!keyword || product.name.toLowerCase().includes(keyword)) &&
    (!query || `${product.name} ${product.brand} ${product.category} ${product.description}`.toLowerCase().includes(query))
  );
  $('#product-grid').innerHTML = matches.slice(0, visible).map(card).join('');
  $('#product-count').textContent = `${matches.length} PRODUCTS${brand ? ` · ${brand.toUpperCase()}` : ''}${keyword ? ` · ${keyword.toUpperCase()}` : ''}`;
  $('#load-more').hidden = matches.length <= visible;
  $('#no-results').hidden = matches.length !== 0;
  renderFilters();
}
function setCategory(name) {
  category = name;
  brand = '';
  keyword = '';
  query = '';
  visible = 8;
  $('#search').value = '';
  renderProducts();
}
document.addEventListener('click', event => {
  const categoryLink = event.target.closest('[data-category]');
  if (categoryLink && categoryLink.closest('#category-grid, .wide-promo')) setCategory(categoryLink.dataset.category);
  const filter = event.target.closest('[data-filter]');
  if (filter) setCategory(filter.dataset.filter);
});
$('#search').addEventListener('input', () => { if ($('#search').value === '' && query) { query = ''; renderProducts(); } });
$('#load-more').addEventListener('click', () => { visible += 8; renderProducts(); });
fetch('data/products.json').then(response => response.json()).then(data => {
  products = data.sort((a,b) => {
    const ai = featuredIds.indexOf(a.id), bi = featuredIds.indexOf(b.id);
    return (ai < 0 ? 999 : ai) - (bi < 0 ? 999 : bi);
  });
  const params = new URLSearchParams(location.search);
  const selected = params.get('category');
  if (selected && CATEGORIES.includes(selected)) category = selected;
  brand = params.get('brand') || '';
  keyword = (params.get('keyword') || '').toLowerCase();
  query = (params.get('search') || '').toLowerCase();
  if (query) $('#search').value = params.get('search');
  renderCategories();
  renderNewArrivals();
  renderProducts();
}).catch(() => { $('#product-grid').innerHTML = '<p>Products are temporarily unavailable. Please contact us on WhatsApp for help.</p>'; if ($('#new-arrivals-grid')) $('#new-arrivals-grid').innerHTML = '<p>Ask us about the latest gear on WhatsApp.</p>'; });
