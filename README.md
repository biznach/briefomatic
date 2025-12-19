# Briefomatic

Automated daily briefing system for AI agents. Aggregates news from multiple sources and uses Venice AI to create summarized briefings.

## Data Sources

| Source | Category | API Key Required |
|--------|----------|------------------|
| Hacker News | Tech, AI, Nerd | No (free) |
| CoinGecko | Crypto prices & trends | No (free) |
| Alpha Vantage | Stocks, Macro, Sentiment | Yes (free tier) |
| NewsAPI | Gaming, AI news | Yes (free tier) |
| Venice AI | Summarization | Yes |

## How It Works

1. GitHub Actions runs on a schedule (every 6 hours by default)
2. Python script fetches data from all configured APIs
3. Venice AI summarizes and filters the raw data
4. Outputs `briefing.json` and `briefing.md` to the `output/` directory
5. Commits and pushes the updated briefing

## Agent Access

Your agents can fetch the briefing with a simple HTTP GET:

```python
import requests

# JSON format (structured data + summary)
BRIEFING_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/briefomatic/main/output/briefing.json"
briefing = requests.get(BRIEFING_URL).json()

# Access the AI summary
print(briefing["summary"])

# Access raw data by category
print(briefing["raw_data"]["crypto_prices"])
print(briefing["raw_data"]["hackernews"])
```

```javascript
// JavaScript/Node
const response = await fetch("https://raw.githubusercontent.com/YOUR_USERNAME/briefomatic/main/output/briefing.json");
const briefing = await response.json();
console.log(briefing.summary);
```

## Setup

### 1. Get API Keys

| Service | Get Key At | Required |
|---------|------------|----------|
| Venice AI | [venice.ai](https://venice.ai) | Yes |
| Alpha Vantage | [alphavantage.co](https://www.alphavantage.co/support/#api-key) | Optional |
| NewsAPI | [newsapi.org](https://newsapi.org/register) | Optional |

### 2. Add GitHub Secrets

Go to your repo → Settings → Secrets and variables → Actions → New repository secret

Add these secrets:
- `VENICE_API_KEY` - Required for AI summarization
- `ALPHAVANTAGE_API_KEY` - Optional, for stocks/macro news
- `NEWSAPI_KEY` - Optional, for gaming/AI news

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

Edit the NewsAPI queries in `scripts/fetch_briefing.py`:

```python
briefing["raw_data"]["gaming"] = fetch_newsapi(
    newsapi_key,
    query="your custom query here",
    category="gaming"
)
```

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
    "market_news": { "items": [...] },
    "gaming": { "items": [...] },
    "ai_news": { "items": [...] }
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
export VENICE_API_KEY="your-key"
export ALPHAVANTAGE_API_KEY="your-key"  # optional
export NEWSAPI_KEY="your-key"  # optional

# Run the script
python scripts/fetch_briefing.py
```

## License

MIT
