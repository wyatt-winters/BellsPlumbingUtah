(function () {
  'use strict';

  if (!window.matchMedia('(max-width: 720px)').matches) return;

  var call = document.querySelector('.sticky-call');
  if (!call || document.querySelector('.sticky-actions')) return;

  var wrap = document.createElement('div');
  wrap.className = 'sticky-actions';
  call.parentNode.insertBefore(wrap, call);
  wrap.appendChild(call);

  call.innerHTML = '<span aria-hidden="true">📞</span><span>Call</span>';

  var sms = document.createElement('a');
  sms.className = 'sticky-text';
  sms.href = 'sms:8016853976?body=' + encodeURIComponent('Hi — I need help with my boiler or radiant heat system.');
  sms.setAttribute('aria-label', 'Text Utah Boiler Experts');
  sms.setAttribute('data-track', 'sms_sticky');
  sms.innerHTML = '<span aria-hidden="true">💬</span><span>Text</span>';
  wrap.appendChild(sms);
  document.body.classList.add('has-sticky-actions');
})();
