# GitHub → cPanel Deploy

Repo: https://github.com/wyatt-winters/BellsPlumbingUtah

## GitHub Secrets (already set)

| Secret | Value |
|--------|-------|
| `FTP_USERNAME` | `BellsPlumbing@bellsplumbingutah.com` |
| `FTP_PASSWORD` | *(your FTP password — stored in GitHub only)* |
| `BLOG_BOT_KEY` | *(matches `blog/config.php` cron_secret)* |

**Important:** Rotate your FTP password since it was shared in chat. Update the GitHub secret after changing it in cPanel.

## Option A — GitHub Actions FTP (automatic on push)

Every push to `main` runs `.github/workflows/deploy.yml`.

If deploy fails with **timeout**, your host may block GitHub’s cloud IPs. Use Option B.

Monitor runs: https://github.com/wyatt-winters/BellsPlumbingUtah/actions

## Option B — cPanel Git Version Control (recommended if FTP times out)

1. Log into cPanel for **agentadvisers.com**
2. Open **Git Version Control**
3. Clone: `https://github.com/wyatt-winters/BellsPlumbingUtah.git`
4. Repository path: `/home1/agentors/public_html/website_302faf96`
5. Set **Deploy HEAD** branch to `main`
6. Deploy script:

```bash
/bin/bash /home1/agentors/public_html/website_302faf96/deploy.sh
```

7. In GitHub repo → Settings → Webhooks → Add:
   - URL: *(cPanel gives you a webhook URL after creating the repo)*
   - Content type: `application/json`
   - Events: Push

Now every `git push` pulls on the server automatically — no FTP needed.

## After deploy — blog bot cron

In cPanel → **Cron Jobs**, add daily:

```bash
/usr/local/bin/php /home1/agentors/public_html/website_302faf96/blog/bot.php
```

Dashboard: `https://bellsplumbingutah.com/SeoBot?key=YOUR_CRON_SECRET`

## Manual push from your Mac

```bash
cd "/Users/paden/Documents/sites/Bells Plumbing"
git add -A && git commit -m "your message" && git push origin main
```
