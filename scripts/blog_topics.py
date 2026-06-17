"""55 SEO blog topics for Bells Plumbing Utah."""

from datetime import date, timedelta

START_DATE = date(2026, 6, 17)
SITE = "https://bellsplumbingutah.com"
PHONE = "(385) 255-8400"
PHONE_TEL = "3852558400"
COUNTIES = "Davis, Weber, Box Elder, and northern Salt Lake County"

TOPICS = [
    # Emergency
    {"title": "Emergency Plumber in Bountiful UT: What to Do Before We Arrive", "slug": "emergency-plumber-bountiful-utah", "category": "Emergency", "city": "Bountiful", "service": "emergency plumbing", "keyword": "emergency plumber Bountiful"},
    {"title": "Burst Pipe in Utah Winter: Step-by-Step Emergency Guide", "slug": "burst-pipe-utah-winter-emergency", "category": "Emergency", "city": "Layton", "service": "burst pipe repair", "keyword": "burst pipe Utah"},
    {"title": "Sewer Backup in Your Home: Health Risks and Immediate Actions", "slug": "sewer-backup-home-health-risks", "category": "Emergency", "city": "Ogden", "service": "sewer backup repair", "keyword": "sewer backup Utah"},
    {"title": "No Water in Your House? Causes and When to Call a Plumber", "slug": "no-water-in-house-utah", "category": "Emergency", "city": "Clearfield", "service": "emergency plumbing", "keyword": "no water house Utah"},
    {"title": "Frozen Pipes in Utah: Prevention and Thawing Safely", "slug": "frozen-pipes-utah-prevention", "category": "Emergency", "city": "Farmington", "service": "frozen pipe repair", "keyword": "frozen pipes Utah"},
    # Drain Cleaning
    {"title": "Slow Drain vs Clogged Drain: How to Tell the Difference", "slug": "slow-drain-vs-clogged-drain", "category": "Drain Cleaning", "city": "Kaysville", "service": "drain cleaning", "keyword": "clogged drain Utah"},
    {"title": "Kitchen Sink Won't Drain? 5 Causes We See Every Week in Davis County", "slug": "kitchen-sink-wont-drain-davis-county", "category": "Drain Cleaning", "city": "Layton", "service": "kitchen drain cleaning", "keyword": "kitchen sink clogged"},
    {"title": "Hydro Jetting vs Snaking: Which Drain Cleaning Method Is Right?", "slug": "hydro-jetting-vs-snaking-utah", "category": "Drain Cleaning", "city": "Ogden", "service": "hydro jetting", "keyword": "hydro jetting Utah"},
    {"title": "Main Line Clog Symptoms Every Utah Homeowner Should Know", "slug": "main-line-clog-symptoms-utah", "category": "Drain Cleaning", "city": "Roy", "service": "main sewer line repair", "keyword": "main line clog"},
    {"title": "How Often Should You Clean Your Drains in Utah?", "slug": "how-often-clean-drains-utah", "category": "Drain Cleaning", "city": "Syracuse", "service": "drain cleaning", "keyword": "drain cleaning schedule"},
    {"title": "Grease Clogs in Restaurant Drains: Commercial Plumbing Tips", "slug": "grease-clogs-restaurant-drains", "category": "Commercial", "city": "Ogden", "service": "commercial drain cleaning", "keyword": "commercial drain cleaning"},
    # Water Heaters
    {"title": "No Hot Water in Utah? Tank vs Tankless Troubleshooting Guide", "slug": "no-hot-water-utah-troubleshooting", "category": "Water Heaters", "city": "Bountiful", "service": "water heater repair", "keyword": "no hot water Utah"},
    {"title": "Water Heater Leaking From the Bottom: Repair or Replace?", "slug": "water-heater-leaking-bottom-utah", "category": "Water Heaters", "city": "Layton", "service": "water heater replacement", "keyword": "water heater leaking"},
    {"title": "Tankless Water Heater Pros and Cons for Utah Homes", "slug": "tankless-water-heater-pros-cons-utah", "category": "Water Heaters", "city": "Centerville", "service": "tankless water heater installation", "keyword": "tankless water heater Utah"},
    {"title": "How Long Do Water Heaters Last in Utah's Hard Water?", "slug": "water-heater-lifespan-utah-hard-water", "category": "Water Heaters", "city": "Farmington", "service": "water heater replacement", "keyword": "water heater lifespan Utah"},
    {"title": "Rumbling Water Heater Sounds: Sediment Buildup Explained", "slug": "rumbling-water-heater-sounds-utah", "category": "Water Heaters", "city": "Clearfield", "service": "water heater repair", "keyword": "water heater rumbling"},
    {"title": "Water Heater Replacement Cost in Utah (2026 Guide)", "slug": "water-heater-replacement-cost-utah-2026", "category": "Water Heaters", "city": "Ogden", "service": "water heater replacement", "keyword": "water heater cost Utah"},
    {"title": "Pilot Light Won't Stay Lit: Gas Water Heater Fixes", "slug": "pilot-light-wont-stay-lit-gas-water-heater", "category": "Water Heaters", "city": "Roy", "service": "water heater repair", "keyword": "pilot light water heater"},
    {"title": "When to Flush Your Water Heater in Utah (And Why It Matters)", "slug": "flush-water-heater-utah", "category": "Water Heaters", "city": "Kaysville", "service": "water heater maintenance", "keyword": "flush water heater Utah"},
    # Leaks
    {"title": "Slab Leak Signs in Utah Homes: Don't Ignore These Warnings", "slug": "slab-leak-signs-utah-homes", "category": "Leaks", "city": "Bountiful", "service": "slab leak repair", "keyword": "slab leak Utah"},
    {"title": "Hidden Water Leaks: How to Find Them Before Mold Sets In", "slug": "hidden-water-leaks-utah", "category": "Leaks", "city": "Layton", "service": "leak detection", "keyword": "hidden water leak"},
    {"title": "Toilet Running Constantly? How Much Water (and Money) You're Losing", "slug": "toilet-running-constantly-cost", "category": "Leaks", "city": "Ogden", "service": "toilet repair", "keyword": "running toilet fix"},
    {"title": "Under-Sink Leak Repair: DIY vs Calling a Licensed Plumber", "slug": "under-sink-leak-repair-utah", "category": "Leaks", "city": "Farmington", "service": "leak repair", "keyword": "under sink leak"},
    {"title": "High Water Bill in Utah? 7 Plumbing Leaks That Could Be the Cause", "slug": "high-water-bill-plumbing-leaks-utah", "category": "Leaks", "city": "Clearfield", "service": "leak detection", "keyword": "high water bill Utah"},
    {"title": "Ceiling Water Stain: What It Means and What to Do Next", "slug": "ceiling-water-stain-plumbing", "category": "Leaks", "city": "Roy", "service": "leak detection", "keyword": "ceiling water stain"},
    # Sewer & Pipe
    {"title": "Sewer Camera Inspection: What Homeowners in Utah Should Expect", "slug": "sewer-camera-inspection-utah", "category": "Sewer & Pipe", "city": "Ogden", "service": "sewer camera inspection", "keyword": "sewer camera inspection Utah"},
    {"title": "Trenchless Sewer Repair in Utah: Less Digging, Same Results", "slug": "trenchless-sewer-repair-utah", "category": "Sewer & Pipe", "city": "Layton", "service": "trenchless sewer repair", "keyword": "trenchless sewer repair"},
    {"title": "Tree Roots in Sewer Lines: A Common Utah Problem", "slug": "tree-roots-sewer-lines-utah", "category": "Sewer & Pipe", "city": "Bountiful", "service": "sewer line repair", "keyword": "tree roots sewer line"},
    {"title": "Sewer Smell in Your House: Causes and Professional Fixes", "slug": "sewer-smell-in-house-utah", "category": "Sewer & Pipe", "city": "Kaysville", "service": "sewer repair", "keyword": "sewer smell house"},
    {"title": "Cast Iron vs PVC Sewer Pipes in Older Utah Homes", "slug": "cast-iron-vs-pvc-sewer-pipes-utah", "category": "Sewer & Pipe", "city": "Ogden", "service": "sewer line replacement", "keyword": "sewer pipe replacement Utah"},
    {"title": "Main Water Line Break: Signs, Costs, and Emergency Steps", "slug": "main-water-line-break-utah", "category": "Sewer & Pipe", "city": "Clearfield", "service": "water main repair", "keyword": "water main break Utah"},
    {"title": "Sewer Line Replacement Cost in Utah: What Affects the Price", "slug": "sewer-line-replacement-cost-utah", "category": "Sewer & Pipe", "city": "Roy", "service": "sewer line installation", "keyword": "sewer line cost Utah"},
    {"title": "Bellied Sewer Pipe: What It Is and Why It Causes Backups", "slug": "bellied-sewer-pipe-backups", "category": "Sewer & Pipe", "city": "Syracuse", "service": "sewer line repair", "keyword": "bellied sewer pipe"},
    # Bathroom
    {"title": "Toilet Won't Flush Properly? Common Fixes and When to Replace", "slug": "toilet-wont-flush-properly-utah", "category": "Bathroom", "city": "Layton", "service": "toilet repair", "keyword": "toilet won't flush"},
    {"title": "Shower Drain Slow? Hair, Soap Scum, and Utah Hard Water", "slug": "shower-drain-slow-utah-hard-water", "category": "Bathroom", "city": "Bountiful", "service": "drain cleaning", "keyword": "slow shower drain"},
    {"title": "Low Water Pressure in the Shower: Causes and Solutions", "slug": "low-water-pressure-shower-utah", "category": "Bathroom", "city": "Farmington", "service": "plumbing repair", "keyword": "low water pressure shower"},
    {"title": "Bathroom Remodel Plumbing: What Permits You Need in Utah", "slug": "bathroom-remodel-plumbing-permits-utah", "category": "Bathroom", "city": "Centerville", "service": "plumbing installation", "keyword": "bathroom remodel plumbing Utah"},
    {"title": "Running Out of Hot Water During Showers? Sizing Your Water Heater", "slug": "running-out-hot-water-showers-utah", "category": "Bathroom", "city": "Ogden", "service": "water heater replacement", "keyword": "not enough hot water"},
    # Kitchen
    {"title": "Garbage Disposal Humming But Not Working: Quick Fixes", "slug": "garbage-disposal-humming-not-working", "category": "Kitchen", "city": "Kaysville", "service": "garbage disposal repair", "keyword": "garbage disposal humming"},
    {"title": "Dishwasher Not Draining? Check These Plumbing Issues First", "slug": "dishwasher-not-draining-plumbing", "category": "Kitchen", "city": "Layton", "service": "drain cleaning", "keyword": "dishwasher not draining"},
    {"title": "Kitchen Faucet Dripping: Repair vs Replace Guide", "slug": "kitchen-faucet-dripping-repair-replace", "category": "Kitchen", "city": "Bountiful", "service": "faucet repair", "keyword": "kitchen faucet dripping"},
    {"title": "Water Line to Refrigerator Leaking: Ice Maker Plumbing Tips", "slug": "refrigerator-water-line-leaking", "category": "Kitchen", "city": "Clearfield", "service": "leak repair", "keyword": "refrigerator water line leak"},
    {"title": "Gas Line for Stove Installation: Utah Safety Requirements", "slug": "gas-line-stove-installation-utah", "category": "Kitchen", "city": "Ogden", "service": "gas line services", "keyword": "gas line installation Utah"},
    # Maintenance
    {"title": "Utah Home Plumbing Maintenance Checklist for Every Season", "slug": "utah-home-plumbing-maintenance-checklist", "category": "Maintenance", "city": "Farmington", "service": "plumbing maintenance", "keyword": "plumbing maintenance Utah"},
    {"title": "Sump Pump Testing Before Utah Spring Runoff", "slug": "sump-pump-testing-utah-spring", "category": "Maintenance", "city": "Roy", "service": "sump pump repair", "keyword": "sump pump Utah"},
    {"title": "Water Softener and Your Plumbing: Protecting Pipes in Hard Water Areas", "slug": "water-softener-plumbing-hard-water-utah", "category": "Maintenance", "city": "Layton", "service": "plumbing maintenance", "keyword": "hard water plumbing Utah"},
    {"title": "Shut-Off Valves Every Homeowner Should Locate Today", "slug": "shut-off-valves-homeowner-guide", "category": "Maintenance", "city": "Bountiful", "service": "plumbing inspection", "keyword": "water shut off valve"},
    {"title": "Preparing Your Plumbing for Utah Vacation: Avoid Coming Home to a Flood", "slug": "plumbing-vacation-prep-utah", "category": "Maintenance", "city": "Kaysville", "service": "plumbing maintenance", "keyword": "vacation plumbing prep"},
    {"title": "Annual Plumbing Inspection: What's Included and Why It Saves Money", "slug": "annual-plumbing-inspection-utah", "category": "Maintenance", "city": "Ogden", "service": "plumbing inspection", "keyword": "plumbing inspection Utah"},
    # Service Areas
    {"title": "Plumber in Layton UT: Local Services, Pricing, and Same-Day Availability", "slug": "plumber-layton-utah", "category": "Service Areas", "city": "Layton", "service": "plumbing services", "keyword": "plumber Layton UT"},
    {"title": "Plumber in Ogden UT: Emergency, Sewer, and Water Heater Experts", "slug": "plumber-ogden-utah", "category": "Service Areas", "city": "Ogden", "service": "plumbing services", "keyword": "plumber Ogden UT"},
    {"title": "Plumber in Clearfield UT: Trusted Local Plumbing Since Day One", "slug": "plumber-clearfield-utah", "category": "Service Areas", "city": "Clearfield", "service": "plumbing services", "keyword": "plumber Clearfield UT"},
    {"title": "Plumber in Kaysville UT: Drain, Sewer, and Water Heater Help", "slug": "plumber-kaysville-utah", "category": "Service Areas", "city": "Kaysville", "service": "plumbing services", "keyword": "plumber Kaysville UT"},
    {"title": "Plumber in Roy UT: Fast Response Across Weber County", "slug": "plumber-roy-utah", "category": "Service Areas", "city": "Roy", "service": "plumbing services", "keyword": "plumber Roy UT"},
    {"title": "Plumber in Farmington UT: Family-Owned Service You Can Trust", "slug": "plumber-farmington-utah", "category": "Service Areas", "city": "Farmington", "service": "plumbing services", "keyword": "plumber Farmington UT"},
    {"title": "Plumber in Syracuse UT: Same-Day Plumbing Near You", "slug": "plumber-syracuse-utah", "category": "Service Areas", "city": "Syracuse", "service": "plumbing services", "keyword": "plumber Syracuse UT"},
    {"title": "Plumber in Brigham City UT: Serving Box Elder County", "slug": "plumber-brigham-city-utah", "category": "Service Areas", "city": "Brigham City", "service": "plumbing services", "keyword": "plumber Brigham City UT"},
]


def topics_with_dates():
    out = []
    for i, t in enumerate(TOPICS):
        row = dict(t)
        row["publish_date"] = (START_DATE + timedelta(days=i)).isoformat()
        out.append(row)
    return out
