import pandas as pd
import re
import spacy
from transformers import pipeline
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent 
INPUT_PATH = PROJECT_ROOT / "data/news_data.csv"
OUTPUT_PATH = PROJECT_ROOT / "data/news_sentiment.csv"


nlp = spacy.load("en_core_web_sm")


sentiment_pipeline = pipeline(
    "sentiment-analysis", model="yiyanghkust/finbert-tone", tokenizer="yiyanghkust/finbert-tone"
)


def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r"http\S+|www.\S+", "", text)  
    text = re.sub(r"[^A-Za-z\s]", "", text)  
    text = text.lower().strip()
    doc = nlp(text)
    cleaned = " ".join([token.lemma_ for token in doc if not token.is_stop])
    return cleaned


def analyze_sentiment(text):
    if not text or len(text.strip()) < 5:
        return "neutral"
    result = sentiment_pipeline(text[:512])[0] 
    return result["label"].lower()


def run_nlp_pipeline():
   
    if not INPUT_PATH.exists():
        print(f"❌ ERROR: {INPUT_PATH} does not exist. Make sure news_data.csv exists in data/")
        return

    df = pd.read_csv(INPUT_PATH)
    print(f"🧠 Loaded {len(df)} articles from {INPUT_PATH}")

  
    df["cleaned_text"] = df["title"].fillna("") + " " + df["description"].fillna("")
    df["cleaned_text"] = df["cleaned_text"].apply(clean_text)

  
    print("\nSample cleaned text:")
    print(df["cleaned_text"].head(5))

  
    print("\n🔍 Running sentiment analysis...")
    df["sentiment"] = df["cleaned_text"].apply(analyze_sentiment)

    
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\n✅ NLP analysis complete! Results saved to {OUTPUT_PATH}")

   
    print("\nSentiment distribution:")
    print(df["sentiment"].value_counts())

if __name__ == "__main__":
    run_nlp_pipeline()     

