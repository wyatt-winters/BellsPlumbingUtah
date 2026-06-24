# Bells Plumbing — Auto-Deploy Guide

**Edit the site → push to GitHub → HostGator updates in ~15 seconds.**

No more manual zip uploads to cPanel File Manager.

---

## How it works (the pipeline)

```
Your Mac (Cursor)  →  GitHub  →  GitHub Actions  →  HostGator (FTPS)  →  Live website
```

1. You (or I) edit files locally in `/Users/paden/Documents/sites/Bells Plumbing`
2. Changes get committed and pushed to the `main` branch on GitHub  
   **Repo:** https://github.com/wyatt-winters/BellsPlumbingUtah
3. GitHub Actions sees the push and runs a workflow called **"Deploy to production"**
4. The workflow uploads only the changed files to your HostGator folder over **FTPS (port 21)**
5. After upload, it wakes the **blog bot** so scheduled posts stay on track
6. The live site updates at **https://bellsplumbingutah.com**

---

## What we connected (one-time setup)

| Piece | What it is |
|-------|------------|
| **GitHub repo** | `wyatt-winters/BellsPlumbingUtah` — source of truth for the site |
| **GitHub Actions workflow** | `.github/workflows/deploy.yml` — runs on every push to `main` |
| **FTP secrets** (stored in GitHub, not in the code) | `FTP_USERNAME`, `FTP_PASSWORD`, `BLOG_BOT_KEY` |
| **Deploy folder** | `/home1/agentors/public_html/website_302faf96/` on HostGator |
| **FTP server** | `192.254.188.195` (HostGator shared IP) |
| **FTP username** | `BellsPlumbing@bellsplumbingutah.com` |

**Important:** Your FTP password lives in GitHub Secrets, not in the repo. Nobody sees it in the code. Rotate it in cPanel if it was ever shared, then update the `FTP_PASSWORD` secret in GitHub.

---

## What triggers a deploy

- **Automatic:** Any `git push` to the `main` branch
- **Manual:** GitHub → Actions → **Deploy to production** → Run workflow

Watch deploys here:  
https://github.com/wyatt-winters/BellsPlumbingUtah/actions

**Green check** = live site updated. **Red X** = something failed (usually FTP credentials or path).

---

## Saddle Up AI billboard (agentadvisers.com)

The SEO billboard site lives in **`billboard/`** in this repo and deploys on its own workflow — it does **not** touch bellsplumbingutah.com.

| Piece | Value |
|-------|-------|
| Folder | `billboard/` |
| Workflow | `.github/workflows/deploy-billboard.yml` |
| FTP user | `saddleupbillboard@bellsplumbingutah.com` |
| Document root | `website_f9f5f795` → **agentadvisers.com** |

See `billboard/BILLBOARD-DEPLOY.md` for details.

---

## What gets uploaded (and what doesn't)

**Uploaded:** HTML, CSS, JS, images, PHP, `.htaccess`, blog content — everything visitors need.

**Not uploaded:**

| Excluded | Why |
|----------|-----|
| `.git/`, `.github/` | Dev tooling only |
| `scripts/` | Local dev scripts |
| `blog/schedule.json`, `bot-state.json`, `bot.log` | Server-side bot state — must not be overwritten on deploy |
| `*.zip`, `.DS_Store`, README files | Not needed on production |

---

## How you use it day to day

### Option A — tell me what to change

I edit → commit → push → site updates automatically.

Say things like:

- “Update the hero text and push to GitHub”
- “Deploy this”
- “Push to GitHub”

### Option B — you push yourself

```bash
cd "/Users/paden/Documents/sites/Bells Plumbing"
git add .
git commit -m "Describe your change"
git push origin main
```

~15 seconds later, refresh https://bellsplumbingutah.com

---

## Blog bot (runs on the server)

After each deploy, GitHub Actions hits the blog bot so it stays in sync.

**Daily cron** (set once in cPanel → Cron Jobs):

```bash
/usr/local/bin/php /home1/agentors/public_html/website_302faf96/blog/bot.php
```

**Dashboard:** https://bellsplumbingutah.com/SeoBot?key=YOUR_CRON_SECRET  
*(Secret is in `blog/config.php` → `cron_secret`, and in GitHub as `BLOG_BOT_KEY`.)*

The bot publishes one SEO blog post per day and auto-refills its topic queue.

---

## What we proved works

- GitHub Actions deploy completes in ~10–15 seconds (green check on Actions)
- Homepage loads at https://bellsplumbingutah.com
- Blog index at https://bellsplumbingutah.com/Blog.html
- First post published: `/blog/emergency-plumber-bountiful-utah.html`
- SEO Bot dashboard responds with the cron key

---

## Post-ready one-liner

We wired Bells Plumbing's site to auto-deploy: push to GitHub `main` → GitHub Actions FTPS to HostGator → live in ~15 seconds. No more manual cPanel uploads.

---

## Stack summary

| | |
|---|---|
| **Hosting** | HostGator cPanel (shared), account on agentadvisers.com |
| **CI/CD** | GitHub Actions + SamKirkland/FTP-Deploy-Action |
| **Protocol** | FTPS, port 21 |
| **Branch** | `main` only |
| **Repo** | https://github.com/wyatt-winters/BellsPlumbingUtah |
| **Live site** | https://bellsplumbingutah.com |

---

## Fallback — cPanel Git (if FTP ever times out)

Some hosts block GitHub’s cloud IPs. If deploys start failing with **timeout**, use cPanel Git Version Control instead:

1. cPanel → **Git Version Control** → clone `https://github.com/wyatt-winters/BellsPlumbingUtah.git`
2. Path: `/home1/agentors/public_html/website_302faf96`
3. Branch: `main`
4. Deploy script: `/bin/bash /home1/agentors/public_html/website_302faf96/deploy.sh`
5. Add a GitHub webhook on push events (cPanel provides the URL)

Same repo, same branch — just a different delivery path to the server.
