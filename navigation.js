/* Shared storefront navigation for the home page and individual product pages. */
(() => {
  const root = document.body.dataset.root || '';
  const header = document.querySelector('.site-header');
  const nav = document.querySelector('#nav');
  const panel = document.querySelector('#mega-panel');
  const toggle = document.querySelector('#menu-toggle');
  if (!header || !nav || !panel || !toggle) return;

  const menus = {
    accessories: [
      {name:'Cleaning Products', cards:[
        ['Cleaning Products',null,null,null]]},
      {name:'Roadside Kit', cards:[
        ['Roadside Kit',null,null,null]]}
    ],
    riding: [
      {name:'Riding Gears',hideSidebar:true,cards:[
        ['Jackets','Riding jackets','','feher-ventilated-breathable-sj2311-riding-jacket-aeroflow'],
        ['Pants',null,null,null],
        ['Gloves','Gloves','','alien-monster-preadator-evolution'],
        ['Boots','Boots','','arcx-l60612-urban-guard'],
        ['Knee Guards','Knee & elbow guards','knee','kp16ep16-mx-knee-elbow-guard'],
        ['Elbow Guards','Knee & elbow guards','elbow','kp101ep01-knee-elbow-guard']]}
    ],
    luggage: [
      {name:'Bags and Backpacks', cards:[
        ['Duffle Bags','Luggage & bags','duffel','warrior-series-waterproof-motorcycle-duffel-bag-40l'],
        ['Dry Pak','Luggage & bags','drypak','osah-20l-drypak'],
        ['Hydration Bags','Luggage & bags','hydration','osah-outrider-hydration-bag'],
        ['Pioneer Bags',null,null,null]]},
      {name:'Touring accessories', cards:[
        ['Toolsets',null,null,null],
        ['Med Kit / First-Aid Bags',null,null,null],
        ['Tool Rolls','Luggage & bags','tool roll','motorcycle-tool-roll-bag-black'],
        ['Bottle Holder','Luggage & bags','bottle holder','rhinowalk-1-5ltr-motorcycle-bottle-holder']]}
    ],
    helmets: [
      {name:'Helmets', cards:[
        ['Full Face','Helmets','full face','ilm-mf-568-full-face-helmet'],
        ['Modular','Helmets','modular','ilm-902l-modular-helmet'],
        ['Dual Sports Helmets','Helmets','dual sport','ilm-606v-dual-sports-helmets']]},
      {name:'Rider Tech', cards:[
        ['Intercom','Intercom','','freedcon-fx'],
        ['Navigation',null,null,null],
        ['Phone Holder','Phone holders','','mh01-traillock-pro-phone-mount'],
        ['Tyre Inflater',null,null,null]]}
    ],
    topbox: [
      {name:'Aluminum Top Box', cards:[['Aluminum Top Box',null,null,null]]},
      {name:'Pioneer Box', cards:[['Pioneer Box',null,null,null]]}
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
    const group = groups[activeGroup];
    const cards = group.cards;
    panel.dataset.currentMenu = activeMenu;
    panel.classList.toggle('no-sidebar', Boolean(group.hideSidebar));
    const sidebar = group.hideSidebar ? '' : `<div class="mega-sidebar" role="group" aria-label="Subcategories">${groups.map((item, index) => `<button type="button" class="mega-group${index === activeGroup ? ' active' : ''}" data-menu-group="${index}" aria-pressed="${index === activeGroup}">${escapeHtml(item.name)}</button>`).join('')}</div>`;
    panel.innerHTML = `${sidebar}<div class="mega-tiles">${cards.map(([label, category, keyword, imageId]) => {
      const product = imageId ? products.find(item => item.id === imageId) : null;
      const destination = product ? catalogUrl(category, keyword) : `https://wa.me/9779744464587?text=${encodeURIComponent(`Hello Sherpa Quest Nepal, I'd like to ask about ${label}.`)}`;
      const visual = product ? `<img src="${escapeHtml(root + product.image)}" alt="" loading="lazy">` : `<span class="mega-empty-mark" aria-hidden="true">SQ</span><small>ASK AVAILABILITY</small>`;
      return `<div class="mega-tile${product ? '' : ' mega-tile-inquiry'}"><a class="mega-tile-link" href="${destination}"${product ? '' : ' target="_blank" rel="noopener"'}><span class="mega-tile-image">${visual}</span><span class="mega-tile-label">${escapeHtml(label)}</span></a>${product ? `<a class="mega-product-link" href="${root}products/${encodeURIComponent(product.id)}.html" aria-label="View ${escapeHtml(product.name)}" title="View ${escapeHtml(product.name)}">+</a>` : ''}</div>`;
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
    const away = window.scrollY > 52;
    if (away && (activeMenu || header.classList.contains('menu-open'))) closeMenu();
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
