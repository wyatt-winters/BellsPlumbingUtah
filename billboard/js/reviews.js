/* =====================================================================
   Utah Boiler Experts — sitewide Google reviews client
   =====================================================================
   Fetches /reviews.php once per page load and populates ANY of these
   targets that happen to exist on the current page:

     - Hero rating strip (homepage):  #google-rating-strip wrapper
       └── #grs-score, #grs-count
     - Review section header (homepage):
       └── #g-rating-header, #g-rating-score, #g-rating-stars,
           #g-rating-count, #g-rating-link
     - Review grid (homepage):
       └── #g-reviews-grid (populated from data) + #g-reviews-fallback
     - Footer badge (every page):
       └── #fgr-rating, #fgr-count, #fgr-link

   If /reviews.php returns an error (config not yet set, API quota,
   network issue), every page keeps showing its placeholder "—" or
   static fallback. No console errors, no broken UI.
   ===================================================================== */

(function () {
  'use strict';

  // Skip the fetch entirely if no review element exists on the page
  if (!document.querySelector('#g-rating-header, #google-rating-strip, #footer-google-rating, #g-reviews-grid')) {
    return;
  }

  fetch('/reviews.php', { credentials: 'omit' })
    .then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    })
    .then(function (data) {
      if (!data || data.error) {
        if (window.console && data && data.error) {
          console.info('[reviews] not configured:', data.message || data.error);
        }
        return; // leave placeholders + static fallback in place
      }
      render(data);
    })
    .catch(function (err) {
      if (window.console) console.info('[reviews] fetch skipped:', err.message);
      // Leave placeholders in place — they're already designed to be readable
    });

  // ---------- rendering ----------

  function render(data) {
    var rating = (typeof data.rating === 'number') ? data.rating.toFixed(1) : null;
    var count  = (typeof data.userRatingCount === 'number') ? data.userRatingCount : null;
    var url    = data.googleMapsUri || null;

    // 1) Homepage hero strip
    setText('grs-score', rating);
    setText('grs-count', count !== null ? formatCount(count) : null);
    setHref('google-rating-strip', url);

    // 2) Homepage in-section header
    setText('g-rating-score', rating);
    setText('g-rating-stars', rating ? starStr(rating) : null);
    if (count !== null) {
      setText('g-rating-count', formatCount(count) + (count === 1 ? ' review' : ' reviews'));
    }
    setHref('g-rating-link', url);
    var ratingHeader = document.getElementById('g-rating-header');
    if (ratingHeader && rating) ratingHeader.style.display = 'flex';

    // 3) Footer badge (every page)
    setText('fgr-rating', rating);
    setText('fgr-count', count !== null ? formatCount(count) : null);
    setHref('fgr-link', url);

    // 4) Homepage live review grid
    var grid     = document.getElementById('g-reviews-grid');
    var fallback = document.getElementById('g-reviews-fallback');
    if (grid && Array.isArray(data.reviews) && data.reviews.length > 0) {
      var positive = data.reviews.filter(function (r) {
        return (Number(r.rating) || 0) >= 4;
      });
      if (positive.length > 0) {
        grid.innerHTML = positive.slice(0, 6).map(reviewCardHTML).join('');
        grid.style.display = '';
        if (fallback) fallback.style.display = 'none';
      }
    }
  }

  function reviewCardHTML(r) {
    var rating   = r.rating || 5;
    var author   = (r.authorAttribution && r.authorAttribution.displayName) || 'Google user';
    var photoUri = r.authorAttribution && r.authorAttribution.photoUri;
    var when     = relativeTime(r.publishTime) || (r.relativePublishTimeDescription || '');
    var text     = (r.text && r.text.text) || (r.originalText && r.originalText.text) || '';
    var initial  = author.charAt(0).toUpperCase();

    var avatarInner = photoUri
      ? '<img src="' + escapeHTML(photoUri) + '" alt="" referrerpolicy="no-referrer" loading="lazy">'
      : escapeHTML(initial);

    return ''
      + '<article class="g-review-card">'
      +   '<div class="g-review-head">'
      +     '<div class="g-review-avatar">' + avatarInner + '</div>'
      +     '<div>'
      +       '<div class="g-review-author">' + escapeHTML(author) + '</div>'
      +       (when ? '<div class="g-review-when">' + escapeHTML(when) + ' · via Google</div>' : '')
      +     '</div>'
      +   '</div>'
      +   '<div class="g-review-stars" aria-label="' + rating + ' out of 5 stars">' + starStr(rating) + '</div>'
      +   '<p class="g-review-text">' + escapeHTML(text) + '</p>'
      + '</article>';
  }

  // ---------- helpers ----------

  function setText(id, value) {
    if (value === null || value === undefined) return;
    var el = document.getElementById(id);
    if (el) el.textContent = String(value);
  }

  function setHref(id, url) {
    if (!url) return;
    var el = document.getElementById(id);
    if (el && el.tagName === 'A') el.setAttribute('href', url);
  }

  function starStr(n) {
    var rounded = Math.round(Number(n) || 0);
    if (rounded < 0) rounded = 0;
    if (rounded > 5) rounded = 5;
    return '★★★★★'.slice(0, rounded) + '☆☆☆☆☆'.slice(0, 5 - rounded);
  }

  function formatCount(n) {
    return Number(n).toLocaleString();
  }

  function relativeTime(iso) {
    if (!iso) return '';
    var then = new Date(iso).getTime();
    if (isNaN(then)) return '';
    var diff = Math.floor((Date.now() - then) / 86400000);
    if (diff < 1)   return 'today';
    if (diff < 7)   return diff + ' day' + (diff === 1 ? '' : 's') + ' ago';
    if (diff < 30)  { var w = Math.floor(diff / 7);   return w + ' week'  + (w === 1 ? '' : 's') + ' ago'; }
    if (diff < 365) { var m = Math.floor(diff / 30);  return m + ' month' + (m === 1 ? '' : 's') + ' ago'; }
    var y = Math.floor(diff / 365);
    return y + ' year' + (y === 1 ? '' : 's') + ' ago';
  }

  function escapeHTML(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  }
})();
