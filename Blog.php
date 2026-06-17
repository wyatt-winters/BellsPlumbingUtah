<?php
/**
 * Smart blog index — wakes the bot if cron was missed, then serves Blog.html.
 */
declare(strict_types=1);

$root = __DIR__;
require_once $root . '/blog/lib/BlogBot.php';

$config = require $root . '/blog/config.php';
date_default_timezone_set($config['timezone'] ?? 'America/Denver');

$bot = new BlogBot($root);
$state = $bot->getState();
$staleHours = 26;

$needsWake = true;
if (!empty($state['heartbeat_at'])) {
    $last = strtotime($state['heartbeat_at']);
    $needsWake = ($last === false) || (time() - $last > $staleHours * 3600);
}

if ($needsWake) {
    try {
        $bot->run(date('Y-m-d'), false);
    } catch (Throwable $e) {
        // Still serve blog if wake fails
    }
}

$blogHtml = $root . '/Blog.html';
if (is_readable($blogHtml)) {
    header('Content-Type: text/html; charset=utf-8');
    readfile($blogHtml);
    exit;
}

http_response_code(503);
echo '<!DOCTYPE html><html><body><h1>Blog loading</h1><p>Run the blog bot once to initialize.</p></body></html>';
