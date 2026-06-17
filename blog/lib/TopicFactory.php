<?php

/**
 * Generates new blog topics when the queue runs low — keeps the bot alive indefinitely.
 */
class TopicFactory
{
    private $cfg;

    private $cities = [
        'Bountiful', 'Layton', 'Ogden', 'Clearfield', 'Kaysville', 'Farmington',
        'Roy', 'Syracuse', 'Centerville', 'Brigham City', 'Clinton', 'North Salt Lake',
        'Woods Cross', 'South Ogden', 'West Point', 'Magna', 'Perry',
    ];

    private $categories = [
        'Emergency' => [
            ['service' => 'emergency plumbing', 'keyword' => 'emergency plumber'],
            ['service' => 'burst pipe repair', 'keyword' => 'burst pipe'],
            ['service' => 'sewer backup repair', 'keyword' => 'sewer backup'],
            ['service' => 'frozen pipe repair', 'keyword' => 'frozen pipes'],
        ],
        'Drain Cleaning' => [
            ['service' => 'drain cleaning', 'keyword' => 'drain cleaning'],
            ['service' => 'hydro jetting', 'keyword' => 'hydro jetting'],
            ['service' => 'main sewer line repair', 'keyword' => 'main line clog'],
        ],
        'Water Heaters' => [
            ['service' => 'water heater repair', 'keyword' => 'water heater repair'],
            ['service' => 'water heater replacement', 'keyword' => 'water heater replacement'],
            ['service' => 'tankless water heater installation', 'keyword' => 'tankless water heater'],
        ],
        'Leaks' => [
            ['service' => 'leak detection', 'keyword' => 'water leak'],
            ['service' => 'slab leak repair', 'keyword' => 'slab leak'],
            ['service' => 'toilet repair', 'keyword' => 'running toilet'],
        ],
        'Sewer & Pipe' => [
            ['service' => 'sewer camera inspection', 'keyword' => 'sewer camera'],
            ['service' => 'trenchless sewer repair', 'keyword' => 'trenchless sewer'],
            ['service' => 'water main repair', 'keyword' => 'water main break'],
        ],
        'Kitchen' => [
            ['service' => 'garbage disposal repair', 'keyword' => 'garbage disposal'],
            ['service' => 'faucet repair', 'keyword' => 'kitchen faucet leak'],
            ['service' => 'gas line services', 'keyword' => 'gas line repair'],
        ],
        'Bathroom' => [
            ['service' => 'toilet repair', 'keyword' => 'toilet repair'],
            ['service' => 'drain cleaning', 'keyword' => 'shower drain clog'],
            ['service' => 'plumbing installation', 'keyword' => 'bathroom plumbing'],
        ],
        'Maintenance' => [
            ['service' => 'plumbing maintenance', 'keyword' => 'plumbing maintenance'],
            ['service' => 'sump pump repair', 'keyword' => 'sump pump'],
            ['service' => 'plumbing inspection', 'keyword' => 'plumbing inspection'],
        ],
        'Service Areas' => [
            ['service' => 'plumbing services', 'keyword' => 'plumber'],
        ],
    ];

    private $titlePatterns = [
        '{keyword} in {city} UT: Homeowner Guide from Bells Plumbing',
        'How to Handle {keyword} in {city}, Utah',
        '{city} {keyword}: Signs, Costs, and When to Call a Pro',
        '{keyword} Near {city} UT — Same-Day Plumbing Help',
        'What {city} Homeowners Should Know About {keyword}',
        '{keyword} in {city}: Common Causes and Professional Fixes',
        'Is Your {city} Home Having {keyword} Issues? Read This First',
        '{city} Utah {keyword} — Expert Tips from a Local Plumber',
    ];

    public function __construct(array $cfg)
    {
        $this->cfg = $cfg;
    }

    public function generateBatch(array $existingTopics, string $startDate, int $count): array
    {
        $existingSlugs = [];
        foreach ($existingTopics as $t) {
            $existingSlugs[$t['slug']] = true;
        }

        $new = [];
        $date = new DateTimeImmutable($startDate);
        $attempts = 0;
        $maxAttempts = $count * 40;

        while (count($new) < $count && $attempts < $maxAttempts) {
            $attempts++;
            $topic = $this->randomTopic();
            if (isset($existingSlugs[$topic['slug']])) {
                continue;
            }
            $existingSlugs[$topic['slug']] = true;
            $topic['publish_date'] = $date->format('Y-m-d');
            $new[] = $topic;
            $date = $date->modify('+1 day');
        }

        return $new;
    }

    private function randomTopic(): array
    {
        $category = array_rand($this->categories);
        $items = $this->categories[$category];
        $item = $items[array_rand($items)];
        $city = $this->cities[array_rand($this->cities)];
        $pattern = $this->titlePatterns[array_rand($this->titlePatterns)];

        $keyword = $item['keyword'] . ' ' . $city;
        if ($category === 'Service Areas') {
            $keyword = 'plumber ' . $city . ' UT';
            $title = "Plumber in {$city} UT: Local Service, Pricing, and Same-Day Help";
        } else {
            $title = str_replace(
                ['{keyword}', '{city}'],
                [$item['keyword'], $city],
                $pattern
            );
        }

        $slug = $this->slugify($title);
        if (strlen($slug) > 80) {
            $slug = substr($slug, 0, 80);
            $slug = rtrim($slug, '-');
        }

        return [
            'title' => $title,
            'slug' => $slug,
            'category' => $category,
            'city' => $city,
            'service' => $item['service'],
            'keyword' => $keyword,
            'generated' => true,
        ];
    }

    private function slugify(string $text): string
    {
        $text = strtolower($text);
        $text = preg_replace('/[^a-z0-9]+/', '-', $text);
        return trim($text, '-');
    }
}
