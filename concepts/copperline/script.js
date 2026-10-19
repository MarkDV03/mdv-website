// Copperline Plumbing & Rooter concept: small enhancements only. The page works without JS.
(function () {
  // Mobile menu
  var toggle = document.querySelector('[data-nav-toggle]');
  var nav = document.querySelector('[data-nav]');
  function setOpen(open) {
    toggle.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  }
  if (toggle && nav) {
    toggle.addEventListener('click', function () { setOpen(toggle.getAttribute('aria-expanded') !== 'true'); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) { setOpen(false); toggle.focus(); }
    });
  }

  // Header shadow once the page has scrolled (class toggle only, no scroll-linked animation)
  var header = document.querySelector('[data-header]');
  if (header) {
    var scrolled = false;
    var onScroll = function () {
      var s = window.scrollY > 8;
      if (s !== scrolled) { scrolled = s; header.classList.toggle('is-scrolled', s); }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Offer links preselect the matching service in the booking form
  var select = document.querySelector('[data-service-select]');
  document.querySelectorAll('[data-service]').forEach(function (a) {
    a.addEventListener('click', function () { if (select) select.value = a.getAttribute('data-service'); });
  });

  // Design-only form: validate the two required fields, then show a thank-you note
  var form = document.querySelector('[data-form]');
  if (form) {
    var body = form.querySelector('[data-form-body]');
    var thanks = form.querySelector('[data-form-thanks]');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var first = null;
      ['name', 'phone'].forEach(function (n) {
        var f = form.elements[n];
        var bad = !f.value.trim();
        f.setAttribute('aria-invalid', bad ? 'true' : 'false');
        if (bad && !first) first = f;
      });
      if (first) { first.focus(); return; }
      body.hidden = true;
      thanks.hidden = false;
      thanks.focus();
    });
    form.querySelector('[data-form-reset]').addEventListener('click', function () {
      form.reset();
      thanks.hidden = true;
      body.hidden = false;
      form.elements.name.focus();
    });
  }

  var year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();
})();
