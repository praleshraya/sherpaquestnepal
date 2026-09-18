/* Shared storefront navigation for the home page and individual product pages. */
(() => {
  const root = document.body.dataset.root || '';
  const header = document.querySelector('.site-header');
  const nav = document.querySelector('#nav');
  const panel = document.querySelector('#mega-panel');
  const toggle = document.querySelector('#menu-toggle');
  if (!header || !nav || !panel || !toggle) return;

  const menus = {
    gear: [
      {name:'Riding gears', cards:[
        ['Helmets','Helmets','','ilm-606v-dual-sports-helmets'],
        ['Riding jackets','Riding jackets','','feher-ventilated-breathable-sj2311-riding-jacket-aeroflow'],
        ['Gloves','Gloves','','alien-monster-preadator-evolution'],
        ['Boots','Boots','','arcx-l60612-urban-guard']]},
      {name:'Luggage & bagpacks', cards:[
        ['Luggage & bagpacks','Luggage & bags','','rhinowalk-20ltr-tail-bag'],
        ['Rainwear','Rainwear','','ilm-motorcycle-rain-suit-stormshield'],
        ['Intercom','Intercom','','freedcon-fx']]}
    ],
    accessories: [
      {name:'Motorcycle storage', cards:[
        ['Tail bags','Luggage & bags','tail bag','rhinowalk-20ltr-tail-bag'],
        ['Saddle bags','Luggage & bags','saddle','rhinowalk-28ltr-saddle-bag'],
        ['Tank bags','Luggage & bags','tank bag','mechanic-series-9l-motorcycle-tank-bag-with-1-5l-hydration-bladder'],
        ['Backpacks','Luggage & bags','backpack','rhinowalk-mechanic-series-23l-motorcycle-riding-backpack']]},
      {name:'Ride utilities', cards:[
        ['Intercoms','Intercom','','freedcon-fx'],
        ['Crash bar bags','Luggage & bags','crash bar','mechanic-series-6l-motorcycle-crash-bar-bag-with-waterproof-liner'],
        ['Tool rolls','Luggage & bags','tool roll','motorcycle-tool-roll-bag-black']]}
    ],
    riding: [
      {name:'Riding jackets, gloves & boots', cards:[
        ['Riding jackets','Riding jackets','','feher-ventilated-breathable-sj2311-riding-jacket-aeroflow'],
        ['Gloves','Gloves','','alien-monster-preadator-evolution'],
        ['Boots','Boots','','arcx-l60612-urban-guard']]},
      {name:'Rainwear', cards:[
        ['Rainwear','Rainwear','','ilm-motorcycle-rain-suit-stormshield'],
        ['All-season jackets','Riding jackets','all-season','feher-jk-033a-terrain-all-season-2-layer-motor-cycle-riding-jacket']]}
    ],
    luggage: [
      {name:'Bags and backpacks', cards:[
        ['Saddle bags','Luggage & bags','saddle','rhinowalk-28ltr-saddle-bag'],
        ['Backpacks','Luggage & bags','backpack','rhinowalk-mechanic-series-23l-motorcycle-riding-backpack'],
        ['Tank bags','Luggage & bags','tank bag','mechanic-series-9l-motorcycle-tank-bag-with-1-5l-hydration-bladder'],
        ['Tail bags','Luggage & bags','tail bag','rhinowalk-20ltr-tail-bag']]},
      {name:'Touring accessories', cards:[
        ['Crash bar bags','Luggage & bags','crash bar','mechanic-series-6l-motorcycle-crash-bar-bag-with-waterproof-liner'],
        ['Tool rolls','Luggage & bags','tool roll','motorcycle-tool-roll-bag-black'],
        ['All luggage','Luggage & bags','','rhinowalk-20ltr-tail-bag']]}
    ],
    helmets: [
      {name:'Helmet styles', cards:[
        ['Dual sport','Helmets','dual sport','ilm-606v-dual-sports-helmets'],
        ['Full face','Helmets','full face','ilm-mf-568-full-face-helmet'],
        ['Modular','Helmets','modular','ilm-902l-modular-helmet']]},
      {name:'Helmet essentials', cards:[
        ['All helmets','Helmets','','ilm-606v-dual-sports-helmets'],
        ['Intercoms','Intercom','','freedcon-fx']]}
    ]
  };
  const escapeHtml = value => String(value || '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const catalogUrl = (category, keyword) => `${root}index.html?category=${encodeURIComponent(category)}${keyword ? `&keyword=${encodeURIComponent(keyword)}` : ''}#products`;
  let products = [];
  let activeMenu = '';
  let activeGroup = 0;
  fetch(`${root}data/products.json`).then(r => r.json()).then(data => { products = data; if (activeMenu) renderPanel(); }).catch(() => {});

  function renderPanel() {
    const groups = menus[activeMenu];
    if (!groups) return;
    const cards = groups[activeGroup].cards;
    panel.innerHTML = `<div class="mega-sidebar" role="group" aria-label="Subcategories">${groups.map((group, index) => `<button type="button" class="mega-group${index === activeGroup ? ' active' : ''}" data-menu-group="${index}" aria-pressed="${index === activeGroup}">${escapeHtml(group.name)}</button>`).join('')}</div><div class="mega-tiles">${cards.map(([label, category, keyword, imageId]) => {
      const product = products.find(item => item.id === imageId) || products.find(item => item.category === category);
      const image = product ? `${root}${product.image}` : `${root}assets/placeholder.svg`;
      return `<div class="mega-tile"><a class="mega-tile-link" href="${catalogUrl(category, keyword)}"><span class="mega-tile-image"><img src="${escapeHtml(image)}" alt="" loading="lazy"></span><span class="mega-tile-label">${escapeHtml(label)}</span></a>${product ? `<a class="mega-product-link" href="${root}products/${encodeURIComponent(product.id)}.html" aria-label="View ${escapeHtml(product.name)}" title="View ${escapeHtml(product.name)}">+</a>` : ''}</div>`;
    }).join('')}</div>`;
  }
  function closeMenu() {
    activeMenu = '';
    panel.hidden = true;
    panel.innerHTML = '';
    nav.append(panel);
    header.classList.remove('menu-open');
    nav.classList.remove('open');
    toggle.setAttribute('aria-expanded','false');
    toggle.setAttribute('aria-label','Open menu');
    document.querySelectorAll('.nav-trigger').forEach(button => button.setAttribute('aria-expanded','false'));
  }
  function openMenu(name) {
    if (activeMenu === name) { closeMenu(); return; }
    activeMenu = name;
    activeGroup = 0;
    document.querySelector(`[data-menu="${name}"]`).after(panel);
    renderPanel();
    panel.hidden = false;
    header.classList.add('menu-open');
    nav.classList.add('open');
    toggle.setAttribute('aria-expanded','true');
    toggle.setAttribute('aria-label','Close menu');
    document.querySelectorAll('.nav-trigger').forEach(button => button.setAttribute('aria-expanded', String(button.dataset.menu === name)));
  }
  document.addEventListener('click', event => {
    const trigger = event.target.closest('[data-menu]');
    if (trigger) { openMenu(trigger.dataset.menu); return; }
    const group = event.target.closest('[data-menu-group]');
    if (group) { activeGroup = Number(group.dataset.menuGroup); renderPanel(); return; }
    if (!event.target.closest('.site-header')) closeMenu();
  });
  toggle.addEventListener('click', () => {
    if (header.classList.contains('menu-open')) closeMenu();
    else { header.classList.add('menu-open'); nav.classList.add('open'); toggle.setAttribute('aria-expanded','true'); toggle.setAttribute('aria-label','Close menu'); }
  });
  nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
  document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });
  function updateScrollNavigation() {
    const away = window.innerWidth > 760 && window.scrollY > 52;
    if (away && activeMenu) closeMenu();
    header.classList.toggle('nav-away', away);
  }
  window.addEventListener('scroll', updateScrollNavigation, {passive:true});
  window.addEventListener('resize', updateScrollNavigation);
  updateScrollNavigation();
  const searchForm = document.querySelector('#search-form');
  searchForm?.addEventListener('submit', event => {
    event.preventDefault();
    const query = document.querySelector('#search').value.trim();
    location.href = `${root}index.html${query ? `?search=${encodeURIComponent(query)}` : ''}#products`;
  });
  const year = document.querySelector('#year');
  if (year) year.textContent = new Date().getFullYear();
})();
