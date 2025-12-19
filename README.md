# Briefomatic

Automated daily briefing system for AI agents. Uses Perplexity for real-time news search and Venice AI for summarization.

## Data Sources

| Source | Category | API Key Required |
|--------|----------|------------------|
| Perplexity Sonar | Macro, Stocks, Crypto news, Gaming, Tech, AI | Yes |
| Hacker News | Tech, AI, Nerd community | No (free) |
| CoinGecko | Crypto prices & trends | No (free) |
| Venice AI | Summarization & filtering | Yes |

## How It Works

1. GitHub Actions runs on a schedule (every 6 hours by default)
2. Perplexity Sonar searches the web for current news across categories
3. CoinGecko provides precise crypto price data
4. Hacker News provides tech community signal
5. Venice AI summarizes and filters everything into an executive briefing
6. Outputs `briefing.json` and `briefing.md` to the `output/` directory

## Agent Access

Your agents can fetch the briefing with a simple HTTP GET:

```python
import requests

# JSON format (structured data + summary)
BRIEFING_URL = "https://raw.githubusercontent.com/biznach/briefomatic/main/output/briefing.json"
briefing = requests.get(BRIEFING_URL).json()

# Access the AI summary
print(briefing["summary"])

# Access raw data by category
print(briefing["raw_data"]["crypto_prices"])
print(briefing["raw_data"]["hackernews"])
print(briefing["raw_data"]["macro_markets"])
```

```javascript
// JavaScript/Node
const response = await fetch("https://raw.githubusercontent.com/biznach/briefomatic/main/output/briefing.json");
const briefing = await response.json();
console.log(briefing.summary);
```

## Setup

### 1. Get API Keys

| Service | Get Key At | Required |
|---------|------------|----------|
| Perplexity | [perplexity.ai](https://www.perplexity.ai/settings/api) | Yes |
| Venice AI | [venice.ai](https://venice.ai) | Yes |

### 2. Add GitHub Secrets

Go to your repo → Settings → Secrets and variables → Actions → New repository secret

Add these secrets:
- `PERPLEXITY_API_KEY` - For real-time news search
- `VENICE_API_KEY` - For AI summarization

### 3. Test the Workflow

1. Go to Actions tab in your repo
2. Click "Update Briefing"
3. Click "Run workflow"
4. Check the output in `output/briefing.json`

## Configuration

### Change Schedule

Edit `.github/workflows/update-briefing.yml`:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours (default)
  - cron: '0 * * * *'    # Every hour
  - cron: '0 8 * * *'    # Daily at 8am UTC
```

### Customize Crypto Watchlist

Edit `scripts/fetch_briefing.py`:

```python
briefing["raw_data"]["crypto_prices"] = fetch_crypto_prices(
    coins=["bitcoin", "ethereum", "solana", "your-coin-here"]
)
```

### Customize News Queries

Edit the Perplexity queries in `scripts/fetch_briefing.py`:

```python
briefing["raw_data"]["macro_markets"] = fetch_perplexity_news(
    perplexity_key,
    query="Your custom query here",
    category="macro_stocks",
    recency="day"  # Options: hour, day, week, month
)
```

### Change Perplexity Model

- `sonar` - Faster, cheaper (default)
- `sonar-pro` - More thorough, better for complex queries

## Output Format

### briefing.json

```json
{
  "generated_at": "2024-01-15T12:00:00+00:00",
  "generated_at_human": "2024-01-15 12:00 UTC",
  "raw_data": {
    "hackernews": { "items": [...] },
    "crypto_prices": { "items": [...] },
    "crypto_trending": { "items": [...] },
    "macro_markets": { "items": [...], "citations": [...] },
    "crypto_news": { "items": [...], "citations": [...] },
    "ai_news": { "items": [...], "citations": [...] },
    "gaming": { "items": [...], "citations": [...] },
    "tech_news": { "items": [...], "citations": [...] }
  },
  "summary": "AI-generated executive briefing..."
}
```

### briefing.md

Human-readable markdown version of the AI summary.

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export PERPLEXITY_API_KEY="your-key"
export VENICE_API_KEY="your-key"

# Run the script
python scripts/fetch_briefing.py
```

## Cost Estimate

Per run (every 6 hours = 4 runs/day):
- **Perplexity**: ~5 queries × $0.005 = ~$0.025/run
- **Venice AI**: ~1 summary = ~$0.01/run
- **Daily cost**: ~$0.14/day (~$4/month)

Free sources (Hacker News, CoinGecko) have no cost.

## License

MIT
