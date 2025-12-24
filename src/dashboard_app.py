import streamlit as st
from newsapi import NewsApiClient
from transformers import pipeline
import pandas as pd
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("NEWS_API_KEY")

if not api_key:
    st.error("❌ NEWS_API_KEY not found. Please add it to your .env file.")
    st.stop()

newsapi = NewsApiClient(api_key=api_key)


@st.cache_resource
def load_sentiment_model():
    return pipeline(
    "sentiment-analysis",
    model="yiyanghkust/finbert-tone",
    tokenizer="yiyanghkust/finbert-tone"
)


sentiment_analyzer = load_sentiment_model()


st.title("📰 Smart News Intelligence Dashboard")
st.markdown("Real-time NLP-powered insights from live news data.")

search_term = st.text_input("🔍 Enter any company or topic", "Tesla")

if st.button("Fetch News") or search_term:
    st.subheader(f"Live NLP-powered insights for: {search_term}")
    with st.spinner("Fetching and analyzing live news..."):
        try:
         
            articles = newsapi.get_everything(
                q=search_term,
                language="en",
                sort_by="publishedAt",
                page_size=15,
                domains="bbc.co.uk,techcrunch.com,cnn.com,reuters.com,nytimes.com,bloomberg.com"
            )["articles"]

           
            if not articles:
                articles = newsapi.get_top_headlines(
                    q=search_term,
                    language="en",
                    page_size=15
                )["articles"]

            if not articles:
                st.warning("No articles found for this search term. Try another company or topic.")
            else:
                titles = [a["title"] for a in articles if a["title"]]
                contents = [a["description"] or "" for a in articles]

                df = pd.DataFrame({"title": titles, "content": contents})

               
                st.info("Analyzing sentiment for fetched articles...")
                sentiments = sentiment_analyzer(titles)
                df["sentiment"] = [s["label"] for s in sentiments]
                df["score"] = [s["score"] for s in sentiments]

        
                st.success(f"✅ Found {len(df)} articles for '{search_term}'")
                st.dataframe(df[["title", "sentiment", "score"]])

              
                summary = df["sentiment"].value_counts().to_dict()
                st.write("### 🧠 Sentiment Breakdown")
                st.bar_chart(pd.DataFrame.from_dict(summary, orient="index"))

        except Exception as e:
            st.error(f"Error fetching data: {e}")
