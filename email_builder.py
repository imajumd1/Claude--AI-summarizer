"""Build the HTML email from trend data."""

from trends_data import TRENDS, TODAY


def build_html() -> str:
    # Deduplicated ordered list of tags for the filter bar
    seen = []
    for t in TRENDS:
        if t["tag"] not in seen:
            seen.append(t["tag"])
    unique_tags = seen

    # ── Filter buttons (header) ───────────────────────────────────────────
    tag_buttons = """
    <button onclick="filter('all')" id="btn-all"
      style="display:inline-block;background:#ffffff22;color:#fff;
             border:1px solid #ffffff44;border-radius:20px;padding:5px 14px;
             font-size:11px;font-weight:700;margin:3px 4px;cursor:pointer;
             font-family:inherit;transition:all .2s;letter-spacing:.3px;">
      ✦ All
    </button>"""

    for tag in unique_tags:
        color = next(t["tag_color"] for t in TRENDS if t["tag"] == tag)
        safe  = tag.replace(" ", "-").replace("/", "-")
        tag_buttons += f"""
    <button onclick="filter('{safe}')" id="btn-{safe}"
      style="display:inline-block;background:{color}22;color:{color};
             border:1px solid {color}55;border-radius:20px;padding:5px 14px;
             font-size:11px;font-weight:700;margin:3px 4px;cursor:pointer;
             font-family:inherit;transition:all .2s;letter-spacing:.3px;">
      {tag}
    </button>"""

    # ── Trend cards ───────────────────────────────────────────────────────
    items_html = ""
    for t in TRENDS:
        safe = t["tag"].replace(" ", "-").replace("/", "-")
        items_html += f"""
      <div class="card" data-tag="{safe}" style="margin-bottom:20px;
          transition:opacity .25s ease,transform .25s ease;">
        <div style="background:#1E293B;border-radius:12px;overflow:hidden;
            border-left:4px solid {t['tag_color']};">
          <div style="padding:20px 24px;">

            <!-- Rank + tag -->
            <div style="margin-bottom:14px;">
              <span style="display:inline-block;width:32px;height:32px;line-height:32px;
                  text-align:center;background:{t['tag_color']};color:#fff;
                  border-radius:50%;font-size:14px;font-weight:800;margin-right:10px;
                  vertical-align:middle;">
                {t['rank']}
              </span>
              <span style="background:{t['tag_color']}22;color:{t['tag_color']};
                  border:1px solid {t['tag_color']}55;border-radius:20px;
                  padding:3px 10px;font-size:11px;font-weight:600;vertical-align:middle;">
                {t['tag']}
              </span>
            </div>

            <!-- Headline -->
            <h2 style="margin:0 0 10px 0;font-size:18px;font-weight:700;
                color:#F1F5F9;line-height:1.3;">
              {t['headline']}
            </h2>

            <!-- Summary -->
            <p style="margin:0 0 14px 0;font-size:14px;color:#94A3B8;line-height:1.7;">
              {t['summary']}
            </p>

            <!-- Why it matters -->
            <div style="background:#0F172A;border-radius:8px;padding:12px 16px;margin-bottom:16px;">
              <span style="color:{t['tag_color']};font-size:12px;font-weight:700;
                  text-transform:uppercase;letter-spacing:.5px;">
                💡 Why it matters
              </span>
              <p style="margin:6px 0 0 0;font-size:13px;color:#CBD5E1;
                  line-height:1.6;font-style:italic;">
                {t['why_it_matters']}
              </p>
            </div>

            <!-- Source link -->
            <a href="{t['source_url']}" target="_blank" style="
                display:inline-block;color:{t['tag_color']};font-size:12px;
                font-weight:600;text-decoration:none;
                border-bottom:1px solid {t['tag_color']}44;">
              🔗 {t['source_name']} →
            </a>

          </div>
        </div>
      </div>"""

    # ── JS filter logic ───────────────────────────────────────────────────
    js = """
  <script>
    function filter(tag) {
      var cards   = document.querySelectorAll('.card');
      var buttons = document.querySelectorAll('button[id^="btn-"]');
      var count   = 0;

      // Update cards
      cards.forEach(function(card) {
        if (tag === 'all' || card.dataset.tag === tag) {
          card.style.display   = 'block';
          card.style.opacity   = '1';
          card.style.transform = 'translateY(0)';
          count++;
        } else {
          card.style.opacity   = '0';
          card.style.transform = 'translateY(6px)';
          setTimeout(function(c){ c.style.display = 'none'; }(card), 220);
        }
      });

      // Update button active styles
      buttons.forEach(function(btn) {
        btn.style.boxShadow  = 'none';
        btn.style.transform  = 'scale(1)';
        btn.style.fontWeight = '700';
      });
      var active = document.getElementById('btn-' + tag);
      if (active) {
        active.style.boxShadow  = '0 0 0 2px #fff6, 0 4px 14px #0006';
        active.style.transform  = 'scale(1.08)';
      }

      // Update counter
      var el = document.getElementById('visible-count');
      if (el) el.textContent = count;
    }
  </script>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🤖 AI Trends — {TODAY}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: #0F172A;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      -webkit-font-smoothing: antialiased;
    }}
    a {{ color: inherit; }}
    button:hover {{ opacity: .85; transform: scale(1.05) !important; }}
    @media (max-width: 600px) {{
      .email-wrapper {{ padding: 10px !important; }}
      .header-title  {{ font-size: 26px !important; }}
    }}
  </style>
</head>
<body>
  <div class="email-wrapper" style="max-width:680px;margin:0 auto;padding:24px 16px;">

    <!-- ── HEADER ──────────────────────────────────────────────────────── -->
    <div style="background:linear-gradient(135deg,#1E3A5F 0%,#0F172A 100%);
        border-radius:16px;overflow:hidden;margin-bottom:20px;padding:36px 32px;">
      <p style="color:#60A5FA;font-size:12px;font-weight:700;letter-spacing:1.5px;
          text-transform:uppercase;margin-bottom:8px;">
        Daily Intelligence Briefing
      </p>
      <h1 class="header-title" style="color:#F1F5F9;font-size:32px;font-weight:800;
          line-height:1.2;margin-bottom:12px;">
        🤖 Top 10 AI Trends
      </h1>
      <p style="color:#94A3B8;font-size:15px;line-height:1.5;">
        {TODAY} &nbsp;·&nbsp; Delivered at 7:00 AM PST &nbsp;·&nbsp;
        <span id="visible-count">10</span> stories
      </p>

      <!-- Filter buttons -->
      <div style="margin-top:20px;">
        <p style="color:#64748B;font-size:10px;font-weight:700;letter-spacing:1px;
            text-transform:uppercase;margin-bottom:10px;">
          Filter by category
        </p>
        {tag_buttons}
      </div>
    </div>

    <!-- ── QUICK STATS BAR ──────────────────────────────────────────────── -->
    <div style="background:#1E293B;border-radius:12px;margin-bottom:20px;
        display:flex;overflow:hidden;">
      <div style="flex:1;padding:16px;text-align:center;border-right:1px solid #334155;">
        <div style="color:#60A5FA;font-size:22px;font-weight:800;">10</div>
        <div style="color:#64748B;font-size:11px;margin-top:2px;">Trends Today</div>
      </div>
      <div style="flex:1;padding:16px;text-align:center;border-right:1px solid #334155;">
        <div style="color:#4ADE80;font-size:22px;font-weight:800;">8</div>
        <div style="color:#64748B;font-size:11px;margin-top:2px;">Sources Searched</div>
      </div>
      <div style="flex:1;padding:16px;text-align:center;border-right:1px solid #334155;">
        <div style="color:#FBBF24;font-size:22px;font-weight:800;">3m</div>
        <div style="color:#64748B;font-size:11px;margin-top:2px;">Read Time</div>
      </div>
      <div style="flex:1;padding:16px;text-align:center;">
        <div style="color:#F87171;font-size:22px;font-weight:800;">24h</div>
        <div style="color:#64748B;font-size:11px;margin-top:2px;">News Window</div>
      </div>
    </div>

    <!-- ── TREND CARDS ──────────────────────────────────────────────────── -->
    <div id="cards-container">
      {items_html}
    </div>

    <!-- ── FOOTER ───────────────────────────────────────────────────────── -->
    <div style="background:#1E293B;border-radius:12px;margin-top:8px;padding:20px 24px;
        text-align:center;">
      <p style="color:#475569;font-size:12px;line-height:1.8;">
        AI Trends Daily Digest &nbsp;·&nbsp; Prototype v1.0 &nbsp;·&nbsp; Synthetic Data<br>
        Delivered every morning at <strong style="color:#60A5FA;">7:00 AM PST</strong>
        via Anthropic Claude + Web Search<br>
        <a href="#" style="color:#475569;text-decoration:underline;">Unsubscribe</a>
        &nbsp;·&nbsp;
        <a href="#" style="color:#475569;text-decoration:underline;">Change preferences</a>
      </p>
    </div>

  </div>

  {js}
</body>
</html>"""
    return html
