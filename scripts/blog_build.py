#!/usr/bin/env python3
"""Build Bells Plumbing blog pages from topic data. Run daily to publish scheduled posts."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
BLOG_DIR = ROOT / "blog"
POSTS_JSON = ROOT / "blog" / "posts.json"
SCHEDULE_JSON = ROOT / "blog" / "schedule.json"

from blog_topics import COUNTIES, PHONE, PHONE_TEL, SITE, topics_with_dates  # noqa: E402


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def meta_description(topic: dict) -> str:
    city = topic["city"]
    service = topic["service"]
    return (
        f"{topic['title'][:120]}. Licensed Utah plumber serving {city} and {COUNTIES}. "
        f"Same-day {service}. Call {PHONE} for a free estimate."
    )[:160]


def article_body(topic: dict) -> list[dict]:
    city = topic["city"]
    service = topic["service"]
    keyword = topic["keyword"]
    category = topic["category"]

    signs = [
        f"Water stains, damp spots, or unexplained moisture near fixtures",
        f"Unusual sounds — gurgling drains, banging pipes, or hissing near {service} equipment",
        f"Slower performance than usual (drains, hot water, or water pressure)",
        f"Odors from drains, sewer gas, or musty smells in cabinets and crawl spaces",
        f"Higher utility bills without a change in household usage",
    ]

    causes = [
        f"Age and wear on pipes, fittings, and appliances common in Utah homes built before 2000",
        f"Hard water mineral buildup throughout {COUNTIES}",
        f"Temperature swings that stress pipes — especially in uninsulated crawl spaces and garages",
        f"Improper prior repairs or DIY fixes that didn't meet Utah plumbing code",
        f"Tree roots, ground shifting, or settling that affects underground lines in {city} neighborhoods",
    ]

    diy_safe = [
        "Check that shut-off valves are fully open and accessible",
        "Remove visible debris from drain stoppers and P-traps (with a bucket ready)",
        "Reset tripped breakers or GFCI outlets tied to disposals and pumps",
        "Note when the problem started and which fixtures are affected — this helps us diagnose faster",
    ]

    call_pro = [
        f"Active leaking, flooding, or sewage backing up into the home",
        f"No hot water, no water pressure, or gas smells near water heaters or stoves",
        f"Repeated clogs in the same drain after DIY attempts",
        f"Any work involving gas lines, main water lines, or sewer lines",
        f"You need a written flat-rate price before work begins — that's how Bells Plumbing operates",
    ]

    faqs = [
        (
            f"How fast can Bells Plumbing respond in {city}?",
            f"We offer same-day service across {COUNTIES}, including {city}. "
            f"For emergencies — burst pipes, sewer backups, no hot water — call {PHONE} "
            f"and we'll dispatch a licensed plumber as quickly as possible, often within a few hours.",
        ),
        (
            f"Do you charge trip fees or after-hours surcharges?",
            f"Bells Plumbing provides upfront flat pricing before any work starts. "
            f"We don't hit you with surprise trip fees. You'll know the cost before we pick up a wrench.",
        ),
        (
            f"Are you licensed and insured in Utah?",
            f"Yes. Bells Plumbing is licensed and insured in Utah (License #111076325501). "
            f"Every technician on your job is qualified to work on {service} in residential and commercial properties.",
        ),
        (
            f"What areas do you serve besides {city}?",
            f"We cover {COUNTIES} — from Brigham City and Ogden through Layton, Clearfield, "
            f"Bountiful, and northern Salt Lake County. If you're nearby, call and we'll confirm same-day availability.",
        ),
        (
            f"Should I attempt a DIY fix for {keyword} issues?",
            f"Minor maintenance is fine, but {service} problems often hide bigger issues — especially "
            f"with Utah's hard water and older pipe materials. A quick professional diagnosis can prevent "
            f"thousands in water damage. When in doubt, call {PHONE} for a free phone estimate.",
        ),
    ]

    is_local = category == "Service Areas"
    intro = (
        f"If you're searching for <strong>{keyword}</strong>, you're not alone. Homeowners in "
        f"<strong>{city}</strong> and across {COUNTIES} deal with {service} issues year-round — "
        f"from hard-water wear to freeze-thaw pipe stress. This guide explains what to watch for, "
        f"what you can safely check yourself, and when to call a licensed plumber."
    )
    if is_local:
        intro = (
            f"Looking for a reliable <strong>{keyword}</strong>? Bells Plumbing has served "
            f"<strong>{city}</strong> and surrounding communities for over 17 years. "
            f"We specialize in {service}, sewer repair, hydro jetting, water heaters, and emergency calls — "
            f"with same-day availability and upfront flat pricing."
        )

    sections = [
        {"type": "intro", "html": f"<p>{intro}</p>"},
        {
            "type": "h2",
            "text": f"Signs You Need {service.title()} Help",
            "html": "<ul>"
            + "".join(f"<li>{escape(s)}</li>" for s in signs)
            + "</ul>",
        },
        {
            "type": "h2",
            "text": f"Common Causes in {city} and Northern Utah",
            "html": "<ul>"
            + "".join(f"<li>{escape(c)}</li>" for c in causes)
            + "</ul>",
        },
        {
            "type": "h2",
            "text": "What You Can Check Before Calling",
            "html": (
                "<p>These steps are safe for most homeowners and can save time when our technician arrives:</p><ul>"
                + "".join(f"<li>{escape(d)}</li>" for d in diy_safe)
                + "</ul>"
            ),
        },
        {
            "type": "h2",
            "text": "When to Call a Licensed Plumber Immediately",
            "html": "<ul>"
            + "".join(f"<li>{escape(c)}</li>" for c in call_pro)
            + "</ul>",
        },
        {
            "type": "h2",
            "text": f"How Bells Plumbing Handles {service.title()} in {city}",
            "html": (
                f"<p>When you call <a href=\"tel:{PHONE_TEL}\">{PHONE}</a>, here's what happens:</p>"
                "<ol>"
                "<li><strong>Phone diagnosis</strong> — we ask targeted questions to understand urgency and scope.</li>"
                "<li><strong>Same-day dispatch</strong> — a licensed plumber arrives in a marked van with common parts on board.</li>"
                "<li><strong>Flat-rate quote</strong> — you approve the price in writing before work begins. No surprises.</li>"
                "<li><strong>Fix it right</strong> — we repair or replace using quality parts backed by our workmanship guarantee.</li>"
                "<li><strong>Clean up</strong> — we leave the work area cleaner than we found it. Every time.</li>"
                "</ol>"
                f"<p>Whether you're in {city}, Layton, Ogden, Bountiful, or anywhere in our service area, "
                f"you get the same honest service and upfront pricing.</p>"
            ),
        },
    ]

    if is_local:
        sections.append(
            {
                "type": "h2",
                "text": f"Services We Provide in {city}",
                "html": (
                    "<ul>"
                    "<li>Emergency plumbing — burst pipes, flooding, no water</li>"
                    "<li>Drain cleaning and hydro jetting</li>"
                    "<li>Sewer backup repair and camera inspection</li>"
                    "<li>Water heater repair, replacement, and tankless installation</li>"
                    "<li>Leak detection, slab leaks, and pipe repair</li>"
                    "<li>Toilet, faucet, garbage disposal, and fixture repair</li>"
                    "<li>Gas line and water main services</li>"
                    "</ul>"
                    f"<p>We're locally owned, not a franchise call center. When you call {PHONE}, "
                    f"you talk to real people who know {city}.</p>"
                ),
            }
        )

    sections.append(
        {
            "type": "h2",
            "text": "Frequently Asked Questions",
            "html": "".join(
                f"<details class=\"blog-faq\"><summary>{escape(q)}</summary><p>{a}</p></details>"
                for q, a in faqs
            ),
        }
    )

    return sections


def nav_html(active: str = "", depth: int = 0) -> str:
    prefix = "../" * depth
    links = [
        ("Home", f"{prefix}index.html", "home"),
        ("Services", f"{prefix}index.html#services", "services"),
        ("About", f"{prefix}index.html#about", "about"),
        ("Blog", f"{prefix}Blog.html", "blog"),
        ("Service Areas", f"{prefix}index.html#areas", "areas"),
        ("Contact", f"{prefix}index.html#contact", "contact"),
    ]
    parts = []
    for label, href, key in links:
        cls = "text-[#F5A623] bg-[#FFF3D6]" if key == active else "text-[#0B1D3A] hover:text-[#F5A623]"
        parts.append(
            f'<a class="px-3 py-2 text-sm font-medium {cls} transition-colors rounded-lg hover:bg-[#FFF3D6]" href="{href}">{label}</a>'
        )
    return "".join(parts)


def head_block(title: str, description: str, canonical: str, depth: int = 0) -> str:
    prefix = "../" * depth
    return f"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-3WMTW984F0"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-3WMTW984F0');
</script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)} | Bells Plumbing Utah</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Bells Plumbing Utah">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{prefix}css/main.css">
<link rel="stylesheet" href="{prefix}css/shell.css">
<link rel="stylesheet" href="{prefix}css/blog.css">
<link rel="icon" type="image/png" href="{prefix}images/bells-logo.png">"""


def header_block(active: str = "", depth: int = 0) -> str:
    prefix = "../" * depth
    return f"""<div class="bg-[#0B1D3A] text-white text-sm py-2 hidden md:block">
  <div class="max-w-6xl mx-auto px-4 flex justify-between items-center">
    <span class="opacity-80">Bells Plumbing · Expert Plumbing Services · Mon–Sat 7am–7pm</span>
    <a href="tel:{PHONE_TEL}" class="flex items-center gap-1.5 font-semibold hover:text-[#F5A623] transition-colors">📞 {PHONE}</a>
  </div>
</div>
<header class="sticky top-0 z-50 bg-white transition-shadow duration-300 shadow-sm">
  <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
    <a class="flex items-center gap-3" href="{prefix}index.html">
      <div class="h-14 w-14 flex items-center justify-center">
        <img src="{prefix}images/bells-logo.png" alt="Bells Plumbing Logo" class="w-full h-full object-contain">
      </div>
      <div class="hidden sm:block">
        <span class="font-bold text-[#0B1D3A] text-lg leading-none">Bells Plumbing</span>
        <span class="block text-[11px] text-gray-500 font-medium tracking-wide uppercase mt-0.5">Expert Plumbing Services</span>
      </div>
    </a>
    <nav class="hidden lg:flex items-center gap-1">{nav_html(active, depth)}</nav>
    <div class="flex items-center gap-2">
      <a href="tel:{PHONE_TEL}" class="inline-flex items-center justify-center gap-2 shadow h-8 rounded-md px-3 bg-[#F5A623] hover:bg-[#D4891A] text-black font-bold text-sm">📞 {PHONE}</a>
    </div>
  </div>
</header>"""


def footer_block(depth: int = 0) -> str:
    prefix = "../" * depth
    return f"""<footer class="bg-[#0B1D3A] text-slate-300">
  <div class="max-w-6xl mx-auto px-4 py-12">
    <div class="grid md:grid-cols-3 gap-10 mb-8">
      <div>
        <img src="{prefix}images/bells-logo.png" alt="Bells Plumbing" style="height:64px;width:auto;background:#fff;padding:8px;border-radius:12px;" loading="lazy">
        <p class="text-sm text-slate-400 mt-4">Licensed &amp; insured. Serving {COUNTIES}.</p>
        <a href="tel:{PHONE_TEL}" class="text-[#F5A623] font-bold text-lg mt-2 inline-block">{PHONE}</a>
      </div>
      <div>
        <h4 class="text-white font-semibold mb-3">Quick Links</h4>
        <ul class="space-y-2 text-sm">
          <li><a href="{prefix}index.html" class="hover:text-[#F5A623]">Home</a></li>
          <li><a href="{prefix}Blog.html" class="hover:text-[#F5A623]">Blog</a></li>
          <li><a href="{prefix}index.html#services" class="hover:text-[#F5A623]">Services</a></li>
          <li><a href="{prefix}index.html#contact" class="hover:text-[#F5A623]">Contact</a></li>
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
  <a href="tel:{PHONE_TEL}" class="flex items-center justify-center gap-2 bg-[#F5A623] text-[#0B1D3A] font-extrabold text-lg w-full py-4">📞 Call {PHONE}</a>
</div>"""


def cta_block() -> str:
    return f"""<div class="blog-cta">
  <h2>Need a Plumber in Utah Today?</h2>
  <p>Same-day service · Upfront flat pricing · Licensed &amp; insured</p>
  <a href="tel:{PHONE_TEL}" class="blog-cta-btn">Call {PHONE}</a>
  <p class="blog-cta-note"><a href="../index.html#contact">Or send us a message</a> · Mon–Sat 7am–7pm</p>
</div>"""


def schema_article(topic: dict, description: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": topic["title"],
        "description": description,
        "datePublished": topic["publish_date"],
        "author": {"@type": "Organization", "name": "Bells Plumbing Utah"},
        "publisher": {
            "@type": "Organization",
            "name": "Bells Plumbing Utah",
            "logo": {"@type": "ImageObject", "url": f"{SITE}/images/bells-logo.png"},
        },
        "mainEntityOfPage": f"{SITE}/blog/{topic['slug']}.html",
    }
    return f'<script type="application/ld+json">{json.dumps(data)}</script>'


def render_post(topic: dict) -> str:
    desc = meta_description(topic)
    canonical = f"{SITE}/blog/{topic['slug']}.html"
    sections = article_body(topic)
    body_html = ""
    for sec in sections:
        if sec["type"] == "intro":
            body_html += sec["html"]
        elif sec["type"] == "h2":
            body_html += f"<h2>{escape(sec['text'])}</h2>{sec['html']}"

    pub_display = date.fromisoformat(topic["publish_date"]).strftime("%B %d, %Y")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_block(topic['title'], desc, canonical, depth=1)}
{schema_article(topic, desc)}
</head>
<body class="font-sans antialiased text-[#1F2933] bg-white">
{header_block('blog', depth=1)}
<main>
  <article class="blog-article">
    <div class="blog-hero">
      <p class="blog-cat">{escape(topic['category'])}</p>
      <h1>{escape(topic['title'])}</h1>
      <p class="blog-meta">Published {pub_display} · {escape(topic['city'])}, Utah · <a href="../Blog.html">← All articles</a></p>
    </div>
    <div class="blog-content">
      {body_html}
      {cta_block()}
    </div>
  </article>
</main>
{footer_block(depth=1)}
</body>
</html>"""


def render_index(published: list[dict]) -> str:
    desc = (
        f"Utah plumbing tips, local guides, and expert advice from Bells Plumbing. "
        f"Serving {COUNTIES}. Call {PHONE}."
    )
    canonical = f"{SITE}/Blog.html"

    if published:
        cards = []
        for p in sorted(published, key=lambda x: x["publish_date"], reverse=True):
            d = date.fromisoformat(p["publish_date"]).strftime("%b %d, %Y")
            cards.append(
                f"""<article class="blog-card" data-category="{escape(p['category'])}">
  <p class="blog-card-cat">{escape(p['category'])}</p>
  <h2><a href="blog/{p['slug']}.html">{escape(p['title'])}</a></h2>
  <p class="blog-card-excerpt">{escape(meta_description(p)[:140])}…</p>
  <div class="blog-card-foot"><span>{d}</span><a href="blog/{p['slug']}.html">Read article →</a></div>
</article>"""
            )
        grid = "\n".join(cards)
    else:
        grid = '<p class="blog-empty">New articles publish daily. Check back soon!</p>'

    categories = sorted({p["category"] for p in published})
    filters = ['<button class="blog-filter active" data-filter="all">All Topics</button>']
    for c in categories:
        filters.append(f'<button class="blog-filter" data-filter="{escape(c)}">{escape(c)}</button>')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_block("Utah Plumbing Blog & Local Guides", desc, canonical)}
</head>
<body class="font-sans antialiased text-[#1F2933] bg-white">
{header_block('blog')}
<main>
  <section class="blog-index-hero">
    <p class="blog-hero-eyebrow">Plumbing Tips &amp; Local Guides</p>
    <h1>Utah Plumbing Help Center</h1>
    <p>Practical guides for homeowners in Bountiful, Layton, Ogden, and across the Wasatch Front.</p>
    <a href="tel:{PHONE_TEL}" class="blog-hero-cta">Need a plumber now? {PHONE}</a>
  </section>
  <div class="blog-filters">{''.join(filters)}</div>
  <div class="blog-grid" id="blog-grid">
{grid}
  </div>
  <section class="blog-index-cta">
    <h2>Can't find what you need?</h2>
    <p>Call for a free phone estimate — same-day service available.</p>
    <a href="tel:{PHONE_TEL}" class="blog-cta-btn">Call {PHONE}</a>
  </section>
</main>
{footer_block()}
<script>
(function(){{
  var btns=document.querySelectorAll('.blog-filter');
  var cards=document.querySelectorAll('.blog-card');
  btns.forEach(function(btn){{
    btn.addEventListener('click',function(){{
      btns.forEach(function(b){{b.classList.remove('active');}});
      btn.classList.add('active');
      var f=btn.getAttribute('data-filter');
      cards.forEach(function(card){{
        card.style.display=(f==='all'||card.getAttribute('data-category')===f)?'':'none';
      }});
    }});
  }});
}})();
</script>
</body>
</html>"""


def render_sitemap(published: list[dict]) -> str:
    urls = [
        f"  <url><loc>{SITE}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>",
        f"  <url><loc>{SITE}/Blog.html</loc><changefreq>daily</changefreq><priority>0.9</priority></url>",
    ]
    for p in published:
        urls.append(
            f"  <url><loc>{SITE}/blog/{p['slug']}.html</loc>"
            f"<lastmod>{p['publish_date']}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )


def load_schedule() -> dict:
    if SCHEDULE_JSON.exists():
        return json.loads(SCHEDULE_JSON.read_text())
    return {"published_slugs": []}


def save_schedule(schedule: dict) -> None:
    SCHEDULE_JSON.write_text(json.dumps(schedule, indent=2) + "\n")


def build(as_of: date | None = None, publish_all: bool = False) -> dict:
    as_of = as_of or date.today()
    topics = topics_with_dates()
    POSTS_JSON.parent.mkdir(parents=True, exist_ok=True)
    BLOG_DIR.mkdir(parents=True, exist_ok=True)

    POSTS_JSON.write_text(json.dumps(topics, indent=2) + "\n")

    schedule = load_schedule()
    published_slugs = set(schedule.get("published_slugs", []))

    newly_published = []
    published_topics = []

    for topic in topics:
        pub_date = date.fromisoformat(topic["publish_date"])
        should_publish = publish_all or pub_date <= as_of
        if should_publish:
            out_path = BLOG_DIR / f"{topic['slug']}.html"
            out_path.write_text(render_post(topic))
            published_topics.append(topic)
            if topic["slug"] not in published_slugs:
                newly_published.append(topic["slug"])
                published_slugs.add(topic["slug"])

    schedule["published_slugs"] = sorted(published_slugs)
    schedule["last_run"] = as_of.isoformat()
    save_schedule(schedule)

    (ROOT / "Blog.html").write_text(render_index(published_topics))
    (ROOT / "sitemap.xml").write_text(render_sitemap(published_topics))

    return {
        "as_of": as_of.isoformat(),
        "total_topics": len(topics),
        "published_count": len(published_topics),
        "newly_published": newly_published,
    }


def main() -> int:
    publish_all = "--all" in sys.argv
    as_of = date.today()
    for arg in sys.argv[1:]:
        if arg.startswith("--date="):
            as_of = date.fromisoformat(arg.split("=", 1)[1])

    result = build(as_of=as_of, publish_all=publish_all)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
