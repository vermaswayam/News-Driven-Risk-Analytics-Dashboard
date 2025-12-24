import os
from dotenv import load_dotenv

import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent  # project root
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)        # ensure folder exists

OUTPUT_PATH = DATA_DIR / "news_data.csv"


API_KEY = os.getenv("NEWS_API_KEY")
if not API_KEY:
    raise RuntimeError("NEWS_API_KEY not set. Please add it to your .env file.")

COMPANY = "Tesla" 



def fetch_news(query=COMPANY, page_size=20):
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&language=en&sortBy=publishedAt&pageSize={page_size}&apiKey={API_KEY}"
    )
    response = requests.get(url, timeout=15)

    data = response.json()

    if data["status"] != "ok":
        raise Exception("Error fetching news: ", data)

    articles = data["articles"]
    df = pd.DataFrame(
        [
            {
                "source": a["source"]["name"],
                "title": a["title"],
                "description": a["description"],
                "url": a["url"],
                "publishedAt": a["publishedAt"],
                "content": a["content"],
                "fetched_at":  datetime.utcnow(),
            }
            for a in articles
        ]
    )

    return df



if __name__ == "__main__":
    print(f"🔍 Fetching latest news for: {COMPANY}")
    df = fetch_news(COMPANY)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Saved {len(df)} articles to {OUTPUT_PATH}")

