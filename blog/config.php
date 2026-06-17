<?php
/**
 * Bells Plumbing Blog Bot — lives on cPanel, runs daily via cron.
 */
return [
    'site' => 'https://bellsplumbingutah.com',
    'phone' => '(385) 255-8400',
    'phone_tel' => '3852558400',
    'counties' => 'Davis, Weber, Box Elder, and northern Salt Lake County',
    'timezone' => 'America/Denver',

    // Required for web/cron URL triggers (?key=...)
    'cron_secret' => 'bells-blog-change-me-' . md5('bellsplumbingutah.com'),

    // Bot behavior
    'posts_per_day' => 1,
    'queue_refill_days' => 30,      // generate new topics when fewer than this many days remain
    'queue_batch_size' => 45,       // how many new topics to add each refill
    'max_log_lines' => 500,
    'bot_version' => '1.0.0',
];
