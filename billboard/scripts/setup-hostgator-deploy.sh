#!/usr/bin/env bash
# One-time setup: GitHub repo + HostGator FTP secrets + first push.
# Usage: ./scripts/setup-hostgator-deploy.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
REPO_NAME="utah-boiler-experts"

if ! command -v gh >/dev/null; then
  echo "Install GitHub CLI: brew install gh"
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "Log into GitHub (browser will open)..."
  gh auth login -h github.com -p https -w
fi

GITHUB_USER="$(gh api user -q .login)"
echo "GitHub user: $GITHUB_USER"
REPO="$GITHUB_USER/$REPO_NAME"

echo ""
echo "HostGator FTP credentials (cPanel → FTP Accounts → saddleupbillboard@bellsplumbingutah.com):"
read -r -p "FTP server [192.254.188.195]: " FTP_SERVER
FTP_SERVER="${FTP_SERVER:-192.254.188.195}"
read -r -p "FTP username [saddleupbillboard@bellsplumbingutah.com]: " FTP_USERNAME
FTP_USERNAME="${FTP_USERNAME:-saddleupbillboard@bellsplumbingutah.com}"
read -r -s -p "FTP password: " FTP_PASSWORD
echo ""

# Domain FTP accounts are chrooted to website_f9f5f795 — always deploy to /, never full path.
FTP_SERVER_DIR="/"

gh secret set FTP_SERVER -b "$FTP_SERVER" -R "$REPO"
gh secret set FTP_USERNAME -b "$FTP_USERNAME" -R "$REPO"
gh secret set FTP_PASSWORD -b "$FTP_PASSWORD" -R "$REPO"
gh variable set FTP_SERVER_DIR "$FTP_SERVER_DIR" -R "$REPO"

echo ""
echo "Setup complete."
echo "Repo: https://github.com/$REPO"
echo "Deploy folder: / (chroot root = /home1/agentors/public_html/website_f9f5f795)"
echo "Triggering deploy..."
gh workflow run "Deploy to HostGator" -R "$REPO" || true
gh run list -R "$REPO" -L 3
