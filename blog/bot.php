<?php
/**
 * Blog Bot — single cron entry point for cPanel.
 *
 * cPanel Cron (daily):
 *   /usr/local/bin/php /home/USER/public_html/blog/bot.php
 *
 * URL cron:
 *   curl -s "https://bellsplumbingutah.com/blog/bot.php?key=YOUR_SECRET"
 */
declare(strict_types=1);

require_once __DIR__ . '/lib/BlogBot.php';

$config = require __DIR__ . '/config.php';
$isCli = PHP_SAPI === 'cli';

if (!$isCli) {
    $key = $_GET['key'] ?? '';
    if (!hash_equals((string) $config['cron_secret'], (string) $key)) {
        http_response_code(403);
        header('Content-Type: text/plain; charset=utf-8');
        echo "Forbidden\n";
        exit;
    }
    header('Content-Type: application/json; charset=utf-8');
}

try {
    $root = dirname(__DIR__);
    $bot = new BlogBot($root);

    $forceAll = $isCli
        ? in_array('all', $argv ?? [], true)
        : isset($_GET['all']);

    $asOf = date('Y-m-d');
    if ($isCli) {
        foreach ($argv ?? [] as $arg) {
            if (strpos($arg, '--date=') === 0) {
                $asOf = substr($arg, 7);
            }
        }
    } elseif (!empty($_GET['date']) && preg_match('/^\d{4}-\d{2}-\d{2}$/', (string) $_GET['date'])) {
        $asOf = (string) $_GET['date'];
    }

    $result = $bot->run($asOf, $forceAll);
    $output = json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);

    if ($isCli) {
        echo $output . "\n";
    } else {
        echo $output;
    }
} catch (Throwable $e) {
    $msg = json_encode(['error' => $e->getMessage(), 'bot_status' => 'error'], JSON_PRETTY_PRINT);
    if ($isCli) {
        fwrite(STDERR, $msg . "\n");
        exit(1);
    }
    http_response_code(500);
    echo $msg;
    exit(1);
}
