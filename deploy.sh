#!/bin/bash
# cPanel Git deploy hook — run after `git pull` in cPanel Git Version Control.
# Path: public_html/website_302faf96/deploy.sh (make executable: chmod +x deploy.sh)

set -euo pipefail
cd "$(dirname "$0")"

echo "[deploy] Waking blog bot..."
if [ -f blog/bot.php ]; then
  /usr/local/bin/php blog/bot.php || php blog/bot.php || true
fi

echo "[deploy] Done at $(date -Iseconds)"
