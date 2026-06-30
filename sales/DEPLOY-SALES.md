# Deploy sales page to bellsplumbingutah.com/sales

## Automatic (GitHub Actions)

Repo: https://github.com/wyatt-winters/BellsPlumbingUtah

Push to `main` triggers deploy. **If deploy fails with `530 Login authentication failed`:**

1. cPanel → **FTP Accounts** → reset password for `BellsPlumbing@bellsplumbingutah.com`
2. GitHub → **Settings → Secrets → Actions** on BellsPlumbingUtah repo
3. Update `FTP_PASSWORD` (and `FTP_USERNAME` if needed)
4. Re-run **Deploy to production** workflow

## Manual (cPanel File Manager)

1. Log into HostGator cPanel for bellsplumbingutah.com
2. Open File Manager → document root (`website_302faf96`)
3. Upload the entire `sales/` folder from this repo
4. Confirm: https://bellsplumbingutah.com/sales/

## Stripe success URL

```
https://bellsplumbingutah.com/sales/success.html?session_id={CHECKOUT_SESSION_ID}
```

## URLs

| Page | URL |
|------|-----|
| Sales | https://bellsplumbingutah.com/sales/ |
| Onboarding demo | https://bellsplumbingutah.com/sales/onboarding-demo.html |
| Post-checkout | https://bellsplumbingutah.com/sales/success.html |
| Widget demo | https://bellsplumbingutah.com/sales/lead-desk/demo.html |
