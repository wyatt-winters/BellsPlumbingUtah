#!/usr/bin/env python3
"""Enable Google Ads call conversion tracking across HTML/PHP pages."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONVERSIONS_TAG = '<script src="/js/conversions.js?v=20260624" defer></script>'

GTAG_RE = re.compile(
    r"<script async src=\"https://www\.googletagmanager\.com/gtag/js\?id=G-DF82TDY0D7\"></script>\s*"
    r"<script>.*?</script>",
    re.DOTALL,
)

GTAG_NEW = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-DF82TDY0D7"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-DF82TDY0D7');
  gtag('config', 'AW-17966193749');
  gtag('config', 'AW-17966193749/qPGWCJ26mIMcENW4-fZC', {
    'phone_conversion_number': '(801) 685-3976'
  });
</script>"""

ANALYTICS_COMMENT_RE = re.compile(
    r"<!-- =+\s*\n\s*ANALYTICS / CONVERSION TRACKING.*?-->\s*",
    re.DOTALL,
)

ANALYTICS_COMMENT_NEW = """<!-- =====================================================================
     ANALYTICS / CONVERSION TRACKING — GA4 + Google Ads call conversions
     ===================================================================== -->
"""

CLICK_SCRIPT_RE = re.compile(
    r"\n?<script>\n\(function\(\){\n  ['\"]use strict['\"];.*?"
    r"click_location:.*?"
    r"\}\);\n    \}\);\n  \}\);\n\}\)\(\);\n</script>",
    re.DOTALL,
)


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    if "AW-17966193749" not in text:
        if ANALYTICS_COMMENT_RE.search(text):
            text = ANALYTICS_COMMENT_RE.sub(ANALYTICS_COMMENT_NEW, text, count=1)
        text = GTAG_RE.sub(GTAG_NEW, text, count=1)

    text = CLICK_SCRIPT_RE.sub("", text)

    if CONVERSIONS_TAG not in text and 'href="/js/conversions.js' not in text:
        if '<script src="/js/header-scroll.js' in text:
            text = text.replace(
                '<script src="/js/header-scroll.js',
                CONVERSIONS_TAG + "\n<script src=\"/js/header-scroll.js",
                1,
            )
        elif "</body>" in text:
            text = text.replace("</body>", CONVERSIONS_TAG + "\n</body>", 1)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed: list[str] = []
    for path in sorted(ROOT.rglob("*")):
        if path.suffix not in {".html", ".php"}:
            continue
        if "handlers" in path.parts:
            continue
        if patch_file(path):
            changed.append(str(path.relative_to(ROOT)))

    print(f"Updated {len(changed)} files:")
    for name in changed:
        print(f"  {name}")


if __name__ == "__main__":
    main()
