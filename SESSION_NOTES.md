# Briefomatic - Session Progress

## What We Built

**Briefomatic** - An automated daily briefing system for AI agents.

**Repo:** https://github.com/biznach/briefomatic

## Current State (Working)

### Data Flow
```
GitHub Actions (every 6 hours)
    ↓
Perplexity API → News (macro, crypto, AI, gaming, tech)
CoinGecko API → Crypto prices & trending
Hacker News API → Tech community signal
    ↓
Venice AI → Summarizes everything
    ↓
Output:
  - briefing.json (raw data only)
  - summary.md (executive summary only)
```

### Files Structure
```
briefomatic/
├── .github/workflows/update-briefing.yml  # Runs every 6 hours
├── scripts/fetch_briefing.py              # Main script
├── output/
│   ├── briefing.json                      # Raw data for agents
│   └── summary.md                         # Executive summary
├── run_local.py                           # Local testing runner
├── .env                                   # API keys (gitignored)
├── .env.example                           # Template for API keys
├── AGENT_INSTRUCTIONS.md                  # How agents access the data
└── README.md
```

### Agent Access URLs
- **Summary:** `https://raw.githubusercontent.com/biznach/briefomatic/main/output/summary.md`
- **Raw JSON:** `https://raw.githubusercontent.com/biznach/briefomatic/main/output/briefing.json`

### API Keys Configured
- GitHub Secrets: PERPLEXITY_API_KEY, VENICE_API_KEY
- Local .env: Same keys for local testing

## Next Steps (MCP Server)

We discussed building an MCP server version with tools like:
- `get_summary()` - Returns executive summary
- `get_briefing()` - Returns full JSON
- `get_crypto_prices()` - Returns just crypto data
- `get_news(category)` - Returns news for specific category

Options:
1. **Simple fetch MCP** - Wraps GitHub URLs
2. **Full MCP server** - Runs locally, can refresh on-demand

## To Resume

Just say: "Let's continue with the Briefomatic MCP server" and I'll pick up from here.

## Local Testing

```bash
cd C:\Users\bizfu\Documents\AI\briefomatic
.\venv\Scripts\python run_local.py
```
