const productImage = document.querySelector('#product-main-image');
const productThumbs = document.querySelectorAll('[data-gallery-src]');

productThumbs.forEach(button => button.addEventListener('click', () => {
  if (!productImage) return;
  productImage.src = button.dataset.gallerySrc;
  productImage.alt = button.dataset.galleryAlt;
  productThumbs.forEach(thumb => {
    const active = thumb === button;
    thumb.classList.toggle('active', active);
    thumb.setAttribute('aria-pressed', String(active));
  });
}));
