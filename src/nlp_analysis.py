import pandas as pd
import re
import spacy
from transformers import pipeline
from pathlib import Path

# File paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = PROJECT_ROOT / "data/news_data.csv"
OUTPUT_PATH = PROJECT_ROOT / "data/news_sentiment.csv"

# Load spaCy model for text cleaning
nlp = spacy.load("en_core_web_sm")


# Load FinBERT sentiment model
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="yiyanghkust/finbert-tone",
    tokenizer="yiyanghkust/finbert-tone"
)


# Text cleaning function
def clean_text(text):
    if not isinstance(text, str):
        return ""

    # remove URLs
    text = re.sub(r"http\S+|www.\S+", "", text)

    # keep only letters and spaces (simple & explainable)
    text = re.sub(r"[^A-Za-z\s]", "", text)

    text = text.lower().strip()

    # lemmatization + stopword removal
    doc = nlp(text)
    cleaned = " ".join(
        token.lemma_ for token in doc if not token.is_stop
    )

    return cleaned


# Sentiment analysis function
def analyze_sentiment(text):
    if not text or len(text.strip()) < 5:
        return "neutral", 0.0

    result = sentiment_pipeline(text[:512])[0]
    return result["label"].lower(), float(result["score"])


#  NLP pipeline
def run_nlp_pipeline():
    if not INPUT_PATH.exists():
        print(f"❌ ERROR: {INPUT_PATH} does not exist.")
        return

    df = pd.read_csv(INPUT_PATH)
    print(f"🧠 Loaded {len(df)} articles from {INPUT_PATH}")

    # Combine title + description
    df["cleaned_text"] = (
        df["title"].fillna("") + " " + df["description"].fillna("")
    )

    # Clean text
    df["cleaned_text"] = df["cleaned_text"].apply(clean_text)

    print("\nSample cleaned text:")
    print(df["cleaned_text"].head())

    # Run sentiment analysis
    print("\n🔍 Running sentiment analysis (FinBERT)...")
    df[["sentiment", "sentiment_score"]] = df["cleaned_text"].apply(
        lambda x: pd.Series(analyze_sentiment(x))
    )

    # Save results
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\n✅ NLP analysis complete! Results saved to {OUTPUT_PATH}")

    print("\nSentiment distribution:")
    print(df["sentiment"].value_counts())


# Run script
if __name__ == "__main__":
    run_nlp_pipeline()
   

