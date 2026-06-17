<?php
header('Content-Type: text/plain; charset=utf-8');
echo 'PHP ' . PHP_VERSION . "\n";
echo 'BlogBot file: ' . (file_exists(__DIR__ . '/lib/BlogBot.php') ? 'yes' : 'no') . "\n";
require_once __DIR__ . '/lib/BlogBot.php';
echo "BlogBot class loaded\n";
$bot = new BlogBot(dirname(__DIR__));
echo "Bot run OK\n";
print_r($bot->run(date('Y-m-d'), false));
