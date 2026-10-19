// Bayglow Nail Bar concept: small enhancements only. The page works without JS.
(function () {
  document.documentElement.classList.add('js');

  // Mobile menu
  var toggle = document.querySelector('[data-nav-toggle]');
  var nav = document.querySelector('[data-nav]');
  if (toggle && nav) {
    function setOpen(open) {
      toggle.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('is-open', open);
    }
    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setOpen(false);
    });
  }

  // Header border once the page scrolls
  var header = document.querySelector('[data-header]');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Reveal sections as they enter the viewport
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add('is-in'); io.unobserve(entry.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('is-in'); });
  }

  // Opening promo: shows once per visitor after a short delay, and from the announcement link
  var promo = document.querySelector('[data-promo]');
  var lastFocus = null;
  function seen() { try { return localStorage.getItem('bayglow-promo') === '1'; } catch (e) { return false; } }
  function markSeen() { try { localStorage.setItem('bayglow-promo', '1'); } catch (e) {} }
  function openPromo() {
    if (!promo) return;
    lastFocus = document.activeElement;
    promo.hidden = false;
    var close = promo.querySelector('.promo__close');
    if (close) close.focus();
  }
  function closePromo() {
    if (!promo || promo.hidden) return;
    promo.hidden = true;
    markSeen();
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  if (promo) {
    promo.addEventListener('click', function (e) {
      if (e.target.closest('[data-close-promo]')) closePromo();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closePromo();
    });
    document.querySelectorAll('[data-open-promo]').forEach(function (a) {
      a.addEventListener('click', function (e) { e.preventDefault(); openPromo(); });
    });
    // No popup inside the portfolio preview frames
    if (!seen() && window.self === window.top && !/[?&]nopromo/.test(location.search)) setTimeout(openPromo, 5000);
  }

  var year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();
})();
