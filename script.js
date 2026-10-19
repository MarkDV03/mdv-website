/* MDV Web Design — script.js (vanilla, no build step) */

/* ------------------------------------------------------------------
   Project status: the one place to change a project's label.
   "concept" shows "Concept redesign" and the disclaimer.
   "client"  shows "Client project" and hides the disclaimer.
   ------------------------------------------------------------------ */
const PROJECT_STATUS = {
  "j-carrillo-plumbing": "concept",
  "christinas-salon": "concept",
};

(function () {
  "use strict";

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* ---------- Project labels ---------- */
  document.querySelectorAll("[data-project-label]").forEach((el) => {
    const status = PROJECT_STATUS[el.dataset.projectLabel];
    if (status) el.textContent = status === "client" ? "Client project" : "Concept redesign";
  });
  document.querySelectorAll("[data-concept-only]").forEach((el) => {
    if (PROJECT_STATUS[el.dataset.conceptOnly] === "client") el.hidden = true;
  });

  /* ---------- Footer year ---------- */
  document.querySelectorAll("[data-year]").forEach((el) => {
    el.textContent = String(new Date().getFullYear());
  });

  /* ---------- Loader cleanup ---------- */
  const loader = document.querySelector(".loader");
  if (loader && document.documentElement.classList.contains("show-loader")) {
    loader.addEventListener("animationend", (e) => {
      if (e.target === loader) document.documentElement.classList.remove("show-loader");
    });
    // Safety net: never leave it on screen.
    setTimeout(() => document.documentElement.classList.remove("show-loader"), 1600);
  }

  /* ---------- Header: switch to dark over dark sections ---------- */
  const header = document.querySelector(".site-header");
  const tones = document.querySelectorAll("[data-tone], .site-footer.tone-dark");
  if (header && tones.length && "IntersectionObserver" in window) {
    // Watch a 1px line just under the header instead of hit-testing on every scroll
    let io;
    const inLine = new Set();
    const watch = () => {
      if (io) io.disconnect();
      inLine.clear();
      const y = Math.round(header.getBoundingClientRect().bottom - 8);
      io = new IntersectionObserver((entries) => {
        entries.forEach((e) => { if (e.isIntersecting) inLine.add(e.target); else inLine.delete(e.target); });
        const tone = [...inLine].pop();
        header.classList.toggle("is-dark", !!tone && (tone.dataset.tone === "dark" || (!tone.dataset.tone && tone.classList.contains("tone-dark"))));
      }, { rootMargin: `${-y}px 0px ${-(window.innerHeight - y - 1)}px 0px` });
      tones.forEach((t) => io.observe(t));
    };
    let rt;
    window.addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(watch, 150); }, { passive: true });
    watch();
  }

  /* ---------- Full-screen menu with focus trap ---------- */
  const menu = document.getElementById("menu");
  const toggle = document.querySelector(".menu-toggle");
  if (menu && toggle) {
    const closeBtn = menu.querySelector(".menu-close");
    const focusables = () =>
      Array.from(menu.querySelectorAll('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])'));
    let lastFocus = null;

    const open = () => {
      lastFocus = document.activeElement;
      menu.classList.add("is-open");
      document.body.classList.add("menu-open");
      toggle.setAttribute("aria-expanded", "true");
      setTimeout(() => (closeBtn || focusables()[0]).focus(), 30);
    };
    const close = (restore = true) => {
      menu.classList.remove("is-open");
      document.body.classList.remove("menu-open");
      toggle.setAttribute("aria-expanded", "false");
      if (restore && lastFocus) lastFocus.focus();
    };

    toggle.addEventListener("click", open);
    if (closeBtn) closeBtn.addEventListener("click", () => close());
    menu.addEventListener("click", (e) => {
      if (e.target.closest("a[href]")) close(false);
    });
    document.addEventListener("keydown", (e) => {
      if (!menu.classList.contains("is-open")) return;
      if (e.key === "Escape") { e.preventDefault(); close(); return; }
      if (e.key === "Tab") {
        const items = focusables();
        if (!items.length) return;
        const first = items[0];
        const last = items[items.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    window.matchMedia("(min-width: 1024px)").addEventListener("change", (m) => {
      if (m.matches && menu.classList.contains("is-open")) close(false);
    });
  }

  /* ---------- Headlines: split into words for the word-by-word reveal ---------- */
  if (!reduceMotion.matches && "IntersectionObserver" in window) {
    // Only the hero headline: section headings stay solid so fast scrolling never shows blank text
    const heads = document.querySelectorAll(".hero__title");
    const splitNode = (node, counter) => {
      Array.from(node.childNodes).forEach((child) => {
        if (child.nodeType === 3) {
          const frag = document.createDocumentFragment();
          child.textContent.split(/(\s+)/).forEach((part) => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            const w = document.createElement("span");
            w.className = "w";
            w.style.setProperty("--i", counter.n++);
            w.textContent = part;
            frag.appendChild(w);
          });
          child.replaceWith(frag);
        } else if (child.nodeType === 1 && !child.classList.contains("sr-only")) {
          splitNode(child, counter);
        }
      });
    };
    const headIO = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) { entry.target.classList.add("is-in"); headIO.unobserve(entry.target); }
      });
    }, { threshold: 0.2 });
    heads.forEach((h) => {
      splitNode(h, { n: 0 });
      h.classList.add("split-words");
      headIO.observe(h);
    });
  }

  /* ---------- Reveal on scroll ---------- */
  const reveals = document.querySelectorAll(".reveal");
  if (reduceMotion.matches || !("IntersectionObserver" in window)) {
    reveals.forEach((el) => el.classList.add("is-visible"));
  } else {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            // Scrolled in too fast to animate: show it straight away instead of fading in late
            if (entry.boundingClientRect.top < window.innerHeight * 0.9) entry.target.style.transition = "none";
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px 15% 0px", threshold: 0 }
    );
    reveals.forEach((el) => io.observe(el));
  }

  /* ---------- Before / after sliders ---------- */
  document.querySelectorAll("[data-compare]").forEach((box) => {
    const range = box.querySelector(".compare__range");
    if (!range) return;

    const set = (value) => {
      const v = Math.max(0, Math.min(100, Math.round(value)));
      range.value = String(v);
      box.style.setProperty("--pos", v + "%");
      range.setAttribute("aria-valuetext", v + "% before, " + (100 - v) + "% after");
    };
    set(range.value);
    range.addEventListener("input", () => set(range.value));

    const fromPointer = (e) => {
      const rect = box.getBoundingClientRect();
      set(((e.clientX - rect.left) / rect.width) * 100);
    };
    let dragging = false;
    let startX = 0;
    let startY = 0;
    let decided = false;

    box.addEventListener("pointerdown", (e) => {
      if (e.button !== undefined && e.button !== 0) return;
      dragging = true;
      decided = e.pointerType === "mouse";
      startX = e.clientX;
      startY = e.clientY;
      if (decided) {
        box.setPointerCapture(e.pointerId);
        box.classList.add("is-dragging");
        fromPointer(e);
      }
    });
    box.addEventListener("pointermove", (e) => {
      if (!dragging) return;
      if (!decided) {
        // On touch, only take over for mostly-horizontal drags so the page still scrolls.
        const dx = Math.abs(e.clientX - startX);
        const dy = Math.abs(e.clientY - startY);
        if (dx < 6 && dy < 6) return;
        if (dy > dx) { dragging = false; return; }
        decided = true;
        box.setPointerCapture(e.pointerId);
        box.classList.add("is-dragging");
      }
      fromPointer(e);
    });
    const end = (e) => {
      if (dragging && !decided && e.type === "pointerup") fromPointer(e); // a tap jumps to that spot
      dragging = false;
      box.classList.remove("is-dragging");
    };
    box.addEventListener("pointerup", end);
    box.addEventListener("pointercancel", end);
    box.addEventListener("click", () => range.focus({ preventScroll: true }));
  });

  /* ---------- Quote form (Netlify Forms via fetch, normal POST as fallback) ---------- */
  const form = document.querySelector("[data-quote-form]");
  if (form) {
    const thanks = document.querySelector("[data-thanks]");
    const status = form.querySelector("[data-form-status]");
    const submit = form.querySelector("[data-submit]");
    const submitLabel = form.querySelector("[data-submit-label]");
    const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

    const messages = {
      name: "Please enter your name.",
      business: "Please enter your business name.",
      email: "Please enter your email address.",
      emailFormat: "That email doesn't look right. Check for a typo, like name@example.com.",
      message: "Please add a short message so I know what you need.",
    };

    const errorEl = (input) => document.getElementById("e-" + input.id.replace("f-", ""));
    const validate = (input) => {
      const v = input.value.trim();
      let msg = "";
      if (input.required && !v) msg = messages[input.name] || "This field is required.";
      else if (input.type === "email" && v && !emailRe.test(v)) msg = messages.emailFormat;
      const err = errorEl(input);
      if (err) err.textContent = msg;
      if (msg) input.setAttribute("aria-invalid", "true");
      else input.removeAttribute("aria-invalid");
      return !msg;
    };

    const fields = Array.from(form.querySelectorAll("input[required], textarea[required]"));
    fields.forEach((input) => {
      input.addEventListener("blur", () => { if (input.value.trim() || input.dataset.touched) validate(input); input.dataset.touched = "1"; });
      input.addEventListener("input", () => { if (input.getAttribute("aria-invalid") === "true") validate(input); });
    });

    form.addEventListener("submit", async (e) => {
      const invalid = fields.filter((f) => !validate(f));
      if (invalid.length) {
        e.preventDefault();
        invalid[0].focus();
        return;
      }
      if (!window.fetch) return; // let the normal POST go through to thanks.html

      e.preventDefault();
      status.textContent = "";
      submit.disabled = true;
      submitLabel.textContent = "Sending...";

      try {
        const body = new URLSearchParams(new FormData(form)).toString();
        const res = await fetch("/", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body,
        });
        if (!res.ok) throw new Error("HTTP " + res.status);
        form.hidden = true;
        thanks.hidden = false;
        thanks.focus();
      } catch (err) {
        status.innerHTML =
          'Sorry, that didn’t send. Please try again, or email me at <a href="mailto:markdv.webdesign@gmail.com">markdv.webdesign@gmail.com</a>.';
        submit.disabled = false;
        submitLabel.textContent = "Get my free concept";
      }
    });
  }
})();

/* Main street doodles slide up when they scroll into view */
(function () {
  var street = document.querySelector(".street");
  if (!street || !("IntersectionObserver" in window)) { if (street) street.classList.add("is-in"); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { street.classList.add("is-in"); io.disconnect(); } });
  }, { threshold: 0.3 });
  io.observe(street);
})();

/* Highlight the menu link for the section you're in */
(function () {
  var ids = ["work", "benefits", "process", "about", "contact"];
  var sections = ids.map(function (id) { return document.getElementById(id); }).filter(Boolean);
  if (!sections.length) return;
  var links = Array.prototype.slice.call(document.querySelectorAll('.site-nav a[href^="#"], .menu a[href^="#"]'));
  var current = null, ticking = false;
  function update() {
    ticking = false;
    var line = window.innerHeight * 0.4, active = null;
    sections.forEach(function (s) { if (s.getBoundingClientRect().top <= line) active = s.id; });
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) active = sections[sections.length - 1].id;
    if (active === current) return;
    current = active;
    links.forEach(function (a) {
      var on = a.getAttribute("href") === "#" + active;
      a.classList.toggle("is-active", on);
      if (on) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
    });
  }
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  window.addEventListener("resize", update);
  update();
})();

/* Live project previews: scale each full-size iframe down to fit its device screen */
(function () {
  var frames = document.querySelectorAll(".live-frame");
  if (!frames.length) return;
  function fit(el) { el.style.setProperty("--s", el.clientWidth / Number(el.dataset.w)); }
  frames.forEach(fit);
  if ("ResizeObserver" in window) {
    var ro = new ResizeObserver(function (entries) { entries.forEach(function (e) { fit(e.target); }); });
    frames.forEach(function (el) { ro.observe(el); });
  } else {
    window.addEventListener("resize", function () { frames.forEach(fit); });
  }
})();

/* Live project previews: slowly scroll through the real site, loop, and only while on screen.
   Works when both sites share an origin (markdv03.github.io); otherwise the top of the site just shows. */
(function () {
  var frames = document.querySelectorAll(".live-frame iframe");
  if (!frames.length || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  frames.forEach(function (iframe) {
    var visible = false, started = false, running = false, resume = null;
    function start() {
      var win, doc;
      try { win = iframe.contentWindow; doc = iframe.contentDocument; if (!doc || !doc.head || doc.URL === "about:blank" || doc.readyState === "loading") return; } catch (e) { return; }
      if (started) return; started = true;
      var css = doc.createElement("style");
      css.textContent = "html{scrollbar-width:none;scroll-behavior:auto!important}html::-webkit-scrollbar{display:none}";
      doc.head.appendChild(css);
      var speed = iframe.width < 600 ? 170 : 150;   // site pixels per second
      var viewH = Number(iframe.getAttribute("height")) || win.innerHeight;
      var root = doc.documentElement, useTransform = false;
      // iPhone Safari won't scroll inside a frame, so slide the page itself instead
      function moveTo(v) {
        if (!useTransform) {
          win.scrollTo(0, v);
          if (v > 40 && Math.abs(win.scrollY - v) > 20) { useTransform = true; win.scrollTo(0, 0); root.style.overflow = "hidden"; root.style.willChange = "transform"; }
          else return;
        }
        root.style.transform = "translateY(" + (-v) + "px)";
      }
      var y = 0, pauseUntil = performance.now() + 1800, last = performance.now();
      function tick(now) {
        var dt = Math.min(now - last, 100); last = now;
        if (visible && now > pauseUntil) {
          var max = (doc.body ? Math.max(doc.body.scrollHeight, root.scrollHeight) : root.scrollHeight) - viewH;
          y += speed * dt / 1000;
          if (y >= max) { y = max; pauseUntil = now + 2200; moveTo(y); setTimeout(function () { y = 0; moveTo(0); }, 2000); }
          else moveTo(y);
        }
        if (visible) requestAnimationFrame(tick); else running = false;
      }
      resume = function () { if (running) return; running = true; last = performance.now(); requestAnimationFrame(tick); };
      resume();
    }
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) { start(); if (resume) resume(); } }).observe(iframe);
    } else { visible = true; }
    iframe.addEventListener("load", function () { if (visible) start(); });
    start();
  });
})();

/* Logos: the ring draws itself around MDV. The top bar logo plays on load, the others
   each time you scroll to them, and the menu logo when the menu opens. */
(function () {
  var logos = document.querySelectorAll(".logo__mark--anim");
  if (!logos.length) return;
  if (matchMedia("(prefers-reduced-motion: reduce)").matches || !("IntersectionObserver" in window)) {
    logos.forEach(function (l) { l.classList.add("is-done"); });
    return;
  }
  function play(el) {
    el.classList.remove("is-done", "is-playing");
    void el.offsetWidth; // restart the animation
    el.classList.add("is-playing");
  }
  logos.forEach(function (l) {
    l.addEventListener("animationend", function (e) {
      if (e.animationName === "logo-ring") { l.classList.remove("is-playing"); l.classList.add("is-done"); }
    });
  });
  var head = document.querySelector(".site-header .logo__mark--anim");
  // Top bar logo plays once on load (after the first-visit loader clears)
  if (head) setTimeout(function () { play(head); }, document.documentElement.classList.contains("show-loader") ? 1350 : 100);
  var seen = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) play(e.target); });
  }, { threshold: 0.6 });
  logos.forEach(function (l) { if (l !== head && !l.closest(".menu")) seen.observe(l); });
  var menuLogo = document.querySelector(".menu .logo__mark--anim"), toggle = document.querySelector(".menu-toggle");
  if (menuLogo && toggle) toggle.addEventListener("click", function () { setTimeout(function () { play(menuLogo); }, 150); });
})();
