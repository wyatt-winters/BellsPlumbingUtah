===================================================================
  UTAH BOILER EXPERTS — COMPLETE SITE UPDATE
  20 SEO blog posts + blog hub + nav update + 30 pages refreshed
===================================================================

This zip is a COMPLETE site update. Extract into public_html and it
replaces/adds everything needed. You don't need any prior deploys to
be in place — this zip stands alone.

  Total HTML files: 50 (30 existing pages + blog hub + 20 new posts)
  Architecture:     PHP-driven incremental blog release (no cron needed)
  Total new words:  ~22,000 across blog posts

-------------------------------------------------------------------
  HOW THE INCREMENTAL RELEASE WORKS
-------------------------------------------------------------------

All 20 HTML posts upload immediately. The PHP blog hub at /blog/
reads /blog/posts.json and only DISPLAYS posts whose publish date
has arrived. Date math runs on every page load. No cron job.

WHAT YOU CAN ADJUST in /blog/posts.json:

  "start_date": "2026-06-16"
  
  This is the day post #1 goes live. Posts #2-20 release one per
  day after that. Change to:
    - Delay schedule: push start_date forward
    - Restart schedule: change to today's date
    - Speed-publish all: set to a past date

-------------------------------------------------------------------
  DEPLOYMENT
-------------------------------------------------------------------

STEP 1 — Upload to public_html/
  cPanel File Manager → Upload → this zip
  Right-click zip → Extract → current directory (overwrites)
  Delete the zip after extraction

STEP 2 — Adjust start date (if needed)
  Edit /blog/posts.json, change "start_date" to today or your preferred
  launch date. Save.

STEP 3 — Test
  Visit https://utahboilerexperts.com/blog/
  Should show hero + 1 featured post + cards for released posts

STEP 4 — Resubmit sitemap to Google Search Console
  50 URLs (was 30)

-------------------------------------------------------------------
  THE 20 BLOG POSTS (release order)
-------------------------------------------------------------------

Day 1:  How Long Does a Boiler Last in Utah?
Day 2:  What's That Banging Noise? (Kettling)
Day 3:  Why Is My Boiler Leaking Water?
Day 4:  Hard Water and Your Boiler — Utah's Hidden Killer
Day 5:  Snow-Melt Driveway Cost & ROI
Day 6:  Radiant Floor Heating Cost in Utah
Day 7:  Combi Boiler vs Tank Water Heater
Day 8:  Why Won't My Boiler Turn On?
Day 9:  How to Bleed a Radiator (DIY)
Day 10: Mod-Con Boilers Explained
Day 11: How to Prepare Your Boiler for Utah Winter
Day 12: What Size Boiler Do I Need?
Day 13: Annual Maintenance — DIY vs. Pro
Day 14: Tankless Water Heaters Worth It?
Day 15: How to Cut Your Utah Heating Bill
Day 16: Heated Bathroom Floors — Cost
Day 17: Radiant Heat vs Forced Air
Day 18: When to Schedule Boiler Service
Day 19: Whole-House Hydronic Heating
Day 20: Your Boiler Died in January

Each post: 1,000-1,800 words, Article + FAQPage + Breadcrumb schema,
internal links to pillars, final CTA driving phone calls.

-------------------------------------------------------------------
  TROUBLESHOOTING
-------------------------------------------------------------------

/blog/ shows 500 error or PHP source code:
  PHP not enabled. cPanel → Select PHP Version → ensure 7.4+ active.

/blog/ shows "directory index forbidden":
  .htaccess missing. Re-upload it.

Blog hub shows empty state:
  start_date in posts.json is in the future. Edit to today.

Individual posts return 404:
  Verify file exists at /blog/{slug}.html. Check .htaccess present.

CSS broken on /blog/:
  /css/site.css wasn't updated. Re-extract zip.

Nav missing "Blog" on some pages:
  Re-extract or manually re-upload those pages.

-------------------------------------------------------------------
  ADDING / EDITING POSTS LATER
-------------------------------------------------------------------

NEW post: Copy an existing post HTML, edit content, save as
  /blog/your-slug.html. Add entry to posts.json with day_offset
  matching your desired release order. Add to sitemap.xml.

EDIT post: Edit HTML file directly in cPanel.

REMOVE from schedule: Set day_offset to 9999 in posts.json.

---
Built June 2026. Phase 1 (30 service pages) + 20-post blog now live.
