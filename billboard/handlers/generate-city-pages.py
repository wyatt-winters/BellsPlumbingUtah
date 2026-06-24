#!/usr/bin/env python3
"""Generate missing service-area city pages from sandy.html template."""

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "service-area")
CSS_VER = "20260622"
JS_VER = "20260622"

CITIES = [
    {
        "slug": "south-jordan",
        "name": "South Jordan",
        "title": "Boiler Repair South Jordan, UT | Daybreak &amp; South Valley Hydronic",
        "description": "Boiler repair, radiant heat, and water heater service across South Jordan. Daybreak, Jordan Landing, and south valley subdivisions. (801) 685-3976.",
        "og_desc": "South Jordan hydronic specialists. Daybreak radiant installs to aging atmospheric boiler upgrades.",
        "lat": 40.5622, "lng": -111.9297,
        "eyebrow": "Daybreak · Jordan Landing · Oquirrh Shadows · Welby",
        "h1": "South Jordan <span class=\"accent\">hydronic</span> service done right.",
        "lede": "From Daybreak's newer radiant-heavy builds to 1990s subdivisions with boilers now hitting end-of-life. Same combustion-analysis standard across all of it.",
        "meta": ["~4,400 ft", "&lt;45 min", "Daybreak radiant", "Atmospheric upgrades"],
        "overview_h2": "South Jordan mixes new construction with 1990s boiler stock",
        "overview_p1": "South Jordan grew fast — Daybreak, Jordan Landing, and the Oquirrh Shadows corridor brought thousands of homes with hydronic or dual-fuel heating. Older pockets west of Bangerter still run original atmospheric boilers from the '90s build boom, many now due for condensing upgrades.",
        "overview_p2": "We handle both ends: emergency no-heat on a Weil-McLain CGa in Welby, and full mod-con replacements in Daybreak where homeowners want better efficiency and quieter operation. Hard water here is moderate-to-high — tankless descaling and boiler water treatment matter.",
        "issues": [
            ("Daybreak radiant &amp; combi installs", "Many Daybreak homes run combi or boiler-plus-indirect setups. We service Navien, Lochinvar, and Triangle Tube daily — ignition faults, expansion tank failures, and air-bound loops are the common calls."),
            ("1990s atmospheric end-of-life", "Welby and Jordan Landing subdivisions installed the same few atmospheric models. Banging, short-cycling, and rising gas bills usually mean replacement math beats another repair."),
            ("Hard water on tankless units", "South Jordan municipal water accelerates scale in tankless coils. Annual descaling doubles typical service life; we include it in maintenance visits."),
        ],
        "quote": "South Jordan is split between brand-new hydronic installs and boilers that have been running since the Clinton administration. We speak both languages.",
        "neighborhoods": ["Daybreak", "Jordan Landing", "Oquirrh Shadows", "Welby", "Glenmoor", "Highland Park", "Oquirrh Lake", "Terra Linda", "Country Park", "West Jordan border"],
        "adjacent": [("West Jordan", "west-jordan"), ("Riverton", "riverton"), ("Herriman", "herriman"), ("Sandy", "sandy")],
        "response": "South Jordan is a straightforward south-valley run — typically <strong>under 45 minutes during business hours</strong>. Daybreak and west-side calls are fast; eastern pockets near the mountain front add a few minutes.",
        "faqs": [
            ("Do you service all of South Jordan?", "Yes — Daybreak through Welby, Jordan Landing to the west bench. We also cover adjacent Riverton, West Jordan, and Herriman."),
            ("How fast is emergency response in South Jordan?", "Most business-hour calls see us within 45 minutes. After-hours winter emergencies same night."),
            ("Do you work on Daybreak combi boilers?", "Yes — Navien, Lochinvar, and Triangle Tube combis are common in Daybreak. We carry parts for same-visit fixes on most failures."),
            ("Is my 1990s boiler worth fixing?", "Depends on the failure. Ignition and gas valve repairs on sound units often make sense. Heat exchanger or control board failure on a 30-year-old atmospheric unit usually means replacement."),
            ("Do you install radiant in South Jordan remodels?", "Yes — staple-up and slab systems for additions, basements, and whole-home retrofits where forced air isn't the right fit."),
        ],
        "cta": "From <span class=\"accent\">Daybreak combis</span> to '90s atmospheric swaps.",
        "aside": "South valley depth.",
    },
    {
        "slug": "west-jordan",
        "name": "West Jordan",
        "title": "Boiler Repair West Jordan, UT | Central Valley Hydronic Specialists",
        "description": "Boiler repair, water heater, and radiant heat service across West Jordan. Family neighborhoods from 1970s stock to newer builds. (801) 685-3976.",
        "og_desc": "West Jordan boiler repair and replacement. Central valley response under 45 minutes.",
        "lat": 40.6097, "lng": -111.9391,
        "eyebrow": "Jordan Hills · Westwood · Copper Hills · Gardner Village",
        "h1": "West Jordan <span class=\"accent\">boiler</span> service without the runaround.",
        "lede": "Dense family neighborhoods with a wide spread of boiler ages — from original 1970s atmospheric units to newer mod-con installs near Copper Hills.",
        "meta": ["~4,400 ft", "&lt;45 min", "1970s–2000s stock", "All major brands"],
        "overview_h2": "West Jordan has one of the valley's widest boiler age ranges",
        "overview_p1": "West Jordan's housing stock spans five decades in a single city. Jordan Hills and older west-side neighborhoods still run cast iron and atmospheric sectional boilers. Copper Hills and newer east-side builds often have mod-con or combi systems with radiant in the basement slab.",
        "overview_p2": "That mix is exactly what we do daily — combustion analysis on a 1982 Burnham in Gardner Village one call, altitude-neutral mod-con tune on a Lochinvar in Copper Hills the next. We don't treat boilers as a side business.",
        "issues": [
            ("Original 1970s–80s atmospheric boilers", "Jordan Hills and central West Jordan have high concentrations of end-of-life atmospheric units. We do more repair-vs-replace consultations here than almost anywhere in the south valley."),
            ("Basement radiant in 2000s builds", "Copper Hills and east-side subdivisions often have in-slab radiant with boilers now 15–20 years old. Circulator and expansion tank failures are the typical mid-life service items."),
            ("Water heater + boiler combos", "Many homes run a boiler for heat and a separate tank or tankless for domestic hot water. We service the whole mechanical room — not just the piece that's loudest."),
        ],
        "quote": "West Jordan homeowners call us when the generalist HVAC company shrugged at the boiler. That's our entire business model.",
        "neighborhoods": ["Jordan Hills", "Westwood", "Copper Hills", "Gardner Village", "Bloomington", "Oquirrh Shadows border", "Archibald", "Newberry", "West Jordan City Center", "South Jordan border"],
        "adjacent": [("South Jordan", "south-jordan"), ("Riverton", "riverton"), ("Murray", "murray"), ("Herriman", "herriman")],
        "response": "West Jordan sits central in our south-valley territory — <strong>typically under 45 minutes</strong> during business hours from dispatch.",
        "faqs": [
            ("Do you cover all of West Jordan?", "Yes — Gardner Village to Copper Hills, Jordan Hills to the south bench. Adjacent Murray, South Jordan, and Riverton too."),
            ("What's the most common West Jordan boiler call?", "No-heat on a 25–35 year old atmospheric unit in winter. Second most common: circulator failure on a radiant system in a 2000s build."),
            ("Do you replace boilers same-week?", "Often yes — when the replacement unit is in stock and the venting path is straightforward. We quote lead time honestly upfront."),
            ("Can you service both my boiler and water heater?", "Yes — one trip, one invoice. We stock common parts for both."),
            ("Do you work on forced-air homes adding radiant?", "Yes — basement and bathroom staple-up radiant tied to an existing or new boiler is a common West Jordan remodel scope."),
        ],
        "cta": "Five decades of <span class=\"accent\">West Jordan</span> boilers. One specialist shop.",
        "aside": "Central valley coverage.",
    },
    {
        "slug": "murray",
        "name": "Murray",
        "title": "Boiler Repair Murray, UT | Central Salt Lake Valley Hydronic",
        "description": "Boiler repair, replacement, and radiant heat across Murray. Central valley location, fast response. Fashion Place to Wheeler Farm. (801) 685-3976.",
        "og_desc": "Murray boiler specialists. Central valley — under 40 minute typical response.",
        "lat": 40.6669, "lng": -111.8879,
        "eyebrow": "Fashion Place · Wheeler Farm · Murray Park · Vine Street",
        "h1": "Murray <span class=\"accent\">central valley</span> hydronic service.",
        "lede": "Dead-center in the Salt Lake Valley — fast response, dense mix of post-war homes and 1980s subdivisions with boilers now reaching replacement age.",
        "meta": ["~4,400 ft", "&lt;40 min", "Post-war to 1990s", "Fast dispatch"],
        "overview_h2": "Murray's central location means fast response and diverse housing",
        "overview_p1": "Murray sits in the geographic center of the Salt Lake Valley, which makes it one of our fastest response cities. Housing ranges from post-war ranches near Murray Park to 1980s–90s subdivisions east of Fashion Place — most with original or second-generation hydronic heating.",
        "overview_p2": "We see a lot of Murray calls in January: aging atmospheric boilers that held on through December finally fail on the coldest night. We carry common ignition modules, gas valves, and circulators on the truck for same-visit fixes when repair makes sense.",
        "issues": [
            ("Post-war boiler retrofits", "Older Murray ranches often had forced air added later while the original boiler still runs the basement or a wing. Dual-system homes need a tech who understands both."),
            ("1980s–90s atmospheric end-of-life", "East Murray subdivisions are hitting the replacement wave now — same Weil-McLain and Burnham models we see across the central valley."),
            ("Commercial-adjacent residential", "Murray's mix of small multi-family and converted units near State Street sometimes have commercial-scale boilers in residential envelopes. We size and service correctly."),
        ],
        "quote": "Murray is where we can get to you fastest in the valley. That matters when it's 12° and the boiler just quit.",
        "neighborhoods": ["Murray Park", "Wheeler Farm", "Vine Street", "Fashion Place East", "Grant", "Woodside", "Pavilion", "Southwood", "Poppy Lane", "Millcreek border"],
        "adjacent": [("Millcreek", "millcreek"), ("Holladay", "holladay"), ("Sandy", "sandy"), ("West Jordan", "west-jordan")],
        "response": "Murray is our fastest central-valley city — <strong>often under 40 minutes</strong> during business hours because dispatch runs straight down I-15 or State Street.",
        "faqs": [
            ("Do you service all of Murray?", "Yes — Murray Park to Fashion Place, Wheeler Farm to the Millcreek border."),
            ("How fast is Murray emergency response?", "Among our fastest — typically under 40 minutes business hours, same-night after hours."),
            ("My Murray home has two heating systems — can you handle that?", "Yes — boiler plus furnace combos are common in older Murray stock. We diagnose the whole picture."),
            ("Do you do boiler replacements in Murray?", "Yes — heat-loss sized replacements, not like-for-like guesses. Financing on qualifying installs."),
            ("What brands do you see most in Murray?", "Weil-McLain, Burnham, and Slant/Fin atmospheric units in older homes; Lochinvar and Navien in newer retrofits."),
        ],
        "cta": "Central valley <span class=\"accent\">fast response</span>. Real boiler depth.",
        "aside": "Fast central dispatch.",
    },
    {
        "slug": "millcreek",
        "name": "Millcreek",
        "title": "Boiler Repair Millcreek, UT | East Bench Hydronic Specialists",
        "description": "Boiler repair and radiant heat across Millcreek. East bench neighborhoods adjacent to Holladay and SLC. (801) 685-3976.",
        "og_desc": "Millcreek east bench boiler and radiant specialists.",
        "lat": 40.6869, "lng": -111.8755,
        "eyebrow": "East Millcreek · Canyon Rim · Evergreen · Brickyard",
        "h1": "Millcreek east bench <span class=\"accent\">hydronic</span> depth.",
        "lede": "Tucked between Holladay and Salt Lake City — post-war homes, east-bench custom builds, and radiant systems that need a specialist, not a generalist.",
        "meta": ["~4,500 ft", "&lt;45 min", "East bench mix", "Radiant service"],
        "overview_h2": "Millcreek blends older east-bench homes with newer infill",
        "overview_p1": "Millcreek incorporated recently but the neighborhoods are old — Canyon Rim, Evergreen, and east-side streets off 3300 South have post-war and mid-century homes, many still on original or second-generation boilers. Infill and remodels added radiant bathrooms and basement zones.",
        "overview_p2": "We're adjacent constantly — Holladay to the south, SLC Avenues to the north. Millcreek gets the same east-bench depth: cast iron sectional service, copper-tube atmospheric repair, and mod-con upgrades when the math works.",
        "issues": [
            ("Mid-century atmospheric boilers", "Evergreen and Canyon Rim have high concentrations of 1960s–80s atmospheric units. Pilot assemblies, thermocouples, and gas valves — we stock them."),
            ("Radiant bathroom add-ons", "East bench remodels often add hydronic bath floors without upgrading the boiler. We balance the whole system so the new zone doesn't starve the rest."),
            ("Brickyard corridor hard water", "Millcreek's water chemistry accelerates scale in boilers and tankless coils. Annual service and proper water treatment extend equipment life."),
        ],
        "quote": "Millcreek is east-bench work — older metal, tighter mechanical rooms, and homeowners who expect the tech to actually know the system.",
        "neighborhoods": ["Canyon Rim", "Evergreen", "East Millcreek", "Brickyard", "Olympus Cove border", "Holladay border", "SLC east bench", "Mt. Olympus area", "Valley Center", "Highland Drive corridor"],
        "adjacent": [("Holladay", "holladay"), ("Salt Lake City", "salt-lake-city"), ("Murray", "murray"), ("Cottonwood Heights", "cottonwood-heights")],
        "response": "Millcreek runs <strong>40–50 minutes</strong> typical business-hour response — easy access from valley dispatch up Highland Drive or I-215.",
        "faqs": [
            ("Do you service all of Millcreek?", "Yes — Canyon Rim through Brickyard, Evergreen to the Olympus foothills."),
            ("Are Millcreek boilers different from Holladay?", "Similar stock — post-war east bench. Same brands, same end-of-life timeline, same specialist approach."),
            ("Can you add radiant to my Millcreek remodel?", "Yes — bath floors, basement zones, and whole-wing radiant tied to your existing or new boiler."),
            ("Do you work on cast iron sectional boilers?", "Daily — they're common in Millcreek's older pockets. Section replacement, gasket work, and full replacement when warranted."),
            ("How fast on a no-heat call?", "Typically 40–50 minutes business hours. After-hours same night in winter."),
        ],
        "cta": "East bench <span class=\"accent\">Millcreek</span> — specialist service.",
        "aside": "East bench expertise.",
    },
    {
        "slug": "riverton",
        "name": "Riverton",
        "title": "Boiler Repair Riverton, UT | South Valley Growth Corridor",
        "description": "Boiler repair, radiant heat, and water heater service in Riverton. South valley growth area from 1990s builds to new construction. (801) 685-3976.",
        "og_desc": "Riverton hydronic service. South valley growth corridor specialists.",
        "lat": 40.5219, "lng": -111.9391,
        "eyebrow": "Riverton · Rosecrest · Western Springs · Camp Williams corridor",
        "h1": "Riverton <span class=\"accent\">south valley</span> hydronic service.",
        "lede": "South valley growth from 1990s subdivisions to new builds pushing toward Herriman — boilers, radiant, and tankless service with under-45-minute response.",
        "meta": ["~4,400 ft", "&lt;45 min", "1990s–new builds", "Radiant + combi"],
        "overview_h2": "Riverton grew south — and brought hydronic heating with it",
        "overview_p1": "Riverton expanded aggressively from the 1990s onward. Rosecrest and western subdivisions have boilers and radiant systems now 15–25 years old — entering the phase where circulators, expansion tanks, and ignition components need real attention.",
        "overview_p2": "Newer construction toward Herriman often runs combi boilers or mod-con with indirect tanks. We install, service, and replace across the full range — not just the units that are easy to access.",
        "issues": [
            ("Mid-life radiant mechanicals", "1990s–2000s Riverton radiant homes need manifold actuator, zone valve, and circulator service. The tubing is fine; the moving parts age out."),
            ("Combi boiler scaling", "Hard south-valley water affects combi domestic coils. Descaling and proper inlet filtration prevent premature failure."),
            ("New-build warranty follow-up", "Some Riverton installs weren't commissioned correctly. We retune combustion, verify expansion tank pre-charge, and fix air-bound loops left by the builder."),
        ],
        "quote": "Riverton is the south valley's growth story — and growth means a lot of hydronic systems hitting their first real service decade.",
        "neighborhoods": ["Rosecrest", "Western Springs", "Riverton City Center", "Oquirrh Lake border", "Herriman border", "South Jordan border", "Camp Williams area", "Mountain View Corridor", "Riverbend", "Monarch Meadows"],
        "adjacent": [("Herriman", "herriman"), ("South Jordan", "south-jordan"), ("Bluffdale", None), ("Draper", "draper")],
        "response": "Riverton is a standard south-valley run — <strong>under 45 minutes</strong> typical business-hour response.",
        "faqs": [
            ("Do you service all of Riverton?", "Yes — Rosecrest to the Herriman border, western springs to the valley floor."),
            ("My Riverton radiant system has cold spots — can you fix it?", "Yes — air purge, circulator diagnosis, actuator replacement, and loop balancing are common fixes."),
            ("Do you install new boilers in Riverton?", "Yes — heat-loss sized mod-con and atmospheric-to-condensing upgrades with financing on qualifying jobs."),
            ("How fast on emergencies?", "Typically under 45 minutes business hours. Winter after-hours same night."),
            ("Do you service tankless water heaters too?", "Yes — repair, descale, and replacement. Hard water makes annual descaling worth it."),
        ],
        "cta": "Riverton <span class=\"accent\">growth corridor</span> hydronic specialists.",
        "aside": "South valley service.",
    },
    {
        "slug": "herriman",
        "name": "Herriman",
        "title": "Boiler Repair Herriman, UT | Foothill &amp; New Build Hydronic",
        "description": "Boiler repair, radiant heat, and snow-melt service in Herriman. Newer construction, higher elevation, combi and mod-con specialists. (801) 685-3976.",
        "og_desc": "Herriman foothill boiler service. New construction and elevation-aware installs.",
        "lat": 40.5141, "lng": -112.0325,
        "eyebrow": "Herriman · Rose Canyon · Butterfield Canyon · Shamrock Ridge",
        "h1": "Herriman <span class=\"accent\">foothill</span> hydronic specialists.",
        "lede": "Newer south-west valley builds at slightly higher elevation — combi boilers, in-slab radiant, and the commissioning issues that come with fast-growth construction.",
        "meta": ["~4,600 ft", "&lt;50 min", "New construction", "Combi + radiant"],
        "overview_h2": "Herriman's newer stock still needs specialist service",
        "overview_p1": "Herriman built out fast in the 2000s and 2010s. Most homes have boilers or combis with radiant in the slab — systems that are fine when commissioned correctly and frustrating when they're not. We fix builder shortcuts: wrong expansion tank charge, unbalanced loops, combustion never tuned.",
        "overview_p2": "Elevation runs a few hundred feet above the valley floor. Not Park City altitude, but enough that combustion should be verified on every mod-con service call. We run analyzers on every visit.",
        "issues": [
            ("Builder commissioning gaps", "Expansion tank pre-charge, loop fill pressure, and combustion tuning are often skipped at turnover. We correct it in one visit."),
            ("In-slab radiant air locks", "Herriman's staple-up and slab systems get air-bound after service or power outages. Proper purge procedure matters."),
            ("Combi scaling from hard water", "West-side valley water plus high hot-water demand in larger Herriman homes means combi coils need descaling on schedule."),
        ],
        "quote": "Herriman homes are new enough that homeowners assume nothing should break yet. The mechanical room tells a different story.",
        "neighborhoods": ["Rose Canyon", "Shamrock Ridge", "Herriman Town Center", "Butterfield Canyon area", "Copper Cove", "Herriman Main Street", "South Hills", "Blackridge", "Riverton border", "Mountain View Corridor"],
        "adjacent": [("Riverton", "riverton"), ("South Jordan", "south-jordan"), ("Bluffdale", None), ("Draper", "draper")],
        "response": "Herriman runs <strong>45–55 minutes</strong> typical response — slightly longer for upper foothill streets.",
        "faqs": [
            ("Do you service all of Herriman?", "Yes — town center through Rose Canyon and the Butterfield corridor."),
            ("My new Herriman home's boiler never ran right — why?", "Usually commissioning — expansion tank, fill pressure, or combustion. One proper service visit often fixes years of annoyance."),
            ("Is altitude a factor in Herriman?", "Moderately — we verify combustion on mod-cons. Not Park City derate territory, but not sea level either."),
            ("Do you install snow-melt in Herriman?", "Where driveway grade warrants it — design, install, and service."),
            ("Emergency response time?", "Typically 45–55 minutes business hours. After-hours same night."),
        ],
        "cta": "Herriman <span class=\"accent\">new build</span> hydronic done right.",
        "aside": "Foothill commissioning.",
    },
    {
        "slug": "midway",
        "name": "Midway",
        "title": "Boiler Repair Midway, UT | Heber Valley Luxury Hydronic",
        "description": "Boiler repair, radiant heat, and snow-melt across Midway and the Heber Valley. Luxury homes, altitude-tuned service. (801) 685-3976.",
        "og_desc": "Midway Heber Valley hydronic specialists. Luxury radiant and snow-melt.",
        "lat": 40.5122, "lng": -111.4743,
        "eyebrow": "Midway · Soldier Hollow · Wasatch Mountain State Park · Charleston border",
        "h1": "Midway <span class=\"accent\">Heber Valley</span> luxury hydronic.",
        "lede": "Swiss Days charm outside, serious mechanical rooms inside — radiant, snow-melt, and altitude-tuned boilers for Midway's luxury and vacation homes.",
        "meta": ["~5,600 ft", "60–75 min", "Luxury radiant", "Snow-melt"],
        "overview_h2": "Midway is Heber Valley luxury — with real altitude",
        "overview_p1": "Midway sits around 5,600 feet in the Heber Valley, with luxury homes, vacation properties, and full hydronic packages — in-slab radiant, snow-melt driveways, mod-con boilers with indirect tanks. The same altitude and glycol considerations as Heber City apply here.",
        "overview_p2": "We drive Midway regularly from valley dispatch. Response is longer than Salt Lake County — typically 60–75 minutes — but we know these systems and stock the parts that mountain homes actually need.",
        "issues": [
            ("Altitude combustion on mod-cons", "Midway's elevation requires proper derate. Rich-running units foul flame rods and waste gas — we tune to manufacturer tables."),
            ("Snow-melt on steep driveways", "Midway properties often have heated drives and walks. Sensor failures and idle-mode runaway are common service items."),
            ("Vacation-home freeze protection", "Second homes need reliable low-temp strategy and glycol checks before owners arrive for the weekend."),
        ],
        "quote": "Midway mechanical rooms are built like Park City lite — radiant, snow-melt, indirect tanks — and they need the same specialist attention.",
        "neighborhoods": ["Midway town center", "Soldier Hollow", "Wasatch Mountain State Park area", "Charleston border", "Interlaken", "Creek View", "Homestead", "Valley hills", "Heber border", "Deer Creek corridor"],
        "adjacent": [("Heber City", "heber-city"), ("Charleston", None), ("Park City", "park-city"), ("Provo Canyon", None)],
        "response": "Midway runs <strong>60–75 minutes</strong> typical business-hour response from valley dispatch. We batch Heber Valley calls when possible.",
        "faqs": [
            ("Do you service Midway and the Heber Valley?", "Yes — Midway, Heber City, Charleston, and surrounding valley properties."),
            ("How fast can you get to Midway on a no-heat call?", "Typically 60–75 minutes business hours. After-hours same night in winter emergencies."),
            ("Do you work on snow-melt in Midway?", "Yes — service, sensor replacement, control upgrades, and new design."),
            ("Is altitude derate required in Midway?", "Yes — around 5,600 ft. We tune every mod-con to altitude specs."),
            ("Do you service vacation homes?", "Yes — pre-season checks, glycol verification, and emergency response when you're not in town."),
        ],
        "cta": "Midway <span class=\"accent\">valley luxury</span> hydronic depth.",
        "aside": "Heber Valley coverage.",
    },
    {
        "slug": "american-fork",
        "name": "American Fork",
        "title": "Boiler Repair American Fork, UT | North Utah County Hydronic",
        "description": "Boiler repair, radiant heat, and water heater service in American Fork. North Utah County neighborhoods. (801) 685-3976.",
        "og_desc": "American Fork boiler and radiant specialists. North Utah County.",
        "lat": 40.3769, "lng": -111.7958,
        "eyebrow": "American Fork · Highland border · Cedar Hills · Pleasant Grove border",
        "h1": "American Fork <span class=\"accent\">north county</span> hydronic service.",
        "lede": "North Utah County neighborhoods with a mix of 1980s boiler stock and newer foothill builds pushing toward Highland — same-day response on most calls.",
        "meta": ["~4,600 ft", "&lt;55 min", "North Utah County", "Radiant + repair"],
        "overview_h2": "American Fork bridges valley floor and foothill custom homes",
        "overview_p1": "American Fork sits at the north end of Utah County with housing from established valley neighborhoods to newer construction climbing toward Cedar Hills and Highland. Boilers range from 1980s atmospheric units to mod-con installs in custom foothill properties.",
        "overview_p2": "We're in American Fork regularly as part of our Utah County expansion — repair, replacement, and radiant service with honest repair-vs-replace guidance.",
        "issues": [
            ("1980s–90s atmospheric replacements", "Central American Fork subdivisions are entering the condensing upgrade wave. We run heat-loss math before quoting."),
            ("Foothill custom radiant", "Homes toward Cedar Hills often have multi-zone radiant. Manifold and actuator service is common mid-life work."),
            ("Hard Utah County water", "Scale affects tankless and combi performance. Descaling and inlet filtration are part of our maintenance scope."),
        ],
        "quote": "American Fork is where Utah County starts feeling like the Wasatch — and the boilers get more interesting as you climb.",
        "neighborhoods": ["American Fork city center", "Cedar Hills border", "Highland border", "Pleasant Grove border", "Saratoga Springs border", "Lehi border", "East bench", "West fields", "Alpine Highway corridor", "Mutual Dell"],
        "adjacent": [("Pleasant Grove", "pleasant-grove"), ("Highland", "highland"), ("Lehi", "lehi"), ("Orem", "orem")],
        "response": "American Fork runs <strong>50–60 minutes</strong> typical business-hour response from valley dispatch.",
        "faqs": [
            ("Do you service American Fork?", "Yes — full city coverage plus adjacent Pleasant Grove, Highland, and Lehi."),
            ("How fast is response from Salt Lake?", "Typically 50–60 minutes business hours. Same-day on most calls."),
            ("Do you replace aging atmospheric boilers?", "Yes — right-sized mod-con replacements with financing on qualifying installs."),
            ("Radiant heat service?", "Yes — in-slab, staple-up, and panel systems."),
            ("Emergency winter service?", "Yes — after-hours line with same-night response when possible."),
        ],
        "cta": "American Fork <span class=\"accent\">north county</span> boiler depth.",
        "aside": "Utah County north.",
    },
    {
        "slug": "pleasant-grove",
        "name": "Pleasant Grove",
        "title": "Boiler Repair Pleasant Grove, UT | Utah County Hydronic",
        "description": "Boiler repair, radiant floor heat, and water heater service in Pleasant Grove. Mix of older and newer Utah County homes. (801) 685-3976.",
        "og_desc": "Pleasant Grove boiler repair and radiant service.",
        "lat": 40.3641, "lng": -111.7385,
        "eyebrow": "Pleasant Grove · Grove Creek · Battle Creek · Lindon border",
        "h1": "Pleasant Grove <span class=\"accent\">hydronic</span> specialists.",
        "lede": "Established Utah County neighborhoods plus newer growth — boilers from the '80s through today's mod-con installs, serviced by a hydronic-first shop.",
        "meta": ["~4,600 ft", "&lt;55 min", "Older + new mix", "All brands"],
        "overview_h2": "Pleasant Grove has decades of boiler installs to service",
        "overview_p1": "Pleasant Grove's core neighborhoods date to the 1970s–90s with original or second-generation boilers now aging out. Newer construction on the edges adds combi and radiant systems. We work across both — repair when it makes sense, replace when the math says so.",
        "overview_p2": "Grove Creek and Battle Creek areas bring foothill elevation and slightly more custom mechanical rooms. Combustion analysis on every service call, not guesswork.",
        "issues": [
            ("End-of-life atmospheric boilers", "Pleasant Grove's core has the same 30-year atmospheric units we see across Utah County — banging, short cycling, rising bills."),
            ("Battle Creek foothill installs", "Higher streets often have mod-con boilers that need altitude-aware tuning and proper venting."),
            ("Radiant zone valve failures", "Mid-life radiant homes need actuator and valve service — we stock common replacements."),
        ],
        "quote": "Pleasant Grove is classic Utah County — older boilers in the core, newer hydronic on the edges. We cover the whole map.",
        "neighborhoods": ["Pleasant Grove city center", "Grove Creek", "Battle Creek", "Lindon border", "American Fork border", "Manila", "Canyon View", "East bench", "West side", "State Street corridor"],
        "adjacent": [("Lindon", "lindon"), ("American Fork", "american-fork"), ("Orem", "orem"), ("Lehi", "lehi")],
        "response": "Pleasant Grove — <strong>50–60 minutes</strong> typical business-hour response.",
        "faqs": [
            ("Do you cover Pleasant Grove?", "Yes — full city plus Lindon, American Fork, and Orem adjacent."),
            ("Common Pleasant Grove boiler issue?", "No-heat on aging atmospheric units in winter — ignition, gas valve, or circulator failures."),
            ("Do you install radiant?", "Yes — new installs and repairs on existing systems."),
            ("Same-day service?", "Most business-day calls same day. Emergencies prioritized."),
            ("What brands?", "All major hydronic brands — Weil-McLain, Lochinvar, Navien, Burnham, Triangle Tube, and more."),
        ],
        "cta": "Pleasant Grove <span class=\"accent\">Utah County</span> boiler service.",
        "aside": "Utah County service.",
    },
    {
        "slug": "orem",
        "name": "Orem",
        "title": "Boiler Repair Orem, UT | UVU Corridor Hydronic Specialists",
        "description": "Boiler repair, replacement, and radiant heat in Orem. UVU corridor, mix of student housing and family neighborhoods. (801) 685-3976.",
        "og_desc": "Orem boiler repair and radiant heat. UVU corridor specialists.",
        "lat": 40.2969, "lng": -111.6946,
        "eyebrow": "Orem · SCERA · Lakeview · Vineyard border · Provo border",
        "h1": "Orem <span class=\"accent\">UVU corridor</span> hydronic service.",
        "lede": "Utah County's hub city — older east-side homes with original boilers, west-side growth with radiant and combi systems, and everything in between.",
        "meta": ["~4,700 ft", "&lt;55 min", "UVU corridor", "Repair + install"],
        "overview_h2": "Orem's housing stock demands real hydronic breadth",
        "overview_p1": "Orem spans from post-war neighborhoods near SCERA to massive west-side growth toward Vineyard. East Orem has boilers and radiators from the 1960s–80s. West Orem and Geneva Road corridors have newer radiant and combi installs — some commissioned well, some not.",
        "overview_p2": "We treat Orem as core Utah County territory — same-day response on most calls, combustion analysis standard, and honest guidance when a 35-year-old boiler should retire.",
        "issues": [
            ("East Orem aging boilers", "Older neighborhoods still run atmospheric sectional boilers. Repair vs replace is a conversation we have weekly in Orem."),
            ("West-side combi scaling", "Larger new homes with combi boilers and high DHW load need descaling and proper flow settings."),
            ("Multi-unit and ADU systems", "Orem's rental and ADU conversions sometimes add zones without resizing the boiler. We balance and right-size."),
        ],
        "quote": "Orem is Utah County in miniature — old metal on the east, new radiant on the west, and a lot of boilers in between.",
        "neighborhoods": ["SCERA area", "Lakeview", "Sunset", "Sharon", "Orem city center", "Vineyard border", "Provo border", "Lindon border", "Palos Verdes", "Westmore"],
        "adjacent": [("Provo", "provo"), ("Vineyard", None), ("Lindon", "lindon"), ("Pleasant Grove", "pleasant-grove")],
        "response": "Orem — <strong>50–60 minutes</strong> typical business-hour response from valley dispatch.",
        "faqs": [
            ("Do you service all of Orem?", "Yes — SCERA to Vineyard border, Lakeview to Provo line."),
            ("East vs west Orem — different service?", "East skews older atmospheric repair and replacement. West skews combi and radiant mid-life service. We handle both."),
            ("Student rental no-heat calls?", "Yes — we work with owners and property managers. Up-front pricing, clear communication."),
            ("Boiler replacement timeline?", "Often within a week when unit is in stock. We quote honestly."),
            ("Radiant floor service?", "Yes — full diagnostic, purge, actuator, and circulator service."),
        ],
        "cta": "Orem <span class=\"accent\">hydronic</span> breadth. One specialist shop.",
        "aside": "UVU corridor coverage.",
    },
    {
        "slug": "provo",
        "name": "Provo",
        "title": "Boiler Repair Provo, UT | BYU Corridor &amp; Old-Home Hydronic",
        "description": "Boiler repair, radiant heat, and boiler replacement in Provo. BYU corridor, historic neighborhoods, older boiler stock. (801) 685-3976.",
        "og_desc": "Provo boiler specialists. BYU corridor and historic home hydronic.",
        "lat": 40.2338, "lng": -111.6585,
        "eyebrow": "Provo · Grandview · Riverbottoms · BYU corridor · East Bench",
        "h1": "Provo <span class=\"accent\">old-home</span> boiler specialists.",
        "lede": "Utah County's oldest city — Victorian-era housing through mid-century neighborhoods with boilers, radiators, and hydronic systems that need depth, not a furnace tech guessing.",
        "meta": ["~4,700 ft", "55–65 min", "Historic + mid-century", "Cast iron + radiant"],
        "overview_h2": "Provo has real old-home boiler inventory",
        "overview_p1": "Provo's east bench and central neighborhoods have homes from every decade — some with original cast iron boilers and column radiators, others with 1970s copper-tube atmospheric units, and newer west-side builds with radiant slabs. It's one of the more mechanically interesting cities in Utah County.",
        "overview_p2": "We drive Provo regularly. The BYU corridor brings rental and multi-family work; the east bench brings restoration-quality boiler service on systems other companies won't touch.",
        "issues": [
            ("Cast iron sectional boilers", "Provo's oldest homes still run sectional cast iron. We service, section-replace, and full-replace when warranted."),
            ("Column radiator systems", "Older hydronic with column rads needs proper air purge and zone balancing — not a one-size approach."),
            ("Rental property no-heat", "Landlords need fast, documented service. We answer the phone and show up."),
        ],
        "quote": "Provo is where you still find boilers that were installed when Eisenhower was president — and they can run another decade with the right service.",
        "neighborhoods": ["Grandview", "Riverbottoms", "East Bench", "Provo city center", "BYU corridor", "Lakeview", "Southeast Provo", "North Park", "Rock Canyon", "Orem border"],
        "adjacent": [("Orem", "orem"), ("Springville", None), ("Lindon", "lindon"), ("Mapleton", None)],
        "response": "Provo — <strong>55–65 minutes</strong> typical business-hour response. Same-day on most calls.",
        "faqs": [
            ("Do you service all of Provo?", "Yes — Grandview to west-side growth, BYU corridor to east bench."),
            ("Can you work on cast iron boilers?", "Yes — it's a core competency. Section gaskets, aquastat, gas valve, full replacement."),
            ("Rental emergency service?", "Yes — we work with property owners regularly. Clear pricing upfront."),
            ("Radiator heat — do you bleed and balance?", "Yes — column and baseboard systems across Provo's older neighborhoods."),
            ("Boiler replacement in historic homes?", "Yes — right-sized replacements that respect existing distribution where possible."),
        ],
        "cta": "Provo <span class=\"accent\">historic hydronic</span> done right.",
        "aside": "Old-home boiler depth.",
    },
    {
        "slug": "lindon",
        "name": "Lindon",
        "title": "Boiler Repair Lindon, UT | Established Utah County Hydronic",
        "description": "Boiler repair and radiant heat service in Lindon. Established Utah County neighborhoods between Orem and Pleasant Grove. (801) 685-3976.",
        "og_desc": "Lindon boiler repair and radiant service.",
        "lat": 40.3433, "lng": -111.7208,
        "eyebrow": "Lindon · Pleasant Grove border · Orem border · East bench",
        "h1": "Lindon <span class=\"accent\">established</span> neighborhood hydronic.",
        "lede": "Quiet Utah County city with decades of boiler installs — atmospheric units hitting end-of-life and radiant systems entering mid-life service.",
        "meta": ["~4,600 ft", "&lt;55 min", "Established homes", "Repair + replace"],
        "overview_h2": "Lindon is established Utah County — with aging boilers",
        "overview_p1": "Lindon sits between Orem and Pleasant Grove with stable, established neighborhoods built primarily from the 1970s through 2000s. Most homes heat with boilers — atmospheric units now 25–40 years old, and radiant systems from the 1990s build wave.",
        "overview_p2": "We service Lindon as part of our regular Utah County routes. Fast enough response, deep enough expertise — combustion analysis, honest repair-vs-replace, and mod-con upgrades when the numbers work.",
        "issues": [
            ("Atmospheric boiler replacement wave", "Lindon's core neighborhoods are in the replacement window — we quote heat-loss sized mod-con upgrades."),
            ("1990s radiant circulator wear", "Circulators and zone valves from the original install are failing now. Same-visit replacement when stocked."),
            ("Water quality and scale", "Utah County hard water affects both tank and tankless DHW. Maintenance extends life."),
        ],
        "quote": "Lindon doesn't make headlines — but it has a lot of boilers that need a specialist this winter.",
        "neighborhoods": ["Lindon city center", "Pleasant Grove border", "Orem border", "East bench", "North Lindon", "South fields", "Mountain vista", "State Street area", "600 North corridor", "Geneva Road area"],
        "adjacent": [("Orem", "orem"), ("Pleasant Grove", "pleasant-grove"), ("American Fork", "american-fork"), ("Provo", "provo")],
        "response": "Lindon — <strong>50–60 minutes</strong> typical business-hour response.",
        "faqs": [
            ("Do you service Lindon?", "Yes — full coverage plus adjacent Orem and Pleasant Grove."),
            ("Most common Lindon call?", "No-heat on 30-year atmospheric boiler — gas valve, ignition, or circulator."),
            ("Replacement financing?", "Available on qualifying installs — ask when you call."),
            ("Radiant service?", "Yes — diagnostic, purge, actuator, and pump replacement."),
            ("Same-day availability?", "Most business-day calls same day."),
        ],
        "cta": "Lindon <span class=\"accent\">hydronic</span> service without the wait.",
        "aside": "Established neighborhood care.",
    },
    {
        "slug": "highland",
        "name": "Highland",
        "title": "Boiler Repair Highland, UT | Foothill Custom Home Hydronic",
        "description": "Boiler repair, radiant heat, and snow-melt service in Highland. Foothill custom homes, altitude-aware mod-con service. (801) 685-3976.",
        "og_desc": "Highland foothill custom home boiler and radiant specialists.",
        "lat": 40.4263, "lng": -111.7955,
        "eyebrow": "Highland · Alpine border · American Fork · Cedar Hills",
        "h1": "Highland <span class=\"accent\">foothill custom</span> hydronic.",
        "lede": "North Utah County foothills — larger custom homes with multi-zone radiant, indirect tanks, and mod-con boilers that need altitude-aware service.",
        "meta": ["~4,900 ft", "55–65 min", "Custom homes", "Multi-zone radiant"],
        "overview_h2": "Highland custom homes run serious hydronic packages",
        "overview_p1": "Highland climbs the Wasatch foothills with custom and semi-custom homes — many with full in-slab radiant, snow-melt on steep approaches, Lochinvar or Navien mod-cons, and indirect domestic tanks. These aren't entry-level mechanical rooms.",
        "overview_p2": "Elevation approaches 5,000 feet in upper Highland. Combustion must be verified. We service, tune, and replace with altitude tables — not sea-level defaults.",
        "issues": [
            ("Multi-zone radiant balancing", "Large Highland homes with 8+ zones need proper actuator and flow balancing. Cold rooms are often a control issue, not a boiler failure."),
            ("Mod-con altitude tuning", "Upper Highland mod-cons need derate verification. Rich combustion fouls flame rods within a season."),
            ("Snow-melt on steep drives", "Heated approaches are common. We service sensors, glycol, and boiler-side controls."),
        ],
        "quote": "Highland mechanical rooms are built for comfort, not compromise — and they need a tech who reads a combustion analyzer.",
        "neighborhoods": ["Highland city center", "Cedar Hills border", "Alpine border", "American Fork border", "East bench", "West hills", "Canyon Road", "Mockingbird Lane area", "Olympus Hills border", "Highland Glen"],
        "adjacent": [("American Fork", "american-fork"), ("Alpine", None), ("Cedar Hills", None), ("Lehi", "lehi")],
        "response": "Highland — <strong>55–65 minutes</strong> typical response. Upper foothill streets may run slightly longer.",
        "faqs": [
            ("Do you service Highland custom homes?", "Yes — multi-zone radiant, snow-melt, mod-con, and indirect tanks."),
            ("Altitude service required?", "Yes — upper Highland approaches 5,000 ft. We tune combustion accordingly."),
            ("Cold room in one zone?", "Often actuator or balancing — we diagnose before recommending boiler replacement."),
            ("New snow-melt install?", "Yes — design and install integrated with existing or new boiler."),
            ("Emergency response?", "Same-night winter emergencies when possible. Typically 55–65 min business hours."),
        ],
        "cta": "Highland <span class=\"accent\">custom hydronic</span> at foothill elevation.",
        "aside": "Foothill custom expertise.",
    },
    {
        "slug": "bountiful",
        "name": "Bountiful",
        "title": "Boiler Repair Bountiful, UT | Davis County Hydronic Specialists",
        "description": "Boiler repair, replacement, and radiant heat in Bountiful. Established Davis County homes, 1960s–70s boiler stock. (801) 685-3976.",
        "og_desc": "Bountiful Davis County boiler repair and replacement.",
        "lat": 40.8894, "lng": -111.8808,
        "eyebrow": "Bountiful · Fruit Heights · West Bountiful · South Davis bench",
        "h1": "Bountiful <span class=\"accent\">Davis County</span> boiler depth.",
        "lede": "Established Davis County city with decades of atmospheric boiler installs — many original 1960s–70s units ready for condensing upgrades and same-day repair when they still have life left.",
        "meta": ["~4,800 ft", "45–55 min", "1960s–70s stock", "Cast iron + atmospheric"],
        "overview_h2": "Bountiful has classic Davis County boiler inventory",
        "overview_p1": "Bountiful's neighborhoods matured in the 1960s–80s with the same atmospheric sectional boilers installed across Davis County — Weil-McLain, Burnham, Slant/Fin. Many are original. Many are on borrowed time.",
        "overview_p2": "We run Bountiful regularly from valley dispatch. North Davis access is straightforward — typically under an hour. We do cast iron service, atmospheric repair, and full mod-con replacements with heat-loss sizing.",
        "issues": [
            ("Original 1960s–70s atmospheric boilers", "Bountiful's core has high concentrations of end-of-life atmospheric units. Replacement often beats the third repair in one season."),
            ("South bench radiant add-ons", "Remodeled homes added radiant zones without boiler upgrades. We balance and right-size."),
            ("Davis County hard water", "Accelerates scale in boilers and tankless. Water treatment and annual service matter."),
        ],
        "quote": "Bountiful is Davis County classic — the boilers are old, the homeowners are practical, and they want straight answers.",
        "neighborhoods": ["Bountiful city center", "Fruit Heights border", "West Bountiful", "South bench", "Orchard Drive", "Millcreek border", "North Salt Lake border", "Woods Cross border", "Val Verda", "Mueller Park area"],
        "adjacent": [("North Salt Lake", None), ("Woods Cross", None), ("Centerville", None), ("Farmington", "farmington")],
        "response": "Bountiful — <strong>45–55 minutes</strong> typical business-hour response from valley dispatch.",
        "faqs": [
            ("Do you service Bountiful?", "Yes — full city plus adjacent Farmington, Centerville, and North Salt Lake."),
            ("Most common Bountiful boiler?", "1960s–70s atmospheric sectional — Weil-McLain and Burnham dominate."),
            ("Cast iron repair?", "Yes — section work, gaskets, and full replacement when warranted."),
            ("Same-day repair?", "Most business-day calls same day when parts are on the truck."),
            ("Condensing upgrade savings?", "Typically 15–25% gas reduction vs old atmospheric. We run the math openly."),
        ],
        "cta": "Bountiful <span class=\"accent\">Davis County</span> atmospheric-to-mod-con.",
        "aside": "North Davis service.",
    },
    {
        "slug": "farmington",
        "name": "Farmington",
        "title": "Boiler Repair Farmington, UT | Lagoon Corridor Hydronic",
        "description": "Boiler repair and radiant heat in Farmington. Davis County, Lagoon corridor neighborhoods. (801) 685-3976.",
        "og_desc": "Farmington Davis County boiler and radiant specialists.",
        "lat": 40.9805, "lng": -111.8874,
        "eyebrow": "Farmington · Station Park · Lagoon corridor · Clark Lane",
        "h1": "Farmington <span class=\"accent\">Davis County</span> hydronic service.",
        "lede": "Lagoon corridor and established Davis County neighborhoods — 1970s boiler stock, newer west-side growth, and honest specialist service north of Salt Lake.",
        "meta": ["~4,400 ft", "45–55 min", "Davis County", "Atmospheric + radiant"],
        "overview_h2": "Farmington mixes Davis County old stock with new growth",
        "overview_p1": "Farmington stretches from established neighborhoods near Lagoon to newer construction around Station Park and the west-side I-15 corridor. Older sections have atmospheric boilers from the 1970s–90s; newer builds often have combi or mod-con with radiant.",
        "overview_p2": "We service Farmington as core Davis County territory — repair, replacement, and radiant with same-day availability on most business-day calls.",
        "issues": [
            ("1970s–90s atmospheric end-of-life", "East Farmington and Lagoon corridor subdivisions are in the replacement window."),
            ("West-side combi commissioning", "Newer builds sometimes ship with combustion never tuned. One service visit fixes years of nuisance faults."),
            ("I-15 corridor hard water", "Davis County municipal water affects DHW performance. Descaling on schedule."),
        ],
        "quote": "Farmington is the Davis County commute corridor — and a lot of boilers that have been commuting through winters since the Ford administration.",
        "neighborhoods": ["Farmington city center", "Lagoon area", "Station Park", "Clark Lane", "West Farmington", "Kaysville border", "Bountiful border", "East bench", "Glover Lane", "Promontory border"],
        "adjacent": [("Kaysville", "kaysville"), ("Bountiful", "bountiful"), ("Centerville", None), ("Layton", "layton")],
        "response": "Farmington — <strong>45–55 minutes</strong> typical response from valley dispatch.",
        "faqs": [
            ("Do you service Farmington?", "Yes — Lagoon corridor to Station Park, east bench to west growth."),
            ("Davis County response time?", "Typically 45–55 minutes business hours."),
            ("Boiler replacement?", "Yes — heat-loss sized, financing on qualifying installs."),
            ("Radiant floor service?", "Yes — full diagnostic and repair."),
            ("Emergency line?", "24/7 winter no-heat — same-night when possible."),
        ],
        "cta": "Farmington <span class=\"accent\">Davis County</span> boiler specialists.",
        "aside": "Lagoon corridor coverage.",
    },
    {
        "slug": "kaysville",
        "name": "Kaysville",
        "title": "Boiler Repair Kaysville, UT | Davis County Hydronic",
        "description": "Boiler repair, replacement, and radiant heat in Kaysville. Mix of older Davis County homes and growth areas. (801) 685-3976.",
        "og_desc": "Kaysville boiler repair and radiant service.",
        "lat": 41.0352, "lng": -111.9386,
        "eyebrow": "Kaysville · Fruit Heights border · Layton border · East bench",
        "h1": "Kaysville <span class=\"accent\">Davis County</span> hydronic.",
        "lede": "North Davis County with a mix of established neighborhoods and newer growth — atmospheric boilers aging out, radiant systems mid-life, specialist response from valley dispatch.",
        "meta": ["~4,400 ft", "50–60 min", "North Davis", "Repair + replace"],
        "overview_h2": "Kaysville sits in north Davis County's boiler belt",
        "overview_p1": "Kaysville's established neighborhoods have the same 1970s–90s atmospheric boiler inventory as the rest of Davis County. Newer growth toward Fruit Heights and the Layton border adds mod-con and radiant installs from the 2000s build wave.",
        "overview_p2": "We're in Kaysville regularly — part of our Davis County loop with Farmington and Layton. Combustion analysis standard, repair-vs-replace honesty, and mod-con upgrades when the homeowner is ready.",
        "issues": [
            ("Atmospheric replacement timing", "Kaysville's core is deciding repair vs replace on 30-year boilers — we run the numbers openly."),
            ("Fruit Heights border custom homes", "Larger homes with multi-zone radiant need balancing and actuator service."),
            ("Layton border new builds", "Combi boilers with scaling issues from hard water — descaling prevents premature failure."),
        ],
        "quote": "Kaysville homeowners call when the third repair in a winter doesn't hold. We tell them when it's time.",
        "neighborhoods": ["Kaysville city center", "Fruit Heights border", "Layton border", "Farmington border", "East bench", "West side", "Cherry Hill", "Holbrook Canyon area", "Mountain Road", "South Kaysville"],
        "adjacent": [("Layton", "layton"), ("Farmington", "farmington"), ("Fruit Heights", None), ("Centerville", None)],
        "response": "Kaysville — <strong>50–60 minutes</strong> typical business-hour response.",
        "faqs": [
            ("Do you service Kaysville?", "Yes — full city plus adjacent Layton and Farmington."),
            ("North Davis response?", "Typically 50–60 minutes from valley dispatch."),
            ("When to replace vs repair?", "We assess age, failure type, and efficiency. Major heat exchanger failure on 30+ year unit = replace."),
            ("Radiant heat?", "Yes — service and install."),
            ("Financing on replacements?", "Available on qualifying installs."),
        ],
        "cta": "Kaysville <span class=\"accent\">north Davis</span> boiler clarity.",
        "aside": "North Davis County.",
    },
    {
        "slug": "layton",
        "name": "Layton",
        "title": "Boiler Repair Layton, UT | Hill AFB Corridor Hydronic",
        "description": "Boiler repair and radiant heat in Layton. Hill AFB corridor, Davis County's largest city. (801) 685-3976.",
        "og_desc": "Layton Davis County boiler repair. Hill AFB corridor specialists.",
        "lat": 41.0602, "lng": -111.9711,
        "eyebrow": "Layton · Hill AFB corridor · East Layton · West Layton · Kaysville border",
        "h1": "Layton <span class=\"accent\">Hill AFB corridor</span> hydronic.",
        "lede": "Davis County's largest city — dense 1980s subdivisions, Hill AFB corridor housing, and boilers from every decade serviced by a hydronic-first shop.",
        "meta": ["~4,400 ft", "50–60 min", "Hill AFB corridor", "High volume repair"],
        "overview_h2": "Layton has volume — and variety",
        "overview_p1": "Layton is Davis County's biggest city by population. East Layton's 1980s–90s subdivisions have atmospheric boilers hitting end-of-life. West Layton and the Hill AFB corridor mix military housing, rentals, and owner-occupied homes with diverse mechanical setups.",
        "overview_p2": "We run Layton calls daily in heating season. High volume means we stock the parts Layton's common boiler models need — Weil-McLain, Burnham, Lochinvar — for same-visit fixes when repair makes sense.",
        "issues": [
            ("1980s subdivision atmospheric wave", "East Layton is peak replacement territory — same models, same failures, same condensing upgrade path."),
            ("Rental and multi-family no-heat", "We work with property managers. Documented service, upfront pricing, fast response."),
            ("Hill AFB corridor hard water", "Accelerates scale in tank and tankless. Maintenance contracts available."),
        ],
        "quote": "Layton is high-volume Davis County work — and we'd rather fix it right once than come back three times.",
        "neighborhoods": ["East Layton", "West Layton", "Hill AFB corridor", "Kaysville border", "Syracuse border", "Clearfield border", "Layton Hills", "Valley View", "East Gate", "Woodland"],
        "adjacent": [("Kaysville", "kaysville"), ("Clearfield", None), ("Syracuse", None), ("Ogden", "ogden")],
        "response": "Layton — <strong>50–60 minutes</strong> typical business-hour response.",
        "faqs": [
            ("Do you service all of Layton?", "Yes — East to West Layton, Hill AFB corridor to Kaysville border."),
            ("Rental property service?", "Yes — property managers welcome. Clear invoices, fast response."),
            ("Most common Layton boiler?", "1980s–90s Weil-McLain and Burnham atmospheric — replacement wave now."),
            ("Same-day service?", "Most business-day calls same day."),
            ("Water heater too?", "Yes — tank, tankless, and indirect."),
        ],
        "cta": "Layton <span class=\"accent\">Davis County</span> volume, specialist depth.",
        "aside": "Hill AFB corridor.",
    },
    {
        "slug": "ogden",
        "name": "Ogden",
        "title": "Boiler Repair Ogden, UT | Historic Home &amp; Cast Iron Specialists",
        "description": "Boiler repair, replacement, and radiant heat in Ogden. Historic homes, cast iron sectional boilers, Weber County. (801) 685-3976.",
        "og_desc": "Ogden historic home boiler specialists. Cast iron and radiant.",
        "lat": 41.2230, "lng": -111.9738,
        "eyebrow": "Ogden · East Bench · Jefferson · Historic districts · Weber State corridor",
        "h1": "Ogden <span class=\"accent\">historic</span> boiler specialists.",
        "lede": "Weber County's hub — Victorian and early-century housing with cast iron sectional boilers, column radiators, and the hydronic depth most HVAC generalists don't carry.",
        "meta": ["~4,300 ft", "60–75 min", "Historic homes", "Cast iron specialty"],
        "overview_h2": "Ogden has Utah's densest historic boiler inventory north of SLC",
        "overview_p1": "Ogden's east bench and historic districts have homes from the early 1900s through mid-century — many still heated by cast iron sectional boilers and column radiators. These systems need a specialist who understands steam vs hot water, section gaskets, and when a 60-year-old boiler still has life.",
        "overview_p2": "We're Ogden's northern reach — drive time is longer than Davis County, typically 60–75 minutes, but we know cast iron and we show up. Weber County calls are grouped when possible; emergencies get priority.",
        "issues": [
            ("Cast iron sectional boilers", "Ogden's oldest homes run sectional cast iron daily. We section-replace, re-gasket, and full-replace when the block is done."),
            ("Column and cast radiators", "Proper air purge and zone balancing on century-old distribution — not a furnace tech's job."),
            ("East bench 1970s atmospheric", "Newer Ogden neighborhoods have the same atmospheric end-of-life pattern as Davis County."),
        ],
        "quote": "Ogden is where cast iron still earns its keep — if you know how to service it.",
        "neighborhoods": ["Historic Ogden", "East Bench", "Jefferson", "West Ogden", "South Ogden border", "Weber State corridor", "Bonneville", "East Central", "Trolley District", "Mount Ogden foothills"],
        "adjacent": [("Layton", "layton"), ("Roy", None), ("South Ogden", None), ("North Ogden", None)],
        "response": "Ogden — <strong>60–75 minutes</strong> typical business-hour response. Northern reach of our active territory.",
        "faqs": [
            ("Do you service Ogden?", "Yes — historic districts to east bench subdivisions. Northern Weber County."),
            ("Cast iron boiler repair?", "Core competency — section work, controls, gas valve, full replacement."),
            ("How fast on emergencies?", "Typically 60–75 minutes business hours. Same-night winter emergencies when possible."),
            ("Steam vs hot water?", "Both — we diagnose correctly before touching anything."),
            ("Radiator bleeding?", "Yes — column and baseboard across Ogden's older neighborhoods."),
        ],
        "cta": "Ogden <span class=\"accent\">cast iron</span> and historic hydronic.",
        "aside": "Weber County historic depth.",
    },
]


def esc(s):
    return s.replace("&", "&amp;") if "&amp;" not in s and "&lt;" not in s else s


def adjacent_html(adjacent):
    links = []
    for name, slug in adjacent:
        if slug:
            links.append(f'<a href="/service-area/{slug}">{name}</a>')
        else:
            links.append(name)
    return ", ".join(links) + "."


def faq_schema(faqs):
    return json.dumps([
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faqs
    ], indent=8)


def render_city(c):
    slug = c["slug"]
    name = c["name"]
    neighborhoods_li = "\n".join(f"            <li>{n}</li>" for n in c["neighborhoods"])
    issues_html = ""
    for title, body in c["issues"]:
        issues_html += f"          <h3>{title}</h3>\n          <p>{body}</p>\n"
    faq_html = ""
    for q, a in c["faqs"]:
        faq_html += (
            f'            <div class="faq-item"><button class="faq-q" aria-expanded="false">'
            f"<span>{q}</span><span class=\"faq-icon\">+</span></button>"
            f'<div class="faq-a"><div class="faq-a-inner">{a}</div></div></div>\n'
        )
    meta_strip = "\n".join(f"        <span><strong>{m.split(' ', 1)[0]}</strong>{m.split(' ', 1)[1] if ' ' in m else ''}</span>" for m in c["meta"])
    # fix meta strip - the format is weird. Let me use simpler approach
    meta_parts = []
    for m in c["meta"]:
        if m.startswith("<"):
            parts = m.split(" ", 1)
            meta_parts.append(f'        <span><strong>{parts[0]}</strong> {parts[1]}</span>')
        else:
            idx = m.find(" ")
            if idx > 0:
                meta_parts.append(f'        <span><strong>{m[:idx]}</strong> {m[idx+1:]}</span>')
            else:
                meta_parts.append(f'        <span><strong>{m}</strong></span>')
    meta_strip = "\n".join(meta_parts)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{c['title']}</title>
<meta name="description" content="{c['description']}">
<link rel="canonical" href="https://utahboilerexperts.com/service-area/{slug}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0F1217">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:url" content="https://utahboilerexperts.com/service-area/{slug}">
<meta property="og:site_name" content="Utah Boiler Experts">
<meta property="og:title" content="{c['title']}">
<meta property="og:description" content="{c['og_desc']}">
<meta property="og:image" content="https://utahboilerexperts.com/images/share.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700;9..144,800&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/site.css?v={CSS_VER}">

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{ "@type": ["LocalBusiness", "HVACBusiness"], "@id": "https://utahboilerexperts.com#localbusiness", "name": "Utah Boiler Experts", "telephone": "+1-801-685-3976", "url": "https://utahboilerexperts.com", "address": {{ "@type": "PostalAddress", "streetAddress": "5212 Chester Rd", "addressLocality": "West Valley City", "addressRegion": "UT", "postalCode": "84120", "addressCountry": "US" }} }},
    {{
      "@type": "Service",
      "@id": "https://utahboilerexperts.com/service-area/{slug}#service",
      "name": "Boiler Repair & Hydronic Heating in {name}, UT",
      "serviceType": "Boiler Repair, Replacement, Radiant Heating, Snow-Melt",
      "description": "{c['og_desc']}",
      "url": "https://utahboilerexperts.com/service-area/{slug}",
      "provider": {{ "@id": "https://utahboilerexperts.com#localbusiness" }},
      "areaServed": {{
        "@type": "City",
        "name": "{name}",
        "containedInPlace": {{ "@type": "State", "name": "Utah" }},
        "geo": {{ "@type": "GeoCoordinates", "latitude": {c['lat']}, "longitude": {c['lng']} }}
      }}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://utahboilerexperts.com/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Service Areas", "item": "https://utahboilerexperts.com/service-areas" }},
        {{ "@type": "ListItem", "position": 3, "name": "{name}", "item": "https://utahboilerexperts.com/service-area/{slug}" }}
      ]
    }},
    {{
      "@type": "FAQPage",
      "mainEntity": {faq_schema(c['faqs'])}
    }}
  ]
}}
</script>

<script async src="https://www.googletagmanager.com/gtag/js?id=G-DF82TDY0D7"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-DF82TDY0D7');
  gtag('config', 'AW-17966193749');
  gtag('config', 'AW-17966193749/qPGWCJ26mIMcENW4-fZC', {{
    'phone_conversion_number': '(801) 685-3976'
  }});
</script>

</head>
<body>

<header class="site">
  <div class="wrap header-row">
    <a href="/" class="brand"><img src="/images/logo.png" alt="The Other Buddy Plumbing & Heating" class="brand-logo"></a>
    <nav class="primary" id="primary-nav"><a href="/#services">Services</a><a href="/#brands">Brands</a><a href="/service-areas">Service Areas</a><a href="/blog/">Blog</a><a href="/about">About</a><a href="/#faq">FAQ</a></nav>
    <div class="header-cta"><a href="tel:+18016853976" class="phone-pill"><span class="pulse"></span><span>(801) 685-3976</span></a><button class="nav-toggle" id="nav-toggle" aria-expanded="false" aria-controls="primary-nav">☰</button></div>
  </div>
</header>

<main id="top">

  <section class="page-hero">
    <div class="wrap">
      <nav class="breadcrumbs">
        <a href="/">Home</a><span class="sep">/</span>
        <a href="/service-areas">Service Areas</a><span class="sep">/</span>
        <span class="current">{name}</span>
      </nav>
      <span class="eyebrow">{c['eyebrow']}</span>
      <h1>{c['h1']}</h1>
      <p class="lede">{c['lede']}</p>
      <div class="page-hero-ctas">
        <a class="btn btn--primary" href="tel:+18016853976">Call (801) 685-3976 <span class="arrow">→</span></a>
        <a class="btn btn--ghost" href="#services">What we do here</a>
      </div>
      <div class="meta-strip">
{meta_strip}
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="content-grid">
        <article class="prose">

          <h2 id="overview">{c['overview_h2']}</h2>
          <p>{c['overview_p1']}</p>
          <p>{c['overview_p2']}</p>

          <h2 id="services">What we service in {name}</h2>
          <div class="checklist">
            <div class="item"><div><strong>Boiler repair</strong>All brands. <a href="/boiler-repair">More →</a></div></div>
            <div class="item"><div><strong>Boiler replacement</strong>Right-sized upgrades. <a href="/boiler-replacement">More →</a></div></div>
            <div class="item"><div><strong>Water heater service</strong>Tank, tankless, hybrid. <a href="/water-heater-repair">More →</a></div></div>
            <div class="item"><div><strong>Radiant floor heating</strong>Service &amp; install. <a href="/radiant-floor-heating">More →</a></div></div>
            <div class="item"><div><strong>Snow-melt systems</strong>Where applicable. <a href="/snow-melt-systems">More →</a></div></div>
            <div class="item"><div><strong>Emergency repair</strong>24/7 winter. <a href="/emergency-boiler-repair">More →</a></div></div>
          </div>

          <h2 id="local-issues">Issues we see in {name} specifically</h2>
{issues_html}
          <blockquote>
"{c['quote']}"
          </blockquote>

          <h2 id="neighborhoods">Neighborhoods we cover</h2>
          <ul class="neighborhood-grid">
{neighborhoods_li}
          </ul>
          <p>Adjacent: {adjacent_html(c['adjacent'])}</p>

          <h2 id="response">Response times</h2>
          <p>{c['response']}</p>

          <h2 id="faq">Common questions</h2>
          <div class="faq-list">
{faq_html}          </div>

        </article>

        <aside class="content-aside">
          <div class="aside-card">
            <div class="label">{name} service</div>
            <h3>{c['aside']}</h3>
            <p>Boiler repair, replacement, radiant heat, and emergency no-heat response across {name}.</p>
            <a class="btn btn--primary" href="tel:+18016853976">(801) 685-3976</a>
          </div>
          <div class="aside-card">
            <span class="toc"><span class="label">On this page</span>
              <ol>
                <li><a href="#overview">{name} overview</a></li>
                <li><a href="#services">What we service</a></li>
                <li><a href="#local-issues">{name}-specific issues</a></li>
                <li><a href="#neighborhoods">Neighborhoods</a></li>
                <li><a href="#response">Response times</a></li>
                <li><a href="#faq">FAQ</a></li>
              </ol>
            </span>
          </div>
        </aside>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-intro">
        <div><span class="eyebrow">Related</span><h2 style="margin-top:18px;">{name} services.</h2></div>
        <p class="lede">Each service has its own deep dive.</p>
      </div>
      <div class="related-grid">
        <a class="related-link" href="/boiler-repair"><div><div class="what">Service</div><div class="name">Boiler repair</div></div><div class="arrow">→</div></a>
        <a class="related-link" href="/water-heater-repair"><div><div class="what">Hot water</div><div class="name">Water heater repair</div></div><div class="arrow">→</div></a>
        <a class="related-link" href="/radiant-floor-heating"><div><div class="what">Comfort</div><div class="name">Radiant heat</div></div><div class="arrow">→</div></a>
        <a class="related-link" href="/boiler-replacement"><div><div class="what">Upgrade</div><div class="name">Boiler replacement</div></div><div class="arrow">→</div></a>
      </div>
    </div>
  </section>

  <section class="final-cta">
    <div class="wrap wrap--tight">
      <span class="eyebrow">{name} hydronic specialists</span>
      <h2 style="margin-top:18px;">{c['cta']}</h2>
      <p>Boiler repair, radiant heat, and emergency service across {name} — hydronic-first, not a side gig.</p>
      <div class="final-cta-buttons">
        <a class="btn btn--primary" href="tel:+18016853976">Call (801) 685-3976 <span class="arrow">→</span></a>
        <a class="btn btn--ghost" href="mailto:hello@utahboilerexperts.com">Email us <span class="arrow">↗</span></a>
      </div>
    </div>
  </section>

</main>

<footer class="site">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="/" class="brand"><img src="/images/logo.png" alt="The Other Buddy Plumbing & Heating" class="brand-logo brand-logo--footer"></a>
        <p>Hydronic heating specialists — boiler repair, radiant floor heat, and snow-melt systems across Utah and the Wasatch Front. Locally owned and operated by The Other Buddy Plumbing &amp; Heating.</p>
        <p style="margin-top:14px;"><a href="tel:+18016853976" style="color:var(--ink); font-weight:600; font-family:var(--display); font-size:18px;">(801) 685-3976</a></p>
        <div class="footer-google-rating" id="footer-google-rating">
          <span class="fgr-stars">★★★★★</span>
          <span class="fgr-text"><strong id="fgr-rating">—</strong>/5 · <strong id="fgr-count">—</strong> Google reviews</span>
          <a id="fgr-link" href="https://www.google.com/maps/search/Utah+Boiler+Experts+Salt+Lake+City" target="_blank" rel="noopener" data-track="gbp_footer">Read on Google →</a>
        </div>
      </div>
      <div class="footer-col"><h5>Services</h5><ul><li><a href="/boiler-repair">Boiler repair</a></li><li><a href="/boiler-replacement">Boiler replacement</a></li><li><a href="/water-heater-repair">Water heater repair</a></li><li><a href="/radiant-floor-heating">Radiant floor heating</a></li><li><a href="/snow-melt-systems">Snow-melt systems</a></li><li><a href="/emergency-boiler-repair">Emergency repair</a></li></ul></div>
      <div class="footer-col"><h5>Service Areas</h5><ul><li><a href="/service-area/salt-lake-city">Salt Lake City</a></li><li><a href="/service-area/park-city">Park City</a></li><li><a href="/service-area/{slug}">{name}</a></li><li><a href="/service-area/sandy">Sandy</a></li><li><a href="/service-areas">All 26 cities →</a></li></ul></div>
      <div class="footer-col"><h5>Reach us</h5><ul><li><a href="tel:+18016853976">(801) 685-3976</a></li><li>Mon–Sat: 7am–7pm</li><li>24/7 emergency line</li><li><a href="https://www.facebook.com/TheOtherBuddy" target="_blank" rel="noopener">Facebook</a></li></ul></div>
    </div>
    <div class="footer-bottom"><span>© <span id="year">2026</span> The Other Buddy Plumbing &amp; Heating · DBA Utah Boiler Experts</span><span>Licensed · Bonded · Insured</span></div>
  </div>
</footer>

<a class="sticky-call" href="tel:+18016853976" aria-label="Call (801) 685-3976"><span>📞</span><span>Call (801) 685-3976</span></a>

<script>(function(){{'use strict';var y=document.getElementById('year');if(y)y.textContent=new Date().getFullYear();var nt=document.getElementById('nav-toggle'),pn=document.getElementById('primary-nav');if(nt&&pn){{nt.addEventListener('click',function(){{var o=pn.classList.toggle('open');nt.setAttribute('aria-expanded',o?'true':'false')}});pn.querySelectorAll('a').forEach(function(a){{a.addEventListener('click',function(){{pn.classList.remove('open');nt.setAttribute('aria-expanded','false')}})}})}}document.querySelectorAll('.faq-q').forEach(function(b){{b.addEventListener('click',function(){{var i=b.closest('.faq-item'),a=i.querySelector('.faq-a');if(i.classList.contains('open')){{i.classList.remove('open');a.style.maxHeight='0';b.setAttribute('aria-expanded','false')}}else{{i.classList.add('open');a.style.maxHeight=a.scrollHeight+'px';b.setAttribute('aria-expanded','true')}}}})}});}})();</script>

<script src="/js/conversions.js?v={JS_VER}" defer></script>
<script src="/js/header-scroll.js?v={JS_VER}" defer></script>
<script src="/js/reviews.js?v={JS_VER}" defer></script>
</body>
</html>
"""
    return html


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for city in CITIES:
        path = os.path.join(OUT_DIR, f"{city['slug']}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(render_city(city))
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
