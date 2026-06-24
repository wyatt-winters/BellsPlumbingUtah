(function () {
  'use strict';

  var header = document.querySelector('header.site');
  if (!header) return;

  var isHome = document.body.classList.contains('home');
  var brand = header.querySelector('.brand');
  var logo = header.querySelector('.brand-logo');
  var eyebrow = isHome ? document.querySelector('.hero--photo .eyebrow--pill') : null;

  var LOGO_ASPECT = 500 / 369;
  var SCROLL_RANGE = 240;
  var start = { w: 42, left: 0, top: 0 };
  var end = { w: 42, left: 0, top: 0 };
  var layoutReady = false;

  function clamp(n, min, max) {
    return Math.min(max, Math.max(min, n));
  }

  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  function measureStart() {
    if (!isHome || !brand || !logo || !eyebrow) return;

    var mobile = window.innerWidth <= 600;
    var gap = mobile ? 10 : 14;
    var minTop = 8;
    var eyebrowRect = eyebrow.getBoundingClientRect();
    var eyebrowCenterX = eyebrowRect.left + (eyebrowRect.width / 2);
    var availableH = eyebrowRect.top - gap - minTop;

    if (availableH < 40) {
      availableH = 40;
    }

    var startH = availableH;
    start.w = startH * LOGO_ASPECT;

    start.left = eyebrowCenterX - (start.w / 2);
    start.top = eyebrowRect.top - startH - gap;
    SCROLL_RANGE = mobile ? 180 : 240;
  }

  function measureEnd() {
    if (!brand) return;
    var mobile = window.innerWidth <= 600;
    var brandRect = brand.getBoundingClientRect();
    var endH = brandRect.height - 8;
    end.w = endH * LOGO_ASPECT;
    end.left = brandRect.left + (mobile ? -6 : -10);
    end.top = brandRect.top + ((brandRect.height - endH) / 2);
  }

  function applyLogoStyles(w, left, top) {
    var h = w / LOGO_ASPECT;

    logo.style.position = 'fixed';
    logo.style.left = left + 'px';
    logo.style.top = top + 'px';
    logo.style.objectFit = 'contain';
    logo.style.transform = 'none';
    logo.style.zIndex = '110';
    logo.style.setProperty('width', w + 'px', 'important');
    logo.style.setProperty('height', h + 'px', 'important');
    logo.style.setProperty('max-width', 'none', 'important');
    logo.style.setProperty('max-height', 'none', 'important');
  }

  function markLayoutReady() {
    if (layoutReady) return;
    layoutReady = true;
    document.body.classList.add('logo-ready');
  }

  function settleLayout() {
    if (!isHome || !logo || !brand || !eyebrow) return;
    measureStart();
    measureEnd();
    markLayoutReady();
    update();
  }

  function update() {
    var scrollY = window.scrollY;
    header.classList.toggle('is-scrolled', scrollY > 12);

    if (!isHome || !logo || !brand || !eyebrow) return;

    if (!layoutReady) {
      if (scrollY > 2) {
        measureStart();
        measureEnd();
        markLayoutReady();
      } else {
        return;
      }
    }

    if (scrollY < 2) {
      measureStart();
    }

    measureEnd();

    var rawT = clamp(scrollY / SCROLL_RANGE, 0, 1);
    var t = 1 - Math.pow(1 - rawT, 2.2);
    var w = lerp(start.w, end.w, t);
    var left = lerp(start.left, end.left, t);
    var top = lerp(start.top, end.top, t);

    applyLogoStyles(w, left, top);

    header.classList.toggle('logo-collapsed', t > 0.92);
    document.body.classList.add('logo-morphing');
  }

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      update();
      ticking = false;
    });
  }

  if (isHome && eyebrow) {
    var heroCopy = document.querySelector('.hero--photo .hero-copy');

    /* Wait for hero rise animation (0.9s) before first measure — avoids wrong
       position flash on load. Logo stays hidden via .logo-ready CSS until then. */
    if (heroCopy) {
      heroCopy.addEventListener('animationend', function (e) {
        if (e.target === heroCopy) settleLayout();
      });
    }

    setTimeout(settleLayout, 950);

    logo.addEventListener('load', function () {
      if (layoutReady) settleLayout();
    });

    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(function () {
        if (layoutReady) settleLayout();
      });
    }

    window.addEventListener('resize', function () {
      if (layoutReady) settleLayout();
    });

    if (window.ResizeObserver) {
      var layoutObserver = new ResizeObserver(function () {
        if (layoutReady) settleLayout();
      });
      layoutObserver.observe(eyebrow);
      layoutObserver.observe(heroCopy || eyebrow);
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  update();
})();
