#!/usr/bin/env python3
"""
Briefomatic - Fetch and compile briefing data from various sources.

Data Sources:
- Perplexity Sonar: Real-time web search for news (macro, stocks, gaming, tech, AI)
- Hacker News: Tech/AI/Nerd community signal (free, no key)
- CoinGecko: Crypto prices and trends (free, no key)
- Venice AI: Summarization and filtering
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import requests


# =============================================================================
# DATA SOURCE: Perplexity Sonar (Real-time web search)
# =============================================================================

def fetch_perplexity_news(
    api_key: str,
    query: str,
    category: str,
    recency: str = "day",
    model: str = "sonar"
) -> dict:
    """
    Fetch news using Perplexity Sonar's real-time web search.

    Args:
        api_key: Perplexity API key
        query: The search query / question
        category: Category label for the briefing
        recency: Time filter - 'hour', 'day', 'week', 'month'
        model: 'sonar' (faster/cheaper) or 'sonar-pro' (more thorough)
    """
    try:
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        system_prompt = """You are a news research assistant. Provide factual, current information based on your web search.
Format your response as a JSON array of news items. Each item should have:
- "title": Brief headline
- "summary": 1-2 sentence summary
- "source": Publication name
- "url": Source URL if available

Return ONLY valid JSON array, no other text. Example:
[{"title": "...", "summary": "...", "source": "...", "url": "..."}]

If no relevant news found, return empty array: []"""

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            "max_tokens": 2000,
            "temperature": 0.1,
            "search_recency_filter": recency
        }

        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        content = data.get("choices", [{}])[0].get("message", {}).get("content", "[]")

        # Parse the JSON response
        try:
            # Clean up the response - sometimes wrapped in markdown code blocks
            content = content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            items = json.loads(content)
        except json.JSONDecodeError:
            items = [{"title": "Raw response", "summary": content[:500], "source": "perplexity", "url": ""}]

        # Get citations if available
        citations = data.get("citations", [])

        return {
            "source": "perplexity",
            "category": category,
            "query": query,
            "recency_filter": recency,
            "count": len(items) if isinstance(items, list) else 1,
            "items": items if isinstance(items, list) else [items],
            "citations": citations
        }

    except Exception as e:
        return {"source": "perplexity", "category": category, "error": str(e), "items": []}


# =============================================================================
# DATA SOURCE: Hacker News (Free, no API key needed)
# =============================================================================

def fetch_hackernews(limit: int = 30) -> dict:
    """
    Fetch top stories from Hacker News.
    Great for tech, AI, and nerd news.
    """
    try:
        # Get top story IDs
        top_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(top_url, timeout=10)
        response.raise_for_status()
        story_ids = response.json()[:limit]

        items = []
        for story_id in story_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_resp = requests.get(story_url, timeout=5)
            if story_resp.status_code == 200:
                story = story_resp.json()
                if story and story.get("title"):
                    items.append({
                        "title": story.get("title", ""),
                        "url": story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                        "score": story.get("score", 0),
                        "comments": story.get("descendants", 0),
                    })

        return {
            "source": "hackernews",
            "category": "tech_ai_nerd",
            "count": len(items),
            "items": items
        }
    except Exception as e:
        return {"source": "hackernews", "error": str(e), "items": []}


# =============================================================================
# DATA SOURCE: CoinGecko (Free, no API key needed for basic)
# =============================================================================

def fetch_crypto_prices(coins: list = None) -> dict:
    """
    Fetch crypto prices and 24h changes from CoinGecko.
    """
    if coins is None:
        coins = ["bitcoin", "ethereum", "solana", "cardano", "dogecoin"]

    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "ids": ",".join(coins),
            "order": "market_cap_desc",
            "sparkline": "false",
            "price_change_percentage": "24h,7d"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        items = []
        for coin in data:
            items.append({
                "name": coin.get("name"),
                "symbol": coin.get("symbol", "").upper(),
                "price": coin.get("current_price"),
                "change_24h": round(coin.get("price_change_percentage_24h", 0), 2),
                "change_7d": round(coin.get("price_change_percentage_7d_in_currency", 0) or 0, 2),
                "market_cap": coin.get("market_cap"),
            })

        return {
            "source": "coingecko",
            "category": "crypto",
            "count": len(items),
            "items": items
        }
    except Exception as e:
        return {"source": "coingecko", "error": str(e), "items": []}


def fetch_crypto_trending() -> dict:
    """
    Fetch trending coins from CoinGecko.
    """
    try:
        url = "https://api.coingecko.com/api/v3/search/trending"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        items = []
        for coin in data.get("coins", [])[:10]:
            item = coin.get("item", {})
            items.append({
                "name": item.get("name"),
                "symbol": item.get("symbol"),
                "market_cap_rank": item.get("market_cap_rank"),
            })

        return {
            "source": "coingecko_trending",
            "category": "crypto",
            "count": len(items),
            "items": items
        }
    except Exception as e:
        return {"source": "coingecko_trending", "error": str(e), "items": []}


# =============================================================================
# VENICE AI SUMMARIZATION
# =============================================================================

def summarize_with_venice(api_key: str, content: dict, model: str = "llama-3.3-70b") -> Optional[str]:
    """
    Use Venice AI to summarize and filter the briefing content.
    Venice uses OpenAI-compatible API format.
    """
    try:
        url = "https://api.venice.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Build the prompt
        prompt = f"""You are an AI briefing assistant. Analyze the following raw news and market data, then create a concise executive briefing.

Structure your response as follows:
1. **Market Overview** - Key macro/stock/crypto movements and sentiment
2. **Tech & AI** - Most important tech and AI developments
3. **Gaming & Entertainment** - Notable gaming news if any
4. **Key Insights** - 3-5 bullet points of actionable insights or notable trends
5. **Watch List** - Items to monitor in coming days

Be concise, factual, and highlight only the most significant items. Skip anything that seems like noise or clickbait.

RAW DATA:
{json.dumps(content, indent=2)[:15000]}
"""

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a professional market and tech analyst creating daily briefings for busy professionals."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000,
            "temperature": 0.3
        }

        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        return data.get("choices", [{}])[0].get("message", {}).get("content", "")

    except Exception as e:
        return f"Error generating summary: {str(e)}"


# =============================================================================
# MAIN BRIEFING COMPILER
# =============================================================================

def compile_briefing() -> dict:
    """
    Compile all data sources into a single briefing.
    """
    now = datetime.now(timezone.utc)

    briefing = {
        "generated_at": now.isoformat(),
        "generated_at_human": now.strftime("%Y-%m-%d %H:%M UTC"),
        "raw_data": {},
        "summary": None
    }

    # Get API keys from environment
    perplexity_key = os.environ.get("PERPLEXITY_API_KEY")
    venice_key = os.environ.get("VENICE_API_KEY")

    # ==========================================================================
    # FETCH RAW DATA
    # ==========================================================================

    # Free sources (no API key needed)
    print("Fetching Hacker News...")
    briefing["raw_data"]["hackernews"] = fetch_hackernews(limit=25)

    print("Fetching crypto prices...")
    briefing["raw_data"]["crypto_prices"] = fetch_crypto_prices()

    print("Fetching trending crypto...")
    briefing["raw_data"]["crypto_trending"] = fetch_crypto_trending()

    # Perplexity-powered news searches
    if perplexity_key:
        print("Fetching macro/market news via Perplexity...")
        briefing["raw_data"]["macro_markets"] = fetch_perplexity_news(
            perplexity_key,
            query="What are the most important macroeconomic and stock market news and developments from the past 24 hours? Include major index movements, Fed/central bank news, and significant company earnings or announcements.",
            category="macro_stocks",
            recency="day"
        )

        print("Fetching crypto news via Perplexity...")
        briefing["raw_data"]["crypto_news"] = fetch_perplexity_news(
            perplexity_key,
            query="What are the most significant cryptocurrency and blockchain news from the past 24 hours? Include major price movements, regulatory news, and notable project developments.",
            category="crypto_news",
            recency="day"
        )

        print("Fetching AI news via Perplexity...")
        briefing["raw_data"]["ai_news"] = fetch_perplexity_news(
            perplexity_key,
            query="What are the most important artificial intelligence and machine learning news and developments from the past 24 hours? Include new model releases, company announcements, research breakthroughs, and industry trends.",
            category="ai",
            recency="day"
        )

        print("Fetching gaming news via Perplexity...")
        briefing["raw_data"]["gaming"] = fetch_perplexity_news(
            perplexity_key,
            query="What are the most notable video game and gaming industry news from the past 24 hours? Include game releases, announcements, esports, and industry developments.",
            category="gaming",
            recency="day"
        )

        print("Fetching tech news via Perplexity...")
        briefing["raw_data"]["tech_news"] = fetch_perplexity_news(
            perplexity_key,
            query="What are the most important technology news and developments from the past 24 hours? Include major product launches, company news, and significant tech industry developments. Exclude AI-specific news.",
            category="tech",
            recency="day"
        )
    else:
        print("Skipping Perplexity news (no API key)")

    # ==========================================================================
    # GENERATE AI SUMMARY
    # ==========================================================================

    if venice_key:
        print("Generating summary with Venice AI...")
        briefing["summary"] = summarize_with_venice(venice_key, briefing["raw_data"])
    else:
        print("Skipping Venice AI summary (no API key)")
        briefing["summary"] = "No summary generated - VENICE_API_KEY not set"

    return briefing


def main():
    # Compile the briefing
    briefing = compile_briefing()

    # Ensure output directory exists
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    # Write JSON output
    output_file = output_dir / "briefing.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(briefing, f, indent=2, ensure_ascii=False)

    print(f"\nBriefing generated: {output_file}")
    print(f"Timestamp: {briefing['generated_at_human']}")
    print(f"Sections: {list(briefing['raw_data'].keys())}")

    # Also write a markdown version for easy reading
    if briefing.get("summary"):
        md_file = output_dir / "briefing.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(f"# Daily Briefing\n\n")
            f.write(f"*Generated: {briefing['generated_at_human']}*\n\n")
            f.write(briefing["summary"])
        print(f"Markdown version: {md_file}")


if __name__ == "__main__":
    main()
