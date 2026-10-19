// Christina's Hair Salon: small enhancements only. The page works without JS.
(function () {
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
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        toggle.focus();
      }
    });
  }

  // Header border once the page scrolls
  var header = document.querySelector('[data-header]');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Today's hours, in salon time (Pacific)
  var hours = {
    0: [10.5, 18.5], 1: [10.5, 18.5], 2: [10.5, 18.5], 3: [10.5, 18.5], 4: [10.5, 18.5],
    5: [10, 18.5], 6: [10, 18.5]
  };
  var labels = { 10: '10 AM', 10.5: '10:30 AM', 18.5: '6:30 PM' };
  var now;
  try {
    now = new Date(new Date().toLocaleString('en-US', { timeZone: 'America/Los_Angeles' }));
  } catch (e) {
    now = new Date();
  }
  var day = now.getDay();
  var row = document.querySelector('.hours tr[data-days="' + day + '"]');
  if (row) row.classList.add('is-today');

  var todayEl = document.querySelector('[data-today-hours]');
  if (todayEl) {
    var h = now.getHours() + now.getMinutes() / 60;
    var open = hours[day];
    if (h >= open[0] && h < open[1]) {
      todayEl.textContent = 'Open now until ' + labels[open[1]] + ', walk-ins welcome';
    } else if (h < open[0]) {
      todayEl.textContent = 'Opens today at ' + labels[open[0]] + ', walk-ins welcome';
    } else {
      todayEl.textContent = 'Closed now. Walk-ins welcome during open hours';
    }
  }

  // Before & after: one slider above the photos moves every pair
  var compareRange = document.querySelector('[data-compare-range]');
  if (compareRange) {
    var compares = document.querySelectorAll('[data-compare]');
    var header = document.querySelector('.site-header');
    var setCompare = function () {
      // The line on each photo follows the slider
      var pos = compareRange.value + '%';
      compareRange.style.setProperty('--fill', pos);
      compares.forEach(function (fig) { fig.style.setProperty('--pos', pos); });
    };
    var setHeaderH = function () {
      if (header) document.documentElement.style.setProperty('--header-h', header.offsetHeight + 'px');
    };
    compareRange.addEventListener('input', setCompare);
    window.addEventListener('resize', setHeaderH);
    setHeaderH();
    setCompare();
  }

  // Scroll reveals, with a small stagger for items in the same row
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var revealEls = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window && !reduceMotion) {
    revealEls.forEach(function (el) {
      var siblings = el.parentElement ? el.parentElement.querySelectorAll(':scope > [data-reveal]') : [];
      var i = Array.prototype.indexOf.call(siblings, el);
      if (i > 0) el.style.setProperty('--delay', (i * 0.12) + 's');
    });
    var revealIo = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealIo.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
    revealEls.forEach(function (el) { revealIo.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-visible'); });
  }

  // Count-up numbers
  var counters = document.querySelectorAll('[data-count]');
  if ('IntersectionObserver' in window && !reduceMotion) {
    var countIo = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target, end = +el.getAttribute('data-count'), start = null;
        countIo.unobserve(el);
        var step = function (t) {
          if (start === null) start = t;
          var p = Math.min((t - start) / 1200, 1);
          el.textContent = String(Math.round(end * (1 - Math.pow(1 - p, 3))));
          if (p < 1) requestAnimationFrame(step);
        };
        el.textContent = '0';
        requestAnimationFrame(step);
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { countIo.observe(el); });
  }

  // Pause looping animations when they're offscreen or the tab is hidden
  var loops = document.querySelectorAll('[data-loop]');
  if ('IntersectionObserver' in window) {
    var loopIo = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) { entry.target.classList.toggle('is-paused', !entry.isIntersecting); });
    });
    loops.forEach(function (el) { loopIo.observe(el); });
  }
  document.addEventListener('visibilitychange', function () {
    document.documentElement.classList.toggle('is-hidden', document.hidden);
  });

  var year = document.querySelector('[data-year]');
  if (year) year.textContent = String(new Date().getFullYear());

  // Request form: design only until it's connected to a form service (e.g. Formspree)
  var form = document.querySelector('[data-request-form]');
  if (form) {
    var status = form.querySelector('[data-form-status]');
    var checks = [
      { input: form.querySelector('#name'), valid: function (v) { return v.trim().length > 0; } },
      { input: form.querySelector('#phone'), valid: function (v) { return v.replace(/\D/g, '').length >= 10; } }
    ];

    function validate(check) {
      var ok = check.valid(check.input.value);
      var err = document.getElementById(check.input.getAttribute('aria-describedby'));
      check.input.setAttribute('aria-invalid', String(!ok));
      if (err) err.hidden = ok;
      return ok;
    }

    checks.forEach(function (c) {
      c.input.addEventListener('blur', function () { if (c.input.value) validate(c); });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var firstBad = null;
      checks.forEach(function (c) { if (!validate(c) && !firstBad) firstBad = c.input; });
      if (firstBad) {
        status.textContent = '';
        firstBad.focus();
        return;
      }
      status.textContent = 'Preview only: this form isn’t connected yet. Please call (408) 550-4392 to book.';
    });
  }

  // "Love is in the Hair!" logos: the heart draws itself in. Every logo moves together, led by the header:
  // they redraw as each new section scrolls into view (bottom to top when scrolling up),
  // when the header logo is hovered, and every 7 seconds when idle
  var loves = document.querySelectorAll('.love');
  if (loves.length) {
    var instant = window.matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window);
    if (instant) {
      loves.forEach(function (l) { l.classList.add('is-drawn'); });
    } else {
      // Two frames so the first draw-in transition plays
      requestAnimationFrame(function () { requestAnimationFrame(function () {
        loves.forEach(function (l) { l.classList.add('is-drawn'); });
      }); });

      // up: draw the heart backwards, from the bottom tip to the top
      var redraw = function (l, up) {
        if (l.classList.contains('is-replay')) return;
        l.classList.toggle('is-up', !!up);
        l.classList.add('is-replay');
      };
      loves.forEach(function (l) {
        l.addEventListener('animationend', function (e) {
          var lastPen = l.classList.contains('is-up') ? 'love__pen--a' : 'love__pen--b';
          if (e.target.classList.contains(lastPen)) l.classList.remove('is-replay', 'is-up');
        });
      });

      var lastDraw = Date.now();
      var lastY = window.scrollY, goingUp = false;
      window.addEventListener('scroll', function () {
        var y = window.scrollY;
        if (y !== lastY) goingUp = y < lastY;
        lastY = y;
      }, { passive: true });
      var replay = function (up) {
        if (document.hidden || Date.now() - lastDraw < 1800) return;
        lastDraw = Date.now();
        loves.forEach(function (l) { redraw(l, up === true); });
      };
      var sectionObs = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting && (goingUp || window.scrollY > 50)) replay(goingUp); });
      }, { rootMargin: '-45% 0px -45% 0px' });
      document.querySelectorAll('main > section').forEach(function (s) { sectionObs.observe(s); });
      var headerLove = document.querySelector('.love--header');
      if (headerLove) headerLove.parentElement.addEventListener('mouseenter', function () { replay(); });
      setInterval(function () { if (Date.now() - lastDraw > 6500) replay(); }, 1000);
    }
  }

  // Gallery lightbox
  var box = document.querySelector('[data-lightbox]');
  if (box && typeof box.showModal === 'function') {
    var boxImg = box.querySelector('[data-lightbox-img]');
    document.querySelectorAll('.work__btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var img = btn.querySelector('img');
        boxImg.src = btn.getAttribute('data-full');
        boxImg.alt = img.alt;
        box.showModal();
      });
    });
    box.querySelector('[data-lightbox-close]').addEventListener('click', function () { box.close(); });
    box.addEventListener('click', function (e) { if (e.target === box) box.close(); });
  }
})();
