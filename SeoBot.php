<?php
/**
 * SEO Bot — Blog organism dashboard (footer link: /SeoBot)
 * Visit: /SeoBot?key=YOUR_CRON_SECRET
 */
declare(strict_types=1);

$root = __DIR__;
require_once $root . '/blog/lib/BlogBot.php';

$config = require $root . '/blog/config.php';
$key = $_GET['key'] ?? $_POST['key'] ?? '';

if (!hash_equals((string) $config['cron_secret'], (string) $key)) {
    http_response_code(403);
    ?><!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>SEO Bot</title>
<style>body{font-family:system-ui,sans-serif;background:#0B1D3A;color:#fff;display:grid;place-items:center;min-height:100vh;margin:0}
.box{background:#13294d;padding:2rem;border-radius:1rem;max-width:420px;text-align:center}
code{background:#0B1D3A;padding:.2rem .4rem;border-radius:.25rem}</style></head>
<body><div class="box"><h1>🤖 SEO Bot</h1><p>Access denied.</p><p>Add <code>?key=YOUR_SECRET</code> to the URL.</p></div></body></html><?php
    exit;
}

$bot = new BlogBot($root);
$message = '';
$result = null;
$isError = false;

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['run'])) {
    try {
        $forceAll = !empty($_POST['all']);
        $result = $bot->run(date('Y-m-d'), $forceAll);
        $message = $forceAll
            ? 'Bot ran full publish — all due posts are live.'
            : ('Bot heartbeat OK — ' . count($result['newly_published'] ?? []) . ' new post(s) published.');
        if (!empty($result['queue_refilled'])) {
            $message .= ' Queue refilled: +' . $result['queue_refilled'] . ' topics.';
        }
    } catch (Throwable $e) {
        $message = 'Error: ' . $e->getMessage();
        $isError = true;
    }
}

$state = $bot->getState();
$schedule = $bot->getSchedule();
$topics = $bot->getTopics();
$logs = $bot->getRecentLogs(8);
$today = date('Y-m-d');
$published = count($schedule['published_slugs'] ?? []);
$total = count($topics);
$daysAhead = $state['queue_days_ahead'] ?? 0;

$next = null;
foreach ($topics as $t) {
    if ($t['publish_date'] >= $today && !in_array($t['slug'], $schedule['published_slugs'] ?? [], true)) {
        $next = $t;
        break;
    }
}

$status = $state['status'] ?? 'unknown';
$heartbeat = $state['heartbeat_at'] ?? 'Never';
$esc = fn ($s) => htmlspecialchars((string) $s, ENT_QUOTES, 'UTF-8');
$statusColor = $status === 'alive' ? '#22c55e' : '#f59e0b';
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex,nofollow">
  <title>SEO Bot — Bells Plumbing</title>
  <style>
    *{box-sizing:border-box}
    body{font-family:system-ui,-apple-system,sans-serif;background:#0B1D3A;color:#e2e8f0;margin:0;padding:1.5rem}
    .wrap{max-width:720px;margin:0 auto}
    h1{font-size:1.6rem;margin:0;display:flex;align-items:center;gap:.5rem}
    .pulse{width:10px;height:10px;border-radius:50%;background:<?= $statusColor ?>;box-shadow:0 0 8px <?= $statusColor ?>;animation:pulse 2s infinite}
    @keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
    .sub{color:#94a3b8;margin:.35rem 0 1.5rem;font-size:.9rem}
    .card{background:#13294d;border:1px solid #1e3a5f;border-radius:1rem;padding:1.25rem;margin-bottom:1rem}
    .card h2{font-size:.75rem;text-transform:uppercase;letter-spacing:.1em;color:#F5A623;margin:0 0 .75rem}
    .stat{display:flex;justify-content:space-between;padding:.45rem 0;border-bottom:1px solid #1e3a5f;font-size:.9rem}
    .stat:last-child{border:0}
    .btn{display:inline-block;background:#F5A623;color:#0B1D3A;font-weight:700;border:0;border-radius:.5rem;padding:.7rem 1.2rem;cursor:pointer;margin:.25rem .25rem .25rem 0;font-size:.9rem}
    .btn:hover{background:#D4891A}
    .btn-dark{background:#1e3a5f;color:#fff}
    .msg{padding:.75rem 1rem;border-radius:.5rem;margin-bottom:1rem;font-size:.9rem}
    .msg-ok{background:#064e3b;color:#a7f3d0;border:1px solid #059669}
    .msg-err{background:#450a0a;color:#fecaca;border:1px solid #dc2626}
    pre{background:#0B1D3A;padding:.75rem;border-radius:.5rem;font-size:.75rem;overflow:auto;margin:0}
    .log{font-size:.75rem;color:#94a3b8;font-family:monospace;padding:.25rem 0;border-bottom:1px solid #1e3a5f}
    .log:last-child{border:0}
    code{background:#0B1D3A;padding:.1rem .35rem;border-radius:.2rem;font-size:.8rem}
    .organism{display:grid;grid-template-columns:repeat(3,1fr);gap:.75rem;margin-bottom:1rem}
    .org-cell{background:#13294d;border:1px solid #1e3a5f;border-radius:.75rem;padding:1rem;text-align:center}
    .org-cell strong{display:block;font-size:1.4rem;color:#F5A623}
    .org-cell span{font-size:.75rem;color:#94a3b8}
  </style>
</head>
<body>
<div class="wrap">
  <h1><span class="pulse"></span> SEO Bot</h1>
  <p class="sub">Self-running blog organism · v<?= $esc($state['bot_version'] ?? '1.0') ?> · creates pages, publishes daily, refills its queue</p>

  <?php if ($message): ?>
    <div class="msg <?= $isError ? 'msg-err' : 'msg-ok' ?>"><?= $esc($message) ?></div>
  <?php endif; ?>

  <div class="organism">
    <div class="org-cell"><strong><?= $esc(strtoupper($status)) ?></strong><span>Status</span></div>
    <div class="org-cell"><strong><?= $published ?></strong><span>Posts live</span></div>
    <div class="org-cell"><strong><?= $daysAhead ?></strong><span>Days queued</span></div>
  </div>

  <div class="card">
    <h2>Heartbeat</h2>
    <div class="stat"><span>Last pulse</span><strong><?= $esc($heartbeat) ?></strong></div>
    <div class="stat"><span>Total runs</span><strong><?= $esc($state['runs'] ?? 0) ?></strong></div>
    <div class="stat"><span>Queue</span><strong><?= $published ?> / <?= $total ?> topics</strong></div>
    <?php if ($next): ?>
    <div class="stat"><span>Next post</span><strong style="max-width:60%;text-align:right;font-size:.8rem"><?= $esc($next['title']) ?><br><span style="color:#94a3b8"><?= $esc($next['publish_date']) ?></span></strong></div>
    <?php endif; ?>
  </div>

  <?php if ($result): ?>
  <div class="card"><h2>Last run output</h2><pre><?= $esc(json_encode($result, JSON_PRETTY_PRINT)) ?></pre></div>
  <?php endif; ?>

  <div class="card">
    <h2>Manual controls</h2>
    <p style="margin:0 0 .75rem;font-size:.85rem;color:#94a3b8">Normally the bot runs itself via cPanel cron. Use these only for testing.</p>
    <form method="post" style="display:inline">
      <input type="hidden" name="key" value="<?= $esc($key) ?>">
      <button type="submit" name="run" value="1" class="btn">Run heartbeat now</button>
    </form>
    <form method="post" style="display:inline" onsubmit="return confirm('Publish ALL scheduled posts immediately?');">
      <input type="hidden" name="key" value="<?= $esc($key) ?>">
      <input type="hidden" name="all" value="1">
      <button type="submit" name="run" value="1" class="btn btn-dark">Publish all now</button>
    </form>
    <p style="margin:1rem 0 0;font-size:.78rem;color:#64748b">Cron command:<br><code>/usr/local/bin/php ~/public_html/blog/bot.php</code></p>
  </div>

  <?php if ($logs): ?>
  <div class="card">
    <h2>Recent activity</h2>
    <?php foreach ($logs as $line): ?>
      <div class="log"><?= $esc($line) ?></div>
    <?php endforeach; ?>
  </div>
  <?php endif; ?>
</div>
</body>
</html>
