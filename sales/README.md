# Lead Desk sales page — bellsplumbingutah.com/sales

Static sales funnel for Saddle Up Lead Desk, hosted on the Bells Plumbing HostGator site.

| URL | File |
|-----|------|
| https://bellsplumbingutah.com/sales/ | `index.html` |
| https://bellsplumbingutah.com/sales/onboarding-demo.html | Onboarding walkthrough |
| https://bellsplumbingutah.com/sales/success.html | Post-Stripe checkout (site key) |
| https://bellsplumbingutah.com/sales/lead-desk/demo.html | Live widget demo |

## Before launch

1. Edit `stripe.config.json` — paste real Stripe payment links + billing portal URL
2. Upload `lead-desk-bundle.zip` to `/downloads/` on the server (via FTP/cPanel; zips are gitignored)
3. Set Stripe checkout success URL to:  
   `https://bellsplumbingutah.com/sales/success.html?session_id={CHECKOUT_SESSION_ID}`

## Deploy

Push to `main` → GitHub Actions deploys to bellsplumbingutah.com (~15s). See root `DEPLOY.md`.
