(function () {
  'use strict';

  var ADS_SEND_TO = 'AW-17966193749/qPGWCJ26mIMcENW4-fZC';

  function trackEvent(name, params) {
    if (typeof window.gtag === 'function') {
      window.gtag('event', name, params || {});
    }
    if (window.dataLayer) {
      window.dataLayer.push(Object.assign({ event: name }, params || {}));
    }
  }

  function clickLocation(el) {
    return el.getAttribute('data-track')
      || el.getAttribute('data-call-location')
      || 'unknown';
  }

  document.querySelectorAll('a[href^="tel:"]').forEach(function (a) {
    a.addEventListener('click', function () {
      var phone = (a.getAttribute('href') || '').replace('tel:', '');
      trackEvent('click_to_call', {
        phone_number: phone,
        click_location: clickLocation(a),
        page_path: window.location.pathname
      });
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'conversion', { send_to: ADS_SEND_TO });
      }
    });
  });

  document.querySelectorAll('a[href^="sms:"]').forEach(function (a) {
    a.addEventListener('click', function () {
      trackEvent('click_to_text', {
        click_location: clickLocation(a),
        page_path: window.location.pathname
      });
    });
  });
})();
