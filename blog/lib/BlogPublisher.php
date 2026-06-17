<?php

class BlogPublisher
{
    private $root;
    private $cfg;

    public function __construct(?string $root = null)
    {
        $this->root = $root ?: dirname(dirname(__DIR__));
        $this->cfg = require $this->root . '/blog/config.php';
        date_default_timezone_set($this->cfg['timezone'] ?? 'America/Denver');
    }

    public function build(?string $asOf = null, bool $publishAll = false): array
    {
        $asOf = $asOf ?: date('Y-m-d');
        $topics = $this->loadTopics();
        $schedule = $this->loadSchedule();
        $publishedSlugs = $schedule['published_slugs'] ?? [];
        $slugSet = array_flip($publishedSlugs);
        $newlyPublished = [];
        $publishedTopics = [];

        foreach ($topics as $topic) {
            $shouldPublish = $publishAll || ($topic['publish_date'] <= $asOf);
            if (!$shouldPublish) {
                continue;
            }

            $out = $this->root . '/blog/' . $topic['slug'] . '.html';
            file_put_contents($out, $this->renderPost($topic));
            $publishedTopics[] = $topic;

            if (!isset($slugSet[$topic['slug']])) {
                $newlyPublished[] = $topic['slug'];
                $publishedSlugs[] = $topic['slug'];
                $slugSet[$topic['slug']] = true;
            }
        }

        sort($publishedSlugs);
        $schedule['published_slugs'] = array_values(array_unique($publishedSlugs));
        $schedule['last_run'] = $asOf;
        $this->saveSchedule($schedule);

        file_put_contents($this->root . '/Blog.html', $this->renderIndex($publishedTopics));
        file_put_contents($this->root . '/sitemap.xml', $this->renderSitemap($publishedTopics));

        return [
            'as_of' => $asOf,
            'total_topics' => count($topics),
            'published_count' => count($publishedTopics),
            'newly_published' => $newlyPublished,
        ];
    }

    private function loadTopics(): array
    {
        $path = $this->root . '/blog/posts.json';
        if (!is_readable($path)) {
            throw new RuntimeException('Missing blog/posts.json');
        }
        $data = json_decode(file_get_contents($path), true);
        if (!is_array($data)) {
            throw new RuntimeException('Invalid blog/posts.json');
        }
        return $data;
    }

    private function loadSchedule(): array
    {
        $path = $this->root . '/blog/schedule.json';
        if (!is_readable($path)) {
            return ['published_slugs' => []];
        }
        $data = json_decode(file_get_contents($path), true);
        return is_array($data) ? $data : ['published_slugs' => []];
    }

    private function saveSchedule(array $schedule): void
    {
        file_put_contents(
            $this->root . '/blog/schedule.json',
            json_encode($schedule, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . "\n"
        );
    }

    private function e(string $s): string
    {
        return htmlspecialchars($s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
    }

    private function metaDescription(array $topic): string
    {
        $desc = sprintf(
            '%s. Licensed Utah plumber serving %s and %s. Same-day %s. Call %s for a free estimate.',
            substr($topic['title'], 0, 120),
            $topic['city'],
            $this->cfg['counties'],
            $topic['service'],
            $this->cfg['phone']
        );
        return substr($desc, 0, 160);
    }

    private function serviceTitle(string $service): string
    {
        return ucwords($service);
    }

    private function listItems(array $items): string
    {
        $html = '';
        foreach ($items as $item) {
            $html .= '<li>' . $this->e($item) . '</li>';
        }
        return $html;
    }

    private function articleBody(array $topic): array
    {
        $city = $topic['city'];
        $service = $topic['service'];
        $keyword = $topic['keyword'];
        $category = $topic['category'];
        $counties = $this->cfg['counties'];
        $phone = $this->cfg['phone'];
        $phoneTel = $this->cfg['phone_tel'];

        $signs = [
            'Water stains, damp spots, or unexplained moisture near fixtures',
            "Unusual sounds — gurgling drains, banging pipes, or hissing near {$service} equipment",
            'Slower performance than usual (drains, hot water, or water pressure)',
            'Odors from drains, sewer gas, or musty smells in cabinets and crawl spaces',
            'Higher utility bills without a change in household usage',
        ];

        $causes = [
            'Age and wear on pipes, fittings, and appliances common in Utah homes built before 2000',
            "Hard water mineral buildup throughout {$counties}",
            'Temperature swings that stress pipes — especially in uninsulated crawl spaces and garages',
            "Improper prior repairs or DIY fixes that didn't meet Utah plumbing code",
            "Tree roots, ground shifting, or settling that affects underground lines in {$city} neighborhoods",
        ];

        $diySafe = [
            'Check that shut-off valves are fully open and accessible',
            'Remove visible debris from drain stoppers and P-traps (with a bucket ready)',
            'Reset tripped breakers or GFCI outlets tied to disposals and pumps',
            'Note when the problem started and which fixtures are affected — this helps us diagnose faster',
        ];

        $callPro = [
            'Active leaking, flooding, or sewage backing up into the home',
            'No hot water, no water pressure, or gas smells near water heaters or stoves',
            'Repeated clogs in the same drain after DIY attempts',
            'Any work involving gas lines, main water lines, or sewer lines',
            "You need a written flat-rate price before work begins — that's how Bells Plumbing operates",
        ];

        $faqs = [
            [
                "How fast can Bells Plumbing respond in {$city}?",
                "We offer same-day service across {$counties}, including {$city}. For emergencies — burst pipes, sewer backups, no hot water — call {$phone} and we'll dispatch a licensed plumber as quickly as possible, often within a few hours.",
            ],
            [
                'Do you charge trip fees or after-hours surcharges?',
                "Bells Plumbing provides upfront flat pricing before any work starts. We don't hit you with surprise trip fees. You'll know the cost before we pick up a wrench.",
            ],
            [
                'Are you licensed and insured in Utah?',
                "Yes. Bells Plumbing is licensed and insured in Utah (License #111076325501). Every technician on your job is qualified to work on {$service} in residential and commercial properties.",
            ],
            [
                "What areas do you serve besides {$city}?",
                "We cover {$counties} — from Brigham City and Ogden through Layton, Clearfield, Bountiful, and northern Salt Lake County. If you're nearby, call and we'll confirm same-day availability.",
            ],
            [
                "Should I attempt a DIY fix for {$keyword} issues?",
                "Minor maintenance is fine, but {$service} problems often hide bigger issues — especially with Utah's hard water and older pipe materials. A quick professional diagnosis can prevent thousands in water damage. When in doubt, call {$phone} for a free phone estimate.",
            ],
        ];

        $isLocal = $category === 'Service Areas';
        if ($isLocal) {
            $intro = "Looking for a reliable <strong>{$this->e($keyword)}</strong>? Bells Plumbing has served <strong>{$this->e($city)}</strong> and surrounding communities for over 17 years. We specialize in {$this->e($service)}, sewer repair, hydro jetting, water heaters, and emergency calls — with same-day availability and upfront flat pricing.";
        } else {
            $intro = "If you're searching for <strong>{$this->e($keyword)}</strong>, you're not alone. Homeowners in <strong>{$this->e($city)}</strong> and across {$this->e($counties)} deal with {$this->e($service)} issues year-round — from hard-water wear to freeze-thaw pipe stress. This guide explains what to watch for, what you can safely check yourself, and when to call a licensed plumber.";
        }

        $sections = [
            ['type' => 'intro', 'html' => "<p>{$intro}</p>"],
            [
                'type' => 'h2',
                'text' => 'Signs You Need ' . $this->serviceTitle($service) . ' Help',
                'html' => '<ul>' . $this->listItems($signs) . '</ul>',
            ],
            [
                'type' => 'h2',
                'text' => "Common Causes in {$city} and Northern Utah",
                'html' => '<ul>' . $this->listItems($causes) . '</ul>',
            ],
            [
                'type' => 'h2',
                'text' => 'What You Can Check Before Calling',
                'html' => '<p>These steps are safe for most homeowners and can save time when our technician arrives:</p><ul>'
                    . $this->listItems($diySafe) . '</ul>',
            ],
            [
                'type' => 'h2',
                'text' => 'When to Call a Licensed Plumber Immediately',
                'html' => '<ul>' . $this->listItems($callPro) . '</ul>',
            ],
            [
                'type' => 'h2',
                'text' => 'How Bells Plumbing Handles ' . $this->serviceTitle($service) . " in {$city}",
                'html' => <<<HTML
<p>When you call <a href="tel:{$phoneTel}">{$this->e($phone)}</a>, here's what happens:</p>
<ol>
<li><strong>Phone diagnosis</strong> — we ask targeted questions to understand urgency and scope.</li>
<li><strong>Same-day dispatch</strong> — a licensed plumber arrives in a marked van with common parts on board.</li>
<li><strong>Flat-rate quote</strong> — you approve the price in writing before work begins. No surprises.</li>
<li><strong>Fix it right</strong> — we repair or replace using quality parts backed by our workmanship guarantee.</li>
<li><strong>Clean up</strong> — we leave the work area cleaner than we found it. Every time.</li>
</ol>
<p>Whether you're in {$this->e($city)}, Layton, Ogden, Bountiful, or anywhere in our service area, you get the same honest service and upfront pricing.</p>
HTML,
            ],
        ];

        if ($isLocal) {
            $sections[] = [
                'type' => 'h2',
                'text' => "Services We Provide in {$city}",
                'html' => <<<HTML
<ul>
<li>Emergency plumbing — burst pipes, flooding, no water</li>
<li>Drain cleaning and hydro jetting</li>
<li>Sewer backup repair and camera inspection</li>
<li>Water heater repair, replacement, and tankless installation</li>
<li>Leak detection, slab leaks, and pipe repair</li>
<li>Toilet, faucet, garbage disposal, and fixture repair</li>
<li>Gas line and water main services</li>
</ul>
<p>We're locally owned, not a franchise call center. When you call {$this->e($phone)}, you talk to real people who know {$this->e($city)}.</p>
HTML,
            ];
        }

        $faqHtml = '';
        foreach ($faqs as $faq) {
            $q = $faq[0];
            $a = $faq[1];
            $faqHtml .= '<details class="blog-faq"><summary>' . $this->e($q) . '</summary><p>' . $a . '</p></details>';
        }
        $sections[] = ['type' => 'h2', 'text' => 'Frequently Asked Questions', 'html' => $faqHtml];

        return $sections;
    }

    private function navHtml(string $active = '', int $depth = 0): string
    {
        $prefix = str_repeat('../', $depth);
        $links = [
            ['Home', "{$prefix}index.html", 'home'],
            ['Services', "{$prefix}index.html#services", 'services'],
            ['About', "{$prefix}index.html#about", 'about'],
            ['Blog', "{$prefix}Blog.html", 'blog'],
            ['Service Areas', "{$prefix}index.html#areas", 'areas'],
            ['Contact', "{$prefix}index.html#contact", 'contact'],
        ];
        $out = '';
        foreach ($links as $link) {
            $label = $link[0];
            $href = $link[1];
            $key = $link[2];
            $cls = $key === $active
                ? 'text-[#F5A623] bg-[#FFF3D6]'
                : 'text-[#0B1D3A] hover:text-[#F5A623]';
            $out .= '<a class="px-3 py-2 text-sm font-medium ' . $cls . ' transition-colors rounded-lg hover:bg-[#FFF3D6]" href="' . $href . '">' . $label . '</a>';
        }
        return $out;
    }

    private function headBlock(string $title, string $description, string $canonical, int $depth = 0): string
    {
        $prefix = str_repeat('../', $depth);
        $t = $this->e($title);
        $d = $this->e($description);
        return <<<HTML
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-3WMTW984F0"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-3WMTW984F0');
</script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{$t} | Bells Plumbing Utah</title>
<meta name="description" content="{$d}">
<link rel="canonical" href="{$canonical}">
<meta property="og:title" content="{$t}">
<meta property="og:description" content="{$d}">
<meta property="og:url" content="{$canonical}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Bells Plumbing Utah">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{$prefix}css/main.css">
<link rel="stylesheet" href="{$prefix}css/shell.css">
<link rel="stylesheet" href="{$prefix}css/blog.css">
<link rel="icon" type="image/png" href="{$prefix}images/bells-logo.png">
HTML;
    }

    private function headerBlock(string $active = '', int $depth = 0): string
    {
        $prefix = str_repeat('../', $depth);
        $phone = $this->e($this->cfg['phone']);
        $phoneTel = $this->cfg['phone_tel'];
        $nav = $this->navHtml($active, $depth);
        return <<<HTML
<div class="bg-[#0B1D3A] text-white text-sm py-2 hidden md:block">
  <div class="max-w-6xl mx-auto px-4 flex justify-between items-center">
    <span class="opacity-80">Bells Plumbing · Expert Plumbing Services · Mon–Sat 7am–7pm</span>
    <a href="tel:{$phoneTel}" class="flex items-center gap-1.5 font-semibold hover:text-[#F5A623] transition-colors">📞 {$phone}</a>
  </div>
</div>
<header class="sticky top-0 z-50 bg-white transition-shadow duration-300 shadow-sm">
  <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
    <a class="flex items-center gap-3" href="{$prefix}index.html">
      <div class="h-14 w-14 flex items-center justify-center">
        <img src="{$prefix}images/bells-logo.png" alt="Bells Plumbing Logo" class="w-full h-full object-contain">
      </div>
      <div class="hidden sm:block">
        <span class="font-bold text-[#0B1D3A] text-lg leading-none">Bells Plumbing</span>
        <span class="block text-[11px] text-gray-500 font-medium tracking-wide uppercase mt-0.5">Expert Plumbing Services</span>
      </div>
    </a>
    <nav class="hidden lg:flex items-center gap-1">{$nav}</nav>
    <div class="flex items-center gap-2">
      <a href="tel:{$phoneTel}" class="inline-flex items-center justify-center gap-2 shadow h-8 rounded-md px-3 bg-[#F5A623] hover:bg-[#D4891A] text-black font-bold text-sm">📞 {$phone}</a>
    </div>
  </div>
</header>
HTML;
    }

    private function footerBlock(int $depth = 0): string
    {
        $prefix = str_repeat('../', $depth);
        $phone = $this->e($this->cfg['phone']);
        $phoneTel = $this->cfg['phone_tel'];
        $counties = $this->e($this->cfg['counties']);
        return <<<HTML
<footer class="bg-[#0B1D3A] text-slate-300">
  <div class="max-w-6xl mx-auto px-4 py-12">
    <div class="grid md:grid-cols-3 gap-10 mb-8">
      <div>
        <img src="{$prefix}images/bells-logo.png" alt="Bells Plumbing" style="height:64px;width:auto;background:#fff;padding:8px;border-radius:12px;" loading="lazy">
        <p class="text-sm text-slate-400 mt-4">Licensed &amp; insured. Serving {$counties}.</p>
        <a href="tel:{$phoneTel}" class="text-[#F5A623] font-bold text-lg mt-2 inline-block">{$phone}</a>
      </div>
      <div>
        <h4 class="text-white font-semibold mb-3">Quick Links</h4>
        <ul class="space-y-2 text-sm">
          <li><a href="{$prefix}index.html" class="hover:text-[#F5A623]">Home</a></li>
          <li><a href="{$prefix}Blog.html" class="hover:text-[#F5A623]">Blog</a></li>
          <li><a href="{$prefix}index.html#services" class="hover:text-[#F5A623]">Services</a></li>
          <li><a href="{$prefix}index.html#contact" class="hover:text-[#F5A623]">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4 class="text-white font-semibold mb-3">Top Services</h4>
        <ul class="space-y-2 text-sm text-slate-400">
          <li>Emergency Plumbing</li>
          <li>Drain Cleaning &amp; Hydro Jetting</li>
          <li>Water Heater Repair &amp; Replacement</li>
          <li>Sewer Backup &amp; Camera Inspection</li>
        </ul>
      </div>
    </div>
    <p class="text-xs text-slate-500 text-center border-t border-white/10 pt-4">© 2026 Bells Plumbing. License #111076325501</p>
  </div>
</footer>
<div class="fixed bottom-0 left-0 right-0 md:hidden z-50">
  <a href="tel:{$phoneTel}" class="flex items-center justify-center gap-2 bg-[#F5A623] text-[#0B1D3A] font-extrabold text-lg w-full py-4">📞 Call {$phone}</a>
</div>
HTML;
    }

    private function ctaBlock(): string
    {
        $phone = $this->e($this->cfg['phone']);
        $phoneTel = $this->cfg['phone_tel'];
        return <<<HTML
<div class="blog-cta">
  <h2>Need a Plumber in Utah Today?</h2>
  <p>Same-day service · Upfront flat pricing · Licensed &amp; insured</p>
  <a href="tel:{$phoneTel}" class="blog-cta-btn">Call {$phone}</a>
  <p class="blog-cta-note"><a href="../index.html#contact">Or send us a message</a> · Mon–Sat 7am–7pm</p>
</div>
HTML;
    }

    private function schemaArticle(array $topic, string $description): string
    {
        $data = [
            '@context' => 'https://schema.org',
            '@type' => 'Article',
            'headline' => $topic['title'],
            'description' => $description,
            'datePublished' => $topic['publish_date'],
            'author' => ['@type' => 'Organization', 'name' => 'Bells Plumbing Utah'],
            'publisher' => [
                '@type' => 'Organization',
                'name' => 'Bells Plumbing Utah',
                'logo' => ['@type' => 'ImageObject', 'url' => $this->cfg['site'] . '/images/bells-logo.png'],
            ],
            'mainEntityOfPage' => $this->cfg['site'] . '/blog/' . $topic['slug'] . '.html',
        ];
        return '<script type="application/ld+json">' . json_encode($data, JSON_UNESCAPED_SLASHES) . '</script>';
    }

    private function renderPost(array $topic): string
    {
        $desc = $this->metaDescription($topic);
        $canonical = $this->cfg['site'] . '/blog/' . $topic['slug'] . '.html';
        $bodyHtml = '';
        foreach ($this->articleBody($topic) as $sec) {
            if ($sec['type'] === 'intro') {
                $bodyHtml .= $sec['html'];
            } elseif ($sec['type'] === 'h2') {
                $bodyHtml .= '<h2>' . $this->e($sec['text']) . '</h2>' . $sec['html'];
            }
        }
        $pubDisplay = date('F j, Y', strtotime($topic['publish_date'] . ' 12:00:00'));
        $head = $this->headBlock($topic['title'], $desc, $canonical, 1);
        $schema = $this->schemaArticle($topic, $desc);
        $header = $this->headerBlock('blog', 1);
        $footer = $this->footerBlock(1);
        $cta = $this->ctaBlock();

        return <<<HTML
<!DOCTYPE html>
<html lang="en">
<head>
{$head}
{$schema}
</head>
<body class="font-sans antialiased text-[#1F2933] bg-white">
{$header}
<main>
  <article class="blog-article">
    <div class="blog-hero">
      <p class="blog-cat">{$this->e($topic['category'])}</p>
      <h1>{$this->e($topic['title'])}</h1>
      <p class="blog-meta">Published {$pubDisplay} · {$this->e($topic['city'])}, Utah · <a href="../Blog.html">← All articles</a></p>
    </div>
    <div class="blog-content">
      {$bodyHtml}
      {$cta}
    </div>
  </article>
</main>
{$footer}
</body>
</html>
HTML;
    }

    private function renderIndex(array $published): string
    {
        $desc = sprintf(
            'Utah plumbing tips, local guides, and expert advice from Bells Plumbing. Serving %s. Call %s.',
            $this->cfg['counties'],
            $this->cfg['phone']
        );
        $canonical = $this->cfg['site'] . '/Blog.html';

        usort($published, function ($a, $b) {
            return strcmp($b['publish_date'], $a['publish_date']);
        });

        if ($published) {
            $cards = '';
            foreach ($published as $p) {
                $d = date('M j, Y', strtotime($p['publish_date'] . ' 12:00:00'));
                $excerpt = $this->e(substr($this->metaDescription($p), 0, 140)) . '…';
                $cards .= <<<HTML
<article class="blog-card" data-category="{$this->e($p['category'])}">
  <p class="blog-card-cat">{$this->e($p['category'])}</p>
  <h2><a href="blog/{$this->e($p['slug'])}.html">{$this->e($p['title'])}</a></h2>
  <p class="blog-card-excerpt">{$excerpt}</p>
  <div class="blog-card-foot"><span>{$d}</span><a href="blog/{$this->e($p['slug'])}.html">Read article →</a></div>
</article>

HTML;
            }
            $grid = $cards;
        } else {
            $grid = '<p class="blog-empty">New articles publish daily. Check back soon!</p>';
        }

        $categories = array_unique(array_column($published, 'category'));
        sort($categories);
        $filters = '<button class="blog-filter active" data-filter="all">All Topics</button>';
        foreach ($categories as $c) {
            $filters .= '<button class="blog-filter" data-filter="' . $this->e($c) . '">' . $this->e($c) . '</button>';
        }

        $phone = $this->e($this->cfg['phone']);
        $phoneTel = $this->cfg['phone_tel'];
        $head = $this->headBlock('Utah Plumbing Blog & Local Guides', $desc, $canonical);
        $header = $this->headerBlock('blog');
        $footer = $this->footerBlock();

        return <<<HTML
<!DOCTYPE html>
<html lang="en">
<head>
{$head}
</head>
<body class="font-sans antialiased text-[#1F2933] bg-white">
{$header}
<main>
  <section class="blog-index-hero">
    <p class="blog-hero-eyebrow">Plumbing Tips &amp; Local Guides</p>
    <h1>Utah Plumbing Help Center</h1>
    <p>Practical guides for homeowners in Bountiful, Layton, Ogden, and across the Wasatch Front.</p>
    <a href="tel:{$phoneTel}" class="blog-hero-cta">Need a plumber now? {$phone}</a>
  </section>
  <div class="blog-filters">{$filters}</div>
  <div class="blog-grid" id="blog-grid">
{$grid}
  </div>
  <section class="blog-index-cta">
    <h2>Can't find what you need?</h2>
    <p>Call for a free phone estimate — same-day service available.</p>
    <a href="tel:{$phoneTel}" class="blog-cta-btn">Call {$phone}</a>
  </section>
</main>
{$footer}
<script>
(function(){
  var btns=document.querySelectorAll('.blog-filter');
  var cards=document.querySelectorAll('.blog-card');
  btns.forEach(function(btn){
    btn.addEventListener('click',function(){
      btns.forEach(function(b){b.classList.remove('active');});
      btn.classList.add('active');
      var f=btn.getAttribute('data-filter');
      cards.forEach(function(card){
        card.style.display=(f==='all'||card.getAttribute('data-category')===f)?'':'none';
      });
    });
  });
})();
</script>
</body>
</html>
HTML;
    }

    private function renderSitemap(array $published): string
    {
        $site = $this->cfg['site'];
        $urls = [
            "  <url><loc>{$site}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>",
            "  <url><loc>{$site}/Blog.html</loc><changefreq>daily</changefreq><priority>0.9</priority></url>",
        ];
        foreach ($published as $p) {
            $urls[] = "  <url><loc>{$site}/blog/{$p['slug']}.html</loc><lastmod>{$p['publish_date']}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>";
        }
        return "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
            . "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
            . implode("\n", $urls) . "\n</urlset>\n";
    }
}
