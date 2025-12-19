#!/usr/bin/env python3
"""
Briefomatic - Fetch and compile briefing data from various sources.

Add your data sources below. Each source should return a dict that gets
merged into the final briefing.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

# Optional imports - uncomment as needed
# import requests


def fetch_placeholder_data() -> dict:
    """
    Placeholder data source - replace with your actual API calls.
    """
    return {
        "source": "placeholder",
        "message": "Replace this with real data sources",
        "items": [
            {"title": "Example item 1", "summary": "This is placeholder content"},
            {"title": "Example item 2", "summary": "Add your API integrations"},
        ]
    }


# def fetch_news(api_key: str) -> dict:
#     """
#     Example: Fetch news from NewsAPI.
#     """
#     url = "https://newsapi.org/v2/top-headlines"
#     params = {
#         "apiKey": api_key,
#         "country": "us",
#         "pageSize": 10
#     }
#     response = requests.get(url, params=params)
#     response.raise_for_status()
#     data = response.json()
#
#     return {
#         "source": "newsapi",
#         "items": [
#             {"title": article["title"], "summary": article.get("description", "")}
#             for article in data.get("articles", [])
#         ]
#     }


# def fetch_weather(location: str) -> dict:
#     """
#     Example: Fetch weather data.
#     """
#     # Add your weather API integration
#     pass


# def fetch_twitter_trends(api_key: str) -> dict:
#     """
#     Example: Fetch Twitter/X trends or mentions.
#     """
#     # Add your Twitter API integration
#     pass


def compile_briefing() -> dict:
    """
    Compile all data sources into a single briefing.
    """
    now = datetime.now(timezone.utc)

    briefing = {
        "generated_at": now.isoformat(),
        "generated_at_human": now.strftime("%Y-%m-%d %H:%M UTC"),
        "sections": {}
    }

    # Add your data sources here
    # Each source gets its own section in the briefing

    # Placeholder - remove once you add real sources
    briefing["sections"]["placeholder"] = fetch_placeholder_data()

    # Example: News
    # if os.environ.get("NEWS_API_KEY"):
    #     briefing["sections"]["news"] = fetch_news(os.environ["NEWS_API_KEY"])

    # Example: Weather
    # briefing["sections"]["weather"] = fetch_weather("New York")

    # Example: Twitter
    # if os.environ.get("TWITTER_API_KEY"):
    #     briefing["sections"]["twitter"] = fetch_twitter_trends(os.environ["TWITTER_API_KEY"])

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

    print(f"Briefing generated: {output_file}")
    print(f"Timestamp: {briefing['generated_at_human']}")
    print(f"Sections: {list(briefing['sections'].keys())}")


if __name__ == "__main__":
    main()
