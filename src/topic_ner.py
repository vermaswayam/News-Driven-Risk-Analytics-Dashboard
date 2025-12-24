from bertopic import BERTopic
import pandas as pd
import spacy
from pathlib import Path

# File paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = PROJECT_ROOT / "data/news_sentiment.csv"
OUTPUT_TOPIC_PATH = PROJECT_ROOT / "data/news_topics.csv"
OUTPUT_ENTITY_PATH = PROJECT_ROOT / "data/news_topics_entities.csv"


# Main function
def run_topic_and_ner_pipeline():

    if not INPUT_PATH.exists():
        print(f"❌ ERROR: {INPUT_PATH} not found.")
        return

    # Load data
    df = pd.read_csv(INPUT_PATH)
    texts = df["cleaned_text"].fillna("").tolist()


    # Topic Modeling (BERTopic)
    print("🔍 Running topic modeling...")
    topic_model = BERTopic(language="english")
    topics, probs = topic_model.fit_transform(texts)

    df["topic"] = topics
    df.to_csv(OUTPUT_TOPIC_PATH, index=False)

    print("\nSample topics:")
    print(df[["cleaned_text", "topic"]].head())

    # Named Entity Recognition
    print("\n🔍 Extracting named entities...")
    nlp = spacy.load("en_core_web_sm")

    def extract_entities(text):
        doc = nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]

    df["entities"] = df["cleaned_text"].apply(extract_entities)
    df.to_csv(OUTPUT_ENTITY_PATH, index=False)

    print("\nSample entities:")
    print(df[["cleaned_text", "entities"]].head())

    print("\n✅ Topic modeling and NER completed successfully.")


# Run script
if __name__ == "__main__":
    run_topic_and_ner_pipeline()

