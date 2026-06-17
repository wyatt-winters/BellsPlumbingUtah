# Blog Bot — Self-Running Organism on cPanel

The blog bot lives entirely on your server. It **creates** SEO pages, **publishes** one per day, **refills** its topic queue when running low, and **wakes itself** if someone visits the blog and cron was missed.

## What the bot does (every day)

1. **Checks its queue** — if fewer than 30 days of topics remain, it auto-generates 45 new ones
2. **Builds today's article** — full SEO HTML page in `blog/<slug>.html`
3. **Updates the blog index** — regenerates `Blog.html`
4. **Updates sitemap** — `sitemap.xml` for Google
5. **Logs a heartbeat** — `blog/bot-state.json` + `blog/bot.log`

No GitHub. No Python on the server. Pure PHP.

## One-time cPanel setup

### 1. Upload the site

Upload everything to `public_html`, including:

```
blog/bot.php          ← cron hits this
blog/lib/             ← bot brain
blog/posts.json       ← starting queue (57 posts)
blog/config.php       ← settings + secret
Blog.php              ← self-wake when blog is visited
SeoBot.php            ← dashboard (/SeoBot?key=SECRET)
```

### 2. Add ONE cron job

cPanel → **Cron Jobs** → daily (8:00 AM recommended):

```bash
/usr/local/bin/php /home/YOUR_USER/public_html/blog/bot.php
```

**URL alternative:**

```bash
curl -s "https://bellsplumbingutah.com/blog/bot.php?key=YOUR_CRON_SECRET"
```

Default secret (change in `blog/config.php`):  
`bells-blog-change-me-6014c1288aa3fef54142e083f9266af7`

### 3. Activate it once

Open the dashboard:

```
https://bellsplumbingutah.com/SeoBot?key=YOUR_CRON_SECRET
```

Click **Run heartbeat now**. You should see status **ALIVE** and post #1 on `Blog.html`.

## Self-healing

If cron fails, visiting `Blog.html` wakes the bot automatically (if last heartbeat was > 26 hours ago). The organism keeps itself alive.

## Dashboard

**SeoBot** (footer link on your site) shows:

- Alive / status pulse
- Posts live vs queued
- Days of content ahead
- Recent activity log
- Manual run buttons (for testing)

## Files the bot maintains

| File | Purpose |
|------|---------|
| `blog/bot-state.json` | Heartbeat + stats |
| `blog/bot.log` | Activity log |
| `blog/posts.json` | Topic queue (auto-refills) |
| `blog/schedule.json` | What's been published |
| `blog/*.html` | Article pages |
| `Blog.html` | Blog index |
| `sitemap.xml` | SEO sitemap |

## Config (`blog/config.php`)

- `queue_refill_days` — refill when queue drops below this (default 30)
- `queue_batch_size` — new topics per refill (default 45)
- `cron_secret` — change this after upload

## Local dev (Mac only)

Python script still works for preview:

```bash
python3 scripts/blog_build.py
```

On cPanel, only PHP runs.
