const productImage = document.querySelector('#product-main-image');
const productThumbs = document.querySelectorAll('[data-gallery-src]');
const sizeOptions = document.querySelectorAll('[data-option-size]');
const colorOptions = document.querySelectorAll('[data-option-color]');
const inquiry = document.querySelector('#product-inquiry');
const imageStatus = document.querySelector('#color-image-status');

function showImage(src, alt) {
  if (!productImage) return;
  productImage.src = src;
  productImage.alt = alt;
  productThumbs.forEach(thumb => {
    const active = thumb.dataset.gallerySrc === src;
    thumb.classList.toggle('active', active);
    thumb.setAttribute('aria-pressed', String(active));
  });
}

function updateInquiry() {
  if (!inquiry) return;
  const size = document.querySelector('[data-option-size][aria-pressed="true"]')?.dataset.optionSize;
  const color = document.querySelector('[data-option-color][aria-pressed="true"]')?.dataset.optionColor;
  const details = [size && `size ${size}`, color && `color ${color}`].filter(Boolean).join(' and ');
  const message = `Hello Sherpa Quest Nepal, I'd like to ask about ${inquiry.dataset.productName}${details ? ` in ${details}` : ''}.`;
  inquiry.href = `https://wa.me/9779744464587?text=${encodeURIComponent(message)}`;
}

productThumbs.forEach(button => button.addEventListener('click', () => {
  showImage(button.dataset.gallerySrc, button.dataset.galleryAlt);
  const picturedColor = button.dataset.galleryColor;
  if (picturedColor) {
    colorOptions.forEach(option => {
      const active = option.dataset.optionColor === picturedColor;
      option.classList.toggle('active', active);
      option.setAttribute('aria-pressed', String(active));
    });
    if (imageStatus) imageStatus.textContent = `Showing ${picturedColor} product photo.`;
    updateInquiry();
  }
}));

sizeOptions.forEach(button => button.addEventListener('click', () => {
  sizeOptions.forEach(option => {
    const active = option === button;
    option.classList.toggle('active', active);
    option.setAttribute('aria-pressed', String(active));
  });
  updateInquiry();
}));

colorOptions.forEach(button => button.addEventListener('click', () => {
  colorOptions.forEach(option => {
    const active = option === button;
    option.classList.toggle('active', active);
    option.setAttribute('aria-pressed', String(active));
  });
  const color = button.dataset.optionColor;
  if (button.dataset.previewSrc) {
    showImage(button.dataset.previewSrc, `${inquiry?.dataset.productName || 'Product'} — ${color}`);
    if (imageStatus) imageStatus.textContent = `Showing ${color} product photo.`;
  } else {
    showImage(productImage.dataset.primarySrc, `${inquiry?.dataset.productName || 'Product'} — reference photo`);
    if (imageStatus) imageStatus.textContent = `A ${color} photo is not available; showing a reference image.`;
  }
  updateInquiry();
}));

updateInquiry();
