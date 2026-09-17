document.querySelectorAll('[data-carousel]').forEach(carousel => {
  const slides = [...carousel.querySelectorAll('[data-slide]')];
  const dots = [...carousel.querySelectorAll('[data-carousel-dot]')];
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const delay = Number(carousel.dataset.delay) || 6500;
  let current = 0;
  let timer;

  function show(index) {
    current = (index + slides.length) % slides.length;
    slides.forEach((slide, position) => {
      const active = position === current;
      slide.classList.toggle('is-active', active);
      slide.setAttribute('aria-hidden', String(!active));
      slide.inert = !active;
    });
    dots.forEach((dot, position) => {
      const active = position === current;
      dot.classList.toggle('active', active);
      if (active) dot.setAttribute('aria-current', 'true');
      else dot.removeAttribute('aria-current');
    });
  }
  function pause() { clearInterval(timer); }
  function play() {
    pause();
    if (!reduceMotion.matches && !document.hidden) timer = setInterval(() => show(current + 1), delay);
  }

  carousel.querySelector('[data-carousel-prev]')?.addEventListener('click', () => { show(current - 1); play(); });
  carousel.querySelector('[data-carousel-next]')?.addEventListener('click', () => { show(current + 1); play(); });
  dots.forEach((dot, index) => dot.addEventListener('click', () => { show(index); play(); }));
  carousel.addEventListener('mouseenter', pause);
  carousel.addEventListener('mouseleave', play);
  carousel.addEventListener('focusin', pause);
  carousel.addEventListener('focusout', event => { if (!carousel.contains(event.relatedTarget)) play(); });
  carousel.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') { event.preventDefault(); show(current - 1); play(); }
    if (event.key === 'ArrowRight') { event.preventDefault(); show(current + 1); play(); }
  });
  document.addEventListener('visibilitychange', () => document.hidden ? pause() : play());
  reduceMotion.addEventListener('change', play);
  show(0);
  play();
});
