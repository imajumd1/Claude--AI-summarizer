# Product Scope: PM Agent — AI Assistant for IT Product Managers

## Project Overview

PM Agent is a Python CLI tool that gives a Product Manager an AI-powered thought partner for their day-to-day research, documentation, and prioritization work. Powered by Anthropic's Claude API with structured tool use (`beta_tool` + `tool_runner`), it connects the PM directly to their corpus of user research, live PRD documents, and product metrics — all through a natural-language conversation loop. Rather than a generic chatbot bolted onto documents, PM Agent acts as a domain-aware collaborator that can cite specific data points, make edits to PRDs with stated reasoning, and surface the "so what" behind the numbers. The initial implementation targets Jamie Rivera, a PM at a 312-person tech company building three IT tools (an asset tracker, a helpdesk platform, and an employee onboarding portal).

---

## Problem Statement

Product managers spend a disproportionate share of their time on information retrieval and synthesis rather than decision-making. A 2025 Productboard survey found that PMs save an average of four hours per task using AI — yet most AI tools are either too generic (ChatGPT) or too narrowly scoped (ChatPRD does only PRD writing; Dovetail does only research tagging). The result is a fragmented workflow: a PM doing research synthesis opens one tool, writes a PRD in another, checks metrics in a dashboard, and tries to hold the connections between all three in working memory.

For PMs building internal IT tools specifically, the problem is compounded: the audience is internal, the data is fragmented across MDM systems, helpdesk logs, and satisfaction surveys, and the PRDs are cross-referenced with compliance requirements (SOC2, SLA targets). No existing tool speaks that language.

**Who has this problem:** Any PM responsible for internal IT tooling — typically a solo PM or a team of 2–4 embedded in an IT organization — who needs to move fast between user research, spec-writing, and data review without context-switching between five different apps.

---

## Goals

1. **Research access in under 10 seconds** — A PM should be able to ask "what are IT admins most frustrated about?" and get a cited, synthesized answer (naming specific participants or percentages) within one round trip.
2. **PRD edits grounded in evidence** — Every `edit_prd` call must include a `reason` field; the agent should always explain which data point or interview motivated the change.
3. **Zero-setup conversation history** — The session maintains full multi-turn context so the PM can ask follow-up questions ("now do the same for the onboarding portal") without re-specifying context.
4. **Extensible tool surface** — Adding a new data source (e.g., Jira tickets, OKR tracker) requires only defining a new `@beta_tool` function — no changes to the conversation loop.
5. **Honest uncertainty** — The agent should flag when a question requires data it doesn't have, rather than hallucinating an answer from its training weights.

---

## Non-Goals

- **Real-time data integration** — The current implementation uses synthetic, in-memory data. Live sync with Jira, Confluence, Notion, or MDM systems is out of scope for v1.
- **Multi-user / team collaboration** — This is a single-PM CLI. Shared sessions, access control, or team dashboards are not in scope.
- **PRD persistence across sessions** — `edit_prd` changes are in-session only. Writing back to a document store (Confluence, Notion, Google Docs) is a future integration.
- **Autonomous agent operation** — PM Agent responds to explicit prompts; it does not proactively monitor metrics or alert the PM to changes. Push-style notifications are out of scope.
- **GUI or web interface** — This is a terminal CLI. A browser-based frontend is explicitly deferred.
- **General-purpose PM assistant** — PM Agent is scoped to IT tooling context. It is not a horizontal product management platform.

---

## Target Users

### Primary: The Solo IT PM (like Jamie Rivera)
- Owns 2–4 products simultaneously with limited engineering support
- Context-switches constantly between user research, spec writing, and stakeholder updates
- Comfortable with the terminal; not afraid of a CLI
- Frustrated that existing AI tools make them re-paste context every session
- Wants a tool that already knows their PRDs, research, and metrics — so they can ask questions, not manage prompts
- Success metric: spends less time hunting for data and more time making decisions

### Secondary: IT PM Leads / Directors
- Reviewing PRDs written by junior PMs, looking for evidence-backed prioritization
- Want to spot-check whether user stories map back to validated pain points
- Would use PM Agent to stress-test a spec ("does this problem statement match what we heard in research?")
- Less interested in editing; more interested in synthesis and gap analysis

---

## Key Features

### Must Have

- **`read_user_research` tool** — Retrieve interviews (filterable by segment: `it_admin`, `end_user`, `manager`), satisfaction surveys, and support ticket analysis; returns structured JSON the agent can reason over.
- **`get_prd` tool** — Fetch any of the three PRDs in full (asset tracker, helpdesk v2, onboarding portal) as structured JSON.
- **`edit_prd` tool** — Update specific PRD sections (`problem_statement`, `user_stories`, `success_metrics`, `requirements`, `out_of_scope`) with a mandatory `reason` field; changes persist for the session.
- **`analyze_data` tool** — Pull usage, satisfaction, adoption, support load, or performance metrics for a given time window (`last_week`, `last_month`, `last_quarter`, `last_year`).
- **Multi-turn conversation loop** — Full message history maintained across turns so the PM can ask follow-up questions without re-specifying context.
- **Graceful API error handling** — Handles `AuthenticationError`, `RateLimitError`, `APIConnectionError`, and `APIStatusError` without crashing; removes unanswered turns from history on failure.
- **`tool_runner` integration** — Uses Anthropic's beta `tool_runner` to automatically manage the tool call / tool result / response cycle without manual loop management.

### Nice to Have

- **Session export** — Save the conversation transcript and any PRD edits to a markdown file at session end.
- **Research diff mode** — After editing a PRD, show a before/after diff of the changed section.
- **Streaming output** — Stream the assistant's response token-by-token rather than waiting for the full response (better UX for long answers).
- **Configurable data sources** — Load user research and PRDs from YAML/JSON files at startup rather than hardcoded Python dicts, enabling real-world data without code changes.
- **`list_prds` and `list_research` tools** — Let the agent discover what's available without the PM needing to know exact names.
- **Slash commands** — `/prds`, `/research`, `/metrics` shortcuts to quickly pull common data without a full natural-language prompt.

---

## Technical Considerations

### Stack
- **Language:** Python 3.9+ (current deployment target, constrained by system Python on macOS)
- **AI SDK:** `anthropic` Python SDK v0.100.0+ with `beta_tool` decorator and `client.beta.messages.tool_runner()`
- **Model:** `claude-opus-4-7` — highest reasoning capability for synthesis tasks; appropriate given low request volume (one PM, interactive pace)
- **Data layer:** In-memory Python dicts (`_USER_RESEARCH`, `_PRDS_ORIGINAL`, `_METRICS`) with a session-scoped copy for edits (`_prd_state = json.loads(json.dumps(_PRDS_ORIGINAL))`)

### Key Architectural Decisions
- **`@beta_tool` decorator pattern** — Tools are defined as plain Python functions with type hints and docstrings; the SDK introspects them into the JSON schema Anthropic's API expects. This keeps tool definitions readable and avoids manual schema maintenance.
- **`tool_runner` loop** — Replaces manual `stop_reason == "tool_use"` polling. The runner iterates until the model returns a final text response, handling intermediate tool calls transparently.
- **Conversation history as plain dicts** — Only text turns are appended to `messages`; tool call/result rounds are handled internally by `tool_runner` and not stored in the PM's history. This keeps context window usage efficient.
- **Session-scoped PRD state** — Deep-copied at startup so edits don't mutate the original data, but do persist across turns within a session.

### Non-Functional Requirements
- **Latency:** Target < 15s end-to-end for a tool-calling turn on a standard broadband connection (Opus 4.7 is slower than Sonnet; acceptable for a single interactive user).
- **Security:** API key via `ANTHROPIC_API_KEY` environment variable only — never hardcoded. No sensitive data persisted to disk.
- **Reliability:** All four API error types caught and handled; the session survives transient failures without corrupting message history.
- **Extensibility:** New tools require only a new `@beta_tool`-decorated function added to the `tools=[...]` list in the `tool_runner` call — no other changes.

### Integrations (v1 — None Required)
All data is synthetic and self-contained. Future integrations that would make this production-ready:
- Confluence / Notion (PRD read/write)
- Jira / Linear (ticket data)
- Jamf / Intune (MDM asset data)
- Workday (HRIS for onboarding)
- Slack (push notifications on PRD edits)

---

## Competitors & Differentiation

| Tool | What It Does | Key Weakness vs. PM Agent |
|---|---|---|
| **ChatPRD** | PRD generation from templates, 100K+ PM users | No access to your actual research or metrics; generic output |
| **Notion AI** | Drafts and rewrites docs within Notion | Requires all data to live in Notion; no cross-source synthesis |
| **Dovetail** | AI-powered user research tagging and clustering | Research-only; no PRD editing or metrics; expensive ($400+/mo for teams) |
| **NotebookLM** | Cited Q&A over uploaded documents | Read-only; can't edit PRDs; no metrics; not PM-workflow-aware |
| **Lindy** | General-purpose AI personal assistant for PMs | No domain model; starts from scratch each session; no tool use |
| **GitHub Copilot / Claude Code** | Agentic coding assistant with file access | Built for engineers, not PMs; no product management data model |
| **Productboard / Amplitude** | Roadmapping and analytics platforms | Expensive, team-oriented; no natural-language interface for ad-hoc synthesis |

**PM Agent's differentiation:** It is the only tool that combines (1) a persistent domain model of your research, PRDs, and metrics, (2) evidence-grounded PRD editing with mandatory reasoning, (3) multi-turn conversation that retains context across a session, and (4) a fully extensible tool surface — all in a zero-setup CLI that runs locally. It is purpose-built for a single PM working across multiple IT products, not a team dashboard or a generic document editor.

---

## Open Questions

1. **Data persistence:** Should PRD edits write back to a file (e.g., `prds/*.json`) at session end, or remain ephemeral? Recommendation: add an optional `--save` flag that writes the final PRD state to JSON on exit.
2. **Model choice:** `claude-opus-4-7` maximizes quality but is the slowest and most expensive model. For a PM asking 20–30 questions per session, is `claude-sonnet-4-6` fast enough and sufficiently capable? Recommend A/B testing on real PM workflows before locking in.
3. **Real data migration:** What does the path from synthetic data to real data look like? Options: (a) load from JSON/YAML config files at startup, (b) build live connectors (Confluence, Jira), (c) hybrid (static snapshots refreshed nightly). Decision needed before any production deployment.
4. **Multi-PM support:** Is this a single-PM tool or should it eventually support a team sharing one agent with role-based data access? The current architecture is single-user by design — supporting teams would require auth, tenancy, and a persistent backend.
5. **Tool discovery:** As the tool surface grows, how does the PM know what to ask? Consider adding a `/help` command that lists available tools and example prompts, or a `list_capabilities` tool the model can call on ambiguous queries.
6. **Evaluation:** How do we know the agent is giving good answers? Consider adding an eval harness (a set of golden Q&A pairs against the synthetic data) to catch regressions when the model or tools change.

---

*Generated by Claude Code using research from [ChatPRD](https://www.chatprd.ai/learn/ai-for-product-managers), [prodmgmt.world](https://www.prodmgmt.world/blog/ai-for-product-managers), [Atomicwork ITSM](https://www.atomicwork.com/itsm/best-itsm-tools), [Anthropic Agent SDK Docs](https://platform.claude.com/docs/en/agent-sdk/overview), and [MindStudio AI Agents for PMs](https://www.mindstudio.ai/blog/ai-agents-for-product-managers). Last updated: May 2026.*
