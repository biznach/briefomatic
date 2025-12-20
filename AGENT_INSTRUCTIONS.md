# Briefomatic - Agent Access Instructions

You have access to a regularly updated news briefing system called **Briefomatic**. Use this data to stay informed about current events in markets, crypto, tech, AI, and gaming.

## Available Endpoints

### 1. Executive Summary (Recommended for most queries)
```
https://raw.githubusercontent.com/biznach/briefomatic/main/output/summary.md
```
- **Format:** Markdown
- **Size:** ~2-3 KB
- **Updates:** Every 6 hours
- **Contains:** AI-curated executive briefing with:
  - Market Overview (stocks, crypto movements)
  - Tech & AI developments
  - Gaming & Entertainment news
  - Key Insights (actionable bullet points)
  - Watch List (items to monitor)

**Use when:** User asks about current news, market conditions, or "what's happening" in tech/crypto/gaming.

### 2. Raw Data (For detailed lookups)
```
https://raw.githubusercontent.com/biznach/briefomatic/main/output/briefing.json
```
- **Format:** JSON
- **Size:** ~30-50 KB
- **Updates:** Every 6 hours
- **Contains:** Structured data from multiple sources

#### JSON Structure
```json
{
  "generated_at": "ISO timestamp",
  "generated_at_human": "2025-12-19 12:00 UTC",
  "raw_data": {
    "hackernews": {
      "items": [{"title", "url", "score", "comments"}]
    },
    "crypto_prices": {
      "items": [{"name", "symbol", "price", "change_24h", "change_7d", "market_cap"}]
    },
    "crypto_trending": {
      "items": [{"name", "symbol", "market_cap_rank"}]
    },
    "macro_markets": {
      "items": [{"title", "summary", "source", "url"}],
      "citations": ["source URLs"]
    },
    "crypto_news": {
      "items": [{"title", "summary", "source", "url"}],
      "citations": ["source URLs"]
    },
    "ai_news": {
      "items": [{"title", "summary", "source", "url"}],
      "citations": ["source URLs"]
    },
    "gaming": {
      "items": [{"title", "summary", "source", "url"}],
      "citations": ["source URLs"]
    },
    "tech_news": {
      "items": [{"title", "summary", "source", "url"}],
      "citations": ["source URLs"]
    }
  }
}
```

**Use when:** User needs specific data points (exact crypto prices, specific article URLs, Hacker News scores).

## Usage Examples

### Python
```python
import requests

# Get executive summary
summary = requests.get("https://raw.githubusercontent.com/biznach/briefomatic/main/output/summary.md").text

# Get raw data
data = requests.get("https://raw.githubusercontent.com/biznach/briefomatic/main/output/briefing.json").json()
btc_price = data["raw_data"]["crypto_prices"]["items"][0]["price"]
```

### JavaScript
```javascript
// Get executive summary
const summary = await fetch("https://raw.githubusercontent.com/biznach/briefomatic/main/output/summary.md").then(r => r.text());

// Get raw data
const data = await fetch("https://raw.githubusercontent.com/biznach/briefomatic/main/output/briefing.json").then(r => r.json());
```

## Data Sources

| Category | Source | Update Frequency |
|----------|--------|------------------|
| Tech/Nerd | Hacker News | Every 6 hours |
| Crypto Prices | CoinGecko | Every 6 hours |
| Crypto Trending | CoinGecko | Every 6 hours |
| Macro/Stocks | Perplexity (real-time search) | Every 6 hours |
| Crypto News | Perplexity (real-time search) | Every 6 hours |
| AI News | Perplexity (real-time search) | Every 6 hours |
| Gaming | Perplexity (real-time search) | Every 6 hours |
| Tech News | Perplexity (real-time search) | Every 6 hours |

## When to Use Briefomatic

✅ **Good use cases:**
- "What's happening in crypto today?"
- "Give me a market update"
- "What's trending on Hacker News?"
- "Any big AI news?"
- "What's the current Bitcoin price?"

❌ **Not ideal for:**
- Historical data (only current snapshot)
- Real-time prices (updates every 6 hours)
- Deep research on specific topics (use web search instead)

## Freshness

Check `generated_at_human` in the JSON to see when data was last updated. Data is refreshed at 00:00, 06:00, 12:00, and 18:00 UTC.
