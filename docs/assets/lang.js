/*
 * Language switcher: the English (/), 简体 (/zh/) and 繁體 (/zh-hant/) sites
 * have the same pages, so switching keeps the reader on the page they are on.
 */
(function () {
  "use strict";
  var PREFIXES = ["/zh-hant/", "/zh/"];

  function pagePath() {
    var p = location.pathname;
    for (var i = 0; i < PREFIXES.length; i++) {
      if (p.indexOf(PREFIXES[i]) === 0) return p.slice(PREFIXES[i].length);
    }
    return p.replace(/^\//, "");
  }

  document.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest("a.md-select__link[hreflang]");
    if (!a) return;
    var base = new URL(a.getAttribute("href"), location.href).pathname;
    ev.preventDefault();
    location.href = base.replace(/\/?$/, "/") + pagePath() + location.hash;
  }, true);
})();
