#!/usr/bin/env python3
"""
Local runner for Briefomatic.
Loads .env file and runs the briefing script.
"""

import os
import sys
from pathlib import Path

def load_env():
    """Load environment variables from .env file."""
    env_file = Path(__file__).parent / ".env"

    if not env_file.exists():
        print("ERROR: .env file not found!")
        print("Create one by copying .env.example:")
        print("  cp .env.example .env")
        print("Then edit .env and add your API keys.")
        sys.exit(1)

    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()

    # Verify required keys
    missing = []
    if not os.environ.get("PERPLEXITY_API_KEY"):
        missing.append("PERPLEXITY_API_KEY")
    if not os.environ.get("VENICE_API_KEY"):
        missing.append("VENICE_API_KEY")

    if missing:
        print(f"ERROR: Missing API keys in .env: {', '.join(missing)}")
        sys.exit(1)

    print("Environment loaded from .env")

if __name__ == "__main__":
    load_env()

    # Import and run the main script
    from scripts.fetch_briefing import main
    main()
