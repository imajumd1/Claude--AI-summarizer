"""
AI Trends Daily Digest — Prototype Runner
------------------------------------------
Generates the HTML email and opens it in your browser.
Run:  python3 run.py
"""

import os
import sys
import webbrowser
import subprocess
from datetime import datetime
from email_builder import build_html
from trends_data import TRENDS, TODAY

OUT_FILE = os.path.join(os.path.dirname(__file__), "email_preview.html")

# ── Terminal banner ───────────────────────────────────────────────────────────
def banner():
    print()
    print("  ┌─────────────────────────────────────────────────────┐")
    print("  │         🤖  AI Trends Daily Digest  —  v1.0         │")
    print("  │             Prototype with Synthetic Data            │")
    print("  └─────────────────────────────────────────────────────┘")
    print()

# ── Simulated fetch step ──────────────────────────────────────────────────────
def simulate_fetch():
    sources = [
        "OpenAI Blog", "DeepMind / Nature", "Anthropic Blog",
        "Meta AI", "The Verge", "Stanford HAI", "Reuters",
        "TechCrunch", "VentureBeat", "Hacker News",
    ]
    print(f"  📅  {TODAY}")
    print(f"  🕖  Triggered at 7:00 AM PST\n")
    print("  [1/4] Fetching AI news from sources...")
    for src in sources:
        print(f"        ✓  {src}")

    print()
    print(f"  [2/4] Ranking & deduplicating stories...")
    print(f"        ✓  47 candidate articles fetched")
    print(f"        ✓  Deduplication: 47 → 18 unique topics")
    print(f"        ✓  Top 10 selected by relevance + recency")

    print()
    print("  [3/4] Summarising trends via Claude API...")
    for t in TRENDS:
        print(f"        ✓  #{t['rank']}  {t['headline'][:55]}...")

    print()
    print("  [4/4] Building HTML email...")
    print("        ✓  Email composed (10 trend cards)")
    print("        ✓  Plain-text fallback generated")
    print()

# ── Print terminal digest ─────────────────────────────────────────────────────
def print_digest():
    print("  ─────────────────────────────────────────────────────")
    print("  📨  EMAIL PREVIEW (terminal)")
    print("  ─────────────────────────────────────────────────────")
    print(f"  Subject: 🤖 AI Trends — {TODAY}")
    print(f"  To:      you@yourdomain.com")
    print()
    for t in TRENDS:
        print(f"  #{t['rank']:02d}  [{t['tag']}]  {t['headline']}")
        print(f"       {t['why_it_matters'][:75]}...")
        print(f"       🔗 {t['source_name']}")
        print()

# ── Save & open HTML ─────────────────────────────────────────────────────────
def open_browser():
    html = build_html()
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✅  HTML email saved → {OUT_FILE}")
    print()
    print("  Opening in browser...")
    webbrowser.open(f"file://{os.path.abspath(OUT_FILE)}")
    print()

# ── Scheduler simulation ──────────────────────────────────────────────────────
def print_schedule_info():
    print("  ─────────────────────────────────────────────────────")
    print("  ⏰  SCHEDULER (GitHub Actions cron)")
    print("  ─────────────────────────────────────────────────────")
    print()
    print("  Cron expression:  0 15 * * *  (7:00 AM PST = 15:00 UTC)")
    print()
    print("  .github/workflows/ai_trends.yml  ──────────────────")
    print("""
  name: AI Trends Daily Digest
  on:
    schedule:
      - cron: '0 15 * * *'   # 7:00 AM PST every day
    workflow_dispatch:         # allow manual trigger

  jobs:
    send-digest:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-python@v5
          with: { python-version: '3.11' }
        - run: pip install anthropic sendgrid python-dotenv
        - run: python run.py --send
          env:
            ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
            SENDGRID_API_KEY:  ${{ secrets.SENDGRID_API_KEY }}
            TO_EMAIL:          ${{ secrets.TO_EMAIL }}
  """)
    print("  ─────────────────────────────────────────────────────")
    print()

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    banner()
    simulate_fetch()
    print_digest()
    open_browser()
    print_schedule_info()
    print("  Done! Check your browser for the full email preview. 🚀")
    print()
