(function () {
  'use strict';

  var FORM_ENDPOINT = 'https://script.google.com/macros/s/AKfycbzaR9sFnOFQocPqG_p95ItochSzKeNjZ5JhgyLphKvAPbd3g-kqIEbJocsLGVqV4WYN_A/exec';

  function trackEvent(name, params) {
    if (typeof window.gtag === 'function') {
      window.gtag('event', name, params || {});
    }
    if (window.dataLayer) {
      window.dataLayer.push(Object.assign({ event: name }, params || {}));
    }
  }

  document.querySelectorAll('[data-lead-form]').forEach(function (form) {
    if (!form.getAttribute('action') || form.getAttribute('action') === '#') {
      form.setAttribute('action', FORM_ENDPOINT);
    }

    form.addEventListener('submit', function (e) {
      var honeypot = form.querySelector('[name="website"]');
      if (honeypot && honeypot.value) {
        e.preventDefault();
        return false;
      }

      var source = form.getAttribute('data-source') || form.querySelector('[name="source"]');
      source = source && source.value ? source.value : (source || 'website');

      trackEvent('generate_lead', {
        form_id: form.id || 'lead-form',
        form_source: source,
        page_path: window.location.pathname
      });
    });
  });

  if (new URLSearchParams(window.location.search).get('submitted') === '1') {
    document.querySelectorAll('[data-lead-success]').forEach(function (el) {
      el.classList.add('is-visible');
    });
    document.querySelectorAll('[data-lead-form]').forEach(function (form) {
      form.style.display = 'none';
    });
    var anchor = document.querySelector('[data-lead-anchor]');
    if (anchor) {
      anchor.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
})();
