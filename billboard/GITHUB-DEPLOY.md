# Deploy — Utah Boiler Experts

Same pipeline as Saddle Up AI.

## Pipeline

```
Your Mac (Cursor) → GitHub → GitHub Actions → HostGator (FTPS) → Live site
```

Push to `main` → live in ~15 seconds. No cPanel uploads.

## Setup

| Piece | Value |
|-------|-------|
| Repo | https://github.com/wyatt-winters/utah-boiler-experts |
| Workflow | `.github/workflows/deploy-hostgator.yml` |
| FTP server | `192.254.188.195` (secret `FTP_SERVER`) — use IP, not `agentadvisers.com` (DNS points elsewhere) |
| FTP user | `saddleupbillboard@bellsplumbingutah.com` (secret `FTP_USERNAME`) |
| Deploy folder | `/` only — domain FTP is chrooted to `website_f9f5f795` |
| Document root (cPanel) | `/home1/agentors/public_html/website_f9f5f795` |
| Live site | https://agentadvisers.com |

**Important:** Never set `FTP_SERVER_DIR` to the full `/home1/agentors/...` path.
That nests files under `home1/agentors/...` inside the site folder and causes 403.

If the site still 403s after deploy: cPanel → **Domains** → confirm document root
matches `website_f9f5f795`, delete any nested `home1/` folder in File Manager.

## Day to day

Say **push**, or:

```bash
cd "/Users/paden/Documents/sites/The other buddy"
git add .
git commit -m "Describe your change"
git push origin main
```

Watch deploys: https://github.com/wyatt-winters/utah-boiler-experts/actions
