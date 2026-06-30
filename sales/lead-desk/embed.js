(function () {
  'use strict';

  var VERSION = '1.0.0';
  var STEP_COUNT = 3;
  var DEFAULT_API_URL = 'https://api.saddleupai.com/v1';
  var DEFAULT_LICENSE_API_URL = 'https://api.saddleupai.com';
  var LICENSE_CACHE_MS = 30 * 60 * 1000;

  var URGENCY_OPTIONS = [
    { value: 'emergency', label: 'Emergency — need help now' },
    { value: 'today', label: 'Today if possible' },
    { value: 'this_week', label: 'This week' },
    { value: 'planning', label: 'Just planning / getting quotes' }
  ];

  var TRADE_TEMPLATES = {
    hvac: {
      headline: 'How can we help with your HVAC system?',
      subheadline: 'Answer a few quick questions so we can prioritize your request.',
      issueOptions: [
        { value: 'no_heat', label: 'No heat' },
        { value: 'no_ac', label: 'No AC / not cooling' },
        { value: 'maintenance', label: 'Maintenance or tune-up' },
        { value: 'quote', label: 'New system quote' },
        { value: 'other', label: 'Something else' }
      ]
    },
    plumbing: {
      headline: 'Tell us about your plumbing issue',
      subheadline: 'We route urgent calls first — especially active leaks.',
      issueOptions: [
        { value: 'water_leak', label: 'Active leak / flooding' },
        { value: 'no_water', label: 'No water / low pressure' },
        { value: 'drain', label: 'Clogged drain' },
        { value: 'water_heater', label: 'Water heater issue' },
        { value: 'quote', label: 'Install or remodel quote' },
        { value: 'other', label: 'Something else' }
      ]
    },
    electrical: {
      headline: 'What electrical issue are you dealing with?',
      subheadline: 'Safety first — sparking or no power gets routed immediately.',
      issueOptions: [
        { value: 'no_power', label: 'No power / breaker tripping' },
        { value: 'sparking', label: 'Sparking or burning smell' },
        { value: 'panel', label: 'Panel upgrade' },
        { value: 'install', label: 'Install or repair' },
        { value: 'quote', label: 'Estimate / quote' },
        { value: 'other', label: 'Something else' }
      ]
    },
    roofing: {
      headline: 'Describe your roofing need',
      subheadline: 'Active leaks and storm damage are prioritized.',
      issueOptions: [
        { value: 'roof_leak', label: 'Active roof leak' },
        { value: 'storm', label: 'Storm damage' },
        { value: 'inspection', label: 'Inspection' },
        { value: 'replacement', label: 'Full replacement' },
        { value: 'quote', label: 'Estimate / quote' },
        { value: 'other', label: 'Something else' }
      ]
    },
    general: {
      headline: 'How can we help?',
      subheadline: 'Share a few details and we will follow up shortly.',
      issueOptions: [
        { value: 'repair', label: 'Repair needed' },
        { value: 'maintenance', label: 'Maintenance' },
        { value: 'quote', label: 'Quote / estimate' },
        { value: 'other', label: 'Something else' }
      ]
    }
  };

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function sanitizeTrade(trade) {
    var allowed = ['hvac', 'plumbing', 'electrical', 'roofing', 'general'];
    trade = String(trade || 'hvac').toLowerCase();
    return allowed.indexOf(trade) > -1 ? trade : 'hvac';
  }

  function parseBool(value, fallback) {
    if (value === undefined || value === null || value === '') {
      return fallback;
    }
    if (typeof value === 'boolean') {
      return value;
    }
    return String(value).toLowerCase() === 'true' || value === '1';
  }

  function getScriptTag() {
    return document.currentScript || document.querySelector('script[data-saddle-up-lead-desk],script[src*="embed.js"]');
  }

  function getAssetBase(script) {
    if (!script || !script.src) {
      return './';
    }
    return script.src.replace(/[^/]+$/, '');
  }

  function loadStylesheet(href) {
    if (document.querySelector('link[data-suld-widget-css]')) {
      return;
    }
    var link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = href;
    link.setAttribute('data-suld-widget-css', '1');
    document.head.appendChild(link);
  }

  function readDataset(el) {
    if (!el || !el.dataset) {
      return {};
    }

    var officeHours = null;
    if (el.dataset.officeHours) {
      try {
        officeHours = JSON.parse(el.dataset.officeHours);
      } catch (error) {
        officeHours = null;
      }
    }

    return {
      siteKey: el.dataset.siteKey || '',
      siteId: el.dataset.siteId || '',
      licenseApiUrl: el.dataset.licenseApiUrl || DEFAULT_LICENSE_API_URL,
      apiUrl: el.dataset.apiUrl || DEFAULT_API_URL,
      configUrl: el.dataset.config || '',
      trade: el.dataset.trade || 'hvac',
      businessName: el.dataset.businessName || '',
      primaryColor: el.dataset.primaryColor || '#c45a11',
      accentColor: el.dataset.accentColor || '#1a2332',
      buttonText: el.dataset.buttonText || 'Get Help Now',
      successMessage: el.dataset.successMessage || 'Thanks! We received your request and will contact you shortly.',
      title: el.dataset.title || '',
      inline: parseBool(el.dataset.inline, false),
      afterHoursMode: parseBool(el.dataset.afterHours, true),
      googleSheetUrl: el.dataset.googleSheetUrl || '',
      webhookUrl: el.dataset.webhookUrl || '',
      officeHours: officeHours
    };
  }

  function mergeConfig() {
    var script = getScriptTag();
    var scriptConfig = readDataset(script);
    var containers = document.querySelectorAll('[data-saddle-up-lead-desk]');
    var containerConfig = containers.length ? readDataset(containers[0]) : {};

    return Object.assign({}, scriptConfig, containerConfig);
  }

  function defaultOfficeHours() {
    return {
      mon: { open: '08:00', close: '17:00' },
      tue: { open: '08:00', close: '17:00' },
      wed: { open: '08:00', close: '17:00' },
      thu: { open: '08:00', close: '17:00' },
      fri: { open: '08:00', close: '17:00' },
      sat: { open: '', close: '' },
      sun: { open: '', close: '' }
    };
  }

  function normalizeConfig(raw) {
    var trade = sanitizeTrade(raw.trade);
    var template = TRADE_TEMPLATES[trade] || TRADE_TEMPLATES.hvac;

    return {
      siteKey: raw.siteKey || raw.site_id || '',
      siteId: raw.siteId || '',
      licenseApiUrl: (raw.licenseApiUrl || raw.license_api_url || DEFAULT_LICENSE_API_URL).replace(/\/$/, ''),
      apiUrl: (raw.apiUrl || DEFAULT_API_URL).replace(/\/$/, ''),
      trade: trade,
      businessName: raw.businessName || document.title || 'Lead Desk',
      primaryColor: raw.primaryColor || '#c45a11',
      accentColor: raw.accentColor || '#1a2332',
      buttonText: raw.buttonText || 'Get Help Now',
      successMessage: raw.successMessage || 'Thanks! We received your request and will contact you shortly.',
      title: raw.title || '',
      inline: parseBool(raw.inline, false),
      afterHoursMode: parseBool(raw.afterHoursMode, true),
      googleSheetUrl: raw.googleSheetUrl || raw.google_sheet_url || '',
      webhookUrl: raw.webhookUrl || '',
      officeHours: raw.officeHours || defaultOfficeHours(),
      questions: Object.assign({}, template, { urgencyOptions: URGENCY_OPTIONS })
    };
  }

  function fetchJsonConfig(url) {
    return fetch(url, { credentials: 'same-origin' }).then(function (response) {
      if (!response.ok) {
        throw new Error('Config fetch failed');
      }
      return response.json();
    });
  }

  function fetchRemoteConfig(config) {
    if (!config.siteKey) {
      return Promise.resolve(config);
    }

    var url = config.apiUrl + '/embed/config?site_key=' + encodeURIComponent(config.siteKey);
    return fetch(url, {
      headers: { 'X-SULD-Embed': VERSION }
    })
      .then(function (response) {
        if (!response.ok) {
          return config;
        }
        return response.json();
      })
      .then(function (remote) {
        return normalizeConfig(Object.assign({}, config, remote || {}));
      })
      .catch(function () {
        return config;
      });
  }

  function isAfterHours(officeHours) {
    var now = new Date();
    var days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'];
    var key = days[now.getDay()];
    var slot = officeHours[key] || { open: '', close: '' };

    if (!slot.open || !slot.close) {
      return true;
    }

    var current = now.getHours() * 60 + now.getMinutes();
    var openParts = slot.open.split(':');
    var closeParts = slot.close.split(':');
    var openMinutes = parseInt(openParts[0], 10) * 60 + parseInt(openParts[1], 10);
    var closeMinutes = parseInt(closeParts[0], 10) * 60 + parseInt(closeParts[1], 10);

    return current < openMinutes || current >= closeMinutes;
  }

  function scoreLead(urgency, issueType) {
    var score = 30;
    var urgencyScores = { emergency: 50, today: 35, this_week: 20, planning: 10 };
    var issueScores = {
      no_heat: 40,
      no_ac: 40,
      water_leak: 45,
      no_power: 45,
      roof_leak: 40,
      maintenance: 10,
      quote: 15,
      other: 20
    };

    score += urgencyScores[urgency] || 15;
    score += issueScores[issueType] || 15;
    score = Math.min(100, score);

    var label = 'Low Priority';
    if (score >= 80) {
      label = 'Emergency';
    } else if (score >= 55) {
      label = 'High Priority';
    } else if (score >= 35) {
      label = 'Standard';
    }

    return { value: score, label: label };
  }

  function renderStepDots(step) {
    var html = '';
    for (var i = 1; i <= STEP_COUNT; i += 1) {
      var cls = 'suld-step-dot';
      if (i < step) {
        cls += ' is-complete';
      } else if (i === step) {
        cls += ' is-active';
      }
      html += '<div class="' + cls + '" aria-hidden="true"></div>';
    }
    return '<div class="suld-steps" aria-label="Form progress">' + html + '</div>';
  }

  function renderOptions(name, options, selected) {
    return options.map(function (option) {
      var isSelected = selected === option.value;
      return (
        '<label class="suld-option' + (isSelected ? ' is-selected' : '') + '">' +
          '<input type="radio" name="' + escapeHtml(name) + '" value="' + escapeHtml(option.value) + '"' + (isSelected ? ' checked' : '') + ' />' +
          '<span>' + escapeHtml(option.label) + '</span>' +
        '</label>'
      );
    }).join('');
  }

  function buildLeadPayload(state, config) {
    return {
      name: state.name,
      phone: state.phone,
      email: state.email,
      zip: state.zip,
      issue_type: state.issue_type,
      urgency: state.urgency,
      description: state.description,
      preferred_contact: state.preferred_contact,
      trade: config.trade,
      source_url: window.location.href,
      page_title: document.title,
      site_url: window.location.origin + '/',
      site_name: config.businessName,
      submitted_at: new Date().toISOString(),
      is_after_hours: isAfterHours(config.officeHours),
      score: scoreLead(state.urgency, state.issue_type),
      site_id: config.siteId || undefined,
      embed_version: VERSION
    };
  }

  function validateLicense(config) {
    if (!config.siteKey) {
      return Promise.resolve({
        active: false,
        status: 'missing',
        message: 'Site key required. Add data-site-key from your purchase confirmation.',
        billing_url: ''
      });
    }

    var cacheKey = 'suld_license_' + config.siteKey;
    try {
      var cached = sessionStorage.getItem(cacheKey);
      if (cached) {
        var parsed = JSON.parse(cached);
        if (parsed.expires > Date.now()) {
          return Promise.resolve(parsed.data);
        }
        sessionStorage.removeItem(cacheKey);
      }
    } catch (error) {
      // ignore cache errors
    }

    var url = config.licenseApiUrl + '/v1/license/validate?site_key=' + encodeURIComponent(config.siteKey);

    return fetch(url, { headers: { Accept: 'application/json' } })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        try {
          sessionStorage.setItem(cacheKey, JSON.stringify({
            expires: Date.now() + LICENSE_CACHE_MS,
            data: data
          }));
        } catch (error) {
          // ignore
        }
        return data;
      })
      .catch(function () {
        return {
          active: false,
          status: 'unreachable',
          message: 'Unable to verify subscription. Check your connection.',
          billing_url: ''
        };
      });
  }

  function renderInactiveWidget(root, license) {
    root.classList.add('suld-widget', 'suld-widget--inactive');
    var billing = license.billing_url
      ? '<p style="margin:0.75rem 0 0"><a href="' + escapeHtml(license.billing_url) + '" style="color:inherit;font-weight:700" target="_blank" rel="noopener">Renew subscription →</a></p>'
      : '';
    root.innerHTML =
      '<div class="suld-card">' +
        '<div class="suld-card__body">' +
          '<div class="suld-alert suld-alert--error" style="margin-bottom:0">' +
            '<strong>Lead form unavailable</strong><br>' +
            escapeHtml(license.message || 'Subscription inactive.') +
            billing +
          '</div>' +
        '</div>' +
      '</div>';
  }

  function submitToGoogleSheet(sheetUrl, payload) {
    return fetch(sheetUrl, {
      method: 'POST',
      mode: 'no-cors',
      headers: {
        'Content-Type': 'text/plain;charset=utf-8'
      },
      body: JSON.stringify(payload)
    }).then(function () {
      return { success: true, message: 'Lead saved.' };
    });
  }

  function submitLeadEverywhere(config, payload) {
    var tasks = [];

    if (config.googleSheetUrl) {
      tasks.push(submitToGoogleSheet(config.googleSheetUrl, payload));
    }

    if (config.siteKey) {
      tasks.push(
        submitToApi(config, payload).catch(function (error) {
          if (config.googleSheetUrl) {
            return { skipped: true };
          }
          throw error;
        })
      );
    }

    if (!config.googleSheetUrl && !config.siteKey && config.webhookUrl) {
      tasks.push(submitToWebhook(config, payload));
    }

    if (!tasks.length) {
      return Promise.reject(new Error('Add data-site-key from your Lead Desk subscription.'));
    }

    return Promise.allSettled(tasks).then(function (results) {
      var fulfilled = results.filter(function (result) {
        return result.status === 'fulfilled';
      });

      if (!fulfilled.length) {
        var reason = results[0] && results[0].reason;
        throw new Error((reason && reason.message) || 'Unable to submit lead.');
      }

      return {
        success: true,
        message: config.successMessage
      };
    });
  }

  function submitToApi(config, payload) {
    if (!config.siteKey) {
      return Promise.reject(new Error('Missing site key. Add data-site-key to your embed code.'));
    }

    return fetch(config.apiUrl + '/leads', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Site-Key': config.siteKey,
        'X-SULD-Embed': VERSION
      },
      body: JSON.stringify(payload)
    }).then(function (response) {
      return response.json().catch(function () {
        return {};
      }).then(function (data) {
        if (!response.ok) {
          throw new Error((data && (data.message || data.error)) || 'Unable to submit lead.');
        }
        return data;
      });
    });
  }

  function submitToWebhook(config, payload) {
    if (!config.webhookUrl) {
      return Promise.reject(new Error('No webhook configured.'));
    }

    return fetch(config.webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(function (response) {
      if (!response.ok) {
        throw new Error('Webhook submission failed.');
      }
      return { success: true, message: config.successMessage };
    });
  }

  function buildWidget(root, config) {
    var state = {
      step: 1,
      issue_type: '',
      urgency: '',
      name: '',
      phone: '',
      email: '',
      zip: '',
      description: '',
      preferred_contact: 'phone',
      submitting: false,
      error: ''
    };

    root.classList.add('suld-widget');
    if (config.inline) {
      root.classList.add('suld-widget--inline');
    }

    root.style.setProperty('--suld-primary', config.primaryColor);
    root.style.setProperty('--suld-accent', config.accentColor);

    function afterHoursBanner() {
      if (!config.afterHoursMode || !isAfterHours(config.officeHours)) {
        return '';
      }
      return (
        '<div class="suld-alert suld-alert--info">' +
          '<strong>After hours:</strong> We are currently closed. Submit your request and we will contact you first thing.' +
        '</div>'
      );
    }

    function render() {
      var questions = config.questions;
      var headline = config.title || questions.headline || 'How can we help?';
      var body = '';

      if (state.error) {
        body += '<div class="suld-alert suld-alert--error">' + escapeHtml(state.error) + '</div>';
      }

      body += afterHoursBanner();
      body += renderStepDots(state.step);

      if (state.step === 1) {
        body += '<div class="suld-options">' + renderOptions('issue_type', questions.issueOptions, state.issue_type) + '</div>';
      } else if (state.step === 2) {
        body += '<div class="suld-options">' + renderOptions('urgency', questions.urgencyOptions, state.urgency) + '</div>';
      } else {
        body += (
          '<div class="suld-grid-2">' +
            '<div class="suld-field"><label for="suld-name">Name *</label><input id="suld-name" name="name" value="' + escapeHtml(state.name) + '" required /></div>' +
            '<div class="suld-field"><label for="suld-phone">Phone *</label><input id="suld-phone" name="phone" type="tel" value="' + escapeHtml(state.phone) + '" required /></div>' +
          '</div>' +
          '<div class="suld-grid-2">' +
            '<div class="suld-field"><label for="suld-email">Email</label><input id="suld-email" name="email" type="email" value="' + escapeHtml(state.email) + '" /></div>' +
            '<div class="suld-field"><label for="suld-zip">ZIP code *</label><input id="suld-zip" name="zip" value="' + escapeHtml(state.zip) + '" required /></div>' +
          '</div>' +
          '<div class="suld-field"><label for="suld-description">Anything else we should know?</label><textarea id="suld-description" name="description">' + escapeHtml(state.description) + '</textarea></div>' +
          '<div class="suld-field"><label for="suld-contact">Preferred contact</label><select id="suld-contact" name="preferred_contact">' +
            '<option value="phone"' + (state.preferred_contact === 'phone' ? ' selected' : '') + '>Phone</option>' +
            '<option value="text"' + (state.preferred_contact === 'text' ? ' selected' : '') + '>Text</option>' +
            '<option value="email"' + (state.preferred_contact === 'email' ? ' selected' : '') + '>Email</option>' +
          '</select></div>'
        );
      }

      var actions = '';
      if (state.step > 1) {
        actions += '<button type="button" class="suld-btn suld-btn--ghost" data-action="back">Back</button>';
      }
      if (state.step < STEP_COUNT) {
        actions += '<button type="button" class="suld-btn suld-btn--primary" data-action="next">Continue</button>';
      } else {
        actions += '<button type="button" class="suld-btn suld-btn--primary" data-action="submit"' + (state.submitting ? ' disabled' : '') + '>' +
          escapeHtml(config.buttonText) + '</button>';
      }

      root.innerHTML =
        '<div class="suld-card">' +
          '<div class="suld-card__header">' +
            '<div class="suld-card__badge">' + escapeHtml(config.trade.toUpperCase()) + ' Lead Desk</div>' +
            '<h2 class="suld-card__title">' + escapeHtml(headline) + '</h2>' +
            '<p class="suld-card__subtitle">' + escapeHtml(questions.subheadline || '') + '</p>' +
          '</div>' +
          '<div class="suld-card__body">' + body + '<div class="suld-actions">' + actions + '</div></div>' +
        '</div>';

      bindEvents();
    }

    function bindEvents() {
      root.querySelectorAll('.suld-option input').forEach(function (input) {
        input.addEventListener('change', function (event) {
          state[event.target.name] = event.target.value;
          root.querySelectorAll('label.suld-option').forEach(function (label) {
            label.classList.toggle('is-selected', label.contains(event.target));
          });
        });
      });

      ['name', 'phone', 'email', 'zip', 'description', 'preferred_contact'].forEach(function (field) {
        var el = root.querySelector('[name="' + field + '"]');
        if (!el) {
          return;
        }
        el.addEventListener('input', function (event) {
          state[field] = event.target.value;
        });
      });

      var backBtn = root.querySelector('[data-action="back"]');
      if (backBtn) {
        backBtn.addEventListener('click', function () {
          state.error = '';
          state.step -= 1;
          render();
        });
      }

      var nextBtn = root.querySelector('[data-action="next"]');
      if (nextBtn) {
        nextBtn.addEventListener('click', function () {
          state.error = '';
          if (state.step === 1 && !state.issue_type) {
            state.error = 'Please select an issue type.';
            render();
            return;
          }
          if (state.step === 2 && !state.urgency) {
            state.error = 'Please select how soon you need help.';
            render();
            return;
          }
          state.step += 1;
          render();
        });
      }

      var submitBtn = root.querySelector('[data-action="submit"]');
      if (submitBtn) {
        submitBtn.addEventListener('click', submitLead);
      }
    }

    function submitLead() {
      state.error = '';

      if (!state.name || !state.phone || !state.zip) {
        state.error = 'Please fill in name, phone, and ZIP code.';
        render();
        return;
      }

      state.submitting = true;
      render();

      var payload = buildLeadPayload(state, config);

      submitLeadEverywhere(config, payload)
        .then(function (data) {
          root.innerHTML =
            '<div class="suld-card">' +
              '<div class="suld-success">' +
                '<div class="suld-success__icon">✓</div>' +
                '<h3>Request received</h3>' +
                '<p>' + escapeHtml((data && data.message) || config.successMessage) + '</p>' +
              '</div>' +
            '</div>';
        })
        .catch(function (error) {
          state.submitting = false;
          state.error = error.message || 'Something went wrong. Please try again.';
          render();
        });
    }

    render();
  }

  function resolveConfig(raw) {
    var config = normalizeConfig(raw);
    var chain = Promise.resolve(config);

    if (raw.configUrl) {
      chain = chain.then(function () {
        return fetchJsonConfig(raw.configUrl).then(function (fileConfig) {
          return normalizeConfig(Object.assign({}, raw, fileConfig));
        });
      });
    }

    return chain.then(fetchRemoteConfig);
  }

  function initContainer(container, config) {
    container.innerHTML = '<div class="suld-widget__loading">Loading lead form…</div>';
    resolveConfig(config)
      .then(function (resolved) {
        return validateLicense(resolved).then(function (license) {
          if (!license.active) {
            renderInactiveWidget(container, license);
            return;
          }
          buildWidget(container, resolved);
        });
      })
      .catch(function () {
        container.innerHTML = '<div class="suld-alert suld-alert--error">Unable to load the lead form.</div>';
      });
  }

  function boot() {
    var script = getScriptTag();
    var base = getAssetBase(script);
    loadStylesheet(base + 'widget.css');

    var merged = mergeConfig();
    var containers = document.querySelectorAll('[data-saddle-up-lead-desk]');

    if (!containers.length) {
      var auto = document.createElement('div');
      auto.setAttribute('data-saddle-up-lead-desk', '');
      if (script && script.parentNode) {
        script.parentNode.insertBefore(auto, script);
      } else {
        document.body.appendChild(auto);
      }
      containers = document.querySelectorAll('[data-saddle-up-lead-desk]');
    }

    containers.forEach(function (container) {
      var config = Object.assign({}, merged, readDataset(container));
      initContainer(container, config);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
