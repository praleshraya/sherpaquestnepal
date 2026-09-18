(() => {
  const root = document.body.dataset.root || '';
  let dismissed = false;
  try { dismissed = sessionStorage.getItem('sherpa-promo-dismissed') === '1'; } catch (_) {}
  if (dismissed) return;

  const promo = document.createElement('aside');
  promo.className = 'floating-promo';
  promo.setAttribute('aria-label', 'Sherpa Quest video promotion');
  promo.innerHTML = `<video src="${root}floating_ad_promotion_video.mov" autoplay muted loop playsinline preload="metadata" aria-label="Sherpa Quest Nepal promotional video"></video><button class="floating-promo-close" type="button" aria-label="Close video promotion">×</button><div class="floating-promo-copy"><span>GEAR FOR THE JOURNEY</span><a href="${root}index.html#products">EXPLORE GEAR</a></div>`;
  document.body.append(promo);
  const video = promo.querySelector('video');
  video.play().catch(() => {});
  promo.querySelector('button').addEventListener('click', () => {
    video.pause();
    promo.remove();
    try { sessionStorage.setItem('sherpa-promo-dismissed', '1'); } catch (_) {}
  });
})();
