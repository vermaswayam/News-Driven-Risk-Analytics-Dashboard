<<<<<<< HEAD
# News-Driven-Risk-Analytics-Dashboard
A real-time financial news analytics system that combines Natural Language Processing (NLP) and data visualization to assess how media sentiment impacts market risk. The project automates an end-to-end datapipeline — from live news ingestion to sentiment analysis and dashboard reporting — mirroring workflows used in risk management and traded-risk model monitoring.
=======

The initial sentiment analysis in this project uses a general-purpose sentiment model (trained on movie reviews, social media posts, etc.).
Such models are not optimized for financial or business news, which often contains:

Neutral or technical language

Market terms (“IPO”, “investment”, “funding”, “valuation”)

Headlines without emotional wording

Because of this mismatch, the model sometimes mislabels positive financial headlines as negative, even when a human would interpret them as clearly positive.
This is a known limitation in NLP: general sentiment models underperform on financial text and tend to bias toward negative classifications in news contexts.

Solution Summary

To resolve this, the project switches to a finance-specific sentiment model, such as FinBERT, which is trained on real financial news and analyst reports.
FinBERT correctly interprets headlines like:

“Meesho’s $606M IPO pops as enthusiasm rises” → positive

because it understands the financial meaning behind market-related terms.
This results in far more accurate sentiment outputs for business and stock-related news.
>>>>>>> e12581e (Initial commit: Smart News Intelligence project)
