# Briefomatic

Automated daily briefing system for AI agents.

## How It Works

1. GitHub Actions runs on a schedule (configurable)
2. Python script fetches data from configured APIs
3. Outputs `briefing.json` to the `output/` directory
4. Commits and pushes the updated briefing
5. Your agents fetch the raw file via HTTP

## Agent Access

```python
import requests

BRIEFING_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/briefomatic/main/output/briefing.json"
briefing = requests.get(BRIEFING_URL).json()
```

## Setup

1. Clone this repo
2. Add your API keys as GitHub Secrets (Settings → Secrets → Actions)
3. Configure data sources in `scripts/fetch_briefing.py`
4. Adjust schedule in `.github/workflows/update-briefing.yml`

## Configuration

### Schedule

Edit the cron expression in `.github/workflows/update-briefing.yml`:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
```

### Secrets

Add these in GitHub repo settings → Secrets → Actions:
- `NEWS_API_KEY` (if using NewsAPI)
- `TWITTER_API_KEY` (if using Twitter API)
- Add others as needed

## Local Development

```bash
pip install -r requirements.txt
python scripts/fetch_briefing.py
```
