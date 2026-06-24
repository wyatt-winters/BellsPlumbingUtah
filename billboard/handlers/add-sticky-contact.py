#!/usr/bin/env python3
"""Add sticky-contact.js sitewide and bump conversions.js cache version."""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STICKY = '<script src="/js/sticky-contact.js?v=20260627" defer></script>'
LEAD = '<script src="/js/lead-form.js?v=20260627" defer></script>'
CONVERSIONS_OLD = re.compile(r'/js/conversions\.js\?v=\d+')
CONVERSIONS_NEW = '/js/conversions.js?v=20260627'

LEAD_PAGES = {
    'boiler-repair.html',
    'boiler-replacement.html',
    'emergency-boiler-repair.html',
    'radiant-floor-heating-repair.html',
    'snow-melt-systems.html',
}

for dirpath, _, files in os.walk(ROOT):
    if '/.git' in dirpath or '/handlers' in dirpath:
        continue
    for name in files:
        if not name.endswith('.html'):
            continue
        path = os.path.join(dirpath, name)
        with open(path, encoding='utf-8') as f:
            content = f.read()

        if 'conversions.js' not in content:
            continue

        original = content
        content = CONVERSIONS_OLD.sub(CONVERSIONS_NEW, content)

        if STICKY not in content and 'sticky-call' in content:
            content = content.replace(
                f'<script src="{CONVERSIONS_NEW}" defer></script>',
                f'<script src="{CONVERSIONS_NEW}" defer></script>\n{STICKY}',
                1,
            )

        rel = os.path.relpath(path, ROOT)
        if rel.replace('\\', '/') in LEAD_PAGES and LEAD not in content:
            content = content.replace(
                f'<script src="{CONVERSIONS_NEW}" defer></script>',
                f'<script src="{CONVERSIONS_NEW}" defer></script>\n{LEAD}',
                1,
            )

        if content != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print('updated', rel)
