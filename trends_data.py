"""Synthetic AI trends data simulating a real morning fetch."""

from datetime import date

TODAY = date.today().strftime("%A, %B %d, %Y")

TRENDS = [
    {
        "rank": 1,
        "headline": "OpenAI Releases GPT-5 with Native Multimodal Reasoning",
        "summary": (
            "OpenAI announced GPT-5, capable of seamlessly reasoning across text, images, audio, "
            "and video in a single context window. Early benchmarks show a 40% improvement over "
            "GPT-4o on complex multi-step reasoning tasks. The model is now available via API "
            "with a phased rollout to ChatGPT users starting this week."
        ),
        "why_it_matters": "GPT-5 sets a new baseline for frontier models — every AI product roadmap needs a reassessment.",
        "source_name": "OpenAI Blog",
        "source_url": "https://openai.com/blog",
        "tag": "Model Release",
        "tag_color": "#7C3AED",
    },
    {
        "rank": 2,
        "headline": "Google DeepMind's AlphaFold 3 Predicts Drug-Protein Interactions",
        "summary": (
            "DeepMind published AlphaFold 3, extending its protein-folding breakthrough to predict "
            "how small molecules, DNA, and RNA interact with proteins. Pharmaceutical companies are "
            "already using the model to cut early-stage drug discovery timelines from years to weeks. "
            "The model is available via a research access program."
        ),
        "why_it_matters": "AI is now accelerating drug discovery at a pace that could reshape the pharmaceutical industry within a decade.",
        "source_name": "Nature / DeepMind",
        "source_url": "https://deepmind.google",
        "tag": "Research",
        "tag_color": "#059669",
    },
    {
        "rank": 3,
        "headline": "Anthropic Launches Claude for Enterprise with SOC 2 Compliance",
        "summary": (
            "Anthropic released Claude for Enterprise, adding SSO, audit logs, data residency controls, "
            "and SOC 2 Type II compliance. The offering targets regulated industries — finance, healthcare, "
            "and legal — that have been blocked from adopting AI due to data governance requirements. "
            "Pricing is seat-based with volume discounts."
        ),
        "why_it_matters": "Enterprise compliance unlocks a massive wave of AI adoption in industries that have been waiting on the sidelines.",
        "source_name": "Anthropic Blog",
        "source_url": "https://anthropic.com",
        "tag": "Product Launch",
        "tag_color": "#D97706",
    },
    {
        "rank": 4,
        "headline": "Meta Releases Llama 4 with 1M Token Context Window — Open Source",
        "summary": (
            "Meta open-sourced Llama 4 with a 1-million-token context window and performance rivalling "
            "proprietary models on coding and reasoning benchmarks. The weights are freely downloadable "
            "under a commercial license. Developers are already fine-tuning it for domain-specific tasks "
            "at a fraction of the cost of API-based alternatives."
        ),
        "why_it_matters": "A free, commercially-licensed frontier model fundamentally changes the cost structure of AI-powered applications.",
        "source_name": "Meta AI",
        "source_url": "https://ai.meta.com",
        "tag": "Open Source",
        "tag_color": "#2563EB",
    },
    {
        "rank": 5,
        "headline": "Microsoft Copilot Now Embedded in Every Windows 11 App",
        "summary": (
            "Microsoft pushed an OS-level update embedding Copilot across Notepad, Paint, File Explorer, "
            "and the Windows taskbar. Users can invoke AI assistance anywhere with a keyboard shortcut. "
            "The update reaches 400 million Windows 11 devices over the next 30 days. Enterprise admins "
            "can disable it via Group Policy."
        ),
        "why_it_matters": "AI is becoming ambient infrastructure — the question is no longer whether users will interact with AI, but how often.",
        "source_name": "The Verge",
        "source_url": "https://theverge.com",
        "tag": "Big Tech",
        "tag_color": "#0284C7",
    },
    {
        "rank": 6,
        "headline": "Stanford HAI Report: AI Agents Outperform Humans on 60% of Knowledge Work Tasks",
        "summary": (
            "Stanford's Human-Centered AI Institute published its 2026 AI Index, finding that agentic AI "
            "systems now outperform median human workers on 60% of knowledge work benchmarks — up from "
            "34% in 2024. The report highlights coding, data analysis, and document summarisation as "
            "the highest-impact areas. It also flags rising concerns around AI-generated misinformation."
        ),
        "why_it_matters": "The automation frontier is moving faster than policy or workforce training can keep up — a signal for every business leader.",
        "source_name": "Stanford HAI",
        "source_url": "https://hai.stanford.edu",
        "tag": "Research",
        "tag_color": "#059669",
    },
    {
        "rank": 7,
        "headline": "EU AI Act Enforcement Begins — First Fines Issued to High-Risk Deployments",
        "summary": (
            "The European AI Act entered its enforcement phase, with regulators issuing the first fines "
            "to three companies deploying AI in hiring and credit scoring without required transparency "
            "disclosures. Penalties range from €500K to €2M. Legal teams across the EU are scrambling "
            "to complete AI system audits ahead of upcoming deadlines."
        ),
        "why_it_matters": "Regulatory risk is now real and measurable — AI compliance is no longer optional for EU-market companies.",
        "source_name": "Reuters",
        "source_url": "https://reuters.com",
        "tag": "Policy",
        "tag_color": "#DC2626",
    },
    {
        "rank": 8,
        "headline": "Mistral Releases 'Le Chat Pro' — A Fully Local AI Assistant for Mac",
        "summary": (
            "Mistral launched Le Chat Pro, a privacy-first AI assistant that runs entirely on-device on "
            "Apple Silicon Macs with no data leaving the machine. It supports 128K context, tool use, "
            "and RAG over local documents. The app costs $9.99/month and is already topping the Mac "
            "App Store productivity charts."
        ),
        "why_it_matters": "On-device AI is maturing fast — privacy-sensitive users now have a credible alternative to cloud-based assistants.",
        "source_name": "TechCrunch",
        "source_url": "https://techcrunch.com",
        "tag": "Product Launch",
        "tag_color": "#D97706",
    },
    {
        "rank": 9,
        "headline": "NVIDIA Blackwell Ultra GPU Ships — 3x Performance Gain for LLM Inference",
        "summary": (
            "NVIDIA began shipping the Blackwell Ultra GPU, delivering a 3x throughput improvement over "
            "Hopper for large language model inference at lower power consumption. Cloud providers are "
            "fast-tracking data centre upgrades. Analysts expect the hardware wave to compress inference "
            "costs by 50% within 18 months, making AI APIs significantly cheaper."
        ),
        "why_it_matters": "Cheaper inference means more AI features become economically viable — the cost floor for AI products is dropping fast.",
        "source_name": "VentureBeat",
        "source_url": "https://venturebeat.com",
        "tag": "Hardware",
        "tag_color": "#7C3AED",
    },
    {
        "rank": 10,
        "headline": "Y Combinator W26 Batch: 45% of Startups Are 'AI-Native' with <5 Employees",
        "summary": (
            "Y Combinator's Winter 2026 batch revealed that 45% of funded startups are AI-native — "
            "defined as companies where AI does the core work, not just assists it. The median team "
            "size is 4 people. Partners noted that AI is enabling founder pairs to build what once "
            "required 20-person engineering teams, fundamentally changing startup economics."
        ),
        "why_it_matters": "The era of the two-person unicorn is beginning — AI is collapsing the cost of building software companies.",
        "source_name": "Hacker News / YC",
        "source_url": "https://news.ycombinator.com",
        "tag": "Startups",
        "tag_color": "#EA580C",
    },
]
