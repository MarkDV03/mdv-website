/* La Brisa Taqueria concept: nav toggle, today's hours, footer year. No scroll effects. */
(function () {
  "use strict";

  // Mobile nav
  var toggle = document.querySelector("[data-nav-toggle]");
  var nav = document.querySelector("[data-nav]");
  if (toggle && nav) {
    var setOpen = function (open) {
      toggle.setAttribute("aria-expanded", String(open));
      nav.classList.toggle("is-open", open);
    };
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setOpen(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setOpen(false);
    });
  }

  // Hours (24h open/close per weekday, 0 = Sunday)
  var HOURS = { 0: [9, 20], 1: [9, 21], 2: [9, 21], 3: [9, 21], 4: [9, 21], 5: [9, 22], 6: [9, 22] };
  var fmt = function (h) { return (h % 12 || 12) + (h < 12 ? "am" : "pm"); };
  var now = new Date();
  var day = now.getDay();
  var hr = now.getHours() + now.getMinutes() / 60;
  var today = HOURS[day];

  var row = document.querySelector('.hours tr[data-day="' + day + '"]');
  if (row) row.classList.add("is-today");

  var label = document.querySelector("[data-today]");
  var dot = document.querySelector(".status-dot");
  if (label && today) {
    var text;
    var open = hr >= today[0] && hr < today[1];
    if (open) {
      text = "Open now · today " + fmt(today[0]) + " to " + fmt(today[1]);
    } else if (hr < today[0]) {
      text = "Opens today at " + fmt(today[0]) + " · until " + fmt(today[1]);
    } else {
      var next = HOURS[(day + 1) % 7];
      text = "Closed now · opens tomorrow at " + fmt(next[0]);
    }
    if (day === 2) text += " · Taco Tuesday!";
    label.textContent = text;
    if (dot && !open) dot.classList.add("is-closed");
  }

  var y = document.querySelectorAll("[data-year]");
  for (var i = 0; i < y.length; i++) y[i].textContent = now.getFullYear();
})();
