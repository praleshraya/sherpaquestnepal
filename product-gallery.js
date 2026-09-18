const productImage = document.querySelector('#product-main-image');
const productThumbs = document.querySelectorAll('[data-gallery-src]');
const sizeOptions = document.querySelectorAll('[data-option-size]');
const colorOptions = document.querySelectorAll('[data-option-color]');
const inquiry = document.querySelector('#product-inquiry');
const imageStatus = document.querySelector('#color-image-status');
const imageStage = document.querySelector('.product-main-image');
const galleryGroups = document.querySelectorAll('[data-gallery-group]');

function showColorGroup(color) {
  if (!galleryGroups.length || !color) {
    galleryGroups.forEach(group => { group.hidden = false; });
    return;
  }
  const hasColor = [...galleryGroups].some(group => group.dataset.galleryGroup === color);
  const hasOther = [...galleryGroups].some(group => group.dataset.galleryGroup === 'Other views');
  galleryGroups.forEach(group => {
    group.hidden = hasColor
      ? group.dataset.galleryGroup !== color && group.dataset.galleryGroup !== 'Other views'
      : hasOther && group.dataset.galleryGroup !== 'Other views';
  });
}

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

function activateThumb(button) {
  showImage(button.dataset.gallerySrc, button.dataset.galleryAlt);
  const picturedColor = button.dataset.galleryColor;
  if (picturedColor) {
    colorOptions.forEach(option => {
      const active = option.dataset.optionColor === picturedColor;
      option.classList.toggle('active', active);
      option.setAttribute('aria-pressed', String(active));
    });
    if (imageStatus) imageStatus.textContent = `Showing ${picturedColor} product photo.`;
    showColorGroup(picturedColor);
    updateInquiry();
  }
}

productThumbs.forEach(button => button.addEventListener('click', () => activateThumb(button)));

function moveGallery(direction) {
  const visible = [...productThumbs].filter(thumb => !thumb.closest('[data-gallery-group]')?.hidden);
  if (visible.length < 2) return;
  const current = visible.findIndex(thumb => thumb.classList.contains('active'));
  const next = (current + direction + visible.length) % visible.length;
  activateThumb(visible[next]);
  visible[next].scrollIntoView({block:'nearest', inline:'nearest', behavior:'smooth'});
}

document.querySelector('.gallery-prev')?.addEventListener('click', () => moveGallery(-1));
document.querySelector('.gallery-next')?.addEventListener('click', () => moveGallery(1));
let touchStartX = null;
imageStage?.addEventListener('touchstart', event => {
  touchStartX = event.changedTouches[0]?.screenX ?? null;
}, {passive:true});
imageStage?.addEventListener('touchend', event => {
  if (touchStartX === null) return;
  const distance = (event.changedTouches[0]?.screenX ?? touchStartX) - touchStartX;
  if (Math.abs(distance) > 45) moveGallery(distance < 0 ? 1 : -1);
  touchStartX = null;
}, {passive:true});

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
  showColorGroup(color);
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
showColorGroup(document.querySelector('[data-option-color][aria-pressed="true"]')?.dataset.optionColor);
