# Saddle Up AI Billboard — agentadvisers.com

Lives in this repo under `billboard/`. Deploys separately from the main Bells Plumbing site.

## Pipeline

```
Edit billboard/ → push to main → GitHub Actions → FTPS → agentadvisers.com
```

| Piece | Value |
|-------|-------|
| Repo | https://github.com/wyatt-winters/BellsPlumbingUtah |
| Workflow | `.github/workflows/deploy-billboard.yml` |
| FTP server | `192.254.188.195` |
| FTP user | `saddleupbillboard@bellsplumbingutah.com` (secret `BILLBOARD_FTP_USERNAME`) |
| Deploy folder | `/` — chrooted to `website_f9f5f795` |
| Document root | `/home1/agentors/public_html/website_f9f5f795` |
| Live site | https://agentadvisers.com |

## Day to day

```bash
cd "/Users/paden/Documents/Client Work/Websites/Bells Plumbing"
# edit files under billboard/
git add billboard/
git commit -m "Update billboard copy"
git push origin main
```

Watch deploys: https://github.com/wyatt-winters/BellsPlumbingUtah/actions
