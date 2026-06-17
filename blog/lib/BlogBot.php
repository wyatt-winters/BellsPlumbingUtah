<?php

require_once __DIR__ . '/BlogPublisher.php';
require_once __DIR__ . '/TopicFactory.php';

/**
 * Self-contained blog organism for cPanel.
 * Creates pages, publishes on schedule, refills its topic queue, maintains sitemap/index.
 */
class BlogBot
{
    private $root;
    private $cfg;
    private BlogPublisher $publisher;
    private TopicFactory $factory;

    public function __construct(?string $root = null)
    {
        $this->root = $root ?: dirname(dirname(__DIR__));
        $this->cfg = require $this->root . '/blog/config.php';
        date_default_timezone_set($this->cfg['timezone'] ?? 'America/Denver');
        $this->publisher = new BlogPublisher($this->root);
        $this->factory = new TopicFactory($this->cfg);
    }

    /**
     * Main heartbeat — run once daily from cPanel cron.
     */
    public function run(?string $asOf = null, bool $forcePublishAll = false): array
    {
        $asOf = $asOf ?: date('Y-m-d');
        $state = $this->loadState();
        $topics = $this->loadTopics();

        $refill = $this->refillQueueIfNeeded($topics, $asOf);
        if ($refill['added'] > 0) {
            $topics = $this->loadTopics();
            $this->log('queue_refill', $refill);
        }

        $build = $this->publisher->build($asOf, $forcePublishAll);

        $state['heartbeat_at'] = date('c');
        $state['last_run'] = $asOf;
        $state['bot_version'] = $this->cfg['bot_version'] ?? '1.0.0';
        $state['status'] = 'alive';
        $state['total_published'] = $build['published_count'];
        $state['total_queued'] = count($topics) + ($refill['added'] ?? 0);
        $state['queue_days_ahead'] = $this->daysAhead($topics, $asOf);
        $state['last_new_posts'] = $build['newly_published'];
        $state['runs'] = ($state['runs'] ?? 0) + 1;
        $this->saveState($state);

        $result = array_merge($build, [
            'bot_status' => 'alive',
            'queue_refilled' => $refill['added'],
            'queue_days_ahead' => $state['queue_days_ahead'],
            'heartbeat_at' => $state['heartbeat_at'],
        ]);

        $this->log('heartbeat', $result);

        return $result;
    }

    public function getState(): array
    {
        return $this->loadState();
    }

    public function getTopics(): array
    {
        return $this->loadTopics();
    }

    public function getSchedule(): array
    {
        $path = $this->root . '/blog/schedule.json';
        if (!is_readable($path)) {
            return ['published_slugs' => []];
        }
        $data = json_decode(file_get_contents($path), true);
        return is_array($data) ? $data : ['published_slugs' => []];
    }

    public function getRecentLogs(int $lines = 20): array
    {
        $path = $this->root . '/blog/bot.log';
        if (!is_readable($path)) {
            return [];
        }
        $all = file($path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) ?: [];
        return array_slice(array_reverse($all), 0, $lines);
    }

    private function refillQueueIfNeeded(array $topics, string $asOf): array
    {
        $daysAhead = $this->daysAhead($topics, $asOf);
        $threshold = (int) ($this->cfg['queue_refill_days'] ?? 30);
        $batch = (int) ($this->cfg['queue_batch_size'] ?? 45);

        if ($daysAhead >= $threshold) {
            return ['added' => 0, 'days_ahead' => $daysAhead, 'reason' => 'queue_healthy'];
        }

        $lastDate = $asOf;
        foreach ($topics as $t) {
            if ($t['publish_date'] > $lastDate) {
                $lastDate = $t['publish_date'];
            }
        }
        $start = (new DateTimeImmutable($lastDate))->modify('+1 day')->format('Y-m-d');

        $newTopics = $this->factory->generateBatch($topics, $start, $batch);
        if (!$newTopics) {
            return ['added' => 0, 'days_ahead' => $daysAhead, 'reason' => 'generation_failed'];
        }

        $merged = array_merge($topics, $newTopics);
        $this->saveTopics($merged);

        return [
            'added' => count($newTopics),
            'days_ahead' => $this->daysAhead($merged, $asOf),
            'next_start' => $start,
            'reason' => 'refilled',
        ];
    }

    private function daysAhead(array $topics, string $asOf): int
    {
        $future = 0;
        $schedule = $this->getSchedule();
        $published = array_flip($schedule['published_slugs'] ?? []);

        foreach ($topics as $t) {
            if ($t['publish_date'] >= $asOf && !isset($published[$t['slug']])) {
                $future++;
            }
        }
        return $future;
    }

    private function loadTopics(): array
    {
        $path = $this->root . '/blog/posts.json';
        if (!is_readable($path)) {
            return [];
        }
        $data = json_decode(file_get_contents($path), true);
        return is_array($data) ? $data : [];
    }

    private function saveTopics(array $topics): void
    {
        file_put_contents(
            $this->root . '/blog/posts.json',
            json_encode($topics, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . "\n"
        );
    }

    private function loadState(): array
    {
        $path = $this->root . '/blog/bot-state.json';
        if (!is_readable($path)) {
            return [
                'status' => 'new',
                'runs' => 0,
                'installed_at' => date('c'),
            ];
        }
        $data = json_decode(file_get_contents($path), true);
        return is_array($data) ? $data : [];
    }

    private function saveState(array $state): void
    {
        file_put_contents(
            $this->root . '/blog/bot-state.json',
            json_encode($state, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . "\n"
        );
    }

    private function log(string $event, array $data): void
    {
        $line = date('c') . "\t{$event}\t" . json_encode($data, JSON_UNESCAPED_SLASHES) . "\n";
        $path = $this->root . '/blog/bot.log';
        file_put_contents($path, $line, FILE_APPEND | LOCK_EX);

        $max = (int) ($this->cfg['max_log_lines'] ?? 500);
        if ($max > 0 && is_readable($path)) {
            $lines = file($path, FILE_IGNORE_NEW_LINES) ?: [];
            if (count($lines) > $max) {
                $trimmed = array_slice($lines, -$max);
                file_put_contents($path, implode("\n", $trimmed) . "\n");
            }
        }
    }
}
