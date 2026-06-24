<?php
/**
 * ============================================================================
 * UTAH BOILER EXPERTS — Google Reviews proxy
 * ============================================================================
 *
 * Fetches Google Places API v1 reviews for the Utah Boiler Experts Google
 * Business Profile, caches the result for 24 hours, and serves it as JSON.
 * The homepage JS hits /reviews.php and renders the result.
 *
 * Why a server-side proxy:
 *   - Hides the API key from the client (browser can't see it)
 *   - Caches responses so we don't hammer the Places API (cost + rate-limit)
 *   - Gives us a stable JSON shape regardless of upstream changes
 *
 * SETUP (one time):
 *   1. Get a Google Maps Platform API key. Restrict it server-side (by IP
 *      of your HostGator server, NOT by HTTP referrer — this is server-to-
 *      server). Enable the Places API (New) for the project.
 *      https://console.cloud.google.com/google/maps-apis/credentials
 *   2. Find your Place ID for "Utah Boiler Experts" Google Business Profile:
 *      https://developers.google.com/maps/documentation/places/web-service/place-id
 *   3. Paste both into the constants below.
 *   4. Upload reviews.php to public_html/ on HostGator.
 *   5. Test by visiting https://utahboilerexperts.com/reviews.php — you
 *      should see JSON. If you see an error, check the API key restriction
 *      and that the Places API (New) is enabled in Google Cloud.
 *
 * NOTE on costs:
 *   With a 24h cache and one fetch per cache miss, this hits the Places API
 *   about 30 times a month. Well inside Google Maps Platform's $200/month
 *   free credit.
 *
 * NOTE on which Place ID:
 *   - If UBE has its own Google Business Profile, use that Place ID.
 *   - If UBE shares The Other Buddy's GBP (same legal entity), use that
 *     Place ID. The reviews will display as the same business reviews.
 *   - If neither GBP has reviews yet, leave the constants as the
 *     PASTE-YOUR-...-HERE values — the homepage will fall back to static
 *     testimonials automatically.
 * ============================================================================
 */

// ---- CONFIGURATION ----------------------------------------------------------

define('GOOGLE_API_KEY', 'AIzaSyBAmUNSloSxL71pavjtJQNGx4kDQr1Ztv4');
define('PLACE_ID',       'ChIJs2uzLFr80qMRyxMPRCbiKGQ');

define('CACHE_FILE',     __DIR__ . '/reviews-cache.json');
define('CACHE_TTL',      86400);  // 24 hours
define('REQUEST_TIMEOUT', 8);     // seconds

// ---- HEADERS ----------------------------------------------------------------

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: public, max-age=3600');  // browsers can cache 1h
header('X-Content-Type-Options: nosniff');

// ---- GUARD: not configured --------------------------------------------------

if (GOOGLE_API_KEY === 'PASTE-YOUR-GOOGLE-API-KEY-HERE' ||
    PLACE_ID === 'PASTE-YOUR-PLACE-ID-HERE') {
    http_response_code(503);
    echo json_encode([
        'error'   => 'not_configured',
        'message' => 'reviews.php has not been configured with an API key and Place ID yet.'
    ]);
    exit;
}

// ---- SERVE FROM CACHE IF FRESH ----------------------------------------------

if (file_exists(CACHE_FILE)) {
    $age = time() - filemtime(CACHE_FILE);
    if ($age < CACHE_TTL) {
        $cached = @file_get_contents(CACHE_FILE);
        if ($cached !== false) {
            header('X-Cache: HIT');
            header('X-Cache-Age: ' . $age);
            echo $cached;
            exit;
        }
    }
}

// ---- FETCH FROM GOOGLE PLACES API (NEW) -------------------------------------

$endpoint = 'https://places.googleapis.com/v1/places/' . rawurlencode(PLACE_ID);

$fieldMask = implode(',', [
    'id',
    'displayName',
    'rating',
    'userRatingCount',
    'googleMapsUri',
    'reviews'
]);

$ch = curl_init($endpoint);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT        => REQUEST_TIMEOUT,
    CURLOPT_CONNECTTIMEOUT => 4,
    CURLOPT_SSL_VERIFYPEER => true,
    CURLOPT_HTTPHEADER     => [
        'X-Goog-Api-Key: ' . GOOGLE_API_KEY,
        'X-Goog-FieldMask: ' . $fieldMask,
        'Accept: application/json'
    ],
]);

$raw       = curl_exec($ch);
$httpCode  = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlErr   = curl_error($ch);
curl_close($ch);

// ---- HANDLE UPSTREAM FAILURE ------------------------------------------------

if ($raw === false || $httpCode !== 200) {
    // Serve stale cache if available — better than nothing
    if (file_exists(CACHE_FILE)) {
        $stale = @file_get_contents(CACHE_FILE);
        if ($stale !== false) {
            header('X-Cache: STALE');
            header('X-Upstream-Status: ' . $httpCode);
            echo $stale;
            exit;
        }
    }
    http_response_code(502);
    echo json_encode([
        'error'   => 'upstream_failed',
        'http'    => $httpCode,
        'message' => $curlErr ?: 'Upstream API returned a non-200 response.'
    ]);
    exit;
}

// ---- NORMALIZE THE RESPONSE -------------------------------------------------

$data = json_decode($raw, true);
if (!is_array($data)) {
    http_response_code(502);
    echo json_encode(['error' => 'bad_json', 'message' => 'Could not decode Places API response.']);
    exit;
}

$reviews = isset($data['reviews']) && is_array($data['reviews']) ? $data['reviews'] : [];

// Filter out reviews with empty text (rating-only)
$reviews = array_values(array_filter($reviews, function($r) {
    $t = '';
    if (isset($r['text']['text'])) $t = $r['text']['text'];
    elseif (isset($r['originalText']['text'])) $t = $r['originalText']['text'];
    return trim($t) !== '';
}));

// Only surface positive reviews (4★ and 5★) on the site
$reviews = array_values(array_filter($reviews, function($r) {
    $rating = isset($r['rating']) ? floatval($r['rating']) : 0;
    return $rating >= 4;
}));

// Sort newest first by publishTime
usort($reviews, function($a, $b) {
    $at = isset($a['publishTime']) ? strtotime($a['publishTime']) : 0;
    $bt = isset($b['publishTime']) ? strtotime($b['publishTime']) : 0;
    return $bt - $at;
});

$normalized = [
    'placeId'         => isset($data['id']) ? $data['id'] : PLACE_ID,
    'displayName'     => isset($data['displayName']['text']) ? $data['displayName']['text'] : 'Utah Boiler Experts',
    'rating'          => isset($data['rating']) ? floatval($data['rating']) : null,
    'userRatingCount' => isset($data['userRatingCount']) ? intval($data['userRatingCount']) : null,
    'googleMapsUri'   => isset($data['googleMapsUri']) ? $data['googleMapsUri'] : null,
    'reviews'         => $reviews,
    'cachedAt'        => time(),
];

$payload = json_encode($normalized);

// ---- WRITE CACHE ------------------------------------------------------------

@file_put_contents(CACHE_FILE, $payload, LOCK_EX);

// ---- SERVE ------------------------------------------------------------------

header('X-Cache: MISS');
echo $payload;
