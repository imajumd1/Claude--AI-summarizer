# Product Requirements Document
## AI Trends Daily Digest

**Version:** 1.0  
**Date:** 2026-05-27  
**Status:** Draft  
**Author:** Ishita Majumdar

---

## 1. Overview

### 1.1 Product Summary
AI Trends Daily Digest is an automated intelligence service that fetches the top 10 AI trends from the internet every morning at 7:00 AM PST and delivers a curated, human-readable email summary directly to the user's inbox.

### 1.2 Problem Statement
The AI space moves faster than any individual can track. Staying current requires manually checking multiple sources — news sites, research blogs, LinkedIn, Reddit, arXiv — every day. This is time-consuming, inconsistent, and easy to skip. There is no single automated tool that aggregates, ranks, and summarizes the most relevant AI developments into a concise daily briefing.

### 1.3 Solution
A scheduled agent that runs every morning, searches across trusted AI news sources, ranks the top 10 trending topics by relevance and recency, and delivers a clean, scannable email summary — before the user's workday begins.

### 1.4 Target User
- AI practitioners, researchers, and engineers
- Product managers and executives building AI-powered products
- Investors and consultants tracking the AI landscape
- Anyone who wants to stay informed on AI without spending time searching

---

## 2. Goals & Success Metrics

### 2.1 Goals
| Goal | Description |
|------|-------------|
| Automate discovery | Eliminate daily manual searching across AI news sources |
| Deliver on time | Email arrives at 7:00 AM PST every day, reliably |
| Stay relevant | Trends reflect what's actually happening in the last 24 hours |
| Be readable | Summary is scannable in under 3 minutes |

### 2.2 Success Metrics
| Metric | Target |
|--------|--------|
| Email delivery reliability | ≥ 99% on-time delivery |
| Trend relevance (user rating) | ≥ 4/5 avg rating after 30 days |
| Time to read summary | < 3 minutes |
| Open rate | ≥ 70% within 2 hours of delivery |
| User retention (30-day) | ≥ 85% continue using after first week |

---

## 3. Features & Requirements

### 3.1 Core Features

#### F1 — Scheduled Web Fetch (Daily at 7:00 AM PST)
- A cron job triggers the agent every day at 07:00 PST (15:00 UTC)
- The agent searches the web for AI news published in the last 24 hours
- Sources include: TechCrunch, VentureBeat, The Verge, arXiv, Hacker News, MIT Technology Review, Google AI Blog, OpenAI Blog, Anthropic Blog, Reddit r/MachineLearning

#### F2 — Trend Ranking & Deduplication
- Agent fetches at least 30–50 candidate stories/topics
- Stories are ranked by a combination of: recency, source authority, engagement signals (upvotes, shares), and novelty
- Duplicate or near-duplicate topics are deduplicated (e.g., multiple articles on the same GPT release are merged into one trend)
- Final output: exactly 10 distinct trends, ranked 1–10

#### F3 — AI-Powered Summarization
- Each trend is summarized in 2–3 sentences: what happened, why it matters, who it affects
- Summaries are written in plain English — no jargon, no filler
- A one-line "Why this matters" is appended to each item

#### F4 — Email Delivery
- Email is sent to the user's configured address via SMTP or a transactional email provider (e.g., SendGrid, Gmail API)
- Subject line format: `🤖 AI Trends — [Weekday], [Date]` (e.g., `🤖 AI Trends — Wednesday, May 27`)
- Email is HTML-formatted with a clean, readable layout
- Each trend includes: rank number, headline, 2–3 sentence summary, source link, and "Why it matters" line
- Plain-text fallback included for email clients that don't render HTML

#### F5 — Configuration
- User can configure: recipient email address, timezone (default PST), number of trends (default 10), topic filters (e.g., "focus on LLMs and agents")
- Configuration stored in a local `.env` or `config.yaml` file

---

### 3.2 Requirements

#### Functional Requirements
| ID | Requirement |
|----|-------------|
| FR-01 | System shall trigger automatically at 07:00 PST every day |
| FR-02 | System shall search at least 5 distinct sources per run |
| FR-03 | System shall return exactly 10 trends per email |
| FR-04 | Each trend summary shall be 2–3 sentences maximum |
| FR-05 | Email shall include a clickable link to each source article |
| FR-06 | System shall deduplicate stories covering the same topic |
| FR-07 | System shall send email within 10 minutes of 07:00 PST trigger |
| FR-08 | System shall log each run (timestamp, sources searched, trends selected, delivery status) |
| FR-09 | System shall send an alert email if a run fails |

#### Non-Functional Requirements
| ID | Requirement |
|----|-------------|
| NFR-01 | Delivery latency ≤ 10 minutes from trigger time |
| NFR-02 | System shall run on a cloud scheduler (e.g., cron, GitHub Actions, AWS EventBridge) |
| NFR-03 | No user action required to receive the email — fully automated |
| NFR-04 | Email renders correctly on Gmail, Outlook, and Apple Mail |
| NFR-05 | Source fetching shall respect robots.txt and rate limits |
| NFR-06 | API keys and credentials stored in environment variables, never in code |

---

## 4. User Flow

```
[07:00 AM PST — Scheduler Triggers]
         │
         ▼
[Agent fetches AI news from web sources]
         │
         ▼
[Stories ranked by recency + relevance + engagement]
         │
         ▼
[Top 30–50 stories deduplicated → top 10 selected]
         │
         ▼
[Claude API summarizes each trend in 2–3 sentences]
         │
         ▼
[Email composed as HTML with ranked list]
         │
         ▼
[Email delivered to user inbox]
         │
         ▼
[Run logged — success or failure alert sent]
```

---

## 5. Email Design

### 5.1 Subject Line
```
🤖 AI Trends — Wednesday, May 27
```

### 5.2 Email Structure
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🤖 AI Trends Daily Digest
  Wednesday, May 27 · Top 10 Stories
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#1  [Headline of Trend 1]
    [2–3 sentence summary]
    💡 Why it matters: [one line]
    🔗 Source: [link]

#2  [Headline of Trend 2]
    ...

...

#10 [Headline of Trend 10]
    ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Delivered by AI Trends Digest · Unsubscribe
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 6. Technical Architecture

### 6.1 Components
| Component | Technology |
|-----------|------------|
| Scheduler | GitHub Actions cron / AWS EventBridge / macOS `launchd` |
| Web Fetcher | Python + `requests` + Claude `web_search` tool |
| Summarizer | Claude API (`claude-opus-4-7`) with `web_search` tool |
| Email Sender | SendGrid API or Gmail SMTP |
| Config | `.env` file + `python-dotenv` |
| Logging | Local log file + optional email alert on failure |

### 6.2 Tech Stack
- **Language:** Python 3.11+
- **AI:** Anthropic Claude API (`claude-opus-4-7`) with web search tool
- **Email:** SendGrid (recommended) or Gmail SMTP
- **Scheduling:** GitHub Actions (recommended for zero-infra) or cron
- **Dependencies:** `anthropic`, `requests`, `python-dotenv`, `sendgrid` (or `smtplib`)

### 6.3 Data Flow
```
Scheduler → Python Script → Claude API (web_search) → Summarization → Email API → Inbox
```

---

## 7. Out of Scope (v1.0)

| Feature | Reason Deferred |
|---------|-----------------|
| Web UI / dashboard | Not needed for v1 — email is the interface |
| Multi-user support | Single user initially |
| User feedback loop (thumbs up/down per trend) | v2 feature |
| Topic personalization via ML | Manual config filter sufficient for v1 |
| Slack / Teams delivery | v2 channel expansion |
| Weekly digest mode | v2 |
| Source subscription management (add/remove sources) | v2 |

---

## 8. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Web search returns stale/irrelevant results | Medium | High | Use date filters in search queries; validate recency |
| Email delivery failure | Low | High | Retry logic + failure alert to backup email |
| Scheduler misfire (no run) | Low | Medium | Monitoring alert if no log entry by 07:15 PST |
| Duplicate trends in output | Medium | Low | Deduplication step with topic clustering |
| API rate limits exceeded | Low | Medium | Error handling + exponential backoff |
| Source website blocks scraping | Medium | Low | Use web_search tool (doesn't scrape directly) |

---

## 9. Milestones

| Milestone | Deliverable | Target |
|-----------|-------------|--------|
| M1 | Working agent that fetches + summarizes 10 trends | Week 1 |
| M2 | Email delivery working (HTML formatted) | Week 1 |
| M3 | Scheduler set up and tested (GitHub Actions) | Week 2 |
| M4 | Logging + failure alerts | Week 2 |
| M5 | Config file for email, timezone, topic filters | Week 2 |
| M6 | 7-day run validation (reliability + relevance check) | Week 3 |

---

## 10. Open Questions

| # | Question | Owner | Due |
|---|----------|-------|-----|
| 1 | Which email provider — SendGrid or Gmail SMTP? | Ishita | Before M2 |
| 2 | Which scheduler — GitHub Actions or local cron? | Ishita | Before M3 |
| 3 | Should topic filters be keywords or categories? | Ishita | Before M5 |
| 4 | Should failed runs retry, and how many times? | Ishita | Before M4 |
| 5 | Any specific sources to include or exclude? | Ishita | Before M1 |
