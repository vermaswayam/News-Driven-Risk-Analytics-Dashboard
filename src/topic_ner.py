from bertopic import BERTopic
import pandas as pd


df = pd.read_csv("../data/news_sentiment.csv")
texts = df["cleaned_text"].tolist()


topic_model = BERTopic(language="english")
topics, probs = topic_model.fit_transform(texts)

df["topic"] = topics


print(df[["cleaned_text", "topic"]].head())
df.to_csv("../data/news_topics.csv", index=False)

import spacy

nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]


df["entities"] = df["cleaned_text"].apply(extract_entities)


print(df[["cleaned_text", "entities"]].head())
df.to_csv("../data/news_topics_entities.csv", index=False)
